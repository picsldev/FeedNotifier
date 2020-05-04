def init_path():
    """[summary]
    """

    import os
    import dummy
    file = dummy.__file__
    file = os.path.abspath(file)
    while file and not os.path.isdir(file):
        file, ext = os.path.split(file)
    os.chdir(file)


def init_logging():
    """[summary]
    """

    import sys
    import logging
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
    """[summary]
    """

    init_path()
    init_logging()
    import wx
    import ipc
    import controller
    container, message = ipc.init()
    if not container:
        return
    # app = wx.App()  # redirect=True, filename='log.txt')
    app = wx.App(redirect=True, filename='log.txt')
    wx.Log.SetActiveTarget(wx.LogStderr())
    ctrl = controller.Controller()
    container.callback = ctrl.parse_args
    container(message)
    app.MainLoop()


if __name__ == '__main__':
    main()
