from unittest.mock import MagicMock, patch

import pytest

from agentic_devtools.cli.ci.pipeline.actions import critique_task_binding
from agentic_devtools.cli.ci.pipeline.models import ActionDecision, ActionResult
from agentic_devtools.cli.ci.pipeline.snapshot_models import PRStateSnapshot
from agentic_devtools.cli.shared.retry import ProviderRateLimitError


def test_record_receipt_and_bind_attempts_both_operations() -> None:
    ledger = MagicMock()
    provider = MagicMock()
    snapshot = PRStateSnapshot(pr_number=42, head_sha="head")

    with patch(
        "agentic_devtools.cli.ci.pipeline.actions.critique_task_binding.bind_dispatched_critique_task",
        return_value=None,
    ) as binder:
        result = critique_task_binding.record_receipt_and_bind_critique_task(
            ledger,
            provider,
            snapshot,
            None,
            "task:owner/repo:123",
            "dispatch_repair",
        )

    assert result == (None, None)
    ledger.record.assert_called_once_with("task:owner/repo:123")
    binder.assert_called_once_with(provider, snapshot, None, "task:owner/repo:123", "dispatch_repair")


def test_record_receipt_and_bind_preserves_record_failure_and_binds_receipt() -> None:
    failure = RuntimeError("receipt persistence failed")
    ledger = MagicMock()
    ledger.record.side_effect = failure
    binding_failure = ActionResult(name="dispatch_repair", decision=ActionDecision.FAILED, error="bind failed")
    provider = MagicMock()
    snapshot = PRStateSnapshot(pr_number=42, head_sha="head")

    with patch(
        "agentic_devtools.cli.ci.pipeline.actions.critique_task_binding.bind_dispatched_critique_task",
        return_value=binding_failure,
    ) as binder:
        result = critique_task_binding.record_receipt_and_bind_critique_task(
            ledger,
            provider,
            snapshot,
            (7, 100, 1),
            "task:owner/repo:123",
            "dispatch_repair",
        )

    assert result == (failure, binding_failure)
    binder.assert_called_once_with(provider, snapshot, (7, 100, 1), "task:owner/repo:123", "dispatch_repair")


def test_record_receipt_and_bind_suppresses_binding_rate_limit_when_requested() -> None:
    ledger = MagicMock()
    provider = MagicMock()
    provider.update_comment_as_pr_token.side_effect = ProviderRateLimitError(provider="github", is_rate_limit=True)
    snapshot = PRStateSnapshot(pr_number=42, head_sha="head", base_repo_full_name="owner/repo")

    result = critique_task_binding.record_receipt_and_bind_critique_task(
        ledger,
        provider,
        snapshot,
        (7, 100, 1),
        "task:owner/repo:123",
        "dispatch_repair",
        suppress_binding_errors=True,
    )

    assert result == (None, None)
    ledger.record.assert_called_once_with("task:owner/repo:123")
    assert provider.update_comment_as_pr_token.call_count == 1


def test_record_receipt_and_bind_suppresses_other_binding_errors_when_requested() -> None:
    ledger = MagicMock()
    provider = MagicMock()
    snapshot = PRStateSnapshot(pr_number=42, head_sha="head")
    binding_error = RuntimeError("binding failed")

    with patch(
        "agentic_devtools.cli.ci.pipeline.actions.critique_task_binding.bind_dispatched_critique_task",
        side_effect=binding_error,
    ):
        result = critique_task_binding.record_receipt_and_bind_critique_task(
            ledger,
            provider,
            snapshot,
            (7, 100, 1),
            "task:owner/repo:123",
            "dispatch_repair",
            suppress_binding_errors=True,
        )

    assert result == (None, None)


def test_record_receipt_and_bind_propagates_binding_errors_by_default() -> None:
    ledger = MagicMock()
    provider = MagicMock()
    snapshot = PRStateSnapshot(pr_number=42, head_sha="head")
    binding_error = RuntimeError("binding failed")

    with (
        patch(
            "agentic_devtools.cli.ci.pipeline.actions.critique_task_binding.bind_dispatched_critique_task",
            side_effect=binding_error,
        ),
        pytest.raises(RuntimeError, match="binding failed"),
    ):
        critique_task_binding.record_receipt_and_bind_critique_task(
            ledger,
            provider,
            snapshot,
            (7, 100, 1),
            "task:owner/repo:123",
            "dispatch_repair",
        )
