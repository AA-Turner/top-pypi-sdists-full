"""Json primitive value module."""

from __future__ import (
    annotations,
)

from collections.abc import Callable
from dataclasses import (
    dataclass,
    field,
)
from decimal import (
    Decimal,
)
from typing import (
    TypeVar,
)

from fa_purity._core.coproduct import (
    Coproduct,
)

_T = TypeVar("_T")

_BoolOrNone = Coproduct[bool, None]
_DecimalOr = Coproduct[Decimal, _BoolOrNone]
_FloatOr = Coproduct[float, _DecimalOr]
_IntOr = Coproduct[int, _FloatOr]
_JsonPrimitive = Coproduct[str, _IntOr]
Primitive = str | int | float | Decimal | bool | None


@dataclass(frozen=True)
class _Private:
    pass


@dataclass(frozen=True)
class JsonPrimitive:
    """The type for primitive objects in a json."""

    _private: _Private = field(repr=False, hash=False, compare=False)
    _value: _JsonPrimitive

    def map(  # noqa: PLR0913
        self,
        str_case: Callable[[str], _T],
        int_case: Callable[[int], _T],
        float_case: Callable[[float], _T],
        decimal_case: Callable[[Decimal], _T],
        bool_case: Callable[[bool], _T],
        none_case: Callable[[], _T],
    ) -> _T:
        """Core transform of a `JsonPrimitive` into some other type `_T`."""
        return self._value.map(
            str_case,
            lambda a: a.map(
                int_case,
                lambda b: b.map(
                    float_case,
                    lambda c: c.map(
                        decimal_case,
                        lambda d: d.map(bool_case, lambda _: none_case()),
                    ),
                ),
            ),
        )

    @staticmethod
    def from_str(item: str) -> JsonPrimitive:
        """Build `JsonPrimitive` from a string."""
        return JsonPrimitive(_Private(), Coproduct.inl(item))

    @staticmethod
    def from_int(item: int) -> JsonPrimitive:
        """Build `JsonPrimitive` from an integer."""
        return JsonPrimitive(_Private(), Coproduct.inr(Coproduct.inl(item)))

    @staticmethod
    def from_float(item: float) -> JsonPrimitive:
        """Build `JsonPrimitive` from a float."""
        return JsonPrimitive(_Private(), Coproduct.inr(Coproduct.inr(Coproduct.inl(item))))

    @staticmethod
    def from_decimal(item: Decimal) -> JsonPrimitive:
        """Build `JsonPrimitive` from a Decimal."""
        return JsonPrimitive(
            _Private(),
            Coproduct.inr(Coproduct.inr(Coproduct.inr(Coproduct.inl(item)))),
        )

    @staticmethod
    def from_bool(item: bool) -> JsonPrimitive:
        """Build `JsonPrimitive` from a bool."""
        return JsonPrimitive(
            _Private(),
            Coproduct.inr(Coproduct.inr(Coproduct.inr(Coproduct.inr(Coproduct.inl(item))))),
        )

    @staticmethod
    def empty() -> JsonPrimitive:
        """Build an empty `JsonPrimitive`."""
        return JsonPrimitive(
            _Private(),
            Coproduct.inr(Coproduct.inr(Coproduct.inr(Coproduct.inr(Coproduct.inr(None))))),
        )
