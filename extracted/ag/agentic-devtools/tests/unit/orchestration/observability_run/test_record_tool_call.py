"""Tests for record_tool_call function."""

import json
import threading
from pathlib import Path
from unittest.mock import MagicMock

from agentic_devtools.orchestration.observability_run import (
    WorkflowRun,
    record_tool_call,
)


class TestRecordToolCall:
    """Tests for record_tool_call."""

    def _make_tool_result(
        self, *, success: bool = True, dry_run: bool = False, duration_ms: float = 100.0, output: object = None
    ) -> MagicMock:
        result = MagicMock()
        result.success = success
        result.dry_run = dry_run
        result.duration_ms = duration_ms
        result.output = output
        return result

    def _make_tool_def(self, *, mutating: bool = False) -> MagicMock:
        tool_def = MagicMock()
        tool_def.mutating = mutating
        return tool_def

    def test_successful_tool_call_event(self, tmp_path: Path) -> None:
        with WorkflowRun(state_dir=tmp_path) as run:
            record_tool_call(
                run,
                node_name="commit",
                tool_name="git_commit",
                input_params={"message": "feat: add feature"},
                tool_result=self._make_tool_result(success=True, duration_ms=150.0),
                tool_def=self._make_tool_def(mutating=True),
            )

        log_file = tmp_path / "observability" / f"run-{run.run_id}.jsonl"
        events = [json.loads(line) for line in log_file.read_text().strip().split("\n")]
        assert events[0]["type"] == "tool_call"
        assert events[0]["tool_name"] == "git_commit"
        assert events[0]["success"] is True
        assert events[0]["mutating"] is True
        assert events[0]["duration_ms"] == 150.0

    def test_failed_tool_call_has_error_class(self, tmp_path: Path) -> None:
        with WorkflowRun(state_dir=tmp_path) as run:
            record_tool_call(
                run,
                node_name="jira",
                tool_name="jira_add_comment",
                input_params={"comment": "Hello"},
                tool_result=self._make_tool_result(success=False, duration_ms=500.0),
                tool_def=self._make_tool_def(mutating=True),
            )

        log_file = tmp_path / "observability" / f"run-{run.run_id}.jsonl"
        events = [json.loads(line) for line in log_file.read_text().strip().split("\n")]
        assert events[0]["success"] is False
        assert events[0]["error_class"] == "tool"

    def test_dry_run_sourced_from_tool_result(self, tmp_path: Path) -> None:
        with WorkflowRun(state_dir=tmp_path) as run:
            record_tool_call(
                run,
                node_name="commit",
                tool_name="git_push",
                input_params={},
                tool_result=self._make_tool_result(dry_run=True),
                tool_def=self._make_tool_def(mutating=True),
            )

        log_file = tmp_path / "observability" / f"run-{run.run_id}.jsonl"
        events = [json.loads(line) for line in log_file.read_text().strip().split("\n")]
        assert events[0]["dry_run"] is True
        assert events[0]["mutating"] is True

    def test_mutating_sourced_from_tool_def(self, tmp_path: Path) -> None:
        with WorkflowRun(state_dir=tmp_path) as run:
            record_tool_call(
                run,
                node_name="read",
                tool_name="get_file",
                input_params={"path": "/tmp/file.txt"},
                tool_result=self._make_tool_result(),
                tool_def=self._make_tool_def(mutating=False),
            )

        log_file = tmp_path / "observability" / f"run-{run.run_id}.jsonl"
        events = [json.loads(line) for line in log_file.read_text().strip().split("\n")]
        assert events[0]["mutating"] is False

    def test_input_redaction_applied(self, tmp_path: Path) -> None:
        with WorkflowRun(state_dir=tmp_path) as run:
            record_tool_call(
                run,
                node_name="auth",
                tool_name="api_call",
                input_params={"password": "secret123", "url": "https://example.com"},
                tool_result=self._make_tool_result(),
                tool_def=self._make_tool_def(),
            )

        log_file = tmp_path / "observability" / f"run-{run.run_id}.jsonl"
        events = [json.loads(line) for line in log_file.read_text().strip().split("\n")]
        input_params = events[0]["input_params"]
        assert "secret123" not in str(input_params)

    def test_dry_run_only_when_mutating_and_dry_run_mode(self, tmp_path: Path) -> None:
        """dry_run: true only when ToolResult reports dry_run."""
        with WorkflowRun(state_dir=tmp_path) as run:
            # Non-mutating tool with dry_run=False
            record_tool_call(
                run,
                node_name="read",
                tool_name="get_status",
                input_params={},
                tool_result=self._make_tool_result(dry_run=False),
                tool_def=self._make_tool_def(mutating=False),
            )

        log_file = tmp_path / "observability" / f"run-{run.run_id}.jsonl"
        events = [json.loads(line) for line in log_file.read_text().strip().split("\n")]
        assert events[0]["dry_run"] is False

    def test_output_redaction_applied(self, tmp_path: Path) -> None:
        """tool_result.output is redacted before truncation."""
        with WorkflowRun(state_dir=tmp_path) as run:
            tool_result = self._make_tool_result(
                success=True,
                output={"token": "ghp_SUPERSECRET123", "status": "ok"},
            )
            record_tool_call(
                run,
                node_name="auth",
                tool_name="fetch_token",
                input_params={"url": "https://example.com"},
                tool_result=tool_result,
                tool_def=self._make_tool_def(),
            )

        log_file = tmp_path / "observability" / f"run-{run.run_id}.jsonl"
        events = [json.loads(line) for line in log_file.read_text().strip().split("\n")]
        result_summary = str(events[0].get("tool_result_summary", ""))
        assert "SUPERSECRET" not in result_summary

    def test_updates_tool_summary_stats(self, tmp_path: Path) -> None:
        with WorkflowRun(state_dir=tmp_path) as run:
            record_tool_call(
                run,
                node_name="commit",
                tool_name="git_push",
                input_params={},
                tool_result=self._make_tool_result(success=True, duration_ms=150.0),
                tool_def=self._make_tool_def(mutating=True),
            )
            record_tool_call(
                run,
                node_name="jira",
                tool_name="jira_comment",
                input_params={},
                tool_result=self._make_tool_result(success=False, duration_ms=350.0),
                tool_def=self._make_tool_def(mutating=True),
            )

            assert run.tool_call_count == 2
            assert run.tool_failures == 1
            assert run.total_tool_duration_ms == 500.0

    def test_stats_accumulate_correctly_under_concurrency(self, tmp_path: Path) -> None:
        """Tool counters are accurate when concurrent threads call record_tool_call."""
        n_threads = 20
        duration_each = 100.0

        with WorkflowRun(state_dir=tmp_path) as run:
            threads = []
            for i in range(n_threads):
                success = i % 2 == 0  # 10 success, 10 failure
                t = threading.Thread(
                    target=record_tool_call,
                    kwargs={
                        "run": run,
                        "node_name": f"node_{i}",
                        "tool_name": "some_tool",
                        "input_params": {},
                        "tool_result": self._make_tool_result(success=success, duration_ms=duration_each),
                        "tool_def": self._make_tool_def(mutating=True),
                    },
                )
                threads.append(t)

            for t in threads:
                t.start()
            for t in threads:
                t.join()

            assert run.tool_call_count == n_threads
            assert run.tool_failures == 10
            assert run.total_tool_duration_ms == n_threads * duration_each

    def test_none_duration_ms_coerced_to_zero(self, tmp_path: Path) -> None:
        """None duration_ms must not raise TypeError on stats accumulation."""
        tool_result = MagicMock()
        tool_result.success = True
        tool_result.dry_run = False
        tool_result.duration_ms = None  # problematic value
        tool_result.output = None

        with WorkflowRun(state_dir=tmp_path) as run:
            record_tool_call(
                run,
                node_name="node",
                tool_name="tool",
                input_params={},
                tool_result=tool_result,
                tool_def=self._make_tool_def(),
            )
            assert run.total_tool_duration_ms == 0.0

        log_file = tmp_path / "observability" / f"run-{run.run_id}.jsonl"
        events = [json.loads(line) for line in log_file.read_text().strip().split("\n")]
        assert events[0]["duration_ms"] == 0.0

    def test_noops_after_exit(self, tmp_path: Path) -> None:
        run = WorkflowRun(state_dir=tmp_path)
        run.__enter__()
        run.__exit__(None, None, None)

        log_file = tmp_path / "observability" / f"run-{run.run_id}.jsonl"
        before = log_file.read_text() if log_file.exists() else ""

        record_tool_call(
            run,
            node_name="commit",
            tool_name="git_commit",
            input_params={"message": "feat: add feature"},
            tool_result=self._make_tool_result(success=True, duration_ms=150.0),
            tool_def=self._make_tool_def(mutating=True),
        )

        after = log_file.read_text() if log_file.exists() else ""
        assert before == after
        assert run.tool_call_count == 0

    def test_string_duration_ms_coerced_to_zero(self, tmp_path: Path) -> None:
        """Non-numeric duration_ms must not raise TypeError on stats accumulation."""
        tool_result = MagicMock()
        tool_result.success = True
        tool_result.dry_run = False
        tool_result.duration_ms = "fast"  # non-numeric string
        tool_result.output = None

        with WorkflowRun(state_dir=tmp_path) as run:
            record_tool_call(
                run,
                node_name="node",
                tool_name="tool",
                input_params={},
                tool_result=tool_result,
                tool_def=self._make_tool_def(),
            )
            assert run.total_tool_duration_ms == 0.0

    def test_none_success_coerced_to_true(self, tmp_path: Path) -> None:
        """None success must not mark the call as failed."""
        tool_result = MagicMock()
        tool_result.success = None  # absent-equivalent value
        tool_result.dry_run = False
        tool_result.duration_ms = 50.0
        tool_result.output = None

        with WorkflowRun(state_dir=tmp_path) as run:
            record_tool_call(
                run,
                node_name="node",
                tool_name="tool",
                input_params={},
                tool_result=tool_result,
                tool_def=self._make_tool_def(),
            )
            assert run.tool_failures == 0

        log_file = tmp_path / "observability" / f"run-{run.run_id}.jsonl"
        events = [json.loads(line) for line in log_file.read_text().strip().split("\n")]
        assert events[0]["success"] is True
        assert events[0]["error_class"] is None

    def test_none_dry_run_and_mutating_coerced_to_false(self, tmp_path: Path) -> None:
        """None dry_run/mutating must not propagate as None into the event."""
        tool_result = MagicMock()
        tool_result.success = True
        tool_result.dry_run = None  # abnormal value
        tool_result.duration_ms = 10.0
        tool_result.output = None

        tool_def = MagicMock()
        tool_def.mutating = None  # abnormal value

        with WorkflowRun(state_dir=tmp_path) as run:
            record_tool_call(
                run,
                node_name="node",
                tool_name="tool",
                input_params={},
                tool_result=tool_result,
                tool_def=tool_def,
            )

        log_file = tmp_path / "observability" / f"run-{run.run_id}.jsonl"
        events = [json.loads(line) for line in log_file.read_text().strip().split("\n")]
        assert events[0]["dry_run"] is False
        assert events[0]["mutating"] is False

    def test_string_flag_values_fall_back_to_safe_defaults(self, tmp_path: Path) -> None:
        """Unexpected string flags must not be truthified via bool()."""
        tool_result = MagicMock()
        tool_result.success = "false"
        tool_result.dry_run = "false"
        tool_result.duration_ms = 10.0
        tool_result.output = None

        tool_def = MagicMock()
        tool_def.mutating = "false"

        with WorkflowRun(state_dir=tmp_path) as run:
            record_tool_call(
                run,
                node_name="node",
                tool_name="tool",
                input_params={},
                tool_result=tool_result,
                tool_def=tool_def,
            )
            assert run.tool_failures == 0

        log_file = tmp_path / "observability" / f"run-{run.run_id}.jsonl"
        events = [json.loads(line) for line in log_file.read_text().strip().split("\n")]
        assert events[0]["success"] is True
        assert events[0]["dry_run"] is False
        assert events[0]["mutating"] is False

    def test_truthy_string_success_still_falls_back_to_default(self, tmp_path: Path) -> None:
        """Even truthy string success values must not be treated as real booleans."""
        tool_result = MagicMock()
        tool_result.success = "true"
        tool_result.dry_run = False
        tool_result.duration_ms = 10.0
        tool_result.output = None

        with WorkflowRun(state_dir=tmp_path) as run:
            record_tool_call(
                run,
                node_name="node",
                tool_name="tool",
                input_params={},
                tool_result=tool_result,
                tool_def=self._make_tool_def(),
            )
            assert run.tool_failures == 0

        log_file = tmp_path / "observability" / f"run-{run.run_id}.jsonl"
        events = [json.loads(line) for line in log_file.read_text().strip().split("\n")]
        assert events[0]["success"] is True
        assert events[0]["error_class"] is None

    def test_bool_duration_ms_falls_back_to_zero(self, tmp_path: Path) -> None:
        """Boolean duration_ms must not be treated as a numeric duration."""
        tool_result = MagicMock()
        tool_result.success = True
        tool_result.dry_run = False
        tool_result.duration_ms = True
        tool_result.output = None

        with WorkflowRun(state_dir=tmp_path) as run:
            record_tool_call(
                run,
                node_name="node",
                tool_name="tool",
                input_params={},
                tool_result=tool_result,
                tool_def=self._make_tool_def(),
            )
            assert run.total_tool_duration_ms == 0.0

        log_file = tmp_path / "observability" / f"run-{run.run_id}.jsonl"
        events = [json.loads(line) for line in log_file.read_text().strip().split("\n")]
        assert events[0]["duration_ms"] == 0.0

    def test_false_duration_ms_falls_back_to_zero(self, tmp_path: Path) -> None:
        """False duration_ms must also be rejected as a boolean, not a number."""
        tool_result = MagicMock()
        tool_result.success = True
        tool_result.dry_run = False
        tool_result.duration_ms = False
        tool_result.output = None

        with WorkflowRun(state_dir=tmp_path) as run:
            record_tool_call(
                run,
                node_name="node",
                tool_name="tool",
                input_params={},
                tool_result=tool_result,
                tool_def=self._make_tool_def(),
            )
            assert run.total_tool_duration_ms == 0.0

        log_file = tmp_path / "observability" / f"run-{run.run_id}.jsonl"
        events = [json.loads(line) for line in log_file.read_text().strip().split("\n")]
        assert events[0]["duration_ms"] == 0.0

    def test_negative_duration_ms_is_clamped_to_zero(self, tmp_path: Path) -> None:
        """Negative duration_ms values must not reduce total elapsed tool time."""
        tool_result = MagicMock()
        tool_result.success = True
        tool_result.dry_run = False
        tool_result.duration_ms = -42.5
        tool_result.output = None

        with WorkflowRun(state_dir=tmp_path) as run:
            record_tool_call(
                run,
                node_name="node",
                tool_name="tool",
                input_params={},
                tool_result=tool_result,
                tool_def=self._make_tool_def(),
            )
            assert run.total_tool_duration_ms == 0.0

        log_file = tmp_path / "observability" / f"run-{run.run_id}.jsonl"
        events = [json.loads(line) for line in log_file.read_text().strip().split("\n")]
        assert events[0]["duration_ms"] == 0.0
