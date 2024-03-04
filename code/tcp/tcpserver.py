# echo-server.py

import socket
import hashlib

HOST = "server"
PORT = 8000

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

            # Sending small object
            small_filepath = '/root/objects/small-' + file_num_in_string + '.obj'
            small_md5_path = small_filepath + '.md5'

            print(f"Sending small file at {small_filepath}")
            print(f"Sending small object number: {file_num_in_string}")

            with open(small_filepath, 'rb') as f:
                small_file_data = f.read()

            small_file_size = str(len(small_file_data)).encode()
            conn.send(small_file_size)
            print(f"Small file size sent: {len(small_file_data)} bytes")

            with open(small_md5_path, 'r') as f:
                small_md5_hash = f.read()
            conn.send(small_md5_hash.encode())
            print(f"Small MD5 hash sent: {small_md5_hash}")

            conn.sendall(small_file_data)
            print("Small file data sent")

            # Sending large object
            large_filepath = '/root/objects/large-' + file_num_in_string + '.obj'
            large_md5_path = large_filepath + '.md5'

            print(f"Sending large file at {large_filepath}")
            print(f"Sending large object number: {file_num_in_string}")

            with open(large_filepath, 'rb') as f:
                large_file_data = f.read()

            large_file_size = str(len(large_file_data)).encode()
            conn.send(large_file_size)
            print(f"Large file size sent: {len(large_file_data)} bytes")

            with open(large_md5_path, 'r') as f:
                large_md5_hash = f.read()
            conn.send(large_md5_hash.encode())
            print(f"Large MD5 hash sent: {large_md5_hash}")

            conn.sendall(large_file_data)
            print("Large file data sent")

