"""THE STRUCTURED-OUTPUT CORPUS — every schema a real provider refused or
silently degraded in production (2026-08-15 .. 2026-09-27) must translate into
a shape that provider accepts, with its structure still enforced.

Arman, 2026-09-27: the shape we hold is modified by each provider's translator;
a provider rejecting our request is OUR translator's bug. The corpus
(``fixtures/structured_output_corpus.json``) was pulled from
``runtime.global_execution.error``, ``ops.app_log`` and ``chat.request_snapshot``;
provenance per case is in its ``origin``.

These checks deliberately do NOT reuse ``matrx_ai.schema.rules`` to judge the
translators' output — a guard that shares the builder's frame proves nothing.
Each provider's subset is restated here from what the provider itself said
(the refusal messages are quoted in ``_anthropic_problems`` / ``_openai_problems``).
The live twin — the same corpus sent to the real providers — is aidream's
``scripts/check_structured_output_corpus.py``.
"""

from __future__ import annotations

import asyncio
import contextlib
import io
import json
from pathlib import Path
from typing import Any

import pytest

FIXTURE = Path(__file__).parent / "fixtures" / "structured_output_corpus.json"
CORPUS = json.loads(FIXTURE.read_text())
SCHEMAS: dict[str, Any] = CORPUS["schemas"]
TOOLS: dict[str, Any] = CORPUS["tools"]
CASES: list[dict[str, Any]] = CORPUS["cases"]


def _response_format(case: dict[str, Any]) -> dict[str, Any]:
    entry = SCHEMAS[case["schema"]]
    if "response_format" in entry:
        return entry["response_format"]
    from matrx_ai.config.response_format import response_format_for_schema

    return response_format_for_schema(entry["raw_schema"], name=entry["name"]).model_dump(
        mode="json", by_alias=True, exclude_none=True
    )


def _quiet(fn: Any, *args: Any, **kwargs: Any) -> Any:
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        return fn(*args, **kwargs)


def _walk(node: Any, path: str = "$"):
    if isinstance(node, dict):
        yield path, node
        for key, value in node.items():
            if key in ("enum", "const", "required", "default", "examples"):
                continue
            if key in ("properties", "$defs", "definitions") and isinstance(value, dict):
                for name, sub in value.items():
                    yield from _walk(sub, f"{path}.{key}.{name}")
            else:
                yield from _walk(value, f"{path}.{key}")
    elif isinstance(node, list):
        for index, item in enumerate(node):
            yield from _walk(item, f"{path}[{index}]")


def _is_object(node: dict[str, Any]) -> bool:
    t = node.get("type")
    return t == "object" or (isinstance(t, list) and "object" in t) or "properties" in node


def _cycles(schema: dict[str, Any]) -> list[str]:
    defs = schema.get("$defs") or schema.get("definitions") or {}

    def refs(node: Any) -> set[str]:
        return {
            n["$ref"].rsplit("/", 1)[-1] for _, n in _walk(node) if isinstance(n.get("$ref"), str)
        } & set(defs)

    edges = {name: refs(body) for name, body in defs.items()}
    found: list[str] = []

    def visit(name: str, stack: list[str]) -> None:
        if name in stack:
            found.append(" -> ".join(stack[stack.index(name) :] + [name]))
            return
        for child in edges.get(name, ()):
            visit(child, stack + [name])

    for name in edges:
        visit(name, [])
    return found


def _dangling_refs(schema: dict[str, Any]) -> list[str]:
    """Every ``$ref`` that names nothing, judged the way a provider judges it:
    resolve the pointer from the DOCUMENT ROOT and nowhere else.

    Anthropic: ``Invalid schema: Reference to non-existent definition:
    #/$defs/plan_draft_section``. OpenAI: ``reference to component
    '#/$defs/plan_draft_section' which was not found``. Restated here from those
    two messages — deliberately NOT by calling ``rules.unresolvable_refs``, which
    is the code under test.
    """
    bad: list[str] = []
    for path, node in _walk(schema):
        ref = node.get("$ref")
        if not isinstance(ref, str) or not ref.startswith("#"):
            continue
        target: Any = schema
        for raw in [part for part in ref.lstrip("#").split("/") if part]:
            part = raw.replace("~1", "/").replace("~0", "~")
            if isinstance(target, dict) and part in target:
                target = target[part]
            else:
                bad.append(f"{path}: {ref}")
                break
    return bad


def _anthropic_problems(schema: dict[str, Any]) -> list[str]:
    """Anthropic's structured-output subset, restated from its own refusals."""
    problems: list[str] = []
    unions = 0
    for path, node in _walk(schema):
        if "oneOf" in node:  # "Schema type 'oneOf' is not supported"
            problems.append(f"{path}: oneOf")
        if "allOf" in node:  # siblings beside allOf are refused
            problems.append(f"{path}: allOf")
        if isinstance(node.get("anyOf"), list):
            # "For 'anyOf', '<keys>' is not supported"
            bad = set(node) - {"anyOf", "title", "description", "default", "enum", "const"}
            if bad:
                problems.append(f"{path}: {sorted(bad)} beside anyOf")
        if _is_object(node) and node.get("additionalProperties") is not False:
            # "For 'object' type, 'additionalProperties: object' is not supported"
            problems.append(f"{path}: additionalProperties must be false")
        if isinstance(node.get("items"), list):
            problems.append(f"{path}: tuple items")
        if set(node) <= {"title", "description"}:  # "Empty schema ({}) ... is not supported"
            problems.append(f"{path}: empty schema")
        props = node.get("properties")
        if isinstance(props, dict):
            unions += sum(
                1
                for sub in props.values()
                if isinstance(sub, dict)
                and (isinstance(sub.get("anyOf"), list) or isinstance(sub.get("type"), list))
            )
            optional = set(props) - set(node.get("required") or [])
            if optional:  # 13 optional parameters -> "Schema is too complex."
                problems.append(f"{path}: optional {sorted(optional)[:5]}")
        if "type" not in node and not ({"$ref", "anyOf", "enum", "const"} & set(node)):
            # "Schema type is missing for schema: {...}"
            if set(node) - {"title", "description", "default"}:
                problems.append(f"{path}: schema type is missing")
    if unions > 16:  # "Schemas contains too many parameters with union types"
        problems.append(f"$: {unions} union parameters (limit 16)")
    problems.extend(f"$defs: circular {c}" for c in _cycles(schema))
    problems.extend(f"unresolvable {r}" for r in _dangling_refs(schema))
    return problems


def _openai_problems(schema: dict[str, Any]) -> list[str]:
    """OpenAI strict json_schema, restated from its own refusals (gpt-4o-mini)."""
    problems: list[str] = []
    for path, node in _walk(schema):
        if "oneOf" in node:  # "'oneOf' is not permitted"
            problems.append(f"{path}: oneOf")
        if "allOf" in node:
            problems.append(f"{path}: allOf")
        if _is_object(node):
            if node.get("additionalProperties") is not False:
                # "'additionalProperties' is required to be supplied and to be false"
                problems.append(f"{path}: additionalProperties must be false")
            props = node.get("properties")
            if not isinstance(props, dict):
                # without `properties` the parent's required names an "Extra required key"
                problems.append(f"{path}: object without a properties map")
            elif set(node.get("required") or []) != set(props):
                # "'required' ... an array including every key in properties"
                problems.append(f"{path}: required != properties")
    problems.extend(f"unresolvable {r}" for r in _dangling_refs(schema))
    return problems


ANTHROPIC_CASES = [c for c in CASES if c["provider"] == "anthropic"]
OPENAI_CASES = [c for c in CASES if c["provider"] == "openai"]


@pytest.mark.parametrize("case", ANTHROPIC_CASES, ids=[c["id"] for c in ANTHROPIC_CASES])
def test_anthropic_translation_lands_inside_the_subset(case: dict[str, Any]) -> None:
    import inspect

    from matrx_ai.providers.anthropic.translator import AnthropicTranslator

    tools = TOOLS.get(case["tools"] or "", [])
    build = AnthropicTranslator._build_anthropic_output_format
    kwargs = (
        {"tool_count": len(tools)} if "tool_count" in inspect.signature(build).parameters else {}
    )
    fmt = _quiet(build, _response_format(case), **kwargs)
    assert fmt is not None, f"{case['id']}: structured output was dropped at translation"
    problems = _anthropic_problems(fmt["schema"])
    assert not problems, f"{case['id']} ({case['origin']}): {problems[:6]}"


@pytest.mark.parametrize("case", OPENAI_CASES, ids=[c["id"] for c in OPENAI_CASES])
def test_openai_translation_is_strict_and_valid(case: dict[str, Any]) -> None:
    from matrx_ai.providers.openai.translator import OpenAITranslator

    fmt = _quiet(OpenAITranslator._build_openai_text_format, _response_format(case))
    assert fmt and fmt["type"] == "json_schema", f"{case['id']}: not schema-enforced"
    assert fmt.get("strict") is True, f"{case['id']}: strict is off — the schema is only a hint"
    problems = _openai_problems(fmt["schema"])
    assert not problems, f"{case['id']} ({case['origin']}): {problems[:6]}"


def test_a_map_stays_a_map_in_the_portable_contract() -> None:
    """The portable schema is what the answer is VALIDATED against and what
    Gemini receives: emptying a map there silently forbade every entry for every
    provider. Only the strict providers narrow it, and they say so."""
    from matrx_ai.config.response_format import response_format_for_schema

    schema = {
        "type": "object",
        "properties": {
            "labels": {"type": "object", "additionalProperties": {"type": "string"}},
            "hints": {"type": "object", "additionalProperties": True},
        },
    }
    rf = response_format_for_schema(schema, name="maps").model_dump(
        mode="json", by_alias=True, exclude_none=True
    )
    portable = rf["json_schema"]["schema"]["properties"]
    assert portable["labels"]["additionalProperties"] == {"type": "string"}
    assert portable["hints"]["additionalProperties"] is True


def _ladder_payload(schema_unions: int, tool_count: int) -> tuple[dict[str, Any], dict[str, Any]]:
    props = {f"f{i}": {"type": ["string", "null"]} for i in range(schema_unions)}
    props["title"] = {"type": "string"}
    schema = {
        "type": "object",
        "properties": props,
        "required": list(props),
        "additionalProperties": False,
    }
    tools = [
        {"name": f"tool_{i}", "input_schema": {"type": "object", "properties": {}}}
        for i in range(tool_count)
    ]
    payload = {
        "model": "claude-sonnet-5",
        "messages": [],
        "output_config": {"effort": "low", "format": {"type": "json_schema", "schema": schema}},
        "tools": tools,
    }
    rf = {"type": "json_schema", "json_schema": {"name": "ladder_probe", "schema": schema}}
    return payload, rf


class _Emitter:
    def __init__(self) -> None:
        self.warnings: list[str] = []

    async def send_warning(self, warning: Any) -> None:
        self.warnings.append(getattr(warning, "code", str(warning)))


def _run_ladder(accept: Any, schema_unions: int = 4, tool_count: int = 2, monkeypatch: Any = None):
    from matrx_ai.providers.anthropic.anthropic_api import AnthropicChat

    payload, rf = _ladder_payload(schema_unions, tool_count)
    sent: list[dict[str, Any]] = []

    async def send(p: dict[str, Any]) -> str:
        sent.append(p)
        if accept(p):
            return "served"
        raise RuntimeError(
            "The compiled grammar is too large, which would cause performance issues."
        )

    chat = AnthropicChat.__new__(AnthropicChat)
    kwargs: dict[str, Any] = {}
    import inspect

    if "response_format" in inspect.signature(AnthropicChat._retry_over_grammar_budget).parameters:
        kwargs["response_format"] = rf
    emitter = _Emitter()
    result = asyncio.run(
        _quiet_async(
            chat._retry_over_grammar_budget(
                payload,
                send,
                emitter,
                "claude-sonnet-5",
                RuntimeError("compiled grammar is too large"),
                **kwargs,
            )
        )
    )
    return result, sent, emitter


async def _quiet_async(coro: Any) -> Any:
    with contextlib.redirect_stdout(io.StringIO()):
        return await coro


def _unions(p: dict[str, Any]) -> int:
    schema = ((p.get("output_config") or {}).get("format") or {}).get("schema") or {}
    return sum(
        1 for s in (schema.get("properties") or {}).values() if isinstance(s.get("type"), list)
    )


@pytest.fixture
def findings(monkeypatch: pytest.MonkeyPatch) -> list[tuple[str, dict[str, Any]]]:
    recorded: list[tuple[str, dict[str, Any]]] = []

    async def fake_capture(key: str, **kwargs: Any) -> None:
        recorded.append((key, kwargs))

    import matrx_ai.ops.issue_capture as issue_capture

    monkeypatch.setattr(issue_capture, "capture_issue", fake_capture)
    return recorded


def test_ladder_narrows_before_it_sheds_anything(findings) -> None:
    """Rung 1 keeps the contract ENFORCED and every tool: nullable unions are
    narrowed (the flashcards node + tool and the agent factory's envelope were
    cured by exactly this, live 2026-09-27)."""
    result, sent, emitter = _run_ladder(
        lambda p: _unions(p) == 0 and len(p.get("tools") or []) == 2
    )
    assert result == "served"
    assert len(sent) == 1, "the first retry must be the narrowing, not a shed"
    assert sent[0]["tools"], "tools were shed although narrowing alone fits"
    assert (sent[0].get("output_config") or {}).get("format"), "enforcement dropped"
    assert [k for k, _ in findings] == ["structured_output.narrowed"]
    detail = findings[0][1]["detail"]
    assert detail["schema_name"] == "ladder_probe" and detail["schema_fingerprint"]
    assert emitter.warnings == [], "a narrowing the user cannot notice is not a user warning"


def test_ladder_last_rung_restores_the_tools(findings) -> None:
    """When the schema itself is over budget, dropping the tools cannot help;
    the final rung must send the TOOLS without the format — until 2026-09-27 it
    sent neither (an 18-tool agent lost every tool AND its contract)."""
    result, sent, emitter = _run_ladder(lambda p: not (p.get("output_config") or {}).get("format"))
    assert result == "served"
    final = sent[-1]
    assert len(final.get("tools") or []) == 2, "the last rung dropped the tools too"
    assert [k for k, _ in findings] == ["structured_output.enforcement_dropped"]
    assert findings[0][1]["was_recovered"] is True
    assert findings[0][1]["detail"]["schema_size"]["properties"] >= 1
    assert emitter.warnings == ["anthropic_grammar_over_budget"]


def test_ladder_sheds_tools_only_when_the_schema_alone_fits(findings) -> None:
    result, sent, _ = _run_ladder(
        lambda p: bool((p.get("output_config") or {}).get("format")) and not p.get("tools"),
    )
    assert result == "served"
    assert not sent[-1].get("tools") and sent[-1]["output_config"]["format"]
    assert [k for k, _ in findings] == ["structured_output.tools_shed"]


def test_translation_findings_are_flushed_with_the_schema_named(findings) -> None:
    from matrx_ai.providers.structured_output_findings import (
        begin_translation_findings,
        end_translation_findings,
        flush_translation_findings,
        note_translation,
    )

    token = begin_translation_findings()
    try:
        note_translation(
            "anthropic",
            narrowed=["$.properties.keyword_goals: dynamic-key map narrowed"],
            response_format={
                "type": "json_schema",
                "json_schema": {"name": "research_setup", "schema": {"type": "object"}},
            },
        )
        asyncio.run(flush_translation_findings(model="claude-sonnet-5"))
    finally:
        end_translation_findings(token)
    assert [k for k, _ in findings] == ["structured_output.narrowed"]
    assert findings[0][1]["detail"]["schema_name"] == "research_setup"


def test_dedupe_is_lossless() -> None:
    import jsonschema

    from matrx_ai.schema.rules import dedupe_identical_subtrees

    obj = {
        "type": "object",
        "properties": {"k": {"type": "string"}, "n": {"type": "integer"}},
        "required": ["k", "n"],
        "additionalProperties": False,
    }
    schema = {
        "type": "object",
        "properties": {
            "a": {"type": "array", "items": obj},
            "b": {"type": "array", "items": obj},
            "c": obj,
        },
        "required": ["a", "b", "c"],
        "additionalProperties": False,
    }
    shared = dedupe_identical_subtrees(schema)
    assert "$defs" in shared and len(shared["$defs"]) == 1
    good = {"a": [{"k": "x", "n": 1}], "b": [], "c": {"k": "y", "n": 2}}
    bad = {"a": [{"k": "x"}], "b": [], "c": {"k": "y", "n": 2}}
    jsonschema.validate(good, shared)
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(bad, shared)


def test_a_refinement_oneof_stays_satisfiable_in_the_portable_contract() -> None:
    """The plan node specialist's either/or rule ("recommendations non-empty, OR
    an empty list plus a gap_description") is validation logic about the parent's
    properties. The portable step used to stamp ``additionalProperties: false``
    and a full ``required`` onto each branch, which made the contract impossible
    to satisfy — a perfect answer failed validation (measured 2026-09-27)."""
    import jsonschema

    from matrx_ai.config.response_format import response_format_for_schema

    schema = {
        "type": "object",
        "required": ["recommendations"],
        "properties": {
            "recommendations": {
                "type": "array",
                "items": {"type": "object", "properties": {"title": {"type": "string"}}},
            },
            "gap_description": {"type": "string"},
        },
        "oneOf": [
            {"properties": {"recommendations": {"minItems": 1}}},
            {
                "properties": {
                    "recommendations": {"maxItems": 0},
                    "gap_description": {"minLength": 1},
                },
                "required": ["gap_description"],
            },
        ],
    }
    portable = response_format_for_schema(schema, name="plan").model_dump(
        mode="json", by_alias=True, exclude_none=True
    )["json_schema"]["schema"]
    jsonschema.validate({"recommendations": [{"title": "x"}], "gap_description": ""}, portable)
    jsonschema.validate({"recommendations": [], "gap_description": "no email node"}, portable)
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate({"recommendations": [], "gap_description": ""}, portable)
