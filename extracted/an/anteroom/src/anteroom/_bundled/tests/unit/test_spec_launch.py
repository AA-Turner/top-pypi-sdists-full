"""Unit tests for spec task launch — get_task, launch_from_task, and router/CLI."""

from __future__ import annotations

from pathlib import Path
from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from anteroom.services.spec_schema import SpecPhaseStatus

VALID_SPEC_YAML = """\
requirements: |
  Must support widgets.
design: |
  Use the widget parser pattern.
tasks:
  - id: t1
    summary: Implement widget parser
  - id: t2
    summary: Add validation layer
    depends_on: [t1]
"""


@pytest.fixture()
def db(tmp_path: Path) -> Any:
    from anteroom.db import init_db

    return init_db(tmp_path / "test.db")


@pytest.fixture()
def spec_fqn(db: Any) -> str:
    from anteroom.services.spec_service import create_spec

    create_spec(db, "ns", "feat", VALID_SPEC_YAML)
    return "@ns/spec/feat"


# ---------------------------------------------------------------------------
# get_task
# ---------------------------------------------------------------------------


class TestGetTask:
    def test_found(self, db: Any, spec_fqn: str) -> None:
        from anteroom.services.spec_service import get_task

        result = get_task(db, spec_fqn, "t1")
        assert result is not None
        art, task = result
        assert art["fqn"] == spec_fqn
        assert task.id == "t1"
        assert task.summary == "Implement widget parser"

    def test_not_found_bad_task_id(self, db: Any, spec_fqn: str) -> None:
        from anteroom.services.spec_service import get_task

        assert get_task(db, spec_fqn, "nonexistent") is None

    def test_not_found_bad_fqn(self, db: Any) -> None:
        from anteroom.services.spec_service import get_task

        assert get_task(db, "@ns/spec/nope", "t1") is None

    def test_second_task(self, db: Any, spec_fqn: str) -> None:
        from anteroom.services.spec_service import get_task

        result = get_task(db, spec_fqn, "t2")
        assert result is not None
        _, task = result
        assert task.id == "t2"
        assert task.depends_on == ["t1"]


# ---------------------------------------------------------------------------
# launch_from_task
# ---------------------------------------------------------------------------


class TestLaunchFromTask:
    def test_happy_path(self, db: Any, spec_fqn: str) -> None:
        from anteroom.services.spec_service import approve_phase, launch_from_task

        approve_phase(db, spec_fqn, "tasks", "troy")
        inputs = launch_from_task(db, spec_fqn, "t1", "my-workflow")
        assert inputs["spec_fqn"] == spec_fqn
        assert inputs["task_id"] == "t1"
        assert inputs["task_summary"] == "Implement widget parser"

    def test_spec_not_found(self, db: Any) -> None:
        from anteroom.services.spec_service import launch_from_task

        with pytest.raises(ValueError, match="Spec not found"):
            launch_from_task(db, "@ns/spec/nope", "t1", "wf")

    def test_invalid_task_id(self, db: Any, spec_fqn: str) -> None:
        from anteroom.services.spec_service import approve_phase, launch_from_task

        approve_phase(db, spec_fqn, "tasks", "troy")
        with pytest.raises(ValueError, match="Task.*not found"):
            launch_from_task(db, spec_fqn, "bad-task", "wf")

    def test_tasks_not_approved(self, db: Any, spec_fqn: str) -> None:
        from anteroom.services.spec_service import launch_from_task

        with pytest.raises(ValueError, match="must be approved"):
            launch_from_task(db, spec_fqn, "t1", "wf")

    def test_tasks_stale_rejected(self, db: Any, spec_fqn: str) -> None:
        from anteroom.services import artifact_storage
        from anteroom.services.spec_schema import set_phase_status
        from anteroom.services.spec_service import launch_from_task

        art = artifact_storage.get_artifact_by_fqn(db, spec_fqn)
        assert art is not None
        new_meta = set_phase_status(art["metadata"], "tasks", SpecPhaseStatus.STALE)
        artifact_storage.update_artifact(db, art["id"], metadata=new_meta)

        with pytest.raises(ValueError, match="must be approved"):
            launch_from_task(db, spec_fqn, "t1", "wf")

    def test_extra_inputs_merged(self, db: Any, spec_fqn: str) -> None:
        from anteroom.services.spec_service import approve_phase, launch_from_task

        approve_phase(db, spec_fqn, "tasks", "troy")
        inputs = launch_from_task(db, spec_fqn, "t1", "wf", extra_inputs={"branch": "main", "dry_run": True})
        assert inputs["branch"] == "main"
        assert inputs["dry_run"] is True
        assert inputs["spec_fqn"] == spec_fqn


# ---------------------------------------------------------------------------
# Router: POST /specs/{fqn}/tasks/{task_id}/launch
# ---------------------------------------------------------------------------


class TestLaunchEndpoint:
    @pytest.fixture()
    def client_with_config(self, db: Any) -> Any:
        from fastapi import FastAPI
        from fastapi.testclient import TestClient

        from anteroom.routers.specs import router

        app = FastAPI()
        app.include_router(router, prefix="/api")
        app.state.db = db

        mock_config = MagicMock()
        mock_config.workflow.credentials = {}
        mock_config.ai.allowed_domains = []
        mock_config.ai.block_localhost_api = False
        app.state.config = mock_config

        return TestClient(app)

    def test_launch_spec_not_found(self, client_with_config: Any) -> None:
        resp = client_with_config.post(
            "/api/specs/@ns/spec/nope/tasks/t1/launch",
            json={"workflow_id": "wf"},
        )
        assert resp.status_code == 422
        assert "not found" in resp.json()["detail"].lower()

    def test_launch_invalid_fqn(self, client_with_config: Any) -> None:
        resp = client_with_config.post(
            "/api/specs/bad-fqn/tasks/t1/launch",
            json={"workflow_id": "wf"},
        )
        assert resp.status_code == 400

    def test_launch_invalid_task(self, db: Any, spec_fqn: str, client_with_config: Any) -> None:
        from anteroom.services.spec_service import approve_phase

        approve_phase(db, spec_fqn, "tasks", "troy")
        resp = client_with_config.post(
            f"/api/specs/{spec_fqn}/tasks/bad-task/launch",
            json={"workflow_id": "wf"},
        )
        assert resp.status_code == 422

    def test_launch_workflow_not_found(self, db: Any, spec_fqn: str, client_with_config: Any) -> None:
        from anteroom.services.spec_service import approve_phase

        approve_phase(db, spec_fqn, "tasks", "troy")
        with patch("anteroom.services.workflow_resolution.resolve_workflow_path", return_value=None):
            resp = client_with_config.post(
                f"/api/specs/{spec_fqn}/tasks/t1/launch",
                json={"workflow_id": "nonexistent"},
            )
        assert resp.status_code == 404
        assert "Workflow not found" in resp.json()["detail"]


# ---------------------------------------------------------------------------
# Router: GET /specs/{fqn}/traceability
# ---------------------------------------------------------------------------


class TestTraceabilityEndpoint:
    @pytest.fixture()
    def client(self, db: Any) -> Any:
        from fastapi import FastAPI
        from fastapi.testclient import TestClient

        from anteroom.routers.specs import router

        app = FastAPI()
        app.include_router(router, prefix="/api")
        app.state.db = db
        return TestClient(app)

    def test_traceability_found(self, client: Any, db: Any, spec_fqn: str) -> None:
        resp = client.get(f"/api/specs/{spec_fqn}/traceability")
        assert resp.status_code == 200
        data = resp.json()
        assert data["fqn"] == spec_fqn
        assert "t1" in data["tasks"]
        assert "t2" in data["tasks"]

    def test_traceability_not_found(self, client: Any) -> None:
        resp = client.get("/api/specs/@ns/spec/nope/traceability")
        assert resp.status_code == 404

    def test_traceability_invalid_fqn(self, client: Any) -> None:
        resp = client.get("/api/specs/bad-fqn/traceability")
        assert resp.status_code == 400

    def test_traceability_with_runs(self, client: Any, db: Any, spec_fqn: str) -> None:
        from anteroom.services.workflow_storage import create_workflow_run

        create_workflow_run(
            db,
            workflow_id="wf1",
            workflow_version="1.0",
            target_kind="spec",
            target_ref=spec_fqn,
            inputs={"spec_fqn": spec_fqn, "task_id": "t1"},
        )
        resp = client.get(f"/api/specs/{spec_fqn}/traceability")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data["tasks"]["t1"]) == 1


# ---------------------------------------------------------------------------
# CLI: _handle_spec_command launch
# ---------------------------------------------------------------------------


class TestHandleSpecCommandLaunch:
    @pytest.mark.asyncio
    async def test_launch_missing_args(self, db: Any) -> None:
        from anteroom.cli.repl import _handle_spec_command

        with patch("anteroom.cli.repl.renderer") as mock_renderer:
            await _handle_spec_command("/spec launch", cmd="/spec", db=db)
            call_args = mock_renderer.console.print.call_args[0][0]
            assert "Usage" in call_args

    @pytest.mark.asyncio
    async def test_launch_spec_not_found(self, db: Any) -> None:
        from anteroom.cli.repl import _handle_spec_command

        mock_config = MagicMock()
        with patch("anteroom.cli.repl.renderer") as mock_renderer:
            await _handle_spec_command("/spec launch @ns/spec/nope t1 my-wf", cmd="/spec", db=db, config=mock_config)
            call_args = mock_renderer.console.print.call_args[0][0]
            assert "not found" in call_args.lower()

    @pytest.mark.asyncio
    async def test_launch_no_config(self, db: Any) -> None:
        from anteroom.cli.repl import _handle_spec_command

        with patch("anteroom.cli.repl.renderer") as mock_renderer:
            await _handle_spec_command("/spec launch @ns/spec/feat t1 my-wf", cmd="/spec", db=db, config=None)
            call_args = mock_renderer.console.print.call_args[0][0]
            assert "Config not available" in call_args

    @pytest.mark.asyncio
    async def test_launch_success(self, db: Any, spec_fqn: str) -> None:
        from anteroom.services.spec_service import approve_phase

        approve_phase(db, spec_fqn, "tasks", "troy")

        mock_config = MagicMock()
        mock_engine = MagicMock()
        mock_run = {"id": "run-123", "status": "completed"}
        mock_engine.start_run = AsyncMock(return_value=mock_run)
        mock_event_bus = MagicMock()

        with (
            patch("anteroom.cli.repl.renderer"),
            patch(
                "anteroom.cli.repl._handle_spec_command.__module__",
                create=True,
            ),
            patch(
                "anteroom.services.workflow_resolution.resolve_workflow_path",
                return_value=Path("/tmp/test.yaml"),
            ),
            patch(
                "anteroom.services.workflow_engine.load_definition",
                return_value=MagicMock(),
            ),
            patch(
                "anteroom.cli.workflow_cli._create_engine",
                return_value=(mock_engine, mock_event_bus),
            ),
            patch(
                "anteroom.cli.workflow_cli._cleanup_event_bus",
            ),
        ):
            from anteroom.cli.repl import _handle_spec_command

            await _handle_spec_command(f"/spec launch {spec_fqn} t1 my-wf", cmd="/spec", db=db, config=mock_config)
            mock_engine.start_run.assert_called_once()
            call_args = mock_engine.start_run.call_args
            assert call_args.kwargs["target_kind"] == "spec"
            assert call_args.kwargs["inputs"]["task_id"] == "t1"
