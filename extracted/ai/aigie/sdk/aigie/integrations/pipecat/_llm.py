"""LLM span handlers for the Pipecat observer.

Module-level functions taking the observer as the first argument, rather than
methods on ``PipecatObserver`` — ``native_callback.py`` is close to the file-length
cap and absorbs several more tasks after this one. Accumulated response text and
the latest usage-metrics object live on the *span's own open state*
(``SpanEventHandler.get_state``), never on the observer or on ``_Boundary``: a
Pipecat pipeline runs each observer callback in its own asyncio task, so state
kept on ``self``/the boundary is a cross-task hazard, while span state is scoped
to the one run_id these handlers already coordinate through.
"""

from __future__ import annotations

import logging
import uuid
from typing import Any

from aigie.context_manager import merge_metadata
from aigie.integrations.pipecat import _frames
from aigie.tracing.llm_metadata import extract_prompt_content
from aigie.tracing.usage import llm_span_payload

logger = logging.getLogger(__name__)

_LLM_KEY = "llm"
_BASE_META = _frames._BASE_META


def on_llm_context(obs: Any, frame: Any) -> None:
    """Stash the context's messages for the llm span ``on_llm_start`` opens next.

    ``LLMContextFrame`` is what triggers the LLM service to run, so it can
    (and in practice does) arrive before ``LLMFullResponseStartFrame`` — there
    is no open llm span yet to attach to, hence stash-then-consume on the
    boundary rather than on span state. Overwritten, not appended: only the
    most recent context is ever relevant to the call it precedes, and per-hop
    redelivery of the identical frame is already filtered by the observer's
    `_is_duplicate_frame` before this handler ever runs.
    """
    boundary = obs._boundary
    if boundary is None:
        return
    context = getattr(frame, "context", None)
    get_messages = getattr(context, "get_messages", None)
    if not callable(get_messages):
        return
    boundary.pending_llm_context = list(get_messages())


def _consume_llm_prompt_input(obs: Any, boundary: Any) -> dict[str, Any] | None:
    """Pop the stashed context and shape it into the llm span's ``input``.

    Always pops, even when ``capture_inputs`` is off, so a stash never
    outlives the call it belongs to and bleeds into a later one.
    """
    messages = boundary.pending_llm_context
    boundary.pending_llm_context = None
    if messages is None or not obs._flag("capture_inputs"):
        return None
    system_prompt, message_dicts = extract_prompt_content(messages)
    limit = obs._limit()
    llm_input: dict[str, Any] = {
        "prompts": [
            {**message, "content": _frames.truncate(message.get("content"), limit)}
            for message in message_dicts
        ],
        "prompt_count": len(message_dicts),
    }
    if system_prompt:
        llm_input["system_prompt"] = _frames.truncate(system_prompt, limit)
    return llm_input


def on_llm_start(obs: Any, frame: Any) -> None:
    boundary = obs._boundary
    if boundary is None or not obs._flag("trace_llm_calls"):
        return
    if _LLM_KEY in boundary.open_spans:
        return  # genuinely still open, no end frame yet; never orphan a span
    del frame  # start frame carries nothing we need for the run_id
    # A finished call's run_id can now outlive the frame it was minted from —
    # it lingers on `pending_llm` until usage arrives or a fallback flushes it
    # — so `id(frame)` is no longer safe here: CPython can and does reuse a
    # freed object's id, which would collide with a still-pending run_id and
    # silently merge two calls' spans into one. A uuid can't collide.
    run_id = f"llm:{boundary.trace_id}:{uuid.uuid4().hex}"
    boundary.open_spans[_LLM_KEY] = run_id
    input_value = _consume_llm_prompt_input(obs, boundary)
    obs.spans.open_span(
        run_id=run_id,
        parent_run_id=obs.turn_run_id or obs.CONVERSATION_RUN_ID,
        name="llm",
        span_type="llm",
        input=input_value,
        metadata=merge_metadata(_BASE_META),
    )
    state = obs.spans.get_state(run_id)
    if state is not None:
        state["_text_parts"] = []
        state["_usage_data"] = None


def on_llm_text(obs: Any, frame: Any) -> None:
    boundary = obs._boundary
    if boundary is None:
        return
    run_id = boundary.open_spans.get(_LLM_KEY)
    state = obs.spans.get_state(run_id) if run_id else None
    if state is None:
        return
    text = getattr(frame, "text", None)
    if text:
        state.setdefault("_text_parts", []).append(text)


def on_metrics(obs: Any, frame: Any) -> None:
    boundary = obs._boundary
    if boundary is None:
        return
    for item in getattr(frame, "data", None) or []:
        if type(item).__name__ == "LLMUsageMetricsData":
            _attach_llm_usage(obs, boundary, item)


def _attach_llm_usage(obs: Any, boundary: Any, usage_data: Any) -> None:
    """Route one ``LLMUsageMetricsData`` item to the call it prices.

    A still-open call (its end frame hasn't arrived yet) is favored first —
    that is a provider reporting usage ahead of the end frame. Otherwise this
    is the real Bedrock/Anthropic case: usage for an already-ended call
    arriving late, possibly after the NEXT call's ``LLMFullResponseStartFrame``
    has already opened a new active span (see ``on_llm_start``/``on_llm_end``)
    — matched FIFO against ``pending_llm``, since a single LLM processor
    resolves its own calls, and therefore emits their usage, in call order
    even when that usage lags behind other frames on shared queues.
    """
    active_run_id = boundary.open_spans.get(_LLM_KEY)
    active_state = obs.spans.get_state(active_run_id) if active_run_id else None
    if active_state is not None:
        active_state["_usage_data"] = usage_data
        return
    if not boundary.pending_llm:
        return
    run_id = boundary.pending_llm.pop(0)
    state = obs.spans.get_state(run_id)
    if state is None:
        return
    state["_usage_data"] = usage_data
    # The status was already decided in on_llm_end, at the moment the end
    # frame arrived — never re-read boundary.interrupted here, it may since
    # have been cleared (or re-armed by an unrelated later barge-in).
    _close_llm_span(obs, boundary, run_id, state, status=state.get("_status", "success"))


def on_llm_end(obs: Any, frame: Any) -> None:
    del frame  # end frame itself carries nothing we need; the span state does
    boundary = obs._boundary
    if boundary is None:
        return
    run_id = boundary.open_spans.pop(_LLM_KEY, None)
    if run_id is None:
        return
    state = obs.spans.get_state(run_id)
    if state is None:
        return
    # Pipecat still pushes this end frame after a barge-in — without checking
    # the flag, a response the user talked over closes exactly like one that
    # finished on its own.
    status = "interrupted" if boundary.interrupted else "success"
    state["_status"] = status
    if state.get("_usage_data") is not None:
        # Usage already arrived (a provider that reports it ahead of the end
        # frame) — close now, nothing left to wait for.
        _close_llm_span(obs, boundary, run_id, state, status=status)
        _frames.clear_interrupted_if_settled(boundary)
        return
    # Frames cross per-processor asyncio queues: push order upstream is NOT the
    # order this observer sees them in. With real Bedrock (and Anthropic), the
    # MetricsFrame carrying LLMUsageMetricsData — the model and token counts —
    # arrives AFTER this end frame, and possibly after the NEXT call's start
    # frame too (a multi-turn exchange starts call 2 before call 1's usage has
    # surfaced). Closing here unconditionally is the bug: SpanEventHandler.
    # close_span emits immediately and can't be patched later, so an early
    # close ships an unpriceable span. Instead, park the run_id on
    # ``pending_llm`` (freeing ``_LLM_KEY`` so the next call can open its own
    # active span) and mark it awaiting usage; ``_attach_llm_usage`` closes it
    # once usage lands, and ``flush_pending_llm`` guarantees a fallback close
    # — as success unless this call was itself interrupted — if usage never comes.
    state["_awaiting_usage"] = True
    boundary.pending_llm.append(run_id)
    _frames.clear_interrupted_if_settled(boundary)


def flush_pending_llm(obs: Any) -> None:
    """Fallback-close every ``llm`` span still waiting for its usage MetricsFrame.

    Must be called at every point such a span could otherwise outlive its
    reason for existing: turn end, the conversation drain, and ``cleanup()``.
    Status comes from what ``on_llm_end`` already decided (``state["_status"]``)
    — success unless that particular call was itself interrupted; "interrupted"
    otherwise stays reserved for a span reached by draining something that
    genuinely never finished, e.g. no end frame at all.
    """
    boundary = obs._boundary
    if boundary is None:
        return
    while boundary.pending_llm:
        run_id = boundary.pending_llm.pop(0)
        state = obs.spans.get_state(run_id)
        if state is not None:
            _close_llm_span(obs, boundary, run_id, state, status=state.get("_status", "success"))


def _close_llm_span(
    obs: Any, boundary: Any, run_id: str, state: dict[str, Any], *, status: str
) -> None:
    text = "".join(state.get("_text_parts", []))
    usage_data = state.get("_usage_data")
    model = getattr(usage_data, "model", None) if usage_data is not None else None
    provider = (
        _frames.provider_for(getattr(usage_data, "processor", ""))
        if usage_data is not None
        else None
    )
    usage = _frames.usage_mapping(usage_data) if usage_data is not None else None
    extras, usage_md = llm_span_payload(usage, model_id=model)
    metadata_updates = {**usage_md, "provider": provider} if provider else (usage_md or None)
    output = _frames.truncate(text, obs._limit()) if obs._flag("capture_outputs") else None
    obs.spans.close_span(
        run_id=run_id,
        output=output,
        extras=extras or None,
        metadata_updates=metadata_updates,
        status=status,
    )
    if output:
        boundary.root.note_output(output)


def _tool_key(tool_call_id: Any) -> str | None:
    """Key on ``tool_call_id``, never ``function_name`` — parallel calls to the
    same function share a function_name, so name-keying would close the wrong
    span when they resolve out of order.
    """
    return f"tool:{tool_call_id}" if tool_call_id is not None else None


def on_function_call_started(obs: Any, frame: Any) -> None:
    boundary = obs._boundary
    if boundary is None or not obs._flag("trace_tools"):
        return
    tool_call_id = getattr(frame, "tool_call_id", None)
    key = _tool_key(tool_call_id)
    if key is None or key in boundary.open_spans:
        return  # no tool_call_id to key on, or a duplicate start; never orphan
    run_id = f"tool:{boundary.trace_id}:{tool_call_id}"
    boundary.open_spans[key] = run_id
    arguments = getattr(frame, "arguments", None)
    input_value = _frames.truncate(arguments, obs._limit()) if obs._flag("capture_inputs") else None
    parent_run_id = boundary.open_spans.get(_LLM_KEY) or obs.turn_run_id or obs.CONVERSATION_RUN_ID
    obs.spans.open_span(
        run_id=run_id,
        parent_run_id=parent_run_id,
        name=getattr(frame, "function_name", None) or "tool",
        span_type="tool",
        input=input_value,
        metadata=merge_metadata(_BASE_META, {"tool_call_id": tool_call_id}),
    )


def on_function_call_result(obs: Any, frame: Any) -> None:
    boundary = obs._boundary
    if boundary is None:
        return
    key = _tool_key(getattr(frame, "tool_call_id", None))
    run_id = boundary.open_spans.pop(key, None) if key else None
    if run_id is None:
        return
    result = getattr(frame, "result", None)
    output = _frames.truncate(result, obs._limit()) if obs._flag("capture_outputs") else None
    obs.spans.close_span(run_id=run_id, output=output)


def on_function_call_cancel(obs: Any, frame: Any) -> None:
    boundary = obs._boundary
    if boundary is None:
        return
    key = _tool_key(getattr(frame, "tool_call_id", None))
    run_id = boundary.open_spans.pop(key, None) if key else None
    if run_id is None:
        return
    # A cancel is neither a success nor an error — "interrupted" matches the
    # status already used for spans abandoned by a conversation ending mid-flight.
    obs.spans.close_span(run_id=run_id, output=None, status="interrupted")


def _innermost_child_run_id(boundary: Any) -> str | None:
    """Resolve the innermost open child span: tool, then llm, then turn.

    The conversation (root) itself is deliberately excluded here — a caller
    that gets None back is responsible for finalizing the conversation, which
    needs its own drain/ambient/claim teardown, not a bare fail_span.

    Tool keys are scanned in reverse insertion order: with parallel calls the
    most recently opened one is the "innermost" — the oldest one (dict
    insertion order) is not necessarily the one an error is attributable to.
    """
    key: str
    run_id: str
    for key, run_id in reversed(list(boundary.open_spans.items())):
        if key.startswith("tool:"):
            return run_id
    llm_run_id: str | None = boundary.open_spans.get(_LLM_KEY)
    if llm_run_id is not None:
        return llm_run_id
    turn_run_id: str | None = boundary.turn_run_id
    return turn_run_id


def _forget_run_id(boundary: Any, run_id: str) -> None:
    for key, value in list(boundary.open_spans.items()):
        if value == run_id:
            del boundary.open_spans[key]
    if boundary.turn_run_id == run_id:
        boundary.turn_run_id = None


def on_error(obs: Any, frame: Any) -> None:
    """Fail the innermost open child span, then finalize the conversation
    only when the error is fatal.

    ``fail_span`` emits a payload; that emission is not isolated, and a raise
    there must not skip ``_fail_conversation`` for a fatal error — that call
    is what releases the thread-keyed provider-span claim and drains the rest
    of the boundary. Hence the try/finally, rather than sequential calls.

    A non-fatal error with nothing open (no tool/llm/turn) has no span to
    fail; it must NOT fall through to tearing down the conversation — an
    otherwise-recoverable blip between turns would silently end the trace.
    """
    boundary = obs._boundary
    if boundary is None:
        return
    error = _frames.error_from_frame(frame)
    fatal = bool(getattr(frame, "fatal", False))
    run_id = _innermost_child_run_id(boundary)
    try:
        if run_id is not None:
            obs.spans.fail_span(run_id=run_id, error=error)
            _forget_run_id(boundary, run_id)
        elif not fatal:
            logger.debug("pipecat: non-fatal error with no open span to fail: %s", error)
    finally:
        if fatal:
            obs._fail_conversation(error)
