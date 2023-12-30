# echo-server.py

import socket

HOST = "server"  # Set to the IP address of the server eth0 if you do not use docker compose 
PORT = 8000  # Port to listen on (non-privileged ports are > 1023)

# This implementation supports only one client
# You have to implement threading for handling multiple TCP connections
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                break

            file_num_in_string = data.decode()
            filepath = '/root/objects/small-' + file_num_in_string + '.obj'
            print(f"Sending file at {filepath}")
            print(f"Sending object number: {file_num_in_string}")
            md5_path = filepath + '.md5'

            with open(filepath, 'rb') as f:
                file_data = f.read()

            file_size = str(len(file_data)).encode()
            conn.send(file_size)

            with open(md5_path, 'r') as f:
                md5_hash = f.read()

            conn.send(md5_hash.encode())

            conn.sendall(file_data)