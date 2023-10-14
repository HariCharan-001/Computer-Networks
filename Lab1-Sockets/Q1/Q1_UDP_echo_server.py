import socket
import os

bufferSize  = 1024

# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip
UDPServerSocket.bind(("127.0.0.1", 12000))

print("UDP Echo server up and listening")

# Listen for incoming datagrams
while (True):
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    print(bytesAddressPair[0])
    message = bytesAddressPair[0].decode('ascii')
    address = bytesAddressPair[1]
    clientMsg = "Message from Client: {}".format(message)
    clientIP  = "Client IP Address: {}".format(address)
    
    print(clientIP)
    print(clientMsg)

    # Sending a reply to client
    UDPServerSocket.sendto(message.encode(), address)
