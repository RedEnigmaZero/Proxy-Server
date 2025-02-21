import time
import socket

def udp_server(host='127.0.0.1', port=5005):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
        server_socket.settimeout(15)  # Set a 15-second timeout
        # Binds server socket to given host and port
        server_socket.bind((host, port))
        print(f"UDP server up and listening on {host}:{port}")

        while True:
            try: 
                # Receive data from the client
                print("Waiting to receive data...")
                payload_size, client_address = server_socket.recvfrom(1024)  # Gets payload size in MB
                payload_size = (int(payload_size.decode()) * 1024 * 1024) # Calculates number of bytes to expect from payload
                print(payload_size)
                # Initializes variables for payload that has been sent and variable for when payload begins sending
                payload_received = 0
                buffer_size = 65507
                received_start_time = None
                
                for x in range(int(payload_size / buffer_size)):
                    if received_start_time is None:
                        received_start_time = float(server_socket.recv(1024).decode())
                    payload = server_socket.recv(buffer_size) # Experiment with different buffer sizes, 65507 is max, 4096 is common
                    payload_received += len(payload)

                received_end_time = time.time()

                try: transmission_time = received_end_time - received_start_time
                except: raise ValueError()

                print(f"Finished receiving data from {client_address} at {received_end_time}\nData: {payload_size} bytes")

                # Calculate throughput
                throughput = payload_received / transmission_time  # Throughput in bytes per second
                throughput_KBps = throughput / 1024.0  # Convert to kilobytes per second

                # Send throughput and received time back to the client
                server_socket.sendto(f"{throughput_KBps:.2f}".encode(), client_address)
                server_socket.sendto(f"{payload_size} bytes were received by server at {received_end_time} seconds from epoch".encode(), client_address)
                break # Breaks loop, closes server
            except socket.timeout:
                print("Socket timed out waiting for data")
                break

if __name__ == "__main__":
    udp_server()
