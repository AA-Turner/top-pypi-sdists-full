"""Tests for _session_state_from_events."""

from unittest.mock import MagicMock

import pytest

from agentic_devtools.cli.ci.models import IssueEvent
from agentic_devtools.cli.ci.pipeline.session_detector import SessionOutcome, _session_state_from_events
from agentic_devtools.cli.shared.retry import ProviderRateLimitError


def test_maps_latest_session_event() -> None:
    provider = MagicMock()
    provider.list_pr_issue_events.return_value = [
        IssueEvent(1, "copilot_work_started", "2026-01-01T00:00:00Z"),
        IssueEvent(2, "copilot_work_finished_failure", "2026-01-01T00:01:00Z"),
    ]
    assert _session_state_from_events(provider, 4).outcome is SessionOutcome.FAILED


def test_reports_unknown_when_event_inventory_is_unusable() -> None:
    provider = MagicMock()
    provider.list_pr_issue_events.return_value = None
    assert _session_state_from_events(provider, 4).outcome is SessionOutcome.UNKNOWN


def test_reports_unknown_when_event_lookup_raises() -> None:
    provider = MagicMock()
    provider.list_pr_issue_events.side_effect = RuntimeError("unavailable")
    assert _session_state_from_events(provider, 4).outcome is SessionOutcome.UNKNOWN


def test_reraises_rate_limit_when_event_lookup_fails() -> None:
    provider = MagicMock()
    provider.list_pr_issue_events.side_effect = ProviderRateLimitError(provider="github", is_rate_limit=True)

    with pytest.raises(ProviderRateLimitError):
        _session_state_from_events(provider, 4)


def test_returns_none_when_events_have_no_valid_copilot_session_ids() -> None:
    provider = MagicMock()
    provider.list_pr_issue_events.return_value = [
        IssueEvent(True, "copilot_work_started", "2026-01-01T00:00:00Z"),
        IssueEvent(1, "labeled", "2026-01-01T00:01:00Z"),
    ]
    assert _session_state_from_events(provider, 4).outcome is SessionOutcome.NONE
