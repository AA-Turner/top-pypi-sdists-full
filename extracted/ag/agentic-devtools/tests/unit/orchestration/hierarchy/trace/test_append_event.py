"""Unit tests for append-only NDJSON trace persistence."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, cast
from unittest.mock import patch

import pytest

from agentic_devtools.orchestration.hierarchy.protected_storage import ProtectedStorage
from agentic_devtools.orchestration.hierarchy.trace import (
    TraceEvent,
    TraceEventType,
    append_event,
    read_events,
)


def _authorized_principals() -> frozenset[str]:
    from agentic_devtools.orchestration.hierarchy.protected_storage import derive_caller_identity

    return frozenset({derive_caller_identity()})


def _event(reason: str = "epic_not_found") -> TraceEvent:
    return TraceEvent(
        event_type=TraceEventType.DEGRADATION,
        agent_scope="orchestrator",
        event_detail={"reason": reason, "missing_level": "epic", "resulting_topology": ["feature", "subtask"]},
    )


def test_append_and_read_round_trip(tmp_path: Path) -> None:
    trace_path = tmp_path / "trace.ndjson"
    append_event(trace_path, _event("a"))
    append_event(trace_path, _event("b"))
    events = read_events(trace_path)
    assert [e["event_detail"]["reason"] for e in events] == ["a", "b"]


def test_append_creates_parent_directories(tmp_path: Path) -> None:
    trace_path = tmp_path / "nested" / "dir" / "trace.ndjson"
    append_event(trace_path, _event())
    assert trace_path.exists()


def test_append_event_truncates_malformed_trailing_line_before_writing(tmp_path: Path) -> None:
    trace_path = tmp_path / "trace.ndjson"
    append_event(trace_path, _event("good"))
    with trace_path.open("a", encoding="utf-8") as handle:
        handle.write("not valid json\n")
    append_event(trace_path, _event("after-recovery"))
    events = read_events(trace_path)
    assert [e["event_detail"]["reason"] for e in events] == ["good", "after-recovery"]


def test_append_event_truncates_malformed_trailing_line_after_non_ascii_content(tmp_path: Path) -> None:
    trace_path = tmp_path / "trace.ndjson"
    append_event(trace_path, _event("ümlaut"))
    with trace_path.open("a", encoding="utf-8") as handle:
        handle.write("not valid json\n")
    append_event(trace_path, _event("after-recovery"))
    events = read_events(trace_path)
    assert [e["event_detail"]["reason"] for e in events] == ["ümlaut", "after-recovery"]


def test_append_and_read_can_use_authorized_encrypted_storage(tmp_path: Path) -> None:
    storage = ProtectedStorage(
        tmp_path / "trace.ndjson",
        master_key=b"trace-master-key-material-32bytes",
        authorized_principals=_authorized_principals(),
    )
    append_event(storage.path, _event("encrypted"), protected_storage=storage)
    assert read_events(storage.path, protected_storage=storage)[0]["event_detail"]["reason"] == "encrypted"


def test_read_encrypted_storage_raises_on_non_json_frames(tmp_path: Path) -> None:
    storage = ProtectedStorage(
        tmp_path / "trace.ndjson",
        master_key=b"trace-master-key-material-32bytes",
        authorized_principals=_authorized_principals(),
    )
    storage.append(b"not-json")
    with pytest.raises((json.JSONDecodeError, UnicodeDecodeError)):
        read_events(storage.path, protected_storage=storage)


def test_append_event_encrypted_path_accepts_in_order_timestamps(tmp_path: Path) -> None:
    storage = ProtectedStorage(
        tmp_path / "trace.ndjson",
        master_key=b"trace-master-key-material-32bytes",
        authorized_principals=_authorized_principals(),
    )
    first = TraceEvent(
        event_type=TraceEventType.DEGRADATION,
        agent_scope="orchestrator",
        event_detail={"reason": "first", "missing_level": "epic", "resulting_topology": ["subtask"]},
        timestamp="2024-06-01T12:00:00+00:00",
    )
    second = TraceEvent(
        event_type=TraceEventType.DEGRADATION,
        agent_scope="orchestrator",
        event_detail={"reason": "second", "missing_level": "epic", "resulting_topology": ["subtask"]},
        timestamp="2024-06-01T13:00:00+00:00",
    )
    append_event(storage.path, first, protected_storage=storage)
    append_event(storage.path, second, protected_storage=storage)
    events = read_events(storage.path, protected_storage=storage)
    assert [e["event_detail"]["reason"] for e in events] == ["first", "second"]


def test_append_event_encrypted_path_skips_order_check_when_no_last_timestamp(tmp_path: Path) -> None:
    """When the last existing frame has no parseable timestamp, append succeeds without raising."""
    storage = ProtectedStorage(
        tmp_path / "trace.ndjson",
        master_key=b"trace-master-key-material-32bytes",
        authorized_principals=_authorized_principals(),
    )
    # Store a raw frame with no timestamp field; this covers the `last_ts is None` branch.
    storage.append(b'{"other":"x"}\n')
    event = TraceEvent(
        event_type=TraceEventType.DEGRADATION,
        agent_scope="orchestrator",
        event_detail={"reason": "after-notimestamp", "missing_level": "epic", "resulting_topology": ["subtask"]},
        timestamp="2024-06-01T12:00:00+00:00",
    )
    append_event(storage.path, event, protected_storage=storage)
    # Two frames total: the raw one and the serialized event.
    assert len(storage.read_all()) == 2


def test_append_event_rejects_out_of_order_timestamp_encrypted_path(tmp_path: Path) -> None:
    from agentic_devtools.orchestration.hierarchy.trace import TraceValidationError

    storage = ProtectedStorage(
        tmp_path / "trace.ndjson",
        master_key=b"trace-master-key-material-32bytes",
        authorized_principals=_authorized_principals(),
    )
    first = TraceEvent(
        event_type=TraceEventType.DEGRADATION,
        agent_scope="orchestrator",
        event_detail={"reason": "first", "missing_level": "epic", "resulting_topology": ["subtask"]},
        timestamp="2024-06-01T12:00:00+00:00",
    )
    append_event(storage.path, first, protected_storage=storage)
    older = TraceEvent(
        event_type=TraceEventType.DEGRADATION,
        agent_scope="orchestrator",
        event_detail={"reason": "older", "missing_level": "epic", "resulting_topology": ["subtask"]},
        timestamp="2024-06-01T11:00:00+00:00",
    )
    with pytest.raises(TraceValidationError, match="out-of-order"):
        append_event(storage.path, older, protected_storage=storage)
    # Original content must be intact.
    events = read_events(storage.path, protected_storage=storage)
    assert len(events) == 1


def test_append_event_encrypted_path_advances_auto_assigned_out_of_order_timestamp(tmp_path: Path) -> None:
    storage = ProtectedStorage(
        tmp_path / "trace.ndjson",
        master_key=b"trace-master-key-material-32bytes",
        authorized_principals=_authorized_principals(),
    )
    with patch(
        "agentic_devtools.orchestration.hierarchy.trace.utc_timestamp",
        side_effect=["2024-06-01T12:00:00.000Z", "2024-06-01T12:00:01.000Z"],
    ):
        older = _event("older-auto")
        newer = _event("newer-auto")
    append_event(storage.path, newer, protected_storage=storage)
    append_event(storage.path, older, protected_storage=storage)
    events = read_events(storage.path, protected_storage=storage)
    assert [e["event_detail"]["reason"] for e in events] == ["newer-auto", "older-auto"]
    assert events[1]["timestamp"] > events[0]["timestamp"]


def test_append_event_encrypted_path_uses_append_transaction_for_order_check() -> None:
    from agentic_devtools.orchestration.hierarchy.trace import TraceValidationError

    class _NoReadAllStorage:
        def __init__(self, last_plaintext: bytes | None = None) -> None:
            self.last_plaintext = last_plaintext
            self.appended: list[bytes] = []

        def read_all(self) -> list[bytes]:
            raise AssertionError("append_event must not call read_all for protected storage ordering checks")

        def append(self, plaintext: bytes, *, nonce: bytes | None = None, before_append=None) -> None:
            _ = nonce
            if before_append is not None:
                before_append(self.last_plaintext)
            self.appended.append(plaintext)
            self.last_plaintext = plaintext

    latest = (
        json.dumps(
            {
                "event_type": "degradation",
                "agent_scope": "orchestrator",
                "timestamp": "2024-06-01T12:00:00+00:00",
                "event_detail": {"reason": "latest", "missing_level": "epic", "resulting_topology": ["subtask"]},
            }
        )
        + "\n"
    ).encode("utf-8")
    storage = _NoReadAllStorage(last_plaintext=latest)
    older = TraceEvent(
        event_type=TraceEventType.DEGRADATION,
        agent_scope="orchestrator",
        event_detail={"reason": "older", "missing_level": "epic", "resulting_topology": ["subtask"]},
        timestamp="2024-06-01T11:00:00+00:00",
    )
    with pytest.raises(TraceValidationError, match="out-of-order"):
        append_event(
            Path("/tmp/ignored.ndjson"),
            older,
            protected_storage=cast(Any, storage),  # noqa: S108 - test-only path
        )
    assert storage.appended == []


def test_append_event_rejects_out_of_order_timestamp(tmp_path: Path) -> None:
    from agentic_devtools.orchestration.hierarchy.trace import TraceValidationError

    trace_path = tmp_path / "trace.ndjson"
    first = TraceEvent(
        event_type=TraceEventType.DEGRADATION,
        agent_scope="orchestrator",
        event_detail={"reason": "first", "missing_level": "epic", "resulting_topology": ["subtask"]},
        timestamp="2024-06-01T12:00:00+00:00",
    )
    append_event(trace_path, first)
    older = TraceEvent(
        event_type=TraceEventType.DEGRADATION,
        agent_scope="orchestrator",
        event_detail={"reason": "older", "missing_level": "epic", "resulting_topology": ["subtask"]},
        timestamp="2024-06-01T11:00:00+00:00",
    )
    with pytest.raises(TraceValidationError, match="out-of-order"):
        append_event(trace_path, older)
    # Original content must be intact.
    events = read_events(trace_path)
    assert len(events) == 1


def test_append_event_advances_auto_assigned_out_of_order_timestamp(tmp_path: Path) -> None:
    trace_path = tmp_path / "trace.ndjson"
    with patch(
        "agentic_devtools.orchestration.hierarchy.trace.utc_timestamp",
        side_effect=["2024-06-01T12:00:00.000Z", "2024-06-01T12:00:01.000Z"],
    ):
        older = _event("older-auto")
        newer = _event("newer-auto")
    append_event(trace_path, newer)
    append_event(trace_path, older)
    events = read_events(trace_path)
    assert [e["event_detail"]["reason"] for e in events] == ["newer-auto", "older-auto"]
    assert events[1]["timestamp"] > events[0]["timestamp"]


def test_append_event_advances_auto_timestamp_to_minimum_next_when_last_is_in_future(tmp_path: Path) -> None:
    trace_path = tmp_path / "trace.ndjson"
    future = TraceEvent(
        event_type=TraceEventType.DEGRADATION,
        agent_scope="orchestrator",
        event_detail={"reason": "future", "missing_level": "epic", "resulting_topology": ["subtask"]},
        timestamp="3024-06-01T12:00:01.000Z",
    )
    with patch("agentic_devtools.orchestration.hierarchy.trace.utc_timestamp", return_value="3024-06-01T12:00:00.000Z"):
        older_auto = _event("older-auto")
    append_event(trace_path, future)
    append_event(trace_path, older_auto)
    events = read_events(trace_path)
    assert events[0]["timestamp"] == "3024-06-01T12:00:01.000Z"
    assert events[1]["timestamp"] > events[0]["timestamp"]


def test_append_event_handles_blank_only_content_before_first_record(tmp_path: Path) -> None:
    trace_path = tmp_path / "trace.ndjson"
    trace_path.parent.mkdir(parents=True, exist_ok=True)
    trace_path.write_text("\n \n\t\n", encoding="utf-8")
    append_event(trace_path, _event("first"))
    events = read_events(trace_path)
    assert [e["event_detail"]["reason"] for e in events] == ["first"]
