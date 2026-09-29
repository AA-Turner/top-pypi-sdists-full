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
            # Whether the call was recovered is only known once it has run: the
            # gates HOLD their findings and the dispatch seam's flush writes them
            # with the real outcome (SCHEMA-TRANSLATION-VERIFY.md, R11).
            assert recorded == [], (
                "a gate wrote was_recovered before the provider was even called: "
                f"{[(k, kw.get('was_recovered')) for k, kw in recorded]}"
            )
            await findings.flush_translation_findings(model="test-model", succeeded=False)
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
        # The call failed, so nothing was recovered — and the row says so.
        assert kwargs["was_recovered"] is False, kwargs
        assert "FAILED" in kwargs["detail"].get("outcome", ""), kwargs["detail"]


# ---------------------------------------------------------------------------
# The five OpenAI-compatible providers (D3) — same completeness, and audible
# ---------------------------------------------------------------------------

#: Every provider whose structured output reaches the wire through
#: ``BaseTranslator.build_openai_chat_response_format`` and which, until
#: 2026-09-27, got only an advisory-keyword strip and no findings at all.
COMPATIBLE_PROVIDERS = ["cerebras", "groq", "xai", "together", "generic_openai"]


@pytest.mark.parametrize("provider", COMPATIBLE_PROVIDERS)
def test_a_compatible_provider_gets_a_resolvable_schema(provider: str) -> None:
    """Measured live 2026-09-27: a dangling ``$ref`` (a nested ``$defs``) is refused
    by name on groq (``json-pointer … not found``), xai (``unresolvable $ref``),
    together (``failed to compile grammar``) and cerebras under strict — four more
    providers than the review found."""
    from matrx_ai.providers.base_translator import BaseTranslator

    out = _quiet(
        BaseTranslator.build_openai_chat_response_format,
        {"type": "json_schema", "name": "r", "schema": NESTED_DEFS_SCHEMA},
        provider,
    )

    assert out and out["type"] == "json_schema", out
    wire = out["json_schema"]["schema"]
    assert not _dangling(wire), f"{provider}: {_dangling(wire)}"


@pytest.mark.parametrize("provider", COMPATIBLE_PROVIDERS)
def test_a_compatible_provider_gets_no_tuple_items(provider: str) -> None:
    """``items: [A, B]`` — groq 400 ``not valid against metaschema``, xai 400 ``is
    not of type object``, together 422 ``failed to compile grammar``."""
    from matrx_ai.providers.base_translator import BaseTranslator

    schema = {
        "type": "object",
        "required": ["t"],
        "additionalProperties": False,
        "properties": {"t": {"type": "array", "items": [{"type": "string"}, {"type": "integer"}]}},
    }

    out = _quiet(
        BaseTranslator.build_openai_chat_response_format,
        {"type": "json_schema", "name": "r", "schema": schema},
        provider,
    )

    wire = out["json_schema"]["schema"]
    tuples = [node for node in _walk_dicts(wire) if isinstance(node.get("items"), list)]
    assert not tuples, f"{provider}: tuple items survived translation"


def _walk_dicts(node: Any):
    if isinstance(node, dict):
        yield node
        for key, value in node.items():
            if key in ("enum", "const", "required"):
                continue
            yield from _walk_dicts(value)
    elif isinstance(node, list):
        for item in node:
            yield from _walk_dicts(item)


@pytest.mark.parametrize("provider", ["together", "generic_openai"])
def test_a_provider_that_cannot_compile_recursion_does_not_receive_it(provider: str) -> None:
    """Together answers **500 Internal server error** on a self-referencing
    ``$def`` — an outcome no caller can classify, and the one refusal a retry
    cannot help with."""
    from matrx_ai.providers.base_translator import BaseTranslator

    schema = {
        "type": "object",
        "required": ["node"],
        "additionalProperties": False,
        "$defs": {
            "N": {
                "type": "object",
                "required": ["kids"],
                "additionalProperties": False,
                "properties": {"kids": {"type": "array", "items": {"$ref": "#/$defs/N"}}},
            }
        },
        "properties": {"node": {"$ref": "#/$defs/N"}},
    }

    out = _quiet(
        BaseTranslator.build_openai_chat_response_format,
        {"type": "json_schema", "name": "r", "schema": schema},
        provider,
    )

    wire = out["json_schema"]["schema"]
    defs = wire.get("$defs") or {}
    for name, body in defs.items():
        refs = [n["$ref"] for n in _walk_dicts(body) if isinstance(n.get("$ref"), str)]
        assert f"#/$defs/{name}" not in refs, f"{provider}: {name} still references itself"


@pytest.mark.parametrize("provider", COMPATIBLE_PROVIDERS)
def test_a_compatible_provider_reports_what_it_gave_up(provider: str) -> None:
    """These five never called ``note_translation``, so every compromise they made
    was invisible — the reason a sweep of the live corpus found thousands of
    untranslated shapes and not one finding."""
    from matrx_ai.providers.base_translator import BaseTranslator
    from matrx_ai.providers.structured_output_findings import (
        begin_translation_findings,
        end_translation_findings,
    )

    # A shape that forces a REAL loss on every one of them: a tuple `items`, which
    # collapses to a single schema.
    schema = {
        "type": "object",
        "required": ["t"],
        "additionalProperties": False,
        "properties": {"t": {"type": "array", "items": [{"type": "string"}, {"type": "integer"}]}},
    }

    token = begin_translation_findings()
    try:
        _quiet(
            BaseTranslator.build_openai_chat_response_format,
            {"type": "json_schema", "name": "r", "schema": schema},
            provider,
        )
        import matrx_ai.providers.structured_output_findings as findings

        buffered = list(findings._PENDING.get() or [])
    finally:
        end_translation_findings(token)

    assert buffered, f"{provider}: the translation gave something up and buffered no finding"
    assert buffered[0]["provider"] == provider
    assert buffered[0]["schema_name"] == "r", buffered[0]
    assert buffered[0]["narrowed"] or buffered[0]["relaxed"], buffered[0]


def test_a_map_a_provider_accepts_is_not_narrowed_for_nothing() -> None:
    """Measured 2026-09-27 at an adequate token budget: groq, cerebras, xai and
    together all accept a dynamic-key map (200). The review's groq 400s were
    ``json_validate_failed`` — groq's own check of a TRUNCATED answer, not a
    rejection of the schema — so emptying the map here would throw the author's
    contract away to fix a problem that does not exist."""
    from matrx_ai.providers.base_translator import BaseTranslator

    schema = {
        "type": "object",
        "required": ["m"],
        "additionalProperties": False,
        "properties": {"m": {"type": "object", "additionalProperties": {"type": "string"}}},
    }

    for provider in COMPATIBLE_PROVIDERS:
        out = _quiet(
            BaseTranslator.build_openai_chat_response_format,
            {"type": "json_schema", "name": "r", "schema": schema},
            provider,
        )
        node = out["json_schema"]["schema"]["properties"]["m"]
        assert node.get("additionalProperties") == {"type": "string"}, (
            f"{provider}: a map the provider accepts was emptied anyway — {node}"
        )


def test_groq_says_so_when_it_sheds_every_tool() -> None:
    """Groq forbids json mode beside tools, so it drops the whole tool surface —
    on every such request, and it told only a console. Anthropic's ladder writes
    ``tools_shed`` plus a user-facing warning for the identical outcome."""
    import asyncio
    from types import SimpleNamespace

    from matrx_ai.config import UnifiedConfig

    async def drive() -> list[tuple[str, dict[str, Any]]]:
        import matrx_ai.providers.structured_output_findings as findings
        from matrx_ai.providers.groq.translator import GroqTranslator

        recorded: list[tuple[str, dict[str, Any]]] = []
        original = findings.record_structured_output_finding

        async def capture(key: str, **kwargs: Any) -> None:
            recorded.append((key, kwargs))

        findings.record_structured_output_finding = capture  # type: ignore[assignment]
        try:
            config = UnifiedConfig(
                model="groq/test",
                messages=[],
                custom_tools=[
                    {
                        "name": "lookup",
                        "description": "Look something up.",
                        "input_schema": {"type": "object", "properties": {}},
                    }
                ],
                response_format={
                    "type": "json_schema",
                    "name": "verdict",
                    "schema": {
                        "type": "object",
                        "required": ["verdict"],
                        "additionalProperties": False,
                        "properties": {"verdict": {"type": "string"}},
                    },
                },
            )
            from matrx_ai.catalog.controls import CompiledControlsMap

            profile = SimpleNamespace(
                controls=CompiledControlsMap(),
                model_name="groq/test",
                provider_model_id="openai/gpt-oss-20b",
            )
            _quiet(GroqTranslator().to_groq, config, profile)
            for _ in range(4):
                await asyncio.sleep(0)
            # The shed happens while the request is still being BUILT, so whether it
            # recovered anything is not a fact yet: the finding is HELD and the
            # dispatch seam's flush writes it with the call's real outcome
            # (SCHEMA-TRANSLATION-VERIFY.md, F2 — the same rule as the gates).
            assert recorded == [], (
                "groq claimed a recovery before the provider was even called: "
                f"{[(k, kw.get('was_recovered')) for k, kw in recorded]}"
            )
            await findings.flush_translation_findings(
                model="groq/test", succeeded=True, answer_off_contract=False
            )
            return recorded
        finally:
            findings.record_structured_output_finding = original  # type: ignore[assignment]

    recorded = asyncio.run(drive())
    keys = [key for key, _ in recorded]
    assert any(k.endswith("tools_shed") for k in keys), (
        f"groq dropped every tool and recorded nothing: {keys}"
    )
    shed = next(kwargs for key, kwargs in recorded if key.endswith("tools_shed"))
    assert shed["was_recovered"] is True and "ON CONTRACT" in shed["detail"]["outcome"], shed
    detail = next(kwargs["detail"] for key, kwargs in recorded if key.endswith("tools_shed"))
    assert detail.get("schema_name") == "verdict", detail
    assert detail.get("dropped_tools"), detail
    assert detail.get("remedy"), detail


# ---------------------------------------------------------------------------
# Attribution (D5) — a finding names BOTH the agent and the shape, or it is noise
# ---------------------------------------------------------------------------


def test_a_schema_with_no_name_is_still_named_by_its_kind() -> None:
    """Every Google finding landed with ``schema_name`` null: the hydrated Gemini
    envelope carries no ``name`` and nothing else was read, so the reader was told
    which agent and not which shape. A registered kind states its identity INSIDE
    the schema, as the ``__kind`` const."""
    from matrx_ai.providers.structured_output_findings import response_format_identity

    kind_schema = {
        "type": "object",
        "required": ["__kind"],
        "properties": {
            "__kind": {"type": "string", "const": "seo.site_intake.offer"},
            "pages": {"type": "array", "items": {"type": "string"}},
        },
    }

    identity = response_format_identity({"type": "json_schema", "schema": kind_schema})
    assert identity["schema_name"] == "seo.site_intake.offer", identity
    assert identity["schema_fingerprint"], identity

    # A `title` is the next best name when there is no discriminator.
    titled = response_format_identity(
        {"type": "json_schema", "schema": {"title": "ResaleReport", "type": "object"}}
    )
    assert titled["schema_name"] == "ResaleReport", titled

    # An explicit name still wins.
    named = response_format_identity(
        {"type": "json_schema", "name": "explicit", "schema": kind_schema}
    )
    assert named["schema_name"] == "explicit", named


def test_the_identity_fallbacks_read_keys_something_actually_writes() -> None:
    """The fallback added on 2026-09-27 read ``agent_run_label`` and
    ``surface_name``. Neither is ever written to ``AppContext.metadata`` anywhere in
    either repository — ``agent_run_label`` lives in the ``context`` JSONB of a
    ``runtime.global_execution`` row — so it could not fire, and 65 of 68 live
    findings arrived with no agent named. A fallback that cannot fire is the same
    defect as no fallback, wearing a comment that says otherwise."""
    from matrx_ai.providers.structured_output_findings import _IDENTITY_METADATA_KEYS

    assert "agent_run_label" not in _IDENTITY_METADATA_KEYS
    assert "surface_name" not in _IDENTITY_METADATA_KEYS
    # The keys an internal run really carries (agents/executor.py writes both).
    assert "conversation_step_label" in _IDENTITY_METADATA_KEYS
    assert "agent_name" in _IDENTITY_METADATA_KEYS


def test_an_internal_run_with_no_agent_id_is_still_attributed() -> None:
    """An agent-factory run reaches the provider with no ``agent_id`` on some
    paths. The finding must still name something a person can act on — and when
    there is genuinely nothing, it must SAY it is unattributed rather than leave
    an empty column that reads like a clean row."""
    from types import SimpleNamespace

    import matrx_ai.providers.structured_output_findings as findings

    class _Ctx(SimpleNamespace):
        pass

    def identity_for(ctx: Any) -> dict[str, Any]:
        import matrx_connect

        original = matrx_connect.try_get_app_context
        matrx_connect.try_get_app_context = lambda: ctx  # type: ignore[assignment]
        try:
            return findings._agent_identity()
        finally:
            matrx_connect.try_get_app_context = original  # type: ignore[assignment]

    labelled = identity_for(
        _Ctx(
            agent_id=None,
            agent_version_id=None,
            source_feature="agent_structure_builder",
            route="/agent-factory/build",
            metadata={
                "conversation_step_label": "agent_factory:Resell Research Agent",
                "runtime_execution_id": "11111111-2222-3333-4444-555555555555",
            },
        )
    )
    assert labelled["conversation_step_label"].startswith("agent_factory:"), labelled
    assert labelled["runtime_execution_id"], labelled
    assert "agent_attribution" not in labelled, labelled

    naked = identity_for(_Ctx(agent_id=None, agent_version_id=None, metadata={}))
    assert naked.get("agent_attribution", "").startswith("UNATTRIBUTED"), naked


def test_every_finding_path_names_both_the_agent_and_the_shape() -> None:
    """Measured over all 89 live rows on 2026-09-27: not one named both. This
    drives the finding paths this lane owns and insists on both halves."""
    import asyncio
    from types import SimpleNamespace

    import matrx_connect

    from matrx_ai.config import UnifiedConfig
    from matrx_ai.providers.resolved_capabilities import resolve_model_capabilities

    kind_schema = {
        "type": "object",
        "required": ["__kind"],
        "additionalProperties": False,
        "properties": {"__kind": {"type": "string", "const": "seo.site_intake.offer"}},
    }
    ctx = SimpleNamespace(
        agent_id=None,
        agent_version_id="aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee",
        source_feature="agent_structure_builder",
        route="/agent-factory/build",
        metadata={"agent_name": "Site Intake Analyst"},
    )

    async def drive() -> list[dict[str, Any]]:
        import matrx_ai.providers.structured_output_findings as findings

        seen: list[dict[str, Any]] = []
        original_record = findings.record_structured_output_finding
        original_ctx = matrx_connect.try_get_app_context

        async def capture(key: str, **kwargs: Any) -> None:
            seen.append({"key": key, **kwargs["detail"]})

        findings.record_structured_output_finding = capture  # type: ignore[assignment]
        matrx_connect.try_get_app_context = lambda: ctx  # type: ignore[assignment]
        try:
            caps = resolve_model_capabilities(
                SimpleNamespace(
                    name="test-model",
                    capabilities={"input": ["text"], "output": ["text"], "features": []},
                )
            )
            from matrx_ai.providers.unified_client import _downgrade_response_format

            # A json_schema envelope with NO `name` — the Google-shaped case.
            config = UnifiedConfig(
                model="test-model",
                messages=[],
                response_format={"type": "json_schema", "schema": kind_schema},
            )
            _quiet(_downgrade_response_format, config, caps, "openai_chat")
            # The gate HOLDS its finding until the call's outcome is known (R11);
            # the identity was captured when the gate fired, in this context.
            matrx_connect.try_get_app_context = lambda: None  # type: ignore[assignment]
            await findings.flush_translation_findings(model="test-model", succeeded=True)
            for _ in range(4):
                await asyncio.sleep(0)
            return seen
        finally:
            findings.record_structured_output_finding = original_record  # type: ignore[assignment]
            matrx_connect.try_get_app_context = original_ctx  # type: ignore[assignment]

    seen = asyncio.run(drive())

    assert seen, "the capability downgrade recorded nothing"
    for row in seen:
        agent = {
            k: row.get(k)
            for k in ("agent_id", "agent_version_id", "mandate_key", "agent_name", "conversation_step_label")
            if row.get(k)
        }
        assert agent, f"{row['key']} names no agent: {sorted(row)}"
        assert row.get("schema_name"), f"{row['key']} names no shape: {sorted(row)}"
        assert row["schema_name"] == "seo.site_intake.offer", row["schema_name"]
        assert row.get("schema_fingerprint"), row


def test_the_contract_check_never_skips_itself_silently() -> None:
    """A check that quietly does not run is worse than no check.

    ``UnifiedMessage`` accepts a bare string for ``content``, and ``get_output()``
    then raises ``AttributeError: 'str' object has no attribute 'get_output'``. The
    first version of this module returned "" on that exception, so the contract
    check was SKIPPED and reported nothing — the very defect this module exists to
    fix, reproduced inside the fix. Found by driving a real provider call through
    it, not by reading it.
    """
    import asyncio

    from matrx_ai.config import Role, UnifiedMessage, UnifiedResponse
    from matrx_ai.schema.answer_contract import (
        bind_declared_output_contract,
        release_declared_output_contract,
        verify_answer_and_record,
    )

    declared = {
        "type": "object",
        "required": ["rows"],
        "additionalProperties": False,
        "properties": {
            "rows": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": ["label", "score"],
                    "additionalProperties": False,
                    "properties": {
                        "label": {"type": "string"},
                        "score": {"type": "integer"},
                    },
                },
            }
        },
    }
    wrong = '```json\n{"rows": [{"label": "apple", "score": "high"}]}\n```'

    async def drive(content: Any) -> tuple[list[str], list[str]]:
        import matrx_ai.providers.structured_output_findings as findings

        keys: list[str] = []
        original = findings.record_structured_output_finding

        async def capture(key: str, **kwargs: Any) -> None:
            keys.append(key)

        findings.record_structured_output_finding = capture  # type: ignore[assignment]
        token = bind_declared_output_contract(
            {"type": "json_schema", "name": "scored_rows", "schema": declared}
        )
        try:
            response = UnifiedResponse(
                messages=[UnifiedMessage(role=Role.ASSISTANT, content=content)],
                usage=None,
                finish_reason="stop",
            )
            problems = await _aquiet(
                verify_answer_and_record, response, provider="anthropic", model="claude-sonnet-5"
            )
            return problems, keys
        finally:
            release_declared_output_contract(token)
            findings.record_structured_output_finding = original  # type: ignore[assignment]

    # A bare string — the shape that used to make the check vanish.
    problems, keys = asyncio.run(drive(wrong))
    assert problems, "the check skipped itself on a plain-string message content"
    assert any("score" in p for p in problems), problems
    assert any(k.endswith("answer_off_contract") for k in keys), keys

    # A conforming answer records nothing.
    good = '```json\n{"rows": [{"label": "apple", "score": 8}]}\n```'
    problems, keys = asyncio.run(drive(good))
    assert problems == [] and keys == [], (problems, keys)


async def _aquiet(fn: Any, *args: Any, **kwargs: Any) -> Any:
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        return await fn(*args, **kwargs)


# ---------------------------------------------------------------------------
# A provider refusal is OUR translator's bug, never a rule we write down
# ---------------------------------------------------------------------------
#
# Arman, 2026-09-27: "we have translators for each schema type and they are
# supposed to take in any input and make it safe for the exact api. Fix it at the
# core and don't do a workaround."


def _recursive_topic_map(children: dict[str, Any]) -> dict[str, Any]:
    """`seo.map_author`'s shape: a self-referencing node reached through a list."""
    return {
        "type": "object",
        "additionalProperties": False,
        "$defs": {
            "MapTopicNode": {
                "type": "object",
                "additionalProperties": False,
                "required": ["slug", "name", "children"],
                "properties": {
                    "slug": {"type": "string"},
                    "name": {"type": "string"},
                    "children": children,
                },
            }
        },
        "required": ["topics"],
        "properties": {
            "topics": {"type": "array", "items": {"$ref": "#/$defs/MapTopicNode"}}
        },
    }


def test_a_ref_cycle_is_made_expressible_not_excused() -> None:
    """Gemini names its own rule in the refusal: "ref loops are only supported if
    they include optional or nullable property values, or a potentially-zero-length
    array items". Measured live on gemini-3.8-flash 2026-09-27, one request per
    form — and "nullable" does NOT mean a type array:

        required + plain array           200
        required + type:["array","null"] 400   <-- what our portable step produced
        required + anyOf[array, null]    200
        optional (out of required)        200
        required + array minItems:1      400
    """
    from matrx_ai.schema.rules import gemini_ref_loop_violations, open_ref_loops

    # (1) the live failure: a required, type-array-nullable loop carrier.
    type_array_nullable = _recursive_topic_map(
        {"type": ["array", "null"], "items": {"$ref": "#/$defs/MapTopicNode"}}
    )
    assert gemini_ref_loop_violations(type_array_nullable), (
        "the forcing function does not see the shape the provider refuses"
    )
    opened = open_ref_loops(type_array_nullable, narrowed=[], relaxed=[])
    assert not gemini_ref_loop_violations(opened)
    carrier = opened["$defs"]["MapTopicNode"]["properties"]["children"]
    branches = carrier["anyOf"]
    assert any(b.get("type") == "null" for b in branches), carrier
    assert any(b.get("type") == "array" for b in branches), carrier
    # Lossless: the cycle still exists and still points at the definition.
    array_branch = next(b for b in branches if b.get("type") == "array")
    assert array_branch["items"]["$ref"] == "#/$defs/MapTopicNode"

    # (2) a minimum-length floor stops the cycle terminating — a RELAXATION, named.
    floored = _recursive_topic_map(
        {"type": "array", "minItems": 1, "items": {"$ref": "#/$defs/MapTopicNode"}}
    )
    assert gemini_ref_loop_violations(floored)
    relaxed: list[str] = []
    opened = open_ref_loops(floored, narrowed=[], relaxed=relaxed)
    assert not gemini_ref_loop_violations(opened)
    assert relaxed and "minItems" in relaxed[0], relaxed

    # (3) a cycle with no escape at all is unrolled — a NARROWING, named.
    inescapable = {
        "type": "object",
        "additionalProperties": False,
        "$defs": {
            "N": {
                "type": "object",
                "additionalProperties": False,
                "required": ["child"],
                "properties": {"child": {"$ref": "#/$defs/N"}},
            }
        },
        "required": ["root"],
        "properties": {"root": {"$ref": "#/$defs/N"}},
    }
    assert gemini_ref_loop_violations(inescapable)
    narrowed: list[str] = []
    opened = open_ref_loops(inescapable, narrowed=narrowed, relaxed=[])
    assert not gemini_ref_loop_violations(opened)
    assert narrowed, "an unrolled cycle is a narrowing and must be recorded"

    # (4) the author's own shape — an OPTIONAL carrier — is already fine and is
    # left exactly as declared.
    as_authored = _recursive_topic_map(
        {"type": "array", "items": {"$ref": "#/$defs/MapTopicNode"}}
    )
    as_authored["$defs"]["MapTopicNode"]["required"] = ["slug", "name"]
    assert gemini_ref_loop_violations(as_authored) == []
    assert open_ref_loops(as_authored, narrowed=[], relaxed=[]) == as_authored


def test_the_google_translator_emits_a_cycle_gemini_can_compile() -> None:
    """End to end through the translator's own entry point, on the schema the
    portable step forces: the cycle must come out in the form Gemini accepts."""
    from matrx_ai.providers.google.translator import GoogleTranslator
    from matrx_ai.schema.rules import gemini_ref_loop_violations

    forced = _recursive_topic_map(
        {"type": ["array", "null"], "items": {"$ref": "#/$defs/MapTopicNode"}}
    )

    wire = _quiet(
        GoogleTranslator._build_google_response_schema,
        {"type": "json_schema", "name": "map_topic_proposal", "schema": forced},
    )

    assert wire is not None, "structured output was dropped instead of translated"
    assert gemini_ref_loop_violations(wire) == [], gemini_ref_loop_violations(wire)


def test_a_nullable_enum_is_not_sent_as_a_type_array() -> None:
    """Anthropic refuses an enum beside a type ARRAY outright, and it fires even
    when the enum holds no null — so it is the type array it objects to:

        {"type": ["string","null"], "enum": ["a","b"]}
            -> Invalid schema: Enum value 'a' does not match declared type
               '['string', 'null']'
        {"anyOf": [{"type":"string","enum":["a","b"]}, {"type":"null"}]}  -> 200

    `Optional[SomeEnum]` in Pydantic emits exactly the refused shape, so every
    live contract with a nullable enum was refused all along — research_page_analysis
    (page_type, analysis_status, recommended_use) is one.
    """
    from matrx_ai.providers.anthropic.translator import AnthropicTranslator
    from matrx_ai.providers.openai.translator import OpenAITranslator
    from matrx_ai.schema.rules import split_enum_from_type_union

    declared = {
        "type": "object",
        "required": ["status"],
        "additionalProperties": False,
        "properties": {
            "status": {"type": ["string", "null"], "enum": ["valid", "invalid", None]},
            "page_type": {"type": "string", "enum": ["news", "blog"]},
        },
    }

    split = split_enum_from_type_union(declared)
    node = split["properties"]["status"]
    assert "type" not in node, node
    branches = node["anyOf"]
    assert {"type": "null"} in branches, branches
    enum_branch = next(b for b in branches if "enum" in b)
    assert enum_branch["type"] == "string"
    assert enum_branch["enum"] == ["valid", "invalid"], enum_branch
    # A plain enum with a scalar type is untouched.
    assert split["properties"]["page_type"] == declared["properties"]["page_type"]

    # And no translator may emit the refused shape, for any input.
    for translator in (AnthropicTranslator, OpenAITranslator):
        wire, _, _ = _quiet(translator.translate_output_schema, declared)
        for n in _walk_dicts(wire):
            assert not (isinstance(n.get("type"), list) and isinstance(n.get("enum"), list)), (
                f"{translator.__name__} emitted an enum beside a type array: {n}"
            )


def test_no_wire_schema_carries_an_unusable_type_list() -> None:
    """`{"type": []}` and `{"type": ["null","null"]}` are both refused by name
    ("[] is not valid under any of the given schemas"). The nullable widening
    produced the second and the union collapse reduced it to the first, which took
    `decision_tree` from 200 to 400 live — found by probing, not by reading."""
    from matrx_ai.providers.anthropic.translator import AnthropicTranslator
    from matrx_ai.schema.rules import admits_null, widen_to_nullable

    # The recursion floor is a null-only node; widening it must be a no-op.
    assert admits_null({"type": "null"})
    assert widen_to_nullable({"type": "null"})["type"] == "null"

    recursive = {
        "type": "object",
        "additionalProperties": False,
        "$defs": {
            "decision_node": {
                "type": "object",
                "additionalProperties": False,
                "required": ["question"],
                "properties": {
                    "question": {"type": "string"},
                    "yes": {"$ref": "#/$defs/decision_node"},
                    "no": {"$ref": "#/$defs/decision_node"},
                },
            }
        },
        "required": ["root"],
        "properties": {"root": {"$ref": "#/$defs/decision_node"}},
    }

    wire, _, _ = _quiet(AnthropicTranslator.translate_output_schema, recursive)

    for node in _walk_dicts(wire):
        types = node.get("type")
        if isinstance(types, list):
            assert types, f"empty type list at {node}"
            assert len(types) == len(set(types)), f"repeated type member: {types}"


def test_a_schema_extension_keyword_never_reaches_the_wire() -> None:
    """A constrained decoder refuses an unknown property on a schema node —
    Anthropic, verbatim: "For 'object' type, property 'x-contract-dynamic' is not
    supported". Three live registered kinds carry one (`agent_result`,
    `agent_react_result`, `web_search_results`), and an EXTENSION is by definition
    not in any enumeration we could keep ahead of it, so it is stripped by prefix.
    Found by probing the 50 largest live schemas against the real provider — an
    enumeration of keywords would never have caught it.
    """
    from matrx_ai.providers.anthropic.translator import AnthropicTranslator
    from matrx_ai.providers.openai.translator import OpenAITranslator
    from matrx_ai.schema.rules import structured_output_schema_violations

    declared = {
        "type": "object",
        "x-contract-dynamic": True,
        "additionalProperties": False,
        "required": ["a", "x-not-a-keyword"],
        "properties": {
            "a": {"type": "string", "x-kind": "agent_result"},
            # A PROPERTY whose NAME starts with x- is data, not a keyword.
            "x-not-a-keyword": {"type": "string"},
        },
    }

    assert any("x-contract-dynamic" in p for p in structured_output_schema_violations(declared)), (
        "the forcing function does not name a schema extension"
    )

    for translator in (AnthropicTranslator, OpenAITranslator):
        wire, _, _ = _quiet(translator.translate_output_schema, declared)
        for node in _walk_dicts(wire):
            extensions = [
                k for k in node if k.startswith("x-") and not isinstance(node.get(k), dict)
            ]
            assert not extensions, f"{translator.__name__} shipped {extensions}"
        # The property NAMED x-… is untouched: only keywords are stripped.
        assert "x-not-a-keyword" in wire["properties"], wire["properties"].keys()
        assert structured_output_schema_violations(wire) == [], structured_output_schema_violations(wire)
