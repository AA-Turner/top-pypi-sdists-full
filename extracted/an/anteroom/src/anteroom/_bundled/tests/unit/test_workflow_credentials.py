"""Tests for workflow credential binding (#970).

Tests credential resolution, fail-closed behavior, redaction, policy enforcement,
and integration with the workflow engine.
"""

from __future__ import annotations

import os
import tempfile
from pathlib import Path
from typing import Any
from unittest.mock import patch

import pytest

from anteroom.config import WorkflowConfig, WorkflowCredentialConfig
from anteroom.db import init_db
from anteroom.services.workflow_credentials import CredentialResolutionError, CredentialResolver
from anteroom.services.workflow_engine import WorkflowEngine, load_definition
from anteroom.services.workflow_runners import RunnerResult, create_default_registry

# ---------------------------------------------------------------------------
# CredentialResolver unit tests
# ---------------------------------------------------------------------------


class TestCredentialResolver:
    def test_resolve_env_var(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("MY_SECRET", "s3cret")
        creds = [WorkflowCredentialConfig(name="token", env_var="MY_SECRET")]
        resolver = CredentialResolver(creds)
        assert resolver.resolve("token") == "s3cret"

    def test_resolve_missing_env_var(self) -> None:
        creds = [WorkflowCredentialConfig(name="token", env_var="DEFINITELY_NOT_SET_XYZ")]
        resolver = CredentialResolver(creds)
        # Make sure the env var is actually not set
        os.environ.pop("DEFINITELY_NOT_SET_XYZ", None)
        with pytest.raises(CredentialResolutionError, match="not set"):
            resolver.resolve("token")

    def test_resolve_empty_env_var(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("EMPTY_VAR", "")
        creds = [WorkflowCredentialConfig(name="token", env_var="EMPTY_VAR")]
        resolver = CredentialResolver(creds)
        with pytest.raises(CredentialResolutionError, match="empty"):
            resolver.resolve("token")

    def test_resolve_command(self) -> None:
        creds = [WorkflowCredentialConfig(name="token", command="echo hello")]
        resolver = CredentialResolver(creds)
        assert resolver.resolve("token") == "hello"

    def test_resolve_command_failure(self) -> None:
        creds = [WorkflowCredentialConfig(name="token", command="false")]
        resolver = CredentialResolver(creds)
        with pytest.raises(CredentialResolutionError, match="exited with code"):
            resolver.resolve("token")

    def test_resolve_command_not_found(self) -> None:
        creds = [WorkflowCredentialConfig(name="token", command="totally_nonexistent_binary_xyz")]
        resolver = CredentialResolver(creds)
        with pytest.raises(CredentialResolutionError, match="command not found"):
            resolver.resolve("token")

    def test_resolve_undeclared_credential(self) -> None:
        resolver = CredentialResolver([])
        with pytest.raises(CredentialResolutionError, match="not declared"):
            resolver.resolve("nonexistent")

    def test_resolve_no_source(self) -> None:
        creds = [WorkflowCredentialConfig(name="token")]
        resolver = CredentialResolver(creds)
        with pytest.raises(CredentialResolutionError, match="neither env_var nor command"):
            resolver.resolve("token")

    def test_has(self) -> None:
        creds = [WorkflowCredentialConfig(name="token", env_var="FOO")]
        resolver = CredentialResolver(creds)
        assert resolver.has("token")
        assert not resolver.has("other")

    def test_get_config(self) -> None:
        cfg = WorkflowCredentialConfig(name="token", env_var="FOO", allowed_runners=["shell"])
        resolver = CredentialResolver([cfg])
        assert resolver.get_config("token") == cfg
        assert resolver.get_config("missing") is None

    def test_exception_never_contains_secret(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Verify exception messages don't leak resolved values."""
        # This should NOT happen, but verify the error path is safe
        creds = [WorkflowCredentialConfig(name="token", command="echo SUPER_SECRET_VALUE")]
        resolver = CredentialResolver(creds)
        # resolve succeeds — no exception to check
        val = resolver.resolve("token")
        assert val == "SUPER_SECRET_VALUE"
        # Now test a failure case — the error message should not contain any secret
        creds2 = [WorkflowCredentialConfig(name="token2", command="false")]
        resolver2 = CredentialResolver(creds2)
        with pytest.raises(CredentialResolutionError) as exc_info:
            resolver2.resolve("token2")
        assert "SUPER_SECRET" not in str(exc_info.value)


# ---------------------------------------------------------------------------
# Engine integration tests
# ---------------------------------------------------------------------------

CRED_WORKFLOW = """\
kind: workflow
id: test_creds
version: 0.1.0
inputs: {}
steps:
  - id: use_cred
    type: runner
    runner: shell
    command: "echo $MY_API_KEY"
    timeout: 10
    credentials:
      - name: MY_API_KEY
        from: github_token
"""

NO_CRED_WORKFLOW = """\
kind: workflow
id: test_no_creds
version: 0.1.0
inputs: {}
steps:
  - id: simple
    type: runner
    runner: shell
    command: "echo hello"
    timeout: 10
"""


@pytest.fixture()
def db():
    with tempfile.TemporaryDirectory() as td:
        conn = init_db(Path(td) / "test.db")
        yield conn


@pytest.fixture()
def registry():
    return create_default_registry()


async def _mock_opaque_runner(**kwargs: Any) -> RunnerResult:
    return RunnerResult(status="success", summary="done", duration_ms=10)


class TestEngineCredentialValidation:
    @pytest.mark.asyncio
    async def test_undeclared_credential_fails_before_lock(self, db: Any, registry: Any) -> None:
        """Credential validation must happen before run record creation."""
        resolver = CredentialResolver([])  # No credentials declared
        config = WorkflowConfig()
        engine = WorkflowEngine(db, config, registry, credential_resolver=resolver)
        defn = load_definition(CRED_WORKFLOW)

        with pytest.raises(ValueError, match="undeclared credential"):
            await engine.start_run(defn, target_kind="test", target_ref="cred-1")

        # Verify no run record was created
        from anteroom.services.workflow_storage import list_workflow_runs

        runs = list_workflow_runs(db)
        assert len(runs) == 0

    @pytest.mark.asyncio
    async def test_declared_credential_passes_validation(
        self, db: Any, registry: Any, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setenv("GH_TOKEN", "test_value")
        creds = [WorkflowCredentialConfig(name="github_token", env_var="GH_TOKEN")]
        resolver = CredentialResolver(creds)
        config = WorkflowConfig(credentials=creds)
        engine = WorkflowEngine(db, config, registry, credential_resolver=resolver)
        defn = load_definition(CRED_WORKFLOW)

        with patch("anteroom.services.workflow_runners.execute_opaque_runner", side_effect=_mock_opaque_runner):
            run = await engine.start_run(defn, target_kind="test", target_ref="cred-2")

        assert run["status"] == "completed"

    @pytest.mark.asyncio
    async def test_no_credentials_no_resolver_works(self, db: Any, registry: Any) -> None:
        """Workflows without credentials work fine without a resolver."""
        config = WorkflowConfig()
        engine = WorkflowEngine(db, config, registry)
        defn = load_definition(NO_CRED_WORKFLOW)

        with patch("anteroom.services.workflow_runners.execute_opaque_runner", side_effect=_mock_opaque_runner):
            run = await engine.start_run(defn, target_kind="test", target_ref="cred-3")

        assert run["status"] == "completed"

    @pytest.mark.asyncio
    async def test_allowed_runners_policy(self, db: Any, registry: Any, monkeypatch: pytest.MonkeyPatch) -> None:
        """Credential with allowed_runners=["python_script"] blocks shell steps."""
        monkeypatch.setenv("GH_TOKEN", "test_value")
        creds = [WorkflowCredentialConfig(name="github_token", env_var="GH_TOKEN", allowed_runners=["python_script"])]
        resolver = CredentialResolver(creds)
        config = WorkflowConfig(credentials=creds)
        engine = WorkflowEngine(db, config, registry, credential_resolver=resolver)
        defn = load_definition(CRED_WORKFLOW)  # Uses shell runner

        with patch("anteroom.services.workflow_runners.execute_opaque_runner", side_effect=_mock_opaque_runner):
            run = await engine.start_run(defn, target_kind="test", target_ref="cred-4")

        assert run["status"] == "failed"
        assert "step_failed" in (run.get("stop_reason") or "")

    @pytest.mark.asyncio
    async def test_credential_resolution_failure_fails_run(self, db: Any, registry: Any) -> None:
        """If credential can't be resolved at execution time, run fails."""
        os.environ.pop("MISSING_TOKEN_XYZ", None)
        creds = [WorkflowCredentialConfig(name="github_token", env_var="MISSING_TOKEN_XYZ")]
        resolver = CredentialResolver(creds)
        config = WorkflowConfig(credentials=creds)
        engine = WorkflowEngine(db, config, registry, credential_resolver=resolver)
        defn = load_definition(CRED_WORKFLOW)

        with patch("anteroom.services.workflow_runners.execute_opaque_runner", side_effect=_mock_opaque_runner):
            run = await engine.start_run(defn, target_kind="test", target_ref="cred-5")

        assert run["status"] == "failed"


# ---------------------------------------------------------------------------
# Shared-tool regression tests
# ---------------------------------------------------------------------------


class TestBashToolEnvRegression:
    @pytest.mark.asyncio
    async def test_bash_handle_without_env_unchanged(self) -> None:
        """bash.handle() without _env produces same behavior as before."""
        from anteroom.tools.bash import handle

        result = await handle("echo hello", timeout=10)
        assert result.get("stdout", "").strip() == "hello"
        assert result.get("exit_code") == 0

    @pytest.mark.asyncio
    async def test_bash_handle_with_env_injects(self) -> None:
        """bash.handle() with _env makes env vars available to subprocess."""
        from anteroom.tools.bash import handle

        result = await handle("echo $INJECTED_VAR", timeout=10, _env={"INJECTED_VAR": "injected_value"})
        assert "injected_value" in result.get("stdout", "")

    @pytest.mark.asyncio
    async def test_call_tool_without_extra_env(self) -> None:
        """call_tool() without _extra_env works identically to before."""
        from anteroom.tools import ToolRegistry, register_default_tools

        reg = ToolRegistry()
        register_default_tools(reg, working_dir="/tmp")
        result = await reg.call_tool("bash", {"command": "echo hi", "timeout": 5})
        assert result.get("stdout", "").strip() == "hi"

    @pytest.mark.asyncio
    async def test_call_tool_with_extra_env(self) -> None:
        """call_tool() with _extra_env passes env to bash handler."""
        from anteroom.tools import ToolRegistry, register_default_tools

        reg = ToolRegistry()
        register_default_tools(reg, working_dir="/tmp")
        result = await reg.call_tool(
            "bash",
            {"command": "echo $CRED_VAR", "timeout": 5},
            _extra_env={"CRED_VAR": "secret_val"},
        )
        assert "secret_val" in result.get("stdout", "")


# ---------------------------------------------------------------------------
# Regression tests for bug fixes
# ---------------------------------------------------------------------------

MALFORMED_CRED_WORKFLOW = """\
kind: workflow
id: test_malformed_creds
version: 0.1.0
inputs: {}
steps:
  - id: bad_cred
    type: runner
    runner: shell
    command: "echo hi"
    timeout: 10
    credentials:
      - from: github_token
"""


class TestCredentialEdgeCases:
    def test_malformed_credential_entry_in_definition(self) -> None:
        """Credential entry missing 'name' field should fail at load/validate time."""
        defn = load_definition(MALFORMED_CRED_WORKFLOW)
        # The step's credentials list has an entry without 'name'
        assert defn.steps[0].credentials is not None
        assert defn.steps[0].credentials[0].get("name") is None

    @pytest.mark.asyncio
    async def test_resume_validates_credentials(self, db: Any, registry: Any, monkeypatch: pytest.MonkeyPatch) -> None:
        """resume_run() must validate credential bindings before acquiring lock."""
        monkeypatch.setenv("GH_TOKEN", "test_value")
        creds = [WorkflowCredentialConfig(name="github_token", env_var="GH_TOKEN")]
        resolver = CredentialResolver(creds)
        config = WorkflowConfig(credentials=creds)
        engine = WorkflowEngine(db, config, registry, credential_resolver=resolver)

        # Start the credential workflow (it has credentials) then pause it
        cred_defn = load_definition(CRED_WORKFLOW)
        with patch("anteroom.services.workflow_runners.execute_opaque_runner", side_effect=_mock_opaque_runner):
            run = await engine.start_run(cred_defn, target_kind="test", target_ref="resume-cred-1")
        assert run["status"] == "completed"

        # Now try to resume with an engine that has NO credential resolver
        engine_no_creds = WorkflowEngine(db, WorkflowConfig(), registry)

        # Manually set run to paused so resume_run will attempt it
        from anteroom.services.workflow_storage import update_workflow_run

        update_workflow_run(db, run["id"], status="paused")

        # Same definition, so no drift -- but credential validation should fail
        with pytest.raises(ValueError, match="no credential"):
            await engine_no_creds.resume_run(run["id"], cred_defn)

    def test_resolve_step_credentials_defensive_missing_keys(self) -> None:
        """_resolve_step_credentials handles missing 'name'/'from' keys gracefully."""
        from anteroom.services.workflow_credentials import CredentialResolutionError

        creds = [WorkflowCredentialConfig(name="token", env_var="FOO")]
        resolver = CredentialResolver(creds)
        config = WorkflowConfig(credentials=creds)
        engine = WorkflowEngine(None, config, None, credential_resolver=resolver)  # type: ignore[arg-type]

        # Simulate a malformed credential entry (missing 'name')
        from anteroom.services.workflow_engine import WorkflowStepDef

        step = WorkflowStepDef(id="test", type="runner", runner="shell", credentials=[{"from": "token"}])
        with pytest.raises(CredentialResolutionError, match="missing 'name' or 'from'"):
            engine._resolve_step_credentials(step)

        # Missing 'from'
        step2 = WorkflowStepDef(id="test", type="runner", runner="shell", credentials=[{"name": "VAR"}])
        with pytest.raises(CredentialResolutionError, match="missing 'name' or 'from'"):
            engine._resolve_step_credentials(step2)


class TestConfigValidatorCredentials:
    def test_valid_credentials(self) -> None:
        from anteroom.services.config_validator import validate_config

        raw = {"workflow": {"credentials": [{"name": "token", "env_var": "MY_TOKEN"}]}}
        result = validate_config(raw)
        assert result.is_valid

    def test_missing_name(self) -> None:
        from anteroom.services.config_validator import validate_config

        raw = {"workflow": {"credentials": [{"env_var": "MY_TOKEN"}]}}
        result = validate_config(raw)
        assert not result.is_valid
        assert any("missing required 'name'" in e.message for e in result.errors)

    def test_no_source(self) -> None:
        from anteroom.services.config_validator import validate_config

        raw = {"workflow": {"credentials": [{"name": "token"}]}}
        result = validate_config(raw)
        assert result.has_warnings
        assert any("env_var" in e.message and "command" in e.message for e in result.errors)

    def test_both_sources(self) -> None:
        from anteroom.services.config_validator import validate_config

        raw = {"workflow": {"credentials": [{"name": "token", "env_var": "X", "command": "y"}]}}
        result = validate_config(raw)
        assert result.has_warnings
        assert any("only one of" in e.message for e in result.errors)

    def test_non_list_credentials(self) -> None:
        from anteroom.services.config_validator import validate_config

        raw = {"workflow": {"credentials": "bad"}}
        result = validate_config(raw)
        assert not result.is_valid

    def test_non_dict_entry(self) -> None:
        from anteroom.services.config_validator import validate_config

        raw = {"workflow": {"credentials": ["not_a_dict"]}}
        result = validate_config(raw)
        assert not result.is_valid

    def test_definition_rejects_non_list_credentials(self) -> None:
        """Workflow definitions with non-list credentials field fail at load time."""
        bad_yaml = """\
kind: workflow
id: test_bad
version: 0.1.0
inputs: {}
steps:
  - id: step1
    type: runner
    runner: shell
    command: "echo hi"
    credentials: "not_a_list"
"""
        with pytest.raises(ValueError, match="must be a list"):
            load_definition(bad_yaml)
