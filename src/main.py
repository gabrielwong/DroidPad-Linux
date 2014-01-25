'''
Created on Jan 24, 2014

@author: gabriel
'''

import json
import socket.tcpbluetooth
import socketfile
import eventhandler

def main():
    connection = socket.tcpbluetooth.connect()
    if connection == None:
        return
    
    f = makefile(connection)
    
    for line in f:
        event = json.load(line)
        eventhandler.handle(event)
    
    print "Stream closed"
            
    
def makefile(socket, mode='r+b', bufsize=0):
    return socketfile._fileobject(socket, mode, bufsize)

if __name__ == '__main__':
    main()