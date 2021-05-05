# CECS327 TermAssignment1
## Justin Mabutas and Joseph Cuevas
---
** Files Explanation **
## 1.FileHandler.py
  * This file is responsible for three things: 
      1. Finding all of the files inside the Shareable directory
      2. Comparing two dictionaries to see which files are unique
      3. Converting the files to bytes and writing the files from byte data so they can be sent through sockets
---
## 2.Network Scanner.py
  * The Network Scanner has one use case with two functions
      *The use case is to obtain all of the active nodes/clients within your network
          1.**Ping Network:** Gets the host ip address and it pings all ip's from 1-255 inside your network (First three octets i.e. "255.255.255.__")
            *We do this because we need to update arp -a, if we run this command without pinging, it will not show all of the nodes in the network.
          2.**Get IP Addresses:** The *get_ip_addresses()* function saves the output of "arp -a" and finds all ip addresses whose network match the current host network.
---
## 3.Client.py
  * Purpose of file: Client.py is the main file that is run for the application. It's intended purpose is to synchronize files within the shareable folder with other peers that are also running Client.py on their system.
  * **On-Run** 
    1. Program will check all available nodes for open port 5050
    2. After it scans for all nodes, it will determine whether or not there are any nodes ready to connect
       * If there aren't any nodes that are available to connect, the node itself acts as a "server" and listens for other nodes once they become available running the application
    3. If there are nodes in the network, begin the exchange of files
---
## 4. Shareable Directory/Folder
  * This folder is responsible for holding files that are desired to be shared between clients
     * We intend for the README to exist at all times so we can there is always a file being exchanged

---
# Questions 
