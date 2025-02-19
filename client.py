import socket
from socket import SocketOne


def main():
  client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  client.connect(('localhost, 5000'))
  print("Connected to server")

  while True:
      msg = input("Enter message: ")
      if not msg:
        break
      client.send(msg.encode())
      response = client.recv(1024).decode()
      print(f"Server says: {response}")

  client.close()