"""
.. module:: picontrol_server.main
.. moduleauthor:: Julien Spronck
.. created:: March 2017

This module contains the main function of the picontrol_server program.
"""

import getopt
import sys

import eventlet
from . import sockets
from . import config


# Not sure what this next line does exactly
# but it will replace time.sleep by eventlet.sleep
# (which solved my multiple threads problem)
eventlet.monkey_patch()


def usage(exit_status):
    '''Displays the help message.

    Args:
        status (int): exit status
    '''
    msg = "\nStarts a WSGI server for controlling a Raspberry Pi from a mobile"
    msg += " device. The server should be running on the Pi. You need "
    msg += "admin privileges for GPIO control.\n"
    msg += "\nUsage: \n\n"
    msg += "    sudo python picontrol_server.py [OPTIONS]\n\n"
    msg += "Options:\n\n"
    msg += "    -h, --help: prints the usage of the program with possible "
    msg += "options\n"
    msg += "    -p, --port: uses specified port number\n"

    print msg
    sys.exit(exit_status)


def main():
    '''Main function
    '''

    port = config.PORT

    # parse command line options/arguments
    try:
        opts, args = getopt.getopt(sys.argv[1:],
                                   "hp:", ["help", "port="])
        print opts
        print args
    except getopt.GetoptError:
        usage(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage(0)
        if opt in ("-p", "--port"):
            port = int(arg)

    sio = sockets.LockedServer(port=port, logger=True, engineio_logger=True)

    app = sockets.socketio.Middleware(sio)
    eventlet.wsgi.server(eventlet.listen(('', port)), app)
