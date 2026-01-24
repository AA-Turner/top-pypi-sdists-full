from fa_purity import (
    FrozenDict,
    Maybe,
    Result,
    ResultE,
    Unsafe,
)
from fa_purity.json import (
    JsonObj,
    JsonPrimitive,
    JsonUnfolder,
    JsonValue,
    JsonValueFactory,
    Unfolder,
)

test_data = (
    JsonValueFactory.from_any({"foo": {"nested": ["hi", 99]}})
    .bind(Unfolder.to_json)
    .alt(Unsafe.raise_exception)
    .to_union()
)


def test_dumps() -> None:
    assert JsonUnfolder.dumps(test_data).replace(
        " ",
        "",
    ) == '{"foo": {"nested": ["hi", 99]} }'.replace(" ", "")


def test_extract_maybe() -> None:
    item = Unfolder.extract_maybe(JsonValue.from_primitive(JsonPrimitive.empty()))
    assert item == Maybe.empty()
    json_value = JsonValue.from_primitive(JsonPrimitive.from_bool(True))
    item2 = Unfolder.extract_maybe(json_value)
    assert item2 == Maybe.some(json_value)


def test_to_optional() -> None:
    json_value_empty = JsonValue.from_primitive(JsonPrimitive.empty())
    fail = Exception("Fail")
    item = Unfolder.to_optional(json_value_empty, lambda _: Result.failure(fail))
    assert item == Result.success(None)
    json_value_2 = JsonValue.from_primitive(JsonPrimitive.from_bool(True))
    result: ResultE[int] = Result.success(77)
    item_2 = Unfolder.to_optional(json_value_2, lambda _: result)
    assert item_2 == Result.success(77)
    item_3 = Unfolder.to_optional(json_value_2, lambda _: Result.failure(fail))
    assert item_3 == Result.failure(fail)


def test_optional_missing_key() -> None:
    fail = Exception("Fail")
    json_obj: JsonObj = FrozenDict({})
    result = JsonUnfolder.optional(json_obj, "missing_key", lambda _: Result.success(77))
    assert result.value_or(None) == Maybe.empty()
    json_obj_2: JsonObj = FrozenDict({"empty_key": JsonValue.from_primitive(JsonPrimitive.empty())})
    result_2 = JsonUnfolder.optional(json_obj_2, "empty_key", lambda _: Result.success(77))
    assert result_2.value_or(None) == Maybe.empty()
    json_obj_3: JsonObj = FrozenDict(
        {"key1": JsonValue.from_primitive(JsonPrimitive.from_bool(True))},
    )
    result_3 = JsonUnfolder.optional(json_obj_3, "key1", lambda _: Result.success(77))
    assert result_3 == Result.success(Maybe.some(77))
    result_4 = JsonUnfolder.optional(json_obj_3, "key1", lambda _: Result.failure(fail, int))
    assert not result_4.map(lambda _: True).value_or(False)
