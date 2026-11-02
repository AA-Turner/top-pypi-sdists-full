from unittest.mock import MagicMock

import pytest

from agentic_devtools.cli.ci.models import AgentTaskInventory, AgentTaskLifecycle, AgentTaskSessionLifecycle
from agentic_devtools.cli.ci.pipeline.session_detector import _read_lifecycle_clocks
from agentic_devtools.cli.shared.retry import ProviderRateLimitError, RetryableError


def test_empty_inventory_needs_no_clocks() -> None:
    provider = MagicMock()
    assert _read_lifecycle_clocks(provider, 7, AgentTaskInventory(()), "", "") == {}
    provider.get_agent_task_first_observed_at.assert_not_called()


@pytest.mark.parametrize("clock", ["2026-10-16T00:00:00Z", None, "", 42])
def test_missing_task_and_session_clocks_accept_only_nonempty_strings(clock: object) -> None:
    provider = MagicMock()
    provider.get_agent_task_first_observed_at.return_value = clock
    task = AgentTaskLifecycle(
        task_id="task",
        repository="org/repo",
        pr_number=7,
        head_branch="",
        state="running",
        created_at="",
        sessions=(AgentTaskSessionLifecycle(session_id="session", state="running"),),
    )
    result = _read_lifecycle_clocks(provider, 7, AgentTaskInventory((task,)), "head", "sha")
    assert result == ({"task": {"task": clock, "session": clock}} if isinstance(clock, str) and clock else {})


def test_retryable_clock_cooldown_preserves_metadata() -> None:
    provider = MagicMock()
    provider.get_agent_task_first_observed_at.side_effect = RetryableError(
        provider="github", credential_identity="reader", retry_after=12, is_rate_limit=True
    )
    task = AgentTaskLifecycle(
        task_id="task", repository="org/repo", pr_number=7, head_branch="", state="running", created_at=""
    )
    with pytest.raises(ProviderRateLimitError) as caught:
        _read_lifecycle_clocks(provider, 7, AgentTaskInventory((task,)), "", "")
    assert caught.value.credential_identity == "reader"
    assert caught.value.retry_after_seconds == 12
