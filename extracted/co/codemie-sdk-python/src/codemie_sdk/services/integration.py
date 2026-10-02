"""Integration service implementation."""

import json
from typing import Any, Literal

from ..exceptions import NotFoundError
from ..models.common import PaginationParams
from ..models.integration import (
    Integration,
    IntegrationType,
    IntegrationTestRequest,
    TransferSettingsResponse,
)
from ..utils import ApiRequestHandler, TokenSource


class IntegrationService:
    """Service for managing CodeMie integrations (both user and project settings)."""

    def __init__(self, api_domain: str, token: TokenSource, verify_ssl: bool = True):
        """Initialize the integration service.

        Args:
            api_domain: Base URL for the CodeMie API
            token: Authentication token
            verify_ssl: Whether to verify SSL certificates
        """
        self._api = ApiRequestHandler(api_domain, token, verify_ssl)

    def _get_base_path(self, setting_type: IntegrationType) -> str:
        """Get base API path based on setting type.

        Args:
            setting_type: Type of settings (USER or PROJECT)

        Returns:
            Base API path for the specified setting type
        """
        return f"/v1/settings/{'user' if setting_type == IntegrationType.USER else 'project'}"

    def list_available(
        self,
        scope: Literal["visible_to_user", "marketplace"] = "visible_to_user",
    ) -> list[Integration]:
        """Get integrations available for assistant configuration (credential
        picker), across both USER and PROJECT settings.

        With scope="marketplace", PROJECT integrations from any project the
        caller has access to are included (not only the assistant's own
        project) — this is the endpoint marketplace assistant configuration
        uses to populate its credential picker.

        Args:
            scope: "visible_to_user" for the caller's own project only, or
                "marketplace" to include every project-accessible integration.

        Returns:
            List of integrations the caller may select.
        """
        return self._api.get(
            "/v1/settings/user/available",
            list[Integration],
            params={"scope": scope},
            wrap_response=False,
        )

    def list(
        self,
        setting_type: IntegrationType = IntegrationType.USER,
        page: int = 0,
        per_page: int = 10,
        filters: dict[str, Any] | None = None,
    ) -> list[Integration]:
        """Get list of available integrations.

        Args:
            setting_type: Type of settings to list (USER or PROJECT)
            page: Page number for pagination
            per_page: Number of items per page
            filters: Optional filters to apply

        Returns:
            List of integrations matching the criteria
        """
        params = PaginationParams(page=page, per_page=per_page).to_dict()
        if filters:
            params["filters"] = json.dumps(filters)

        return self._api.get(
            self._get_base_path(setting_type), list[Integration], params=params
        )

    def get(
        self, integration_id: str, setting_type: IntegrationType = IntegrationType.USER
    ) -> Integration:
        """Get integration by ID.

        Args:
            integration_id: ID of the integration to retrieve
            setting_type: Type of settings to get (USER or PROJECT)

        Returns:
            Integration details

        Raises:
            NotFoundError: If integration with given ID is not found
        """
        integrations = self.list(setting_type=setting_type, per_page=100)
        integration = next((i for i in integrations if i.id == integration_id), None)
        if integration is None:
            raise NotFoundError("Integration", integration_id)

        return integration

    def get_by_alias(
        self, alias: str, setting_type: IntegrationType = IntegrationType.USER
    ) -> Integration | None:
        """Get integration by its alias.

        Args:
            alias: Alias of the integration to retrieve
            setting_type: Type of settings to get (USER or PROJECT)

        Returns:
            Integration details if found, None otherwise

        Raises:
            NotFoundError: If integration with given alias is not found
        """
        integrations = self.list(setting_type=setting_type, per_page=100)
        integration = next((i for i in integrations if i.alias == alias), None)

        if integration is None:
            raise NotFoundError("Integration", alias)

        return integration

    def create(self, settings: Integration) -> dict:
        """Create a new integration.

        Args:
            settings: integration creation request

        Returns:
            Created integration details
        """
        return self._api.post(
            self._get_base_path(settings.setting_type),
            dict,
            json_data=settings.model_dump(exclude_none=True),
        )

    def update(self, setting_id: str, settings: Integration) -> dict:
        """Update an existing integration.

        Args:
            setting_id: ID of the integration to update
            settings: integration update request

        Returns:
            Updated integration details
        """
        return self._api.put(
            f"{self._get_base_path(settings.setting_type)}/{setting_id}",
            dict,
            json_data=settings.model_dump(exclude_none=True),
        )

    def delete(
        self, setting_id: str, setting_type: IntegrationType = IntegrationType.USER
    ) -> dict:
        """Delete an integration by ID.

        Args:
            setting_id: ID of the integration to delete
            setting_type: Type of settings to delete (USER or PROJECT)

        Returns:
            Deletion confirmation
        """
        return self._api.delete(
            f"{self._get_base_path(setting_type)}/{setting_id}", dict
        )

    def test(self, integration: IntegrationTestRequest, response_type: Any) -> Any:
        """Test an integration.

        Args:
            integration: IntegrationTestRequest - integration to test
            response_type: Type of response expected

        Returns:
            Test integration response
        """
        return self._api.post(
            "/v1/settings/test/",
            response_model=response_type,
            json_data=integration.model_dump(exclude_none=True),
        )

    def transfer(
        self,
        source_project_name: str,
        target_project_name: str,
        mode: Literal["move", "copy"] | None,
    ) -> TransferSettingsResponse:
        """Move or copy every transferable integration between two projects.

        Calls ``POST /v1/settings/transfer``, which relocates ("move") or
        duplicates ("copy") every transferable ``PROJECT``- and ``USER``-scoped
        integration ("Settings" row) from ``source_project_name`` into
        ``target_project_name`` in a single all-or-nothing transaction.

        Args:
            source_project_name: Name of the project to transfer integrations from
            target_project_name: Name of the project to transfer integrations to
            mode: "move" relocates integrations (removed from source), "copy"
                duplicates them (source left untouched). ``None`` omits the
                ``mode`` field from the request body entirely -- rather than
                sending a JSON ``null`` -- so callers can exercise the API's
                "field required" validation error (distinct from sending an
                unsupported mode value).

        Returns:
            Summary of the transfer, including transferred and skipped items

        Raises:
            requests.exceptions.HTTPError: On 422 (invalid mode/project names),
                404 (source or target project not found), 403 (caller lacks
                admin-or-maintainer privileges), or 409 (alias collision in the
                target project, or a row changed concurrently).
        """
        json_data = {
            "source_project_name": source_project_name,
            "target_project_name": target_project_name,
        }
        if mode is not None:
            json_data["mode"] = mode

        return self._api.post(
            "/v1/settings/transfer",
            TransferSettingsResponse,
            json_data=json_data,
            wrap_response=False,
        )
