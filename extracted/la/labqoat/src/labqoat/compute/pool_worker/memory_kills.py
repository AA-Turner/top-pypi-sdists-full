"""The host's count of processes the kernel killed in this worker for going over its memory limit."""

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class MemoryKills:
    """Tell a process killed for memory apart from one killed otherwise, by the count its host keeps.

    The host shows the worker the kernel's count read-only; a host that does not show it leaves nothing to compare.
    """

    events: Path = Path("/run/labqoat/memory.events")

    def count(self) -> int | None:
        """The kernel's count of memory kills in this worker, or nothing where the host does not expose it."""
        try:
            lines = self.events.read_text(encoding="ascii").splitlines()
        except OSError:
            return None
        counts = [int(value) for name, _, value in (line.partition(" ") for line in lines) if name == "oom_kill"]
        return counts[0] if counts else None

    def grew(self, before: int | None) -> bool:
        """Whether the kernel killed something for memory since `before` was read."""
        after = self.count()
        return before is not None and after is not None and after > before

    @staticmethod
    def detail() -> str:
        """Say the process ran out of memory, with the limit the host enforces when the host names it."""
        limit = os.environ.get("LABQOAT_MEMORY_LIMIT_MB", "")
        said = f"out of memory (limit {limit} MiB)" if limit.isdigit() else "out of memory"
        return said + ": give the function more memory= (MiB) than its peak"
