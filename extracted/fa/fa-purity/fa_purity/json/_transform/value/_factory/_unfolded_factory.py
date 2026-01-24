from dataclasses import (
    dataclass,
)
from typing import (
    IO,
    TypeVar,
)

from deprecated import deprecated

from fa_purity._core.frozen import (
    FrozenDict,
    FrozenList,
    NewFrozenList,
)
from fa_purity._core.result import (
    Result,
    ResultE,
    ResultFactory,
)
from fa_purity._core.utils import (
    cast_exception,
)
from fa_purity.json._core.primitive import (
    Primitive,
)
from fa_purity.json._core.value import (
    JsonObj,
    JsonValue,
    RawUnfoldedJsonValue,
)

from . import (
    _common,
)
from ._jval_factory import (
    JsonValueFactory,
)

_T = TypeVar("_T")


def _only_json_objs(value: JsonValue) -> ResultE[JsonObj]:
    _factory: ResultFactory[JsonObj, Exception] = ResultFactory()
    return value.map(
        lambda _: _factory.failure(ValueError("Expected `JsonObj` not `JsonPrimitive`")).alt(
            cast_exception,
        ),
        lambda _: _factory.failure(
            ValueError("Expected `JsonObj` not `FrozenList[JsonValue]`"),
        ).alt(cast_exception),
        lambda d: _factory.success(d),
    )


@dataclass(frozen=True)
class UnfoldedFactory:
    """Factory of unfolded `JsonValue` objects."""

    @staticmethod
    def from_list(
        raw: list[Primitive] | FrozenList[Primitive] | NewFrozenList[Primitive],
    ) -> FrozenList[JsonValue]:
        return _common.from_list(raw)

    @staticmethod
    def from_dict(
        raw: dict[str, Primitive] | FrozenDict[str, Primitive],
    ) -> JsonObj:
        return _common.from_dict(raw)

    @staticmethod
    def from_unfolded_dict(
        raw: dict[str, RawUnfoldedJsonValue] | FrozenDict[str, RawUnfoldedJsonValue],
    ) -> JsonObj:
        return FrozenDict({key: JsonValueFactory.from_unfolded(val) for key, val in raw.items()})

    @staticmethod
    def from_unfolded_list(
        raw: list[RawUnfoldedJsonValue] | FrozenList[RawUnfoldedJsonValue],
    ) -> FrozenList[JsonValue]:
        return tuple(JsonValueFactory.from_unfolded(item) for item in raw)

    @staticmethod
    def json_from_any(raw: _T) -> ResultE[JsonObj]:
        err = Result.failure(cast_exception(TypeError("Not a `JsonObj`")), JsonObj)
        return JsonValueFactory.from_any(raw).bind(
            lambda jv: jv.map(
                lambda _: err,
                lambda _: err,
                lambda x: Result.success(x),
            ),
        )

    @classmethod
    @deprecated("Prefer `json_from_any`")  # type: ignore[misc]
    def from_raw_dict(cls, raw: dict[str, _T]) -> ResultE[JsonObj]:
        return cls.json_from_any(raw)

    @staticmethod
    def loads(raw: str) -> ResultE[JsonObj]:
        return JsonValueFactory.loads(raw).bind(_only_json_objs)

    @staticmethod
    def load(raw: IO[str]) -> ResultE[JsonObj]:
        return JsonValueFactory.load(raw).bind(_only_json_objs)
