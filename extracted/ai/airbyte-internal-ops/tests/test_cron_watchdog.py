"""Unit tests for the Hydra cron watchdog."""

from __future__ import annotations

import json
from copy import deepcopy
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from airbyte_ops_mcp import cron_watchdog
from airbyte_ops_mcp.cron_watchdog import (
    Run,
    WatchdogHistory,
    WatchdogResult,
    WatchedWorkflow,
    WorkflowStatus,
    decide,
    derive_status,
)
from airbyte_ops_mcp.slack_api import SlackUsergroup

FIXTURE_DIR = Path(__file__).parent / "fixtures" / "cron_watchdog"
NOW = datetime(2026, 1, 5, 15, 0, tzinfo=timezone.utc)
CONFIG = WatchedWorkflow(
    "airbytehq/airbyte-ops-mcp",
    "fixture.yml",
    "Fixture",
    120,
    frozenset({"schedule"}),
)
KNOWLEDGE_CONFIG = WatchedWorkflow(
    "airbytehq/ai-skills",
    "devin-knowledge-sync.yml",
    "Knowledge Sync",
    None,
    frozenset({"push", "schedule"}),
)
WORKFLOW = json.loads((FIXTURE_DIR / "workflow.json").read_text())


def _fixture_runs() -> list[dict]:
    return json.loads((FIXTURE_DIR / "runs.json").read_text())


@pytest.mark.unit
def test_saved_api_fixtures_derive_recovery() -> None:
    status = derive_status(
        WatchedWorkflow(
            CONFIG.repo,
            CONFIG.workflow,
            CONFIG.label,
            None,
            CONFIG.health_events,
        ),
        WORKFLOW,
        _fixture_runs(),
        NOW,
    )
    assert status.recovery_at == datetime(2026, 1, 5, 12, 0, tzinfo=timezone.utc)


def _run(conclusion: str, minutes_ago: int, *, event: str = "schedule") -> dict:
    data = deepcopy(_fixture_runs()[0])
    data["conclusion"] = conclusion
    data["created_at"] = (NOW - timedelta(minutes=minutes_ago)).isoformat()
    data["event"] = event
    return data


def _run_at(conclusion: str, timestamp: datetime) -> dict:
    data = deepcopy(_fixture_runs()[0])
    data["conclusion"] = conclusion
    data["created_at"] = timestamp.isoformat()
    return data


@pytest.mark.unit
def test_previous_watchdog_start_ignores_pull_request_runs(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    schedule_run = _run_at("success", NOW - timedelta(hours=2))
    schedule_run["id"] = "scheduled-run"
    pull_request_run = _run_at("success", NOW - timedelta(hours=1))
    pull_request_run["id"] = "pull-request-run"
    pull_request_run["event"] = "pull_request"
    monkeypatch.delenv("GITHUB_RUN_ID", raising=False)

    history = cron_watchdog._previous_watchdog_start(
        "github-token",
        now=NOW,
        fetch=lambda *args, **kwargs: {
            "workflow_runs": [pull_request_run, schedule_run]
        },
    )

    assert history == WatchdogHistory(NOW - timedelta(hours=2), known=True)


@pytest.mark.unit
def test_previous_watchdog_start_ignores_workflow_dispatch_runs(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    schedule_run = _run_at("success", NOW - timedelta(hours=2))
    schedule_run["id"] = "scheduled-run"
    manual_run = _run_at("success", NOW - timedelta(hours=1))
    manual_run["id"] = "manual-run"
    manual_run["event"] = "workflow_dispatch"
    monkeypatch.delenv("GITHUB_RUN_ID", raising=False)

    history = cron_watchdog._previous_watchdog_start(
        "github-token",
        now=NOW,
        fetch=lambda *args, **kwargs: {"workflow_runs": [manual_run, schedule_run]},
    )

    assert history == WatchdogHistory(NOW - timedelta(hours=2), known=True)


@pytest.mark.unit
def test_previous_watchdog_start_fetch_error_marks_history_unknown() -> None:
    def fetch(*args: object, **kwargs: object) -> dict:
        raise RuntimeError("GitHub unavailable")

    history = cron_watchdog._previous_watchdog_start(
        "github-token", now=NOW, fetch=fetch
    )

    assert history == WatchdogHistory(None, known=False)


@pytest.mark.unit
def test_previous_watchdog_start_with_no_scheduled_runs_is_known_empty(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    pull_request_run = _run_at("success", NOW - timedelta(hours=1))
    pull_request_run["event"] = "pull_request"
    manual_run = _run_at("success", NOW - timedelta(minutes=30))
    manual_run["event"] = "workflow_dispatch"
    monkeypatch.delenv("GITHUB_RUN_ID", raising=False)

    history = cron_watchdog._previous_watchdog_start(
        "github-token",
        now=NOW,
        fetch=lambda *args, **kwargs: {"workflow_runs": [pull_request_run, manual_run]},
    )

    assert history == WatchdogHistory(None, known=True)


@pytest.mark.unit
def test_self_config_and_history_lookup_are_order_independent(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(cron_watchdog, "WATCHED", list(reversed(cron_watchdog.WATCHED)))
    monkeypatch.delenv("GITHUB_RUN_ID", raising=False)
    requested_urls: list[str] = []

    def fetch(url: str, token: str) -> dict:
        requested_urls.append(url)
        return {"workflow_runs": []}

    config = cron_watchdog._self_config()
    history = cron_watchdog._previous_watchdog_start(
        "github-token", now=NOW, fetch=fetch
    )

    assert config.workflow == cron_watchdog.SELF_WORKFLOW_FILE
    assert history == WatchdogHistory(None, known=True)
    assert requested_urls == [
        f"{cron_watchdog.GITHUB_API}/repos/{config.repo}/actions/workflows/"
        f"{cron_watchdog.SELF_WORKFLOW_FILE}/runs?per_page=10"
    ]


@pytest.mark.unit
def test_unknown_watchdog_history_suppresses_daily_summary() -> None:
    daily_now = datetime(2026, 1, 6, 17, 30, tzinfo=timezone.utc)
    status = _status(unhealthy_minutes=180)
    status.unhealthy_since = daily_now - timedelta(hours=3)

    unknown_history = decide(
        [status],
        now=daily_now,
        previous_watchdog_start=None,
        history_known=False,
    )
    known_history = decide(
        [status],
        now=daily_now,
        previous_watchdog_start=None,
        history_known=True,
    )

    assert "📊 Daily health summary" not in unknown_history.fallback_text
    assert "📊 Daily health summary" in known_history.fallback_text


@pytest.mark.unit
def test_manual_success_does_not_end_scheduled_failure_streak() -> None:
    scheduled_failure = _run("failure", 30)
    manual_success = _run("success", 5, event="workflow_dispatch")

    status = derive_status(CONFIG, WORKFLOW, [manual_success, scheduled_failure], NOW)

    assert status.latest_run is not None
    assert status.latest_run.event == "schedule"
    assert status.unhealthy_since == NOW - timedelta(minutes=30)
    assert status.recovery_at is None


@pytest.mark.unit
def test_manual_success_does_not_prevent_scheduled_stall() -> None:
    scheduled_success = _run("success", 180)
    manual_success = _run("success", 5, event="workflow_dispatch")

    status = derive_status(CONFIG, WORKFLOW, [manual_success, scheduled_success], NOW)

    assert status.latest_run is not None
    assert status.latest_run.event == "schedule"
    assert status.unhealthy_since == NOW - timedelta(minutes=60)


@pytest.mark.unit
def test_knowledge_push_success_counts_as_healthy() -> None:
    push_success = _run("success", 5, event="push")

    status = derive_status(KNOWLEDGE_CONFIG, WORKFLOW, [push_success], NOW)

    assert status.unhealthy_since is None
    assert status.latest_run is not None
    assert status.latest_run.event == "push"


@pytest.mark.unit
def test_knowledge_manual_success_does_not_silence_push_failure() -> None:
    push_failure = _run("failure", 30, event="push")
    manual_success = _run("success", 5, event="workflow_dispatch")

    status = derive_status(
        KNOWLEDGE_CONFIG, WORKFLOW, [manual_success, push_failure], NOW
    )

    assert status.latest_run is not None
    assert status.latest_run.event == "push"
    assert status.unhealthy_since == NOW - timedelta(minutes=30)


@pytest.mark.unit
def test_is_current_workflow_matches_workflow_ref(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv(
        "GITHUB_WORKFLOW_REF",
        "airbytehq/airbyte-ops-mcp/.github/workflows/fixture.yml@refs/heads/main",
    )

    assert cron_watchdog._is_current_workflow(CONFIG)


@pytest.mark.unit
@pytest.mark.parametrize(
    "workflow_ref",
    [
        None,
        "",
        "fixture.yml",
        "airbytehq/airbyte-ops-mcp/.github/workflows/fixture.yml",
    ],
)
def test_is_current_workflow_rejects_missing_or_malformed_ref(
    monkeypatch: pytest.MonkeyPatch, workflow_ref: str | None
) -> None:
    if workflow_ref is None:
        monkeypatch.delenv("GITHUB_WORKFLOW_REF", raising=False)
    else:
        monkeypatch.setenv("GITHUB_WORKFLOW_REF", workflow_ref)

    assert not cron_watchdog._is_current_workflow(CONFIG)


@pytest.mark.unit
def test_self_workflow_without_runs_is_not_marked_unhealthy() -> None:
    status = derive_status(CONFIG, WORKFLOW, [], NOW, is_self=True)

    assert status.unhealthy_since is None


@pytest.mark.unit
def test_self_workflow_old_scheduled_run_is_not_stalled() -> None:
    old_run = _run("success", 300)

    status = derive_status(CONFIG, WORKFLOW, [old_run], NOW, is_self=True)

    assert status.unhealthy_since is None


@pytest.mark.unit
def test_self_workflow_failed_run_is_still_unhealthy() -> None:
    failed_run = _run("failure", 5)

    status = derive_status(CONFIG, WORKFLOW, [failed_run], NOW, is_self=True)

    assert status.unhealthy_since == NOW - timedelta(minutes=5)


@pytest.mark.unit
def test_cancelled_health_run_anchors_knowledge_sync_to_newest_timestamp() -> None:
    older_cancelled = _run("cancelled", 60, event="push")
    newer_cancelled = _run("cancelled", 15, event="push")

    status = derive_status(
        KNOWLEDGE_CONFIG, WORKFLOW, [older_cancelled, newer_cancelled], NOW
    )

    assert status.unhealthy_since == NOW - timedelta(minutes=15)


@pytest.mark.unit
@pytest.mark.parametrize(
    "minutes_ago,expected_ping",
    [(90, False), (180, True)],
)
def test_cancelled_knowledge_sync_run_escalates_from_timestamp_anchor(
    minutes_ago: int, expected_ping: bool
) -> None:
    cancelled_run = _run("cancelled", minutes_ago, event="push")

    status = derive_status(KNOWLEDGE_CONFIG, WORKFLOW, [cancelled_run], NOW)
    result = decide(
        [status],
        now=NOW,
        previous_watchdog_start=NOW - timedelta(hours=1),
    )

    assert status.unhealthy_since == NOW - timedelta(minutes=minutes_ago)
    assert result.should_post
    assert result.ping_oncall is expected_ping


@pytest.mark.unit
def test_finished_health_run_prevents_cancelled_run_anchor() -> None:
    cancelled_run = _run("cancelled", 180, event="push")
    finished_run = _run("success", 15, event="push")

    status = derive_status(
        KNOWLEDGE_CONFIG, WORKFLOW, [cancelled_run, finished_run], NOW
    )

    assert status.unhealthy_since is None
    assert status.latest_run is not None
    assert status.latest_run.conclusion == "success"


@pytest.mark.unit
def test_cancelled_health_runs_fall_back_to_workflow_creation_time() -> None:
    cancelled_run = _run("cancelled", 180, event="push")
    cancelled_run["created_at"] = "not-a-timestamp"
    cancelled_run["run_started_at"] = "also-not-a-timestamp"
    cancelled_run["updated_at"] = "still-not-a-timestamp"
    created_at = NOW - timedelta(minutes=30)
    workflow = {**WORKFLOW, "created_at": created_at.isoformat()}

    status = derive_status(KNOWLEDGE_CONFIG, workflow, [cancelled_run], NOW)

    assert status.unhealthy_since == created_at


@pytest.mark.unit
def test_self_workflow_in_progress_run_is_not_marked_unhealthy() -> None:
    in_progress_run = _run("success", 0)
    in_progress_run["conclusion"] = None

    status = derive_status(CONFIG, WORKFLOW, [in_progress_run], NOW, is_self=True)

    assert status.unhealthy_since is None


@pytest.mark.unit
def test_irrelevant_cancelled_run_does_not_anchor_outage() -> None:
    cancelled_manual_run = _run("cancelled", 180, event="workflow_dispatch")
    created_at = NOW - timedelta(minutes=30)

    status = derive_status(
        CONFIG,
        {**WORKFLOW, "created_at": created_at.isoformat()},
        [cancelled_manual_run],
        NOW,
    )

    assert status.unhealthy_since == created_at


def _status(
    *,
    conclusion: str = "failure",
    unhealthy_minutes: int = 30,
    state: str = "active",
    runs: list[Run] | None = None,
    rate: float | None = None,
) -> WorkflowStatus:
    if runs is None:
        runs = [
            Run(
                conclusion=conclusion,
                timestamp=NOW - timedelta(minutes=unhealthy_minutes),
                html_url="https://example.test/run",
                event="schedule",
                name="Fixture",
            )
        ]
    status = WorkflowStatus(CONFIG, state, runs)
    if state != "active":
        status.unhealthy_since = NOW
    elif conclusion != "success":
        status.unhealthy_since = NOW - timedelta(minutes=unhealthy_minutes)
    if rate is not None:
        status.runs = [
            Run(
                conclusion="success",
                timestamp=NOW,
                html_url="https://example.test/run",
                event="schedule",
                name="Fixture",
            ),
            *[
                Run(
                    conclusion="failure" if i < int(rate * 10) else "success",
                    timestamp=NOW - timedelta(minutes=60 + i),
                    html_url="https://example.test/run",
                    event="schedule",
                    name="Fixture",
                )
                for i in range(9)
            ],
        ]
    return status


@pytest.mark.unit
def test_unhealthy_30_minutes_stays_silent() -> None:
    result = decide(
        [_status(unhealthy_minutes=30)],
        now=NOW,
        previous_watchdog_start=NOW - timedelta(hours=1),
    )
    assert not result.should_post


@pytest.mark.unit
def test_crossing_60_minutes_posts_notice_without_ping() -> None:
    result = decide(
        [_status(unhealthy_minutes=65)],
        now=NOW,
        previous_watchdog_start=NOW - timedelta(hours=1),
    )
    assert result.should_post
    assert not result.ping_oncall
    assert "unhealthy" in result.fallback_text


@pytest.mark.unit
def test_crossing_120_minutes_pages() -> None:
    result = decide(
        [_status(unhealthy_minutes=125)],
        now=NOW,
        previous_watchdog_start=NOW - timedelta(hours=1),
    )
    assert result.should_post
    assert result.ping_oncall
    assert "🚨" in result.fallback_text


@pytest.mark.unit
def test_mid_outage_continuation_tick_stays_silent() -> None:
    status = _status(unhealthy_minutes=3 * 24 * 60)
    result = decide([status], now=NOW, previous_watchdog_start=NOW - timedelta(hours=1))
    assert not result.should_post


@pytest.mark.unit
def test_recovery_after_90_minutes_posts_without_ping() -> None:
    runs = [_run("success", 0), _run("failure", 90)]
    status = derive_status(CONFIG, WORKFLOW, runs, NOW)
    result = decide([status], now=NOW, previous_watchdog_start=NOW - timedelta(hours=1))
    assert result.should_post
    assert not result.ping_oncall
    assert "recovered" in result.fallback_text


@pytest.mark.unit
def test_recovery_after_30_minutes_stays_silent() -> None:
    runs = [_run("success", 0), _run("failure", 30)]
    status = derive_status(CONFIG, WORKFLOW, runs, NOW)
    result = decide([status], now=NOW, previous_watchdog_start=NOW - timedelta(hours=1))
    assert not result.should_post


@pytest.mark.unit
def test_recovered_workflow_that_goes_silent_is_unhealthy() -> None:
    now = datetime(2026, 1, 5, 17, 0, tzinfo=timezone.utc)
    runs = [
        _run_at("success", datetime(2026, 1, 5, 11, 0, tzinfo=timezone.utc)),
        _run_at("failure", datetime(2026, 1, 5, 10, 0, tzinfo=timezone.utc)),
    ]
    status = derive_status(CONFIG, WORKFLOW, runs, now)
    result = decide(
        [status],
        now=now,
        previous_watchdog_start=now - timedelta(hours=5),
    )
    assert status.unhealthy_since == datetime(2026, 1, 5, 13, 0, tzinfo=timezone.utc)
    assert status.recovery_at is None
    assert result.should_post
    assert "recovered" not in result.fallback_text
    assert "unhealthy" in result.fallback_text


@pytest.mark.unit
def test_active_workflow_with_no_usable_runs_is_unhealthy() -> None:
    runs = [_run("cancelled", 0), _run("skipped", 30)]
    status = derive_status(CONFIG, WORKFLOW, runs, NOW)
    assert CONFIG.stall_grace_min is not None
    assert status.unhealthy_since == NOW


@pytest.mark.unit
def test_no_finished_runs_anchor_to_workflow_creation_time() -> None:
    created_at = NOW - timedelta(minutes=5)
    workflow = {**WORKFLOW, "created_at": created_at.isoformat()}
    status = derive_status(CONFIG, workflow, [], NOW)

    assert status.unhealthy_since == created_at
    result = decide(
        [status],
        now=NOW,
        previous_watchdog_start=NOW - timedelta(hours=1),
    )
    assert not result.should_post


@pytest.mark.unit
def test_no_finished_runs_escalate_from_workflow_creation_time() -> None:
    created_at = NOW - timedelta(hours=3)
    workflow = {**WORKFLOW, "created_at": created_at.isoformat()}
    status = derive_status(CONFIG, workflow, [], NOW)

    assert status.unhealthy_since == created_at
    result = decide(
        [status],
        now=NOW,
        previous_watchdog_start=NOW - timedelta(hours=1),
    )
    assert result.should_post
    assert result.ping_oncall
    assert "no finished runs in the last 0 fetched runs" in result.fallback_text


@pytest.mark.unit
def test_no_finished_runs_without_creation_time_falls_back_to_now() -> None:
    status = derive_status(CONFIG, WORKFLOW, [_run("cancelled", 0)], NOW)

    assert status.unhealthy_since == NOW


@pytest.mark.unit
def test_disabled_workflow_stays_silent_between_daily_ticks() -> None:
    status = derive_status(CONFIG, {**WORKFLOW, "state": "disabled_manually"}, [], NOW)
    result = decide([status], now=NOW, previous_watchdog_start=NOW - timedelta(hours=1))
    assert not result.should_post
    assert not result.ping_oncall


@pytest.mark.unit
def test_disabled_workflow_pages_on_first_daily_tick() -> None:
    status = derive_status(CONFIG, {**WORKFLOW, "state": "disabled_manually"}, [], NOW)
    result = decide(
        [status],
        now=datetime(2026, 1, 5, 17, 25, tzinfo=timezone.utc),
        previous_watchdog_start=datetime(2026, 1, 5, 16, 25, tzinfo=timezone.utc),
    )
    assert result.should_post
    assert result.ping_oncall
    assert "disabled" in result.fallback_text


@pytest.mark.unit
def test_zero_minute_outage_does_not_trigger_daily_summary() -> None:
    daily_now = datetime(2026, 1, 6, 17, 25, tzinfo=timezone.utc)
    created_at = daily_now
    workflow = {**WORKFLOW, "created_at": created_at.isoformat()}
    status = derive_status(CONFIG, workflow, [], daily_now)
    result = decide(
        [status],
        now=daily_now,
        previous_watchdog_start=daily_now.replace(hour=8, minute=25),
    )

    assert not result.should_post
    assert not result.ping_oncall
    assert "Daily health summary" not in result.fallback_text


@pytest.mark.unit
def test_ninety_minute_outage_triggers_daily_summary() -> None:
    daily_now = datetime(2026, 1, 6, 17, 25, tzinfo=timezone.utc)
    status = _status(unhealthy_minutes=90)
    status.unhealthy_since = daily_now - timedelta(minutes=90)
    result = decide(
        [status],
        now=daily_now,
        previous_watchdog_start=daily_now.replace(hour=8, minute=25),
    )

    assert result.should_post
    assert result.ping_oncall
    assert "Daily health summary" in result.fallback_text


@pytest.mark.unit
@pytest.mark.parametrize(
    "age,expected",
    [(100, False), (200, True), (260, True)],
)
def test_no_runs_for_age_uses_stall_grace(age: int, expected: bool) -> None:
    runs = [_run("success", age)]
    status = derive_status(CONFIG, WORKFLOW, runs, NOW)
    result = decide([status], now=NOW, previous_watchdog_start=NOW - timedelta(hours=1))
    assert result.should_post is expected
    if age == 260:
        assert result.ping_oncall


@pytest.mark.unit
def test_delayed_watchdog_stretches_reporting_window() -> None:
    status = _status(unhealthy_minutes=150)
    result = decide(
        [status],
        now=NOW,
        previous_watchdog_start=NOW - timedelta(hours=5),
    )
    assert result.should_post


@pytest.mark.unit
def test_green_workflow_with_30_percent_rate_at_daily_tick_pages() -> None:
    status = _status(
        conclusion="success",
        runs=[Run("success", NOW, "", "schedule", "Fixture")],
        rate=0.3,
    )
    status.unhealthy_since = None
    result = decide(
        [status],
        now=datetime(2026, 1, 5, 17, 25, tzinfo=timezone.utc),
        previous_watchdog_start=datetime(2026, 1, 5, 16, 25, tzinfo=timezone.utc),
    )
    assert result.should_post
    assert result.ping_oncall
    assert "30%" in result.fallback_text


@pytest.mark.unit
def test_green_workflow_with_30_percent_rate_mid_afternoon_stays_silent() -> None:
    status = _status(
        conclusion="success",
        runs=[Run("success", NOW, "", "schedule", "Fixture")],
        rate=0.3,
    )
    status.unhealthy_since = None
    result = decide(
        [status],
        now=datetime(2026, 1, 5, 21, 25, tzinfo=timezone.utc),
        previous_watchdog_start=datetime(2026, 1, 5, 20, 25, tzinfo=timezone.utc),
    )
    assert not result.should_post


@pytest.mark.unit
def test_all_healthy_non_monday_stays_silent() -> None:
    status = _status(
        conclusion="success", runs=[Run("success", NOW, "", "schedule", "Fixture")]
    )
    status.unhealthy_since = None
    result = decide(
        [status],
        now=datetime(2026, 1, 6, 17, 25, tzinfo=timezone.utc),
        previous_watchdog_start=datetime(2026, 1, 6, 16, 25, tzinfo=timezone.utc),
    )
    assert not result.should_post


@pytest.mark.unit
def test_all_healthy_monday_posts_heartbeat() -> None:
    status = _status(
        conclusion="success", runs=[Run("success", NOW, "", "schedule", "Fixture")]
    )
    status.unhealthy_since = None
    result = decide(
        [status],
        now=datetime(2026, 1, 5, 17, 25, tzinfo=timezone.utc),
        previous_watchdog_start=datetime(2026, 1, 5, 16, 25, tzinfo=timezone.utc),
    )
    assert result.should_post
    assert "heartbeat" in result.fallback_text


def _run_watchdog_with_status(
    monkeypatch: pytest.MonkeyPatch,
    lookup: object,
) -> WatchdogResult:
    status = _status(unhealthy_minutes=125)
    monkeypatch.setattr(
        cron_watchdog, "collect_statuses", lambda *args, **kwargs: [status]
    )
    monkeypatch.setattr(
        cron_watchdog,
        "_previous_watchdog_start",
        lambda *args, **kwargs: WatchdogHistory(NOW - timedelta(hours=1), known=True),
    )
    monkeypatch.setattr(cron_watchdog, "lookup_slack_usergroup", lookup)
    monkeypatch.delenv("DRY_RUN", raising=False)
    return cron_watchdog.run_watchdog(now=NOW, token="github-token")


@pytest.mark.unit
def test_oncall_lookup_error_uses_plain_text_fallback(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def lookup(*args: object, **kwargs: object) -> list[SlackUsergroup]:
        raise RuntimeError("Slack unavailable")

    result = _run_watchdog_with_status(monkeypatch, lookup)
    assert result.ping_oncall
    assert "@oc-hydra" in result.fallback_text
    assert "<!subteam^" not in result.fallback_text


@pytest.mark.unit
def test_oncall_lookup_uses_usergroup_mention(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    usergroup = SlackUsergroup("S0ONCALL123", "OC-HYDRA", "Hydra On-call", "", 3)

    def lookup(*args: object, **kwargs: object) -> list[SlackUsergroup]:
        return [usergroup]

    result = _run_watchdog_with_status(monkeypatch, lookup)
    assert result.ping_oncall
    assert "<!subteam^S0ONCALL123|@oc-hydra>" in result.fallback_text


@pytest.mark.unit
def test_healthy_dry_run_resolves_oncall_without_mention(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    status = _status(
        conclusion="success", runs=[Run("success", NOW, "", "schedule", "Fixture")]
    )
    status.unhealthy_since = None
    calls: list[str] = []
    usergroup = SlackUsergroup("S0ONCALL123", "oc-hydra", "Hydra On-call", "", 3)

    def lookup(handle: str) -> list[SlackUsergroup]:
        calls.append(handle)
        return [usergroup]

    monkeypatch.setattr(
        cron_watchdog, "collect_statuses", lambda *args, **kwargs: [status]
    )
    monkeypatch.setattr(
        cron_watchdog,
        "_previous_watchdog_start",
        lambda *args, **kwargs: WatchdogHistory(NOW - timedelta(hours=1), known=True),
    )
    monkeypatch.setattr(cron_watchdog, "lookup_slack_usergroup", lookup)
    monkeypatch.setenv("DRY_RUN", "true")

    result = cron_watchdog.run_watchdog(now=NOW, token="github-token")

    assert calls == ["oc-hydra"]
    assert not result.should_post
    assert "<!subteam^" not in result.fallback_text
    assert "@oc-hydra" not in result.fallback_text
    assert "<!subteam^" not in str(result.blocks)
    assert "@oc-hydra" not in str(result.blocks)


@pytest.mark.unit
def test_github_output_preserves_multiline_fallback_text(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    output_path = tmp_path / "github-output"
    output_path.write_text("existing=value\n")
    monkeypatch.setenv("GITHUB_OUTPUT", str(output_path))
    first_result = WatchdogResult(
        should_post=True,
        ping_oncall=False,
        blocks=[{"type": "section"}],
        fallback_text="first line\nsecond line",
        summary="",
        statuses=[],
    )
    second_result = WatchdogResult(
        should_post=False,
        ping_oncall=False,
        blocks=[{"type": "header"}],
        fallback_text="another line\nwith more detail",
        summary="",
        statuses=[],
    )

    cron_watchdog._write_github_output(first_result)
    cron_watchdog._write_github_output(second_result)

    lines = output_path.read_text().splitlines()
    assert lines[0] == "existing=value"
    assert lines[1] == "should_post=true"
    assert lines[2] == 'blocks_json=[{"type":"section"}]'
    first_key, first_delimiter = lines[3].split("<<", 1)
    first_end = lines.index(first_delimiter, 4)
    assert first_key == "fallback_text"
    assert "\n".join(lines[4:first_end]) == first_result.fallback_text
    assert lines[first_end + 1] == "should_post=false"
    assert lines[first_end + 2] == 'blocks_json=[{"type":"header"}]'
    second_key, second_delimiter = lines[first_end + 3].split("<<", 1)
    second_end = lines.index(second_delimiter, first_end + 4)
    assert second_key == "fallback_text"
    assert "\n".join(lines[first_end + 4 : second_end]) == second_result.fallback_text
    assert first_delimiter != second_delimiter
    assert all(" | " not in line for line in lines)
