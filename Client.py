from NetworkScanner import get_ip_addresses
from FileHandler import *
import socket
import threading

"""
Authors: Justin Mabutas and Joseph Cuevas
Client Application
Synchronized files should be in the Shareable directory.
Running the application will scan all nodes in the network.
If the node has an open port (5050), synchronize with them.
Otherwise, listen so that other peers can synchronize with you.
"""

PORT = 5050
CLIENT_IP = socket.gethostbyname(socket.gethostname())
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.bind((CLIENT_IP, 5050))

# Start. Gets called if there are no other peers in the network.
def start():
    client.listen()
    print(f"[LISTENING] Currently listening on {SERVER}")
    while True:
        conn, addr = client.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[CONNECTED] {conn} has connected")
    exit(0)

# Function for handling an incoming client.
# While true, we expect to receive 4 messages per file, followed by a message to indicate whether to continue.
# Messages between sockets need to be encoded before sending and decoded after receiving.
#   file_data comes as a bytes-like objects and thus does not need to be encoded/decoded.
def handle_client(conn, addr):
    while True:
        file_name_length = conn.recv(64).decode('utf-8')
        if file_name_length:
            conn.send("[1/4] File Name Length Received".encode('utf-8'))
            file_name_length = int(file_name_length)
            file_name = conn.recv(file_name_length)
            conn.send("[2/4] File Name Received".encode('utf-8'))
            file_name = file_name.decode('utf-8')
            file_data_length = conn.recv(64).decode('utf-8')
            conn.send("[3/4] File Data Length Received".encode('utf-8'))
            file_data_length = int(file_data_length)
            file_data = conn.recv(file_data_length)
            conn.send("[4/4] File Data Received".encode('utf-8'))
            createFile(file_name, file_data)
            conn.send("[COMPLETE] File Created".encode('utf-8'))
            continue_download = conn.recv(64).decode('utf-8')
            if continue_download == "!DISCONNECT":
                break
    print(f"[DISCONNECTED] {conn} has disconnected")
    conn.close()

# Function for checking whether a host has an open port (5050)
# We use this in conjunction with NetworkScanner to check the ports of only the hosts in our network from arp.
def check_node_port(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    location = (ip, port)
    check = s.connect_ex(location)
    if(check == 0):
        print(f"{ip}: Port {port} open")
        nodes.append(location)
    s.close()

# The function for sending a file to a client.
def send_file(client, file_name, file_data):
    print(f"[SENDING] Sending {file_name}")
    # Send file_name
    fn = bytes(file_name, 'utf-8')
    fn_length = len(fn)
    send_length = bytes(str(fn_length), 'utf-8')
    send_length += b' ' * (64 - len(send_length))
    client.send(send_length)
    print(client.recv(2048).decode('utf-8'))
    client.send(fn)
    print(client.recv(2048).decode('utf-8'))
    # Send file_data
    file_data_length = len(file_data)
    send_length = str(file_data_length).encode('utf-8')
    send_length += b' ' * (64 - len(send_length))
    client.send(bytes(send_length))
    print(client.recv(2048).decode('utf-8'))
    client.send(bytes(file_data))
    print(client.recv(2048).decode('utf-8'))
    # Receive reponse
    print(client.recv(2048).decode('utf-8'))

def notifyNewMessage(client):
    client.send("!NEW MESSAGE".encode('utf-8'))
def sendDisconnectMessage(client):
    client.send("!DISCONNECT".encode('utf-8'))

if __name__ == '__main__':
    host = socket.gethostname()  # Get local machine name
    SERVER = socket.gethostbyname(socket.gethostname())
    port = 5050  # Reserve a port for your service.

    threads = []
    ip_addresses = get_ip_addresses()

    nodes = []
    print(f"[CHECKING] Checking all available nodes for open port {port}")
    for ip in range(len(ip_addresses)):
        t = threading.Thread(target=check_node_port, args=(ip_addresses[ip], port))
        threads.append(t)
        t.start()

    for thread in threads:
        t.join()
    print(f"[CHECKING COMPLETE] ")

    if not nodes:
        print("[STARTING] Client is starting...")
        start()
    for node in nodes:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Socket object
        server.connect(node)
        files = getShareableFiles()
        for file_name in files:
            file_data = getFileContentsAsBytes(file_name)
            t = threading.Thread(target=send_file, args=(server,file_name,file_data))
            t.start()
            t.join()
            if file_name == files[-1]:
                sendDisconnectMessage(server)
            else:
                notifyNewMessage(server)