"""What a writer changed in a mount whose writes land in an overlay's upper layer, read from that layer."""

from __future__ import annotations

import os
import stat
from collections.abc import Mapping
from dataclasses import dataclass, field
from pathlib import Path

from labqoat.volumes.local_item import LocalItem
from labqoat.volumes.local_tree import LocalTree
from labqoat.volumes.volume_entry import VolumeEntry


@dataclass
class OverlayChanges:
    """The paths the upper layer holds, as the mount shows them, and the base paths the mount no longer shows.

    A volume mounted to be read as it is used keeps every write in the upper layer of an overlay over the read-only
    volume, so a commit reads that layer and the directories in it rather than every path of a volume that may hold
    hundreds of thousands. A deleted path is a whiteout there. Each directory the layer holds is also listed in the
    mount: base children missing there are gone, and children neither the base nor the layer holds came with a
    renamed directory and are read whole.
    """

    merged: Path
    upper: Path
    base: Mapping[str, VolumeEntry]
    found: dict[str, LocalItem] = field(default_factory=dict)
    removed: set[str] = field(default_factory=set)

    @classmethod
    def read(
        cls, merged: Path, upper: Path, base: Mapping[str, VolumeEntry]
    ) -> tuple[dict[str, LocalItem], frozenset[str]]:
        """The changed paths as the mount shows them, and every base path the mount no longer shows."""
        changes = cls(merged, upper, base)
        children = cls._children(base)
        pending = [""]
        while pending:
            directory = pending.pop()
            held = changes._layer(directory, pending)
            changes._listed(directory, held, children.get(directory, set()))
        return changes.found, changes._gone()

    def _layer(self, directory: str, pending: list[str]) -> set[str]:
        """Record what the upper layer holds in ``directory`` and name it; directories are visited next."""
        held: set[str] = set()
        with os.scandir(self.upper / directory) as listing:
            for child in listing:
                path = self._join(directory, child.name)
                if not LocalTree.nameable(path):
                    continue
                held.add(child.name)
                if self._whiteout(child):
                    self.removed.add(path)
                elif self._record(path) == "directory":
                    pending.append(path)
        return held

    def _listed(self, directory: str, held: set[str], based: set[str]) -> None:
        """Compare the mount's listing of ``directory`` with the base and the layer."""
        shown = set(os.listdir(self.merged / directory))
        self.removed.update(self._join(directory, name) for name in based - shown)
        for name in shown - held - based:
            self._whole(self._join(directory, name))

    def _whole(self, path: str) -> None:
        """Record a path the mount shows from elsewhere in the volume, and everything below it."""
        if self._record(path) == "directory":
            for below, item in LocalTree.scan(self.merged / path).items():
                self.found[f"{path}/{below}"] = item

    def _record(self, path: str) -> str | None:
        """Record ``path`` as the mount shows it and say what it is."""
        item = LocalItem.read(self.merged / path)
        if item is None:
            return None
        self.found[path] = item
        return item.kind

    def _gone(self) -> frozenset[str]:
        """Every base path at or below a removed one."""
        if not self.removed:
            return frozenset()
        return frozenset(path for path in self.base if any(held in self.removed for held in self._ancestry(path)))

    @staticmethod
    def _ancestry(path: str) -> list[str]:
        """``path`` and every directory holding it."""
        parts = path.split("/")
        return ["/".join(parts[: index + 1]) for index in range(len(parts))]

    @staticmethod
    def _whiteout(child: os.DirEntry[str]) -> bool:
        """Whether the layer marks a removed path: a character device numbered 0:0."""
        status = child.stat(follow_symlinks=False)
        return stat.S_ISCHR(status.st_mode) and status.st_rdev == 0

    @staticmethod
    def _children(base: Mapping[str, VolumeEntry]) -> dict[str, set[str]]:
        """Each base directory's children by name; the root is the empty path."""
        children: dict[str, set[str]] = {}
        for path in base:
            parent, _, name = path.rpartition("/")
            children.setdefault(parent, set()).add(name)
        return children

    @staticmethod
    def _join(directory: str, name: str) -> str:
        """The path of ``name`` in ``directory``."""
        return f"{directory}/{name}" if directory else name
