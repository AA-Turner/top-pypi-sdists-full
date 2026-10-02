"""Vendor service implementation for managing cloud vendor assistant settings."""

from typing import Union

from ..models.vendor_assistant import (
    VendorType,
    VendorAssistantSettingsResponse,
    VendorAssistantsResponse,
    VendorAssistant,
    VendorAssistantVersion,
    VendorAssistantAliasesResponse,
    VendorAssistantInstallRequest,
    VendorAssistantInstallResponse,
    VendorAssistantUninstallResponse,
)
from ..utils import ApiRequestHandler, TokenSource


class VendorAssistantService:
    """Service for managing cloud vendor assistant settings (AWS, Azure, GCP)."""

    def __init__(self, api_domain: str, token: TokenSource, verify_ssl: bool = True):
        """Initialize the vendor service.

        Args:
            api_domain: Base URL for the CodeMie API
            token: Authentication token
            verify_ssl: Whether to verify SSL certificates
        """
        self._api = ApiRequestHandler(api_domain, token, verify_ssl)

    def get_assistant_settings(
        self,
        vendor: Union[VendorType, str],
        page: int = 0,
        per_page: int = 10,
    ) -> VendorAssistantSettingsResponse:
        """Get assistant settings for a specific cloud vendor.

        Args:
            vendor: Cloud vendor type (aws, azure, gcp). Can be VendorType enum or string.
            page: Page number for pagination (0-based)
            per_page: Number of items per page

        Returns:
            VendorAssistantSettingsResponse containing list of settings and pagination info

        Example:
            >>> # Using enum
            >>> settings = client.vendor_assistants.get_assistant_settings(VendorType.AWS, page=0, per_page=10)
            >>> # Using string
            >>> settings = client.vendor_assistants.get_assistant_settings("aws", page=0, per_page=10)
        """
        # Convert enum to string value if needed
        vendor_str = vendor.value if isinstance(vendor, VendorType) else vendor

        params = {
            "page": page,
            "per_page": per_page,
        }

        return self._api.get(
            f"/v1/vendors/{vendor_str}/assistants/settings",
            VendorAssistantSettingsResponse,
            params=params,
            wrap_response=False,
        )

    def get_assistants(
        self,
        vendor: Union[VendorType, str],
        setting_id: str,
        per_page: int = 10,
        next_token: str | None = None,
    ) -> VendorAssistantsResponse:
        """Get assistants for a specific vendor setting.

        Args:
            vendor: Cloud vendor type (aws, azure, gcp). Can be VendorType enum or string.
            setting_id: ID of the vendor setting to retrieve assistants for
            per_page: Number of items per page
            next_token: Token for pagination (optional, for retrieving next page)

        Returns:
            VendorAssistantsResponse containing list of assistants and pagination token

        Example:
            >>> # Get first page
            >>> assistants = client.vendor_assistants.get_assistants(
            ...     vendor=VendorType.AWS,
            ...     setting_id="cac90788-39b7-4ffe-8b57-e8b047fa1f6c",
            ...     per_page=8
            ... )
            >>> # Get next page if available
            >>> if assistants.pagination.next_token:
            ...     next_page = client.vendor_assistants.get_assistants(
            ...         vendor=VendorType.AWS,
            ...         setting_id="cac90788-39b7-4ffe-8b57-e8b047fa1f6c",
            ...         per_page=8,
            ...         next_token=assistants.pagination.next_token
            ...     )
        """
        # Convert enum to string value if needed
        vendor_str = vendor.value if isinstance(vendor, VendorType) else vendor

        params = {
            "setting_id": setting_id,
            "per_page": per_page,
        }

        if next_token:
            params["next_token"] = next_token

        return self._api.get(
            f"/v1/vendors/{vendor_str}/assistants",
            VendorAssistantsResponse,
            params=params,
            wrap_response=False,
        )

    def get_assistant(
        self,
        vendor: Union[VendorType, str],
        assistant_id: str,
        setting_id: str,
    ) -> VendorAssistant:
        """Get a specific assistant by ID for a vendor setting.

        Args:
            vendor: Cloud vendor type (aws, azure, gcp). Can be VendorType enum or string.
            assistant_id: ID of the assistant to retrieve
            setting_id: ID of the vendor setting

        Returns:
            VendorAssistant containing assistant details

        Example:
            >>> assistant = client.vendor_assistants.get_assistant(
            ...     vendor=VendorType.AWS,
            ...     assistant_id="TJBKR0DGWT",
            ...     setting_id="cac90788-39b7-4ffe-8b57-e8b047fa1f6c"
            ... )
            >>> print(f"Name: {assistant.name}, Status: {assistant.status}")
        """
        # Convert enum to string value if needed
        vendor_str = vendor.value if isinstance(vendor, VendorType) else vendor

        params = {
            "setting_id": setting_id,
        }

        return self._api.get(
            f"/v1/vendors/{vendor_str}/assistants/{assistant_id}",
            VendorAssistant,
            params=params,
            wrap_response=False,
        )

    def get_assistant_version(
        self,
        vendor: Union[VendorType, str],
        assistant_id: str,
        version: str,
        setting_id: str,
    ) -> VendorAssistantVersion:
        """Get a specific version of a vendor assistant with detailed information.

        Args:
            vendor: Cloud vendor type (aws, azure, gcp). Can be VendorType enum or string.
            assistant_id: ID of the assistant to retrieve
            version: Version number to retrieve (e.g., "1", "DRAFT")
            setting_id: ID of the vendor setting

        Returns:
            VendorAssistantVersion containing detailed version information including
            instruction, foundation model, and timestamps

        Example:
            >>> version_details = client.vendor_assistants.get_assistant_version(
            ...     vendor=VendorType.AWS,
            ...     assistant_id="TJBKR0DGWT",
            ...     version="1",
            ...     setting_id="cac90788-39b7-4ffe-8b57-e8b047fa1f6c"
            ... )
            >>> print(f"Name: {version_details.name}")
            >>> print(f"Version: {version_details.version}")
            >>> print(f"Instruction: {version_details.instruction}")
            >>> print(f"Model: {version_details.foundationModel}")
        """
        # Convert enum to string value if needed
        vendor_str = vendor.value if isinstance(vendor, VendorType) else vendor

        params = {
            "setting_id": setting_id,
        }

        return self._api.get(
            f"/v1/vendors/{vendor_str}/assistants/{assistant_id}/{version}",
            VendorAssistantVersion,
            params=params,
            wrap_response=False,
        )

    def get_assistant_aliases(
        self,
        vendor: Union[VendorType, str],
        assistant_id: str,
        setting_id: str,
        per_page: int = 10,
        next_token: str | None = None,
    ) -> VendorAssistantAliasesResponse:
        """Get aliases for a specific vendor assistant.

        Args:
            vendor: Cloud vendor type (aws, azure, gcp). Can be VendorType enum or string.
            assistant_id: ID of the assistant to retrieve aliases for
            setting_id: ID of the vendor setting
            per_page: Number of items per page
            next_token: Token for pagination (optional, for retrieving next page)

        Returns:
            VendorAssistantAliasesResponse containing list of aliases and pagination token

        Example:
            >>> # Get first page of aliases
            >>> aliases = client.vendor_assistants.get_assistant_aliases(
            ...     vendor=VendorType.AWS,
            ...     assistant_id="TJBKR0DGWT",
            ...     setting_id="cac90788-39b7-4ffe-8b57-e8b047fa1f6c",
            ...     per_page=5
            ... )
            >>> for alias in aliases.data:
            ...     print(f"{alias.name} (v{alias.version}): {alias.status}")
            >>> # Get next page if available
            >>> if aliases.pagination.next_token:
            ...     next_page = client.vendor_assistants.get_assistant_aliases(
            ...         vendor=VendorType.AWS,
            ...         assistant_id="TJBKR0DGWT",
            ...         setting_id="cac90788-39b7-4ffe-8b57-e8b047fa1f6c",
            ...         per_page=5,
            ...         next_token=aliases.pagination.next_token
            ...     )
        """
        # Convert enum to string value if needed
        vendor_str = vendor.value if isinstance(vendor, VendorType) else vendor

        params = {
            "setting_id": setting_id,
            "per_page": per_page,
        }

        if next_token:
            params["next_token"] = next_token

        return self._api.get(
            f"/v1/vendors/{vendor_str}/assistants/{assistant_id}/aliases",
            VendorAssistantAliasesResponse,
            params=params,
            wrap_response=False,
        )

    def install_assistants(
        self,
        vendor: Union[VendorType, str],
        assistants: list[VendorAssistantInstallRequest],
    ) -> VendorAssistantInstallResponse:
        """Install/activate vendor assistants.

        Args:
            vendor: Cloud vendor type (aws, azure, gcp). Can be VendorType enum or string.
            assistants: List of assistant installation requests with assistant ID, alias ID, and setting ID

        Returns:
            VendorAssistantInstallResponse containing installation summary with AI run IDs

        Example:
            >>> from codemie_sdk import VendorAssistantInstallRequest
            >>> # Install single assistant
            >>> install_request = VendorAssistantInstallRequest(
            ...     id="TJBKR0DGWT",
            ...     agentAliasId="MNULODIW4N",
            ...     setting_id="cac90788-39b7-4ffe-8b57-e8b047fa1f6c"
            ... )
            >>> response = client.vendor_assistants.install_assistants(
            ...     vendor=VendorType.AWS,
            ...     assistants=[install_request]
            ... )
            >>> for item in response.summary:
            ...     print(f"Installed {item.agentId} with run ID: {item.aiRunId}")
            >>>
            >>> # Install multiple assistants
            >>> requests = [
            ...     VendorAssistantInstallRequest(
            ...         id="ASSISTANT_ID_1",
            ...         agentAliasId="ALIAS_ID_1",
            ...         setting_id="SETTING_ID"
            ...     ),
            ...     VendorAssistantInstallRequest(
            ...         id="ASSISTANT_ID_2",
            ...         agentAliasId="ALIAS_ID_2",
            ...         setting_id="SETTING_ID"
            ...     )
            ... ]
            >>> response = client.vendor_assistants.install_assistants(
            ...     vendor=VendorType.AWS,
            ...     assistants=requests
            ... )
        """
        # Convert enum to string value if needed
        vendor_str = vendor.value if isinstance(vendor, VendorType) else vendor

        # Convert list of Pydantic models to list of dicts
        payload = [assistant.model_dump(by_alias=True) for assistant in assistants]

        return self._api.post(
            f"/v1/vendors/{vendor_str}/assistants",
            VendorAssistantInstallResponse,
            json_data=payload,
            wrap_response=False,
        )

    def uninstall_assistant(
        self,
        vendor: Union[VendorType, str],
        ai_run_id: str,
    ) -> VendorAssistantUninstallResponse:
        """Uninstall/deactivate a vendor assistant.

        Args:
            vendor: Cloud vendor type (aws, azure, gcp). Can be VendorType enum or string.
            ai_run_id: AI run ID returned from the install operation

        Returns:
            VendorAssistantUninstallResponse with success status

        Example:
            >>> # First, install an assistant
            >>> install_request = VendorAssistantInstallRequest(
            ...     id="TJBKR0DGWT",
            ...     agentAliasId="MNULODIW4N",
            ...     setting_id="cac90788-39b7-4ffe-8b57-e8b047fa1f6c"
            ... )
            >>> install_response = client.vendor_assistants.install_assistants(
            ...     vendor=VendorType.AWS,
            ...     assistants=[install_request]
            ... )
            >>> ai_run_id = install_response.summary[0].aiRunId
            >>>
            >>> # Later, uninstall the assistant using the AI run ID
            >>> response = client.vendor_assistants.uninstall_assistant(
            ...     vendor=VendorType.AWS,
            ...     ai_run_id=ai_run_id
            ... )
            >>> if response.success:
            ...     print("Assistant successfully uninstalled!")
        """
        # Convert enum to string value if needed
        vendor_str = vendor.value if isinstance(vendor, VendorType) else vendor

        return self._api.delete(
            f"/v1/vendors/{vendor_str}/assistants/{ai_run_id}",
            VendorAssistantUninstallResponse,
            wrap_response=False,
        )
