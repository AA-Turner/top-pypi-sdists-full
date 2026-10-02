"""One stderr line when the server says this client is no longer supported.

Every server response to a client that reports its version carries
``X-Probe-Client-Status: ok|update|unsupported`` and ``X-Probe-Min-Version``
(research-os plan (i)). Only ``unsupported`` -- below the manifest ``min`` -- is
worth interrupting anyone for, and only once: a training loop makes thousands
of requests, and a notice repeated on each is one people learn to filter.

The server never refuses a request by version (no 426), so this is advice, not
an error. It must never raise: it runs on every response, beside a training
loop. Stdlib-only for the same reason.
"""

from __future__ import annotations

import sys
import threading
from collections.abc import Mapping

from ..client_headers import CLIENT_VERSION_HEADER
from .session_marker import WIZARD_HINT

CLIENT_STATUS_HEADER = "X-Probe-Client-Status"
MIN_VERSION_HEADER = "X-Probe-Min-Version"
UNSUPPORTED = "unsupported"

#: How to upgrade depends on how this process was installed, which the
#: transport's surface says. `import probe` in a training script lives in the
#: script's own environment, so pip; the CLI (and the local MCP server it runs)
#: is a `uv tool` install that the wizard updates -- the same pointer the
#: SessionStart hook hands out.
_UPGRADE_BY_SURFACE = {"sdk": "upgrade with `pip install -U probe-research`"}
_CLI_UPGRADE = f"to upgrade, {WIZARD_HINT}"

_lock = threading.Lock()
_noticed = False


def notice(
    response_headers: Mapping[str, str],
    sent_headers: Mapping[str, str],
    surface: str = "sdk",
) -> None:
    """Print the one line, the first time a response says ``unsupported``."""
    global _noticed
    try:
        if _noticed or response_headers.get(CLIENT_STATUS_HEADER) != UNSUPPORTED:
            return
        with _lock:
            if _noticed:
                return
            _noticed = True
        version = sent_headers.get(CLIENT_VERSION_HEADER) or "this version"
        minimum = _printable(response_headers.get(MIN_VERSION_HEADER))
        floor = f" (oldest supported: {minimum})" if minimum else ""
        upgrade = _UPGRADE_BY_SURFACE.get(surface, _CLI_UPGRADE)
        sys.stderr.write(
            f"probe: probe-research {version} is no longer supported by this Probe "
            f"server{floor}; {upgrade}.\n"
        )
    except Exception:  # noqa: BLE001 -- advice may never become a failure
        pass


def _printable(value: str | None) -> str | None:
    """A server-sent version, only if it is short and plainly a version."""
    if not value or len(value) > 64:
        return None
    if not all(ch.isalnum() or ch in ".-+" for ch in value):
        return None
    return value


def _reset_for_tests() -> None:
    global _noticed
    _noticed = False
