'''
Created on Jan 24, 2014

@author: gabriel
'''

import socket.tcpbluetooth
import socketfile._fileobject

def main():
    connection = socket.tcpbluetooth.connect()
    if connection == None:
        return
    
    f = makefile(connection)
    while True:
        print f.readline()
    
def makefile(socket, mode='r+b', bufsize=0):
    return socketfile._fileobject(socket, mode, bufsize)

if __name__ == '__main__':
    main()