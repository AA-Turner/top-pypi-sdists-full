"""MCPConfigs service — Settings > MCPs management (global catalog entries)."""

from ..models.mcp_config import (
    MCPConfigCloneRequest,
    MCPConfigCreateRequest,
    MCPConfigListResponse,
    MCPConfigResponse,
    MCPConfigUpdateRequest,
)
from ..utils import ApiRequestHandler, TokenSource


class MCPConfigsService:
    """Service for managing global MCP server configurations (Settings > MCPs management)."""

    def __init__(self, api_domain: str, token: TokenSource, verify_ssl: bool = True):
        self._api = ApiRequestHandler(api_domain, token, verify_ssl)

    def create(self, request: MCPConfigCreateRequest) -> MCPConfigResponse:
        """Create a new global MCP configuration entry.

        Args:
            request: MCPConfigCreateRequest with name, config, etc.

        Returns:
            Created MCPConfigResponse with id and metadata.
        """
        return self._api.post(
            "/v1/mcp-configs",
            MCPConfigResponse,
            json_data=request.model_dump(exclude_none=True),
            wrap_response=False,
        )

    def get(self, config_id: str) -> MCPConfigResponse:
        """Retrieve a single global MCP configuration by ID.

        Args:
            config_id: The MCP config entry ID.

        Returns:
            MCPConfigResponse.
        """
        return self._api.get(
            f"/v1/mcp-configs/{config_id}",
            MCPConfigResponse,
            wrap_response=False,
        )

    def list(
        self,
        page: int = 0,
        per_page: int = 20,
        search: str | None = None,
    ) -> list[MCPConfigResponse]:
        """List global MCP configuration entries.

        Args:
            page: 0-indexed page number.
            per_page: Items per page (max 100).
            search: Optional search string.

        Returns:
            List of MCPConfigResponse.
        """
        params: dict = {"page": page, "per_page": per_page}
        if search:
            params["search"] = search

        response = self._api.get(
            "/v1/mcp-configs",
            MCPConfigListResponse,
            params=params,
            wrap_response=False,
        )
        return response.configs

    def clone(
        self, config_id: str, request: MCPConfigCloneRequest
    ) -> MCPConfigResponse:
        """Create a new global MCP configuration from a clone form payload (admin only).

        ``is_public`` and ``is_system`` are always copied from the source configuration.
        An unchanged ``client_secret`` is carried over from the source.

        Args:
            config_id: ID of the source MCP config entry.
            request: MCPConfigCloneRequest with the (possibly edited) parameters of the clone.

        Returns:
            The newly created MCPConfigResponse.
        """
        return self._api.post(
            f"/v1/mcp-configs/{config_id}/clone",
            MCPConfigResponse,
            json_data=request.model_dump(exclude_none=True),
            wrap_response=False,
        )

    def update(
        self, config_id: str, request: MCPConfigUpdateRequest
    ) -> MCPConfigResponse:
        """Update a global MCP configuration (admin only).

        Only the fields set on the request are sent.

        Args:
            config_id: The MCP config entry ID to update.
            request: MCPConfigUpdateRequest with the fields to change.

        Returns:
            Updated MCPConfigResponse.
        """
        return self._api.put(
            f"/v1/mcp-configs/{config_id}",
            MCPConfigResponse,
            json_data=request.model_dump(exclude_none=True),
            wrap_response=False,
        )

    def delete(self, config_id: str) -> None:
        """Delete a global MCP configuration entry.

        Args:
            config_id: The MCP config entry ID to delete.
        """
        self._api.delete(
            f"/v1/mcp-configs/{config_id}",
            dict,
            wrap_response=False,
        )
