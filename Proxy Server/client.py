# client.py
import socket
import json

def send_message(server_ip='127.0.0.1', server_port=7000, proxy_ip='127.0.0.1', proxy_port=6000):
    # Create a TCP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((proxy_ip, proxy_port))

    # Prepare the JSON message
    message = {
        "server_ip": server_ip,
        "server_port": server_port,
        "message": "ping"  
    }

    # Send the message to the proxy server
    client_socket.send(json.dumps(message).encode())
    print(f"Sent message to proxy: {message}")

    # Receive the response from the proxy server
    response = client_socket.recv(1024).decode()
    print(f"Received response: {response}")

    # Close the connection
    client_socket.close()

if __name__ == "__main__":
    send_message()