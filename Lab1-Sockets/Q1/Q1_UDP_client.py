import socket

inp_msg = bytearray()
inp_msg.append(15)
inp_msg.append(207)
print(inp_msg)
bytesToSend         = inp_msg
serverAddressPort   = ('localhost', 12000)
bufferSize          = 1024

# Create a UDP socket at client side
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Send to server using created UDP socket
UDPClientSocket.sendto(bytesToSend, serverAddressPort)

#Wait on recvfrom()
msgFromServer = UDPClientSocket.recvfrom(bufferSize)

#Wait completed
msg = "Message from Server: {}".format(msgFromServer[0].decode('ascii'))

print(msg)
