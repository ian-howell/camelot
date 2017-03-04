# Description

This section will give the reader an overview of the project, including why it
was conceived, what it will do when complete, and the types of people we
expect will use it. We also list constraints that were faced during
development and assumptions we made about how we would proceed.
	
The Camelot Server project will create a means of communication between
chat clients, in order to allow end users to communicate with each other.
	
## Product Perspective

We have chosen to develop this project in order to create a standard form of 
communication between the chat clients that are being developed to use the
server. The developers will use this in order to create an interface to house
the information being transmitted.
	
## Product Functions

The server will have the following capabilities:
  1. Create channels
	  * Those server will be able to create channels that clients can
		connect to and users can chat in.
	2. Monitor channels
	  * The server will be able to connect to all channels and see the messages
		that have been transmitted, and the users that are currently connected
	3. Delete channels
	  * The server will be able to remove channels 
  4. Host clients
	  * Clients will be able to connect to the server and access different 
		channels on the server
	5. Send/Receive messages
	  * The server will be able to send messages to all clients accessing a
		channel, and receive messages from clients on any channel
	
## User Characteristics

Most users will be developers who will make clients to interface with the 
server. They will be mostly of a more technical background, with education
background involving computer programming. They will be interfacing with the
server in order to create a client for end users to communicate with each other.
They may encounter obstacles with reading messages if they have no experience
with parsing JSON. 

## General Constraints

## Assumptions and Dependencies