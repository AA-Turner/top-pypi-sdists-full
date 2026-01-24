r"""Implement some helper functions to manipulate objects."""

from __future__ import annotations

__all__ = ["all_child_classes"]

import logging

logger: logging.Logger = logging.getLogger(__name__)


def all_child_classes(cls: type) -> set[type]:
    r"""Get all the child classes (or subclasses) of a given class.

    Based on: https://stackoverflow.com/a/3862957

    Args:
        cls: The class whose child classes are to be retrieved.

    Returns:
        The set of all the child classes of the given class.

    Example usage:

    ```pycon

    >>> from objectory.utils import all_child_classes
    >>> class Foo:
    ...     pass
    ...
    >>> all_child_classes(Foo)
    set()
    >>> class Bar(Foo):
    ...     pass
    ...
    >>> all_child_classes(Foo)
    {<class '....Bar'>}

    ```
    """
    return set(cls.__subclasses__()).union(
        [s for c in cls.__subclasses__() for s in all_child_classes(c)]
    )
