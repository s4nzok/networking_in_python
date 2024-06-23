import threading
import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 8000))

nickname = input("choose a nickname: ")

def receive():   # here we are going to receive messages from the server.
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
                pass
            else:
                print(message)
        except ConnectionError:
            print("an error occured!")
            client.close()
            break

def write():
    while True:

        message = f'{nickname}: {input()}'

        # here the user is asked to input constantly after every inputs.
        # user has two options: either close client or write a message.
        # it is a thread: receiving and writing works simultaneously.

        client.send(message.encode('ascii'))

# now we need to run two threads: receive thread and a write thread.

receive_thread = threading.Thread(target = receive)
# we dont need any arguments here.
receive_thread.start()

write_thread = threading.Thread(target = write)
write_thread.start()