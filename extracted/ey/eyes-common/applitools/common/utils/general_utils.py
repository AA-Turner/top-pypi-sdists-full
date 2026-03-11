from __future__ import absolute_import, division, print_function

import os
from functools import wraps
from typing import TYPE_CHECKING
from urllib.parse import urlparse
from warnings import warn

"""
General purpose utilities.
"""

if TYPE_CHECKING:
    from typing import Any, Callable, Dict, Optional, Text


def cached_property(f):
    # type: (Callable) -> Any
    """
    Returns a cached property that is calculated by function f
    """

    def get(self):
        try:
            return self._property_cache[f]
        except AttributeError:
            self._property_cache = {}
            x = self._property_cache[f] = f(self)
            return x
        except KeyError:
            x = self._property_cache[f] = f(self)
            return x

    return property(get)


def get_env_with_prefix(env_name, default=None):
    # type: (Text, Optional[Text]) -> Optional[Text]
    """
    Takes name of ENV variable, check if exists origin and with list of prefixes
    """
    prefixes_to_check = ["bamboo"]
    try:
        return os.environ[env_name]
    except KeyError:
        for prefix in prefixes_to_check:
            name = "{}_{}".format(prefix, env_name)
            value = os.getenv(name)
            if value:
                return value
    return default


class DeprecatedEnumVariant(object):
    """
    Deprecate Enum variant with message from docstring
    """

    def __init__(self, fget=None, msg=None):
        self.fget = fget
        self.__doc__ = fget.__doc__

    def __get__(self, instance, ownerclass=None):
        warn(self.__doc__, DeprecationWarning, stacklevel=2)
        return self.fget(ownerclass)


class CustomEnumMethod:
    def __init__(self, func):
        self.func = func
        self.__doc__ = func.__doc__

    def __get__(self, obj, objtype=None):
        @wraps(self.func)
        def wrapper(*args, **kwargs):
            if not args or not isinstance(args[0], str):
                raise ValueError("Custom method must be called with a string pattern")
            return self.func(objtype, *args, **kwargs)

        return wrapper


def is_region_like_dict(obj):
    # type: (Dict) -> bool
    """
    Checks if the given object is a dictionary with keys corresponding to a Region.

    Args:
    obj: Object to check.

    Returns:
    bool: True if obj is a dictionary with Region keys, False otherwise.
    """
    return isinstance(obj, dict) and set(obj.keys()) == {
        "left",
        "top",
        "width",
        "height",
    }


def deep_compare(obj1, obj2):
    # type: (Any, Any) -> bool
    """
    Compares two objects deeply.

    Args:
    obj1: First object to compare.
    obj2: Second object to compare.

    Returns:
    bool: True if obj1 and obj2 are the same, False otherwise.
    """
    from applitools.common.geometry import Region

    if is_region_like_dict(obj1):
        obj1 = Region.from_(obj1)

    if is_region_like_dict(obj2):
        obj2 = Region.from_(obj2)

    if type(obj1) is not type(obj2):
        if isinstance(obj1, float) and obj1 == float(obj2):
            return True
        return False

    if isinstance(obj1, dict):
        if obj1.keys() != obj2.keys():
            return False
        return all(deep_compare(obj1[key], obj2[key]) for key in obj1)

    if isinstance(obj1, list):
        if len(obj1) != len(obj2):
            return False
        return all(deep_compare(item1, item2) for item1, item2 in zip(obj1, obj2))

    return obj1 == obj2


def is_url(string):
    try:
        result = urlparse(string)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False
