import socket
import json

def start(host='127.0.0.1', port=7000):
    # Create a TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"Server listening on {host}:{port}")

    while True:
        # Accept a connection from the proxy server
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address}")

        # Receive the message from the proxy server
        data = client_socket.recv(1024).decode()
        print(f"Received data: {data}")

        response_message = "pong"

        # Send the response back to the proxy server
        response = json.dumps({"message": response_message})
        client_socket.send(response.encode())
        print(f"Sent response: {response}")

        # Close the connection
        client_socket.close()

if __name__ == "__main__":
    start()