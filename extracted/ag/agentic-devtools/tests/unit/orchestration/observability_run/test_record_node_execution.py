"""Tests for record_node_execution function."""

import json
import threading
from pathlib import Path
from typing import Any

import pytest

from agentic_devtools.orchestration.observability_errors import ErrorClassification
from agentic_devtools.orchestration.observability_run import (
    WorkflowRun,
    record_node_execution,
)


class TestRecordNodeExecution:
    """Tests for record_node_execution."""

    def test_success_event_emitted(self, tmp_path: object) -> None:
        state_dir = Path(str(tmp_path))
        with WorkflowRun(state_dir=state_dir) as run:
            record_node_execution(
                run,
                node_name="fetch_issue",
                start_time="2024-01-01T00:00:00+00:00",
                end_time="2024-01-01T00:00:01+00:00",
                status="success",
                input_data={"issue_key": "PROJ-123"},
                output_data={"summary": "Issue fetched"},
            )

        log_file = state_dir / "observability" / f"run-{run.run_id}.jsonl"
        assert log_file.exists()
        events = [json.loads(line) for line in log_file.read_text().strip().split("\n")]
        assert len(events) == 1
        assert events[0]["type"] == "node"
        assert events[0]["status"] == "success"
        assert events[0]["node_name"] == "fetch_issue"
        assert events[0]["duration_ms"] == 1000

    def test_failure_event_with_error_classification(self, tmp_path: object) -> None:
        state_dir = Path(str(tmp_path))
        with WorkflowRun(state_dir=state_dir) as run:
            record_node_execution(
                run,
                node_name="analyze",
                start_time="2024-01-01T00:00:00+00:00",
                end_time="2024-01-01T00:00:02+00:00",
                status="failure",
                error=ConnectionError("Network down"),
            )

        log_file = state_dir / "observability" / f"run-{run.run_id}.jsonl"
        events = [json.loads(line) for line in log_file.read_text().strip().split("\n")]
        assert events[0]["status"] == "failure"
        assert events[0]["error_class"] == "transient"
        assert events[0]["retryable"] is True

    def test_skipped_event(self, tmp_path: object) -> None:
        state_dir = Path(str(tmp_path))
        with WorkflowRun(state_dir=state_dir) as run:
            ts = "2024-01-01T00:00:00+00:00"
            record_node_execution(
                run,
                node_name="optional_step",
                start_time=ts,
                end_time=ts,
                status="skipped",
            )

        log_file = state_dir / "observability" / f"run-{run.run_id}.jsonl"
        events = [json.loads(line) for line in log_file.read_text().strip().split("\n")]
        assert events[0]["status"] == "skipped"
        assert events[0]["duration_ms"] == 0

    def test_input_redaction_applied(self, tmp_path: object) -> None:
        state_dir = Path(str(tmp_path))
        with WorkflowRun(state_dir=state_dir) as run:
            record_node_execution(
                run,
                node_name="auth",
                start_time="2024-01-01T00:00:00+00:00",
                end_time="2024-01-01T00:00:01+00:00",
                status="success",
                input_data={"password": "secret123", "name": "test"},
            )

        log_file = state_dir / "observability" / f"run-{run.run_id}.jsonl"
        events = [json.loads(line) for line in log_file.read_text().strip().split("\n")]
        summary = events[0]["input_summary"]
        assert "secret123" not in str(summary)

    def test_summary_stats_updated(self, tmp_path: object) -> None:
        state_dir = Path(str(tmp_path))
        with WorkflowRun(state_dir=state_dir) as run:
            record_node_execution(
                run,
                node_name="n1",
                start_time="2024-01-01T00:00:00+00:00",
                end_time="2024-01-01T00:00:01+00:00",
                status="success",
            )
            record_node_execution(
                run,
                node_name="n2",
                start_time="2024-01-01T00:00:01+00:00",
                end_time="2024-01-01T00:00:02+00:00",
                status="failure",
                error=ValueError("bad"),
            )
            record_node_execution(
                run,
                node_name="n3",
                start_time="2024-01-01T00:00:02+00:00",
                end_time="2024-01-01T00:00:02+00:00",
                status="skipped",
            )
            assert run.node_success == 1
            assert run.node_failure == 1
            assert run.node_skipped == 1
            assert len(run.errors) == 1

    def test_stats_accumulate_correctly_under_concurrency(self, tmp_path: Path) -> None:
        """Node counters are accurate when concurrent threads call record_node_execution."""
        # 10 success, 10 failure, 10 skipped
        statuses = ["success"] * 10 + ["failure"] * 10 + ["skipped"] * 10

        with WorkflowRun(state_dir=tmp_path) as run:
            threads = []
            for i, status in enumerate(statuses):
                kwargs: dict[str, Any] = {
                    "run": run,
                    "node_name": f"node_{i}",
                    "start_time": "2024-01-01T00:00:00+00:00",
                    "end_time": "2024-01-01T00:00:01+00:00",
                    "status": status,
                }
                if status == "failure":
                    kwargs["error"] = ValueError(f"error_{i}")
                t = threading.Thread(target=record_node_execution, kwargs=kwargs)
                threads.append(t)

            for t in threads:
                t.start()
            for t in threads:
                t.join()

            assert run.node_success == 10
            assert run.node_failure == 10
            assert run.node_skipped == 10
            assert len(run.errors) == 10

    def test_unknown_status_does_not_increment_any_counter(self, tmp_path: Path) -> None:
        """Unknown status values do not change the node counters."""
        with WorkflowRun(state_dir=tmp_path) as run:
            record_node_execution(
                run,
                node_name="n1",
                start_time="2024-01-01T00:00:00+00:00",
                end_time="2024-01-01T00:00:01+00:00",
                status="unknown_status",
            )
            assert run.node_success == 0
            assert run.node_failure == 0
            assert run.node_skipped == 0

    def test_error_source_llm_routes_to_llm_class(self, tmp_path: object) -> None:
        """error_source='llm' causes non-transient failures to be classified as 'llm'."""
        state_dir = Path(str(tmp_path))
        with WorkflowRun(state_dir=state_dir) as run:
            record_node_execution(
                run,
                node_name="generate",
                start_time="2024-01-01T00:00:00+00:00",
                end_time="2024-01-01T00:00:01+00:00",
                status="failure",
                error=ValueError("malformed output"),
                error_source="llm",
            )

        log_file = state_dir / "observability" / f"run-{run.run_id}.jsonl"
        events = [json.loads(line) for line in log_file.read_text().strip().split("\n")]
        assert events[0]["error_class"] == "llm"
        assert events[0]["retryable"] is True

    def test_error_source_tool_routes_to_tool_class(self, tmp_path: object) -> None:
        """error_source='tool' causes non-transient failures to be classified as 'tool'."""
        state_dir = Path(str(tmp_path))
        with WorkflowRun(state_dir=state_dir) as run:
            record_node_execution(
                run,
                node_name="exec_tool",
                start_time="2024-01-01T00:00:00+00:00",
                end_time="2024-01-01T00:00:01+00:00",
                status="failure",
                error=RuntimeError("tool failed"),
                error_source="tool",
            )

        log_file = state_dir / "observability" / f"run-{run.run_id}.jsonl"
        events = [json.loads(line) for line in log_file.read_text().strip().split("\n")]
        assert events[0]["error_class"] == "tool"
        assert events[0]["retryable"] is True

    def test_no_error_source_defaults_to_permanent_for_non_transient(self, tmp_path: object) -> None:
        """Without error_source, a non-transient error defaults to 'permanent'."""
        state_dir = Path(str(tmp_path))
        with WorkflowRun(state_dir=state_dir) as run:
            record_node_execution(
                run,
                node_name="step",
                start_time="2024-01-01T00:00:00+00:00",
                end_time="2024-01-01T00:00:01+00:00",
                status="failure",
                error=ValueError("bad input"),
            )

        log_file = state_dir / "observability" / f"run-{run.run_id}.jsonl"
        events = [json.loads(line) for line in log_file.read_text().strip().split("\n")]
        assert events[0]["error_class"] == "permanent"
        assert events[0]["retryable"] is False

    def test_failure_error_message_is_redacted_before_logging(self, tmp_path: Path) -> None:
        token = "ghp_SUPERSECRET12345"
        state_dir = tmp_path
        with WorkflowRun(state_dir=state_dir) as run:
            record_node_execution(
                run,
                node_name="fetch",
                start_time="2024-01-01T00:00:00+00:00",
                end_time="2024-01-01T00:00:01+00:00",
                status="failure",
                error=RuntimeError(f"request failed: token={token}"),
            )

            assert len(run.errors) == 1
            assert token not in run.errors[0]["message"]
            assert run.errors[0]["message"] == "[REDACTED]"

        log_file = state_dir / "observability" / f"run-{run.run_id}.jsonl"
        events = [json.loads(line) for line in log_file.read_text().strip().split("\n")]
        assert events[0]["type"] == "node"
        assert events[0]["status"] == "failure"
        assert token not in str(events[0]["error_message"])
        assert events[0]["error_message"] == "[REDACTED]"

    def test_fallback_error_message_is_redacted(
        self,
        monkeypatch: pytest.MonkeyPatch,
        tmp_path: Path,
    ) -> None:
        state_dir = tmp_path
        secret = "prefix ghs_exampletoken"
        with WorkflowRun(state_dir=state_dir) as run:

            def _classify(_error: BaseException, _context: object = None) -> ErrorClassification:
                return ErrorClassification(error_class="tool", retryable=True, message="")

            monkeypatch.setattr(
                run._classifier,
                "classify",
                _classify,
            )
            record_node_execution(
                run,
                node_name="execute",
                start_time="2024-01-01T00:00:00+00:00",
                end_time="2024-01-01T00:00:01+00:00",
                status="failure",
                error=RuntimeError(secret),
            )

            assert len(run.errors) == 1
            assert secret not in run.errors[0]["message"]
            assert run.errors[0]["message"] == "[REDACTED]"

        # The JSONL event must also carry the redacted fallback, not an empty string.
        log_file = state_dir / "observability" / f"run-{run.run_id}.jsonl"
        events = [json.loads(line) for line in log_file.read_text().strip().split("\n")]
        assert events[0]["type"] == "node"
        assert events[0]["status"] == "failure"
        assert events[0]["error_message"] == "[REDACTED]"

    def test_compat_short_signature_supports_duration_and_summary_aliases(
        self,
        tmp_path: Path,
    ) -> None:
        """Public shorthand args are accepted for backward-compatible usage snippets."""
        with WorkflowRun(state_dir=tmp_path) as run:
            record_node_execution(
                run,
                node_name="fetch_diff",
                status="success",
                duration_ms=342,
                inputs_summary={"pr_id": 123},
                outputs_summary={"files": 7},
            )

            assert run.node_success == 1

        log_file = tmp_path / "observability" / f"run-{run.run_id}.jsonl"
        events = [json.loads(line) for line in log_file.read_text().strip().split("\n")]
        assert events[0]["duration_ms"] == 342
        assert events[0]["input_summary"] == {"pr_id": 123}
        assert events[0]["output_summary"] == {"files": 7}
