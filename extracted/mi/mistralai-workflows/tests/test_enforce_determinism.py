from contextlib import ExitStack

import pytest
from temporalio.testing import WorkflowEnvironment

import mistralai.workflows as workflows
from mistralai.workflows.core.config import config
from mistralai.workflows.core.config.config import config as app_config
from mistralai.workflows.core.sandbox import log_if_sandbox_restriction_error
from mistralai.workflows.core.worker import _create_temporal_workers

from .fixtures_sandbox_violation import SandboxRestrictionViolationWorkflow
from .utils import create_test_worker


@workflows.workflow.define(name="nondeterministic")
class NonDeterministicWorkflow:
    import os

    _pid = os.getpid()  # nondeterministic call at class body level

    @workflows.workflow.entrypoint
    async def run(self) -> str:
        return ""


@workflows.workflow.define(name="nondeterministic-enforced", enforce_determinism=True)
class NonDeterministicWorkflowEnforced:
    import os

    _pid = os.getpid()

    @workflows.workflow.entrypoint
    async def run(self) -> str:
        return ""


@workflows.workflow.define(name="nondeterministic-not-enforced", enforce_determinism=False)
class NonDeterministicWorkflowNotEnforced:
    import os

    _pid = os.getpid()

    @workflows.workflow.entrypoint
    async def run(self) -> str:
        return ""


class TestEnforceDeterminism:
    @pytest.mark.asyncio
    async def test_nondeterministic_workflow(self, temporal_env: WorkflowEnvironment) -> None:
        """Determinism enforcement follows the config default."""
        with ExitStack() as context:
            if config.worker.default_enforce_determinism:
                context.enter_context(pytest.raises(RuntimeError))
            async with create_test_worker(
                temporal_env,
                workflows=[NonDeterministicWorkflow],
                activities=[],
            ):
                pass

    @pytest.mark.asyncio
    async def test_nondeterministic_workflow_decorator_enforced(self, temporal_env: WorkflowEnvironment) -> None:
        """enforce_determinism=True on decorator always enforces, regardless of config."""
        with pytest.raises(RuntimeError):
            async with create_test_worker(
                temporal_env,
                workflows=[NonDeterministicWorkflowEnforced],
                activities=[],
            ):
                pass

    @pytest.mark.asyncio
    async def test_nondeterministic_workflow_decorator_not_enforced(self, temporal_env: WorkflowEnvironment) -> None:
        """enforce_determinism=False on decorator never enforces, regardless of config."""
        async with create_test_worker(
            temporal_env,
            workflows=[NonDeterministicWorkflowNotEnforced],
            activities=[],
        ):
            pass

    @pytest.mark.asyncio
    async def test_sandbox_violation_logs_clear_error(
        self, temporal_env: WorkflowEnvironment, caplog: pytest.LogCaptureFixture
    ) -> None:
        """Sandbox violations log a structured error with actionable guidance."""
        with pytest.raises(RuntimeError):
            _create_temporal_workers(
                temporal_client=temporal_env.client,
                workflows=[SandboxRestrictionViolationWorkflow],
                config=app_config,
                task_queue="test-task-queue",
            )

        assert "sandbox validation failed" in caplog.text.lower()
        assert "Import chain:" in caplog.text
        assert "fixtures_sandbox_violation.py" in caplog.text

    def test_log_if_sandbox_restriction_error_logs_on_match(self, caplog: pytest.LogCaptureFixture) -> None:
        """log_if_sandbox_restriction_error logs when a RestrictedWorkflowAccessError is in the chain."""
        from temporalio.worker.workflow_sandbox import RestrictedWorkflowAccessError

        sandbox_err = RestrictedWorkflowAccessError("Cannot access foo.bar")
        wrapper = RuntimeError("workflow task failed")
        wrapper.__cause__ = sandbox_err

        log_if_sandbox_restriction_error(wrapper, context="execution")

        assert "sandbox execution failed" in caplog.text.lower()
        assert "Cannot access foo.bar" in caplog.text

    def test_log_if_sandbox_restriction_error_noop_on_other_errors(self, caplog: pytest.LogCaptureFixture) -> None:
        """log_if_sandbox_restriction_error does nothing for non-sandbox errors."""
        log_if_sandbox_restriction_error(ValueError("unrelated"), context="execution")

        assert "sandbox" not in caplog.text.lower()

    @pytest.mark.timeout(5)
    def test_log_if_sandbox_restriction_error_terminates_on_cyclic_chain(
        self, caplog: pytest.LogCaptureFixture
    ) -> None:
        """A cyclic __cause__ chain must not spin the walker (would trip the deadlock detector)."""
        first = RuntimeError("first")
        second = RuntimeError("second")
        first.__cause__ = second
        second.__cause__ = first

        log_if_sandbox_restriction_error(first, context="execution")

        assert "sandbox" not in caplog.text.lower()
