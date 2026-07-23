# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Tests for the zero-eligible-actor detection and pre-flight estimate helpers."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone

import pytest

from airbyte_ops_mcp.cloud_admin.version_overrides import ResolvedCloudAuth
from airbyte_ops_mcp.connector_ops.rollouts import _helpers, autopilot
from airbyte_ops_mcp.connector_ops.rollouts._helpers import (
    ELIGIBILITY_WARN_AT_OR_BELOW,
    TierEligibilityEstimate,
    count_eligible_or_pinned_actors,
    estimate_tier_eligible_actors,
    parse_db_timestamp,
)
from airbyte_ops_mcp.connector_ops.rollouts.models import (
    AutopilotResult,
    ConnectorRolloutRecord,
)


@pytest.mark.unit
@pytest.mark.parametrize(
    "sync_info,expected",
    [
        pytest.param(
            {"data": {"actorSelectionInfo": {"numActorsEligibleOrAlreadyPinned": 5}}},
            5,
            id="camel_case",
        ),
        pytest.param(
            {
                "data": {
                    "actor_selection_info": {"num_actors_eligible_or_already_pinned": 3}
                }
            },
            3,
            id="snake_case",
        ),
        pytest.param(
            {"data": {"actorSelectionInfo": {"numActorsEligibleOrAlreadyPinned": 0}}},
            0,
            id="zero_is_the_wedge_signal",
        ),
        pytest.param(
            {"actorSelectionInfo": {"numActorsEligibleOrAlreadyPinned": 2}},
            2,
            id="already_inner_payload_no_data_key",
        ),
        pytest.param({"data": {}}, 0, id="missing_selection_info"),
        pytest.param({}, 0, id="empty_response"),
    ],
)
def test_count_eligible_or_pinned_actors(sync_info: dict, expected: int) -> None:
    assert count_eligible_or_pinned_actors(sync_info) == expected


@pytest.mark.unit
@pytest.mark.parametrize(
    "count,expected_disposition",
    [
        pytest.param(0, "skip", id="zero_is_skip"),
        pytest.param(1, "warn", id="one_is_warn"),
        pytest.param(ELIGIBILITY_WARN_AT_OR_BELOW, "warn", id="threshold_is_warn"),
        pytest.param(ELIGIBILITY_WARN_AT_OR_BELOW + 1, "normal", id="above_is_normal"),
        pytest.param(50, "normal", id="many_is_normal"),
    ],
)
def test_estimate_disposition_thresholds(
    monkeypatch: pytest.MonkeyPatch,
    count: int,
    expected_disposition: str,
) -> None:
    """Skip at 0, warn at 1..N, normal above N — counting distinct actors."""
    rows = [
        {"source_id": f"actor-{i}", "organization_id": "org-1"} for i in range(count)
    ]
    monkeypatch.setattr(
        _helpers, "query_connections_by_connector", lambda **_: list(rows)
    )
    monkeypatch.setattr(_helpers, "enrich_rows_by_org", lambda r: r)
    monkeypatch.setattr(_helpers, "filter_rows_by_tier", lambda r, _tier: r)

    estimate = estimate_tier_eligible_actors(
        actor_definition_id="def-1",
        docker_repository="airbyte/source-faker",
        tier="TIER_2",
    )
    assert estimate.eligible_actor_count == count
    assert estimate.disposition == expected_disposition


@pytest.mark.unit
def test_estimate_counts_distinct_actors(monkeypatch: pytest.MonkeyPatch) -> None:
    """Multiple connections on the same actor count once."""
    rows = [
        {"source_id": "actor-a", "organization_id": "org-1"},
        {"source_id": "actor-a", "organization_id": "org-1"},
        {"source_id": "actor-b", "organization_id": "org-2"},
    ]
    monkeypatch.setattr(
        _helpers, "query_connections_by_connector", lambda **_: list(rows)
    )
    monkeypatch.setattr(_helpers, "enrich_rows_by_org", lambda r: r)
    monkeypatch.setattr(_helpers, "filter_rows_by_tier", lambda r, _tier: r)

    estimate = estimate_tier_eligible_actors(
        actor_definition_id="def-1",
        docker_repository="airbyte/source-faker",
        tier="TIER_2",
    )
    assert estimate.eligible_actor_count == 2


@pytest.mark.unit
def test_estimate_uses_destination_query(monkeypatch: pytest.MonkeyPatch) -> None:
    """A destination repo selects the destination query and `destination_id` key."""
    called: dict[str, bool] = {"source": False, "destination": False}

    def _source(**_: object) -> list[dict]:
        called["source"] = True
        return []

    def _destination(**_: object) -> list[dict]:
        called["destination"] = True
        return [{"destination_id": "dest-a", "organization_id": "org-1"}]

    monkeypatch.setattr(_helpers, "query_connections_by_connector", _source)
    monkeypatch.setattr(
        _helpers, "query_connections_by_destination_connector", _destination
    )
    monkeypatch.setattr(_helpers, "enrich_rows_by_org", lambda r: r)
    monkeypatch.setattr(_helpers, "filter_rows_by_tier", lambda r, _tier: r)

    estimate = estimate_tier_eligible_actors(
        actor_definition_id="def-1",
        docker_repository="airbyte/destination-bigquery",
        tier="TIER_2",
    )
    assert called["destination"] is True
    assert called["source"] is False
    assert estimate.eligible_actor_count == 1


@pytest.mark.unit
@pytest.mark.parametrize(
    "value,expected",
    [
        pytest.param(None, None, id="none"),
        pytest.param(
            "2026-07-08T20:00:00Z",
            datetime(2026, 7, 8, 20, 0, tzinfo=timezone.utc),
            id="iso_with_z",
        ),
        pytest.param(
            datetime(2026, 7, 8, 20, 0),
            datetime(2026, 7, 8, 20, 0, tzinfo=timezone.utc),
            id="naive_assumed_utc",
        ),
        pytest.param("not-a-timestamp", None, id="unparseable_fails_closed"),
        pytest.param(12345, None, id="non_str_non_datetime"),
    ],
)
def test_parse_db_timestamp(value: object, expected: datetime | None) -> None:
    assert parse_db_timestamp(value) == expected


@pytest.mark.unit
@pytest.mark.parametrize(
    "exc",
    [
        pytest.param(RuntimeError("tier cache unavailable"), id="tier_cache_runtime"),
        pytest.param(ValueError("bad input"), id="reraised_unexpected"),
    ],
)
def test_safe_estimate_falls_back_on_estimate_failure(
    monkeypatch: pytest.MonkeyPatch,
    exc: Exception,
) -> None:
    """A tier-cache `RuntimeError` yields an unavailable estimate; other errors propagate."""

    def _raise(**_: object) -> TierEligibilityEstimate:
        raise exc

    monkeypatch.setattr(autopilot, "estimate_tier_eligible_actors", _raise)

    if isinstance(exc, RuntimeError):
        estimate = autopilot._safe_estimate(
            actor_definition_id="def-1",
            docker_repository="airbyte/source-faker",
            tier="TIER_2",
            action="advance",
        )
        assert estimate.eligible_actor_count == -1
        assert estimate.disposition == "normal"
    else:
        with pytest.raises(ValueError):
            autopilot._safe_estimate(
                actor_definition_id="def-1",
                docker_repository="airbyte/source-faker",
                tier="TIER_2",
                action="advance",
            )


@pytest.mark.unit
def test_reconcile_finalizing_skips_when_timestamp_unavailable(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A finalizing rollout with an unparseable `updated_at` is flagged, not re-finalized.

    Without a parseable timestamp the grace window can't be confirmed, so
    reconciliation must fail closed (warn for review) rather than risk a
    premature re-finalize.  `get_registry_default_version` must never be called
    on this path.
    """

    def _fail(*_a: object, **_k: object) -> object:
        raise AssertionError(
            "registry lookup must not run without a confirmed grace window"
        )

    monkeypatch.setattr(autopilot, "get_registry_default_version", _fail)

    rollout = ConnectorRolloutRecord(
        rollout_id="rollout-1",
        actor_definition_id="def-1",
        state="finalizing",
        rc_docker_repository="airbyte/source-faker",
        rc_docker_image_tag="7.2.0-rc.1",
        tag="TIER_2",
        updated_at="not-a-timestamp",
    )
    result = AutopilotResult(command="auto-promote", dry_run=False)

    autopilot._reconcile_finalizing_rollouts(
        finalizing=[rollout],
        auth=ResolvedCloudAuth(bearer_token="t"),
        user_id="user-1",
        result=result,
        dry_run=False,
    )

    assert len(result.warnings) == 1
    assert "updated_at" in result.warnings[0].message
    assert not result.actions


@pytest.mark.unit
@pytest.mark.parametrize(
    "estimate,expected",
    [
        pytest.param(
            TierEligibilityEstimate(
                tier="TIER_2",
                eligible_actor_count=0,
                disposition="skip",
                reason="0 eligible actors",
            ),
            "complete",
            id="confirmed_empty_is_complete",
        ),
        pytest.param(
            TierEligibilityEstimate(
                tier="TIER_2",
                eligible_actor_count=-1,
                disposition="normal",
                reason="eligibility estimate unavailable",
            ),
            "skip",
            id="unavailable_estimate_skips",
        ),
        pytest.param(
            TierEligibilityEstimate(
                tier="TIER_2",
                eligible_actor_count=2,
                disposition="warn",
                reason="low sample",
            ),
            "proceed",
            id="low_sample_proceeds",
        ),
        pytest.param(
            TierEligibilityEstimate(
                tier="TIER_2",
                eligible_actor_count=50,
                disposition="normal",
                reason="",
            ),
            "proceed",
            id="normal_proceeds",
        ),
    ],
)
def test_recovery_tier_action(
    estimate: TierEligibilityEstimate,
    expected: str,
) -> None:
    """Confirmed-empty completes, unavailable skips, populated proceeds.

    A missing estimate (`eligible_actor_count == -1`) must skip: it's the only
    eligibility check on the `workflow_started` recovery path, so treating an
    unavailable read as complete or re-driving it could wedge the tier again.
    """
    assert autopilot._recovery_tier_action(estimate) == expected


def _tier_estimate(tier: str, count: int) -> TierEligibilityEstimate:
    """Build an estimate matching `_safe_estimate` conventions for a tier."""
    if count < 0:
        return TierEligibilityEstimate(
            tier=tier,
            eligible_actor_count=-1,
            disposition="normal",
            reason="eligibility estimate unavailable",
        )
    disposition = "skip" if count == 0 else "normal"
    return TierEligibilityEstimate(
        tier=tier,
        eligible_actor_count=count,
        disposition=disposition,
        reason=f"{tier} has {count} eligible actors",
    )


@pytest.mark.unit
@pytest.mark.parametrize(
    "current_tier,tier_counts,expected_kind,expected_tier",
    [
        pytest.param(
            "TIER_2",
            {"TIER_1": 5, "TIER_0": 10},
            "start",
            "TIER_1",
            id="next_tier_has_actors",
        ),
        pytest.param(
            "TIER_2",
            {"TIER_1": 0, "TIER_0": 10},
            "start",
            "TIER_0",
            id="skips_empty_intermediate_tier",
        ),
        pytest.param(
            "TIER_1",
            {"TIER_0": 10},
            "start",
            "TIER_0",
            id="tier_1_starts_tier_0_when_populated",
        ),
        pytest.param(
            "TIER_2",
            {"TIER_1": 0, "TIER_0": 0},
            "ga",
            None,
            id="all_later_tiers_empty_promotes_to_ga",
        ),
        pytest.param(
            "TIER_1",
            {"TIER_0": 0},
            "ga",
            None,
            id="only_remaining_tier_empty_promotes_to_ga",
        ),
        pytest.param(
            "TIER_0",
            {},
            "ga",
            None,
            id="terminal_tier_has_no_successor_promotes_to_ga",
        ),
        pytest.param(
            "TIER_1",
            {"TIER_0": -1},
            "unavailable",
            "TIER_0",
            id="unavailable_terminal_estimate_defers",
        ),
        pytest.param(
            "TIER_2",
            {"TIER_1": -1, "TIER_0": 10},
            "unavailable",
            "TIER_1",
            id="unavailable_estimate_defers",
        ),
    ],
)
def test_select_forward_tier(
    monkeypatch: pytest.MonkeyPatch,
    current_tier: str,
    tier_counts: dict[str, int],
    expected_kind: str,
    expected_tier: str | None,
) -> None:
    """Forward scan starts the first later tier with actors, else promotes to GA."""

    def _estimate(*, actor_definition_id: str, docker_repository: str, tier: str):
        return _tier_estimate(tier, tier_counts[tier])

    monkeypatch.setattr(autopilot, "estimate_tier_eligible_actors", _estimate)

    kind, next_t, _ = autopilot._select_forward_tier(
        actor_definition_id="def-1",
        docker_repository="airbyte/source-faker",
        current_tier=current_tier,
        action="promote",
    )

    assert kind == expected_kind
    assert (next_t.value if next_t else None) == expected_tier


@dataclass
class _FakeAutopilotConfig:
    """Minimal stand-in for the registry `autopilotConfig` block."""

    auto_promote_stages: bool = True
    strategy: object = None


@dataclass
class _FakeRolloutConfig:
    """Minimal stand-in for `get_connector_rollout_config`'s return value."""

    default_rollout_mode: object
    autopilot_config: _FakeAutopilotConfig


@dataclass
class _FakeHealthGate:
    """Minimal stand-in for `check_health_gate`'s return value."""

    passed: bool
    reason: str


def _autopilot_config_for(adid: str, rc_version: str) -> _FakeRolloutConfig:
    return _FakeRolloutConfig(
        default_rollout_mode=autopilot.RolloutMode.autopilot,
        autopilot_config=_FakeAutopilotConfig(),
    )


@pytest.mark.unit
def test_run_auto_advance_finalizes_empty_workflow_started(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A `workflow_started` rollout with confirmed 0 eligible actors → succeeded."""
    row = {
        "rollout_id": "rollout-1",
        "actor_definition_id": "def-1",
        "state": "workflow_started",
        "rc_docker_repository": "airbyte/source-faker",
        "rc_docker_image_tag": "7.2.0-rc.1",
        "tag": "TIER_2",
        "current_target_rollout_pct": 0,
        "final_target_rollout_pct": 100,
    }
    monkeypatch.setattr(autopilot, "query_connector_rollouts", lambda **_: [row])
    monkeypatch.setattr(autopilot, "get_admin_user_id", lambda **_: "user-1")
    monkeypatch.setattr(
        autopilot, "get_connector_rollout_config", _autopilot_config_for
    )
    monkeypatch.setattr(
        autopilot,
        "estimate_tier_eligible_actors",
        lambda **_: _tier_estimate("TIER_2", 0),
    )

    calls: list[dict] = []

    def _finalize(**kwargs: object) -> dict:
        calls.append(kwargs)
        return {}

    monkeypatch.setattr(autopilot.api_client, "finalize_connector_rollout", _finalize)

    result = autopilot.run_auto_advance(
        auth=ResolvedCloudAuth(bearer_token="t"), dry_run=False
    )

    assert len(calls) == 1
    assert calls[0]["state"] == "succeeded"
    assert calls[0]["rollout_id"] == "rollout-1"
    assert not result.errors
    assert [a.action for a in result.actions] == ["complete"]


@pytest.mark.unit
def test_run_auto_advance_empty_workflow_started_dry_run_does_not_finalize(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Dry run reports the would-be completion without mutating."""
    row = {
        "rollout_id": "rollout-1",
        "actor_definition_id": "def-1",
        "state": "workflow_started",
        "rc_docker_repository": "airbyte/source-faker",
        "rc_docker_image_tag": "7.2.0-rc.1",
        "tag": "TIER_2",
        "current_target_rollout_pct": 0,
        "final_target_rollout_pct": 100,
    }
    monkeypatch.setattr(autopilot, "query_connector_rollouts", lambda **_: [row])
    monkeypatch.setattr(autopilot, "get_admin_user_id", lambda **_: "user-1")
    monkeypatch.setattr(
        autopilot, "get_connector_rollout_config", _autopilot_config_for
    )
    monkeypatch.setattr(
        autopilot,
        "estimate_tier_eligible_actors",
        lambda **_: _tier_estimate("TIER_2", 0),
    )

    def _fail(**_: object) -> dict:
        raise AssertionError("dry run must not finalize")

    monkeypatch.setattr(autopilot.api_client, "finalize_connector_rollout", _fail)

    result = autopilot.run_auto_advance(
        auth=ResolvedCloudAuth(bearer_token="t"), dry_run=True
    )

    assert [a.action for a in result.actions] == ["complete"]
    assert not result.errors


@pytest.mark.unit
def test_run_auto_advance_unavailable_estimate_skips(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """An unavailable estimate skips rather than finalizing a tier it can't confirm."""
    row = {
        "rollout_id": "rollout-1",
        "actor_definition_id": "def-1",
        "state": "workflow_started",
        "rc_docker_repository": "airbyte/source-faker",
        "rc_docker_image_tag": "7.2.0-rc.1",
        "tag": "TIER_2",
        "current_target_rollout_pct": 0,
        "final_target_rollout_pct": 100,
    }
    monkeypatch.setattr(autopilot, "query_connector_rollouts", lambda **_: [row])
    monkeypatch.setattr(autopilot, "get_admin_user_id", lambda **_: "user-1")
    monkeypatch.setattr(
        autopilot, "get_connector_rollout_config", _autopilot_config_for
    )
    monkeypatch.setattr(
        autopilot,
        "estimate_tier_eligible_actors",
        lambda **_: _tier_estimate("TIER_2", -1),
    )

    def _fail(**_: object) -> dict:
        raise AssertionError("unavailable estimate must not finalize")

    monkeypatch.setattr(autopilot.api_client, "finalize_connector_rollout", _fail)

    result = autopilot.run_auto_advance(
        auth=ResolvedCloudAuth(bearer_token="t"), dry_run=False
    )

    assert not result.actions
    assert len(result.skipped) == 1


@pytest.mark.unit
def test_run_auto_promote_ga_when_no_later_tier_has_actors(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """No later customer tier has actors → finalize current tier to GA."""
    row = {
        "rollout_id": "rollout-1",
        "actor_definition_id": "def-1",
        "state": "in_progress",
        "rc_docker_repository": "airbyte/source-faker",
        "rc_docker_image_tag": "7.2.0-rc.1",
        "tag": "TIER_2",
        "current_target_rollout_pct": 100,
        "final_target_rollout_pct": 100,
    }
    monkeypatch.setattr(autopilot, "query_connector_rollouts", lambda **_: [row])
    monkeypatch.setattr(autopilot, "get_admin_user_id", lambda **_: "user-1")
    monkeypatch.setattr(
        autopilot, "get_connector_rollout_config", _autopilot_config_for
    )
    monkeypatch.setattr(autopilot.api_client, "get_actor_sync_info", lambda **_: {})
    monkeypatch.setattr(
        autopilot,
        "check_health_gate",
        lambda *_a, **_k: _FakeHealthGate(passed=True, reason="healthy"),
    )
    monkeypatch.setattr(
        autopilot,
        "estimate_tier_eligible_actors",
        lambda *, actor_definition_id, docker_repository, tier: _tier_estimate(tier, 0),
    )

    calls: list[dict] = []

    def _finalize(**kwargs: object) -> dict:
        calls.append(kwargs)
        return {}

    monkeypatch.setattr(autopilot.api_client, "finalize_connector_rollout", _finalize)

    result = autopilot.run_auto_promote(
        auth=ResolvedCloudAuth(bearer_token="t"), dry_run=False
    )

    assert len(calls) == 1
    assert calls[0]["state"] == "succeeded"
    assert calls[0]["rollout_id"] == "rollout-1"
    assert [a.action for a in result.actions] == ["promote"]
    assert not result.errors


@pytest.mark.unit
def test_run_auto_promote_skips_empty_intermediate_tier_and_starts_next(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """An empty intermediate tier is skipped; the next tier with actors is started."""
    row = {
        "rollout_id": "rollout-1",
        "actor_definition_id": "def-1",
        "state": "in_progress",
        "rc_docker_repository": "airbyte/source-faker",
        "rc_docker_image_tag": "7.2.0-rc.1",
        "tag": "TIER_2",
        "current_target_rollout_pct": 100,
        "final_target_rollout_pct": 100,
    }
    monkeypatch.setattr(autopilot, "query_connector_rollouts", lambda **_: [row])
    monkeypatch.setattr(autopilot, "get_admin_user_id", lambda **_: "user-1")
    monkeypatch.setattr(
        autopilot, "get_connector_rollout_config", _autopilot_config_for
    )
    # Non-empty sync info so the platform drift backstop does not fire.
    populated = {
        "data": {"actorSelectionInfo": {"numActorsEligibleOrAlreadyPinned": 5}}
    }
    monkeypatch.setattr(
        autopilot.api_client, "get_actor_sync_info", lambda **_: populated
    )
    monkeypatch.setattr(
        autopilot,
        "check_health_gate",
        lambda *_a, **_k: _FakeHealthGate(passed=True, reason="healthy"),
    )
    tier_counts = {"TIER_1": 0, "TIER_0": 5}
    monkeypatch.setattr(
        autopilot,
        "estimate_tier_eligible_actors",
        lambda *, actor_definition_id, docker_repository, tier: _tier_estimate(
            tier, tier_counts[tier]
        ),
    )

    started: list[dict] = []
    progressed: list[dict] = []

    def _start(**kwargs: object) -> dict:
        started.append(kwargs)
        return {"id": "rollout-2"}

    def _progress(**kwargs: object) -> dict:
        progressed.append(kwargs)
        return {}

    def _no_finalize(**_: object) -> dict:
        raise AssertionError("starting a tier must not finalize the current one")

    monkeypatch.setattr(autopilot.api_client, "start_connector_rollout", _start)
    monkeypatch.setattr(autopilot.api_client, "progress_connector_rollout", _progress)
    monkeypatch.setattr(
        autopilot.api_client, "finalize_connector_rollout", _no_finalize
    )

    result = autopilot.run_auto_promote(
        auth=ResolvedCloudAuth(bearer_token="t"), dry_run=False
    )

    assert len(started) == 1
    assert started[0]["customer_tier"] == "TIER_0"
    assert len(progressed) == 1
    assert [a.action for a in result.actions] == ["promote"]
    assert not result.errors


def _close_row(
    *,
    rollout_id: str,
    tag: str,
    actor_definition_id: str = "def-1",
    repo: str = "airbyte/destination-motherduck",
    state: str = "in_progress",
) -> dict:
    """Build a minimal raw rollout row for `run_auto_close` tests."""
    return {
        "rollout_id": rollout_id,
        "actor_definition_id": actor_definition_id,
        "state": state,
        "rc_docker_repository": repo,
        "rc_docker_image_tag": tag,
    }


def _manual_config_for(adid: str, rc_version: str) -> _FakeRolloutConfig:
    return _FakeRolloutConfig(
        default_rollout_mode=autopilot.RolloutMode.manual,
        autopilot_config=_FakeAutopilotConfig(),
    )


@pytest.mark.unit
def test_run_auto_close_cancels_rollout_already_ga(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A rollout whose RC is already the registry GA default is canceled (retain pins)."""
    row = _close_row(rollout_id="r-1", tag="0.2.4")
    monkeypatch.setattr(autopilot, "query_connector_rollouts", lambda **_: [row])
    monkeypatch.setattr(autopilot, "get_admin_user_id", lambda **_: "user-1")
    monkeypatch.setattr(
        autopilot, "get_connector_rollout_config", _autopilot_config_for
    )
    monkeypatch.setattr(
        autopilot, "get_registry_default_version", lambda _adid: "0.2.4"
    )

    calls: list[dict] = []

    def _finalize(**kwargs: object) -> dict:
        calls.append(kwargs)
        return {}

    monkeypatch.setattr(autopilot.api_client, "finalize_connector_rollout", _finalize)

    result = autopilot.run_auto_close(
        auth=ResolvedCloudAuth(bearer_token="t"), dry_run=False
    )

    assert len(calls) == 1
    assert calls[0]["rollout_id"] == "r-1"
    assert calls[0]["state"] == "canceled"
    assert calls[0]["failed_reason"] == "already_ga"
    assert calls[0]["retain_pins_on_cancellation"] is True
    assert [a.action for a in result.actions] == ["close"]
    assert not result.errors


@pytest.mark.unit
def test_run_auto_close_cancels_already_ga_rc_suffix_tag(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """An `X.Y.Z-rc.N` tag whose base version equals the GA default is canceled."""
    row = _close_row(rollout_id="r-rc", tag="0.2.4-rc.1")
    monkeypatch.setattr(autopilot, "query_connector_rollouts", lambda **_: [row])
    monkeypatch.setattr(autopilot, "get_admin_user_id", lambda **_: "user-1")
    monkeypatch.setattr(
        autopilot, "get_connector_rollout_config", _autopilot_config_for
    )
    monkeypatch.setattr(
        autopilot, "get_registry_default_version", lambda _adid: "0.2.4"
    )

    calls: list[dict] = []

    def _finalize(**kwargs: object) -> dict:
        calls.append(kwargs)
        return {}

    monkeypatch.setattr(autopilot.api_client, "finalize_connector_rollout", _finalize)

    result = autopilot.run_auto_close(
        auth=ResolvedCloudAuth(bearer_token="t"), dry_run=False
    )

    assert len(calls) == 1
    assert calls[0]["rollout_id"] == "r-rc"
    assert calls[0]["failed_reason"] == "already_ga"
    assert calls[0]["retain_pins_on_cancellation"] is True
    assert not result.errors


@pytest.mark.unit
def test_run_auto_close_supersedes_lower_version(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """With two active RCs, the lower version is canceled and the newer left alone."""
    rows = [
        _close_row(rollout_id="old", tag="0.2.4"),
        _close_row(rollout_id="new", tag="0.2.5"),
    ]
    monkeypatch.setattr(autopilot, "query_connector_rollouts", lambda **_: rows)
    monkeypatch.setattr(autopilot, "get_admin_user_id", lambda **_: "user-1")
    monkeypatch.setattr(
        autopilot, "get_connector_rollout_config", _autopilot_config_for
    )
    # Older GA default: neither active RC is already GA, so only supersession fires.
    monkeypatch.setattr(
        autopilot, "get_registry_default_version", lambda _adid: "0.2.3"
    )
    # The newer RC is the highest advertised candidate, so the catch-all leaves it.
    monkeypatch.setattr(
        autopilot, "get_registry_release_candidates", lambda _adid: ["0.2.5"]
    )

    calls: list[dict] = []

    def _finalize(**kwargs: object) -> dict:
        calls.append(kwargs)
        return {}

    monkeypatch.setattr(autopilot.api_client, "finalize_connector_rollout", _finalize)

    result = autopilot.run_auto_close(
        auth=ResolvedCloudAuth(bearer_token="t"), dry_run=False
    )

    assert len(calls) == 1
    assert calls[0]["rollout_id"] == "old"
    assert calls[0]["failed_reason"] == "superseded_by_newer_rc"
    assert calls[0]["retain_pins_on_cancellation"] is True
    assert [a.action for a in result.actions] == ["close"]


@pytest.mark.unit
def test_run_auto_close_dry_run_does_not_cancel(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Dry run reports the would-be cancellation without mutating."""
    row = _close_row(rollout_id="r-1", tag="0.2.4")
    monkeypatch.setattr(autopilot, "query_connector_rollouts", lambda **_: [row])
    monkeypatch.setattr(autopilot, "get_admin_user_id", lambda **_: "user-1")
    monkeypatch.setattr(
        autopilot, "get_connector_rollout_config", _autopilot_config_for
    )
    monkeypatch.setattr(
        autopilot, "get_registry_default_version", lambda _adid: "0.2.4"
    )

    def _fail(**_: object) -> dict:
        raise AssertionError("dry run must not finalize")

    monkeypatch.setattr(autopilot.api_client, "finalize_connector_rollout", _fail)

    result = autopilot.run_auto_close(
        auth=ResolvedCloudAuth(bearer_token="t"), dry_run=True
    )

    assert result.dry_run is True
    assert [a.action for a in result.actions] == ["close"]


@pytest.mark.unit
def test_run_auto_close_skips_non_autopilot(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A redundant rollout on a non-autopilot connector is skipped, not canceled."""
    row = _close_row(rollout_id="r-1", tag="0.2.4")
    monkeypatch.setattr(autopilot, "query_connector_rollouts", lambda **_: [row])
    monkeypatch.setattr(autopilot, "get_admin_user_id", lambda **_: "user-1")
    monkeypatch.setattr(autopilot, "get_connector_rollout_config", _manual_config_for)
    monkeypatch.setattr(
        autopilot, "get_registry_default_version", lambda _adid: "0.2.4"
    )

    def _fail(**_: object) -> dict:
        raise AssertionError("non-autopilot connector must not finalize")

    monkeypatch.setattr(autopilot.api_client, "finalize_connector_rollout", _fail)

    result = autopilot.run_auto_close(
        auth=ResolvedCloudAuth(bearer_token="t"), dry_run=False
    )

    assert not result.actions
    assert [a.action for a in result.skipped] == ["close"]


@pytest.mark.unit
def test_run_auto_close_noop_when_rc_not_redundant(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A single active RC that is the highest advertised candidate is left untouched."""
    row = _close_row(rollout_id="r-1", tag="0.2.5")
    monkeypatch.setattr(autopilot, "query_connector_rollouts", lambda **_: [row])
    monkeypatch.setattr(autopilot, "get_admin_user_id", lambda **_: "user-1")
    monkeypatch.setattr(
        autopilot, "get_connector_rollout_config", _autopilot_config_for
    )
    monkeypatch.setattr(
        autopilot, "get_registry_default_version", lambda _adid: "0.2.4"
    )
    monkeypatch.setattr(
        autopilot, "get_registry_release_candidates", lambda _adid: ["0.2.5"]
    )

    def _fail(**_: object) -> dict:
        raise AssertionError("a non-redundant rollout must not finalize")

    monkeypatch.setattr(autopilot.api_client, "finalize_connector_rollout", _fail)

    result = autopilot.run_auto_close(
        auth=ResolvedCloudAuth(bearer_token="t"), dry_run=False
    )

    assert not result.actions
    assert not result.errors
    assert not result.skipped


@pytest.mark.unit
def test_run_auto_close_closes_not_highest_candidate(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """An RC that is not the highest advertised candidate is closed via the catch-all."""
    row = _close_row(rollout_id="r-62", tag="0.3.62")
    monkeypatch.setattr(autopilot, "query_connector_rollouts", lambda **_: [row])
    monkeypatch.setattr(autopilot, "get_admin_user_id", lambda **_: "user-1")
    monkeypatch.setattr(
        autopilot, "get_connector_rollout_config", _autopilot_config_for
    )
    # RC is ahead of GA (not already_ga) but a higher candidate is advertised.
    monkeypatch.setattr(
        autopilot, "get_registry_default_version", lambda _adid: "0.3.61"
    )
    monkeypatch.setattr(
        autopilot,
        "get_registry_release_candidates",
        lambda _adid: ["0.3.62", "0.3.63"],
    )

    calls: list[dict] = []

    def _finalize(**kwargs: object) -> dict:
        calls.append(kwargs)
        return {}

    monkeypatch.setattr(autopilot.api_client, "finalize_connector_rollout", _finalize)

    result = autopilot.run_auto_close(
        auth=ResolvedCloudAuth(bearer_token="t"), dry_run=False
    )

    assert len(calls) == 1
    assert calls[0]["rollout_id"] == "r-62"
    assert calls[0]["failed_reason"] == "not_highest_candidate"
    assert calls[0]["retain_pins_on_cancellation"] is True
    assert [a.action for a in result.actions] == ["close"]


@pytest.mark.unit
def test_run_auto_close_keeps_highest_candidate_with_rc_suffix(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A healthy RC is kept when the advertised candidate key carries an `-rc.N` suffix.

    The compiled registry can key `releases.releaseCandidates` by the raw RC
    version string (e.g. `0.2.5-rc.1`). The catch-all must compare base versions
    on both sides so the highest advertised candidate is not wrongly closed.
    """
    row = _close_row(rollout_id="r-25rc", tag="0.2.5-rc.1")
    monkeypatch.setattr(autopilot, "query_connector_rollouts", lambda **_: [row])
    monkeypatch.setattr(autopilot, "get_admin_user_id", lambda **_: "user-1")
    monkeypatch.setattr(
        autopilot, "get_connector_rollout_config", _autopilot_config_for
    )
    # RC is ahead of GA (not already_ga) and is the highest advertised candidate.
    monkeypatch.setattr(
        autopilot, "get_registry_default_version", lambda _adid: "0.2.4"
    )
    monkeypatch.setattr(
        autopilot,
        "get_registry_release_candidates",
        lambda _adid: ["0.2.5-rc.1"],
    )

    def _fail(**_: object) -> dict:
        raise AssertionError("highest advertised candidate must not be closed")

    monkeypatch.setattr(autopilot.api_client, "finalize_connector_rollout", _fail)

    result = autopilot.run_auto_close(
        auth=ResolvedCloudAuth(bearer_token="t"), dry_run=False
    )

    assert not result.actions
    assert not result.errors


@pytest.mark.unit
def test_run_auto_close_closes_superseded_prerelease_of_same_base(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A suffixed RC is closed when a newer prerelease of the same base is advertised.

    When the rollout tag itself carries an explicit `-rc.N` suffix, matching is
    exact, so `0.2.5-rc.1` is superseded by an advertised `0.2.5-rc.2` even
    though they share a base version.
    """
    row = _close_row(rollout_id="r-25rc1", tag="0.2.5-rc.1")
    monkeypatch.setattr(autopilot, "query_connector_rollouts", lambda **_: [row])
    monkeypatch.setattr(autopilot, "get_admin_user_id", lambda **_: "user-1")
    monkeypatch.setattr(
        autopilot, "get_connector_rollout_config", _autopilot_config_for
    )
    monkeypatch.setattr(
        autopilot, "get_registry_default_version", lambda _adid: "0.2.4"
    )
    monkeypatch.setattr(
        autopilot,
        "get_registry_release_candidates",
        lambda _adid: ["0.2.5-rc.1", "0.2.5-rc.2"],
    )

    calls: list[dict] = []

    def _finalize(**kwargs: object) -> dict:
        calls.append(kwargs)
        return {}

    monkeypatch.setattr(autopilot.api_client, "finalize_connector_rollout", _finalize)

    result = autopilot.run_auto_close(
        auth=ResolvedCloudAuth(bearer_token="t"), dry_run=False
    )

    assert len(calls) == 1
    assert calls[0]["rollout_id"] == "r-25rc1"
    assert calls[0]["failed_reason"] == "not_highest_candidate"
    assert [a.action for a in result.actions] == ["close"]


@pytest.mark.unit
def test_run_auto_close_skips_when_candidates_all_unparseable(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The catch-all fails closed when advertised candidates are all non-semver.

    A non-empty candidate list whose keys are all unparseable means the highest
    candidate cannot be determined, so the rollout is left alone (distinct from
    an empty list, which means nothing is advertised and closes the rollout).
    """
    row = _close_row(rollout_id="r-junk", tag="0.2.5")
    monkeypatch.setattr(autopilot, "query_connector_rollouts", lambda **_: [row])
    monkeypatch.setattr(autopilot, "get_admin_user_id", lambda **_: "user-1")
    monkeypatch.setattr(
        autopilot, "get_connector_rollout_config", _autopilot_config_for
    )
    monkeypatch.setattr(
        autopilot, "get_registry_default_version", lambda _adid: "0.2.4"
    )
    monkeypatch.setattr(
        autopilot,
        "get_registry_release_candidates",
        lambda _adid: ["not-a-version", "latest"],
    )

    def _fail(**_: object) -> dict:
        raise AssertionError("unparseable candidates must not finalize")

    monkeypatch.setattr(autopilot.api_client, "finalize_connector_rollout", _fail)

    result = autopilot.run_auto_close(
        auth=ResolvedCloudAuth(bearer_token="t"), dry_run=False
    )

    assert not result.actions
    assert not result.errors


@pytest.mark.unit
def test_run_auto_close_closes_when_no_candidate_advertised(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A rollout is closed when the registry advertises no release candidate."""
    row = _close_row(rollout_id="r-380", tag="3.8.0")
    monkeypatch.setattr(autopilot, "query_connector_rollouts", lambda **_: [row])
    monkeypatch.setattr(autopilot, "get_admin_user_id", lambda **_: "user-1")
    monkeypatch.setattr(
        autopilot, "get_connector_rollout_config", _autopilot_config_for
    )
    # RC differs from GA (not already_ga), and no candidate is advertised.
    monkeypatch.setattr(
        autopilot, "get_registry_default_version", lambda _adid: "3.8.1"
    )
    monkeypatch.setattr(autopilot, "get_registry_release_candidates", lambda _adid: [])

    calls: list[dict] = []

    def _finalize(**kwargs: object) -> dict:
        calls.append(kwargs)
        return {}

    monkeypatch.setattr(autopilot.api_client, "finalize_connector_rollout", _finalize)

    result = autopilot.run_auto_close(
        auth=ResolvedCloudAuth(bearer_token="t"), dry_run=False
    )

    assert len(calls) == 1
    assert calls[0]["rollout_id"] == "r-380"
    assert calls[0]["failed_reason"] == "not_highest_candidate"
    assert calls[0]["retain_pins_on_cancellation"] is True
    assert [a.action for a in result.actions] == ["close"]


@pytest.mark.unit
def test_run_auto_close_skips_when_registry_unresolved(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The catch-all fails closed: an unresolved registry leaves the rollout alone."""
    row = _close_row(rollout_id="r-1", tag="0.2.9")
    monkeypatch.setattr(autopilot, "query_connector_rollouts", lambda **_: [row])
    monkeypatch.setattr(autopilot, "get_admin_user_id", lambda **_: "user-1")
    monkeypatch.setattr(
        autopilot, "get_connector_rollout_config", _autopilot_config_for
    )
    # RC differs from GA (not already_ga); registry candidate lookup unresolved.
    monkeypatch.setattr(
        autopilot, "get_registry_default_version", lambda _adid: "0.2.4"
    )
    monkeypatch.setattr(
        autopilot, "get_registry_release_candidates", lambda _adid: None
    )

    def _fail(**_: object) -> dict:
        raise AssertionError("unresolved registry must not finalize")

    monkeypatch.setattr(autopilot.api_client, "finalize_connector_rollout", _fail)

    result = autopilot.run_auto_close(
        auth=ResolvedCloudAuth(bearer_token="t"), dry_run=False
    )

    assert not result.actions
    assert not result.errors
    assert not result.skipped
