import socket

def compute(cmd):
    cmd = cmd.split()
    if cmd[0] == "add":
        return int(int(cmd[1]) + int(cmd[2]))
    elif cmd[0] == "mul":
        return int(int(cmd[1]) * int(cmd[2]))
    elif cmd[0] == "mod":
        return int(int(cmd[1]) % int(cmd[2]))
    elif cmd[0] == "hyp":
        return int(round(((int(cmd[1])**2 + int(cmd[2])**2)**0.5),0))
    else:
        return "Invalid command"

bufferSize  = 1024

# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip
UDPServerSocket.bind(("127.0.0.1", 12000))

print("UDP Math server up and listening")

# Listen for incoming datagrams
while (True):
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    message = bytesAddressPair[0].decode()
    address = bytesAddressPair[1]
    clientMsg = "Recieved: {}".format(message)
    clientIP  = "Client IP Address: {}".format(address)
    
    print(clientIP)
    print(clientMsg)
    
    # Sending a reply to client
    UDPServerSocket.sendto(str(compute(message)).encode(), address)