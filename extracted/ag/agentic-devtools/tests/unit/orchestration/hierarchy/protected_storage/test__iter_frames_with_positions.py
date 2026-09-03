"""Unit tests for AES-256-GCM protected storage (FR-011, FR-012, SC-017)."""

from __future__ import annotations

from pathlib import Path

import pytest

from agentic_devtools.orchestration.hierarchy.protected_storage import (
    ProtectedStorage,
    _iter_frames_with_positions,
    derive_caller_identity,
)


@pytest.fixture
def master_key() -> bytes:
    return b"unit-test-master-key-material-32b"


@pytest.fixture
def authorized_principals() -> frozenset[str]:
    return frozenset({derive_caller_identity()})


def test_positioned_frames_skip_blank_lines(
    tmp_path: Path, master_key: bytes, authorized_principals: frozenset[str]
) -> None:
    path = tmp_path / "frames.ndjson"
    storage = ProtectedStorage(path, master_key=master_key, authorized_principals=authorized_principals)
    storage.append(b"content")
    lines = path.read_text(encoding="utf-8").splitlines()
    path.write_text("\n" + lines[0] + "\n", encoding="utf-8")
    assert [position for position, _frame in _iter_frames_with_positions(path)] == [1]


def test_iter_frames_with_positions_returns_nothing_for_missing_path(tmp_path: Path) -> None:
    assert list(_iter_frames_with_positions(tmp_path / "missing.ndjson")) == []
