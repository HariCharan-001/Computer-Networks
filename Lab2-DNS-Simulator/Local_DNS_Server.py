import sys
import socket
import signal

def sigterm_handler(_signo, _stack_frame):
    print("Local DNS shutting down")
    sys.exit(0)

signal.signal(signal.SIGTERM, sigterm_handler)

server_name = sys.argv[1]
ip_add = sys.argv[2]
port = int(sys.argv[3])
root_ip = (sys.argv[4], int(sys.argv[5]))
output_file = open('NR.output', 'w')

bufferSize = 2048

UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPServerSocket.bind((ip_add, port))

output_file.write(server_name + " server up and listening on ip address: " + ip_add + " and port: " + str(port) + '\n\n')

while(True):
    try:
        Client_req = UDPServerSocket.recvfrom(bufferSize)
        host_name = Client_req[0]
        clientIP = Client_req[1]

        if(host_name.decode() == 'bye'):
            output_file.write("Local DNS shutting down\n")
            break

        output_file.write("Client IP address: " + str(clientIP) + '\n')
        output_file.write("msg recieved from client: " + host_name.decode() + '\n\n')

        UDPServerSocket.sendto(host_name, root_ip)
        output_file.write("msg sent to root: " + host_name.decode() + '\n')

        msg_from_root = UDPServerSocket.recvfrom(bufferSize)[0].decode().split()
        output_file.write('msg from root: ' + ' '.join((msg_from_root)) + '\n\n')

        UDPServerSocket.sendto(host_name, (msg_from_root[0], int(msg_from_root[1])))
        output_file.write("msg sent to TLD: " + host_name.decode() + '\n')

        msg_from_tld = UDPServerSocket.recvfrom(bufferSize)[0].decode().split()
        output_file.write('msg fro TLD:  ' + ' '.join((msg_from_tld)) + '\n\n')

        UDPServerSocket.sendto(host_name, (msg_from_tld[0], int(msg_from_tld[1])))
        output_file.write("msg sent to authoritative: " + host_name.decode() + '\n')

        msg_from_authoritative = UDPServerSocket.recvfrom(bufferSize)[0].decode().split()
        output_file.write('msg from authoritative: ' + ' '.join(msg_from_authoritative) + '\n\n')

        UDPServerSocket.sendto(' '.join(msg_from_authoritative).encode(), clientIP)
        output_file.write("msg sent to client: " + ' '.join(msg_from_authoritative) + '\n\n')
        continue

    except:
        UDPServerSocket.sendto("No such host exists".encode(), clientIP)
        output_file.write("msg sent to client: No such host exists" + '\n\n')
        continue