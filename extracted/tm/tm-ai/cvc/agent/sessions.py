"""
cvc.agent.sessions — Session management for the CVC Agent.

Tracks named sessions with metadata, supports resume, fork, and rewind.
Sessions are stored as JSON in ~/.cvc/sessions/.
"""

from __future__ import annotations

import hashlib
import json
import logging
import os
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

logger = logging.getLogger("cvc.agent.sessions")


def _sessions_dir() -> Path:
    """Return the global sessions directory (~/.cvc/sessions/)."""
    d = Path.home() / ".cvc" / "sessions"
    d.mkdir(parents=True, exist_ok=True)
    return d


@dataclass
class Session:
    """A single agent session."""
    id: str
    workspace: str
    provider: str = ""
    model: str = ""
    name: str = ""
    created_at: float = 0.0
    last_active: float = 0.0
    turn_count: int = 0
    branch: str = "main"
    cost_summary: str = ""
    cost_data: dict = field(default_factory=dict)

    def save(self) -> None:
        path = _sessions_dir() / f"{self.id}.json"
        path.write_text(json.dumps(asdict(self), indent=2), encoding="utf-8")

    def save_cost(self, cost_tracker) -> None:
        """Persist cost tracker state into this session."""
        self.cost_data = cost_tracker.to_dict()
        self.cost_summary = cost_tracker.format_summary()

    def restore_cost_tracker(self):
        """Restore a CostTracker from persisted cost_data."""
        from cvc.agent.cost_tracker import CostTracker
        if self.cost_data:
            return CostTracker.from_dict(self.cost_data)
        return None

    @classmethod
    def load(cls, session_id: str) -> Session | None:
        path = _sessions_dir() / f"{session_id}.json"
        if not path.exists():
            return None
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})
        except Exception as e:
            logger.debug("Failed to load session %s: %s", session_id, e)
            return None


def create_session(
    workspace: str,
    provider: str = "",
    model: str = "",
    branch: str = "main",
) -> Session:
    """Create a new session with a unique ID."""
    sid = hashlib.sha256(
        f"{workspace}:{time.time()}:{os.getpid()}".encode()
    ).hexdigest()[:16]
    session = Session(
        id=sid,
        workspace=str(workspace),
        provider=provider,
        model=model,
        created_at=time.time(),
        last_active=time.time(),
        branch=branch,
    )
    session.save()
    return session


def list_sessions(workspace: str | None = None) -> list[Session]:
    """List all sessions, optionally filtered by workspace. Sorted by last_active desc."""
    sessions = []
    for f in _sessions_dir().glob("*.json"):
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
            s = Session(**{k: v for k, v in data.items() if k in Session.__dataclass_fields__})
            if workspace and s.workspace != str(workspace):
                continue
            sessions.append(s)
        except Exception:
            continue
    sessions.sort(key=lambda s: s.last_active, reverse=True)
    return sessions


def find_session(id_or_name: str, workspace: str | None = None) -> Session | None:
    """Find a session by ID prefix or name."""
    for s in list_sessions(workspace):
        if s.id.startswith(id_or_name) or s.name == id_or_name:
            return s
    return None


def get_most_recent_session(workspace: str) -> Session | None:
    """Get the most recently active session for a workspace."""
    sessions = list_sessions(workspace)
    return sessions[0] if sessions else None


def fork_session(source: Session, name: str = "") -> Session:
    """Fork a new session from an existing one."""
    new = create_session(
        workspace=source.workspace,
        provider=source.provider,
        model=source.model,
        branch=source.branch,
    )
    new.name = name or f"fork-of-{source.name or source.id[:8]}"
    new.save()
    return new
