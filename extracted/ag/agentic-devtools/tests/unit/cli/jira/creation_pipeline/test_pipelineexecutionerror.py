"""Tests for ``PipelineExecutionError`` (T047).

Covers structured-field storage, actionable operation identification in the
message, and credential redaction (NFR-004).  Failure-propagation tests for
``_create_issue_operations`` live in ``test__create_issue_operations.py``
and for ``_blocking_operations`` in ``test__blocking_operations.py``.
"""

from __future__ import annotations

from agentic_devtools.cli.jira.creation_pipeline import (
    OperationPlan,
    PipelineExecutionError,
)


class TestPipelineExecutionErrorAttributes:
    def test_stores_all_structured_fields(self):
        plan = OperationPlan(operations=(), dry_run=False, check_existing=False)
        cause = RuntimeError("adapter down")
        err = PipelineExecutionError(
            cause=cause,
            operation_type="create_issue",
            refs=("s1",),
            stage="create_issue",
            created_result=None,
            partial_plan=plan,
        )
        assert err.cause is cause
        assert err.operation_type == "create_issue"
        assert err.refs == ("s1",)
        assert err.stage == "create_issue"
        assert err.created_result is None
        assert err.partial_plan is plan

    def test_message_identifies_operation_and_refs(self):
        plan = OperationPlan(operations=(), dry_run=False, check_existing=False)
        err = PipelineExecutionError(
            cause=RuntimeError("boom"),
            operation_type="add_blocked_by",
            refs=("s1", "s2"),
            stage="add_blocked_by",
            created_result=None,
            partial_plan=plan,
        )
        assert "add_blocked_by" in err.message
        assert "s1" in err.message and "s2" in err.message

    def test_message_redacts_credentials(self):
        plan = OperationPlan(operations=(), dry_run=False, check_existing=False)
        secret = "ghp_" + "A" * 36
        err = PipelineExecutionError(
            cause=RuntimeError(f"auth failed with token {secret}"),
            operation_type="create_issue",
            refs=("e1",),
            stage="create_issue",
            created_result=None,
            partial_plan=plan,
        )
        assert secret not in err.message
        assert "[REDACTED]" in err.message
