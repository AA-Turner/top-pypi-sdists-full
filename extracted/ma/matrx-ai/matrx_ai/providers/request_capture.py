"""PROVIDER REQUEST CAPTURE — run everything, send nothing, return the request.

The agent builder's Model view must show EXACTLY what a provider receives. The
only honest way to know that is to run all of the real code — agent load,
variables, pick-list swaps, context, skills, prompt blocks, tool merge, the send
boundary, the provider translator, the provider SDK's own serializer — and stop
at the one instant the request would leave the process. This module is that
stop.

One flag, one place: ``capturing_provider_request()`` sets a ContextVar for the
duration of a run. Every transport a chat provider uses checks it at the point
of sending, and instead of sending raises ``ProviderRequestCaptured`` carrying
the complete request:

* httpx-based SDKs (Anthropic, OpenAI, Groq, Cerebras, Together, every
  OpenAI-compatible endpoint incl. Moonshot / Hugging Face) — the request hook
  every provider client is built with (``outbound_capture._outbound_request_hook``)
  hands the ``httpx.Request`` here AFTER the SDK serialized it: the body bytes
  ARE what the provider would receive.
* Google ``genai`` — the SDK's own last step before its transport
  (``BaseApiClient._async_request_once``) is wrapped once, at import
  (``install_genai_capture``), with the same check.
* xAI (gRPC) — the adapter hands over the exact request proto the stub would
  send (``capture_grpc_request``).
* The mock provider — its adapter hands over the unified config it answers from.

The capture is a ``BaseException`` (like ``CancelledError``) so no
``except Exception`` on the way out — retries, fallbacks, failure reports —
mistakes it for a provider failure. The few ``except BaseException`` seams on the
path re-raise it untouched (``is_request_capture``).

Secrets never leave: auth-bearing headers are replaced with ``<redacted>``.
Zero impact when off: one ContextVar read.
"""

from __future__ import annotations

import copy
import json
from collections.abc import Iterator
from contextlib import contextmanager
from contextvars import ContextVar
from dataclasses import dataclass, field
from typing import Any

#: Header names whose values are credentials (matched case-insensitively).
SECRET_HEADERS: frozenset[str] = frozenset(
    {
        "authorization",
        "x-api-key",
        "x-goog-api-key",
        "api-key",
        "proxy-authorization",
        "anthropic-api-key",
        "openai-organization",
        "openai-project",
        "cookie",
    }
)

REDACTED = "<redacted>"


@dataclass
class CaptureSlot:
    """The active capture. ``captured`` holds the request once a transport reached it."""

    captured: dict[str, Any] | None = None
    notes: list[str] = field(default_factory=list)
    #: Paid steps that would have run BEFORE the main request and were skipped
    #: (``{"kind", "detail", "status": "skipped"}``). The caller returns them.
    pre_steps: list[dict[str, Any]] = field(default_factory=list)


_capture_var: ContextVar[CaptureSlot | None] = ContextVar("matrx_ai_provider_request_capture", default=None)


class ProviderRequestCaptured(BaseException):  # noqa: N818 — a stop, not an error
    """Raised at the transport instead of sending. ``request`` is the complete request."""

    def __init__(self, request: dict[str, Any]) -> None:
        super().__init__(f"provider request captured ({request.get('provider')})")
        self.request = request


@contextmanager
def capturing_provider_request() -> Iterator[CaptureSlot]:
    """Run the enclosed code in capture mode: the first provider send is captured, not sent."""
    install_paid_send_guard()
    slot = CaptureSlot()
    token = _capture_var.set(slot)
    try:
        yield slot
    finally:
        _capture_var.reset(token)


def is_capturing() -> bool:
    return _capture_var.get() is not None


class PaidSendBlockedInCapture(BaseException):  # noqa: N818 — a stop, not an error
    """A capture run reached a paid provider call that is not the main request.

    A ``BaseException`` so a pre-step's own ``except Exception`` (e.g. "transcription
    failed, tell the model") cannot swallow it and quietly put a stand-in into the
    payload. The Model view door turns it into a plain refusal naming the call.
    """

    def __init__(self, method: str, url: str) -> None:
        super().__init__(f"capture run blocked a paid provider call: {method} {url}")
        self.method = method
        self.url = url


def skip_paid_pre_step(kind: str, detail: str) -> bool:
    """Declare a paid pre-step (transcription, embedding, ...) and say whether to skip it.

    Returns True in a capture run, after recording the skip on the capture so the
    result says what was not run. Callers return their stand-in WITHOUT caching it.
    """
    slot = _capture_var.get()
    if slot is None:
        return False
    slot.pre_steps.append({"kind": kind, "detail": detail, "status": "skipped"})
    slot.notes.append(f"{kind} was not run in a capture ({detail}); a placeholder stands in for its output.")
    return True


def note_capture(note: str) -> None:
    """Record a fact about how the request was shaped on an active capture (no-op otherwise).

    The Model view returns these beside the request, so a conversion the wire shows (e.g. a
    history system message sent as a marked note) is said in words, not left to be spotted."""
    slot = _capture_var.get()
    if slot is not None:
        slot.notes.append(note)


#: Hosts whose calls cost money. A capture run must never reach one except through the
#: capture hook that stops the main request. Matched as a host suffix.
PAID_PROVIDER_HOST_SUFFIXES: tuple[str, ...] = (
    "api.groq.com",
    "api.openai.com",
    "api.anthropic.com",
    "generativelanguage.googleapis.com",
    "aiplatform.googleapis.com",
    "api.x.ai",
    "api.cerebras.ai",
    "api.together.xyz",
    "api.together.ai",
    "api.elevenlabs.io",
    "api.replicate.com",
    "api.cohere.com",
    "api.cohere.ai",
    "api.moonshot.ai",
    "api.moonshot.cn",
    "api.deepgram.com",
    "api.assemblyai.com",
    "router.huggingface.co",
    "api-inference.huggingface.co",
    "api.mistral.ai",
    "api.perplexity.ai",
    "api.deepseek.com",
    "api.fireworks.ai",
    "openrouter.ai",
)


def _is_paid_host(host: str | None) -> bool:
    host = (host or "").lower()
    return any(host == h or host.endswith("." + h) for h in PAID_PROVIDER_HOST_SUFFIXES)


def guard_paid_send(request: Any) -> None:
    """Backstop: refuse any httpx send to a paid provider host while capturing.

    The main request is stopped earlier by the capture hook; whatever reaches the
    transport is a pre-step (or a client built without the hook). Never sends.
    """
    if _capture_var.get() is None:
        return
    url = getattr(request, "url", None)
    host = getattr(url, "host", None)
    if _is_paid_host(host):
        raise PaidSendBlockedInCapture(str(getattr(request, "method", "?")), _redact_url(str(url)))


_PAID_GUARD_INSTALLED = False


def install_paid_send_guard() -> None:
    """Wrap every installed httpx flavor's transports once. Idempotent; inert unless capturing."""
    global _PAID_GUARD_INSTALLED
    if _PAID_GUARD_INSTALLED:
        return
    flavors: list[Any] = []
    import httpx

    flavors.append(httpx)
    try:
        import httpx2  # type: ignore[import-not-found]

        flavors.append(httpx2)
    except ImportError:
        pass

    for mod in flavors:
        for cls_name, attr, is_async in (
            ("AsyncHTTPTransport", "handle_async_request", True),
            ("HTTPTransport", "handle_request", False),
        ):
            cls = getattr(mod, cls_name, None)
            original = getattr(cls, attr, None) if cls is not None else None
            if original is None:
                continue

            def _wrap(orig: Any, is_async: bool) -> Any:
                if is_async:

                    async def _async(self: Any, request: Any) -> Any:
                        guard_paid_send(request)
                        return await orig(self, request)

                    return _async

                def _sync(self: Any, request: Any) -> Any:
                    guard_paid_send(request)
                    return orig(self, request)

                return _sync

            setattr(cls, attr, _wrap(original, is_async))
    _PAID_GUARD_INSTALLED = True


def is_request_capture(exc: BaseException) -> bool:
    return isinstance(exc, ProviderRequestCaptured)


def redact_headers(headers: Any) -> dict[str, str]:
    items = headers.items() if hasattr(headers, "items") else []
    return {str(k): (REDACTED if str(k).lower() in SECRET_HEADERS else str(v)) for k, v in items}


def _redact_url(url: str) -> str:
    """Google puts the key in ``?key=`` on some paths; never return it."""
    if "key=" not in url:
        return url
    from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

    parts = urlsplit(url)
    query = [(k, REDACTED if k.lower() == "key" else v) for k, v in parse_qsl(parts.query, keep_blank_values=True)]
    return urlunsplit(parts._replace(query=urlencode(query, safe="<>")))


def _sdk_kwargs() -> Any:
    """The provider's SDK-ready request (``capture_request_payload``), as JSON-safe data."""
    try:
        from matrx_ai.orchestrator.execution_state import try_get_execution_state

        state = try_get_execution_state()
        payload = getattr(state, "snapshot_payload", None) if state is not None else None
        if payload is None:
            return None
        # The same serializer chat.request_snapshot uses, so the two compare field for field.
        from matrx_ai.orchestrator.executor import _json_safe

        return json.loads(json.dumps(_json_safe(payload), default=str))
    except Exception:  # noqa: BLE001 — the wire body is the truth; this is a companion view
        return None


def _call_meta() -> tuple[str | None, str | None, bool]:
    from matrx_ai.providers.outbound_capture import get_call_meta

    meta = get_call_meta()
    if meta is None:
        return None, None, False
    return meta.provider, meta.model, bool(meta.is_streaming)


def _finish(record: dict[str, Any]) -> None:
    slot = _capture_var.get()
    if slot is None:
        return
    slot.captured = record
    raise ProviderRequestCaptured(copy.deepcopy(record))


def capture_wire_request(
    *,
    method: str,
    url: str,
    headers: Any,
    body: bytes | str | None,
    provider: str | None = None,
    transport: str = "https",
) -> None:
    """Stop an HTTP send in capture mode. No-op when not capturing.

    ``body`` is the exact bytes the transport would put on the wire. It is
    returned verbatim as ``body_text`` and, when it is JSON, parsed (key order
    kept) as ``body``.
    """
    if _capture_var.get() is None:
        return
    meta_provider, meta_model, streaming = _call_meta()
    raw = body.decode("utf-8", errors="replace") if isinstance(body, bytes | bytearray) else (body or "")
    parsed: Any = None
    if raw:
        try:
            parsed = json.loads(raw)
        except ValueError:
            parsed = None
    _finish(
        {
            "provider": provider or meta_provider or "unknown",
            "model": meta_model,
            "transport": transport,
            "method": method.upper(),
            "url": _redact_url(str(url)),
            "headers": redact_headers(headers),
            "body": parsed,
            "body_text": raw,
            "is_streaming": streaming,
            "sdk_kwargs": _sdk_kwargs(),
        }
    )


def capture_grpc_request(*, provider: str, rpc: str, target: str, request_proto: Any) -> None:
    """Stop a gRPC send in capture mode: the request proto the stub would send, as JSON."""
    if _capture_var.get() is None:
        return
    from google.protobuf.json_format import MessageToDict

    body = MessageToDict(request_proto, preserving_proto_field_name=True)
    _, meta_model, streaming = _call_meta()
    _finish(
        {
            "provider": provider,
            "model": meta_model,
            "transport": "grpc",
            "method": "RPC",
            "url": f"{target}/{rpc}",
            "headers": {},
            "body": body,
            "body_text": json.dumps(body, indent=2, ensure_ascii=False),
            "is_streaming": streaming,
            "sdk_kwargs": _sdk_kwargs(),
        }
    )


def capture_local_request(*, provider: str, model: str | None, body: Any, transport: str = "local") -> None:
    """Stop an in-process provider (the mock) in capture mode: what it would answer from."""
    if _capture_var.get() is None:
        return
    safe = json.loads(json.dumps(body, default=str))
    _finish(
        {
            "provider": provider,
            "model": model,
            "transport": transport,
            "method": "CALL",
            "url": f"{provider}://local",
            "headers": {},
            "body": safe,
            "body_text": json.dumps(safe, indent=2, ensure_ascii=False),
            "is_streaming": False,
            "sdk_kwargs": _sdk_kwargs(),
        }
    )


_GENAI_INSTALLED = False


def install_genai_capture() -> None:
    """Wrap ``genai``'s last pre-transport step once. Idempotent; inert unless capturing."""
    global _GENAI_INSTALLED
    if _GENAI_INSTALLED:
        return
    from google.genai import _api_client

    original = _api_client.BaseApiClient._async_request_once

    async def _async_request_once(self: Any, http_request: Any, stream: bool = False) -> Any:
        if _capture_var.get() is not None:
            data = http_request.data
            body = data if isinstance(data, bytes) else (json.dumps(data).encode("utf-8") if data else b"")
            capture_wire_request(
                method=http_request.method,
                url=http_request.url,
                headers=http_request.headers,
                body=body,
                provider="google",
            )
        return await original(self, http_request, stream)

    _api_client.BaseApiClient._async_request_once = _async_request_once  # type: ignore[method-assign]
    _GENAI_INSTALLED = True


__all__ = [
    "CaptureSlot",
    "PAID_PROVIDER_HOST_SUFFIXES",
    "PaidSendBlockedInCapture",
    "ProviderRequestCaptured",
    "SECRET_HEADERS",
    "capture_grpc_request",
    "capture_local_request",
    "capture_wire_request",
    "capturing_provider_request",
    "note_capture",
    "guard_paid_send",
    "install_genai_capture",
    "install_paid_send_guard",
    "is_capturing",
    "is_request_capture",
    "redact_headers",
    "skip_paid_pre_step",
]
