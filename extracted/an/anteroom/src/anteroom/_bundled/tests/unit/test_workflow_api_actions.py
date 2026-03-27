"""Tests for workflow API action endpoints (#890): cancel, approve, deny, respond, resume."""

from __future__ import annotations

import tempfile
from pathlib import Path
from typing import Any

import pytest
from starlette.testclient import TestClient

from anteroom.db import init_db
from anteroom.services.workflow_storage import (
    create_approval_request,
    create_human_decision,
    create_workflow_run,
    get_workflow_run,
    update_workflow_run,
)

_MINIMAL_WORKFLOW_YAML = """
kind: workflow
id: test
version: "0.1.0"
steps:
  - id: step1
    type: runner
    runner: stub
    prompt: "test"
""".strip()


@pytest.fixture()
def test_app():
    from unittest.mock import MagicMock

    from fastapi import FastAPI

    from anteroom.config import WorkflowConfig
    from anteroom.routers.workflows import router

    with tempfile.TemporaryDirectory() as td:
        db = init_db(Path(td) / "test.db")

        app = FastAPI()
        app.state.db = db

        # Minimal config for resume endpoint
        config = MagicMock()
        config.workflow = WorkflowConfig()
        config.ai.allowed_domains = []
        config.ai.block_localhost_api = False
        app.state.config = config
        app.state.event_bus = None
        app.state.artifact_registry = None
        app.state.skill_registry = None
        app.state.audit_writer = None

        app.include_router(router, prefix="/api")

        yield app, db
        db.close()


@pytest.fixture()
def client(test_app: tuple) -> TestClient:
    app, _ = test_app
    return TestClient(app)


@pytest.fixture()
def db(test_app: tuple) -> Any:
    _, db = test_app
    return db


def _make_run(db: Any, **overrides: Any) -> dict[str, Any]:
    defaults = {
        "workflow_id": "test",
        "workflow_version": "0.1.0",
        "target_kind": "task",
        "target_ref": "t1",
    }
    defaults.update(overrides)
    return create_workflow_run(db, **defaults)


# ---------------------------------------------------------------------------
# POST /workflow-runs/{run_id}/cancel
# ---------------------------------------------------------------------------


class TestCancelEndpoint:
    def test_cancel_running_run(self, client: TestClient, db: Any) -> None:
        run = _make_run(db)
        update_workflow_run(db, run["id"], status="running")
        resp = client.post(f"/api/workflow-runs/{run['id']}/cancel")
        assert resp.status_code == 200
        data = resp.json()
        assert data["run_id"] == run["id"]

    def test_cancel_paused_run(self, client: TestClient, db: Any) -> None:
        run = _make_run(db)
        update_workflow_run(db, run["id"], status="paused")
        resp = client.post(f"/api/workflow-runs/{run['id']}/cancel")
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "cancelled"

    def test_cancel_completed_run_409(self, client: TestClient, db: Any) -> None:
        run = _make_run(db)
        update_workflow_run(db, run["id"], status="completed")
        resp = client.post(f"/api/workflow-runs/{run['id']}/cancel")
        assert resp.status_code == 409

    def test_cancel_not_found_404(self, client: TestClient) -> None:
        resp = client.post("/api/workflow-runs/nonexistent/cancel")
        assert resp.status_code == 404

    def test_cancel_blocked_run_accepted(self, client: TestClient, db: Any) -> None:
        """Blocked runs can be cancelled — not terminal (#1141)."""
        run = _make_run(db)
        update_workflow_run(db, run["id"], status="blocked")
        resp = client.post(f"/api/workflow-runs/{run['id']}/cancel")
        assert resp.status_code == 200


# ---------------------------------------------------------------------------
# POST /workflow-runs/{run_id}/approve
# ---------------------------------------------------------------------------


class TestApproveEndpoint:
    def test_approve_pending(self, client: TestClient, db: Any) -> None:
        run = _make_run(db)
        update_workflow_run(db, run["id"], status="waiting_for_approval")
        create_approval_request(
            db,
            run_id=run["id"],
            step_id="step1",
            tool_name="bash",
            tool_args={"command": "ls"},
            risk_tier="EXECUTE",
        )
        resp = client.post(f"/api/workflow-runs/{run['id']}/approve")
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "approved"

    def test_approve_no_pending_404(self, client: TestClient, db: Any) -> None:
        run = _make_run(db)
        resp = client.post(f"/api/workflow-runs/{run['id']}/approve")
        assert resp.status_code == 404

    def test_approve_run_not_found_404(self, client: TestClient) -> None:
        resp = client.post("/api/workflow-runs/nonexistent/approve")
        assert resp.status_code == 404

    def test_approve_with_resolved_by(self, client: TestClient, db: Any) -> None:
        run = _make_run(db)
        update_workflow_run(db, run["id"], status="waiting_for_approval")
        create_approval_request(
            db,
            run_id=run["id"],
            step_id="step1",
            tool_name="bash",
            tool_args={},
            risk_tier="WRITE",
        )
        resp = client.post(
            f"/api/workflow-runs/{run['id']}/approve",
            json={"resolved_by": "admin"},
        )
        assert resp.status_code == 200


# ---------------------------------------------------------------------------
# POST /workflow-runs/{run_id}/deny
# ---------------------------------------------------------------------------


class TestDenyEndpoint:
    def test_deny_pending(self, client: TestClient, db: Any) -> None:
        run = _make_run(db)
        update_workflow_run(db, run["id"], status="waiting_for_approval")
        create_approval_request(
            db,
            run_id=run["id"],
            step_id="step1",
            tool_name="write_file",
            tool_args={"path": "/tmp/test.txt"},
            risk_tier="WRITE",
        )
        resp = client.post(f"/api/workflow-runs/{run['id']}/deny")
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "denied"
        # Run should be paused
        updated_run = get_workflow_run(db, run["id"])
        assert updated_run is not None
        assert updated_run["status"] == "paused"

    def test_deny_no_pending_404(self, client: TestClient, db: Any) -> None:
        run = _make_run(db)
        resp = client.post(f"/api/workflow-runs/{run['id']}/deny")
        assert resp.status_code == 404

    def test_deny_run_not_found_404(self, client: TestClient) -> None:
        resp = client.post("/api/workflow-runs/nonexistent/deny")
        assert resp.status_code == 404


# ---------------------------------------------------------------------------
# POST /workflow-runs/{run_id}/respond
# ---------------------------------------------------------------------------


class TestRespondEndpoint:
    def test_respond_pending_decision(self, client: TestClient, db: Any) -> None:
        run = _make_run(db)
        update_workflow_run(db, run["id"], status="waiting_for_input")
        create_human_decision(
            db,
            run_id=run["id"],
            step_id="gate1",
            prompt="Continue?",
            options=[{"value": "yes"}, {"value": "no"}],
        )
        resp = client.post(
            f"/api/workflow-runs/{run['id']}/respond",
            json={"selected_option": "yes"},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["selected_option"] == "yes"

    def test_respond_no_pending_404(self, client: TestClient, db: Any) -> None:
        run = _make_run(db)
        resp = client.post(
            f"/api/workflow-runs/{run['id']}/respond",
            json={"selected_option": "yes"},
        )
        assert resp.status_code == 404

    def test_respond_run_not_found_404(self, client: TestClient) -> None:
        resp = client.post(
            "/api/workflow-runs/nonexistent/respond",
            json={"selected_option": "yes"},
        )
        assert resp.status_code == 404

    def test_respond_missing_option_422(self, client: TestClient, db: Any) -> None:
        run = _make_run(db)
        resp = client.post(
            f"/api/workflow-runs/{run['id']}/respond",
            json={},
        )
        assert resp.status_code == 422


# ---------------------------------------------------------------------------
# POST /workflow-runs/{run_id}/resume
# ---------------------------------------------------------------------------


class TestResumeEndpoint:
    def test_resume_paused_run(self, client: TestClient, db: Any) -> None:
        run = _make_run(db)
        update_workflow_run(db, run["id"], status="paused", definition_content=_MINIMAL_WORKFLOW_YAML)
        resp = client.post(f"/api/workflow-runs/{run['id']}/resume")
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "resuming"

    def test_resume_waiting_for_approval_resolved(self, client: TestClient, db: Any) -> None:
        """Resume succeeds when the pending approval has been resolved."""
        run = _make_run(db)
        update_workflow_run(db, run["id"], status="waiting_for_approval", definition_content=_MINIMAL_WORKFLOW_YAML)
        # No pending approval → resolved, so resume is allowed
        resp = client.post(f"/api/workflow-runs/{run['id']}/resume")
        assert resp.status_code == 200

    def test_resume_waiting_for_approval_unresolved_409(self, client: TestClient, db: Any) -> None:
        """Resume blocked when approval is still pending."""
        run = _make_run(db)
        update_workflow_run(db, run["id"], status="waiting_for_approval", definition_content=_MINIMAL_WORKFLOW_YAML)
        create_approval_request(
            db,
            run_id=run["id"],
            step_id="step1",
            tool_name="bash",
            tool_args={},
            risk_tier="WRITE",
        )
        resp = client.post(f"/api/workflow-runs/{run['id']}/resume")
        assert resp.status_code == 409
        assert "unresolved approval" in resp.json()["detail"].lower()

    def test_resume_waiting_for_input_resolved(self, client: TestClient, db: Any) -> None:
        """Resume succeeds when the pending decision has been resolved."""
        run = _make_run(db)
        update_workflow_run(db, run["id"], status="waiting_for_input", definition_content=_MINIMAL_WORKFLOW_YAML)
        # No pending decision → resolved, so resume is allowed
        resp = client.post(f"/api/workflow-runs/{run['id']}/resume")
        assert resp.status_code == 200

    def test_resume_waiting_for_input_unresolved_409(self, client: TestClient, db: Any) -> None:
        """Resume blocked when human decision is still pending."""
        run = _make_run(db)
        update_workflow_run(db, run["id"], status="waiting_for_input", definition_content=_MINIMAL_WORKFLOW_YAML)
        create_human_decision(
            db,
            run_id=run["id"],
            step_id="step1",
            prompt="Choose",
            options=[{"id": "a"}, {"id": "b"}],
        )
        resp = client.post(f"/api/workflow-runs/{run['id']}/resume")
        assert resp.status_code == 409
        assert "unresolved human decision" in resp.json()["detail"].lower()

    def test_resume_failed_run(self, client: TestClient, db: Any) -> None:
        """POST /resume on a failed run returns 200 and triggers resume."""
        run = _make_run(db)
        update_workflow_run(
            db,
            run["id"],
            status="failed",
            stop_reason="step_failed:s1",
            definition_content=_MINIMAL_WORKFLOW_YAML,
        )
        resp = client.post(f"/api/workflow-runs/{run['id']}/resume")
        assert resp.status_code == 200
        assert resp.json()["status"] == "resuming"

    def test_resume_running_run_409(self, client: TestClient, db: Any) -> None:
        run = _make_run(db)
        update_workflow_run(db, run["id"], status="running")
        resp = client.post(f"/api/workflow-runs/{run['id']}/resume")
        assert resp.status_code == 409

    def test_resume_completed_run_409(self, client: TestClient, db: Any) -> None:
        run = _make_run(db)
        update_workflow_run(db, run["id"], status="completed")
        resp = client.post(f"/api/workflow-runs/{run['id']}/resume")
        assert resp.status_code == 409

    def test_resume_no_definition_422(self, client: TestClient, db: Any) -> None:
        run = _make_run(db)
        update_workflow_run(db, run["id"], status="paused")
        resp = client.post(f"/api/workflow-runs/{run['id']}/resume")
        assert resp.status_code == 422

    def test_resume_not_found_404(self, client: TestClient) -> None:
        resp = client.post("/api/workflow-runs/nonexistent/resume")
        assert resp.status_code == 404

    def test_resume_blocked_run_accepted(self, client: TestClient, db: Any) -> None:
        """Blocked runs can be resumed (#1141)."""
        run = _make_run(db)
        update_workflow_run(db, run["id"], status="blocked", definition_content=_MINIMAL_WORKFLOW_YAML)
        resp = client.post(f"/api/workflow-runs/{run['id']}/resume")
        assert resp.status_code == 200
        assert resp.json()["status"] == "resuming"


# ---------------------------------------------------------------------------
# GET /workflow-runs/{run_id} — recovery_actions field (#1153)
# ---------------------------------------------------------------------------


class TestRunDetailRecoveryActions:
    def test_run_detail_includes_recovery_actions(self, client: TestClient, db: Any) -> None:
        """Non-success run includes recovery_actions in detail response."""
        run = _make_run(db)
        update_workflow_run(db, run["id"], status="waiting_for_approval")
        resp = client.get(f"/api/workflow-runs/{run['id']}")
        assert resp.status_code == 200
        data = resp.json()
        assert "recovery_actions" in data
        assert len(data["recovery_actions"]) > 0
        assert any("approve" in a.lower() for a in data["recovery_actions"])

    def test_run_detail_no_recovery_for_completed(self, client: TestClient, db: Any) -> None:
        """Completed run has empty recovery_actions list."""
        run = _make_run(db)
        update_workflow_run(db, run["id"], status="completed")
        resp = client.get(f"/api/workflow-runs/{run['id']}")
        assert resp.status_code == 200
        data = resp.json()
        assert "recovery_actions" in data
        assert data["recovery_actions"] == []
