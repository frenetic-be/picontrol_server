"""
.. moduleauthor:: Julien Spronck
.. created:: March 2017

This file contains all user-defined functions that you want to use remotely in
your PiControl App on your iPhone. All functions correspond to a command that
can be called from the PiControl App. The return value of all the functions
will be sent to the client as a response from the call.

This file also contains a few configurable constants used by the
picontrol_server script.

When changed are being made to this file, the server should be restarted.

Example:
Imagine the following function:

def time():
    return datetime.datetime.now().strftime('%H:%M:%S')

In the PiControl app, you can then send the command "time" to the server. The
server will execute the function "time()" and send the current time as a
response to the client.
"""

import datetime
import random


##########################
# Configurable constants #
##########################

# Default port number: if picontrol_server is run without the port option, it
# will use this as port number
PORT = 5234

# File where connection code is saved. In order for the iOS user to connect to
# picontrol_server, it requires a code. This code will be generated and saved
# in the file defined here
CONNECTION_CODE_FILE = '~/.config/picontrol_server_socket_connection'

# If your server supports GPIO (that is if you are running this program on a
# Raspberry Pi.
SERVER_HAS_GPIO = False

# For debugging purposes, you might want to set these logging options to True.
SERVER_LOGGER = True
SERVER_ENGINEIO_LOGGER = True 

##########################
# User-defined functions #
##########################


def time():
    return datetime.datetime.now().strftime('%H:%M:%S')


def date():
    return datetime.datetime.now().strftime('%m/%d/%Y')


def coin_flip():
    number = random.randint(0, 1)
    return "Heads" if number else "Tails"


def test():
    return "Test received!"


def test_arg(arg1):
    return "`{0}` well received".format(arg1)
        