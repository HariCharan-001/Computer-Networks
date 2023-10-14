import socket

serverName = 'localhost'
serverPort = 12000
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((serverName,serverPort))

filename = input("Input a filename : ")
N = int(input("Input the number of bytes required : "))
clientSocket.sendto((filename + " " + str(N)).encode(), (serverName, serverPort))

server_msg = (clientSocket.recv(1024)).decode()

if server_msg == "SORRY!":
    print("Server says that the file does not exist.")

else:
    new_file_name = filename.removesuffix('.txt') + "1.txt"
    f = open(new_file_name, 'w')
    f.write(server_msg)
    f.close()
    print("Created file " + new_file_name + " with " + str(N) + " bytes data from server")

clientSocket.close()
