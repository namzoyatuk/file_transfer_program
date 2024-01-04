import socket

# Server details
serverIP   = "127.0.0.1"  # Change to your server IP
serverPort = 8000
bufferSize = 1024

# Create a datagram socket
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
serverAddressPort = (serverIP, serverPort)

# Send initial hello message to server to initiate transfer
helloMessage = "Hello"
UDPClientSocket.sendto(helloMessage.encode(), serverAddressPort)

# Prepare to receive file
received_packets = {}
expected_seq = 0
file_data = []

try:
    while True:
        # Receive packet from the server
        message, address = UDPClientSocket.recvfrom(bufferSize)
        packet = message.decode()

        # Check for the end of the file transfer
        if packet == 'END':
            print("File transfer completed.")
            break

        # Extract sequence number and data from the packet
        seq, data = packet.split(':', 1)
        seq = int(seq)

        # Send acknowledgment back to the server
        UDPClientSocket.sendto(str(seq).encode(), address)

        # If this is the next expected packet, save the data
        if seq == expected_seq:
            file_data.append(data)
            expected_seq += 1

            # Check for any buffered packets
            while expected_seq in received_packets:
                file_data.append(received_packets.pop(expected_seq))
                expected_seq += 1
        else:
            # Buffer out-of-order packets
            received_packets[seq] = data

except KeyboardInterrupt:
    print("File transfer interrupted.")

finally:
    # Save the received data to a file
    with open('received_file.txt', 'w') as f:
        for data in file_data:
            f.write(data)
    print("Received file saved as 'received_file.txt'")
