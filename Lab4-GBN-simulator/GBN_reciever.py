# NAME: Hari Charan Korrapati
# Roll Number: CS20B086
# Course: CS3205 Jan. 2023 semester
# Lab number: 4
# Date of submission: 05-04-2023
# I confirm that the source file is entirely written by me without
# resorting to any dishonest means.
# Website(s) that I used for basic socket programming code are:
# URL(s): 

import sys
import socket
import time
import random

random.seed(time.time())

debug_mode = 0
port  = 0
n = 0
error_rate = 0 
NFE = 0
total_received = 0
rotations = 0

i = 1
while i < len(sys.argv):
    if sys.argv[i] == '-d':
        debug_mode = 1
        i += 1

    elif sys.argv[i] == '-p':
        port = int(sys.argv[i+1])
        i += 2

    elif sys.argv[i] == '-n':
        n = int(sys.argv[i+1])
        i += 2
    
    elif sys.argv[i] == '-e':
        error_rate = float(sys.argv[i+1])
        i += 2

drop_pkt_cnt = int(1/ error_rate)

#create UDP server socket
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverSocket.bind(('localhost', port))

print('Reciever up and running on port: ' + str(port))

while(True):
    #receive message from client
    message, address = serverSocket.recvfrom(1024)
    message = message.decode()
    seq_no = ord(message[0])
    drop_cur = False
    
    #drop packet randomly 
    if random.randint(1, drop_pkt_cnt) == 1:
        drop_cur = True

    #if NFE does not match the seq_no
    if NFE != int(seq_no):
        drop_cur = True

    if debug_mode == 1:
        cur = time.time()
        print('Seq #:', seq_no, 'Time recieved:', int(cur*1000), ':', int(cur*1e6) % 1000, ' Packet dropped:', drop_cur)
    
    if drop_cur == True:
        continue

    #send ACK
    serverSocket.sendto(str(seq_no + 256*rotations).encode(), address)

    #increment NFE and total packets recieved
    NFE = (NFE + 1)% 256
    if(NFE == 0):
        rotations += 1
    total_received += 1

    #check if all packets received
    if total_received == n:
        print('\nRecieved ' + str(n) + ' packets successfully, terminating reciever')
        break