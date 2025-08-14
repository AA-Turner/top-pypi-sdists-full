# Copyright © 2025 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import inspect

NOTIMPLEMENTED_MSG = "This method should be implemented by concrete subclass subclass"


def get_name(obj):
    return f"{obj.__module__}.{obj.__name__}" if inspect.isclass(obj) else obj.__name__
