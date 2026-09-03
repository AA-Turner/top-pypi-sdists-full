"""Unit tests for AES-256-GCM protected storage (FR-011, FR-012, SC-017)."""

from __future__ import annotations

from pathlib import Path

import pytest

from agentic_devtools.orchestration.hierarchy.protected_storage import (
    MasterKeyUnavailableError,
    ProtectedStorage,
    derive_caller_identity,
    resolve_master_key,
)


@pytest.fixture
def authorized_principals() -> frozenset[str]:
    return frozenset({derive_caller_identity()})


def test_resolve_master_key_from_env_var(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("AGDT_HIERARCHY_MASTER_KEY", "env-secret")
    assert resolve_master_key() == b"env-secret"


def test_resolve_master_key_from_secret_file(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("AGDT_HIERARCHY_MASTER_KEY", raising=False)
    monkeypatch.setattr("keyring.get_password", lambda *a, **k: None)
    secret_file = tmp_path / "secret.txt"
    secret_file.write_text("file-secret\n", encoding="utf-8")
    assert resolve_master_key(secret_file=secret_file) == b"file-secret"


def test_resolve_master_key_from_keyring(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("AGDT_HIERARCHY_MASTER_KEY", raising=False)
    monkeypatch.setattr("keyring.get_password", lambda *a, **k: "keyring-secret")
    assert resolve_master_key() == b"keyring-secret"


def test_resolve_master_key_ignores_blank_secret_file_content(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("AGDT_HIERARCHY_MASTER_KEY", raising=False)
    monkeypatch.setattr("keyring.get_password", lambda *a, **k: None)
    secret_file = tmp_path / "secret.txt"
    secret_file.write_text("   \n", encoding="utf-8")
    with pytest.raises(MasterKeyUnavailableError):
        resolve_master_key(secret_file=secret_file)


def test_resolve_master_key_raises_when_no_source_available(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("AGDT_HIERARCHY_MASTER_KEY", raising=False)
    monkeypatch.setattr("keyring.get_password", lambda *a, **k: None)
    with pytest.raises(MasterKeyUnavailableError):
        resolve_master_key(secret_file=tmp_path / "does-not-exist.txt")


def test_empty_master_key_raises_value_error(tmp_path: Path, authorized_principals: frozenset[str]) -> None:
    """An empty master key must be rejected at construction time."""
    with pytest.raises(ValueError, match="master_key must be at least 32 bytes"):
        ProtectedStorage(tmp_path / "s.ndjson", master_key=b"", authorized_principals=authorized_principals)
