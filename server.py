import socket
import threading

server_running = True
client_sockets = []



def receive_messages(client_socket, client_username):
    global server_running
    while server_running:
        try:
            msg = client_socket.recv(1024).decode()
            if not msg:
                print(f"\n{client_username} has diconnected.")
                break


            print(F"\r{client_username}: {msg}") # \nEnter message: ", end="", flush=True)
            print("<You> ", end="", flush=True)

            if msg.lower() == "/exit":
                print(f"\n{client_username} has left the chat.")
                try:
                    client_socket.send("Disconnected from the server.".encode())
                except:
                    pass
                break

        except ConnectionResetError:
            print(f"\n{client_username} disconnected.")
            break

def send_messages(client_socket):
    global server_running
    while server_running:
        try:
            msg = input("<You> ")
            if msg.lower() == "/exit":
                print("\nShutting down server...")
                server_running = False
                try:
                    client_socket.send("Server is shutting down...".encode())
                except:
                    pass
                try:
                    client_socket.close()
                except:
                    pass
                break

            if server_running:
                broadcast(msg, client_socket)

        except (ConnectionAbortedError, ConnectionResetError):
            print("\nClient disconnected.")
            break

def broadcast(msg, sender_socket):
    for client_socket in client_sockets:
        if client_socket != sender_socket:
            try:
                sender_username = sender_socket.recv(1024).decode()
                client_socket.send(f"{sender_username}: {msg}".encode())
            except:
                pass

def handle_client(client_socket, client_username):
    global server_running
    try:
        print(f"{client_username} connected.")
        client_sockets.append(client_socket)
        while server_running:
            msg = client_socket.recv(1024).decode()
            if not msg:
                print(f"{client_username} disconnected.")
                break
            print(f"{client_username}: {msg}")
            broadcast(msg, client_socket)
    except:
        print(f"Error with client {client_username}")
    finally:
        client_socket.close()
        client_sockets.remove(client_socket)

def main():
    global server_running
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 8080))
    server.listen()
    print("Server created. Waiting for users...")

    while server_running:
        client_socket, addr = server.accept()
        client_username = client_socket.recv(1024).decode()
        print(f"{client_username} joined!")
        threading.Thread(target=handle_client, args=(client_socket, addr, client_username)).start()

    print("Server closed.")


if __name__ == "__main__":
    server_running = True
    main()