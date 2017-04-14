import socket
import json
import threading

############ GENERAL NOTES ##############
# 'json.dumps' encodes the data into json
# 'json.loads' decodes the json data
#########################################

def bad_json():
    return json.dumps({
        "creating_channel": {
            "test":"asd"
        }
    }, indent=4)

def create_account_1():
    return json.dumps({
        "create_account": {
            "username": "username1",
            "password": "password",
        }
    }, indent=4)

def create_account_2():
    return json.dumps({
        "create_account": {
            "username": "username2",
            "password": "password",
        }
    }, indent=4)

def login_1():
    return json.dumps({
        "login": {
            "username": "username1",
            "password": "password",
        }
    }, indent=4)

def login_2():
    return json.dumps({
        "login": {
            "username": "username2",
            "password": "password",
        }
    }, indent=4)

def join_channel_1():
    return json.dumps({
        "join_channel": [
            "TestChannel1"
        ]
    }, indent=4)

def join_channel_2():
    return json.dumps({
        "join_channel": [
            "TestChannel2"
        ]
    }, indent=4)

def new_message_1():
    return json.dumps({
        "new_message": {
            "channel_receiving_message": "Client Team",
            "user": "username1",
            "timestamp": "2017-03-14 14:11:30",
            "message": "Message inside of `Client Team` channel"
        }
    }, indent=4)

def new_message_2():
    return json.dumps({
        "new_message": {
            "channel_receiving_message": "TestChannel1",
            "user": "username2",
            "timestamp": "2017-03-14 14:11:30",
            "message": "Message inside of `TestChannel1` channel"
        }
    }, indent=4)

def new_message_3():
    return json.dumps({
        "new_message": {
            "channel_receiving_message": "TestChannel2",
            "user": "username1",
            "timestamp": "2017-03-14 14:11:30",
            "message": "Message inside of `TestChannel2` channel"
        }
    }, indent=4)

def create_channel_1():
    return json.dumps({
        "create_channel": "TestChannel1"
    }, indent=4)

def create_channel_2():
    return json.dumps({
        "create_channel": "TestChannel2"
    }, indent=4)

def delete_channel():
    return json.dumps({
        "delete_channel": "some new channel name"
    }, indent=4)

def delete_account():
    return json.dumps({
        "delete_account": {
            "username": "zach",
            "password": "pass"
        }
    }, indent=4)

def get_users_in_channel():
    return json.dumps({
        "get_users_in_channel": "Client Team"
    }, indent=4)

def leave_channel():
    return json.dumps({
        "leave_channel": "Client Team"
    }, indent=4)

def change_password():
    return json.dumps({
        "change_password": {
            "username": "username",
            "current_password": "password",
            "new_password": "their new password"
        }
    }, indent=4)

def logged_in():
    return json.dumps({
        "This info doesn't matter; client shouldn't be able to access this function.": "blam"
    }, indent=4)

def __init__():
    return json.dumps({
        "This info doesn't matter; client shouldn't be able to access this function.": "blam"
    }, indent=4)

def logout():
    return json.dumps({
        "logout":"logout"
    }, indent=4)

client_lock = threading.Lock()
server_running = True

class ClientRecvThread(threading.Thread):
    def __init__(self, soc):
        threading.Thread.__init__(self)
        self.soc = soc

    def run(self):
        global server_running

        while True:
            result_bytes = soc.recv(4096) # the number means how the response can be in bytes
            result_string = json.loads(result_bytes.decode("ascii")) # the return will be in bytes, so decode

            try:
                if result_string['connection'] == 'Broke':
                    print('Server connection has been broke.')
                    server_running = False
                    return None
            except KeyError:
                print("Result from server is {}".format(result_string))

class ClientSendThread(threading.Thread):
    def __init__(self, soc):
        threading.Thread.__init__(self)
        self.soc = soc

    def run(self):
        connected = True
        # Loops while the user is connected to the server
        while connected:
            error = None

            # Loops until the user selects a function to use
            #while True:
            # Gets user input on the server function to be used
            client_request = input('Please enter a server function to use: (Type -h to get a list of server functions): \n')

            '''
            # Outputs the functions the client can use on the server
            if client_request == '-h':
                print('')
                for func in functions.keys():
                    print('- {}'.format(func))
                print('')

            else:
                break
            '''

            try:
                #client_request = functions[client_request]()
                client_request = globals()[client_request]()
            except:
                error = 'Invalid function given\n'

            if error:
                print(error)
            else:
                with client_lock:
                    soc.send(client_request.encode("ascii")) # we must encode the string to bytes


if __name__ == '__main__':
    '''
    functions = {
        'bad_json': bad_json,
        'create_account': create_account,
        'login': login,
        'join_channel': join_channel,
        'new_message': new_message,
        'create_channel': create_channel,
        'delete_channel': delete_channel,
        'delete_account': delete_account,
        'get_users_in_channel': get_users_in_channel,
        'leave_channel': leave_channel,
        'change_password': change_password
    }
    '''

    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.connect(("127.0.0.1", 12345))

    send_thread = ClientSendThread(soc)
    send_thread.daemon = True
    send_thread.start()

    recv_thread = ClientRecvThread(soc)
    recv_thread.daemon = True
    recv_thread.start()

    try:
        while server_running:
            pass
    except KeyboardInterrupt:
        pass

    print('Closing client')
    soc.close()

    '''
    server = Camelot_Server()
    mydb = Camelot_Database()
    #mydb.insert_data('data.sql')

    client_request = json.loads(test_bad_json())
    #client_request = json.loads(create_account())
    #client_request = json.loads(login())
    #client_request = json.loads(join_channel())
    #client_request = json.loads(new_message())
    #client_request = json.loads(create_channel())
    #client_request = json.loads(delete_channel())
    #client_request = json.loads(delete_account())
    #client_request = json.loads(get_users_in_channel())
    #client_request = json.loads(leave_channel())
    #client_request = json.loads(change_password())

    for operation in client_request.keys():
        try:
            response = getattr(server, operation)(mydb, client_request)
        except AttributeError:
            response = json.dumps({
                "error": "The JSON file sent didn't contain valid information."
            }, indent=4)


    # TODO ZW 3-20: Need to add a check that makes sure a client is only getting sent
    # messages if the user is a part of the specified channel.
    #response = json.dumps(client_request, indent=4)

    # TODO zw 4-1: Need to add a way to send a message to all users if a channel has
    # been deleted.
    '''
