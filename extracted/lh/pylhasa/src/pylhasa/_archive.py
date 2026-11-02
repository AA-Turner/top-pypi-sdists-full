from __future__ import annotations

import io
import os
import shutil
import tempfile
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from types import TracebackType
from typing import Dict, Iterable, Iterator, Optional, Union

from ._exceptions import BadArchiveError, PylhasaError, UnsafePathError
from ._paths import NormalizedPath, normalize_path

try:
    from . import _pylhasa
except ImportError as exc:  # pragma: no cover - import error shown at runtime
    raise ImportError("pylhasa native extension is not built") from exc


@dataclass(frozen=True)
class Entry:
    """
    Metadata for a single archive entry.

    Fields:
    - raw_path: best-effort decoded original path from the archive.
    - raw_path_bytes: raw path bytes from the archive.
    - safe_path: sanitized relative path (None if unsafe).
    - size: uncompressed size in bytes.
    - compressed_size: compressed size in bytes.
    - method: compression method string (e.g., "-lh5-").
    - crc: CRC-16 from header (None if absent).
    - timestamp: Unix timestamp if present (None if absent).
    - is_dir: True if entry is a directory.
    - is_symlink: True if entry is a symlink.
    - header_level: LHA header level (0-3).
    - os_type: OS type byte from header.
    - extra_flags: parsed extended header flags bitfield.
    - unix_perms: Unix permissions if present.
    - unix_uid: Unix UID if present.
    - unix_gid: Unix GID if present.
    - os9_perms: OS-9 permissions if present.
    - unix_username: Unix username if present.
    - unix_group: Unix group name if present.
    - common_crc: common header CRC if present.
    - win_creation_time: Windows FILETIME creation time if present.
    - win_modification_time: Windows FILETIME modification time if present.
    - win_access_time: Windows FILETIME access time if present.
    - datetime_utc(): best-effort UTC datetime (Windows FILETIME if present, otherwise Unix timestamp).
    - symlink_target: symlink target if present.
    - raw_header_bytes: raw header bytes if present.
    - path: directory path component if present.
    - filename: filename component if present.
    """
    raw_path: str
    raw_path_bytes: bytes
    safe_path: Optional[str]
    size: int
    compressed_size: int
    method: str
    crc: Optional[int]
    timestamp: Optional[int]
    is_dir: bool
    is_symlink: bool
    header_level: int
    os_type: int
    extra_flags: int
    unix_perms: Optional[int]
    unix_uid: Optional[int]
    unix_gid: Optional[int]
    os9_perms: Optional[int]
    unix_username: Optional[str]
    unix_group: Optional[str]
    common_crc: Optional[int]
    win_creation_time: Optional[int]
    win_modification_time: Optional[int]
    win_access_time: Optional[int]
    symlink_target: Optional[str]
    raw_header_bytes: Optional[bytes]
    path: Optional[str]
    filename: Optional[str]
    _index: int
    _archive: "Archive"

    def open(self) -> io.BufferedReader:
        """Open the entry for streaming reads of decompressed data."""
        return self._archive._open_entry(self)

    def read(self) -> bytes:
        """Read the entry fully into memory (convenience API)."""
        return self._archive.read(self)

    def datetime_utc(self) -> Optional[datetime]:
        """
        Return the best available timestamp as a timezone-aware UTC datetime.

        Prefers Windows FILETIME modification time when present, otherwise
        falls back to the Unix timestamp.
        """
        if self.win_modification_time is not None:
            return _filetime_to_datetime(self.win_modification_time)
        if self.timestamp is None:
            return None
        return datetime.fromtimestamp(self.timestamp, tz=timezone.utc)


class _EntryRawIO(io.RawIOBase):
    def __init__(self, reader: "_pylhasa.EntryReader") -> None:
        self._reader = reader

    def readable(self) -> bool:
        return True

    def read(self, size: int = -1) -> bytes:
        return self._reader.read(size)

    def readinto(self, b: bytearray) -> int:
        return self._reader.readinto(b)

    def close(self) -> None:
        if self._reader is not None:
            self._reader.close()
            self._reader = None
        super().close()


_CRC16_TABLE = [
    0x0000, 0xC0C1, 0xC181, 0x0140, 0xC301, 0x03C0, 0x0280, 0xC241,
    0xC601, 0x06C0, 0x0780, 0xC741, 0x0500, 0xC5C1, 0xC481, 0x0440,
    0xCC01, 0x0CC0, 0x0D80, 0xCD41, 0x0F00, 0xCFC1, 0xCE81, 0x0E40,
    0x0A00, 0xCAC1, 0xCB81, 0x0B40, 0xC901, 0x09C0, 0x0880, 0xC841,
    0xD801, 0x18C0, 0x1980, 0xD941, 0x1B00, 0xDBC1, 0xDA81, 0x1A40,
    0x1E00, 0xDEC1, 0xDF81, 0x1F40, 0xDD01, 0x1DC0, 0x1C80, 0xDC41,
    0x1400, 0xD4C1, 0xD581, 0x1540, 0xD701, 0x17C0, 0x1680, 0xD641,
    0xD201, 0x12C0, 0x1380, 0xD341, 0x1100, 0xD1C1, 0xD081, 0x1040,
    0xF001, 0x30C0, 0x3180, 0xF141, 0x3300, 0xF3C1, 0xF281, 0x3240,
    0x3600, 0xF6C1, 0xF781, 0x3740, 0xF501, 0x35C0, 0x3480, 0xF441,
    0x3C00, 0xFCC1, 0xFD81, 0x3D40, 0xFF01, 0x3FC0, 0x3E80, 0xFE41,
    0xFA01, 0x3AC0, 0x3B80, 0xFB41, 0x3900, 0xF9C1, 0xF881, 0x3840,
    0x2800, 0xE8C1, 0xE981, 0x2940, 0xEB01, 0x2BC0, 0x2A80, 0xEA41,
    0xEE01, 0x2EC0, 0x2F80, 0xEF41, 0x2D00, 0xEDC1, 0xEC81, 0x2C40,
    0xE401, 0x24C0, 0x2580, 0xE541, 0x2700, 0xE7C1, 0xE681, 0x2640,
    0x2200, 0xE2C1, 0xE381, 0x2340, 0xE101, 0x21C0, 0x2080, 0xE041,
    0xA001, 0x60C0, 0x6180, 0xA141, 0x6300, 0xA3C1, 0xA281, 0x6240,
    0x6600, 0xA6C1, 0xA781, 0x6740, 0xA501, 0x65C0, 0x6480, 0xA441,
    0x6C00, 0xACC1, 0xAD81, 0x6D40, 0xAF01, 0x6FC0, 0x6E80, 0xAE41,
    0xAA01, 0x6AC0, 0x6B80, 0xAB41, 0x6900, 0xA9C1, 0xA881, 0x6840,
    0x7800, 0xB8C1, 0xB981, 0x7940, 0xBB01, 0x7BC0, 0x7A80, 0xBA41,
    0xBE01, 0x7EC0, 0x7F80, 0xBF41, 0x7D00, 0xBDC1, 0xBC81, 0x7C40,
    0xB401, 0x74C0, 0x7580, 0xB541, 0x7700, 0xB7C1, 0xB681, 0x7640,
    0x7200, 0xB2C1, 0xB381, 0x7340, 0xB101, 0x71C0, 0x7080, 0xB041,
    0x5000, 0x90C1, 0x9181, 0x5140, 0x9301, 0x53C0, 0x5280, 0x9241,
    0x9601, 0x56C0, 0x5780, 0x9741, 0x5500, 0x95C1, 0x9481, 0x5440,
    0x9C01, 0x5CC0, 0x5D80, 0x9D41, 0x5F00, 0x9FC1, 0x9E81, 0x5E40,
    0x5A00, 0x9AC1, 0x9B81, 0x5B40, 0x9901, 0x59C0, 0x5880, 0x9841,
    0x8801, 0x48C0, 0x4980, 0x8941, 0x4B00, 0x8BC1, 0x8A81, 0x4A40,
    0x4E00, 0x8EC1, 0x8F81, 0x4F40, 0x8D01, 0x4DC0, 0x4C80, 0x8C41,
    0x4400, 0x84C1, 0x8581, 0x4540, 0x8701, 0x47C0, 0x4680, 0x8641,
    0x8201, 0x42C0, 0x4380, 0x8341, 0x4100, 0x81C1, 0x8081, 0x4040,
]


def _crc16_update(crc: int, data: bytes) -> int:
    for b in data:
        crc = ((crc >> 8) ^ _CRC16_TABLE[(crc ^ b) & 0xFF]) & 0xFFFF
    return crc


def _filetime_to_datetime(filetime: Optional[int]) -> Optional[datetime]:
    if filetime is None:
        return None
    # Windows FILETIME is 100-ns intervals since 1601-01-01 UTC.
    seconds = filetime / 10_000_000
    return datetime(1601, 1, 1, tzinfo=timezone.utc) + timedelta(seconds=seconds)


class Archive(Iterable[Entry]):
    """
    High-level archive wrapper that provides iteration and extraction.

    Entries are materialized on open. Use `read()` for convenience or
    `Entry.open()` to stream decompressed bytes.
    """
    def __init__(self, backend: "_pylhasa.Archive", temp_path: Optional[Path] = None) -> None:
        self._backend = backend
        self._temp_path = temp_path
        self._closed = False
        self._entries = self._load_entries()
        self._entries_by_raw: Dict[str, Entry] = {entry.raw_path: entry for entry in self._entries}

    def _load_entries(self) -> list[Entry]:
        entries = []
        for idx, meta in enumerate(self._backend.entries()):
            raw_bytes = meta["raw_path_bytes"]
            if not isinstance(raw_bytes, (bytes, bytearray)):
                raw_bytes = bytes(raw_bytes)
            norm = normalize_path(bytes(raw_bytes))
            entry = Entry(
                raw_path=norm.raw_path,
                raw_path_bytes=norm.raw_path_bytes,
                safe_path=norm.safe_path,
                size=int(meta["size"]),
                compressed_size=int(meta["compressed_size"]),
                method=str(meta["method"]),
                crc=None if meta["crc"] is None else int(meta["crc"]),
                timestamp=None if meta["timestamp"] is None else int(meta["timestamp"]),
                is_dir=bool(meta["is_dir"]),
                is_symlink=bool(meta.get("is_symlink", False)),
                header_level=int(meta.get("header_level", 0)),
                os_type=int(meta.get("os_type", 0)),
                extra_flags=int(meta.get("extra_flags", 0)),
                unix_perms=None if meta.get("unix_perms") is None else int(meta["unix_perms"]),
                unix_uid=None if meta.get("unix_uid") is None else int(meta["unix_uid"]),
                unix_gid=None if meta.get("unix_gid") is None else int(meta["unix_gid"]),
                os9_perms=None if meta.get("os9_perms") is None else int(meta["os9_perms"]),
                unix_username=None if meta.get("unix_username") is None else str(meta["unix_username"]),
                unix_group=None if meta.get("unix_group") is None else str(meta["unix_group"]),
                common_crc=None if meta.get("common_crc") is None else int(meta["common_crc"]),
                win_creation_time=None if meta.get("win_creation_time") is None else int(meta["win_creation_time"]),
                win_modification_time=None if meta.get("win_modification_time") is None else int(meta["win_modification_time"]),
                win_access_time=None if meta.get("win_access_time") is None else int(meta["win_access_time"]),
                symlink_target=None if meta.get("symlink_target") is None else str(meta["symlink_target"]),
                raw_header_bytes=None if meta.get("raw_header_bytes") is None else bytes(meta["raw_header_bytes"]),
                path=None if meta.get("path") is None else str(meta["path"]),
                filename=None if meta.get("filename") is None else str(meta["filename"]),
                _index=idx,
                _archive=self,
            )
            entries.append(entry)
        return entries

    def __iter__(self) -> Iterator[Entry]:
        return iter(self._entries)

    def __enter__(self) -> "Archive":
        return self

    def __exit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc: Optional[BaseException],
        tb: Optional[TracebackType],
    ) -> None:
        self.close()

    def __del__(self) -> None:  # pragma: no cover - best-effort cleanup
        try:
            self.close()
        except Exception:
            pass

    def close(self) -> None:
        if self._closed:
            return
        self._backend.close()
        self._closed = True
        if self._temp_path is not None:
            try:
                self._temp_path.unlink(missing_ok=True)
            except OSError:
                pass

    def _open_entry(self, entry: Entry) -> io.BufferedReader:
        reader = self._backend.open_entry(entry._index)
        raw = _EntryRawIO(reader)
        return io.BufferedReader(raw)

    def read(self, name_or_entry: Union[str, Entry]) -> bytes:
        """Read an entry fully into memory."""
        entry = self._resolve_entry(name_or_entry)
        if entry.is_dir or entry.is_symlink:
            return b""
        with entry.open() as fp:
            return fp.read()

    def extract(
        self,
        name_or_entry: Union[str, Entry],
        dest_dir: Union[str, Path],
        safe: bool = True,
        allow_symlinks: bool = False,
        verify_crc: bool = True,
    ) -> Path:
        """Extract a single entry to disk."""
        entry = self._resolve_entry(name_or_entry)
        return self._extract_entry(entry, Path(dest_dir), safe=safe, allow_symlinks=allow_symlinks, verify_crc=verify_crc)

    def extractall(
        self,
        dest_dir: Union[str, Path],
        safe: bool = True,
        allow_symlinks: bool = False,
        verify_crc: bool = True,
    ) -> list[Path]:
        """Extract all entries to disk."""
        dest = Path(dest_dir)
        extracted: list[Path] = []
        for entry in self._entries:
            extracted.append(self._extract_entry(entry, dest, safe=safe, allow_symlinks=allow_symlinks, verify_crc=verify_crc))
        return extracted

    def _resolve_entry(self, name_or_entry: Union[str, Entry]) -> Entry:
        if isinstance(name_or_entry, Entry):
            return name_or_entry
        if not isinstance(name_or_entry, str):
            raise TypeError("expected entry name or Entry")
        if name_or_entry in self._entries_by_raw:
            return self._entries_by_raw[name_or_entry]
        for entry in self._entries:
            if entry.safe_path == name_or_entry:
                return entry
        raise KeyError(f"entry not found: {name_or_entry}")

    def _extract_entry(self, entry: Entry, dest_dir: Path, safe: bool, allow_symlinks: bool, verify_crc: bool) -> Path:
        if safe:
            if entry.safe_path is None:
                raise UnsafePathError(f"unsafe entry path: {entry.raw_path}")
            rel_path = Path(entry.safe_path)
        else:
            rel_path = Path(entry.raw_path)

        if entry.is_symlink and not allow_symlinks:
            raise UnsafePathError(f"symlink entry blocked: {entry.raw_path}")

        dest_dir = dest_dir.resolve()
        target = (dest_dir / rel_path).resolve()

        if safe:
            try:
                common = os.path.commonpath([str(dest_dir), str(target)])
            except ValueError:
                raise UnsafePathError(f"unsafe entry path: {entry.raw_path}")
            if common != str(dest_dir):
                raise UnsafePathError(f"unsafe entry path: {entry.raw_path}")

        if entry.is_dir:
            target.mkdir(parents=True, exist_ok=True)
            return target

        target.parent.mkdir(parents=True, exist_ok=True)
        crc = 0
        do_crc = verify_crc and entry.crc is not None
        with entry.open() as src, target.open("wb") as dst:
            while True:
                chunk = src.read(131072)
                if not chunk:
                    break
                if do_crc:
                    crc = _crc16_update(crc, chunk)
                dst.write(chunk)
        if do_crc:
            if crc != entry.crc:
                try:
                    target.unlink()
                except OSError:
                    pass
                raise BadArchiveError(f"CRC mismatch for {entry.raw_path}")
        return target


def _open_from_path(path: Union[str, Path]) -> Archive:
    resolved = os.path.expanduser(os.fspath(path))
    backend = _pylhasa.open_path(resolved)
    return Archive(backend)


def _open_from_bytes(data: bytes) -> Archive:
    backend = _pylhasa.open_bytes(data)
    return Archive(backend)


def _open_from_fileobj(fileobj: io.BufferedIOBase, buffering: int) -> Archive:
    if buffering <= 0:
        raise ValueError("buffering must be positive")
    # Spool to a temp file so liblhasa can stream without loading all bytes.
    temp = tempfile.NamedTemporaryFile(prefix="pylhasa_", suffix=".lha", delete=False)
    temp_path = Path(temp.name)
    try:
        shutil.copyfileobj(fileobj, temp, length=buffering)
    finally:
        temp.close()
    backend = _pylhasa.open_path(os.fspath(temp_path))
    return Archive(backend, temp_path=temp_path)


def open(path: Union[str, Path]) -> Archive:
    """
    Open an LHA/LZH archive from a file path.

    The path supports `~` expansion. The archive is parsed eagerly to
    collect entry metadata.
    """
    return _open_from_path(path)


def open_bytes(data: bytes) -> Archive:
    """
    Open an LHA/LZH archive from bytes in memory.

    This keeps a reference to the bytes for the lifetime of the archive.
    """
    if not isinstance(data, (bytes, bytearray, memoryview)):
        raise TypeError("data must be bytes-like")
    return _open_from_bytes(bytes(data))


def from_bytes(data: bytes) -> Archive:
    """Alias for open_bytes()."""
    return open_bytes(data)


def open_fileobj(fileobj: io.BufferedIOBase, buffering: int = 131072) -> Archive:
    """
    Open an LHA/LZH archive from a file-like object.

    The stream is spooled to a temporary file to avoid loading the full
    archive into memory.
    """
    if not hasattr(fileobj, "read"):
        raise TypeError("fileobj must be file-like")
    return _open_from_fileobj(fileobj, buffering)
