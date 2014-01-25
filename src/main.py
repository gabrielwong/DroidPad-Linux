'''
Created on Jan 24, 2014

@author: gabriel
'''

import socket.tcpbluetooth

def main():
    connection = socket.tcpbluetooth.connect()
    if connection == None:
        return
    
    while True:
        pass
    
    #with open(connection, "rw") as f:
     #   print f.readline()
    

if __name__ == '__main__':
    main()