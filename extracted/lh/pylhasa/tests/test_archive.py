from __future__ import annotations

import io
from pathlib import Path

import pytest

import pylhasa
from pylhasa import Entry, UnsafePathError
from pylhasa._paths import normalize_path


def fixture_path(name: str) -> Path:
    return Path(__file__).parent / "fixtures" / name


def test_open_bytes_and_read() -> None:
    data = fixture_path("sample.lzh").read_bytes()
    archive = pylhasa.open_bytes(data)
    try:
        entries = list(archive)
        assert len(entries) >= 1
        entry = entries[0]
        payload = archive.read(entry)
        assert len(payload) == entry.size
    finally:
        archive.close()


def test_open_fileobj_streaming() -> None:
    data = fixture_path("sample.lzh").read_bytes()
    bio = io.BytesIO(data)
    archive = pylhasa.open_fileobj(bio, buffering=8)
    try:
        entry = next(iter(archive))
        with entry.open() as fp:
            data = fp.read()
            assert len(data) == entry.size
    finally:
        archive.close()


def test_safe_path_rejects_traversal() -> None:
    norm = normalize_path(b"../evil.txt")
    assert norm.safe_path is None


def test_extractall_safe(tmp_path: Path) -> None:
    archive = pylhasa.open(fixture_path("sample.lzh"))
    try:
        extracted = archive.extractall(tmp_path, verify_crc=False)
        assert extracted
        for path in extracted:
            assert path.exists()
    finally:
        archive.close()


def test_extractall_unsafe_raises(tmp_path: Path) -> None:
    archive = pylhasa.open(fixture_path("sample.lzh"))
    try:
        entry = next(iter(archive))
        unsafe_entry = Entry(
            raw_path="../evil.txt",
            raw_path_bytes=b"../evil.txt",
            safe_path=None,
            size=entry.size,
            compressed_size=entry.compressed_size,
            method=entry.method,
            crc=entry.crc,
            timestamp=entry.timestamp,
            is_dir=False,
            is_symlink=False,
            header_level=entry.header_level,
            os_type=entry.os_type,
            extra_flags=entry.extra_flags,
            unix_perms=entry.unix_perms,
            unix_uid=entry.unix_uid,
            unix_gid=entry.unix_gid,
            os9_perms=entry.os9_perms,
            unix_username=entry.unix_username,
            unix_group=entry.unix_group,
            common_crc=entry.common_crc,
            win_creation_time=entry.win_creation_time,
            win_modification_time=entry.win_modification_time,
            win_access_time=entry.win_access_time,
            symlink_target=entry.symlink_target,
            raw_header_bytes=entry.raw_header_bytes,
            path=entry.path,
            filename=entry.filename,
            _index=entry._index,
            _archive=archive,
        )
        with pytest.raises(UnsafePathError):
            archive._extract_entry(unsafe_entry, tmp_path, safe=True, allow_symlinks=False, verify_crc=False)
    finally:
        archive.close()
