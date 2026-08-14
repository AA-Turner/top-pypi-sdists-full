"""Tests for release attribution context in rollout HITL alerts."""

from __future__ import annotations

from typing import Any

import pytest

from airbyte_ops_mcp import slack_posting
from airbyte_ops_mcp.connector_ops.rollouts import autopilot
from airbyte_ops_mcp.connector_ops.rollouts._helpers import HealthGateResult
from airbyte_ops_mcp.connector_ops.rollouts.models import ConnectorRolloutRecord
from airbyte_ops_mcp.registry.release_attribution import (
    ReleaseAttribution,
    ReleaseAttributionLookupResult,
)
from airbyte_ops_mcp.registry.store import RegistryStore


def _rollout() -> ConnectorRolloutRecord:
    return ConnectorRolloutRecord(
        rollout_id="rollout-1",
        actor_definition_id="actor-1",
        state="in_progress",
        current_target_rollout_pct=25,
        rc_docker_image_tag="1.2.3",
        rc_docker_repository="airbyte/source-test",
    )


def _gate() -> HealthGateResult:
    return HealthGateResult(
        passed=False,
        reason="too many failures",
        failure_count=3,
        should_rollback=True,
    )


def _result(
    *,
    status: str = "found",
    lookup_path: str = "index",
    **kwargs: Any,
) -> ReleaseAttributionLookupResult:
    return ReleaseAttributionLookupResult(
        connector_name="source-test",
        version="1.2.3",
        status=status,
        lookup_path=lookup_path,
        **kwargs,
    )


@pytest.mark.parametrize(
    "result,contact,expected,absent",
    [
        pytest.param(
            _result(
                attribution=ReleaseAttribution(
                    pr_number=42,
                    pr_url="https://github.com/airbytehq/airbyte/pull/42",
                    attributed_to="engineer",
                    source="publish",
                )
            ),
            "<@U12345678>",
            ("PR 42", "<@U12345678>"),
            (),
            id="human_with_mention",
        ),
        pytest.param(
            _result(
                attribution=ReleaseAttribution(
                    pr_number=42,
                    attributed_to="unknown-engineer",
                    source="publish",
                )
            ),
            "unknown-engineer",
            ("Release contact: unknown-engineer",),
            ("<@",),
            id="roster_miss_plain_login",
        ),
        pytest.param(
            _result(
                attribution=ReleaseAttribution(
                    pr_number=42,
                    pr_author_login="release-bot[bot]",
                    pr_author_type="Bot",
                    source="publish",
                )
            ),
            "release-bot[bot]",
            ("Release author: `release-bot[bot]`",),
            ("<@",),
            id="bot_never_mentioned",
        ),
        pytest.param(
            _result(
                attribution=ReleaseAttribution(
                    pr_number=42,
                    pr_author_login="human-author",
                    pr_author_type="User",
                    source="publish",
                )
            ),
            "human-author",
            ("Release author: `human-author`",),
            ("<@",),
            id="human_without_attribution",
        ),
        pytest.param(
            _result(status="error", lookup_path="none", error="GCS unavailable"),
            "unused",
            (),
            (),
            id="lookup_error",
        ),
    ],
)
def test_release_context_scenarios(
    monkeypatch,
    result: ReleaseAttributionLookupResult,
    contact: str,
    expected: tuple[str, ...],
    absent: tuple[str, ...],
) -> None:
    captured: dict[str, RegistryStore] = {}

    def lookup(store, *args, **kwargs):
        captured["store"] = store
        return result

    monkeypatch.setattr(autopilot, "lookup_release_attribution", lookup)
    monkeypatch.setattr(autopilot, "format_github_login_contact", lambda _: contact)

    context = autopilot._release_context(
        "source-test",
        "1.2.3",
        store=RegistryStore.parse("coral:dev"),
    )

    for text in expected:
        assert text in context
    for text in absent:
        assert text not in context
    assert captured["store"] == RegistryStore.parse("coral:dev")


def test_public_github_contact_formatter_uses_roster_and_fallback(monkeypatch) -> None:
    monkeypatch.setattr(
        slack_posting,
        "fetch_roster",
        lambda: [{"github_handle": "engineer", "slack_id": "U12345678"}],
    )
    assert slack_posting.format_github_login_contact("engineer") == "<@U12345678>"
    assert slack_posting.format_github_login_contact("unknown") == "unknown"


def test_alert_is_sent_when_attribution_lookup_fails(monkeypatch) -> None:
    monkeypatch.setattr(
        autopilot,
        "lookup_release_attribution",
        lambda *args, **kwargs: _result(
            status="error",
            lookup_path="none",
            error="GCS unavailable",
        ),
    )
    sent: dict[str, str] = {}

    def capture(**kwargs: Any) -> None:
        sent.update(kwargs)

    monkeypatch.setattr(autopilot, "send_hitl_notification", capture)

    assert autopilot._send_failure_threshold_hitl(_rollout(), "1.2.3", _gate())
    assert "Release PR" not in sent["message"]
    assert "Rollout paused" in sent["message"]
