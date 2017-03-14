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

#### Script usage


#### Python package documentation

The `picontrol_server` package is composed of seven sub-modules:

1. picontrol_server
...
