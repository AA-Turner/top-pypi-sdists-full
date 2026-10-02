"""A2A (agent-to-agent) service implementation."""

from ..models.a2a import AgentCard
from ..utils import ApiRequestHandler, TokenSource


class A2AService:
    """Service for A2A agent discovery endpoints."""

    def __init__(self, api_domain: str, token: TokenSource, verify_ssl: bool = True):
        """Initialize the A2A service.

        Args:
            api_domain: Base URL for the CodeMie API
            token: Authentication token
            verify_ssl: Whether to verify SSL certificates
        """
        self._api = ApiRequestHandler(api_domain, token, verify_ssl)

    def get_agent_card(self, assistant_id: str) -> AgentCard:
        """Get the A2A agent card for an assistant.

        Args:
            assistant_id: ID of the assistant

        Returns:
            AgentCard: agent discovery metadata for the assistant
        """
        return self._api.get(
            f"/v1/a2a/assistants/{assistant_id}/.well-known/agent.json",
            AgentCard,
            wrap_response=False,
        )
