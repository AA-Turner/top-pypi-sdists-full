r"""Contain the default applier."""

from __future__ import annotations

__all__ = ["DefaultApplier"]


from typing import TYPE_CHECKING, Any

from batchtensor.recursive.auto import register_appliers
from batchtensor.recursive.base import BaseApplier

if TYPE_CHECKING:
    from collections.abc import Callable

    from batchtensor.recursive import ApplyState


class DefaultApplier(BaseApplier[Any]):
    r"""Define the default applier.

    Example usage:

    ```pycon

    >>> from batchtensor.recursive import DefaultApplier, AutoApplier, ApplyState
    >>> state = ApplyState(applier=AutoApplier())
    >>> applier = DefaultApplier()
    >>> applier
    DefaultApplier()
    >>> out = applier.apply([1, "abc"], str, state)
    >>> out
    "[1, 'abc']"

    ```
    """

    def apply(self, data: Any, func: Callable, state: ApplyState) -> Any:  # noqa: ARG002
        return func(data)


register_appliers({object: DefaultApplier()})
