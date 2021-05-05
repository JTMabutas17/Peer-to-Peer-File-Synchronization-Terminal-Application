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
# Key Feature Questions Answered
1. How does the client discover other clients on the network?
   * We do so by pinging all of the devices within the network and check the "arp -a" command. After we find all of the devices available, we then check if port 5050 (in our case) is open and ready to sync.
2. How does the client deal with matching files of the same name?
   * We deal with matching files of the same name by checking for unique files before making the exchange. Each client passes a dictionary of each file and coresponding file size to compare and identify which files are unique based on name so they can be synched between the systems.
3. How does the client determine the order of syncing with regards to the files of other clients?
   * In the case that the client.py runs (Node 1) and does not find any other nodes, it acts as the "server". Once the node is in that state, another node (Node 2) searches for available nodes through client.py on their system will find Node 1 is available to connect and goes through these steps.
     1. Node 2 sends over its dictionary
     2. Node 1 receives the dictionary and identifies which files are unique then sends Node 2 the dictionary of unique files it wants
     3. Node 2 uses that dictionary to determine which of the files to send over.
     4. Once Node 2 has finished sending its files over, it listens to receive the files from Node 1
     5. And they live happily ever after (hopefully) with synched files
4. How are files sent over sockets?
   * Files are sent over sockets by reading their data in bytes and sending it through the socket.
     * The program reads the data in bytes by opening a file in readable bytes through the following commands commands:
       ```
       file = open(file_path, "rb")
       data = file.read()
       file.close()
       ```
   *  The receiver receives the data bytes and opens a file in writeable bytes mode through the following commands:
       ```
       file = open(file_path, "wb")
       file.write(file_contents)
       file.close()
       ```
---
