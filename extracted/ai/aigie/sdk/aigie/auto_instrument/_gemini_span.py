"""Span plumbing shared by the two Gemini clients.

Both clients emit the same span — provider ``gemini``, type ``llm``, the same usage
triple off ``usage_metadata`` — and differ only in where the request keeps its model,
its contents and its system instruction. Each client supplies that reading as a
``describe`` callable and takes its wrapper from ``traced`` / ``traced_async`` here, so
the enter/exit pairing is written once: a ``SpanContext`` is built mutably in memory and
shipped exactly once by ``__aexit__``, and the legacy patch's missing ``__aexit__`` is
precisely why a direct Gemini call used to produce a trace with no spans in it. The
pairing holds once the span is open; a raise while *populating* it still drops the span,
which is a narrower hole than the one this replaced but not no hole.

Separately, and on **every** call including a successful one: the trace these spans hang
under is entered and never exited, because that is what ``get_or_create_trace`` does to
every caller. Each call therefore leaves one ``trace_state._open_spans`` entry that ships
at shutdown as a ``workflow`` root named "LLM Call: gemini" with ``status="interrupted"``
— 500 Gemini calls, 500 such roots. Pre-existing and not Gemini's to fix alone.

The async wrapper awaits its span steps instead of reusing the sync ones. Inside a
running loop ``_run_async_safely`` spawns a thread and blocks on ``join``, so sharing the
sync path would make every instrumented ``await`` stall the caller's event loop on span
setup — instrumentation charging the hot path it exists to measure.

Everything here is *our* code, so every entry point is contained: a failure extracting
attributes must degrade the span, never surface in the caller's ``generate_content``.
"""

from __future__ import annotations

import functools
import logging
import time
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from typing import Any

logger = logging.getLogger(__name__)

PROVIDER = "gemini"
TEXT_LIMIT = 500
_TRACE_NAME = "LLM Call: gemini"

# (receiver, args, kwargs) -> (model name, span input). The receiver is the model object
# on the legacy client and the bound ``Models`` instance on the current one.
Describe = Callable[[Any, "tuple[Any, ...]", "dict[str, Any]"], "tuple[str, dict[str, Any]]"]


@dataclass
class SpanHandle:
    """An open span plus what closing it needs.

    ``model_name`` travels here rather than being re-read at close time because a raise
    while re-reading it would cost the span: the close step is guarded, so it cannot
    reach the host, but the span would be dropped un-emitted.
    """

    span: Any
    start: float
    model_name: str


def guard(fn: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
    """Run one of our own span steps, absorbing whatever it raises.

    The host called ``generate_content``; a bug in our token extraction is not theirs to
    catch. Logged at debug because this is a per-call path.
    """
    try:
        return fn(*args, **kwargs)
    except Exception as exc:  # noqa: BLE001 - instrumentation must never break the caller
        logger.debug("gemini span step %s failed: %s", getattr(fn, "__name__", fn), exc)
        return None


async def aguard(coro: Awaitable[Any]) -> Any:
    """``guard`` for the awaited span steps on the async path.

    The label is read off the coroutine rather than passed in: hand-written step names
    drift from the functions they label, and one of the three here already had.
    """
    try:
        return await coro
    except Exception as exc:  # noqa: BLE001 - instrumentation must never break the caller
        logger.debug("gemini span step %s failed: %s", getattr(coro, "__qualname__", coro), exc)
        return None


def traced(original: Callable[..., Any], describe: Describe) -> Callable[..., Any]:
    """Wrap a synchronous ``generate_content`` so it emits exactly one span.

    On the legacy client a ``stream=True`` call returns a generator, so the span closes
    on the unconsumed stream and records no completion text. Inherited, and no worse than
    before: previously it recorded nothing at all. The current client has no such
    parameter — its streaming lives on ``generate_content_stream``, left unpatched.
    """

    @functools.wraps(original)
    def traced_call(self: Any, *args: Any, **kwargs: Any) -> Any:
        handle = guard(_open, describe, self, args, kwargs)
        if handle is None:
            return original(self, *args, **kwargs)
        try:
            response = original(self, *args, **kwargs)
        except BaseException as exc:
            guard(fail_span, handle, exc)
            raise
        guard(close_span, handle, response)
        return response

    traced_call._aigie_patched = True  # type: ignore[attr-defined]
    return traced_call


def traced_async(original: Callable[..., Any], describe: Describe) -> Callable[..., Any]:
    """Wrap an asynchronous ``generate_content`` so it emits one span, without threads."""

    @functools.wraps(original)
    async def traced_call(self: Any, *args: Any, **kwargs: Any) -> Any:
        handle = await aguard(_open_async(describe, self, args, kwargs))
        if handle is None:
            return await original(self, *args, **kwargs)
        try:
            response = await original(self, *args, **kwargs)
        except BaseException as exc:
            await aguard(fail_span_async(handle, exc))
            raise
        await aguard(close_span_async(handle, response))
        return response

    traced_call._aigie_patched = True  # type: ignore[attr-defined]
    return traced_call


def _open(
    describe: Describe, receiver: Any, args: tuple[Any, ...], kwargs: dict[str, Any]
) -> SpanHandle | None:
    read = _read(describe, receiver, args, kwargs)
    if read is None:
        return None
    return open_span(*read)


async def _open_async(
    describe: Describe, receiver: Any, args: tuple[Any, ...], kwargs: dict[str, Any]
) -> SpanHandle | None:
    read = _read(describe, receiver, args, kwargs)
    if read is None:
        return None
    return await open_span_async(*read)


def _read(
    describe: Describe, receiver: Any, args: tuple[Any, ...], kwargs: dict[str, Any]
) -> tuple[str, dict[str, Any]] | None:
    """Read the request, naming the client in the log if that read fails.

    Both clients funnel through one ``_open``, so without this a failure logged only
    ``_open`` — telling you neither which client broke nor whether it broke reading the
    request or opening the span. ``getattr`` rather than ``describe.__module__`` because
    a callable without one (a ``functools.partial``) would raise from inside the handler,
    and the outer ``guard`` would absorb that back into the message this replaced.
    """
    try:
        return describe(receiver, args, kwargs)
    except Exception as exc:  # noqa: BLE001 - instrumentation must never break the caller
        client = getattr(describe, "__module__", describe)
        logger.debug("gemini request read failed in %s: %s", client, exc)
        return None


def _traceable() -> bool:
    """Whether this call should be traced at all.

    False when there is no client, it is not initialized, or an outer framework callback
    is already tracing this same call.
    """
    from aigie.auto_instrument.llm import _llm_autoinstrument_suppressed
    from aigie.client import get_aigie

    aigie = get_aigie()
    return bool(aigie and aigie._initialized and not _llm_autoinstrument_suppressed())


def _trace_request() -> Any:
    """The coroutine that resolves this call's trace — awaited by both paths."""
    from aigie.auto_instrument.trace import get_or_create_trace

    return get_or_create_trace(name=_TRACE_NAME, metadata={"provider": PROVIDER, "type": "llm"})


def _start_span(trace: Any, model_name: str) -> Any:
    # No parent, deliberately. The obvious improvement — parent it to the span published
    # by `get_current_span_context`, so a call inside `@traceable` nests under it — is
    # wrong here: the decorators publish that span through `context_manager`, while
    # `get_or_create_trace` reads a *different* contextvar that the decorators never set.
    # So a decorated caller mints one trace and this span another, and claiming that
    # parent points at an id absent from this span's own trace. A dangling parent renders
    # worse than none. Bridging the two context systems is the actual fix, and it is not
    # this seam's to make.
    return trace.span(f"LLM: {PROVIDER} - {model_name}", type="llm")


def open_span(model_name: str, span_input: dict[str, Any]) -> SpanHandle | None:
    """Open, enter and populate this call's span, or None when there is nothing to trace."""
    from aigie.auto_instrument.llm import _run_async_safely

    if not _traceable():
        return None
    trace = _run_async_safely(_trace_request())
    if not trace:
        return None
    span = _start_span(trace, model_name)
    _run_async_safely(span.__aenter__())
    span.set_input(span_input)
    return SpanHandle(span, time.time(), model_name)


async def open_span_async(model_name: str, span_input: dict[str, Any]) -> SpanHandle | None:
    """``open_span`` for a caller that already has a running loop."""
    from aigie.auto_instrument.trace import get_current_trace, set_current_trace

    if not _traceable():
        return None
    inherited = get_current_trace()
    trace = await _trace_request()
    if not trace:
        return None
    if trace is not inherited:
        # A trace `get_or_create_trace` *creates* is published to the `_current_trace`
        # contextvar, and nothing here ever closes it. On the sync path that write cannot
        # escape: `_run_async_safely` either runs the coroutine under `copy_context().run`
        # in a worker thread, or hands it to `asyncio.run`, which wraps it in a Task —
        # and Task creation snapshots the context. Awaiting in the caller's own context
        # instead left this span's private
        # trace installed for the rest of the task, filing every later call (a LangChain
        # `ainvoke`, the next request on a queue worker) under a trace named
        # "LLM Call: gemini". `trace is not inherited` holds only when nothing was
        # inherited, so this is an exact restore rather than a guess.
        #
        # Two things it does not fix, both pre-existing on every path and every caller of
        # `get_or_create_trace`: the trace was *entered* and is never exited, so it keeps
        # a `trace_state._open_spans` entry for the process's life (see the module
        # docstring); and `set_current_trace` also writes two thread-keyed dicts in
        # `span_enricher` that no context copy isolates, so restoring can clear another
        # instrumentor's active ids. Nothing reads either dict today, so that is dead
        # state rather than a live defect.
        set_current_trace(inherited)
    span = _start_span(trace, model_name)
    await span.__aenter__()
    span.set_input(span_input)
    return SpanHandle(span, time.time(), model_name)


def close_span(handle: SpanHandle, response: Any) -> None:
    """Record the response and emit the span."""
    from aigie.auto_instrument.llm import _run_async_safely

    _record_response(handle, response)
    _run_async_safely(handle.span.__aexit__(None, None, None))


async def close_span_async(handle: SpanHandle, response: Any) -> None:
    _record_response(handle, response)
    await handle.span.__aexit__(None, None, None)


def fail_span(handle: SpanHandle, exc: BaseException) -> None:
    """Emit the span for a call that raised, then let the exception continue."""
    from aigie.auto_instrument.llm import _run_async_safely

    _record_error(handle, exc)
    _run_async_safely(handle.span.__aexit__(type(exc), exc, exc.__traceback__))


async def fail_span_async(handle: SpanHandle, exc: BaseException) -> None:
    _record_error(handle, exc)
    await handle.span.__aexit__(type(exc), exc, exc.__traceback__)


def _record_response(handle: SpanHandle, response: Any) -> None:
    output: dict[str, Any] = {
        "latency": time.time() - handle.start,
        "model": handle.model_name,
        "provider": PROVIDER,
    }
    usage = _usage(response)
    if usage:
        output["usage"] = usage
    text = _response_text(response)
    if text is not None:
        output["content"] = text[:TEXT_LIMIT]
    handle.span.set_output(output)

    # The span contract reads model, tokens and provider off the *top level* of the
    # payload, not out of `output` — a span carrying them only nested is unpriceable and
    # unattributed, which is what these setters exist to avoid. Cost is left alone: the
    # contract asks that the span *can* be priced, which is model plus tokens, and the
    # rate table is not ours.
    handle.span.set_model(handle.model_name)
    handle.span.set_metadata({"provider": PROVIDER})
    if usage:
        handle.span.set_usage(
            prompt_tokens=usage["prompt_tokens"],
            completion_tokens=usage["completion_tokens"],
            total_tokens=usage["total_tokens"],
        )


def _record_error(handle: SpanHandle, exc: BaseException) -> None:
    """Populate the span from a failed call.

    Callers hand the exception on to ``__aexit__`` rather than swallowing it there: that
    is what turns the span's own status away from ``success`` and fills in
    ``error_message`` / ``error_type``. Closing with ``(None, None, None)`` would ship a
    failed call as a successful span.
    """
    handle.span.set_output(
        {
            "error": str(exc),
            "error_type": type(exc).__name__,
            "latency": time.time() - handle.start,
            "status": "error",
        }
    )


def _usage(response: Any) -> dict[str, int] | None:
    """The usage triple, normalised across two clients that report it differently.

    Reasoning tokens are counted as completion. Gemini reports them in their own field
    and bills them as output, so a span that reads only ``candidates_token_count``
    claimed 24 tokens for a live call the provider totalled at 88 — and left
    ``prompt + completion`` contradicting ``total`` on the same span.

    The shortfall rule below only holds once every *input* component has been added to
    ``prompt``; anything left unaccounted is then genuinely unitemised reasoning.
    """
    usage = getattr(response, "usage_metadata", None)
    if usage is None:
        return None
    prompt = getattr(usage, "prompt_token_count", 0) or 0
    candidates = getattr(usage, "candidates_token_count", 0) or 0
    total = getattr(usage, "total_token_count", 0) or 0
    tool_use = getattr(usage, "tool_use_prompt_token_count", 0) or 0
    itemises_thoughts = hasattr(usage, "thoughts_token_count")
    reasoning = (getattr(usage, "thoughts_token_count", 0) or 0) if itemises_thoughts else 0

    # Tool results are fed back to the model as *input* and the current client counts
    # them in `total` as a fourth component. Left in the shortfall below they were billed
    # as output at roughly 4-8x their rate: prompt=100 candidates=50 tool_use=200
    # total=350 reported 100 in / 250 out instead of 300 in / 50 out.
    #
    # KNOWN GAP: Grounding-with-Google-Search retrieval is billed as a per-request search
    # fee and excluded from input billing, unlike URL context, File Search and code
    # execution, whose tool-use tokens are charged at the input rate. Detecting it needs
    # `groundingMetadata.webSearchQueries` off the response — grounding chunks alone will
    # not do, URL context emits those and *is* input-billed. So a search-grounded call
    # over-states input by `tool_use` here. Note its true split does not sum to `total`
    # at all, so the invariant below cannot hold for it either way.
    prompt += tool_use

    # `candidates_token_count` is inclusive of thinking on some surfaces and exclusive on
    # others — the same patched method reaches both, since `Client(vertexai=True)` and
    # `Client(api_key=...)` share it. Derive which, rather than picking one: if the
    # itemised parts already reach `total`, adding reasoning again double-counts it.
    completion = candidates if prompt + candidates == total else candidates + reasoning

    # The legacy protobuf carries no `thoughts_token_count` field at all, yet its
    # `total_token_count` still bills the thinking tokens, so an unexplained shortfall is
    # reasoning the response never itemised. Live, it reported prompt=22 completion=1
    # against a total of 101 — 78 output tokens priced at zero.
    if not itemises_thoughts and total > prompt + completion:
        completion = total - prompt

    return {
        "prompt_tokens": prompt,
        "completion_tokens": completion,
        "total_tokens": total or (prompt + completion),
    }


def _response_text(response: Any) -> str | None:
    """The completion text, or None when this response has none.

    ``.text`` is a property that *raises* when the response carries no usable candidate
    — a safety block, or a reply that is only a function call. ``hasattr`` does not help
    and neither does ``getattr(..., None)``: both absorb only ``AttributeError``, so the
    ``ValueError`` the client raises would travel out through the host's own call.
    """
    try:
        text = response.text
    except Exception as exc:  # noqa: BLE001 - a blocked response is not our error to raise
        logger.debug("gemini response carried no text: %s", type(exc).__name__)
        return None
    return text if isinstance(text, str) else None
