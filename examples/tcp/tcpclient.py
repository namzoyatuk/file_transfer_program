# echo-client.py

import socket
import hashlib
HOST = socket.gethostbyname("server")  # Use this if you are using docker compose
# if you do not use docker compose, instead of resolving name
# set host to the ip address directly
#HOST = "172.19.0.2"
PORT = 8000  # socket server port number

client_socket = socket.socket()  # instantiate
client_socket.connect((HOST, PORT))  # connect to the server

file_number = input(" -> ")  # take input

while file_number.lower().strip() != 'bye':
    client_socket.send(file_number.encode())            # send which file to get
    file_size = int(client_socket.recv(1024).decode())  # receive file_size
    print(f"Received file size: {file_size}")
    received_hash = client_socket.recv(1024).decode().strip()   # receive md5 hash
    print(f"Received md5 hash {received_hash}")

    file_data = b''
    while len(file_data) < file_size:
        chunk = client_socket.recv(1024)
        file_data += chunk                              # receive file

    calculated_hash = hashlib.md5(file_data).hexdigest()
    print(f"Calculated md5 hash {calculated_hash}")

    if calculated_hash != received_hash:
        print(f"File {file_number} integrity check failed")
    else:
        print(f"File {file_number} received successfully ")

    file_number = input(" -> ")  # again take input

client_socket.close()  # close the connection
