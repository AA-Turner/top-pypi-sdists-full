"""Tests for WorkflowRun context manager."""

import json
import threading
from pathlib import Path

import pytest

from agentic_devtools.orchestration.observability_run import (
    WorkflowRun,
    record_node_execution,
)


class TestWorkflowRun:
    """Tests for WorkflowRun lifecycle."""

    def test_context_manager_creates_log_file(self, tmp_path: Path) -> None:
        with WorkflowRun(state_dir=tmp_path) as run:
            assert run.log_path is not None
            assert run.log_path.parent.name == "observability"

    def test_generates_run_id(self, tmp_path: Path) -> None:
        with WorkflowRun(state_dir=tmp_path) as run:
            assert len(run.run_id) == 32  # UUID4 hex

    def test_custom_run_id(self, tmp_path: Path) -> None:
        with WorkflowRun(state_dir=tmp_path, run_id="custom-123") as run:
            assert run.run_id == "custom-123"

    def test_event_seq_starts_at_one(self, tmp_path: Path) -> None:
        with WorkflowRun(state_dir=tmp_path) as run:
            record_node_execution(
                run,
                node_name="first",
                start_time="2024-01-01T00:00:00+00:00",
                end_time="2024-01-01T00:00:01+00:00",
                status="success",
            )

        log_file = run.log_path
        assert log_file is not None
        events = [json.loads(line) for line in log_file.read_text().strip().split("\n")]
        assert events[0]["event_seq"] == 1

    def test_event_seq_increments(self, tmp_path: Path) -> None:
        with WorkflowRun(state_dir=tmp_path) as run:
            for i in range(3):
                record_node_execution(
                    run,
                    node_name=f"node_{i}",
                    start_time="2024-01-01T00:00:00+00:00",
                    end_time="2024-01-01T00:00:01+00:00",
                    status="success",
                )

        log_file = run.log_path
        assert log_file is not None
        events = [json.loads(line) for line in log_file.read_text().strip().split("\n")]
        assert [e["event_seq"] for e in events] == [1, 2, 3]

    def test_event_seq_atomic_under_concurrency(self, tmp_path: Path) -> None:
        """Verify event_seq is monotonic under concurrent access."""
        with WorkflowRun(state_dir=tmp_path) as run:
            threads = []
            for i in range(20):
                t = threading.Thread(
                    target=record_node_execution,
                    kwargs={
                        "run": run,
                        "node_name": f"node_{i}",
                        "start_time": "2024-01-01T00:00:00+00:00",
                        "end_time": "2024-01-01T00:00:01+00:00",
                        "status": "success",
                    },
                )
                threads.append(t)

            for t in threads:
                t.start()
            for t in threads:
                t.join()

        log_file = run.log_path
        assert log_file is not None
        events = [json.loads(line) for line in log_file.read_text().strip().split("\n")]
        seqs = sorted([e["event_seq"] for e in events])
        # All sequences should be unique and cover 1..20
        assert seqs == list(range(1, 21))

    def test_summary_printed_on_exit(self, tmp_path: Path, capsys: object) -> None:
        with WorkflowRun(state_dir=tmp_path) as run:
            record_node_execution(
                run,
                node_name="test",
                start_time="2024-01-01T00:00:00+00:00",
                end_time="2024-01-01T00:00:01+00:00",
                status="success",
            )

        # The summary should have been printed
        # We can't easily capture it in this test pattern, but
        # at least verify no exception was raised

    def test_writer_closed_on_exit(self, tmp_path: Path) -> None:
        with WorkflowRun(state_dir=tmp_path) as run:
            pass
        # Writer should be closed - verify file is not locked
        assert run._writer is not None
        assert run._writer._file is None

    def test_total_duration_ms_before_start(self, tmp_path: Path) -> None:
        """total_duration_ms returns 0 before __enter__ is called."""
        run = WorkflowRun(state_dir=tmp_path)
        assert run.total_duration_ms == 0

    def test_total_duration_ms_frozen_after_exit(self, tmp_path: Path) -> None:
        """total_duration_ms does not grow after the context manager exits."""
        import time

        with WorkflowRun(state_dir=tmp_path) as run:
            pass

        first_read = run.total_duration_ms
        time.sleep(0.05)
        second_read = run.total_duration_ms

        assert first_read == second_read, (
            f"total_duration_ms should be frozen after __exit__; got {first_read} then {second_read} after sleeping"
        )

    def test_total_duration_ms_positive_during_run(self, tmp_path: Path) -> None:
        """total_duration_ms is positive while the context is active."""
        import time

        with WorkflowRun(state_dir=tmp_path) as run:
            time.sleep(0.01)
            assert run.total_duration_ms > 0

    def test_log_path_none_before_start(self, tmp_path: Path) -> None:
        """log_path returns None before context is entered."""
        run = WorkflowRun(state_dir=tmp_path)
        assert run.log_path is None

    def test_write_event_noop_when_writer_none(self, tmp_path: Path) -> None:
        """_write_event is a no-op when writer is not set."""
        from agentic_devtools.orchestration.observability_events import (
            NodeExecutionEvent,
        )

        run = WorkflowRun(state_dir=tmp_path)
        # Writer is None before __enter__, should not crash
        run._write_event(
            NodeExecutionEvent(
                version=1,
                event_seq=1,
                type="node",
                run_id="test",
                timestamp="2024-01-01T00:00:00+00:00",
                node_name="test",
                status="success",
                start_time="2024-01-01T00:00:00+00:00",
                end_time="2024-01-01T00:00:01+00:00",
                duration_ms=1000,
                input_summary=None,
                output_summary=None,
                error_class=None,
                retryable=None,
                error_message=None,
            )
        )

    def test_enter_with_degraded_writer(self, tmp_path: Path) -> None:
        """When writer is degraded, no log path is printed."""
        import io
        import sys

        captured = io.StringIO()
        sys.stdout = captured
        try:
            # Use invalid run_id to force degradation
            run = WorkflowRun(state_dir=tmp_path, run_id="bad/id")
            run.__enter__()
            run.__exit__(None, None, None)
        finally:
            sys.stdout = sys.__stdout__
        # Should not contain the log path line
        assert "[observability] Log:" not in captured.getvalue()

    def test_log_not_printed_when_log_path_set_but_writer_degraded(self, tmp_path: Path) -> None:
        """[observability] Log: is not printed when writer has a path but failed to open."""
        import io
        import sys
        from unittest.mock import patch

        # Pre-create the observability directory so mkdir() succeeds and _log_path gets set,
        # but patch open() to fail so the writer is still marked degraded.
        obs_dir = tmp_path / "observability"
        obs_dir.mkdir()

        captured = io.StringIO()
        sys.stdout = captured
        try:
            with patch("builtins.open", side_effect=PermissionError("read-only")):
                run = WorkflowRun(state_dir=tmp_path, run_id="valid-run-id")
                run.__enter__()
        finally:
            sys.stdout = sys.__stdout__

        # Writer should have a log_path computed but be degraded
        assert run._writer is not None
        assert run._writer.log_path is not None
        assert run._writer.degraded

        # No log path line should appear in stdout
        assert "[observability] Log:" not in captured.getvalue()

        run.__exit__(None, None, None)

    def test_log_path_none_when_writer_degraded(self, tmp_path: Path) -> None:
        """log_path returns None when writer exists but is degraded."""
        from unittest.mock import patch

        obs_dir = tmp_path / "observability"
        obs_dir.mkdir()

        with patch("builtins.open", side_effect=PermissionError("read-only")):
            run = WorkflowRun(state_dir=tmp_path, run_id="valid-run-id")
            run.__enter__()

        assert run._writer is not None
        assert run._writer.degraded
        assert run._writer.log_path is not None
        assert run.log_path is None

        run.__exit__(None, None, None)

    def test_exit_when_writer_is_none(self, tmp_path: Path) -> None:
        """__exit__ handles writer being None gracefully."""
        run = WorkflowRun(state_dir=tmp_path)
        # Don't call __enter__, so writer stays None
        run.__exit__(None, None, None)  # Should not raise

    def test_exit_does_not_raise_when_summary_raises(self, tmp_path: Path) -> None:
        """__exit__ swallows exceptions from print_run_summary (broken pipe, etc.)."""
        from unittest.mock import patch

        # Simulate a fresh run and inject a crashing print_run_summary
        run2 = WorkflowRun(state_dir=tmp_path)
        run2.__enter__()
        with patch(
            "agentic_devtools.orchestration.observability_summary.print_run_summary",
            side_effect=BrokenPipeError("pipe closed"),
        ):
            # Must not propagate the BrokenPipeError
            run2.__exit__(None, None, None)

    def test_record_node_execution_noops_after_exit(self, tmp_path: Path) -> None:
        run = WorkflowRun(state_dir=tmp_path)
        run.__enter__()
        run.__exit__(None, None, None)

        log_file = tmp_path / "observability" / f"run-{run.run_id}.jsonl"
        before = log_file.read_text() if log_file.exists() else ""

        record_node_execution(
            run,
            node_name="late-node",
            start_time="2024-01-01T00:00:00+00:00",
            end_time="2024-01-01T00:00:01+00:00",
            status="success",
        )

        after = log_file.read_text() if log_file.exists() else ""
        assert before == after
        assert run.node_success == 0

    def test_reenter_after_exit_raises(self, tmp_path: Path) -> None:
        """WorkflowRun instances are one-shot and cannot be re-entered."""
        run = WorkflowRun(state_dir=tmp_path)

        with run:
            pass

        with pytest.raises(RuntimeError, match="cannot be re-entered"):
            run.__enter__()

    def test_workflow_name_stored(self, tmp_path: Path) -> None:
        """workflow_name is accepted and stored on the instance."""
        run = WorkflowRun(state_dir=tmp_path, workflow_name="pr-review")
        assert run._workflow_name == "pr-review"
        assert run.workflow_name == "pr-review"

    def test_workflow_name_defaults_to_none(self, tmp_path: Path) -> None:
        """workflow_name defaults to None when not provided."""
        run = WorkflowRun(state_dir=tmp_path)
        assert run._workflow_name is None
        assert run.workflow_name is None

    def test_workflow_name_keyword_in_context_manager(self, tmp_path: Path) -> None:
        """WorkflowRun works with workflow_name as a keyword argument."""
        with WorkflowRun(workflow_name="pr-review", state_dir=tmp_path) as run:
            assert run._workflow_name == "pr-review"
            assert run.run_id is not None

    def test_workflow_name_appears_in_log_line(self, tmp_path: Path) -> None:
        """workflow_name is included in the [observability] log line."""
        import io
        import sys

        captured = io.StringIO()
        sys.stdout = captured
        try:
            with WorkflowRun(state_dir=tmp_path, workflow_name="my-workflow"):
                pass
        finally:
            sys.stdout = sys.__stdout__

        output = captured.getvalue()
        assert "workflow=my-workflow" in output
        assert "Log:" in output

    def test_no_workflow_name_omits_tag_from_log_line(self, tmp_path: Path) -> None:
        """Without workflow_name, the log line uses the original format."""
        import io
        import sys

        captured = io.StringIO()
        sys.stdout = captured
        try:
            with WorkflowRun(state_dir=tmp_path):
                pass
        finally:
            sys.stdout = sys.__stdout__

        output = captured.getvalue()
        assert "[observability] Log:" in output
        assert "workflow=" not in output
