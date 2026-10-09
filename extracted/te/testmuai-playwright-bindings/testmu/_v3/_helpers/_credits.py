"""Automind's credits-exhausted refusal.

Automind answers **403** with ``{"error_code": "INSUFFICIENT_CREDITS"}`` once the
organization's KaneAI credits run out. This is **terminal**: no retry can
succeed, so the run stops here rather than continuing to issue calls that will
all be refused — and, critically, the transient-retry layer must not swallow it
into repeated pointless attempts.

Ports the credits half of V2.
"""
from __future__ import annotations

import logging
from typing import Any

_log = logging.getLogger("testmu")

#: Recognisable without importing this class — the binding and the host ship
#: independently, so the host matches on the attribute rather than the type.
KANEAI_ERROR_CODE = "INSUFFICIENT_CREDITS"


class KaneAICreditsExhausted(Exception):
    """Raised when an AI call is refused because the organization is out of credits."""

    kaneai_error_code = KANEAI_ERROR_CODE


def raise_if_insufficient_credits(status: int | None, body: Any) -> None:
    """Raise when ``(status, body)`` is automind's credits refusal.

    Both halves are required: a 403 carrying any other body is an ordinary
    auth/permission failure and must keep its existing handling. A non-dict body
    is not a credits refusal.
    """
    if status != 403 or not isinstance(body, dict):
        return
    if body.get("error_code") != KANEAI_ERROR_CODE:
        return
    _log.error(
        "[KANEAI][CREDITS] ERROR: Organization KaneAI credits exhausted — "
        "AI step blocked. Recharge credits to resume runs."
    )
    raise KaneAICreditsExhausted(
        body.get("message") or "Organization KaneAI credits exhausted."
    )
