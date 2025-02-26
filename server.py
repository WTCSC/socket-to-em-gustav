import socket
import threading
import time

def receive_messages(client_socket):
    while True:
        msg = client_socket.recv(1024).decode()
        if not msg:
            break
        print(F"Client: {msg}")
        client_socket.send(f"Server received: {msg}".encode())

def send_messages(client_socket):
    while True:
        msg = input("Enter message: ")
        if msg.lower == "/exit":
            time.sleep(1)
            client_socket.send("Disconnecting...")


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 5000))

    server.listen(1)
    print("Waiting for connection...")

    client, addr = server.accept()
    print(f"Connected to {addr}")

    while True:
        msg = client.recv(1024).decode()
        if not msg:
            break
        print(f"Recieved: {msg}")
        client.send(f"server received: {msg}".encode())

    client.close()
    server.close()

if __name__ == "__main__":
    main()


# Add 'User Disconnected' Erase Convo?