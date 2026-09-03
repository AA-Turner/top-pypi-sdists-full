"""Unit tests for AES-256-GCM protected storage (FR-011, FR-012, SC-017)."""

from __future__ import annotations

from pathlib import Path

import pytest

from agentic_devtools.orchestration.hierarchy.protected_storage import (
    ProtectedStorage,
    UnauthorizedAccessError,
    authorize,
    derive_caller_identity,
)
from agentic_devtools.orchestration.hierarchy.trace import read_events


@pytest.fixture
def master_key() -> bytes:
    return b"unit-test-master-key-material-32b"


@pytest.fixture
def authorized_principals() -> frozenset[str]:
    return frozenset({derive_caller_identity()})


def test_rejects_missing_authorized_principals(tmp_path: Path, master_key: bytes) -> None:
    with pytest.raises(ValueError, match="authorized_principals"):
        ProtectedStorage(tmp_path / "snapshots.ndjson", master_key=master_key)


def test_rejects_empty_authorized_principals(tmp_path: Path, master_key: bytes) -> None:
    with pytest.raises(ValueError, match="authorized_principals"):
        ProtectedStorage(tmp_path / "snapshots.ndjson", master_key=master_key, authorized_principals=frozenset())


def test_rejects_blank_authorized_principal_name(tmp_path: Path, master_key: bytes) -> None:
    with pytest.raises(ValueError, match="authorized_principals"):
        ProtectedStorage(
            tmp_path / "snapshots.ndjson",
            master_key=master_key,
            authorized_principals=frozenset({"   "}),
        )


def test_authorize_rejects_identity_not_in_allowlist() -> None:
    with pytest.raises(UnauthorizedAccessError):
        authorize(operation="write_snapshot", allowlist=frozenset({"nonexistent-user-xyz"}))


def test_authorize_ignores_asserted_identity_bypass_attempt() -> None:
    """An asserted allowlisted principal name passed as an argument must not bypass the check."""
    real_identity = derive_caller_identity()
    with pytest.raises(UnauthorizedAccessError):
        authorize(
            operation="write_snapshot",
            allowlist=frozenset({"someone-else-entirely"}),
            asserted_identity=real_identity,  # even asserting the real identity must not matter here
        )


def test_authorize_succeeds_when_derived_identity_allowlisted() -> None:
    real_identity = derive_caller_identity()
    result = authorize(operation="write_snapshot", allowlist=frozenset({real_identity}))
    assert result == real_identity


def test_storage_enforces_allowlist_on_write_and_read(tmp_path: Path, master_key: bytes) -> None:
    path = tmp_path / "protected.ndjson"
    storage = ProtectedStorage(path, master_key=master_key, authorized_principals=frozenset({"other-user"}))
    with pytest.raises(UnauthorizedAccessError):
        storage.append(b"secret")
    with pytest.raises(UnauthorizedAccessError):
        storage.read_all()


def test_storage_ignores_asserted_identity_on_write(tmp_path: Path, master_key: bytes) -> None:
    storage = ProtectedStorage(
        tmp_path / "protected.ndjson",
        master_key=master_key,
        authorized_principals=frozenset({"other-user"}),
        asserted_identity=derive_caller_identity(),
    )
    with pytest.raises(UnauthorizedAccessError):
        storage.append(b"secret")


def test_storage_records_unauthorized_access_attempt(tmp_path: Path, master_key: bytes) -> None:
    access_trace = tmp_path / "access.ndjson"
    storage = ProtectedStorage(
        tmp_path / "protected.ndjson",
        master_key=master_key,
        authorized_principals=frozenset({"other-user"}),
        access_trace_path=access_trace,
    )
    trace_storage = ProtectedStorage(
        access_trace,
        master_key=master_key,
        authorized_principals=frozenset({derive_caller_identity()}),
    )
    with pytest.raises(UnauthorizedAccessError):
        storage.append(b"secret")
    assert "unauthorized_access" not in access_trace.read_text(encoding="utf-8")
    assert any(
        event["event_detail"]["reason"] == "unauthorized_access"
        for event in read_events(access_trace, protected_storage=trace_storage)
    )
