import threading
import socket

HOST = '127.0.0.1'
PORT = 8000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []
nicknames = []


# Broadcast function: sends messages to all clients currently connected to the server.
def broadcast(message):
    for client in clients:
        client.send(message)


# Handle method for client connection.
def handle_client(client):
    while True:
        try:
            message = client.recv(1024)
            # Try to receive message from clients.
            broadcast(message)
            # If successful, broadcast this message to all clients, including the sender.
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} has left the chat!'.encode('ascii'))
            nicknames.remove(nickname)
            break


# Receive method: combines all methods into the main method.
def receive_connections():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        # Now we need to ask the client for their nickname.
        # The first message that the client sends should be their nickname.
        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        print(f"Nickname of the client is {nickname}")
        broadcast(f"{nickname} joined the chat.".encode('ascii'))
        client.send('Connected to the server'.encode('ascii'))

        # Now we define and run a thread for each client.
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()


print('Server is listening...')
receive_connections()
