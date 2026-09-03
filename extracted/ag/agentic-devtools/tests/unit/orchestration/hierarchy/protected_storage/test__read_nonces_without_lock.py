"""Unit tests for AES-256-GCM protected storage (FR-011, FR-012, SC-017)."""

from __future__ import annotations

import os
from pathlib import Path

import pytest

from agentic_devtools.orchestration.hierarchy.protected_storage import (
    NonceReuseError,
    ProtectedStorage,
    ProtectedStorageError,
    _read_nonces_without_lock,
    derive_caller_identity,
)


@pytest.fixture
def master_key() -> bytes:
    return b"unit-test-master-key-material-32b"


@pytest.fixture
def authorized_principals() -> frozenset[str]:
    return frozenset({derive_caller_identity()})


def test_read_nonces_without_lock_handles_missing_and_invalid_frames(tmp_path: Path) -> None:
    path = tmp_path / "nonces.ndjson"
    assert _read_nonces_without_lock(path) == set()
    path.write_text(
        'not json\n{"nonce": "YQ=="}\n{"nonce": "AAAAAAAA"}\n',
        encoding="utf-8",
    )
    assert _read_nonces_without_lock(path) == set()


def test_duplicate_nonce_raises(tmp_path: Path, master_key: bytes, authorized_principals: frozenset[str]) -> None:
    storage = ProtectedStorage(
        tmp_path / "snapshots.ndjson", master_key=master_key, authorized_principals=authorized_principals
    )
    nonce = os.urandom(12)
    storage.append(b"frame one", nonce=nonce)
    with pytest.raises(NonceReuseError):
        storage.append(b"frame two", nonce=nonce)


def test_append_rejects_wrong_length_nonce(
    tmp_path: Path, master_key: bytes, authorized_principals: frozenset[str]
) -> None:
    storage = ProtectedStorage(
        tmp_path / "snapshots.ndjson", master_key=master_key, authorized_principals=authorized_principals
    )
    with pytest.raises(ProtectedStorageError, match="96 bits"):
        storage.append(b"frame", nonce=b"too-short")
