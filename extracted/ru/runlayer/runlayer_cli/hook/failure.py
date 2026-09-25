"""Relay failure classification shared by the relay and deny-message rendering.

Extracted from ``hook/relay.py`` (ENG-5365) so ``messages.py`` can import the
context type at runtime without pulling the whole relay module. Keep this
module stdlib + httpx only.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Literal, NamedTuple

import httpx

# Closed vocabulary for FailureContext.kind. messages._unreachable_cause has a
# rendering branch per kind (contract-tested); a kind added here without one
# falls back to the generic legacy message.
FailureKind = Literal["connect", "upload_timeout", "upload_failed", "timeout", "http"]

# Who answered a non-2xx. ``"runlayer"``: the Runlayer application (its error
# responses carry ``X-Runlayer-Origin`` and ``X-Request-ID`` and a JSON
# ``{"detail": ...}`` body). ``"intermediary"``: something in front of it — an
# AWS WAF IP-allowlist block, an ALB error page, a corporate proxy — which
# returns the same status codes with an HTML body and neither header. The
# distinction decides both wording (a WAF 403 is a network rejection, not a
# Runlayer policy decision) and whether a 401 may touch the credential caches
# (an intermediary 401 says nothing about the Runlayer credential).
ResponseOrigin = Literal["runlayer", "intermediary"]

# Header names the backend stamps on every error response it answers. The
# origin header's value is a fixed literal; only its presence is inspected.
ORIGIN_HEADER_NAME = "X-Runlayer-Origin"
REQUEST_ID_HEADER_NAME = "X-Request-ID"

# Statuses an intermediary can answer that would otherwise read as a Runlayer
# credential (401) or policy (403) decision. Other intermediary statuses (an
# ALB 5xx with no healthy target, a proxy 429) keep the generic
# answered-request wording, which blames the request, not Runlayer.
NETWORK_REJECT_STATUSES = frozenset({401, 403})

# Server-supplied text is rendered into the deny reason, so it is bounded and
# reduced to printable characters; a request id is only echoed when it looks
# like one.
_MAX_DETAIL_CHARS = 200
_MAX_REQUEST_ID_CHARS = 64
_REQUEST_ID_CHARS = frozenset(
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789._:-"
)


@dataclass(frozen=True, slots=True)
class FailureContext:
    """What a failed relay POST knew at the moment it failed (ENG-5197).

    ``kind``: ``"connect"`` (no connection acquired — includes pool
    exhaustion), ``"upload_timeout"`` (body still uploading when the write
    timed out), ``"upload_failed"`` (connection dropped while the body was
    uploading), ``"timeout"`` (request sent, no response in time), ``"http"``
    (non-2xx, see ``status_code``), or ``None`` (unclassified). ``payload_bytes``
    is the UTF-8 wire size of the request body; ``elapsed_s`` is time spent in
    the POST before it failed (all attempts, retries included);
    ``attempts`` is how many attempts ran before giving up (1 = no retry).
    Carried whole on ``RelayError`` so new fields never need re-threading
    through call sites.
    """

    kind: FailureKind | None = None
    payload_bytes: int | None = None
    elapsed_s: float | None = None
    status_code: int | None = None
    attempts: int = 1
    # ``kind == "http"`` only. ``None`` = unclassified (a transport without
    # headers, or callers that predate classification): status-only wording,
    # treated as Runlayer.
    origin: ResponseOrigin | None = None
    # Echoed only for a Runlayer-origin response, so support can find the
    # server-side log line. Already shape-checked and bounded.
    request_id: str | None = None
    # The backend's ``detail`` string, sanitized and bounded; never set for an
    # intermediary (its body is untrusted HTML and is not rendered).
    detail: str | None = None

    @property
    def is_network_rejection(self) -> bool:
        """An HTTP 401/403 attributed to an intermediary: worded as a network
        rejection, and no credential state may be touched."""
        return (
            self.kind == "http"
            and self.origin == "intermediary"
            and self.status_code in NETWORK_REJECT_STATUSES
        )


class ResponseOriginInfo(NamedTuple):
    origin: ResponseOrigin | None
    request_id: str | None
    detail: str | None


_UNCLASSIFIED = ResponseOriginInfo(None, None, None)
_INTERMEDIARY = ResponseOriginInfo("intermediary", None, None)


def _sanitize_detail(value: Any) -> str | None:
    if not isinstance(value, str):
        return None
    printable = "".join(c if c.isprintable() else " " for c in value)
    cleaned = " ".join(printable.split())
    if len(cleaned) > _MAX_DETAIL_CHARS:
        cleaned = cleaned[: _MAX_DETAIL_CHARS - 1].rstrip() + "…"
    return cleaned or None


def _request_id(headers: Any) -> str | None:
    value = headers.get(REQUEST_ID_HEADER_NAME)
    if not isinstance(value, str):
        return None
    value = value.strip()
    is_token = (
        0 < len(value) <= _MAX_REQUEST_ID_CHARS and set(value) <= _REQUEST_ID_CHARS
    )
    return value if is_token else None


def _error_envelope(text: Any) -> dict[str, Any] | None:
    """The backend's ``{"detail": ...}`` body, or ``None`` for anything else
    (HTML, non-object JSON, unparseable). ``detail`` may be a list (422); the
    envelope shape is what proves the origin, the caller decides what to
    render. ``json.loads`` can raise more than ``ValueError`` on hostile input
    (``RecursionError`` on deep nesting), so anything it raises means "not an
    envelope"."""
    if not isinstance(text, str) or not text:
        return None
    try:
        body = json.loads(text)
    except Exception:
        return None
    return body if isinstance(body, dict) and "detail" in body else None


def classify_response_origin(resp: Any) -> ResponseOriginInfo:
    """Decide who produced a non-2xx response.

    Runlayer when the origin header is present, or — for backends predating
    it — when the response carries a request id *and* the JSON error envelope
    (both come from the same handler, so either alone is not enough: proxies
    add request-id headers of their own, and any hop can answer JSON).
    Anything else with headers is an intermediary; a response object without
    headers at all is unclassified. Never raises: classification is garnish
    on a deny that must still be emitted, so any failure inside it also
    yields "unclassified" (the pre-classification behaviour).
    """
    headers = getattr(resp, "headers", None)
    if headers is None:
        return _UNCLASSIFIED
    try:
        request_id = _request_id(headers)
        envelope = _error_envelope(getattr(resp, "text", None))
        marked = headers.get(ORIGIN_HEADER_NAME) is not None
    except Exception:
        return _UNCLASSIFIED
    if marked or (request_id is not None and envelope is not None):
        detail = _sanitize_detail(envelope.get("detail")) if envelope else None
        return ResponseOriginInfo("runlayer", request_id, detail)
    return _INTERMEDIARY


def _safe_wire_size(payload: str | bytes) -> int | None:
    """Byte size of the body as sent (UTF-8, post-compression when compressed),
    or ``None`` if the encode itself fails.

    A compressed body is already bytes, so sizing it is O(1). The str encode
    allocates a full copy of a potentially multi-MB body; under memory
    pressure it can raise. Size is diagnostic garnish — it must never be the
    reason a deny path stops denying (fail-closed depends on ``RelayError``
    actually being raised).
    """
    try:
        if isinstance(payload, bytes):
            return len(payload)
        return len(payload.encode("utf-8"))
    except Exception:
        return None


def _classify_network_failure(exc: Exception) -> FailureKind | None:
    """Map an httpx transport exception to a ``FailureContext.kind``.

    ``WriteTimeout``/``WriteError`` both prove the body was still in flight
    (timed out vs connection dropped — the latter is the signature of the
    stalled uploads the ALB reaps). ``PoolTimeout`` means no connection was
    ever acquired (shared-client saturation), so it is "connect", not
    "timeout": only read timeouts mean the request was sent with no response
    in time. Non-httpx exceptions stay unclassified rather than guessing.
    """
    if isinstance(exc, httpx.WriteTimeout):
        return "upload_timeout"
    if isinstance(exc, httpx.WriteError):
        return "upload_failed"
    if isinstance(exc, httpx.ConnectError | httpx.ConnectTimeout | httpx.PoolTimeout):
        return "connect"
    if isinstance(exc, httpx.TimeoutException):
        return "timeout"
    return None
