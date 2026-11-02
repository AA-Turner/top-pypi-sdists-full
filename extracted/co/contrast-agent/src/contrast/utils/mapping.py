# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.


class GlomDict(dict):
    """
    A dictionary that allows for dot notation access to nested dictionaries.

    Inspired by the glom library.
    """

    def __getitem__(self, key):
        work_dict = super()
        *parents, key = key.split(".")
        for parent in parents:
            work_dict = work_dict.__getitem__(parent)
        return work_dict.__getitem__(key)

    def get(self, key, default=None):
        try:
            return self[key]
        except (KeyError, AttributeError):
            return default
