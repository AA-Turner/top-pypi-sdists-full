from collections.abc import Callable
from dataclasses import (
    dataclass,
)
from typing import (
    Any,
    TypeVar,
)

from simplejson import (
    JSONEncoder,
)
from simplejson import (
    dumps as _dumps,
)

from fa_purity._core.coproduct import (
    UnionFactory,
)
from fa_purity._core.frozen import (
    FrozenDict,
    FrozenList,
    FrozenTools,
    NewFrozenList,
)
from fa_purity._core.maybe import (
    Maybe,
)
from fa_purity._core.result import (
    Result,
    ResultE,
)
from fa_purity._core.utils import (
    cast_exception,
)
from fa_purity._transform.result import (
    ResultTransform,
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
    JsonPrimitiveUnfolder,
)

_T = TypeVar("_T")


class _JsonEncoder(JSONEncoder):
    def default(self: JSONEncoder, o: _T) -> Any:  # type: ignore[explicit-any] # noqa: ANN401
        if isinstance(o, FrozenDict):
            return FrozenTools.unfreeze(o)  # type: ignore[misc]
        if isinstance(o, JsonValue):
            return o.map(
                lambda x: x.map(
                    lambda y: y,
                    lambda y: y,
                    lambda y: y,
                    lambda y: y,
                    lambda y: y,
                    lambda: None,
                ),
                lambda x: x,
                lambda x: x,
            )
        return JSONEncoder.default(self, o)  # type: ignore[misc]


def _transform_json(
    item: JsonObj,
    transform: Callable[[JsonValue], ResultE[_T]],
) -> ResultE[FrozenDict[str, _T]]:
    key_values = NewFrozenList(tuple(item.items())).map(
        lambda t: transform(t[1])
        .map(lambda p: (t[0], p))
        .alt(lambda e: ValueError(f"key '{t[0]}' transform failed i.e. {e}"))
        .alt(cast_exception),
    )
    return ResultTransform.all_ok_2(key_values).map(lambda x: FrozenDict(dict(x)))


@dataclass(frozen=True)
class Unfolder:
    """Common transforms to unfold `JsonValue` objects."""

    @staticmethod
    def to_primitive(item: JsonValue) -> ResultE[JsonPrimitive]:
        """Transform to primitive."""
        fail: ResultE[JsonPrimitive] = Result.failure(
            cast_exception(TypeError("Expected `JsonPrimitive` in unfolded `JsonValue`")),
        )
        return item.map(
            lambda x: Result.success(x),
            lambda _: fail,
            lambda _: fail,
        )

    @staticmethod
    def to_list(item: JsonValue) -> ResultE[FrozenList[JsonValue]]:
        """Transform to list."""
        fail: ResultE[FrozenList[JsonValue]] = Result.failure(
            cast_exception(TypeError("Expected `FrozenList[JsonValue]` in unfolded `JsonValue`")),
        )
        return item.map(
            lambda _: fail,
            lambda x: Result.success(x),
            lambda _: fail,
        )

    @staticmethod
    def to_json(item: JsonValue) -> ResultE[JsonObj]:
        """Transform to json."""
        fail: ResultE[JsonObj] = Result.failure(
            cast_exception(TypeError("Expected `JsonObj` in unfolded `JsonValue`")),
        )
        return item.map(
            lambda _: fail,
            lambda _: fail,
            lambda x: Result.success(x),
        )

    @staticmethod
    def transform_list(
        items: FrozenList[JsonValue],
        transform: Callable[[JsonValue], ResultE[_T]],
    ) -> ResultE[FrozenList[_T]]:
        """Transform to list of `_T`."""
        return ResultTransform.all_ok_2(NewFrozenList(items).map(transform)).map(lambda i: i.items)

    @classmethod
    def get(cls, item: JsonValue, key: str) -> ResultE[JsonValue]:
        """Transform into `JsonObj` and get an specific key value."""
        return cls.to_json(item).alt(cast_exception).bind(lambda d: ResultTransform.get_key(d, key))

    @classmethod
    def to_list_of(
        cls,
        item: JsonValue,
        transform: Callable[[JsonValue], ResultE[_T]],
    ) -> ResultE[FrozenList[_T]]:
        """Transform `JsonValue` into `FrozenList[_T]`."""
        return cls.to_list(item).bind(lambda i: cls.transform_list(i, transform))

    @classmethod
    def to_dict_of(
        cls,
        item: JsonValue,
        transform: Callable[[JsonValue], ResultE[_T]],
    ) -> ResultE[FrozenDict[str, _T]]:
        """Transform `JsonValue` into `FrozenDict[str, _T]`."""
        return cls.to_json(item).bind(lambda i: _transform_json(i, transform))

    @staticmethod
    def extract_maybe(item: JsonValue) -> Maybe[JsonValue]:
        """If `JsonValue` is `None` return empty."""
        to_none = (
            Unfolder.to_primitive(item).bind(JsonPrimitiveUnfolder.to_none).alt(lambda _: item)
        )
        return Maybe.from_result(to_none.swap())

    @classmethod
    def to_optional(
        cls,
        item: JsonValue,
        transform: Callable[[JsonValue], ResultE[_T]],
    ) -> ResultE[_T | None]:
        """Transform `JsonValue` into `None` or `_T`."""
        _union: UnionFactory[_T, None] = UnionFactory()
        return (
            cls.extract_maybe(item)
            .map(lambda v: transform(v).map(_union.inl))
            .value_or(Result.success(_union.inr(None), Exception))
        )

    @classmethod
    def to_raw(cls, value: JsonValue) -> dict[str, Any] | list[Any] | Primitive:  # type: ignore[explicit-any]
        """Transform to untyped and unfrozen raw json object."""
        return value.map(
            JsonPrimitiveUnfolder.to_raw,
            lambda items: [cls.to_raw(i) for i in items],  # type: ignore[misc]
            lambda dict_obj: {key: cls.to_raw(val) for key, val in dict_obj.items()},  # type: ignore[misc]
        )


@dataclass(frozen=True)
class JsonUnfolder:
    """Common transforms over a `JsonObj`."""

    @staticmethod
    def dumps(obj: JsonObj) -> str:
        """Transform into string format."""
        return _dumps(obj, cls=_JsonEncoder)  # type: ignore[misc]

    @staticmethod
    def require(
        item: JsonObj,
        key: str,
        transform: Callable[[JsonValue], ResultE[_T]],
    ) -> ResultE[_T]:
        """Require some specific key on the `JsonObj`, if success apply the supplied transform."""
        return (
            ResultTransform.get_key(item, key)
            .bind(transform)
            .alt(lambda e: ValueError(f"required key '{key}' unfold failed i.e. {e}"))
            .alt(cast_exception)
        )

    @staticmethod
    def optional(
        item: JsonObj,
        key: str,
        transform: Callable[[JsonValue], ResultE[_T]],
    ) -> ResultE[Maybe[_T]]:
        """
        Get some specific key on the `JsonObj`.

        - return empty if key is missing
        - return empty if value is `None`
        - else apply the supplied transform
        """
        empty: Maybe[_T] = Maybe.empty()

        return (
            (
                Maybe.from_result(ResultTransform.get_key(item, key).alt(lambda _: None))
                .bind(Unfolder.extract_maybe)
                .map(lambda x: transform(x).map(lambda v: Maybe.some(v)))
                .value_or(Result.success(empty))
            )
            .alt(lambda e: ValueError(f"optional key '{key}' unfold failed i.e. {e}"))
            .alt(cast_exception)
        )

    @staticmethod
    def map_values(
        item: JsonObj,
        transform: Callable[[JsonValue], ResultE[_T]],
    ) -> ResultE[FrozenDict[str, _T]]:
        """Apply the transform to each value of the json."""
        return _transform_json(item, transform)

    @staticmethod
    def to_raw(item: JsonObj) -> dict[str, dict[str, Any] | list[Any] | Primitive]:  # type: ignore[explicit-any]
        """Transform to untyped and unfrozen raw json object."""
        return FrozenTools.unfreeze(item.map(lambda k: k, Unfolder.to_raw))  # type: ignore[misc]
