r"""Contain the main public functions to recursively apply a function on
nested data."""

from __future__ import annotations

__all__ = ["recursive_apply"]


from typing import TYPE_CHECKING, Any

from batchtensor.recursive.auto import AutoApplier
from batchtensor.recursive.state import ApplyState

if TYPE_CHECKING:
    from collections.abc import Callable


_applier = AutoApplier()


def recursive_apply(data: Any, func: Callable) -> Any:
    r"""Recursively apply a function on all the items in a nested data.

    Args:
        data: The input data.
        func: The function to apply on each item.

    Returns:
        The transformed data.

     Example usage:

    ```pycon

    >>> from batchtensor.recursive import recursive_apply
    >>> out = recursive_apply({"a": 1, "b": "abc"}, str)
    >>> out
    {'a': '1', 'b': 'abc'}

    ```
    """
    return _applier.apply(data=data, func=func, state=ApplyState(_applier))
