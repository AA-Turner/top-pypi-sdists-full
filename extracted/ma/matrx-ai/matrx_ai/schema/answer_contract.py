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

#: The heading a grounded Gemini JSON reply STARTS with (the grounded text contract,
#: ``providers/google/translator.py`` ``_grounded_json_text_contract``). The ONE token: the translator
#: asks the model for it and the blocks splitter reads only this exact heading (any ``#`` level or
#: ``**bold**`` form) as the reply's working text — a ``reasoning`` block, never the answer.
GROUNDED_DIGEST_HEADING = "GROUNDED RESEARCH DIGEST"

#: The first line of the grounded Gemini JSON text contract (the Google translator writes it as the
#: system text; the registry's ``grounded_json_contract`` frame finds it by this line, so the
#: residual check accounts for it).
GROUNDED_JSON_CONTRACT_OPEN = "GEMINI GROUNDED-JSON STREAM CONTRACT:"
#: The line that opens the compact schema the contract ends with (one line, after it).
GROUNDED_JSON_CONTRACT_SCHEMA_LABEL = "JSON Schema:"

#: One issue class for the outcome this module exists to make visible: the answer
#: did not satisfy the contract the caller declared. HIGH — a machine consumer
#: downstream is about to read a shape it was promised and did not get.
ANSWER_OFF_CONTRACT = "structured_output.answer_off_contract"

#: Prefix of a :func:`conform_answer_to_contract` note that RESTORED a pinned
#: ``__kind`` — the model wrote the wrong value there, so it is recorded as a
#: recovered ``answer_off_contract`` finding, never passed over in silence.
KIND_RESTORED_PREFIX = "kind restored: "

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


def is_audio_only_output(caps: Any) -> bool:
    """THE one modality test: the model speaks (audio out) and writes no text (TTS).

    The Google translator skips the response schema on this signal; the contract
    binding reads the same function, so a spoken answer is never judged as JSON.
    """
    return bool(getattr(caps, "produces_audio", False)) and not bool(
        getattr(caps, "produces_text", False)
    )


def is_media_generator_output(caps: Any) -> bool:
    """A model whose answer IS media (audio, image, video) and that cannot hold a JSON
    structure: the declared JSON contract cannot apply to what it returns.

    Media agents (podcast audio / video / feature image) declare the ``media_asset``
    kind, but the answer is the generated asset, never a JSON text. Judging it
    produced false ``enforcement_dropped`` and ``answer_off_contract`` findings on
    every media call. A model that DOES declare json_schema / json_object keeps its
    contract, whatever else it emits. Reads the capability flags only, never a name.
    """
    if is_audio_only_output(caps):
        return True
    media = any(
        bool(getattr(caps, flag, False))
        for flag in ("produces_audio", "produces_image", "produces_video")
    )
    mode = getattr(getattr(caps, "structured_output_mode", None), "value", None) or getattr(
        caps, "structured_output_mode", None
    )
    return media and mode not in ("schema", "json")


def bind_declared_output_contract(response_format: Any, caps: Any = None) -> Token:
    """Record the contract THIS call declared, before anything can downgrade it.

    ALWAYS sets — to ``None`` when there is no schema — because a ContextVar set
    inside one dispatch outlives it in the same asyncio task: a call that declares
    nothing must not inherit the previous call's contract and be judged against it.

    Must run before the capability gates: ``_downgrade_response_format`` replaces
    ``config.response_format`` outright and takes the schema with it.
    """
    if caps is not None and is_media_generator_output(caps):
        # An audio answer is not text: no JSON contract applies (answer_off_contract f257f0c5).
        return _DECLARED.set(None)
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


#: Kind slug → writer of that kind's prompt contract (``fn(schema) -> str | None``). A kind whose schema
#: is too large to read well as raw JSON (``visual_map``: ten engine schemas, ~65 KB) registers the
#: authoring text a model actually follows; ``json_text_contract`` uses it in place of the dump. The
#: answer is still checked against the full declared schema. Registered by the host at startup.
_KIND_CONTRACT_WRITERS: dict[str, Any] = {}


def register_kind_contract_writer(kind_slug: str, writer: Any) -> None:
    """Register ``writer(schema) -> str | None`` as the prompt contract body for ``kind_slug``."""
    _KIND_CONTRACT_WRITERS[kind_slug] = writer


def _schema_kind(schema: dict[str, Any]) -> str | None:
    marker = (schema.get("properties") or {}).get("__kind") if isinstance(schema, dict) else None
    if isinstance(marker, dict):
        if isinstance(marker.get("const"), str):
            return marker["const"]
        enum = marker.get("enum")
        if isinstance(enum, list) and len(enum) == 1 and isinstance(enum[0], str):
            return enum[0]
    return None


def json_text_contract(schema: dict[str, Any]) -> str:
    """The final-answer contract to put in the prompt when the provider's native
    schema switch cannot be used.

    This exact wording has been Google's ``_tool_json_text_contract`` in
    production since 2026-08 (it is the reason a Gemini turn that cannot send
    ``response_json_schema`` still comes back parseable), so every other
    enforcement drop now sends the same words rather than inventing its own.
    """
    writer = _KIND_CONTRACT_WRITERS.get(_schema_kind(schema) or "")
    if writer is not None:
        try:
            body = writer(schema)
        except Exception as exc:  # noqa: BLE001 — fall back to the schema dump, loudly
            vcprint(f"[answer_contract] kind contract writer failed: {exc}", color="red")
            body = None
        if isinstance(body, str) and body.strip():
            return f"""FINAL ANSWER FORMAT:
Use your tools as needed. When you give your final answer, reply with exactly one fenced `json` object written by the rules below, and nothing else: no prose before or after it, and no field omitted or truncated.

{body.strip()}"""
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
        # The send boundary may already have rendered this turn's block into the platform's host turn
        # (``send_boundary.order_for_wire``); a slot joined after it is then never sent, and the translator
        # does not re-render a placed block. 2026-10-24: every capability downgrade's contract was lost this
        # way — Haiku saw 4,138 input tokens and no contract, and answered in Mermaid. Re-render the host
        # turn so the contract rides with the block (the converted-prefill path does the same).
        wire = getattr(messages, "_messages", None)
        render = getattr(messages, "render_turn_context", None)
        if isinstance(wire, list) and callable(render):
            from matrx_ai.config.typed_text_last import refresh_host_turn

            messages._messages = refresh_host_turn(wire, render())
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


#: Why a provider stopped an answer before it was finished, in words a reader can act on. A schema
#: change fixes none of these, so an off-contract finding on a cut-short answer must never prescribe one.
_CUT_SHORT_REMEDY: dict[str, str] = {
    "max_tokens": (
        "the output cap was reached mid-answer — raise the agent's max output tokens or ask for a "
        "shorter answer; the schema is not the cause"
    ),
    "recitation": (
        "the provider stopped the answer because it was reproducing source text verbatim "
        "(RECITATION) — ask the agent to paraphrase instead of copying long passages (transcripts, "
        "articles); the schema is not the cause"
    ),
    "model_context_window_exceeded": (
        "the context window filled mid-answer — send less input or bind a larger-context model; "
        "the schema is not the cause"
    ),
    "refusal": "the model refused to answer — the request, not the schema, is what it declined",
}
_CUT_SHORT_FILTERED = (
    "the provider's content filter stopped the answer ({reason}) — the input or the request "
    "tripped it; the schema is not the cause"
)
#: Tool-call stops are a turn that is not the answer (``_turn_is_final``), never a cut-short answer.
_NOT_CUT_SHORT = frozenset({"malformed_function_call", "unexpected_tool_call"})


def answer_cut_short_by(response: Any) -> str | None:
    """The finish reason that STOPPED this answer before it was complete, or ``None``.

    A provider that stops a structured answer mid-way (output cap, RECITATION, a content filter,
    a refusal) leaves a JSON fragment. Judged as a finished answer, that fragment was reported as
    "reduce the schema" — and the schema-less fallback extraction then picked an inner array out
    of the broken object and filed "[...] is not of type 'object'" (2026-11-17: the YouTube
    analyzer stopped on ``recitation`` after ~16k tokens, twice, both filed as schema failures).
    Read off the unified :class:`FinishReason`, so every provider shares one answer.
    """
    from matrx_ai.config.finish_reason import FinishReason

    raw = getattr(response, "finish_reason", None)
    value = str(getattr(raw, "value", raw) or "").strip().lower()
    if not value or value in _NOT_CUT_SHORT:
        return None
    try:
        reason = FinishReason(value)
    except ValueError:
        return None
    if reason.is_truncated() or reason.is_error():
        return reason.value
    return None


def _finish_reason_text(response: Any) -> str:
    raw = getattr(response, "finish_reason", None)
    return str(getattr(raw, "value", raw) or "unknown").strip().lower()


def cut_short_remedy(reason: str) -> str:
    """What to change when ``reason`` stopped the answer (never "reduce the schema")."""
    return _CUT_SHORT_REMEDY.get(reason) or _CUT_SHORT_FILTERED.format(reason=reason)


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

    Only a JSON answer is touched, and only when pruning (or restoring a
    ``__kind`` the schema pins to one value) changes it: an answer
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
    from matrx_ai.schema.rules import prune_optional_nulls, restore_declared_kinds

    blocks = [
        (index, block)
        for index, block in enumerate(getattr(message, "content", None) or [])
        if isinstance(block, TextContent) and block.text
    ]
    if not blocks:
        return []

    def _conformed_json(raw: str) -> tuple[str, list[str]] | None:
        # Read through the ONE parse funnel, exactly as every consumer downstream reads it (strict,
        # then the faithful near-miss repair; a cut-off document is refused). Strict `json.loads`
        # alone skipped a block holding LaTeX `\(` (an illegal JSON escape) and pruned nothing, while
        # the mandate's reader repaired the same text and judged the boundary's nulls as drift
        # (system_error c9559cdf, 2026-11-18).
        from matrx_ai.agents.response_parser import parse_json_document

        parsed = parse_json_document(raw)
        if not isinstance(parsed, (dict, list)):
            return None
        pruned = prune_optional_nulls(parsed, schema)
        notes: list[str] = []
        if pruned != parsed:
            notes.append("$: optional fields answered null were removed, and empty placeholders at fields narrowed to non-null read as the null the author allows")
        # A `__kind` the schema pins to ONE value is restored to it — the slot
        # carries no information from the model (rules.restore_declared_kinds).
        restored, kind_notes = restore_declared_kinds(pruned, schema)
        notes.extend(f"{KIND_RESTORED_PREFIX}{note}" for note in kind_notes)
        if not notes:
            return None
        return json.dumps(restored, ensure_ascii=False), notes

    whole = "".join(block.text for _, block in blocks)
    conformed = _conformed_json(whole.strip())
    if conformed is not None:
        replacement, notes = conformed
        first_index, first = blocks[0]
        first.text = replacement
        drop = {index for index, _ in blocks[1:]}
        if drop:
            message.content = [b for i, b in enumerate(message.content) if i not in drop]
        return notes

    for _, block in blocks:
        spans = _json_fences(block.text)
        for start, end in reversed(spans):
            conformed = _conformed_json(block.text[start:end].strip())
            if conformed is not None:
                replacement, notes = conformed
                block.text = block.text[:start] + replacement + block.text[end:]
                return notes
    return []


def bounds_the_provider_cannot_carry(answer: Any, schema: Any, provider: str) -> list[str]:
    """The stripped keywords that ALONE put ``answer`` off contract, sorted.

    The request boundary strips the bounds a provider's engine refuses
    (``maxLength``, ``pattern``, ``minItems``…, ``unsupported_structured_output_keywords``)
    while ``verify_answer`` keeps judging them. An answer that passes the schema the
    provider actually received and fails only the declared one broke a bound the
    provider never held — not a translator divergence. Empty when the answer also
    fails the provider's copy (the shape itself is off) or nothing was stripped."""
    from matrx_ai.schema.rules import strip_unsupported_keywords, unsupported_structured_output_keywords

    unsupported = unsupported_structured_output_keywords(provider)
    if not unsupported or not isinstance(schema, dict):
        return []
    if verify_answer(answer, strip_unsupported_keywords(schema, unsupported)):
        return []
    present: set[str] = set()

    def walk(node: Any, *, name_map: bool = False) -> None:
        if isinstance(node, list):
            for item in node:
                walk(item)
        elif isinstance(node, dict):
            for key, value in node.items():
                if not name_map and key in unsupported:
                    present.add(key)
                walk(value, name_map=key in ("properties", "$defs", "definitions") and not name_map)

    walk(schema)
    return sorted(present)


async def verify_answer_and_record(
    response: Any,
    *,
    provider: str,
    model: str | None,
    was_enforced: bool | None = None,
    identity: dict[str, Any] | None = None,
    conformed: list[str] | None = None,
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
    restored = [n[len(KIND_RESTORED_PREFIX):] for n in conformed or () if n.startswith(KIND_RESTORED_PREFIX)]
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
    extraction = extract_json(text, schema=schema, detailed=True)
    parsed = extraction.data if extraction.success else None
    cut_short = answer_cut_short_by(response)
    if parsed is None and not cut_short:
        # A finished answer only: on a cut-short one the plain extraction picks a complete INNER
        # value out of the broken object and the finding then blames its type, not the stop.
        extraction = extract_json(text, detailed=True)
        parsed = extraction.data if extraction.success else None
    # A document the text left OPEN that json-repair closed is cut-off data, whatever the stop
    # reason says: every required key may have been written before the cut, so it can satisfy the
    # schema while the tail (the half-written item, everything after it) is gone. Never on contract.
    truncated_json = parsed is not None and extraction.truncated
    if truncated_json:
        problems = [
            f"$: the answer's JSON was cut off before it closed (finish_reason={cut_short or _finish_reason_text(response)}) "
            "— json-repair closed it, so everything after the cut is lost; an incomplete answer is "
            "never judged on contract"
        ]
    elif parsed is None:
        problems = [
            f"$: the provider stopped the answer (finish_reason={cut_short}) before its JSON "
            "was complete — no answer object exists to judge"
            if cut_short
            else "$: no JSON object could be recovered from the answer at all — "
            "the declared contract describes an object"
        ]
    else:
        problems = verify_answer(parsed, schema)

    from matrx_ai.providers.structured_output_findings import (
        record_structured_output_finding,
        schema_fingerprint,
        schema_name_from_schema,
    )

    if not problems:
        if restored:
            # The model missed the contract and the pinned `__kind` slots were
            # restored before any consumer read the answer: on contract now, and
            # recorded as RECOVERED so the slip stays visible.
            vcprint(
                f"⚠️  [answer_contract] {provider}/{model}: restored {len(restored)} pinned "
                f"__kind slot(s) the model got wrong: {restored}",
                color="yellow",
            )
            await record_structured_output_finding(
                ANSWER_OFF_CONTRACT,
                provider=provider,
                model=model,
                detail={
                    "schema_name": contract.get("name") or schema_name_from_schema(schema),
                    "schema_fingerprint": schema_fingerprint(schema),
                    "provider_enforced": was_enforced,
                    "dropped_because": contract.get("dropped_because"),
                    "failures": restored,
                    "remedy": "restored: each slot is a schema-pinned __kind, so the declared value is the only legal one",
                    **(identity or {}),
                },
                was_recovered=True,
            )
        return []

    unenforced_bounds = (
        bounds_the_provider_cannot_carry(parsed, schema, provider)
        if was_enforced and parsed is not None and not cut_short and not truncated_json
        else []
    )
    remedy = (
        cut_short_remedy(cut_short)
        if cut_short
        else "the answer text ended mid-JSON although the provider reported a normal stop — the "
        "stream or the model ended early; rerun it, and if it repeats raise the output cap or ask "
        "for a shorter answer; the schema is not the cause"
        if truncated_json
        else "the provider was NOT enforcing this contract on this call, so nothing held it — "
        "reduce the schema (fewer properties / union fields) until the provider can enforce "
        "it, or bind the run to a model that can"
        if not was_enforced
        else f"the answer breaks only bound(s) {provider} cannot enforce ({', '.join(unenforced_bounds)}) — "
        "the request boundary strips them, so this check is the only thing holding them; state "
        "the bound in the field's description or the prompt, relax it, or bind the run to a "
        "provider that enforces it"
        if unenforced_bounds
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
            **({"cut_short_by": cut_short} if cut_short else {}),
            **({"truncated_json": True} if truncated_json else {}),
            **({"kinds_restored": restored} if restored else {}),
            **({"unenforced_bounds": unenforced_bounds} if unenforced_bounds else {}),
            "remedy": remedy,
            **(identity or {}),
        },
        was_recovered=False,
    )
    return problems


__all__ = [
    "ANSWER_OFF_CONTRACT",
    "KIND_RESTORED_PREFIX",
    "GROUNDED_DIGEST_HEADING",
    "conform_answer_to_contract",
    "answer_cut_short_by",
    "append_json_text_contract_to_system",
    "attach_json_text_contract",
    "bind_declared_output_contract",
    "is_audio_only_output",
    "is_media_generator_output",
    "cut_short_remedy",
    "declared_output_contract",
    "declared_schema_of",
    "json_text_contract",
    "mark_enforcement_dropped",
    "release_declared_output_contract",
    "use_declared_output_contract",
    "verify_answer",
    "verify_answer_and_record",
]
