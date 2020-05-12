# -*- coding: utf-8 -*-

"""
docstring
"""

# import gettext
import logging
import os
import sys

import controller
import dummy
import ipc

try:
    import wx
    # import wx.Locale
    # import wx.GetTranslation
except ImportError:
    sys.exit('\n\tInstall wxPython.\n')


APPNAME = os.path.splitext(os.path.basename(sys.argv[0]))[0]
INI_FILENAME = APPNAME + '.ini'
LOG_FILENAME = APPNAME + '.log'
LOG_LEVEL = logging.DEBUG  #: Example: "DEBUG" o "WARNING"

# languagelist = [locale.getdefaultlocale()[0], 'en_US']
# t = gettext.translation('FeedNotifier', localedir, ['es_ES', 'en_US'])
# _ = t.ugettext
# # pygettext -d FeedNotifier main.py


def init_path():
    """Set the current directory.
    """

    file = dummy.__file__
    file = os.path.abspath(file)

    while file and not os.path.isdir(file):
        file = os.path.split(file)[0]
        os.chdir(file)


def init_logging():
    """[summary]
    """

    # import sys  # FIXME: delete this import
    # import logging

    mformat = "%(asctime)s" \
              " %(levelname)s %(module)s:%(lineno)s %(funcName)s %(message)s"

    logging.basicConfig(format=mformat,
                        datefmt='%Y%m%d%H%M%S',
                        filename=LOG_FILENAME,
                        level=LOG_LEVEL,
                        # style="{"
                        )

    logging.logThreads = 0
    logging.logProcesses = 0

    # logging.basicConfig(
    #    level=LOG_LEVEL,
    #    filename=LOG_FILENAME,
    #    filemode='w',
    #    format='%(asctime)s %(levelname)s %(message)s',
    #    datefmt='%H:%M:%S',
    # )

    # if not hasattr(sys, 'frozen'):
    #    console = logging.StreamHandler(sys.stdout)
    #    console.setLevel(logging.DEBUG)
    #    formatter = logging.Formatter(
    #        '%(asctime)s %(levelname)s %(message)s',
    #        '%H:%M:%S',
    #    )
    #    console.setFormatter(formatter)
    #    logging.getLogger('').addHandler(console)

    # logging.debug('Test DEBUG')  # DEBUG    10
    # logging.info('Test INFO')  # INFO   20
    # logging.warning('Test WARNING')  # WARNING  30
    # logging.error('Test ERROR')  # ERROR    40
    # logging.critical('Test CRITICAL')  # CRITICAL   50


def main():
    """Start point of app.
    """

    init_path()
    init_logging()

    # import sys  # FIXME: delete this import
    # import wx
    # import ipc
    # import controller

    logging.debug('-> ipc.init() - In')  # FIXME: delete this
    try:
        container, message = ipc.init()
    except TypeError:
        logging.error('IPC no initialize!\nExit.')
        sys.exit('Problems! IPC no initialize')
    logging.debug(f'container: {container}')
    logging.debug(f'message: {message}')
    logging.debug('<- ipc.init() - Out')

    if not container:
        logging.error('main:: The container could not be created.')
        return

    logging.debug(f'Initializing wx.app()')

    # app = wx.App()  # redirect=True, filename='log.txt')
    app = wx.App(redirect=True, filename="log.txt", useBestVisual=True)
    logging.debug(f'Initializing wx.app()')
    wx.Log.SetActiveTarget(wx.LogStderr())
    logging.debug(f'Initializing wx.Log.SetActiveTarget(wx.LogStderr())')
    ctrl = controller.Controller()
    logging.debug(f'Initializing ctrl with controller.Controller()')
    container.callback = ctrl.parse_args
    logging.debug(f'Initializing container.callback with ctrl.parse_args')
    container(message)
    logging.debug(f'Initializing container(message)')
    app.MainLoop()


if __name__ == '__main__':
    main()

# EOF
