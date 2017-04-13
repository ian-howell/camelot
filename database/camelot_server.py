import socket
import threading
import json
from server import Camelot_Server
from database import Camelot_Database

global MY_CLIENTS
MY_CLIENTS = {}
#global my_threads
#my_threads = []
client_lock = threading.Lock()

class ClientThread(threading.Thread):
    def __init__(self, conn, addr):
        threading.Thread.__init__(self)
        self.conn = conn
        self.addr = addr

    def run(self):
        #global MY_CLIENTS
        user = None
        connected = True

        # Get this client's thread
        cur_thread = threading.current_thread()
        thread_name = cur_thread.name

        # Gives access to server functions and accessing the database
        server = Camelot_Server()
        mydb = Camelot_Database()

        while connected:

            # Checks for new packages from the client
            error, client_request = self.validate_request_data(thread_name)

            # If a new package was recieved from the client (and no errors occured with the package)
            if not error:

                # Attempt to carry out the clients request
                for operation in client_request.keys():
                    try:
                        with client_lock:
                            response = getattr(server, operation)(mydb, client_request)
                    except AttributeError:
                        response = json.dumps({
                            "error": "The JSON file sent didn't contain valid information."
                        }, indent=4)

                if response:
                    with client_lock:
                        for client_conn in MY_CLIENTS.values():
                            client_conn.sendall(bytes(str(response), 'ascii'))

            #If an error occured
            else:
                client_lock.acquire()

                try:
                    self.conn.sendall(bytes(str(client_request), 'ascii'))

                except BrokenPipeError:
                    print("{} disconnected.".format(thread_name))
                    MY_CLIENTS.pop(self.addr)
                    client_lock.release()
                    return None

                client_lock.release()

    def validate_request_data(self, thread_name):
        error = False

        try:
            # Receive the data from that socket
            request = json.loads(self.conn.recv(1024).decode('ascii'))
            print("Received `{}` from `{}`".format(json.dumps(request), thread_name))

        except:
            error = True
            request = json.dumps({
                "error": "Something went wrong"
                }, indent=4)

        return (error, request)

if __name__ == '__main__':
    host = '127.0.0.1'
    port = 12345
    my_threads = []

    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # this is for easy starting/killing the app
    soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    soc.bind((host,port))
    soc.listen(10)

    try:
        # Accept new incoming clients
        while True:
            client_socket, addr = soc.accept()
            MY_CLIENTS[addr] = client_socket
            print('Got a new connection from {}'.format(addr))
            new_client_thread = ClientThread(client_socket, addr)
            new_client_thread.daemon = True
            my_threads.append(new_client_thread)
            new_client_thread.start()

    except KeyboardInterrupt:
        print('Shutting down server...')
        client_lock.acquire()
        for client in MY_CLIENTS.values():
            client_request = json.dumps({
                "connection": "Broke"
            }, indent=4)
            client.sendall(bytes(str(client_request), 'ascii'))
        client_lock.release()

    soc.close()

    # Join all threads
    #for thread in my_threads:
    #    thread.join()
