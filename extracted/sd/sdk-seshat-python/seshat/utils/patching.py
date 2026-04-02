import importlib
import inspect
import pkgutil
from typing import Callable


def patch(
    decorator: Callable,
    dirname,
    prefix,
    to_track,
    condition: Callable = lambda *_: False,
):
    for loader, name, is_pkg in pkgutil.iter_modules([dirname], prefix=prefix):
        if not is_pkg:
            continue
        module = importlib.import_module(name)
        for _, klass in inspect.getmembers(module, inspect.isclass):
            for attr_name in dir(klass):
                attr = getattr(klass, attr_name)
                if not callable(attr):
                    continue

                if attr_name in to_track or condition(klass, attr_name):
                    if hasattr(attr, "_patched"):
                        continue
                    new_attr = decorator(attr)
                    new_attr._patched = True
                    setattr(klass, attr_name, new_attr)
