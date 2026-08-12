import uuid
from datetime import timedelta
from typing import Any, TypeVar, Union

import structlog
import temporalio.workflow
from pydantic import BaseModel, ValidationError
from temporalio.exceptions import ApplicationError

from mistralai.workflows.core._events.event_activities import (
    _emit_waiting_for_input_completed,
    _emit_waiting_for_input_failed,
    _emit_waiting_for_input_started,
)
from mistralai.workflows.core._registration.search_key_ingestion import ingest_search_keys
from mistralai.workflows.core.workflow import workflow

logger = structlog.get_logger(__name__)

T = TypeVar("T", bound=BaseModel)

WAITING_FOR_INPUT_SEARCH_KEY = "internal.execution.state"
WAITING_FOR_INPUT_STATE = "waiting_for_input"
RUNNING_STATE = "running"


class _SubmitInputParams(BaseModel):
    task_id: str
    input: Any


class _SubmitInputResult(BaseModel):
    pass


class _PendingInputRequest(BaseModel):
    task_id: str
    input_schema: type[BaseModel]
    input_schema_dict: dict
    label: str | None = None
    has_received_input: bool = False
    input: Any | None = None


class _PendingInputInfo(BaseModel):
    task_id: str
    input_schema: dict
    label: str | None = None


class _PendingInputsResult(BaseModel):
    pending_inputs: list[_PendingInputInfo]


class InteractiveWorkflow:
    """
    Base class for workflows that need to wait for external input.

    Workflows inheriting from this class gain the ability to pause execution
    and wait for external input via the wait_for_input() method.

    Example usage:
        @workflow.define(name="my-workflow")
        class MyWorkflow(InteractiveWorkflow):
            @workflow.entrypoint
            async def run(self, params: MyInput):
                # Ask human for approval
                approval = await self.wait_for_input(ApprovalSchema)
                if approval.approved:
                    return "Approved!"
                return "Denied"

    How to submit input (from external client):
        await handle.execute_update(
            "__submit_input",
            {"task_id": "task-456", "input": {"approved": True}}
        )
    """

    def __init__(self) -> None:
        super().__init__()
        # In-memory storage: tracks which tasks are waiting for input
        self._pending_inputs: dict[str, _PendingInputRequest] = {}
        # Outstanding wait_for_input calls
        self._pending_wait_count = 0

    async def wait_for_input(
        self, schema: type[T], label: str | None = None, timeout: Union[timedelta, float, None] = None
    ) -> T:
        """
        Pause workflow and wait for external input matching the provided schema.

        The workflow suspends execution until input is submitted via the workflow
        update handler. The task becomes visible in streaming events, allowing
        external systems to detect and respond to the input request.

        Args:
            schema: Pydantic model class defining the expected input structure.
                    Input will be validated against this schema.
            label: Optional human-readable label to identify this input request.
                   Useful when multiple inputs are pending to help clients distinguish
                   between them (e.g., "Manager Approval", "File Upload", "Review Step 1").
            timeout: Optional timeout in seconds (or timedelta) before raising asyncio.TimeoutError.
                     If not specified, the workflow will wait indefinitely.

        Returns:
            Validated input data as an instance of the schema class.

        Raises:
            ValidationError: If submitted input fails validation against the schema.
            asyncio.TimeoutError: If the timeout is reached before input is submitted.

        Example:
            ```python
            from pydantic import BaseModel
            import workflows

            class ApprovalRequest(BaseModel):
                approved: bool
                reviewer: str
                comments: str

            @workflows.define()
            class ApprovalWorkflow(InteractiveWorkflow):
                @workflows.entrypoint
                async def run(self, document_id: str) -> str:
                    # Workflow pauses here until input is submitted
                    approval = await self.wait_for_input(ApprovalRequest)

                    if approval.approved:
                        return f"Document approved by {approval.reviewer}"
                    return f"Document rejected: {approval.comments}"
            ```

        Submitting Input (Client Side):
            ```python
            # Get pending inputs with metadata
            result = await handle.query("__get_pending_inputs")
            # result["pending_inputs"] = [
            #   {
            #     "task_id": "abc-123",
            #     "label": "Manager Approval",
            #     "input_schema": {"type": "object", "properties": {...}}
            #   }
            # ]

            # Find the specific task you want to respond to
            approval_task = next(
                inp for inp in result["pending_inputs"]
                if inp["label"] == "Manager Approval"
            )

            # Submit input for that specific task
            await handle.execute_update(
                "__submit_input",
                {
                    "task_id": approval_task["task_id"],
                    "input": {"approved": True, "reviewer": "Alice", "comments": "LGTM"}
                }
            )
            ```
        """
        task_id = str(temporalio.workflow.uuid4() if temporalio.workflow.in_workflow() else uuid.uuid4())
        schema_dict = schema.model_json_schema()

        pending_request = _PendingInputRequest(
            task_id=task_id,
            input_schema=schema,
            input_schema_dict=schema_dict,
            label=label,
        )

        self._pending_inputs[task_id] = pending_request
        self._pending_wait_count += 1

        def check_received() -> bool:
            return self._pending_inputs.get(task_id, pending_request).has_received_input

        try:
            # Emit CUSTOM_TASK_STARTED event via activity to notify stream consumers
            await temporalio.workflow.execute_local_activity(
                _emit_waiting_for_input_started,
                args=[task_id, schema_dict, label],
                start_to_close_timeout=timedelta(seconds=10),
            )
            await self._write_waiting_state(WAITING_FOR_INPUT_STATE)
            await temporalio.workflow.wait_condition(check_received, timeout=timeout)
            validated_input = schema.model_validate(pending_request.input)
        except BaseException as e:
            await temporalio.workflow.execute_local_activity(
                _emit_waiting_for_input_failed,
                args=[task_id, schema_dict, label, str(e)],
                start_to_close_timeout=timedelta(seconds=10),
            )
            raise
        finally:
            self._pending_inputs.pop(task_id, None)
            self._pending_wait_count -= 1
            if self._pending_wait_count == 0:
                await self._write_waiting_state(RUNNING_STATE)

        await temporalio.workflow.execute_local_activity(
            _emit_waiting_for_input_completed,
            args=[task_id, schema_dict, label, validated_input.model_dump(mode="json")],
            start_to_close_timeout=timedelta(seconds=10),
        )

        return validated_input

    async def _write_waiting_state(self, state: str) -> None:
        try:
            await ingest_search_keys({WAITING_FOR_INPUT_SEARCH_KEY: state}, _allow_reserved=True)
        except Exception as e:
            logger.warning(
                "Could not write the wait-state search key; the execution continues without it",
                state=state,
                error=str(e),
            )

    @workflow.update(name="__submit_input", _internal=True)
    async def _handle_input_submission(self, params: _SubmitInputParams) -> _SubmitInputResult:
        """
        Called by external API when external input is submitted.

        Flow:
        1. External client calls: mistral_client.workflows.executions.update_workflow_execution_async(...)
        2. Temporal routes update to this handler
        3. This handler sets: has_received_input = True
        4. Setting that flag is an EVENT → Temporal re-evaluates wait_condition()
        5. wait_condition() sees flag is True → workflow resumes!

        Args:
            params: Contains task_id and input data from external source

        Returns:
            Result confirming the input was accepted

        Raises:
            ApplicationError: If task_id is unknown or input fails schema validation
        """
        pending_request = self._pending_inputs.get(params.task_id)
        if not pending_request:
            raise ApplicationError(f"No pending input request found for task {params.task_id}", non_retryable=True)

        try:
            pending_request.input_schema.model_validate(params.input)
        except ValidationError as e:
            raise ApplicationError(f"Invalid input for task {params.task_id}: {str(e)}", non_retryable=True) from e

        pending_request.input = params.input
        pending_request.has_received_input = True
        return _SubmitInputResult()

    @workflow.query(name="__get_pending_inputs", _internal=True)
    def _get_pending_inputs(self) -> _PendingInputsResult:
        """
        Query handler to get all pending input requests.

        Returns:
            List of pending input requests with their schemas and labels.
        """
        pending_input_list = [
            _PendingInputInfo(
                task_id=task_id,
                input_schema=request.input_schema_dict,
                label=request.label,
            )
            for task_id, request in self._pending_inputs.items()
        ]
        return _PendingInputsResult(pending_inputs=pending_input_list)
