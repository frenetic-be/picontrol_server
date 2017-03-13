"""
.. module:: picontrol_server.threads
.. moduleauthor:: Julien Spronck
.. created:: March 2017

This module contains everything related to threading. In particular,
multi-threading will be used for pushing data about the GPIO input pins from
the server to the client.
"""

import threading

def start_new_thread(target, args, kwargs=None, name=''):
    '''Starts a new thread with target function. If not successful, error is
    logged.

    Args:
        target (function): Function to execute in the new thread.
        args (tuple): Tuple with arguments of the function.

    Keyword args:
        kwargs (dict): dictionary of keyword arguments for the
            function.
        name (str): Thread name. Defaults to ''.

    Returns:

    Raises:
    '''
    if kwargs is None:
        kwargs = {}
#     try:
    thread = threading.Thread(target=target, args=args, name=name,
                              kwargs=kwargs)
    thread.start()
#     except:
#         errmsg = traceback.format_exc()
#         print errmsg

class Thread(object):
    '''
    Class to start and stop a thread.

    Args:
        func (function): function to execute inside the thread
        name (str): name of the thread
    '''

    def __init__(self, func, name): # , logging_queue):
        '''
        Initialization
        '''
        self._func = func
        self._name = name
        self._stop_event = threading.Event()
        self._stop_event.set()
#         self._logging_queue = logging_queue

    @property
    def _is_running(self):
        '''
        Is the thread running?
        '''
        return not self._stop_event.is_set()

    def start(self, args, kwargs=None, main=False):
        '''Starts the thread.

        Args:
            args (tuple): tuple with arguments for the function to execute
                inside thread.

        Keyword args:
            kwargs (dict): keyword arguments for the function to execute
                inside thread.
            main (bool): if True, simply executes the function in same thread
                (does not start a new thread). Default is False.
        '''
        if kwargs is None:
            kwargs = {}
        if not self._is_running:
#             myprint('Starting thread: '+self._name, queue=self._logging_queue)
            print '*** Starting thread: '+self._name
            self._stop_event.clear()
            kwargs['stop_event'] = self._stop_event
            if main:
                self._func(*args, **kwargs)  # pylint: disable=star-args
            else:
                start_new_thread(self._func, args, kwargs=kwargs,
                                 name=self._name)
#         else:
#             myprint('Thread arleady running: '+self._name,
#                     queue=self._logging_queue)

    def stop(self):
        '''Stops the thread.
        '''
        if self._is_running:
#             myprint('Ending thread: '+self._name, queue=self._logging_queue)
            print '*** Stopping thread: '+self._name
            self._stop_event.set()
#         else:
#             myprint('Cannot stop non-running thread: '+self._name,
#                     queue=self._logging_queue)
