"""
.. module:: picontrol_server.gpio
.. moduleauthor:: Julien Spronck
.. created:: March 2017

This module contains GPIO-related classes and functions.
"""

import gpiozero


class Switch(gpiozero.DigitalOutputDevice):
    '''General DigitalOutputDevice subclass
    '''
    pass


class PollingInputdevice(gpiozero.DigitalInputDevice):
    '''General DigitalInputDevice subclass with the addition of a `polling`
    attribute.
    '''
    def __init__(self, pin=None, polling=5, pull_up=False):
        super(PollingInputdevice, self).__init__(pin, pull_up)
        self.polling = polling
