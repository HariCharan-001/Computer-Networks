# NAME: Hari Charan Korrapati
# Roll Number: CS20B086
# Course: CS3205 Jan. 2023 semester
# Lab number: 5
# Date of submission:= 29/04/2023
# I confirm that the source file is entirely written by me without resorting to any dishonest means.
# Website(s) that I used for basic socket programming code are:

import sys
import socket
import time
import threading
import random
from queue import PriorityQueue

class Router:
    id = 0
    infile = 'input.txt'
    outfile_name = 'output'
    hello = 1
    lsa = 5
    spf = 20
    links = []
    addr = ('localhost', 10000 + id)
    neighbours = {}
    UDP_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    seq_no = 0
    routing_table = {}
    maxx = 100000
    time = 0

    def __init__(self):
        for i in range(1, len(sys.argv)):
            if sys.argv[i] == '-i':
                self.id = int(sys.argv[i+1])
                self.outfile_name = 'output-' + str(self.id) + '.txt'
                self.addr = ('localhost', 10000 + self.id)
                self.UDP_sock.bind(self.addr)

            elif sys.argv[i] == '-f':
                self.infile = sys.argv[i+1]
            
            elif sys.argv[i] == '-o':
                self.outfile_name = sys.argv[i+1] + '-' + str(self.id) + '.txt'
            
            elif sys.argv[i] == '-h':
                self.hello = int(sys.argv[i+1])

            elif sys.argv[i] == '-a':
                self.lsa = int(sys.argv[i+1])
            
            elif sys.argv[i] == '-s':
                self.spf = int(sys.argv[i+1])


        self.infile = open(str(self.infile), 'r')
        self.N, self.M = [int(i) for i in self.infile.readline().strip().split()]

        self.links = [[] for i in range(self.N)]
        self.cost = [[ self.maxx  for i in range(self.N)] for j in range(self.N)]
        for i in range(self.N):
            self.cost[i][i] = 0

        self.exp_seq = [0 for i in range(self.N)]
        self.routing_table = [['', self.maxx] for i in range(self.N)]

        for i in range(self.M):
            x,y, minc, maxc = [int(i) for i in self.infile.readline().strip().split()]

            self.links[x].append(y)
            self.links[y].append(x)

            if(y == self.id): 
                self.neighbours[x] = [('localhost', 10000 + x), minc, maxc]
            elif(x == self.id):
                self.neighbours[y] = [('localhost', 10000 + y), minc, maxc]

    def send_HELLO(self):
        while(True):
            time.sleep(self.hello)
            for x in self.neighbours:
                self.UDP_sock.sendto(('HELLO ' + str(self.id)).encode(), self.neighbours[x][0])

    def send_LSA(self):
        while(True):
            time.sleep(self.lsa) 
            lsa_packet = f'LSA {self.id} {self.seq_no} {str(len(self.neighbours))}'

            for x in self.neighbours:
                lsa_packet += f' {x} {self.cost[self.id][x]}'

            for x in self.neighbours:
                self.UDP_sock.sendto(lsa_packet.encode(), self.neighbours[x][0])
            
            self.seq_no += 1

    def Dijkstra(self):
        pq = PriorityQueue()
        pq.put((0, self.id))
        visited = [False for i in range(self.N)]

        path = ['' for i in range(self.N)]
        path[self.id] = str(self.id)

        dis = [self.maxx for i in range(self.N)]
        dis[self.id] = 0

        while not pq.empty():
            _, node = pq.get()
            visited[node] = True
            
            for x in self.links[node]:
                if not visited[x]:
                    if(dis[x] > dis[node] + self.cost[node][x]):
                        dis[x] = dis[node] + self.cost[node][x]
                        pq.put((dis[x], x))
                        path[x] = path[node] + '-' + str(x)
                
        self.routing_table = [[path[i], dis[i]] for i in range(self.N)]

    def compute_SPF(self):
        # open the output file
        self.outfile = open(str(self.outfile_name), 'w')
        self.outfile.write('Router ' + str(self.id) + '\n\n')
        self.outfile.close()

        while True:
            time.sleep(self.spf)
            self.time += self.spf

            self.Dijkstra()

            # write the routing table to output file
            self.outfile = open(str(self.outfile_name), 'a')
            self.outfile.write('Routing Table at Time ' + str(self.time) + '\n')
            self.outfile.write('Destination        Path            Cost\n')
            for i in range(self.N):
                self.outfile.write(str(i) + '    ' + self.routing_table[i][0] + '    ' + str(self.routing_table[i][1]) + '\n')
            
            self.outfile.write('\n')
            self.outfile.close()

    def recieve_thread(self):
        while True:
            message, addr = self.UDP_sock.recvfrom(10240)
            message = message.decode().split()
            sender_id = addr[1] - 10000

            if(message[0] == 'HELLO'):
                radom_weight = random.randint(self.neighbours[sender_id][1], self.neighbours[sender_id][2])
                self.UDP_sock.sendto(('HELLOREPLY ' + str(self.id) + ' ' + str(sender_id) + ' '  + str(radom_weight)).encode(), addr)

            elif(message[0] == 'HELLOREPLY'):
                self.cost[self.id][sender_id] = int(message[3])
                self.cost[sender_id][self.id] = int(message[3])

            elif(message[0] == 'LSA'):
                sender_id = int(message[1])
                if(sender_id == self.id):
                    continue

                seq_no = int(message[2])
                if(seq_no < self.exp_seq[sender_id]):
                    continue

                self.exp_seq[sender_id] += 1
                len = int(message[3])
                
                # udate the costs for each link in the LSA
                for i in range(4, len*2 + 4, 2):
                    self.cost[sender_id][int(message[i])] = int(message[i+1])
                    self.cost[int(message[i])][sender_id] = int(message[i+1])
                
                # forward LSA to its neighbours except the sender
                for x in self.neighbours:
                    if(x != sender_id):
                        self.UDP_sock.sendto(' '.join(message).encode(), (self.neighbours[x][0]))

router = Router()
hello_thread = threading.Thread(target=router.send_HELLO)
lsa_thread = threading.Thread(target=router.send_LSA)
spf_thread = threading.Thread(target=router.compute_SPF)
recieve_thread = threading.Thread(target=router.recieve_thread)

hello_thread.start()
lsa_thread.start()
spf_thread.start()
recieve_thread.start()