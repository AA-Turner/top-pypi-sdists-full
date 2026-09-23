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
from airbyte_ops_mcp.slack_posting import SlackPostResult

_POSTED = SlackPostResult(channel_id="C0HITL", ts="1789000000.000001")


def _rollout(connector_name: str = "source-test") -> ConnectorRolloutRecord:
    return ConnectorRolloutRecord(
        rollout_id="rollout-1",
        actor_definition_id="actor-1",
        state="in_progress",
        current_target_rollout_pct=25,
        rc_docker_image_tag="1.2.3",
        rc_docker_repository=f"airbyte/{connector_name}",
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


def _capture_alert(monkeypatch) -> dict[str, Any]:
    sent: dict[str, Any] = {}

    def capture(**kwargs: Any) -> SlackPostResult:
        sent.update(kwargs)
        return _POSTED

    monkeypatch.setattr(autopilot, "send_hitl_notification", capture)
    return sent


def test_airbyte_human_author_is_targeted_and_hydra_cc(monkeypatch) -> None:
    monkeypatch.setattr(
        autopilot,
        "lookup_release_attribution",
        lambda *args, **kwargs: _result(
            attribution=ReleaseAttribution(
                pr_number=42,
                pr_url="https://github.com/airbytehq/airbyte/pull/42",
                pr_author_login="sunil-kuruba",
                pr_author_type="User",
                pr_author_association="CONTRIBUTOR",
                source="publish",
            )
        ),
    )
    monkeypatch.setattr(
        autopilot,
        "resolve_airbyte_human_slack_id",
        lambda login: "U12345678" if login == "sunil-kuruba" else None,
    )
    monkeypatch.setattr(
        autopilot,
        "team_oncall_alias_for_connector",
        lambda *args, **kwargs: None,
    )
    sent = _capture_alert(monkeypatch)

    assert (
        autopilot._send_failure_threshold_hitl(_rollout(), "1.2.3", _gate()) == _POSTED
    )
    assert sent["target_person"] == "U12345678"
    assert sent["cc_persons"] == [autopilot._AUTOPILOT_ESCALATION_FALLBACK]
    assert (
        "Release PR: <https://github.com/airbytehq/airbyte/pull/42|PR 42>"
        in sent["message"]
    )
    assert "Release contact: <@U12345678> (`sunil-kuruba`)" in sent["message"]
    assert (
        "Escalation: routed to PR author (Airbyte release contact)" in sent["message"]
    )


def test_community_author_falls_through_to_human_merger(monkeypatch) -> None:
    monkeypatch.setattr(
        autopilot,
        "lookup_release_attribution",
        lambda *args, **kwargs: _result(
            attribution=ReleaseAttribution(
                pr_author_login="community-author",
                pr_author_type="User",
                pr_author_association="CONTRIBUTOR",
                pr_merged_by_login="rodi",
                pr_merged_by_type="User",
                source="publish",
            )
        ),
    )
    monkeypatch.setattr(
        autopilot,
        "resolve_airbyte_human_slack_id",
        lambda login: "U87654321" if login == "rodi" else None,
    )
    monkeypatch.setattr(
        autopilot,
        "team_oncall_alias_for_connector",
        lambda *args, **kwargs: None,
    )
    sent = _capture_alert(monkeypatch)

    autopilot._send_failure_threshold_hitl(_rollout(), "1.2.3", _gate())
    assert sent["target_person"] == "U87654321"
    assert sent["cc_persons"] == [autopilot._AUTOPILOT_ESCALATION_FALLBACK]
    assert "Release contact: <@U87654321> (`rodi`)" in sent["message"]
    assert (
        "Escalation: routed to PR merger (Airbyte release contact)" in sent["message"]
    )
    assert "community-author" not in sent["message"]


def test_legacy_maintainer_attribution_is_targeted(monkeypatch) -> None:
    monkeypatch.setattr(
        autopilot,
        "lookup_release_attribution",
        lambda *args, **kwargs: _result(
            attribution=ReleaseAttribution(
                attributed_to="alice",
                attributed_to_kind="maintainer",
                source="publish",
            )
        ),
    )
    monkeypatch.setattr(
        autopilot,
        "resolve_airbyte_human_slack_id",
        lambda login: "U11223344" if login == "alice" else None,
    )
    monkeypatch.setattr(
        autopilot,
        "team_oncall_alias_for_connector",
        lambda *args, **kwargs: None,
    )
    sent = _capture_alert(monkeypatch)

    autopilot._send_failure_threshold_hitl(_rollout(), "1.2.3", _gate())
    assert sent["target_person"] == "U11223344"
    assert sent["cc_persons"] == [autopilot._AUTOPILOT_ESCALATION_FALLBACK]
    assert "Release contact: <@U11223344> (`alice`)" in sent["message"]
    assert "Escalation: routed to release contact" in sent["message"]


def test_unresolved_legacy_maintainer_attribution_falls_back_to_hydra(
    monkeypatch,
) -> None:
    monkeypatch.setattr(
        autopilot,
        "lookup_release_attribution",
        lambda *args, **kwargs: _result(
            attribution=ReleaseAttribution(
                attributed_to="alice",
                attributed_to_kind="maintainer",
                source="publish",
            )
        ),
    )
    monkeypatch.setattr(autopilot, "resolve_airbyte_human_slack_id", lambda _: None)
    monkeypatch.setattr(
        autopilot,
        "team_oncall_alias_for_connector",
        lambda *args, **kwargs: None,
    )
    sent = _capture_alert(monkeypatch)

    autopilot._send_failure_threshold_hitl(_rollout(), "1.2.3", _gate())
    assert sent["target_person"] == autopilot._AUTOPILOT_ESCALATION_FALLBACK
    assert sent["cc_persons"] == []
    assert "<@U11223344>" not in sent["message"]
    assert "alice" not in sent["message"]


def test_community_author_and_bot_merger_route_certified_database_to_db_dw(
    monkeypatch,
) -> None:
    monkeypatch.setattr(
        autopilot,
        "lookup_release_attribution",
        lambda *args, **kwargs: _result(
            attribution=ReleaseAttribution(
                pr_author_login="community-author",
                pr_author_type="User",
                pr_author_association="CONTRIBUTOR",
                pr_merged_by_login="octavia-bot-admin",
                pr_merged_by_type="Bot",
                source="publish",
            )
        ),
    )
    monkeypatch.setattr(autopilot, "resolve_airbyte_human_slack_id", lambda _: None)
    monkeypatch.setattr(
        autopilot,
        "team_oncall_alias_for_connector",
        lambda *args, **kwargs: "@oc-db-dw",
    )
    sent = _capture_alert(monkeypatch)

    autopilot._send_failure_threshold_hitl(
        _rollout("destination-test"),
        "1.2.3",
        _gate(),
    )
    assert sent["target_person"] == "@oc-db-dw"
    assert sent["cc_persons"] == [autopilot._AUTOPILOT_ESCALATION_FALLBACK]
    assert "Released by: `octavia-bot-admin` (automated account)" in sent["message"]
    assert "community-author" not in sent["message"]
    assert "Escalation: routed to oc-db-dw" in sent["message"]


def test_bot_author_and_merger_route_certified_api_source_to_apis(monkeypatch) -> None:
    monkeypatch.setattr(
        autopilot,
        "lookup_release_attribution",
        lambda *args, **kwargs: _result(
            attribution=ReleaseAttribution(
                pr_author_login="release-bot[bot]",
                pr_author_type="Bot",
                pr_merged_by_login="octavia-bot-admin",
                pr_merged_by_type="Bot",
                source="publish",
            )
        ),
    )
    monkeypatch.setattr(autopilot, "resolve_airbyte_human_slack_id", lambda _: None)
    monkeypatch.setattr(
        autopilot,
        "team_oncall_alias_for_connector",
        lambda *args, **kwargs: "@oc-apis",
    )
    sent = _capture_alert(monkeypatch)

    autopilot._send_failure_threshold_hitl(_rollout("source-test"), "1.2.3", _gate())
    assert sent["target_person"] == "@oc-apis"
    assert sent["cc_persons"] == [autopilot._AUTOPILOT_ESCALATION_FALLBACK]
    assert "Released by: `release-bot[bot]` (automated account)" in sent["message"]


def test_community_connector_routes_to_hydra_without_cc(monkeypatch) -> None:
    monkeypatch.setattr(
        autopilot,
        "lookup_release_attribution",
        lambda *args, **kwargs: _result(
            attribution=ReleaseAttribution(
                pr_author_login="community-author",
                pr_author_type="User",
                pr_author_association="CONTRIBUTOR",
                source="publish",
            )
        ),
    )
    monkeypatch.setattr(autopilot, "resolve_airbyte_human_slack_id", lambda _: None)
    monkeypatch.setattr(
        autopilot,
        "team_oncall_alias_for_connector",
        lambda *args, **kwargs: None,
    )
    sent = _capture_alert(monkeypatch)

    autopilot._send_failure_threshold_hitl(
        _rollout("source-community"),
        "1.2.3",
        _gate(),
    )
    assert sent["target_person"] == autopilot._AUTOPILOT_ESCALATION_FALLBACK
    assert sent["cc_persons"] == []
    assert "<@" not in sent["message"]
    assert "community-author" not in sent["message"]
    assert "routed to oc-hydra" in sent["message"]


def test_alert_lookup_error_still_routes_certified_connector_to_team(
    monkeypatch,
) -> None:
    monkeypatch.setattr(
        autopilot,
        "lookup_release_attribution",
        lambda *args, **kwargs: _result(
            status="error",
            lookup_path="none",
            error="GCS unavailable",
        ),
    )
    monkeypatch.setattr(
        autopilot,
        "team_oncall_alias_for_connector",
        lambda *args, **kwargs: "@oc-db-dw",
    )
    sent = _capture_alert(monkeypatch)

    autopilot._send_failure_threshold_hitl(
        _rollout("destination-test"),
        "1.2.3",
        _gate(),
    )
    assert sent["target_person"] == "@oc-db-dw"
    assert sent["cc_persons"] == [autopilot._AUTOPILOT_ESCALATION_FALLBACK]
    assert "Escalation: routed to oc-db-dw" in sent["message"]


def test_public_github_contact_formatter_uses_roster_and_fallback(monkeypatch) -> None:
    monkeypatch.setattr(
        slack_posting,
        "fetch_roster",
        lambda: [{"github_handle": "engineer", "slack_id": "U12345678"}],
    )
    assert slack_posting.format_github_login_contact("engineer") == "<@U12345678>"
    assert slack_posting.format_github_login_contact("unknown") == "unknown"


@pytest.mark.parametrize(
    "roster,expected",
    [
        (
            [
                {
                    "github_handle": "engineer",
                    "slack_id": "U12345678",
                    "slack_email": "engineer@airbyte.io",
                }
            ],
            "U12345678",
        ),
        (
            [
                {
                    "github_handle": "engineer",
                    "slack_id": "U12345678",
                    "slack_email": "engineer@example.com",
                }
            ],
            None,
        ),
        (
            [
                {
                    "github_handle": "Engineer",
                    "slack_id": "U12345678",
                    "github_public_email": "engineer@airbyte.io",
                }
            ],
            "U12345678",
        ),
    ],
)
def test_resolve_airbyte_human_slack_id(roster, expected, monkeypatch) -> None:
    monkeypatch.setattr(slack_posting, "fetch_roster", lambda: roster)
    assert slack_posting.resolve_airbyte_human_slack_id("ENGINEER") == expected


def test_resolve_airbyte_human_slack_id_handles_roster_failure(monkeypatch) -> None:
    def raise_roster_error():
        raise RuntimeError("roster unavailable")

    monkeypatch.setattr(slack_posting, "fetch_roster", raise_roster_error)
    assert slack_posting.resolve_airbyte_human_slack_id("engineer") is None


def test_alert_reports_failed_investigation_lookup(monkeypatch) -> None:
    monkeypatch.setattr(
        autopilot,
        "lookup_release_attribution",
        lambda *args, **kwargs: _result(),
    )
    monkeypatch.setattr(
        autopilot,
        "team_oncall_alias_for_connector",
        lambda *args, **kwargs: None,
    )
    monkeypatch.setattr(autopilot.devin_api, "is_configured", lambda: True)
    sent = _capture_alert(monkeypatch)

    autopilot._send_failure_threshold_hitl(
        _rollout(),
        "1.2.3",
        _gate(),
        investigation_lookup_failed=True,
    )
    assert "no investigation was started" in sent["message"]
    assert "is starting a Devin investigation" not in sent["message"]

    autopilot._send_failure_threshold_hitl(_rollout(), "1.2.3", _gate())
    assert "is starting a Devin investigation" in sent["message"]
