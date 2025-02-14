import time
import socket

def start_up(host='127.0.0.1', port=5005):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((host, port))
    print(f"UDP server up and listening on {host}:{port}")

    while True:
        # Receive data from the client
        print("Waiting to receive data...")
        data, client_address = server_socket.recvfrom(4096)  # Adjust buffer size if needed
        receive_time = time.time()
        print(f"Received data from {client_address} at {receive_time}")

        # Calculate throughput
        data_size = len(data)  # Size of data in bytes
        throughput = data_size / (receive_time - float(data.decode()))  # Throughput in bytes per second
        throughput_kbps = (throughput * 8) / 1024  # Convert to kilobits per second

        # Send throughput back to the client
        server_socket.sendto(str(throughput_kbps).encode(), client_address)
        print(f"Throughput: {throughput_kbps:.2f} kbps")

if __name__ == "__main__":
    start_up()