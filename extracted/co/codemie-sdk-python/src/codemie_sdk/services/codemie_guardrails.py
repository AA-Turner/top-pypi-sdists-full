"""CodeMie guardrail service implementation for managing guardrail assignments."""

from ..models.guardrails import (
    GuardrailAssignmentRequest,
    GuardrailAssignmentResponse,
)
from ..utils import ApiRequestHandler, TokenSource


class CodemieGuardrailService:
    """Service for managing CodeMie guardrail assignments."""

    def __init__(self, api_domain: str, token: TokenSource, verify_ssl: bool = True):
        """Initialize the CodeMie guardrail service.

        Args:
            api_domain: Base URL for the CodeMie API
            token: Authentication token
            verify_ssl: Whether to verify SSL certificates
        """
        self._api = ApiRequestHandler(api_domain, token, verify_ssl)

    def assign_guardrails(
        self,
        guardrail_id: str,
        assignment: GuardrailAssignmentRequest,
    ) -> GuardrailAssignmentResponse:
        """Assign guardrails to project entities (assistants, workflows, datasources).

        Args:
            guardrail_id: ID of the guardrail to assign (AI run ID from installation)
            assignment: Assignment configuration for different entity types

        Returns:
            GuardrailAssignmentResponse with success status

        Example:
            >>> from codemie_sdk.models.guardrails import (
            ...     GuardrailAssignmentRequest,
            ...     GuardrailAssignmentEntity,
            ...     GuardrailAssignmentSetting
            ... )
            >>> # Assign guardrail to all project assistants
            >>> assignment = GuardrailAssignmentRequest(
            ...     assistants=GuardrailAssignmentEntity(
            ...         settings=[GuardrailAssignmentSetting(mode="all", source="input")],
            ...         items=[]
            ...     )
            ... )
            >>> response = client.codemie_guardrails.assign_guardrails(
            ...     guardrail_id="ai_run_123",
            ...     assignment=assignment
            ... )
            >>> if response.success:
            ...     print("Guardrail assigned successfully!")
            >>>
            >>> # Assign to specific assistants
            >>> assignment = GuardrailAssignmentRequest(
            ...     assistants=GuardrailAssignmentEntity(
            ...         settings=[],
            ...         items=["asst_123", "asst_456"]
            ...     )
            ... )
            >>> response = client.codemie_guardrails.assign_guardrails(
            ...     guardrail_id="ai_run_123",
            ...     assignment=assignment
            ... )
        """
        payload = assignment.model_dump(by_alias=True)

        return self._api.put(
            f"/v1/guardrails/{guardrail_id}/assignments",
            GuardrailAssignmentResponse,
            json_data=payload,
            wrap_response=False,
        )
