"""Gather small files into pack blocks, so a volume of many small files moves in few storage requests."""

from __future__ import annotations

import hashlib
from collections.abc import Sequence
from pathlib import Path
from typing import ClassVar

from labqoat.volumes.volume_entry import VolumeEntry
from labqoat.volumes.volume_pack import VolumePack


class ContentPacks:
    """Write files under ``LIMIT`` bytes into pack files of at most ``BYTES`` bytes in a scratch directory.

    Each file keeps its own digest as its block; its pack only says where the bytes are stored, and identical
    contents are stored once. A file whose bytes no longer match the digest it was listed with fails the upload
    rather than storing other content under that digest.
    """

    LIMIT: ClassVar[int] = 256 * 1024
    BYTES: ClassVar[int] = 16 * 1024 * 1024

    def __init__(self, directory: Path) -> None:
        """Write pack files into ``directory``."""
        self._directory = directory
        self._buffer = bytearray()
        self._pending: dict[str, int] = {}
        self._placed: dict[str, VolumePack] = {}
        self.sources: dict[str, tuple[Path, int, int]] = {}

    @classmethod
    def small(cls, entry: VolumeEntry) -> bool:
        """Whether a file entry is packed: a non-empty one-block file under the size limit."""
        return 0 < entry.size < cls.LIMIT and len(entry.blocks) == 1

    def pack(self, files: Sequence[tuple[Path, VolumeEntry]]) -> dict[str, VolumePack]:
        """Pack every file and return each path's place; ``sources`` then names the pack files to upload."""
        for source, entry in files:
            self._add(source, entry.blocks[0])
        self._seal()
        return {entry.path: self._placed[entry.blocks[0]] for _source, entry in files}

    def _add(self, source: Path, own: str) -> None:
        """Buffer one distinct content, sealing the pack first when it would overflow."""
        if own in self._pending or own in self._placed:
            return
        data = source.read_bytes()
        if hashlib.sha256(data).hexdigest() != own:
            raise OSError(f"{source} changed while it was being uploaded; upload it again")
        if len(self._buffer) + len(data) > self.BYTES:
            self._seal()
        self._pending[own] = len(self._buffer)
        self._buffer += data

    def _seal(self) -> None:
        """Write the buffered pack to a file named by its digest and place its contents."""
        if not self._buffer:
            return
        digest = hashlib.sha256(self._buffer).hexdigest()
        path = self._directory / digest
        path.write_bytes(self._buffer)
        self.sources[digest] = (path, 0, len(self._buffer))
        for own, offset in self._pending.items():
            self._placed[own] = VolumePack(digest, offset, len(self._buffer))
        self._pending = {}
        self._buffer = bytearray()
