"""Tests for cleanup_workflow_retention."""

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

from agentic_devtools.orchestration.hierarchy.aggregation import (
    append_retention_record,
    cleanup_workflow_retention,
)

_MASTER_KEY = b"x" * 32
_PRINCIPALS = frozenset({"test-principal"})


def test_cleanup_workflow_retention_removes_all_traces(tmp_path: Path) -> None:
    """Workflow deletion removes every retained trace and registry entry."""
    registry = tmp_path / "retention.ndjson"
    trace = tmp_path / "run-1" / "trace.ndjson"
    trace.parent.mkdir(parents=True, exist_ok=True)
    trace.write_text("encrypted", encoding="utf-8")
    append_retention_record(
        registry,
        run_id="run-1",
        trace_path=str(trace),
        expires_at="2099-01-01T00:00:00+00:00",
    )

    mock_storage = MagicMock()

    def _delete() -> bool:
        trace.unlink()
        return True

    mock_storage.delete.side_effect = _delete
    with patch("agentic_devtools.orchestration.hierarchy.aggregation.ProtectedStorage", return_value=mock_storage):
        assert cleanup_workflow_retention(registry, master_key=_MASTER_KEY, authorized_principals=_PRINCIPALS) == (
            "run-1",
        )
    mock_storage.delete.assert_called_once()
    assert not trace.exists()
    assert not registry.exists()


def test_cleanup_workflow_retention_handles_missing_registry(tmp_path: Path) -> None:
    """Workflow cleanup is a no-op when no retention registry exists."""
    assert cleanup_workflow_retention(tmp_path / "missing.ndjson") == ()


def test_cleanup_workflow_retention_handles_invalid_records(tmp_path: Path) -> None:
    """Workflow cleanup removes the registry while ignoring invalid record fields."""
    registry = tmp_path / "retention.ndjson"
    registry.write_text(
        "\n".join(
            [
                json.dumps({"run_id": 1, "trace_path": None, "timestamp": "2026-01-01T00:00:00+00:00"}),
                json.dumps({"run_id": "run-2", "trace_path": str(tmp_path / "missing"), "timestamp": "bad"}),
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    assert cleanup_workflow_retention(registry, master_key=_MASTER_KEY, authorized_principals=_PRINCIPALS) == ()
    assert not registry.exists()


def test_cleanup_workflow_retention_preserves_records_on_trace_delete_errors(tmp_path: Path) -> None:
    """Workflow cleanup keeps records whose retained trace cannot be deleted."""
    registry = tmp_path / "retention.ndjson"
    trace = tmp_path / "run-1" / "trace.ndjson"
    trace.parent.mkdir(parents=True, exist_ok=True)
    trace.write_text("encrypted", encoding="utf-8")
    append_retention_record(
        registry,
        run_id="run-1",
        trace_path=str(trace),
        expires_at="2099-01-01T00:00:00+00:00",
    )

    mock_storage = MagicMock()
    mock_storage.delete.side_effect = OSError("permission denied")
    with patch("agentic_devtools.orchestration.hierarchy.aggregation.ProtectedStorage", return_value=mock_storage):
        assert cleanup_workflow_retention(registry, master_key=_MASTER_KEY, authorized_principals=_PRINCIPALS) == ()
    records = [json.loads(line) for line in registry.read_text().splitlines() if line.strip()]
    assert len(records) == 1
    assert records[0]["run_id"] == "run-1"


def test_cleanup_workflow_retention_tolerates_registry_removed_before_unlink(tmp_path: Path) -> None:
    """Workflow cleanup tolerates registry unlink races after successful truncation."""
    registry = tmp_path / "retention.ndjson"
    trace = tmp_path / "run-1" / "trace.ndjson"
    trace.parent.mkdir(parents=True, exist_ok=True)
    trace.write_text("encrypted", encoding="utf-8")
    append_retention_record(
        registry,
        run_id="run-1",
        trace_path=str(trace),
        expires_at="2099-01-01T00:00:00+00:00",
    )

    mock_storage = MagicMock()
    mock_storage.delete.return_value = True
    with (
        patch("agentic_devtools.orchestration.hierarchy.aggregation.ProtectedStorage", return_value=mock_storage),
        patch("pathlib.Path.unlink", side_effect=FileNotFoundError),
    ):
        assert cleanup_workflow_retention(registry, master_key=_MASTER_KEY, authorized_principals=_PRINCIPALS) == (
            "run-1",
        )


def test_cleanup_workflow_retention_preserves_string_trace_path_when_run_id_is_not_string(tmp_path: Path) -> None:
    """Workflow cleanup keeps string trace-path records that have a non-string run_id."""
    registry = tmp_path / "retention.ndjson"
    append_retention_record(
        registry,
        run_id="run-1",
        trace_path=str(tmp_path / "run-1" / "trace.ndjson"),
        expires_at="2099-01-01T00:00:00+00:00",
    )
    records = [json.loads(line) for line in registry.read_text().splitlines() if line.strip()]
    records[0]["run_id"] = 1
    registry.write_text("\n".join(json.dumps(r, sort_keys=True) for r in records) + "\n", encoding="utf-8")

    removed = cleanup_workflow_retention(registry, master_key=_MASTER_KEY, authorized_principals=_PRINCIPALS)

    assert removed == ()
    retained = [json.loads(line) for line in registry.read_text().splitlines() if line.strip()]
    assert retained[0]["run_id"] == 1


def test_cleanup_workflow_retention_preserves_record_for_non_canonical_trace_path(tmp_path: Path) -> None:
    """Workflow cleanup keeps records whose trace path escapes the canonical run directory layout."""
    registry = tmp_path / "retention.ndjson"
    outside_trace = tmp_path / "outside-trace.ndjson"
    outside_trace.write_text("encrypted", encoding="utf-8")
    append_retention_record(
        registry,
        run_id="run-unsafe",
        trace_path=str(outside_trace),
        expires_at="2099-01-01T00:00:00+00:00",
    )

    removed = cleanup_workflow_retention(registry, master_key=_MASTER_KEY, authorized_principals=_PRINCIPALS)

    assert removed == ()
    records = [json.loads(line) for line in registry.read_text().splitlines() if line.strip()]
    assert len(records) == 1
    assert records[0]["run_id"] == "run-unsafe"


def test_cleanup_workflow_retention_removes_record_when_canonical_trace_is_missing(tmp_path: Path) -> None:
    registry = tmp_path / "retention.ndjson"
    append_retention_record(
        registry,
        run_id="run-missing",
        trace_path=str(tmp_path / "run-missing" / "trace.ndjson"),
        expires_at="2099-01-01T00:00:00+00:00",
    )

    removed = cleanup_workflow_retention(registry, master_key=_MASTER_KEY, authorized_principals=_PRINCIPALS)

    assert removed == ("run-missing",)
    assert not registry.exists()


def test_cleanup_workflow_retention_resolves_keys_when_not_passed(tmp_path: Path) -> None:
    registry = tmp_path / "retention.ndjson"
    trace = tmp_path / "run-1" / "trace.ndjson"
    trace.parent.mkdir(parents=True, exist_ok=True)
    trace.write_text("encrypted", encoding="utf-8")
    append_retention_record(
        registry,
        run_id="run-1",
        trace_path=str(trace),
        expires_at="2099-01-01T00:00:00+00:00",
    )

    mock_storage = MagicMock()
    mock_storage.delete.return_value = True
    with (
        patch("agentic_devtools.orchestration.hierarchy.aggregation.resolve_master_key", return_value=_MASTER_KEY),
        patch(
            "agentic_devtools.orchestration.hierarchy.aggregation.resolve_authorized_principals",
            return_value=_PRINCIPALS,
        ),
        patch("agentic_devtools.orchestration.hierarchy.aggregation.ProtectedStorage", return_value=mock_storage),
    ):
        removed = cleanup_workflow_retention(registry)

    assert removed == ("run-1",)
