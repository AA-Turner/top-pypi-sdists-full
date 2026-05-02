from abc import ABC
import os
from navconfig import config


class EnvSupport(ABC):
    """EnvSupport.

    Support for Environment Variables
    """

    def __init__(self, *args, **kwargs):
        self._environment = config
        # Call super only if there’s a next class in the MRO
        try:
            super().__init__(*args, **kwargs)
        except TypeError:
            super().__init__()

    def get_env_value(self, key, default: str = None, expected_type: object = None):
        """
        Retrieves a value from the environment variables or the configuration.

        :param key: The key for the environment variable.
        :param default: The default value to return if the key is not found.
        :param expected_type: the data type to be expected.
        :return: The value of the environment variable or the default value.
        """
        if key is None:
            return default
        if expected_type is not None:
            if expected_type in (int, float):
                return self._environment.getint(key, default)
            elif expected_type == bool:
                return self._environment.getboolean(key, default)
            else:
                return self._environment.get(key, default)
        if val := os.getenv(str(key), default):
            return val
        if val := self._environment.get(key, default):
            return val
        else:
            if hasattr(self, "masks") and hasattr(self, "_mask"):
                if key in self._mask.keys():
                    return self._mask[key]
            return key
