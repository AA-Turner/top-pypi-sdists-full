r"""Implement a function to indicate if the input configuration is a
configuration for a given class."""

from __future__ import annotations

__all__ = ["is_object_config"]

import inspect
import sys
from typing import _UnionGenericAlias as UnionGenericAlias
from typing import get_type_hints

if sys.version_info >= (3, 10):
    from types import UnionType
else:  # pragma: no cover
    UnionType = UnionGenericAlias

from objectory.constants import OBJECT_TARGET
from objectory.utils.object_helpers import import_object


def is_object_config(config: dict, cls: type) -> bool:
    r"""Indicate if the input configuration is a configuration for a
    given class.

    This function only checks if the value of the key  ``_target_``
    is valid. It does not check the other values. If ``_target_``
    indicates a function, the returned type hint is used to check
    the class.

    Args:
        config: Specifies the configuration to check.
        cls: Specifies the object class.

    Returns:
        ``True`` if the input configuration is a configuration
            for the given class.

    Example usage:

    ```pycon
    >>> from objectory.utils import is_object_config
    >>> from collections import Counter
    >>> is_object_config({"_target_": "collections.Counter", "iterable": [1, 2, 1, 3]}, Counter)
    True

    ```
    """
    target = config.get(OBJECT_TARGET)
    if target is None:
        return False
    target = import_object(target)
    if inspect.isfunction(target):
        target = get_type_hints(target).get("return")
    if target is None:
        return False
    # Union and | -> (UnionGenericAlias, UnionType)
    targets = target.__args__ if isinstance(target, (UnionGenericAlias, UnionType)) else [target]
    return any(cls in target.__mro__ for target in targets)
