"""Copy files between a local filesystem and a volume, and remove them from it."""

from __future__ import annotations

import os
from pathlib import Path, PurePosixPath

from labqoat.json_document import JsonValue
from labqoat.volumes.block_digests import BlockDigests
from labqoat.volumes.content_download import ContentDownload
from labqoat.volumes.content_upload import ContentUpload
from labqoat.volumes.local_item import LocalItem
from labqoat.volumes.local_tree import LocalTree
from labqoat.volumes.volume_api import VolumeApi
from labqoat.volumes.volume_entry import VolumeEntry


class VolumeFiles:
    """Puts, gets and removals of one volume; puts commit a batch of paths at a time."""

    BATCH = 5000

    def __init__(self, api: VolumeApi) -> None:
        """Work on the volume ``api`` reaches."""
        self._api = api

    @staticmethod
    def remote(path: str) -> str:
        """A volume path without leading or trailing separators; ``""`` is the volume's root."""
        trimmed = path.strip("/")
        if trimmed and any(part in ("", ".", "..") for part in trimmed.split("/")):
            raise ValueError(f"Volume paths are plain relative paths, not {path!r}")
        return trimmed

    def put(self, local: Path, remote: str) -> int:
        """Copy ``local`` into the volume and return the version the last commit made."""
        planned = self.planned(local, remote)
        packs = ContentUpload(self._api).send([(path, entry) for path, entry in planned if entry.kind == "file"])
        planned = [(path, entry.packed(packs.get(entry.path))) for path, entry in planned]
        version = 0
        for start in range(0, len(planned), self.BATCH):
            entries: list[JsonValue] = [entry.to_dict() for _path, entry in planned[start : start + self.BATCH]]
            version = self._api.commit({"entries": entries})
        return version

    def planned(self, local: Path, remote: str) -> list[tuple[Path, VolumeEntry]]:
        """Every local path to copy with the entry it becomes; a file lands in ``remote`` ending in ``/``."""
        if local.is_dir() and not local.is_symlink():
            base = self.remote(remote)
            return [
                (local / relative, self._entry(local / relative, self._join(base, relative), item))
                for relative, item in sorted(LocalTree.scan(local).items())
            ]
        item = LocalItem.read(local)
        if item is None:
            raise FileNotFoundError(f"Nothing to put at {local}")
        named = self.remote(remote)
        target = self._join(named, local.name) if not named or remote.endswith("/") else named
        return [(local, self._entry(local, target, item))]

    def get(self, remote: str, local: Path) -> int:
        """Copy what the volume holds at ``remote`` to ``local`` and return how many files were written."""
        _version, entries = self._api.entries(remote, True)
        if entries and entries[0].path == remote and entries[0].kind != "directory":
            target = local / PurePosixPath(remote).name if local.is_dir() else local
            return self._write([(entries[0], target)])
        local.mkdir(parents=True, exist_ok=True)
        cut = len(remote) + 1 if remote else 0
        return self._write([(entry, local / entry.path[cut:]) for entry in entries if entry.path != remote])

    def remove(self, remote: str, *, recursive: bool) -> int:
        """Remove ``remote``; without ``recursive`` a directory that still holds entries is refused."""
        if not remote:
            raise ValueError("Name a path to remove; deleting the volume removes everything")
        if not recursive:
            _version, entries = self._api.entries(remote, False)
            if len(entries) > 1:
                raise IsADirectoryError(f"{remote} is a directory that holds entries; remove it recursively")
        return self._api.commit({"deletions": [{"path": remote, "recursive": recursive}]})

    def _write(self, placed: list[tuple[VolumeEntry, Path]]) -> int:
        """Lay out directories and links and download the files whose content differs from what is there."""
        files: list[tuple[VolumeEntry, Path]] = []
        for entry, target in placed:
            if entry.kind == "directory":
                target.mkdir(parents=True, exist_ok=True)
            elif entry.kind == "symlink":
                target.parent.mkdir(parents=True, exist_ok=True)
                target.unlink(missing_ok=True)
                os.symlink(entry.target, target)
            elif not self._present(entry, target):
                files.append((entry, target))
        ContentDownload(self._api).fetch(files)
        return len(files)

    @staticmethod
    def _present(entry: VolumeEntry, target: Path) -> bool:
        """Whether ``target`` already holds the entry's content."""
        return target.is_file() and target.stat().st_size == entry.size and BlockDigests.of(target)[1] == entry.blocks

    @staticmethod
    def _join(base: str, relative: str) -> str:
        """A path below ``base``, or ``relative`` itself below the root."""
        return f"{base}/{relative}" if base else relative

    @staticmethod
    def _entry(source: Path, path: str, item: LocalItem) -> VolumeEntry:
        """The entry a local path becomes."""
        if item.kind == "file":
            size, blocks = BlockDigests.of(source)
            return VolumeEntry(path, "file", item.mode, item.mtime_ns // 1_000_000_000, size, blocks)
        if item.kind == "symlink":
            return VolumeEntry(path, "symlink", target=item.target)
        return VolumeEntry(path, "directory", item.mode)
