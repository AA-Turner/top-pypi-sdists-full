from dataclasses import replace
from unittest.mock import MagicMock

import pytest

from agentic_devtools.cli.ci.critique_adjudicator import build_critique_task_comment, build_critique_task_id_marker
from agentic_devtools.cli.ci.pipeline.actions.critique_task_binding import bind_dispatched_critique_task
from agentic_devtools.cli.ci.pipeline.models import ActionDecision
from agentic_devtools.cli.ci.pipeline.snapshot_models import PRStateSnapshot
from agentic_devtools.cli.shared.retry import ProviderRateLimitError


def _snapshot() -> PRStateSnapshot:
    return replace(PRStateSnapshot(pr_number=42, head_sha="head"), base_repo_full_name="owner/repo")


def test_bind_dispatched_critique_task_skips_missing_or_invalid_receipts() -> None:
    provider = MagicMock()

    assert (
        bind_dispatched_critique_task(
            provider,
            _snapshot(),
            None,
            "task:owner/repo:task-123",
            "dispatch_repair",
        )
        is None
    )
    result = bind_dispatched_critique_task(provider, _snapshot(), (77, 100, 1), 77, "dispatch_repair")

    assert result is not None
    assert result.decision is ActionDecision.FAILED
    provider.update_comment_as_pr_token.assert_not_called()


def test_bind_dispatched_critique_task_verifies_a_valid_receipt() -> None:
    marker_body = build_critique_task_comment(42, "head", 100, 1) + "\n" + build_critique_task_id_marker("task-123")
    provider = MagicMock()
    provider.find_comment.return_value = (77, marker_body)

    result = bind_dispatched_critique_task(
        provider,
        _snapshot(),
        (77, 100, 1),
        "task:owner/repo:task-123",
        "dispatch_repair",
    )

    assert result is None
    provider.update_comment_as_pr_token.assert_called_once_with(77, marker_body)


def test_bind_dispatched_critique_task_retries_a_failed_marker_write() -> None:
    marker_body = build_critique_task_comment(42, "head", 100, 1) + "\n" + build_critique_task_id_marker("task-123")
    provider = MagicMock()
    provider.update_comment_as_pr_token.side_effect = [RuntimeError("temporary write failure"), None]
    provider.find_comment.return_value = (77, marker_body)

    result = bind_dispatched_critique_task(
        provider,
        _snapshot(),
        (77, 100, 1),
        "task:owner/repo:task-123",
        "dispatch_repair",
    )

    assert result is None
    assert provider.update_comment_as_pr_token.call_count == 2


def test_bind_dispatched_critique_task_reports_persistent_write_failure() -> None:
    provider = MagicMock()
    provider.find_comment.return_value = None

    result = bind_dispatched_critique_task(
        provider,
        _snapshot(),
        (77, 100, 1),
        "task:owner/repo:task-123",
        "dispatch_repair",
    )

    assert result is not None
    assert result.decision is ActionDecision.FAILED
    assert provider.update_comment_as_pr_token.call_count == 2


@pytest.mark.parametrize("is_rate_limit", [True, False])
def test_bind_dispatched_critique_task_handles_rate_limit_errors(is_rate_limit: bool) -> None:
    provider = MagicMock()
    provider.update_comment_as_pr_token.side_effect = ProviderRateLimitError(
        provider="github",
        is_rate_limit=is_rate_limit,
    )

    if is_rate_limit:
        with pytest.raises(ProviderRateLimitError):
            bind_dispatched_critique_task(
                provider,
                _snapshot(),
                (77, 100, 1),
                "task:owner/repo:task-123",
                "dispatch_repair",
            )
        return

    result = bind_dispatched_critique_task(
        provider,
        _snapshot(),
        (77, 100, 1),
        "task:owner/repo:task-123",
        "dispatch_repair",
    )

    assert result is not None
    assert result.decision is ActionDecision.FAILED
