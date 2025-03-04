import socket
import threading
import time

client_running = True

def help():
    print("1. Enter the server's IP address when prompted (e.g., 127.0.0.1 for local connections). \n2. Enter the port number (default is 8080). \n3. Choose a username for the session. \n4. Once connected, you can type your messages and they will be sent to the server. \n5. To disconnect from the server at any time, type '/exit' and press Enter. \n\nCommands: \n/exit \n- Disconnect from the server. \n/whoami \n- Shows your current username. \n/help \n- Repeats this message. \n\nTips: \n- The server must be running for the client to connect. \n- Messages from the server will appear with 'Server: ' prefix. \n- Your own messages will be prefixed with '<You>'.")

def receive_messages(client_socket):
    global client_running
    while client_running:
        try:
            response = client_socket.recv(1024).decode()
            if not response:
                print("\nServer has disconnected.")
                client_running = False
                break


            print(f"\rServer: {response}") #\nEnter message: ", end="", flush=True)
            print("<You> ", end="", flush=True)

        except ConnectionResetError:
            if client_running:
                print("\nLost connection to server.")
            client_running = False
            break

def main():
    global client_running
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_ip = input("Enter server IP address: ").strip() # 127.0.0.1

  # port = int(input("Enter server port: "))
    port = 8080

  # client_username = input("Enter Username: ")
    try:
        client.connect((server_ip, port))
        print("Connected to server.")

        client_username = input("Enter your username: ").strip()
        client.send(client_username.encode())

        receive_thread = threading.Thread(target=receive_messages, args=(client,))
        receive_thread.start()
        def whoami():
            print(f"Your current username is: {client_username}")
        while client_running:
            msg = input("<You> ").strip()
            if msg.lower() == "/exit":
                print("\nDisconnecting...")
                client_running = False
                try:
                    client.send("/exit".encode())
                except:
                    pass
                time.sleep(1)
                client.close()
                break
            if msg.lower() == "/help":
                help()

            if msg.lower() == "/whoami":
                whoami()

            if client_running:
                try:
                    client.send(msg.encode())
                except:
                    print("\nConnection lost. Can't send message.")
                    client_running = False
                    break

    except ConnectionRefusedError:
        print("Failed to connect to server. Make sure server is running.")

      # print(f"<You> {msg}\n", end='', flush=True)

      #response = client.recv(1024).decode()
      #print(f"<You> {response}")

    print("Client closed.")
  #receive_thread.join()    



if __name__ == "__main__":
   main()
