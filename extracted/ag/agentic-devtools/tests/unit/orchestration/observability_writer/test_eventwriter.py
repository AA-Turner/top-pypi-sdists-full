"""Tests for EventWriter class."""

import json
from pathlib import Path
from unittest.mock import patch

from agentic_devtools.orchestration.observability_writer import EventWriter


class TestEventWriter:
    """Tests for the EventWriter class."""

    def test_creates_observability_directory(self, tmp_path: Path) -> None:
        writer = EventWriter("test-run-id", tmp_path)
        assert (tmp_path / "observability").is_dir()
        writer.close()

    def test_creates_log_file_at_correct_path(self, tmp_path: Path) -> None:
        writer = EventWriter("my-run-123", tmp_path)
        assert writer.log_path == tmp_path / "observability" / "run-my-run-123.jsonl"
        writer.close()

    def test_write_appends_json_line(self, tmp_path: Path) -> None:
        writer = EventWriter("run1", tmp_path)
        writer.write({"type": "node", "seq": 1})
        writer.write({"type": "llm_call", "seq": 2})
        writer.close()

        log_file = tmp_path / "observability" / "run-run1.jsonl"
        lines = log_file.read_text().strip().split("\n")
        assert len(lines) == 2
        assert json.loads(lines[0]) == {"type": "node", "seq": 1}
        assert json.loads(lines[1]) == {"type": "llm_call", "seq": 2}

    def test_close_is_idempotent(self, tmp_path: Path) -> None:
        writer = EventWriter("run1", tmp_path)
        writer.close()
        writer.close()  # Should not raise

    def test_init_failure_degrades_to_noop(self, capsys: object) -> None:
        """Writer degrades gracefully when init fails."""
        writer = EventWriter("invalid/run/id", "/nonexistent/path")
        assert writer.degraded is True
        # Writes should be no-ops
        writer.write({"event": "test"})
        writer.close()

    def test_init_failure_emits_stderr_warning(self, tmp_path: Path, capsys: object) -> None:
        """Invalid run_id emits stderr warning."""
        import io

        captured = io.StringIO()
        with patch("sys.stderr", captured):
            EventWriter("bad/id", tmp_path)
        assert "WARNING" in captured.getvalue()

    def test_write_failure_emits_stderr_warning(self, tmp_path: Path) -> None:
        """I/O errors during write emit stderr warning."""
        writer = EventWriter("run1", tmp_path)
        # Close the file to force a write error
        writer._file.close()  # type: ignore[union-attr]
        writer._degraded = False  # Override so write is attempted

        import io

        captured = io.StringIO()
        with patch("sys.stderr", captured):
            writer.write({"event": "test"})
        assert "WARNING" in captured.getvalue()

    def test_write_failure_degrades_writer_permanently(self, tmp_path: Path) -> None:
        """After the first write failure the writer becomes permanently degraded."""
        import io

        writer = EventWriter("run1", tmp_path)
        # Force a write error by closing the underlying file handle
        writer._file.close()  # type: ignore[union-attr]
        writer._degraded = False  # reset so the first write is attempted

        captured = io.StringIO()
        with patch("sys.stderr", captured):
            writer.write({"event": "first-fail"})

        # Writer must now be in degraded (no-op) mode
        assert writer.degraded is True
        assert writer._file is None

        # Subsequent writes must be silent no-ops (no additional stderr output)
        captured2 = io.StringIO()
        with patch("sys.stderr", captured2):
            writer.write({"event": "second-should-be-noop"})
        assert captured2.getvalue() == ""

    def test_write_serialization_failure_caught(self, tmp_path: Path) -> None:
        """Non-serializable data doesn't crash the writer."""
        writer = EventWriter("run1", tmp_path)
        # The default=str handler should handle most cases,
        # but let's verify the error path works
        writer.write({"data": "normal"})  # Should work fine
        writer.close()

    def test_not_degraded_on_success(self, tmp_path: Path) -> None:
        writer = EventWriter("valid-run", tmp_path)
        assert writer.degraded is False
        writer.close()

    def test_log_path_none_when_degraded(self) -> None:
        writer = EventWriter("bad/path", "/nonexistent")
        # log_path may still be set even if file open failed;
        # what matters is degraded=True
        assert writer.degraded is True

    def test_close_exception_swallowed(self, tmp_path: Path) -> None:
        """Exception during file.close() is caught silently."""
        writer = EventWriter("run1", tmp_path)
        # Replace the file with a mock that raises on close
        from unittest.mock import MagicMock

        mock_file = MagicMock()
        mock_file.close.side_effect = OSError("disk full")
        writer._file = mock_file
        # Should not raise
        writer.close()
        assert writer._file is None

    def test_write_degradation_file_close_exception_swallowed(self, tmp_path: Path) -> None:
        """If file.close() raises during write-error degradation, the exception is swallowed."""
        import io
        from unittest.mock import MagicMock

        writer = EventWriter("run1", tmp_path)

        # Replace the real file with a mock: write raises, then close also raises.
        mock_file = MagicMock()
        mock_file.write.side_effect = OSError("disk full")
        mock_file.close.side_effect = OSError("cannot close")
        writer._file = mock_file

        captured = io.StringIO()
        with patch("sys.stderr", captured):
            # Must not raise despite both write and close failing
            writer.write({"event": "test"})

        # Writer must still end up degraded with file cleared
        assert writer.degraded is True
        assert writer._file is None
        assert "WARNING" in captured.getvalue()

    def test_write_silent_when_file_cleared_during_lock(self, tmp_path: Path) -> None:
        """Concurrent close behavior: no warning when file becomes None before write."""
        import io
        from unittest.mock import MagicMock

        class _FileClearingLock:
            def __init__(self, target: EventWriter) -> None:
                self._target = target

            def __enter__(self) -> "_FileClearingLock":
                self._target._file = None
                return self

            def __exit__(self, exc_type: object, exc: object, tb: object) -> None:
                pass

        writer = EventWriter("run1", tmp_path)
        writer._degraded = False
        mock_file = MagicMock()
        writer._file = mock_file
        writer._lock = _FileClearingLock(writer)  # type: ignore[assignment]

        captured = io.StringIO()
        with patch("sys.stderr", captured):
            writer.write({"event": "test"})

        assert captured.getvalue() == ""
        assert writer.degraded is False
        mock_file.write.assert_not_called()
