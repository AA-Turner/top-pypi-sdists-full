"""THE ANSWER EVERY CONSUMER RECEIVES, AND THE CONTRACT IT IS JUDGED BY, ARE THE
AUTHOR'S — and a check never cries wolf.

Re-verification 2 of the structured-output schema translation
(``common-docs/projects/checks-run-in-the-app/SCHEMA-TRANSLATION-VERIFY.md``,
"Re-verification 2 (full sweep)") measured, in production and against the real
providers:

* R2 — every Gemini TOOL-CALL turn was judged as the final answer: 335 false HIGH
  ``answer_off_contract`` rows for one mandate in ~40 minutes;
* R3 — the check was bound to the PORTABLE copy (every property required), so an
  answer that correctly omitted an optional key was reported off contract;
* R1/R4 — the ``null`` the boundary asks for reached every consumer, and the
  pruner stopped at ``$ref``: the kind validator rejected 4/4 live kinds;
* R9 — ``UnboundLocalError`` in the Anthropic translator on 10 live schemas;
* R5/R6 — widening optional fields turned 29 Anthropic and 135 Groq schemas the
  provider ACCEPTED into refusals;
* R7 — Google never got the nested-``$defs`` fix, nor a root-recursion fix;
* R10/R11 — ``provider_enforced`` and ``was_recovered`` asserted before the truth
  was known, and the findings flush swallowed its own failure.

Each test below restates the rule from the provider's or the reader's side and is
RED on ``c0b560c30d`` (proved with ``git show <sha>:path > path``, never stash).
"""

from __future__ import annotations

import asyncio
import contextlib
import copy
import io
import json
from pathlib import Path
from typing import Any

import jsonschema
import pytest

FIXTURES = Path(__file__).parent / "fixtures"


def _quiet(fn: Any, *args: Any, **kwargs: Any) -> Any:
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        return fn(*args, **kwargs)


async def _aquiet(fn: Any, *args: Any, **kwargs: Any) -> Any:
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        return await fn(*args, **kwargs)


def _capture_findings(monkeypatch: pytest.MonkeyPatch) -> list[tuple[str, dict[str, Any]]]:
    import matrx_ai.providers.structured_output_findings as findings

    recorded: list[tuple[str, dict[str, Any]]] = []

    async def capture(key: str, **kwargs: Any) -> None:
        recorded.append((key, kwargs))

    monkeypatch.setattr(findings, "record_structured_output_finding", capture)
    return recorded


# The author's contract: two optional fields, one of them inside a `$defs` object.
AUTHORS_SCHEMA: dict[str, Any] = {
    "type": "object",
    "additionalProperties": False,
    "required": ["title", "rows"],
    "properties": {
        "title": {"type": "string"},
        "summary": {"type": "string"},
        "rows": {"type": "array", "items": {"$ref": "#/$defs/Row"}},
    },
    "$defs": {
        "Row": {
            "type": "object",
            "additionalProperties": False,
            "required": ["label"],
            "properties": {"label": {"type": "string"}, "hint": {"type": "string"}},
        }
    },
}


# ---------------------------------------------------------------------------
# R2 — a tool-call turn is never the answer
# ---------------------------------------------------------------------------


def test_a_tool_call_turn_is_never_judged_as_the_answer(monkeypatch: pytest.MonkeyPatch) -> None:
    """Gemini returns ``finishReason: STOP`` on a turn that CALLS a tool, with a
    narrating text part. Judged by the finish reason, that narration was "the
    answer", and "no JSON object could be recovered" was filed as HIGH — 335 times."""
    from matrx_ai.config import Role, UnifiedMessage, UnifiedResponse
    from matrx_ai.config.tools_config import ToolCallContent
    from matrx_ai.config.unified_content import TextContent
    from matrx_ai.schema.answer_contract import (
        bind_declared_output_contract,
        release_declared_output_contract,
        verify_answer_and_record,
    )

    recorded = _capture_findings(monkeypatch)
    turn = UnifiedResponse(
        messages=[
            UnifiedMessage(
                role=Role.ASSISTANT,
                content=[
                    TextContent(text="I will fetch the webpage to find the origin of the story."),
                    ToolCallContent(id="call_1", name="web_fetch", arguments={"url": "https://x"}),
                ],
            )
        ],
        usage=None,
        finish_reason="stop",  # what FinishReason.from_google gives a functionCall turn
    )

    async def drive() -> list[str]:
        token = bind_declared_output_contract(
            {"type": "json_schema", "json_schema": {"name": "origin", "schema": AUTHORS_SCHEMA}}
        )
        try:
            return await _aquiet(
                verify_answer_and_record, turn, provider="google", model="gemini-3.8-flash"
            )
        finally:
            release_declared_output_contract(token)

    problems = asyncio.run(drive())
    assert problems == [], f"a tool-call turn was judged as the final answer: {problems}"
    assert recorded == [], f"a tool-call turn filed a finding: {[k for k, _ in recorded]}"


# ---------------------------------------------------------------------------
# R3 — the envelope, and so the check, carries the AUTHOR's contract
# ---------------------------------------------------------------------------


def test_the_agent_path_envelope_carries_the_authors_contract(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """``response_format_for_schema`` is how a persisted or code-authored agent's
    contract reaches the call. It used to put the portable copy on the envelope,
    so an answer that omitted an optional key failed a contract the author never
    wrote ("'max_output_tokens' is a required property")."""
    from matrx_ai.config import Role, UnifiedMessage, UnifiedResponse
    from matrx_ai.config.response_format import response_format_for_schema
    from matrx_ai.schema.answer_contract import (
        bind_declared_output_contract,
        release_declared_output_contract,
        verify_answer_and_record,
    )

    envelope = response_format_for_schema(copy.deepcopy(AUTHORS_SCHEMA), name="report").model_dump(
        mode="json", by_alias=True, exclude_none=True
    )
    on_the_envelope = envelope["json_schema"]["schema"]
    assert set(on_the_envelope["required"]) == {"title", "rows"}, (
        "the envelope carries a copy whose `required` is not the author's: "
        f"{on_the_envelope['required']}"
    )

    recorded = _capture_findings(monkeypatch)
    omits_optional = '{"title": "T", "rows": [{"label": "a"}]}'  # no summary, no hint

    async def drive() -> list[str]:
        token = bind_declared_output_contract(envelope)
        try:
            return await _aquiet(
                verify_answer_and_record,
                UnifiedResponse(
                    messages=[UnifiedMessage(role=Role.ASSISTANT, content=omits_optional)],
                    usage=None,
                    finish_reason="stop",
                ),
                provider="anthropic",
                model="claude-sonnet-5",
            )
        finally:
            release_declared_output_contract(token)

    assert asyncio.run(drive()) == [], "an answer the author's contract allows was flagged"
    assert recorded == []


def test_a_missing_required_key_is_named_not_reported_as_no_json(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """``extract_json(schema=…)`` is a candidate selector: it returns nothing when a
    required key is missing, and the finding then said "no JSON object could be
    recovered" — which sends the reader looking for prose that is not there."""
    from matrx_ai.config import Role, UnifiedMessage, UnifiedResponse
    from matrx_ai.schema.answer_contract import (
        bind_declared_output_contract,
        release_declared_output_contract,
        verify_answer_and_record,
    )

    _capture_findings(monkeypatch)

    async def drive() -> list[str]:
        token = bind_declared_output_contract(
            {"type": "json_schema", "json_schema": {"name": "r", "schema": AUTHORS_SCHEMA}}
        )
        try:
            return await _aquiet(
                verify_answer_and_record,
                UnifiedResponse(
                    messages=[UnifiedMessage(role=Role.ASSISTANT, content='{"rows": []}')],
                    usage=None,
                    finish_reason="stop",
                ),
                provider="anthropic",
                model="claude-sonnet-5",
            )
        finally:
            release_declared_output_contract(token)

    problems = asyncio.run(drive())
    assert any("'title' is a required property" in p for p in problems), problems


# ---------------------------------------------------------------------------
# R1 / R4 — the answer every consumer receives is pruned to the author's shape
# ---------------------------------------------------------------------------


def test_pruning_follows_ref_and_combinators() -> None:
    from matrx_ai.schema.rules import prune_optional_nulls

    answer = {"title": "T", "summary": None, "rows": [{"label": "a", "hint": None}]}
    pruned = prune_optional_nulls(answer, AUTHORS_SCHEMA)
    assert pruned == {"title": "T", "rows": [{"label": "a"}]}, pruned
    jsonschema.validate(pruned, AUTHORS_SCHEMA)

    union = {
        "type": "object",
        "additionalProperties": False,
        "required": ["item"],
        "properties": {
            "item": {
                "anyOf": [
                    {
                        "type": "object",
                        "additionalProperties": False,
                        "required": ["kind"],
                        "properties": {"kind": {"const": "a"}, "note": {"type": "string"}},
                    },
                    {
                        "type": "object",
                        "additionalProperties": False,
                        "required": ["kind"],
                        "properties": {"kind": {"const": "b"}, "size": {"type": "integer"}},
                    },
                ]
            },
            "meta": {"allOf": [{"$ref": "#/$defs/M"}]},
        },
        "$defs": {
            "M": {
                "type": "object",
                "properties": {"source": {"type": "string"}},
            }
        },
    }
    answer = {"item": {"kind": "b", "size": None}, "meta": {"source": None}}
    pruned = prune_optional_nulls(answer, union)
    assert pruned == {"item": {"kind": "b"}, "meta": {}}, pruned
    jsonschema.validate(pruned, union)

    # A null the author DID allow is kept.
    nullable = {
        "type": "object",
        "properties": {"x": {"anyOf": [{"$ref": "#/$defs/S"}, {"type": "null"}]}},
        "$defs": {"S": {"type": "string"}},
    }
    assert prune_optional_nulls({"x": None}, nullable) == {"x": None}


def _live_answers() -> list[dict[str, Any]]:
    return json.loads((FIXTURES / "live_answers_2026_09_28.json").read_text())["answers"]


def _drive_seam(declared: dict[str, Any], answer_text: str, name: str) -> tuple[str, list[str]]:
    """The answer as it leaves the one dispatch seam every provider passes through,
    and what the contract check said about it."""
    from types import SimpleNamespace

    import matrx_ai.schema.answer_contract as answer_contract
    from matrx_ai.config import Role, UnifiedMessage, UnifiedResponse
    from matrx_ai.config.unified_content import TextContent
    from matrx_ai.providers.unified_client import UnifiedAIClient
    from matrx_ai.schema.answer_contract import (
        bind_declared_output_contract,
        release_declared_output_contract,
    )

    judged: list[str] = []
    real_verify = answer_contract.verify_answer_and_record

    async def spy(response: Any, **kwargs: Any) -> list[str]:
        problems = await real_verify(response, **kwargs)
        judged.extend(problems)
        return problems

    async def dispatch() -> Any:
        return UnifiedResponse(
            messages=[UnifiedMessage(role=Role.ASSISTANT, content=[TextContent(text=answer_text)])],
            usage=None,
            finish_reason="stop",
        )

    async def run() -> str:
        answer_contract.verify_answer_and_record = spy  # type: ignore[assignment]
        token = bind_declared_output_contract(
            {"type": "json_schema", "json_schema": {"name": name, "schema": declared}}
        )
        try:
            result = await _aquiet(
                UnifiedAIClient._dispatch_with_billing_net,
                dispatch,
                profile=SimpleNamespace(
                    vendor="google",
                    model_name="gemini-3.8-flash",
                    endpoint_id="test",
                    base_url=None,
                    offering_metadata={},
                ),
            )
            return result.messages[0].get_output()
        finally:
            release_declared_output_contract(token)
            answer_contract.verify_answer_and_record = real_verify  # type: ignore[assignment]

    return asyncio.run(run()), judged


@pytest.mark.parametrize(
    "answer",
    [a for a in _live_answers() if a["subject"] == "kind"],
    ids=lambda a: f"{a['name']}-{a['provider']}",
)
def test_the_kind_validator_accepts_what_the_seam_delivers(
    answer: dict[str, Any], monkeypatch: pytest.MonkeyPatch
) -> None:
    """REAL answers (gemini-3.8-flash and gpt-4o-mini through the fixed translators,
    2026-09-28) for the four live kinds R1 measured. The platform's kind validator
    judges exactly what the seam delivers; before the fix it rejected every one."""
    from matrx_graph.content_ir.markers import strip_kind_markers
    from matrx_graph.executor.schema_validation import validate_instance

    _capture_findings(monkeypatch)
    declared = answer["declared_schema"]
    raw = json.loads(answer["answer_text"])
    assert validate_instance(declared, strip_kind_markers(raw, declared)), (
        "fixture sanity: the provider's raw answer is expected to carry the boundary's nulls"
    )
    delivered, judged = _drive_seam(declared, answer["answer_text"], answer["name"])
    parsed = json.loads(delivered)
    errors = validate_instance(declared, strip_kind_markers(parsed, declared))
    assert errors == [], f"{answer['name']} ({answer['provider']}): {errors[:3]}"
    assert judged == [], f"the contract check disagrees with the kind validator: {judged[:3]}"


# ---------------------------------------------------------------------------
# R9 — the Anthropic translator never dies on a Python error
# ---------------------------------------------------------------------------


def test_the_anthropic_forcing_function_records_instead_of_crashing(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A live io_contract (ValidateKindInput) whose `ui:*` property keywords survive
    translation. The branch that names them used to raise UnboundLocalError."""
    import matrx_ai.providers.structured_output_findings as findings
    from matrx_ai.providers.anthropic.translator import AnthropicTranslator

    schema = json.loads((FIXTURES / "live_validate_kind_input_schema.json").read_text())
    seen: list[str] = []
    monkeypatch.setattr(
        findings,
        "record_structured_output_finding_sync",
        lambda key, **kwargs: seen.append(key) or True,
    )
    body = _quiet(
        AnthropicTranslator._build_anthropic_output_format,
        {"type": "json_schema", "json_schema": {"name": "validate_kind", "schema": schema}},
    )
    assert isinstance(body, dict) and isinstance(body.get("schema"), dict)
    assert any(k.endswith("relaxed") for k in seen), seen


# ---------------------------------------------------------------------------
# R5 — widening never pushes an Anthropic request over its grammar budget
# ---------------------------------------------------------------------------


def _grammar_cost(schema: Any) -> float:
    """Restated here from the measured model (properties + 1.5 × unions + 3 ×
    arrays + 0.3 × enum members, each $defs entry once) rather than imported."""
    t = {"p": 0, "u": 0, "a": 0, "e": 0}

    def walk(n: Any) -> None:
        if isinstance(n, list):
            for x in n:
                walk(x)
            return
        if not isinstance(n, dict):
            return
        if isinstance(n.get("properties"), dict):
            t["p"] += len(n["properties"])
        if isinstance(n.get("anyOf"), list) or isinstance(n.get("type"), list):
            t["u"] += 1
        if n.get("type") == "array" or "items" in n:
            t["a"] += 1
        if isinstance(n.get("enum"), list):
            t["e"] += len(n["enum"])
        for k, v in n.items():
            if k in ("required", "enum", "const", "default", "examples"):
                continue
            if k in ("properties", "$defs", "definitions") and isinstance(v, dict):
                for s in v.values():
                    walk(s)
            else:
                walk(v)

    walk(schema)
    return t["p"] + 1.5 * t["u"] + 3 * t["a"] + 0.3 * t["e"]


def test_widening_stops_below_anthropics_measured_grammar_ceiling() -> None:
    """``flashcard_set`` (live kind, 2026-09-28): Anthropic ACCEPTED it with its
    optional fields forced and refused it — "The compiled grammar is too large" —
    once they were widened to nullable. Every refusal in the 1,300-body sweep
    scored ≥ 72 on the measured model; the translator must not spend past 64 on
    widening, and must never make the body costlier than the forced shape when
    the forced shape is already over."""
    from matrx_ai.providers.anthropic.translator import AnthropicTranslator

    declared = json.loads((FIXTURES / "live_kind_flashcard_set_schema.json").read_text())
    wire, narrowed, _relaxed = _quiet(AnthropicTranslator.translate_output_schema, declared)
    cost = _grammar_cost(wire)
    if cost > 64.0:
        # Over the ceiling only if NOTHING was widened: every field the author left
        # optional is forced — the exact shape Anthropic accepted before.
        optional = [n for n in declared["properties"] if n not in set(declared.get("required") or ())]
        for name in optional:
            node = wire["properties"][name]
            assert not (
                isinstance(node.get("anyOf"), list)
                and {"type": "null"} in node["anyOf"]
            ), f"{name} was widened although the body is over the ceiling ({cost})"
    # And what it could not widen it says so, by field.
    assert any("made REQUIRED and not nullable" in n for n in narrowed), narrowed


# ---------------------------------------------------------------------------
# R6 — groq receives only union spellings its validator accepts
# ---------------------------------------------------------------------------


def _walk_nodes(node: Any):
    if isinstance(node, dict):
        yield node
        for v in node.values():
            yield from _walk_nodes(v)
    elif isinstance(node, list):
        for v in node:
            yield from _walk_nodes(v)


def test_groq_gets_no_union_its_validator_refuses() -> None:
    """Measured live 2026-09-28 (openai/gpt-oss-20b): `required` beside empty or
    missing `properties` → "'required' present but 'properties' is missing"; an
    `anyOf` branch that is a `$ref` to a primitive → "anyOf branches must be
    disambiguated"; two branches admitting null → "multiple branches accept null"."""
    from matrx_ai.providers.base_translator import BaseTranslator

    declared = {
        "type": "object",
        "additionalProperties": False,
        "required": ["name"],
        "properties": {
            "name": {"type": "string"},
            "attrs": {"type": "object", "additionalProperties": False},
            "value": {"$ref": "#/$defs/JsonValue", "description": "any value"},
            "profile": {"$ref": "#/$defs/Profile"},
            "count": {"type": ["integer", "null"]},
        },
        "$defs": {
            "JsonValue": {"type": "string"},
            "Profile": {"type": "string", "enum": ["weekly", "monthly"]},
        },
    }
    rf = {"type": "json_schema", "json_schema": {"name": "g", "schema": declared, "strict": True}}
    wire = _quiet(BaseTranslator.build_openai_chat_response_format, rf, "groq")["json_schema"]["schema"]
    defs = wire.get("$defs") or {}
    for node in _walk_nodes(wire):
        if "required" in node:
            assert node.get("properties"), f"`required` without properties: {node}"
        branches = node.get("anyOf")
        if isinstance(branches, list) and any(
            isinstance(b, dict) and b.get("type") == "null" for b in branches
        ):
            nullish = 0
            for b in branches:
                assert isinstance(b, dict)
                target = b
                if "$ref" in b:
                    target = defs.get(b["$ref"].rsplit("/", 1)[-1], {})
                    assert target.get("type") == "object" or "properties" in target, (
                        f"a $ref to a non-object beside null: {node}"
                    )
                t = target.get("type")
                if t == "null" or (isinstance(t, list) and "null" in t):
                    nullish += 1
            assert nullish == 1, f"more than one branch accepts null: {node}"
    # And the author's optional fields can still be answered absent (null).
    for name in ("attrs", "value", "profile"):
        jsonschema.validate(
            {"name": "n", "attrs": None, "value": None, "profile": None, "count": None},
            {**wire, "$defs": defs},
        )


# ---------------------------------------------------------------------------
# R7 — Google: nested $defs and root recursion
# ---------------------------------------------------------------------------


def test_google_receives_a_resolvable_schema_for_a_nested_defs_kind() -> None:
    """24 live kinds embed a whole schema, with its own `$defs`, under a property.
    Gemini: "reference to undefined schema at properties.draft…"."""
    from matrx_ai.providers.google.translator import GoogleTranslator

    declared = {
        "type": "object",
        "additionalProperties": False,
        "required": ["draft"],
        "properties": {
            "draft": {
                "type": "object",
                "additionalProperties": False,
                "required": ["sections"],
                "$defs": {"Section": {"type": "object", "properties": {"h": {"type": "string"}}}},
                "properties": {"sections": {"type": "array", "items": {"$ref": "#/$defs/Section"}}},
            }
        },
    }
    wire = _quiet(
        GoogleTranslator._build_google_response_schema,
        {"type": "json_schema", "json_schema": {"name": "d", "schema": declared}},
    )
    refs = [n["$ref"] for n in _walk_nodes(wire) if isinstance(n.get("$ref"), str)]
    assert refs
    for ref in refs:
        node: Any = wire
        for part in ref[2:].split("/"):
            node = node.get(part) if isinstance(node, dict) else None
        assert isinstance(node, dict), f"{ref} resolves to nothing from the root"


def test_google_can_compile_a_cycle_through_the_root() -> None:
    """Live ``decision_node``: `yes`/`no` → `{"$ref": "#"}`. Measured 2026-09-28 on
    gemini-3.8-flash: a REQUIRED `anyOf: [{$ref}, null]` loop carrier is refused
    ("a ref loop of required fields"), an OPTIONAL one is accepted — so the carrier
    must leave `required`, and every `$ref` must still resolve."""
    from matrx_ai.providers.google.translator import GoogleTranslator

    declared = {
        "type": "object",
        "required": ["__kind", "question"],
        "properties": {
            "__kind": {"type": "string", "enum": ["decision_node"]},
            "question": {"type": "string"},
            "yes": {"$ref": "#"},
            "no": {"$ref": "#"},
        },
    }
    wire = _quiet(
        GoogleTranslator._build_google_response_schema,
        {"type": "json_schema", "json_schema": {"name": "decision_node", "schema": declared}},
    )
    # Every object that carries a loop back to a recursive node must not REQUIRE it.
    for node in _walk_nodes(wire):
        props = node.get("properties") if isinstance(node, dict) else None
        if not isinstance(props, dict):
            continue
        required = set(node.get("required") or ())
        for name, sub in props.items():
            carries = any(isinstance(n.get("$ref"), str) for n in _walk_nodes(sub))
            if carries and sub.get("type") != "array":
                assert name not in required, f"loop carrier {name!r} is still required: {node}"
    for n in _walk_nodes(wire):
        ref = n.get("$ref")
        if isinstance(ref, str):
            assert ref != "#", "a root self-reference reached Gemini"
            target: Any = wire
            for part in ref[2:].split("/"):
                target = target.get(part) if isinstance(target, dict) else None
            assert isinstance(target, dict), ref


# ---------------------------------------------------------------------------
# R10 / R11 — the findings tell the truth about enforcement and recovery
# ---------------------------------------------------------------------------


def test_google_tool_conflict_says_the_contract_was_not_enforced(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """When Gemini's native schema switch is left off beside tools, the schema
    rides the system instruction — so the answer check must say the provider was
    NOT enforcing it, not "the wire and the declared schema have diverged"."""
    from test_google_schema_beside_oversize_tool import _FORMAT, _GEMINI_3, DECLS, _wire

    from matrx_ai.schema.answer_contract import (
        bind_declared_output_contract,
        declared_output_contract,
        release_declared_output_contract,
    )

    token = bind_declared_output_contract(_FORMAT)
    try:
        request = _quiet(_wire, _GEMINI_3, DECLS, monkeypatch)
        config = request.get("config") if isinstance(request, dict) else None
        assert getattr(config, "response_json_schema", None) is None, (
            "fixture sanity: this is the tool-conflict path, which withholds the native switch"
        )
        contract = declared_output_contract()
        assert contract is not None and contract["enforced"] is False, contract
    finally:
        release_declared_output_contract(token)


def test_the_anthropic_ladder_marks_enforcement_dropped_only_when_that_rung_serves(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The ladder used to mark the contract "not enforced" while BUILDING its
    rungs, so when the narrowed rung served under full enforcement the answer
    check still said the provider was not holding the contract."""
    from test_structured_output_corpus import _Emitter, _ladder_payload

    from matrx_ai.providers.anthropic.anthropic_api import AnthropicChat
    from matrx_ai.schema.answer_contract import (
        bind_declared_output_contract,
        declared_output_contract,
        release_declared_output_contract,
    )

    _capture_findings(monkeypatch)
    import matrx_ai.ops.issue_capture as issue_capture

    async def ignore(*_a: Any, **_k: Any) -> None:
        return None

    monkeypatch.setattr(issue_capture, "capture_issue", ignore)
    payload, rf = _ladder_payload(4, 2)

    async def send(p: dict[str, Any]) -> str:
        schema = ((p.get("output_config") or {}).get("format") or {}).get("schema") or {}
        still_unions = any(
            isinstance(s.get("type"), list) or "anyOf" in s
            for s in (schema.get("properties") or {}).values()
        )
        if schema and not still_unions:
            return "served"  # the narrowed rung: schema enforced, unions gone
        raise RuntimeError("The compiled grammar is too large, which would cause performance issues.")

    async def drive() -> tuple[Any, Any]:
        token = bind_declared_output_contract(rf)
        try:
            chat = AnthropicChat.__new__(AnthropicChat)
            result = await _aquiet(
                chat._retry_over_grammar_budget,
                payload,
                send,
                _Emitter(),
                "claude-sonnet-5",
                RuntimeError("compiled grammar is too large"),
                response_format=rf,
            )
            return result, declared_output_contract()
        finally:
            release_declared_output_contract(token)

    result, contract = asyncio.run(drive())
    assert result == "served"
    assert contract is not None and contract["enforced"] is True, (
        "the narrowed rung served under full enforcement, yet the contract says it "
        f"was not enforced: {contract}"
    )


def test_a_broken_findings_sink_screams(
    monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture
) -> None:
    from types import SimpleNamespace

    import matrx_ai.providers.structured_output_findings as findings
    from matrx_ai.providers.unified_client import UnifiedAIClient

    async def broken(**_kwargs: Any) -> None:
        raise RuntimeError("sink is down")

    monkeypatch.setattr(findings, "flush_translation_findings", broken)

    async def ok() -> str:
        return "answer"

    out = io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(out), caplog.at_level("ERROR"):
        result = asyncio.run(
            UnifiedAIClient._dispatch_with_billing_net(
                ok,
                profile=SimpleNamespace(
                    vendor="xai",
                    model_name="grok",
                    endpoint_id="t",
                    base_url=None,
                    offering_metadata={},
                ),
            )
        )
    assert result == "answer"
    said = out.getvalue() + caplog.text
    assert "NOT recorded" in said and "sink is down" in said, said[-500:]
