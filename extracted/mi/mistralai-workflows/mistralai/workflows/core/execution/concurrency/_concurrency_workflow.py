import temporalio.workflow
from temporalio.exceptions import ApplicationError

from mistralai.workflows.core.execution.concurrency.executors._chain_executor import execute_chain_activities
from mistralai.workflows.core.execution.concurrency.executors._list_executor import execute_list_activities
from mistralai.workflows.core.execution.concurrency.executors._offset_pagination_executor import (
    execute_offset_pagination_activities,
)
from mistralai.workflows.core.execution.concurrency.types import (
    ChainExecutorParams,
    ListExecutorParams,
    OffsetPaginationExecutorParams,
    WorkflowParams,
    WorkflowResults,
)
from mistralai.workflows.core.workflow import workflow
from mistralai.workflows.exceptions import WorkflowError


def _extract_first_application_error(eg: ExceptionGroup) -> ApplicationError | None:
    """Recursively search an ExceptionGroup for an ApplicationError.

    Checks direct sub-exceptions, nested ExceptionGroups, and __cause__ chains.
    Prefer non-retryable ApplicationErrors and fall back to the first retryable
    one when no non-retryable ApplicationError is present.
    """
    first_retryable: ApplicationError | None = None
    for exc in eg.exceptions:
        if isinstance(exc, ApplicationError):
            if getattr(exc, "non_retryable", False):
                return exc
            if first_retryable is None:
                first_retryable = exc
            continue
        if isinstance(exc, ExceptionGroup):
            found = _extract_first_application_error(exc)
            if found is not None:
                if getattr(found, "non_retryable", False):
                    return found
                if first_retryable is None:
                    first_retryable = found
        # Walk the __cause__ chain (e.g. ActivityError -> ApplicationError)
        cause = getattr(exc, "__cause__", None)
        while cause is not None:
            if isinstance(cause, ApplicationError):
                if getattr(cause, "non_retryable", False):
                    return cause
                if first_retryable is None:
                    first_retryable = cause
            cause = getattr(cause, "__cause__", None)
    return first_retryable


@workflow.define(name="__parallel_execution__", workflow_display_name="parallel-execution", is_technical=True)
class ParallelExecutionWorkflow:
    """Workflow implementation for concurrent item processing."""

    @workflow.entrypoint
    async def run(self, params: WorkflowParams) -> WorkflowResults:
        """Workflow implementation for concurrent item processing.

        Args:
            params: Parameters for the workflow execution.
        """
        if isinstance(params.params, ListExecutorParams):
            task = execute_list_activities(params.params)
        elif isinstance(params.params, ChainExecutorParams):
            task = execute_chain_activities(params.params)
        elif isinstance(params.params, OffsetPaginationExecutorParams):
            task = execute_offset_pagination_activities(params.params)
        else:
            raise WorkflowError(f"Unknown workflow params type: {type(params.params)}")

        try:
            res = await task
        except Exception as e:
            if isinstance(e, ApplicationError):
                raise
            if isinstance(e, ExceptionGroup):
                # Extract the first meaningful exception from nested TaskGroups
                first = _extract_first_application_error(e)
                if first is not None:
                    raise first from e
            raise WorkflowError(f"Error executing workflow: {e}") from e

        if isinstance(res, WorkflowResults):
            return res
        elif isinstance(res, WorkflowParams):
            temporalio.workflow.continue_as_new(res)
        else:
            raise WorkflowError(f"Unknown workflow result type: {type(res)}")
