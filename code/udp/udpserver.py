#udpserver.py

import socket
import threading
import time

# Server details
localIP     = "server"  # Change to your server IP
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

stop_thread = False

def restart_threads():
    global stop_thread, ack_thread
    stop_thread = False  # Reset the flag
    ack_thread = threading.Thread(target=ack_receiver)  # Recreate the thread
    ack_thread.daemon = True
    ack_thread.start()


# Function to reset global variables for next transfer
def reset_globals():
    global send_base, ack_received
    send_base = 0
    ack_received.clear()
# Function to handle multiple file transfers
def handle_multiple_transfers(filenames, clientAddr):
    for filename in filenames:
        print(f"Starting transfer for {filename}")
        UDP_sender(filename, clientAddr)  # Call your existing file transfer function
        reset_globals()  # Reset global variables for the next file

# Packet creation
def create_packet(seq, data):
    return f'{seq}:{data}'.encode()

# Send packet
def send_packet(packet, addr):
    UDPServerSocket.sendto(packet, addr)

# Receive acknowledgments
def ack_receiver():
    global send_base
    global stop_thread
    while True:
        if stop_thread:
            break
        msg, _ = UDPServerSocket.recvfrom(bufferSize)
        decoded_msg = msg.decode()

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

ack_thread = threading.Thread(target=ack_receiver)
ack_thread.daemon = True


while True:
    # Wait for an incoming connection
    print("Waiting for incoming connection...")
    data, addr = UDPServerSocket.recvfrom(bufferSize)

    if data.decode() == 'bye':
        break


    file_number = data.decode()
    print(f"Connection established with {addr}")
    large_file = '/root/objects/large-' + file_number + '.obj'
    small_file = '/root/objects/small-' + file_number + '.obj'
    file_list = [small_file, large_file]  # Add paths to your files
    # Start acknowledgment receiver thread
    restart_threads()
    handle_multiple_transfers(file_list, addr)
    stop_thread = True
