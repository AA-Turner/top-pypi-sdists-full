from __future__ import annotations

"""Simple timestamped reflection log with mood adaptation."""

from dataclasses import dataclass, field
from typing import List, Optional
from pathlib import Path
import hashlib
import json
import time

SURFACE_TAGS = {"spiral_flip", "observer_effect", "notable", "humor"}

MOOD_FROM_TRAIT = {
    "Joker": "playful",
    "Trickster": "sly",
    "Scientist": "curious",
    "Schrodinger": "paradox",
    "Teacher": "helpful",
}


def mood_from_traits(traits: List[str]) -> str:
    for t in traits:
        if t in MOOD_FROM_TRAIT:
            return MOOD_FROM_TRAIT[t]
    return "neutral"


@dataclass
class ReflectionEntry:
    timestamp: float
    message: str
    tags: List[str]
    mood: str = "neutral"


@dataclass
class ReflectionLog:
    pace: float = 0.0
    rate: float = 0.0
    state: str = ""
    spin: str = ""
    observer: Optional[str] = None
    entries: List[ReflectionEntry] = field(default_factory=list)

    def compute_hash(self) -> str:
        """Return short fingerprint from pace, rate, state and spin."""
        data = f"{self.pace}:{self.rate}:{self.state}:{self.spin}"
        return hashlib.sha1(data.encode("utf-8")).hexdigest()[:8]

    @property
    def spiral_hash(self) -> str:
        return self.compute_hash()

    def dest_path(self, base: Path, seeds: List[str]) -> Path:
        """Determine file path for this log."""
        path = base
        if self.observer:
            path = path / self.observer
        name = seeds[0] if len(seeds) == 1 else self.spiral_hash
        path.mkdir(parents=True, exist_ok=True)
        return path / f"{name}.jsonl"

    def flush(self, base: Path, seeds: List[str]) -> Path:
        """Write log entries to disk and clear memory."""
        path = self.dest_path(base, seeds)
        with path.open("a", encoding="utf-8") as fh:
            for e in self.entries:
                fh.write(json.dumps(e.__dict__) + "\n")
        self.entries.clear()
        return path

    def log(self, message: str, tags: List[str] | None = None, mood: str = "neutral") -> None:
        self.entries.append(
            ReflectionEntry(time.time(), message, tags or [], mood)
        )

    def surface_entries(self) -> List[ReflectionEntry]:
        return [e for e in self.entries if any(t in SURFACE_TAGS for t in e.tags)]

    def to_markdown(self) -> str:
        """Return entries formatted as markdown bullet list."""
        lines = []
        for e in self.entries:
            ts = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(e.timestamp))
            lines.append(f"- {ts} [{e.mood}] {e.message}")
        return "\n".join(lines)

    def emit_mesh(self) -> None:
        """Send entries to mesh_logger."""
        from . import mesh_logger

        for e in self.entries:
            mesh_logger.log_event(
                "REFLECTION",
                {
                    "message": e.message,
                    "mood": e.mood,
                    "tags": e.tags,
                },
                origin="ReflectionLog",
            )

