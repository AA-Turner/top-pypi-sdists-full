"""Local-only auth + path safety for the Bingo web IDE.

Bingo reads/writes files and drives a pentest engine, so the web surface is a
local RCE target if exposed. We bind to loopback, mint a random per-run session
token, and require it on every request. Paths from the browser are confined to
the workspace root.
"""
from __future__ import annotations

import hmac
import secrets
from pathlib import Path

# One token per server process. Printed in the launch URL; the SPA echoes it
# back on every /api and /ws call. Not persisted anywhere.
SESSION_TOKEN: str = secrets.token_urlsafe(32)


def verify_token(candidate: str | None) -> bool:
    """Constant-time compare of a presented token against the session token."""
    if not candidate:
        return False
    return hmac.compare_digest(candidate, SESSION_TOKEN)


def safe_resolve(root: Path, rel: str) -> Path | None:
    """Resolve ``rel`` under ``root``; return None on any escape attempt.

    Blocks absolute paths, ``..`` traversal, and symlink escapes by requiring
    the resolved real path to stay inside the resolved root.
    """
    if rel is None:
        return None
    try:
        root_r = root.resolve()
        # An absolute rel would override root in `/`; reject outright.
        if Path(rel).is_absolute():
            return None
        target = (root_r / rel).resolve()
        target.relative_to(root_r)  # raises ValueError if outside
        return target
    except (ValueError, OSError):
        return None
