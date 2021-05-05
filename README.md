# CECS327 TermAssignment1
## Justin Mabutas and Joseph Cuevas
---
** Files Explanation **
## 1. FileHandler.py
  *This file is responsible for three things: 
      1. Finding all of the files inside the Shareable directory
      2. Comparing two dictionaries to see which files are unique
      3. Converting the files to bytes and writing the files from byte data so they can be sent through sockets
---
2. Network Scanner.py
  *The Network Scanner has one use case with two functions
      *The use case is to obtain all of the active nodes/clients within your network
          1.**Ping Network:** Gets the host ip address and it pings all ip's from 1-255 inside your network (First three octets i.e. "255.255.255.__")
            *We do this because we need to update arp -a, if we run this command without pinging, it will not show all of the nodes in the network.
          2.**Get IP Addresses:** The *get_ip_addresses()* function saves the output of "arp -a" and finds all ip addresses whose network match the current host network.
---
3. Client.py
  *  aa
---
4. Shareable Directory/Folder
  *
