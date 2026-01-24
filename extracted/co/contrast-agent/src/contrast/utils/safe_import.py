# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.

from importlib import import_module


def safe_import_list(*import_names: str):
    return list(filter(None, [safe_import(x) for x in import_names]))


def safe_import(full_name: str):
    module_name, import_name = full_name.rsplit(".", 1)

    try:
        module = import_module(module_name)
        return getattr(module, import_name)
    except (AttributeError, ModuleNotFoundError):
        return None
