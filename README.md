# picontrol_server

## Python server for the PiControl iOS App

This program is meant to be used together with the PiControl IOS App (under development). This is a simple socket.io Python server that will continuously listen for connection. 
Via the iOS PiControl App, a user can connect to the server and execute user-defined commands on the server. 

This program was meant to run on a Raspberry Pi and allow limited control of the Pi through an iOS interface.

#### Set-up

To install this program, simply use the `setup.py` file in the `picontrol_server` directory:

    python setup.py install
    
Depending on how your computer is set-up, you might need admin privileges for the installation:

    sudo python setup.py install
    

This will install a console script called `picontrol_server` and a configuration file located at `~/.config/picontrol_server_commands.py`.

#### Usage

...
