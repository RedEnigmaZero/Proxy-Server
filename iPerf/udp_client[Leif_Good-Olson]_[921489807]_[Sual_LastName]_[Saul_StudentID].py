import time
import socket

def udp_client(host='127.0.0.1', port=5005):

    payload_size_str = input("Enter how many MBs to send: ").strip()
    payload_size = int(payload_size_str)
    payload_size_bytes = (1024*1024*payload_size)

    payload = b"x" * payload_size_bytes

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
        client_socket.connect((host, port))
        local_ip, local_port = client_socket.getsockname()
        print(f"Client running on {local_ip}:{local_port}")
        print(f"Server address is {host}:{port}")
        #client_socket.sendall(payload_size_str.encode())
        client_socket.sendto(payload_size_str.encode(), (host, port))

        payload_sent = 0
        packet_size = 4096
        send_start_time = None


        while payload_sent < payload_size_bytes:
            end_index = min(payload_sent + packet_size, payload_size_bytes)
            print(end_index)
            # Send a chunk
            client_socket.sendto(payload[payload_sent:end_index], (host, port))
            payload_sent = end_index
            print("Sending...")
            print(payload_sent)
            
            
        send_end_time = time.time()
        data = client_socket.recvfrom(1024)
    print(f"Throughput: {data[0].decode()} KBps")

if __name__ == "__main__":
    udp_client()
