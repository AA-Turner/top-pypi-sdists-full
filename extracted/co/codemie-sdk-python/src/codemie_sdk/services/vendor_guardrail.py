"""Vendor guardrail service implementation for managing cloud vendor guardrail settings."""

from typing import Union

from ..models.vendor_assistant import VendorType
from ..models.vendor_guardrail import (
    VendorGuardrailSettingsResponse,
    VendorGuardrailsResponse,
    VendorGuardrail,
    VendorGuardrailVersion,
    VendorGuardrailVersionsResponse,
    VendorGuardrailInstallRequest,
    VendorGuardrailInstallResponse,
    VendorGuardrailUninstallResponse,
)
from ..utils import ApiRequestHandler, TokenSource


class VendorGuardrailService:
    """Service for managing cloud vendor guardrail settings (AWS, Azure, GCP)."""

    def __init__(self, api_domain: str, token: TokenSource, verify_ssl: bool = True):
        """Initialize the vendor guardrail service.

        Args:
            api_domain: Base URL for the CodeMie API
            token: Authentication token
            verify_ssl: Whether to verify SSL certificates
        """
        self._api = ApiRequestHandler(api_domain, token, verify_ssl)

    def get_guardrail_settings(
        self,
        vendor: Union[VendorType, str],
        page: int = 0,
        per_page: int = 10,
    ) -> VendorGuardrailSettingsResponse:
        """Get guardrail settings for a specific cloud vendor.

        Args:
            vendor: Cloud vendor type (aws, azure, gcp). Can be VendorType enum or string.
            page: Page number for pagination (0-based)
            per_page: Number of items per page

        Returns:
            VendorGuardrailSettingsResponse containing list of settings and pagination info

        Example:
            >>> # Using enum
            >>> settings = client.vendor_guardrails.get_guardrail_settings(VendorType.AWS, page=0, per_page=10)
            >>> # Using string
            >>> settings = client.vendor_guardrails.get_guardrail_settings("aws", page=0, per_page=10)
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
            f"/v1/vendors/{vendor_str}/guardrails/settings",
            VendorGuardrailSettingsResponse,
            params=params,
            wrap_response=False,
        )

    def get_guardrails(
        self,
        vendor: Union[VendorType, str],
        setting_id: str,
        per_page: int = 10,
        next_token: str | None = None,
    ) -> VendorGuardrailsResponse:
        """Get guardrails for a specific vendor setting.

        Args:
            vendor: Cloud vendor type (aws, azure, gcp). Can be VendorType enum or string.
            setting_id: ID of the vendor setting to retrieve guardrails for
            per_page: Number of items per page
            next_token: Token for pagination (optional, for retrieving next page)

        Returns:
            VendorGuardrailsResponse containing list of guardrails and pagination token

        Example:
            >>> # Get first page
            >>> guardrails = client.vendor_guardrails.get_guardrails(
            ...     vendor=VendorType.AWS,
            ...     setting_id="cac90788-39b7-4ffe-8b57-e8b047fa1f6c",
            ...     per_page=8
            ... )
            >>> # Access guardrail data
            >>> for guardrail in guardrails.data:
            ...     print(f"Name: {guardrail.name}, Status: {guardrail.status}")
            ...     print(f"Version: {guardrail.version}, Description: {guardrail.description}")
            >>> # Get next page if available
            >>> if guardrails.pagination.next_token:
            ...     next_page = client.vendor_guardrails.get_guardrails(
            ...         vendor=VendorType.AWS,
            ...         setting_id="cac90788-39b7-4ffe-8b57-e8b047fa1f6c",
            ...         per_page=8,
            ...         next_token=guardrails.pagination.next_token
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
            f"/v1/vendors/{vendor_str}/guardrails",
            VendorGuardrailsResponse,
            params=params,
            wrap_response=False,
        )

    def get_guardrail(
        self,
        vendor: Union[VendorType, str],
        guardrail_id: str,
        setting_id: str,
    ) -> VendorGuardrail:
        """Get a specific guardrail by ID for a vendor setting.

        Args:
            vendor: Cloud vendor type (aws, azure, gcp). Can be VendorType enum or string.
            guardrail_id: ID of the guardrail to retrieve
            setting_id: ID of the vendor setting

        Returns:
            VendorGuardrail containing guardrail details

        Example:
            >>> guardrail = client.vendor_guardrails.get_guardrail(
            ...     vendor=VendorType.AWS,
            ...     guardrail_id="lss9vxro9oxg",
            ...     setting_id="cac90788-39b7-4ffe-8b57-e8b047fa1f6c"
            ... )
            >>> print(f"Name: {guardrail.name}, Status: {guardrail.status}")
            >>> print(f"Version: {guardrail.version}, Description: {guardrail.description}")
        """
        # Convert enum to string value if needed
        vendor_str = vendor.value if isinstance(vendor, VendorType) else vendor

        params = {
            "setting_id": setting_id,
        }

        return self._api.get(
            f"/v1/vendors/{vendor_str}/guardrails/{guardrail_id}",
            VendorGuardrail,
            params=params,
            wrap_response=False,
        )

    def get_guardrail_version(
        self,
        vendor: Union[VendorType, str],
        guardrail_id: str,
        version: str,
        setting_id: str,
    ) -> VendorGuardrailVersion:
        """Get a specific version of a vendor guardrail with detailed information.

        Args:
            vendor: Cloud vendor type (aws, azure, gcp). Can be VendorType enum or string.
            guardrail_id: ID of the guardrail to retrieve
            version: Version number to retrieve (e.g., "1", "2", "DRAFT")
            setting_id: ID of the vendor setting

        Returns:
            VendorGuardrailVersion containing detailed version information including
            blocked messaging settings and timestamps

        Example:
            >>> version_details = client.vendor_guardrails.get_guardrail_version(
            ...     vendor=VendorType.AWS,
            ...     guardrail_id="lss9vxro9oxg",
            ...     version="1",
            ...     setting_id="cac90788-39b7-4ffe-8b57-e8b047fa1f6c"
            ... )
            >>> print(f"Name: {version_details.name}")
            >>> print(f"Version: {version_details.version}")
            >>> print(f"Status: {version_details.status}")
            >>> print(f"Blocked Input Message: {version_details.blockedInputMessaging}")
            >>> print(f"Blocked Output Message: {version_details.blockedOutputsMessaging}")
        """
        # Convert enum to string value if needed
        vendor_str = vendor.value if isinstance(vendor, VendorType) else vendor

        params = {
            "setting_id": setting_id,
        }

        return self._api.get(
            f"/v1/vendors/{vendor_str}/guardrails/{guardrail_id}/{version}",
            VendorGuardrailVersion,
            params=params,
            wrap_response=False,
        )

    def get_guardrail_versions(
        self,
        vendor: Union[VendorType, str],
        guardrail_id: str,
        setting_id: str,
        per_page: int = 10,
        next_token: str | None = None,
    ) -> VendorGuardrailVersionsResponse:
        """Get versions for a specific vendor guardrail.

        Args:
            vendor: Cloud vendor type (aws, azure, gcp). Can be VendorType enum or string.
            guardrail_id: ID of the guardrail to retrieve versions for
            setting_id: ID of the vendor setting
            per_page: Number of items per page
            next_token: Token for pagination (optional, for retrieving next page)

        Returns:
            VendorGuardrailVersionsResponse containing list of versions and pagination token

        Example:
            >>> # Get first page of versions
            >>> versions = client.vendor_guardrails.get_guardrail_versions(
            ...     vendor=VendorType.AWS,
            ...     guardrail_id="lss9vxro9oxg",
            ...     setting_id="cac90788-39b7-4ffe-8b57-e8b047fa1f6c",
            ...     per_page=5
            ... )
            >>> for version in versions.data:
            ...     print(f"{version.name} (v{version.version}): {version.status}")
            >>> # Get next page if available
            >>> if versions.pagination.next_token:
            ...     next_page = client.vendor_guardrails.get_guardrail_versions(
            ...         vendor=VendorType.AWS,
            ...         guardrail_id="lss9vxro9oxg",
            ...         setting_id="cac90788-39b7-4ffe-8b57-e8b047fa1f6c",
            ...         per_page=5,
            ...         next_token=versions.pagination.next_token
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
            f"/v1/vendors/{vendor_str}/guardrails/{guardrail_id}/versions",
            VendorGuardrailVersionsResponse,
            params=params,
            wrap_response=False,
        )

    def install_guardrails(
        self,
        vendor: Union[VendorType, str],
        guardrails: list[VendorGuardrailInstallRequest],
    ) -> VendorGuardrailInstallResponse:
        """Install/activate vendor guardrails.

        Args:
            vendor: Cloud vendor type (aws, azure, gcp). Can be VendorType enum or string.
            guardrails: List of guardrail installation requests with guardrail ID, version, and setting ID

        Returns:
            VendorGuardrailInstallResponse containing installation summary with AI run IDs

        Example:
            >>> from codemie_sdk import VendorGuardrailInstallRequest
            >>> # Install single guardrail
            >>> install_request = VendorGuardrailInstallRequest(
            ...     id="lss9vxro9oxg",
            ...     version="1",
            ...     setting_id="cac90788-39b7-4ffe-8b57-e8b047fa1f6c"
            ... )
            >>> response = client.vendor_guardrails.install_guardrails(
            ...     vendor=VendorType.AWS,
            ...     guardrails=[install_request]
            ... )
            >>> for item in response.summary:
            ...     print(f"Installed {item.guardrailId} version {item.version} with run ID: {item.aiRunId}")
            >>>
            >>> # Install multiple guardrails
            >>> requests = [
            ...     VendorGuardrailInstallRequest(
            ...         id="GUARDRAIL_ID_1",
            ...         version="1",
            ...         setting_id="SETTING_ID"
            ...     ),
            ...     VendorGuardrailInstallRequest(
            ...         id="GUARDRAIL_ID_2",
            ...         version="2",
            ...         setting_id="SETTING_ID"
            ...     )
            ... ]
            >>> response = client.vendor_guardrails.install_guardrails(
            ...     vendor=VendorType.AWS,
            ...     guardrails=requests
            ... )
        """
        # Convert enum to string value if needed
        vendor_str = vendor.value if isinstance(vendor, VendorType) else vendor

        # Convert list of Pydantic models to list of dicts
        payload = [guardrail.model_dump(by_alias=True) for guardrail in guardrails]

        return self._api.post(
            f"/v1/vendors/{vendor_str}/guardrails",
            VendorGuardrailInstallResponse,
            json_data=payload,
            wrap_response=False,
        )

    def uninstall_guardrail(
        self,
        vendor: Union[VendorType, str],
        ai_run_id: str,
    ) -> VendorGuardrailUninstallResponse:
        """Uninstall/deactivate a vendor guardrail.

        Args:
            vendor: Cloud vendor type (aws, azure, gcp). Can be VendorType enum or string.
            ai_run_id: AI run ID returned from the install operation

        Returns:
            VendorGuardrailUninstallResponse with success status

        Example:
            >>> # First, install a guardrail
            >>> install_request = VendorGuardrailInstallRequest(
            ...     id="lss9vxro9oxg",
            ...     version="1",
            ...     setting_id="cac90788-39b7-4ffe-8b57-e8b047fa1f6c"
            ... )
            >>> install_response = client.vendor_guardrails.install_guardrails(
            ...     vendor=VendorType.AWS,
            ...     guardrails=[install_request]
            ... )
            >>> ai_run_id = install_response.summary[0].aiRunId
            >>>
            >>> # Later, uninstall the guardrail using the AI run ID
            >>> response = client.vendor_guardrails.uninstall_guardrail(
            ...     vendor=VendorType.AWS,
            ...     ai_run_id=ai_run_id
            ... )
            >>> if response.success:
            ...     print("Guardrail successfully uninstalled!")
        """
        # Convert enum to string value if needed
        vendor_str = vendor.value if isinstance(vendor, VendorType) else vendor

        return self._api.delete(
            f"/v1/vendors/{vendor_str}/guardrails/{ai_run_id}",
            VendorGuardrailUninstallResponse,
            wrap_response=False,
        )
