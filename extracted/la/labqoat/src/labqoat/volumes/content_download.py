"""Fetch volume files into place: blocks in parallel, each checked, the file appearing only when whole."""

from __future__ import annotations

import hashlib
import os
import tempfile
from collections.abc import Sequence
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from pathlib import Path

from labqoat.volumes.block_digests import BlockDigests
from labqoat.volumes.block_transfer import BlockTransfer
from labqoat.volumes.volume_api import VolumeApi
from labqoat.volumes.volume_entry import VolumeEntry
from labqoat.volumes.volume_pack import VolumePack


class ContentDownload:
    """Write each file beside its destination and rename it into place once every block is verified.

    A partial file left by an interrupted download keeps the blocks it already holds, so fetching again
    resumes instead of starting over. Packed small files are cut out of their pack, fetched once per download.
    """

    BATCH = 1000

    def __init__(self, api: VolumeApi, workers: int = 32) -> None:
        """Download through ``api`` with at most ``workers`` blocks in flight."""
        self._api = api
        self._workers = workers

    def fetch(self, files: Sequence[tuple[VolumeEntry, Path]]) -> None:
        """Place every file entry at its destination with its mode and modification time."""
        packed = [(entry, entry.pack, destination) for entry, destination in files if entry.pack is not None]
        whole = [(entry, destination) for entry, destination in files if entry.pack is None]
        wanted = [(entry, destination, *self._prepare(entry, destination)) for entry, destination in whole]
        jobs = [(partial, index, digest) for _entry, _target, partial, needed in wanted for index, digest in needed]
        with tempfile.TemporaryDirectory(prefix="labqoat-packs-") as scratch:
            packs = self._packs(Path(scratch), packed)
            self._transfer([*jobs, *((path, 0, digest) for digest, path in packs.items())])
            for entry, destination, assembled, _needed in wanted:
                self.place(entry, assembled, destination)
            for entry, pack, destination in packed:
                self._cut(entry, packs[pack.digest], pack.offset, destination)

    def _transfer(self, jobs: list[tuple[Path, int, str]]) -> None:
        """Fetch every block job in parallel."""
        urls = self._urls(sorted({digest for _partial, _index, digest in jobs}))
        with ThreadPoolExecutor(self._workers, thread_name_prefix="labqoat-volume-download") as pool:
            list(pool.map(partial(self._block, urls=urls), jobs))

    @staticmethod
    def _packs(scratch: Path, packed: Sequence[tuple[VolumeEntry, VolumePack, Path]]) -> dict[str, Path]:
        """An empty scratch file for each distinct pack the packed files lie in."""
        packs = {pack.digest: scratch / pack.digest for _entry, pack, _target in packed}
        for path in packs.values():
            path.write_bytes(b"")
        return packs

    def _cut(self, entry: VolumeEntry, pack: Path, offset: int, destination: Path) -> None:
        """Write a packed file's range of its fetched pack into place."""
        with pack.open("rb") as source:
            source.seek(offset)
            data = source.read(entry.size)
        destination.parent.mkdir(parents=True, exist_ok=True)
        assembled = self.partial(destination)
        assembled.write_bytes(data)
        self.place(entry, assembled, destination)

    @staticmethod
    def partial(destination: Path) -> Path:
        """Where a file is assembled before it is complete."""
        return destination.with_name(f".{destination.name}.labqoat-part")

    @staticmethod
    def place(entry: VolumeEntry, source: Path, destination: Path) -> None:
        """Give an assembled file its size, mode and time, then move it into place."""
        os.truncate(source, entry.size)
        source.chmod(entry.mode)
        os.utime(source, ns=(entry.mtime * 1_000_000_000, entry.mtime * 1_000_000_000))
        source.replace(destination)

    def _prepare(self, entry: VolumeEntry, destination: Path) -> tuple[Path, list[tuple[int, str]]]:
        """Open the partial file and name the blocks it does not hold yet."""
        destination.parent.mkdir(parents=True, exist_ok=True)
        partial = self.partial(destination)
        if not partial.is_file():
            partial.write_bytes(b"")
        needed = [
            (index, digest) for index, digest in enumerate(entry.blocks) if not self._holds(partial, index, digest)
        ]
        return partial, needed

    @staticmethod
    def _holds(partial: Path, index: int, digest: str) -> bool:
        """Whether the partial file already holds this block."""
        with partial.open("rb") as file:
            file.seek(index * BlockDigests.BLOCK_BYTES)
            data = file.read(BlockDigests.BLOCK_BYTES)
        return bool(data) and hashlib.sha256(data).hexdigest() == digest

    def _urls(self, digests: list[str]) -> dict[str, str]:
        """Signed URLs for every needed block, asked for a batch at a time."""
        urls: dict[str, str] = {}
        for start in range(0, len(digests), self.BATCH):
            urls.update(self._api.downloads(digests[start : start + self.BATCH]))
        return urls

    @staticmethod
    def _block(job: tuple[Path, int, str], urls: dict[str, str]) -> None:
        """Fetch one block into its file."""
        partial, index, digest = job
        BlockTransfer.get(urls[digest], partial, index * BlockDigests.BLOCK_BYTES, digest)
