import threading
import socket
import ssl

# Configuration
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 8000
CERT_FILE = '/Users/s4nzok/python_practicals/Enhanced_TCP_chat(SSL)/server.crt'
# Path to the server's SSL certificate file

# SSL context setup
ssl_context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
ssl_context.load_verify_locations(CERT_FILE)

# Global variables
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # Create TCP socket
secure_client = ssl_context.wrap_socket(client, server_hostname=SERVER_HOST)  # Wrap with SSL/TLS

nickname = input("Choose a nickname: ")
if nickname == 'admin':
    password = input('Enter the admin password: ')

stop_thread = False

def receive_messages():
    """Receives messages from the server."""
    while True:
        global stop_thread
        if stop_thread:
            break
        try:
            message = secure_client.recv(1024).decode('utf-8')
            if message == 'NICK':
                secure_client.send(nickname.encode('utf-8'))
                next_message = secure_client.recv(1024).decode('utf-8')
                if next_message == 'PASS':
                    secure_client.send(password.encode('utf-8'))
                    if secure_client.recv(1024).decode('utf-8') == 'REFUSE':
                        print('The connection was refused. Wrong Password!')
                        stop_thread = True
                elif next_message == 'BAN':
                    print("Connection refused because of ban!")
                    secure_client.close()
                    stop_thread = True
            else:
                print(message)
        except socket.error:
            print("An error occurred!")
            secure_client.close()
            break

def send_message():
    """Sends messages to the server."""
    while True:
        if stop_thread:
            break
        message = f'{nickname}: {input("")}'
        if message[len(nickname)+2:].startswith('/'):   # username: /kick
            if nickname == 'admin':
                if message[len(nickname)+2].startswith('/kick'):
                    secure_client.send(f'KICK {message[len(nickname)+2+6:]}'.encode('utf-8'))
                elif message[len(nickname)+2].startswith('/ban'):
                    secure_client.send(f'BAN {message[len(nickname)+2+5:]}'.encode('utf-8'))
            else:
                print('commands can only be executed by admin!')
        else:
            secure_client.send(message.encode('utf-8'))

# Connect to the server
secure_client.connect((SERVER_HOST, SERVER_PORT))

# Send nickname to server
secure_client.send(nickname.encode('utf-8'))

# Start receive and send threads
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

send_thread = threading.Thread(target=send_message)
send_thread.start()
