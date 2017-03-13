"""
.. module:: picontrol_server.config
.. moduleauthor:: Julien Spronck
.. created:: March 2017

This module will take care of loading the config file. It will be split into
two submodules:
1. config.config will contain configurable constants
2. config.usercommands will contain user-defined commands to be used in the
iOS PiControl app.
"""

import os as _os
import imp as _imp
import types as _types

_FILENAME = 'picontrol_server_config.py'

# Check if there is a config file in ~/.config/
_USERNAME = _os.getenv("SUDO_USER") or _os.getenv("USER")
_HOME = _os.path.expanduser('~'+_USERNAME)
_CONFIGDIR = _os.path.join(_HOME, ".config")
_CONFIGFILE = _os.path.join(_CONFIGDIR, _FILENAME)

if _os.path.exists(_CONFIGFILE):
    # Use the file in ~/.config/
    _FILENAME = _CONFIGFILE

# Import config file
_config = _imp.load_source('picontrol_server_config', _FILENAME)

# Create two submodules: config and usercommands
_CONFIG_DOC = '''Module containing all configurable constants for
picontrol_server. The constants are defined in the config file.'''
config = _types.ModuleType('config', _CONFIG_DOC)

_USERCOMMANDS_DOC = '''Module containing all configurable constants for
picontrol_server. The constants are defined in the config file.'''
usercommands = _types.ModuleType('usercommands', _USERCOMMANDS_DOC)

# Split _config in two separate submodules
for name in dir(_config):
    if name.startswith('__'):
        continue
    var = getattr(_config, name)
    if callable(var):
        usercommands.__dict__[name] = var
    elif not isinstance(var, _types.ModuleType):
        config.__dict__[name] = var
