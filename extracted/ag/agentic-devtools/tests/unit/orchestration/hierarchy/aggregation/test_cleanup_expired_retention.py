"""Tests for cleanup_expired_retention."""

import json
from datetime import UTC, datetime, timedelta
from pathlib import Path
from unittest.mock import MagicMock, patch

from agentic_devtools.orchestration.hierarchy.aggregation import (
    append_retention_record,
    cleanup_expired_retention,
)

_MASTER_KEY = b"x" * 32
_PRINCIPALS = frozenset({"test-principal"})


def test_cleanup_expired_retention_returns_empty_when_no_registry(tmp_path: Path) -> None:
    registry = tmp_path / "retention-registry.ndjson"
    result = cleanup_expired_retention(registry, master_key=_MASTER_KEY, authorized_principals=_PRINCIPALS)
    assert result == ()


def test_cleanup_expired_retention_keeps_unexpired_records(tmp_path: Path) -> None:
    registry = tmp_path / "retention-registry.ndjson"
    future = (datetime.now(UTC) + timedelta(days=10)).isoformat()
    append_retention_record(
        registry,
        run_id="run-keep",
        trace_path=str(tmp_path / "trace-keep.ndjson"),
        expires_at=future,
    )

    removed = cleanup_expired_retention(registry, master_key=_MASTER_KEY, authorized_principals=_PRINCIPALS)

    assert removed == ()
    records = [json.loads(line) for line in registry.read_text().splitlines() if line.strip()]
    assert len(records) == 1


def test_cleanup_expired_retention_removes_expired_run_ids(tmp_path: Path) -> None:
    registry = tmp_path / "retention-registry.ndjson"
    past = (datetime.now(UTC) - timedelta(days=1)).isoformat()
    future = (datetime.now(UTC) + timedelta(days=10)).isoformat()
    append_retention_record(
        registry, run_id="run-expired", trace_path=str(tmp_path / "run-expired" / "trace.ndjson"), expires_at=past
    )
    append_retention_record(registry, run_id="run-keep", trace_path=str(tmp_path / "keep.ndjson"), expires_at=future)

    removed = cleanup_expired_retention(registry, master_key=_MASTER_KEY, authorized_principals=_PRINCIPALS)

    assert removed == ("run-expired",)
    records = [json.loads(line) for line in registry.read_text().splitlines() if line.strip()]
    assert len(records) == 1
    assert records[0]["run_id"] == "run-keep"


def test_cleanup_expired_retention_deletes_existing_trace_file(tmp_path: Path) -> None:
    registry = tmp_path / "retention-registry.ndjson"
    trace_file = tmp_path / "run-del" / "trace.ndjson"
    trace_file.parent.mkdir(parents=True, exist_ok=True)
    trace_file.write_text("", encoding="utf-8")
    past = (datetime.now(UTC) - timedelta(days=1)).isoformat()
    append_retention_record(registry, run_id="run-del", trace_path=str(trace_file), expires_at=past)

    mock_storage = MagicMock()
    mock_storage.delete.return_value = True
    with patch(
        "agentic_devtools.orchestration.hierarchy.aggregation.ProtectedStorage",
        return_value=mock_storage,
    ):
        removed = cleanup_expired_retention(registry, master_key=_MASTER_KEY, authorized_principals=_PRINCIPALS)

    assert removed == ("run-del",)
    mock_storage.delete.assert_called_once()


def test_cleanup_expired_retention_skips_delete_for_missing_trace_file(tmp_path: Path) -> None:
    registry = tmp_path / "retention-registry.ndjson"
    past = (datetime.now(UTC) - timedelta(days=1)).isoformat()
    append_retention_record(
        registry,
        run_id="run-missing",
        trace_path=str(tmp_path / "run-missing" / "trace.ndjson"),
        expires_at=past,
    )

    removed = cleanup_expired_retention(registry, master_key=_MASTER_KEY, authorized_principals=_PRINCIPALS)

    assert removed == ("run-missing",)


def test_cleanup_expired_retention_tolerates_delete_error(tmp_path: Path) -> None:
    registry = tmp_path / "retention-registry.ndjson"
    trace_file = tmp_path / "run-err" / "trace.ndjson"
    trace_file.parent.mkdir(parents=True, exist_ok=True)
    trace_file.write_text("", encoding="utf-8")
    past = (datetime.now(UTC) - timedelta(days=1)).isoformat()
    append_retention_record(registry, run_id="run-err", trace_path=str(trace_file), expires_at=past)

    mock_storage = MagicMock()
    mock_storage.delete.side_effect = OSError("permission denied")
    with patch(
        "agentic_devtools.orchestration.hierarchy.aggregation.ProtectedStorage",
        return_value=mock_storage,
    ):
        removed = cleanup_expired_retention(registry, master_key=_MASTER_KEY, authorized_principals=_PRINCIPALS)

    assert removed == ()
    records = [json.loads(line) for line in registry.read_text().splitlines() if line.strip()]
    assert len(records) == 1
    assert records[0]["run_id"] == "run-err"


def test_cleanup_expired_retention_keeps_record_with_non_string_expires_at(tmp_path: Path) -> None:
    """Records with non-string expires_at are kept (treated as unexpired/unknown)."""
    import json as _json

    registry = tmp_path / "retention-registry.ndjson"
    registry.parent.mkdir(parents=True, exist_ok=True)
    registry.write_text(
        _json.dumps(
            {
                "run_id": "run-bad",
                "trace_path": "/tmp/x.ndjson",
                "expires_at": 12345,
                "timestamp": "2099-01-01T00:00:00+00:00",
            }
        )
        + "\n",
        encoding="utf-8",
    )

    removed = cleanup_expired_retention(registry, master_key=_MASTER_KEY, authorized_principals=_PRINCIPALS)

    assert removed == ()


def test_cleanup_expired_retention_keeps_record_with_unparseable_expires_at(tmp_path: Path) -> None:
    """Records with unparseable expires_at are kept (treated as unexpired/unknown)."""
    import json as _json

    registry = tmp_path / "retention-registry.ndjson"
    registry.parent.mkdir(parents=True, exist_ok=True)
    registry.write_text(
        _json.dumps(
            {
                "run_id": "run-bad",
                "trace_path": "/tmp/x.ndjson",
                "expires_at": "not-a-date",
                "timestamp": "2099-01-01T00:00:00+00:00",
            }
        )
        + "\n",
        encoding="utf-8",
    )

    removed = cleanup_expired_retention(registry, master_key=_MASTER_KEY, authorized_principals=_PRINCIPALS)

    assert removed == ()


def test_cleanup_expired_retention_handles_expired_record_with_non_string_trace_path(tmp_path: Path) -> None:
    """Expired records with non-string trace_path skip file deletion but are still removed."""
    import json as _json

    registry = tmp_path / "retention-registry.ndjson"
    past = (datetime.now(UTC) - timedelta(days=1)).isoformat()
    registry.parent.mkdir(parents=True, exist_ok=True)
    registry.write_text(
        _json.dumps({"run_id": "run-no-path", "trace_path": None, "expires_at": past, "timestamp": past}) + "\n",
        encoding="utf-8",
    )

    removed = cleanup_expired_retention(registry, master_key=_MASTER_KEY, authorized_principals=_PRINCIPALS)

    assert removed == ("run-no-path",)


def test_cleanup_expired_retention_handles_expired_record_with_non_string_run_id(tmp_path: Path) -> None:
    """Expired records with non-string run_id are cleaned up silently without run_id in the result."""
    import json as _json

    registry = tmp_path / "retention-registry.ndjson"
    past = (datetime.now(UTC) - timedelta(days=1)).isoformat()
    registry.parent.mkdir(parents=True, exist_ok=True)
    registry.write_text(
        _json.dumps({"run_id": 999, "trace_path": None, "expires_at": past, "timestamp": past}) + "\n",
        encoding="utf-8",
    )

    removed = cleanup_expired_retention(registry, master_key=_MASTER_KEY, authorized_principals=_PRINCIPALS)

    assert removed == ()


def test_cleanup_expired_retention_keeps_record_for_non_canonical_trace_path(tmp_path: Path) -> None:
    """Expired records with trace paths outside the canonical run directory are preserved."""
    registry = tmp_path / "retention-registry.ndjson"
    past = (datetime.now(UTC) - timedelta(days=1)).isoformat()
    outside_trace = tmp_path / "outside-trace.ndjson"
    append_retention_record(registry, run_id="run-unsafe", trace_path=str(outside_trace), expires_at=past)

    removed = cleanup_expired_retention(registry, master_key=_MASTER_KEY, authorized_principals=_PRINCIPALS)

    assert removed == ()
    records = [json.loads(line) for line in registry.read_text().splitlines() if line.strip()]
    assert len(records) == 1
    assert records[0]["run_id"] == "run-unsafe"


def test_cleanup_expired_retention_preserves_string_trace_path_when_run_id_is_not_string(tmp_path: Path) -> None:
    """Expired records with string trace paths require a string run_id for canonical validation."""
    registry = tmp_path / "retention-registry.ndjson"
    past = (datetime.now(UTC) - timedelta(days=1)).isoformat()
    append_retention_record(
        registry, run_id="run-1", trace_path=str(tmp_path / "run-1" / "trace.ndjson"), expires_at=past
    )
    records = [json.loads(line) for line in registry.read_text().splitlines() if line.strip()]
    records[0]["run_id"] = 1
    registry.write_text("\n".join(json.dumps(r, sort_keys=True) for r in records) + "\n", encoding="utf-8")

    removed = cleanup_expired_retention(registry, master_key=_MASTER_KEY, authorized_principals=_PRINCIPALS)

    assert removed == ()
    retained = [json.loads(line) for line in registry.read_text().splitlines() if line.strip()]
    assert retained[0]["run_id"] == 1


def test_cleanup_expired_retention_keeps_record_for_relative_trace_path(tmp_path: Path) -> None:
    """Relative trace paths are not trusted for deletion and are preserved."""
    registry = tmp_path / "retention-registry.ndjson"
    past = (datetime.now(UTC) - timedelta(days=1)).isoformat()
    append_retention_record(registry, run_id="run-relative", trace_path="trace.ndjson", expires_at=past)

    removed = cleanup_expired_retention(registry, master_key=_MASTER_KEY, authorized_principals=_PRINCIPALS)

    assert removed == ()
    records = [json.loads(line) for line in registry.read_text().splitlines() if line.strip()]
    assert records[0]["run_id"] == "run-relative"


def test_cleanup_expired_retention_keeps_record_when_trace_path_escapes_hierarchy_root(tmp_path: Path) -> None:
    """Absolute trace paths outside the hierarchy root are preserved."""
    registry = tmp_path / "retention-registry.ndjson"
    past = (datetime.now(UTC) - timedelta(days=1)).isoformat()
    append_retention_record(registry, run_id="run-escape", trace_path="/etc/passwd", expires_at=past)

    removed = cleanup_expired_retention(registry, master_key=_MASTER_KEY, authorized_principals=_PRINCIPALS)

    assert removed == ()
    records = [json.loads(line) for line in registry.read_text().splitlines() if line.strip()]
    assert records[0]["run_id"] == "run-escape"


def test_cleanup_expired_retention_keeps_record_when_trace_path_resolution_fails(tmp_path: Path) -> None:
    """Resolution errors are treated as unsafe paths and preserve the record."""
    registry = tmp_path / "retention-registry.ndjson"
    past = (datetime.now(UTC) - timedelta(days=1)).isoformat()
    append_retention_record(
        registry,
        run_id="run-bad-resolve",
        trace_path=str(tmp_path / "run-bad-resolve" / "trace.ndjson"),
        expires_at=past,
    )

    with patch("pathlib.Path.resolve", side_effect=OSError("resolve failed")):
        removed = cleanup_expired_retention(registry, master_key=_MASTER_KEY, authorized_principals=_PRINCIPALS)

    assert removed == ()
    records = [json.loads(line) for line in registry.read_text().splitlines() if line.strip()]
    assert records[0]["run_id"] == "run-bad-resolve"


def test_cleanup_expired_retention_keeps_record_when_registry_path_has_symlink_component(tmp_path: Path) -> None:
    """Symlinked registry paths are rejected for canonical-trace cleanup."""
    real_dir = tmp_path / "real"
    real_dir.mkdir()
    linked_dir = tmp_path / "linked"
    linked_dir.symlink_to(real_dir, target_is_directory=True)
    registry = linked_dir / "retention-registry.ndjson"
    past = (datetime.now(UTC) - timedelta(days=1)).isoformat()
    append_retention_record(
        registry,
        run_id="run-symlink-registry",
        trace_path=str(real_dir / "run-symlink-registry" / "trace.ndjson"),
        expires_at=past,
    )

    removed = cleanup_expired_retention(registry, master_key=_MASTER_KEY, authorized_principals=_PRINCIPALS)

    assert removed == ()
    records = [json.loads(line) for line in registry.read_text().splitlines() if line.strip()]
    assert records[0]["run_id"] == "run-symlink-registry"


def test_cleanup_expired_retention_keeps_record_when_expected_trace_path_has_symlink_component(tmp_path: Path) -> None:
    """Symlinked run directories are rejected even when paths otherwise match canonically."""
    registry = tmp_path / "retention-registry.ndjson"
    real_run_dir = tmp_path / "real-run"
    real_run_dir.mkdir()
    run_dir = tmp_path / "run-symlink"
    run_dir.symlink_to(real_run_dir, target_is_directory=True)
    trace_path = run_dir / "trace.ndjson"
    past = (datetime.now(UTC) - timedelta(days=1)).isoformat()
    append_retention_record(registry, run_id="run-symlink", trace_path=str(trace_path), expires_at=past)

    removed = cleanup_expired_retention(registry, master_key=_MASTER_KEY, authorized_principals=_PRINCIPALS)

    assert removed == ()
    records = [json.loads(line) for line in registry.read_text().splitlines() if line.strip()]
    assert records[0]["run_id"] == "run-symlink"
