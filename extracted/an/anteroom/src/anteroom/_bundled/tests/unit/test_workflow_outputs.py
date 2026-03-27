"""Tests for structured workflow step outputs (#1131)."""

from __future__ import annotations

import tempfile
from pathlib import Path
from typing import Any

import pytest

from anteroom.config import WorkflowConfig
from anteroom.db import init_db
from anteroom.services.workflow_engine import (
    WorkflowEngine,
    _resolve_step_outputs,
    load_definition,
    resolve_context_from,
)
from anteroom.services.workflow_runners import RunnerResult, create_default_registry
from anteroom.services.workflow_storage import (
    create_workflow_run,
    create_workflow_step,
    get_workflow_step,
    list_workflow_steps,
    update_workflow_step,
)


@pytest.fixture()
def db():
    with tempfile.TemporaryDirectory() as td:
        conn = init_db(Path(td) / "test.db")
        yield conn
        conn.close()


def _make_run(db: Any, **overrides: Any) -> dict[str, Any]:
    defaults = {
        "workflow_id": "test_outputs",
        "workflow_version": "0.1.0",
        "target_kind": "task",
        "target_ref": "1",
    }
    defaults.update(overrides)
    return create_workflow_run(db, **defaults)


# ---------------------------------------------------------------------------
# _resolve_step_outputs (unit)
# ---------------------------------------------------------------------------


class TestResolveStepOutputs:
    def test_resolve_from_artifacts(self) -> None:
        decls = [{"name": "exit_code", "from": "result_artifacts.exit_code"}]
        step_data = {"result_artifacts": {"exit_code": 0}}
        result = _resolve_step_outputs(decls, step_data, {})
        assert result == {"exit_code": 0}

    def test_resolve_from_status(self) -> None:
        decls = [{"name": "status", "from": "result_status"}]
        step_data = {"result_status": "success"}
        result = _resolve_step_outputs(decls, step_data, {})
        assert result == {"status": "success"}

    def test_runner_outputs_take_precedence(self) -> None:
        decls = [{"name": "count", "from": "result_artifacts.count"}]
        step_data = {"result_artifacts": {"count": 10}}
        runner_outputs = {"count": 42}
        result = _resolve_step_outputs(decls, step_data, runner_outputs)
        assert result == {"count": 42}

    def test_missing_path_resolves_to_none(self) -> None:
        decls = [{"name": "missing", "from": "result_artifacts.nonexistent"}]
        step_data = {"result_artifacts": {}}
        result = _resolve_step_outputs(decls, step_data, {})
        assert result == {"missing": None}

    def test_multiple_outputs(self) -> None:
        decls = [
            {"name": "code", "from": "result_artifacts.exit_code"},
            {"name": "model", "from": "result_artifacts.model"},
        ]
        step_data = {"result_artifacts": {"exit_code": 0, "model": "gpt-4"}}
        result = _resolve_step_outputs(decls, step_data, {})
        assert result == {"code": 0, "model": "gpt-4"}

    def test_deeply_nested_path(self) -> None:
        decls = [{"name": "val", "from": "result_artifacts.structured_output.data.key"}]
        step_data = {"result_artifacts": {"structured_output": {"data": {"key": "found"}}}}
        result = _resolve_step_outputs(decls, step_data, {})
        assert result == {"val": "found"}


# ---------------------------------------------------------------------------
# RunnerResult.outputs field
# ---------------------------------------------------------------------------


class TestRunnerResultOutputs:
    def test_default_empty(self) -> None:
        r = RunnerResult(status="success")
        assert r.outputs == {}

    def test_outputs_in_to_dict(self) -> None:
        r = RunnerResult(status="success", outputs={"key": "val"})
        d = r.to_dict()
        assert d["outputs"] == {"key": "val"}


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------


class TestOutputsValidation:
    def test_valid_outputs_declaration(self) -> None:
        yaml_str = """\
kind: workflow
id: test_outputs
version: 0.1.0
inputs: {}
steps:
  - id: run_tests
    type: runner
    runner: shell
    command: echo ok
    outputs:
      - name: exit_code
        from: result_artifacts.exit_code
"""
        defn = load_definition(yaml_str)
        assert defn.steps[0].outputs is not None
        assert len(defn.steps[0].outputs) == 1

    def test_output_missing_name_raises(self) -> None:
        yaml_str = """\
kind: workflow
id: test_outputs
version: 0.1.0
inputs: {}
steps:
  - id: s1
    type: runner
    runner: shell
    command: echo ok
    outputs:
      - from: result_artifacts.exit_code
"""
        with pytest.raises(ValueError, match="missing 'name'"):
            load_definition(yaml_str)

    def test_output_missing_from_raises(self) -> None:
        yaml_str = """\
kind: workflow
id: test_outputs
version: 0.1.0
inputs: {}
steps:
  - id: s1
    type: runner
    runner: shell
    command: echo ok
    outputs:
      - name: exit_code
"""
        with pytest.raises(ValueError, match="missing 'from'"):
            load_definition(yaml_str)

    def test_duplicate_output_name_raises(self) -> None:
        yaml_str = """\
kind: workflow
id: test_outputs
version: 0.1.0
inputs: {}
steps:
  - id: s1
    type: runner
    runner: shell
    command: echo ok
    outputs:
      - name: dup
        from: result_status
      - name: dup
        from: result_summary
"""
        with pytest.raises(ValueError, match="duplicate output name"):
            load_definition(yaml_str)


# ---------------------------------------------------------------------------
# When clause with result_outputs
# ---------------------------------------------------------------------------


class TestWhenWithOutputs:
    def test_when_equals_on_result_outputs(self) -> None:
        when = {"step": "s1", "field": "result_outputs.exit_code", "equals": "0"}
        results = {"s1": {"result_outputs": {"exit_code": "0"}}}
        assert WorkflowEngine._evaluate_when(when, results) is True

    def test_when_not_equals_on_result_outputs(self) -> None:
        when = {"step": "s1", "field": "result_outputs.exit_code", "not_equals": "0"}
        results = {"s1": {"result_outputs": {"exit_code": "1"}}}
        assert WorkflowEngine._evaluate_when(when, results) is True

    def test_when_is_not_empty_on_result_outputs(self) -> None:
        when = {"step": "s1", "field": "result_outputs.report_path", "is_not_empty": True}
        results = {"s1": {"result_outputs": {"report_path": "/tmp/report.xml"}}}
        assert WorkflowEngine._evaluate_when(when, results) is True

    def test_when_field_validation_allows_result_outputs(self) -> None:
        yaml_str = """\
kind: workflow
id: test_outputs
version: 0.1.0
inputs: {}
steps:
  - id: s1
    type: runner
    runner: shell
    command: echo ok
  - id: s2
    type: runner
    runner: shell
    command: echo ok
    when:
      step: s1
      field: result_outputs.exit_code
      equals: "0"
"""
        defn = load_definition(yaml_str)
        assert defn.steps[1].when is not None


# ---------------------------------------------------------------------------
# Context from result_outputs
# ---------------------------------------------------------------------------


class TestContextFromOutputs:
    def test_resolve_context_from_result_outputs(self) -> None:
        refs = [{"step": "s1", "field": "result_outputs.report_path"}]
        results = {"s1": {"result_outputs": {"report_path": "/tmp/report.xml"}}}
        ctx = resolve_context_from(refs, results)
        assert "/tmp/report.xml" in ctx

    def test_resolve_context_from_missing_output(self) -> None:
        refs = [{"step": "s1", "field": "result_outputs.missing"}]
        results = {"s1": {"result_outputs": {}}}
        ctx = resolve_context_from(refs, results)
        assert ctx == ""


# ---------------------------------------------------------------------------
# Storage round-trip
# ---------------------------------------------------------------------------


class TestOutputsStorage:
    def test_update_and_get_step_outputs(self, db: Any) -> None:
        run = _make_run(db)
        step = create_workflow_step(db, run_id=run["id"], step_id="s1", step_type="runner", runner_type="shell")
        outputs = {"exit_code": 0, "report_path": "/tmp/report.xml"}
        update_workflow_step(db, step["id"], result_outputs=outputs)
        fetched = get_workflow_step(db, step["id"])
        assert fetched is not None
        assert fetched["result_outputs"] == outputs

    def test_outputs_none_by_default(self, db: Any) -> None:
        run = _make_run(db)
        step = create_workflow_step(db, run_id=run["id"], step_id="s1", step_type="runner")
        fetched = get_workflow_step(db, step["id"])
        assert fetched is not None
        assert fetched["result_outputs"] is None

    def test_outputs_survive_list_steps(self, db: Any) -> None:
        run = _make_run(db)
        create_workflow_step(db, run_id=run["id"], step_id="s1", step_type="runner", runner_type="shell")
        steps = list_workflow_steps(db, run["id"])
        step = steps[0]
        update_workflow_step(db, step["id"], result_outputs={"key": "val"})
        steps = list_workflow_steps(db, run["id"])
        assert steps[0]["result_outputs"] == {"key": "val"}


# ---------------------------------------------------------------------------
# Sanitize checkpoint data includes result_outputs
# ---------------------------------------------------------------------------


class TestSanitizeWithOutputs:
    def test_sanitize_preserves_result_outputs(self) -> None:
        data = {
            "s1": {
                "result_status": "success",
                "result_summary": "ok",
                "result_artifacts": {},
                "result_findings": None,
                "result_outputs": {"exit_code": 0, "report": "/tmp/r.xml"},
            }
        }
        result = WorkflowEngine._sanitize_checkpoint_data(data)
        assert result["s1"]["result_outputs"] == {"exit_code": 0, "report": "/tmp/r.xml"}

    def test_sanitize_handles_none_outputs(self) -> None:
        data = {
            "s1": {
                "result_status": "success",
                "result_summary": "ok",
                "result_artifacts": {},
                "result_findings": None,
                "result_outputs": None,
            }
        }
        result = WorkflowEngine._sanitize_checkpoint_data(data)
        assert result["s1"]["result_outputs"] is None

    def test_sanitize_handles_missing_outputs(self) -> None:
        data = {
            "s1": {
                "result_status": "success",
                "result_summary": "ok",
                "result_artifacts": {},
                "result_findings": None,
            }
        }
        result = WorkflowEngine._sanitize_checkpoint_data(data)
        assert result["s1"]["result_outputs"] is None


# ---------------------------------------------------------------------------
# Rebuild step results includes result_outputs
# ---------------------------------------------------------------------------


class TestRebuildWithOutputs:
    def test_rebuild_includes_outputs(self, db: Any) -> None:
        config = WorkflowConfig()
        registry = create_default_registry()
        engine = WorkflowEngine(db, config, registry)

        run = _make_run(db)
        step = create_workflow_step(db, run_id=run["id"], step_id="s1", step_type="runner", runner_type="shell")
        update_workflow_step(
            db,
            step["id"],
            status="completed",
            result_status="success",
            result_outputs={"exit_code": 0},
        )
        results = engine._rebuild_step_results(run["id"])
        assert results["s1"]["result_outputs"] == {"exit_code": 0}

    def test_rebuild_none_when_no_outputs(self, db: Any) -> None:
        config = WorkflowConfig()
        registry = create_default_registry()
        engine = WorkflowEngine(db, config, registry)

        run = _make_run(db)
        step = create_workflow_step(db, run_id=run["id"], step_id="s1", step_type="runner", runner_type="shell")
        update_workflow_step(
            db,
            step["id"],
            status="completed",
            result_status="success",
        )
        results = engine._rebuild_step_results(run["id"])
        assert results["s1"]["result_outputs"] is None
