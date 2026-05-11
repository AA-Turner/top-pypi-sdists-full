"""Item #18 — Online learning from corrections."""

from __future__ import annotations

import json
import time
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

__all__ = ["CorrectionLog", "aggregate_corrections"]


def _root() -> Path:
    p = Path.home() / ".sage" / "corrections"
    p.mkdir(parents=True, exist_ok=True)
    return p


@dataclass
class CorrectionLog:
    session_id: str

    @property
    def path(self) -> Path:
        return _root() / f"{self.session_id}.jsonl"

    def record_undo(self, *,
                    prompt: str,
                    bad_output: str,
                    accepted_alternative: str | None = None,
                    validator_signal: str | None = None) -> None:
        rec = {
            "ts": time.time(),
            "session": self.session_id,
            "prompt": prompt,
            "bad_output": bad_output[:4000],
            "accepted_alternative": (accepted_alternative or "")[:4000],
            "validator_signal": validator_signal,
        }
        with self.path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(rec) + "\n")

    def read(self) -> list[dict]:
        if not self.path.exists():
            return []
        out: list[dict] = []
        for line in self.path.read_text("utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                continue
        return out


def aggregate_corrections() -> dict[str, int]:
    counter: Counter = Counter()
    root = _root()
    if not root.is_dir():
        return {}
    for path in root.glob("*.jsonl"):
        for line in path.read_text("utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                d = json.loads(line)
                sig = d.get("validator_signal")
                if sig:
                    counter[sig] += 1
            except json.JSONDecodeError:
                continue
    return dict(counter)
