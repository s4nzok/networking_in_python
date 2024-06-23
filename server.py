import threading
import socket

host = '127.0.0.1'
port = 8000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

# three methods: broadcast, handle method for client con and recv method,
# which combines all method into main method.

clients = []
nicknames = []

# broadcast func: sends msg to all clients, currentlly connected to the server.

def broadcast(message):
    for client in clients:
        client.send(message)

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            # try to receive msg from clients
            
            broadcast(message)
            # if succeeds, broad this msg to all clients.
            # including this client as well.

        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} has left the char!'.encode('ascii'))
            nicknames.remove(nickname)
            break
        
def receive():
    while True:
        client, address = server.accept()
        print(f"connected with {str(address)}")
        
        # now we need to ask the client for the nickname.
        # first msg that client sends should be nickname.

        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        print(f"nickname of the client is {nickname}")
        broadcast(f"{nickname} joined the chat.".encode('ascii'))
        client.send('connected to the server'.encode('ascii'))

        # now we define and run a thread.
        # one thread for each client.

        thread = threading.thread(target=handle, args=(client,))
        thread.start()

print('server is listening...')       
receive()
        

        














        


