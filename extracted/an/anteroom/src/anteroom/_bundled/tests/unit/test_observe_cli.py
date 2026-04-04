from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from anteroom.cli import observe_cli
from anteroom.db import init_db
from anteroom.services import mission_storage, workflow_storage


@pytest.fixture()
def db(tmp_path: Path) -> Any:
    return init_db(tmp_path / "test.db")


def test_resolve_target_prefers_unique_mission(db: Any) -> None:
    session = mission_storage.create_session(db, title="Mission")
    kind, resolved_id, error = observe_cli._resolve_target(db, session["id"])
    assert error is None
    assert kind == "mission"
    assert resolved_id == session["id"]


def test_resolve_target_prefers_unique_workflow(db: Any) -> None:
    run = workflow_storage.create_workflow_run(
        db,
        workflow_id="test-flow",
        workflow_version="1",
        target_kind="issue",
        target_ref="123",
    )
    kind, resolved_id, error = observe_cli._resolve_target(db, run["id"])
    assert error is None
    assert kind == "workflow"
    assert resolved_id == run["id"]


def test_resolve_target_cross_target_ambiguity(db: Any, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(observe_cli, "_resolve_mission_session_id", lambda _db, _target: "mission-1")
    monkeypatch.setattr(observe_cli, "_resolve_workflow_run_id", lambda _db, _target: "workflow-1")
    kind, resolved_id, error = observe_cli._resolve_target(db, "shared")
    assert kind is None
    assert resolved_id is None
    assert "Ambiguous ID" in error


def test_build_mission_payload_includes_linked_workflow_and_approval(db: Any) -> None:
    session = mission_storage.create_session(db, title="Mission", status="active")
    item = mission_storage.create_item(db, session_id=session["id"], summary="Review change", status="blocked")
    run = workflow_storage.create_workflow_run(
        db,
        workflow_id="child-flow",
        workflow_version="1",
        target_kind="mission_item",
        target_ref=item["id"],
    )
    workflow_storage.update_workflow_run(db, run["id"], status="waiting_for_approval", current_step_id="approval")
    mission_storage.create_execution(db, item_id=item["id"], attempt_number=1, status="running", adapter_ref=run["id"])
    workflow_storage.create_approval_request(
        db,
        run_id=run["id"],
        step_id="approval",
        tool_name="bash",
        tool_args={"command": "git push"},
        risk_tier="high",
    )

    payload = observe_cli._build_mission_payload(db, session["id"])
    enriched = payload["items"][0]
    assert enriched["latest_execution"]["adapter_ref"] == run["id"]
    assert enriched["linked_workflow"]["status"] == "waiting_for_approval"
    assert enriched["linked_workflow"]["pending_approvals"][0]["tool_name"] == "bash"
    assert "waiting on linked workflow approval" in enriched["blockers"]


def test_build_workflow_payload_includes_pending_decision(db: Any) -> None:
    run = workflow_storage.create_workflow_run(
        db,
        workflow_id="decision-flow",
        workflow_version="1",
        target_kind="issue",
        target_ref="1225",
    )
    workflow_storage.update_workflow_run(db, run["id"], status="waiting_for_input")
    workflow_storage.create_human_decision(
        db,
        run_id=run["id"],
        step_id="human_gate",
        prompt="Choose a path",
        options=[{"id": "approve", "label": "Approve"}],
    )

    payload = observe_cli._build_workflow_payload(db, run["id"])
    assert payload["pending_decisions"][0]["prompt"] == "Choose a path"


def test_build_workflow_payload_lists_all_pending_approvals_and_decisions(db: Any) -> None:
    run = workflow_storage.create_workflow_run(
        db,
        workflow_id="multi-gate-flow",
        workflow_version="1",
        target_kind="issue",
        target_ref="1225",
    )
    workflow_storage.update_workflow_run(db, run["id"], status="waiting_for_input")
    workflow_storage.create_approval_request(
        db,
        run_id=run["id"],
        step_id="approval-1",
        tool_name="bash",
        tool_args={"command": "git push"},
        risk_tier="high",
    )
    workflow_storage.create_approval_request(
        db,
        run_id=run["id"],
        step_id="approval-2",
        tool_name="write_file",
        tool_args={"path": "README.md"},
        risk_tier="medium",
    )
    workflow_storage.create_human_decision(
        db,
        run_id=run["id"],
        step_id="human-1",
        prompt="Choose a path",
        options=[{"id": "approve", "label": "Approve"}],
    )
    workflow_storage.create_human_decision(
        db,
        run_id=run["id"],
        step_id="human-2",
        prompt="Pick an owner",
        options=[{"id": "troy", "label": "Troy"}],
    )

    payload = observe_cli._build_workflow_payload(db, run["id"])
    assert [approval["step_id"] for approval in payload["pending_approvals"]] == ["approval-2", "approval-1"]
    assert [decision["step_id"] for decision in payload["pending_decisions"]] == ["human-2", "human-1"]


def test_json_payload_is_machine_readable(db: Any) -> None:
    session = mission_storage.create_session(db, title="Mission")
    payload = observe_cli._build_mission_payload(db, session["id"])
    encoded = json.dumps(payload)
    decoded = json.loads(encoded)
    assert decoded["kind"] == "mission"


class TestObserveSinceFlag:
    """Tests for --since flag on observe (#1263)."""

    def test_since_renders_delta_summary(self, db: Any) -> None:
        from io import StringIO
        from unittest.mock import MagicMock, patch

        from rich.console import Console

        session = mission_storage.create_session(db, title="Delta Mission", status="active")
        item = mission_storage.create_item(db, session_id=session["id"], summary="Task A")
        ev = mission_storage.create_event(db, session_id=session["id"], item_id=item["id"], event_type="item_launched")
        mission_storage.create_event(db, session_id=session["id"], item_id=item["id"], event_type="item_completed")

        import argparse

        args = argparse.Namespace(target=session["id"], json_output=False, since=ev["created_at"], summary=False)
        buf = StringIO()
        test_console = Console(file=buf, width=120, no_color=True)
        config = MagicMock()
        with (
            patch.object(observe_cli, "console", test_console),
            patch("anteroom.db.get_db", return_value=db),
        ):
            observe_cli._run_observe(config, args)
        output = buf.getvalue()
        assert "Delta summary" in output
        assert "Completed: 1" in output

    def test_since_json_output(self, db: Any) -> None:
        import io
        from contextlib import redirect_stdout
        from unittest.mock import MagicMock, patch

        session = mission_storage.create_session(db, title="JSON Delta", status="active")
        mission_storage.create_event(db, session_id=session["id"], event_type="session_completed")

        import argparse

        args = argparse.Namespace(target=session["id"], json_output=True, since="2000-01-01T00:00:00", summary=False)
        config = MagicMock()
        captured = io.StringIO()
        with (
            patch("anteroom.db.get_db", return_value=db),
            redirect_stdout(captured),
        ):
            observe_cli._run_observe(config, args)
        output = captured.getvalue()
        parsed = json.loads(output)
        assert parsed["event_count"] >= 1


class TestObserveSummaryFlag:
    """Tests for --summary flag on observe (#1263)."""

    def test_summary_renders_retrospective(self, db: Any) -> None:
        from io import StringIO
        from unittest.mock import MagicMock, patch

        from rich.console import Console

        session = mission_storage.create_session(db, title="Retro Mission", status="completed")
        mission_storage.create_item(db, session_id=session["id"], summary="Done", status="completed")

        import argparse

        args = argparse.Namespace(target=session["id"], json_output=False, since=None, summary=True)
        buf = StringIO()
        test_console = Console(file=buf, width=120, no_color=True)
        config = MagicMock()
        with (
            patch.object(observe_cli, "console", test_console),
            patch("anteroom.db.get_db", return_value=db),
        ):
            observe_cli._run_observe(config, args)
        output = buf.getvalue()
        assert "Retrospective" in output
        assert "1/1" in output


class TestRenderWorkflowStatusColors:
    """Tests for status color/icon in workflow step table (#1241)."""

    def test_step_table_contains_status_styled(self) -> None:
        from io import StringIO
        from unittest.mock import patch

        from rich.console import Console

        payload = {
            "run": {
                "id": "abc12345-1234-5678-9012-abcdef123456",
                "workflow_id": "test_wf",
                "workflow_version": "1",
                "target_kind": "issue",
                "target_ref": "42",
                "status": "running",
            },
            "steps": [
                {"step_id": "step1", "step_type": "runner", "status": "completed", "result_status": "success"},
                {"step_id": "step2", "step_type": "runner", "status": "running", "result_status": None},
            ],
            "checkpoint_count": 0,
            "pending_approvals": [],
            "pending_decisions": [],
        }
        buf = StringIO()
        test_console = Console(file=buf, force_terminal=True, width=120)
        with patch.object(observe_cli, "console", test_console):
            observe_cli._render_workflow(payload)
        text = buf.getvalue()
        assert "completed" in text
        assert "running" in text


class TestRenderMissionStatusColors:
    """Tests for status color/icon in mission items table (#1241)."""

    def test_item_table_contains_status_styled(self) -> None:
        from io import StringIO
        from unittest.mock import patch

        from rich.console import Console

        payload = {
            "session": {
                "id": "sess12345-1234-5678-9012-abcdef123456",
                "title": "Test mission",
                "status": "active",
            },
            "items": [
                {
                    "id": "item1",
                    "summary": "Do thing A",
                    "status": "completed",
                    "latest_execution": {"attempt_number": 1, "status": "success"},
                    "linked_workflow": None,
                    "blockers": [],
                },
                {
                    "id": "item2",
                    "summary": "Do thing B",
                    "status": "pending",
                    "latest_execution": None,
                    "linked_workflow": None,
                    "blockers": ["eligible"],
                },
            ],
        }
        buf = StringIO()
        test_console = Console(file=buf, force_terminal=True, width=120)
        with patch.object(observe_cli, "console", test_console):
            observe_cli._render_mission(payload)
        text = buf.getvalue()
        assert "completed" in text
        assert "pending" in text
        assert "Do thing A" in text
        assert "Do thing B" in text


def test_render_mission_shows_item_type() -> None:
    from io import StringIO
    from unittest.mock import patch

    from rich.console import Console

    payload = {
        "session": {
            "id": "sess-1234567890",
            "title": "Typed mission",
            "status": "active",
        },
        "items": [
            {
                "id": "item1",
                "summary": "Write docs",
                "item_type": "docs",
                "status": "pending",
                "latest_execution": None,
                "linked_workflow": None,
                "blockers": ["eligible"],
            },
            {
                "id": "item2",
                "summary": "Research topic",
                "item_type": "research",
                "status": "pending",
                "latest_execution": None,
                "linked_workflow": None,
                "blockers": ["eligible"],
            },
        ],
    }
    buf = StringIO()
    test_console = Console(file=buf, force_terminal=True, width=120)
    with patch.object(observe_cli, "console", test_console):
        observe_cli._render_mission(payload)
    text = buf.getvalue()
    assert "docs" in text
    assert "research" in text
    assert "Type" in text
    assert "ID" in text
    assert "item1"[:8] in text
    assert "item2"[:8] in text
