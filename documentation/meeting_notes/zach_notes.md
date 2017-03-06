## User Authentication & Login

<mark>NOTE</mark>: Do we want users to be able to create accounts first and then
login, or just do it one step? Doing it one step will make it harder for the
client (and user) to see why exactly they couldn't login (less user-friendly).
Was it because they entered the wrong password or because they were trying to
create a new account with a username that had already been taken? Another error
that could occur is the server password being incorrect. The following approach
is with the assumption that you want users to be able to create an account and
login in one step (the less user-friendly option, depending on how the client
displays the information).

Users will be able to create accounts by logging in with a username that hasn't
been taken. If the username has already been taken or if the password the user
enters doesn't match the password associated with the user, then the client will
receive a JSON encoded file that looks something like:
<pre><code>{
	"tags": {
		"loginSuccess": False
    }
}
</code></pre>
Whenever the client sends a request to login, it should send a JSON encoded
package to the server. It should look something like this:
<pre><code>{
  "tags": {
    "login": True
  },
  "login": {
    "username": "some username",
    "password": "some password",
    "server_password": "some server password"
  }
}
</code></pre>
There will also be a server password given to each client that the user doesn't
have to enter but the client will have to pass along with the user login so that
the client can be authenticated.

## Channels
### Channel Creation
As of right now, there will be a set number of channels created by the server
that the clients will have the option of joining. Later on in development, we
may add the option for users to create channels.

### Channel Deletion
The server will have the option of deleting specific channels.

<mark>NOTE</mark>: How do we intend to implement this? Would the server have to
be taken down or could it be interrupted while running? What kind of errors
could occur with interrupting the server?

### Initial Joining of Channels
After a user has logged in, the server will send the client a list of channels
that the user has the option of joining. It will look something like this:
<pre><code>{
	"tags":{
		"loginSuccess": True
    },
 	"channels": [
    	"channel 1",
    	"channel 2",
    	"channel 3"
  ]
}
</code></pre>
The client will then need to send back a JSON encoded file to the server
describing what channels the user would like to join. The JSON file should look
something like this:
<pre><code>{
	"tags": {
		"login": False,
        "joinChannel": True
    },
    "joinChannel": [
    	"channel 1",
        "other channels they may want to join"
    ]
}
</code></pre>
<mark>NOTE</mark>: Would there be any reason a user would run into an error
with joining channels? Is there a limit on the number of users in each channel?
Do we need to send back some kind of bool value notifying the client if the
user had successfully joined the channels?

After the user successfully joins the channels, the specified user will have
access to the channels that they decided to join.

### Joining Channels after selecting initial channels to join
<mark>NOTE:</mark> Is this something we want? Are users going to be restricted to
the initial channels that they join?

### Send/Receive Messages
Whenever the server receives notice that a new message has been posted to a
given channel, the server will send out a message to each user who is connected
to that given channel. The message will be a JSON file that looks something
like this:
<pre><code>{
	"tags": {
        "newMessage": True,
        "channel_receiving_message": "some channel name"
    },
    "message": {
		"user": "the username",
        "timestamp": "the time at which the message was received",
        "message": "the actual message that the user posted"
	}
}
</code></pre>
When a user(client) wishes to send a message to a certain channel, the JSON
file should look something like this:
<pre><code>{
	"tags": {
		"newMessage": True,
        "channel_receiving_message": "some channel name"
    },
    "message": {
		user": "the username",
        "timestamp": "the time at which the message was received",
        "message": "the actual message that the user posted"
    }
}
</code></pre>
Notice that both the JSON file being received by the client and the JSON
being sent out by the server look exactly the same. This is done so that
the server can simply broadcast messages to all users without having to
decode a JSON file server side. This will give the least amount of delay
in messages being sent out to each user. Also, the user that sends the
message out will also receive the message. It's up to the client in how
they want to approach this situation.

