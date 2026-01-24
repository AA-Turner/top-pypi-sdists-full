from typing import Callable


def register_config(func: Callable) -> Callable:
    """
    A decorator that wraps a function and adds `_is_config=True` to it. This is needed for the auto-discover
    of all configs. This function should only be used in a module called configs, otherwise the auto-discover
    functionality won't work.
    """
    func._is_config = True
    return func
