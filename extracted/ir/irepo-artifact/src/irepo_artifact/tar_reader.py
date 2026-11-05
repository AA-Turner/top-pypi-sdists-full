"""Read tar archives with bounded headers, payloads and retained metadata."""
from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass
import gzip
from pathlib import Path
import tarfile
from typing import BinaryIO

from .errors import DownloadError

MAX_HEADER_BYTES = 8 * 1024**2
MAX_METADATA_BYTES = 32 * 1024**2
MAX_EXPANDED_BYTES = 64 * 1024**3
MAX_MEMBERS = 100_000
_INDEX_ENTRY_OVERHEAD_BYTES = 128
_SPARSE_REGION_RETAINED_BYTES = 256
_SPARSE_REGION_PARSING_BYTES = 512
_SPARSE_LIST_OVERHEAD_BYTES = 64


class ArchiveLimitExceeded(DownloadError):
    """Archive parsing or indexing exceeds the shared resource budget."""


class _ArchiveHeaderReader:
    """Cap extended-header reads before tarfile can allocate their payload."""

    def __init__(self, stream: BinaryIO, budget: ArchiveBudget) -> None:
        self.stream = stream
        self.budget = budget
        self.header_budget: int | None = MAX_HEADER_BYTES

    def read(self, size: int = -1) -> bytes:
        if self.header_budget is not None:
            if size < 0 or size > self.header_budget:
                raise ArchiveLimitExceeded('archive header metadata limit exceeded')
        data = self.stream.read(size)
        if self.header_budget is not None:
            self.header_budget -= len(data)
        return data

    def tell(self) -> int:
        return self.stream.tell()

    def seek(self, offset: int, whence: int = 0) -> int:
        current = self.tell()
        if self.header_budget is not None:
            if whence not in (0, 1):
                raise ArchiveLimitExceeded('unsafe archive header seek')
            target = offset if whence == 0 else current + offset
            distance = max(0, target - current)
            if distance > self.header_budget:
                raise ArchiveLimitExceeded('archive header metadata limit exceeded')
            self.header_budget -= distance
        return self.stream.seek(offset, whence)


@dataclass
class ArchiveBudget:
    """Bound member data and retained metadata, including auxiliary indexes."""

    entries: int = 0
    expanded_bytes: int = 0
    metadata_bytes: int = 0

    def add_metadata(self, size: int) -> None:
        self.metadata_bytes += size
        if self.metadata_bytes > MAX_METADATA_BYTES:
            raise ArchiveLimitExceeded('archive extraction limits exceeded')

    def add_index_path(self, path: str) -> None:
        self.add_metadata(len(path.encode('utf-8')) + _INDEX_ENTRY_OVERHEAD_BYTES)

    def reserve_sparse_regions(self, count: int) -> None:
        """Account for retained tuples and check temporary parser allocations first."""
        parsing_bytes = _SPARSE_LIST_OVERHEAD_BYTES + count * _SPARSE_REGION_PARSING_BYTES
        if count < 0 or self.metadata_bytes + parsing_bytes > MAX_METADATA_BYTES:
            raise ArchiveLimitExceeded('archive sparse metadata limit exceeded')
        self.add_metadata(_SPARSE_LIST_OVERHEAD_BYTES + count * _SPARSE_REGION_RETAINED_BYTES)

    def add_member(self, member: tarfile.TarInfo, stored_bytes: int) -> None:
        self.entries += 1
        # Sparse headers have both a logical size and an encoded data extent.
        # Bound both before the reader seeks past any unselected payload.
        self.expanded_bytes += max(0, member.size, stored_bytes)
        if (self.entries > MAX_MEMBERS or member.size < 0 or stored_bytes < 0
                or self.expanded_bytes > MAX_EXPANDED_BYTES):
            raise ArchiveLimitExceeded('archive extraction limits exceeded')
        size = (len(member.name.encode('utf-8')) + len(member.linkname.encode('utf-8'))
                + _INDEX_ENTRY_OVERHEAD_BYTES)
        size += sum(len(key.encode('utf-8')) + len(value.encode('utf-8'))
                    for key, value in member.pax_headers.items())
        self.add_metadata(size)


class _BoundedTarInfo(tarfile.TarInfo):
    """Guard sparse-map allocation before the standard parser builds its lists."""

    __slots__ = ('_budget',)

    def _proc_member(self, archive: tarfile.TarFile) -> tarfile.TarInfo:
        self._budget = archive.fileobj.budget
        return super()._proc_member(archive)

    @staticmethod
    def _validate_sparse(member: tarfile.TarInfo) -> None:
        # This also bounds the retained Python integers covered by the estimate.
        for offset, length in member.sparse:
            if not (0 <= offset <= MAX_EXPANDED_BYTES and 0 <= length <= MAX_EXPANDED_BYTES):
                raise ArchiveLimitExceeded('archive sparse extent limit exceeded')

    def _proc_gnusparse_01(self, following: tarfile.TarInfo, headers: dict[str, str]) -> None:
        fields = headers['GNU.sparse.map'].count(',') + 1
        self._budget.reserve_sparse_regions((fields + 1) // 2)
        super()._proc_gnusparse_01(following, headers)
        self._validate_sparse(following)

    def _proc_gnusparse_00(
        self, following: tarfile.TarInfo,
        *headers: bytes | dict[str, str] | list[tuple[int, bytes, bytes]],
    ) -> None:
        # Python maintenance releases changed this argument from raw PAX bytes
        # to parsed records. Count without building either offsets/lengths list.
        records = headers[-1]
        if isinstance(records, bytes):
            offsets = records.count(b'GNU.sparse.offset=')
            lengths = records.count(b'GNU.sparse.numbytes=')
        else:
            offsets = sum(key == b'GNU.sparse.offset' for _, key, _ in records)
            lengths = sum(key == b'GNU.sparse.numbytes' for _, key, _ in records)
        self._budget.reserve_sparse_regions(max(offsets, lengths))
        super()._proc_gnusparse_00(following, *headers)
        self._validate_sparse(following)

    def _proc_gnusparse_10(self, following: tarfile.TarInfo, headers: dict[str, str],
                          archive: tarfile.TarFile) -> None:
        # Version 1.0 puts the count and mapping at the start of the data area.
        # Check the declared count before accumulating any offsets or lengths.
        block = archive.fileobj.read(tarfile.BLOCKSIZE)
        count, remainder = block.split(b'\n', 1)
        regions = int(count)
        self._budget.reserve_sparse_regions(regions)
        values = []
        while len(values) < regions * 2:
            if b'\n' not in remainder:
                remainder += archive.fileobj.read(tarfile.BLOCKSIZE)
            number, remainder = remainder.split(b'\n', 1)
            values.append(int(number))
        following.offset_data = archive.fileobj.tell()
        following.sparse = list(zip(values[::2], values[1::2]))
        self._validate_sparse(following)

    def _proc_sparse(self, archive: tarfile.TarFile) -> tarfile.TarInfo:
        # Old GNU headers carry four initial regions, then up to 21 per block.
        regions, extended, logical_size = self._sparse_structs
        del self._sparse_structs
        self._budget.reserve_sparse_regions(len(regions))
        while extended:
            self._budget.reserve_sparse_regions(21)
            block = archive.fileobj.read(tarfile.BLOCKSIZE)
            if len(block) != tarfile.BLOCKSIZE:
                raise tarfile.ReadError('truncated GNU sparse header')
            for start in range(0, 21 * 24, 24):
                try:
                    offset = tarfile.nti(block[start:start + 12])
                    length = tarfile.nti(block[start + 12:start + 24])
                except ValueError:
                    break
                if offset and length:
                    regions.append((offset, length))
            extended = bool(block[504])
        self.sparse = regions
        self._validate_sparse(self)
        self.offset_data = archive.fileobj.tell()
        archive.offset = self.offset_data + self._block(self.size)
        self.size = logical_size
        return self


def _iter_members(tar: tarfile.TarFile, reader: _ArchiveHeaderReader,
                  budget: ArchiveBudget) -> Iterator[tarfile.TarInfo]:
    while True:
        # Skip validated file bodies outside the header budget. Selected
        # downloads scan them without extracting unselected content.
        reader.header_budget = None
        if tar.firstmember is None and tar.offset != reader.tell():
            reader.seek(tar.offset - 1)
            if not reader.read(1):
                raise tarfile.ReadError('unexpected end of data')
        reader.header_budget = MAX_HEADER_BYTES
        member = tar.next()
        reader.header_budget = None
        if member is None:
            return
        budget.add_member(member, tar.offset - member.offset_data)
        yield member


@contextmanager
def open_archive(
    path: Path, budget: ArchiveBudget | None = None,
) -> Iterator[tuple[tarfile.TarFile, Iterator[tarfile.TarInfo]]]:
    """Keep the archive open while callers iterate members and copy content.

    Pass a budget when the caller also retains an index that must be counted.
    Parsing errors propagate so each caller can apply its own fallback policy.
    """
    if budget is None:
        budget = ArchiveBudget()
    with gzip.open(path, 'rb') as compressed:
        reader = _ArchiveHeaderReader(compressed, budget)
        with tarfile.open(fileobj=reader, mode='r:', tarinfo=_BoundedTarInfo) as tar:
            yield tar, _iter_members(tar, reader, budget)
