"""what a compressed file or archive holds, for the content scan: member names and bytes, read up to wherever it breaks."""

from __future__ import annotations
import bz2
import lzma
import os
import struct
import tarfile
import time
import zipfile
import zlib
from typing import Any, BinaryIO, Iterator

#: Compressed bytes fed to a decompressor per step, and the most it may return
#: per step: a small piece can expand ~1000x, so output is asked for in bounded pieces.
_PIECE = 64 * 1024
_MAX_OUT = 4 * 1024 * 1024
_DECOMPRESS_ERRORS = (zlib.error, OSError, EOFError, lzma.LZMAError, ValueError)
_ZIP_LOCAL = struct.Struct("<4sHHHHHIIIHH")
_ZIP_DEFLATED = 8
_ZIP_BZIP2 = 12
_ZIP_LZMA = 14
_ZIP_SIZES_AFTER_DATA = 0x08  # flag bit 3: sizes follow the data, the header has none
_ZIP_UTF8_NAME = 0x800


#: A GNU long-name or pax header block tarfile reads whole into memory; a bigger one
#: stops the read (a 0.78 MB `.tar.gz` can declare a 768 MiB name, T51 review).
_MAX_TAR_HEADER_BYTES = 1024 * 1024
_TAR_LONG_HEADERS = (
    tarfile.GNUTYPE_LONGNAME, tarfile.GNUTYPE_LONGLINK, tarfile.XHDTYPE, tarfile.XGLTYPE, tarfile.SOLARIS_XHDTYPE
)


class ArchiveCutShort(Exception):
    """The archive ended or broke before its end; every byte before the break was yielded."""


class ArchiveOverLimit(Exception):
    """The archive unpacked past its byte cap or ran past its time budget."""


class ArchiveLimits:
    """One archive's caps: EVERY decompressed byte counts (also those tarfile reads
    or skips itself), and the clock is read at each step, not only while scanning.
    Past either, the streams end (``is_over``): what already came out is scanned."""

    def __init__(self, max_bytes: int, deadline: float) -> None:
        self.max_bytes, self.deadline = max_bytes, deadline
        self.expanded = 0
        self.is_over = False

    def count_bytes(self, size: int) -> None:
        self.expanded += size
        if self.expanded > self.max_bytes or time.monotonic() >= self.deadline:
            self.is_over = True

    def check_limits(self) -> None:
        if self.is_over or time.monotonic() >= self.deadline:
            self.is_over = True
            raise ArchiveOverLimit


def _get_archive_kind(head: bytes) -> str | None:
    """The archive format of a file, from its first bytes (512 for a plain tar):
    a compressed file's CONTENT is not in its raw bytes, so the raw scan cannot
    see it. A zip's stored members and a plain tar's members are plain in the
    raw bytes: only their NAMES are read here (``_read_archive_members``)."""
    if head[:2] == b"\x1f\x8b":
        return "gzip"
    if head[:3] == b"BZh":
        return "bz2"
    if head[:6] == b"\xfd7zXZ\x00":
        return "xz"
    if head[:4] in (b"PK\x03\x04", b"PK\x05\x06"):
        return "zip"
    if head[257:262] == b"ustar":
        return "tar"
    return None


_DECOMPRESSORS = {
    "gzip": lambda: zlib.decompressobj(wbits=47),  # 32 + 15: a gzip or zlib header
    "deflate": lambda: zlib.decompressobj(wbits=-15),  # a zip member: raw deflate
    "bz2": bz2.BZ2Decompressor,
    "xz": lzma.LZMADecompressor,
    "zip-bz2": bz2.BZ2Decompressor,
}
_ZLIB_KINDS = ("gzip", "deflate")
#: A zip member is one stream: its end is the member's end, never a next stream.
_ONE_STREAM_KINDS = ("deflate", "zip-bz2", "zip-lzma")


class _Unpacked:
    """One compressed stream, decompressed piece by piece. Where the input ends
    early or breaks (truncated, corrupt) reading ends too, with ``is_cut`` set:
    what came out before the break is still returned, never dropped with it."""

    def __init__(self, raw: BinaryIO, kind: str, limits: ArchiveLimits, decompressor: Any = None) -> None:
        self._raw, self._kind, self._limits = raw, kind, limits
        self._decompressor = decompressor or _DECOMPRESSORS[kind]()
        self._pending = b""
        self._out = bytearray()
        self._is_done = False
        self.is_cut = False

    def read(self, size: int | None = -1) -> bytes:
        want = (1 << 62) if size is None or size < 0 else size
        while len(self._out) < want and not self._is_done and not self._limits.is_over:
            try:
                self._step(min(want - len(self._out), _MAX_OUT))
            except _DECOMPRESS_ERRORS:
                self.is_cut = self._is_done = True
        piece = bytes(self._out[:want])
        del self._out[:want]
        if not piece and want:
            self._limits.check_limits()  # an older tarfile seek loops on empty reads (2^62-byte member)
        return piece

    def _step(self, want: int) -> None:
        decompressor = self._decompressor
        if decompressor.eof:
            # zlib leaves the leftover in BOTH `unused_data` and `unconsumed_tail` here.
            self._pending = b""
            self._start_next_stream(decompressor.unused_data)
            return
        if self._kind in _ZLIB_KINDS:
            data = self._pending or self._raw.read(_PIECE)
            if not data:
                self.is_cut = self._is_done = True
                return
            self._take(decompressor.decompress(data, want))
            self._pending = decompressor.unconsumed_tail
            return
        data = b""
        if decompressor.needs_input:
            data, self._pending = self._pending or self._raw.read(_PIECE), b""
            if not data:
                self.is_cut = self._is_done = True
                return
        self._take(decompressor.decompress(data, max_length=want))

    def _take(self, out: bytes) -> None:
        self._out += out
        self._limits.count_bytes(len(out))

    def _start_next_stream(self, rest: bytes) -> None:
        """After one stream ends: the next one of a multi-stream `.gz`/`.bz2`/`.xz`,
        or the clean end (trailing zero padding is ignored, as `gzip.open` does)."""
        while not rest.strip(b"\x00"):
            rest = self._raw.read(_PIECE)
            if not rest or self._kind in _ONE_STREAM_KINDS:
                self._is_done = True
                return
        if self._kind in _ONE_STREAM_KINDS:
            self._is_done = True
            return
        self._decompressor = _DECOMPRESSORS[self._kind]()
        self._pending = rest


class _MemberBytes:
    """At most ``size`` bytes of ``source``; a short read (the archive broke) ends it."""

    def __init__(self, source: Any, size: int) -> None:
        self._source, self._left = source, size

    def read(self, size: int) -> bytes:
        size = min(size, self._left)
        if size <= 0:
            return b""
        piece = self._source.read(size)
        self._left = self._left - len(piece) if len(piece) == size else 0
        return piece


class _TimedRaw:
    """A plain tar's raw file: an empty read checks the limits, as `_Unpacked` does."""

    def __init__(self, raw: BinaryIO, limits: ArchiveLimits) -> None:
        self._raw, self._limits = raw, limits

    def read(self, size: int = -1) -> bytes:
        piece = self._raw.read(size)
        if not piece and size:
            self._limits.check_limits()
        return piece


class _CountedBytes:
    """A member stream another library decompresses (an intact zip's), its output counted."""

    def __init__(self, source: Any, limits: ArchiveLimits) -> None:
        self._source, self._limits = source, limits

    def read(self, size: int) -> bytes:
        if self._limits.is_over:
            return b""
        piece = self._source.read(size)
        self._limits.count_bytes(len(piece))
        return piece


class _BoundedTarInfo(tarfile.TarInfo):
    """A tar header that refuses a long-name or pax block over `_MAX_TAR_HEADER_BYTES`."""

    def _proc_member(self, tarfile: Any) -> Any:  # tarfile's own hook, so its name
        if self.type in _TAR_LONG_HEADERS and self.size > _MAX_TAR_HEADER_BYTES:
            raise ArchiveOverLimit
        return super()._proc_member(tarfile)


def _read_tar_entries(tar: tarfile.TarFile, limits: ArchiveLimits) -> Iterator[tarfile.TarInfo]:
    """A stream-mode tar's entries, one at a time: `tar.members` is cleared each
    step (stream mode keeps every entry, 2M empty members held 728 MB) and the
    limits are checked between entries."""
    while True:
        limits.check_limits()
        info = tar.next()
        tar.members.clear()
        if info is None:
            return
        yield info


def _read_archive_members(path: str | BinaryIO, kind: str, limits: ArchiveLimits) -> Iterator[tuple[str, Any]]:
    """``(member name, readable or None)`` pairs: every member of a tar, zip or
    compressed tar, or the one stream of a plain `.gz`/`.bz2`/`.xz`. ``None``
    means its bytes are plain in the file's raw bytes (a stored zip member, a
    plain tar's member): only its name is checked. One level deep. Raises
    ``ArchiveCutShort`` after the last byte it could read when the archive
    breaks early, ``ArchiveOverLimit`` past ``limits``. ``path`` may be an open
    binary file (the output sweep)."""
    if isinstance(path, str):
        with open(path, "rb") as raw:
            yield from _read_archive_members(raw, kind, limits)
        return
    reader = _MEMBER_READERS.get(kind)
    if reader is not None:
        yield from reader(path, limits)
        return
    name = os.path.basename(getattr(path, "name", "") or "").rsplit(".", 1)[0]
    yield from _read_compressed(path, kind, name, limits)


def _read_compressed(raw: BinaryIO, kind: str, name: str, limits: ArchiveLimits) -> Iterator[tuple[str, Any]]:
    unpacked = _Unpacked(raw, kind, limits)
    try:
        tar = tarfile.open(fileobj=unpacked, mode="r|", tarinfo=_BoundedTarInfo)
    except tarfile.ReadError:
        tar = None
    if tar is not None and tar.firstmember is None:
        tar.close()  # opens as an empty tar when the content starts with a zero block: read it plain
        tar = None
    if tar is None:
        raw.seek(0)
        unpacked = _Unpacked(raw, kind, limits)
        yield name, unpacked
    else:
        with tar:
            for info in _read_tar_entries(tar, limits):
                if info.isfile():
                    # Read through the tar's own stream, not `extractfile`: that one
                    # raises on a short read and drops the bytes it already had.
                    yield info.name, _MemberBytes(tar.fileobj, info.size)
    if unpacked.is_cut:
        raise ArchiveCutShort


def _read_tar_names(raw: BinaryIO, limits: ArchiveLimits) -> Iterator[tuple[str, Any]]:
    """A plain tar's member names, each as it is read. A break ends them without a
    finding: its bytes, member contents included, are already in the raw scan."""
    try:
        with tarfile.open(fileobj=_TimedRaw(raw, limits), mode="r|", tarinfo=_BoundedTarInfo) as tar:
            for info in _read_tar_entries(tar, limits):
                if info.isfile():
                    yield info.name, None
    except tarfile.TarError:
        return


def _read_zip_members(raw: BinaryIO, limits: ArchiveLimits) -> Iterator[tuple[str, Any]]:
    try:
        archive = zipfile.ZipFile(raw)
    except zipfile.BadZipFile:
        raw.seek(0)
        yield from _walk_zip_local_headers(raw, limits)
        return
    with archive:
        for info in archive.infolist():
            if info.is_dir():
                continue
            if info.compress_type == zipfile.ZIP_STORED:
                yield info.filename, None
                continue
            with archive.open(info) as member:
                yield info.filename, _CountedBytes(member, limits)


def _walk_zip_local_headers(raw: BinaryIO, limits: ArchiveLimits) -> Iterator[tuple[str, Any]]:
    """A zip with no central directory (cut short): its members from their local
    headers, compressed ones (deflate, bzip2, lzma) unpacked to wherever they
    break. A member whose sizes follow its data (a zip written to a pipe) is the
    last one this can find."""
    while True:
        head = raw.read(_ZIP_LOCAL.size)
        if len(head) < _ZIP_LOCAL.size or head[:4] != b"PK\x03\x04":
            break
        _, _, flags, method, _, _, _, packed_size, _, name_len, extra_len = _ZIP_LOCAL.unpack(head)
        name = raw.read(name_len).decode("utf-8" if flags & _ZIP_UTF8_NAME else "cp437", "replace")
        raw.read(extra_len)
        is_sized = not flags & _ZIP_SIZES_AFTER_DATA
        start = raw.tell()
        if method in (_ZIP_DEFLATED, _ZIP_BZIP2, _ZIP_LZMA):
            source = _MemberBytes(raw, packed_size) if is_sized else raw
            yield name, _unpack_zip_member(source, method, limits)
        elif not name.endswith("/"):
            yield name, None
        if not is_sized:
            break
        raw.seek(start + packed_size)
    raise ArchiveCutShort


def _unpack_zip_member(source: Any, method: int, limits: ArchiveLimits) -> _Unpacked:
    if method == _ZIP_DEFLATED:
        return _Unpacked(source, "deflate", limits)
    if method == _ZIP_BZIP2:
        return _Unpacked(source, "zip-bz2", limits)
    # A zip's lzma member: a 4-byte header (version, properties size), then the
    # LZMA1 properties (lc/lp/pb byte, dictionary size), then the raw stream.
    _, props_size = struct.unpack("<HH", source.read(4))
    props = source.read(props_size)
    lc_lp_pb, dict_size = props[0], int.from_bytes(props[1:5], "little")
    lzma_filter = {"id": lzma.FILTER_LZMA1, "dict_size": dict_size,
                   "lc": lc_lp_pb % 9, "lp": lc_lp_pb // 9 % 5, "pb": lc_lp_pb // 45}
    decompressor = lzma.LZMADecompressor(lzma.FORMAT_RAW, filters=[lzma_filter])
    return _Unpacked(source, "zip-lzma", limits, decompressor)


_MEMBER_READERS = {"zip": _read_zip_members, "tar": _read_tar_names}
