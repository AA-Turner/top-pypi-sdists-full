"""Unit tests for mission storage — CRUD for sessions, items, deps, executions, revisions, events."""

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any

import pytest

from anteroom.db import init_db
from anteroom.services import mission_storage as ms


@pytest.fixture()
def db(tmp_path: Path) -> Any:
    return init_db(tmp_path / "test.db")


# ---------------------------------------------------------------------------
# Sessions
# ---------------------------------------------------------------------------


class TestSessionCRUD:
    def test_create_session_defaults(self, db: Any) -> None:
        s = ms.create_session(db, title="Test mission")
        assert s["id"]
        assert s["status"] == "pending"
        assert s["title"] == "Test mission"
        assert s["created_at"]
        assert s["updated_at"]

    def test_create_session_with_source_provenance(self, db: Any) -> None:
        s = ms.create_session(
            db,
            title="From spec",
            source_type="spec",
            source_fqn="@ns/feature/auth",
            source_version=2,
            referenced_artifacts=[{"fqn": "@ns/feature/auth", "version": 2}],
        )
        assert s["source_type"] == "spec"
        assert s["source_fqn"] == "@ns/feature/auth"
        assert s["source_version"] == 2
        assert s["referenced_artifacts"] == [{"fqn": "@ns/feature/auth", "version": 2}]

    def test_create_session_invalid_status(self, db: Any) -> None:
        with pytest.raises(ValueError, match="Invalid session status"):
            ms.create_session(db, status="bogus")

    def test_get_session(self, db: Any) -> None:
        s = ms.create_session(db, title="Get me")
        fetched = ms.get_session(db, s["id"])
        assert fetched is not None
        assert fetched["title"] == "Get me"

    def test_create_session_with_explicit_active_status(self, db: Any) -> None:
        s = ms.create_session(db, title="Launch me", status="active")
        fetched = ms.get_session(db, s["id"])
        assert fetched is not None
        assert fetched["status"] == "active"

    def test_get_session_not_found(self, db: Any) -> None:
        assert ms.get_session(db, "nonexistent") is None

    def test_list_sessions(self, db: Any) -> None:
        ms.create_session(db, title="A", status="active")
        ms.create_session(db, title="B", status="completed")
        ms.create_session(db, title="C", status="active")

        all_sessions = ms.list_sessions(db)
        assert len(all_sessions) == 3

        active = ms.list_sessions(db, status="active")
        assert len(active) == 2

    def test_list_sessions_pagination(self, db: Any) -> None:
        for i in range(5):
            ms.create_session(db, title=f"S{i}")
        page = ms.list_sessions(db, limit=2, offset=2)
        assert len(page) == 2

    def test_update_session(self, db: Any) -> None:
        s = ms.create_session(db, title="Original")
        updated = ms.update_session(db, s["id"], status="active", title="Updated")
        assert updated is not None
        assert updated["status"] == "active"
        assert updated["title"] == "Updated"

    def test_update_session_bad_column(self, db: Any) -> None:
        s = ms.create_session(db, title="X")
        with pytest.raises(ValueError, match="not in allowed"):
            ms.update_session(db, s["id"], bad_col="nope")

    def test_update_session_json_auto_serialize(self, db: Any) -> None:
        s = ms.create_session(db, title="X")
        updated = ms.update_session(db, s["id"], lane_limits_json={"build": 2})
        assert updated is not None
        assert updated["lane_limits"] == {"build": 2}

    def test_update_session_no_updates(self, db: Any) -> None:
        s = ms.create_session(db, title="X")
        result = ms.update_session(db, s["id"])
        assert result is not None
        assert result["title"] == "X"


# ---------------------------------------------------------------------------
# Items
# ---------------------------------------------------------------------------


class TestItemCRUD:
    def _session(self, db: Any) -> dict[str, Any]:
        return ms.create_session(db, title="S", status="active")

    def test_create_item_defaults(self, db: Any) -> None:
        s = self._session(db)
        item = ms.create_item(db, session_id=s["id"], summary="Do the thing")
        assert item["status"] == "pending"
        assert item["priority"] == 50
        assert item["adapter_type"] == "noop"
        assert item["hold_requested"] == 0

    def test_create_item_with_all_fields(self, db: Any) -> None:
        s = self._session(db)
        item = ms.create_item(
            db,
            session_id=s["id"],
            summary="Build it",
            description="More details",
            priority=10,
            item_type="milestone",
            adapter_type="workflow",
            adapter_config={"workflow_path": "/defs/build.yaml"},
            concurrency_group="build",
            lane="ci",
            hold_requested=True,
        )
        assert item["priority"] == 10
        assert item["adapter_config"] == {"workflow_path": "/defs/build.yaml"}
        assert item["concurrency_group"] == "build"
        assert item["lane"] == "ci"
        assert item["hold_requested"] == 1

    def test_create_item_invalid_status(self, db: Any) -> None:
        s = self._session(db)
        with pytest.raises(ValueError, match="Invalid item status"):
            ms.create_item(db, session_id=s["id"], summary="X", status="bogus")

    def test_get_item(self, db: Any) -> None:
        s = self._session(db)
        item = ms.create_item(db, session_id=s["id"], summary="Fetch me")
        fetched = ms.get_item(db, item["id"])
        assert fetched is not None
        assert fetched["summary"] == "Fetch me"

    def test_get_item_not_found(self, db: Any) -> None:
        assert ms.get_item(db, "nonexistent") is None

    def test_list_items_by_session(self, db: Any) -> None:
        s = self._session(db)
        ms.create_item(db, session_id=s["id"], summary="A", priority=20)
        ms.create_item(db, session_id=s["id"], summary="B", priority=10)
        items = ms.list_items_by_session(db, s["id"])
        assert len(items) == 2
        assert items[0]["summary"] == "B"  # lower priority first

    def test_list_items_by_session_with_status_filter(self, db: Any) -> None:
        s = self._session(db)
        i1 = ms.create_item(db, session_id=s["id"], summary="A")
        ms.create_item(db, session_id=s["id"], summary="B")
        ms.update_item(db, i1["id"], status="completed")
        completed = ms.list_items_by_session(db, s["id"], status="completed")
        assert len(completed) == 1
        assert completed[0]["id"] == i1["id"]

    def test_update_item(self, db: Any) -> None:
        s = self._session(db)
        item = ms.create_item(db, session_id=s["id"], summary="X")
        updated = ms.update_item(db, item["id"], status="active", priority=1)
        assert updated is not None
        assert updated["status"] == "active"
        assert updated["priority"] == 1

    def test_update_item_no_updates(self, db: Any) -> None:
        s = self._session(db)
        item = ms.create_item(db, session_id=s["id"], summary="X")
        result = ms.update_item(db, item["id"])
        assert result is not None
        assert result["summary"] == "X"

    def test_update_item_bad_column(self, db: Any) -> None:
        s = self._session(db)
        item = ms.create_item(db, session_id=s["id"], summary="X")
        with pytest.raises(ValueError, match="not in allowed"):
            ms.update_item(db, item["id"], bad_col="nope")


# ---------------------------------------------------------------------------
# Dependencies
# ---------------------------------------------------------------------------


class TestDependencies:
    def _make_items(self, db: Any) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
        s = ms.create_session(db, title="S", status="active")
        a = ms.create_item(db, session_id=s["id"], summary="A")
        b = ms.create_item(db, session_id=s["id"], summary="B")
        return s, a, b

    def test_add_and_get_dependency(self, db: Any) -> None:
        _, a, b = self._make_items(db)
        ms.add_dependency(db, item_id=b["id"], depends_on_id=a["id"])
        deps = ms.get_dependencies(db, b["id"])
        assert deps == [a["id"]]

    def test_get_dependents(self, db: Any) -> None:
        _, a, b = self._make_items(db)
        ms.add_dependency(db, item_id=b["id"], depends_on_id=a["id"])
        dependents = ms.get_dependents(db, a["id"])
        assert dependents == [b["id"]]

    def test_remove_dependency(self, db: Any) -> None:
        _, a, b = self._make_items(db)
        ms.add_dependency(db, item_id=b["id"], depends_on_id=a["id"])
        ms.remove_dependency(db, item_id=b["id"], depends_on_id=a["id"])
        assert ms.get_dependencies(db, b["id"]) == []

    def test_duplicate_dependency_ignored(self, db: Any) -> None:
        _, a, b = self._make_items(db)
        ms.add_dependency(db, item_id=b["id"], depends_on_id=a["id"])
        ms.add_dependency(db, item_id=b["id"], depends_on_id=a["id"])  # INSERT OR IGNORE
        deps = ms.get_dependencies(db, b["id"])
        assert len(deps) == 1

    def test_empty_dependencies(self, db: Any) -> None:
        _, a, _ = self._make_items(db)
        assert ms.get_dependencies(db, a["id"]) == []
        assert ms.get_dependents(db, a["id"]) == []

    def test_self_dependency_rejected(self, db: Any) -> None:
        _, a, _ = self._make_items(db)
        with pytest.raises(ValueError, match="cannot depend on itself"):
            ms.add_dependency(db, item_id=a["id"], depends_on_id=a["id"])

    def test_cross_session_dependency_rejected(self, db: Any) -> None:
        s1 = ms.create_session(db, title="S1", status="active")
        s2 = ms.create_session(db, title="S2", status="active")
        a = ms.create_item(db, session_id=s1["id"], summary="A")
        b = ms.create_item(db, session_id=s2["id"], summary="B")
        with pytest.raises(ValueError, match="across different mission sessions"):
            ms.add_dependency(db, item_id=b["id"], depends_on_id=a["id"])

    def test_dependency_with_nonexistent_item_rejected(self, db: Any) -> None:
        _, a, _ = self._make_items(db)
        with pytest.raises(ValueError, match="do not exist"):
            ms.add_dependency(db, item_id=a["id"], depends_on_id="nonexistent")


# ---------------------------------------------------------------------------
# Executions
# ---------------------------------------------------------------------------


class TestExecutionCRUD:
    def _make_item(self, db: Any) -> dict[str, Any]:
        s = ms.create_session(db, title="S", status="active")
        return ms.create_item(db, session_id=s["id"], summary="X")

    def test_create_execution(self, db: Any) -> None:
        item = self._make_item(db)
        exc = ms.create_execution(db, item_id=item["id"], attempt_number=1)
        assert exc["status"] == "pending"
        assert exc["attempt_number"] == 1
        assert exc["adapter_ref"] is None

    def test_create_execution_invalid_status(self, db: Any) -> None:
        item = self._make_item(db)
        with pytest.raises(ValueError, match="Invalid execution status"):
            ms.create_execution(db, item_id=item["id"], attempt_number=1, status="bogus")

    def test_unique_attempt_number(self, db: Any) -> None:
        item = self._make_item(db)
        ms.create_execution(db, item_id=item["id"], attempt_number=1)
        with pytest.raises(sqlite3.IntegrityError):
            ms.create_execution(db, item_id=item["id"], attempt_number=1)

    def test_get_execution(self, db: Any) -> None:
        item = self._make_item(db)
        exc = ms.create_execution(db, item_id=item["id"], attempt_number=1)
        fetched = ms.get_execution(db, exc["id"])
        assert fetched is not None
        assert fetched["item_id"] == item["id"]

    def test_get_execution_not_found(self, db: Any) -> None:
        assert ms.get_execution(db, "nonexistent") is None

    def test_list_executions_by_item(self, db: Any) -> None:
        item = self._make_item(db)
        ms.create_execution(db, item_id=item["id"], attempt_number=1)
        ms.create_execution(db, item_id=item["id"], attempt_number=2)
        execs = ms.list_executions_by_item(db, item["id"])
        assert len(execs) == 2
        assert execs[0]["attempt_number"] == 1
        assert execs[1]["attempt_number"] == 2

    def test_get_latest_execution(self, db: Any) -> None:
        item = self._make_item(db)
        ms.create_execution(db, item_id=item["id"], attempt_number=1)
        ms.create_execution(db, item_id=item["id"], attempt_number=2)
        latest = ms.get_latest_execution(db, item["id"])
        assert latest is not None
        assert latest["attempt_number"] == 2

    def test_get_latest_execution_none(self, db: Any) -> None:
        item = self._make_item(db)
        assert ms.get_latest_execution(db, item["id"]) is None

    def test_update_execution(self, db: Any) -> None:
        item = self._make_item(db)
        exc = ms.create_execution(db, item_id=item["id"], attempt_number=1)
        updated = ms.update_execution(db, exc["id"], status="completed", summary="Done", adapter_ref="wf-123")
        assert updated is not None
        assert updated["status"] == "completed"
        assert updated["summary"] == "Done"
        assert updated["adapter_ref"] == "wf-123"

    def test_update_execution_no_updates(self, db: Any) -> None:
        item = self._make_item(db)
        exc = ms.create_execution(db, item_id=item["id"], attempt_number=1)
        result = ms.update_execution(db, exc["id"])
        assert result is not None
        assert result["status"] == "pending"

    def test_update_execution_bad_column(self, db: Any) -> None:
        item = self._make_item(db)
        exc = ms.create_execution(db, item_id=item["id"], attempt_number=1)
        with pytest.raises(ValueError, match="not in allowed"):
            ms.update_execution(db, exc["id"], bad_col="nope")

    def test_update_execution_json_auto_serialize(self, db: Any) -> None:
        item = self._make_item(db)
        exc = ms.create_execution(db, item_id=item["id"], attempt_number=1)
        updated = ms.update_execution(db, exc["id"], artifacts_json={"output": "file.txt"})
        assert updated is not None
        assert updated["artifacts"] == {"output": "file.txt"}


# ---------------------------------------------------------------------------
# Revisions
# ---------------------------------------------------------------------------


class TestRevisionCRUD:
    def _session(self, db: Any) -> dict[str, Any]:
        return ms.create_session(db, title="S", status="active")

    def test_create_revision(self, db: Any) -> None:
        s = self._session(db)
        rev = ms.create_revision(
            db,
            session_id=s["id"],
            revision_number=1,
            operations=[{"op": "add_item", "payload": {"summary": "New"}}],
            plan_snapshot_after={"items": []},
            reason="Initial plan",
        )
        assert rev["revision_number"] == 1
        assert rev["operations"] == [{"op": "add_item", "payload": {"summary": "New"}}]
        assert rev["plan_snapshot_after"] == {"items": []}
        assert rev["reason"] == "Initial plan"

    def test_create_revision_with_artifacts(self, db: Any) -> None:
        s = self._session(db)
        rev = ms.create_revision(
            db,
            session_id=s["id"],
            revision_number=1,
            operations=[],
            plan_snapshot_after={},
            referenced_artifacts=[{"fqn": "@ns/rule/sec", "version": 1}],
        )
        assert rev["referenced_artifacts"] == [{"fqn": "@ns/rule/sec", "version": 1}]

    def test_unique_revision_number(self, db: Any) -> None:
        s = self._session(db)
        ms.create_revision(
            db,
            session_id=s["id"],
            revision_number=1,
            operations=[],
            plan_snapshot_after={},
        )
        with pytest.raises(sqlite3.IntegrityError):
            ms.create_revision(
                db,
                session_id=s["id"],
                revision_number=1,
                operations=[],
                plan_snapshot_after={},
            )

    def test_list_revisions(self, db: Any) -> None:
        s = self._session(db)
        ms.create_revision(
            db,
            session_id=s["id"],
            revision_number=1,
            operations=[],
            plan_snapshot_after={},
        )
        ms.create_revision(
            db,
            session_id=s["id"],
            revision_number=2,
            operations=[{"op": "drop_item"}],
            plan_snapshot_after={},
        )
        revs = ms.list_revisions(db, s["id"])
        assert len(revs) == 2
        assert revs[0]["revision_number"] == 1
        assert revs[1]["revision_number"] == 2

    def test_get_revision(self, db: Any) -> None:
        s = self._session(db)
        rev = ms.create_revision(
            db,
            session_id=s["id"],
            revision_number=1,
            operations=[],
            plan_snapshot_after={},
        )
        fetched = ms.get_revision(db, rev["id"])
        assert fetched is not None
        assert fetched["session_id"] == s["id"]

    def test_get_revision_not_found(self, db: Any) -> None:
        assert ms.get_revision(db, "nonexistent") is None


# ---------------------------------------------------------------------------
# Events
# ---------------------------------------------------------------------------


class TestEventCRUD:
    def _session(self, db: Any) -> dict[str, Any]:
        return ms.create_session(db, title="S", status="active")

    def test_create_event(self, db: Any) -> None:
        s = self._session(db)
        ev = ms.create_event(db, session_id=s["id"], event_type="item_launched")
        assert ev["id"] is not None
        assert ev["event_type"] == "item_launched"
        assert ev["item_id"] is None
        assert ev["detail"] is None

    def test_create_event_with_detail(self, db: Any) -> None:
        s = self._session(db)
        ev = ms.create_event(
            db,
            session_id=s["id"],
            event_type="item_failed",
            item_id="item-123",
            detail={"reason": "timeout"},
        )
        assert ev["item_id"] == "item-123"
        assert ev["detail"] == {"reason": "timeout"}

    def test_list_events(self, db: Any) -> None:
        s = self._session(db)
        ms.create_event(db, session_id=s["id"], event_type="started")
        ms.create_event(db, session_id=s["id"], event_type="item_launched")
        ms.create_event(db, session_id=s["id"], event_type="item_launched")
        events = ms.list_events(db, s["id"])
        assert len(events) == 3

    def test_list_events_filter_type(self, db: Any) -> None:
        s = self._session(db)
        ms.create_event(db, session_id=s["id"], event_type="started")
        ms.create_event(db, session_id=s["id"], event_type="item_launched")
        events = ms.list_events(db, s["id"], event_type="item_launched")
        assert len(events) == 1

    def test_list_events_filter_item(self, db: Any) -> None:
        s = self._session(db)
        ms.create_event(db, session_id=s["id"], event_type="launched", item_id="i1")
        ms.create_event(db, session_id=s["id"], event_type="launched", item_id="i2")
        events = ms.list_events(db, s["id"], item_id="i1")
        assert len(events) == 1

    def test_list_events_pagination(self, db: Any) -> None:
        s = self._session(db)
        for i in range(5):
            ms.create_event(db, session_id=s["id"], event_type=f"ev{i}")
        page = ms.list_events(db, s["id"], limit=2, offset=2)
        assert len(page) == 2


# ---------------------------------------------------------------------------
# Scheduler queries
# ---------------------------------------------------------------------------


class TestSchedulerQueries:
    def _setup(self, db: Any) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
        s = ms.create_session(db, title="S", status="active")
        a = ms.create_item(db, session_id=s["id"], summary="A")
        b = ms.create_item(db, session_id=s["id"], summary="B")
        c = ms.create_item(db, session_id=s["id"], summary="C")
        return s, a, b, c

    def test_eligible_no_deps(self, db: Any) -> None:
        s, a, b, c = self._setup(db)
        eligible = ms.list_eligible_items(db, s["id"])
        assert len(eligible) == 3

    def test_eligible_with_unsatisfied_dep(self, db: Any) -> None:
        s, a, b, c = self._setup(db)
        ms.add_dependency(db, item_id=b["id"], depends_on_id=a["id"])
        eligible = ms.list_eligible_items(db, s["id"])
        ids = {e["id"] for e in eligible}
        assert a["id"] in ids
        assert b["id"] not in ids  # dep not completed
        assert c["id"] in ids

    def test_eligible_with_satisfied_dep(self, db: Any) -> None:
        s, a, b, c = self._setup(db)
        ms.add_dependency(db, item_id=b["id"], depends_on_id=a["id"])
        ms.update_item(db, a["id"], status="completed")
        eligible = ms.list_eligible_items(db, s["id"])
        ids = {e["id"] for e in eligible}
        assert b["id"] in ids

    def test_eligible_excludes_held(self, db: Any) -> None:
        s, a, b, c = self._setup(db)
        ms.update_item(db, a["id"], hold_requested=1)
        eligible = ms.list_eligible_items(db, s["id"])
        ids = {e["id"] for e in eligible}
        assert a["id"] not in ids

    def test_eligible_excludes_non_pending(self, db: Any) -> None:
        s, a, b, c = self._setup(db)
        ms.update_item(db, a["id"], status="active")
        eligible = ms.list_eligible_items(db, s["id"])
        ids = {e["id"] for e in eligible}
        assert a["id"] not in ids

    def test_count_active_by_lane(self, db: Any) -> None:
        s = ms.create_session(db, title="S", status="active")
        ms.create_item(db, session_id=s["id"], summary="A", lane="ci", status="active")
        ms.create_item(db, session_id=s["id"], summary="B", lane="ci", status="active")
        ms.create_item(db, session_id=s["id"], summary="C", lane="deploy", status="active")
        ms.create_item(db, session_id=s["id"], summary="D", lane="ci", status="pending")
        counts = ms.count_active_by_lane(db, s["id"])
        assert counts == {"ci": 2, "deploy": 1}

    def test_count_active_by_concurrency_group(self, db: Any) -> None:
        s = ms.create_session(db, title="S", status="active")
        ms.create_item(db, session_id=s["id"], summary="A", concurrency_group="build", status="active")
        ms.create_item(db, session_id=s["id"], summary="B", concurrency_group="build", status="pending")
        counts = ms.count_active_by_concurrency_group(db, s["id"])
        assert counts == {"build": 1}

    def test_eligible_blocks_on_failed_dep(self, db: Any) -> None:
        s, a, b, c = self._setup(db)
        ms.add_dependency(db, item_id=b["id"], depends_on_id=a["id"])
        ms.update_item(db, a["id"], status="failed")
        eligible = ms.list_eligible_items(db, s["id"])
        ids = {e["id"] for e in eligible}
        assert b["id"] not in ids

    def test_eligible_blocks_on_active_dep(self, db: Any) -> None:
        s, a, b, c = self._setup(db)
        ms.add_dependency(db, item_id=b["id"], depends_on_id=a["id"])
        ms.update_item(db, a["id"], status="active")
        eligible = ms.list_eligible_items(db, s["id"])
        ids = {e["id"] for e in eligible}
        assert b["id"] not in ids

    def test_eligible_blocks_on_dropped_dep(self, db: Any) -> None:
        s, a, b, c = self._setup(db)
        ms.add_dependency(db, item_id=b["id"], depends_on_id=a["id"])
        ms.update_item(db, a["id"], status="dropped")
        eligible = ms.list_eligible_items(db, s["id"])
        ids = {e["id"] for e in eligible}
        assert b["id"] not in ids


# ---------------------------------------------------------------------------
# Cascade deletes
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# retry_item and prepare_replace
# ---------------------------------------------------------------------------


class TestRetryItem:
    def _make_failed_item(self, db: Any) -> tuple[dict[str, Any], dict[str, Any]]:
        s = ms.create_session(db, title="S", status="active")
        item = ms.create_item(db, session_id=s["id"], summary="Fail task")
        ms.update_item(db, item["id"], status="failed")
        return s, ms.get_item(db, item["id"])  # type: ignore[return-value]

    def test_retry_resets_to_pending(self, db: Any) -> None:
        s, item = self._make_failed_item(db)
        result = ms.retry_item(db, item["id"])
        assert result["status"] == "pending"

    def test_retry_emits_event(self, db: Any) -> None:
        s, item = self._make_failed_item(db)
        ms.retry_item(db, item["id"])
        events = ms.list_events(db, s["id"], item_id=item["id"])
        assert any(e["event_type"] == "item_retried" for e in events)

    def test_retry_non_failed_raises(self, db: Any) -> None:
        s = ms.create_session(db, title="S", status="active")
        item = ms.create_item(db, session_id=s["id"], summary="X")
        with pytest.raises(ValueError, match="must be in 'failed' status"):
            ms.retry_item(db, item["id"])

    def test_retry_not_found_raises(self, db: Any) -> None:
        with pytest.raises(ValueError, match="Item not found"):
            ms.retry_item(db, "nonexistent")


class TestPrepareReplace:
    def _make_active_item_with_execution(self, db: Any) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
        s = ms.create_session(db, title="S", status="active")
        item = ms.create_item(db, session_id=s["id"], summary="Replace task", status="active")
        exc = ms.create_execution(db, item_id=item["id"], attempt_number=1, status="running", adapter_ref="ref-1")
        return s, item, exc

    def test_prepare_replace_resets_item(self, db: Any) -> None:
        s, item, exc = self._make_active_item_with_execution(db)
        result = ms.prepare_replace(db, item["id"], exc["id"])
        assert result["status"] == "pending"

    def test_prepare_replace_cancels_execution(self, db: Any) -> None:
        s, item, exc = self._make_active_item_with_execution(db)
        ms.prepare_replace(db, item["id"], exc["id"])
        updated_exc = ms.get_execution(db, exc["id"])
        assert updated_exc is not None
        assert updated_exc["status"] == "cancelled"
        assert updated_exc["finished_at"] is not None

    def test_prepare_replace_emits_event(self, db: Any) -> None:
        s, item, exc = self._make_active_item_with_execution(db)
        ms.prepare_replace(db, item["id"], exc["id"])
        events = ms.list_events(db, s["id"], item_id=item["id"])
        assert any(e["event_type"] == "item_replaced" for e in events)
        replaced_event = [e for e in events if e["event_type"] == "item_replaced"][0]
        assert replaced_event["detail"]["cancelled_execution_id"] == exc["id"]

    def test_prepare_replace_item_not_found_raises(self, db: Any) -> None:
        with pytest.raises(ValueError, match="Item not found"):
            ms.prepare_replace(db, "nonexistent", "some-exec")

    def test_prepare_replace_execution_not_found_raises(self, db: Any) -> None:
        s = ms.create_session(db, title="S", status="active")
        item = ms.create_item(db, session_id=s["id"], summary="X")
        with pytest.raises(ValueError, match="Execution not found"):
            ms.prepare_replace(db, item["id"], "nonexistent")

    def test_prepare_replace_execution_mismatch_raises(self, db: Any) -> None:
        s = ms.create_session(db, title="S", status="active")
        item_a = ms.create_item(db, session_id=s["id"], summary="A")
        item_b = ms.create_item(db, session_id=s["id"], summary="B")
        exc = ms.create_execution(db, item_id=item_a["id"], attempt_number=1)
        with pytest.raises(ValueError, match="does not belong"):
            ms.prepare_replace(db, item_b["id"], exc["id"])


class TestCascadeDeletes:
    def test_delete_session_cascades(self, db: Any) -> None:
        s = ms.create_session(db, title="S", status="active")
        item = ms.create_item(db, session_id=s["id"], summary="X")
        ms.create_execution(db, item_id=item["id"], attempt_number=1)
        ms.create_revision(
            db,
            session_id=s["id"],
            revision_number=1,
            operations=[],
            plan_snapshot_after={},
        )
        ms.create_event(db, session_id=s["id"], event_type="test")

        # Add a second item and a dependency
        item2 = ms.create_item(db, session_id=s["id"], summary="Y")
        ms.add_dependency(db, item_id=item2["id"], depends_on_id=item["id"])

        # Delete the session
        db.execute("DELETE FROM mission_sessions WHERE id = ?", (s["id"],))
        db.commit()

        # Everything should be gone
        assert ms.get_session(db, s["id"]) is None
        assert ms.get_item(db, item["id"]) is None
        assert ms.get_item(db, item2["id"]) is None
        assert ms.list_executions_by_item(db, item["id"]) == []
        assert ms.list_revisions(db, s["id"]) == []
        assert ms.list_events(db, s["id"]) == []
        assert ms.get_dependencies(db, item2["id"]) == []


# ---------------------------------------------------------------------------
# Plan snapshot
# ---------------------------------------------------------------------------


class TestPlanSnapshot:
    def test_build_plan_snapshot(self, db: Any) -> None:
        s = ms.create_session(db, title="S", status="active")
        a = ms.create_item(db, session_id=s["id"], summary="A")
        b = ms.create_item(db, session_id=s["id"], summary="B")
        ms.add_dependency(db, item_id=b["id"], depends_on_id=a["id"])

        snap = ms.build_plan_snapshot(db, s["id"])
        assert len(snap["items"]) == 2
        assert snap["dependencies"][b["id"]] == [a["id"]]
        assert snap["dependencies"][a["id"]] == []

    def test_build_plan_snapshot_empty(self, db: Any) -> None:
        s = ms.create_session(db, title="S", status="active")
        snap = ms.build_plan_snapshot(db, s["id"])
        assert snap["items"] == []
        assert snap["dependencies"] == {}


# ---------------------------------------------------------------------------
# Reconcile
# ---------------------------------------------------------------------------


class TestReconcileItem:
    def _setup(self, db: Any) -> tuple[dict[str, Any], dict[str, Any]]:
        s = ms.create_session(db, title="S", status="active")
        item = ms.create_item(db, session_id=s["id"], summary="Task", status="active")
        return s, item

    def test_reconcile_active_to_completed(self, db: Any) -> None:
        s, item = self._setup(db)
        result = ms.reconcile_item(db, item["id"], reason="Done manually")
        assert result["status"] == "completed"

    def test_reconcile_failed_to_completed(self, db: Any) -> None:
        s = ms.create_session(db, title="S", status="active")
        item = ms.create_item(db, session_id=s["id"], summary="Task", status="failed")
        result = ms.reconcile_item(db, item["id"], reason="Fixed externally")
        assert result["status"] == "completed"

    def test_reconcile_blocked_to_completed(self, db: Any) -> None:
        s = ms.create_session(db, title="S", status="active")
        item = ms.create_item(db, session_id=s["id"], summary="Task", status="blocked")
        result = ms.reconcile_item(db, item["id"], reason="Unblocked and done")
        assert result["status"] == "completed"

    def test_reconcile_already_completed_raises(self, db: Any) -> None:
        s = ms.create_session(db, title="S", status="active")
        item = ms.create_item(db, session_id=s["id"], summary="Task", status="completed")
        with pytest.raises(ValueError, match="Cannot reconcile item in status 'completed'"):
            ms.reconcile_item(db, item["id"], reason="Nope")

    def test_reconcile_dropped_raises(self, db: Any) -> None:
        s = ms.create_session(db, title="S", status="active")
        item = ms.create_item(db, session_id=s["id"], summary="Task", status="dropped")
        with pytest.raises(ValueError, match="Cannot reconcile item in status 'dropped'"):
            ms.reconcile_item(db, item["id"], reason="Nope")

    def test_reconcile_pending_raises(self, db: Any) -> None:
        s = ms.create_session(db, title="S", status="active")
        item = ms.create_item(db, session_id=s["id"], summary="Task", status="pending")
        with pytest.raises(ValueError, match="Cannot reconcile item in status 'pending'"):
            ms.reconcile_item(db, item["id"], reason="Nope")

    def test_reconcile_not_found_raises(self, db: Any) -> None:
        with pytest.raises(ValueError, match="Item not found"):
            ms.reconcile_item(db, "nonexistent", reason="Nope")

    def test_reconcile_emits_event(self, db: Any) -> None:
        s, item = self._setup(db)
        ms.reconcile_item(db, item["id"], reason="CI finished")
        events = ms.list_events(db, s["id"], event_type="item_reconciled")
        assert len(events) == 1
        assert events[0]["item_id"] == item["id"]
        assert events[0]["detail"]["reason"] == "CI finished"
        assert events[0]["detail"]["from_status"] == "active"
        assert events[0]["detail"]["to_status"] == "completed"

    def test_reconcile_rejects_running_execution(self, db: Any) -> None:
        s, item = self._setup(db)
        ms.create_execution(db, item_id=item["id"], attempt_number=1, status="running")
        with pytest.raises(ValueError, match="live execution"):
            ms.reconcile_item(db, item["id"], reason="Done outside")

    def test_reconcile_rejects_pending_execution(self, db: Any) -> None:
        s, item = self._setup(db)
        ms.create_execution(db, item_id=item["id"], attempt_number=1, status="pending")
        with pytest.raises(ValueError, match="live execution"):
            ms.reconcile_item(db, item["id"], reason="Done outside")

    def test_reconcile_skips_already_finished_execution(self, db: Any) -> None:
        s, item = self._setup(db)
        exc = ms.create_execution(db, item_id=item["id"], attempt_number=1, status="failed")
        ms.update_execution(db, exc["id"], finished_at="2025-01-01T00:00:00Z")
        ms.reconcile_item(db, item["id"], reason="Fixed")
        updated_exc = ms.get_execution(db, exc["id"])
        assert updated_exc is not None
        assert updated_exc["status"] == "failed"  # not changed

    def test_reconcile_custom_status(self, db: Any) -> None:
        s, item = self._setup(db)
        result = ms.reconcile_item(db, item["id"], status="dropped", reason="No longer needed")
        assert result["status"] == "dropped"

    def test_reconcile_event_persists_atomically_with_status(self, db: Any) -> None:
        """Event and status update are in the same transaction (#1306)."""
        s, item = self._setup(db)
        ms.reconcile_item(db, item["id"], reason="Atomic check")
        updated = ms.get_item(db, item["id"])
        assert updated is not None
        assert updated["status"] == "completed"
        events = ms.list_events(db, s["id"], event_type="item_reconciled")
        assert len(events) == 1
        assert events[0]["detail"]["reason"] == "Atomic check"


class TestForceReconcileItem:
    """Tests for force_reconcile_item (#1306)."""

    def _setup(self, db: Any) -> tuple[dict[str, Any], dict[str, Any]]:
        s = ms.create_session(db, title="S", status="active")
        item = ms.create_item(db, session_id=s["id"], summary="Task", status="failed")
        return s, item

    def test_force_reconcile_cancels_live_execution_then_reconciles(self, db: Any) -> None:
        s = ms.create_session(db, title="S", status="active")
        item = ms.create_item(db, session_id=s["id"], summary="Task", status="active")
        exc = ms.create_execution(db, item_id=item["id"], attempt_number=1, status="running")
        result = ms.force_reconcile_item(db, item["id"], reason="PR merged externally")
        assert result["status"] == "completed"
        updated_exc = ms.get_execution(db, exc["id"])
        assert updated_exc is not None
        assert updated_exc["status"] == "cancelled"
        assert updated_exc["summary"] == "superseded_by_external_completion"

    def test_force_reconcile_works_when_no_live_execution(self, db: Any) -> None:
        s, item = self._setup(db)
        exc = ms.create_execution(db, item_id=item["id"], attempt_number=1, status="failed")
        result = ms.force_reconcile_item(db, item["id"], reason="Issue closed")
        assert result["status"] == "completed"
        updated_exc = ms.get_execution(db, exc["id"])
        assert updated_exc is not None
        assert updated_exc["status"] == "failed"  # not changed

    def test_force_reconcile_fails_for_terminal_item(self, db: Any) -> None:
        s = ms.create_session(db, title="S", status="active")
        item = ms.create_item(db, session_id=s["id"], summary="Task", status="completed")
        with pytest.raises(ValueError, match="Cannot reconcile"):
            ms.force_reconcile_item(db, item["id"], reason="Nope")

    def test_force_reconcile_reason_preserved_in_event(self, db: Any) -> None:
        s, item = self._setup(db)
        ms.force_reconcile_item(db, item["id"], reason="Issue #42 closed externally")
        events = ms.list_events(db, s["id"], event_type="item_reconciled")
        assert len(events) == 1
        assert events[0]["detail"]["reason"] == "Issue #42 closed externally"
        assert events[0]["detail"]["from_status"] == "failed"
        assert events[0]["detail"]["to_status"] == "completed"

    def test_force_reconcile_cancels_pending_execution(self, db: Any) -> None:
        s = ms.create_session(db, title="S", status="active")
        item = ms.create_item(db, session_id=s["id"], summary="Task", status="active")
        exc = ms.create_execution(db, item_id=item["id"], attempt_number=1, status="pending")
        result = ms.force_reconcile_item(db, item["id"], reason="Superseded")
        assert result["status"] == "completed"
        updated_exc = ms.get_execution(db, exc["id"])
        assert updated_exc is not None
        assert updated_exc["status"] == "cancelled"


class TestSessionResolution:
    def test_resolve_session_id_exact(self, db: Any) -> None:
        session = ms.create_session(db, title="Exact")
        assert ms.resolve_session_id(db, session["id"]) == session["id"]

    def test_resolve_session_id_unique_prefix(self, db: Any) -> None:
        session = ms.create_session(db, title="Prefix")
        prefix = session["id"][:12]
        assert ms.resolve_session_id(db, prefix) == session["id"]

    def test_resolve_session_id_not_found(self, db: Any) -> None:
        with pytest.raises(ValueError, match="Mission not found"):
            ms.resolve_session_id(db, "does-not-exist")

    def test_resolve_session_id_ambiguous_prefix(self, db: Any) -> None:
        s1 = ms.create_session(db, title="One")
        s2 = ms.create_session(db, title="Two")
        shared = s1["id"][:4]
        while not s2["id"].startswith(shared):
            db.execute("DELETE FROM mission_sessions WHERE id = ?", (s2["id"],))
            db.commit()
            s2 = ms.create_session(db, title="Two")
        with pytest.raises(ValueError, match="Ambiguous mission ID prefix"):
            ms.resolve_session_id(db, shared)


# ---------------------------------------------------------------------------
# Item resolution
# ---------------------------------------------------------------------------


class TestItemResolution:
    def test_resolve_item_id_exact(self, db: Any) -> None:
        s = ms.create_session(db, title="Test")
        item = ms.create_item(db, session_id=s["id"], summary="Do stuff")
        assert ms.resolve_item_id(db, item["id"]) == item["id"]

    def test_resolve_item_id_unique_prefix(self, db: Any) -> None:
        s = ms.create_session(db, title="Test")
        item = ms.create_item(db, session_id=s["id"], summary="Do stuff")
        prefix = item["id"][:8]
        assert ms.resolve_item_id(db, prefix) == item["id"]

    def test_resolve_item_id_not_found(self, db: Any) -> None:
        with pytest.raises(ValueError, match="Item not found"):
            ms.resolve_item_id(db, "does-not-exist")

    def test_resolve_item_id_ambiguous(self, db: Any) -> None:
        s = ms.create_session(db, title="Test")
        i1 = ms.create_item(db, session_id=s["id"], summary="First")
        i2 = ms.create_item(db, session_id=s["id"], summary="Second")
        shared = i1["id"][:4]
        while not i2["id"].startswith(shared):
            db.execute("DELETE FROM mission_items WHERE id = ?", (i2["id"],))
            db.commit()
            i2 = ms.create_item(db, session_id=s["id"], summary="Second")
        with pytest.raises(ValueError, match="Ambiguous item ID prefix"):
            ms.resolve_item_id(db, shared)

    def test_resolve_item_id_session_scoped(self, db: Any) -> None:
        s1 = ms.create_session(db, title="Session A")
        s2 = ms.create_session(db, title="Session B")
        i1 = ms.create_item(db, session_id=s1["id"], summary="Item A")
        i2 = ms.create_item(db, session_id=s2["id"], summary="Item B")
        shared = i1["id"][:4]
        while not i2["id"].startswith(shared):
            db.execute("DELETE FROM mission_items WHERE id = ?", (i2["id"],))
            db.commit()
            i2 = ms.create_item(db, session_id=s2["id"], summary="Item B")
        # Without session_id, both match — ambiguous
        with pytest.raises(ValueError, match="Ambiguous item ID prefix"):
            ms.resolve_item_id(db, shared)
        # With session_id, only one matches — resolves
        assert ms.resolve_item_id(db, shared, session_id=s1["id"]) == i1["id"]
        assert ms.resolve_item_id(db, shared, session_id=s2["id"]) == i2["id"]
