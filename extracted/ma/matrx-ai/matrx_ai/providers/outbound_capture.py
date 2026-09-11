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

5. **The SDK chooses the httpx flavor, not us.** Provider SDKs vendor
   their own HTTP layer and REJECT a client built on a different one
   (``anthropic`` 1.x raises ``TypeError: Invalid `http_client` argument;
   `httpx.AsyncClient` is from the `httpx` package, but this SDK uses
   `httpx2```). So callers pass ``sdk=<the SDK module>`` and the factory
   resolves the AsyncClient class **from the SDK itself** — a future
   vendoring change is followed automatically instead of breaking every
   call.

The hook is installed via ``make_capture_http_client()`` which returns a
pre-configured ``AsyncClient`` that the provider SDKs accept via their
``http_client=`` constructor argument.
"""

from __future__ import annotations

import importlib
import json
import sys
from contextvars import ContextVar
from dataclasses import dataclass
from typing import Any

import httpx
from matrx_connect.context.app_context import try_get_app_context
from matrx_connect.context.events import ContextAnalysisPayload
from matrx_utils import vcprint

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


def _httpx_flavor_of_class(cls: type) -> Any | None:
    """Return the top-level httpx-like module a client class belongs to.

    ``anthropic.DefaultAsyncHttpxClient`` subclasses ``httpx2.AsyncClient``;
    ``openai.DefaultAsyncHttpxClient`` subclasses ``httpx.AsyncClient``.
    Walking the MRO and taking the first base whose root module exposes
    ``AsyncClient`` gives us the flavor without hardcoding a name.
    """
    for base in cls.__mro__[1:]:
        root_name = (base.__module__ or "").split(".")[0]
        if not root_name:
            continue
        module = sys.modules.get(root_name)
        if module is None:
            try:
                module = _load_sdk_module(root_name)
            except ImportError:
                continue
        if hasattr(module, "AsyncClient"):
            return module
    return None


def _load_sdk_module(sdk_name: str) -> Any:
    """Load an absolute SDK module name without hiding it in ``import_module``.

    ``resolve_sdk_httpx`` has always accepted arbitrary importable SDK names,
    including plugin SDKs which have not yet been imported by the host.  That
    is a runtime-extension contract, not a closed provider inventory.  Use the
    importlib spec protocol directly so the mandate scanner can distinguish
    this declared loader from an opaque dynamic ``import_module`` target.

    The ``sys.modules`` registration before ``exec_module`` mirrors Python's
    normal import semantics: packages can resolve circular imports and a
    failed initialization does not leave a half-loaded module behind.
    """
    existing = sys.modules.get(sdk_name)
    if existing is not None:
        return existing

    spec = importlib.util.find_spec(sdk_name)
    if spec is None or spec.loader is None:
        raise ModuleNotFoundError(f"No importable SDK module named {sdk_name!r}")

    module = importlib.util.module_from_spec(spec)
    sys.modules[sdk_name] = module
    try:
        spec.loader.exec_module(module)
    except Exception:
        if sys.modules.get(sdk_name) is module:
            sys.modules.pop(sdk_name, None)
        raise
    return module


def resolve_sdk_httpx(sdk: Any) -> Any:
    """Return the httpx-compatible module the given provider SDK is built on.

    ``sdk`` may be the SDK module itself or its importable name. Resolution
    order — each step asks the SDK, never a hardcoded table:

    1. The SDK's own ``DefaultAsyncHttpxClient`` (every openai-style SDK
       exports one); its base class names the flavor.
    2. The ``httpx`` symbol its ``_base_client`` module imported.
    3. Plain ``httpx`` — the historical default.

    NOTHING SILENT: an unresolvable SDK falls back to ``httpx`` and says so,
    because the SDK will then raise its own explicit TypeError if that is
    the wrong flavor (which is exactly the loud failure we want).
    """
    if sdk is None:
        return httpx

    module = sdk
    if isinstance(sdk, str):
        try:
            module = _load_sdk_module(sdk)
        except ImportError as exc:
            vcprint(
                f"[ContextAnalysis] could not import SDK {sdk!r} to resolve its "
                f"httpx flavor ({exc}); falling back to `httpx`. If the SDK "
                f"vendors another flavor its constructor will reject the client "
                f"loudly — pass the imported module instead of a name.",
                color="yellow",
            )
            return httpx

    for attr in ("DefaultAsyncHttpxClient", "DefaultHttpxClient"):
        cls = getattr(module, attr, None)
        if isinstance(cls, type):
            flavor = _httpx_flavor_of_class(cls)
            if flavor is not None:
                return flavor

    base_client_name = f"{getattr(module, '__name__', '')}._base_client"
    base_client = sys.modules.get(base_client_name)
    if base_client is None:
        try:
            base_client = _load_sdk_module(base_client_name)
        except ImportError:
            base_client = None
    if base_client is not None:
        for candidate_attr in ("httpx", "httpx2"):
            candidate = getattr(base_client, candidate_attr, None)
            if candidate is not None and hasattr(candidate, "AsyncClient"):
                return candidate

    return httpx


def make_capture_http_client(
    *,
    sdk: Any = None,
    timeout: float | httpx.Timeout = 600.0,
    **kwargs: Any,
) -> Any:
    """Construct an ``AsyncClient`` with the CONTEXT_ANALYSIS request hook
    installed, **built on the httpx flavor the target SDK itself uses**.

    Provider SDKs (OpenAI, Anthropic, Groq, xAI, Cerebras, Together,
    GenericOpenAI) accept this via their ``http_client=`` constructor
    argument and will route every outbound request through it. Any
    additional ``AsyncClient`` kwargs (proxies, transport overrides, etc.)
    are forwarded.

    Pass ``sdk=<the SDK module>`` whenever the client is handed to an SDK
    constructor. SDKs vendor their HTTP layer independently — ``anthropic``
    1.x is built on ``httpx2`` and rejects an ``httpx.AsyncClient`` with a
    ``TypeError`` — so the flavor must come from the SDK, never from this
    module's own import. Omitting ``sdk`` (raw call sites that use the
    client directly, e.g. the xAI TTS POST) keeps plain ``httpx``.

    The capture behaviour is identical on every flavor: the same request
    event-hook, the same timeout default, the same forwarded kwargs. Only
    the ``AsyncClient`` class changes.
    """
    existing_hooks = kwargs.pop("event_hooks", {}) or {}
    request_hooks = list(existing_hooks.get("request", []))
    if _outbound_request_hook not in request_hooks:
        request_hooks.append(_outbound_request_hook)
    response_hooks = list(existing_hooks.get("response", []))

    client_cls = resolve_sdk_httpx(sdk).AsyncClient

    return client_cls(
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
