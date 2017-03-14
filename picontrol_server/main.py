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
from .config import config, usercommands
from . import codes

def usage(exit_status):
    '''Displays the help message.

    Args:
        status (int): exit status
    '''
    msg = "\nStarts a WSGI server for controlling a Raspberry Pi from a mobile"
    msg += " device. The server should be running on the Pi. You need "
    msg += "admin privileges for GPIO control.\n"
    msg += "\nUsage: \n\n"
    msg += "    sudo picontrol_server [OPTIONS] ARGUMENTS\n\n"
    msg += "Options:\n\n"
    msg += "    -h, --help: prints the usage of the program with possible "
    msg += "options\n"
    msg += "    -p, --port: uses specified port number\n\n"
    msg += "Arguments:\n\n"
    msg += "    run: starts the WSGI server\n\n"
    msg += "    code: displays the connection code\n"
    msg += "    code reset: resets the connection code\n\n"
    msg += "    config: displays the configurable constants\n"
    msg += "    config file: displays the configuration file\n\n"
    msg += "    commands: displays the user-defined commands\n"
    msg += "    commands file: displays the user-defined commands file\n\n"

    print msg
    sys.exit(exit_status)

def show_config():
    '''Displays the options set in the config file
    '''
    for name in sorted(dir(config)):
        if name.startswith('_'):
            continue
        print '{0:<30}: {1}'.format(name, getattr(config, name))

def show_commands():
    '''Displays the user-defined commands
    '''
    for name in sorted(dir(usercommands)):
        if name.startswith('_'):
            continue
        print '{0}'.format(name)

def run_server(port):
    '''Starts the WSGI server
    '''
    # Not sure what this next line does exactly
    # but it will replace time.sleep by eventlet.sleep
    # (which solved my multiple threads problem)
    eventlet.monkey_patch()
    
    sio = sockets.LockedServer(port=port,
                               logger=config.SERVER_LOGGER,
                               engineio_logger=config.SERVER_ENGINEIO_LOGGER)

    app = sockets.socketio.Middleware(sio)
    eventlet.wsgi.server(eventlet.listen(('', port)), app)


def main():
    '''Main function
    '''

    port = config.PORT

    # parse command line options/arguments
    try:
        opts, args = getopt.getopt(sys.argv[1:],
                                   "hp:", ["help", "port="])

    except getopt.GetoptError:
        usage(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage(0)
        if opt in ("-p", "--port"):
            port = int(arg)

    if len(args) < 1:
        usage(0)
    
    jargs = ' '.join(args)
    if jargs == 'run':
        run_server(port)
        return

    if jargs == 'code':
        print codes.get_connection_code()
        return
        
    if jargs == 'code reset':
        codes.create_connection_code()
        print codes.get_connection_code()
        return
    
    if jargs == 'config':
        show_config()
        return

    if jargs == 'config file':
        print config.__file__
        return

    if jargs == 'commands':
        show_commands()
        return

    if jargs == 'commands file':
        print usercommands.__file__
        return

    usage(0)
