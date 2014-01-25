'''
Created on Jan 24, 2014

@author: gabriel
'''
import bluetooth

UUID = "370a07a0-8557-11e3-9d72-0002a5d5c51b"

# Connect to a device running the app with the given name.
# Returns a socket
def connect(name = None, address = None):
    print "Searching for Bluetooth services"
    # Find matching Bluetooth services
    service_matches = bluetooth.find_service(name = name, uuid = UUID, address = address)
    
    # If there are no matches
    if len(service_matches) == 0:
        print "No services found"
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

def server():
    server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    server_sock.bind(("", 0))
    server_sock.listen(1)
    print "Listening on port 0"
    
    bluetooth.advertise_service(server_sock, "DroidPad Service", UUID)
    client_sock,address = server_sock.accept()
    print "Accepted connection from ", address
    
    return client_sock
    

# Close the socket
def close(sock):
    sock.close()

if __name__ == '__main__':
    connect()