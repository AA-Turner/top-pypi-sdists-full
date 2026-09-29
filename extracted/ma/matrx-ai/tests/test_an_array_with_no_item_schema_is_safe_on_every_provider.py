"""An array the author never described the elements of is OUR translator's job.

Arman's ruling: each provider's translator takes ANY shape we hold and makes it
safe for that exact API. After the ``__kind`` fix (F5), 5 live kind contracts were
still refused by OpenAI strict — ``array schema missing items`` — because the
author wrote ``{"type": "array"}`` (or a bare ``Any`` spelled
``["string", "number", "boolean", "object", "array", "null"]``) and named no
element schema. SCHEMA-TRANSLATION.md §15.

The contract pinned here:

* the shared first step makes the element schema EXPLICIT (``items: {}``) —
  losslessly, for every provider;
* a type LIST that includes ``array`` is split so ``items`` belongs to the array
  branch alone (Anthropic, live: "For 'object' type, property 'items' is not
  supported") — the same documents, proven by validation;
* a permissive provider keeps ``items: {}`` — nothing given up;
* a strict provider gets the widest element shape it compiles (every scalar and
  null), recorded as a narrowing that says the item type was unspecified.

Every check fails on the tree before the fix and passes after.
"""

from __future__ import annotations

import copy
from typing import Any

import jsonschema
import pytest

from matrx_ai.providers.anthropic.translator import AnthropicTranslator
from matrx_ai.providers.base_translator import BaseTranslator
from matrx_ai.providers.google.translator import GoogleTranslator
from matrx_ai.providers.openai.translator import OpenAITranslator

try:  # absent before the fix; keep the file importable so each check reds alone
    from matrx_ai.schema.rules import OPEN_SCALAR_ITEM_SCHEMA, make_array_items_explicit
except ImportError:  # pragma: no cover - only on the pre-fix tree
    OPEN_SCALAR_ITEM_SCHEMA = None  # type: ignore[assignment]
    make_array_items_explicit = None  # type: ignore[assignment]

ANY_TYPES = ["string", "number", "boolean", "object", "array", "null"]

#: The live shapes, reproduced: 91 bare `{"type": "array"}` (+ description /
#: default variants) and 9 bare-`Any` type lists, census 2026-09-28.
SCHEMA: dict[str, Any] = {
    "type": "object",
    "additionalProperties": False,
    "required": ["links", "estimated_count"],
    "properties": {
        "links": {"type": "array", "description": "supporting links"},
        "estimated_count": {"type": ANY_TYPES, "description": "whatever the page said"},
    },
}


def _explicit(node: Any) -> Any:
    assert make_array_items_explicit is not None, (
        "matrx_ai.schema.rules exports no make_array_items_explicit: an array with no "
        "item schema reaches OpenAI strict and is refused 'array schema missing items'"
    )
    return make_array_items_explicit(node)


def _wires() -> dict[str, dict[str, Any]]:
    response_format = {
        "type": "json_schema",
        "json_schema": {"name": "probe", "schema": copy.deepcopy(SCHEMA)},
    }
    out = {
        "anthropic": AnthropicTranslator._build_anthropic_output_format(
            copy.deepcopy(response_format)
        )["schema"],
        "openai": OpenAITranslator._build_openai_text_format(copy.deepcopy(response_format))[
            "schema"
        ],
        "google": GoogleTranslator._build_google_response_schema(copy.deepcopy(response_format)),
    }
    for provider in ("groq", "cerebras", "xai", "together"):
        out[provider] = BaseTranslator.build_openai_chat_response_format(
            copy.deepcopy(response_format), provider
        )["json_schema"]["schema"]
    return out


def _array_nodes(node: Any) -> list[dict[str, Any]]:
    found: list[dict[str, Any]] = []
    if isinstance(node, list):
        for item in node:
            found.extend(_array_nodes(item))
        return found
    if not isinstance(node, dict):
        return found
    kind = node.get("type")
    if kind == "array" or (isinstance(kind, list) and "array" in kind):
        found.append(node)
    for key, value in node.items():
        if key in ("enum", "const", "required"):
            continue
        found.extend(_array_nodes(value))
    return found


def test_a_bare_array_gets_an_explicit_item_schema() -> None:
    assert _explicit({"type": "array", "description": "d"}) == {
        "type": "array",
        "description": "d",
        "items": {},
    }


def test_a_type_list_is_split_so_items_belongs_to_the_array_alone() -> None:
    out = _explicit({"type": ANY_TYPES, "description": "d", "minItems": 1})
    assert out["description"] == "d"
    branches = out["anyOf"]
    array_branch = next(b for b in branches if b.get("type") == "array")
    assert array_branch == {"type": "array", "items": {}, "minItems": 1}
    others = [b for b in branches if b is not array_branch]
    assert all("items" not in b for b in others), others


@pytest.mark.parametrize(
    "document",
    ["s", 1.5, 3, True, None, {"a": 1}, [], [1, "x", {"b": [None]}], [[1, 2]]],
)
def test_making_items_explicit_admits_exactly_the_same_documents(document: Any) -> None:
    """Lossless, proven by validation rather than asserted: every JSON kind is
    admitted by the rewritten node exactly when it was by the author's."""
    for authored in ({"type": "array"}, {"type": ANY_TYPES}, {"type": ["array", "null"]}):
        rewritten = _explicit(copy.deepcopy(authored))
        before = jsonschema.Draft202012Validator(authored).is_valid(document)
        after = jsonschema.Draft202012Validator(rewritten).is_valid(document)
        assert before == after, (authored, rewritten, document)


def test_no_provider_receives_an_array_without_an_item_schema() -> None:
    offenders = {
        provider: [node for node in _array_nodes(wire) if "items" not in node]
        for provider, wire in _wires().items()
    }
    offenders = {p: n for p, n in offenders.items() if n}
    assert offenders == {}, (
        "OpenAI strict refuses this by name ('array schema missing items'): "
        f"{offenders}"
    )


def test_items_never_sits_beside_a_non_array_type_on_any_provider() -> None:
    """Anthropic reads `items` beside a type list as a keyword of every listed
    type and refuses it on the object ("property 'items' is not supported")."""
    for provider, wire in _wires().items():
        mixed = [
            node
            for node in _array_nodes(wire)
            if isinstance(node.get("type"), list)
            and set(node["type"]) - {"array", "null"}
            and "items" in node
        ]
        assert mixed == [], f"{provider}: {mixed}"


def test_strict_providers_get_the_widest_element_and_say_it_was_unspecified() -> None:
    assert OPEN_SCALAR_ITEM_SCHEMA is not None, "no OPEN_SCALAR_ITEM_SCHEMA exported"
    for name, translate in (
        ("anthropic", lambda s: AnthropicTranslator.translate_output_schema(s)),
        ("openai", lambda s: OpenAITranslator.translate_output_schema(s)),
        (
            "groq-strict",
            lambda s: BaseTranslator.translate_openai_compatible_output_schema(
                s, "groq", strict=True
            ),
        ),
    ):
        wire, narrowed, _relaxed = translate(copy.deepcopy(SCHEMA))
        items = [node["items"] for node in _array_nodes(wire)]
        assert items and all(item == OPEN_SCALAR_ITEM_SCHEMA for item in items), (name, items)
        assert any("UNSPECIFIED" in note for note in narrowed), (
            f"{name}: the element was narrowed and no finding says the author left the "
            f"item type unspecified: {narrowed}"
        )


def test_permissive_providers_keep_the_element_open() -> None:
    """Nothing is given up where nothing has to be: `items: {}` is the author's
    own meaning, and google/groq/cerebras/xai/together accept it (live, §15)."""
    wires = _wires()
    for provider in ("google", "groq", "cerebras", "xai", "together"):
        items = [node["items"] for node in _array_nodes(wires[provider])]
        assert items and all(item == {} for item in items), (provider, items)
