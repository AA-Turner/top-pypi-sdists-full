"""Tests for the ``run_specialization`` I/O wrapper."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

from agentic_devtools.cli.setup.expectations_specializer import (
    SPECIALIZED_OUTPUT_FILENAME,
    RepositoryConfiguration,
    _StartupFingerprintError,
    _StartupFingerprintState,
    run_specialization,
)

VALID_DOC = "# agdt-setup\n\n## Phases\n\n1. `version_check`\n"
MALFORMED_DOC = "# agdt-setup\n\nno phases heading here\n"
MALFORMED_VERSION_GUARD_DOC = """# agdt-setup

## Phases

1. `version_check`

## Decision Points / Paths

| Decision | Condition | Path |
|----------|-----------|------|
| Version guard — block |
"""


def _config() -> RepositoryConfiguration:
    return RepositoryConfiguration(
        repo="owner/repo",
        issue_adapter="github",
        has_npm=True,
        ssl_hosts=("a.internal",),
        system_only=False,
        version_pin="1.0.0",
        effective_flags={},
    )


class TestSkip:
    """FR-004 skip behavior when the general doc is absent."""

    def test_none_path_skips_without_writing(self, tmp_path: Path) -> None:
        """A ``None`` path yields a skip result and writes nothing."""
        result = run_specialization(_config(), tmp_path, None)
        assert result.status == "skipped"
        assert result.reason is not None
        assert "not found" in result.reason
        assert not (tmp_path / SPECIALIZED_OUTPUT_FILENAME).exists()

    def test_missing_path_skips_without_writing(self, tmp_path: Path) -> None:
        """A non-existent path yields a skip result and writes nothing."""
        missing = tmp_path / "missing.md"
        result = run_specialization(_config(), tmp_path, missing)
        assert result.status == "skipped"
        assert not (tmp_path / SPECIALIZED_OUTPUT_FILENAME).exists()

    def test_skip_invalidates_stale_output(self, tmp_path: Path) -> None:
        """A stale specialized artifact from a previous run is removed on skip."""
        output = tmp_path / SPECIALIZED_OUTPUT_FILENAME
        output.write_text("STALE CONTENT", encoding="utf-8")
        result = run_specialization(_config(), tmp_path, None)
        assert result.status == "skipped"
        assert not output.exists()

    def test_skip_cleanup_failure_yields_error(self, tmp_path: Path) -> None:
        """A stale-output cleanup failure upgrades a skip result to ``error``."""
        output = tmp_path / SPECIALIZED_OUTPUT_FILENAME
        output.write_text("STALE CONTENT", encoding="utf-8")
        with patch("pathlib.Path.unlink", side_effect=OSError("cleanup failed")):
            result = run_specialization(_config(), tmp_path, None)
        assert result.status == "error"
        assert result.reason is not None
        assert "cleanup failed" in result.reason

    def test_initial_inspect_failure_yields_error(self, tmp_path: Path) -> None:
        """An ``OSError`` from the initial ``_output_fingerprint`` becomes an error result."""
        doc = tmp_path / "general.md"
        output = tmp_path / SPECIALIZED_OUTPUT_FILENAME

        original_stat = Path.stat

        def _selective_stat(path: Path, *args, **kwargs):
            if path == output:
                raise OSError("inspect failed")
            return original_stat(path, *args, **kwargs)

        with patch.object(Path, "stat", autospec=True, side_effect=_selective_stat):
            result = run_specialization(_config(), tmp_path, doc)

        assert result.status == "error"
        assert result.reason is not None
        assert "inspect failed" in result.reason

    def test_exists_failure_yields_error(self, tmp_path: Path) -> None:
        """An ``OSError`` from ``Path.exists()`` becomes an error result."""
        doc = tmp_path / "general.md"
        with patch.object(Path, "exists", side_effect=OSError("exists failed")):
            result = run_specialization(_config(), tmp_path, doc)
        assert result.status == "error"
        assert result.reason is not None
        assert "exists failed" in result.reason


class TestSuccess:
    """FR-007 success + overwrite behavior."""

    def test_success_writes_file(self, tmp_path: Path) -> None:
        """A valid doc produces a success result and writes the output file."""
        doc = tmp_path / "general.md"
        doc.write_text(VALID_DOC, encoding="utf-8")
        result = run_specialization(_config(), tmp_path, doc)
        assert result.status == "success"
        assert result.content is not None
        output = tmp_path / SPECIALIZED_OUTPUT_FILENAME
        assert output.exists()
        assert output.read_text(encoding="utf-8") == result.content

    def test_overwrites_existing_output(self, tmp_path: Path) -> None:
        """An existing output file is overwritten on re-invocation."""
        doc = tmp_path / "general.md"
        doc.write_text(VALID_DOC, encoding="utf-8")
        output = tmp_path / SPECIALIZED_OUTPUT_FILENAME
        output.write_text("STALE CONTENT", encoding="utf-8")
        result = run_specialization(_config(), tmp_path, doc)
        assert result.status == "success"
        assert "STALE CONTENT" not in output.read_text(encoding="utf-8")


class TestError:
    """FR-007 error conversion for every failure mode."""

    def test_malformed_doc_yields_error(self, tmp_path: Path) -> None:
        """A ``ValueError`` from the helper becomes an error result."""
        doc = tmp_path / "general.md"
        doc.write_text(MALFORMED_DOC, encoding="utf-8")
        result = run_specialization(_config(), tmp_path, doc)
        assert result.status == "error"
        assert result.reason is not None
        assert "Phases" in result.reason

    def test_malformed_version_guard_row_yields_error(self, tmp_path: Path) -> None:
        """A malformed version-guard row becomes an error result."""
        doc = tmp_path / "general.md"
        doc.write_text(MALFORMED_VERSION_GUARD_DOC, encoding="utf-8")
        result = run_specialization(_config(), tmp_path, doc)
        assert result.status == "error"
        assert result.reason is not None
        assert "Malformed decision row" in result.reason

    def test_invalid_utf8_yields_error(self, tmp_path: Path) -> None:
        """Invalid UTF-8 bytes raise ``UnicodeDecodeError`` -> error result."""
        doc = tmp_path / "general.md"
        doc.write_bytes(b"\xff\xfe invalid utf8")
        result = run_specialization(_config(), tmp_path, doc)
        assert result.status == "error"

    def test_read_failure_yields_error(self, tmp_path: Path) -> None:
        """An ``OSError`` while reading becomes an error result."""
        # A directory that exists but cannot be read as text.
        doc_dir = tmp_path / "a_directory"
        doc_dir.mkdir()
        result = run_specialization(_config(), tmp_path, doc_dir)
        assert result.status == "error"

    def test_creates_missing_state_directory_before_writing(self, tmp_path: Path) -> None:
        """A missing state directory is created before writing the specialized file."""
        doc = tmp_path / "general.md"
        doc.write_text(VALID_DOC, encoding="utf-8")
        missing_state_dir = tmp_path / "does_not_exist"
        result = run_specialization(_config(), missing_state_dir, doc)
        assert result.status == "success"
        output = missing_state_dir / SPECIALIZED_OUTPUT_FILENAME
        assert output.exists()

    def test_state_directory_creation_failure_yields_error(self, tmp_path: Path) -> None:
        """An ``OSError`` creating the state directory becomes an error result."""
        doc = tmp_path / "general.md"
        doc.write_text(VALID_DOC, encoding="utf-8")
        target_dir = tmp_path / "state_dir"
        with patch.object(Path, "mkdir", side_effect=OSError("mkdir failed")):
            result = run_specialization(_config(), target_dir, doc)
        assert result.status == "error"
        assert result.reason is not None
        assert "mkdir failed" in result.reason

    def test_error_invalidates_stale_output(self, tmp_path: Path) -> None:
        """A stale specialized artifact is removed when specialization errors."""
        doc = tmp_path / "general.md"
        doc.write_text(MALFORMED_DOC, encoding="utf-8")
        output = tmp_path / SPECIALIZED_OUTPUT_FILENAME
        output.write_text("STALE CONTENT", encoding="utf-8")
        result = run_specialization(_config(), tmp_path, doc)
        assert result.status == "error"
        assert not output.exists()

    def test_error_cleanup_failure_includes_cleanup_reason(self, tmp_path: Path) -> None:
        """A cleanup failure is included in the returned error reason."""
        doc = tmp_path / "general.md"
        doc.write_text(MALFORMED_DOC, encoding="utf-8")
        output = tmp_path / SPECIALIZED_OUTPUT_FILENAME
        output.write_text("STALE CONTENT", encoding="utf-8")

        original_unlink = Path.unlink

        def _selective_unlink(path: Path, *args, **kwargs) -> None:
            if path == output:
                raise OSError("cleanup failed")
            original_unlink(path, *args, **kwargs)

        with patch.object(Path, "unlink", autospec=True, side_effect=_selective_unlink):
            result = run_specialization(_config(), tmp_path, doc)
        assert result.status == "error"
        assert result.reason is not None
        assert "cleanup failed" in result.reason

    def test_error_inspect_failure_includes_inspect_reason(self, tmp_path: Path) -> None:
        """An inspect failure while checking stale-output ownership becomes an error."""
        doc = tmp_path / "general.md"
        doc.write_text(MALFORMED_DOC, encoding="utf-8")
        output = tmp_path / SPECIALIZED_OUTPUT_FILENAME
        output.write_text("STALE CONTENT", encoding="utf-8")

        original_stat = Path.stat
        stat_calls = 0

        def _selective_stat(path: Path, *args, **kwargs):
            nonlocal stat_calls
            if path == output:
                stat_calls += 1
                if stat_calls == 2:
                    raise OSError("inspect failed")
            return original_stat(path, *args, **kwargs)

        with patch.object(Path, "stat", autospec=True, side_effect=_selective_stat):
            result = run_specialization(_config(), tmp_path, doc)

        assert result.status == "error"
        assert result.reason is not None
        assert "inspect failed" in result.reason

    def test_error_cleanup_race_after_stat_keeps_original_reason(self, tmp_path: Path) -> None:
        """A delete-by-another-run between stat and unlink is treated as already clean."""
        doc = tmp_path / "general.md"
        doc.write_text(MALFORMED_DOC, encoding="utf-8")
        output = tmp_path / SPECIALIZED_OUTPUT_FILENAME
        output.write_text("STALE CONTENT", encoding="utf-8")

        original_unlink = Path.unlink

        def _selective_unlink(path: Path, *args, **kwargs) -> None:
            if path == output:
                raise FileNotFoundError
            original_unlink(path, *args, **kwargs)

        with patch.object(Path, "unlink", autospec=True, side_effect=_selective_unlink):
            result = run_specialization(_config(), tmp_path, doc)

        assert result.status == "error"
        assert result.reason is not None
        assert "Phases" in result.reason

    def test_error_preserves_output_published_by_concurrent_run(self, tmp_path: Path) -> None:
        """A later error does not delete output created after this run started."""
        doc = tmp_path / "general.md"
        doc.write_text(VALID_DOC, encoding="utf-8")
        output = tmp_path / SPECIALIZED_OUTPUT_FILENAME

        def _concurrent_publish_then_fail(*args, **kwargs) -> str:
            output.write_text("fresh concurrent content", encoding="utf-8")
            raise ValueError("specialization failed")

        with patch(
            "agentic_devtools.cli.setup.expectations_specializer.specialize_expectations",
            side_effect=_concurrent_publish_then_fail,
        ):
            result = run_specialization(_config(), tmp_path, doc)

        assert result.status == "error"
        assert output.read_text(encoding="utf-8") == "fresh concurrent content"

    def test_error_preserves_replaced_output_from_concurrent_run(self, tmp_path: Path) -> None:
        """A later error does not delete a stale file that another run replaced."""
        doc = tmp_path / "general.md"
        doc.write_text(VALID_DOC, encoding="utf-8")
        output = tmp_path / SPECIALIZED_OUTPUT_FILENAME
        output.write_text("stale content", encoding="utf-8")

        def _concurrent_replace_then_fail(*args, **kwargs) -> str:
            output.unlink()
            output.write_text("fresh concurrent content", encoding="utf-8")
            raise ValueError("specialization failed")

        with patch(
            "agentic_devtools.cli.setup.expectations_specializer.specialize_expectations",
            side_effect=_concurrent_replace_then_fail,
        ):
            result = run_specialization(_config(), tmp_path, doc)

        assert result.status == "error"
        assert output.read_text(encoding="utf-8") == "fresh concurrent content"

    def test_success_last_writer_wins_when_output_changes_before_publish(self, tmp_path: Path) -> None:
        """A concurrent run that publishes before our lock is acquired keeps its output."""
        doc = tmp_path / "general.md"
        doc.write_text(VALID_DOC, encoding="utf-8")
        output = tmp_path / SPECIALIZED_OUTPUT_FILENAME
        output.write_text("stale content", encoding="utf-8")
        stale_fingerprint = (output.stat().st_ino, output.stat().st_size, output.stat().st_mtime_ns)

        def _concurrent_replace_then_succeed(*args, **kwargs) -> str:
            output.unlink()
            output.write_text("concurrent content", encoding="utf-8")
            return "our specialized content"

        with patch(
            "agentic_devtools.cli.setup.expectations_specializer.specialize_expectations",
            side_effect=_concurrent_replace_then_succeed,
        ):
            result = run_specialization(_config(), tmp_path, doc, startup_fingerprint=stale_fingerprint)

        assert result.status == "skipped"
        assert result.content is None
        assert result.reason is not None
        assert "newer specialization result was already written" in result.reason
        # The concurrent run's output is preserved; we yielded to the newer publish.
        assert output.read_text(encoding="utf-8") == "concurrent content"

    def test_success_yields_to_newer_run_even_when_tmp_unlink_fails(self, tmp_path: Path) -> None:
        """Failure to remove the tmp file when yielding to a newer publish is tolerated."""
        doc = tmp_path / "general.md"
        doc.write_text(VALID_DOC, encoding="utf-8")
        output = tmp_path / SPECIALIZED_OUTPUT_FILENAME
        output.write_text("stale content", encoding="utf-8")
        stale_fingerprint = (output.stat().st_ino, output.stat().st_size, output.stat().st_mtime_ns)

        def _concurrent_replace_then_succeed(*args, **kwargs) -> str:
            # Another run replaces the output while we are still specializing.
            output.unlink()
            output.write_text("concurrent content", encoding="utf-8")
            return "our specialized content"

        original_unlink = Path.unlink

        def _unlink_raises_for_tmp(self: Path, missing_ok: bool = False) -> None:
            if self.suffix == ".tmp":
                raise OSError("cannot remove tmp")
            original_unlink(self, missing_ok=missing_ok)

        with (
            patch(
                "agentic_devtools.cli.setup.expectations_specializer.specialize_expectations",
                side_effect=_concurrent_replace_then_succeed,
            ),
            patch.object(Path, "unlink", _unlink_raises_for_tmp),
        ):
            result = run_specialization(_config(), tmp_path, doc, startup_fingerprint=stale_fingerprint)

        assert result.status == "skipped"
        assert result.content is None
        assert result.reason is not None
        assert "newer specialization result was already written" in result.reason

    def test_success_publishes_when_concurrent_failing_run_deletes_artifact(self, tmp_path: Path) -> None:
        """A concurrent non-success run that deletes the output does not prevent publish.

        Scenario:
        - A pre-existing output artifact exists when this run starts.
        - A concurrent *failing* run deletes that artifact before our lock is acquired.
        - Under the lock ``current_fingerprint`` is ``None`` (file absent).
        - ``None`` differs from ``initial_output_fingerprint`` but no newer output exists.
        - The successful run must publish rather than skip.
        """
        doc = tmp_path / "general.md"
        doc.write_text(VALID_DOC, encoding="utf-8")
        output = tmp_path / SPECIALIZED_OUTPUT_FILENAME
        output.write_text("stale content", encoding="utf-8")
        stale_fingerprint = (output.stat().st_ino, output.stat().st_size, output.stat().st_mtime_ns)

        def _concurrent_delete_then_succeed(*args, **kwargs) -> str:
            # Concurrent failing run removes the artifact; our run still succeeds.
            output.unlink()
            return "our specialized content"

        with patch(
            "agentic_devtools.cli.setup.expectations_specializer.specialize_expectations",
            side_effect=_concurrent_delete_then_succeed,
        ):
            result = run_specialization(_config(), tmp_path, doc, startup_fingerprint=stale_fingerprint)

        assert result.status == "success"
        assert result.content == "our specialized content"
        assert output.read_text(encoding="utf-8") == "our specialized content"


class TestStartupFingerprintThreading:
    """Verify that a supplied startup_fingerprint is used for all non-success paths."""

    def test_provided_fingerprint_skips_initial_stat(self, tmp_path: Path) -> None:
        """When startup_fingerprint is provided, the initial output-file stat is skipped.

        Without ``startup_fingerprint``, ``run_specialization`` performs two stat calls on
        the output file: one to capture the initial fingerprint and one inside
        ``_finalize_non_success`` to compare.  When the fingerprint is pre-supplied, only
        the comparison stat occurs — verifiable by counting output-file stat calls.
        """
        output = tmp_path / SPECIALIZED_OUTPUT_FILENAME
        output.write_text("stale content", encoding="utf-8")
        real_fingerprint = (output.stat().st_ino, output.stat().st_size, output.stat().st_mtime_ns)

        original_stat = Path.stat
        output_stat_calls = 0

        def _count_stat(path: Path, *args, **kwargs):
            nonlocal output_stat_calls
            if path == output:
                output_stat_calls += 1
            return original_stat(path, *args, **kwargs)

        with patch.object(Path, "stat", autospec=True, side_effect=_count_stat):
            result = run_specialization(_config(), tmp_path, None, startup_fingerprint=real_fingerprint)

        assert result.status == "skipped"
        assert not output.exists()
        # Exactly one stat on the output file: the comparison inside _finalize_non_success.
        # The initial capture is skipped because startup_fingerprint was pre-supplied.
        assert output_stat_calls == 1

    def test_provided_none_fingerprint_skips_deletion(self, tmp_path: Path) -> None:
        """startup_fingerprint=None means no prior artifact; concurrent output is left untouched."""
        output = tmp_path / SPECIALIZED_OUTPUT_FILENAME
        output.write_text("concurrent content", encoding="utf-8")
        result = run_specialization(_config(), tmp_path, None, startup_fingerprint=None)
        assert result.status == "skipped"
        assert output.exists()
        assert output.read_text(encoding="utf-8") == "concurrent content"

    def test_startup_fingerprint_error_marker_returns_error(self, tmp_path: Path) -> None:
        """A startup fingerprint inspection failure marker returns an error result."""
        result = run_specialization(
            _config(),
            tmp_path,
            None,
            startup_fingerprint=_StartupFingerprintError(error=OSError("permission denied")),
        )
        assert result.status == "error"
        assert result.reason is not None
        assert "permission denied" in result.reason

    def test_run_specialization_uses_startup_snapshot_directory(self, tmp_path: Path) -> None:
        """A startup snapshot forces all non-success paths to the original directory."""
        output = tmp_path / SPECIALIZED_OUTPUT_FILENAME
        output.write_text("stale content", encoding="utf-8")
        fingerprint = (output.stat().st_ino, output.stat().st_size, output.stat().st_mtime_ns)
        snapshot = _StartupFingerprintState(state_dir=tmp_path, fingerprint=fingerprint)

        result = run_specialization(_config(), tmp_path / "other", None, startup_fingerprint=snapshot)

        assert result.status == "skipped"
        assert not output.exists()

    def test_provided_fingerprint_protects_concurrent_publish_on_error(self, tmp_path: Path) -> None:
        """A mid-flight error does not delete an artifact whose fingerprint changed after startup."""
        doc = tmp_path / "general.md"
        doc.write_text(VALID_DOC, encoding="utf-8")
        output = tmp_path / SPECIALIZED_OUTPUT_FILENAME
        output.write_text("stale content", encoding="utf-8")
        stale_fingerprint = (output.stat().st_ino, output.stat().st_size, output.stat().st_mtime_ns)

        def _concurrent_replace_then_fail(*args, **kwargs) -> str:
            output.unlink()
            output.write_text("fresh concurrent content", encoding="utf-8")
            raise ValueError("specialization failed mid-flight")

        with patch(
            "agentic_devtools.cli.setup.expectations_specializer.specialize_expectations",
            side_effect=_concurrent_replace_then_fail,
        ):
            result = run_specialization(_config(), tmp_path, doc, startup_fingerprint=stale_fingerprint)

        assert result.status == "error"
        assert output.exists()
        assert output.read_text(encoding="utf-8") == "fresh concurrent content"
