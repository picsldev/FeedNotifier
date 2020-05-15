# -*- coding: utf-8 -*-

"""[summary]

Returns:
    [type] -- [description]
"""

import logging
import sys
import time

if sys.platform.startswith('win32'):
    from ctypes import *

if sys.platform.startswith('win32'):

    # Detecting idle time using python
    # https://stackoverflow.com/questions/911856/detecting-idle-time-using-python
    #
    # https://stackoverflow.com/questions/217157/how-can-i-determine-the-display-idle-time-from-python-in-windows-linux-and-mac?noredirect=1&lq=1
    # TODO: 

    class LASTINPUTINFO(Structure):
        """[summary]

        Arguments:
            Structure {[type]} -- [description]
        """

        _fields_ = [
            ('cbSize', c_uint),
            ('dwTime', c_int),
        ]

    def get_idle_duration():
        """[summary]

        Returns:
            [type] -- [description]
        """

        lastInputInfo = LASTINPUTINFO()
        lastInputInfo.cbSize = sizeof(lastInputInfo)

        if windll.user32.GetLastInputInfo(byref(lastInputInfo)):
            millis = windll.kernel32.GetTickCount() - lastInputInfo.dwTime
            return millis / 1000.0
        else:
            return 0

elif sys.platform.startswith('darwin'):

    print('We are in MacOX')  # FIXME: ¿?

    def get_idle_duration():
        return 0

elif sys.platform.startswith('linux'):

    print('We are in linux')  # FIXME: ¿?

    def get_idle_duration():
        return 0

else:
    pass

    # def get_idle_duration():
    #    return 0

if __name__ == '__main__':

    while True:
        duration = get_idle_duration()
        logging.debug(('User idle for %.2f seconds.' % duration))
        time.sleep(1)

# EOF
