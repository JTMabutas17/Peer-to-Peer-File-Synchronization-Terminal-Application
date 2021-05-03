import socket
import subprocess
import re
import threading

"""
CECS 327
Authors: Justin Mabutas and Joseph Cuevas
Python file for scanning the current network.
"""

# Function to ping all hosts in the current network.
#   We do this to update arp -a command.
def ping_network():
    host_ip = socket.gethostbyname(socket.gethostname())
    # Get the network from the host_ip with regex.
    network = re.match(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\b", host_ip).group()
    for num in range(1,255):
        # Use Popen to asynchronously run ping commands on all hosts in the current network from [1,255). Ignore output.
        subprocess.Popen("ping -n 1 " + network + str(num), shell=True, stdout=False)

# Function to get the output of arp -a. The output is then filtered for ips in the current host's network.
#   Returns the list of ips within the network, ignoring all elements of ip_to_ignore.
def get_ip_addresses():
    thread = threading.Thread(target=ping_network())
    host_ip = socket.gethostbyname(socket.gethostname())
    gateway_ip = "1"
    broadcast_ip = "255"
    network = re.match(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\b", host_ip).group()
    # Save output of arp -a to ip_addresses
    ip_addresses = subprocess.check_output("arp -a", shell=True)
    # Currently ip_addresses is a bytes-like object, so decode it to utf-8
    ip_addresses = ip_addresses.decode("utf-8")

    gateway_ip = network + gateway_ip
    broadcast_ip = network + broadcast_ip
    # Define ip_to_ignore to include host_ip, gateway_ip, and broadcast_ip
    ip_to_ignore = [host_ip, gateway_ip, broadcast_ip]
    # Use regex to find all ip addresses that match network
    ip_addresses = re.findall(network+"\d{1,3}", ip_addresses)

    # Remove all elements in ip_to_ignore
    for x in ip_to_ignore:
        try:
            ip_addresses.remove(x)
        except ValueError:
            print("Error Caught, Value not present int list: " + x)
    return ip_addresses