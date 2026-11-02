"""Integration test for full workflow lifecycle."""

import json
from pathlib import Path
from unittest.mock import MagicMock

from agentic_devtools.orchestration.observability_run import (
    WorkflowRun,
    record_llm_call,
    record_node_execution,
    record_tool_call,
)


class TestWorkflowRunIntegration:
    """Integration tests verifying full workflow lifecycle."""

    def test_full_lifecycle(self, tmp_path: Path) -> None:
        """Start → node → LLM → tool → end → JSONL output + summary."""
        tool_result = MagicMock()
        tool_result.success = True
        tool_result.dry_run = False
        tool_result.duration_ms = 200.0
        tool_result.output = "Committed"

        tool_def = MagicMock()
        tool_def.mutating = True

        with WorkflowRun(state_dir=tmp_path) as run:
            # Record a node execution
            record_node_execution(
                run,
                node_name="fetch_issue",
                start_time="2024-01-01T00:00:00+00:00",
                end_time="2024-01-01T00:00:01+00:00",
                status="success",
                input_data={"key": "PROJ-123"},
                output_data={"summary": "Bug fix needed"},
            )

            # Record an LLM call
            record_llm_call(
                run,
                node_name="analyze",
                node_type="review",
                model="gpt-4o",
                input_tokens=2000,
                output_tokens=1000,
                latency_ms=3000,
                validation_result="pass",
            )

            # Record a tool call
            record_tool_call(
                run,
                node_name="commit",
                tool_name="git_commit",
                input_params={"message": "fix: resolve bug"},
                tool_result=tool_result,
                tool_def=tool_def,
            )

        # Verify JSONL output
        log_file = tmp_path / "observability" / f"run-{run.run_id}.jsonl"
        assert log_file.exists()

        events = [json.loads(line) for line in log_file.read_text().strip().split("\n")]
        assert len(events) == 3

        # Verify event types
        assert events[0]["type"] == "node"
        assert events[1]["type"] == "llm_call"
        assert events[2]["type"] == "tool_call"

        # Verify monotonic event_seq
        assert events[0]["event_seq"] == 1
        assert events[1]["event_seq"] == 2
        assert events[2]["event_seq"] == 3

        # Verify run_id consistency
        assert all(e["run_id"] == run.run_id for e in events)

        # Verify summary stats
        assert run.node_success == 1
        assert run.llm_call_count == 1
        assert run.total_input_tokens == 2000
        assert run.total_output_tokens == 1000
