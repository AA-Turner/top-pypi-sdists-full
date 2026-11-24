"""A plain string where an object or array is required is refused with what was actually wrong.

C94 (live 2026-11-04..10): ``web(queries="Boise city Idaho population")`` and
``records(entity_read, match="Hazel Cummerata")`` were told "You sent a JSON-encoded string; send the raw
JSON object/array itself". They had sent no JSON at all, so the advice could not be followed and the
retry repeated the call. Only a string that IS JSON gets the JSON-encoded advice.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, JsonValue, ValidationError

from matrx_ai.tools._dispatch_util import format_args_error


class _Search(BaseModel):
    model_config = ConfigDict(extra="forbid")
    queries: list[str]


class _Read(BaseModel):
    model_config = ConfigDict(extra="forbid")
    match: dict[str, JsonValue] | None = None


def _refusal(model: type[BaseModel], args: dict[str, Any]) -> str:
    try:
        model.model_validate(args)
    except ValidationError as exc:
        return format_args_error(exc)
    raise AssertionError("the call was expected to be refused")


def test_a_plain_string_for_a_list_is_told_to_wrap_it() -> None:
    msg = _refusal(_Search, {"queries": "Boise city Idaho population 2024 estimate"})
    assert "JSON-encoded" not in msg
    assert "`queries` takes a JSON array" in msg
    assert "plain string" in msg


def test_a_plain_string_for_an_object_is_told_it_needs_keys() -> None:
    msg = _refusal(_Read, {"match": "Hazel Cummerata"})
    assert "JSON-encoded" not in msg
    assert "`match` takes a JSON object" in msg


def test_a_json_encoded_string_still_gets_the_json_advice() -> None:
    assert "JSON-encoded string" in _refusal(_Search, {"queries": '["a", "b"'})
    assert "JSON-encoded string" in _refusal(_Read, {"match": '{"name": "x"'})


def test_one_field_gets_one_line_even_across_union_branches() -> None:
    msg = _refusal(_Read, {"match": "Hazel"})
    assert msg.count("`match` takes") == 1
