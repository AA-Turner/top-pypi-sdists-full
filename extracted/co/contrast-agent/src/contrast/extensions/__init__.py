# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.

import sys

# This is the only place where we should directly import _c_ext. Everywhere else, use
# The alias here (`c_ext`, without the underscore). This lets us control where the C
# extension is _actually_ loaded.
assert "contrast.extensions._c_ext" not in sys.modules
from contrast.extensions import _c_ext as c_ext  # noqa: E402


SPECIAL_METHOD_EXCEPTIONS = ["__repr__", "__getitem__"]


def smart_setattr(owner, name, patch):
    """
    Use either setattr or set_attr_on_type as appropriate
    """
    # For some reason, set_attr_on_type doesn't work for special methods
    # We may eventually need to refine this logic
    force_patch = isinstance(owner, type) and not (
        name not in SPECIAL_METHOD_EXCEPTIONS
        and name.startswith("__")
        and name.endswith("__")
    )

    setattr(owner, name, patch) if not force_patch else c_ext.set_attr_on_type(
        owner, name, patch
    )


def is_interned(value):
    """
    Checks if a string is interned,
    uses cpython implemented function is_string_interned()
    Arguments:
        value: a string or byte
    Returns:
        Boolean True if value is interned and False if it's not
    """
    # We need to check if the value is bytes or string type
    # because we currently can't tell if another object is interned
    if not isinstance(value, (str, bytes)):
        return False

    # In the byteobject.c implmentation only bytes strings
    # that have a size of 1 character are interned
    if isinstance(value, (bytes)) and len(value) < 2:
        return True

    return c_ext.is_string_interned(value)
