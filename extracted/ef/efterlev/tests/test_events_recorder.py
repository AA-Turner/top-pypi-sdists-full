"""Tests for the JSONL event recorder — the `studio --live` transport.

`record_events_to` binds a process-global bus that writes each emitted event
as one JSON line. These pin that contract; the cleanup resets the global bus
so the permanence (intended for a one-shot subprocess) doesn't leak into
other tests.
"""

from __future__ import annotations

import json
from collections.abc import Iterator
from pathlib import Path

import pytest


@pytest.fixture
def _reset_bus() -> Iterator[None]:
    yield
    # record_events_to sets the process-global bus with no reset (subprocess
    # semantics); undo that here so emit() is a no-op again for other tests.
    import efterlev.events.recorder as recorder
    from efterlev.events import bus

    bus._active_bus.set(None)
    if recorder._sink_file is not None:
        recorder._sink_file.close()
        recorder._sink_file = None


def test_record_events_to_writes_one_json_line_per_event(tmp_path: Path, _reset_bus: None) -> None:
    from efterlev.events import EvidenceFound, KsiClassified, emit
    from efterlev.events.recorder import record_events_to

    log = tmp_path / "events.jsonl"
    record_events_to(log)

    emit(EvidenceFound(detector_id="d", ksis=["KSI-SVC-SNT"], source_file="main.tf", line_start=14))
    emit(KsiClassified(ksi="KSI-SVC-SNT", status="implemented", rationale="TLS enforced"))

    lines = log.read_text(encoding="utf-8").strip().splitlines()
    assert len(lines) == 2
    first = json.loads(lines[0])
    assert first["kind"] == "evidence_found" and first["ksis"] == ["KSI-SVC-SNT"]
    second = json.loads(lines[1])
    assert second["kind"] == "ksi_classified" and second["status"] == "implemented"


def test_record_events_to_creates_parent_dir(tmp_path: Path, _reset_bus: None) -> None:
    from efterlev.events.recorder import record_events_to

    log = tmp_path / "nested" / "deeper" / "events.jsonl"
    record_events_to(log)
    assert log.exists()
