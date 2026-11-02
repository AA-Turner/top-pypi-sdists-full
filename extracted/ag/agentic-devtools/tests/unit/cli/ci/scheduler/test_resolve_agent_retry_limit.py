"""Tests for resolve_agent_retry_limit."""

from agentic_devtools.cli.ci.scheduler import resolve_agent_retry_limit


def test_defaults_and_clamps_retry_limit(monkeypatch) -> None:
    monkeypatch.delenv("AI_PR_LOOP_AGENT_RETRY_LIMIT", raising=False)
    assert resolve_agent_retry_limit() == 2
    monkeypatch.setenv("AI_PR_LOOP_AGENT_RETRY_LIMIT", "0")
    assert resolve_agent_retry_limit() == 0
    monkeypatch.setenv("AI_PR_LOOP_AGENT_RETRY_LIMIT", "99")
    assert resolve_agent_retry_limit() == 5
    monkeypatch.setenv("AI_PR_LOOP_AGENT_RETRY_LIMIT", "invalid")
    assert resolve_agent_retry_limit() == 2
