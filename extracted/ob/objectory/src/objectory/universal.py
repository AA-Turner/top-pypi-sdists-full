r"""Implement a "universal" factory function."""

from __future__ import annotations

__all__ = ["factory"]

from typing import Any

from objectory.utils import import_object, instantiate_object


def factory(_target_: str, *args: Any, _init_: str = "__init__", **kwargs: Any) -> Any:
    r"""Instantiate dynamically an object given its configuration.

    Args:
        _target_: Specifies the name of the object (class or
            function) to instantiate. It can be the class name or
            the full class name.
        *args: Variable length argument list.
        _init_: Specifies the function to use to create the
            object. If ``"__init__"``, the object is created by
            calling the constructor.
        **kwargs: Arbitrary keyword arguments.

    Returns:
        The instantiated object with the given parameters.

    Raises:
        RuntimeError: if the target cannot be found.

    Example usage:

    ```pycon
    >>> from objectory import factory
    >>> factory("collections.Counter", [1, 2, 1, 3])
    Counter({1: 2, 2: 1, 3: 1})

    ```
    """
    target = import_object(_target_)
    if target is None:
        msg = f"The target object does not exist: {_target_}"
        raise RuntimeError(msg)
    return instantiate_object(target, *args, _init_=_init_, **kwargs)
