"""Tests for workflow router endpoints."""

from __future__ import annotations

import tempfile
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

import pytest
from starlette.testclient import TestClient

from anteroom.db import init_db
from anteroom.services.workflow_storage import (
    create_workflow_event,
    create_workflow_run,
    create_workflow_step,
    get_workflow_run,
    update_workflow_step,
)


@pytest.fixture()
def test_app():
    """Create a minimal FastAPI app with the workflow router for testing."""
    from fastapi import FastAPI

    from anteroom.routers.workflows import router

    with tempfile.TemporaryDirectory() as td:
        db = init_db(Path(td) / "test.db")

        app = FastAPI()
        app.state.db = db
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


class TestListWorkflows:
    def test_returns_list(self, client: TestClient) -> None:
        resp = client.get("/api/workflows")
        assert resp.status_code == 200
        assert isinstance(resp.json(), list)


class TestListWorkflowRuns:
    def test_empty_list(self, client: TestClient) -> None:
        resp = client.get("/api/workflow-runs")
        assert resp.status_code == 200
        assert resp.json() == []

    def test_with_runs(self, client: TestClient, db: Any) -> None:
        create_workflow_run(
            db,
            workflow_id="test",
            workflow_version="0.1.0",
            target_kind="task",
            target_ref="t1",
        )
        resp = client.get("/api/workflow-runs")
        assert resp.status_code == 200
        runs = resp.json()
        assert len(runs) == 1
        assert runs[0]["workflow_id"] == "test"

    def test_filter_by_status(self, client: TestClient, db: Any) -> None:
        run = create_workflow_run(
            db,
            workflow_id="test",
            workflow_version="0.1.0",
            target_kind="task",
            target_ref="t1",
        )
        from anteroom.services.workflow_storage import update_workflow_run

        update_workflow_run(db, run["id"], status="completed")

        resp = client.get("/api/workflow-runs?status=completed")
        assert len(resp.json()) == 1
        resp2 = client.get("/api/workflow-runs?status=running")
        assert len(resp2.json()) == 0


class TestGetWorkflowRun:
    def test_returns_run_with_steps(self, client: TestClient, db: Any) -> None:
        run = create_workflow_run(
            db,
            workflow_id="test",
            workflow_version="0.1.0",
            target_kind="task",
            target_ref="t1",
        )
        create_workflow_step(
            db,
            run_id=run["id"],
            step_id="s1",
            step_type="runner",
        )
        resp = client.get(f"/api/workflow-runs/{run['id']}")
        assert resp.status_code == 200
        data = resp.json()
        assert data["workflow_id"] == "test"
        assert len(data["steps"]) == 1
        assert data["pending_approval"] is None

    def test_404_on_missing(self, client: TestClient) -> None:
        resp = client.get("/api/workflow-runs/nonexistent")
        assert resp.status_code == 404


class TestGetWorkflowEvents:
    def test_returns_events(self, client: TestClient, db: Any) -> None:
        run = create_workflow_run(
            db,
            workflow_id="test",
            workflow_version="0.1.0",
            target_kind="task",
            target_ref="t1",
        )
        create_workflow_event(
            db,
            run_id=run["id"],
            event_type="run_started",
            payload={"workflow_id": "test"},
        )
        resp = client.get(f"/api/workflow-runs/{run['id']}/events")
        assert resp.status_code == 200
        events = resp.json()
        assert len(events) == 1
        assert events[0]["event_type"] == "run_started"

    def test_404_on_missing_run(self, client: TestClient) -> None:
        resp = client.get("/api/workflow-runs/nonexistent/events")
        assert resp.status_code == 404


class TestGetWorkflowRunLlmStepArtifacts:
    """Verify that llm step result_artifacts (model, tokens, structured_output) are
    visible through the GET /api/workflow-runs/{run_id} endpoint."""

    def test_llm_step_result_artifacts_visible(self, client: TestClient, db: Any) -> None:
        run = create_workflow_run(
            db,
            workflow_id="llm-test",
            workflow_version="0.1.0",
            target_kind="task",
            target_ref="t1",
        )
        step = create_workflow_step(
            db,
            run_id=run["id"],
            step_id="summarize",
            step_type="llm",
        )
        update_workflow_step(
            db,
            step["id"],
            status="completed",
            result_status="success",
            result_summary="Summary of the report",
            result_artifacts={
                "model": "gpt-4o-mini",
                "prompt_tokens": 150,
                "completion_tokens": 80,
                "total_tokens": 230,
            },
        )

        resp = client.get(f"/api/workflow-runs/{run['id']}")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data["steps"]) == 1
        artifacts = data["steps"][0]["result_artifacts"]
        assert artifacts is not None
        assert artifacts["model"] == "gpt-4o-mini"
        assert artifacts["total_tokens"] == 230
        assert artifacts["prompt_tokens"] == 150
        assert artifacts["completion_tokens"] == 80

    def test_llm_step_structured_output_visible(self, client: TestClient, db: Any) -> None:
        run = create_workflow_run(
            db,
            workflow_id="llm-json-test",
            workflow_version="0.1.0",
            target_kind="task",
            target_ref="t2",
        )
        step = create_workflow_step(
            db,
            run_id=run["id"],
            step_id="extract",
            step_type="llm",
        )
        update_workflow_step(
            db,
            step["id"],
            status="completed",
            result_status="success",
            result_summary='{"title": "Test"}',
            result_artifacts={
                "model": "gpt-4o-mini",
                "prompt_tokens": 100,
                "completion_tokens": 50,
                "total_tokens": 150,
                "structured_output": {"title": "Test"},
            },
        )

        resp = client.get(f"/api/workflow-runs/{run['id']}")
        assert resp.status_code == 200
        data = resp.json()
        artifacts = data["steps"][0]["result_artifacts"]
        assert artifacts["structured_output"] == {"title": "Test"}


# ---------------------------------------------------------------------------
# POST /workflow-runs (enqueue) (#888)
# ---------------------------------------------------------------------------


@pytest.fixture()
def executor_app():
    """App with executor_enabled config for POST endpoint tests."""
    from fastapi import FastAPI

    from anteroom.config import AIConfig, WorkflowConfig
    from anteroom.routers.workflows import router

    with tempfile.TemporaryDirectory() as td:
        db = init_db(Path(td) / "test.db")
        app = FastAPI()
        app.state.db = db
        wf_config = WorkflowConfig(executor_enabled=True)
        ai_config = AIConfig(base_url="http://localhost:1/v1", api_key="test", model="test")
        mock_config = MagicMock()
        mock_config.workflow = wf_config
        mock_config.ai = ai_config
        app.state.config = mock_config
        app.include_router(router, prefix="/api")
        yield app, db
        db.close()


@pytest.fixture()
def executor_client(executor_app: tuple) -> TestClient:
    app, _ = executor_app
    return TestClient(app)


@pytest.fixture()
def executor_db(executor_app: tuple) -> Any:
    _, db = executor_app
    return db


class TestEnqueueWorkflowRun:
    def test_503_when_executor_disabled(self, client: TestClient) -> None:
        """POST returns 503 when executor is not enabled."""
        from anteroom.config import WorkflowConfig

        app = client.app
        app.state.config = MagicMock()
        app.state.config.workflow = WorkflowConfig(executor_enabled=False)

        resp = client.post(
            "/api/workflow-runs",
            json={"workflow_id": "test", "target_ref": "t"},
        )
        assert resp.status_code == 503

    def test_404_unknown_workflow(self, executor_client: TestClient) -> None:
        resp = executor_client.post(
            "/api/workflow-runs",
            json={"workflow_id": "nonexistent-xyz", "target_ref": "t"},
        )
        assert resp.status_code == 404

    def test_201_enqueues_run(self, executor_client: TestClient, executor_db: Any) -> None:
        """POST with a valid workflow returns 201 and creates a pending run."""
        mock_def = MagicMock()
        mock_def.id = "test-wf"
        mock_def.version = "1.0"
        mock_def.notifications = None
        mock_def.inputs = {}
        mock_def.steps = []
        mock_def.raw_yaml = b""
        mock_def.content_hash = ""
        mock_def.policies = {}

        with (
            patch("anteroom.services.workflow_resolution.resolve_workflow_path") as mock_resolve,
            patch("anteroom.services.workflow_engine.load_definition") as mock_load,
        ):
            mock_resolve.return_value = Path("/fake/path.yaml")
            mock_load.return_value = mock_def

            resp = executor_client.post(
                "/api/workflow-runs",
                json={"workflow_id": "test-wf", "target_ref": "my-target"},
            )

        assert resp.status_code == 201
        data = resp.json()
        assert "run_id" in data

        run = get_workflow_run(executor_db, data["run_id"])
        assert run["status"] == "pending"
        assert run["trigger_source"] == "web_api"


# ---------------------------------------------------------------------------
# PATCH /workflow-runs/{run_id}/repair (#995)
# ---------------------------------------------------------------------------


@pytest.fixture()
def repair_app():
    """App with config.identity for server-side actor resolution."""
    from fastapi import FastAPI

    from anteroom.config import WorkflowConfig
    from anteroom.routers.workflows import router

    with tempfile.TemporaryDirectory() as td:
        db = init_db(Path(td) / "test.db")
        app = FastAPI()
        app.state.db = db
        mock_config = MagicMock()
        mock_config.workflow = WorkflowConfig()
        mock_config.identity.user_id = "test-user-id"
        app.state.config = mock_config
        app.include_router(router, prefix="/api")
        yield app, db
        db.close()


@pytest.fixture()
def repair_client(repair_app: tuple) -> TestClient:
    app, _ = repair_app
    return TestClient(app)


@pytest.fixture()
def repair_db(repair_app: tuple) -> Any:
    _, db = repair_app
    return db


class TestRepairWorkflowRun:
    def test_repair_run_inputs(self, repair_client: TestClient, repair_db: Any) -> None:
        from anteroom.services.workflow_storage import update_workflow_run

        run = create_workflow_run(
            repair_db,
            workflow_id="test",
            workflow_version="0.1.0",
            target_kind="task",
            target_ref="t1",
            inputs={"issue": 42},
        )
        update_workflow_run(repair_db, run["id"], status="paused")

        resp = repair_client.patch(
            f"/api/workflow-runs/{run['id']}/repair",
            json={"field_path": "inputs", "value": {"issue": 99}},
        )
        assert resp.status_code == 200
        assert resp.json()["inputs"] == {"issue": 99}

    def test_repair_step_artifacts(self, repair_client: TestClient, repair_db: Any) -> None:
        from anteroom.services.workflow_storage import update_workflow_run

        run = create_workflow_run(
            repair_db,
            workflow_id="test",
            workflow_version="0.1.0",
            target_kind="task",
            target_ref="t1",
        )
        update_workflow_run(repair_db, run["id"], status="paused")
        step = create_workflow_step(repair_db, run_id=run["id"], step_id="s1", step_type="runner")
        update_workflow_step(
            repair_db,
            step["id"],
            status="completed",
            result_status="success",
            result_artifacts={"pr": 1},
        )

        resp = repair_client.patch(
            f"/api/workflow-runs/{run['id']}/repair",
            json={"field_path": "step.s1.result_artifacts", "value": {"pr": 2}},
        )
        assert resp.status_code == 200
        assert resp.json()["result_artifacts"] == {"pr": 2}

    def test_repair_404_missing_run(self, repair_client: TestClient) -> None:
        resp = repair_client.patch(
            "/api/workflow-runs/nonexistent/repair",
            json={"field_path": "inputs", "value": {}},
        )
        assert resp.status_code == 404

    def test_repair_422_invalid_field(self, repair_client: TestClient, repair_db: Any) -> None:
        from anteroom.services.workflow_storage import update_workflow_run

        run = create_workflow_run(
            repair_db,
            workflow_id="test",
            workflow_version="0.1.0",
            target_kind="task",
            target_ref="t1",
        )
        update_workflow_run(repair_db, run["id"], status="paused")

        resp = repair_client.patch(
            f"/api/workflow-runs/{run['id']}/repair",
            json={"field_path": "status", "value": "completed"},
        )
        assert resp.status_code == 422

    def test_repair_422_non_paused_run(self, repair_client: TestClient, repair_db: Any) -> None:
        run = create_workflow_run(
            repair_db,
            workflow_id="test",
            workflow_version="0.1.0",
            target_kind="task",
            target_ref="t1",
            inputs={"x": 1},
        )
        # Run is in 'pending' status — not repairable
        resp = repair_client.patch(
            f"/api/workflow-runs/{run['id']}/repair",
            json={"field_path": "inputs", "value": {"x": 2}},
        )
        assert resp.status_code == 422

    def test_repair_failed_run_inputs(self, repair_client: TestClient, repair_db: Any) -> None:
        """PATCH /repair on a failed run returns 200."""
        from anteroom.services.workflow_storage import update_workflow_run

        run = create_workflow_run(
            repair_db,
            workflow_id="test",
            workflow_version="0.1.0",
            target_kind="task",
            target_ref="t1",
            inputs={"x": 1},
        )
        update_workflow_run(repair_db, run["id"], status="failed", stop_reason="step_failed:s1")
        resp = repair_client.patch(
            f"/api/workflow-runs/{run['id']}/repair",
            json={"field_path": "inputs", "value": {"x": 2}},
        )
        assert resp.status_code == 200
        assert resp.json()["inputs"] == {"x": 2}

    def test_repair_422_empty_step_id(self, repair_client: TestClient, repair_db: Any) -> None:
        from anteroom.services.workflow_storage import update_workflow_run

        run = create_workflow_run(
            repair_db,
            workflow_id="test",
            workflow_version="0.1.0",
            target_kind="task",
            target_ref="t1",
        )
        update_workflow_run(repair_db, run["id"], status="paused")

        resp = repair_client.patch(
            f"/api/workflow-runs/{run['id']}/repair",
            json={"field_path": "step..result_artifacts", "value": {}},
        )
        assert resp.status_code == 422
        assert "empty" in resp.json()["detail"].lower()

    def test_repair_422_invalid_field_path_format(self, repair_client: TestClient, repair_db: Any) -> None:
        from anteroom.services.workflow_storage import update_workflow_run

        run = create_workflow_run(
            repair_db,
            workflow_id="test",
            workflow_version="0.1.0",
            target_kind="task",
            target_ref="t1",
        )
        update_workflow_run(repair_db, run["id"], status="paused")

        resp = repair_client.patch(
            f"/api/workflow-runs/{run['id']}/repair",
            json={"field_path": "a.b", "value": "x"},
        )
        assert resp.status_code == 422

    def test_repair_uses_server_identity_not_client(self, repair_client: TestClient, repair_db: Any) -> None:
        """Actor in audit event must come from server identity, not request body."""
        from anteroom.services.workflow_storage import list_workflow_events, update_workflow_run

        run = create_workflow_run(
            repair_db,
            workflow_id="test",
            workflow_version="0.1.0",
            target_kind="task",
            target_ref="t1",
            inputs={"x": 1},
        )
        update_workflow_run(repair_db, run["id"], status="paused")

        resp = repair_client.patch(
            f"/api/workflow-runs/{run['id']}/repair",
            json={"field_path": "inputs", "value": {"x": 2}},
        )
        assert resp.status_code == 200

        events = list_workflow_events(repair_db, run["id"])
        repair_events = [e for e in events if e["event_type"] == "repair_applied"]
        assert len(repair_events) == 1
        assert repair_events[0]["payload"]["actor"] == "test-user-id"


# ---------------------------------------------------------------------------
# GET /workflow-schedules (#969)
# ---------------------------------------------------------------------------


class TestWorkflowScheduleAPI:
    def test_list_empty(self, client: TestClient) -> None:
        resp = client.get("/api/workflow-schedules")
        assert resp.status_code == 200
        assert resp.json() == []

    def test_list_with_schedules(self, client: TestClient, db: Any) -> None:
        from anteroom.services.workflow_storage import create_schedule

        create_schedule(
            db,
            workflow_ref="test-wf",
            ref_type="builtin",
            cron_expr="0 * * * *",
            target_ref="t1",
            next_run_at="2026-01-01T00:00:00+00:00",
        )
        resp = client.get("/api/workflow-schedules")
        assert resp.status_code == 200
        schedules = resp.json()
        assert len(schedules) == 1
        assert schedules[0]["workflow_ref"] == "test-wf"

    def test_get_by_id(self, client: TestClient, db: Any) -> None:
        from anteroom.services.workflow_storage import create_schedule

        sched = create_schedule(
            db,
            workflow_ref="test-wf",
            ref_type="builtin",
            cron_expr="0 * * * *",
            target_ref="t1",
            next_run_at="2026-01-01T00:00:00+00:00",
        )
        resp = client.get(f"/api/workflow-schedules/{sched['id']}")
        assert resp.status_code == 200
        assert resp.json()["id"] == sched["id"]

    def test_get_404(self, client: TestClient) -> None:
        resp = client.get("/api/workflow-schedules/00000000-0000-0000-0000-000000000000")
        assert resp.status_code == 404

    def test_get_invalid_id_format(self, client: TestClient) -> None:
        resp = client.get("/api/workflow-schedules/not-a-uuid")
        assert resp.status_code == 422
