"""One commit or reload of a mount at a time, across the workload's threads and processes."""

from __future__ import annotations

import fcntl
import threading
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path
from typing import ClassVar


class MountLock:
    """Hold a mount's state while it is compared, sent or refreshed."""

    _threads: ClassVar[dict[Path, threading.Lock]] = {}
    _guard: ClassVar[threading.Lock] = threading.Lock()

    @classmethod
    @contextmanager
    def held(cls, state: Path) -> Iterator[None]:
        """Lock the mount whose state lives at ``state`` for this thread and process."""
        with cls._guard:
            local = cls._threads.setdefault(state, threading.Lock())
        with local, state.with_name(f"{state.name}.lock").open("a") as handle:
            fcntl.flock(handle, fcntl.LOCK_EX)
            try:
                yield
            finally:
                fcntl.flock(handle, fcntl.LOCK_UN)
