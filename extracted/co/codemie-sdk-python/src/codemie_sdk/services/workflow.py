"""Workflow service implementation."""

from __future__ import annotations

import json
from typing import Any

from .workflow_execution import WorkflowExecutionService
from ..models.common import PaginationParams
from ..models.workflow import (
    WorkflowCreateRequest,
    WorkflowUpdateRequest,
    WorkflowEvaluationRequest,
    WorkflowGeneratorRequest,
    WorkflowGeneratorResponse,
    Workflow,
)
from ..utils import ApiRequestHandler, TokenSource


class WorkflowService:
    """Service for managing CodeMie workflows."""

    def __init__(self, api_domain: str, token: TokenSource, verify_ssl: bool = True):
        """Initialize the workflow service.

        Args:
            api_domain: Base URL for the CodeMie API
            token: Authentication token
            verify_ssl: Whether to verify SSL certificates
        """
        self._api = ApiRequestHandler(api_domain, token, verify_ssl)

    def get_prebuilt(self) -> list[Workflow]:
        """Get list of prebuilt workflows.

        Returns:
            List of prebuilt workflow templates
        """
        return self._api.get("/v1/workflows/prebuilt", list[Workflow])

    def create_workflow(self, request: WorkflowCreateRequest) -> dict:
        """Create a new workflow.

        Args:
            request: The workflow creation request containing required fields:
                    - name: Name of the workflow
                    - description: Description of the workflow
                    - project: Project identifier
                    - yaml_config: YAML configuration for the workflow
                    Optional fields with defaults:
                    - mode: WorkflowMode (defaults to SEQUENTIAL)
                    - shared: bool (defaults to False)
                    - icon_url: Optional URL for workflow icon
                    - categories: Optional list of category IDs (at most 3)

        Returns:
            Created WorkflowTemplate instance
        """
        return self._api.post("/v1/workflows", dict, json_data=request.model_dump())

    def generate(
        self,
        text: str,
        llm_model: str | None = None,
        persist: bool = False,
        guardrail_ids: list[str] | None = None,
    ) -> WorkflowGeneratorResponse:
        """Generate a workflow configuration from a natural language description.

        Args:
            text: Natural language description of the desired workflow.
            llm_model: Optional LLM model to use for generation. Falls back to
                the platform default (``WORKFLOW_GENERATOR_LLM_MODEL`` or the
                global default LLM) when not provided.
            persist: When True, the generated workflow is validated
                (``WorkflowExecutor.validate_workflow``) and saved on the
                backend, and the response includes ``workflow_id``. When False
                (default), only the in-memory ``workflow_config`` is returned
                for client-side review/edit before an explicit
                ``create_workflow`` call.
            guardrail_ids: Optional guardrail IDs to attach to the generated
                workflow's guardrail assignments.

        Returns:
            WorkflowGeneratorResponse containing the generated ``workflow_config``
            and, when ``persist=True``, the created ``workflow_id``.
        """
        request = WorkflowGeneratorRequest(
            text=text,
            llm_model=llm_model,
            persist=persist,
            guardrail_ids=guardrail_ids,
        )
        return self._api.post(
            "/v1/workflows/generate",
            WorkflowGeneratorResponse,
            json_data=request.model_dump(exclude_none=True),
        )

    def update(self, workflow_id: str, request: WorkflowUpdateRequest) -> dict:
        """Update an existing workflow.

        Args:
            workflow_id: ID of the workflow to update
            request: The workflow update request containing optional fields to update:
                    - name: New name for the workflow
                    - description: New description
                    - yaml_config: New YAML configuration
                    - mode: New workflow mode
                    - shared: New sharing status
                    - icon_url: New icon URL
                    - categories: New list of category IDs (at most 3); omit to keep
                      the current ones, pass [] to clear them
                    Only specified fields will be updated.

        Returns:
            Updated WorkflowTemplate instance
        """
        return self._api.put(
            f"/v1/workflows/{workflow_id}",
            dict,
            json_data=request.model_dump(exclude_none=True),
        )

    def list(
        self,
        page: int = 0,
        per_page: int = 10,
        projects: list[str] | None = None,
        filters: dict[str, Any] | None = None,
        filter_by_user: bool = False,
    ) -> list[Workflow]:
        """List workflows with filtering and pagination support.

        Args:
            page: Page number (0-based). Must be >= 0. Defaults to 0.
            per_page: Number of items per page. Must be > 0. Defaults to 10.
            projects: Optional projects to filter by.
            filters: Optional filters to apply. Should be a dictionary with filter criteria.

        Returns:
            List of Workflow objects containing workflow information and pagination metadata.

        """

        params = PaginationParams(page=page, per_page=per_page).to_dict()

        if projects:
            params["project"] = projects
        if filters:
            params["filters"] = json.dumps(filters)

        params["filter_by_user"] = filter_by_user

        return self._api.get("/v1/workflows", list[Workflow], params=params)

    def get(self, workflow_id: str) -> Workflow:
        """Get workflow by ID.

        Args:
            workflow_id: The ID of the workflow to retrieve.

        Returns:
            Workflow object containing the workflow information.

        Raises:
            ApiError: If the workflow is not found or other API errors occur.
        """
        return self._api.get(f"/v1/workflows/id/{workflow_id}", Workflow)

    def delete(self, workflow_id: str) -> dict:
        """Delete a workflow by ID.

        Args:
            workflow_id: ID of the workflow to delete

        Returns:
            Deletion confirmation
        """
        return self._api.delete(f"/v1/workflows/{workflow_id}", dict)

    def run(
        self,
        workflow_id: str,
        user_input: str | None = None,
        file_name: str | None = None,
        session_id: str | None = None,
        propagate_headers: bool = False,
        headers: dict[str, str] | None = None,
        tags: list[str] | None = None,
        file_names: list[str] | None = None,
    ) -> dict:
        """Run a workflow with optional input parameters.

        Args:
            workflow_id: ID of the workflow to run
            user_input: Optional user input for the workflow execution
            file_name: Optional file name for the workflow execution
            session_id: Optional session identifier for Langfuse tracing. If not provided, execution_id will be used.
            propagate_headers: Enable propagation of X-* HTTP headers to MCP servers
            headers: Optional additional HTTP headers (e.g., X-* for MCP propagation)
            tags: Optional tags to attach to the workflow execution trace in Langfuse.
            file_names: Optional list of file references provided as inputs to the run.

        Returns:
            dict: Created workflow execution details
        """
        return self.executions(workflow_id).create(
            user_input=user_input,
            file_name=file_name,
            file_names=file_names,
            session_id=session_id,
            propagate_headers=propagate_headers,
            headers=headers,
            tags=tags,
        )

    def evaluate(self, workflow_id: str, request: WorkflowEvaluationRequest) -> dict:
        """Evaluate a workflow with a dataset.

        Args:
            workflow_id: ID of the workflow to evaluate
            request: Evaluation request details

        Returns:
            Evaluation results
        """
        return self._api.post(
            f"/v1/workflows/{workflow_id}/evaluate",
            dict,
            json_data=request.model_dump(exclude_none=True),
        )

    def publish(self, workflow_id: str, categories: list[str] | None = None) -> dict:
        """Publish a workflow to the marketplace, setting ``is_global=True``.

        Args:
            workflow_id: ID of the workflow to publish
            categories: Optional list of category IDs for marketplace classification

        Returns:
            Publication confirmation
        """
        body = {}
        if categories:
            body["categories"] = categories
        return self._api.post(
            f"/v1/workflows/{workflow_id}/marketplace/publish",
            dict,
            json_data=body if body else None,
        )

    def marketplace_validate(self, workflow_id: str) -> dict:
        """Validate a workflow before publishing to the marketplace.

        Surfaces the credential/warning review for the pending publish without
        changing ``is_global``.

        Args:
            workflow_id: ID of the workflow to validate

        Returns:
            Validation result, including any credential warnings
        """
        return self._api.post(
            f"/v1/workflows/{workflow_id}/marketplace/publish/validate", dict
        )

    def unpublish(self, workflow_id: str) -> dict:
        """Unpublish a workflow from the marketplace, setting ``is_global=False``.

        Args:
            workflow_id: ID of the workflow to unpublish

        Returns:
            Unpublication confirmation
        """
        return self._api.post(
            f"/v1/workflows/{workflow_id}/marketplace/unpublish", dict
        )

    def executions(self, workflow_id: str) -> WorkflowExecutionService:
        """Get workflow execution service for the specified workflow.

        Args:
            workflow_id: ID of the workflow to manage executions for

        Returns:
            WorkflowExecutionService instance configured for the specified workflow
        """
        return WorkflowExecutionService(self._api, workflow_id)
