from database import Camelot_Database
import json


############ GENERAL NOTES ##############
# 'json.dumps' encodes the data into json
# 'json.loads' decodes the json data
#########################################

def test_client_create_account():
    return json.dumps({
        "create_account": {
            "username": "zach",
            "password": "password",
        }
    }, indent=4)

def test_client_login():
    return json.dumps({
        "login": {
            "username": "username",
            "password": "password",
        }
    }, indent=4)

def test_client_join_channels():
    return json.dumps({
        "join_channel": [
            "Client Team",
            "Server Team"
        ]
    }, indent=4)

def test_client_new_message():
    return json.dumps({
        "new_message": {
            "channel_receiving_message": "Client Team",
            "user": "username",
            "timestamp": "2017-03-14 14:11:30",
            "message": "the actual message that the user posted"
        }
    }, indent=4)

def test_client_create_channel():
    return json.dumps({
        "create_channel": "some new channel name"
    }, indent=4)

def test_client_delete_channel():
    return json.dumps({
        "delete_channel": "some new channel name"
    }, indent=4)

def test_client_delete_account():
    return json.dumps({
        "delete_account": {
            "username": "zach",
            "password": "pass"
        }
    }, indent=4)

def test_client_get_users_in_channel():
    return json.dumps({
        "get_users_in_channel": "Client Team"
    }, indent=4)

def test_client_leave_channel():
    return json.dumps({
        "leave_channel": "Client Team"
    }, indent=4)

def leave_channel(mydb, client_request):
    channel_name = client_request['leave_channel']

    # Eventaully, when the server is working, you'll grab the user making the request
    # and set it to the admin. A check will also need to be done to make sure that
    # a session has a user
    #user = session.user
    user = "zach" #Temporary

    return mydb.leave_channel(channel_name, user)

def get_users_in_channel(mydb, client_request):
    try:
        channel_name = client_request['get_users_in_channel']
    except KeyError:
        return json.dumps({
            "error": "The JSON file sent didn't contain valid information."
        }, indent=4)

    return mydb.get_users_in_channel(channel_name)

def delete_account(mydb, client_request):
    # Check that no one is logged in under the given username
    # Checks what channels the user is an admin of because those channels
    # will be deleted; these channels need to be known so that users can
    # be notified of channels that are deleted.

    try:
        username = client_request['delete_account']['username']
        password = client_request['delete_account']['password']
    except KeyError:
        return json.dumps({
            "error": "The JSON file sent didn't contain valid information."
        }, indent=4)

    return mydb.delete_account(username, password)

def delete_channel(mydb, client_request):
    channel_name = client_request['delete_channel']

    # Eventaully, when the server is working, you'll grab the user making the request
    # and set it to the admin. A check will also need to be done to make sure that
    # a session has a user
    #user = session.user
    user = "username" #Temporary

    return mydb.delete_channel(channel_name, user)

def create_channel(mydb, client_request):
    channel_name = client_request['create_channel']

    # Eventaully, when the server is working, you'll grab the user making the request
    # and set it to the admin. A check will also need to be done to make sure that
    # a session has a user
    #admin = session.user
    admin = "username" #Temporary

    return mydb.create_channel(channel_name, admin)

# NOTE: Some variable will also need to be passed to identify which
#       user is trying to join a channel. I'm guessing this variable
#       will be created when the client logs into the server.
def join_channel(mydb, client_request):

    # For now, I'll assume with a local variable the client's username
    # Eventaully, this will come from session.user
    username = 'zach'

    # Makes sure there are channels for the user to join
    current_channels_available = mydb.get_channels()
    if 'error' in current_channels_available.keys():
        return current_channels_available

    channels_user_wants_to_join = [channel for channel in client_request['join_channel']]

    # Make sure the user isn't trying to join invalid channels
    for channel in channels_user_wants_to_join:
        if channel not in current_channels_available['channels']:
            return json.dumps({
                "error": "The user is trying to join a channel that doesn't exist."
            }, indent=4)

    # Connects the user to the specified channels and stores the information in the database
    mydb.add_channels_to_user_info(username, channels_user_wants_to_join)

def login(mydb, client_request):
    # Makes sure the user is sending valid information
    if client_request['login']['username'] and client_request['login']['password']:
        client_username = client_request['login']['username']
        client_password = client_request['login']['password']

        result = mydb.check_username_password(client_username, client_password)
        if result:
            return result
    else:
        return json.dumps({
            "error": "The JSON file sent didn't contain valid information."
        }, indent=4)

def create_account(mydb, client_request):
    if client_request['create_account']['username'] and client_request['create_account']['password']:
        client_username = client_request['create_account']['username']
        client_password = client_request['create_account']['password']

        result = mydb.create_account(client_username, client_password)
        if result:
            return result
    else:
        return json.dumps({
            "error": "The JSON file sent didn't contain valid information."
        }, indent=4)

def send_to_client(response):
    print("This is what will get sent to the client:\n")
    print(response)
    print('')

if __name__ == '__main__':
    mydb = Camelot_Database()
    mydb.create_tables('tables.sql')
    #mydb.insert_data('data.sql')

    #client_request = json.loads(test_client_create_account())
    #client_request = json.loads(test_client_login())
    #client_request = json.loads(test_client_join_channels())
    #client_request = json.loads(test_client_new_message())
    #client_request = json.loads(test_client_create_channel())
    #client_request = json.loads(test_client_delete_channel())
    #client_request = json.loads(test_client_delete_account())
    #client_request = json.loads(test_client_get_users_in_channel())
    client_request = json.loads(test_client_leave_channel())

    for operation in client_request.keys():
        if operation == 'create_account':
            response = create_account(mydb, client_request)
        elif operation == 'login':
            response = login(mydb, client_request)
        elif operation == 'join_channel':
            response = join_channel(mydb, client_request)
        elif operation == 'new_message':
            # TODO ZW 3-20: Need to add a check that makes sure a client is only getting sent
            # messages if the user is a part of the specified channel.
            response = json.dumps(client_request, indent=4)
        elif operation == 'create_channel':
            response = create_channel(mydb, client_request)
        elif operation == 'delete_channel':
            # TODO zw 4-1: Need to add a way to send a message to all users if a channel has
            # been deleted.
            response = delete_channel(mydb, client_request)
        elif operation == 'delete_account':
            response = delete_account(mydb, client_request)
        elif operation == 'get_users_in_channel':
            response = get_users_in_channel(mydb, client_request)
        elif operation == 'leave_channel':
            response = leave_channel(mydb, client_request)
        else:
            response = json.dumps({
                "error": "The JSON file sent didn't contain valid information."
            }, indent=4)

    if response:
        send_to_client(response)
