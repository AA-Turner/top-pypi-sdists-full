from typing import Any

import pytest
from temporalio.client import WorkflowUpdateFailedError

from .fixtures_interactive_workflow import (
    ApprovalInput,
    MultiStepApprovalWorkflow,
    ParallelApprovalWorkflow,
    SimpleApprovalWorkflow,
    StatefulApprovalWorkflow,
    mock_should_publish_event,  # noqa: F401
)
from .utils import create_test_worker, wait_for_pending_inputs


@pytest.mark.usefixtures("mock_should_publish_event")
class TestInteractiveWorkflowIntegration:
    @pytest.mark.asyncio
    async def test_simple_approval_accepted(self, temporal_env: Any) -> None:
        async with create_test_worker(
            temporal_env,
            workflows=[SimpleApprovalWorkflow],
        ):
            handle = await temporal_env.client.start_workflow(
                "simple_approval_workflow",
                {"request_id": "req-001", "description": "Test approval"},
                id="test-simple-approval-accepted",
                task_queue="test-task-queue",
            )

            pending_inputs = await wait_for_pending_inputs(handle, expected_count=1, label="Approval Request")

            first_input = pending_inputs[0]
            assert "task_id" in first_input
            assert "input_schema" in first_input
            assert first_input["label"] == "Approval Request"

            task_id = first_input["task_id"]

            await handle.execute_update(
                "__submit_input",
                {"task_id": task_id, "input": {"approved": True, "reason": "LGTM"}},
            )

            workflow_result = await handle.result()

            assert workflow_result["status"] == "approved"
            assert workflow_result["reason"] == "LGTM"

    @pytest.mark.asyncio
    async def test_multi_step_approval(self, temporal_env: Any) -> None:
        async with create_test_worker(
            temporal_env,
            workflows=[MultiStepApprovalWorkflow],
        ):
            handle = await temporal_env.client.start_workflow(
                "multi_step_approval_workflow",
                {"request_id": "req-005"},
                id="test-multi-step-approval",
                task_queue="test-task-queue",
            )

            pending_inputs = await wait_for_pending_inputs(handle, expected_count=1)
            task_id_1 = pending_inputs[0]["task_id"]

            await handle.execute_update(
                "__submit_input",
                {"task_id": task_id_1, "input": {"approved": True, "reason": "Step 1 OK"}},
            )

            pending_inputs = await wait_for_pending_inputs(handle, expected_count=1)
            task_id_2 = pending_inputs[0]["task_id"]

            await handle.execute_update(
                "__submit_input",
                {"task_id": task_id_2, "input": {"approved": True, "reason": "Step 2 OK"}},
            )

            workflow_result = await handle.result()

            assert workflow_result["final_status"] == "approved"
            assert len(workflow_result["approvals"]) == 2
            assert "Step 1" in workflow_result["approvals"][0]
            assert "Step 2" in workflow_result["approvals"][1]

    @pytest.mark.asyncio
    async def test_stateful_approval_workflow(self, temporal_env: Any) -> None:
        async with create_test_worker(
            temporal_env,
            workflows=[StatefulApprovalWorkflow],
        ):
            handle = await temporal_env.client.start_workflow(
                "stateful_approval_workflow",
                {"request_id": "req-006"},
                id="test-stateful-approval",
                task_queue="test-task-queue",
            )

            pending_inputs = await wait_for_pending_inputs(handle, expected_count=1)
            task_id = pending_inputs[0]["task_id"]

            await handle.execute_update(
                "__submit_input",
                {"task_id": task_id, "input": {"approved": True, "reason": "State tracked"}},
            )

            workflow_result = await handle.result()

            assert workflow_result["status"] == "approved"
            assert "1 approvals" in workflow_result["reason"]

    @pytest.mark.asyncio
    async def test_parallel_approval_workflow(self, temporal_env: Any) -> None:
        async with create_test_worker(
            temporal_env,
            workflows=[ParallelApprovalWorkflow],
        ):
            handle = await temporal_env.client.start_workflow(
                "parallel_approval_workflow",
                {"request_id": "req-007"},
                id="test-parallel-approval",
                task_queue="test-task-queue",
            )

            pending_inputs = await wait_for_pending_inputs(handle, expected_count=2)

            assert len(pending_inputs) == 2, f"Expected 2 pending inputs, got {len(pending_inputs)}"

            labels = {inp["label"] for inp in pending_inputs}

            assert "Manager Approval" in labels
            assert "Executive Approval" in labels

            executive_task = next(inp for inp in pending_inputs if inp["label"] == "Executive Approval")
            manager_task = next(inp for inp in pending_inputs if inp["label"] == "Manager Approval")

            await handle.execute_update(
                "__submit_input",
                {"task_id": executive_task["task_id"], "input": {"approved": True, "reason": "Executive OK"}},
            )

            pending_inputs = await wait_for_pending_inputs(handle, expected_count=1)
            assert len(pending_inputs) == 1, "One input should still be pending"

            await handle.execute_update(
                "__submit_input",
                {"task_id": manager_task["task_id"], "input": {"approved": True, "reason": "Manager OK"}},
            )

            workflow_result = await handle.result()

            assert workflow_result["final_status"] == "approved"
            assert len(workflow_result["approvals"]) == 2

            approval_text = " ".join(workflow_result["approvals"])
            assert "Manager OK" in approval_text
            assert "Executive OK" in approval_text

    @pytest.mark.asyncio
    async def test_submit_input_rejects_unknown_task_id(self, temporal_env: Any) -> None:
        async with create_test_worker(
            temporal_env,
            workflows=[SimpleApprovalWorkflow],
        ):
            handle = await temporal_env.client.start_workflow(
                "simple_approval_workflow",
                {"request_id": "req-unknown", "description": "Test unknown task"},
                id="test-unknown-task-id",
                task_queue="test-task-queue",
            )

            await wait_for_pending_inputs(handle, expected_count=1, label="Approval Request")

            with pytest.raises(WorkflowUpdateFailedError) as exc_info:
                await handle.execute_update(
                    "__submit_input",
                    {"task_id": "nonexistent-task", "input": {"approved": True, "reason": "LGTM"}},
                )
            assert "No pending input request found for task nonexistent-task" in str(exc_info.value.cause)

    @pytest.mark.asyncio
    async def test_submit_input_rejects_invalid_input(self, temporal_env: Any) -> None:
        async with create_test_worker(
            temporal_env,
            workflows=[SimpleApprovalWorkflow],
        ):
            handle = await temporal_env.client.start_workflow(
                "simple_approval_workflow",
                {"request_id": "req-invalid", "description": "Test invalid input"},
                id="test-invalid-input",
                task_queue="test-task-queue",
            )

            pending_inputs = await wait_for_pending_inputs(handle, expected_count=1, label="Approval Request")
            task_id = pending_inputs[0]["task_id"]

            with pytest.raises(WorkflowUpdateFailedError) as exc_info:
                await handle.execute_update(
                    "__submit_input",
                    {"task_id": task_id, "input": {"wrong_field": "bad"}},
                )
            assert "Invalid input for task" in str(exc_info.value.cause)


class TestInputValidation:
    def test_approval_input_valid(self) -> None:
        approval = ApprovalInput(approved=True, reason="Test reason")
        assert approval.approved is True
        assert approval.reason == "Test reason"

    def test_approval_input_invalid_type(self) -> None:
        with pytest.raises(Exception):  # Pydantic validation error
            ApprovalInput(approved="not a bool", reason="Test")  # type: ignore

    def test_approval_input_missing_field(self) -> None:
        with pytest.raises(Exception):  # Pydantic validation error
            ApprovalInput(approved=True)  # type: ignore
