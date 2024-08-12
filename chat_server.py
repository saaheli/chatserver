import socket
import threading

# Server configuration
HOST = '127.0.0.1'  # Localhost
PORT = 12345        # Port to listen on

# List to keep track of connected clients
clients = []
names = []

# Function to broadcast messages to all clients
def broadcast(message):
    for client in clients:
        try:
            client.send(message)
        except BrokenPipeError:
            # Handle broken pipe error
            remove_client(client)

# Function to handle individual client connections
def handle_client(client):
    while True:
        try:
            # Receive and broadcast messages
            message = client.recv(1024)
            if not message:
                # Connection was closed
                remove_client(client)
                break
            broadcast(message)
        except Exception as e:
            # Handle other exceptions (e.g., connection reset by peer)
            print(f"Error: {e}")
            remove_client(client)
            break

# Function to remove and close a client connection
def remove_client(client):
    try:
        index = clients.index(client)
        clients.remove(client)
        name = names.pop(index)
        client.close()
        broadcast(f'{name} left the chat!'.encode('utf-8'))
    except ValueError:
        # Handle the case where the client was not found
        pass

# Function to receive and accept new clients
def receive_connections():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    print(f"Server running on {HOST}:{PORT}")

    while True:
        # Accept new client connection
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        # Request and store the name
        client.send('NAME'.encode('utf-8'))
        name = client.recv(1024).decode('utf-8')
        names.append(name)
        clients.append(client)

        # Broadcast name and start handling thread
        print(f'Name of the client is {name}')
        broadcast(f'{name} joined the chat!'.encode('utf-8'))
        client.send('Connected to the server!'.encode('utf-8'))

        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

if __name__ == "__main__":
    receive_connections()



