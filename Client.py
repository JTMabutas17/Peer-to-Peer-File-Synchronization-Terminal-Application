from NetworkScanner import get_ip_addresses
from FileHandler import *
import socket
import threading
import pickle

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
host_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_client.bind((CLIENT_IP, 5050))

# Start. Gets called if there are no other peers in the network.
def start():
    host_client.listen()
    print(f"[LISTENING] Currently listening on {SERVER}")
    while True:
        conn, addr = host_client.accept()
        thread = threading.Thread(target=handle_client, args=(host_client, conn, addr))
        thread.start()
        print(f"[CONNECTED] {addr} has connected")
    exit(0)

# Function for handling an incoming client.
# While true, we expect to receive 4 messages per file, followed by a message to indicate whether to continue.
# Messages between sockets need to be encoded before sending and decoded after receiving.
#   file_data comes as a bytes-like objects and thus does not need to be encoded/decoded.
def handle_client(client, conn, addr):
    method = conn.recv(2048).decode('utf-8')
    if method == "!ACCEPT-DICTIONARY":
        host_file_dict = getShareableFilesAsDictionary()
        while True:
            remote_file_dictionary_length = conn.recv(64).decode('utf-8')
            if remote_file_dictionary_length:
                remote_file_dictionary_length = int(remote_file_dictionary_length)
                conn.send("[1/2] Remote Dictionary Length Received".encode('utf-8'))
                remote_file_dictionary = conn.recv(remote_file_dictionary_length)
                conn.send("[2/2] Remote Dictionary Received".encode('utf-8'))
                remote_file_dictionary = pickle.loads(remote_file_dictionary)
                host_unique_file_dict = compareShareableFiles(host_file_dict, remote_file_dictionary)
                remote_unique_file_dict = compareShareableFiles(remote_file_dictionary, host_file_dict)
                print("Remote Unique File Dictionary:",remote_unique_file_dict)
                print("Host Unique File Dictionary:", host_unique_file_dict)
                remote_unique_file_dict = pickle.dumps(remote_unique_file_dict)
                sendMessageWithHeader(conn, remote_unique_file_dict)
                break
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
            elif continue_download == "!KILL":
                print(f"[DISCONNECTED] {addr} has disconnected")
                conn.close()
                return
    temp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Socket object
    temp_client.connect((addr[0], PORT))
    temp_client.send("!IGNORE-DICTIONARY".encode('utf-8'))
    sendFilesByDictionary(temp_client, host_unique_file_dict, True)
    print(f"[DISCONNECTED] {addr} has disconnected")
    conn.close()
    return

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
    # [1/4] File Name Length Received
    # [2/4] File Name Received
    sendMessageWithHeader(client,bytes(file_name,'utf-8'))
    # Send file_data
    # [3/4] File Data Length Received
    # [4/4] File Data Received
    sendMessageWithHeader(client,file_data)
    # [COMPLETE] File Created
    print(client.recv(2048).decode('utf-8'))

def sendFilesByList(client, files):
    for file in files:
        file_data = getFileContentsAsBytes(file)
        t = threading.Thread(target=send_file, args=(client, file, file_data))
        t.start()
        t.join()
        if file == files[-1]:
            sendMessage(client, "!DISCONNECT")
        else:
            sendMessage(client, "!CONTINUTE")

def sendFilesByDictionary(client, files, terminate_cycle):
    for i, (file_name,file_size) in enumerate(files.items()):
        file_data = getFileContentsAsBytes(file_name)
        t = threading.Thread(target=send_file, args=(client, file_name, file_data))
        t.start()
        t.join()
        if i == len(files)-1:
            if terminate_cycle:
                sendMessage(client, bytes("!KILL", 'utf-8'))
            else:
                sendMessage(client, bytes("!DISCONNECT",'utf-8'))
        else:
            sendMessage(client, bytes("!CONTINUE",'utf-8'))

def sendFileDictionary(client):
    file_dict = getShareableFilesAsDictionary()
    file_data_pickled = pickle.dumps(file_dict)
    sendMessageWithHeader(client, file_data_pickled)

# For sending raw messages
# Use this when message < 2048
def sendMessage(client, message):
    client.send(message)

# For sending messages with variable message sizes
# Use this for sending files
def sendMessageWithHeader(client, message):
    message_length = len(message)
    send_length = bytes(str(message_length), 'utf-8')
    send_length += b' ' * (64 - len(send_length))
    client.send(send_length)
    print(client.recv(2048).decode('utf-8'))
    client.send(message)
    print(client.recv(2048).decode('utf-8'))

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

    # If nodes is empty, begin listening
    if not nodes:
        print("[STARTING] Client is starting...")
        start()
    else:
        for node in nodes:
            remote_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Socket object
            remote_client.connect(node)
            remote_client.send("!ACCEPT-DICTIONARY".encode('utf-8'))
            sendFileDictionary(remote_client)
            remote_file_dictionary_length = remote_client.recv(64).decode('utf-8')
            remote_file_dictionary_length = int(remote_file_dictionary_length)
            remote_client.send("[1/2] Remote Dictionary Length Received".encode('utf-8'))
            remote_file_dictionary = remote_client.recv(remote_file_dictionary_length)
            remote_client.send("[2/2] Remote Dictionary Received".encode('utf-8'))
            remote_file_dictionary = pickle.loads(remote_file_dictionary)
            sendFilesByDictionary(remote_client, remote_file_dictionary, False)
        print("[STARTING] Client is starting...")
        start()
