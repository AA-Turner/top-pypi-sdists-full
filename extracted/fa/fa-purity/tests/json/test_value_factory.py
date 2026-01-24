from decimal import Decimal
from io import StringIO
from typing import TypeVar

from fa_purity import (
    FrozenDict,
    FrozenTools,
    Result,
    Unsafe,
)
from fa_purity.json import JsonPrimitiveFactory, JsonValue, JsonValueFactory, Primitive, Unfolder
from fa_purity.json._core.value import JsonObj

_S = TypeVar("_S")
_F = TypeVar("_F")


def _assert_success(item: Result[_S, _F]) -> _S:
    return item.alt(lambda _: Unsafe.raise_exception(ValueError("not success"))).to_union()


def _prim_value(value: Primitive) -> JsonValue:
    return JsonValue.from_primitive(JsonPrimitiveFactory.from_raw(value))


def test_from_unfolded() -> None:
    from_unfolded = JsonValueFactory.from_unfolded
    assert from_unfolded(1) != from_unfolded(Decimal("1.00"))
    assert from_unfolded("foo") != from_unfolded(3.59)
    assert from_unfolded("foo") == from_unfolded("foo")
    assert from_unfolded(33) == from_unfolded(33)


def test_from_list() -> None:
    from_list = JsonValueFactory.from_list
    item_1 = from_list((3, Decimal("0.023"), True))
    item_2 = from_list([3, Decimal("0.023"), True])
    assert item_1 == item_2


def test_from_dict() -> None:
    from_dict = JsonValueFactory.from_dict
    raw: dict[str, Primitive] = {"a": 3, "b": Decimal("0.023"), "c": True}
    item_1 = from_dict(raw)
    item_2 = from_dict(FrozenDict(raw))
    assert item_1 == item_2


def test_from_any() -> None:
    from_any = JsonValueFactory.from_any
    _assert_success(from_any(1))
    _assert_success(from_any(Decimal("1.00")))
    _assert_success(from_any("foo"))
    _assert_success(from_any(3.59))
    _assert_success(from_any(True))
    _assert_success(from_any(None))
    _assert_success(from_any(_prim_value(1)))
    _assert_success(from_any({"a": _prim_value(1)}))
    _assert_success(from_any([_prim_value(1)]))
    _assert_success(from_any(FrozenDict({"a": _prim_value(1)})))


def _mock_json() -> JsonObj:
    return FrozenTools.freeze(
        {
            "foo": JsonValue.from_json(
                FrozenTools.freeze(
                    {
                        "nested": JsonValue.from_list((_prim_value("hi"), _prim_value(99))),
                    },
                ),
            ),
        },
    )


def test_from_any_2() -> None:
    json_obj = _mock_json()
    json_obj_from_raw = (
        JsonValueFactory.from_any({"foo": {"nested": ["hi", 99]}})
        .bind(Unfolder.to_json)
        .alt(Unsafe.raise_exception)
        .to_union()
    )
    assert json_obj == json_obj_from_raw


def test_load() -> None:
    raw = r'{"foo": {"nested": ["hi", 99]}}'
    string_io = StringIO(raw)
    expected = _mock_json()
    assert _assert_success(JsonValueFactory.load(string_io)) == JsonValue.from_json(expected)


def test_loads() -> None:
    raw = r'{"foo": {"nested": ["hi", 99]}}'
    expected = _mock_json()
    assert _assert_success(JsonValueFactory.loads(raw)) == JsonValue.from_json(expected)
