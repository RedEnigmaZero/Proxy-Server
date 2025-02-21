# proxy_server.py
import socket
import json

# Define the blocklist of IP addresses
BLOCKLIST = ["127.0.0.2"]  # Example blocklist

def start_proxy_server(host='127.0.0.1', port=6000):
    # Create a TCP socket
    proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy_socket.settimeout(15)
    proxy_socket.bind((host, port))
    proxy_socket.listen(1)
    print(f"Proxy server listening on {host}:{port}")

    while True:
        try:
            # Accept a connection from the client
            client_socket, client_address = proxy_socket.accept()
            print(f"Connection from {client_address}")

            # Receive the JSON message from the client
            data = client_socket.recv(1024).decode()
            print(f"Received data: {data}")

            # Parse the JSON message
            message = json.loads(data)
            server_ip = message["server_ip"]
            server_port = message["server_port"]
            client_message = message["message"]

            # Check if the server IP is in the blocklist
            if server_ip in BLOCKLIST:
                print(f"Blocked request to {server_ip}")
                response = json.dumps({"message": "Error"})
                client_socket.send(response.encode())
            else:
                # Forward the message to the server
                server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                server_socket.connect((server_ip, server_port))
                print(f"Sending message to server: {client_message}")
                server_socket.send(json.dumps({"message": client_message}).encode())

                # Receive the response from the server
                response = server_socket.recv(1024).decode()
                print(f"Received response from server: {response}")

                # Forward the response back to the client
                client_socket.send(response.encode())

            # Close the connection
            client_socket.close()
            #break
        except socket.timeout:
            print("Proxy Timeout")
            proxy_socket.close()
            break

if __name__ == "__main__":
    start_proxy_server()