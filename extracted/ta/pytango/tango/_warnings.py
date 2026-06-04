# SPDX-FileCopyrightText: All Contributors to the PyTango project
# SPDX-License-Identifier: LGPL-3.0-or-later

"""Internal warning helpers and categories used across PyTango modules."""

import warnings
from collections.abc import Hashable

_already_warned_keys: set[Hashable] = set()


class PyTangoUserWarning(UserWarning):
    """Warning category for user-visible PyTango warnings."""


def warn_once(
    message: str,
    key: Hashable,
    category: type[Warning] = Warning,
    stacklevel: int = 1,
) -> bool:
    """Emit a warning only once for the given key.

    :return: True if a new warning was emitted, or False if the key had
             already been seen.
    """
    if key in _already_warned_keys:
        return False
    _already_warned_keys.add(key)
    warnings.warn(message, category=category, stacklevel=stacklevel + 1)
    return True
