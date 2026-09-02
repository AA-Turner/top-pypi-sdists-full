"""Shared output model + helpers for matrx-ai graph actions.

Chat / agent.start / conversation.continue / llm.chat all converge on the
same underlying ``execute_ai_request(config, ...)`` — so they share the
same output shape.

Why a custom output model instead of returning ``CompletedRequest`` directly:

- ``CompletedRequest`` is a dataclass, not a Pydantic model — can't round-trip
  through a channel/checkpoint without a manual dump.
- The Studio inspector only needs a handful of fields; serializing the full
  request + provider-raw response bloats checkpoints by an order of magnitude.
- Actions are contracts. Stable Pydantic shapes here mean downstream nodes
  can wire to specific fields (``final_text``, ``messages``) without needing
  to know how matrx-ai internally represents messages.

``normalize_completed()`` is the single function that converts a
``CompletedRequest`` into the typed output — keep all field-extraction logic
there so the four action wrappers stay thin.
"""

from __future__ import annotations

import logging

from typing import TYPE_CHECKING, Any

from pydantic import BaseModel, ConfigDict, Field, JsonValue

if TYPE_CHECKING:
    from matrx_graph.types.result import NodeResult

    from matrx_ai.orchestrator.requests import CompletedRequest


logger = logging.getLogger(__name__)

class AiTurnFailedError(RuntimeError):
    """The underlying AI turn did not complete successfully.

    Raised by ``normalize_completed`` when the orchestrator's
    ``CompletedRequest.metadata`` carries a terminal non-success status — a
    provider error after exhausted retries (``failed``) or a loop that never
    reached completion (``paused_loop_guard`` / ``max_iterations_exceeded``).

    A workflow node MUST fail in these cases so the scheduler parks the run
    (recoverable) at the node that broke. The HTTP chat path surfaces these
    in-stream instead of raising — that is correct for a live stream, but a
    graph action swallowing them returned an empty-but-"successful" result:
    the run went green while the agent had actually failed (found live
    2026-07-04). That silent-success class is exactly what this raise kills.
    """


# CompletedRequest.metadata statuses that mean "the turn did not do its job".
# ``truncated`` is deliberately NOT here — a truncated turn carries real
# content and matches the chat path's behavior of returning it.
_FAILURE_STATUSES: frozenset[str] = frozenset(
    {"failed", "paused_loop_guard", "max_iterations_exceeded"}
)


class AiMessage(BaseModel):
    """Single message in the conversation as seen by the workflow.

    Flattens the matrx-ai ``UnifiedMessage`` into a stable JSON shape.
    Unknown / provider-specific keys land in ``extra`` so consumers can
    reach them without losing fidelity — ``extra="allow"`` is deliberate
    and must stay (``to_storage_dict()`` payloads carry provider keys we
    never declare here).

    ``content`` / ``tool_calls`` values are genuinely dynamic JSON —
    provider content blocks and tool-call envelopes whose shape varies per
    provider — hence ``JsonValue``, never a declared block union that
    would drift from the providers.
    """

    model_config = ConfigDict(
        extra="allow",
        json_schema_extra={
            "x-contract-dynamic": "provider-specific storage keys (to_storage_dict payloads) must survive"
        },
    )

    role: str
    content: JsonValue = None
    tool_calls: list[dict[str, JsonValue]] = Field(default_factory=list)
    tool_call_id: str | None = None
    name: str | None = None


class AiModelUsage(BaseModel):
    """Per-model token/cost breakdown — one entry in :class:`AiUsage.models`.

    Closed shape, one canonical key-set across every producer. ``cost_usd``
    matches the top-level ``AiUsage.cost_usd`` (this unified a prior divergence
    where graph_nodes wrote ``cost`` while the podcast aggregator wrote
    ``cost_usd``). ``api`` / ``request_count`` default to ``""`` / ``0`` for
    producers that don't track them.
    """

    model_config = ConfigDict(extra="forbid")

    input_tokens: int = 0
    output_tokens: int = 0
    total_tokens: int = 0
    cost_usd: float = 0.0
    request_count: int = 0
    api: str = ""


class AiUsage(BaseModel):
    """Aggregated token / cost usage for the run.

    Every constructor in the package (``_extract_usage`` below and the
    podcast pipeline's stage aggregators) sets only the declared fields, so
    the model is closed — no ``extra="allow"``. Per-model breakdown values are
    typed as :class:`AiModelUsage`: the two producer shapes were unified onto
    one canonical key-set (``cost_usd`` everywhere), so this is a precise
    contract, not an open ``dict[str, JsonValue]``.
    """

    input_tokens: int = Field(default=0, description="Total input tokens billed across the run.")
    output_tokens: int = Field(default=0, description="Total output tokens billed across the run.")
    total_tokens: int = Field(
        default=0, description="Combined input and output token count across the run."
    )
    cost_usd: float = Field(default=0.0, description="Total estimated provider cost in US dollars.")
    models: dict[str, AiModelUsage] = Field(
        default_factory=dict, description="Per-model usage breakdown keyed by canonical model name."
    )


class AiExecutionResult(BaseModel):
    """Canonical output for every matrx-ai graph action.

    Whether the node ran a single chat turn or a multi-iteration agent loop,
    the workflow sees the same shape: ``final_text`` for the final assistant
    response, ``messages`` for the full conversation history (so the next
    node in the graph can continue the thread), and ``usage`` for cost
    tracking.
    """

    model_config = ConfigDict(extra="forbid")

    conversation_id: str
    request_id: str
    iterations: int
    finish_reason: str | None = None
    final_text: str = ""
    final_message: AiMessage | None = None
    messages: list[AiMessage] = Field(default_factory=list)
    usage: AiUsage = Field(default_factory=AiUsage)
    duration_ms: int = 0
    tool_calls_made: int = 0
    # Orchestrator run metadata (status, error detail, loop stats, caller
    # tags) — an open provider/orchestrator passthrough, hence JsonValue.
    metadata: dict[str, JsonValue] = Field(default_factory=dict)
    # Parsed structured output when the request carried a json_schema
    # response_format (i.e. the agent has an output_schema). This is the
    # graph-payload twin of the STRUCTURED_OUTPUT stream event — without it,
    # downstream nodes could see only final_text and would have to re-parse.
    # None when there is no schema or parsing failed. Model-authored JSON —
    # genuinely dynamic, hence JsonValue.
    structured_output: dict[str, JsonValue] | list[JsonValue] | None = None
    # THE AGENT OUTPUT CONTRACT (plan of record KINDS_EVERYWHERE_PLAN.md §6,
    # Arman 2026-08-20): the response as an ORDERED LIST OF KIND INSTANCES —
    # Anthropic's content-block model applied to platform kinds. Plain prose
    # is ONE markdown instance; a bound agent is ONE instance of its bound
    # kind; prose with embedded structures is the interleaved sequence, each
    # element carrying __kind. Populated by the SAME detection pipeline chat
    # runs (processing.blocks.content_view) — never a second parser. This is
    # what kind-filtered edges and triggers route on; final_text remains the
    # verbatim transcript.
    content: list[dict[str, JsonValue]] = Field(default_factory=list)


def normalize_completed_result(completed: CompletedRequest) -> NodeResult[AiExecutionResult]:
    """Node Result System wrapper over :func:`normalize_completed`.

    Returns ``Success[AiExecutionResult]`` for a completed turn, or a
    ``Failure(code='ai_turn_failed')`` for a terminal non-success — with the
    billed usage carried under ``error.details['usage']`` so the scheduler's
    failure-path cost settlement still records the spend (a failed paid call
    is billed in full). Migrated ai.* graph nodes use THIS; legacy nodes keep
    calling ``normalize_completed`` (its raise goes through the scheduler's
    same failure ladder) until their Wave-1 migration.
    """
    from matrx_graph.types.result import NodeResult, failure, success  # noqa: F401

    try:
        normalized = normalize_completed(completed)
    except AiTurnFailedError as e:
        meta = dict(getattr(completed, "metadata", {}) or {})
        usage = _extract_usage(getattr(completed, "total_usage", None))
        request = getattr(completed, "request", None)
        return failure(
            "ai_turn_failed",
            str(e),
            details={
                "status": str(meta.get("status") or ""),
                "error_type": str(meta.get("error_type") or ""),
                "usage": usage.model_dump(mode="json"),
                "conversation_id": getattr(request, "conversation_id", "") or "",
                "request_id": getattr(request, "request_id", "") or "",
            },
        )
    if _requires_structured_output(completed) and normalized.structured_output is None:
        return failure(
            "structured_output_invalid",
            "AI completed, but its declared structured output could not be parsed and validated.",
            details={
                "usage": normalized.usage.model_dump(mode="json"),
                "conversation_id": normalized.conversation_id,
                "request_id": normalized.request_id,
            },
        )
    return success(normalized)


def _requires_structured_output(completed: CompletedRequest) -> bool:
    request = getattr(completed, "request", None)
    config = getattr(request, "config", None)
    response_format = getattr(config, "response_format", None)
    return isinstance(response_format, dict) and response_format.get("type") == "json_schema"


def normalize_completed(completed: CompletedRequest) -> AiExecutionResult:
    """Convert a matrx-ai ``CompletedRequest`` into the canonical result shape.

    Raises :class:`AiTurnFailedError` when the turn's terminal status is a
    failure (see ``_FAILURE_STATUSES``) — a failed turn must fail the node,
    never flow an empty payload downstream as "success".

    Otherwise defensive: matrx-ai internals evolve, so every field is pulled
    with ``getattr`` + a fallback. Missing fields become their type defaults
    rather than raising — a workflow node failing because of a new
    CompletedRequest field would be a hostile UX.
    """
    meta = dict(getattr(completed, "metadata", {}) or {})
    status = str(meta.get("status") or "")
    if status in _FAILURE_STATUSES:
        error_message = str(meta.get("error") or "no error detail recorded")
        error_type = str(meta.get("error_type") or status)
        raise AiTurnFailedError(
            f"AI turn ended with status '{status}' ({error_type}): {error_message}"
        )

    request = getattr(completed, "request", None)
    final_response = getattr(completed, "final_response", None)

    messages = _extract_messages(request)

    final_text = _extract_final_text(final_response)
    if not final_text and messages:
        # Fallback to the last message if final_response was empty or missing
        last_msg = messages[-1]
        if last_msg.content:
            if isinstance(last_msg.content, str):
                final_text = last_msg.content
            elif isinstance(last_msg.content, list):
                parts = []
                for p in last_msg.content:
                    if isinstance(p, dict) and p.get("type") in ("text", "output_text"):
                        parts.append(p.get("text", ""))
                final_text = "".join(parts)

    final_message = _extract_final_message(final_response)
    if not final_message and messages:
        final_message = messages[-1]

    usage = _extract_usage(getattr(completed, "total_usage", None))

    timing = getattr(completed, "timing_stats", {}) or {}
    # ``TimingUsage.aggregate`` reports SECONDS under ``total_duration``; it has
    # no ``total_duration_ms`` key at all, so reading only that name made
    # ``duration_ms`` 0 on every real run of every matrx-ai graph node (found
    # 2026-08-20 distilling ``agent_react_result`` — a live agent turn reported
    # ``duration_ms: 0``). The replay harness DOES emit ``total_duration_ms``
    # directly, so that name still wins when present.
    duration_ms = int(timing.get("total_duration_ms") or 0)
    if not duration_ms:
        duration_ms = int(round(float(timing.get("total_duration") or 0.0) * 1000))

    tool_stats = getattr(completed, "tool_call_stats", {}) or {}
    # The SAME key-name bug as ``duration_ms`` above, in the same function, found
    # the same way (2026-08-22, reading real research-node outcomes):
    # ``ToolCallUsage.aggregate`` returns ``total_tool_calls`` and has no
    # ``total_calls`` key at all, so reading only that name reported
    # ``tool_calls_made: 0`` on EVERY run of every matrx-ai graph node — including
    # runs whose own recorded messages contain tool_call/tool_result blocks. It is
    # not a cosmetic counter: a Hindsight reviewer judging a research step read it
    # as proof that no search had occurred and filed a confident, wrong finding
    # ("wire a real search tool into the mandate" — the tools were wired).
    # The replay harness (``testing/record_replay.py``) builds the ``total_calls``
    # shape directly, so that name is still honored when present.
    tool_calls_made = int(
        tool_stats.get("total_tool_calls") or tool_stats.get("total_calls") or 0
    )

    finish_reason: str | None = None
    if final_response is not None:
        finish_reason = getattr(final_response, "finish_reason", None)

    structured_output = _extract_structured_output(request, final_text)
    return AiExecutionResult(
        conversation_id=getattr(request, "conversation_id", "") or "",
        request_id=getattr(request, "request_id", "") or "",
        iterations=int(getattr(completed, "iterations", 0) or 0),
        finish_reason=finish_reason,
        final_text=final_text,
        final_message=final_message,
        messages=messages,
        usage=usage,
        duration_ms=duration_ms,
        tool_calls_made=tool_calls_made,
        metadata=dict(getattr(completed, "metadata", {}) or {}),
        structured_output=structured_output,
        content=_extract_content(structured_output, final_text),
    )


def _extract_content(
    structured_output: dict[str, Any] | list[Any] | None, final_text: str
) -> list[dict[str, Any]]:
    """The §6 content list — ordered kind instances, one element when simple.

    A BOUND agent's answer IS its structured output: one instance, provided it
    says what it is (``__kind`` — true whenever the binding came from
    ``response_format_for_kind``, whose block schema declares the
    discriminator). A schema-bound answer WITHOUT the marker cannot be named
    here, and inventing a name would be a fake kind — so content stays empty
    and ``structured_output`` remains the typed access path (binding the agent
    to a registered kind is the fix, and the parity boards make that visible).
    An unbound agent's text goes through the same detection pipeline chat
    runs. Never raises: content is a VIEW — a parse hiccup must not fail a
    completed, billed turn.
    """
    try:
        if structured_output is not None:
            if (
                isinstance(structured_output, dict)
                and isinstance(structured_output.get("__kind"), str)
                and structured_output["__kind"]
            ):
                return [structured_output]
            # Round-1 F11: a LIST of self-described instances is content too
            # — each element routable. Mixed/anonymous lists stay out (cannot
            # be named without inventing identities).
            if isinstance(structured_output, list) and structured_output:
                elements = [
                    e
                    for e in structured_output
                    if isinstance(e, dict)
                    and isinstance(e.get("__kind"), str)
                    and e["__kind"]
                ]
                if len(elements) == len(structured_output):
                    return elements
            return []
        from matrx_ai.processing.blocks.content_view import content_from_text

        return content_from_text(final_text)
    except Exception as exc:  # noqa: BLE001 — a view must never fail the turn
        logger.error(
            "content view extraction failed (content=[] on a completed turn — "
            "final_text/structured_output remain authoritative): %s: %s",
            type(exc).__name__,
            exc,
        )
        return []


def _extract_structured_output(request: Any, final_text: str) -> dict[str, Any] | list[Any] | None:
    """Parse ``final_text`` against the request's json_schema response_format.

    Mirrors the orchestrator's STRUCTURED_OUTPUT funnel
    (``_emit_structured_output_if_schema``) minus the stream emission: fires
    for the OpenAI ``json_schema`` envelope (schema-validated parse) AND for
    a bare ``json_object`` format (schema-less parse — the model was told to
    emit JSON, so downstream nodes still deserve the parsed object; this is
    the second, independent layer behind the ai_task hydration that upgrades
    an agent's ``json_object`` to its declared ``output_schema``). Routes
    through the one parse funnel (``parse_agent_output``), and never raises —
    no JSON format or a failed parse yields ``None``.
    """
    try:
        config = getattr(request, "config", None)
        rf = getattr(config, "response_format", None) if config is not None else None
        if not isinstance(rf, dict) or not final_text:
            return None
        rf_type = rf.get("type")
        if rf_type == "json_schema":
            envelope = rf.get("json_schema")
            if not isinstance(envelope, dict):
                return None
        elif rf_type == "json_object":
            envelope = None  # schema-less extraction
        else:
            return None

        from matrx_ai.agents.output import parse_agent_output

        extraction = parse_agent_output(final_text, envelope)
        if not extraction.success:
            return None
        data = extraction.data
        return data if isinstance(data, dict | list) else None
    except Exception:  # noqa: BLE001 — same defensive stance as the rest of this module
        return None


def _extract_final_text(final_response: Any) -> str:
    """Extract the final assistant text from a ``UnifiedResponse``.

    The canonical shape is::

        UnifiedResponse(
            messages: list[UnifiedMessage],
            usage, stop_reason, finish_reason, ...
        )
        UnifiedMessage(role: str, content: list[UnifiedContent])
        TextContent(type="text", text="...")

    The text we want is the **last assistant message's** TextContent
    parts, concatenated. (Streaming, non-streaming, agent-loop — they
    all converge on this same shape; the orchestrator finalises the
    streamed chunks into a TextContent before returning.)

    Fallbacks are kept for legacy provider responses that haven't been
    fully unified yet.
    """
    if final_response is None:
        return ""

    # CANONICAL: UnifiedResponse.messages[-1].content[i].text
    messages = getattr(final_response, "messages", None)
    if isinstance(messages, list) and messages:
        last_assistant = None
        for msg in reversed(messages):
            role = getattr(msg, "role", None)
            if role == "assistant":
                last_assistant = msg
                break
        target = last_assistant or messages[-1]
        text = _text_from_unified_content(getattr(target, "content", None))
        if text:
            return text

    # Legacy fallback: some adapters return text/final_text/content directly.
    for attr in ("text", "final_text"):
        value = getattr(final_response, attr, None)
        if isinstance(value, str) and value:
            return value

    # Legacy fallback: content may be a string or a list of parts.
    content = getattr(final_response, "content", None)
    if isinstance(content, str) and content:
        return content
    if isinstance(content, list):
        text = _text_from_unified_content(content)
        if text:
            return text
    return ""


def _text_from_unified_content(content: Any) -> str:
    """Concatenate TextContent.text from a UnifiedMessage.content list.

    Accepts Pydantic models, dataclasses, dicts (post-serialization), or
    bare strings. Returns empty string if nothing text-like is found.
    """
    if content is None:
        return ""
    if isinstance(content, str):
        return content
    if not isinstance(content, list):
        return ""
    parts: list[str] = []
    for part in content:
        if isinstance(part, str):
            parts.append(part)
            continue
        if isinstance(part, dict):
            part_type = part.get("type")
            text = part.get("text")
            if part_type in ("text", "output_text", "input_text", None) and isinstance(text, str):
                parts.append(text)
            continue
        # Pydantic models / dataclasses / TextContent instances.
        part_type = getattr(part, "type", getattr(part, "part_type", None))
        if part_type in ("text", "output_text", "input_text", None):
            text = getattr(part, "text", None)
            if isinstance(text, str):
                parts.append(text)
    return "".join(parts)


def _extract_final_message(final_response: Any) -> AiMessage | None:
    if final_response is None:
        return None
    message = getattr(final_response, "message", None)
    if message is None:
        text = _extract_final_text(final_response)
        return AiMessage(role="assistant", content=text) if text else None
    return _message_to_model(message)


def _extract_messages(request: Any) -> list[AiMessage]:
    if request is None:
        return []
    config = getattr(request, "config", None)
    if config is None:
        return []
    messages = getattr(config, "messages", None)
    if messages is None:
        return []
    out: list[AiMessage] = []
    for m in messages:
        out.append(_message_to_model(m))
    return out


def _message_to_model(message: Any) -> AiMessage:
    if isinstance(message, AiMessage):
        return _ensure_jsonable_message(message)
    if isinstance(message, dict):
        return AiMessage.model_validate(_jsonable_message_dict(message))

    to_storage = getattr(message, "to_storage_dict", None)
    if callable(to_storage):
        try:
            stored = to_storage()
            if isinstance(stored, dict):
                return AiMessage.model_validate(_jsonable_message_dict(stored))
        except Exception:  # noqa: BLE001
            # Normalization is deliberately defensive: in-memory messages may
            # contain provider-ready or transient content that is not yet in
            # the persistence serializer's storage shape. Fall through to the
            # JSON-safe attribute conversion instead of failing the graph node
            # after the underlying AI turn already completed successfully.
            pass

    # UnifiedMessage dataclass-ish: try model_dump / asdict fallback
    for attr in ("model_dump", "dict", "to_dict"):
        method = getattr(message, attr, None)
        if callable(method):
            try:
                dumped = method()
                if isinstance(dumped, dict):
                    return AiMessage.model_validate(_jsonable_message_dict(dumped))
            except Exception:  # noqa: BLE001
                pass
    role = getattr(message, "role", "unknown")
    content = _content_to_jsonable(getattr(message, "content", None))
    return AiMessage(role=str(role), content=content)


def _ensure_jsonable_message(message: AiMessage) -> AiMessage:
    if message.content is None or isinstance(message.content, str):
        return message
    sanitized = _content_to_jsonable(message.content)
    if sanitized is message.content:
        return message
    return message.model_copy(update={"content": sanitized})


def _jsonable_message_dict(payload: dict[str, Any]) -> dict[str, Any]:
    out = dict(payload)
    if "content" in out:
        out["content"] = _content_to_jsonable(out["content"])
    return out


def _content_to_jsonable(content: Any) -> Any:
    if content is None or isinstance(content, str):
        return content
    if isinstance(content, list):
        return [_content_item_to_jsonable(item) for item in content]
    return _content_item_to_jsonable(content)


def _content_item_to_jsonable(item: Any) -> Any:
    to_storage = getattr(item, "to_storage_dict", None)
    if callable(to_storage):
        return to_storage()
    if isinstance(item, dict):
        return _sanitize_content_dict(item)
    return item


def _sanitize_content_dict(block: dict[str, Any]) -> dict[str, Any]:
    import base64

    out: dict[str, Any] = {}
    for key, value in block.items():
        if isinstance(value, bytes):
            if key == "signature":
                out[key] = base64.b64encode(value).decode("ascii")
                out.setdefault("signature_encoding", "base64")
            else:
                out[f"{key}__b64"] = base64.b64encode(value).decode("ascii")
            continue
        if isinstance(value, dict):
            out[key] = _sanitize_content_dict(value)
        elif isinstance(value, list):
            out[key] = [_content_item_to_jsonable(entry) for entry in value]
        else:
            out[key] = value
    return out


def _extract_usage(raw: Any) -> AiUsage:
    if raw is None:
        return AiUsage()
    if isinstance(raw, AiUsage):
        return raw
    if isinstance(raw, dict):
        return AiUsage.model_validate(raw)
    # AggregatedUsage (CompletedRequest.total_usage) — the canonical shape.
    # NOTE: the attribute is ``total`` (UsageTotals) + ``by_model``; a prior
    # version of this function read a non-existent ``totals`` attribute, so
    # every workflow AI node reported all-zero usage/cost (found 2026-07-06
    # while building the node_cost live spend ticker).
    total = getattr(raw, "total", None)
    by_model = getattr(raw, "by_model", None)
    if total is not None and hasattr(total, "input_tokens"):
        models: dict[str, AiModelUsage] = {}
        if isinstance(by_model, dict):
            for name, summary in by_model.items():
                models[str(name)] = AiModelUsage(
                    input_tokens=int(getattr(summary, "input_tokens", 0) or 0),
                    output_tokens=int(getattr(summary, "output_tokens", 0) or 0),
                    total_tokens=int(getattr(summary, "total_tokens", 0) or 0),
                    # Canonical key: cost_usd (was "cost" — unified with the
                    # top-level AiUsage.cost_usd and the podcast aggregator).
                    cost_usd=float(getattr(summary, "cost", 0.0) or 0.0),
                    request_count=int(getattr(summary, "request_count", 0) or 0),
                    api=str(getattr(summary, "api", "") or ""),
                )
        return AiUsage(
            input_tokens=int(getattr(total, "input_tokens", 0) or 0),
            output_tokens=int(getattr(total, "output_tokens", 0) or 0),
            total_tokens=int(getattr(total, "total_tokens", 0) or 0),
            cost_usd=float(getattr(total, "total_cost", 0.0) or 0.0),
            models=models,
        )
    # Legacy fallback: flat usage-like objects.
    totals = getattr(raw, "totals", None)
    if totals is not None:
        return AiUsage(
            input_tokens=int(getattr(totals, "input_tokens", 0) or 0),
            output_tokens=int(getattr(totals, "output_tokens", 0) or 0),
            total_tokens=int(getattr(totals, "total_tokens", 0) or 0),
            cost_usd=float(getattr(totals, "cost_usd", 0.0) or 0.0),
        )
    return AiUsage(
        input_tokens=int(getattr(raw, "input_tokens", 0) or 0),
        output_tokens=int(getattr(raw, "output_tokens", 0) or 0),
        total_tokens=int(getattr(raw, "total_tokens", 0) or 0),
        cost_usd=float(getattr(raw, "cost_usd", 0.0) or 0.0),
    )
