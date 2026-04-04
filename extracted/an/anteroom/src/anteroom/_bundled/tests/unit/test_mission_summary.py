"""Unit tests for mission_summary — delta summaries and retrospectives (#1263)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

from anteroom.db import init_db
from anteroom.services import mission_storage as ms
from anteroom.services.mission_summary import (
    build_delta_summary,
    build_retrospective,
    generate_and_store_retrospective,
)


@pytest.fixture()
def db(tmp_path: Path) -> Any:
    return init_db(tmp_path / "test.db")


# ---------------------------------------------------------------------------
# build_delta_summary
# ---------------------------------------------------------------------------


class TestBuildDeltaSummary:
    def test_empty_session(self, db: Any) -> None:
        s = ms.create_session(db, title="Empty")
        result = build_delta_summary(db, s["id"])
        assert result["event_count"] == 0
        assert result["items_launched"] == []
        assert result["items_completed"] == []
        assert result["items_failed"] == []

    def test_all_events_without_since(self, db: Any) -> None:
        s = ms.create_session(db, title="Full")
        item = ms.create_item(db, session_id=s["id"], summary="Task A")
        ms.create_event(db, session_id=s["id"], item_id=item["id"], event_type="item_launched")
        ms.create_event(db, session_id=s["id"], item_id=item["id"], event_type="item_completed")

        result = build_delta_summary(db, s["id"])
        assert result["event_count"] == 2
        assert item["id"] in result["items_launched"]
        assert item["id"] in result["items_completed"]

    def test_since_filters_events(self, db: Any) -> None:
        s = ms.create_session(db, title="Delta")
        item = ms.create_item(db, session_id=s["id"], summary="Task B")
        ev1 = ms.create_event(db, session_id=s["id"], item_id=item["id"], event_type="item_launched")
        ms.create_event(db, session_id=s["id"], item_id=item["id"], event_type="item_completed")

        # Use the first event's timestamp as the cutoff — only the second should appear
        result = build_delta_summary(db, s["id"], since=ev1["created_at"])
        assert result["event_count"] == 1
        assert result["items_completed"] == [item["id"]]
        assert result["items_launched"] == []

    def test_failed_items_tracked(self, db: Any) -> None:
        s = ms.create_session(db, title="Fail")
        item = ms.create_item(db, session_id=s["id"], summary="Fail Task")
        ms.create_event(db, session_id=s["id"], item_id=item["id"], event_type="item_failed")

        result = build_delta_summary(db, s["id"])
        assert item["id"] in result["items_failed"]

    def test_session_events_captured(self, db: Any) -> None:
        s = ms.create_session(db, title="Sess Events")
        ms.create_event(db, session_id=s["id"], event_type="session_completed")

        result = build_delta_summary(db, s["id"])
        assert len(result["session_events"]) == 1
        assert result["session_events"][0]["event_type"] == "session_completed"

    def test_other_transitions_captured(self, db: Any) -> None:
        s = ms.create_session(db, title="Other")
        item = ms.create_item(db, session_id=s["id"], summary="Task")
        ms.create_event(
            db, session_id=s["id"], item_id=item["id"], event_type="item_reconciled", detail={"reason": "manual"}
        )

        result = build_delta_summary(db, s["id"])
        assert len(result["other_transitions"]) == 1
        assert result["other_transitions"][0]["event_type"] == "item_reconciled"


# ---------------------------------------------------------------------------
# build_retrospective
# ---------------------------------------------------------------------------


class TestBuildRetrospective:
    def test_session_not_found(self, db: Any) -> None:
        with pytest.raises(ValueError, match="Session not found"):
            build_retrospective(db, "nonexistent")

    def test_empty_session(self, db: Any) -> None:
        s = ms.create_session(db, title="Empty Retro")
        retro = build_retrospective(db, s["id"])
        assert retro["total_items"] == 0
        assert retro["completion_rate"] == 0.0

    def test_full_retrospective(self, db: Any) -> None:
        s = ms.create_session(db, title="Full Retro", status="completed")
        item_a = ms.create_item(db, session_id=s["id"], summary="Task A", status="completed")
        item_b = ms.create_item(db, session_id=s["id"], summary="Task B", status="failed")
        ms.create_item(db, session_id=s["id"], summary="Task C", status="dropped")

        ms.create_event(db, session_id=s["id"], item_id=item_a["id"], event_type="item_launched")
        ms.create_event(db, session_id=s["id"], item_id=item_a["id"], event_type="item_completed")
        ms.create_event(db, session_id=s["id"], item_id=item_b["id"], event_type="item_launched")
        ms.create_event(db, session_id=s["id"], item_id=item_b["id"], event_type="item_failed")

        retro = build_retrospective(db, s["id"])
        assert retro["total_items"] == 3
        assert retro["completed"] == 1
        assert retro["failed"] == 1
        assert retro["dropped"] == 1
        assert retro["completion_rate"] == pytest.approx(33.3, abs=0.1)
        assert "Task A" in retro["completed_summaries"]
        assert "Task B" in retro["failed_summaries"]
        assert retro["duration_seconds"] >= 0
        assert retro["event_count"] == 4

    def test_item_durations_computed(self, db: Any) -> None:
        s = ms.create_session(db, title="Duration Test", status="completed")
        item = ms.create_item(db, session_id=s["id"], summary="Timed Task", status="completed")
        ms.create_event(db, session_id=s["id"], item_id=item["id"], event_type="item_launched")
        ms.create_event(db, session_id=s["id"], item_id=item["id"], event_type="item_completed")

        retro = build_retrospective(db, s["id"])
        assert item["id"] in retro["item_durations"]
        assert retro["item_durations"][item["id"]] >= 0.0


# ---------------------------------------------------------------------------
# generate_and_store_retrospective
# ---------------------------------------------------------------------------


class TestGenerateAndStoreRetrospective:
    def test_final_retrospective_stored(self, db: Any) -> None:
        s = ms.create_session(db, title="Final", status="completed")
        ms.create_item(db, session_id=s["id"], summary="Done", status="completed")

        event = generate_and_store_retrospective(db, s["id"], is_draft=False)
        assert event["event_type"] == "session_retrospective"
        assert event["detail"]["completed"] == 1

        events = ms.list_events(db, s["id"], event_type="session_retrospective")
        assert len(events) == 1

    def test_draft_retrospective_stored(self, db: Any) -> None:
        s = ms.create_session(db, title="Draft", status="failed")
        ms.create_item(db, session_id=s["id"], summary="Failed Task", status="failed")

        event = generate_and_store_retrospective(db, s["id"], is_draft=True)
        assert event["event_type"] == "session_retrospective_draft"
        assert event["detail"]["failed"] == 1

        events = ms.list_events(db, s["id"], event_type="session_retrospective_draft")
        assert len(events) == 1

    def test_draft_superseded_by_final(self, db: Any) -> None:
        s = ms.create_session(db, title="Recover", status="completed")
        ms.create_item(db, session_id=s["id"], summary="Task", status="completed")

        generate_and_store_retrospective(db, s["id"], is_draft=True)
        generate_and_store_retrospective(db, s["id"], is_draft=False)

        drafts = ms.list_events(db, s["id"], event_type="session_retrospective_draft")
        finals = ms.list_events(db, s["id"], event_type="session_retrospective")
        assert len(drafts) == 0
        assert len(finals) == 1


# ---------------------------------------------------------------------------
# list_events_since
# ---------------------------------------------------------------------------


class TestListEventsSince:
    def test_filters_by_timestamp(self, db: Any) -> None:
        s = ms.create_session(db, title="Since Test")
        ev1 = ms.create_event(db, session_id=s["id"], event_type="early")
        ms.create_event(db, session_id=s["id"], event_type="late")

        events = ms.list_events_since(db, s["id"], ev1["created_at"])
        assert len(events) == 1
        assert events[0]["event_type"] == "late"

    def test_empty_when_no_new_events(self, db: Any) -> None:
        s = ms.create_session(db, title="No New")
        ev = ms.create_event(db, session_id=s["id"], event_type="only")
        events = ms.list_events_since(db, s["id"], ev["created_at"])
        assert events == []
