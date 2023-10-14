All the problems have been solved in python and can be run using, 
python3 $filename

For all servers, we assumed localhost and port 12000, so 2 server codes cannot be run simultaneously on the same port. So Please close the previous server before running other server codes. 
Servers are in an infinite while loop and does not have an exit command, so we have to force exit by using ctrl + C.

No additional command line arguments are required for servers or client. Client assumes local host and port 12000 and connects automatically if server is up.