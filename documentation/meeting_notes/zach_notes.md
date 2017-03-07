## User Authentication & Login

Users Will have the option to either create an account or to log in with an existing account. 

Users will be able to create accounts by submitting a username that hasn't
been taken. The client will send a JSON encoded file that looks something like:
<pre><code>{
	"tags": {
		"create_account": True
    },
    	"create_account": {
	    "username": "some username",
    	    "password": "some password",
	    "server_password": "some server password"
    }
}
</code></pre>

If the username has already been taken, then the client will
receive a JSON encoded file that looks something like:
<pre><code>{
	"tags": {
		"account_creation_success": False
    },
        "message": "Some string"
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


If the username doesn't exist or if the password the user
enters doesn't match the password associated with the user, then the client will
receive a JSON encoded file that looks something like:
<pre><code>{
	"tags": {
		"login_success": False
    },
        "message": "Some string"
}
</code></pre>

There will also be a server password given to each client that the user doesn't
have to enter but the client will have to pass along with the user login so that
the client can be authenticated.

## Channels
### Channel Creation
As of right now, there will be a set number of channels created by the server
that the clients will have the option of joining. Later on in development, we
may add the option for users to create channels. Upon creation, the creator will become
the admin of that channel. Each user will have a limit on the number of channels they
may create.

### Channel Deletion
As of this writing, only the server team will have the option of deleting specific channels.
When users gain the ability to create channels, they will also gain the ability to
delete channels that they have created.

&#x1F534;NOTE: The initial channels will be owned by the server team.

### Initial Joining of Channels
After a user has logged in, the server will send the client a list of default channels
that the user has the option of joining. It will look something like this:
<pre><code>{
	"tags": {
		"loginSuccess": True
    },
 	"channels": [
    	"channel 1",
    	"channel 2",
    	"channel 3"
  ]
}
</code></pre>

&#x1F534;NOTE: Later on, the user will have the option to search for channels
based on a keyword.

The client will then need to send back a JSON encoded file to the server
describing what channels the user would like to join. The JSON file should look
something like this:
<pre><code>{
	"tags": {
        "joinChannel": True
    },
    "joinChannel": [
    	"channel 1",
        "other channels they may want to join"
    ]
}
</code></pre>

After the user successfully joins the channels, the specified user will have
access to the channels that they decided to join.

### Joining Channels after selecting initial channels to join
Users will have the option to list the channels when logged in. They will be
able to join channels in the same fashion as they did initially.
&#x1F534;NOTE: Later on, the user will have the option to leave channels.

### Send/Receive Messages
Whenever the server receives notice that a new message has been posted to a
given channel, the server will send out a message to each user who is connected
to that given channel. The message will be a JSON file that looks something
like this:
<pre><code>{
	"tags": {
        "newMessage": True
    },
    "channel_receiving_message": "some channel name",
    "message": {
		"user": "the username",
        "timestamp": "the time at which the message was received",
        "message": "the actual message that the user posted"
	}
}
</code></pre>
When a user(client) wishes to send a message to a certain channel, the JSON
object should look something like this:
<pre><code>{
	"tags": {
        "newMessage": True
    },
    "channel_receiving_message": "some channel name",
    "message": {
		"user": "the username",
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

