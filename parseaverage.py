import re
import sys
import linecache
import os
import socket

import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ("192.168.0.2", 9050)
sock.bind(server_address)
sock.listen(1)

while True:
    # Wait for a connection
    connection, client_address = sock.accept()
    try:
        data = connection.recv(1024)
        os.system()
        os.system("ping -c 5 10.139.57.122 > pingout.txt")
        s = linecache.getline('pingout.txt',10)		
        arr = s.split('/')
        print(arr[4])
	connection.sendall(arr[4])
            
    finally:
        # Clean up the connection
        connection.shutdown(SHUT_RDWR)
        connection.close()
sock.shutdown(SHUT_RDWR)
sock.close()
