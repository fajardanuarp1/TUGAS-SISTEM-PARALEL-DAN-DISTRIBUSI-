import socket
import threading

HOST = '127.0.0.1'
PORT = 55555


server  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []
nicknames = []

def broadcast(message, sender_client):
    for client in clients:
        if client != sender_client:
            client.send(message)


def handle_client(client):
   
    index = clients.index(client)
    nickname = nicknames[index]
    
    while True:
        try:
            message_raw = client.recv(1024)
            if not message_raw:
                raise ConnectionError()
            full_message = f"{nickname}: {message_raw.decode('utf-8')}".encode('utf-8')   
            print(full_message.decode('utf-8')) 
            broadcast(full_message, client)

        except:
   
            clients.remove(client)
            client.close()
            nicknames.pop(index) 
            broadcast(f'{nickname} telah meninggalkan chat!'.encode('utf-8'), client)
            break

def receive_connections():
    while True: 
        client, address = server.accept()
        print(f'Connected with {str(address)}')

        client.send('NICK'.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        nicknames.append(nickname)
        clients.append(client)

        print(f"Nickname of the client is {nickname}")

        join_message = f"{nickname} joined the chat!"

        print(join_message)

        broadcast(join_message.encode('utf-8'), client)
        client.send("Connected to the server!".encode('utf-8'))

        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

print('Server is listening...')
receive_connections()
    