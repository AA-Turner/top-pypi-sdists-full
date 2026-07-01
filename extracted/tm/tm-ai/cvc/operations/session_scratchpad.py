"""
cvc.operations.session_scratchpad — Per-session JSONL log of turns.

The scratchpad is where CVC writes everything it saw and everything it
produced during a chat session.  It's the raw material for:

* The Phase 3 observer (aggregates turn stats into cognome).
* The Phase 4 cross-session handoff (replay of the last scratchpad).
* Later training data for L2/L3 (soft-prompt + LoRA compressors).

File layout::

    .cvc/sessions/
        <session_id>.jsonl  ← append-only, one event per line

Event schema (JSON, one per line)::

    {"ts": <float>, "kind": "user" | "assistant" | "engram" | "response",
     "session_id": "<id>", ...event-specific fields...}

Design invariants
-----------------
* **Never blocks**.  All writes are fire-and-forget.  If the disk is
  full or the file is locked we drop the event and log a debug note.
* **Never raises**.  The scratchpad is instrumentation — it cannot take
  down a user chat.
* **No schema lock-in**.  Events are JSONL with arbitrary extra keys so
  Phase 4+ can extend without migrations.
"""

from __future__ import annotations

import asyncio
import json
import logging
import secrets
import threading
import time
from pathlib import Path
from typing import Any

logger = logging.getLogger("cvc.operations.session_scratchpad")

# One directory per workspace.  Session files live here.
SESSIONS_DIR_NAME = "sessions"


def _new_session_id() -> str:
    # e.g. 20260419-141055-ab12cd34  (local-sortable + unique)
    stamp = time.strftime("%Y%m%d-%H%M%S", time.localtime())
    return f"{stamp}-{secrets.token_hex(4)}"


class SessionScratchpad:
    """
    Append-only JSONL log for a single chat session.

    Typical lifecycle (managed by :class:`CognomeRuntime`)::

        sp = SessionScratchpad(cvc_root)
        await sp.record_user(query, engram=engram)
        await sp.record_response(text, usage={"input_tokens": 120, ...})
    """

    def __init__(
        self,
        cvc_root: Path,
        *,
        session_id: str | None = None,
    ) -> None:
        self._root = Path(cvc_root)
        self._session_id = session_id or _new_session_id()
        self._dir = self._root / SESSIONS_DIR_NAME
        # Ensure directory exists (non-fatal if we can't create it).
        try:
            self._dir.mkdir(parents=True, exist_ok=True)
        except Exception as exc:
            logger.debug("scratchpad: cannot create %s (%s)", self._dir, exc)
        # Cross-thread write lock.  We use threading.Lock (not asyncio)
        # because write() runs via to_thread and may race CLI ctrl-c.
        self._write_lock = threading.Lock()

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def session_id(self) -> str:
        return self._session_id

    @property
    def path(self) -> Path:
        return self._dir / f"{self._session_id}.jsonl"

    # ------------------------------------------------------------------
    # Record helpers
    # ------------------------------------------------------------------

    async def record_user(
        self,
        query: str,
        *,
        engram_hash: str | None = None,
        engram_tokens: int | None = None,
        noeme_count: int | None = None,
        provider: str = "",
        model: str = "",
        branch: str | None = None,
    ) -> None:
        """Record a user turn + the Engram we injected for it."""
        await self._append({
            "kind": "user",
            "query": query,
            "engram_hash": engram_hash,
            "engram_tokens": engram_tokens,
            "noeme_count": noeme_count,
            "provider": provider,
            "model": model,
            "branch": branch,
        })

    async def record_response(
        self,
        text: str,
        *,
        engram_hash: str | None = None,
        usage: dict[str, Any] | None = None,
        duration_ms: float | None = None,
    ) -> None:
        """Record an assistant turn and the usage that came back."""
        await self._append({
            "kind": "assistant",
            "text": text[:2000],  # guard against runaway completions
            "engram_hash": engram_hash,
            "usage": usage or {},
            "duration_ms": duration_ms,
        })

    async def record_event(self, kind: str, **fields: Any) -> None:
        """Escape hatch for arbitrary event kinds (observer, handoff, etc.)."""
        payload = {"kind": kind}
        payload.update(fields)
        await self._append(payload)

    def record_event_sync(self, kind: str, **fields: Any) -> None:
        """
        Non-async alternative for callers outside an event loop.
        Runs the write directly without scheduling.
        """
        payload = {"kind": kind}
        payload.update(fields)
        self._write_line(payload)

    # ------------------------------------------------------------------
    # Read helpers
    # ------------------------------------------------------------------

    def read_all(self, limit: int | None = None) -> list[dict[str, Any]]:
        """Return all events for this session (most-recent last)."""
        path = self.path
        if not path.exists():
            return []
        out: list[dict[str, Any]] = []
        try:
            with path.open("r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        out.append(json.loads(line))
                    except Exception:
                        continue
        except Exception as exc:
            logger.debug("scratchpad read failed: %s", exc)
            return []
        if limit is not None and limit > 0:
            return out[-limit:]
        return out

    # ------------------------------------------------------------------
    # Internals
    # ------------------------------------------------------------------

    async def _append(self, payload: dict[str, Any]) -> None:
        # Run the blocking file write on the default executor so we
        # never block the event loop.  Never raise.
        try:
            await asyncio.to_thread(self._write_line, payload)
        except Exception as exc:
            logger.debug("scratchpad write failed: %s", exc)

    def _write_line(self, payload: dict[str, Any]) -> None:
        enriched = {
            "ts": time.time(),
            "session_id": self._session_id,
        }
        enriched.update(payload)
        line = json.dumps(enriched, ensure_ascii=False, default=str)
        try:
            with self._write_lock, self.path.open("a", encoding="utf-8") as f:
                f.write(line + "\n")
        except Exception as exc:
            logger.debug("scratchpad write I/O failed: %s", exc)


# ---------------------------------------------------------------------------
# Convenience: list known sessions for a workspace
# ---------------------------------------------------------------------------

def list_sessions(cvc_root: Path) -> list[str]:
    """Return session IDs in *cvc_root*/sessions, newest first."""
    d = Path(cvc_root) / SESSIONS_DIR_NAME
    if not d.exists():
        return []
    try:
        files = sorted(d.glob("*.jsonl"), key=lambda p: p.stat().st_mtime, reverse=True)
        return [f.stem for f in files]
    except Exception:
        return []
