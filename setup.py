#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Setup script for picontrol_server
'''
# import os
# _USERNAME = os.getenv("SUDO_USER") or os.getenv("USER")
# _HOME = os.path.expanduser("~"+_USERNAME)
# _CONFIGDIR = os.path.join(_HOME, ".config")

from distutils.core import setup

setup(name="picontrol_server",
      version="1.0",
      description="",
      long_description="""
      Simple module to ...
      """,
      author="Julien Spronck",
      author_email="github@frenetic.be",
      url="http://frenetic.be",
      packages=["picontrol_server"],
#       entry_points = {"console_scripts":["picontrol_server = 
#                                          "picontrol_server:main"]},
#       data_files=[(_CONFIGDIR, ["picontrol_server/picontrol_server_config.py"])],
      license="Free for non-commercial use",
     )

