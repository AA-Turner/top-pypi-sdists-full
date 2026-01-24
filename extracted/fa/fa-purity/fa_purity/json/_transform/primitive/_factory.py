from dataclasses import (
    dataclass,
)
from decimal import (
    Decimal,
)
from typing import (
    TypeVar,
)

from fa_purity._core.result import (
    Result,
    ResultE,
)
from fa_purity._core.utils import (
    cast_exception,
)
from fa_purity.json._core.primitive import (
    JsonPrimitive,
    Primitive,
)

_T = TypeVar("_T")


@dataclass(frozen=True)
class JsonPrimitiveFactory:
    """Factory of `JsonPrimitive` objects."""

    @staticmethod
    def from_any(  # noqa: PLR0911
        raw: _T,
    ) -> ResultE[JsonPrimitive]:
        if isinstance(raw, JsonPrimitive):
            return Result.success(raw)
        if raw is None:
            return Result.success(JsonPrimitive.empty())
        if isinstance(raw, bool):
            return Result.success(JsonPrimitive.from_bool(raw))
        if isinstance(raw, str):
            return Result.success(JsonPrimitive.from_str(raw))
        if isinstance(raw, int):
            return Result.success(JsonPrimitive.from_int(raw))
        if isinstance(raw, float):
            return Result.success(JsonPrimitive.from_float(raw))
        if isinstance(raw, Decimal):
            return Result.success(JsonPrimitive.from_decimal(raw))
        return Result.failure(cast_exception(TypeError("Cannot convert to `JsonPrimitive`")))

    @staticmethod
    def from_raw(raw: Primitive) -> JsonPrimitive:
        if raw is None:
            return JsonPrimitive.empty()
        if isinstance(raw, bool):
            return JsonPrimitive.from_bool(raw)
        if isinstance(raw, str):
            return JsonPrimitive.from_str(raw)
        if isinstance(raw, int):
            return JsonPrimitive.from_int(raw)
        if isinstance(raw, float):
            return JsonPrimitive.from_float(raw)
        if isinstance(raw, Decimal):
            return JsonPrimitive.from_decimal(raw)
