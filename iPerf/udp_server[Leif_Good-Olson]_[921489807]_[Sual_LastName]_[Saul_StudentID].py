import time
import socket

def udp_server(host='127.0.0.1', port=5005):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
        server_socket.bind((host, port))
        print(f"UDP server up and listening on {host}:{port}")

        while True:
            # Receive data from the client
            print("Waiting to receive data...")
            payload_size, client_address = server_socket.recvfrom(1024)  # Gets payload size in MB
            payload_size = (int(payload_size.decode()) * 1024 * 1024) # Calculates number of bytes to expect from payload
            payload_received = 0

            print(payload_size)
            start_time = None 
            
            while payload_received < payload_size:
                payload, client_address = server_socket.recvfrom(4096) # Experiment with different buffer sizes
                if start_time is None:
                    start_time = time.time()
                payload_received += len(payload)
                print("Receiving...")
                print(payload_received)
                print(f"Payload length: {len(payload)}")
            end_time = time.time()

            try:
                transmission_time = end_time - start_time
            except:
                raise ValueError()

            print(f"Received data from {client_address} at {end_time}\nData: {payload_size}")

            # Calculate throughput
            # data_size = len(payload_size)  # Size of data in bytes
            throughput = payload_received / transmission_time  # Throughput in bytes per second
            throughput_KBps = throughput / 1024.0  # Convert to kilobytes per second

            # Send throughput back to the client
            server_socket.sendto(f"{throughput_KBps:.2f}".encode(), client_address)

            break

if __name__ == "__main__":
    udp_server()
