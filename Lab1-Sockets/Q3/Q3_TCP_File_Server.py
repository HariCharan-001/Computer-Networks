import socket
import os

serverPort = 12000
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind(('',serverPort))
serverSocket.listen(1)

print("TCP File Server up and running")

while True:
    (connectionSocket, clientAddress) = serverSocket.accept()
    print("Accepted a connection request from %s:%s"%(clientAddress[0], clientAddress[1]))
    
    sentence = connectionSocket.recv(1024)
    file_name, N = sentence.decode().split(' ')

    if(os.path.isfile(file_name)):
        with open(file_name, 'rb') as f:
            f.seek(-int(N), 2)
            msg_to_client = f.read().decode()
            connectionSocket.send(msg_to_client.encode())
        
        print("Sent file" + file_name + " with " + N + " bytes to client" )

    else:
        print("File not found")
        connectionSocket.send("SORRY!".encode())


    connectionSocket.close()