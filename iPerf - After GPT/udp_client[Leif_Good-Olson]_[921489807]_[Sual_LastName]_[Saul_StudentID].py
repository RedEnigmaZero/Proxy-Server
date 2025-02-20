import time
import socket

def udp_client(host='127.0.0.1', port=5005):
    # Accepts user input for payload size in megabytes, converts to bytes
    payload_size_str = input("Enter number of MBs to send: ").strip()
    payload_size_bytes = (1024 * 1024 * int(payload_size_str))
    print(f"Size in bytes: {payload_size_bytes}\nSize: {int(payload_size_str)}")
    # Creates specified number of bytes filled with "x" for testing
    payload = b"x" * payload_size_bytes 

    # Creates connection and sends payload, closes connection when done
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
        client_socket.settimeout(15)  # Set a 15-second timeout
        client_socket.connect((host, port)) # Connects to server with host/port IP
        local_ip, local_port = client_socket.getsockname() # Gets IP of client

        print(f"Client running on {local_ip}:{local_port}") # Prints IP of client
        print(f"Server address is {host}:{port}") # Prints IP of server
        
        try:
            client_socket.send(payload_size_str.encode()) # Sends payload size so server knows how much data to expect

            # Initializes variables for payload that has been sent and amount of data we will send at once
            payload_sent = 0
            packet_size = 65507 # 65507 is max datagram size, 4096 is commons

            # Initializes variable for when payload begins sending
            send_start_time = None
            print("Before sending")
            check = 0
            # While any of payload is unsent, iterates through payload, sending chunks
            while payload_sent < payload_size_bytes:
                # If send time has not yet been specified, sends start transmission time to server for throughput calculation
                if send_start_time is None: 
                    send_start_time = time.time()
                    client_socket.send(str(send_start_time).encode())
                end_index = min(payload_sent + packet_size, payload_size_bytes)
                client_socket.send(payload[payload_sent:end_index])
                print(f"Check: {check}")
                check+=1
                payload_sent = end_index
            print("Done")
            # Receives throughput data from server and prints it
            data = client_socket.recv(1024)
            received_info = client_socket.recv(1024)
            print(f"Throughput: {data.decode()} KBps")
            print(f"{payload_size_bytes} bytes were sent at {send_start_time} seconds from epoch")
            print(f"{received_info.decode()}")
        except socket.timeout:
            print("Socket timed out waiting for data")

if __name__ == "__main__":
    udp_client()
