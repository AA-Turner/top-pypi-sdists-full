"""Unit tests for AES-256-GCM protected storage (FR-011, FR-012, SC-017)."""

from __future__ import annotations

import base64
import hashlib
import json
from pathlib import Path

import pytest

from agentic_devtools.orchestration.hierarchy.protected_storage import (
    ProtectedStorage,
    ProtectedStorageError,
    RemoteStorageRejectedError,
    UnauthorizedAccessError,
    derive_caller_identity,
)
from agentic_devtools.orchestration.hierarchy.trace import read_events


@pytest.fixture
def master_key() -> bytes:
    return b"unit-test-master-key-material-32b"


@pytest.fixture
def authorized_principals() -> frozenset[str]:
    return frozenset({derive_caller_identity()})


def test_write_and_read_round_trip(tmp_path: Path, master_key: bytes, authorized_principals: frozenset[str]) -> None:
    storage = ProtectedStorage(
        tmp_path / "snapshots.ndjson", master_key=master_key, authorized_principals=authorized_principals
    )
    storage.append(b"hello world")
    storage.append(b"second frame")
    assert storage.read_all() == [b"hello world", b"second frame"]


def test_constructor_rejects_symlinked_parent_directory(
    tmp_path: Path, master_key: bytes, authorized_principals: frozenset[str]
) -> None:
    real_parent = tmp_path / "real-parent"
    real_parent.mkdir()
    symlink_parent = tmp_path / "symlink-parent"
    symlink_parent.symlink_to(real_parent, target_is_directory=True)
    with pytest.raises(RemoteStorageRejectedError, match="symlinked component"):
        ProtectedStorage(
            symlink_parent / "snapshots.ndjson",
            master_key=master_key,
            authorized_principals=authorized_principals,
        )


def test_constructor_rejects_symlinked_storage_file(
    tmp_path: Path, master_key: bytes, authorized_principals: frozenset[str]
) -> None:
    target = tmp_path / "target.ndjson"
    target.write_text("", encoding="utf-8")
    symlink_file = tmp_path / "snapshots.ndjson"
    symlink_file.symlink_to(target)
    with pytest.raises(RemoteStorageRejectedError, match="symlinked component"):
        ProtectedStorage(
            symlink_file,
            master_key=master_key,
            authorized_principals=authorized_principals,
        )


def test_write_snapshot_returns_matching_sha256_ref(
    tmp_path: Path, master_key: bytes, authorized_principals: frozenset[str]
) -> None:
    storage = ProtectedStorage(
        tmp_path / "snapshots.ndjson", master_key=master_key, authorized_principals=authorized_principals
    )
    snapshot_ref = storage.write_snapshot(b"hello world")
    assert snapshot_ref == "sha256:" + hashlib.sha256(b"hello world").hexdigest()
    assert storage.read_all() == [b"hello world"]


def test_reopening_storage_recovers_persisted_salt(
    tmp_path: Path, master_key: bytes, authorized_principals: frozenset[str]
) -> None:
    path = tmp_path / "snapshots.ndjson"
    storage = ProtectedStorage(path, master_key=master_key, authorized_principals=authorized_principals)
    storage.append(b"persisted")

    reopened = ProtectedStorage(path, master_key=master_key, authorized_principals=authorized_principals)
    assert reopened.read_all() == [b"persisted"]


def test_reopening_storage_ignores_invalid_persisted_salt(
    tmp_path: Path, master_key: bytes, authorized_principals: frozenset[str]
) -> None:
    path = tmp_path / "invalid-salt.ndjson"
    path.write_text(
        '{"version": 1, "salt": "%%%", "nonce": "YQ==", "ciphertext": "YQ==", "tag": "YQ=="}\n'
        '{"version": 1, "salt": "YQ==", "nonce": "YQ==", "ciphertext": "YQ==", "tag": "YQ=="}\n',
        encoding="utf-8",
    )

    storage = ProtectedStorage(path, master_key=master_key, authorized_principals=authorized_principals)
    assert storage._salt != b"a"


def test_caller_supplied_salt_must_be_16_bytes(
    tmp_path: Path, master_key: bytes, authorized_principals: frozenset[str]
) -> None:
    with pytest.raises(ValueError, match="16 bytes"):
        ProtectedStorage(
            tmp_path / "s.ndjson",
            master_key=master_key,
            salt=b"short",
            authorized_principals=authorized_principals,
        )


def test_caller_supplied_salt_must_match_persisted_salt(
    tmp_path: Path, master_key: bytes, authorized_principals: frozenset[str]
) -> None:
    path = tmp_path / "existing.ndjson"
    storage = ProtectedStorage(path, master_key=master_key, authorized_principals=authorized_principals)
    storage.append(b"data")
    persisted = storage._salt  # noqa: SLF001
    assert persisted is not None and len(persisted) == 16
    wrong_salt = bytes(b ^ 0xFF for b in persisted)  # every byte flipped
    with pytest.raises(ValueError, match="does not match"):
        ProtectedStorage(path, master_key=master_key, salt=wrong_salt, authorized_principals=authorized_principals)


def test_append_rechecks_persisted_salt_under_lock_for_caller_supplied_salt(
    tmp_path: Path, master_key: bytes, authorized_principals: frozenset[str]
) -> None:
    path = tmp_path / "race-salt.ndjson"
    salt_a = b"\x01" * 16
    salt_b = b"\x02" * 16
    writer_a = ProtectedStorage(path, master_key=master_key, salt=salt_a, authorized_principals=authorized_principals)
    writer_b = ProtectedStorage(path, master_key=master_key, salt=salt_b, authorized_principals=authorized_principals)

    writer_a.append(b"frame-a")
    with pytest.raises(ValueError, match="does not match"):
        writer_b.append(b"frame-b")


def test_read_last_frame_from_handle_returns_none_for_blank_file(
    tmp_path: Path, master_key: bytes, authorized_principals: frozenset[str]
) -> None:
    path = tmp_path / "blank.ndjson"
    path.write_text("\n", encoding="utf-8")
    storage = ProtectedStorage(path, master_key=master_key, authorized_principals=authorized_principals)
    with path.open("r", encoding="utf-8") as handle:
        assert storage._read_last_frame_from_handle(handle) is None


def test_append_before_append_receives_last_plaintext(
    tmp_path: Path, master_key: bytes, authorized_principals: frozenset[str]
) -> None:
    path = tmp_path / "before-append.ndjson"
    storage = ProtectedStorage(path, master_key=master_key, authorized_principals=authorized_principals)
    storage.append(b"first")
    seen: list[bytes | None] = []

    def _capture(last_plaintext: bytes | None) -> None:
        seen.append(last_plaintext)

    storage.append(b"second", before_append=_capture)
    assert seen == [b"first"]


def test_append_before_append_can_replace_plaintext(
    tmp_path: Path, master_key: bytes, authorized_principals: frozenset[str]
) -> None:
    path = tmp_path / "before-append-rewrite.ndjson"
    storage = ProtectedStorage(path, master_key=master_key, authorized_principals=authorized_principals)
    storage.append(b"first")
    storage.append(b"ignored", before_append=lambda _last: b"rewritten")
    assert storage.read_all() == [b"first", b"rewritten"]


def test_append_before_append_receives_none_when_file_is_empty(
    tmp_path: Path, master_key: bytes, authorized_principals: frozenset[str]
) -> None:
    path = tmp_path / "before-append-empty.ndjson"
    storage = ProtectedStorage(path, master_key=master_key, authorized_principals=authorized_principals)
    seen: list[bytes | None] = []
    storage.append(b"first", before_append=lambda last_plaintext: seen.append(last_plaintext))
    assert seen == [None]


def test_append_before_append_rejects_last_frame_salt_mismatch(
    tmp_path: Path, master_key: bytes, authorized_principals: frozenset[str]
) -> None:
    path = tmp_path / "salt-mismatch.ndjson"
    storage = ProtectedStorage(path, master_key=master_key, authorized_principals=authorized_principals)
    storage.append(b"first")
    storage.append(b"second")
    lines = path.read_text(encoding="utf-8").splitlines()
    frame = json.loads(lines[-1])
    frame["salt"] = "AgICAgICAgICAgICAgICAg=="
    lines[-1] = json.dumps(frame)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    with pytest.raises(ProtectedStorageError, match="does not match"):
        storage.append(b"third", before_append=lambda _last: None)


def test_append_before_append_rejects_malformed_last_frame_salt(
    tmp_path: Path, master_key: bytes, authorized_principals: frozenset[str]
) -> None:
    path = tmp_path / "salt-malformed.ndjson"
    storage = ProtectedStorage(path, master_key=master_key, authorized_principals=authorized_principals)
    storage.append(b"first")
    lines = path.read_text(encoding="utf-8").splitlines()
    frame = json.loads(lines[-1])
    frame["salt"] = "not-base64"
    path.write_text(json.dumps(frame) + "\n", encoding="utf-8")
    with pytest.raises(ProtectedStorageError, match="Malformed protected-storage frame salt"):
        storage.append(b"second", before_append=lambda _last: None)


def test_append_before_append_rejects_tampered_last_frame(
    tmp_path: Path, master_key: bytes, authorized_principals: frozenset[str]
) -> None:
    path = tmp_path / "tampered-last.ndjson"
    storage = ProtectedStorage(path, master_key=master_key, authorized_principals=authorized_principals)
    storage.append(b"first")
    lines = path.read_text(encoding="utf-8").splitlines()
    frame = json.loads(lines[-1])
    frame["ciphertext"] = "AAAAAAAAAAAAAAAA"
    path.write_text(json.dumps(frame) + "\n", encoding="utf-8")
    with pytest.raises(ProtectedStorageError, match="tampered"):
        storage.append(b"second", before_append=lambda _last: None)


def test_corrupt_final_frame_raises_integrity_error(
    tmp_path: Path, master_key: bytes, authorized_principals: frozenset[str]
) -> None:
    path = tmp_path / "snapshots.ndjson"
    storage = ProtectedStorage(path, master_key=master_key, authorized_principals=authorized_principals)
    storage.append(b"good frame")
    with path.open("a", encoding="utf-8") as handle:
        handle.write('{"version": 1, "salt": "not-valid-base64===", "nonce": "x", "ciphertext": "y", "tag": "z"}\n')
    # Reopen a fresh instance so the corrupt trailing frame is exercised on read.
    reopened = ProtectedStorage(
        path,
        master_key=master_key,
        salt=storage._salt,  # noqa: SLF001
        authorized_principals=authorized_principals,
    )
    with pytest.raises(ProtectedStorageError, match="tampered"):
        reopened.read_all()


def test_malformed_final_line_does_not_block_earlier_reads(
    tmp_path: Path, master_key: bytes, authorized_principals: frozenset[str]
) -> None:
    path = tmp_path / "snapshots.ndjson"
    storage = ProtectedStorage(path, master_key=master_key, authorized_principals=authorized_principals)
    storage.append(b"good frame")
    with path.open("a", encoding="utf-8") as handle:
        handle.write("not valid json\n")
    reopened = ProtectedStorage(
        path,
        master_key=master_key,
        salt=storage._salt,  # noqa: SLF001
        authorized_principals=authorized_principals,
    )
    assert reopened.read_all() == [b"good frame"]


def test_append_truncates_invalid_final_frame_before_writing(
    tmp_path: Path, master_key: bytes, authorized_principals: frozenset[str]
) -> None:
    path = tmp_path / "snapshots.ndjson"
    storage = ProtectedStorage(path, master_key=master_key, authorized_principals=authorized_principals)
    storage.append(b"good frame")
    with path.open("a", encoding="utf-8") as handle:
        handle.write("not valid json")
    storage.append(b"next frame")
    reopened = ProtectedStorage(
        path,
        master_key=master_key,
        salt=storage._salt,  # noqa: SLF001
        authorized_principals=authorized_principals,
    )
    assert reopened.read_all() == [b"good frame", b"next frame"]


def test_append_preserves_blank_trailing_lines(
    tmp_path: Path, master_key: bytes, authorized_principals: frozenset[str]
) -> None:
    path = tmp_path / "snapshots.ndjson"
    storage = ProtectedStorage(path, master_key=master_key, authorized_principals=authorized_principals)
    storage.append(b"first frame")
    path.write_text(path.read_text(encoding="utf-8") + "\n", encoding="utf-8")
    storage.append(b"second frame")
    reopened = ProtectedStorage(
        path,
        master_key=master_key,
        salt=storage._salt,  # noqa: SLF001
        authorized_principals=authorized_principals,
    )
    assert reopened.read_all() == [b"first frame", b"second frame"]


def test_file_permissions_are_owner_only(
    tmp_path: Path, master_key: bytes, authorized_principals: frozenset[str]
) -> None:
    storage = ProtectedStorage(
        tmp_path / "snapshots.ndjson", master_key=master_key, authorized_principals=authorized_principals
    )
    storage.append(b"content")
    mode = storage.path.stat().st_mode & 0o777
    assert mode == 0o600


def test_storage_delete_enforces_authorization_and_reports_missing_file(
    tmp_path: Path, master_key: bytes, authorized_principals: frozenset[str]
) -> None:
    storage = ProtectedStorage(
        tmp_path / "protected.ndjson", master_key=master_key, authorized_principals=authorized_principals
    )
    assert storage.delete() is False
    storage.append(b"content")
    assert storage.delete() is True
    assert storage.delete() is False


def test_storage_audit_failure_does_not_bypass_authorization(tmp_path: Path, master_key: bytes, monkeypatch) -> None:
    storage = ProtectedStorage(
        tmp_path / "protected.ndjson",
        master_key=master_key,
        authorized_principals=frozenset({"other-user"}),
        access_trace_path=tmp_path / "trace.ndjson",
    )
    monkeypatch.setattr(
        ProtectedStorage,
        "_append_audit_trace_event",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(OSError("trace unavailable")),
    )
    with pytest.raises(UnauthorizedAccessError):
        storage.read_all()


def test_corrupted_non_final_frame_raises_integrity_error(
    tmp_path: Path, master_key: bytes, authorized_principals: frozenset[str]
) -> None:
    """A tampered middle frame must surface as a ProtectedStorageError, not be silently skipped."""
    path = tmp_path / "protected.ndjson"
    storage = ProtectedStorage(path, master_key=master_key, authorized_principals=authorized_principals)
    storage.append(b"good frame")
    storage.append(b"second good frame")
    # Corrupt the FIRST (non-final) frame by overwriting its ciphertext with garbage.
    lines = path.read_text(encoding="utf-8").splitlines()
    first = json.loads(lines[0])
    first["ciphertext"] = "AAAAAAAAAAAAAAAA"  # wrong ciphertext, AES-GCM auth will fail
    lines[0] = json.dumps(first)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    reopened = ProtectedStorage(
        path,
        master_key=master_key,
        salt=storage._salt,  # noqa: SLF001
        authorized_principals=authorized_principals,
    )
    with pytest.raises(ProtectedStorageError, match="tampered"):
        reopened.read_all()


def test_malformed_middle_frame_raises_integrity_error(
    tmp_path: Path, master_key: bytes, authorized_principals: frozenset[str]
) -> None:
    path = tmp_path / "protected.ndjson"
    storage = ProtectedStorage(path, master_key=master_key, authorized_principals=authorized_principals)
    storage.append(b"first")
    storage.append(b"last")
    lines = path.read_text(encoding="utf-8").splitlines()
    lines.insert(1, "not valid json")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    reopened = ProtectedStorage(
        path,
        master_key=master_key,
        salt=storage._salt,  # noqa: SLF001
        authorized_principals=authorized_principals,
    )
    with pytest.raises(ProtectedStorageError, match="Malformed protected-storage frame"):
        reopened.read_all()


def test_corrupt_frame_before_malformed_final_frame_raises(
    tmp_path: Path, master_key: bytes, authorized_principals: frozenset[str]
) -> None:
    path = tmp_path / "protected.ndjson"
    storage = ProtectedStorage(path, master_key=master_key, authorized_principals=authorized_principals)
    storage.append(b"corrupt")
    lines = path.read_text(encoding="utf-8").splitlines()
    frame = json.loads(lines[0])
    frame["ciphertext"] = "AAAAAAAAAAAAAAAA"
    path.write_text(json.dumps(frame) + "\nnot valid json\n", encoding="utf-8")
    reopened = ProtectedStorage(
        path,
        master_key=master_key,
        salt=storage._salt,  # noqa: SLF001
        authorized_principals=authorized_principals,
    )
    with pytest.raises(ProtectedStorageError, match="tampered"):
        reopened.read_all()


def test_deferred_salt_selected_under_lock_on_first_append(
    tmp_path: Path, master_key: bytes, authorized_principals: frozenset[str]
) -> None:
    """When no salt is found at construction, it is selected and persisted on the first append."""
    path = tmp_path / "deferred.ndjson"
    # Do NOT supply a salt — this exercises the deferred path.
    storage = ProtectedStorage(path, master_key=master_key, authorized_principals=authorized_principals)
    assert storage._salt is None  # noqa: SLF001 — not yet assigned
    storage.append(b"first write")
    assert storage._salt is not None  # noqa: SLF001 — assigned during append
    # A second instance honours the already-persisted salt rather than generating a new one.
    storage2 = ProtectedStorage(path, master_key=master_key, authorized_principals=authorized_principals)
    assert storage2._salt == storage._salt


def test_deferred_salt_adopts_existing_salt_from_concurrent_writer(
    tmp_path: Path, master_key: bytes, authorized_principals: frozenset[str]
) -> None:
    """When another instance writes first, the deferred instance adopts the persisted salt."""
    path = tmp_path / "concurrent.ndjson"
    # Instance A is created before the file exists — salt is deferred.
    instance_a = ProtectedStorage(path, master_key=master_key, authorized_principals=authorized_principals)
    assert instance_a._salt is None  # noqa: SLF001

    # Instance B creates the file and writes a frame first.
    instance_b = ProtectedStorage(path, master_key=master_key, authorized_principals=authorized_principals)
    instance_b.append(b"from B")

    # Instance A now appends; it must adopt B's persisted salt, not generate a new one.
    instance_a.append(b"from A")
    assert instance_a._salt == instance_b._salt  # noqa: SLF001

    # Both records must be readable by either instance.
    records = instance_b.read_all()
    assert records == [b"from B", b"from A"]


def test_append_rejects_parseable_invalid_final_frame(
    tmp_path: Path, master_key: bytes, authorized_principals: frozenset[str]
) -> None:
    path = tmp_path / "invalid-final-frame.ndjson"
    storage = ProtectedStorage(path, master_key=master_key, authorized_principals=authorized_principals)
    storage.append(b"good frame")
    with path.open("a", encoding="utf-8") as handle:
        handle.write("{}\n")
    with pytest.raises(ProtectedStorageError, match="Malformed protected-storage final frame"):
        storage.append(b"next frame")


def test_read_salt_from_handle_skips_blank_and_invalid_lines(tmp_path: Path, master_key: bytes) -> None:
    """_read_salt_from_handle tolerates blank lines and malformed JSON when looking for the salt."""
    path = tmp_path / "blanks.ndjson"
    # Write a blank line, then an invalid-JSON line, then a frame without a salt field,
    # then a valid frame.  Only the valid frame should be returned.
    valid_salt = b"\xab" * 16
    path.write_text(
        "\n"  # blank line → triggers the `if not stripped: continue` branch
        + "not json\n"  # malformed → triggers `except Exception: continue`
        + json.dumps({"salt": base64.b64encode(valid_salt).decode()})
        + "\n",
        encoding="utf-8",
    )
    with path.open("r", encoding="utf-8") as fh:
        result = ProtectedStorage._read_salt_from_handle(fh)  # noqa: SLF001
    assert result == valid_salt


def test_read_salt_from_handle_skips_wrong_length_salt(tmp_path: Path, master_key: bytes) -> None:
    """_read_salt_from_handle must skip frames whose decoded salt is not 16 bytes."""
    valid_salt = b"\xcd" * 16
    # First frame has a salt that is valid base64 but only 8 bytes (wrong length).
    wrong_length_salt = base64.b64encode(b"\xab" * 8).decode()
    correct_salt = base64.b64encode(valid_salt).decode()
    path = tmp_path / "wrong_len.ndjson"
    path.write_text(
        json.dumps({"salt": wrong_length_salt}) + "\n" + json.dumps({"salt": correct_salt}) + "\n",
        encoding="utf-8",
    )
    with path.open("r", encoding="utf-8") as fh:
        result = ProtectedStorage._read_salt_from_handle(fh)  # noqa: SLF001
    assert result == valid_salt


def test_version_salt_tampering_detected_via_aad(
    tmp_path: Path, master_key: bytes, authorized_principals: frozenset[str]
) -> None:
    """Modifying a frame's version or salt header field must cause AES-GCM authentication to fail."""
    path = tmp_path / "aad-test.ndjson"
    storage = ProtectedStorage(path, master_key=master_key, authorized_principals=authorized_principals)
    storage.append(b"sensitive payload")

    lines = path.read_text(encoding="utf-8").splitlines()
    frame = json.loads(lines[0])

    # Tamper with the salt field in the header (keep everything else intact).
    original_salt_bytes = base64.b64decode(frame["salt"])
    tampered_salt = bytes(b ^ 0x01 for b in original_salt_bytes)
    frame["salt"] = base64.b64encode(tampered_salt).decode("ascii")
    path.write_text(json.dumps(frame) + "\n", encoding="utf-8")

    # Pass the tampered salt so construction succeeds; read_all must fail because the
    # AAD (version+salt) bound during encryption no longer matches the tampered header.
    reopened = ProtectedStorage(
        path,
        master_key=master_key,
        salt=tampered_salt,
        authorized_principals=authorized_principals,
    )
    with pytest.raises(ProtectedStorageError, match="tampered"):
        reopened.read_all()


def test_append_audit_trace_event_advances_out_of_order_timestamp(
    tmp_path: Path, master_key: bytes, authorized_principals: frozenset[str]
) -> None:
    from unittest.mock import patch

    from agentic_devtools.orchestration.hierarchy.trace import TraceEvent, TraceEventType

    path = tmp_path / "audit.ndjson"
    storage = ProtectedStorage(path, master_key=master_key, authorized_principals=authorized_principals)
    storage._append_audit_trace_event(  # noqa: SLF001 - exercises recursion-safe internal audit path
        TraceEvent(
            event_type=TraceEventType.SCOPE_VIOLATION,
            agent_scope="orchestrator",
            event_detail={"agent_id": "protected-storage", "attempted_path": "/tmp/first", "enforcement": "blocked"},
            timestamp="2024-06-01T12:00:00+00:00",
        )
    )
    with patch(
        "agentic_devtools.orchestration.hierarchy.trace.utc_timestamp",
        return_value="2024-06-01T11:00:00.000Z",
    ):
        second_event = TraceEvent(
            event_type=TraceEventType.SCOPE_VIOLATION,
            agent_scope="orchestrator",
            event_detail={"agent_id": "protected-storage", "attempted_path": "/tmp/second", "enforcement": "blocked"},
        )
    storage._append_audit_trace_event(second_event)  # noqa: SLF001 - exercises timestamp advancement branch

    events = read_events(path, protected_storage=storage)
    assert [event["event_detail"]["attempted_path"] for event in events] == ["/tmp/first", "/tmp/second"]
    assert events[1]["timestamp"] > events[0]["timestamp"]


def test_append_audit_trace_event_preserves_in_order_timestamp(
    tmp_path: Path, master_key: bytes, authorized_principals: frozenset[str]
) -> None:
    from agentic_devtools.orchestration.hierarchy.trace import TraceEvent, TraceEventType

    path = tmp_path / "audit-in-order.ndjson"
    storage = ProtectedStorage(path, master_key=master_key, authorized_principals=authorized_principals)
    storage._append_audit_trace_event(  # noqa: SLF001 - internal audit helper coverage
        TraceEvent(
            event_type=TraceEventType.SCOPE_VIOLATION,
            agent_scope="orchestrator",
            event_detail={"agent_id": "protected-storage", "attempted_path": "/tmp/first", "enforcement": "blocked"},
            timestamp="2024-06-01T12:00:00+00:00",
        )
    )
    storage._append_audit_trace_event(  # noqa: SLF001 - covers no-rewrite branch with prior plaintext present
        TraceEvent(
            event_type=TraceEventType.SCOPE_VIOLATION,
            agent_scope="orchestrator",
            event_detail={"agent_id": "protected-storage", "attempted_path": "/tmp/second", "enforcement": "blocked"},
            timestamp="2024-06-01T12:00:01+00:00",
        )
    )

    events = read_events(path, protected_storage=storage)
    assert [event["timestamp"] for event in events] == ["2024-06-01T12:00:00+00:00", "2024-06-01T12:00:01+00:00"]


def test_read_all_returns_empty_list_for_nonexistent_file(
    tmp_path: Path, master_key: bytes, authorized_principals: frozenset[str]
) -> None:
    storage = ProtectedStorage(
        tmp_path / "snapshots.ndjson", master_key=master_key, authorized_principals=authorized_principals
    )
    assert storage.read_all() == []


def test_read_all_with_deferred_salt(tmp_path: Path, master_key: bytes, authorized_principals: frozenset[str]) -> None:
    """read_all derives the key from the persisted salt when none was loaded eagerly."""
    path = tmp_path / "deferred_read.ndjson"
    writer = ProtectedStorage(path, master_key=master_key, authorized_principals=authorized_principals)
    writer.append(b"payload")
    # Open a new instance without supplying a salt to trigger the deferred read_all path.
    reader = ProtectedStorage(path, master_key=master_key, authorized_principals=authorized_principals)
    # Force the salt to None to simulate the deferred state (salt was not in file at __init__ time).
    object.__setattr__(reader, "_salt", None)  # type: ignore[arg-type]
    object.__setattr__(reader, "_key", None)  # type: ignore[arg-type]
    result = reader.read_all()
    assert result == [b"payload"]


def test_read_all_deferred_salt_returns_empty_when_no_file(
    tmp_path: Path, master_key: bytes, authorized_principals: frozenset[str]
) -> None:
    """read_all returns [] when the file is absent, even with a deferred salt."""
    path = tmp_path / "missing.ndjson"
    storage = ProtectedStorage(path, master_key=master_key, authorized_principals=authorized_principals)
    assert storage.read_all() == []


def test_read_all_deferred_salt_file_has_parseable_invalid_final_frame_raises(
    tmp_path: Path, master_key: bytes, authorized_principals: frozenset[str]
) -> None:
    """A parseable but invalid final frame must fail closed as potential tampering."""
    path = tmp_path / "nosalt.ndjson"
    path.write_text('{"version":1,"nonce":"AA==","ciphertext":"AA==","tag":"AA=="}\n', encoding="utf-8")
    storage = ProtectedStorage(path, master_key=master_key, authorized_principals=authorized_principals)
    # Force deferred state: null out the eagerly-loaded salt/key.
    object.__setattr__(storage, "_salt", None)  # type: ignore[arg-type]
    object.__setattr__(storage, "_key", None)  # type: ignore[arg-type]
    with pytest.raises(ProtectedStorageError, match="Malformed protected-storage frame"):
        storage.read_all()


def test_read_all_deferred_salt_raises_when_frames_exist_without_valid_salt(
    tmp_path: Path, master_key: bytes, authorized_principals: frozenset[str]
) -> None:
    path = tmp_path / "invalid-salt.ndjson"
    path.write_text(
        '{"version":1,"salt":"AA==","nonce":"AA==","ciphertext":"AA==","tag":"AA=="}\n',
        encoding="utf-8",
    )
    storage = ProtectedStorage(path, master_key=master_key, authorized_principals=authorized_principals)
    object.__setattr__(storage, "_salt", None)  # type: ignore[arg-type]
    object.__setattr__(storage, "_key", None)  # type: ignore[arg-type]
    with pytest.raises(ProtectedStorageError, match="no valid persisted salt"):
        storage.read_all()


def test_read_all_deferred_salt_returns_empty_for_only_malformed_final_line(
    tmp_path: Path, master_key: bytes, authorized_principals: frozenset[str]
) -> None:
    path = tmp_path / "malformed-only.ndjson"
    path.write_text("not valid json\n", encoding="utf-8")
    storage = ProtectedStorage(path, master_key=master_key, authorized_principals=authorized_principals)
    object.__setattr__(storage, "_salt", None)  # type: ignore[arg-type]
    object.__setattr__(storage, "_key", None)  # type: ignore[arg-type]
    assert storage.read_all() == []
