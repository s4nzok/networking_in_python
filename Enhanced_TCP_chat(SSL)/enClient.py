import threading
import socket
import ssl

# Configuration
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 8000
CERT_FILE = 'server.crt'  # Path to the server's SSL certificate file

# SSL context setup
ssl_context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
ssl_context.load_verify_locations(CERT_FILE)

# Global variables
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # Create TCP socket
secure_client = ssl_context.wrap_socket(client)              # Wrap with SSL/TLS

nickname = input("Choose a nickname: ")

def receive_messages():
    """Receives messages from the server."""
    while True:
        try:
            message = secure_client.recv(1024).decode('utf-8')
            print(message)
        except socket.error:
            print("An error occurred!")
            secure_client.close()
            break

def send_message():
    """Sends messages to the server."""
    while True:
        message = input("")
        secure_client.send(f'{nickname}: {message}'.encode('utf-8'))

# Connect to the server
secure_client.connect((SERVER_HOST, SERVER_PORT))

# Send nickname to server
secure_client.send(nickname.encode('utf-8'))

# Start receive and send threads
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

send_thread = threading.Thread(target=send_message)
send_thread.start()
