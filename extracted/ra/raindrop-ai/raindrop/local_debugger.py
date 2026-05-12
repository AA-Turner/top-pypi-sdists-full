"""Local Workshop daemon resolution for the Python SDK.

Mirrors `@raindrop-ai/core/local-debugger.ts`. Resolution precedence:
explicit kwarg → `RAINDROP_LOCAL_DEBUGGER` → `RAINDROP_WORKSHOP` →
TCP probe of localhost:5899 → disabled. Mirroring is always additive —
the local URL never replaces the cloud destination.
"""

from __future__ import annotations

import os
import socket
from typing import Any, Optional, Union
from urllib.parse import urlparse

import requests

LOCAL_DEBUGGER_ENV_VAR = "RAINDROP_LOCAL_DEBUGGER"
WORKSHOP_ENV_VAR = "RAINDROP_WORKSHOP"
DEFAULT_LOCAL_WORKSHOP_URL = "http://localhost:5899/v1/"
_PROBE_HOST = "127.0.0.1"
_PROBE_PORT = 5899
_PROBE_TIMEOUT_SECONDS = 0.1


class _Unset:
    """Distinguishes ``not provided`` (fall through to env / auto-detect) from
    ``None`` (explicit opt-out)."""

    _instance: Optional["_Unset"] = None

    def __new__(cls) -> "_Unset":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __bool__(self) -> bool:
        return False

    def __repr__(self) -> str:
        return "<UNSET>"


UNSET: Any = _Unset()


def _format_endpoint(url: str) -> Optional[str]:
    trimmed = url.strip()
    if not trimmed:
        return None
    parsed = urlparse(trimmed)
    if parsed.scheme not in ("http", "https"):
        return None
    return trimmed if trimmed.endswith("/") else f"{trimmed}/"


def _read_workshop_env() -> Union[str, bool, None]:
    raw = os.environ.get(WORKSHOP_ENV_VAR)
    if not raw:
        return None
    trimmed = raw.strip()
    if not trimmed:
        return None
    if trimmed.startswith(("http://", "https://")):
        return trimmed
    lowered = trimmed.lower()
    if lowered in {"1", "true", "yes", "on"}:
        return True
    if lowered in {"0", "false", "no", "off"}:
        return False
    return None


def _probe_default_workshop() -> bool:
    # An HTTP-level probe — not just a raw TCP connect — keeps random non-HTTP
    # listeners on 5899 (or HTTP services that aren't Workshop's `/v1/`) from
    # silently receiving mirrored telemetry. We can't fully verify daemon
    # identity here without Workshop-side cooperation; users in shared-host
    # or container environments who consider that residual risk unacceptable
    # should set `RAINDROP_WORKSHOP=0` (or pass `local_workshop_url=None`)
    # to disable auto-detect.
    url = f"http://{_PROBE_HOST}:{_PROBE_PORT}/v1/"
    try:
        response = requests.head(url, timeout=_PROBE_TIMEOUT_SECONDS, allow_redirects=False)
    except (requests.exceptions.RequestException, OSError, socket.timeout):
        return False
    return 200 <= response.status_code < 500


def resolve_local_workshop_url(
    explicit: Any = UNSET,
    *,
    auto_detect: bool = True,
) -> Optional[str]:
    if explicit is False or explicit is None:
        return None
    if isinstance(explicit, str):
        # Empty string is treated as an explicit opt-out, mirroring how
        # ``init(api_key="")`` collapses to ``None`` — passing falsy strings
        # never falls through to env / auto-detect.
        if not explicit:
            return None
        return _format_endpoint(explicit)

    env_url = os.environ.get(LOCAL_DEBUGGER_ENV_VAR)
    if env_url:
        formatted = _format_endpoint(env_url)
        if formatted:
            return formatted

    workshop_env = _read_workshop_env()
    if workshop_env is False:
        return None
    if workshop_env is True:
        return DEFAULT_LOCAL_WORKSHOP_URL
    if isinstance(workshop_env, str):
        return _format_endpoint(workshop_env)

    if auto_detect and _probe_default_workshop():
        return DEFAULT_LOCAL_WORKSHOP_URL

    return None
