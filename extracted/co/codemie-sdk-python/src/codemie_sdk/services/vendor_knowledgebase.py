"""Vendor knowledge base service implementation for managing cloud vendor knowledge base settings."""

from typing import Union

from ..models.vendor_assistant import VendorType
from ..models.vendor_knowledgebase import (
    VendorKnowledgeBaseSettingsResponse,
    VendorKnowledgeBasesResponse,
    VendorKnowledgeBaseDetail,
    VendorKnowledgeBaseInstallRequest,
    VendorKnowledgeBaseInstallResponse,
    VendorKnowledgeBaseUninstallResponse,
)
from ..utils import ApiRequestHandler, TokenSource


class VendorKnowledgeBaseService:
    """Service for managing cloud vendor knowledge base settings (AWS, Azure, GCP)."""

    def __init__(self, api_domain: str, token: TokenSource, verify_ssl: bool = True):
        """Initialize the vendor knowledge base service.

        Args:
            api_domain: Base URL for the CodeMie API
            token: Authentication token
            verify_ssl: Whether to verify SSL certificates
        """
        self._api = ApiRequestHandler(api_domain, token, verify_ssl)

    def get_knowledgebase_settings(
        self,
        vendor: Union[VendorType, str],
        page: int = 0,
        per_page: int = 10,
    ) -> VendorKnowledgeBaseSettingsResponse:
        """Get knowledge base settings for a specific cloud vendor.

        Args:
            vendor: Cloud vendor type (aws, azure, gcp). Can be VendorType enum or string.
            page: Page number for pagination (0-based)
            per_page: Number of items per page

        Returns:
            VendorKnowledgeBaseSettingsResponse containing list of settings and pagination info

        Example:
            >>> # Using enum
            >>> settings = client.vendor_knowledgebases.get_knowledgebase_settings(VendorType.AWS, page=0, per_page=10)
            >>> # Using string
            >>> settings = client.vendor_knowledgebases.get_knowledgebase_settings("aws", page=0, per_page=10)
            >>> # Access settings data
            >>> for setting in settings.data:
            ...     print(f"Setting: {setting.setting_name}, Project: {setting.project}")
            ...     if setting.invalid:
            ...         print(f"Error: {setting.error}")
        """
        # Convert enum to string value if needed
        vendor_str = vendor.value if isinstance(vendor, VendorType) else vendor

        params = {
            "page": page,
            "per_page": per_page,
        }

        return self._api.get(
            f"/v1/vendors/{vendor_str}/knowledgebases/settings",
            VendorKnowledgeBaseSettingsResponse,
            params=params,
            wrap_response=False,
        )

    def get_knowledgebases(
        self,
        vendor: Union[VendorType, str],
        setting_id: str,
        per_page: int = 10,
        next_token: str | None = None,
    ) -> VendorKnowledgeBasesResponse:
        """Get knowledge bases for a specific vendor setting.

        Args:
            vendor: Cloud vendor type (aws, azure, gcp). Can be VendorType enum or string.
            setting_id: ID of the vendor setting to retrieve knowledge bases for
            per_page: Number of items per page
            next_token: Token for pagination (optional, for retrieving next page)

        Returns:
            VendorKnowledgeBasesResponse containing list of knowledge bases and pagination token

        Example:
            >>> # Get first page
            >>> kbs = client.vendor_knowledgebases.get_knowledgebases(
            ...     vendor=VendorType.AWS,
            ...     setting_id="cac90788-39b7-4ffe-8b57-e8b047fa1f6c",
            ...     per_page=8
            ... )
            >>> # Access knowledge base data
            >>> for kb in kbs.data:
            ...     print(f"Name: {kb.name}, Status: {kb.status}")
            ...     if kb.aiRunId:
            ...         print(f"  AI Run ID: {kb.aiRunId}")
            >>> # Get next page if available
            >>> if kbs.pagination.next_token:
            ...     next_page = client.vendor_knowledgebases.get_knowledgebases(
            ...         vendor=VendorType.AWS,
            ...         setting_id="cac90788-39b7-4ffe-8b57-e8b047fa1f6c",
            ...         per_page=8,
            ...         next_token=kbs.pagination.next_token
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
            f"/v1/vendors/{vendor_str}/knowledgebases",
            VendorKnowledgeBasesResponse,
            params=params,
            wrap_response=False,
        )

    def get_knowledgebase(
        self,
        vendor: Union[VendorType, str],
        knowledgebase_id: str,
        setting_id: str,
    ) -> VendorKnowledgeBaseDetail:
        """Get detailed information about a specific knowledge base by ID.

        Args:
            vendor: Cloud vendor type (aws, azure, gcp). Can be VendorType enum or string.
            knowledgebase_id: ID of the knowledge base to retrieve
            setting_id: ID of the vendor setting

        Returns:
            VendorKnowledgeBaseDetail containing detailed knowledge base information

        Example:
            >>> kb = client.vendor_knowledgebases.get_knowledgebase(
            ...     vendor=VendorType.AWS,
            ...     knowledgebase_id="HIKPIQ2FMT",
            ...     setting_id="cac90788-39b7-4ffe-8b57-e8b047fa1f6c"
            ... )
            >>> print(f"Name: {kb.name}")
            >>> print(f"Type: {kb.type}")
            >>> print(f"Status: {kb.status}")
            >>> print(f"Embedding Model: {kb.embeddingModel}")
            >>> if kb.aiRunId:
            ...     print(f"AI Run ID: {kb.aiRunId}")
        """
        # Convert enum to string value if needed
        vendor_str = vendor.value if isinstance(vendor, VendorType) else vendor

        params = {
            "setting_id": setting_id,
        }

        return self._api.get(
            f"/v1/vendors/{vendor_str}/knowledgebases/{knowledgebase_id}",
            VendorKnowledgeBaseDetail,
            params=params,
            wrap_response=False,
        )

    def install_knowledgebases(
        self,
        vendor: Union[VendorType, str],
        knowledgebases: list[VendorKnowledgeBaseInstallRequest],
    ) -> VendorKnowledgeBaseInstallResponse:
        """Install/activate vendor knowledge bases.

        Args:
            vendor: Cloud vendor type (aws, azure, gcp). Can be VendorType enum or string.
            knowledgebases: List of knowledge base installation requests with knowledge base ID and setting ID

        Returns:
            VendorKnowledgeBaseInstallResponse containing installation summary with AI run IDs

        Example:
            >>> from codemie_sdk import VendorKnowledgeBaseInstallRequest
            >>> # Install single knowledge base
            >>> install_request = VendorKnowledgeBaseInstallRequest(
            ...     id="HIKPIQ2FMT",
            ...     setting_id="cac90788-39b7-4ffe-8b57-e8b047fa1f6c"
            ... )
            >>> response = client.vendor_knowledgebases.install_knowledgebases(
            ...     vendor=VendorType.AWS,
            ...     knowledgebases=[install_request]
            ... )
            >>> for item in response.summary:
            ...     print(f"Installed knowledge base {item.knowledgeBaseId} with run ID: {item.aiRunId}")
            >>>
            >>> # Install multiple knowledge bases
            >>> requests = [
            ...     VendorKnowledgeBaseInstallRequest(
            ...         id="KB_ID_1",
            ...         setting_id="SETTING_ID"
            ...     ),
            ...     VendorKnowledgeBaseInstallRequest(
            ...         id="KB_ID_2",
            ...         setting_id="SETTING_ID"
            ...     )
            ... ]
            >>> response = client.vendor_knowledgebases.install_knowledgebases(
            ...     vendor=VendorType.AWS,
            ...     knowledgebases=requests
            ... )
        """
        # Convert enum to string value if needed
        vendor_str = vendor.value if isinstance(vendor, VendorType) else vendor

        # Convert list of Pydantic models to list of dicts
        payload = [kb.model_dump(by_alias=True) for kb in knowledgebases]

        return self._api.post(
            f"/v1/vendors/{vendor_str}/knowledgebases",
            VendorKnowledgeBaseInstallResponse,
            json_data=payload,
            wrap_response=False,
        )

    def uninstall_knowledgebase(
        self,
        vendor: Union[VendorType, str],
        ai_run_id: str,
    ) -> VendorKnowledgeBaseUninstallResponse:
        """Uninstall/deactivate a vendor knowledge base.

        Args:
            vendor: Cloud vendor type (aws, azure, gcp). Can be VendorType enum or string.
            ai_run_id: AI run ID returned from the knowledge base (aiRunId field)

        Returns:
            VendorKnowledgeBaseUninstallResponse with success status

        Example:
            >>> # Get knowledge bases to find the aiRunId
            >>> kbs = client.vendor_knowledgebases.get_knowledgebases(
            ...     vendor=VendorType.AWS,
            ...     setting_id="cac90788-39b7-4ffe-8b57-e8b047fa1f6c"
            ... )
            >>> # Find an installed knowledge base with aiRunId
            >>> for kb in kbs.data:
            ...     if kb.aiRunId:
            ...         ai_run_id = kb.aiRunId
            ...         break
            >>>
            >>> # Uninstall the knowledge base using the AI run ID
            >>> response = client.vendor_knowledgebases.uninstall_knowledgebase(
            ...     vendor=VendorType.AWS,
            ...     ai_run_id="2364feec-f8c7-4db8-a8b4-ea56289e67a4"
            ... )
            >>> if response.success:
            ...     print("Knowledge base successfully uninstalled!")
        """
        # Convert enum to string value if needed
        vendor_str = vendor.value if isinstance(vendor, VendorType) else vendor

        return self._api.delete(
            f"/v1/vendors/{vendor_str}/knowledgebases/{ai_run_id}",
            VendorKnowledgeBaseUninstallResponse,
            wrap_response=False,
        )
