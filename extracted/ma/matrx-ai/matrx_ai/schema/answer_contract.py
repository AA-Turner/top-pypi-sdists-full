"""THE DECLARED OUTPUT CONTRACT — carried through the call, injected as prompt
guidance when the provider will not enforce it, and CHECKED against the answer.

Eight docstrings in ``matrx_ai.schema.rules`` excused a provider-side loss with
"platform-side validation still enforces it", and the ``enforcement_dropped``
finding told the reader "the answer is prompt-guided and validated after the
fact". On 2026-09-27 an independent review measured both halves and found
neither existed on the general path: Anthropic's last rung sent
``with_format(config_data, None)`` with no schema text added to the prompt, and
the only ``jsonschema`` uses in the package were design-time
(``schema/lint.py``) and tool arguments (``tools/executor.py``). What the agent
path had was ``extract_json(text, schema=…)``, whose own docstring scopes it
honestly: it FILTERS candidates to those matching ``type`` + ``required`` at
depth 1. A key-presence test one level deep is a candidate SELECTOR, not a
contract check — it never reads nested structure, types below depth 1, enums, or
any constraint a relaxation gave up, and it never raises.

This module is the missing half, built as one platform primitive rather than
per-provider:

* :func:`bind_declared_output_contract` records, once per call and BEFORE any
  capability gate can overwrite ``config.response_format``, the contract the
  caller declared. Everything below the gate reads it with
  :func:`declared_output_contract`.
* :func:`json_text_contract` is the ONE prompt-guidance text. Google has used it
  in production since 2026-08 for the two situations where it cannot send a
  native schema; every other place that drops enforcement now sends the same
  words instead of nothing.
* :func:`verify_answer` judges the answer against the DECLARED schema with
  ``jsonschema`` — after :func:`prune_optional_nulls`, so a ``null`` the boundary
  itself asked for is read as the absence the author meant, and only the model's
  own mistakes count.
* :func:`verify_answer_and_record` is what the dispatch seam calls: it never
  raises into a live turn, and on a real mismatch it records
  ``structured_output.answer_off_contract`` naming the agent, the schema and the
  first failures, prints the remedy, and warns the person.

A contract that is neither enforced NOR checked is a contract nobody holds.
"""

from __future__ import annotations

import json
import re
from contextvars import ContextVar, Token
from typing import Any

from matrx_utils import vcprint

#: One issue class for the outcome this module exists to make visible: the answer
#: did not satisfy the contract the caller declared. HIGH — a machine consumer
#: downstream is about to read a shape it was promised and did not get.
ANSWER_OFF_CONTRACT = "structured_output.answer_off_contract"

#: How many individual validation failures travel in a finding. The point is to
#: name the shape that broke, not to ship the whole diff.
_MAX_REPORTED_FAILURES = 8

_DECLARED: ContextVar[dict[str, Any] | None] = ContextVar(
    "declared_output_contract", default=None
)


def declared_schema_of(response_format: Any) -> tuple[dict[str, Any] | None, str | None]:
    """Pull ``(schema, name)`` out of any shape ``response_format`` arrives in.

    The same three envelopes every translator reads: a full OpenAI-style
    ``{name, schema, strict}``, a raw JSON Schema nested under ``json_schema``, or
    a bare ``{"type": "json_schema"}`` placeholder with no schema at all.
    """
    if not isinstance(response_format, dict):
        return None, None
    if response_format.get("type") not in (None, "json_schema"):
        return None, None
    inner = response_format.get("json_schema")
    if isinstance(inner, dict):
        if isinstance(inner.get("schema"), dict):
            return inner["schema"], inner.get("name") or response_format.get("name")
        if {"type", "properties", "items"} & inner.keys():
            return inner, response_format.get("name")
    if isinstance(response_format.get("schema"), dict):
        return response_format["schema"], response_format.get("name")
    return None, None


def bind_declared_output_contract(response_format: Any) -> Token:
    """Record the contract THIS call declared, before anything can downgrade it.

    ALWAYS sets — to ``None`` when there is no schema — because a ContextVar set
    inside one dispatch outlives it in the same asyncio task: a call that declares
    nothing must not inherit the previous call's contract and be judged against it.

    Must run before the capability gates: ``_downgrade_response_format`` replaces
    ``config.response_format`` outright and takes the schema with it.
    """
    schema, name = declared_schema_of(response_format)
    if not isinstance(schema, dict):
        return _DECLARED.set(None)
    return _DECLARED.set({"schema": schema, "name": name, "enforced": True})


def use_declared_output_contract(contract: Any) -> Token:
    """Re-bind a contract that was recorded EARLIER, on another call.

    For the batch lane: the request is rendered (and the contract bound) hours
    before the answer arrives, in a different task. The contract travels on the
    work item exactly as :func:`declared_output_contract` returned it at render
    time — the AUTHOR's schema, its name, and whether the provider was enforcing
    it — and is re-bound here so the answer runs through the SAME
    :func:`conform_answer_to_contract` + :func:`verify_answer_and_record` step a
    live answer does. Anything that is not a contract binds ``None``.
    """
    if not isinstance(contract, dict) or not isinstance(contract.get("schema"), dict):
        return _DECLARED.set(None)
    return _DECLARED.set(
        {
            "schema": contract["schema"],
            "name": contract.get("name"),
            "enforced": bool(contract.get("enforced", True)),
            **(
                {"dropped_because": contract["dropped_because"]}
                if contract.get("dropped_because")
                else {}
            ),
        }
    )


def mark_enforcement_dropped(reason: str) -> None:
    """Say, on the contract itself, that the provider is NOT holding it on this
    call. Read back by :func:`verify_answer_and_record` so the finding's remedy
    tells the truth about who was supposed to be enforcing."""
    contract = _DECLARED.get()
    if contract is None:
        return
    _DECLARED.set({**contract, "enforced": False, "dropped_because": reason})


def release_declared_output_contract(token: Token | None) -> None:
    if token is not None:
        _DECLARED.reset(token)


def declared_output_contract() -> dict[str, Any] | None:
    """``{"schema": …, "name": …}`` for the current call, or ``None``."""
    return _DECLARED.get()


def json_text_contract(schema: dict[str, Any]) -> str:
    """The final-answer contract to put in the prompt when the provider's native
    schema switch cannot be used.

    This exact wording has been Google's ``_tool_json_text_contract`` in
    production since 2026-08 (it is the reason a Gemini turn that cannot send
    ``response_json_schema`` still comes back parseable), so every other
    enforcement drop now sends the same words rather than inventing its own.
    """
    compact_schema = json.dumps(schema, ensure_ascii=False, separators=(",", ":"))
    return f"""FINAL ANSWER FORMAT:
Use your tools as needed. When you give your final answer, reply with exactly one fenced `json` object that conforms to the JSON Schema below, and nothing else: no prose before or after it, and no field omitted or truncated.

JSON Schema:
{compact_schema}"""


def attach_json_text_contract(config: Any, schema: dict[str, Any]) -> bool:
    """Put :func:`json_text_contract` into the request's system channel.

    Uses the canonical per-turn context block (``attach_turn_context``), which
    every translator renders into its own provider's system channel — so the
    guidance reaches Anthropic's ``system``, OpenAI's instructions and Gemini's
    ``system_instruction`` without a per-provider branch, and it never touches
    the person's own turn. Returns whether it landed.
    """
    messages = getattr(config, "messages", None)
    attach = getattr(messages, "attach_turn_context", None)
    if attach is None or not isinstance(schema, dict):
        return False
    try:
        attach(json_text_contract(schema), slot="structured_output_contract")
    except Exception as exc:  # noqa: BLE001 — guidance is never worth failing a turn
        vcprint(
            f"[answer_contract] could not attach the JSON text contract: {exc}",
            color="red",
        )
        return False
    return True


def append_json_text_contract_to_system(payload: dict[str, Any], schema: dict[str, Any]) -> None:
    """Append the contract to an already-assembled provider payload's ``system``.

    For the one place that has no ``UnifiedConfig`` left to attach to: the
    Anthropic grammar-budget ladder, whose rungs are rebuilt wire payloads. Both
    Anthropic system shapes are handled — a plain string, and the list of
    (possibly cache-marked) text blocks.
    """
    if not isinstance(payload, dict) or not isinstance(schema, dict):
        return
    contract = json_text_contract(schema)
    system = payload.get("system")
    if isinstance(system, str):
        payload["system"] = f"{system.rstrip()}\n\n{contract}" if system.strip() else contract
    elif isinstance(system, list):
        # A trailing, deliberately UNCACHED block: appending text to an existing
        # block would change the bytes a cache breakpoint was written against.
        payload["system"] = [*system, {"type": "text", "text": contract}]
    else:
        payload["system"] = contract


def verify_answer(answer: Any, schema: Any) -> list[str]:
    """Every way ``answer`` fails the DECLARED ``schema``, as readable lines.

    ``prune_optional_nulls`` runs first: a provider that demands every property in
    ``required`` is answered with required-and-nullable, so a ``null`` there is
    the boundary's own compromise speaking, not the model's mistake. Removing it
    restores the answer the author's schema describes.

    Advisory keywords the boundary strips for a provider (``minItems``,
    ``pattern``, …) are deliberately KEPT here — the whole point of the
    "platform-side validation still enforces it" line is that something does.
    """
    if not isinstance(schema, dict):
        return []
    try:
        import jsonschema
    except ImportError:  # pragma: no cover — jsonschema is a hard dependency
        return []
    from matrx_ai.schema.rules import prune_optional_nulls

    try:
        candidate = prune_optional_nulls(answer, schema)
    except Exception:  # noqa: BLE001 — a malformed schema is not the answer's fault
        candidate = answer
    validator_cls = jsonschema.validators.validator_for(schema)
    try:
        validator = validator_cls(schema)
    except Exception as exc:  # noqa: BLE001
        return [f"the declared schema is not a usable JSON Schema: {exc}"]
    problems: list[str] = []
    try:
        for error in validator.iter_errors(candidate):
            where = "$" + "".join(f".{part}" for part in error.absolute_path)
            problems.append(f"{where}: {error.message}")
            if len(problems) >= _MAX_REPORTED_FAILURES:
                break
    except Exception as exc:  # noqa: BLE001 — never turn a check into a failure
        return [f"the declared schema could not be applied: {exc}"]
    return problems


def _plain_text_of(content: Any) -> str:
    """Text out of whatever ``content`` is, when the canonical accessor cannot
    read it. ``UnifiedMessage.content`` is normally a list of content blocks, but
    the dataclass accepts a bare string too, and ``get_output()`` then raises
    ``AttributeError: 'str' object has no attribute 'get_output'``."""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts: list[str] = []
        for block in content:
            if isinstance(block, str):
                parts.append(block)
            elif isinstance(block, dict):
                if block.get("type") in (None, "text", "output_text"):
                    parts.append(str(block.get("text") or ""))
            else:
                text = getattr(block, "text", None)
                if isinstance(text, str) and type(block).__name__ != "ThinkingContent":
                    parts.append(text)
        return "\n".join(part for part in parts if part)
    return ""


def _answer_text(response: Any) -> str:
    """The last assistant turn's OUTPUT text — reasoning excluded, via the
    canonical accessor, with a plain-content fallback.

    🚨 The fallback is not defensive padding. This function used to
    ``return ""`` on any exception, and ``UnifiedMessage(content="…")`` — a bare
    string, which the dataclass accepts — makes ``get_output()`` raise, so the
    contract check was SKIPPED and reported nothing. A check that quietly does not
    run is worse than no check: it is the very defect this module exists to fix,
    reproduced inside the fix. Found by driving a real provider call through it.
    """
    for message in reversed(list(getattr(response, "messages", None) or [])):
        if str(getattr(message, "role", "")) not in ("assistant", "Role.ASSISTANT"):
            continue
        getter = getattr(message, "get_output", None)
        if getter is not None:
            try:
                text = getter()
            except Exception as exc:  # noqa: BLE001 — say so, never swallow
                vcprint(
                    f"[answer_contract] get_output() failed on the assistant turn "
                    f"({type(exc).__name__}: {exc}); reading its content directly so the "
                    "contract check still runs.",
                    color="yellow",
                )
            else:
                if text:
                    return text
        return _plain_text_of(getattr(message, "content", None))
    return ""


def _carries_tool_call(message: Any) -> bool:
    from matrx_ai.config.tools_config import ToolCallContent

    for block in getattr(message, "content", None) or ():
        if isinstance(block, ToolCallContent):
            return True
        if isinstance(block, dict) and block.get("type") in ("tool_call", "function_call"):
            return True
    return False


def _turn_is_final(response: Any) -> bool:
    """A turn that asked for a tool is not the answer — the contract is judged on
    the turn that ANSWERS.

    🚨 Read off the response's CONTENT, never off the finish reason alone. Gemini
    never returns a tool-call finish reason: a turn carrying a ``functionCall``
    comes back ``finishReason: STOP`` with a narrating text part ("I will fetch
    the webpage…"), ``FinishReason.from_google`` maps it to ``stop``, and judging
    by the reason alone called that narration the final answer. On 2026-09-28
    that produced 335 false HIGH ``answer_off_contract`` rows for one mandate in
    ~40 minutes, every one "no JSON object could be recovered" from a turn that
    was busy calling a tool (SCHEMA-TRANSLATION-VERIFY.md, R2). A check that cries
    wolf teaches everyone to ignore it.
    """
    reason = str(getattr(response, "finish_reason", None) or "")
    if reason in ("tool_calls", "malformed_function_call", "unexpected_tool_call"):
        return False
    for message in getattr(response, "messages", None) or ():
        if str(getattr(message, "role", "")) in ("assistant", "Role.ASSISTANT") and (
            _carries_tool_call(message)
        ):
            return False
    return True


def _final_assistant_message(response: Any) -> Any:
    for message in reversed(list(getattr(response, "messages", None) or [])):
        if str(getattr(message, "role", "")) in ("assistant", "Role.ASSISTANT"):
            return message
    return None


_FENCE = re.compile(r"```(?:json|JSON)?[ \t]*\n(.*?)\n?```", re.DOTALL)


def _json_fences(text: str) -> list[tuple[int, int]]:
    """``(start, end)`` spans of the BODY of every fenced ```json block."""
    return [(m.start(1), m.end(1)) for m in _FENCE.finditer(text)]


def conform_answer_to_contract(response: Any) -> list[str]:
    """Rewrite the FINAL answer in ``response`` so it says what the author's
    contract says: every ``null`` the boundary asked for becomes the absence the
    author meant. Returns the changes made (empty when nothing changed).

    This is the one place every answer passes through before any consumer reads
    it — the kind validator, a Pydantic output model, ``extract_json``, the
    persisted message, the ``STRUCTURED_OUTPUT`` event. Until 2026-09-28 the
    pruning ran only inside :func:`verify_answer`, on a private copy, so every
    consumer received ``null`` where the author's schema says "absent": the kind
    validator rejected 4 of 4 live kinds tested and Pydantic output models with a
    defaulted field failed to parse (SCHEMA-TRANSLATION-VERIFY.md, R1).

    Only a JSON answer is touched, and only when pruning changes it: an answer
    that is the whole text (provider-enforced), or one fenced ```json block
    (prompt-guided). Anything it cannot locate exactly is left alone — the
    contract check then reports it; nothing is ever rewritten on a guess.
    """
    contract = declared_output_contract()
    if not contract or not _turn_is_final(response):
        return []
    schema = contract.get("schema")
    message = _final_assistant_message(response)
    if message is None or not isinstance(schema, dict):
        return []
    from matrx_ai.config.unified_content import TextContent
    from matrx_ai.schema.rules import prune_optional_nulls

    blocks = [
        (index, block)
        for index, block in enumerate(getattr(message, "content", None) or [])
        if isinstance(block, TextContent) and block.text
    ]
    if not blocks:
        return []

    def _pruned_json(raw: str) -> str | None:
        try:
            parsed = json.loads(raw)
        except (TypeError, ValueError):
            return None
        if not isinstance(parsed, (dict, list)):
            return None
        pruned = prune_optional_nulls(parsed, schema)
        if pruned == parsed:
            return None
        return json.dumps(pruned, ensure_ascii=False)

    whole = "".join(block.text for _, block in blocks)
    replacement = _pruned_json(whole.strip())
    if replacement is not None:
        first_index, first = blocks[0]
        first.text = replacement
        drop = {index for index, _ in blocks[1:]}
        if drop:
            message.content = [b for i, b in enumerate(message.content) if i not in drop]
        return ["$: optional fields answered null were removed (the author's contract says absent)"]

    for _, block in blocks:
        spans = _json_fences(block.text)
        for start, end in reversed(spans):
            replacement = _pruned_json(block.text[start:end].strip())
            if replacement is not None:
                block.text = block.text[:start] + replacement + block.text[end:]
                return [
                    "$: optional fields answered null were removed from the fenced answer "
                    "(the author's contract says absent)"
                ]
    return []


async def verify_answer_and_record(
    response: Any,
    *,
    provider: str,
    model: str | None,
    was_enforced: bool | None = None,
    identity: dict[str, Any] | None = None,
) -> list[str]:
    """Judge the answer against the declared contract and, on a mismatch, RECORD
    it. Never raises into the caller's request; returns the problems it found.

    ``identity`` names the agent when the call has no app context to name it —
    the batch lane, whose answer is judged hours later in a handler dispatcher
    that runs as nobody. It overrides the context-derived identity.

    ``was_enforced=False`` says the provider was not holding the contract on this
    call, which is the case the finding text has to say out loud — the schema was
    dropped or relaxed and the answer is all there is.
    """
    contract = declared_output_contract()
    if not contract or not _turn_is_final(response):
        return []
    if was_enforced is None:
        was_enforced = bool(contract.get("enforced", True))
    schema = contract["schema"]
    text = _answer_text(response)
    if not text.strip():
        return []

    from matrx_ai.agents.response_parser import extract_json

    # `extract_json(schema=…)` is a candidate SELECTOR (type + required at depth
    # 1). It picks the right object out of prose when there are several — and
    # when the answer misses a required key it returns nothing, which used to be
    # reported as "no JSON could be recovered". Fall back to the plain extraction
    # so the finding names the key that is actually missing.
    parsed = extract_json(text, schema=schema)
    if parsed is None:
        parsed = extract_json(text)
    if parsed is None:
        problems = [
            "$: no JSON object could be recovered from the answer at all — "
            "the declared contract describes an object"
        ]
    else:
        problems = verify_answer(parsed, schema)
    if not problems:
        return []

    from matrx_ai.providers.structured_output_findings import (
        record_structured_output_finding,
        schema_fingerprint,
        schema_name_from_schema,
    )

    remedy = (
        "the provider was NOT enforcing this contract on this call, so nothing held it — "
        "reduce the schema (fewer properties / union fields) until the provider can enforce "
        "it, or bind the run to a model that can"
        if not was_enforced
        else "the provider accepted the request as enforced and the answer still misses the "
        "contract — the translated wire schema and the declared schema have diverged; "
        "the divergence is the bug, not the model"
    )
    vcprint(
        data={
            "provider": provider,
            "model": model,
            "schema_name": contract.get("name") or schema_name_from_schema(schema),
            "provider_enforced": was_enforced,
            "failures": problems,
        },
        title="🚨 ANSWER OFF CONTRACT",
        color="red",
        verbose=False,
    )
    vcprint(f"🚨 REMEDY [{provider}]: {remedy}", color="red")
    await record_structured_output_finding(
        ANSWER_OFF_CONTRACT,
        provider=provider,
        model=model,
        detail={
            "schema_name": contract.get("name") or schema_name_from_schema(schema),
            "schema_fingerprint": schema_fingerprint(schema),
            "provider_enforced": was_enforced,
            "dropped_because": contract.get("dropped_because"),
            "failures": problems,
            "remedy": remedy,
            **(identity or {}),
        },
        was_recovered=False,
    )
    return problems


__all__ = [
    "ANSWER_OFF_CONTRACT",
    "conform_answer_to_contract",
    "append_json_text_contract_to_system",
    "attach_json_text_contract",
    "bind_declared_output_contract",
    "declared_output_contract",
    "declared_schema_of",
    "json_text_contract",
    "mark_enforcement_dropped",
    "release_declared_output_contract",
    "use_declared_output_contract",
    "verify_answer",
    "verify_answer_and_record",
]
