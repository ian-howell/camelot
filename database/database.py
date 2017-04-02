import psycopg2
from sys import exit
import json

## Camelot_Database
#
#  This class provides an interface with the Camelot Database
class Camelot_Database():

    def __init__(self):
        pass

    ## Makes a connection to database
    #
    #  @return The connection object
    def make_connection(self):
        try:
            conn = psycopg2.connect("dbname='camelot' host='localhost'")
        except:
            exit("Unable to connect to the database")

        return conn

    ## Adds a user to the database
    #
    #  @param self The object pointer
    #  @param username The name (string) of the user to add
    #  @param password The password (string) to be associated with this user
    #  @return None on success, a JSON object with failure reason otherwise
    def create_account(self, username, password):
        conn = self.make_connection()
        cur = conn.cursor()
        error = None

        # Makes sure the username isn't already taken
        cur.execute('''
        SELECT userid
        FROM "USER"
        WHERE userid='{}'
        '''.format(username))

        if cur.rowcount:
            error = "That username is already taken."

        # Checks the lengths of the username & password
        elif len(username) > 20 or len(username) < 1:
            error = "The username isn't of the correct length (0 < len(username) <= 20)."
        elif len(password) > 20 or len(username) < 1:
            error = "The password isn't of the correct length (0 < len(password) <= 20)."

        # If any error occured
        if error:
            self.commit_and_close_connection(conn)
            return json.dumps({
                "error": error
            })

        # If no errors occured, create the account
        cur.execute('''INSERT INTO "USER" VALUES ('{}', '{}')'''.format(username, password))
        self.commit_and_close_connection(conn)

    ## Checks that the username & password are a match in the database
    #
    #  @param self The object pointer
    #  @param username The name (string) of the user to check
    #  @param password The password (string) to be associated with this user
    #  @return A JSON object containing a list of channels on success, or an error code otherwise
    def check_username_password(self, username, password):
        conn = self.make_connection()
        cur = conn.cursor()

        cur.execute('''
        SELECT userid, password
        FROM "USER"
        WHERE userid='{}' AND password='{}'
        '''.format(username, password))

        rows = cur.fetchall()
        if not rows:
            self.commit_and_close_connection(conn)
            return json.dumps({
                "error": "The username/password combination do not exist in the database."
            }, indent=4)

        # TODO IH 3-19: This should probably be in its own function
        # Actually, isn't this just a copy-paste of the get_channels function?
        # Return back to the user the channels in the database
        cur.execute('''
        SELECT channelid
        FROM "CHANNEL"
        ''')

        rows = cur.fetchall()
        if not rows:
            self.commit_and_close_connection(conn)
            return json.dumps({
                "error": "No channels exist in the database."
            }, indent=4)

        json_to_be_sent = {"channels": []}
        for channel in rows:
            json_to_be_sent['channels'].append(channel[0])

        self.commit_and_close_connection(conn)
        return json.dumps(json_to_be_sent, indent=4)

    ## Gets the current channels in the database
    #
    #  @param self The object pointer
    #  @return A JSON object containing a list of channels on success, or an error code otherwise
    def get_channels(self):
        conn = self.make_connection()
        cur = conn.cursor()

        cur.execute('''
        SELECT channelid
        FROM "CHANNEL"
        ''')

        rows = cur.fetchall()
        if not rows:
            self.commit_and_close_connection(conn)
            return json.dumps({
                "error": "No channels exist in the database."
            }, indent=4)

        channels = {"channels": []}
        for channel in rows:
            channels['channels'].append(channel[0])

        self.commit_and_close_connection(conn)
        return channels

    ## Adds to "CHANNELS_JOINED" table in the database; adds the
    #  channels that the user wants to join.
    #
    #  @param self The object pointer
    #  @param username The user to add to the channels
    #  @param channels The list of channels to add the user to
    def add_channels_to_user_info(self, username, channels):
        conn = self.make_connection()
        cur = conn.cursor()

        for channel in channels:
            # TODO ZW 3-20: Need to add an error handler for if the user has already joined
            # a channel, and is trying to join it again.
            cur.execute('''INSERT INTO "CHANNELS_JOINED" VALUES ('{}', '{}')'''.format(username, channel))

        self.commit_and_close_connection(conn)

    ## Creates a channel in the database
    #
    # @param self The object pointer
    # @param channel_name The name of the channel to be created
    # @param admin The username of the creator of the channel
    # @return A JSON object containing an error if there is one, none if successful
    def create_channel(self, channel_name, admin):
        conn = self.make_connection()
        cur = conn.cursor()

        if len(channel_name) > 40 or len(channel_name) < 1:
            self.commit_and_close_connection(conn)
            return json.dumps({
                "error": "The name of the channel isn't of the correct length (0 < len(channel_name) <= 40)."
            }, indent=4)

        cur.execute('''INSERT INTO "CHANNEL" VALUES ('{}', '{}')'''.format(channel_name, admin))
        self.commit_and_close_connection(conn)


    ## Removes a channel from the database
    #
    # @param self The object pointer
    # @param channel_name The channel to be removed
    # @param user The user calling the function
    # @return On success returns None, else returns a json object containing the error
    def delete_channel(self, channel_name, user):
        conn = self.make_connection()
        cur = conn.cursor()

        # Checks if the channel exists in the database
        cur.execute('''
        SELECT channelid
        FROM "CHANNEL"
        WHERE channelid='{}'
        '''.format(channel_name))

        if cur.rowcount != 1:
            self.commit_and_close_connection(conn)
            return json.dumps({
                "error": "The specified channel was not found."
            }, indent=4)

        # Checks if the user trying to delete the channel, is the admin of the channel
        cur.execute('''
        SELECT channelid
        FROM "CHANNEL"
        WHERE channelid='{}' AND admin='{}'
        '''.format(channel_name, user))

        if cur.rowcount != 1:
            self.commit_and_close_connection(conn)
            return json.dumps({
                "error": "The user trying to delete the channel isn't the admin of the channel."
            }, indent=4)

        # If no errors occur, delete the channel
        cur.execute('''
        DELETE FROM "CHANNEL"
        WHERE channelid='{}'
        '''.format(channel_name))

        self.commit_and_close_connection(conn)

    ## Removes a user from the database
    #
    # @param self The object pointer
    # @param username The username to be deleted
    # @param password The password to be associated with the username
    # @return On success returns None, else returns a JSON object containing the error
    def delete_account(self, username, password):
        conn = self.make_connection()
        cur = conn.cursor()

        # Check for username and password are in database
        cur.execute('''
        SELECT userid
        FROM "USER"
        WHERE userid='{}' AND password='{}'
        '''.format(username, password))

        if cur.rowcount != 1:
            self.commit_and_close_connection(conn)
            return json.dumps({
                "error": "The username/password combination is incorrect."
            })

        # If no errors occur, delete the account
        cur.execute('''
        DELETE FROM "USER"
        WHERE userid='{}'
        '''.format(username))

        self.commit_and_close_connection(conn)

    ## Gets all over the users in a specified channel
    #
    # @param self The object pointer
    # @param channel_name The channel specified for getting the users of
    # @return On success returns None, else returns a JSON object containing the error
    def get_users_in_channel(self, channel_name):
        conn = self.make_connection()
        cur = conn.cursor()

        cur.execute('''
        SELECT userid
        FROM "CHANNELS_JOINED"
        WHERE channelid='{}'
        '''.format(channel_name))
        rows = cur.fetchall()
        result = {
            "users_in_channel": {
                "channel": channel_name,
                "users": []
            }
        }

        for user in rows:
            result['users_in_channel']['users'].append(user[0])

        self.commit_and_close_connection(conn)
        return json.dumps(result, indent=4)

    ## Creates tables in database
    #
    #  @param self The object pointer
    #  @param filename The SQL file to pull table generation from
    def create_tables(self, filename):
        # TODO IH 3-19: We should consider combining the following 2 functions into one.
        # Maybe something like `execute_sql_script`?
        conn = self.make_connection()
        cur = conn.cursor()
        cur.execute(open(filename, 'r').read())
        self.commit_and_close_connection(conn)

    ## Readies initial data for database
    #
    #  @param self The object pointer
    #  @param filename The SQL file to pull table insertion data from
    def insert_data(self, filename):
        conn = self.make_connection()
        cur = conn.cursor()
        cur.execute(open(filename, 'r').read())
        self.commit_and_close_connection(conn)

    ## Empties all of the current database tables (created by create_tables)
    #
    #  @param self The object pointer
    def empty_tables(self, ):
        conn = self.make_connection()
        cur = conn.cursor()
        cur.execute("""Truncate "USER", "CHANNEL", "CHANNELS_JOINED", "IS_CONNECTED_TO" CASCADE""")
        self.commit_and_close_connection(conn)

    ## Adds data to the database & closes the connection to the database
    #
    #  @param self The object pointer
    #  @param conn The connection to the database to be modified
    def commit_and_close_connection(self, conn):
        conn.commit()
        conn.close()
