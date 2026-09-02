"""Wire-level outbound HTTP capture for the CONTEXT_ANALYSIS stream event.

This module implements the "middleware that gates outbound requests and
takes their snapshot on their way out" — installed as an ``httpx`` request
event-hook on every provider SDK's underlying HTTP client.

Design contract
---------------
1. **Zero impact when off.** The hook's fast path is a single ContextVar
   read + a getattr + a bool check. If ``AppContext.snapshot`` is False
   (which is >99% of all calls in production) the hook returns immediately.
   No allocations, no body parsing, no emitter touch.

2. **Wire fidelity.** The hook receives ``httpx.Request`` objects *after*
   the provider SDK has serialized them, so the captured bytes are exactly
   what the provider will receive. We never modify the request — we only
   read ``request.content`` and ``request.headers``. The only mutation is
   redacting auth-bearing headers in the emitted *event* (the on-wire
   request itself is untouched).

3. **Never breaks the call.** The capture path is wrapped in a single
   try/except that logs and swallows. Snapshotting MUST NOT cause a live
   request to fail.

4. **Concurrent-safe.** ``CallMeta`` is stored in a ``ContextVar`` so each
   asyncio Task sees its own value. Parallel agents and child sub-agents
   cannot leak per-call metadata into each other's HTTP traffic.

The hook is installed via ``make_capture_http_client()`` which returns a
pre-configured ``httpx.AsyncClient`` that the provider SDKs accept via
their ``http_client=`` constructor argument.
"""

from __future__ import annotations

import json
from contextvars import ContextVar
from dataclasses import dataclass
from typing import Any

import httpx
from matrx_utils import vcprint

from matrx_connect.context.app_context import try_get_app_context
from matrx_connect.context.events import ContextAnalysisPayload


# ---------------------------------------------------------------------------
# Auth-bearing headers to redact in the emitted event (NOT on the wire)
# ---------------------------------------------------------------------------
# The hook leaves the actual ``httpx.Request`` headers untouched — these
# values are only swapped out inside the ``ContextAnalysisPayload`` we
# construct for the stream event. The keys are matched case-insensitively.

_REDACT_HEADERS: frozenset[str] = frozenset(
    {
        "authorization",
        "x-api-key",
        "x-goog-api-key",
        "x-goog-api-client",  # Often carries identifying tokens
        "proxy-authorization",
        "anthropic-api-key",
        "openai-organization",
        "openai-project",
        "cookie",
    }
)


# ---------------------------------------------------------------------------
# CallMeta — per-call metadata stamped by the provider before the SDK call
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class CallMeta:
    """Metadata describing the provider call about to be made.

    Set by the provider's ``execute()`` method via ``set_call_meta(...)``
    immediately before the SDK invocation. Read by the request hook to
    annotate the emitted ``ContextAnalysisPayload``. ContextVar storage
    means concurrent provider calls (parallel agents) each see only their
    own metadata.

    The default ``("unknown", None, None, False, 1)`` is what the hook
    sees if a provider forgot to call ``set_call_meta`` — the event still
    fires (we always prefer some signal over none), it just lacks the
    matrx-side decoration.
    """

    provider: str
    model: str | None = None
    iteration: int | None = None
    is_streaming: bool = False
    attempt: int = 1


_call_meta_var: ContextVar[CallMeta | None] = ContextVar(
    "matrx_ai_outbound_call_meta", default=None
)


def set_call_meta(meta: CallMeta) -> None:
    """Stamp per-call metadata on the current async context.

    Call this from the provider's ``execute()`` immediately before the
    SDK call (right after ``capture_request_payload(config_data)`` for
    consistency). Subsequent ``httpx`` requests issued from the same
    asyncio Task will see this metadata in the request hook.
    """
    _call_meta_var.set(meta)


def get_call_meta() -> CallMeta | None:
    """Return the metadata stamped for the current call, or None."""
    return _call_meta_var.get()


def stamp_call_meta(
    *,
    provider: str,
    model: str | None = None,
    is_streaming: bool = False,
    attempt: int = 1,
) -> None:
    """Convenience wrapper — read iteration from ExecutionState and call
    ``set_call_meta`` in one line.

    Provider ``execute()`` methods call this immediately after
    ``capture_request_payload(config_data)`` and immediately before the
    SDK invocation. Importing ``ExecutionState`` lazily inside the
    function keeps this module's import graph minimal.
    """
    iteration: int | None = None
    try:
        from matrx_ai.orchestrator.execution_state import try_get_execution_state

        state = try_get_execution_state()
        if state is not None:
            iteration = state.iteration
    except Exception:
        iteration = None

    set_call_meta(
        CallMeta(
            provider=provider,
            model=model,
            iteration=iteration,
            is_streaming=is_streaming,
            attempt=attempt,
        )
    )


# ---------------------------------------------------------------------------
# The hook itself — fast path first, capture path second
# ---------------------------------------------------------------------------


def _is_snapshot_enabled() -> tuple[bool, Any]:
    """Single fused fast-path check — returns ``(enabled, ctx)``.

    Inlined into the hook so the cold path is exactly one ContextVar
    read + one attr access + one bool check before returning.
    """
    ctx = try_get_app_context()
    if ctx is None:
        return False, None
    if not getattr(ctx, "snapshot", False):
        return False, ctx
    return True, ctx


async def _outbound_request_hook(request: httpx.Request) -> None:
    """httpx request event-hook — captures the outbound request when
    ``AppContext.snapshot`` is True, otherwise returns immediately.

    This runs on EVERY outbound HTTP request from every provider SDK that
    was constructed with ``make_capture_http_client()``. Keep the cold
    path tiny.
    """
    enabled, ctx = _is_snapshot_enabled()
    if not enabled:
        return

    if ctx is None or ctx.emitter is None:
        return

    try:
        meta = _call_meta_var.get() or CallMeta(provider="unknown")

        body_bytes: bytes = request.content or b""
        body_obj: dict[str, Any] | None = None
        body_raw: str | None = None
        if body_bytes:
            try:
                parsed = json.loads(body_bytes)
                if isinstance(parsed, dict):
                    body_obj = parsed
                else:
                    body_obj = {"__non_dict_root__": parsed}
            except (json.JSONDecodeError, ValueError, UnicodeDecodeError):
                body_raw = body_bytes.decode("utf-8", errors="replace")

        headers = {
            k: ("<redacted>" if k.lower() in _REDACT_HEADERS else v)
            for k, v in request.headers.items()
        }

        payload = ContextAnalysisPayload(
            provider=meta.provider,
            model=meta.model,
            iteration=meta.iteration,
            conversation_id=getattr(ctx, "conversation_id", None) or None,
            request_id=getattr(ctx, "request_id", None) or None,
            attempt=meta.attempt,
            is_streaming=meta.is_streaming,
            method=request.method,
            url=str(request.url),
            headers=headers,
            body=body_obj,
            body_raw=body_raw,
            body_size_bytes=len(body_bytes),
        )

        await ctx.emitter.send_context_analysis(payload)
    except Exception as exc:
        vcprint(
            f"[ContextAnalysis] capture failed (non-fatal): {exc}",
            color="yellow",
        )


# ---------------------------------------------------------------------------
# Factory — produces an httpx.AsyncClient with the hook installed
# ---------------------------------------------------------------------------


def make_capture_http_client(
    *,
    timeout: float | httpx.Timeout = 600.0,
    **kwargs: Any,
) -> httpx.AsyncClient:
    """Construct an ``httpx.AsyncClient`` with the CONTEXT_ANALYSIS request
    hook installed.

    Provider SDKs (OpenAI, Anthropic, Groq, xAI, Cerebras, Together,
    GenericOpenAI) accept this via their ``http_client=`` constructor
    argument and will route every outbound request through it. Any
    additional ``httpx.AsyncClient`` kwargs (proxies, transport overrides,
    etc.) are forwarded.
    """
    existing_hooks = kwargs.pop("event_hooks", {}) or {}
    request_hooks = list(existing_hooks.get("request", []))
    if _outbound_request_hook not in request_hooks:
        request_hooks.append(_outbound_request_hook)
    response_hooks = list(existing_hooks.get("response", []))

    return httpx.AsyncClient(
        timeout=timeout,
        event_hooks={"request": request_hooks, "response": response_hooks},
        **kwargs,
    )


async def emit_explicit_context_analysis(
    *,
    provider: str,
    method: str,
    url: str,
    headers: dict[str, str] | None = None,
    body: dict[str, Any] | None = None,
    body_raw: str | None = None,
    body_size_bytes: int | None = None,
    is_streaming: bool = False,
    model: str | None = None,
    attempt: int = 1,
) -> None:
    """Emit a CONTEXT_ANALYSIS event from a non-httpx provider call site.

    Used by SDKs that don't use ``httpx`` (or where we can't inject the
    capture client) — currently ElevenLabs and the Google ``genai`` client
    when its httpx transport isn't reachable. Same gating semantics as the
    hook: silent no-op unless ``AppContext.snapshot`` is True.

    Provider call sites should still call ``set_call_meta(...)`` first so
    iteration / model / streaming flags are recorded consistently.
    """
    enabled, ctx = _is_snapshot_enabled()
    if not enabled:
        return
    if ctx is None or ctx.emitter is None:
        return

    try:
        meta = _call_meta_var.get() or CallMeta(provider=provider)
        safe_headers = {
            k: ("<redacted>" if k.lower() in _REDACT_HEADERS else v)
            for k, v in (headers or {}).items()
        }
        size = body_size_bytes
        if size is None:
            if body_raw is not None:
                size = len(body_raw.encode("utf-8", errors="replace"))
            elif body is not None:
                try:
                    size = len(json.dumps(body).encode("utf-8"))
                except (TypeError, ValueError):
                    size = 0
            else:
                size = 0

        payload = ContextAnalysisPayload(
            provider=provider,
            model=meta.model if meta.model is not None else model,
            iteration=meta.iteration,
            conversation_id=getattr(ctx, "conversation_id", None) or None,
            request_id=getattr(ctx, "request_id", None) or None,
            attempt=attempt,
            is_streaming=is_streaming if is_streaming else meta.is_streaming,
            method=method,
            url=url,
            headers=safe_headers,
            body=body,
            body_raw=body_raw,
            body_size_bytes=size,
        )

        await ctx.emitter.send_context_analysis(payload)
    except Exception as exc:
        vcprint(
            f"[ContextAnalysis] explicit emit failed (non-fatal): {exc}",
            color="yellow",
        )
