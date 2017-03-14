# picontrol_server

## Python server for the PiControl iOS App

This program is meant to be used together with the PiControl iOS app (under development). This is a simple socket.io Python server that will continuously listen for connection. 
Via the iOS PiControl app, a user can connect to the server and execute user-defined commands on the server. 

This program was meant to run on a Raspberry Pi and allow limited control of the Pi through an iOS interface.

#### Set-up

To install this program, simply use the `setup.py` file in the `picontrol_server` directory:

    python setup.py install
    
Depending on how your computer is set-up, you might need admin privileges for the installation:

    sudo python setup.py install
    

This will install the `picontrol_server` Python package, a console script called `picontrol_server` and a configuration file located at `~/.config/picontrol_server_config.py`. 

#### Auto-completion

For bash users, it should also install a script in `/etc/bash_completion.d/` that enables auto-completion for the `picontrol_server` script. If auto-completion doesn't work in a new bash terminal, you might need to add the following lines to your bashrc file:

    if [ -f /etc/bash_completion.d/picontrol_server ]; then
        source /etc/bash_completion.d/picontrol_server
    fi

#### Configuration

The configuration file is located at `~/.config/picontrol_server_config.py`.

In this file, you can change a few settings:

- `PORT`: Default port number for the server. You will need to provide the port number that end up using (default or not) in the Settings page of the iOS app.

- `CONNECTION_CODE_FILE`: In order to provide a more secure connection between the iOS app and the server. The server will require a code upon first connection. This code will be written in the `CONNECTION_CODE_FILE`. However, you do not need to change this or to see the file since you can get the code through the Python package or the console script.

- `SERVER_HAS_GPIO`: Raspberry Pi have a couple rows of GPIO pins that can be controlled in Python using the `gpiozero` package. If you want to make use of this capability, set `SERVER_HAS_GPIO` to `True`. For other types of servers, set it to `False`.

- `SERVER_LOGGER` and `SERVER_ENGINEIO_LOGGER`: For debugging purposes, it can be useful to set these variables to `True`. This will start the socket.io server with logging flags that will give you detailed information about the server requests and events.

#### User-defined commands

The PiControl iOS app allows the user to perform user-defined commands on a remote server. The commands are defined in the config file located at `~/.config/picontrol_server_config.py`.

All functions defined in the file will correspond to a command that can be executed from the PiControl iOS app. The function names are the names of the commands. Whatever the function returns will be sent to the client back as a response to the requested command.

For example, if the config file contains the following function:

    def time():
        return datetime.datetime.now().strftime('%H:%M:%S')

In the PiControl app, you can then send the command "time" to the server (either using a user-defined button or using the free command textfield). The
server will execute the function "time()" and send the current time as a
response to the client.

The function can also have arguments. However, the arguments must be of type strings, as only strings will be sent by the iOS app.

For example,

    def test(arg1):
        return "`{0}` well received".format(arg1)

In the PiControl app, you can then send the command "test" to the server (using a user-defined button). If the command was configured in the app settings to accept arguments, a dialog will pop up and ask you for the arguments (as a space-separated string).

#### Script usage

For controlling the GPIO pins on your Raspberry Pi, you will need admin privileges.

    sudo picontrol_server [OPTIONS] ARGUMENTS

##### Options:

- -h, --help: prints the usage of the program with possible options
- -p, --port: uses specified port number

##### Arguments:

- `sudo picontrol_server run`: starts the WSGI server

- `sudo picontrol_server code`: displays the connection code
- `sudo picontrol_server code reset`: resets the connection code

- `sudo picontrol_server config`: displays the configurable constants
- `sudo picontrol_server config file`: displays the configuration file

- `sudo picontrol_server commands`: displays the user-defined commands
- `sudo picontrol_server commands file`: displays the user-defined commands file

#### Python package documentation

The `picontrol_server` package is composed of seven sub-modules:

##### picontrol_server.code

This module contains everything related to connection codes.

##### picontrol_server.config

This module contains all configurable constants for picontrol_server. The constants are defined in the config file.

##### picontrol_server.gpio

This module contains GPIO-related classes and functions.

##### picontrol_server.main

This module contains the main function of the program. If you want to run the server from inside the Python shell, use the `picontrol_server.main.run_server(port)`

##### picontrol_server.sockets

This module contains everything related to sockets (using socket.io)

##### picontrol_server.threads

This module contains everything related to threading. In particular,
multi-threading will be used for pushing data about the GPIO input pins from
the server to the client.

##### picontrol_server.usercommands

