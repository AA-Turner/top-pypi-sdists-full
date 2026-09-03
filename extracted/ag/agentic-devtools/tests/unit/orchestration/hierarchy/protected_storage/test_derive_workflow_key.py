"""Unit tests for AES-256-GCM protected storage (FR-011, FR-012, SC-017)."""

from __future__ import annotations

import os

import pytest

from agentic_devtools.orchestration.hierarchy.protected_storage import (
    derive_workflow_key,
)


@pytest.fixture
def master_key() -> bytes:
    return b"unit-test-master-key-material-32b"


def test_derive_workflow_key_is_deterministic_for_same_salt(master_key: bytes) -> None:
    salt = os.urandom(16)
    key1 = derive_workflow_key(master_key, salt)
    key2 = derive_workflow_key(master_key, salt)
    assert key1 == key2
    assert len(key1) == 32


def test_derive_workflow_key_differs_for_different_salt(master_key: bytes) -> None:
    key1 = derive_workflow_key(master_key, os.urandom(16))
    key2 = derive_workflow_key(master_key, os.urandom(16))
    assert key1 != key2


def test_derive_workflow_key_rejects_low_entropy_master_key() -> None:
    with pytest.raises(ValueError, match="at least 32 bytes"):
        derive_workflow_key(b"short", os.urandom(16))
