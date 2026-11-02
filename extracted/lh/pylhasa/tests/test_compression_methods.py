from __future__ import annotations

from pathlib import Path

import pytest

import pylhasa


def fixture_path(name: str) -> Path:
    return Path(__file__).parent / "fixtures" / name


METHOD_FIXTURES = [
    ("lh1.lzh", "-lh1-", False),
    ("lh2.lzh", "-lh2-", False),
    ("lh3.lzh", "-lh3-", False),
    ("lh4.lzh", "-lh4-", False),
    ("lh5.lzh", "-lh5-", False),
    ("lh6.lzh", "-lh6-", False),
    ("lh7.lzh", "-lh7-", False),
    ("lhd_dir.lzh", "-lhd-", True),
    ("lz4.lzs", "-lz4-", False),
    ("lz5.lzs", "-lz5-", False),
    ("lzs.lzs", "-lzs-", False),
]


@pytest.mark.parametrize("archive_name, method, dir_ok", METHOD_FIXTURES)
def test_compression_method_fixture(archive_name: str, method: str, dir_ok: bool) -> None:
    archive = pylhasa.open(fixture_path(archive_name))
    try:
        entries = [entry for entry in archive if entry.method == method]
        assert entries, f"no entries found for method {method}"
        if dir_ok:
            dir_entry = next(e for e in entries if e.is_dir or e.is_symlink)
            assert archive.read(dir_entry) == b""
            return
        entry = next(e for e in entries if not e.is_dir and not e.is_symlink)
        data = archive.read(entry)
        assert len(data) == entry.size
        assert entry.size > 0
    finally:
        archive.close()
