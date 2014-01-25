'''
Created on Jan 24, 2014

@author: gabriel
'''

import socket.tcpbluetooth
import socketfile

def main():
    connection = socket.tcpbluetooth.connect()
    if connection == None:
        return
    
    f = makefile(connection)
    while True:
        if f.readline() == "DroidPad 1.0":
            json = f.readline()
            
    
def makefile(socket, mode='r+b', bufsize=0):
    return socketfile._fileobject(socket, mode, bufsize)

if __name__ == '__main__':
    main()