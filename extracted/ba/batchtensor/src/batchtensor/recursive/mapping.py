r"""Contain the applier for mappings."""

from __future__ import annotations

__all__ = ["MappingApplier"]

from collections.abc import Mapping
from typing import TYPE_CHECKING, TypeVar

from batchtensor.recursive.auto import register_appliers
from batchtensor.recursive.base import BaseApplier

if TYPE_CHECKING:
    from collections.abc import Callable

    from batchtensor.recursive import ApplyState

T = TypeVar("T", Mapping, dict)


class MappingApplier(BaseApplier[T]):
    r"""Define an applier for mappings/dictionaries.

    Example usage:

    ```pycon

    >>> from batchtensor.recursive import MappingApplier, AutoApplier, ApplyState
    >>> state = ApplyState(applier=AutoApplier())
    >>> applier = MappingApplier()
    >>> applier
    MappingApplier()
    >>> out = applier.apply({"a": 1, "b": "abc"}, str, state)
    >>> out
    {'a': '1', 'b': 'abc'}

    ```
    """

    def apply(self, data: T, func: Callable, state: ApplyState) -> T:
        return type(data)(
            {
                key: state.applier.apply(value, func, state.increment_depth())
                for key, value in data.items()
            }
        )


register_appliers({Mapping: MappingApplier(), dict: MappingApplier()})
