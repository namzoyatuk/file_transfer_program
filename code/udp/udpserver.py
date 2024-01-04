#udpserver.py

import socket
import threading
import time

# Server details
localIP     = "server"  # Change to your server IP
localPort   = 8000
buffer_size  = 1024

# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPServerSocket.bind((localIP, localPort))
print("UDP server up and listening")

# Global variables for managing acknowledgments and window
ack_received = []
window_size = 4  # Adjust as needed
send_base = 0

# Packet creation
def create_packet(seq, data):
    return f'{seq}:{data}'.encode()

# Send packet
def send_packet(packet, addr):
    UDPServerSocket.sendto(packet, addr)

# Receive acknowledgments
def ack_receiver():
    global send_base
    while True:
        msg, _ = UDPServerSocket.recvfrom(buffer_size)
        try:
            ack_seq = int(msg.decode().split(':', 1)[0])
            if ack_seq >= send_base:
                ack_received.append(ack_seq)
                print(f"Acknowledgment received for packet: {ack_seq}")
        except ValueError:
            # Handle messages that are not in the expected format
            print(f"Ignoring unexpected message: {msg}")
            continue


# UDP Sender function
def UDP_sender(file_path, client_addr):
    global send_base
    filename = file_path.split('/')[-1]  # Extracts file name from the path
    send_packet(f'FILENAME:{filename}'.encode(), client_addr)

    with open(file_path, "rb") as f:
        seq = 0
        packets_to_send = []

        # Read and packetize the entire file
        while True:
            data = f.read(buffer_size - len(str(seq)) - 1)
            if not data:
                break
            packet = create_packet(seq, data)
            packets_to_send.append((seq, packet))
            seq += 1

        # Start sending packets
        while packets_to_send or send_base < seq:
            while packets_to_send and send_base + window_size > packets_to_send[0][0]:
                packet_seq, packet = packets_to_send.pop(0)
                send_packet(packet, client_addr)
                print(f"Sent packet {packet_seq}")

            # Check for acknowledgments and slide window
            ack_received.sort()
            while ack_received and ack_received[0] == send_base:
                send_base += 1
                ack_received.pop(0)

            # If all packets are sent and acknowledged
            if send_base >= seq and not packets_to_send:
                break

            time.sleep(0.1)  # Adjust timing as needed for your network conditions

        # Send a final message indicating transfer completion
        send_packet(b'END', client_addr)
        print("File transfer completed.")



while True:
    print("Waiting for file number...")
    number_message, client_addr = UDPServerSocket.recvfrom(buffer_size)
    file_number = number_message.decode()

    small_file_path = '/root/objects/small-' + file_number + '.obj'
    large_file_path = '/root/objects/large-' + file_number + '.obj'

    UDP_sender(small_file_path, client_addr)
    UDP_sender(large_file_path, client_addr)


