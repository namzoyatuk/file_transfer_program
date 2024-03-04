# echo-client.py

import socket
import hashlib

HOST = socket.gethostbyname("server")
PORT = 8000

client_socket = socket.socket()
client_socket.connect((HOST, PORT))

file_number = input("Enter file number (or 'bye' to exit): ")

while file_number.lower().strip() != 'bye':
    # Receive and process small object
    client_socket.send(file_number.encode())

    small_file_size = int(client_socket.recv(4).decode())
    print(f"Received small file size: {small_file_size}")

    small_received_hash = client_socket.recv(33).decode().strip()
    small_file_data = b""
    while len(small_file_data) < small_file_size:
        chunk = client_socket.recv(1024)
        if not chunk:
            break
        small_file_data += chunk

    print(f"Small file {file_number} received but not checked for integrity")

    small_calculated_hash = hashlib.md5(small_file_data).hexdigest()
    print(f"Calculated md5 hash for small file: {small_calculated_hash}")

    if small_calculated_hash != small_received_hash:
        print(f"Small file {file_number} integrity check failed")
    else:
        print(f"Small file {file_number} received successfully")

        # Save the received small file_data to a file
        small_received_filename = f"received-small-{file_number}.obj"
        with open(small_received_filename, 'wb') as small_received_file:
            small_received_file.write(small_file_data)
            print(f"Small file {file_number} saved as {small_received_filename}")

    # Receive and process large object
    large_file_size = int(client_socket.recv(6).decode())   #problem
    print(f"Received large file size: {large_file_size}")

    large_received_hash = client_socket.recv(33).decode().strip()
    large_file_data = b""
    while len(large_file_data) < large_file_size:
        chunk = client_socket.recv(1024)
        if not chunk:
            break
        large_file_data += chunk

    print(f"Large file {file_number} received but not checked for integrity")

    large_calculated_hash = hashlib.md5(large_file_data).hexdigest()
    print(f"Calculated md5 hash for large file: {large_calculated_hash}")

    if large_calculated_hash != large_received_hash:
        print(f"Large file {file_number} integrity check failed")
    else:
        print(f"Large file {file_number} received successfully")

        # Save the received large file_data to a file
        large_received_filename = f"received-large-{file_number}.obj"
        with open(large_received_filename, 'wb') as large_received_file:
            large_received_file.write(large_file_data)
            print(f"Large file {file_number} saved as {large_received_filename}")

    file_number = input("Enter file number (or 'bye' to exit): ")

client_socket.close()

