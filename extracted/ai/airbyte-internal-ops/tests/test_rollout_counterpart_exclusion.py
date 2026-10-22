"""Tests for rollout counterpart-failure exclusion."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Literal
from unittest.mock import Mock

import pytest

from airbyte_ops_mcp.connector_ops.rollouts import _helpers
from airbyte_ops_mcp.connector_ops.rollouts.constants import RolloutStrategy
from airbyte_ops_mcp.connector_ops.rollouts.models import ConnectorRolloutRecord
from airbyte_ops_mcp.prod_db_access import queries
from airbyte_ops_mcp.prod_db_access.sql import (
    SELECT_LATEST_RC_COUNTERPART_FAILURES_FOR_DESTINATION_ROLLOUT,
    SELECT_LATEST_RC_COUNTERPART_FAILURES_FOR_SOURCE_ROLLOUT,
)


def _rollout(
    *,
    connector_name: str = "source-faker",
    release_candidate_version_id: str | None = "rc-version",
    created_at: datetime | None = datetime(2025, 1, 1, tzinfo=timezone.utc),
) -> ConnectorRolloutRecord:
    """Build a rollout record with enough metadata for counterpart lookup."""
    return ConnectorRolloutRecord.from_db_row(
        {
            "rollout_id": "rollout-1",
            "actor_definition_id": "definition-1",
            "release_candidate_version_id": release_candidate_version_id,
            "state": "in_progress",
            "rc_docker_repository": f"airbyte/{connector_name}",
            "created_at": created_at,
            "updated_at": datetime.now(timezone.utc) - timedelta(hours=5),
            "tag": "TIER_2",
        }
    )


@pytest.mark.unit
def test_query_latest_rc_counterpart_failures_skips_empty_actor_ids(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    run_sql_query = Mock()
    monkeypatch.setattr(queries, "_run_sql_query", run_sql_query)

    assert (
        queries.query_latest_rc_counterpart_failures(
            actor_type="destination",
            actor_ids=[],
            rc_version_id="rc-version",
            created_at_start=datetime(2025, 1, 1, tzinfo=timezone.utc),
        )
        == []
    )
    run_sql_query.assert_not_called()


@pytest.mark.unit
@pytest.mark.parametrize(
    ("actor_type", "statement", "excluded_origin", "query_name"),
    [
        pytest.param(
            "destination",
            SELECT_LATEST_RC_COUNTERPART_FAILURES_FOR_DESTINATION_ROLLOUT,
            "source",
            "SELECT_LATEST_RC_COUNTERPART_FAILURES_FOR_DESTINATION_ROLLOUT",
            id="destination-rollout-excludes-source-origin",
        ),
        pytest.param(
            "source",
            SELECT_LATEST_RC_COUNTERPART_FAILURES_FOR_SOURCE_ROLLOUT,
            "destination",
            "SELECT_LATEST_RC_COUNTERPART_FAILURES_FOR_SOURCE_ROLLOUT",
            id="source-rollout-excludes-destination-origin",
        ),
    ],
)
def test_query_latest_rc_counterpart_failures_selects_actor_query(
    monkeypatch: pytest.MonkeyPatch,
    actor_type: Literal["source", "destination"],
    statement: object,
    excluded_origin: str,
    query_name: str,
) -> None:
    run_sql_query = Mock(return_value=[{"actor_id": "actor-1"}])
    monkeypatch.setattr(queries, "_run_sql_query", run_sql_query)
    created_at_start = datetime(2025, 1, 1, tzinfo=timezone.utc)

    result = queries.query_latest_rc_counterpart_failures(
        actor_type=actor_type,
        actor_ids=["actor-1"],
        rc_version_id="rc-version",
        created_at_start=created_at_start,
    )

    assert result == [{"actor_id": "actor-1"}]
    run_sql_query.assert_called_once_with(
        statement,
        parameters={
            "actor_ids": ["actor-1"],
            "rc_version_id": "rc-version",
            "created_at_start": created_at_start,
            "excluded_origin": excluded_origin,
        },
        query_name=query_name,
        gsm_client=None,
    )


@pytest.mark.unit
def test_exclude_counterpart_failures_adjusts_counts_and_does_not_mutate_input(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    sync_info = {
        "data": {
            "syncs": {
                "ACTOR-ONE": {"numSucceeded": 0, "numFailed": 2},
                "Actor-Two": {"num_succeeded": 0, "num_failed": 1},
                "healthy-actor": {"numSucceeded": 2, "numFailed": 0},
            }
        }
    }
    original_sync_info = {
        "data": {
            "syncs": {
                "ACTOR-ONE": {"numSucceeded": 0, "numFailed": 2},
                "Actor-Two": {"num_succeeded": 0, "num_failed": 1},
                "healthy-actor": {"numSucceeded": 2, "numFailed": 0},
            }
        }
    }
    query = Mock(
        return_value=[
            {"actor_id": "actor-one"},
            {"actor_id": "actor-two"},
        ]
    )
    monkeypatch.setattr(
        "airbyte_ops_mcp.connector_ops.rollouts._helpers.query_latest_rc_counterpart_failures",
        query,
    )
    rollout = _rollout(
        connector_name="destination-faker",
        created_at=datetime(2025, 1, 1, 2, tzinfo=timezone(timedelta(hours=2))),
    )

    adjusted, excluded = _helpers.exclude_counterpart_failures(rollout, sync_info)

    assert excluded == 2
    assert adjusted["data"]["syncs"]["ACTOR-ONE"]["numFailed"] == 1
    assert adjusted["data"]["syncs"]["Actor-Two"]["num_failed"] == 0
    assert adjusted["data"]["syncs"]["healthy-actor"] == {
        "numSucceeded": 2,
        "numFailed": 0,
    }
    assert adjusted is not sync_info
    assert sync_info == original_sync_info
    query.assert_called_once_with(
        actor_type="destination",
        actor_ids=["ACTOR-ONE", "Actor-Two"],
        rc_version_id="rc-version",
        created_at_start=datetime(2025, 1, 1, tzinfo=timezone.utc),
    )


@pytest.mark.unit
def test_exclude_counterpart_failures_uses_source_rollout_query(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    query = Mock(return_value=[{"actor_id": "actor-1"}])
    monkeypatch.setattr(
        "airbyte_ops_mcp.connector_ops.rollouts._helpers.query_latest_rc_counterpart_failures",
        query,
    )
    sync_info = {"syncs": {"actor-1": {"numFailed": 1, "numSucceeded": 0}}}

    adjusted, excluded = _helpers.exclude_counterpart_failures(_rollout(), sync_info)

    assert excluded == 1
    assert adjusted["syncs"]["actor-1"]["numFailed"] == 0
    query.assert_called_once()
    assert query.call_args.kwargs["actor_type"] == "source"


@pytest.mark.unit
def test_exclude_counterpart_failures_skips_query_without_failing_actors(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    query = Mock()
    monkeypatch.setattr(
        "airbyte_ops_mcp.connector_ops.rollouts._helpers.query_latest_rc_counterpart_failures",
        query,
    )
    sync_info = {"syncs": {"actor-1": {"numFailed": 0, "numSucceeded": 1}}}

    adjusted, excluded = _helpers.exclude_counterpart_failures(_rollout(), sync_info)

    assert adjusted is sync_info
    assert excluded == 0
    query.assert_not_called()


@pytest.mark.unit
@pytest.mark.parametrize(
    "rollout",
    [
        pytest.param(
            _rollout(release_candidate_version_id=None),
            id="missing-release-candidate-version",
        ),
        pytest.param(_rollout(created_at=None), id="missing-rollout-created-at"),
    ],
)
def test_exclude_counterpart_failures_skips_query_without_rollout_metadata(
    monkeypatch: pytest.MonkeyPatch,
    rollout: ConnectorRolloutRecord,
) -> None:
    query = Mock()
    monkeypatch.setattr(
        "airbyte_ops_mcp.connector_ops.rollouts._helpers.query_latest_rc_counterpart_failures",
        query,
    )
    sync_info = {"syncs": {"actor-1": {"numFailed": 1, "numSucceeded": 0}}}

    adjusted, excluded = _helpers.exclude_counterpart_failures(rollout, sync_info)

    assert adjusted is sync_info
    assert excluded == 0
    query.assert_not_called()


@pytest.mark.unit
def test_exclude_counterpart_failures_fails_open_on_query_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    query = Mock(side_effect=RuntimeError("query unavailable"))
    monkeypatch.setattr(
        "airbyte_ops_mcp.connector_ops.rollouts._helpers.query_latest_rc_counterpart_failures",
        query,
    )
    sync_info = {"syncs": {"actor-1": {"numFailed": 1, "numSucceeded": 0}}}

    adjusted, excluded = _helpers.exclude_counterpart_failures(_rollout(), sync_info)

    assert adjusted is sync_info
    assert excluded == 0


@pytest.mark.unit
def test_excluded_failures_can_turn_a_tripping_gate_into_a_pass(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    syncs = {
        **{
            f"failing-{actor_id}": {"numSucceeded": 0, "numFailed": 1}
            for actor_id in range(40)
        },
        **{
            f"succeeded-{actor_id}": {"numSucceeded": 1, "numFailed": 0}
            for actor_id in range(460)
        },
    }
    sync_info = {
        "data": {
            "actorSelectionInfo": {"numPinnedToConnectorRollout": 500},
            "syncs": syncs,
        }
    }
    query = Mock(
        return_value=[{"actor_id": f"failing-{actor_id}"} for actor_id in range(30)]
    )
    monkeypatch.setattr(
        "airbyte_ops_mcp.connector_ops.rollouts._helpers.query_latest_rc_counterpart_failures",
        query,
    )
    rollout = _rollout(connector_name="destination-faker")

    adjusted, excluded = _helpers.exclude_counterpart_failures(rollout, sync_info)
    gate = _helpers.check_health_gate(
        rollout,
        adjusted,
        RolloutStrategy.FAST,
        excluded_counterpart_failures=excluded,
    )
    gate_without_exclusion = _helpers.check_health_gate(
        rollout,
        sync_info,
        RolloutStrategy.FAST,
    )

    assert gate.passed is True
    assert gate.should_rollback is False
    assert gate.failed_actor_count == 10
    assert gate.actors_with_sync_signal == 470
    assert gate.excluded_counterpart_failures == 30
    assert "30 counterpart-origin failures excluded" in gate.reason
    assert gate_without_exclusion.should_rollback is True


@pytest.mark.unit
def test_counterpart_exclusion_reduces_failures_before_count_threshold(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    syncs = {
        **{
            f"failing-{actor_id}": {"numSucceeded": 0, "numFailed": 1}
            for actor_id in range(55)
        },
        **{
            f"succeeded-{actor_id}": {"numSucceeded": 1, "numFailed": 0}
            for actor_id in range(1945)
        },
    }
    sync_info = {
        "data": {
            "actorSelectionInfo": {"numPinnedToConnectorRollout": 2000},
            "syncs": syncs,
        }
    }
    query = Mock(
        return_value=[{"actor_id": f"failing-{actor_id}"} for actor_id in range(10)]
    )
    monkeypatch.setattr(
        "airbyte_ops_mcp.connector_ops.rollouts._helpers.query_latest_rc_counterpart_failures",
        query,
    )
    rollout = _rollout(connector_name="destination-faker")

    adjusted, excluded = _helpers.exclude_counterpart_failures(rollout, sync_info)
    gate_with_exclusion = _helpers.check_health_gate(
        rollout,
        adjusted,
        RolloutStrategy.FAST,
        excluded_counterpart_failures=excluded,
    )

    query.return_value = []
    unadjusted, no_exclusions = _helpers.exclude_counterpart_failures(
        rollout, sync_info
    )
    gate_without_exclusion = _helpers.check_health_gate(
        rollout,
        unadjusted,
        RolloutStrategy.FAST,
        excluded_counterpart_failures=no_exclusions,
    )

    assert excluded == 10
    assert gate_with_exclusion.should_rollback is False
    assert gate_with_exclusion.failed_actor_count == 45
    assert "count >= 50" not in gate_with_exclusion.reason
    assert no_exclusions == 0
    assert gate_without_exclusion.should_rollback is True
    assert gate_without_exclusion.failed_actor_count == 55
    assert "count >= 50" in gate_without_exclusion.reason


@pytest.mark.unit
def test_tripped_gate_reason_reports_excluded_counterpart_failures() -> None:
    syncs = {
        **{
            f"failing-{actor_id}": {"numSucceeded": 0, "numFailed": 1}
            for actor_id in range(40)
        },
        **{
            f"succeeded-{actor_id}": {"numSucceeded": 1, "numFailed": 0}
            for actor_id in range(460)
        },
    }
    sync_info = {
        "data": {
            "actorSelectionInfo": {"numPinnedToConnectorRollout": 500},
            "syncs": syncs,
        }
    }

    gate = _helpers.check_health_gate(
        _rollout(),
        sync_info,
        RolloutStrategy.FAST,
        excluded_counterpart_failures=30,
    )

    assert gate.should_rollback is True
    assert gate.excluded_counterpart_failures == 30
    assert "30 counterpart-origin failures excluded" in gate.reason
