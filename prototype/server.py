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
        # Add the new client socket to the socket list
        SOCKET_LIST.append(self.request)
        # Get this client's thread
        cur_thread = threading.current_thread()

        while True:
            # Prompt the OS for all of the sockets which are ready to read from
            ready_to_read, ignore1, ignore2 = select.select(SOCKET_LIST,[],[],0)
            for sock in ready_to_read:
                # Receive the data from that socket
                data = str(self.request.recv(1024), 'ascii')
                if data:
                    print("Received `{}` from `{}`".format(data, sock))
                    for s in SOCKET_LIST:
                        # If this is someone else's client
                        if s != sock:
                            # response = bytes("({}): {}".format(cur_thread.name, data), 'ascii')
                            response = bytes("({}): {}".format(s.fileno(), data), 'ascii')
                        else:
                            response = bytes("(you): {}".format(data), 'ascii')
                        s.sendall(response)
                else:
                    if sock in SOCKET_LIST:
                        print("Removing {}".format(sock.fileno()))
                        # This line breaks because multiple threads are trying
                        # to remove the same socket from the SOCKET_LIST at
                        # the same time
                        SOCKET_LIST.remove(sock)


## ThreadedTCPServer
#
#  A TCP server for managing connections
class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    def server_bind(self):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(self.server_address)


if __name__ == "__main__":
    main()
