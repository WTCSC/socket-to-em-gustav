import socket
import threading

server_running = True
client_sockets = []
connected_usernames = []

def broadcast(message, sender_socket=None):
    for client_socket in client_sockets:
        if client_socket != sender_socket:
            try:
                client_socket.send(message.encode())
            except:
                client_socket.close()
                client_sockets.remove(client_socket)

def handle_client(client_socket, client_username):
    global server_running
    try:
        print(f"{client_username} connected.")
        client_sockets.append(client_socket)
        connected_usernames.append(client_username)
        broadcast(f"{client_username} has joined the chat.", client_socket)

        while server_running:
            msg = client_socket.recv(1024).decode()
            if not msg:
                print(f"{client_username} disconnected.")
                break
            
            if msg.lower() == "/exit":
                print(f"{client_username} has left the chat.")
                broadcast(f"{client_username} has left the chat.", client_socket)
                break
            elif msg.lower() == "/users":
                user_list = ", ".join(connected_usernames)
                client_socket.send(f"Connected users: {user_list}".encode())
            else:
                print(f"{client_username}: {msg}")
                broadcast(f"{client_username}: {msg}", client_socket)

    except Exception as e:
        print(f"Error with client {client_username}: {e}")
    finally:
        client_socket.close()
        client_sockets.remove(client_socket)
        connected_usernames.remove(client_username)

def main():
    global server_running
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 8080))
    server.listen()
    print("Server created. Waiting for users...")

    while server_running:
        client_socket, addr = server.accept()
        print(f"Connection from {addr} established.")
        client_username = client_socket.recv(1024).decode()
        print(f"{client_username} joined!")
        threading.Thread(target=handle_client, args=(client_socket, client_username)).start()

    print("Server closed.")


if __name__ == "__main__":
    main()