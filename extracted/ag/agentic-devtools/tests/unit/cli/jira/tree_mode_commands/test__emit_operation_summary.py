"""Tests for ``_emit_operation_summary``."""

from __future__ import annotations

import json

from agentic_devtools.adapters.operation_plan import OperationDescriptor, OperationPlan
from agentic_devtools.cli.jira.tree_mode_commands import _emit_operation_summary


class TestEmitOperationSummary:
    """_emit_operation_summary writes the execution summary as one JSON line."""

    def test_emits_summary_event_line(self, capsys) -> None:
        plan = OperationPlan(
            operations=(
                OperationDescriptor(
                    operation_type="create_issue",
                    orchestration_key="k1",
                    refs=("e1",),
                    status="created",
                ),
                OperationDescriptor(
                    operation_type="create_issue",
                    orchestration_key="k2",
                    refs=("f1",),
                    status="existing",
                ),
            ),
            dry_run=False,
            check_existing=False,
        )

        _emit_operation_summary(plan)

        payload = json.loads(capsys.readouterr().out)
        assert payload["event"] == "create_epic.summary"
        assert payload["created_issues"] == 1
        assert payload["skipped_issues"] == 1
        assert payload["total"] == 2
