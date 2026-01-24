from collections.abc import (
    Callable,
)
from dataclasses import (
    dataclass,
)
from typing import (
    IO,
    TypeVar,
)

import simplejson

from fa_purity._core.frozen import (
    FrozenDict,
    FrozenList,
)
from fa_purity._core.result import (
    ResultE,
    ResultFactory,
)
from fa_purity._core.utils import (
    cast_exception,
)
from fa_purity.json._core.primitive import (
    JsonPrimitive,
    Primitive,
)
from fa_purity.json._core.value import (
    JsonObj,
    JsonValue,
)
from fa_purity.json._transform.primitive import (
    JsonPrimitiveFactory,
)

from . import (
    _common,
)

RawUnfoldedJVal = Primitive | JsonPrimitive | JsonObj | FrozenList[JsonValue]
_T = TypeVar("_T")


def _handle_decode_errors(procedure: Callable[[], _T]) -> ResultE[_T]:
    _factory: ResultFactory[_T, Exception] = ResultFactory()
    try:
        return _factory.success(procedure())
    except simplejson.JSONDecodeError as err:
        return _factory.failure(err).alt(cast_exception)


@dataclass(frozen=True)
class JsonValueFactory:
    """Factory of `JsonValue` objects."""

    @staticmethod
    def from_unfolded(raw: RawUnfoldedJVal) -> JsonValue:
        if isinstance(raw, tuple):
            return JsonValue.from_list(raw)
        if isinstance(raw, FrozenDict):
            return JsonValue.from_json(raw)
        if isinstance(raw, JsonPrimitive):
            return JsonValue.from_primitive(raw)
        return JsonValue.from_primitive(JsonPrimitiveFactory.from_raw(raw))

    @staticmethod
    def from_list(raw: list[Primitive] | FrozenList[Primitive]) -> JsonValue:
        return JsonValue.from_list(_common.from_list(raw))

    @staticmethod
    def from_dict(
        raw: dict[str, Primitive] | FrozenDict[str, Primitive],
    ) -> JsonValue:
        return JsonValue.from_json(_common.from_dict(raw))

    @staticmethod
    def from_any(raw: _T) -> ResultE[JsonValue]:
        return _common.from_any(raw)

    @staticmethod
    def load(raw: IO[str]) -> ResultE[JsonValue]:
        return _handle_decode_errors(
            lambda: simplejson.load(raw),  # type: ignore[misc]
        ).bind(
            lambda d: JsonValueFactory.from_any(d),  # type: ignore[misc]
        )

    @staticmethod
    def loads(raw: str) -> ResultE[JsonValue]:
        return _handle_decode_errors(
            lambda: simplejson.loads(raw),  # type: ignore[misc]
        ).bind(
            lambda d: JsonValueFactory.from_any(d),  # type: ignore[misc]
        )
