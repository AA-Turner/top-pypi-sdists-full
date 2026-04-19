"""Unit tests for the memory retention / eviction pipeline (#625)."""

from __future__ import annotations

import sqlite3
from datetime import datetime, timedelta, timezone
from typing import Any
from unittest.mock import MagicMock

import pytest

from anteroom.config import MemoryRetentionConfig
from anteroom.db import _SCHEMA, ThreadSafeConnection
from anteroom.services.memory_retention import (
    PurgeResult,
    _age_days,
    _eligible_by_status,
    _expired_by_age,
    _expired_by_idle,
    _idle_days,
    _is_pack_sourced,
    _is_pinned,
    _reason_for,
    purge_memories,
)
from anteroom.services.memory_service import (
    create_memory,
    pin_memory,
    update_memory_metadata,
)

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def db() -> ThreadSafeConnection:
    conn = sqlite3.connect(":memory:", check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys=ON")
    conn.executescript(_SCHEMA)
    conn.commit()
    return ThreadSafeConnection(conn)


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _backdate(db: ThreadSafeConnection, fqn: str, *, days_old: int) -> None:
    """Forcibly back-date an artifact's ``created_at`` and optionally its
    ``last_recalled_at``. Used to simulate aging without time.sleep."""
    ts = (_now() - timedelta(days=days_old)).isoformat()
    db.execute("UPDATE artifacts SET created_at = ? WHERE fqn = ?", (ts, fqn))
    db.commit()


def _set_last_recalled(db: ThreadSafeConnection, fqn: str, *, days_ago: int) -> None:
    ts = (_now() - timedelta(days=days_ago)).isoformat()
    update_memory_metadata(db, fqn, last_recalled_at=ts)


# ---------------------------------------------------------------------------
# Pure eligibility helpers
# ---------------------------------------------------------------------------


class TestEligibilityHelpers:
    def test_age_days_from_created_at(self) -> None:
        past = (_now() - timedelta(days=10)).isoformat()
        assert _age_days({"created_at": past}, _now()) >= 9  # floating by seconds

    def test_age_days_unparseable_is_zero(self) -> None:
        assert _age_days({"created_at": "not-a-date"}, _now()) == 0
        assert _age_days({}, _now()) == 0

    def test_idle_days_prefers_last_recalled(self) -> None:
        past = (_now() - timedelta(days=30)).isoformat()
        recent = (_now() - timedelta(days=2)).isoformat()
        art = {
            "created_at": past,
            "metadata": {"last_recalled_at": recent},
        }
        assert _idle_days(art, _now()) <= 3

    def test_idle_days_falls_back_to_created_at(self) -> None:
        past = (_now() - timedelta(days=20)).isoformat()
        art = {"created_at": past, "metadata": {}}
        assert _idle_days(art, _now()) >= 19

    def test_expired_by_age_none_disables(self) -> None:
        art = {"created_at": (_now() - timedelta(days=365)).isoformat()}
        assert _expired_by_age(art, _now(), None) is False

    def test_expired_by_idle_grace_floor(self) -> None:
        # Memory was created 2 days ago, min_age_days is 5 — even if it
        # has never been recalled, the grace floor blocks idle eviction.
        art = {"created_at": (_now() - timedelta(days=2)).isoformat(), "metadata": {}}
        assert _expired_by_idle(art, _now(), idle_days=1, min_age_days=5) is False
        # Past the grace floor it becomes eligible.
        old = {"created_at": (_now() - timedelta(days=10)).isoformat(), "metadata": {}}
        assert _expired_by_idle(old, _now(), idle_days=1, min_age_days=5) is True

    def test_eligible_by_status_matches(self) -> None:
        art = {"metadata": {"memory_status": "rejected"}}
        assert _eligible_by_status(art, ["rejected"]) is True
        assert _eligible_by_status(art, ["archived"]) is False

    def test_is_pinned_bool(self) -> None:
        assert _is_pinned({"metadata": {"pinned": True}}) is True
        assert _is_pinned({"metadata": {"pinned": False}}) is False
        assert _is_pinned({"metadata": {}}) is False

    def test_is_pack_sourced_skips_non_local(self) -> None:
        assert _is_pack_sourced({"source": "pack"}) is True
        assert _is_pack_sourced({"source": "local"}) is False

    def test_reason_for_order_max_age_wins(self) -> None:
        art = {
            "created_at": (_now() - timedelta(days=120)).isoformat(),
            "metadata": {"memory_status": "rejected"},
        }
        policy = MemoryRetentionConfig(
            enabled=True,
            max_age_days=30,
            idle_days=10,
            purge_statuses=["rejected"],
        )
        assert _reason_for(art, policy, _now()) == "max_age"

    def test_reason_for_returns_none_when_ineligible(self) -> None:
        art = {
            "created_at": (_now() - timedelta(days=1)).isoformat(),
            "metadata": {"memory_status": "active"},
        }
        policy = MemoryRetentionConfig(
            enabled=True,
            max_age_days=30,
            purge_statuses=["rejected"],
        )
        assert _reason_for(art, policy, _now()) is None


# ---------------------------------------------------------------------------
# purge_memories — end-to-end via in-memory DB
# ---------------------------------------------------------------------------


class TestPurgeMemories:
    def test_disabled_policy_is_no_op(self, db: ThreadSafeConnection) -> None:
        create_memory(db, "x", scope="user", category="preference", name="off1")
        result = purge_memories(db, MemoryRetentionConfig(enabled=False))
        assert result.purged_count == 0
        assert result.items == []

    def test_rejected_status_purged(self, db: ThreadSafeConnection) -> None:
        art = create_memory(db, "x", scope="user", category="preference", name="rs1")
        update_memory_metadata(db, art["fqn"], memory_status="rejected")
        result = purge_memories(
            db,
            MemoryRetentionConfig(enabled=True, purge_statuses=["rejected"]),
        )
        assert result.purged_count == 1
        assert result.items[0].reason == "status"
        assert result.items[0].fqn == art["fqn"]

    def test_active_memory_not_purged(self, db: ThreadSafeConnection) -> None:
        create_memory(db, "x", scope="user", category="preference", name="act1")
        result = purge_memories(
            db,
            MemoryRetentionConfig(enabled=True, purge_statuses=["rejected"]),
        )
        assert result.purged_count == 0

    def test_max_age_days(self, db: ThreadSafeConnection) -> None:
        art = create_memory(db, "x", scope="user", category="preference", name="ma1")
        _backdate(db, art["fqn"], days_old=45)
        result = purge_memories(
            db,
            MemoryRetentionConfig(enabled=True, max_age_days=30, purge_statuses=[]),
        )
        assert result.purged_count == 1
        assert result.items[0].reason == "max_age"

    def test_idle_days_with_last_recalled(self, db: ThreadSafeConnection) -> None:
        art = create_memory(db, "x", scope="user", category="preference", name="id1")
        _backdate(db, art["fqn"], days_old=50)
        _set_last_recalled(db, art["fqn"], days_ago=40)
        result = purge_memories(
            db,
            MemoryRetentionConfig(enabled=True, idle_days=30, min_age_days=1, purge_statuses=[]),
        )
        assert result.purged_count == 1
        assert result.items[0].reason == "idle"

    def test_idle_days_grace_floor_blocks_fresh(self, db: ThreadSafeConnection) -> None:
        # Created 3 days ago, min_age_days is 7 — idle eviction must skip.
        art = create_memory(db, "x", scope="user", category="preference", name="id2")
        _backdate(db, art["fqn"], days_old=3)
        result = purge_memories(
            db,
            MemoryRetentionConfig(enabled=True, idle_days=1, min_age_days=7, purge_statuses=[]),
        )
        assert result.purged_count == 0

    def test_pinned_memory_skipped_by_default(self, db: ThreadSafeConnection) -> None:
        art = create_memory(db, "x", scope="user", category="preference", name="p1")
        update_memory_metadata(db, art["fqn"], memory_status="rejected")
        pin_memory(db, art["fqn"])
        result = purge_memories(
            db,
            MemoryRetentionConfig(enabled=True, purge_statuses=["rejected"]),
        )
        assert result.purged_count == 0
        assert result.skipped_pinned_count == 1

    def test_pinned_memory_purged_when_respect_pins_false(self, db: ThreadSafeConnection) -> None:
        art = create_memory(db, "x", scope="user", category="preference", name="p2")
        update_memory_metadata(db, art["fqn"], memory_status="rejected")
        pin_memory(db, art["fqn"])
        result = purge_memories(
            db,
            MemoryRetentionConfig(
                enabled=True,
                purge_statuses=["rejected"],
                respect_pins=False,
            ),
        )
        assert result.purged_count == 1
        assert result.skipped_pinned_count == 0

    def test_dry_run_returns_candidates_without_deleting(self, db: ThreadSafeConnection) -> None:
        art = create_memory(db, "x", scope="user", category="preference", name="d1")
        update_memory_metadata(db, art["fqn"], memory_status="rejected")
        result = purge_memories(
            db,
            MemoryRetentionConfig(enabled=True, purge_statuses=["rejected"]),
            dry_run=True,
        )
        assert result.dry_run is True
        assert result.purged_count == 1
        # DB unchanged.
        from anteroom.services.memory_service import get_memory

        assert get_memory(db, art["fqn"]) is not None

    def test_non_local_source_never_purged(self, db: ThreadSafeConnection) -> None:
        # Artifacts sourced from a pack / team / project layer must not be
        # evicted — they'd re-install on the next pack sync. Simulate by
        # mutating the source column to one of the non-local enum values
        # allowed by the schema.
        art = create_memory(db, "x", scope="user", category="preference", name="pk1")
        update_memory_metadata(db, art["fqn"], memory_status="rejected")
        db.execute("UPDATE artifacts SET source = 'team' WHERE id = ?", (art["id"],))
        db.commit()
        result = purge_memories(
            db,
            MemoryRetentionConfig(enabled=True, purge_statuses=["rejected"]),
        )
        assert result.purged_count == 0


# ---------------------------------------------------------------------------
# Audit integration
# ---------------------------------------------------------------------------


class TestPurgeAudit:
    def test_audit_emitted_per_purged_memory(self, db: ThreadSafeConnection) -> None:
        for i in range(3):
            art = create_memory(db, f"x{i}", scope="user", category="preference", name=f"au{i}")
            update_memory_metadata(db, art["fqn"], memory_status="rejected")
        audit_writer = MagicMock()
        result = purge_memories(
            db,
            MemoryRetentionConfig(enabled=True, purge_statuses=["rejected"]),
            audit_writer=audit_writer,
        )
        assert result.purged_count == 3
        assert audit_writer.emit.call_count == 3
        # Every emitted entry has the expected shape.
        for call in audit_writer.emit.call_args_list:
            entry = call.args[0]
            assert entry.event_type == "memory.purge"
            assert set(entry.details.keys()) == {
                "fqn",
                "reason",
                "age_days",
                "last_recalled_at",
                "recall_count",
                "status",
                "pinned",
                "reviewer_id",
                "triggered_by",
            }
            # Content is never logged.
            assert "content" not in entry.details
            assert "message_content" not in entry.details
            # Scheduler path: no reviewer identity stamped.
            assert entry.user_id == ""
            assert entry.details["reviewer_id"] is None
            assert entry.details["triggered_by"] == "scheduler"

    def test_dry_run_does_not_emit(self, db: ThreadSafeConnection) -> None:
        art = create_memory(db, "x", scope="user", category="preference", name="dre1")
        update_memory_metadata(db, art["fqn"], memory_status="rejected")
        audit_writer = MagicMock()
        purge_memories(
            db,
            MemoryRetentionConfig(enabled=True, purge_statuses=["rejected"]),
            dry_run=True,
            audit_writer=audit_writer,
        )
        audit_writer.emit.assert_not_called()

    def test_audit_writer_none_safe_passthrough(self, db: ThreadSafeConnection) -> None:
        art = create_memory(db, "x", scope="user", category="preference", name="an1")
        update_memory_metadata(db, art["fqn"], memory_status="rejected")
        result = purge_memories(
            db,
            MemoryRetentionConfig(enabled=True, purge_statuses=["rejected"]),
            audit_writer=None,
        )
        assert result.purged_count == 1

    def test_audit_emit_failure_does_not_abort(self, db: ThreadSafeConnection) -> None:
        # Per the service docstring, an audit failure must never abort
        # the retention pass — the purge still completes.
        art = create_memory(db, "x", scope="user", category="preference", name="af1")
        update_memory_metadata(db, art["fqn"], memory_status="rejected")
        audit_writer = MagicMock()
        audit_writer.emit.side_effect = RuntimeError("audit sink offline")
        result = purge_memories(
            db,
            MemoryRetentionConfig(enabled=True, purge_statuses=["rejected"]),
            audit_writer=audit_writer,
        )
        assert result.purged_count == 1


class TestReviewerIdentity:
    """The on-demand purge path stamps a reviewer id on the audit trail
    and returns it in PurgeResult.purged_by. The scheduled worker path
    leaves reviewer_id None (the existing TestPurgeAudit case covers
    the scheduler side of this contract)."""

    def test_reviewer_id_stamped_on_audit_entry(self, db: ThreadSafeConnection) -> None:
        art = create_memory(db, "x", scope="user", category="preference", name="rvr1")
        update_memory_metadata(db, art["fqn"], memory_status="rejected")
        audit_writer = MagicMock()
        purge_memories(
            db,
            MemoryRetentionConfig(enabled=True, purge_statuses=["rejected"]),
            audit_writer=audit_writer,
            reviewer_id="reviewer-alice",
        )
        entry = audit_writer.emit.call_args.args[0]
        assert entry.event_type == "memory.purge"
        assert entry.user_id == "reviewer-alice"
        assert entry.details["reviewer_id"] == "reviewer-alice"
        assert entry.details["triggered_by"] == "reviewer"

    def test_purged_by_echoed_in_result(self, db: ThreadSafeConnection) -> None:
        art = create_memory(db, "x", scope="user", category="preference", name="rvr2")
        update_memory_metadata(db, art["fqn"], memory_status="rejected")
        result = purge_memories(
            db,
            MemoryRetentionConfig(enabled=True, purge_statuses=["rejected"]),
            reviewer_id="reviewer-bob",
        )
        assert result.purged_by == "reviewer-bob"

    def test_scheduler_path_leaves_purged_by_none(self, db: ThreadSafeConnection) -> None:
        art = create_memory(db, "x", scope="user", category="preference", name="rvr3")
        update_memory_metadata(db, art["fqn"], memory_status="rejected")
        result = purge_memories(
            db,
            MemoryRetentionConfig(enabled=True, purge_statuses=["rejected"]),
        )
        assert result.purged_by is None

    def test_different_reviewers_produce_different_audit_entries(self, db: ThreadSafeConnection) -> None:
        art = create_memory(db, "x", scope="user", category="preference", name="rvr4a")
        update_memory_metadata(db, art["fqn"], memory_status="rejected")
        art2 = create_memory(db, "x", scope="user", category="preference", name="rvr4b")
        update_memory_metadata(db, art2["fqn"], memory_status="rejected")

        audit_writer = MagicMock()
        purge_memories(
            db,
            MemoryRetentionConfig(enabled=True, purge_statuses=["rejected"]),
            audit_writer=audit_writer,
            reviewer_id="alice",
        )
        # New memory + fresh purge as a different reviewer.
        art3 = create_memory(db, "x", scope="user", category="preference", name="rvr4c")
        update_memory_metadata(db, art3["fqn"], memory_status="rejected")
        purge_memories(
            db,
            MemoryRetentionConfig(enabled=True, purge_statuses=["rejected"]),
            audit_writer=audit_writer,
            reviewer_id="bob",
        )
        reviewers = [call.args[0].details["reviewer_id"] for call in audit_writer.emit.call_args_list]
        assert "alice" in reviewers and "bob" in reviewers
        assert reviewers.count("alice") == 2  # the two memories from the first pass
        assert reviewers.count("bob") == 1

    def test_dry_run_does_not_emit_even_with_reviewer_id(self, db: ThreadSafeConnection) -> None:
        art = create_memory(db, "x", scope="user", category="preference", name="rvr5")
        update_memory_metadata(db, art["fqn"], memory_status="rejected")
        audit_writer = MagicMock()
        result = purge_memories(
            db,
            MemoryRetentionConfig(enabled=True, purge_statuses=["rejected"]),
            dry_run=True,
            audit_writer=audit_writer,
            reviewer_id="dry-reviewer",
        )
        # purged_by still propagates through the dry-run result so the
        # UI can show "Previewed by: ...", but no audit entries emit.
        assert result.purged_by == "dry-reviewer"
        audit_writer.emit.assert_not_called()


class TestResultShape:
    def test_purge_result_is_frozen(self) -> None:
        result: Any = PurgeResult(purged_count=0, skipped_pinned_count=0)
        with pytest.raises(Exception):
            result.purged_count = 5  # type: ignore[misc]
