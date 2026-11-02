"""Tests for typed lifecycle models and session clock selection."""

from dataclasses import FrozenInstanceError
from datetime import UTC, datetime, timedelta
from types import SimpleNamespace

import pytest

from agentic_devtools.cli.ci.agent_task_lifecycle import (
    AgentTaskInventory,
    AgentTaskLifecycle,
    AgentTaskSessionLifecycle,
    parse_lifecycle_timestamp,
    select_session_lifecycle_timestamp,
    select_valid_timestamp_alias,
    session_lifecycle_timestamp_values,
)
from agentic_devtools.cli.ci.models import (
    AgentTaskInventory as PublicAgentTaskInventory,
)
from agentic_devtools.cli.ci.models import (
    AgentTaskLifecycle as PublicAgentTaskLifecycle,
)
from agentic_devtools.cli.ci.models import (
    AgentTaskSessionLifecycle as PublicAgentTaskSessionLifecycle,
)

NOW = datetime(2026, 10, 16, 10, 0, tzinfo=UTC)


def test_selects_newest_eligible_clock_across_sessions() -> None:
    sessions = (
        AgentTaskSessionLifecycle(
            "new",
            "running",
            created_at=(NOW - timedelta(minutes=5)).isoformat(),
        ),
        AgentTaskSessionLifecycle(
            "old",
            "running",
            started_at=(NOW - timedelta(minutes=90)).isoformat(),
            created_at=(NOW - timedelta(minutes=1)).isoformat(),
        ),
    )

    assert select_session_lifecycle_timestamp(sessions) == NOW - timedelta(minutes=5)


def test_invalid_activity_clock_falls_back_to_session_creation() -> None:
    session = AgentTaskSessionLifecycle(
        "session",
        "running",
        started_at="not-a-timestamp",
        created_at=(NOW - timedelta(minutes=5)).isoformat(),
    )

    assert select_session_lifecycle_timestamp((session,)) == NOW - timedelta(minutes=5)


def test_session_activity_suppresses_newer_creation() -> None:
    session = AgentTaskSessionLifecycle(
        "session",
        "running",
        started_at=(NOW - timedelta(minutes=10)).isoformat(),
        created_at=(NOW - timedelta(minutes=1)).isoformat(),
    )

    assert select_session_lifecycle_timestamp((session,)) == NOW - timedelta(minutes=10)


def test_idle_timestamp_is_session_activity() -> None:
    session = AgentTaskSessionLifecycle(
        "session",
        "running",
        started_at=(NOW - timedelta(minutes=15)).isoformat(),
        idle_at=(NOW - timedelta(minutes=5)).isoformat(),
        created_at=(NOW - timedelta(minutes=1)).isoformat(),
    )

    assert select_session_lifecycle_timestamp((session,)) == NOW - timedelta(minutes=5)


def test_timestamp_alias_skips_invalid_earlier_alias() -> None:
    assert (
        select_valid_timestamp_alias(
            {"started_at": "invalid", "startedAt": "2026-10-16T09:55:00Z"},
            "started_at",
            "startedAt",
        )
        == "2026-10-16T09:55:00Z"
    )


def test_timestamp_alias_reads_metadata_and_preserves_unusable_values() -> None:
    assert (
        select_valid_timestamp_alias(
            {"started_at": "invalid", "metadata": {"startedAt": "2026-10-16T09:55:00Z"}},
            "started_at",
            "startedAt",
        )
        == "2026-10-16T09:55:00Z"
    )
    assert select_valid_timestamp_alias({"started_at": "invalid"}, "started_at") == "invalid"
    assert select_valid_timestamp_alias({}, "started_at") == ""


def test_timestamp_alias_selects_newest_value_across_fields_and_fallback() -> None:
    assert (
        select_valid_timestamp_alias(
            {"started_at": "2026-10-16T09:30:00Z", "startedAt": "2026-10-16T09:40:00Z"},
            "started_at",
            "startedAt",
            fallback={"started_at": "2026-10-16T09:55:00Z"},
        )
        == "2026-10-16T09:55:00Z"
    )


def test_timestamp_alias_ignores_non_mapping_metadata() -> None:
    assert select_valid_timestamp_alias({"metadata": None}, "started_at") == ""


def test_session_values_can_exclude_top_level_creation() -> None:
    assert session_lifecycle_timestamp_values({"createdAt": "2026-10-16T09:55:00Z"}, include_created=False) == (
        "",
        "",
        "",
    )
    assert session_lifecycle_timestamp_values(
        {
            "startedAt": "2026-10-16T09:50:00Z",
            "createdAt": "2026-10-16T09:55:00Z",
            "idleSince": "2026-10-16T09:58:00Z",
        }
    ) == ("2026-10-16T09:50:00Z", "2026-10-16T09:55:00Z", "2026-10-16T09:58:00Z")


@pytest.mark.parametrize("value", [None, "", "   ", "invalid"])
def test_timestamp_parser_rejects_missing_and_malformed_values(value: object) -> None:
    assert parse_lifecycle_timestamp(value) is None


def test_timestamp_parser_normalizes_naive_and_offset_values_to_utc() -> None:
    assert parse_lifecycle_timestamp("2026-10-16T09:55:00") == datetime(2026, 10, 16, 9, 55, tzinfo=UTC)
    assert parse_lifecycle_timestamp("2026-10-16T10:55:00+01:00") == datetime(2026, 10, 16, 9, 55, tzinfo=UTC)


def test_session_selector_returns_none_without_valid_clocks() -> None:
    assert select_session_lifecycle_timestamp(()) is None
    assert (
        select_session_lifecycle_timestamp(
            (
                AgentTaskSessionLifecycle(
                    "session",
                    "running",
                    created_at="",
                ),
            )
        )
        is None
    )
    assert (
        select_session_lifecycle_timestamp(
            (
                AgentTaskSessionLifecycle(
                    "session",
                    "running",
                    created_at="",
                    idle_at="",
                ),
            )
        )
        is None
    )
    assert (
        select_session_lifecycle_timestamp(
            (SimpleNamespace(started_at="", idle_at="", created_at="", updated_at=NOW.isoformat()),)
        )
        is None
    )


def test_models_reexport_extracted_lifecycle_dataclasses() -> None:
    assert PublicAgentTaskSessionLifecycle is AgentTaskSessionLifecycle
    assert PublicAgentTaskLifecycle is AgentTaskLifecycle
    assert PublicAgentTaskInventory is AgentTaskInventory
    session = PublicAgentTaskSessionLifecycle("session", "running")
    assert session.created_at == ""
    positional = PublicAgentTaskSessionLifecycle("session", "running", "start", "idle", "head", "run")
    assert (positional.head_sha, positional.workflow_run_id, positional.created_at) == ("head", "run", "")
    with pytest.raises(FrozenInstanceError):
        setattr(session, "created_at", "2026-10-16T09:55:00Z")
