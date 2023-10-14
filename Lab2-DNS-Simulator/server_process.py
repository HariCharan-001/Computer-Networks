import sys
import socket
import signal

def sigterm_handler(_signo, _stack_frame):
    print("Server shutting down")
    sys.exit(0)

signal.signal(signal.SIGTERM, sigterm_handler)

server_name = sys.argv[1]
ip_add = sys.argv[2]
port = int(sys.argv[3])
output_file = open(sys.argv[4], 'w')
data = sys.argv[5:]
records = {}

def construct_records():
    n = len(data)
    for i in range(0, n, 4):
        records[data[i]] = data[i+1] + ' ' + data[i+2]

    for key in records:
        output_file.write(key + ' ' + records[key] + '\n')
    
    output_file.write('\n')

def root(host_name):
    tld = host_name.split('.')[-1]
    return records['TDS_' + tld]

def TLD(host_name):
    authoritative = '.'.join(host_name.split('.')[1:])
    return records[authoritative]

def Authoritative(host_name):
    return records[host_name]

bufferSize = 2048

UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPServerSocket.bind((ip_add, port))

output_file.write(server_name + " server up and listening on ip address: " + ip_add +  " port: " + str(port) + '\n')
output_file.write("Server has the following records\n")
construct_records()

while(True):
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    host_name = bytesAddressPair[0].decode()
    clientIP = bytesAddressPair[1]

    if(host_name == 'bye'):
        output_file.write(server_name + " Server shutting down\n")
        break

    output_file.write('\n' + server_name + '\n')
    output_file.write("Client IP address: " + str(clientIP) + '\n')
    output_file.write("msg recieved from client: " + host_name + '\n')

    try:
        if(server_name == "RDS"):
            UDPServerSocket.sendto(root(host_name).encode(), clientIP)
            output_file.write("msg sent to client: " + root(host_name) + '\n\n')

        elif(server_name.startswith('TDS')):
            UDPServerSocket.sendto(TLD(host_name).encode(), clientIP)
            output_file.write("msg sent to client: " + TLD(host_name) + '\n\n')
        
        else:
            UDPServerSocket.sendto(Authoritative(host_name).encode(), clientIP)
            output_file.write("msg sent to client: " + Authoritative(host_name) + '\n\n')

        continue

    except:
        output_file.write("msg sent to client: No such host exists\n")
        UDPServerSocket.sendto('No such host exists'.encode(), clientIP)