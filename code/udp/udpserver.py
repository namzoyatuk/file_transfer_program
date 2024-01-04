import socket
import threading
import time

# Server details
localIP     = "127.0.0.1"  # Change to your server IP
localPort   = 8000
bufferSize  = 1024

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
        msg, _ = UDPServerSocket.recvfrom(bufferSize)
        ack = int(msg.decode())
        if ack >= send_base:
            ack_received.append(ack)
            print(f"Acknowledgment received for packet: {ack}")

# UDP Sender function
def UDP_sender(filename, clientAddr):
    global send_base
    with open(filename, "rb") as f:
        seq = 0
        packets_to_send = []

        # Read and packetize the entire file
        while True:
            data = f.read(bufferSize - len(str(seq)) - 1)
            if not data:
                break
            packet = create_packet(seq, data)
            packets_to_send.append((seq, packet))
            seq += 1

        # Start sending packets
        while packets_to_send or send_base < seq:
            while packets_to_send and send_base + window_size > packets_to_send[0][0]:
                packet_seq, packet = packets_to_send.pop(0)
                send_packet(packet, clientAddr)
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
        send_packet(b'END', clientAddr)
        print("File transfer completed.")

# Start acknowledgment receiver thread
ack_thread = threading.Thread(target=ack_receiver)
ack_thread.daemon = True
ack_thread.start()

# Wait for an incoming connection
print("Waiting for incoming connection...")
data, addr = UDPServerSocket.recvfrom(bufferSize)
if data.decode() == 'Hello':
    print(f"Connection established with {addr}")
    UDP_sender("path/to/your/file.txt", addr)
