import socket
from socket import SocketOne

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 5000))

    server.listen(6)
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