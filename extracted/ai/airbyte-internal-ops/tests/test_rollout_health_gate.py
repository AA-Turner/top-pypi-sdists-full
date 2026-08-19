# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Unit tests for the autopilot health gate's failure-rate threshold."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest

from airbyte_ops_mcp.connector_ops.rollouts._helpers import check_health_gate
from airbyte_ops_mcp.connector_ops.rollouts.constants import RolloutStrategy
from airbyte_ops_mcp.connector_ops.rollouts.models import ConnectorRolloutRecord


def _rollout() -> ConnectorRolloutRecord:
    """Build an `in_progress` rollout record last updated an hour ago."""
    return ConnectorRolloutRecord.from_db_row(
        {
            "rollout_id": "rollout-1",
            "actor_definition_id": "def-1",
            "state": "in_progress",
            "rc_docker_repository": "airbyte/source-faker",
            "rc_docker_image_tag": "7.2.0-rc.1",
            "tag": "TIER_2",
            "current_target_rollout_pct": 100,
            "final_target_rollout_pct": 100,
            "updated_at": datetime.now(tz=timezone.utc) - timedelta(hours=1),
        }
    )


def _sync_info(
    *,
    failing: int,
    succeeding: int,
    failed_syncs_per_actor: int = 1,
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
            "actorSelectionInfo": {"numPinnedToConnectorRollout": failing + succeeding},
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
