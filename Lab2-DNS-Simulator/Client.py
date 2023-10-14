import socket
import sys
import os
import time

startportnum = int(sys.argv[1])
input_file = open(sys.argv[2], "r")

def read_servers():
    #BEGIN_DATA line
    line = input_file.readline().strip()

    #local DNS Server
    global name_resolver
    name_resolver = input_file.readline().strip() + ' ' + str(startportnum + 53)

    #Root DNS server
    global root
    root = input_file.readline().strip()  + ' ' + str(startportnum + 54) + ' ' + 'RDS.output'

    #TLD DNS Servers
    tld1 = input_file.readline().strip() + ' ' + str(startportnum + 55) + ' ' + 'TDS1.output'
    tld2 = input_file.readline().strip()  + ' ' + str(startportnum + 56) + ' ' + 'TDS2.output'

    #Authoritative DNS Servers
    auth = []
    auth.append(input_file.readline().strip() + ' ' + str(startportnum + 57) + ' ' + 'ADS1.output')
    auth.append(input_file.readline().strip() + ' ' + str(startportnum + 58) + ' ' + 'ADS2.output')
    auth.append(input_file.readline().strip() + ' ' + str(startportnum + 59) + ' ' + 'ADS3.output')
    auth.append(input_file.readline().strip() + ' ' + str(startportnum + 60) + ' ' + 'ADS4.output')
    auth.append(input_file.readline().strip() + ' ' + str(startportnum + 61) + ' ' + 'ADS5.output')
    auth.append(input_file.readline().strip() + ' ' + str(startportnum + 62) + ' ' + 'ADS6.output')

    #appending TLD ip addresses as records in root server
    root += ' ' + tld1 + ' ' + tld2

    #appending hostname ip addresses as recods in Authoritative servers
    line = input_file.readline().split()
    i = -1
    first = 1
    while(line[0] != 'END_DATA'):
        while(len(line) == 2):
            if(first):
                auth_name = '.'.join(line[0].split('.')[1:])
                auth[i] = auth_name + ' ' + ' '.join((auth[i].split())[1:])
            auth[i] += ' ' + line[0] + ' ' + line[1] + ' ' + str(0) + ' ' + 'junk_file.txt'
            line = input_file.readline().split()

        i += 1
        line = input_file.readline().split()
        first = 1

    #appending Authoritative ip addresses as records in TLD servers
    tld1 += ' ' + ' '.join(auth[0].split()[0:4])
    tld1 += ' ' + ' '.join(auth[1].split()[0:4])
    tld1 += ' ' + ' '.join(auth[2].split()[0:4])

    tld2 += ' ' + ' '.join(auth[3].split()[0:4])
    tld2 += ' ' + ' '.join(auth[4].split()[0:4])
    tld2 += ' ' + ' '.join(auth[5].split()[0:4])
    
    global all_servers
    all_servers = [root, tld1, tld2]
    all_servers.extend(auth)

read_servers()

pid = os.fork()
if pid == 0:
    os.system("python3 Local_DNS_Server.py " + name_resolver + ' ' + root.split()[1] + ' ' + str(startportnum+54))
    sys.exit(0)

for i in range(9):
    pid = os.fork()
    if pid == 0:
        os.system("python3 server_process.py " + all_servers[i])
        sys.exit(0)

time.sleep(5)
print('All Server Processes are up and running.')

UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

while(True):
    host_name = input("Enter Server Name: ")

    if(host_name == 'bye'):
        for portno in range(startportnum + 53, startportnum + 63):
            UDPClientSocket.sendto('bye'.encode(), (name_resolver.split()[1], portno))
        print('All Server Processes are killed. Exiting.\n')

        break

    UDPClientSocket.sendto(host_name.encode(), (name_resolver.split()[1], int(startportnum + 53)))
    msg_from_NR = UDPClientSocket.recvfrom(2048)[0].decode()

    print("DNS Mapping:", msg_from_NR)