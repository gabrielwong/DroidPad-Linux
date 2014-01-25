'''
Created on Jan 24, 2014

@author: gabriel
'''
import bluetooth
import sys

UUID = "370a07a0-8557-11e3-9d72-0002a5d5c51b"

# Connect to a device running the app with the given name.
# Returns a socket
def connect(name = None):
    # Find matching Bluetooth services
    service_matches = bluetooth.find_service(name = name, uuid = UUID)
    
    # If there are no matches
    if len(services_matches) == 0:
        print("No services found")
        return None
    
    # Info from SDP
    first_match = service_matches[0]
    port = first_match["port"]
    name = first_match["name"]
    host = first_match["host"]
    
    # Connect to device
    print "Connecting to {name} on {host} on port {port}".format(name=name, host=host, port=port)
    sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    sock.connect((host, port))
    
    return sock

# Close the socket
def close(sock):
    sock.close()