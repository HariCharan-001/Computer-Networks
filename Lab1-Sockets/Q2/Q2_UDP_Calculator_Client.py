import socket

serverAddressPort   = ('localhost', 12000)
bufferSize          = 1024

# Create a UDP socket at client side
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

while(True):
    cmd = input("Enter command: ")
    if(cmd == "exit"):
        break
    
    # Send to server using created UDP socket
    UDPClientSocket.sendto(cmd.encode(), serverAddressPort)

    #Wait on recvfrom()
    msgFromServer = UDPClientSocket.recvfrom(bufferSize)
    msg = "Answer from server: {}".format(msgFromServer[0].decode())
    print(msg)