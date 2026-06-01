"""Integration tests for convert_result_to_temporal_format fallback behavior.

When a workflow's return value doesn't match its declared return type, the
convert_result_to_temporal_format function now logs an error and returns the
raw result as a fallback. This prevents workflow task failures that would
cause the workflow to hang forever.

These tests verify:
1. Workflows complete successfully despite type mismatches
2. The raw result is returned as fallback
3. Error is logged (can be verified in caplog)
"""

import pytest
from temporalio.client import WorkflowExecutionStatus
from temporalio.testing import WorkflowEnvironment

import mistralai.workflows as workflows
from mistralai.workflows import get_workflow_definition

from .utils import create_test_worker


# Workflow that declares int return type but returns a dict
# convert_result_to_temporal_format will log error and return raw result
@workflows.workflow.define(name="test-type-mismatch-fallback", enforce_determinism=False)
class TypeMismatchFallbackWorkflow:
    @workflows.workflow.entrypoint
    async def run(self) -> int:
        # The workflow logic completes successfully...
        # But the return type doesn't match the declared int
        # The SDK now returns this as-is instead of raising ValidationError
        return {"unexpected": "dict"}  # type: ignore


class TestConvertResultFallbackBehavior:
    """Tests that demonstrate the fallback behavior for result conversion failures.

    When convert_result_to_temporal_format encounters a ValidationError or other
    exception, it now logs the error and returns the raw result instead of raising.
    This prevents workflows from hanging forever.
    """

    @pytest.mark.asyncio
    async def test_type_mismatch_completes_with_fallback(self, temporal_env: WorkflowEnvironment) -> None:
        """A workflow with type mismatch now completes with raw result fallback."""
        async with create_test_worker(
            temporal_env,
            workflows=[TypeMismatchFallbackWorkflow],
            activities=[],
        ):
            workflow_def = get_workflow_definition(TypeMismatchFallbackWorkflow)
            assert workflow_def is not None

            handle = await temporal_env.client.start_workflow(
                workflow_def.name,
                id="test-type-mismatch-fallback-1",
                task_queue="test-task-queue",
            )

            # Workflow should complete successfully (not hang)
            result = await handle.result()

            # The raw result is returned as fallback
            assert result == {"unexpected": "dict"}

            # Verify workflow completed
            description = await handle.describe()
            assert description.status == WorkflowExecutionStatus.COMPLETED

    @pytest.mark.asyncio
    async def test_type_mismatch_logs_error(
        self, temporal_env: WorkflowEnvironment, caplog: pytest.LogCaptureFixture
    ) -> None:
        """The conversion failure is logged as an error.
        This helps developers identify and fix type mismatches in their workflows.
        """
        async with create_test_worker(
            temporal_env,
            workflows=[TypeMismatchFallbackWorkflow],
            activities=[],
        ):
            workflow_def = get_workflow_definition(TypeMismatchFallbackWorkflow)
            assert workflow_def is not None

            handle = await temporal_env.client.start_workflow(
                workflow_def.name,
                id="test-type-mismatch-fallback-2",
                task_queue="test-task-queue",
            )

            # Workflow completes
            await handle.result()

            # Error should be logged with reason
            error_logs = [r for r in caplog.records if r.levelname == "ERROR"]
            assert any(
                "Failed to convert workflow result to temporal format" in record.message for record in error_logs
            ), f"Expected error log about conversion failure. Logs: {[r.message for r in error_logs]}"
