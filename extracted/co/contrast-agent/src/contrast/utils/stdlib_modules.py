# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import sys

from contrast_vendor.stdlib_list import stdlib_list

# this logic (and all of vendored isort) can be removed when we drop py39
version_info = sys.version_info
_stdlib_modules = (
    set(stdlib_list("3.9")) if version_info[:2] == (3, 9) else sys.stdlib_module_names
)


def is_stdlib_module(module_name):
    """
    Returns True if module_name belongs to standard library module, False otherwise.

    NOTE: 'test' is included in _stdlib_modules so if we're testing this,
    we cannot pass in a module that starts with test.file...
    """
    top_module_name = module_name.split(".")[0]
    return top_module_name in _stdlib_modules
