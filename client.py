import socket
import threading
import time

def main():
  client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  client.connect(('localhost', 5000))
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
      print(f"Server says: {response}")

  client.close()

if __name__ == "__main__":
   main()