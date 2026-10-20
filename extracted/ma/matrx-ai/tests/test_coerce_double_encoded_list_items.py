"""A list-of-objects argument whose ITEMS arrive as JSON strings is decoded, once, before dispatch.

Live 2026-10-20 (conversation a8b580e1, gemini-3.1-flash-lite on scope_system): the model sent
``operations: ["{\\"op\\": \\"upsert_context_item\\", ...}"]`` eight times; recovery decoded only a
top-level string field, so every turn was rejected and the step stalled.
"""

from __future__ import annotations

from typing import Any

import pytest
from pydantic import BaseModel, ConfigDict, Field, ValidationError

from matrx_ai.tools._dispatch_util import coerce_stringified_containers


class _Args(BaseModel):
    model_config = ConfigDict(extra="forbid")
    action: str
    operations: list[dict[str, Any]] = Field(default_factory=list)


def _recover(arguments: dict[str, Any]):
    with pytest.raises(ValidationError) as exc:
        _Args.model_validate(arguments)
    return coerce_stringified_containers(arguments, exc.value)


def test_double_encoded_items_are_decoded_and_validate() -> None:
    arguments = {
        "action": "apply",
        "operations": ['{"op": "upsert_context_item", "key": "a"}', '{\n  "op": "x"\n}'],
    }
    recovered = _recover(arguments)
    assert recovered is not None
    fixed, fields = recovered
    assert fields == ["operations"]
    assert fixed["operations"] == [{"op": "upsert_context_item", "key": "a"}, {"op": "x"}]
    _Args.model_validate(fixed)
    assert arguments["operations"][0].startswith("{"), "the caller's dict is never mutated"


def test_an_item_that_is_not_json_is_left_for_the_refusal() -> None:
    arguments = {"action": "apply", "operations": ['upsert_context_item(key="a")']}
    assert _recover(arguments) is None


def test_an_item_that_decodes_to_the_wrong_container_is_left() -> None:
    arguments = {"action": "apply", "operations": ['["not", "an", "object"]']}
    assert _recover(arguments) is None


def test_the_top_level_string_case_still_works() -> None:
    arguments = {"action": "apply", "operations": '[{"op": "x"}]'}
    recovered = _recover(arguments)
    assert recovered is not None and recovered[0]["operations"] == [{"op": "x"}]
