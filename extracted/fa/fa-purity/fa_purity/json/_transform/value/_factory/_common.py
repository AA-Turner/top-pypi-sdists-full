from __future__ import (
    annotations,
)

from typing import (
    TypeVar,
)

from fa_purity._core.frozen import (
    FrozenDict,
    FrozenList,
    NewFrozenList,
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
    Primitive,
)
from fa_purity.json._core.value import (
    JsonObj,
    JsonValue,
)
from fa_purity.json._transform.primitive import (
    JsonPrimitiveFactory,
    JsonPrimitiveUnfolder,
)

_T = TypeVar("_T")


class HandledException(Exception):
    pass


def from_list_2(
    raw: NewFrozenList[Primitive],
) -> NewFrozenList[JsonValue]:
    return raw.map(JsonPrimitiveFactory.from_raw).map(JsonValue.from_primitive)


def from_list(
    raw: list[Primitive] | FrozenList[Primitive] | NewFrozenList[Primitive],
) -> FrozenList[JsonValue]:
    if isinstance(raw, NewFrozenList):
        return from_list_2(raw).items
    if isinstance(raw, list):
        return from_list_2(NewFrozenList(tuple(raw))).items
    if isinstance(raw, tuple):
        return from_list_2(NewFrozenList(raw)).items


def from_dict(raw: dict[str, Primitive] | FrozenDict[str, Primitive]) -> JsonObj:
    items = FrozenDict(raw) if isinstance(raw, dict) else raw
    return items.map(
        lambda k: k,
        lambda v: JsonValue.from_primitive(JsonPrimitiveFactory.from_raw(v)),
    )


def from_any(raw: _T) -> ResultE[JsonValue]:
    if isinstance(raw, JsonValue):
        return Result.success(raw)
    if isinstance(raw, FrozenDict | dict):
        return (
            NewFrozenList(tuple(raw.items()))
            .map(
                lambda t: JsonPrimitiveFactory.from_any(t[0])
                .bind(JsonPrimitiveUnfolder.to_str)
                .alt(
                    lambda e: cast_exception(
                        ValueError(f"Cannot decode json key `{t[0]}` i.e. {e}"),
                    ),
                )
                .bind(
                    lambda key: from_any(t[1])
                    .alt(
                        lambda e: cast_exception(
                            ValueError(f"Cannot decode json value `{t[1]}` i.e. {e}"),
                        ),
                    )
                    .map(lambda value: (key, value)),
                ),
            )
            .transform(ResultTransform.all_ok_2)
            .map(FrozenDict.from_items)
            .map(JsonValue.from_json)
        )
    if isinstance(raw, list | tuple):
        return (
            NewFrozenList(tuple(raw))  # type: ignore[misc]
            .map(
                from_any,
            )
            .transform(ResultTransform.all_ok_2)
            .map(lambda i: i.items)
            .map(JsonValue.from_list)
        )
    return JsonPrimitiveFactory.from_any(raw).map(JsonValue.from_primitive)
