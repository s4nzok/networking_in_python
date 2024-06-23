import threading
import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 8000))

nickname = input("Choose a nickname: ")

def receive_messages():  # Here we are going to receive messages from the server.
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
            else:
                print(message)
        except ConnectionError:
            print("An error occurred!")
            client.close()
            break

def write_messages():
    while True:
        message = f'{nickname}: {input()}'
        # Here the user is asked to input constantly after every input.
        # The user has two options: either close the client or write a message.
        # It is a thread: receiving and writing works simultaneously.
        client.send(message.encode('ascii'))

# Now we need to run two threads: a receive thread and a write thread.
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

write_thread = threading.Thread(target=write_messages)
write_thread.start()
