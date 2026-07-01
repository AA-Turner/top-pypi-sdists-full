"""Trajectory recording — one JSONL line per turn."""
from __future__ import annotations

import json
import os
import threading
import time
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class TurnRecord:
    turn: int
    timestamp: float
    messages: List[Dict[str, Any]] = field(default_factory=list)
    tool_calls: List[Dict[str, Any]] = field(default_factory=list)
    tool_results: List[Dict[str, Any]] = field(default_factory=list)
    prompt_tokens: int = 0
    completion_tokens: int = 0
    cache_read_tokens: int = 0
    model: str = ""
    provider: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)


class TrajectoryRecorder:
    def __init__(self, path: str | Path, *, enabled: bool = True):
        self.path = Path(os.path.expanduser(str(path)))
        self.enabled = bool(enabled)
        self._lock = threading.Lock()
        self._turn = 0
        if self.enabled:
            self.path.parent.mkdir(parents=True, exist_ok=True)

    def record(
        self,
        *,
        messages: Optional[List[Dict[str, Any]]] = None,
        tool_calls: Optional[List[Dict[str, Any]]] = None,
        tool_results: Optional[List[Dict[str, Any]]] = None,
        prompt_tokens: int = 0,
        completion_tokens: int = 0,
        cache_read_tokens: int = 0,
        model: str = "",
        provider: str = "",
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Optional[TurnRecord]:
        if not self.enabled:
            return None
        with self._lock:
            self._turn += 1
            rec = TurnRecord(
                turn=self._turn,
                timestamp=time.time(),
                messages=list(messages or []),
                tool_calls=list(tool_calls or []),
                tool_results=list(tool_results or []),
                prompt_tokens=int(prompt_tokens),
                completion_tokens=int(completion_tokens),
                cache_read_tokens=int(cache_read_tokens),
                model=model or "",
                provider=provider or "",
                metadata=dict(metadata or {}),
            )
            try:
                with self.path.open("a", encoding="utf-8") as f:
                    f.write(json.dumps(asdict(rec), ensure_ascii=False, default=str) + "\n")
            except OSError:
                pass
            return rec

    def disable(self) -> None:
        self.enabled = False


__all__ = ["TurnRecord", "TrajectoryRecorder"]
