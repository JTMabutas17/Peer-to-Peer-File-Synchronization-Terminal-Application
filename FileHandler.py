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