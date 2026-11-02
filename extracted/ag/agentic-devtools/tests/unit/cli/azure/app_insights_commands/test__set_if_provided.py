"""Tests for _set_if_provided."""

from agentic_devtools.cli.azure import app_insights_commands


def test_sets_state_only_when_value_is_provided(monkeypatch):
    calls = []
    monkeypatch.setattr(app_insights_commands, "set_value", lambda key, value: calls.append((key, value)))

    app_insights_commands._set_if_provided("azure.environment", None)
    app_insights_commands._set_if_provided("azure.environment", "DEV")

    assert calls == [("azure.environment", "DEV")]
