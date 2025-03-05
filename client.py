import socket
import threading
import time

client_running = True # Set client_running to True

# Function that prints help instructions
def help():
    print("1. Enter the server's IP address when prompted (e.g., 127.0.0.1 for local connections). \n2. Enter the port number (default is 8080). \n3. Choose a username for the session. \n4. Once connected, you can type your messages and they will be sent to the server. \n5. To disconnect from the server at any time, type '/exit' and press Enter. \n\nCommands: \n/exit \n- Disconnect from the server. \n/whoami \n- Shows your current username. \n/help \n- Repeats this message. \n/users \n- Shows the list of currently connected users. \n\nTips: \n- The server must be running for the client to connect. \n- Messages from the server will appear with 'Server: ' prefix. \n- Your own messages will be prefixed with '<You>'.")

# Function to recieve messages from the server
def receive_messages(client_socket):
    global client_running
    while client_running: # Keep running until client_running is set to False
        try:
            response = client_socket.recv(1024).decode() # Recieve message from server
            if not response: # if no response, server might have disconnected
                print(f"\n{client_username} has disconnected.") # Notify clients
                break
            print(f"\r{response}\n<You> ", end="", flush=True) # Print received message
        except (ConnectionResetError, ConnectionAbortedError): # If connection is lost
            if client_running: # Only show error if client is still running
                print("\nLost connection to the server.")
            break # Exit loop if connection is lost
        except Exception as e: # Catch other errors
            print(f"\nError receiving message: {e}")
            break # Exit loop if error

# Function that runs the client portion
def main():
    global client_running, client_username # Use global variables for client running and client's username
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create a socket object

    server_ip = input("Enter server IP address: ").strip() # Enter IP Address (Local: 127.0.0.1)

    port = 8080 # Default port is 8080


    try:
        client.connect((server_ip, port)) # Connect to server at the given IP and port
        print("Connected to server.") # Notifys user that user has connected

        client_username = input("Enter your username: ").strip() # Ask user for username and store it
        client.send(client_username.encode()) # Send username to server

        # Start a new thread to receive messages from the server
        receive_thread = threading.Thread(target=receive_messages, args=(client,)) 
        receive_thread.start()

        # Function to show current username
        def whoami():
            print(f"Your current username is: {client_username}")

        while client_running: # Keep running until client_running = False
            msg = input("<You> ").strip() # Get input message from the user

            if msg.lower() == "/exit": # Check if user wants to disconnect
                print("\nDisconnecting...") # Prints disconnecting message
                client_running = False # Stop the client
                try:
                    client.send("/exit".encode()) # Send exit command to server
                except:
                    pass
                time.sleep(1) # Wait one second before continuing
                break # Exit the while loop

            if msg.lower() == "/help": # Check if user wants help and instructions
                help() # Prints help message

            elif msg.lower() == "/whoami": # Check if user wants to see own username
                whoami() # Prints user's username

            elif msg.lower() == "/users": # Check if user wants to see list of current active users
                try:
                    client.send("/users".encode()) # Send request to server
                except:
                    print("\nConnection lost. Can't send message.") # Prints error message
                    client_running = False # Stop the client
                    break

            elif client_running: # If client is still running
                try:
                    client.send(msg.encode()) # Send message to the server
                except:
                    print("\nConnection lost. Can't send message.") # Prints error message if connection is lost
                    client_running = False # Stops the client
                    break

    except ConnectionRefusedError: # Handles server connection refusal
        print("Failed to connect to server. Make sure server is running.")

    finally:
        client.close() # Close the client socket
        receive_thread.join() # Wait for the receiving thread to finish
        print("Client closed.") # Notify user that server is closed    


# Start the main function if the script is run
if __name__ == "__main__":
   main()