# -*- coding: utf-8 -*-

"""
docstring
"""

import gettext
import logging
import os
import sys

import controller
import dummy
import ipc

try:
    import wx
    import wx.Locale
    import wx.GetTranslation
except ImportError:
    sys.exit('\n\tInstall wxPython.\n')


languagelist = [locale.getdefaultlocale()[0], 'en_US']
t = gettext.translation('FeedNotifier', localedir, ['es_ES', 'en_US'])
_ = t.ugettext
# pygettext -d FeedNotifier main.py


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

    logging.basicConfig(
        level=logging.DEBUG,
        filename='log.txt',
        filemode='w',
        format='%(asctime)s %(levelname)s %(message)s',
        datefmt='%H:%M:%S',
    )

    if not hasattr(sys, 'frozen'):
        console = logging.StreamHandler(sys.stdout)
        console.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            '%(asctime)s %(levelname)s %(message)s',
            '%H:%M:%S',
        )
        console.setFormatter(formatter)
        logging.getLogger('').addHandler(console)


def main():
    """Start point of app.
    """

    init_path()
    init_logging()

    # import sys  # FIXME: delete this import
    # import wx
    # import ipc
    # import controller

    print('main:: -> ipc.init() - In')  # FIXME: delete this
    container, message = ipc.init()
    print('container: %s' % container)  # FIXME: delete this
    print('message: %s' % message)  # FIXME: delete this
    print('main:: -> ipc.init() - Out')  # FIXME: delete this

    if not container:
        # FIXME: delete this
        print('main:: The container could not be created.')
        return

    app = wx.App()  # redirect=True, filename='log.txt')
    # app = wx.App(redirect=True, filename=None, useBestVisual=True)
    wx.Log.SetActiveTarget(wx.LogStderr())
    ctrl = controller.Controller()
    container.callback = ctrl.parse_args
    container(message)
    app.MainLoop()


if __name__ == '__main__':
    main()

# EOF
