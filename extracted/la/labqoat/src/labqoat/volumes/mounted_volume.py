"""One volume as a workload mounted it: what to commit from it and how to bring others' commits into it."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from labqoat.json_document import JsonValue
from labqoat.volumes.content_upload import ContentUpload
from labqoat.volumes.mount_changes import MountChanges
from labqoat.volumes.mount_lock import MountLock
from labqoat.volumes.mount_reload import MountReload
from labqoat.volumes.mount_state import MountState
from labqoat.volumes.volume_api import VolumeApi


@dataclass(frozen=True)
class MountedVolume:
    """A volume, or its directory ``subpath``, mounted at ``path``; its base is at ``state``, the host's record ``record``.

    A mount whose writes land in an overlay shows that overlay's upper layer at ``changes``, and is compared with its
    base through that layer alone.
    """

    path: Path
    name: str
    volume: str
    read_only: bool
    state: Path
    record: Mapping[str, JsonValue]
    api: VolumeApi
    subpath: str = ""
    changes: Path | None = None

    BATCH: ClassVar[int] = 5000

    def commit(self) -> int:
        """Send what changed under the mount since its base and return the volume's version.

        Only paths this writer changed are sent, so paths others wrote meanwhile keep their content; of two
        writers of one path the later commit wins. Nothing changed means nothing is sent.
        """
        self._writable("commit")
        with MountLock.held(self.state):
            state = MountState.load(self.state, self.record)
            changes = MountChanges.between(self.path, state.entries, state.observed, self.changes)
            state.observed.update(changes.observed)
            if not changes.empty:
                files = [(self.path / entry.path, entry) for entry in changes.entries if entry.kind == "file"]
                packs = ContentUpload(self.api).send(files)
                changes = changes.packed(packs)
                state.version = self._send(changes)
                self._committed(state, changes)
            state.save(self.state)
            return state.version

    def reload(self) -> int:
        """Bring the volume's latest committed state into the mount and return its version.

        Paths this writer changed and has not committed yet keep their local content.
        """
        self._writable("reload")
        with MountLock.held(self.state):
            state = MountState.load(self.state, self.record)
            mine = MountChanges.between(self.path, state.entries, state.observed, self.changes)
            state.observed.update(mine.observed)
            version, head = self.api.entries()
            MountReload(self.api, self.path).apply(state, head, mine.paths)
            state.version = version
            state.save(self.state)
            return version

    def _writable(self, operation: str) -> None:
        """Refuse to change a mount the function declared read-only."""
        if self.read_only:
            raise PermissionError(f"Volume {self.name!r} is mounted read-only at {self.path}; it cannot {operation}")

    def _send(self, changes: MountChanges) -> int:
        """Commit the changes in batches the platform accepts; the last batch's version is the volume's.

        Changes that fit one batch are one commit. Deletions come deepest first, so a directory is never removed
        in an earlier batch than what it holds.
        """
        version = 0
        for start in range(0, max(len(changes.entries), len(changes.deletions)), self.BATCH):
            entries: list[JsonValue] = [entry.to_dict() for entry in changes.entries[start : start + self.BATCH]]
            deletions: list[JsonValue] = [{"path": path} for path in changes.deletions[start : start + self.BATCH]]
            version = self.api.commit({"volume": self.volume, "entries": entries, "deletions": deletions})
        return version

    @staticmethod
    def _committed(state: MountState, changes: MountChanges) -> None:
        """Make what was sent the new base."""
        for entry in changes.entries:
            state.entries[entry.path] = entry
        for path in changes.deletions:
            state.entries.pop(path, None)
            state.observed.pop(path, None)
