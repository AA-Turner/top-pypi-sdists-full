import asyncio
from datetime import timedelta
from typing import Any, Generator
from unittest.mock import patch

import pytest
import temporalio.workflow
from pydantic import BaseModel

from mistralai.workflows import InteractiveWorkflow, workflow
from mistralai.workflows.core.interactive_workflow import (
    _emit_waiting_for_input_failed,
    _emit_waiting_for_input_started,
    _PendingInputRequest,
)


@pytest.fixture
def mock_should_publish_event() -> Generator[Any, None, None]:
    with patch("mistralai.workflows.core.task.task.should_publish_event", return_value=False) as mock:
        yield mock


class ApprovalInput(BaseModel):
    approved: bool
    reason: str


class ApprovalResult(BaseModel):
    status: str
    reason: str


class MultiStepResult(BaseModel):
    approvals: list[str]
    final_status: str


@workflow.define(name="basic_workflow")
class BasicWorkflow(InteractiveWorkflow):
    @workflow.entrypoint
    async def run(self, value: str) -> dict:
        return {"status": "completed", "value": value}


@workflow.define(name="simple_approval_workflow")
class SimpleApprovalWorkflow(InteractiveWorkflow):
    @workflow.entrypoint
    async def run(self, request_id: str, description: str = "Test request") -> ApprovalResult:
        approval = await self.wait_for_input(ApprovalInput, label="Approval Request")

        if approval.approved:
            return ApprovalResult(status="approved", reason=approval.reason)
        else:
            return ApprovalResult(status="rejected", reason=approval.reason)


@workflow.define(name="simple_approval_workflow_with_timeout")
class TimeoutTestWorkflow(InteractiveWorkflow):
    @workflow.entrypoint
    async def run(self) -> ApprovalResult:
        approval = await self.wait_for_input(
            ApprovalInput, label="Approval Request", timeout=timedelta(milliseconds=100)
        )

        if approval.approved:
            return ApprovalResult(status="approved", reason=approval.reason)
        else:
            return ApprovalResult(status="rejected", reason=approval.reason)


@workflow.define(name="multi_step_approval_workflow")
class MultiStepApprovalWorkflow(InteractiveWorkflow):
    @workflow.entrypoint
    async def run(self, request_id: str) -> MultiStepResult:
        approvals = []

        approval1 = await self.wait_for_input(ApprovalInput, label="Manager Approval")
        approvals.append(f"Step 1: {'approved' if approval1.approved else 'rejected'} - {approval1.reason}")

        approval2 = await self.wait_for_input(ApprovalInput, label="Executive Approval")
        approvals.append(f"Step 2: {'approved' if approval2.approved else 'rejected'} - {approval2.reason}")

        all_approved = approval1.approved and approval2.approved
        return MultiStepResult(approvals=approvals, final_status="approved" if all_approved else "rejected")


@workflow.define(name="stateful_approval_workflow")
class StatefulApprovalWorkflow(InteractiveWorkflow):
    def __init__(self) -> None:
        super().__init__()
        self.approvals_received: list[str] = []
        self.status: str = "pending"

    @workflow.entrypoint
    async def run(self, request_id: str) -> ApprovalResult:
        self.status = "waiting_for_approval"

        approval = await self.wait_for_input(ApprovalInput, label="State Tracked Approval")
        self.approvals_received.append(approval.reason)
        self.status = "approved" if approval.approved else "rejected"

        return ApprovalResult(status=self.status, reason=f"Processed {len(self.approvals_received)} approvals")


@workflow.define(name="parallel_approval_workflow")
class ParallelApprovalWorkflow(InteractiveWorkflow):
    @workflow.entrypoint
    async def run(self, request_id: str) -> MultiStepResult:
        approval1_task = asyncio.create_task(self.wait_for_input(ApprovalInput, label="Manager Approval"))
        approval2_task = asyncio.create_task(self.wait_for_input(ApprovalInput, label="Executive Approval"))

        approval1, approval2 = await asyncio.gather(approval1_task, approval2_task)

        approvals = [
            f"Manager: {'approved' if approval1.approved else 'rejected'} - {approval1.reason}",
            f"Executive: {'approved' if approval2.approved else 'rejected'} - {approval2.reason}",
        ]

        all_approved = approval1.approved and approval2.approved
        return MultiStepResult(approvals=approvals, final_status="approved" if all_approved else "rejected")


@workflow.define(name="workflow_with_validation_failure")
class WorkflowWithValidationFailure(InteractiveWorkflow):
    @workflow.entrypoint
    async def run(self, request_id: str) -> ApprovalResult:
        task_id = str(temporalio.workflow.uuid4())
        schema_dict = ApprovalInput.model_json_schema()

        pending_request = _PendingInputRequest(
            task_id=task_id,
            input_schema=ApprovalInput,
            input_schema_dict=schema_dict,
            label="Test Validation Failure",
        )

        self._pending_inputs[task_id] = pending_request

        await temporalio.workflow.execute_local_activity(
            _emit_waiting_for_input_started,
            args=[task_id, schema_dict, "Test Validation Failure"],
            start_to_close_timeout=timedelta(seconds=10),
        )

        pending_request.input = {"invalid": "data"}
        pending_request.has_received_input = True

        try:
            validated_input = ApprovalInput.model_validate(pending_request.input)
            return ApprovalResult(status="approved", reason=validated_input.reason)
        except Exception as e:
            await temporalio.workflow.execute_local_activity(
                _emit_waiting_for_input_failed,
                args=[task_id, schema_dict, "Test Validation Failure", str(e)],
                start_to_close_timeout=timedelta(seconds=10),
            )
            self._pending_inputs.pop(task_id, None)
            return ApprovalResult(status="error", reason=str(e))
