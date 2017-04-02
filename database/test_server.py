from database import Camelot_Database
from server import Camelot_Server
import json

############################### HOW TO USE THIS FILE ####################################
# INSTALL: pytest (for me I installed it via command-line using: "pip3 install pytest") #
# RUN: Just type "pytest" in the command-line while in the same directory as this file  #
#########################################################################################

def test_create_account_invalid_json():
    server = Camelot_Server()
    mydb = Camelot_Database()

    client_request = json.loads(json.dumps({
        "create_account": {
            "username_invalid": "username",
            "password": "password",
        }
    }, indent=4))

    expected_response = json.dumps({
        "error": "The JSON file sent didn't contain valid information."
    }, indent=4)

    result = server.create_account(mydb, client_request)

    assert expected_response == result
    mydb.empty_tables()

def test_create_account_username_incorrect_length():
    server = Camelot_Server()
    mydb = Camelot_Database()

    client_request = json.loads(json.dumps({
        "create_account": {
            "username": "username-----------------------------------------------",
            "password": "password",
        }
    }, indent=4))

    expected_response = json.dumps({
        "error": "The username isn't of the correct length (0 < len(username) <= 20)."
    }, indent=4)

    result = server.create_account(mydb, client_request)

    assert expected_response == result
    mydb.empty_tables()

def test_create_account_password_incorrect_length():
    server = Camelot_Server()
    mydb = Camelot_Database()

    client_request = json.loads(json.dumps({
        "create_account": {
            "username": "username",
            "password": "password-----------------------------------------------",
        }
    }, indent=4))

    expected_response = json.dumps({
        "error": "The password isn't of the correct length (0 < len(password) <= 20)."
    }, indent=4)

    result = server.create_account(mydb, client_request)

    assert expected_response == result
    mydb.empty_tables()

def test_create_account_username_already_taken():
    server = Camelot_Server()
    mydb = Camelot_Database()

    client_request = json.loads(json.dumps({
        "create_account": {
            "username": "username",
            "password": "password",
        }
    }, indent=4))

    expected_response = json.dumps({
        "error": "That username is already taken."
    }, indent=4)

    server.create_account(mydb, client_request)
    result = server.create_account(mydb, client_request)

    assert expected_response == result
    mydb.empty_tables()

def test_create_account_success():
    server = Camelot_Server()
    mydb = Camelot_Database()

    client_request = json.loads(json.dumps({
        "create_account": {
            "username": "username",
            "password": "password",
        }
    }, indent=4))

    expected_response = None

    result = server.create_account(mydb, client_request)

    assert expected_response == result
    mydb.empty_tables()

def test_login_invalid_json():
    server = Camelot_Server()
    mydb = Camelot_Database()

    client_request = json.loads(json.dumps({
        "login": {
            "username_invalid": "username",
            "password": "password",
        }
    }, indent=4))

    expected_response = json.dumps({
        "error": "The JSON file sent didn't contain valid information."
    }, indent=4)

    result = server.login(mydb, client_request)

    assert expected_response == result
    mydb.empty_tables()

def test_login_user_password_combination_not_in_database():
    server = Camelot_Server()
    mydb = Camelot_Database()

    client_request = json.loads(json.dumps({
        "login": {
            "username": "username",
            "password": "password",
        }
    }, indent=4))

    expected_response = json.dumps({
        "error": "The username/password combination do not exist in the database."
    }, indent=4)

    result = server.login(mydb, client_request)

    assert expected_response == result
    mydb.empty_tables()

def test_login_no_channels_available():
    server = Camelot_Server()
    mydb = Camelot_Database()

    client_request = json.loads(json.dumps({
        "login": {
            "username": "username",
            "password": "password",
        }
    }, indent=4))

    expected_response = json.dumps({
        "error": "No channels exist in the database."
    }, indent=4)

    mydb.create_account("username", "password")
    result = server.login(mydb, client_request)

    assert expected_response == result
    mydb.empty_tables()

def test_login_success():
    server = Camelot_Server()
    mydb = Camelot_Database()

    client_request = json.loads(json.dumps({
        "login": {
            "username": "username",
            "password": "password",
        }
    }, indent=4))

    mydb.create_account("username", "password")
    mydb.create_channel("ChannelTest", "username")

    expected_response = mydb.get_channels()
    result = server.login(mydb, client_request)

    assert expected_response == result
    mydb.empty_tables()

def test_new_message():
    server = Camelot_Server()
    mydb = Camelot_Database()

    client_request = json.loads(json.dumps({
        "new_message": {
            "channel_receiving_message": "Client Team",
            "user": "username",
            "timestamp": "2017-03-14 14:11:30",
            "message": "the actual message that the user posted"
        }
    }, indent=4))

    expected_response = json.dumps({
        "new_message": {
            "channel_receiving_message": "Client Team",
            "user": "username",
            "timestamp": "2017-03-14 14:11:30",
            "message": "the actual message that the user posted"
        }
    }, indent=4)

    result = server.new_message(mydb, client_request)

    assert expected_response == result
    mydb.empty_tables()
