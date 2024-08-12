import socket
import threading

# Client configuration
HOST = '127.0.0.1'  # Server's IP address
PORT = 12345        # Port to connect to

def receive_messages(client):
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == 'NAME':
                client.send(name.encode('utf-8'))
            elif message:
                print(message)
            else:
                print("Disconnected from server")
                client.close()
                break
        except:
            print("An error occurred!")
            client.close()
            break

def send_messages(client):
    while True:
        message = input()
        if message.lower() == 'exit':
            client.send(f'{name} has left the chat.'.encode('utf-8'))
            client.close()
            break
        else:
            client.send(f'{name}: {message}'.encode('utf-8'))

# Main function to start the client
if __name__ == "__main__":
    name = input("Choose your name: ")

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))

    # Start threads to handle sending and receiving messages
    receive_thread = threading.Thread(target=receive_messages, args=(client,))
    receive_thread.start()

    send_thread = threading.Thread(target=send_messages, args=(client,))
    send_thread.start()


