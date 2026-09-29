"""The request-level block list for press clips — data, not code.

The tokens live in ``blocked_hosts.json`` beside this file. A hostname is blocked
when a token occurs in it followed by a dot OR the end of the hostname,
case-insensitive. So ``cdn.taboola.com`` is blocked and ``piano-lessons.com``
is not (the token is ``piano.io``).

One deliberate deviation from upstream: its regex was ``(tok1|…)\\.`` — a dot
REQUIRED after the token — so the two tokens that end a hostname
(``spot.im``, ``piano.io``) never matched ``launcher.spot.im`` or
``cdn.piano.io``. The spec names spot.im/openweb and piano as blocked, so the
match accepts end-of-host too.
"""

from __future__ import annotations

import json
import re
from functools import lru_cache
from pathlib import Path

_DATA = Path(__file__).with_name("blocked_hosts.json")


def _load_tokens() -> tuple[str, ...]:
    tokens = json.loads(_DATA.read_text())["tokens"]
    if not tokens or not all(isinstance(t, str) and t.strip() for t in tokens):
        raise ValueError(f"{_DATA} must hold a non-empty list of host tokens")
    return tuple(t.strip() for t in tokens)


BLOCKED_HOST_TOKENS: tuple[str, ...] = _load_tokens()


@lru_cache(maxsize=1)
def blocked_host_pattern() -> re.Pattern[str]:
    return re.compile("(" + "|".join(re.escape(t) for t in BLOCKED_HOST_TOKENS) + r")(\.|$)", re.I)


def is_blocked_host(hostname: str) -> bool:
    return bool(hostname) and blocked_host_pattern().search(hostname) is not None


__all__ = ["BLOCKED_HOST_TOKENS", "blocked_host_pattern", "is_blocked_host"]
