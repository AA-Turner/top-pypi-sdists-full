# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Tests for the Rollout AutoPilot Slack audit output."""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from airbyte_ops_mcp.connector_ops.rollouts import audit
from airbyte_ops_mcp.connector_ops.rollouts.models import (
    AutopilotAction,
    AutopilotResult,
)
from airbyte_ops_mcp.slack_posting import SlackPostResult


def _entry(
    *, message: str, action: str = "test", tier: str = "TIER_2"
) -> AutopilotAction:
    """Build a representative AutoPilot result entry."""
    return AutopilotAction(
        rollout_id="rollout-1",
        actor_definition_id="actor-1",
        connector_name="source-faker",
        rc_version="1.2.3",
        action=action,
        success=action == "advance",
        message=message,
        tier=tier,
    )


@pytest.mark.unit
def test_post_autopilot_audit_posts_parent_and_thread(monkeypatch) -> None:
    """Audit output includes actionable entries but omits skipped entries."""
    result = AutopilotResult(command="auto-advance", dry_run=False)
    result.actions.append(_entry(message="Advanced to 50%", action="advance"))
    result.errors.append(_entry(message="Cloud API failed", action="advance"))
    result.warnings.append(_entry(message="Low eligible actor count"))
    result.holds.append(_entry(message="Health gate not passed"))
    result.skipped.append(_entry(message="Already at target percentage"))
    parent = SlackPostResult(channel_id="C123", ts="123.456")
    post_parent = MagicMock(return_value=parent)
    post_reply = MagicMock()
    monkeypatch.setenv("SLACK_CHANNEL_ROLLOUT_AUDIT", "C123")
    monkeypatch.setenv("SLACK_BOT_TOKEN_HITL", "xoxb-test")
    monkeypatch.setenv("GITHUB_SERVER_URL", "https://github.example.com")
    monkeypatch.setenv("GITHUB_REPOSITORY", "airbyte/example")
    monkeypatch.setenv("GITHUB_RUN_ID", "1234")
    monkeypatch.setattr(audit, "post_channel_message", post_parent)
    monkeypatch.setattr(audit, "post_thread_reply", post_reply)

    audit.post_autopilot_audit(result)

    post_parent.assert_called_once()
    parent_text = post_parent.call_args.args[1]
    assert "auto-advance" in parent_text
    assert (
        "<https://github.example.com/airbyte/example/actions/runs/1234|"
        "View GitHub Actions run>"
    ) in parent_text
    post_reply.assert_called_once()
    detail_text = post_reply.call_args.args[2]
    assert "Advanced to 50%" in detail_text
    assert "Cloud API failed" in detail_text
    assert "Low eligible actor count" in detail_text
    assert "Health gate not passed" in detail_text
    assert "Already at target percentage" not in detail_text


@pytest.mark.unit
@pytest.mark.parametrize(
    ("dry_run", "skipped_only"),
    [
        pytest.param(False, True, id="nothing_audit_worthy"),
        pytest.param(True, False, id="dry_run"),
    ],
)
def test_post_autopilot_audit_no_ops_for_non_audited_results(
    monkeypatch, dry_run: bool, skipped_only: bool
) -> None:
    """Routine and dry-run passes do not post."""
    result = AutopilotResult(command="auto-start", dry_run=dry_run)
    if skipped_only:
        result.skipped.append(_entry(message="autoStart is false"))
    else:
        result.actions.append(_entry(message="Would start rollout", action="start"))
    post_parent = MagicMock()
    monkeypatch.setenv("SLACK_CHANNEL_ROLLOUT_AUDIT", "C123")
    monkeypatch.setenv("SLACK_BOT_TOKEN_HITL", "xoxb-test")
    monkeypatch.setattr(audit, "post_channel_message", post_parent)

    audit.post_autopilot_audit(result)

    post_parent.assert_not_called()


@pytest.mark.unit
@pytest.mark.parametrize(
    ("category", "message"),
    [
        pytest.param("holds", "Health gate not passed", id="hold_only"),
        pytest.param("errors", "Cloud API failed", id="error_only"),
    ],
)
def test_post_autopilot_audit_no_ops_without_actions(
    monkeypatch, category: str, message: str
) -> None:
    """Passes without actions do not post, regardless of other entries."""
    result = AutopilotResult(command="auto-advance", dry_run=False)
    getattr(result, category).append(_entry(message=message))
    post_parent = MagicMock()
    monkeypatch.setenv("SLACK_CHANNEL_ROLLOUT_AUDIT", "C123")
    monkeypatch.setenv("SLACK_BOT_TOKEN_HITL", "xoxb-test")
    monkeypatch.setattr(audit, "post_channel_message", post_parent)

    audit.post_autopilot_audit(result)

    post_parent.assert_not_called()


@pytest.mark.unit
@pytest.mark.parametrize(
    ("configured_channel", "expected_channel"),
    [
        pytest.param(None, "C0BRZHL7P41", id="default_when_unset"),
        pytest.param("", "C0BRZHL7P41", id="default_when_empty"),
        pytest.param("   ", "C0BRZHL7P41", id="default_when_whitespace"),
        pytest.param("C123", "C123", id="explicit_override"),
    ],
)
def test_post_autopilot_audit_uses_default_or_override_channel(
    monkeypatch, configured_channel: str | None, expected_channel: str
) -> None:
    """The audit uses the default channel unless explicitly overridden."""
    result = AutopilotResult(command="auto-close", dry_run=False)
    result.actions.append(_entry(message="Closed obsolete rollout", action="close"))
    post_parent = MagicMock(
        return_value=SlackPostResult(channel_id=expected_channel, ts="123.456")
    )
    post_reply = MagicMock()
    if configured_channel is None:
        monkeypatch.delenv("SLACK_CHANNEL_ROLLOUT_AUDIT", raising=False)
    else:
        monkeypatch.setenv("SLACK_CHANNEL_ROLLOUT_AUDIT", configured_channel)
    monkeypatch.setenv("SLACK_BOT_TOKEN_HITL", "xoxb-test")
    monkeypatch.setattr(audit, "post_channel_message", post_parent)
    monkeypatch.setattr(audit, "post_thread_reply", post_reply)

    audit.post_autopilot_audit(result)

    post_parent.assert_called_once()
    assert post_parent.call_args.args[0] == expected_channel
    post_reply.assert_called_once()


@pytest.mark.unit
def test_post_autopilot_audit_no_ops_without_token(monkeypatch) -> None:
    """The audit remains disabled without Slack credentials."""
    result = AutopilotResult(command="auto-close", dry_run=False)
    result.actions.append(_entry(message="Closed obsolete rollout", action="close"))
    post_parent = MagicMock()
    monkeypatch.setenv("SLACK_CHANNEL_ROLLOUT_AUDIT", "C123")
    monkeypatch.delenv("SLACK_BOT_TOKEN_HITL", raising=False)
    monkeypatch.delenv("SLACK_HYDRA_BOT_TOKEN", raising=False)
    monkeypatch.delenv("SLACK_BOT_TOKEN_AIRBYTE_TEAM", raising=False)
    monkeypatch.delenv("SLACK_BOT_TOKEN", raising=False)
    monkeypatch.setattr(audit, "post_channel_message", post_parent)

    audit.post_autopilot_audit(result)

    post_parent.assert_not_called()


@pytest.mark.unit
def test_post_autopilot_audit_swallows_slack_failure(monkeypatch) -> None:
    """A Slack failure is logged and does not escape the presentation layer."""
    result = AutopilotResult(command="auto-promote", dry_run=False)
    result.actions.append(_entry(message="Promoted rollout", action="promote"))
    result.holds.append(_entry(message="Health gate not passed"))
    monkeypatch.setenv("SLACK_CHANNEL_ROLLOUT_AUDIT", "C123")
    monkeypatch.setenv("SLACK_BOT_TOKEN_HITL", "xoxb-test")
    monkeypatch.setattr(
        audit,
        "post_channel_message",
        MagicMock(side_effect=RuntimeError("Slack unavailable")),
    )

    audit.post_autopilot_audit(result)
