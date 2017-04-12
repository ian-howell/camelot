#!/usr/bin/python3
import json
import select
import socket
import socketserver
import threading
import time
from server import Camelot_Server
from database import Camelot_Database

global SOCKET_LIST
SOCKET_LIST = []

def main():
    mydb = Camelot_Database()
    mydb.insert_data('tables.sql')

    server = ThreadedTCPServer(("127.0.0.1", 12345), ThreadedTCPRequestHandler)
    ip, port = server.server_address
    server.socket.listen(10)

    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.dameon = False
    server_thread.start()
    print("Server loop running in thread:", server_thread.name)

    try:
        # Loop forever
        while True:
            pass
    except KeyboardInterrupt:
        print("Cleaning up server....")

        # Need to add something that disconnects all threads here

        server.shutdown()
        server.server_close()
        print("Done! Goodbye")


## ThreadedTCPRequestHandler
#
#  A TCP Request handler to be used by a TCP server
class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):

    ## handle
    #
    #  Recieve and manage incoming requests
    #  @param self The object pointer
    def handle(self):
        global SOCKET_LIST
        user = None
        connected = True

        # alias this thread's socket for readability
        my_socket = self.request
        # Add the new client socket to the socket list
        SOCKET_LIST.append(my_socket)
        # Get this client's thread
        cur_thread = threading.current_thread()
        thread_name = cur_thread.name

        # Gives access to server functions and accessing the database
        server = Camelot_Server()
        mydb = Camelot_Database()

        while connected:
            #response = None
            #error = None

            # Checks for new packages from the client
            client_request = self.recieve_json_package(my_socket, thread_name)
            print('test')
            # If a new package was recieved from the client (and no errors occured with the package)
            if client_request:

                # Attempt to carry out the clients request
                for operation in client_request.keys():
                    try:
                        response = getattr(server, operation)(mydb, client_request)
                    except AttributeError:
                        response = json.dumps({
                            "error": "The JSON file sent didn't contain valid information."
                        }, indent=4)

                if response:
                    for socket in SOCKET_LIST:
                        socket.sendall(bytes(response, 'ascii'))


    def validate_request_data(self, my_socket, thread_name):
        error = None
        #print("Received `{}` from `{}`".format(request.strip('\n'), thread_name))

        try:
            # Receive the data from that socket
            request = json.loads(str(my_socket.recv(1024), 'ascii'))
            #print("Received `{}` from `{}`".format(request.strip('\n'), thread_name))
            #request = bytes(client_request, 'ascii')
        except:
            error = True
            request = bytes(json.dumps({
                "error": "Something went wrong"
                }, indent=4), 'ascii')

        return (error, request)


    # Returns: None if no new package recieved or if there was an error, otherwise returns a decoded a JSON package
    def recieve_json_package(self, my_socket, thread_name):
        # Receive the data from that socket
        #client_request = str(my_socket.recv(1024), 'ascii')

        # Checks for new information from the client
        #if client_request:
        error, request = self.validate_request_data(my_socket, thread_name)

        # If there was an error, send the client a JSON-encoded error message
        if error:
            my_socket.sendall(request)
            return None
        else:
            return request

## ThreadedTCPServer
#
#  A TCP server for managing connections
class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    def server_bind(self):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(self.server_address)


if __name__ == "__main__":
    main()
