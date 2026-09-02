r"""Contain the applier for sequences/lists/tuples."""

from __future__ import annotations

__all__ = ["SequenceApplier"]

from collections.abc import Sequence
from typing import TYPE_CHECKING, TypeVar

from batchtensor.recursive.auto import register_appliers
from batchtensor.recursive.base import BaseApplier

if TYPE_CHECKING:
    from collections.abc import Callable

    from batchtensor.recursive import ApplyState

T = TypeVar("T", Sequence, list, tuple, set)


class SequenceApplier(BaseApplier[T]):
    r"""Define a applier for sequences/lists/tuples.

    Example usage:

    ```pycon

    >>> from batchtensor.recursive import SequenceApplier, AutoApplier, ApplyState
    >>> state = ApplyState(applier=AutoApplier())
    >>> applier = SequenceApplier()
    >>> applier
    SequenceApplier()
    >>> out = applier.apply([1, "abc"], str, state)
    >>> out
    ['1', 'abc']

    ```
    """

    def apply(self, data: T, func: Callable, state: ApplyState) -> T:
        return type(data)(
            [state.applier.apply(value, func, state.increment_depth()) for value in data]
        )


register_appliers(
    {
        Sequence: SequenceApplier(),
        list: SequenceApplier(),
        set: SequenceApplier(),
        tuple: SequenceApplier(),
    }
)
