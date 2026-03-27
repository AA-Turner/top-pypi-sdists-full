"""Advanced workflow engine tests — triggers, when, context_from, drift, idempotency (#1021)."""

from __future__ import annotations

import tempfile
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from anteroom.config import WorkflowConfig
from anteroom.db import init_db
from anteroom.services.workflow_engine import (
    WorkflowEngine,
    WorkflowStepDef,
    load_definition,
    resolve_context_from,
)
from anteroom.services.workflow_runners import create_default_registry


@pytest.fixture()
def db() -> Any:
    with tempfile.TemporaryDirectory() as td:
        conn = init_db(Path(td) / "test.db")
        yield conn
        conn.close()


@pytest.fixture()
def engine(db: Any) -> WorkflowEngine:
    config = WorkflowConfig()
    registry = create_default_registry()
    return WorkflowEngine(db, config, registry)


# ---------------------------------------------------------------------------
# Trigger parsing
# ---------------------------------------------------------------------------


class TestParseTrigger:
    def test_schedule_missing_cron_raises(self) -> None:
        yaml_src = """\
kind: workflow
id: t
version: 1.0
triggers:
  - type: schedule
steps:
  - id: s1
    type: runner
    runner: shell
    command: echo hi
"""
        with pytest.raises(ValueError, match="cron"):
            load_definition(yaml_src)

    def test_invalid_missed_policy_raises(self) -> None:
        yaml_src = """\
kind: workflow
id: t
version: 1.0
triggers:
  - type: schedule
    cron: "0 * * * *"
    missed_policy: run_all
steps:
  - id: s1
    type: runner
    runner: shell
    command: echo hi
"""
        with pytest.raises(ValueError, match="missed_policy"):
            load_definition(yaml_src)

    def test_valid_schedule_trigger(self) -> None:
        yaml_src = """\
kind: workflow
id: t
version: 1.0
triggers:
  - type: schedule
    cron: "0 * * * *"
    missed_policy: queue
steps:
  - id: s1
    type: runner
    runner: shell
    command: echo hi
"""
        defn = load_definition(yaml_src)
        assert len(defn.triggers) == 1
        assert defn.triggers[0].type == "schedule"
        assert defn.triggers[0].cron == "0 * * * *"
        assert defn.triggers[0].missed_policy == "queue"

    def test_non_schedule_no_cron_validation(self) -> None:
        yaml_src = """\
kind: workflow
id: t
version: 1.0
triggers:
  - type: webhook
steps:
  - id: s1
    type: runner
    runner: shell
    command: echo hi
"""
        defn = load_definition(yaml_src)
        assert len(defn.triggers) == 1
        assert defn.triggers[0].type == "webhook"
        assert defn.triggers[0].cron is None


# ---------------------------------------------------------------------------
# When clause validation
# ---------------------------------------------------------------------------


class TestWhenClauseValidation:
    def test_missing_step_raises(self) -> None:
        yaml_src = """\
kind: workflow
id: t
version: 1.0
steps:
  - id: gen
    type: runner
    runner: shell
    command: echo hi
  - id: check
    type: runner
    runner: shell
    command: echo check
    when:
      field: result_status
      equals: "success"
"""
        with pytest.raises(ValueError, match="'when' requires a 'step' field"):
            load_definition(yaml_src)

    def test_missing_field_raises(self) -> None:
        yaml_src = """\
kind: workflow
id: t
version: 1.0
steps:
  - id: gen
    type: runner
    runner: shell
    command: echo hi
  - id: check
    type: runner
    runner: shell
    command: echo check
    when:
      step: gen
      equals: "success"
"""
        with pytest.raises(ValueError, match="'when' requires a 'field' field"):
            load_definition(yaml_src)

    def test_invalid_field_prefix_raises(self) -> None:
        yaml_src = """\
kind: workflow
id: t
version: 1.0
steps:
  - id: gen
    type: runner
    runner: shell
    command: echo hi
  - id: check
    type: runner
    runner: shell
    command: echo check
    when:
      step: gen
      field: bad_field
      equals: "x"
"""
        with pytest.raises(ValueError, match="must start with one of"):
            load_definition(yaml_src)

    def test_no_operator_raises(self) -> None:
        yaml_src = """\
kind: workflow
id: t
version: 1.0
steps:
  - id: gen
    type: runner
    runner: shell
    command: echo hi
  - id: check
    type: runner
    runner: shell
    command: echo check
    when:
      step: gen
      field: result_status
"""
        with pytest.raises(ValueError, match="exactly one operator"):
            load_definition(yaml_src)

    def test_multiple_operators_raises(self) -> None:
        yaml_src = """\
kind: workflow
id: t
version: 1.0
steps:
  - id: gen
    type: runner
    runner: shell
    command: echo hi
  - id: check
    type: runner
    runner: shell
    command: echo check
    when:
      step: gen
      field: result_status
      equals: "success"
      not_equals: "failed"
"""
        with pytest.raises(ValueError, match="exactly one operator"):
            load_definition(yaml_src)


# ---------------------------------------------------------------------------
# When clause evaluation
# ---------------------------------------------------------------------------


class TestWhenClauseEvaluation:
    def test_equals_true(self) -> None:
        step_results = {"gen": {"result_status": "success"}}
        when = {"step": "gen", "field": "result_status", "equals": "success"}
        assert WorkflowEngine._evaluate_when(when, step_results) is True

    def test_equals_false(self) -> None:
        step_results = {"gen": {"result_status": "failed"}}
        when = {"step": "gen", "field": "result_status", "equals": "success"}
        assert WorkflowEngine._evaluate_when(when, step_results) is False

    def test_is_not_empty_true(self) -> None:
        step_results = {"gen": {"result_summary": "some data"}}
        when = {"step": "gen", "field": "result_summary", "is_not_empty": True}
        assert WorkflowEngine._evaluate_when(when, step_results) is True

    def test_is_empty_true(self) -> None:
        step_results = {"gen": {"result_summary": ""}}
        when = {"step": "gen", "field": "result_summary", "is_empty": True}
        assert WorkflowEngine._evaluate_when(when, step_results) is True

    def test_contains_true(self) -> None:
        step_results = {"gen": {"result_summary": "found 3 issues"}}
        when = {"step": "gen", "field": "result_summary", "contains": "issues"}
        assert WorkflowEngine._evaluate_when(when, step_results) is True

    def test_contains_none_value(self) -> None:
        step_results = {"gen": {"result_summary": None}}
        when = {"step": "gen", "field": "result_summary", "contains": "x"}
        assert WorkflowEngine._evaluate_when(when, step_results) is False

    def test_step_not_found(self) -> None:
        when = {"step": "missing", "field": "result_status", "equals": "success"}
        assert WorkflowEngine._evaluate_when(when, {}) is False


# ---------------------------------------------------------------------------
# context_from validation
# ---------------------------------------------------------------------------


class TestContextFromValidation:
    def test_valid_step_ref(self) -> None:
        yaml_src = """\
kind: workflow
id: t
version: 1.0
steps:
  - id: gen
    type: runner
    runner: shell
    command: echo hi
  - id: pub
    type: runner
    runner: shell
    command: echo done
    context_from:
      - step: gen
        field: raw_output
"""
        defn = load_definition(yaml_src)
        assert defn.steps[1].context_from is not None

    def test_missing_field_raises(self) -> None:
        yaml_src = """\
kind: workflow
id: t
version: 1.0
steps:
  - id: gen
    type: runner
    runner: shell
    command: echo hi
  - id: pub
    type: runner
    runner: shell
    command: echo done
    context_from:
      - step: gen
"""
        with pytest.raises(ValueError, match="missing 'field' field"):
            load_definition(yaml_src)

    def test_step_not_seen_raises(self) -> None:
        yaml_src = """\
kind: workflow
id: t
version: 1.0
steps:
  - id: pub
    type: runner
    runner: shell
    command: echo done
    context_from:
      - step: future_step
        field: raw_output
"""
        with pytest.raises(ValueError, match="not appeared before"):
            load_definition(yaml_src)


# ---------------------------------------------------------------------------
# context_from resolver
# ---------------------------------------------------------------------------


class TestResolveContextFrom:
    def test_step_ref(self) -> None:
        step_results = {"gen": {"raw_output": "hello"}}
        refs = [{"step": "gen", "field": "raw_output"}]
        result = resolve_context_from(refs, step_results)
        assert "hello" in result

    def test_source_id_ref(self) -> None:
        refs = [{"source_id": "abc-123"}]
        with patch("anteroom.services.workflow_engine._resolve_source_ref", return_value="source content"):
            result = resolve_context_from(refs, {}, db=MagicMock())
        assert "source content" in result

    def test_source_group_id_ref(self) -> None:
        refs = [{"source_group_id": "grp-1"}]
        with patch("anteroom.services.workflow_engine._resolve_source_group_ref", return_value="group content"):
            result = resolve_context_from(refs, {}, db=MagicMock())
        assert "group content" in result

    def test_unrecognized_ref(self) -> None:
        refs = [{"unknown_key": "val"}]
        result = resolve_context_from(refs, {})
        assert result == ""


# ---------------------------------------------------------------------------
# Drift detection
# ---------------------------------------------------------------------------


class TestDriftDetection:
    @pytest.mark.asyncio
    async def test_hash_matches_no_drift(self, db: Any) -> None:
        yaml_src = """\
kind: workflow
id: t
version: 1.0
steps:
  - id: s1
    type: runner
    runner: shell
    command: echo hi
"""
        config = WorkflowConfig()
        registry = create_default_registry()
        engine = WorkflowEngine(db, config, registry)
        defn = load_definition(yaml_src)
        run = await engine.start_run(defn, target_kind="test", target_ref="drift-test")
        assert run["status"] == "completed"

    @pytest.mark.asyncio
    async def test_hash_mismatch_without_force_raises(self, db: Any) -> None:
        from anteroom.services import workflow_storage as ws

        yaml_v1 = """\
kind: workflow
id: t
version: 1.0
steps:
  - id: s1
    type: runner
    runner: shell
    command: echo v1
"""
        yaml_v2 = """\
kind: workflow
id: t
version: 1.0
steps:
  - id: s1
    type: runner
    runner: shell
    command: echo v2
"""
        config = WorkflowConfig()
        registry = create_default_registry()
        engine = WorkflowEngine(db, config, registry)

        defn_v1 = load_definition(yaml_v1)
        run = await engine.start_run(defn_v1, target_kind="test", target_ref="drift-test")
        run_id = run["id"]

        ws.update_workflow_run(db, run_id, status="paused")

        defn_v2 = load_definition(yaml_v2)
        with pytest.raises(ValueError, match="hash mismatch"):
            await engine.resume_run(run_id, defn_v2, force=False)

    @pytest.mark.asyncio
    async def test_hash_mismatch_with_force_proceeds(self, db: Any) -> None:
        from anteroom.services import workflow_storage as ws

        yaml_v1 = """\
kind: workflow
id: t
version: 1.0
steps:
  - id: s1
    type: runner
    runner: shell
    command: echo v1
"""
        yaml_v2 = """\
kind: workflow
id: t
version: 1.0
steps:
  - id: s1
    type: runner
    runner: shell
    command: echo v2
"""
        config = WorkflowConfig()
        registry = create_default_registry()
        engine = WorkflowEngine(db, config, registry)

        defn_v1 = load_definition(yaml_v1)
        run = await engine.start_run(defn_v1, target_kind="test", target_ref="drift-force")
        run_id = run["id"]

        ws.update_workflow_run(db, run_id, status="paused")

        defn_v2 = load_definition(yaml_v2)
        result = await engine.resume_run(run_id, defn_v2, force=True)
        assert result["status"] == "completed"

    @pytest.mark.asyncio
    async def test_no_stored_hash_warns_and_proceeds(self, db: Any) -> None:
        from anteroom.services import workflow_storage as ws

        yaml_src = """\
kind: workflow
id: t
version: 1.0
steps:
  - id: s1
    type: runner
    runner: shell
    command: echo hi
"""
        config = WorkflowConfig()
        registry = create_default_registry()
        engine = WorkflowEngine(db, config, registry)

        defn = load_definition(yaml_src)
        run = await engine.start_run(defn, target_kind="test", target_ref="no-hash")
        run_id = run["id"]

        ws.update_workflow_run(db, run_id, status="paused")
        db.execute("UPDATE workflow_runs SET definition_hash=NULL WHERE id=?", (run_id,))
        db.commit()

        result = await engine.resume_run(run_id, defn)
        assert result["status"] == "completed"


# ---------------------------------------------------------------------------
# Idempotency key
# ---------------------------------------------------------------------------


class TestIdempotencyKey:
    def test_default_template(self) -> None:
        engine = MagicMock(spec=WorkflowEngine)
        step_def = WorkflowStepDef(id="pub", type="publish")
        run = {"id": "run-abc"}
        inputs: dict[str, Any] = {}
        key = WorkflowEngine._resolve_idempotency_key(engine, step_def, run, inputs)
        assert key == "run-abc:pub"

    def test_custom_template_with_inputs(self) -> None:
        engine = MagicMock(spec=WorkflowEngine)
        step_def = WorkflowStepDef(id="pub", type="publish", idempotency_key="{project}-{run_id}")
        run = {"id": "run-xyz"}
        inputs = {"project": "acme"}
        key = WorkflowEngine._resolve_idempotency_key(engine, step_def, run, inputs)
        assert key == "acme-run-xyz"

    def test_engine_keys_override_user_inputs(self) -> None:
        engine = MagicMock(spec=WorkflowEngine)
        step_def = WorkflowStepDef(id="pub", type="publish")
        run = {"id": "real-run"}
        inputs = {"run_id": "user-run", "step_id": "user-step"}
        key = WorkflowEngine._resolve_idempotency_key(engine, step_def, run, inputs)
        assert key == "real-run:pub"
