#udpclient.py

import socket

# Server details
serverIP   = "server"  # Change to your server IP
serverPort = 8000
bufferSize = 1024

# Create a datagram socket
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
serverAddressPort = (serverIP, serverPort)


def receive_file():
    received_packets = {}
    expected_seq = 0
    file_data = []
    file_name = None

    while True:
        message, address = UDPClientSocket.recvfrom(bufferSize)
        packet = message.decode()

        # check if it is the end of file
        if packet == 'END':
            print(f"File transfer completed for {file_name}")
            break


        try:
            seq, data = packet.split(':', 1)
            seq = int(seq)

            # if this is the next expected packet, save the data
            if seq == expected_seq:
                file_data.append(data)
                expected_seq += 1

                # check for any buffered packets
                while expected_seq in received_packets:
                    file_data.append(received_packets.pop(expected_seq))
                    expected_seq += 1

            else:
                # buffer out-of-order packets
                received_packets[seq] = data

            UDPClientSocket.sendto(str(seq).encode(), address)

        except ValueError:
            # if not a data a packet
            if packet.startswith('FILENAME:'):
                file_name = packet.split(':', 1)[1]
            else:
                print(f"Received an unexpected message: {packet}")

    return file_name, file_data


while True:
    # request specific file number
    file_number = input("Enter the file number: ")
    UDPClientSocket.sendto(file_number.encode(), serverAddressPort)

    for _ in range(2):
        file_name, file_data = receive_file()

        if file_name:
            # Save the received data to a file
            with open(file_name, 'wb') as f:
                for data in file_data:
                    f.write(data.encode())
            print(f"Received file saved as '{file_name}'")
        else:
            print("No file name received.")

