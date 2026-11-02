"""Bring other writers' committed changes into a mount without touching this writer's own."""

from __future__ import annotations

import os
import shutil
from collections.abc import Iterable
from pathlib import Path

from labqoat.volumes.content_download import ContentDownload
from labqoat.volumes.mount_state import MountState
from labqoat.volumes.volume_api import VolumeApi
from labqoat.volumes.volume_entry import VolumeEntry


class MountReload:
    """Apply the volume's current state to every path this writer has not changed since its base."""

    def __init__(self, api: VolumeApi, root: Path) -> None:
        """Reload the mount at ``root`` from ``api``."""
        self._api = api
        self._root = root

    def apply(self, state: MountState, head: Iterable[VolumeEntry], mine: frozenset[str]) -> None:
        """Make the mount and ``state`` match ``head`` except for the paths in ``mine``."""
        remote = {entry.path: entry for entry in head}
        incoming = [
            entry
            for path, entry in sorted(remote.items())
            if path not in mine and not entry.same(state.entries.get(path))
        ]
        gone = sorted((path for path in state.entries if path not in remote and path not in mine), reverse=True)
        for path in gone:
            self._remove(self._root / path, empty_only=True)
            state.entries.pop(path)
            state.observed.pop(path, None)
        files = [(entry, self._root / entry.path) for entry in incoming if self._place(entry)]
        ContentDownload(self._api).fetch(files)
        for entry in incoming:
            state.entries[entry.path] = entry
            if entry.kind == "file":
                state.observed[entry.path] = (entry.size, entry.mtime * 1_000_000_000)

    def _place(self, entry: VolumeEntry) -> bool:
        """Make room for an incoming entry and lay out directories and links; files are left to download."""
        target = self._root / entry.path
        if entry.kind != "directory" or not target.is_dir() or target.is_symlink():
            self._remove(target, empty_only=False)
        target.parent.mkdir(parents=True, exist_ok=True)
        if entry.kind == "directory":
            target.mkdir(exist_ok=True)
            target.chmod(entry.mode)
        elif entry.kind == "symlink":
            os.symlink(entry.target, target)
        return entry.kind == "file"

    @staticmethod
    def _remove(target: Path, *, empty_only: bool) -> None:
        """Remove what is at ``target``; a directory still holding files stays when only empty ones may go."""
        if target.is_symlink() or target.is_file():
            target.unlink()
        elif target.is_dir() and not empty_only:
            shutil.rmtree(target)
        elif target.is_dir() and not any(target.iterdir()):
            target.rmdir()
