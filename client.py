import socket
import threading
import time

def main():
  client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  server_ip = input("Enter server IP address: ")

  port = int(input("Enter server port: "))

  client_username = input("Enter Username: ")

  client.connect((server_ip, port))
  print("Connected to server")

  while True:
      msg = input("Enter message: ")
      if not msg:
        break
      client.send(msg.encode())

      if msg.lower() == "/exit":
         print("Disconnecting...")
         time.sleep(1)
         break

      response = client.recv(1024).decode()
      print(f"<You> {response}")

  client.close()

if __name__ == "__main__":
   main()