"""One ``POST`` to the VSS verify endpoint, stdlib only.

Normative source: ``VLM-VERIFY-INTERFACES.md`` §2 ("stdlib ``urllib.request`` + ``json``
only -- httpx is NOT a runtime dependency") and ``alert-verification-api.md`` §4-§5.

This module does **one** request and reports what came back.  It does not retry, sleep or
decide what a status code means -- that policy lives in
:mod:`matrice_analytics.engine.verify.worker`, so the whole retry table is in one place.

Every failure mode is folded into :class:`HttpReply` rather than raised, because the only
caller is a background thread whose job is to turn *every* outcome into a
:class:`~matrice_analytics.engine.verify.worker.Verdict`:

* a response of any status -- ``code`` is the HTTP status, ``payload`` the decoded JSON
  (``None`` when the body is not JSON);
* no response at all (refused, reset, DNS, timeout) -- ``code`` is ``None``.
"""

from __future__ import annotations

import http.client
import json
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any

__all__ = ["HttpReply", "post_json"]

#: A verify response is a few KB even with 8 frames of evidence; anything past this is not
#: a verify response, and reading it unbounded would let a misrouted URL exhaust memory.
_MAX_BODY_BYTES = 1 << 20


@dataclass(frozen=True, slots=True)
class HttpReply:
    """What one request produced.

    Attributes:
        code: The HTTP status, or ``None`` when no response arrived (transport error or
            timeout).
        payload: The decoded JSON body, or ``None`` when there was none or it did not parse.
        message: A short human-readable description for logs and ``Verdict.reason``: the
            error envelope's ``message`` (plus ``trackingCode``) for a non-2xx, the exception
            text for a transport failure, empty for a well-formed 200.
    """

    code: int | None
    payload: Any
    message: str


def post_json(url: str, body: dict[str, Any], timeout_s: float) -> HttpReply:
    """``POST`` ``body`` as JSON to ``url`` and return what came back; never raises.

    Args:
        url: An ``http://`` or ``https://`` URL.  The scheme is validated by the caller when
            the worker is built (``WorkerSettings.from_env``); this function trusts it.
        body: A JSON-serialisable request body.
        timeout_s: Socket timeout for connect and for each read.

    Returns:
        The reply; see :class:`HttpReply`.

    Raises:
        TypeError: ``body`` is not JSON-serialisable -- a caller bug, raised rather than
            folded so it is not mistaken for a network failure and retried.
    """
    data = json.dumps(body, separators=(",", ":")).encode("utf-8")
    request = urllib.request.Request(  # noqa: S310 - scheme restricted to http(s) at build
        url,
        data=data,
        headers={"Content-Type": "application/json", "Accept": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout_s) as response:  # noqa: S310
            raw = response.read(_MAX_BODY_BYTES)
            return HttpReply(code=response.status, payload=_decode(raw), message="")
    except urllib.error.HTTPError as exc:
        # A non-2xx *is* a response: read the Matrice error envelope for the message.
        with exc:
            payload = _decode(exc.read(_MAX_BODY_BYTES))
        return HttpReply(code=exc.code, payload=payload, message=_envelope_message(exc, payload))
    except (urllib.error.URLError, http.client.HTTPException, OSError) as exc:
        # URLError: refused / DNS / TLS.  OSError covers TimeoutError and a reset mid-read;
        # HTTPException a malformed status line or a server that closed without replying.
        return HttpReply(code=None, payload=None, message=f"{type(exc).__name__}: {exc}")


def _decode(raw: bytes) -> Any:
    """Parse ``raw`` as JSON, or ``None`` when it is empty or not JSON."""
    if not raw:
        return None
    try:
        return json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, ValueError):
        return None


def _envelope_message(exc: urllib.error.HTTPError, payload: Any) -> str:
    """``"<message> (trackingCode <code>)"`` from the error envelope, else the reason phrase."""
    if isinstance(payload, dict):
        message = payload.get("message")
        tracking = payload.get("trackingCode")
        if isinstance(message, str) and message:
            return f"{message} (trackingCode {tracking})" if tracking else message
    return f"HTTP {exc.code} {exc.reason}"
