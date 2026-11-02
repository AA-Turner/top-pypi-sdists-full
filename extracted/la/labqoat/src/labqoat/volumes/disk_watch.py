"""Say, from inside a workload, that the host disk under a volume mount is running out."""

from __future__ import annotations

import shutil
import sys
import time
from pathlib import Path
from typing import ClassVar


class DiskWatch:
    """Warn in the run's own log when little is free beside a writable mount, at most once per interval.

    A host lays a mounted volume out on its own disk and cannot grow it. Writes that fail on a full disk raise
    ``OSError 28`` in code that handles it, and silently truncate files in code that does not: a checkpoint cut
    short fails to load later with an error about its container, far from the cause.
    """

    FLOOR_BYTES: ClassVar[int] = 5 * 1024**3
    FLOOR_SHARE: ClassVar[float] = 0.05
    INTERVAL: ClassVar[float] = 300.0

    def __init__(self) -> None:
        """Start with nothing warned."""
        self._warned: dict[Path, float] = {}

    def check(self, path: Path, name: str) -> bool:
        """Warn if the filesystem holding ``path`` is nearly full; return whether it was."""
        usage = shutil.disk_usage(path)
        if usage.free >= max(self.FLOOR_BYTES, int(usage.total * self.FLOOR_SHARE)):
            return False
        now = time.monotonic()
        if now - self._warned.get(path, -self.INTERVAL) >= self.INTERVAL:
            self._warned[path] = now
            print(self.message(name, path, usage.free, usage.total), file=sys.stderr, flush=True)
        return True

    @staticmethod
    def message(name: str, path: Path, free: int, total: int) -> str:
        """The warning for a mount of volume ``name`` at ``path`` with ``free`` of ``total`` bytes left."""
        return (
            f"Host disk is nearly full beside volume {name!r} mounted at {path}: {free / 1e9:.1f} GB free of "
            f"{total / 1e9:.1f} GB. Writes will fail with OSError 28 (no space left on device) or leave truncated "
            f"files. Delete files or run with more disk: the host's disk holds the whole volume plus what this run "
            f"writes."
        )
