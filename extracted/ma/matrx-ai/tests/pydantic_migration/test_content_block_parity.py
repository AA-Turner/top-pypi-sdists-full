"""Parity for the four dominant content blocks — 99.15% of all stored blocks.

Phase 1b.2. Every number quoted here came from chat.message.content
(136,730 blocks); see FIELD_TRUTH.md §4b.
"""

from __future__ import annotations

import dataclasses
from typing import Any

import pytest
from pydantic import BaseModel, ConfigDict

from matrx_ai.config.models.content import (
    TextContentModel,
    ThinkingContentModel,
    ToolCallContentModel,
    ToolResultContentModel,
)
from matrx_ai.config.tools_config import ToolCallContent, ToolResultContent
from matrx_ai.config.unified_content import TextContent, ThinkingContent, reconstruct_content

PAIRS = [
    (TextContent, TextContentModel),
    (ThinkingContent, ThinkingContentModel),
    (ToolCallContent, ToolCallContentModel),
    (ToolResultContent, ToolResultContentModel),
]


@pytest.mark.parametrize("old,new", PAIRS, ids=lambda c: getattr(c, "__name__", ""))
def test_same_fields_in_the_same_order(old, new):
    assert [f.name for f in dataclasses.fields(old)] == list(new.model_fields)


@pytest.mark.parametrize("old,new", PAIRS, ids=lambda c: getattr(c, "__name__", ""))
def test_defaults_match(old, new):
    for f in dataclasses.fields(old):
        if f.default is not dataclasses.MISSING:
            expected = f.default
        elif f.default_factory is not dataclasses.MISSING:  # type: ignore[misc]
            expected = f.default_factory()  # type: ignore[misc]
        else:
            continue
        assert getattr(new(), f.name) == expected, f"{new.__name__}.{f.name}"


# ── the third declared-type lie, and the worst by volume ──────────────────────


def test_tool_result_content_is_a_str_on_every_real_rebuild():
    """ToolResultContent.content is declared list[dict[str, Any]]. The ONE
    deserializer assigns a str to it on EVERY tool_result rebuild. A literal
    port of the annotation rejects 13,338 production blocks — every tool result
    in the system. This test is the forcing function against narrowing it."""
    pointer = {
        "type": "tool_result", "call_id": "c1", "tool_use_id": "c1",
        "name": "search", "is_error": False, "output_chars": 1234, "metadata": {},
    }
    rebuilt = reconstruct_content(pointer)
    assert isinstance(rebuilt.content, str), "the deserializer stopped producing str"

    # The Anthropic empty-error safeguard synthesises a sentence — also a str.
    errored = reconstruct_content({**pointer, "is_error": True})
    assert isinstance(errored.content, str) and errored.content

    # The twin accepts both; a literal port accepts neither.
    assert ToolResultContentModel(content=rebuilt.content).content == rebuilt.content
    assert ToolResultContentModel(content=errored.content).content == errored.content

    class LiteralPort(BaseModel):
        model_config = ConfigDict(arbitrary_types_allowed=True)
        content: list[dict[str, Any]] = []

    for value in (rebuilt.content, errored.content):
        with pytest.raises(Exception):
            LiteralPort(content=value)


@pytest.mark.parametrize("value", ["a string", [{"type": "image"}], {"a": 1}])
def test_tool_result_content_accepts_every_shape_callers_pass(value):
    """str, list and dict all reach this field from real construction sites."""
    assert ToolResultContentModel(content=value).content == value


# ── thinking: the first shape with real explicit nulls ────────────────────────


def test_thinking_accepts_explicit_nulls_because_storage_holds_them():
    """signature null ×243, signature_encoding null ×1,992 — actually on the
    wire, not merely absent. FIELD_TRUTH §2's 'absence, never null' is a
    CONFIG-corpus fact and does not hold here."""
    m = ThinkingContentModel(text="t", signature=None, signature_encoding=None)
    assert m.signature is None and m.signature_encoding is None


def test_thinking_signature_takes_str_and_bytes():
    # str is the JSON form; bytes is the in-memory decoded Gemini signature.
    assert ThinkingContentModel(signature="abc").signature == "abc"
    assert ThinkingContentModel(signature=b"\x00\x01").signature == b"\x00\x01"


def test_the_provider_literal_still_covers_production():
    """All 8 observed provider values are inside the 9-member Literal. This is
    the one declared type the corpus VINDICATED — so pin it, and let a 10th
    provider fail here rather than at flip time."""
    observed = ["google", "anthropic", "cerebras", "openai",
                "generic_openai", "moonshot", "xai", "groq"]
    for p in observed:
        assert ThinkingContentModel(provider=p).provider == p

    with pytest.raises(Exception):
        ThinkingContentModel(provider="a_provider_nobody_added")


# ── text: the second polymorphic field ────────────────────────────────────────


def test_text_accepts_the_one_stored_array():
    """string ×82,934, array ×1. One row is not a rounding error — a str-only
    annotation raises on a real stored message."""
    assert TextContentModel(text="hello").text == "hello"
    assert TextContentModel(text=[{"type": "text"}]).text == [{"type": "text"}]


# ── construction-time behaviour ───────────────────────────────────────────────


@pytest.mark.parametrize("old,new", PAIRS, ids=lambda c: getattr(c, "__name__", ""))
def test_both_refuse_an_unknown_field(old, new):
    with pytest.raises(TypeError):
        old(nonsense=1)
    with pytest.raises(Exception):
        new(nonsense=1)


@pytest.mark.parametrize("old,new", PAIRS, ids=lambda c: getattr(c, "__name__", ""))
def test_the_discriminator_default_is_identical(old, new):
    assert old().type == new().type


def test_every_model_emits_a_schema_for_the_typescript_twin():
    for model in (TextContentModel, ThinkingContentModel,
                  ToolCallContentModel, ToolResultContentModel):
        schema = model.model_json_schema()
        assert set(schema["properties"]) == set(model.model_fields)
        assert "required" not in schema, f"{model.__name__} gained a required field"
