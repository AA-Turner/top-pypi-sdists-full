from unittest.mock import Mock

import pytest

from agentic_devtools.cli.ci.reconciliation.wp3 import IssueEffectCoordinator


def test_deduplicates_issue_and_recovers_reply_before_resolve() -> None:
    provider = Mock()
    provider.find_followup_issue.return_value = 42
    provider.find_thread_reply.side_effect = [None, 99]
    coordinator = IssueEffectCoordinator(provider)
    kwargs = dict(
        finding_id="finding",
        thread_id="thread",
        pr_url="https://github.com/o/r/pull/1",
        title="follow up",
        body="details",
        marker="wp3-marker",
    )
    first = coordinator.defer(**kwargs)
    second = coordinator.defer(**kwargs)
    assert first == second
    provider.create_followup_issue.assert_not_called()
    provider.post_thread_reply.assert_called_once()
    assert provider.resolve_thread.call_count == 2


def test_creates_issue_and_requires_capabilities() -> None:
    provider = Mock()
    provider.find_followup_issue.return_value = None
    provider.create_followup_issue.return_value = 7
    provider.find_thread_reply.return_value = 3
    coordinator = IssueEffectCoordinator(provider)
    receipt = coordinator.defer(finding_id="f", thread_id="t", pr_url="url", title="title", body="body", marker="m")
    assert receipt.remote_id == 7
    provider.create_followup_issue.assert_called_once()
    provider.post_thread_reply.assert_not_called()
    assert coordinator.receipt(receipt.effect_id) == receipt
    assert coordinator.receipt("unknown") is None
    with pytest.raises(ValueError):
        IssueEffectCoordinator(object())  # type: ignore[arg-type]
    with pytest.raises(ValueError):
        coordinator.effect_id("", "t")
