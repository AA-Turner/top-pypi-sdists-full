"""Put new file content into a volume's storage, sending only the blocks storage lacks."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
import tempfile
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from pathlib import Path

from labqoat.json_document import JsonDocument, JsonValue
from labqoat.volumes.block_digests import BlockDigests
from labqoat.volumes.block_transfer import BlockTransfer
from labqoat.volumes.content_packs import ContentPacks
from labqoat.volumes.volume_api import VolumeApi
from labqoat.volumes.volume_entry import VolumeEntry
from labqoat.volumes.volume_pack import VolumePack


class ContentUpload:
    """Ask for signed uploads a batch at a time and send the granted blocks in parallel.

    Storage already holding a block, from this volume's other files or an interrupted earlier upload, means it
    is not sent again, so a repeated upload resumes where the last one stopped. Small files travel in packs.
    """

    BATCH = 1000

    def __init__(self, api: VolumeApi, workers: int = 32) -> None:
        """Upload through ``api`` with at most ``workers`` blocks in flight."""
        self._api = api
        self._workers = workers

    def send(self, files: Sequence[tuple[Path, VolumeEntry]]) -> dict[str, VolumePack]:
        """Make storage hold every file's content and return where each packed path is stored."""
        with tempfile.TemporaryDirectory(prefix="labqoat-packs-") as scratch:
            packs = ContentPacks(Path(scratch))
            placed = packs.pack([(path, entry) for path, entry in files if ContentPacks.small(entry)])
            whole = [(path, entry) for path, entry in files if not ContentPacks.small(entry)]
            self._upload({**self.sources(whole), **packs.sources})
        return placed

    def _upload(self, sources: Mapping[str, tuple[Path, int, int]]) -> None:
        """Send every block storage lacks, a batch of grants at a time."""
        digests = list(sources)
        with ThreadPoolExecutor(self._workers, thread_name_prefix="labqoat-volume-upload") as pool:
            for start in range(0, len(digests), self.BATCH):
                batch: list[Mapping[str, JsonValue]] = [
                    {"digest": digest, "size": sources[digest][2]} for digest in digests[start : start + self.BATCH]
                ]
                grants = self._api.uploads(batch)
                list(pool.map(partial(self._put, sources=sources), grants))

    @staticmethod
    def sources(files: Sequence[tuple[Path, VolumeEntry]]) -> dict[str, tuple[Path, int, int]]:
        """Where each distinct block is read from: file, offset and length."""
        found: dict[str, tuple[Path, int, int]] = {}
        for path, entry in files:
            for index, digest in enumerate(entry.blocks):
                offset = index * BlockDigests.BLOCK_BYTES
                found.setdefault(digest, (path, offset, min(BlockDigests.BLOCK_BYTES, entry.size - offset)))
        return found

    @staticmethod
    def _put(grant: Mapping[str, JsonValue], sources: Mapping[str, tuple[Path, int, int]]) -> None:
        """Send one granted block with exactly the headers it was signed with."""
        digest = JsonDocument.expect_scalar(grant["digest"], str)
        headers = JsonDocument.expect_dict(grant["headers"])
        source, offset, length = sources[digest]
        signed = {name: JsonDocument.expect_scalar(value, str) for name, value in headers.items()}
        BlockTransfer.put(JsonDocument.expect_scalar(grant["url"], str), signed, source, offset, length)
