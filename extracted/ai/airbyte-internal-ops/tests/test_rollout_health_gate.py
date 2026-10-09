# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Unit tests for the autopilot health gate's failure-rate threshold."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest
from zoneinfo import ZoneInfo

from airbyte_ops_mcp.connector_ops.rollouts._helpers import (
    HealthGateResult,
    check_health_gate,
    describe_gate_next_step,
    next_promotion_time,
)
from airbyte_ops_mcp.connector_ops.rollouts.constants import RolloutStrategy
from airbyte_ops_mcp.connector_ops.rollouts.models import ConnectorRolloutRecord


def _rollout(
    *,
    tier: str = "TIER_2",
    elapsed_hours: float = 1,
) -> ConnectorRolloutRecord:
    """Build an `in_progress` rollout record with a configurable tier and age."""
    return ConnectorRolloutRecord.from_db_row(
        {
            "rollout_id": "rollout-1",
            "actor_definition_id": "def-1",
            "state": "in_progress",
            "rc_docker_repository": "airbyte/source-faker",
            "rc_docker_image_tag": "7.2.0-rc.1",
            "tag": tier,
            "current_target_rollout_pct": 100,
            "final_target_rollout_pct": 100,
            "updated_at": datetime.now(tz=timezone.utc)
            - timedelta(hours=elapsed_hours),
        }
    )


def _sync_info(
    *,
    failing: int,
    succeeding: int,
    failed_syncs_per_actor: int = 1,
    pinned: int | None = None,
) -> dict:
    """Build a `get_actor_sync_info` payload with the given actor outcomes."""
    syncs: dict[str, dict[str, int]] = {
        f"failed-actor-{i}": {"numSucceeded": 0, "numFailed": failed_syncs_per_actor}
        for i in range(failing)
    }
    syncs.update(
        {
            f"ok-actor-{i}": {"numSucceeded": 1, "numFailed": 0}
            for i in range(succeeding)
        }
    )
    return {
        "data": {
            "actorSelectionInfo": {
                "numPinnedToConnectorRollout": (
                    failing + succeeding if pinned is None else pinned
                )
            },
            "syncs": syncs,
        }
    }


@pytest.mark.unit
@pytest.mark.parametrize("strategy", [RolloutStrategy.FAST, RolloutStrategy.SLOW])
@pytest.mark.parametrize(
    ("failing", "succeeding", "failed_syncs_per_actor", "expect_rollback"),
    [
        pytest.param(4, 96, 1, False, id="four_percent_tolerated"),
        pytest.param(5, 95, 1, True, id="five_percent_pauses"),
        pytest.param(20, 80, 1, True, id="twenty_percent_pauses"),
        pytest.param(1, 1, 1, False, id="count_floor_protects_tiny_cohort"),
        pytest.param(1, 99, 50, False, id="repeat_failures_are_one_connector"),
        pytest.param(0, 0, 1, False, id="no_sync_signal_yet"),
        pytest.param(49, 4951, 1, False, id="under_count_backstop_and_rate"),
        pytest.param(50, 4950, 1, True, id="count_backstop_pauses_under_rate"),
    ],
)
def test_check_health_gate_failure_rate(
    strategy: RolloutStrategy,
    failing: int,
    succeeding: int,
    failed_syncs_per_actor: int,
    expect_rollback: bool,
) -> None:
    """Rollback is recommended only at >=5% failing connectors above the floor."""
    gate = check_health_gate(
        _rollout(),
        _sync_info(
            failing=failing,
            succeeding=succeeding,
            failed_syncs_per_actor=failed_syncs_per_actor,
        ),
        strategy,
    )

    assert gate.should_rollback is expect_rollback
    assert gate.failed_actor_count == failing
    assert gate.failure_count == failing * failed_syncs_per_actor
    assert gate.actors_with_sync_signal == failing + succeeding
    if expect_rollback:
        assert gate.passed is False
        assert f"{failing} of {failing + succeeding} connectors failing" in gate.reason


@pytest.mark.unit
def test_fast_tier_2_small_cohort_passes_with_light_evidence() -> None:
    gate = check_health_gate(
        _rollout(elapsed_hours=5),
        _sync_info(failing=0, succeeding=1, pinned=3),
        RolloutStrategy.FAST,
    )

    assert gate.passed is True
    assert gate.light_evidence is True
    assert gate.num_pinned == 3


@pytest.mark.unit
def test_light_evidence_is_limited_to_fast_tier_2_and_tier_1() -> None:
    tier_0_gate = check_health_gate(
        _rollout(tier="TIER_0", elapsed_hours=5),
        _sync_info(failing=0, succeeding=1, pinned=3),
        RolloutStrategy.FAST,
    )
    tier_1_low_coverage = check_health_gate(
        _rollout(tier="TIER_1", elapsed_hours=5),
        _sync_info(failing=0, succeeding=1, pinned=20),
        RolloutStrategy.FAST,
    )
    slow_small_cohort = check_health_gate(
        _rollout(tier="TIER_2", elapsed_hours=10),
        _sync_info(failing=0, succeeding=1, pinned=3),
        RolloutStrategy.SLOW,
    )

    assert tier_0_gate.passed is False
    assert tier_0_gate.light_evidence is False
    assert tier_1_low_coverage.passed is False
    assert slow_small_cohort.passed is False
    assert slow_small_cohort.light_evidence is False


@pytest.mark.unit
@pytest.mark.parametrize(
    ("pinned", "succeeding", "passed"),
    [
        pytest.param(25, 3, True, id="coverage-at-least-ten-percent"),
        pytest.param(25, 2, False, id="coverage-below-ten-percent"),
    ],
)
def test_light_evidence_requires_ten_percent_coverage(
    pinned: int,
    succeeding: int,
    passed: bool,
) -> None:
    gate = check_health_gate(
        _rollout(tier="TIER_1", elapsed_hours=5),
        _sync_info(failing=0, succeeding=succeeding, pinned=pinned),
        RolloutStrategy.FAST,
    )

    assert gate.passed is passed
    assert gate.light_evidence is passed
    assert gate.num_pinned == pinned


@pytest.mark.unit
def test_light_evidence_does_not_pass_with_a_failing_actor() -> None:
    gate = check_health_gate(
        _rollout(elapsed_hours=5),
        _sync_info(failing=1, succeeding=2),
        RolloutStrategy.FAST,
    )

    assert gate.passed is False
    assert gate.light_evidence is False


@pytest.mark.unit
def test_light_evidence_does_not_pass_before_minimum_soak() -> None:
    gate = check_health_gate(
        _rollout(elapsed_hours=3),
        _sync_info(failing=0, succeeding=1, pinned=3),
        RolloutStrategy.FAST,
    )

    assert gate.passed is False
    assert gate.light_evidence is False


@pytest.mark.unit
def test_zero_syncs_remain_held_and_describe_max_soak() -> None:
    now = datetime.now(timezone.utc)
    gate = check_health_gate(
        _rollout(elapsed_hours=5),
        _sync_info(failing=0, succeeding=0),
        RolloutStrategy.FAST,
    )
    next_step = describe_gate_next_step(gate, RolloutStrategy.FAST, now)

    assert gate.passed is False
    assert "no successful syncs on this version yet" in next_step
    assert "auto-promotes at max soak" in next_step


@pytest.mark.unit
def test_next_step_describes_minimum_and_maximum_soak_times() -> None:
    gate = HealthGateResult(
        passed=False,
        reason="min soak",
        soak_elapsed_seconds=2 * 60 * 60,
        tier="TIER_2",
    )
    now = datetime(2024, 5, 9, 16, tzinfo=timezone.utc)

    next_step = describe_gate_next_step(gate, RolloutStrategy.FAST, now)

    assert next_step.startswith("next: check at Thu 18:00 UTC")
    assert "auto-promotes by Mon 07:00 UTC at the latest" in next_step
    assert next_step.endswith("(promotion paused Fri\u2013Sun PT)")


@pytest.mark.unit
def test_tier_0_small_cohort_status_explains_unreachable_success_count() -> None:
    gate = HealthGateResult(
        passed=False,
        reason="insufficient signal",
        soak_elapsed_seconds=5 * 60 * 60,
        actors_with_successful_syncs=1,
        num_pinned=2,
        tier="TIER_0",
    )

    next_step = describe_gate_next_step(
        gate,
        RolloutStrategy.FAST,
        datetime(2024, 5, 9, 16, tzinfo=timezone.utc),
    )

    assert next_step.startswith("only 2 pinned, can't reach 5 successes;")
    assert "next: re-check every 30m" in next_step


@pytest.mark.unit
def test_slow_max_soak_pass_keeps_light_evidence_false() -> None:
    gate = check_health_gate(
        _rollout(tier="TIER_2", elapsed_hours=29),
        _sync_info(failing=0, succeeding=1, pinned=3),
        RolloutStrategy.SLOW,
    )

    assert gate.passed is True
    assert gate.light_evidence is False


@pytest.mark.unit
def test_standard_signal_pass_keeps_light_evidence_false() -> None:
    gate = check_health_gate(
        _rollout(elapsed_hours=5),
        _sync_info(failing=0, succeeding=6, pinned=50),
        RolloutStrategy.FAST,
    )

    assert gate.passed is True
    assert gate.light_evidence is False


@pytest.mark.unit
def test_next_promotion_time_respects_pacific_weekend_pause() -> None:
    pacific = ZoneInfo("America/Los_Angeles")
    thursday = datetime(2024, 5, 9, 10, tzinfo=pacific)
    friday = datetime(2024, 5, 10, 10, tzinfo=pacific)
    sunday = datetime(2024, 5, 12, 23, tzinfo=pacific)

    assert next_promotion_time(thursday) == thursday
    assert next_promotion_time(friday) == datetime(
        2024, 5, 13, 0, tzinfo=pacific
    ).astimezone(timezone.utc)
    assert next_promotion_time(sunday) == datetime(
        2024, 5, 13, 0, tzinfo=pacific
    ).astimezone(timezone.utc)
