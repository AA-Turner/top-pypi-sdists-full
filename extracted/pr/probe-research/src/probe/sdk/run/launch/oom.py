"""OomCounter: the out-of-memory kills counted in this process's cgroup, at start and now.

What tells a SIGKILL nobody chose from the OOM killer's (`_status_for_exit`): cgroup v2
``memory.events`` ``oom_kill`` (hierarchical) or v1 ``memory.oom_control`` ``oom_kill``. A child
starts in its launcher's cgroup; unreadable means "maybe an OOM"."""

from __future__ import annotations

from pathlib import Path


class OomCounter:
    """The count when made (``baseline``) and on each `read`; None wherever it cannot be read."""

    def __init__(
        self, *, cgroup_root: str = "/sys/fs/cgroup", process_cgroup: str = "/proc/self/cgroup"
    ) -> None:
        self._root = Path(cgroup_root)
        self._process_cgroup = Path(process_cgroup)
        self.baseline = self.read()

    def read(self) -> int | None:
        """OOM kills in this process's cgroup and below; None when there is no counter to read
        (no cgroup memory controller, the root cgroup, another OS)."""
        try:
            lines = self._process_cgroup.read_text().splitlines()
        except Exception:  # noqa: BLE001 -- unreadable (or not text) is "maybe an OOM"
            return None
        for line in lines:
            hierarchy, _, rest = line.partition(":")
            controllers, _, path = rest.partition(":")
            if hierarchy == "0" and controllers == "":
                count = _read_field(self._root / path.lstrip("/") / "memory.events", "oom_kill")
            elif "memory" in controllers.split(","):
                count = _read_field(
                    self._root / "memory" / path.lstrip("/") / "memory.oom_control", "oom_kill"
                )
            else:
                continue
            if count is not None:
                return count
        return None

    def is_unchanged(self) -> bool:
        """Readable at both ends, and no OOM kill since the baseline."""
        if self.baseline is None:
            return False
        return self.read() == self.baseline


def _read_field(path: Path, name: str) -> int | None:
    try:
        text = path.read_text()
    except Exception:  # noqa: BLE001 -- as above
        return None
    for line in text.splitlines():
        key, _, value = line.partition(" ")
        if key == name and value.strip().isdigit():
            return int(value.strip())
    return None
