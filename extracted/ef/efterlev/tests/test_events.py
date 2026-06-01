"""Tests for the Studio event spine (schema + bus + scan emission).

The spine is the foundation of Efterlev Studio (DECISIONS 2026-05-22): a
typed event stream that producers emit to and renderers subscribe from.
These pin the contract — frozen/discriminated events, a pub/sub bus, the
no-op-without-an-active-bus property (so the normal CLI path is unchanged),
and that `efterlev scan` actually emits the expected events when a bus is
bound.
"""

from __future__ import annotations

from pathlib import Path

import pytest
from pydantic import ValidationError
from typer.testing import CliRunner

from efterlev.events import (
    EventBus,
    EvidenceFound,
    KsiEvidenced,
    ScanFinished,
    ScanStarted,
    active_event_bus,
    emit,
    get_active_bus,
)

runner = CliRunner()


# --- schema ------------------------------------------------------------


def test_events_are_frozen() -> None:
    ev = ScanStarted(mode="hcl", target="/repo")
    with pytest.raises(ValidationError):
        ev.mode = "plan"  # type: ignore[misc]


def test_event_kind_discriminators() -> None:
    assert ScanStarted(mode="hcl", target="/x").kind == "scan_started"
    assert EvidenceFound(detector_id="d", source_file="a.tf").kind == "evidence_found"
    assert KsiEvidenced(ksi="KSI-X", evidence_count=1).kind == "ksi_evidenced"
    assert ScanFinished(evidence_total=0).kind == "scan_finished"


def test_evidence_found_defaults() -> None:
    ev = EvidenceFound(detector_id="aws.x", source_file="main.tf")
    assert ev.ksis == []
    assert ev.line_start is None
    assert ev.boundary_state == "boundary_undeclared"


# --- bus ---------------------------------------------------------------


def test_bus_delivers_in_order() -> None:
    bus = EventBus()
    seen: list[str] = []
    bus.subscribe(lambda e: seen.append(e.kind))
    bus.publish(ScanStarted(mode="hcl", target="/x"))
    bus.publish(ScanFinished(evidence_total=3))
    assert seen == ["scan_started", "scan_finished"]


def test_bus_unsubscribe_stops_delivery() -> None:
    bus = EventBus()
    seen: list[str] = []
    unsub = bus.subscribe(lambda e: seen.append(e.kind))
    bus.publish(ScanStarted(mode="hcl", target="/x"))
    unsub()
    bus.publish(ScanFinished(evidence_total=0))
    assert seen == ["scan_started"]


def test_multiple_subscribers_all_receive() -> None:
    bus = EventBus()
    a: list[str] = []
    b: list[str] = []
    bus.subscribe(lambda e: a.append(e.kind))
    bus.subscribe(lambda e: b.append(e.kind))
    bus.publish(ScanFinished(evidence_total=1))
    assert a == b == ["scan_finished"]


# --- emit() + active bus ----------------------------------------------


def test_emit_is_noop_without_active_bus() -> None:
    # No active bus bound → emit must not raise and must reach nobody.
    assert get_active_bus() is None
    emit(ScanStarted(mode="hcl", target="/x"))  # must not raise


def test_active_event_bus_binds_emit() -> None:
    bus = EventBus()
    seen: list[str] = []
    bus.subscribe(lambda e: seen.append(e.kind))
    with active_event_bus(bus) as bound:
        assert bound is bus
        assert get_active_bus() is bus
        emit(ScanStarted(mode="hcl", target="/x"))
    # context exited → unbound again
    assert get_active_bus() is None
    assert seen == ["scan_started"]


# --- scan emits events (integration) ----------------------------------


def _init_workspace_with_tf(tmp_path: Path) -> Path:
    from efterlev.workspace import init_workspace

    init_workspace(tmp_path, "fedramp-20x-moderate")
    (tmp_path / "main.tf").write_text(
        'resource "aws_s3_bucket" "audit" {\n'
        '  bucket = "audit-logs"\n'
        "  server_side_encryption_configuration {\n"
        "    rule {\n"
        "      apply_server_side_encryption_by_default {\n"
        '        sse_algorithm = "AES256"\n'
        "      }\n"
        "    }\n"
        "  }\n"
        "}\n"
    )
    return tmp_path


def test_scan_emits_event_stream(tmp_path: Path) -> None:
    from efterlev.cli.main import app

    _init_workspace_with_tf(tmp_path)
    bus = EventBus()
    events: list[object] = []
    bus.subscribe(events.append)

    with active_event_bus(bus):
        result = runner.invoke(app, ["scan", "--target", str(tmp_path)])
    assert result.exit_code == 0, result.output

    kinds = [e.kind for e in events]  # type: ignore[attr-defined]
    assert kinds[0] == "scan_started"
    assert kinds[-1] == "scan_finished"
    assert "evidence_found" in kinds
    assert "ksi_evidenced" in kinds

    started = next(e for e in events if e.kind == "scan_started")  # type: ignore[attr-defined]
    assert started.mode == "hcl"  # type: ignore[attr-defined]

    finished = next(e for e in events if e.kind == "scan_finished")  # type: ignore[attr-defined]
    assert finished.evidence_total > 0  # type: ignore[attr-defined]
    assert finished.ksis_with_evidence > 0  # type: ignore[attr-defined]
    # the encrypted-bucket fixture lights at least the S3 encryption KSI
    ksi_events = [e for e in events if e.kind == "ksi_evidenced"]  # type: ignore[attr-defined]
    assert len(ksi_events) == finished.ksis_with_evidence  # type: ignore[attr-defined]


def test_scan_without_bus_is_unchanged(tmp_path: Path) -> None:
    """No active bus → scan still succeeds and emits nothing (CLI parity)."""
    from efterlev.cli.main import app

    _init_workspace_with_tf(tmp_path)
    assert get_active_bus() is None
    result = runner.invoke(app, ["scan", "--target", str(tmp_path)])
    assert result.exit_code == 0, result.output
    assert "Scanned" in result.output
