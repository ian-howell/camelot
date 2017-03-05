# Specific Requirements

## User Requirements
Our user base will be split across two use cases:

1. The end users, who will be referred to as the user, and

2. The client teams, who will be referred as the developers

### User Requirements
The user will need to have a client that can connect with the Camelot server. They will need to be able to communicate with other users across channels. They should be able to send and receive messages. Messages should be sent and received in a logical order.
### Developer Requirements
The developers will require the ability to request a list of channels. The list will contain information regarding the channel names and the users currently in each channel. With a successsful login, they should be able to create to create a unique user with a specific identifier. Users should be deleted upon signing out or error. The developers should be able to request message information, such as message text, senders, requested channel, and timestamps.

## System Requirements
The Camelot server will be run on a Raspberry Pi 3 Model B. It will need need to have internet access. The hardware will need to have Python3 installed as well as PostgreSQL for database management.

##  Interface Requirements
The Camelot will need to interface with a client using JSON formatting as a data transfer protocol.
