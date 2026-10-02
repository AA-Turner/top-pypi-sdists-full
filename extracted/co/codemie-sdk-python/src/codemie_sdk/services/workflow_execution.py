"""Workflow execution service implementation."""

from __future__ import annotations

from ..models.common import PaginationParams
from ..models.workflow import WorkflowExecution
from ..models.workflow_execution_payload import WorkflowExecutionCreateRequest
from ..models.workflow_thoughts import WorkflowExecutionThought
from ..models.workflow_transition import WorkflowTransition
from .workflow_execution_state import WorkflowExecutionStateService
from ..utils import ApiRequestHandler


class WorkflowExecutionService:
    """Service for managing workflow executions."""

    def __init__(self, api: ApiRequestHandler, workflow_id: str):
        """Initialize the workflow execution service.

        Args:
            api: Request handler for API
            workflow_id: ID of the workflow this service manages executions for
        """
        self._api = api
        self._workflow_id = workflow_id

    def list(
        self,
        page: int = 0,
        per_page: int = 10,
    ) -> list[WorkflowExecution]:
        """List executions for the workflow with filtering and pagination support.

        Args:
            page: Page number (0-based). Must be >= 0. Defaults to 0.
            per_page: Number of items per page. Must be > 0. Defaults to 10.

        Returns:
            List of WorkflowExecutions  containing execution information.
        """

        params = PaginationParams(page=page, per_page=per_page).to_dict()
        return self._api.get(
            f"/v1/workflows/{self._workflow_id}/executions",
            list[WorkflowExecution],
            params=params,
        )

    def create(
        self,
        user_input: str | None = None,
        file_name: str | None = None,
        conversation_id: str | None = None,
        session_id: str | None = None,
        propagate_headers: bool = False,
        headers: dict[str, str] | None = None,
        tags: list[str] | None = None,
    ) -> dict:
        """Create a new workflow execution.

        Args:
            user_input: Optional input data for the workflow execution.
            file_name: Optional file name associated with the workflow execution.
            conversation_id: Optional conversation ID for workflow chat mode.
            session_id: Optional session identifier for Langfuse tracing. If not provided, execution_id will be used.
            propagate_headers: Enable propagation of X-* HTTP headers to MCP servers.
            headers: Optional additional HTTP headers (e.g., X-* for MCP propagation)
            tags: Optional tags to attach to the workflow execution trace in Langfuse.

        Returns:
            dict: Created workflow execution details
        """
        payload = WorkflowExecutionCreateRequest(
            user_input=user_input,
            file_name=file_name,
            conversation_id=conversation_id,
            session_id=session_id,
            propagate_headers=propagate_headers,
            tags=tags,
        )
        return self._api.post(
            f"/v1/workflows/{self._workflow_id}/executions",
            dict,
            json_data=payload.model_dump(),
            extra_headers=headers,
        )

    def get(self, execution_id: str) -> WorkflowExecution:
        """Get workflow execution by ID.

        Args:
            execution_id: ID of the execution to retrieve

        Returns:
            dict: Workflow execution details
        """
        return self._api.get(
            f"/v1/workflows/{self._workflow_id}/executions/{execution_id}",
            WorkflowExecution,
        )

    def states(self, execution_id: str) -> WorkflowExecutionStateService:
        """Get states service for a specific workflow execution.

        Args:
            execution_id: ID of the execution to get states for

        Returns:
            WorkflowExecutionStateService: Service for managing states of this execution
        """
        return WorkflowExecutionStateService(self._api, self._workflow_id, execution_id)

    def delete_all(self) -> dict:
        """Delete all workflow executions."""
        return self._api.delete(f"/v1/workflows/{self._workflow_id}/executions", dict)

    def delete(self, execution_id: str) -> dict:
        """Delete a single workflow execution.

        Args:
            execution_id: ID of the execution to delete

        Returns:
            dict: Response confirming deletion (e.g. {"message": "Execution removed"})
        """
        return self._api.delete(
            f"/v1/workflows/{self._workflow_id}/executions/{execution_id}", dict
        )

    def abort(self, execution_id: str) -> dict:
        """Abort a running workflow execution.

        Args:
            execution_id: ID of the execution to abort

        Returns:
            dict: Updated workflow execution details
        """
        return self._api.put(
            f"/v1/workflows/{self._workflow_id}/executions/{execution_id}/abort", dict
        )

    def resume(
        self,
        execution_id: str,
        propagate_headers: bool = False,
        headers: dict[str, str] | None = None,
    ) -> dict:
        """Resume an interrupted workflow execution.

        Args:
            execution_id: ID of the execution to resume
            propagate_headers: Enable propagation of X-* HTTP headers to MCP servers.
            headers: Optional additional HTTP headers (e.g., X-* for MCP propagation)

        Returns:
            dict: Updated workflow execution details
        """
        params = {"propagate_headers": propagate_headers}
        # Empty body per API; passing empty dict to satisfy typing
        return self._api.put(
            f"/v1/workflows/{self._workflow_id}/executions/{execution_id}/resume",
            dict,
            json_data={},
            params=params,
            extra_headers=headers,
        )

    def get_transition_to(self, execution_id: str, state_id: str) -> WorkflowTransition:
        """Get the transition that led into a specific state.

        Args:
            execution_id: ID of the execution
            state_id: ID of the destination state

        Returns:
            WorkflowTransition including workflow_context.context_store snapshot
        """
        return self._api.get(
            f"/v1/workflows/{self._workflow_id}/executions/{execution_id}/transitions/to/{state_id}",
            WorkflowTransition,
        )

    def get_thoughts(
        self, execution_id: str, thought_ids: list[str]
    ) -> list[WorkflowExecutionThought]:
        """Get detailed thoughts information for specific thought IDs.

        Args:
            execution_id: ID of the execution to get thoughts for
            thought_ids: List of thought IDs to retrieve detailed information for

        Returns:
            list[WorkflowExecutionThought]: List of detailed thought objects
        """
        return self._api.post(
            f"/v1/workflows/{self._workflow_id}/executions/{execution_id}/thoughts",
            list[WorkflowExecutionThought],
            json_data=thought_ids,
        )
