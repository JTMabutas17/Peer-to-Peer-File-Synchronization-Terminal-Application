import os

"""
Authors: Justin Mabutas and Joseph Cuevas
Python file for reading contents of files in bytes and creating new files from that data.
"""

def getShareableFiles():
    os.chdir("./Shareable")
    files = os.listdir()
    files.sort(key=os.path.getsize, reverse=True)
    os.chdir("./..")
    return files

# Returns dictionary with key/value pairs of file_name/file_size
def getShareableFilesAsDictionary():
    shareable_dictionary = dict()
    os.chdir("./Shareable")
    files = os.listdir()
    for file in files:
        file_size = os.path.getsize(file)
        shareable_dictionary[file]= file_size
    os.chdir("./..")
    return shareable_dictionary

# Return a unique dictionary of file_name/file_size between two dictionaries
def compareShareableFiles(host_dict, remote_dict):
    unique_dict = dict()
    for value in host_dict:
        if value not in remote_dict:
            unique_dict[value] = host_dict[value]
    return unique_dict

# Open a file as readable bytes (as opposed to text) and return the data
def getFileContentsAsBytes(file_path):
    os.chdir("./Shareable")
    file = open(file_path, "rb")
    data = file.read()
    file.close()
    os.chdir("./..")
    return data

# Open a file as writable bytes (as opposed to text) and write file_contents into it
def createFile(file_path, file_contents):
    os.chdir("./Shareable")
    file = open(file_path, "wb")
    file.write(file_contents)
    file.close()
    os.chdir("./..")

"""
Example Usage
data = getFile("JustinMabutas_Resume_2021.pdf")
createFile("Other.pdf", data)
"""

# host_dict = {"epic_seven": 101010, "pdf":5050}
# remote_dict = {"epic_seven": 101010, }
#
# print(compareShareableFiles(host_dict,remote_dict))