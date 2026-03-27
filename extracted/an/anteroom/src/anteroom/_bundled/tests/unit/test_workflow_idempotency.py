"""Tests for workflow idempotency keys (#977).

Tests cover key computation, persistence, adapter header injection,
and engine integration.
"""

from __future__ import annotations

import tempfile
from pathlib import Path
from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from anteroom.config import WorkflowConfig
from anteroom.db import init_db
from anteroom.services.workflow_engine import (
    WorkflowEngine,
    WorkflowStepDef,
    load_definition,
    register_gate_condition,
)
from anteroom.services.workflow_publishers import (
    FilePublishAdapter,
    WebhookPublishAdapter,
)
from anteroom.services.workflow_runners import create_default_registry
from anteroom.services.workflow_storage import (
    create_workflow_step,
    get_workflow_step,
    list_workflow_steps,
    update_workflow_step,
)

# ---------------------------------------------------------------------------
# Test YAML definitions
# ---------------------------------------------------------------------------

PUBLISH_WITH_DEFAULT_KEY = """\
kind: workflow
id: test_idem_default
version: 0.1.0
inputs: {}
steps:
  - id: generate
    type: runner
    runner: shell
    command: "echo hello"
  - id: publish_out
    type: publish
    context_from:
      - step: generate
        field: raw_output
    destination:
      adapter: file
      path: "{output_dir}/result.txt"
"""

PUBLISH_WITH_CUSTOM_KEY = """\
kind: workflow
id: test_idem_custom
version: 0.1.0
inputs:
  target_name:
    type: string
    required: true
steps:
  - id: generate
    type: runner
    runner: shell
    command: "echo hello"
  - id: publish_out
    type: publish
    idempotency_key: "{run_id}:{step_id}:{target_name}"
    context_from:
      - step: generate
        field: raw_output
    destination:
      adapter: file
      path: "{output_dir}/result.txt"
"""

RUNNER_ONLY_WORKFLOW = """\
kind: workflow
id: test_no_publish
version: 0.1.0
inputs: {}
steps:
  - id: step1
    type: runner
    runner: shell
    command: "echo hi"
"""

PUBLISH_WEBHOOK_IDEM = """\
kind: workflow
id: test_idem_webhook
version: 0.1.0
inputs: {}
steps:
  - id: generate
    type: runner
    runner: shell
    command: "echo data"
  - id: publish_hook
    type: publish
    context_from:
      - step: generate
        field: raw_output
    destination:
      adapter: webhook
      url: "https://example.com/hook"
"""


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

    register_gate_condition("always_pass", always_pass)
    yield


# ---------------------------------------------------------------------------
# Unit tests: key resolution
# ---------------------------------------------------------------------------


class TestIdempotencyKeyResolution:
    def test_default_key_uses_run_and_step_id(self, engine: WorkflowEngine) -> None:
        step_def = WorkflowStepDef(id="pub_step", type="publish")
        run = {"id": "run-abc-123"}
        key = engine._resolve_idempotency_key(step_def, run, {})
        assert key == "run-abc-123:pub_step"

    def test_custom_key_resolved(self, engine: WorkflowEngine) -> None:
        step_def = WorkflowStepDef(
            id="pub_step",
            type="publish",
            idempotency_key="{run_id}:{step_id}:{target_name}",
        )
        run = {"id": "run-xyz"}
        inputs = {"target_name": "my-target"}
        key = engine._resolve_idempotency_key(step_def, run, inputs)
        assert key == "run-xyz:pub_step:my-target"

    def test_engine_owned_keys_override_inputs(self, engine: WorkflowEngine) -> None:
        """If inputs contain run_id or step_id, engine values take precedence."""
        step_def = WorkflowStepDef(id="pub", type="publish")
        run = {"id": "engine-run-id"}
        inputs = {"run_id": "user-supplied-run-id", "step_id": "user-supplied-step-id"}
        key = engine._resolve_idempotency_key(step_def, run, inputs)
        assert key == "engine-run-id:pub"

    def test_key_stable_across_retries(self, engine: WorkflowEngine) -> None:
        """Same key should be produced regardless of which retry attempt."""
        step_def = WorkflowStepDef(id="pub", type="publish")
        run = {"id": "run-retry"}
        key1 = engine._resolve_idempotency_key(step_def, run, {})
        key2 = engine._resolve_idempotency_key(step_def, run, {})
        assert key1 == key2 == "run-retry:pub"


# ---------------------------------------------------------------------------
# Unit tests: parse
# ---------------------------------------------------------------------------


class TestIdempotencyKeyParsing:
    def test_idempotency_key_parsed_from_yaml(self) -> None:
        defn = load_definition(PUBLISH_WITH_CUSTOM_KEY)
        pub_step = defn.steps[1]
        assert pub_step.idempotency_key == "{run_id}:{step_id}:{target_name}"

    def test_idempotency_key_defaults_to_none(self) -> None:
        defn = load_definition(PUBLISH_WITH_DEFAULT_KEY)
        pub_step = defn.steps[1]
        assert pub_step.idempotency_key is None


# ---------------------------------------------------------------------------
# Unit tests: storage
# ---------------------------------------------------------------------------


class TestIdempotencyKeyStorage:
    def test_key_persisted_on_step_record(self, db: Any) -> None:
        from anteroom.services.workflow_storage import create_workflow_run

        run = create_workflow_run(
            db,
            workflow_id="test",
            workflow_version="0.1.0",
            target_kind="workflow",
            target_ref="test",
        )
        step = create_workflow_step(
            db,
            run_id=run["id"],
            step_id="pub",
            step_type="publish",
            idempotency_key="run-1:pub",
        )
        assert step["idempotency_key"] == "run-1:pub"

        fetched = get_workflow_step(db, step["id"])
        assert fetched is not None
        assert fetched["idempotency_key"] == "run-1:pub"

    def test_key_updated_on_step_record(self, db: Any) -> None:
        from anteroom.services.workflow_storage import create_workflow_run

        run = create_workflow_run(
            db,
            workflow_id="test",
            workflow_version="0.1.0",
            target_kind="workflow",
            target_ref="test",
        )
        step = create_workflow_step(
            db,
            run_id=run["id"],
            step_id="pub",
            step_type="publish",
        )
        assert step["idempotency_key"] is None

        updated = update_workflow_step(db, step["id"], idempotency_key="run-1:pub")
        assert updated is not None
        assert updated["idempotency_key"] == "run-1:pub"

    def test_db_migration_adds_column(self) -> None:
        """Column exists after init_db on a fresh database."""
        with tempfile.TemporaryDirectory() as td:
            conn = init_db(Path(td) / "migration_test.db")
            try:
                cols = {r[1] for r in conn.execute("PRAGMA table_info(workflow_steps)").fetchall()}
                assert "idempotency_key" in cols
            finally:
                conn.close()


# ---------------------------------------------------------------------------
# Unit tests: adapters
# ---------------------------------------------------------------------------


class TestAdapterIdempotencyKey:
    @pytest.mark.asyncio
    async def test_webhook_sends_header(self) -> None:
        adapter = WebhookPublishAdapter()
        mock_response = MagicMock()
        mock_response.status_code = 200

        mock_client = AsyncMock()
        mock_client.request = AsyncMock(return_value=mock_response)
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=False)

        with patch("httpx.AsyncClient", return_value=mock_client):
            result = await adapter.publish(
                content="test",
                destination={"adapter": "webhook", "url": "https://example.com/hook"},
                idempotency_key="run-1:pub",
            )

        assert result.status == "success"
        call_args = mock_client.request.call_args
        headers = call_args.kwargs.get("headers") or call_args[1].get("headers", {})
        assert headers.get("Idempotency-Key") == "run-1:pub"

    @pytest.mark.asyncio
    async def test_webhook_no_header_when_no_key(self) -> None:
        adapter = WebhookPublishAdapter()
        mock_response = MagicMock()
        mock_response.status_code = 200

        mock_client = AsyncMock()
        mock_client.request = AsyncMock(return_value=mock_response)
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=False)

        with patch("httpx.AsyncClient", return_value=mock_client):
            await adapter.publish(
                content="test",
                destination={"adapter": "webhook", "url": "https://example.com/hook"},
            )

        call_args = mock_client.request.call_args
        headers = call_args.kwargs.get("headers") or call_args[1].get("headers", {})
        assert "Idempotency-Key" not in headers

    @pytest.mark.asyncio
    async def test_file_adapter_accepts_key(self, tmp_path: Path) -> None:
        adapter = FilePublishAdapter()
        out = tmp_path / "output.txt"
        result = await adapter.publish(
            content="hello",
            destination={"adapter": "file", "path": str(out)},
            idempotency_key="run-1:pub",
        )
        assert result.status == "success"
        assert out.read_text() == "hello"


# ---------------------------------------------------------------------------
# Unit tests: non-publish steps
# ---------------------------------------------------------------------------


class TestNonPublishSteps:
    def test_key_not_computed_for_runner_steps(self) -> None:
        """Verify that runner steps don't get idempotency keys in their step_def."""
        defn = load_definition(RUNNER_ONLY_WORKFLOW)
        assert defn.steps[0].idempotency_key is None


# ---------------------------------------------------------------------------
# Integration: engine end-to-end
# ---------------------------------------------------------------------------


class TestEngineIntegration:
    @pytest.mark.asyncio
    async def test_publish_step_stores_key_in_db_and_artifacts(self, db: Any, tmp_path: Path) -> None:
        """Full run with publish step: key appears in DB step record and result artifacts."""
        yaml_str = f"""\
kind: workflow
id: test_e2e_idem
version: 0.1.0
inputs: {{}}
steps:
  - id: generate
    type: runner
    runner: shell
    command: "echo hello"
  - id: publish_out
    type: publish
    context_from:
      - step: generate
        field: raw_output
    destination:
      adapter: file
      path: "{tmp_path}/result.txt"
"""
        config = WorkflowConfig()
        registry = create_default_registry()
        eng = WorkflowEngine(db, config, registry)

        defn = load_definition(yaml_str)
        run = await eng.start_run(
            defn,
            target_kind="workflow",
            target_ref="test_e2e_idem",
        )
        assert run["status"] == "completed"

        steps = list_workflow_steps(db, run["id"])
        publish_steps = [s for s in steps if s["step_type"] == "publish"]
        assert len(publish_steps) == 1

        pub = publish_steps[0]
        assert pub["idempotency_key"] is not None
        assert run["id"] in pub["idempotency_key"]
        assert "publish_out" in pub["idempotency_key"]

        artifacts = pub.get("result_artifacts") or {}
        assert artifacts.get("idempotency_key") == pub["idempotency_key"]
