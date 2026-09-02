"""Tests for ``_write_hierarchy_lock_metadata``."""

import json
import os
from pathlib import Path
from unittest.mock import patch

import pytest

from agentic_devtools.cli.speckit.scaffold_new_feature import _write_hierarchy_lock_metadata


def test_writes_json_owner_metadata(tmp_path: Path) -> None:
    lock_path = tmp_path / ".hierarchy.yml.lock"
    fd = os.open(lock_path, os.O_CREAT | os.O_RDWR)
    try:
        _write_hierarchy_lock_metadata(fd)
    finally:
        os.close(fd)

    payload = json.loads(lock_path.read_text(encoding="utf-8"))
    assert payload["pid"] == os.getpid()
    assert isinstance(payload["created_at"], float)


def test_writes_partial_os_writes_until_complete(tmp_path: Path) -> None:
    lock_path = tmp_path / ".hierarchy.yml.lock"
    fd = os.open(lock_path, os.O_CREAT | os.O_RDWR)
    writes: list[int] = []

    def write_partially(_fd: int, data: bytes | bytearray | memoryview) -> int:
        writes.append(len(data))
        return 1 if len(writes) == 1 else len(data)

    try:
        with patch("agentic_devtools.cli.speckit.scaffold_new_feature.os.write", side_effect=write_partially):
            _write_hierarchy_lock_metadata(fd)
    finally:
        os.close(fd)

    assert len(writes) == 2


def test_rejects_zero_length_os_write(tmp_path: Path) -> None:
    lock_path = tmp_path / ".hierarchy.yml.lock"
    fd = os.open(lock_path, os.O_CREAT | os.O_RDWR)
    try:
        with patch("agentic_devtools.cli.speckit.scaffold_new_feature.os.write", return_value=0):
            with pytest.raises(OSError, match="Could not write hierarchy lock metadata"):
                _write_hierarchy_lock_metadata(fd)
    finally:
        os.close(fd)
