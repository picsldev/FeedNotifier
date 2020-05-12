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
        logging.critical('IPC no initialize!\nExit.')
        sys.exit('Problems! IPC no initialize')
    logging.debug('container: %s', container)  # FIXME: delete this
    logging.debug('message: %s', message)  # FIXME: delete this
    logging.debug('<- ipc.init() - Out')  # FIXME: delete this

    if not container:
        # FIXME: delete this
        logging.debug('main:: The container could not be created.')
        return

    # app = wx.App()  # redirect=True, filename='log.txt')
    app = wx.App(redirect=True, filename="log.txt", useBestVisual=True)
    wx.Log.SetActiveTarget(wx.LogStderr())
    ctrl = controller.Controller()
    container.callback = ctrl.parse_args
    container(message)
    app.MainLoop()


if __name__ == '__main__':
    main()

# EOF
