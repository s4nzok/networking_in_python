import threading
import socket
import ssl
import logging

# Configuration
HOST = '127.0.0.1'
PORT = 8000
MAX_CLIENTS = 10
CERT_FILE = 'server.crt'  # Path to your server's SSL certificate file
KEY_FILE = 'server.key'   # Path to your server's SSL private key file

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# SSL context setup
ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
ssl_context.load_cert_chain(certfile=CERT_FILE, keyfile=KEY_FILE)

# Global variables
clients = []         # List to store connected client sockets
nicknames = {}       # Dictionary to map client sockets to their nicknames

def broadcast(message, sender):
    """Broadcasts a message to all connected clients except the sender."""
    for client_socket in clients:
        if client_socket != sender:
            try:
                client_socket.send(message)
            except socket.error:
                handle_disconnect(client_socket)

def handle_client(client_socket):
    """Handles communication with a single client."""
    while True:
        try:
            message = client_socket.recv(1024)
            if message:
                broadcast(message, client_socket)
            else:
                handle_disconnect(client_socket)
                break
        except socket.error:
            handle_disconnect(client_socket)
            break

def handle_disconnect(client_socket):
    """Handles client disconnection."""
    if client_socket in clients:
        nickname = nicknames.get(client_socket, 'Anonymous')
        del nicknames[client_socket]
        clients.remove(client_socket)
        broadcast(f"{nickname} has left the chat.".encode('utf-8'), client_socket)
        client_socket.close()

def receive_connections():
    """Accepts incoming client connections."""
    while True:
        client_socket, client_address = server.accept()
        logger.info(f"Connected with {client_address}")

        # SSL handshake
        try:
            secure_client = ssl_context.wrap_socket(client_socket, server_side=True)
        except ssl.SSLError as e:
            logger.error(f"SSL handshake failed with {client_address}: {e}")
            continue

        secure_client.send('NICK'.encode('utf-8'))        # Request nickname from client
        nickname = secure_client.recv(1024).decode('utf-8')
        nicknames[secure_client] = nickname               # Map client socket to nickname
        clients.append(secure_client)                     # Add client socket to list

        logger.info(f"Nickname of the client is {nickname}")
        broadcast(f"{nickname} joined the chat.".encode('utf-8'), secure_client)
        secure_client.send('Connected to the server'.encode('utf-8'))

        thread = threading.Thread(target=handle_client, args=(secure_client,))
        thread.start()

# Main server setup
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(MAX_CLIENTS)

logger.info('Server is listening...')
receive_connections()
