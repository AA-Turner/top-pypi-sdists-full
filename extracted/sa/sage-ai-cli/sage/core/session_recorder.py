"""Item #2 — Session recorder + replay."""

from __future__ import annotations

import json
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Iterator

from sage.core.telemetry import redact_secrets

__all__ = ["SessionEvent", "SessionRecorder", "replay"]


@dataclass
class SessionEvent:
    kind: str  # "user" | "model" | "tool"
    prompt: str = ""
    model: str = ""
    output: str = ""
    tool_name: str = ""
    payload: dict = field(default_factory=dict)
    ts: float = field(default_factory=time.time)


def _root() -> Path:
    p = Path.home() / ".sage" / "sessions"
    p.mkdir(parents=True, exist_ok=True)
    return p


@dataclass
class SessionRecorder:
    session_id: str

    @property
    def path(self) -> Path:
        return _root() / f"{self.session_id}.replay"

    def record(self, event: SessionEvent) -> None:
        clean = SessionEvent(
            kind=event.kind,
            prompt=redact_secrets(event.prompt or ""),
            model=event.model,
            output=redact_secrets(event.output or ""),
            tool_name=event.tool_name,
            payload=event.payload or {},
            ts=event.ts,
        )
        try:
            with self.path.open("a", encoding="utf-8") as fh:
                fh.write(json.dumps(asdict(clean)) + "\n")
        except OSError:
            pass

    def read(self) -> Iterator[SessionEvent]:
        if not self.path.exists():
            return iter([])
        events: list[SessionEvent] = []
        for line in self.path.read_text("utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                d = json.loads(line)
                events.append(SessionEvent(**d))
            except (json.JSONDecodeError, TypeError):
                continue
        return iter(events)


def replay(*, session_id: str) -> Iterator[SessionEvent]:
    return SessionRecorder(session_id=session_id).read()
