#udpclient.py

import socket

# Server details
serverIP   = "server"  # Change to your server IP
serverPort = 8000
bufferSize = 1024

# Create a datagram socket
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
serverAddressPort = (serverIP, serverPort)

def reset_for_next_file():
    global expected_seq, received_packets, file_data
    expected_seq = 0
    received_packets.clear()
    file_data.clear()

# Send initial hello message to server to initiate transfer


def end_of_file_handling(small_and_large, file_name, file_data):
    print("END OF FILE HANDLING WORKING")
    if small_and_large == 0:
        print("File transfer completed for small-" + file_name + ".obj")
        # with open('received_file.obj', 'w') as f:  #
        #     f.writelines(file_data)
        # print("Received file saved.")
        # Prepare for the next file
    elif small_and_large == 1:
        print("File transfer completed for small-" + file_name + ".obj.md5")
    elif small_and_large == 2:
        print("File transfer completed for large-" + file_name + ".obj")
    else:
        print("File transfer completed for large-" + file_name + ".obj.md5")

    reset_for_next_file()





file_name = input("Please enter the file number: ")
UDPClientSocket.sendto(file_name.encode(), serverAddressPort)

# Prepare to receive file
received_packets = {}
expected_seq = 0
file_data = []

small_and_large = 0

try:
    while True:
        print("END OF FILE HANDLING WORKING")
        # Receive packet from the server
        if small_and_large == 4:
            # a flag for both small and large object has been sent and
            # asks for new file input
            file_name = input("Please enter the file number: ")
            UDPClientSocket.sendto(file_name.encode(), serverAddressPort) # a random message to kill daemon thread
            UDPClientSocket.sendto(file_name.encode(), serverAddressPort)
            small_and_large = 0

        message, address = UDPClientSocket.recvfrom(bufferSize)
        packet = message.decode()

        # Check for the end of the file transfer
        # TODO md5 checking should be implemented
        if packet == 'END':
            end_of_file_handling(small_and_large, file_name)
            small_and_large += 1
            continue  # Continue to receive the next file

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
