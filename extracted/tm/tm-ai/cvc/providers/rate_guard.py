"""Cross-session rate-limit guard.

Persists per-provider rate-limit state to ~/.cvc/rate_limits/{provider}.json
so that 429s observed in one session are respected by subsequent sessions.

Atomic file writes via tempfile + rename. Coarse-grained file locking via
fcntl on POSIX (best-effort — falls back gracefully if unavailable).

Usage:
    from cvc.providers.rate_guard import (
        check_rate_limit, record_429, clear_rate_limit
    )

    if not check_rate_limit("anthropic"):
        raise RuntimeError("Provider locked out — try later")
    try:
        do_request(...)
    except RateLimit:
        record_429("anthropic", retry_after=60)
"""
from __future__ import annotations

import json
import logging
import os
import tempfile
import time
from pathlib import Path
from typing import Any, Optional

logger = logging.getLogger(__name__)

# ── Storage ──────────────────────────────────────────────────────────

_BASE_DIR = Path(os.path.expanduser("~/.cvc/rate_limits"))


def _state_path(provider: str) -> Path:
    safe = "".join(c if c.isalnum() or c in "-_" else "_" for c in provider.lower())
    return _BASE_DIR / f"{safe}.json"


def _ensure_dir() -> None:
    _BASE_DIR.mkdir(parents=True, exist_ok=True)


# ── Atomic read/write ────────────────────────────────────────────────

def _read(provider: str) -> dict[str, Any]:
    p = _state_path(provider)
    if not p.exists():
        return {}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:
        logger.warning("rate_guard: failed to read %s: %s", p, e)
        return {}


def _write(provider: str, payload: dict[str, Any]) -> None:
    _ensure_dir()
    p = _state_path(provider)
    fd, tmp_path = tempfile.mkstemp(prefix=p.name + ".", suffix=".tmp", dir=str(p.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            json.dump(payload, fh, indent=2)
        os.replace(tmp_path, p)
    except Exception:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise


# ── Locking (best-effort POSIX) ──────────────────────────────────────

class _FileLock:
    def __init__(self, provider: str):
        self.path = _state_path(provider).with_suffix(".lock")
        self.fh = None

    def __enter__(self):
        _ensure_dir()
        self.fh = open(self.path, "w")
        try:
            import fcntl
            fcntl.flock(self.fh.fileno(), fcntl.LOCK_EX)
        except Exception:
            pass  # best-effort
        return self

    def __exit__(self, *a):
        try:
            import fcntl
            fcntl.flock(self.fh.fileno(), fcntl.LOCK_UN)
        except Exception:
            pass
        try:
            self.fh.close()
        except Exception:
            pass


# ── Public API ───────────────────────────────────────────────────────

def check_rate_limit(provider: str, *, now: Optional[float] = None) -> bool:
    """Return True if it's safe to make a request to provider."""
    state = _read(provider)
    until = state.get("locked_until", 0)
    return (now or time.time()) >= until


def time_until_unlocked(provider: str, *, now: Optional[float] = None) -> float:
    """Return seconds until provider is unlocked. 0 if unlocked."""
    state = _read(provider)
    until = state.get("locked_until", 0)
    delta = until - (now or time.time())
    return max(0.0, delta)


def record_429(provider: str, *,
               retry_after: Optional[int] = None,
               default_lockout_seconds: int = 60) -> None:
    """Record a 429 from `provider`. Locks it out for retry_after or default seconds.

    Tracks consecutive 429s and applies exponential backoff up to 1h cap.
    """
    with _FileLock(provider):
        state = _read(provider)
        consecutive = state.get("consecutive_429s", 0) + 1

        if retry_after and retry_after > 0:
            lockout = min(retry_after, 3600)
        else:
            lockout = min(default_lockout_seconds * (2 ** (consecutive - 1)), 3600)

        state.update({
            "provider": provider,
            "locked_until": time.time() + lockout,
            "consecutive_429s": consecutive,
            "last_429_at": time.time(),
            "last_lockout_seconds": lockout,
        })
        _write(provider, state)
        logger.warning("[rate_guard] %s locked out for %ds (consecutive=%d)",
                       provider, lockout, consecutive)


def record_success(provider: str) -> None:
    """Reset the 429 counter on a successful request."""
    state = _read(provider)
    if state.get("consecutive_429s", 0) == 0:
        return  # nothing to clear
    with _FileLock(provider):
        state = _read(provider)
        state["consecutive_429s"] = 0
        state["last_success_at"] = time.time()
        state.pop("locked_until", None)
        _write(provider, state)


def clear_rate_limit(provider: str) -> None:
    """Manually clear the rate-limit state for a provider."""
    p = _state_path(provider)
    if p.exists():
        p.unlink()


def status() -> dict[str, dict[str, Any]]:
    """Return rate-limit state for ALL providers in the directory."""
    if not _BASE_DIR.exists():
        return {}
    out: dict[str, dict[str, Any]] = {}
    for p in _BASE_DIR.glob("*.json"):
        provider = p.stem
        try:
            out[provider] = json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            continue
    return out


__all__ = [
    "check_rate_limit",
    "time_until_unlocked",
    "record_429",
    "record_success",
    "clear_rate_limit",
    "status",
]
