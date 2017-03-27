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
            exit("I am unable to connect to the database")

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

        try:
            cur.execute('''INSERT INTO "USER" VALUES ('{}', '{}')'''.format(username, password))
            self.commit_and_close_connection(conn)
        except:

            self.commit_and_close_connection(conn)
            # NOTE: The client will need to do checks to make sure the username
            #       & password are of the correct length, otherwise they will
            #       recieve an error that the says 'username is already taken'
            #       when the username & password have incorrect lengths.
            return json.dumps({
                "error": "That username is already taken."
            })

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
                "error": "The username and/or password do not exist in the database."
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
    # @param admin The username of the creator of the channel
    # @param channel_name The name of the channel to be created
    # @return A JSON object containing an error if there is one, none if successful
    def create_channel(self, admin, channel_name):
        conn = self.make_connection()
        cur = conn.cursor()
        try:
            if(not(len(admin) <= 20)):
                # Probably won't need this check, as the username should already be verified to be acceptable, but just in case
                raise "Invalid admin username" 
            elif(not(len(channel_name) <= 40)):
                raise "Invalid channel name"
            else:
                cur.execute('''INSERT INTO "CHANNEL" VALUES ('{}', '{}')'''.format(channel_name, admin))
                
        except "Invalid admin username":
            
            error = json.dumps({
                "error": "The username for the admin of this channel is longer than the max length."
                }, indent=4)
                
        except "Invalid channel name":
        
            error = json.dumps({
                "error": "The name of the channel is longer than the max length."
                }, indent=4)
                
        finally:
            self.commit_and_close_connection(conn)
            if error is not None:
                return error
                
    ## Removes a channel from the database
    #
    # @param self The object pointer
    # @param channel_name The channel to be removed
    # @return On success returns None, else returns a json object containing the error
    def delete_channel(self, channel_name):
        conn = self.make_connection()
        cur = conn.cursor()
        
        try:
        
            if(not(len(channel_name) <= 40)):
                raise "Invalid channel name"
            else:
                cur.execute('''
                SELECT channelid 
                FROM "CHANNEL" 
                WHERE channelid='{}'
                '''.format(channel_name))
                
                if not(cur.rowcount == 1):
                    raise "Channel not found"
                else:
                    cur.execute('''
                    DELETE FROM "CHANNEL"
                    WHERE channelid='{}'
                    '''.format(channel_name))
        
        except "Invalid channel name":
            error = json.dumps({
                "error": "The name of the specified channel is longer than the max length."
                }, indent=4)
        except "Channel not found":
            error = json.dumps({
                "error": "The specified channel was not found."
                }, indent=4)
        finally:
            self.commit_and_close_connection(conn)
            if error is not None:
                return error
    
    ## Removes a user from the database
    #
    # @param self The object pointer
    # @param username The username to be deleted
    # @return On success returns None, else returns a JSON object containing the error
    def delete_user(self, username):
        conn = make_connection()
        cur = conn.cursor()
        
        try:
            if not(len(username) <= 20):
                raise "Invalid username"
            else:
                # will we be requiring a password to delete the account as well?
                cur.execute('''
                SELECT userid
                FROM "USER"
                WHERE userid='{}'
                '''.format(username))
                
                if not(cur.rowcount == 1):
                    raise "Username not found"
                else:
                    cur.execute('''
                    DELETE FROM "USER"
                    WHERE userid='{}'
                    '''.format(username))
        
        except "Invalid username":
            error = json.dumps({
                "error": "The username exceeds the max length"
                }, indent=4)
        except "Username not found":
            error = json.dumps({
                "error": "The username was not found in the database"
                }, ident=4)
        finally:
            self.commit_and_close_connection(conn)
            if error is not None:
                return error
    
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
