# Server and Client Chatroom in Python

## Introduction 
These two Python scripts provide a simple implementation of a client-server chat application. The **server script** creates a server that listens for incoming connections, while the **client script** allows users to connect to the server and send and/or receive messages to other clients on the server. The server handles multiple clients at the same time by using threads. The client can send and receive messages and commands like `/exit`, `/whoami`, and `/users`.

### Server Script:
- Listens for incoming client connections. 
- Handles multiple clients by creating a new thread for each one. 
- Allows users to chat and interact with each other in real-time. 
- Supports basic commands like `/exit` to disconnect and `/users` to list active users. 

### Client Script: 
- Connects to the server and sends messages to other clients. 
- Receives messages from the server and displays them. 
- Supports basic commands like `/exit` to disconnect and `/whoami` to display the current username.

---

### Installation
1. Clone or download the repository. 
2. Make sure Python is installed on your system and in your PATH.
3. Install any necessary dependencies (these scripts don’t require any additional packages). 

--- 

## Usage 

---

### Running the Server 
1. Run the server script in one terminal window to start the server. 

```python 
python3 server.py 
```

The server will now accept connections from clients and start handling them. It will broadcast messages to all connected clients and keep track of active users as well as the username for each user.


Then run

```python
python3 client.py
```

to join the server.

---

## Error Handling

---

## Troubleshooting

---

## Extras