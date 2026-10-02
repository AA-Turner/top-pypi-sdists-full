"""Workflow execution state service implementation."""

from ..models.common import PaginationParams
from ..models.workflow_state import (
    WorkflowExecutionState,
    WorkflowExecutionStateOutput,
)
from ..utils import ApiRequestHandler


class WorkflowExecutionStateService:
    """Service for managing workflow execution states."""

    def __init__(self, api: ApiRequestHandler, workflow_id: str, execution_id: str):
        """Initialize the workflow execution state service.

        Args:
            api: Request handler for API
            workflow_id: ID of the workflow this service manages states for
            execution_id: ID of the execution this service manages states for
        """
        self._api = api
        self._workflow_id = workflow_id
        self._execution_id = execution_id

    def list(
        self,
        page: int = 0,
        per_page: int = 10,
    ) -> list[WorkflowExecutionState]:
        """List states for the workflow execution with filtering and pagination support.

        Args:
            page: Page number (0-based). Must be >= 0. Defaults to 0.
            per_page: Number of items per page. Must be > 0. Defaults to 10.

        Returns:
            List of WorkflowExecutionState containing state information.
        """
        params = PaginationParams(page=page, per_page=per_page).to_dict()
        return self._api.get(
            f"/v1/workflows/{self._workflow_id}/executions/{self._execution_id}/states",
            list[WorkflowExecutionState],
            params=params,
        )

    def get_output(self, state_id: str) -> WorkflowExecutionStateOutput:
        """Get output for a specific execution state.

        Args:
            state_id: ID of the state to get output for

        Returns:
            WorkflowExecutionStateOutput containing the state output.
        """
        return self._api.get(
            f"/v1/workflows/{self._workflow_id}/executions/{self._execution_id}/states/{state_id}/output",
            WorkflowExecutionStateOutput,
        )
