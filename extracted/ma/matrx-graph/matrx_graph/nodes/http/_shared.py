"""Shared helpers for the http.* node pack.

Single place for the response payload shape, content-type decoding, and
size-cap defense. Any node that calls httpx goes through ``build_response``
so the emitted output is stable regardless of endpoint.

Node Result System: ``HttpResponse`` is the SUCCESS PAYLOAD T inside
``NodeResult[HttpResponse]``. Semantics: receiving an HTTP response — any
status, including 4xx/5xx — is node SUCCESS (the node's job is "make the
request and report the response"; branch on ``status``). A TRANSPORT failure
(DNS, connect, TLS, timeout) is a node Failure built by
``transport_failure(...)`` — route it with an ERROR edge or let it park.
"""

from __future__ import annotations

from typing import Any

from pydantic import Field, JsonValue

from matrx_graph.content_ir.model import KindModel
from matrx_graph.secrets import (
    SecretRef,
    SecretUnavailable,
    SecretValues,
    contains_secret_ref,
    resolve_secret_refs,
)
from matrx_graph.types.result import Failure, failure

#: A request text value: the text itself, or ``{"$secret": "<name>"}`` — a stored secret used
#: for the outgoing request only (never echoed in the output, events, logs or errors).
TextOrSecret = str | SecretRef


class HttpResponse(KindModel, kind="http_response"):
    """Canonical HTTP response payload emitted by http.* nodes.

    Downstream routing branches on ``status`` (e.g. ``inputs['status'] < 300``
    on a conditional edge). Transport-level failures never produce this shape
    — they are node Failures (``code='http_transport_error'``).
    """

    status: int = Field(description="HTTP status code (e.g. 200, 404).")
    url: str = Field(description="The final URL the request resolved to, after any redirects.")
    headers: dict[str, str] = Field(
        default_factory=dict, description="Response headers, with lower-cased keys."
    )
    body: JsonValue = Field(
        default=None,
        description="Parsed JSON when the content-type is JSON-like; the decoded "
        "text otherwise. Use this for structured downstream steps.",
    )
    text: str = Field(
        default="",
        description="Raw response body as text, truncated to the max_bytes cap.",
    )
    content_type: str = Field(default="", description="The response's Content-Type header value.")
    elapsed_ms: int = Field(
        default=0, description="Wall-clock time for the request, in milliseconds."
    )


_DEFAULT_MAX_BYTES = 1_000_000  # 1 MB — guardrail against checkpoint blowups


def _decode_body(resp: Any, max_bytes: int) -> tuple[str, Any, str]:
    """Return (text, parsed_body, content_type).

    Truncates text to ``max_bytes`` to keep checkpoints from ballooning.
    JSON parsing is best-effort; on failure ``parsed`` falls back to text.
    """
    content_type = resp.headers.get("content-type", "")

    raw_bytes = resp.content or b""
    if len(raw_bytes) > max_bytes:
        raw_bytes = raw_bytes[:max_bytes]

    try:
        text = raw_bytes.decode("utf-8", errors="replace")
    except Exception:
        text = repr(raw_bytes)

    parsed: Any = text
    if "json" in content_type.lower():
        try:
            # Prefer httpx's own json parser so we stay consistent with
            # content-negotiation; fall back to the raw-bytes attempt.
            parsed = resp.json()
        except Exception:
            import json as _json

            try:
                parsed = _json.loads(text)
            except Exception:
                parsed = text
    return text, parsed, content_type


def build_response_from_httpx(resp: Any, url: str, elapsed_ms: int, max_bytes: int) -> HttpResponse:
    text, body, ct = _decode_body(resp, max_bytes)
    return HttpResponse(
        status=resp.status_code,
        url=url,
        headers={k.lower(): v for k, v in resp.headers.items()},
        body=body,
        text=text,
        content_type=ct,
        elapsed_ms=elapsed_ms,
    )


def outbound_client(*, timeout: float, follow_redirects: bool = False) -> Any:
    """The ONE client every http.* node sends through.

    Its transport refuses any request (and any redirect hop) whose host is
    not a public address, and connects to the exact IP it checked — the
    person who builds the workflow controls the URL, the server's own
    network is never reachable through it (matrx_utils.outbound_guard).
    """
    from matrx_utils.outbound_guard import public_only_client

    return public_only_client(timeout=timeout, follow_redirects=follow_redirects)


def refused_failure(url: str, exc: Exception, elapsed_ms: int) -> Failure:
    """The URL (or a redirect hop) pointed into a private network — never retried."""
    return failure(
        "outbound_address_refused",
        str(exc),
        details={"url": url, "elapsed_ms": elapsed_ms},
    )


def transport_failure(url: str, error: str, elapsed_ms: int) -> Failure:
    """A request that never produced an HTTP response — node Failure."""
    return failure(
        "http_transport_error",
        error,
        details={"url": url, "elapsed_ms": elapsed_ms},
    )


async def resolve_request_secrets(ctx: Any, parts: dict[str, Any]) -> tuple[dict[str, Any], SecretValues] | Failure:
    """Replace every ``{"$secret": name}`` in the request parts with its value, for sending only.

    Returns the resolved parts and the values used (redact everything the step hands back with
    ``found.redact(...)``), or a Failure naming the secret — never its value."""
    found = SecretValues()
    if not contains_secret_ref(parts):
        return parts, found
    user_id = getattr(ctx, "user_id", None) if ctx is not None else None
    organization_id = getattr(ctx, "organization_id", None) if ctx is not None else None
    workflow_id = getattr(ctx, "workflow_id", None) if ctx is not None else None
    try:
        resolved = await resolve_secret_refs(
            parts, user_id=user_id, organization_id=organization_id, found=found,
            workflow_id=str(workflow_id) if workflow_id else None,
        )
    except SecretUnavailable as exc:
        return failure("secret_unavailable", str(exc), details={"secrets_used": found.names})
    return resolved, found


__all__ = [
    "HttpResponse",
    "TextOrSecret",
    "resolve_request_secrets",
    "_DEFAULT_MAX_BYTES",
    "build_response_from_httpx",
    "outbound_client",
    "refused_failure",
    "transport_failure",
]
