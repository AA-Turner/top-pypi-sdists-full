"""Unit tests for AES-256-GCM protected storage (FR-011, FR-012, SC-017)."""

from __future__ import annotations

from pathlib import Path

import pytest

from agentic_devtools.orchestration.hierarchy.protected_storage import (
    ProtectedStorage,
    RemoteStorageRejectedError,
    _is_local_absolute_path,
    derive_caller_identity,
)


@pytest.fixture
def master_key() -> bytes:
    return b"unit-test-master-key-material-32b"


@pytest.fixture
def authorized_principals() -> frozenset[str]:
    return frozenset({derive_caller_identity()})


def test_rejects_non_absolute_path(tmp_path: Path, master_key: bytes) -> None:
    with pytest.raises(RemoteStorageRejectedError):
        ProtectedStorage(Path("relative/path.ndjson"), master_key=master_key)


def test_rejects_uri_scheme_path(master_key: bytes) -> None:
    with pytest.raises(RemoteStorageRejectedError):
        ProtectedStorage(Path("https://example.com/snapshot"), master_key=master_key)


def test_is_local_absolute_path_rejects_uri_scheme() -> None:
    assert _is_local_absolute_path(Path("https://example.com/x")) is False


def test_is_local_absolute_path_accepts_absolute_local_path(tmp_path: Path) -> None:
    assert _is_local_absolute_path(tmp_path / "x.ndjson") is True


def test_is_local_absolute_path_rejects_relative_path() -> None:
    assert _is_local_absolute_path(Path("relative/x.ndjson")) is False
