"""Tests for workflow step templating — overridable params (#958)."""

from __future__ import annotations

import tempfile
from pathlib import Path
from typing import Any
from unittest.mock import AsyncMock, patch

import pytest

from anteroom.db import init_db
from anteroom.services.workflow_engine import (
    WorkflowEngine,
    _resolve_params,
    load_definition,
    resolve_template,
)
from anteroom.services.workflow_runners import create_default_registry
from anteroom.services.workflow_storage import (
    create_workflow_run,
    get_workflow_run,
)

# ---------------------------------------------------------------------------
# YAML fixtures
# ---------------------------------------------------------------------------

YAML_WITH_PARAMS = """\
kind: workflow
id: test_params
version: "1.0"
params:
  lint_command:
    default: "ruff check src/"
    description: "Lint command"
  test_command:
    default: "pytest tests/"
    description: "Test command"
inputs:
  issue_number:
    required: true
    type: string
steps:
  - id: checks
    type: runner
    runner: shell
    command: "{lint_command} && {test_command}"
  - id: report
    type: runner
    runner: shell
    command: "echo issue {issue_number}"
"""

YAML_WITH_REQUIRED_PARAM = """\
kind: workflow
id: test_required_param
version: "1.0"
params:
  deploy_target:
    description: "Deploy target — no default, must be provided"
steps:
  - id: deploy
    type: runner
    runner: shell
    command: "deploy.sh {deploy_target}"
"""

YAML_PARAM_INPUT_OVERLAP = """\
kind: workflow
id: test_overlap
version: "1.0"
params:
  issue_number:
    default: "99"
inputs:
  issue_number:
    required: true
steps:
  - id: check
    type: runner
    runner: shell
    command: "echo {issue_number}"
"""

YAML_NO_PARAMS = """\
kind: workflow
id: test_no_params
version: "1.0"
steps:
  - id: hello
    type: runner
    runner: shell
    command: "echo hello"
"""

YAML_EMPTY_PARAMS = """\
kind: workflow
id: test_empty_params
version: "1.0"
params: {}
steps:
  - id: hello
    type: runner
    runner: shell
    command: "echo hello"
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
    from anteroom.config import WorkflowConfig

    config = WorkflowConfig()
    registry = create_default_registry()
    return WorkflowEngine(db, config, registry)


# ---------------------------------------------------------------------------
# Parsing tests
# ---------------------------------------------------------------------------


class TestParamParsing:
    def test_load_definition_with_params(self) -> None:
        defn = load_definition(YAML_WITH_PARAMS)
        assert "lint_command" in defn.params
        assert defn.params["lint_command"]["default"] == "ruff check src/"
        assert defn.params["lint_command"]["description"] == "Lint command"
        assert "test_command" in defn.params

    def test_load_definition_no_params(self) -> None:
        defn = load_definition(YAML_NO_PARAMS)
        assert defn.params == {}

    def test_load_definition_empty_params(self) -> None:
        defn = load_definition(YAML_EMPTY_PARAMS)
        assert defn.params == {}

    def test_load_definition_required_param(self) -> None:
        defn = load_definition(YAML_WITH_REQUIRED_PARAM)
        assert "deploy_target" in defn.params
        assert "default" not in defn.params["deploy_target"]


class TestParamInputOverlap:
    def test_overlap_rejected(self) -> None:
        with pytest.raises(ValueError, match="overlap with input keys"):
            load_definition(YAML_PARAM_INPUT_OVERLAP)


# ---------------------------------------------------------------------------
# Resolution tests
# ---------------------------------------------------------------------------


class TestResolveParams:
    def test_defaults_used_when_no_overrides(self) -> None:
        defn = load_definition(YAML_WITH_PARAMS)
        resolved = _resolve_params(defn)
        assert resolved == {
            "lint_command": "ruff check src/",
            "test_command": "pytest tests/",
        }

    def test_overrides_win_over_defaults(self) -> None:
        defn = load_definition(YAML_WITH_PARAMS)
        resolved = _resolve_params(defn, {"lint_command": "eslint src/"})
        assert resolved["lint_command"] == "eslint src/"
        assert resolved["test_command"] == "pytest tests/"

    def test_required_param_missing_raises(self) -> None:
        defn = load_definition(YAML_WITH_REQUIRED_PARAM)
        with pytest.raises(ValueError, match="Required param 'deploy_target'"):
            _resolve_params(defn)

    def test_required_param_supplied(self) -> None:
        defn = load_definition(YAML_WITH_REQUIRED_PARAM)
        resolved = _resolve_params(defn, {"deploy_target": "staging"})
        assert resolved["deploy_target"] == "staging"

    def test_empty_params_returns_empty_dict(self) -> None:
        defn = load_definition(YAML_EMPTY_PARAMS)
        resolved = _resolve_params(defn)
        assert resolved == {}

    def test_override_value_coerced_to_string(self) -> None:
        defn = load_definition(YAML_WITH_PARAMS)
        resolved = _resolve_params(defn, {"lint_command": 42})  # type: ignore[dict-item]
        assert resolved["lint_command"] == "42"


# ---------------------------------------------------------------------------
# Template expansion tests
# ---------------------------------------------------------------------------


class TestTemplateExpansionWithParams:
    def test_params_and_inputs_merged_in_template(self) -> None:
        defn = load_definition(YAML_WITH_PARAMS)
        resolved = _resolve_params(defn)
        template_vars = {**resolved, "issue_number": "123"}
        result = resolve_template("{lint_command} && {test_command} #{issue_number}", template_vars)
        assert result == "ruff check src/ && pytest tests/ #123"

    def test_shell_quoting_applied_to_params(self) -> None:
        defn = load_definition(YAML_WITH_PARAMS)
        resolved = _resolve_params(defn, {"lint_command": "ruff check 'src dir'"})
        template_vars = {**resolved, "issue_number": "1"}
        result = resolve_template("{lint_command}", template_vars, shell_quote=True)
        assert "'" in result  # shlex.quote wraps the value


# ---------------------------------------------------------------------------
# Persistence tests
# ---------------------------------------------------------------------------


class TestParamPersistence:
    def test_params_stored_in_run_record(self, db: Any) -> None:
        params = {"lint_command": "eslint src/", "test_command": "jest"}
        run = create_workflow_run(
            db,
            workflow_id="test",
            workflow_version="1.0",
            target_kind="workflow",
            target_ref="test",
            params=params,
        )
        assert run["params"] == params

    def test_params_round_trip_via_get(self, db: Any) -> None:
        params = {"lint_command": "eslint src/"}
        run = create_workflow_run(
            db,
            workflow_id="test",
            workflow_version="1.0",
            target_kind="workflow",
            target_ref="test",
            params=params,
        )
        fetched = get_workflow_run(db, run["id"])
        assert fetched is not None
        assert fetched["params"] == params

    def test_null_params_for_no_params(self, db: Any) -> None:
        run = create_workflow_run(
            db,
            workflow_id="test",
            workflow_version="1.0",
            target_kind="workflow",
            target_ref="test",
        )
        assert run["params"] is None

    def test_params_deserialized_from_json(self, db: Any) -> None:
        params = {"key": "value with spaces"}
        run = create_workflow_run(
            db,
            workflow_id="test",
            workflow_version="1.0",
            target_kind="workflow",
            target_ref="test",
            params=params,
        )
        fetched = get_workflow_run(db, run["id"])
        assert fetched is not None
        assert fetched["params"]["key"] == "value with spaces"


# ---------------------------------------------------------------------------
# Engine integration tests
# ---------------------------------------------------------------------------


@pytest.fixture(autouse=True)
def _register_test_gates():
    from anteroom.services.workflow_engine import register_gate_condition

    async def always_pass(run: Any, step: Any, inputs: Any) -> bool:
        return True

    register_gate_condition("always_pass", always_pass)
    yield


class TestEngineParamIntegration:
    @pytest.mark.asyncio
    async def test_start_run_resolves_params(self, engine: WorkflowEngine, db: Any) -> None:
        defn = load_definition(YAML_WITH_PARAMS)

        with patch(
            "anteroom.services.workflow_runners.execute_opaque_runner",
            new_callable=AsyncMock,
        ) as mock_runner:
            from anteroom.services.workflow_runners import RunnerResult

            mock_runner.return_value = RunnerResult(status="success", summary="ok")

            run = await engine.start_run(
                defn,
                target_kind="workflow",
                target_ref="test",
                inputs={"issue_number": "42"},
                param_overrides={"lint_command": "eslint ."},
            )

        assert run["status"] == "completed"
        # Verify the runner was called with the resolved param in the command
        calls = mock_runner.call_args_list
        assert len(calls) == 2
        first_call_kwargs = calls[0][1]
        assert "eslint ." in first_call_kwargs.get("command", "")

    @pytest.mark.asyncio
    async def test_start_run_persists_params(self, engine: WorkflowEngine, db: Any) -> None:
        defn = load_definition(YAML_WITH_PARAMS)

        with patch(
            "anteroom.services.workflow_runners.execute_opaque_runner",
            new_callable=AsyncMock,
        ) as mock_runner:
            from anteroom.services.workflow_runners import RunnerResult

            mock_runner.return_value = RunnerResult(status="success", summary="ok")

            run = await engine.start_run(
                defn,
                target_kind="workflow",
                target_ref="test_persist",
                inputs={"issue_number": "99"},
                param_overrides={"test_command": "jest"},
            )

        fetched = get_workflow_run(db, run["id"])
        assert fetched is not None
        assert fetched["params"]["test_command"] == "jest"
        assert fetched["params"]["lint_command"] == "ruff check src/"

    @pytest.mark.asyncio
    async def test_start_run_no_params(self, engine: WorkflowEngine, db: Any) -> None:
        defn = load_definition(YAML_NO_PARAMS)

        with patch(
            "anteroom.services.workflow_runners.execute_opaque_runner",
            new_callable=AsyncMock,
        ) as mock_runner:
            from anteroom.services.workflow_runners import RunnerResult

            mock_runner.return_value = RunnerResult(status="success", summary="ok")

            run = await engine.start_run(
                defn,
                target_kind="workflow",
                target_ref="test_no_params",
            )

        assert run["status"] == "completed"

    @pytest.mark.asyncio
    async def test_start_run_required_param_missing_raises(self, engine: WorkflowEngine) -> None:
        defn = load_definition(YAML_WITH_REQUIRED_PARAM)

        with pytest.raises(ValueError, match="Required param"):
            await engine.start_run(
                defn,
                target_kind="workflow",
                target_ref="test_required",
            )

    @pytest.mark.asyncio
    async def test_enqueue_run_resolves_params(self, engine: WorkflowEngine, db: Any) -> None:
        defn = load_definition(YAML_WITH_PARAMS)

        run = await engine.enqueue_run(
            defn,
            target_kind="workflow",
            target_ref="test_enqueue",
            inputs={"issue_number": "7"},
            param_overrides={"lint_command": "mypy src/"},
        )

        assert run["status"] == "pending"
        fetched = get_workflow_run(db, run["id"])
        assert fetched is not None
        assert fetched["params"]["lint_command"] == "mypy src/"
        assert fetched["params"]["test_command"] == "pytest tests/"
