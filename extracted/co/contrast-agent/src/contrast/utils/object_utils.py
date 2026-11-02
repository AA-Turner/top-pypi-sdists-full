# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import inspect

NOTIMPLEMENTED_MSG = "This method should be implemented by concrete subclass subclass"

MAX_SUBCLASS_SEARCH_DEPTH = 32


def find_subclasses(type, *, _depth=MAX_SUBCLASS_SEARCH_DEPTH):
    """
    Recursively find all subclasses of a given type, including transitive subclasses.
    """
    if _depth == 0:
        return
    for subclass in type.__subclasses__():
        yield subclass
        yield from find_subclasses(subclass, _depth=_depth - 1)


def get_name(obj):
    return f"{obj.__module__}.{obj.__name__}" if inspect.isclass(obj) else obj.__name__
