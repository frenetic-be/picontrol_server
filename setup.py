#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Setup script for picontrol_server
'''
import os
_USERNAME = os.getenv("SUDO_USER") or os.getenv("USER")
_HOME = os.path.expanduser("~"+_USERNAME)
_CONFIGDIR = os.path.join(_HOME, ".config")

from setuptools import setup

setup(name="picontrol_server",
      version="1.0",
      description="",
      long_description="""This program is meant to be used together with the
      PiControl iOS app (under development). This is a simple socket.io Python
      server that will continuously listen for connection. 

      Via the iOS PiControl app, a user can connect to the server and execute
      user-defined commands on the server. 
      """,
      author="Julien Spronck",
      author_email="github@frenetic.be",
      url="http://frenetic.be",
      packages=["picontrol_server"],
      entry_points = {"console_scripts":["picontrol_server = "
                                         "picontrol_server.main:main"]},
      data_files=[(_CONFIGDIR,
                   ["picontrol_server/picontrol_server_config.py"]),
                  ('/etc/bash_completion.d/',
                   ['auto-completion/picontrol_server'])],
      license="Free for non-commercial use",
     )

