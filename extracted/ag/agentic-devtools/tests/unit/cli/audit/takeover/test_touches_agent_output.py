"""Tests for touches_agent_output()."""

from __future__ import annotations

from agentic_devtools.cli.audit.takeover import touches_agent_output


class TestTouchesAgentOutput:
    """Tests for the audit agent-output path detector."""

    def test_true_for_agent_output_path(self) -> None:
        assert touches_agent_output(["audit-batches/abc123/agent-output/specs/copilot-instructions.md"])

    def test_true_with_backslash_paths(self) -> None:
        assert touches_agent_output(["audit-batches\\abc123\\agent-output\\audit-summary-report.md"])

    def test_false_for_prefix_without_agent_output_segment(self) -> None:
        # Starts with the prefix but is not under an agent-output/ directory.
        assert not touches_agent_output(["audit-batches/abc123/batch-meta.json"])

    def test_false_for_unrelated_path(self) -> None:
        assert not touches_agent_output(["src/main.py"])

    def test_false_for_empty(self) -> None:
        assert not touches_agent_output([])
