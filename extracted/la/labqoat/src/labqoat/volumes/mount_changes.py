"""What changed in a mount since the state it was last in step with."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field, replace
from pathlib import Path

from labqoat.volumes.block_digests import BlockDigests
from labqoat.volumes.local_item import LocalItem
from labqoat.volumes.local_tree import LocalTree
from labqoat.volumes.overlay_changes import OverlayChanges
from labqoat.volumes.volume_entry import VolumeEntry
from labqoat.volumes.volume_pack import VolumePack


@dataclass(frozen=True)
class MountChanges:
    """Paths whose content, mode or kind differ from the base, and base paths gone from disk.

    A file whose size and modification time match what was last seen is not read again. ``observed`` holds the
    size and modification time of every file read, so the next comparison can skip it too.
    """

    entries: tuple[VolumeEntry, ...] = ()
    deletions: tuple[str, ...] = ()
    observed: dict[str, tuple[int, int]] = field(default_factory=dict)

    @property
    def empty(self) -> bool:
        """Whether nothing needs committing."""
        return not self.entries and not self.deletions

    @property
    def paths(self) -> frozenset[str]:
        """Every path this writer changed or removed."""
        return frozenset(entry.path for entry in self.entries) | frozenset(self.deletions)

    def packed(self, packs: Mapping[str, VolumePack]) -> MountChanges:
        """These changes with each packed file's place in storage."""
        return replace(self, entries=tuple(entry.packed(packs.get(entry.path)) for entry in self.entries))

    @classmethod
    def between(
        cls,
        root: Path,
        base: Mapping[str, VolumeEntry],
        observed: Mapping[str, tuple[int, int]],
        upper: Path | None = None,
    ) -> MountChanges:
        """Compare the tree under ``root`` with ``base``; with an overlay's ``upper`` layer, only what it holds."""
        if upper is None:
            local = LocalTree.scan(root)
            missing = frozenset(path for path in base if path not in local)
        else:
            local, missing = OverlayChanges.read(root, upper, base)
        seen: dict[str, tuple[int, int]] = {}
        changed: list[VolumeEntry] = []
        for path, item in sorted(local.items()):
            entry = cls._entry(root, path, item, base.get(path), observed.get(path), seen)
            if entry is not None:
                changed.append(entry)
        gone = tuple(sorted((path for path in missing if path not in local), reverse=True))
        return cls(tuple(changed), gone, seen)

    @staticmethod
    def _entry(
        root: Path,
        path: str,
        item: LocalItem,
        before: VolumeEntry | None,
        signature: tuple[int, int] | None,
        seen: dict[str, tuple[int, int]],
    ) -> VolumeEntry | None:
        """The entry ``path`` now is, or nothing when it holds what the base says."""
        if item.kind == "symlink":
            now = VolumeEntry(path, "symlink", target=item.target)
        elif item.kind == "directory":
            now = VolumeEntry(path, "directory", item.mode)
        elif before is not None and before.kind == "file" and before.mode == item.mode and signature == item.signature:
            return None
        else:
            size, blocks = BlockDigests.of(root / path)
            now = VolumeEntry(path, "file", item.mode, item.mtime_ns // 1_000_000_000, size, blocks)
            seen[path] = item.signature
        return None if now.same(before) else now
