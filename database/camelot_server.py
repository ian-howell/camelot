import socket
import threading
import json
from server import Camelot_Server
from database import Camelot_Database


my_clients = {}
my_threads = []
client_lock = threading.Lock()

class ClientThread(threading.Thread):
    def __init__(self, conn, addr):
        threading.Thread.__init__(self)
        self.conn = conn
        self.addr = addr
        self.server = Camelot_Server()
        self.mydb = Camelot_Database()
        self.unauthorized_function_calls = ['__init__', 'login_required']

    def run(self):
        # Global keyword needed if your wanting to change the variable in a method
        global my_clients
        connected = True

        # Get this client's thread
        cur_thread = threading.current_thread()
        thread_name = cur_thread.name

        while connected:
            # Checks for new packages from the client
            error, client_request = self.validate_request_data(thread_name)

            # If a new package was recieved from the client (and no errors occured with the package)
            if not error:

                # Attempt to carry out the clients request
                for operation in client_request.keys():
                    try:
                        if operation in self.unauthorized_function_calls:
                            raise AttributeError
                        with client_lock:
                            response = getattr(self.server, operation)(self.mydb, client_request)
                    except AttributeError:
                        response = json.dumps({
                            "error": "The JSON file sent didn't contain valid information."
                        }, indent=4)

                with client_lock:

                    # Unload the JSON into a dictionary for usage
                    check = json.loads(response)
                    new_message = False

                    # Check if JSON contains "new_message" key meaning the user wants to send a new message
                    try:
                        if check['new_message']:
                            new_message = True

                    # No new message, so just send back to the user who made the request
                    except KeyError:
                        self.conn.sendall(bytes(str(response), 'ascii'))

                    if new_message:
                        response_from_db = self.mydb.get_users_in_channel(check['new_message']['channel_receiving_message'])
                        response_from_db = json.loads(response_from_db)

                        try:
                            if response_from_db['error']:
                                response_from_db = json.dumps(response_from_db, indent=4)
                                self.conn.sendall(bytes(str(response_from_db), 'ascii'))

                        except KeyError:
                            users_to_message = [user for user in response_from_db['users_in_channel']['users']]

                            for client_thread in my_threads:
                                print("test")
                                if client_thread.server.user in users_to_message:
                                    client_thread.conn.sendall(bytes(str(response), 'ascii'))


            #If an error occured
            else:
                client_lock.acquire()

                try:
                    self.conn.sendall(bytes(str(client_request), 'ascii'))

                except BrokenPipeError:
                    print("{} disconnected.".format(thread_name))
                    my_clients.pop(self.addr)
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
    # Add some initial channels to the database
    mydb = Camelot_Database()
    mydb.insert_data('data.sql')

    host = '127.0.0.1'
    port = 12345

    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # this is for easy starting/killing the app
    soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    soc.bind((host,port))
    soc.listen(10)

    try:
        # Accept new incoming clients
        while True:
            client_socket, addr = soc.accept()
            my_clients[addr] = client_socket
            print('Got a new connection from {}'.format(addr))
            new_client_thread = ClientThread(client_socket, addr)
            new_client_thread.daemon = True
            my_threads.append(new_client_thread)
            new_client_thread.start()

    except KeyboardInterrupt:
        print('Shutting down server...')
        client_lock.acquire()
        for client in my_clients.values():
            client_request = json.dumps({
                "connection": "Broke"
            }, indent=4)
            client.sendall(bytes(str(client_request), 'ascii'))
        client_lock.release()

    soc.close()
