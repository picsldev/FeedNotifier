# -*- coding: utf-8 -*-

"""[summary]

Returns:
    [type] -- [description]
"""


import defaults
import safe_pickle


class InvalidSettingError(Exception):
    """[summary]

    Arguments:
        Exception {[type]} -- [description]
    """

    pass


class NOT_SET(object):
    """[summary]

    Arguments:
        object {[type]} -- [description]
    """

    pass


class Settings(object):
    """[summary]

    Arguments:
        object {[type]} -- [description]
    """

    def __init__(self, parent):
        """[summary]

        Arguments:
            parent {[type]} -- [description]
        """

        self._parent = parent

    def __getattr__(self, name):
        """[summary]

        Arguments:
            name {[type]} -- [description]

        Raises:
            InvalidSettingError: [description]

        Returns:
            [type] -- [description]
        """

        if name.startswith('_'):
            return super(Settings, self).__getattr__(name)

        value = self.get(name)

        if value != NOT_SET:
            return value

        if self._parent:
            return getattr(self._parent, name)

        raise InvalidSettingError('Invalid setting: %s' % name)

    def __setattr__(self, name, value):
        """[summary]

        Arguments:
            name {[type]} -- [description]
            value {[type]} -- [description]

        Raises:
            InvalidSettingError: [description]
        """

        if name.startswith('_'):
            super(Settings, self).__setattr__(name, value)
            return

        if self.set(name, value):
            return

        if self._parent:
            setattr(self._parent, name, value)
            return

        raise InvalidSettingError('Invalid setting: %s' % name)

    def get(self, name):
        """[summary]

        Arguments:
            name {[type]} -- [description]

        Raises:
            NotImplementedError: [description]
        """

        raise NotImplementedError(
            'Settings subclasses must implement the get() method.')

    def set(self, name, value):
        """[summary]

        Arguments:
            name {[type]} -- [description]
            value {[type]} -- [description]

        Raises:
            NotImplementedError: [description]
        """

        raise NotImplementedError(
            'Settings subclasses must implement the set() method.')


class ModuleSettings(Settings):
    """[summary]

    Arguments:
        Settings {[type]} -- [description]
    """

    def __init__(self, parent, module):
        """[summary]

        Arguments:
            parent {[type]} -- [description]
            module {[type]} -- [description]
        """

        super(ModuleSettings, self).__init__(parent)
        self._module = module

    def get(self, name):
        """[summary]

        Arguments:
            name {[type]} -- [description]

        Returns:
            [type] -- [description]
        """

        module = self._module

        if hasattr(module, name):
            return getattr(module, name)

        return NOT_SET

    def set(self, name, value):
        """[summary]

        Arguments:
            name {[type]} -- [description]
            value {[type]} -- [description]

        Returns:
            [type] -- [description]
        """
        return False


class FileSettings(Settings):
    """[summary]

    Arguments:
        Settings {[type]} -- [description]
    """

    def __init__(self, parent, file):
        """[summary]

        Arguments:
            parent {[type]} -- [description]
            file {[type]} -- [description]
        """

        super(FileSettings, self).__init__(parent)

        self._file = file
        self.load()

    def load(self):
        """[summary]
        """

        try:
            self._settings = safe_pickle.load(self._file)
        except Exception:
            self._settings = {}

    def save(self):
        """[summary]
        """

        safe_pickle.save(self._file, self._settings)

    def get(self, name):
        """[summary]

        Arguments:
            name {[type]} -- [description]

        Returns:
            [type] -- [description]
        """

        if name in self._settings:
            return self._settings[name]

        return NOT_SET

    def set(self, name, value):
        """[summary]

        Arguments:
            name {[type]} -- [description]
            value {[type]} -- [description]

        Returns:
            [type] -- [description]
        """

        if value != getattr(self, name):
            self._settings[name] = value
            self.save()

        return True


def create_chain():
    """[summary]

    Returns:
        [type] -- [description]
    """

    # import defaults  # FIXME: delete this

    settings = ModuleSettings(None, defaults)
    settings = FileSettings(settings, 'settings.dat')

    return settings


settings = create_chain()

# EOF
