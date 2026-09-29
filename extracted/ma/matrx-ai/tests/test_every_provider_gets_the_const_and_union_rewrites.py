"""THE SHARED STEP OWNS A REWRITE EVERY PROVIDER NEEDS — F5 and F7.

Both defects in this file are the same mistake twice: a rule that only ONE
provider's boundary called, and a ceiling measured on a copy that was never sent.
Independent verification, 2026-09-28
(``common-docs/projects/checks-run-in-the-app/SCHEMA-TRANSLATION-VERIFY.md``):

* **F5 (HIGH)** — ``__kind: {"const": …}`` with no ``type`` made **78 live bound
  contracts unbindable on OpenAI**, 78 of 78 refused live
  (``400 invalid_json_schema: In context=('properties','__kind'), schema must have
  a 'type' key``), and it failed one item of a real OpenAI batch hours after it
  was queued. ``rewrite_const_as_enum`` already existed in
  ``matrx_ai.schema.rules`` and **only Google's translator called it**.
* **F7 (MEDIUM)** — 3 live wire copies went to Anthropic carrying 24 / 21 / 18
  union parameters over its documented 16 and were refused, while the
  translator's own notes said it had narrowed 25 fields to respect that cap:
  ``fits()`` read ``unions_before_collapse``, the count BEFORE the collapse, and
  the surplus left behind was DEGENERATE — ``anyOf: [A, A]``.

Every check below fails on the tree before the fix
(``git show HEAD:<path> > <path>``, never a stash) and passes after.
"""

from __future__ import annotations

import ast
import copy
import json
from pathlib import Path
from typing import Any

import jsonschema
import pytest

from matrx_ai.providers.anthropic.translator import AnthropicTranslator
from matrx_ai.providers.base_translator import BaseTranslator
from matrx_ai.providers.google.translator import GoogleTranslator
from matrx_ai.providers.openai.translator import OpenAITranslator
from matrx_ai.schema.lint import make_portable
from matrx_ai.schema.rules import (
    ANTHROPIC_UNION_PARAM_LIMIT,
    NORMALIZATION_NOTES_KEY,
    count_union_params,
)

try:  # the rule this file exists to pin — absent on the tree before the fix, so
    # importing it at module scope would turn every check below into one collection
    # error instead of the per-check red these defects deserve.
    from matrx_ai.schema.rules import dedupe_combinator_branches
except ImportError:  # pragma: no cover - only on the pre-fix tree
    dedupe_combinator_branches = None  # type: ignore[assignment]


def _dedupe(node: Any) -> Any:
    assert dedupe_combinator_branches is not None, (
        "matrx_ai.schema.rules exports no dedupe_combinator_branches: `A | A` "
        "reaches every provider's wire and costs a union slot for nothing"
    )
    return dedupe_combinator_branches(node)

KIND_SLUG = "flashcard_set"

#: A registered kind exactly as the platform stores one: `__kind` as a `const`
#: with NO `type` — which is what OpenAI refuses by name and what the `__kind`
#: law (KINDS_EVERYWHERE_PLAN.md §4.2a) requires on every schema.
KIND_SCHEMA: dict[str, Any] = {
    "type": "object",
    "additionalProperties": False,
    "required": ["__kind", "title", "cards"],
    "properties": {
        "__kind": {"const": KIND_SLUG},
        "title": {"type": "string"},
        "cards": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": ["__kind", "front", "back"],
                "properties": {
                    "__kind": {"const": "flashcard"},
                    "front": {"type": "string"},
                    "back": {"type": "string"},
                },
            },
        },
    },
}


def _degenerate_union_schema(n: int) -> dict[str, Any]:
    """The live Docker-Hub `getRepositoryTag` output shape, reproduced.

    Every property arrives as ``anyOf: [ anyOf: [ {"not": {}}, {"type": "string"} ],
    {"type": "null"} ]``. The translator empties the refinement branch and
    concretizes it into the SAME ``{"type": "string"}`` its sibling already was,
    so what reaches the wire is ``anyOf: [A, A]`` — a union parameter bought for
    nothing, and one that survives ``collapse_nullable_unions`` (narrowing the
    null away leaves the inner two-branch union in place). ``n`` of them is how a
    live schema reached Anthropic at 18 unions against a cap of 16.
    """
    return {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            f"field_{i}": {
                "anyOf": [
                    {"anyOf": [{"not": {}}, {"type": "string"}]},
                    {"type": "null"},
                ],
                "description": f"field {i}",
            }
            for i in range(n)
        },
    }


def _wire_schemas(schema: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """The copy each of the seven translators actually sends, through the real seams."""
    response_format = {
        "type": "json_schema",
        "json_schema": {"name": "probe", "schema": copy.deepcopy(schema)},
    }
    wires: dict[str, dict[str, Any]] = {}
    anthropic = AnthropicTranslator._build_anthropic_output_format(copy.deepcopy(response_format))
    wires["anthropic"] = anthropic["schema"]
    openai = OpenAITranslator._build_openai_text_format(copy.deepcopy(response_format))
    wires["openai"] = openai["schema"]
    wires["google"] = GoogleTranslator._build_google_response_schema(copy.deepcopy(response_format))
    for provider in ("groq", "cerebras", "xai", "together"):
        built = BaseTranslator.build_openai_chat_response_format(
            copy.deepcopy(response_format), provider
        )
        wires[provider] = built["json_schema"]["schema"]
    return wires


def _const_without_type(node: Any, path: str = "$") -> list[str]:
    """Every node OpenAI would refuse: a ``const`` with neither ``type`` nor ``enum``."""
    found: list[str] = []
    if isinstance(node, list):
        for index, item in enumerate(node):
            found.extend(_const_without_type(item, f"{path}[{index}]"))
        return found
    if not isinstance(node, dict):
        return found
    if "const" in node and "type" not in node and "enum" not in node:
        found.append(path)
    for key, value in node.items():
        if key in ("const", "enum", "required"):
            continue
        if key in ("properties", "$defs", "definitions") and isinstance(value, dict):
            for name, sub in value.items():
                found.extend(_const_without_type(sub, f"{path}.{key}.{name}"))
            continue
        found.extend(_const_without_type(value, f"{path}.{key}"))
    return found


def _marker_values(node: Any) -> list[Any] | None:
    """The set of values a wire copy's ROOT ``__kind`` still admits."""
    marker = (node.get("properties") or {}).get("__kind")
    if not isinstance(marker, dict):
        return None
    if "const" in marker:
        return [marker["const"]]
    enum = marker.get("enum")
    return list(enum) if isinstance(enum, list) else None


# ---------------------------------------------------------------------------
# F5 — the const rewrite belongs to the step ALL SEVEN translators share
# ---------------------------------------------------------------------------


def test_the_shared_first_step_rewrites_const_as_enum() -> None:
    """``make_portable`` is THE shared first step; the rewrite lives THERE."""
    portable = make_portable(copy.deepcopy(KIND_SCHEMA))
    marker = portable["properties"]["__kind"]
    assert "const" not in marker, (
        "make_portable left `const` in place, so every provider whose translator "
        "does not call rewrite_const_as_enum itself still sends it: OpenAI answers "
        "400 'schema must have a type key'."
    )
    assert marker["enum"] == [KIND_SLUG]
    nested = portable["properties"]["cards"]["items"]["properties"]["__kind"]
    assert nested["enum"] == ["flashcard"], "the rewrite must reach every depth"


def test_no_provider_sends_a_const_node_without_a_type() -> None:
    """All seven wires, measured — this is the live 400, in one assertion."""
    offenders = {
        provider: _const_without_type(wire)
        for provider, wire in _wire_schemas(KIND_SCHEMA).items()
        if _const_without_type(wire)
    }
    assert offenders == {}, (
        "these providers receive a `const` node carrying no `type`; OpenAI refuses "
        f"it outright and Gemini's decoder invents a value instead: {offenders}"
    )


def test_the_kind_marker_survives_with_exactly_one_allowed_value() -> None:
    """THE ``__kind`` LAW: the marker reaches the wire, pinned, on every provider.

    The rewrite is allowed to change the SPELLING and nothing else. Proven by
    validating answers against the wire copy itself, not by reading keywords.
    """
    for provider, wire in _wire_schemas(KIND_SCHEMA).items():
        assert _marker_values(wire) == [KIND_SLUG], (
            f"{provider}: the wire copy no longer pins __kind to exactly "
            f"{KIND_SLUG!r} — got {_marker_values(wire)!r}"
        )
        assert "__kind" in (wire.get("required") or []), f"{provider}: __kind left optional"
        right = {"__kind": KIND_SLUG, "title": "t", "cards": []}
        jsonschema.validate(instance=right, schema=wire)
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(
                instance={**right, "__kind": "something_the_model_invented"}, schema=wire
            )


def test_no_translator_owns_the_const_rewrite_privately() -> None:
    """The class fix, not the instance: a provider module that calls the rewrite
    itself is a rule one provider has and the other six do not — which is exactly
    how 78 live contracts stayed unbindable on OpenAI for as long as they did. The
    live request boundary is ``make_portable``; the batch schema converter
    (``google/batch_schema.py``) is not a translator and keeps its own call,
    because it may be handed a raw stored schema."""
    providers = Path(AnthropicTranslator.__module__.replace(".", "/")).parents[1]
    root = Path(__file__).resolve().parents[1] / "matrx_ai" / "providers"
    assert root.is_dir(), root
    callers: dict[str, list[int]] = {}
    for path in sorted(root.rglob("translator.py")):
        tree = ast.parse(path.read_text())
        lines = [
            node.lineno
            for node in ast.walk(tree)
            if isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "rewrite_const_as_enum"
        ]
        if lines:
            callers[str(path.relative_to(root))] = lines
    assert callers == {}, (
        "a provider translator calls rewrite_const_as_enum on its own; move it to "
        f"the shared first step so every provider inherits it: {callers} ({providers})"
    )


# ---------------------------------------------------------------------------
# F7 — a degenerate union, and a ceiling measured on the copy being SENT
# ---------------------------------------------------------------------------


def test_dedupe_drops_a_duplicate_branch_and_collapses_a_lone_union() -> None:
    out = _dedupe(
        {"anyOf": [{"type": "string"}, {"type": "string"}], "description": "d"}
    )
    assert out == {"type": "string", "description": "d"}, out


def test_dedupe_ignores_our_own_bookkeeping_and_keeps_the_note() -> None:
    """Two branches that differ ONLY in ``x-matrx-normalization-notes`` are the
    same schema to the provider — that key is stripped before the wire. Comparing
    them with the note in place is precisely what let the live degenerate union
    through, and the note must still reach the findings channel."""
    note = "empty schema ({}) narrowed to type='string'"
    out = _dedupe(
        {
            "anyOf": [
                {"type": "string", NORMALIZATION_NOTES_KEY: [note]},
                {"type": "string"},
            ]
        }
    )
    assert out.get("type") == "string", out
    assert "anyOf" not in out, out
    assert note in (out.get(NORMALIZATION_NOTES_KEY) or []), (
        "the duplicate was dropped and its normalization note went with it — that "
        "is a compromise the reader would never hear about"
    )


def test_a_real_union_and_a_property_named_const_are_untouched() -> None:
    """No-regression guard: this must pass in BOTH directions."""
    real = {"anyOf": [{"type": "string"}, {"type": "number"}]}
    assert _dedupe(copy.deepcopy(real)) == real
    named = {
        "type": "object",
        "properties": {"const": {"type": "string"}, "anyOf": {"type": "integer"}},
    }
    assert _dedupe(copy.deepcopy(named)) == named
    # A property literally NAMED `const` keeps its name and its declared type —
    # the rewrite reads keyword positions, never property names. (It is optional,
    # so the shared step widens it to nullable, which is the lossless posture.)
    widened = make_portable(copy.deepcopy(named))["properties"]["const"]
    assert widened == {"anyOf": [{"type": "string"}, {"type": "null"}]}, widened


@pytest.mark.parametrize("width", [18, 21, 24, 40])
def test_the_anthropic_wire_never_exceeds_the_documented_union_cap(width: int) -> None:
    """``fits()`` has to measure the copy being SENT.

    The three live refusals scored 24 / 21 / 18 unions on the wire while the
    translator believed it had respected the cap. Over the live shape at four
    widths, the copy Anthropic receives must be at or under the documented
    ceiling.
    """
    wire = _wire_schemas(_degenerate_union_schema(width))["anthropic"]
    unions = count_union_params(wire)
    assert unions <= ANTHROPIC_UNION_PARAM_LIMIT, (
        f"{width} degenerate unions in, {unions} union parameters out — over "
        f"Anthropic's documented {ANTHROPIC_UNION_PARAM_LIMIT}; it answers "
        '400 "Schemas contains too many parameters with union types"'
    )


def test_every_shared_translator_endpoint_can_actually_be_PROBED() -> None:
    """Evidence has to be reachable for every endpoint the shared translator feeds.

    ``translate_openai_compatible_output_schema`` builds the body for cerebras,
    groq, xai and together from ONE code path, and until 2026-09-28 the probe
    primitive could only call Cerebras — so a change to that path could be proven
    on one of the four endpoints it feeds. A new provider added to the subset table
    without a probe endpoint puts us back there.
    """
    from matrx_ai.providers.structured_output_probe import OPENAI_COMPATIBLE_CHAT_ENDPOINTS

    fed = set(BaseTranslator._OPENAI_COMPATIBLE_SUBSET) - {"generic_openai"}
    missing = sorted(fed - set(OPENAI_COMPATIBLE_CHAT_ENDPOINTS))
    assert missing == [], (
        f"{missing} reach the wire through the shared OpenAI-compatible translator "
        "but have no probe endpoint, so nothing can ask them whether they accept it"
    )


def test_the_sent_wire_carries_no_degenerate_union_on_any_provider() -> None:
    """Not just Anthropic: ``A | A`` is compiled twice for nothing everywhere."""
    for provider, wire in _wire_schemas(_degenerate_union_schema(18)).items():
        duplicates: list[str] = []

        def walk(node: Any, path: str = "$") -> None:
            if isinstance(node, list):
                for index, item in enumerate(node):
                    walk(item, f"{path}[{index}]")
                return
            if not isinstance(node, dict):
                return
            for combinator in ("anyOf", "oneOf", "allOf"):
                branches = node.get(combinator)
                if isinstance(branches, list):
                    seen = [
                        json.dumps(branch, sort_keys=True, separators=(",", ":"), default=str)
                        for branch in branches
                    ]
                    if len(set(seen)) != len(seen):
                        duplicates.append(f"{path}.{combinator}")
            for key, value in node.items():
                if key in ("const", "enum", "required"):
                    continue
                walk(value, f"{path}.{key}")

        walk(wire)
        assert duplicates == [], f"{provider} receives duplicate branches at {duplicates}"
