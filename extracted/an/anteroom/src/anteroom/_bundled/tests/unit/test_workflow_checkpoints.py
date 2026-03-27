"""Tests for workflow checkpoint storage, engine integration, sanitization, and API (#979)."""

from __future__ import annotations

import tempfile
from pathlib import Path
from typing import Any

import pytest

from anteroom.config import WorkflowConfig
from anteroom.db import init_db
from anteroom.services.workflow_engine import (
    WorkflowEngine,
    load_definition,
    register_gate_condition,
)
from anteroom.services.workflow_runners import create_default_registry
from anteroom.services.workflow_storage import (
    count_checkpoints,
    create_checkpoint,
    create_workflow_run,
    delete_workflow_run,
    get_latest_checkpoint,
    list_checkpoints,
)

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def db():
    with tempfile.TemporaryDirectory() as td:
        conn = init_db(Path(td) / "test.db")
        yield conn
        conn.close()


@pytest.fixture()
def engine(db: Any) -> WorkflowEngine:
    config = WorkflowConfig()
    registry = create_default_registry()
    return WorkflowEngine(db, config, registry)


@pytest.fixture(autouse=True)
def _register_test_gates():
    async def always_pass(run: Any, step: Any, inputs: Any) -> bool:
        return True

    async def always_fail(run: Any, step: Any, inputs: Any) -> bool:
        return False

    register_gate_condition("always_pass", always_pass)
    register_gate_condition("always_fail", always_fail)
    yield


def _make_run(db: Any) -> dict[str, Any]:
    return create_workflow_run(
        db,
        workflow_id="test",
        workflow_version="0.1.0",
        target_kind="task",
        target_ref="t1",
    )


# ---------------------------------------------------------------------------
# Storage tests
# ---------------------------------------------------------------------------


class TestCheckpointStorage:
    def test_create_checkpoint(self, db: Any) -> None:
        run = _make_run(db)
        cp = create_checkpoint(
            db,
            run_id=run["id"],
            label="after:step1",
            step_id="step1",
            step_results={"step1": {"result_status": "success"}},
            budget_usage={"total_tokens": 100},
            run_status="running",
        )
        assert cp["run_id"] == run["id"]
        assert cp["label"] == "after:step1"
        assert cp["step_id"] == "step1"
        assert cp["step_results"] == {"step1": {"result_status": "success"}}
        assert cp["budget_usage"] == {"total_tokens": 100}
        assert cp["run_status"] == "running"
        assert "id" in cp
        assert "created_at" in cp

    def test_list_checkpoints_ordered(self, db: Any) -> None:
        run = _make_run(db)
        create_checkpoint(
            db,
            run_id=run["id"],
            label="after:step1",
            step_id="step1",
            step_results={"step1": {"result_status": "success"}},
            budget_usage=None,
            run_status="running",
        )
        create_checkpoint(
            db,
            run_id=run["id"],
            label="after:step2",
            step_id="step2",
            step_results={"step1": {}, "step2": {}},
            budget_usage=None,
            run_status="running",
        )
        cps = list_checkpoints(db, run["id"])
        assert len(cps) == 2
        assert cps[0]["label"] == "after:step1"
        assert cps[1]["label"] == "after:step2"

    def test_get_latest_checkpoint(self, db: Any) -> None:
        run = _make_run(db)
        create_checkpoint(
            db,
            run_id=run["id"],
            label="after:step1",
            step_id="step1",
            step_results={},
            budget_usage=None,
            run_status="running",
        )
        create_checkpoint(
            db,
            run_id=run["id"],
            label="completed",
            step_id=None,
            step_results={},
            budget_usage=None,
            run_status="completed",
        )
        latest = get_latest_checkpoint(db, run["id"])
        assert latest is not None
        assert latest["label"] == "completed"

    def test_get_latest_checkpoint_empty(self, db: Any) -> None:
        run = _make_run(db)
        assert get_latest_checkpoint(db, run["id"]) is None

    def test_count_checkpoints(self, db: Any) -> None:
        run = _make_run(db)
        assert count_checkpoints(db, run["id"]) == 0
        create_checkpoint(
            db,
            run_id=run["id"],
            label="after:step1",
            step_id="step1",
            step_results={},
            budget_usage=None,
            run_status="running",
        )
        assert count_checkpoints(db, run["id"]) == 1

    def test_checkpoint_cascade_delete(self, db: Any) -> None:
        run = _make_run(db)
        create_checkpoint(
            db,
            run_id=run["id"],
            label="after:step1",
            step_id="step1",
            step_results={},
            budget_usage=None,
            run_status="running",
        )
        assert count_checkpoints(db, run["id"]) == 1
        delete_workflow_run(db, run["id"])
        assert count_checkpoints(db, run["id"]) == 0


# ---------------------------------------------------------------------------
# Engine integration tests
# ---------------------------------------------------------------------------

TWO_STEP_WORKFLOW = """\
kind: workflow
id: test_two_step
version: 0.1.0
inputs: {}
policies: {}
steps:
  - id: step_one
    type: runner
    runner: shell
    command: "echo step one"
    timeout: 10
  - id: step_two
    type: runner
    runner: shell
    command: "echo step two"
    timeout: 10
"""

FAIL_WORKFLOW = """\
kind: workflow
id: test_fail
version: 0.1.0
inputs: {}
policies: {}
steps:
  - id: will_fail
    type: runner
    runner: shell
    command: "exit 1"
    timeout: 10
"""

TWO_STEP_FAIL_WORKFLOW = """\
kind: workflow
id: test_two_step_fail
version: 0.1.0
inputs: {}
policies: {}
steps:
  - id: step_one
    type: runner
    runner: shell
    command: "echo step one"
    timeout: 10
  - id: step_two
    type: runner
    runner: shell
    command: "exit 1"
    timeout: 10
"""

GATE_BLOCK_WORKFLOW = """\
kind: workflow
id: test_gate_block
version: 0.1.0
inputs: {}
policies: {}
steps:
  - id: pre_check
    type: runner
    runner: shell
    command: "echo pre"
    timeout: 10
  - id: gate_block
    type: gate
    condition: always_fail
    if_false: not_ready
"""


class TestEngineCheckpoints:
    @pytest.mark.asyncio
    async def test_checkpoint_after_step_completion(self, db: Any, engine: WorkflowEngine) -> None:
        defn = load_definition(TWO_STEP_WORKFLOW)
        run = await engine.start_run(defn, target_kind="task", target_ref="t1")
        assert run["status"] == "completed"

        cps = list_checkpoints(db, run["id"])
        labels = [c["label"] for c in cps]
        assert "after:step_one" in labels
        assert "after:step_two" in labels

    @pytest.mark.asyncio
    async def test_checkpoint_on_completion(self, db: Any, engine: WorkflowEngine) -> None:
        defn = load_definition(TWO_STEP_WORKFLOW)
        run = await engine.start_run(defn, target_kind="task", target_ref="t1")

        cps = list_checkpoints(db, run["id"])
        labels = [c["label"] for c in cps]
        assert "completed" in labels

    @pytest.mark.asyncio
    async def test_checkpoint_on_failure(self, db: Any, engine: WorkflowEngine) -> None:
        defn = load_definition(FAIL_WORKFLOW)
        run = await engine.start_run(defn, target_kind="task", target_ref="t1")
        assert run["status"] == "failed"

        cps = list_checkpoints(db, run["id"])
        labels = [c["label"] for c in cps]
        assert any(label.startswith("failure:") for label in labels)

    @pytest.mark.asyncio
    async def test_checkpoint_budget_usage_captured(self, db: Any, engine: WorkflowEngine) -> None:
        defn = load_definition(TWO_STEP_WORKFLOW)
        run = await engine.start_run(defn, target_kind="task", target_ref="t1")

        cps = list_checkpoints(db, run["id"])
        after_step_two = [c for c in cps if c["label"] == "after:step_two"]
        assert len(after_step_two) == 1
        bu = after_step_two[0]["budget_usage"]
        assert bu is not None
        assert "steps_completed" in bu

    @pytest.mark.asyncio
    async def test_checkpoint_step_results_match(self, db: Any, engine: WorkflowEngine) -> None:
        defn = load_definition(TWO_STEP_WORKFLOW)
        run = await engine.start_run(defn, target_kind="task", target_ref="t1")

        cps = list_checkpoints(db, run["id"])
        completed_cp = [c for c in cps if c["label"] == "completed"]
        assert len(completed_cp) == 1
        sr = completed_cp[0]["step_results"]
        assert "step_one" in sr
        assert "step_two" in sr
        assert sr["step_one"]["result_status"] == "success"

    @pytest.mark.asyncio
    async def test_failure_checkpoint_includes_failing_step(self, db: Any, engine: WorkflowEngine) -> None:
        """Regression: failure checkpoint must include the failing step's data, not just prior steps."""
        defn = load_definition(TWO_STEP_FAIL_WORKFLOW)
        run = await engine.start_run(defn, target_kind="task", target_ref="t1")
        assert run["status"] == "failed"

        cps = list_checkpoints(db, run["id"])
        failure_cps = [c for c in cps if c["label"] == "failure:step_two"]
        assert len(failure_cps) == 1
        sr = failure_cps[0]["step_results"]
        # Must include BOTH step_one (success) and step_two (failure)
        assert "step_one" in sr, "failure checkpoint missing prior successful step"
        assert "step_two" in sr, "failure checkpoint missing the failing step itself"
        assert sr["step_one"]["result_status"] == "success"
        assert sr["step_two"]["result_status"] == "failed"

    @pytest.mark.asyncio
    async def test_blocked_checkpoint_includes_blocked_step(self, db: Any, engine: WorkflowEngine) -> None:
        """Regression: blocked checkpoint must include the blocked step's data."""
        defn = load_definition(GATE_BLOCK_WORKFLOW)
        run = await engine.start_run(defn, target_kind="task", target_ref="t1")

        cps = list_checkpoints(db, run["id"])
        blocked_cps = [c for c in cps if c["label"] == "blocked:gate_block"]
        assert len(blocked_cps) == 1
        sr = blocked_cps[0]["step_results"]
        assert "pre_check" in sr, "blocked checkpoint missing prior successful step"
        assert "gate_block" in sr, "blocked checkpoint missing the blocked step itself"
        assert sr["gate_block"]["result_status"] == "blocked"


# ---------------------------------------------------------------------------
# Sanitization tests
# ---------------------------------------------------------------------------


class TestSanitizeCheckpointData:
    def test_sanitize_truncates_summary(self) -> None:
        data = {
            "s1": {
                "result_status": "success",
                "result_summary": "x" * 600,
                "result_artifacts": {},
                "result_findings": None,
            }
        }
        result = WorkflowEngine._sanitize_checkpoint_data(data)
        assert len(result["s1"]["result_summary"]) == 500

    def test_sanitize_allowlists_artifact_keys(self) -> None:
        data = {
            "s1": {
                "result_status": "success",
                "result_summary": "ok",
                "result_artifacts": {
                    "total_tokens": 100,
                    "secret_key": "should-not-appear",
                    "model": "gpt-4",
                },
                "result_findings": None,
            }
        }
        result = WorkflowEngine._sanitize_checkpoint_data(data)
        arts = result["s1"]["result_artifacts"]
        assert "total_tokens" in arts
        assert "model" in arts
        assert "secret_key" not in arts

    def test_sanitize_preserves_safe_keys(self) -> None:
        safe_keys = {
            "result_status": "success",
            "total_tokens": 50,
            "prompt_tokens": 30,
            "completion_tokens": 20,
            "model": "gpt-4",
            "exit_code": 0,
            "tool_call_count": 3,
            "destination": "github",
            "bytes_written": 1024,
            "status_code": 200,
            "duration_ms": 450,
            "idempotency_key": "abc-123",
        }
        data = {
            "s1": {
                "result_status": "success",
                "result_summary": "ok",
                "result_artifacts": safe_keys,
                "result_findings": None,
            }
        }
        result = WorkflowEngine._sanitize_checkpoint_data(data)
        for k in safe_keys:
            if k == "result_status":
                continue
            assert k in result["s1"]["result_artifacts"]

    def test_sanitize_does_not_mutate_original(self) -> None:
        original_artifacts = {"total_tokens": 100, "secret": "leak"}
        data = {
            "s1": {
                "result_status": "success",
                "result_summary": "ok",
                "result_artifacts": original_artifacts,
                "result_findings": None,
            }
        }
        WorkflowEngine._sanitize_checkpoint_data(data)
        assert "secret" in data["s1"]["result_artifacts"]

    def test_sanitize_empty_results(self) -> None:
        result = WorkflowEngine._sanitize_checkpoint_data({})
        assert result == {}


# ---------------------------------------------------------------------------
# API tests
# ---------------------------------------------------------------------------


@pytest.fixture()
def test_app():
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
def client(test_app: tuple):
    from starlette.testclient import TestClient

    app, _ = test_app
    return TestClient(app)


@pytest.fixture()
def api_db(test_app: tuple) -> Any:
    _, db = test_app
    return db


class TestCheckpointAPI:
    def test_api_list_checkpoints(self, client: Any, api_db: Any) -> None:
        run = _make_run(api_db)
        create_checkpoint(
            api_db,
            run_id=run["id"],
            label="after:step1",
            step_id="step1",
            step_results={"step1": {"result_status": "success"}},
            budget_usage=None,
            run_status="running",
        )
        resp = client.get(f"/api/workflow-runs/{run['id']}/checkpoints")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data["checkpoints"]) == 1
        assert data["checkpoints"][0]["label"] == "after:step1"

    def test_api_run_detail_checkpoint_count(self, client: Any, api_db: Any) -> None:
        run = _make_run(api_db)
        create_checkpoint(
            api_db,
            run_id=run["id"],
            label="after:step1",
            step_id="step1",
            step_results={},
            budget_usage=None,
            run_status="running",
        )
        create_checkpoint(
            api_db,
            run_id=run["id"],
            label="completed",
            step_id=None,
            step_results={},
            budget_usage=None,
            run_status="completed",
        )
        resp = client.get(f"/api/workflow-runs/{run['id']}")
        assert resp.status_code == 200
        data = resp.json()
        assert data["checkpoint_count"] == 2

    def test_api_checkpoints_empty(self, client: Any, api_db: Any) -> None:
        run = _make_run(api_db)
        resp = client.get(f"/api/workflow-runs/{run['id']}/checkpoints")
        assert resp.status_code == 200
        data = resp.json()
        assert data["checkpoints"] == []
