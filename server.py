import socket
import threading

server_running = True # Set server_running to True
client_sockets = [] # Create a list of all clients
connected_usernames = [] # Create a list of all client usernames

# Broadcast the message to all clients except for sender
def broadcast(message, sender_socket=None):
    for client_socket in client_sockets: # For loop to loop through all connected clietns
        if client_socket != sender_socket: # Skips the sender socket
            try:
                client_socket.send(message.encode()) # Send message to each client
            except:
                client_socket.close() # Close the connection if an error occurs
                client_sockets.remove(client_socket) # Remove client from the list of sockets when disconnected

# Function to handle client and communication with a single client
def handle_client(client_socket, client_username): 
    global server_running
    try:
        print(f"{client_username} connected.") # Prints connect message when a client connects
        client_sockets.append(client_socket) # Add the client to the client list
        connected_usernames.append(client_username) # Add the username to the username list
        broadcast(f"{client_username} has joined the chat.", client_socket) # Notify other clients that the client has joined

        while server_running: # Keep the client connection alive as long as the server is running
            msg = client_socket.recv(1024).decode() # Receive message from the client
            if not msg: # If no message, client has disconnected
                print(f"{client_username} disconnected.") # Notify server that client disconnected
                break # Exit the loop if the client disconnects
            
            if msg.lower() == "/exit": # Checks if the client sends the exit command
                print(f"{client_username} has left the chat.") # Notify server that client left
                broadcast(f"{client_username} has left the chat.", client_socket) # Notify other clients that the user disconnected
                break # Exit the loop and stop handling this client
            elif msg.lower() == "/users": # If the client asks for the list of connected users
                user_list = ", ".join(connected_usernames) # Create a string from the connected usernames list
                client_socket.send(f"Connected users: {user_list}".encode()) # Send this string to the client
            else: # If the client sends a normal message
                print(f"{client_username}: {msg}") # Print the message on the server
                broadcast(f"{client_username}: {msg}", client_socket) # Broadcast message to other clients

    except Exception as e: # If any error occurs while handling the client
        print(f"Error with client {client_username}: {e}") # Print the error message
    finally:
        client_socket.close() # Close the client socket
        client_sockets.remove(client_socket) # Remove the socket from the list of clients
        connected_usernames.remove(client_username) # Remove the username of socket from the username list

# Function to run server
def main():
    global server_running
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create a server socket
    server.bind(('0.0.0.0', 8080)) # Bind the server to listen on all network interfaces on (0.0.0.0) and on port 8080
    server.listen() # Start listening to users connecting
    print("Server created. Waiting for users...") # Print waiting message to server

    while server_running:
        client_socket, addr = server.accept()
        print(f"Connection from {addr} established.")
        client_username = client_socket.recv(1024).decode()
        print(f"{client_username} joined!") # Prints client username that joined
        threading.Thread(target=handle_client, args=(client_socket, client_username)).start()

    print("Server closed.")


if __name__ == "__main__":
    main()