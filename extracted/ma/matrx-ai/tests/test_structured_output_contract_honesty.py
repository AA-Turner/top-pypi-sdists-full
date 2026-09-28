"""THE CONTRACT WE SEND MUST NOT LIE — about what it enforces, or about what it
still allows the model to say.

Arman, 2026-09-27: the shape we hold is modified by each provider's translator,
and a provider rejecting our request is OUR translator's bug. The corollary the
adversarial review (``common-docs/projects/checks-run-in-the-app/
SCHEMA-TRANSLATION-VERIFY.md``) found broken is the other half of it: a
compromise the boundary makes must be (a) as small as the provider forces,
(b) announced through the findings channel with the agent and the schema named,
and (c) never described in a docstring as something the platform does not do.

These checks judge the PRODUCTION functions from the outside, restating each
provider's rule from the provider's own refusal text rather than by calling the
rules under test. Every one of them fails on the pre-fix baseline ``476caca9a0``.
"""

from __future__ import annotations

import contextlib
import io
from typing import Any

import jsonschema
import pytest


def _quiet(fn: Any, *args: Any, **kwargs: Any) -> Any:
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        return fn(*args, **kwargs)


def _can_say_absent(wire: dict[str, Any], name: str) -> bool:
    """Can the model express "this field is absent" under the wire contract?

    It can iff ``null`` validates against the wire node — the boundary then prunes
    that null back to absence. Judged by ``jsonschema``, not by our own helpers.
    """
    node = (wire.get("properties") or {}).get(name)
    if not isinstance(node, dict):
        return False
    defs = {k: v for k, v in wire.items() if k in ("$defs", "definitions")}
    try:
        jsonschema.validate(instance=None, schema={**defs, **node})
    except jsonschema.ValidationError:
        return False
    return True


# ---------------------------------------------------------------------------
# A nested `$defs` (D1) — the pointer must resolve from the document ROOT
# ---------------------------------------------------------------------------

NESTED_DEFS_SCHEMA: dict[str, Any] = {
    "type": "object",
    "required": ["draft"],
    "additionalProperties": False,
    "properties": {
        "draft": {
            "type": "object",
            "additionalProperties": False,
            # The exact shape of the 17 live registered kinds: a self-contained
            # schema embedded whole under a parent's `properties`, bringing its
            # own `$defs` down with it while its pointers keep naming the root.
            "$defs": {
                "plan_draft_section": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["heading"],
                    "properties": {"heading": {"type": "string"}},
                }
            },
            "required": ["sections"],
            "properties": {
                "sections": {"type": "array", "items": {"$ref": "#/$defs/plan_draft_section"}}
            },
        }
    },
}


def _dangling(schema: Any, path: str = "$") -> list[str]:
    """Every local ``$ref`` that resolves to nothing FROM THE ROOT — the way both
    providers judge it: Anthropic ``Reference to non-existent definition:
    #/$defs/plan_draft_section``; OpenAI ``reference to component
    '#/$defs/plan_draft_section' which was not found in the schema``."""
    root = schema
    bad: list[str] = []

    def resolves(ref: str) -> bool:
        node: Any = root
        for raw in [part for part in ref.lstrip("#").split("/") if part]:
            part = raw.replace("~1", "/").replace("~0", "~")
            if isinstance(node, dict) and part in node:
                node = node[part]
            else:
                return False
        return True

    def walk(node: Any, where: str) -> None:
        if isinstance(node, list):
            for index, item in enumerate(node):
                walk(item, f"{where}[{index}]")
            return
        if not isinstance(node, dict):
            return
        ref = node.get("$ref")
        if isinstance(ref, str) and ref.startswith("#") and not resolves(ref):
            bad.append(f"{where}: {ref}")
        for key, value in node.items():
            if key != "$ref":
                walk(value, f"{where}.{key}")

    walk(schema, path)
    return bad


@pytest.mark.parametrize("provider", ["anthropic", "openai"])
def test_a_nested_defs_is_hoisted_so_every_pointer_resolves(provider: str) -> None:
    if provider == "anthropic":
        from matrx_ai.providers.anthropic.translator import AnthropicTranslator as T
    else:
        from matrx_ai.providers.openai.translator import OpenAITranslator as T

    wire, _, _ = _quiet(T.translate_output_schema, NESTED_DEFS_SCHEMA)

    assert not _dangling(wire), (
        f"{provider}: a pointer in the wire schema resolves to nothing — this is the "
        f"live 400 on 17 registered kinds: {_dangling(wire)}"
    )
    # Lossless: the definition still EXISTS and the array still points at it.
    items = wire["properties"]["draft"]["properties"]["sections"]["items"]
    assert "$ref" in items or items.get("type") == "object", items
    assert "draft" not in (wire.get("$defs") or {})


def test_the_forcing_function_names_an_unresolvable_pointer() -> None:
    """``structured_output_schema_violations`` is the function whose docstring
    promises that anything the subset still forbids is named HERE instead of
    arriving as an opaque provider 400. It had no resolvability check, which is
    exactly why this class walked through it to a live 400."""
    from matrx_ai.schema.rules import structured_output_schema_violations

    problems = structured_output_schema_violations(NESTED_DEFS_SCHEMA)

    assert any("plan_draft_section" in p for p in problems), (
        "the forcing function did not name the unresolvable pointer: " f"{problems}"
    )


def test_hoisting_keeps_two_unrelated_definitions_apart() -> None:
    """A nested name already taken at the root by a DIFFERENT body must not be
    merged onto it — that would silently swap one contract for another."""
    from matrx_ai.schema.rules import hoist_nested_defs

    schema = {
        "type": "object",
        "$defs": {"Row": {"type": "object", "properties": {"a": {"type": "string"}}}},
        "properties": {
            "top": {"$ref": "#/$defs/Row"},
            "nested": {
                "type": "object",
                "$defs": {"Row": {"type": "object", "properties": {"b": {"type": "integer"}}}},
                "properties": {"inner": {"$ref": "#/$defs/Row"}},
            },
        },
    }

    out = hoist_nested_defs(schema)

    assert not _dangling(out)
    top_ref = out["properties"]["top"]["$ref"].rsplit("/", 1)[-1]
    inner_ref = out["properties"]["nested"]["properties"]["inner"]["$ref"].rsplit("/", 1)[-1]
    assert top_ref != inner_ref, "two different `Row` definitions collapsed into one"
    assert "a" in out["$defs"][top_ref]["properties"]
    assert "b" in out["$defs"][inner_ref]["properties"]


# ---------------------------------------------------------------------------
# An optional field (D6) — required is fine, required-and-not-nullable is not
# ---------------------------------------------------------------------------

#: ``plan_node_specialist``'s real shape: ``gap_description`` exists to be set
#: ONLY when there is a gap, so a contract that demands it makes the model invent
#: one on every call.
OPTIONAL_FIELD_SCHEMA: dict[str, Any] = {
    "type": "object",
    "required": ["recommendations"],
    "additionalProperties": False,
    "properties": {
        "recommendations": {"type": "array", "items": {"type": "string"}},
        "gap_description": {"type": "string"},
        "__kind": {"type": "string", "const": "plan_node_recommendation"},
    },
}


@pytest.mark.parametrize("provider", ["anthropic", "openai"])
def test_an_optional_field_can_still_be_answered_absent(provider: str) -> None:
    if provider == "anthropic":
        from matrx_ai.providers.anthropic.translator import AnthropicTranslator as T
    else:
        from matrx_ai.providers.openai.translator import OpenAITranslator as T

    wire, narrowed, _ = _quiet(T.translate_output_schema, OPTIONAL_FIELD_SCHEMA)

    # Both providers demand every property in `required` — that part is theirs.
    assert set(wire["required"]) == set(wire["properties"]), wire["required"]
    # But the model must still be able to say "there is no gap".
    assert _can_say_absent(wire, "gap_description"), (
        f"{provider}: the wire contract forces a value for an optional field, so the "
        "model must invent one. Express it as nullable, or record the narrowing."
    )
    # `__kind` is determined, so forcing it takes nothing away and is NOT a finding.
    assert not _can_say_absent(wire, "__kind"), "a const property must stay pinned"
    assert not any("__kind" in note for note in narrowed), (
        f"{provider}: forcing a const property was reported as a loss: {narrowed}"
    )


def test_the_portable_contract_accepts_an_answer_the_declared_one_accepts() -> None:
    """``_make_portable`` is what the answer is VALIDATED against. Forcing an
    optional field there refused answers the author's own schema allows."""
    from matrx_ai.schema.lint import _make_portable
    from matrx_ai.schema.rules import prune_optional_nulls

    portable = _quiet(_make_portable, OPTIONAL_FIELD_SCHEMA)
    assert _can_say_absent(portable, "gap_description"), (
        "the portable contract cannot express the absence of an optional field"
    )

    # The round trip: the model says null, the reader turns it back into absence,
    # and the DECLARED contract — which never allowed null — is satisfied.
    answered = {"recommendations": ["split the node"], "gap_description": None}
    pruned = prune_optional_nulls(answered, OPTIONAL_FIELD_SCHEMA)
    assert "gap_description" not in pruned
    jsonschema.validate(instance=pruned, schema=OPTIONAL_FIELD_SCHEMA)
    # A null the author DID allow survives.
    nullable_schema = {
        "type": "object",
        "properties": {"maybe": {"type": ["string", "null"]}},
    }
    assert prune_optional_nulls({"maybe": None}, nullable_schema) == {"maybe": None}


def test_a_narrowing_that_cannot_be_avoided_names_the_fields() -> None:
    """Anthropic compiles at most 16 union parameters, so beyond that the
    nullability has to go. That is a real loss and it must arrive in the findings
    channel naming the fields — never as a silent policy."""
    from matrx_ai.providers.anthropic.translator import AnthropicTranslator

    schema: dict[str, Any] = {
        "type": "object",
        "required": [],
        "additionalProperties": False,
        "properties": {f"field_{i}": {"type": "string"} for i in range(30)},
    }

    wire, narrowed, _ = _quiet(AnthropicTranslator.translate_output_schema, schema)

    forced = [name for name in wire["properties"] if not _can_say_absent(wire, name)]
    assert forced, "this shape is meant to exceed the union budget"
    assert narrowed, (
        f"{len(forced)} optional fields lost their nullability and nothing was recorded"
    )
    joined = " ".join(narrowed)
    assert any(name in joined for name in forced), (
        f"the finding does not name a single field it narrowed: {narrowed}"
    )


# ---------------------------------------------------------------------------
# A dropped contract (D2) — prompt-guided AND checked, or say neither
# ---------------------------------------------------------------------------


def _drop_sites() -> list[tuple[str, Any]]:
    """Every place in the package that abandons provider enforcement, by name."""
    from matrx_ai.providers.anthropic.translator import AnthropicTranslator
    from matrx_ai.providers.google.translator import GoogleTranslator
    from matrx_ai.providers.openai.translator import OpenAITranslator

    return [
        ("anthropic", AnthropicTranslator._build_anthropic_output_format),
        ("openai", OpenAITranslator._build_openai_text_format),
        ("google", GoogleTranslator._build_google_response_schema),
    ]


@pytest.mark.parametrize("provider,builder", _drop_sites(), ids=[n for n, _ in _drop_sites()])
def test_dropping_enforcement_is_recorded_not_just_printed(provider: str, builder: Any) -> None:
    """A schema the provider cannot take (a non-object root) means the contract is
    not enforced at all. That is the loudest compromise in the system and it used
    to reach a console and nothing else."""
    import asyncio

    recorded: list[tuple[str, dict[str, Any]]] = []

    async def drive() -> None:
        import matrx_ai.providers.structured_output_findings as findings

        original = findings.record_structured_output_finding

        async def capture(key: str, **kwargs: Any) -> None:
            recorded.append((key, kwargs))

        findings.record_structured_output_finding = capture  # type: ignore[assignment]
        try:
            _quiet(
                builder,
                {"type": "json_schema", "schema": {"type": "array", "items": {"type": "string"}}},
            )
            # `record_structured_output_finding_sync` hands the write to a detached
            # task; let the loop run it.
            await asyncio.sleep(0)
            await asyncio.sleep(0)
        finally:
            findings.record_structured_output_finding = original  # type: ignore[assignment]

    asyncio.run(drive())

    assert recorded, (
        f"{provider}: a non-object-root schema abandoned provider enforcement and wrote "
        "no finding — a console line is not the issue surface"
    )
    key, kwargs = recorded[0]
    assert key.endswith("enforcement_dropped"), key
    assert kwargs["detail"].get("remedy"), (
        f"{provider}: the finding names no remedy — 'nothing fails silently' includes "
        "saying what to do about it"
    )


def test_an_enforcement_drop_puts_the_schema_in_the_prompt() -> None:
    """Anthropic's last rung removed ``output_config.format`` and sent nothing in
    its place, while its own finding said the answer was "prompt-guided"."""
    from matrx_ai.schema.answer_contract import (
        append_json_text_contract_to_system,
        json_text_contract,
    )

    schema = {"type": "object", "properties": {"verdict": {"type": "string"}}}

    for system in ("You are a careful analyst.", None):
        payload: dict[str, Any] = {"messages": []}
        if system is not None:
            payload["system"] = system
        append_json_text_contract_to_system(payload, schema)
        text = payload["system"]
        assert isinstance(text, str)
        assert "JSON Schema:" in text and "verdict" in text
        if system is not None:
            assert text.startswith(system), "the author's own system prompt was lost"

    # The list-of-blocks shape must not have its existing bytes rewritten — a cache
    # breakpoint was written against them.
    blocks = [{"type": "text", "text": "cached prefix", "cache_control": {"type": "ephemeral"}}]
    payload = {"system": list(blocks)}
    append_json_text_contract_to_system(payload, schema)
    assert payload["system"][0] == blocks[0]
    assert "JSON Schema:" in payload["system"][-1]["text"]
    assert "cache_control" not in payload["system"][-1]

    # ONE wording, shared: Google's production contract is now this function.
    from matrx_ai.providers.google.translator import GoogleTranslator

    assert GoogleTranslator._tool_json_text_contract(schema) == json_text_contract(schema)


def test_the_answer_is_checked_against_the_declared_schema() -> None:
    """``extract_json`` filters candidates on ``type`` + ``required`` at DEPTH 1, so
    it accepts an answer whose nested structure is wrong. The contract check must
    not be satisfied by the same evidence."""
    from matrx_ai.agents.response_parser import extract_json
    from matrx_ai.schema.answer_contract import verify_answer

    declared = {
        "type": "object",
        "required": ["rows"],
        "properties": {
            "rows": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": ["label", "score"],
                    "properties": {
                        "label": {"type": "string"},
                        "score": {"type": "integer"},
                    },
                },
            }
        },
    }
    wrong = '{"rows": [{"label": "a", "score": "not-a-number"}]}'

    assert extract_json(wrong, schema=declared) is not None, (
        "the depth-1 selector accepts this — that is the premise of this check"
    )
    problems = verify_answer(extract_json(wrong, schema=declared), declared)
    assert problems, "a nested type violation passed the contract check"
    assert any("score" in p for p in problems), problems

    good = extract_json('{"rows": [{"label": "a", "score": 3}]}', schema=declared)
    assert verify_answer(good, declared) == []


def test_a_null_the_boundary_asked_for_is_not_the_models_mistake() -> None:
    """The boundary forces an optional field into ``required`` and makes it
    nullable; the answer's ``null`` is then the boundary's compromise speaking, and
    must not be reported as the model breaking the declared contract."""
    from matrx_ai.schema.answer_contract import verify_answer

    declared = {
        "type": "object",
        "required": ["a"],
        "properties": {"a": {"type": "string"}, "b": {"type": "string"}},
    }

    assert verify_answer({"a": "x", "b": None}, declared) == []
    # A null where the author DID demand a value is still a failure.
    assert verify_answer({"a": None}, declared)


def test_the_capability_gates_record_what_they_throw_away() -> None:
    """``_downgrade_response_format`` and ``_resolve_tool_structured_output_conflict``
    sit ABOVE every translator, so a translator finding can never fire for them."""
    import asyncio
    from types import SimpleNamespace

    from matrx_ai.config import UnifiedConfig
    from matrx_ai.providers.resolved_capabilities import resolve_model_capabilities
    from matrx_ai.providers.unified_client import (
        _downgrade_response_format,
        _resolve_tool_structured_output_conflict,
    )

    schema = {"type": "object", "required": ["verdict"], "properties": {"verdict": {"type": "string"}}}

    def caps(features: list[str]):
        return resolve_model_capabilities(
            SimpleNamespace(
                name="test-model",
                capabilities={"input": ["text"], "output": ["text"], "features": features},
            )
        )

    async def drive() -> list[tuple[str, dict[str, Any]]]:
        import matrx_ai.providers.structured_output_findings as findings

        recorded: list[tuple[str, dict[str, Any]]] = []
        original = findings.record_structured_output_finding

        async def capture(key: str, **kwargs: Any) -> None:
            recorded.append((key, kwargs))

        findings.record_structured_output_finding = capture  # type: ignore[assignment]
        try:
            # (1) a model with no structured output at all — the schema is discarded
            downgraded = UnifiedConfig(
                model="test-model",
                messages=[],
                response_format={"type": "json_schema", "name": "verdict", "schema": schema},
            )
            _quiet(_downgrade_response_format, downgraded, caps([]), "openai_chat")
            # (2) an endpoint that refuses tools beside a response format
            shed = UnifiedConfig(
                model="test-model",
                messages=[],
                tools=["ctx_get"],
                response_format={"type": "json_schema", "name": "verdict", "schema": schema},
            )
            _quiet(
                _resolve_tool_structured_output_conflict,
                shed,
                caps(["function_calling", "structured_output"]),
                "cerebras_chat",
            )
            for _ in range(4):
                await asyncio.sleep(0)
            assert downgraded.response_format == {"type": "text"}, downgraded.response_format
            assert shed.tools == []
            # The contract the model can no longer be held to is in the prompt.
            staged = downgraded.messages.render_turn_context() or ""
            assert "JSON Schema:" in staged and "verdict" in staged, (
                "the discarded schema was not sent as prompt guidance either — "
                f"turn context was {staged!r}"
            )
            return recorded
        finally:
            findings.record_structured_output_finding = original  # type: ignore[assignment]

    recorded = asyncio.run(drive())
    keys = [key for key, _ in recorded]
    assert any(k.endswith("enforcement_dropped") for k in keys), (
        f"the capability downgrade discarded the schema and recorded nothing: {keys}"
    )
    assert any(k.endswith("tools_shed") for k in keys), (
        f"the whole tool surface was dropped and recorded nothing: {keys}"
    )
    for _, kwargs in recorded:
        assert kwargs["detail"].get("remedy"), kwargs["detail"]
