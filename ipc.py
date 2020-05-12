# -*- coding: utf-8 -*-

"""[summary]

Returns:
    [type] -- [description]
"""

import functools
import logging
import socket
import socketserver
import sys
import time

import wx

import util

if sys.platform.startswith('win32'):
    try:
        import win32file
        import win32pipe
    except ModuleNotFoundError:
        sys.exit("\n\tpip install pywin32 ...\n")


class CallbackContainer(object):
    """[summary]

    Arguments:
        object {[type]} -- [description]
    """

    def __init__(self):
        """Initialize CallbackContainer class.
        """

        self.callback = None
        logging.debug("Return callback=%s", self.callback)

    def __call__(self, message):
        """Making GUI method calls from non-GUI threads.

        Any extra positional or keyword args are passed on to the callable
        when it is called.

        Arguments:
            message {[type]} -- [description]
        """

        if self.callback:
            wx.CallAfter(self.callback, message)

        logging.debug("Launch wx.CallAfter(self.callback, message)")


if sys.platform.startswith('win32'):

    def init():
        """initialize the thread server

        Returns:
            [type] -- [description]
        """

        logging.debug('initializing')

        container = CallbackContainer()
        message = '\n'.join(sys.argv[1:])
        name = r'\\.\pipe\FeedNotifier_%s' % wx.GetUserId()

        if client(name, message):
            logging.debug("Initialized: return message='%s' and name='%s'", message, name)
            return None, message
        else:
            logging.debug("Initialized: message='%s' and name='%s'", message, name)

            logging.debug('Jump to util::start_thread()')
            util.start_thread(server, name, container)
            logging.debug('return of util::start_thread()')

            return container, message

    def server(name, callback_func):
        """[summary]

        Arguments:
            name {[type]} -- [description]
            callback_func {[type]} -- [description]
        """

        buffer = 4096
        timeout = 1000
        error = False

        while True:
            if error:
                time.sleep(1)
                error = False

            handle = win32pipe.CreateNamedPipe(
                name,
                win32pipe.PIPE_ACCESS_INBOUND,
                win32pipe.PIPE_TYPE_BYTE |
                win32pipe.PIPE_READMODE_BYTE |
                win32pipe.PIPE_WAIT,
                win32pipe.PIPE_UNLIMITED_INSTANCES,
                buffer,
                buffer,
                timeout,
                None)

            if handle == win32file.INVALID_HANDLE_VALUE:
                error = True
                continue

            try:
                if win32pipe.ConnectNamedPipe(handle) != 0:
                    error = True
                else:
                    code, message = win32file.ReadFile(handle, buffer, None)
                    if code == 0:
                        callback_func(message)
                    else:
                        error = True
            except Exception:
                error = True
            finally:
                win32pipe.DisconnectNamedPipe(handle)
                win32file.CloseHandle(handle)

    def client(name, message):
        """[summary]

        Arguments:
            name {[type]} -- [description]
            message {[type]} -- [description]

        Returns:
            [type] -- [description]
        """

        try:
            file = open(name, 'wb')
            file.write(message)
            file.close()
            return True
        except IOError:
            return False

elif sys.platform.startswith('darwin'):

    sys.exit('\n\tdarwin platform not soported\n')

elif sys.platform.startswith('linux'):

    # sys.exit('\n\tlinux in not suported at time...\n')

    def init():
        """initialize the thread server

        Returns:
            [type] -- [description]
        """

        print('Entramos en ipc::init()::linux')  # FIXME: delete this

        container = CallbackContainer()
        print(f"Container: {container}")
        print(f"Container: {type(container)}")
        print(f"Container: {container.__doc__}")
        # message = '\n'.join(sys.argv[1:])
        # name = r'\\.\pipe\FeedNotifier_%s' % wx.GetUserId()

        # if client(name, message):
        #    print('ipc::init:win32 - Existen "message" y "name"')
        #    print('Salimos de ipc::init()::linux')
        #    return None, message
        # else:
        #    print('ipc::init:win32 - No existen "message" y "name"')
        #    print('Salimos de ipc::init()::linux')
        #    # jump to util.py
        #    util.start_thread(server, name, container)
        #
        #    return container, message

        print('Salimos de ipc::init()::linux')  # FIXME: delete this

    def server(name, callback_func):
        """[summary]

        Arguments:
            name {[type]} -- [description]
            callback_func {[type]} -- [description]
        """

        buffer = 4096
        timeout = 1000
        error = False

        while True:
            if error:
                time.sleep(1)
                error = False

            handle = win32pipe.CreateNamedPipe(
                name,
                win32pipe.PIPE_ACCESS_INBOUND,
                win32pipe.PIPE_TYPE_BYTE |
                win32pipe.PIPE_READMODE_BYTE |
                win32pipe.PIPE_WAIT,
                win32pipe.PIPE_UNLIMITED_INSTANCES,
                buffer,
                buffer,
                timeout,
                None)

            if handle == win32file.INVALID_HANDLE_VALUE:
                error = True
                continue

            try:
                if win32pipe.ConnectNamedPipe(handle) != 0:
                    error = True
                else:
                    code, message = win32file.ReadFile(handle, buffer, None)
                    if code == 0:
                        callback_func(message)
                    else:
                        error = True
            except Exception:
                error = True
            finally:
                win32pipe.DisconnectNamedPipe(handle)
                win32file.CloseHandle(handle)

    def client(name, message):
        """[summary]

        Arguments:
            name {[type]} -- [description]
            message {[type]} -- [description]

        Returns:
            [type] -- [description]
        """

        try:
            file = open(name, 'wb')
            file.write(message)
            file.close()
            return True
        except IOError:
            return False


else:

    # import functools      # FIXME: delete this
    # import socket         # FIXME: delete this
    # import socketserver   # FIXME: delete this

    def init():
        """[summary]

        Returns:
            [type] -- [description]
        """

        container = CallbackContainer()
        message = '\n'.join(sys.argv[1:])
        host, port = 'localhost', 31763

        try:
            server(host, port, container)
            return container, message
        except socket.error:
            client(host, port, message)
        return None, message

    def server(host, port, callback_func):
        """[summary]

        Arguments:
            host {[type]} -- [description]
            port {[type]} -- [description]
            callback_func {[type]} -- [description]
        """

        class Handler(socketserver.StreamRequestHandler):
            """[summary]

            Arguments:
                socketserver {[type]} -- [description]
            """

            def __init__(self, callback_func, *args, **kwargs):
                """[summary]

                Arguments:
                    callback_func {[type]} -- [description]
                """

                self.callback_func = callback_func
                socketserver.StreamRequestHandler.__init__(self,
                                                           *args,
                                                           **kwargs)

            def handle(self):
                """[summary]
                """

                data = self.rfile.readline().strip()
                self.callback_func(data)

        server = socketserver.TCPServer((host, port),
                                        functools.partial(Handler,
                                                          callback_func))
        util.start_thread(server.serve_forever)

    def client(host, port, message):
        """[summary]

        Arguments:
            host {[type]} -- [description]
            port {[type]} -- [description]
            message {[type]} -- [description]
        """

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        sock.send(message)
        sock.close()

# EOF
