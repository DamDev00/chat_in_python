import socket
import threading

# Creazione del socket del server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('127.0.0.1', 9090))
server_socket.listen()
users = 0
print("Server in ascolto...")
clients = []
nicknames = {}

def broadcast(current:socket.socket, message: str):
    current.send(f"me: {message}".encode())
    for client in clients:
        if nicknames[client.getpeername()[1]] != nicknames[current.getpeername()[1]]:
            client.send(f"{nicknames[current.getpeername()[1]]}: {message}".encode())
def receve(client: socket.socket):
    while True:
        data = client.recv(4096).decode()
        print(data)
        broadcast(client, data)

while True:
    conn, addr = server_socket.accept()
    users += 1
    clients.append(conn)
    print(f"Connessione stabilita con {conn.getpeername()[1]}")
    data = conn.recv(4096).decode()
    print(f"{data} entra in chat")
    nicknames[conn.getpeername()[1]] = data
    threading.Thread(target=receve,args=(conn,)).start()
    broadcast(conn, " join in the chat!")

conn.close()
server_socket.close()
