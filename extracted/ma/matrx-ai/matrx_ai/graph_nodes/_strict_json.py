"""Funnel wrappers for graph_nodes / graph_actions LLM calls.

Two public primitives, both routed through ``execute_ai_request`` — the
single canonical matrx-ai execution funnel that owns sampling-param policy
per ``api_class`` (so adaptive-sampling Claude models never 400 on a
``temperature``), cost tracking, and streaming into the workflow heartbeat.
**Never talk to a provider SDK directly from a graph action** — reach for
one of these.

- ``llm_to_pydantic`` — strict-JSON text call with one-retry fallback; the model
  is prompted with the JSON schema and the response is validated by Pydantic.
  Optional ``on_delta`` streams the first attempt's answer tokens to the caller
  (additive display — validation/persistence unchanged); optional ``wire_kind``
  tags the wire payload with a leading ``__kind`` const (added to the enforced
  schema; reduced through the ingestion shim before validation, so an output
  class that declares the marker KEEPS it) so canonical clients can mount the right
  kind component while the JSON is still streaming.
- ``llm_messages_to_pydantic`` — the same contract over provider-neutral,
  potentially multimodal or multi-turn messages.
- ``llm_to_text`` — free-text call (no schema): one shot, returns the
  assistant's text. Use when the node wants prose, not structured output.
- ``llm_stream_text`` — free-text call with per-token deltas: same as
  ``llm_to_text`` but invokes ``on_delta(text)`` as each token arrives, so the
  caller can emit its OWN typed stream event (or drive an incremental parser)
  without ever touching a provider SDK.

All primitives share the same underlying runner (``_run_completion``) so
the funnel routing, streaming, and drain-fallback behavior is identical.

🚨 The strict-JSON primitives SUPPRESS the token stream by default. That is
correct for an internal call and WRONG for a workflow node, whose live panel
then shows a loader for the whole call. A node call site passes the hooks from
``node_panel_hooks(ctx.app.emitter)`` so its tokens reach the same panel every
``ai.agent.start`` step already streams into.

Public-ish: imported by sibling graph_nodes modules in matrx-ai AND by host
applications' graph_actions modules (e.g. aidream/graph_actions/). Keep the
signatures stable.
"""

from __future__ import annotations

import asyncio
import contextlib
import logging
from collections.abc import Awaitable, Callable
from typing import Any, TypeVar

from pydantic import BaseModel, ValidationError

from matrx_ai.orchestrator.step_phase import emit_step_phase

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseModel)


class StrictJsonError(Exception):
    """Raised when an LLM cannot produce JSON that validates against the schema.

    ``raw_output`` carries the full, PAID model text that failed to parse —
    the latest non-empty attempt (retry over first). Consumers that catch
    this error own the decision to persist it durably; the attribute exists
    so the raw output is never reduced to whatever fragment fits in the
    exception message.
    """

    def __init__(self, message: str, *, raw_output: str = "") -> None:
        super().__init__(message)
        self.raw_output = raw_output


# Stop reasons that indicate the model ran out of room to finish — every
# provider uses slightly different terminology. Anthropic / xAI use
# ``max_tokens``, OpenAI / Groq use ``length``, Cohere uses
# ``MAX_TOKENS``. Normalize aggressively.
_TRUNCATION_REASONS: frozenset[str] = frozenset(
    {"max_tokens", "length", "MAX_TOKENS", "max_completion_tokens"}
)


class StrictJsonTruncatedError(StrictJsonError):
    """Raised when an LLM hit its token cap mid-output.

    Distinct from a parse failure: the model didn't produce broken JSON,
    it produced *incomplete* JSON. The fix is structural (bigger
    ``max_tokens`` / smaller schema / chunked input), not retry.
    """


async def _run_completion(
    messages: list[dict[str, Any]],
    system_text: str,
    *,
    model: str,
    max_tokens: int,
    temperature: float | None = None,
    response_format: str | dict[str, Any] | None = None,
    internal_web_search: bool = False,
    metadata: dict[str, Any] | None = None,
    store: bool | None = None,
    conversation_id: str | None = None,
) -> tuple[str, str | None]:
    """One turn through the matrx-ai funnel. Returns ``(text, finish_reason)``.

    Streaming is enabled deliberately:
    1. Anthropic rejects non-streaming requests with ``max_tokens > ~8K``
       (their 10-minute completion-time SLA). Streaming lifts this to the
       model's full output cap.
    2. Chunks flow through the emitter as ``send_chunk`` calls, which the
       workflow's ProgressTrackingEmitter captures into the heartbeat — so
       the user sees live progress during generation.

    ``temperature`` is passed straight through when not ``None``; the funnel
    (``resolve_call_profile`` → the provider translator) strips it for
    adaptive-sampling api_classes and keeps it for standard ones. Callers
    NEVER branch on the model name.

    ``response_format`` is ``'json'`` / ``'text'`` / ``None`` — provider-enforced
    JSON mode when supported.
    """
    from matrx_ai.config import UnifiedConfig
    from matrx_ai.graph_nodes.shared import normalize_completed
    from matrx_ai.orchestrator.executor import execute_ai_request

    cfg: dict[str, Any] = {
        "model": model,
        "messages": messages,
        "system_instruction": system_text,
        "max_tokens": max_tokens,
        "stream": True,
    }
    if temperature is not None:
        cfg["temperature"] = temperature
    if response_format == "json":
        cfg["response_format"] = {"type": "json_object"}
    elif response_format == "text":
        cfg["response_format"] = {"type": "text"}
    elif isinstance(response_format, dict):
        cfg["response_format"] = response_format
    if internal_web_search:
        cfg["internal_web_search"] = True
    config = UnifiedConfig.from_dict(cfg)
    completed = await execute_ai_request(
        config,
        max_iterations=1,
        max_retries_per_iteration=2,
        metadata=metadata or None,
        store=store,
        conversation_id=conversation_id,
    )
    result = normalize_completed(completed)
    text = result.final_text or ""

    # When streaming, ``CompletedRequest.final_response`` is sometimes not
    # populated with the accumulated text — chunks fired through the emitter
    # and the orchestrator's response object lags behind. If our emitter
    # exposes ``drain_full_text`` (every active workflow uses
    # ``ProgressTrackingEmitter`` which does), pull the accumulated stream
    # from there as the authoritative source.
    if not text:
        from matrx_connect.context.app_context import try_get_app_context

        ctx = try_get_app_context()
        emitter = getattr(ctx, "emitter", None) if ctx is not None else None
        # EventRecordingEmitter wraps ProgressTrackingEmitter — peel one layer.
        base = getattr(emitter, "_base", emitter)
        drain = getattr(base, "drain_full_text", None)
        if callable(drain):
            drained = drain()
            if drained:
                text = drained
    return text, result.finish_reason


async def llm_to_text(
    *,
    model: str,
    system: str,
    user: str,
    max_tokens: int = 8092,
    temperature: float | None = None,
    metadata: dict[str, Any] | None = None,
    store: bool | None = None,
    conversation_id: str | None = None,
) -> str:
    """Free-text LLM call through the matrx-ai funnel — one shot, no schema.

    The single-turn twin of :func:`llm_to_pydantic` for nodes that want prose
    instead of structured output. Routes through ``execute_ai_request`` so the
    sampling-param policy (``temperature`` stripped for adaptive api_classes),
    cost tracking, and heartbeat streaming are identical. Returns the
    assistant's text (empty string if the model produced none).
    """
    text, _finish = await _run_completion(
        [{"role": "user", "content": user}],
        system,
        model=model,
        max_tokens=max_tokens,
        temperature=temperature,
        metadata=metadata,
        store=store,
        conversation_id=conversation_id,
    )
    return text


# ---------------------------------------------------------------------------
# Live-panel hooks — the ONE way a graph node narrates a strict-JSON call
# ---------------------------------------------------------------------------


def node_panel_hooks(
    emitter: Any,
) -> tuple[Callable[[str], Awaitable[None]], Callable[[], Awaitable[None]]]:
    """Return the ``(on_delta, on_reset)`` pair that streams a strict-JSON
    call's tokens into the workflow node's live panel.

    Why this exists
    ---------------
    ``_run_completion`` promises "chunks flow through the emitter ... so the
    user sees live progress during generation", and that is true for
    :func:`llm_to_text`. It is NOT true for :func:`llm_to_pydantic` /
    :func:`llm_messages_to_pydantic`: those route through
    ``_wrapped_completion``, which interposes :class:`_DeltaEmitter`, and that
    wrapper **never forwards ``send_chunk``** — ``on_delta=None`` means
    "suppress entirely". Suppression is the correct default for an internal
    call (a judge, a classifier, a caption must not spray raw JSON into a
    user's chat), but a WORKFLOW NODE is the opposite case: its live panel is
    a diagnostic surface whose whole job is to show that work is happening.

    Measured 2026-08-18 on Study Pack v1: ``docproc.content.structure`` ran
    **72 seconds with ``chars_streamed: 0``** — the single longest stretch of
    the run — while its four sibling ``ai.agent.start`` steps streamed
    normally. That silence is the "nothing happens but a loader, then
    INSTANTLY a giant json" the user reported. The tokens were always there;
    the wrapper ate them.

    Contract
    --------
    * ``on_delta`` forwards answer text to ``emitter.send_chunk`` — the same
      channel every agent node already uses, so one panel renders both.
      Reasoning spans are NOT routed here: :class:`_DeltaEmitter` already
      splits them onto ``send_reasoning_chunk`` before ``on_delta`` sees them.
    * ``on_reset`` fires when the orchestrator replays a turn. It clears the
      emitter's server-side tail and announces the restart as a phase, so the
      panel says what happened instead of showing two half-answers
      concatenated — but ONLY when text was actually streamed first. The
      orchestrator calls ``reset_turn_text()`` at the START of every attempt,
      including the first, so announcing unconditionally stamps
      ``last_phase: "restarted"`` on a completely normal run and leaves it
      there for the whole node (measured in the browser, 2026-08-18). A reset
      with nothing streamed is turn setup, not a restart.
    * Every call is best-effort: narration must never break the node it
      narrates, so both hooks swallow (and log) their own failures.

    Pass the node's emitter (``ctx.app.emitter``); a node with no emitter
    passes ``None`` and gets inert hooks.
    """

    streamed_any = False

    async def on_delta(text: str) -> None:
        nonlocal streamed_any
        if not text or emitter is None:
            return
        send_chunk = getattr(emitter, "send_chunk", None)
        if send_chunk is None:
            return
        try:
            await send_chunk(text)
            streamed_any = True
        except Exception:  # noqa: BLE001 — narration never breaks the node
            logger.warning("node live-panel delta failed; generation continues", exc_info=True)

    async def on_reset() -> None:
        nonlocal streamed_any
        # Turn setup, not a restart — nothing was shown, so there is nothing
        # to retract and nothing to tell the user about.
        if emitter is None or not streamed_any:
            return
        streamed_any = False
        try:
            reset = getattr(emitter, "reset_turn_text", None)
            if reset is not None:
                reset()
            send_phase = getattr(emitter, "send_phase", None)
            if send_phase is not None:
                await send_phase("restarted — discarding the partial answer")
        except Exception:  # noqa: BLE001 — narration never breaks the node
            logger.warning("node live-panel reset failed; generation continues", exc_info=True)

    return on_delta, on_reset


# Anthropic streams a thinking model's chain-of-thought through ``send_chunk``
# — NOT through ``send_reasoning_chunk`` — wrapped in these markers
# (``anthropic_api.py``: ``send_chunk("\n<reasoning>\n")`` … ``send_chunk(thinking)``
# … ``send_chunk("\n</reasoning>\n")``). Reasoning is not answer text, so the
# wrapper below has to recognize the markers and split the stream itself.
_REASONING_OPEN = "<reasoning>"
_REASONING_CLOSE = "</reasoning>"


class _DeltaEmitter:
    """Emitter wrapper that captures a funnel call's answer tokens.

    Every provider reads ``get_app_context().emitter`` at call time (e.g.
    ``anthropic_api.py``: ``emitter = get_app_context().emitter``), so installing
    this on the context for the duration of one funnel call gives the caller
    per-token access — no provider SDK, no orchestrator surgery.

    **``send_chunk`` is never forwarded to the wrapped emitter.** That is the
    whole safety property: an INTERNAL call (a grounding judge, a classifier, a
    caption) must not spray the model's raw output into the user's chat, and a
    caller emitting its own typed event must not ALSO emit raw ``chunk`` events.
    ``on_delta=None`` means "suppress entirely" — the correct default for an
    internal call. Everything else (``send_data`` / ``send_end`` / ``send_error``
    / phases / persistence hooks) passes through via ``__getattr__``, so cost,
    error, and disconnect paths are untouched.

    **Reasoning is split out, not merely documented away.** A thinking model's
    chain-of-thought arrives on the SAME ``send_chunk`` channel, fenced by
    ``<reasoning>`` … ``</reasoning>``. This class tracks that fence and routes
    those spans to the wrapped emitter's reasoning channel, so they never reach
    ``on_delta``, never land in the returned answer, and never corrupt a caller's
    incremental JSON parser.

    **A provider retry replays the turn.** The orchestrator calls
    ``reset_turn_text()`` before each retry attempt; ``on_delta`` has by then
    already fired for the aborted attempt's tokens. We surface that as
    ``on_reset()`` so the caller can tell its client to discard what it showed —
    silently dropping it would leave a duplicated, garbled answer on screen.

    The wrapped emitter is held as ``_inner`` — NOT ``_base`` — on purpose:
    ``_run_completion``'s empty-final-text fallback peels a ``_base`` attribute
    before calling ``drain_full_text``. Naming ours ``_inner`` means that peel
    finds nothing, so it drains THIS wrapper (which actually holds the tokens)
    instead of the wrapped emitter (which never saw them).
    """

    def __init__(
        self,
        inner: Any,
        on_delta: Callable[[str], Awaitable[None]] | None = None,
        on_reset: Callable[[], Awaitable[None]] | None = None,
    ) -> None:
        self._inner = inner
        self._on_delta = on_delta
        self._on_reset = on_reset
        self._parts: list[str] = []
        self._in_reasoning = False
        self._reset_tasks: set[asyncio.Task[None]] = set()

    async def _run_reset_notice(self) -> None:
        try:
            assert self._on_reset is not None
            await self._on_reset()
        except Exception as exc:
            from matrx_connect.streaming.error_capture import capture_error

            await capture_error(
                exc,
                kind="strict_json_reset_failed",
                route="graph_nodes/strict_json/reset",
                error_type=type(exc).__name__,
            )

    async def _answer(self, text: str) -> None:
        if not text:
            return
        self._parts.append(text)
        if self._on_delta is not None:
            await self._on_delta(text)

    async def _reasoning(self, text: str) -> None:
        if not text:
            return
        forward = getattr(self._inner, "send_reasoning_chunk", None)
        if forward is not None:
            await forward(text)

    async def send_chunk(self, text: str) -> None:
        """Split the chunk stream into answer spans and reasoning spans.

        The provider emits each ``<reasoning>`` / ``</reasoning>`` marker as its
        own ``send_chunk`` call, so a marker is never torn across chunks; we
        still scan defensively in case a future provider concatenates them with
        surrounding text.
        """
        remaining = text
        while remaining:
            if self._in_reasoning:
                close = remaining.find(_REASONING_CLOSE)
                if close == -1:
                    await self._reasoning(remaining)
                    return
                await self._reasoning(remaining[:close])
                remaining = remaining[close + len(_REASONING_CLOSE) :]
                self._in_reasoning = False
            else:
                opened = remaining.find(_REASONING_OPEN)
                if opened == -1:
                    await self._answer(remaining)
                    return
                await self._answer(remaining[:opened])
                remaining = remaining[opened + len(_REASONING_OPEN) :]
                self._in_reasoning = True

    async def send_reasoning_chunk(self, text: str) -> None:
        await self._reasoning(text)

    def reset_turn_text(self) -> None:
        """The orchestrator is about to retry — everything we streamed is void."""
        self._parts.clear()
        self._in_reasoning = False
        if self._on_reset is not None:
            # Sync method on the Emitter protocol; schedule the async notice.
            with contextlib.suppress(RuntimeError):
                task = asyncio.get_running_loop().create_task(self._run_reset_notice())
                self._reset_tasks.add(task)
                task.add_done_callback(self._reset_tasks.discard)

    def get_turn_text(self) -> str:
        return "".join(self._parts)

    def drain_full_text(self) -> str:
        return "".join(self._parts)

    def __getattr__(self, name: str) -> Any:
        # Only reached for attributes not defined above. Guard the private
        # names so a lookup during __init__ can't recurse into _inner.
        if name.startswith("_"):
            raise AttributeError(name)
        return getattr(self._inner, name)


async def _wrapped_completion(
    *,
    model: str,
    system: str,
    messages: list[dict[str, Any]],
    on_delta: Callable[[str], Awaitable[None]] | None,
    on_reset: Callable[[], Awaitable[None]] | None,
    max_tokens: int,
    temperature: float | None,
    response_format: str | dict[str, Any] | None,
    internal_web_search: bool,
    api_keys: dict[str, str] | None,
    system_run: bool | None,
    metadata: dict[str, Any] | None,
    store: bool | None,
    conversation_id: str | None,
) -> tuple[str, str | None]:
    """Run one funnel turn while suppressing or redirecting answer chunks.

    The optional key overlay is request-scoped and restored without reverting
    conversation/store mutations made by the executor during the call.
    """
    from matrx_connect.context.app_context import (
        get_app_context,
        set_app_context,
        try_get_app_context,
    )

    ctx = get_app_context()
    wrapper = _DeltaEmitter(ctx.emitter, on_delta, on_reset)
    merged_keys = dict(ctx.api_keys or {})
    if api_keys:
        merged_keys.update({key: value for key, value in api_keys.items() if value})
    overrides: dict[str, Any] = {"emitter": wrapper, "api_keys": merged_keys}
    if system_run is not None:
        overrides["system_run"] = system_run
    set_app_context(ctx.with_overrides(**overrides))
    try:
        text, finish = await _run_completion(
            messages,
            system,
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            response_format=response_format,
            internal_web_search=internal_web_search,
            metadata=metadata,
            store=store,
            conversation_id=conversation_id,
        )
        return text or wrapper.get_turn_text(), finish
    finally:
        # Restore only fields this wrapper owns. The executor may have resolved
        # conversation identity or persistence policy while the call ran.
        current = try_get_app_context() or ctx
        set_app_context(
            current.with_overrides(
                emitter=ctx.emitter,
                api_keys=dict(ctx.api_keys or {}),
                system_run=ctx.system_run,
            )
        )


async def llm_stream_messages(
    *,
    model: str,
    system: str,
    messages: list[dict[str, Any]],
    on_delta: Callable[[str], Awaitable[None]] | None = None,
    on_reset: Callable[[], Awaitable[None]] | None = None,
    max_tokens: int = 8092,
    temperature: float | None = None,
    response_format: str | dict[str, Any] | None = None,
    internal_web_search: bool = False,
    api_keys: dict[str, str] | None = None,
    system_run: bool | None = None,
    metadata: dict[str, Any] | None = None,
    store: bool | None = None,
    conversation_id: str | None = None,
) -> str:
    """Funnel call over pre-built provider-neutral messages, with the emitter WRAPPED.

    This is the lowest-level of the three primitives and the one to reach for
    when the call is **multimodal** (image parts) or **multi-turn** — the other
    two build on it.

    ``on_delta`` fires per answer-token. **``on_delta=None`` SUPPRESSES the token
    stream entirely**, which is what an internal call wants: without the wrapper,
    the funnel streams every token to whatever emitter is on the context, i.e.
    straight into the end user's chat bubble.

    ``on_reset`` fires if the orchestrator retries the turn after a partial
    stream — the caller should tell its client to discard what it already showed.
    """
    text, _finish = await _wrapped_completion(
        model=model,
        system=system,
        messages=messages,
        on_delta=on_delta,
        on_reset=on_reset,
        max_tokens=max_tokens,
        temperature=temperature,
        response_format=response_format,
        internal_web_search=internal_web_search,
        api_keys=api_keys,
        system_run=system_run,
        metadata=metadata,
        store=store,
        conversation_id=conversation_id,
    )
    return text


async def llm_stream_text(
    *,
    model: str,
    system: str,
    user: str,
    on_delta: Callable[[str], Awaitable[None]] | None = None,
    on_reset: Callable[[], Awaitable[None]] | None = None,
    max_tokens: int = 8092,
    temperature: float | None = None,
    response_format: str | None = None,
    metadata: dict[str, Any] | None = None,
    store: bool | None = None,
    conversation_id: str | None = None,
) -> str:
    """Free-text funnel call that hands the caller every token as it arrives.

    ``on_delta(text)`` fires per answer-token; the full assistant text is
    returned. Use this instead of a provider SDK whenever a caller needs to
    stream a model's output as its OWN typed event (e.g. a per-chunk RAG synth
    event) or to drive an incremental parser (e.g. per-claim judge verdicts).
    ``on_delta=None`` suppresses the token stream (internal call).

    Thin wrapper over :func:`llm_stream_messages` for the single-user-turn,
    text-only case.
    """
    return await llm_stream_messages(
        model=model,
        system=system,
        messages=[{"role": "user", "content": user}],
        on_delta=on_delta,
        on_reset=on_reset,
        max_tokens=max_tokens,
        temperature=temperature,
        response_format=response_format,
        metadata=metadata,
        store=store,
        conversation_id=conversation_id,
    )


async def llm_messages_to_pydantic(
    *,
    model: str,
    system: str,
    messages: list[dict[str, Any]],
    output_cls: type[T],
    max_tokens: int = 8092,
    internal_web_search: bool = False,
    api_keys: dict[str, str] | None = None,
    system_run: bool | None = None,
    metadata: dict[str, Any] | None = None,
    store: bool | None = None,
    conversation_id: str | None = None,
    on_delta: Callable[[str], Awaitable[None]] | None = None,
    on_reset: Callable[[], Awaitable[None]] | None = None,
    wire_kind: str | None = None,
) -> T:
    """Validate structured output from multimodal or multi-turn messages.

    Calls the canonical execution funnel with provider-native JSON Schema
    enforcement where supported. Internal answer chunks are suppressed unless
    ``on_delta`` is given. A parse failure gets one repair turn that retains
    the entire original message list, including image/document content.

    ``on_delta`` fires per answer-token of the FIRST attempt only, so a caller
    can stream the structured output live (e.g. as raw chunks a canonical
    client accumulator parses). The repair retry is deliberately NOT streamed:
    the client already saw the first attempt's bytes, and appending a second
    JSON object would corrupt whatever it rendered — the validated result
    still arrives via the caller's own completion event. ``on_reset`` covers
    provider-level retries inside the streamed attempt (see ``_DeltaEmitter``).

    ``wire_kind`` tags the streamed payload for canonical kind resolution: the
    provider-enforced schema gains a REQUIRED ``__kind`` const as its first
    property (providers that enforce the schema natively would otherwise
    forbid the model from emitting it) and the model is told to emit it first,
    so a live client can mount the right component while tokens are still
    arriving. The key is stripped before Pydantic validation — ``output_cls``
    never sees it, so ``extra="forbid"`` models stay valid and the persisted
    shape is unchanged.
    """
    schema = output_cls.model_json_schema()
    kind_rule = ""
    if wire_kind:
        schema = {
            **schema,
            "properties": {
                "__kind": {"type": "string", "enum": [wire_kind]},
                **(schema.get("properties") or {}),
            },
            "required": ["__kind", *(schema.get("required") or [])],
        }
        kind_rule = f'\nThe object MUST begin with "__kind": "{wire_kind}" as its first key.'
    structured_system = (
        f"{system.rstrip()}\n\n"
        "Return ONLY a JSON object matching this schema, with no prose or fences:"
        f"{kind_rule}\n"
        f"{schema}"
    )
    response_format = {
        "type": "json_schema",
        "json_schema": {
            "name": output_cls.__name__,
            "schema": schema,
            "strict": True,
        },
    }

    async def _run(
        run_messages: list[dict[str, Any]], *, allow_web_search: bool, stream: bool = False
    ) -> tuple[str, str | None]:
        return await _wrapped_completion(
            model=model,
            system=structured_system,
            messages=run_messages,
            on_delta=on_delta if stream else None,
            on_reset=on_reset if stream else None,
            max_tokens=max_tokens,
            temperature=None,
            response_format=response_format,
            internal_web_search=allow_web_search,
            api_keys=api_keys,
            system_run=system_run,
            metadata=metadata,
            store=store,
            conversation_id=conversation_id,
        )

    def _validate(raw_text: str) -> T:
        cleaned = strip_json_fences(raw_text)
        if wire_kind:
            # THE INGESTION SHIM, not a strip (KINDS_EVERYWHERE_PLAN §4.2). The
            # marker is DATA; it is dropped ONLY where `output_cls` would fatally
            # reject it — a closed pre-kinds model that does not declare it. An
            # output class that DOES declare `__kind` (any KindModel) keeps it
            # and returns a self-identifying value. This used to be an
            # unconditional `obj.pop("__kind")`, which deleted the identity even
            # from the models built to carry it.
            import json

            from matrx_graph.content_ir.markers import reduce_for_ingestion

            try:
                obj = json.loads(cleaned)
            except ValueError:
                obj = None
            if isinstance(obj, dict):
                obj = reduce_for_ingestion(obj, output_cls.model_json_schema())
                return output_cls.model_validate(obj, strict=False)
        return output_cls.model_validate_json(cleaned, strict=False)

    raw_first, finish_first = await _run(
        messages, allow_web_search=internal_web_search, stream=True
    )
    if finish_first and finish_first in _TRUNCATION_REASONS:
        raise StrictJsonTruncatedError(
            f"Model {model} hit token cap (finish_reason={finish_first!r}, "
            f"max_tokens={max_tokens}) while producing {output_cls.__name__}. "
            "Increase max_tokens, simplify the schema, or chunk the input.",
            raw_output=raw_first,
        )

    # THE ``finalizing`` MOMENT (SPEC §5.1) — this is the second of the two
    # structured-output funnels (the first is the orchestrator's
    # ``_emit_structured_output_if_schema``). Both announce it, neither node
    # authors it.
    await emit_step_phase("finalizing")
    try:
        return _validate(raw_first)
    except ValidationError as first_err:
        retry_messages = [*messages]
        if raw_first:
            retry_messages.append({"role": "assistant", "content": raw_first})
        retry_messages.append(
            {
                "role": "user",
                "content": (
                    "Your previous response did not validate against the required schema. "
                    f"Validation error:\n{first_err}\n\n"
                    "Return corrected JSON only. Preserve your substantive verdict."
                ),
            }
        )
        # A format-repair turn has the first turn's facts in its transcript; do
        # not spend on a second hosted search merely to repair JSON syntax.
        raw_second, finish_second = await _run(retry_messages, allow_web_search=False)
        if finish_second and finish_second in _TRUNCATION_REASONS:
            raise StrictJsonTruncatedError(
                f"Retry of {output_cls.__name__} also hit token cap "
                f"(finish_reason={finish_second!r}, max_tokens={max_tokens}). "
                "Increase max_tokens, simplify the schema, or chunk the input.",
                raw_output=raw_second or raw_first,
            ) from first_err
        try:
            return _validate(raw_second)
        except ValidationError as second_err:
            raise StrictJsonError(
                f"Model failed to produce valid {output_cls.__name__} after one retry. "
                f"First error: {first_err}\n"
                f"Retry error: {second_err}\n"
                f"Retry raw output: {raw_second!r}",
                raw_output=raw_second or raw_first,
            ) from second_err


async def llm_to_pydantic(
    *,
    model: str,
    system: str,
    user: str,
    output_cls: type[T],
    max_tokens: int = 8092,
    metadata: dict[str, Any] | None = None,
    store: bool | None = None,
    conversation_id: str | None = None,
    on_delta: Callable[[str], Awaitable[None]] | None = None,
    on_reset: Callable[[], Awaitable[None]] | None = None,
    wire_kind: str | None = None,
) -> T:
    """Call ``execute_ai_request`` and validate the response against ``output_cls``.

    The first call goes straight to the model. If parsing fails, a
    second call is made with the raw output + validation error embedded
    in the user prompt — this fixes most "model added prose around the
    JSON" failures without masking real schema drift.

    Special handling for truncation: if the first response's
    ``finish_reason`` indicates the model hit the token cap (it would
    produce literally invalid JSON because the output cuts mid-string),
    raise :class:`StrictJsonTruncatedError` immediately instead of
    burning a second LLM call on what's certain to fail again.

    ``store`` / ``conversation_id`` are passed straight through to
    ``execute_ai_request`` so an internal/workflow caller controls
    persistence exactly like an API request body does. ``store=None``
    inherits the context (default: persist). Both retry attempts in this
    helper share the SAME resolved conversation — the first call assigns a
    UUID when none is given and writes it back onto the context, so the
    retry continues the same conversation rather than spawning a new one.
    """
    return await llm_messages_to_pydantic(
        model=model,
        system=system,
        messages=[{"role": "user", "content": user}],
        output_cls=output_cls,
        max_tokens=max_tokens,
        metadata=metadata,
        store=store,
        conversation_id=conversation_id,
        on_delta=on_delta,
        on_reset=on_reset,
        wire_kind=wire_kind,
    )


def strip_json_fences(text: str) -> str:
    """Remove ``` fences and surrounding prose if present.

    Best-effort: the model is told to output JSON only, but sometimes
    wraps in fences or adds a sentence of preamble. This trims the
    obvious cases without doing anything risky.
    """
    s = text.strip()
    if s.startswith("```"):
        first_newline = s.find("\n")
        if first_newline > 0:
            s = s[first_newline + 1 :]
        if s.endswith("```"):
            s = s[:-3]
    s = s.strip()
    if not s.startswith("{") and not s.startswith("["):
        first = min(
            (i for i in (s.find("{"), s.find("[")) if i >= 0),
            default=-1,
        )
        if first > 0:
            last_brace = s.rfind("}")
            last_bracket = s.rfind("]")
            last = max(last_brace, last_bracket)
            if last > first:
                s = s[first : last + 1]
    return s
