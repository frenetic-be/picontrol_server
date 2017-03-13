"""
.. module:: picontrol_server.sockets
.. moduleauthor:: Julien Spronck
.. created:: March 2017

This module contains everything related to sockets (using socket.io).
"""

import threading
import socketio

import codes
from config import config, usercommands
from threads import Thread

if config.SERVER_HAS_GPIO:
    from gpio import Switch, PollingInputdevice

class LockedServer(socketio.Server):
    '''This class is a socketio.Server subclass with the addition of a lock to
    make sure that only one message is emitted at any given time. It also
    defines all socket events necessary for the iOS PiControl app operation.
    '''
    def __init__(self, *args, **kwargs):
        '''Class initialization.
        '''
        super(LockedServer, self).__init__(*args, **kwargs)
        self._lock = threading.Lock()
        self.gpio = {}
        self.threads = {}

        ### SOCKET EVENTS ###

        @self.on('connect')
        def connect(sid, environ):
            '''Define what will be performed when the socket receives a
            `connect` event.
            '''
            print 'Connected with {0}'.format(environ['REMOTE_ADDR'])

        @self.on('disconnect')
        def disconnect(sid):
            print 'Disconnect ', sid
            for thread in self.threads.itervalues():
                thread.stop()

        # check_connection
        @self.on('check_connection')
        def check_connection(sid, code):
            '''Checks that the connection codes on mobile device and on server
            match.

            Args:
                sid (str): the session id
                code (str): the code
            '''
            the_real_code = codes.get_connection_code()
            self.emit('check_connection_response', code == the_real_code)

        # execute
        # This is where user commands are being parsed and executed
        @self.on('execute')
        def parse_command(sid, cmd):
            '''Parses a command received by the server and responds.

            Args:
                sid (str): the session id
                cmd (str): the command sent by the client
            '''
            print 'Received command `{0}`'.format(cmd)
            splitcmd = cmd.split(' ')
            cmd = splitcmd[0]
            args = splitcmd[1:]
            response = 'ERROR - Invalid command'
            func = getattr(usercommands, cmd, None)
            if callable(func):
                response = func(*args)
            self.emit('response', response)

        # gpio_get
        @self.on('gpio_get')
        def gpio_get(sid, data):
            '''Gets status of all GPIO pins.

            Args:
                sid (str): the session id
                data (str): the pin number
            '''
#            print 'Received command `{0}`'.format('gpio_get')
            if not config.SERVER_HAS_GPIO:
                self.emit('response', "Server has no GPIO capability")
                return
            pin = int(data)
            if pin in GPIO:
                value = int(GPIO[pin].is_active)
                self.emit('response_gpio_get', {pin: value})
            else:
                print 'pin not in GPIO', pin, GPIO

        # gpio_get_all
        @self.on('gpio_get_all')
        def gpio_get_all(sid):
            '''Gets status of all GPIO pins.

            Args:
                sid (str): the session id
            '''
#            print 'Received command `{0}`'.format('gpio_get_all')
            if not config.SERVER_HAS_GPIO:
                self.emit('response', "Server has no GPIO capability")
                return
            response = {pin: str(int(GPIO[pin].is_active)) for pin in GPIO
                        if not GPIO[pin].closed}
            self.emit('response_gpio_get_all', response)

        # gpio_set
        # This should not be edited
        @self.on('gpio_set')
        def gpio_set(sid, data):
            '''Turns a GPIO pin on or off.

            Args:
                sid (str): the session id
                data (tuple): a tuple containing the pin number (int) and the
                    value (bool)
            '''
    #         print 'Received command `{0}`'.format('gpio_set')
            if not config.SERVER_HAS_GPIO:
                self.emit('response', "Server has no GPIO capability")
                return
            pin, value = data.split(':')
            pin = int(pin)
            if pin not in GPIO:
                self.emit('gpio_not_configured')
                return
            if GPIO[pin].closed:
                self.emit('response', "GPIO pin is closed")
                return
            value = int(value)
            if value:
                GPIO[pin].on()
                response = 'GPIO - {0}: ON'.format(pin)
            else:
                GPIO[pin].off()
                response = 'GPIO - {0}: OFF'.format(pin)
            print response
            self.emit('response', response)


        # start_probing_input
        @self.on('start_probing_input')
        def start_probing_input(sid):
            '''Start threads for probing GPIO input pins.

            Args:
                sid (str): the session id
            '''
            for pin_number, thread in self.threads.iteritems():
                thread.start((pin_number,))

        # gpio_configure
        @self.on('gpio_configure')
        def gpio_configure(sid, pins):
            '''Configure GPIO pins.

            Args:
                sid (str): the session id
                pins (dict): the GPIO pins and their type
            '''
    #         print 'Received command `{0}`'.format('gpio_configure')

            self.threads = {}
            for pin, pin_type in pins.iteritems():
                pin_number = int(pin)
                self.configure_pin(pin_number, pin_type)
            self.emit('response_gpio_configure')

    def emit(self, *args, **kwargs):
        '''This method emits a message to the clients.
        '''
        with self._lock:
            super(LockedServer, self).emit(*args, **kwargs)

    def probe_gpio_input(self, pin_number, stop_event=None):
        if not config.SERVER_HAS_GPIO:
            return    
        if pin_number not in GPIO:
            return
        gpio_pin = GPIO[pin_number]
        polling = gpio_pin.polling
        old_value = gpio_pin.is_active
        self.emit('gpio_has_changed', {pin_number: old_value})
        while True:
            if stop_event and stop_event.is_set():
                break
            val = int(gpio_pin.is_active)
            if old_value != val:
                old_value = val
                self.emit('gpio_has_changed', {pin_number: val})
            time.sleep(polling)

    def configure_pin(self, pin_number, pin_data):
        if not config.SERVER_HAS_GPIO:
            return
        pin_type, polling = pin_data.split(',')
        polling = int(polling)
        if pin_number in GPIO and not GPIO[pin_number].closed:
            self.gpio[pin_number].close()
        if pin_type == 'output':
            self.gpio[pin_number] = Switch(pin_number)
        elif pin_type == 'input':
            self.gpio[pin_number] = PollingInputdevice(pin=pin_number,
                                                       polling=polling)
            self.threads[pin_number] = Thread(probe_gpio_input,
                                              "Thread - {0}".format(pin_number))
            
        print "GPIO config: Pin {0} - {1}".format(pin_number, pin_type)