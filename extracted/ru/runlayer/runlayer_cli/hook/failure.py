"""Relay failure classification shared by the relay and deny-message rendering.

Extracted from ``hook/relay.py`` (ENG-5365) so ``messages.py`` can import the
context type at runtime without pulling the whole relay module. Keep this
module stdlib + httpx only.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

import httpx

# Closed vocabulary for FailureContext.kind. messages._unreachable_cause has a
# rendering branch per kind (contract-tested); a kind added here without one
# falls back to the generic legacy message.
FailureKind = Literal["connect", "upload_timeout", "upload_failed", "timeout", "http"]


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
