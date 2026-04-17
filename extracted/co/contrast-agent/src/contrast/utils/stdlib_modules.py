# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import sys


def is_stdlib_module(module_name: str) -> bool:
    """
    Returns True if module_name belongs to standard library module, False otherwise.
    """
    top_module_name = module_name.split(".", maxsplit=1)[0]
    return top_module_name in sys.stdlib_module_names
