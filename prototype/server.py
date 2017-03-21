#!/usr/bin/python3
import select
import socket
import socketserver
import threading
import time

SOCKET_LIST = []

def main():
    server = ThreadedTCPServer(("0.0.0.0", 9009), ThreadedTCPRequestHandler)
    ip, port = server.server_address
    server.socket.listen(10)

    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.dameon = True
    server_thread.start()
    print("Server loop running in thread:", server_thread.name)

    try:
        # Loop forever
        while True:
            pass
    except KeyboardInterrupt:
        print("Cleaning up server....")
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
        # alias this thread's socket for readability
        my_socket = self.request
        # Add the new client socket to the socket list
        SOCKET_LIST.append(my_socket)
        # Get this client's thread
        cur_thread = threading.current_thread()
        thread_name = cur_thread.name

        running = True
        while running:
            # Receive the data from that socket
            data = str(my_socket.recv(1024), 'ascii')
            if data:
                print("Received `{}` from `{}`".format(data.strip('\n'), thread_name))
                for s in SOCKET_LIST:
                    # If this is someone else's client
                    if s != my_socket:
                        response = bytes("({}): {}".format(thread_name, data), 'ascii')
                    else:
                        response = bytes("(you): {}".format(data), 'ascii')
                    s.sendall(response)
            else:
                # Remove the socket IF it is owned by this thread
                if my_socket in SOCKET_LIST:
                    print("Removing {}".format(thread_name))
                    SOCKET_LIST.remove(my_socket)
                    running = False


## ThreadedTCPServer
#
#  A TCP server for managing connections
class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    def server_bind(self):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(self.server_address)


if __name__ == "__main__":
    main()
