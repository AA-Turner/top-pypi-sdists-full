"""Json value module."""

from __future__ import (
    annotations,
)

from collections.abc import Callable
from dataclasses import (
    dataclass,
    field,
)
from typing import (
    TypeVar,
)

from fa_purity._core.coproduct import (
    Coproduct,
)
from fa_purity._core.frozen import (
    FrozenDict,
    FrozenList,
)

from .primitive import (
    JsonPrimitive,
    Primitive,
)

UnfoldedJsonValue = FrozenDict[str, "JsonValue"] | FrozenList["JsonValue"] | JsonPrimitive
RawUnfoldedJsonValue = FrozenDict[str, "JsonValue"] | FrozenList["JsonValue"] | Primitive
_T = TypeVar("_T")


@dataclass(frozen=True)
class _Private:
    pass


JsonObj = FrozenDict[str, "JsonValue"]


@dataclass(frozen=True)
class JsonValue:
    """The type for json values."""

    _private: _Private = field(repr=False, hash=False, compare=False)
    _value: Coproduct[JsonPrimitive, Coproduct[JsonObj, FrozenList[JsonValue]]]

    def map(
        self,
        primitive_case: Callable[[JsonPrimitive], _T],
        list_case: Callable[[FrozenList[JsonValue]], _T],
        dict_case: Callable[[FrozenDict[str, JsonValue]], _T],
    ) -> _T:
        """Core transform from `JsonValue` to some other type `_T`."""
        return self._value.map(primitive_case, lambda c: c.map(dict_case, list_case))

    @staticmethod
    def from_primitive(item: JsonPrimitive) -> JsonValue:
        """Build a `JsonValue` from a `JsonPrimitive`."""
        return JsonValue(_Private(), Coproduct.inl(item))

    @staticmethod
    def from_json(item: JsonObj) -> JsonValue:
        """Build a `JsonValue` from a `JsonObj`."""
        return JsonValue(_Private(), Coproduct.inr(Coproduct.inl(item)))

    @staticmethod
    def from_list(item: FrozenList[JsonValue]) -> JsonValue:
        """Build a `JsonValue` from a list of `JsonValue`."""
        return JsonValue(_Private(), Coproduct.inr(Coproduct.inr(item)))
