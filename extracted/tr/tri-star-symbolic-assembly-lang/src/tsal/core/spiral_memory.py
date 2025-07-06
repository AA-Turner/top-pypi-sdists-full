from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List

@dataclass
class SpiralMemory:
    entries: List[Dict[str, Any]] = field(default_factory=list)
    crystallized: bool = False

    def log_vector(self, vector: Dict[str, Any]) -> None:
        if self.crystallized:
            return
        self.entries.append(vector)

    def crystallize(self) -> None:
        self.crystallized = True

    def replay(self) -> List[Dict[str, Any]]:
        return list(self.entries)

__all__ = ["SpiralMemory"]
