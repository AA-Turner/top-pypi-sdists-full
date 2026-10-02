"""Vendor workflow service implementation for managing cloud vendor workflow settings."""

from typing import Union

from ..models.vendor_assistant import VendorType
from ..models.vendor_workflow import (
    VendorWorkflowSettingsResponse,
    VendorWorkflowsResponse,
    VendorWorkflow,
    VendorWorkflowAliasesResponse,
    VendorWorkflowInstallRequest,
    VendorWorkflowInstallResponse,
    VendorWorkflowUninstallResponse,
)
from ..utils import ApiRequestHandler, TokenSource


class VendorWorkflowService:
    """Service for managing cloud vendor workflow settings (AWS, Azure, GCP)."""

    def __init__(self, api_domain: str, token: TokenSource, verify_ssl: bool = True):
        """Initialize the vendor workflow service.

        Args:
            api_domain: Base URL for the CodeMie API
            token: Authentication token
            verify_ssl: Whether to verify SSL certificates
        """
        self._api = ApiRequestHandler(api_domain, token, verify_ssl)

    def get_workflow_settings(
        self,
        vendor: Union[VendorType, str],
        page: int = 0,
        per_page: int = 10,
    ) -> VendorWorkflowSettingsResponse:
        """Get workflow settings for a specific cloud vendor.

        Args:
            vendor: Cloud vendor type (aws, azure, gcp). Can be VendorType enum or string.
            page: Page number for pagination (0-based)
            per_page: Number of items per page

        Returns:
            VendorWorkflowSettingsResponse containing list of settings and pagination info

        Example:
            >>> # Using enum
            >>> settings = client.vendor_workflows.get_workflow_settings(VendorType.AWS, page=0, per_page=10)
            >>> # Using string
            >>> settings = client.vendor_workflows.get_workflow_settings("aws", page=0, per_page=10)
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
            f"/v1/vendors/{vendor_str}/workflows/settings",
            VendorWorkflowSettingsResponse,
            params=params,
            wrap_response=False,
        )

    def get_workflows(
        self,
        vendor: Union[VendorType, str],
        setting_id: str,
        per_page: int = 10,
        next_token: str | None = None,
    ) -> VendorWorkflowsResponse:
        """Get workflows for a specific vendor setting.

        Args:
            vendor: Cloud vendor type (aws, azure, gcp). Can be VendorType enum or string.
            setting_id: ID of the vendor setting to retrieve workflows for
            per_page: Number of items per page
            next_token: Token for pagination (optional, for retrieving next page)

        Returns:
            VendorWorkflowsResponse containing list of workflows and pagination token

        Example:
            >>> # Get first page
            >>> workflows = client.vendor_workflows.get_workflows(
            ...     vendor=VendorType.AWS,
            ...     setting_id="cac90788-39b7-4ffe-8b57-e8b047fa1f6c",
            ...     per_page=8
            ... )
            >>> # Access workflow data
            >>> for workflow in workflows.data:
            ...     print(f"Name: {workflow.name}, Status: {workflow.status}")
            ...     print(f"Version: {workflow.version}, Description: {workflow.description}")
            >>> # Get next page if available
            >>> if workflows.pagination.next_token:
            ...     next_page = client.vendor_workflows.get_workflows(
            ...         vendor=VendorType.AWS,
            ...         setting_id="cac90788-39b7-4ffe-8b57-e8b047fa1f6c",
            ...         per_page=8,
            ...         next_token=workflows.pagination.next_token
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
            f"/v1/vendors/{vendor_str}/workflows",
            VendorWorkflowsResponse,
            params=params,
            wrap_response=False,
        )

    def get_workflow(
        self,
        vendor: Union[VendorType, str],
        workflow_id: str,
        setting_id: str,
    ) -> VendorWorkflow:
        """Get a specific workflow by ID for a vendor setting.

        Args:
            vendor: Cloud vendor type (aws, azure, gcp). Can be VendorType enum or string.
            workflow_id: ID of the workflow to retrieve
            setting_id: ID of the vendor setting

        Returns:
            VendorWorkflow containing workflow details

        Example:
            >>> workflow = client.vendor_workflows.get_workflow(
            ...     vendor=VendorType.AWS,
            ...     workflow_id="9HXLQ7J9YP",
            ...     setting_id="cac90788-39b7-4ffe-8b57-e8b047fa1f6c"
            ... )
            >>> print(f"Name: {workflow.name}, Status: {workflow.status}")
            >>> print(f"Version: {workflow.version}, Description: {workflow.description}")
        """
        # Convert enum to string value if needed
        vendor_str = vendor.value if isinstance(vendor, VendorType) else vendor

        params = {
            "setting_id": setting_id,
        }

        return self._api.get(
            f"/v1/vendors/{vendor_str}/workflows/{workflow_id}",
            VendorWorkflow,
            params=params,
            wrap_response=False,
        )

    def get_workflow_aliases(
        self,
        vendor: Union[VendorType, str],
        workflow_id: str,
        setting_id: str,
        per_page: int = 10,
        next_token: str | None = None,
    ) -> VendorWorkflowAliasesResponse:
        """Get aliases for a specific vendor workflow.

        Args:
            vendor: Cloud vendor type (aws, azure, gcp). Can be VendorType enum or string.
            workflow_id: ID of the workflow to retrieve aliases for
            setting_id: ID of the vendor setting
            per_page: Number of items per page
            next_token: Token for pagination (optional, for retrieving next page)

        Returns:
            VendorWorkflowAliasesResponse containing list of aliases and pagination token

        Example:
            >>> # Get first page of aliases
            >>> aliases = client.vendor_workflows.get_workflow_aliases(
            ...     vendor=VendorType.AWS,
            ...     workflow_id="9HXLQ7J9YP",
            ...     setting_id="cac90788-39b7-4ffe-8b57-e8b047fa1f6c",
            ...     per_page=5
            ... )
            >>> for alias in aliases.data:
            ...     print(f"{alias.name} (v{alias.version}): {alias.status}")
            ...     if alias.aiRunId:
            ...         print(f"  AI Run ID: {alias.aiRunId}")
            >>> # Get next page if available
            >>> if aliases.pagination.next_token:
            ...     next_page = client.vendor_workflows.get_workflow_aliases(
            ...         vendor=VendorType.AWS,
            ...         workflow_id="9HXLQ7J9YP",
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
            f"/v1/vendors/{vendor_str}/workflows/{workflow_id}/aliases",
            VendorWorkflowAliasesResponse,
            params=params,
            wrap_response=False,
        )

    def install_workflows(
        self,
        vendor: Union[VendorType, str],
        workflows: list[VendorWorkflowInstallRequest],
    ) -> VendorWorkflowInstallResponse:
        """Install/activate vendor workflows.

        Args:
            vendor: Cloud vendor type (aws, azure, gcp). Can be VendorType enum or string.
            workflows: List of workflow installation requests with workflow ID, flow alias ID, and setting ID

        Returns:
            VendorWorkflowInstallResponse containing installation summary with AI run IDs

        Example:
            >>> from codemie_sdk import VendorWorkflowInstallRequest
            >>> # Install single workflow
            >>> install_request = VendorWorkflowInstallRequest(
            ...     id="9HXLQ7J9YP",
            ...     flowAliasId="9RUV0BI2L7",
            ...     setting_id="cac90788-39b7-4ffe-8b57-e8b047fa1f6c"
            ... )
            >>> response = client.vendor_workflows.install_workflows(
            ...     vendor=VendorType.AWS,
            ...     workflows=[install_request]
            ... )
            >>> for item in response.summary:
            ...     print(f"Installed workflow {item.flowId} with run ID: {item.aiRunId}")
            >>>
            >>> # Install multiple workflows
            >>> requests = [
            ...     VendorWorkflowInstallRequest(
            ...         id="WORKFLOW_ID_1",
            ...         flowAliasId="ALIAS_ID_1",
            ...         setting_id="SETTING_ID"
            ...     ),
            ...     VendorWorkflowInstallRequest(
            ...         id="WORKFLOW_ID_2",
            ...         flowAliasId="ALIAS_ID_2",
            ...         setting_id="SETTING_ID"
            ...     )
            ... ]
            >>> response = client.vendor_workflows.install_workflows(
            ...     vendor=VendorType.AWS,
            ...     workflows=requests
            ... )
        """
        # Convert enum to string value if needed
        vendor_str = vendor.value if isinstance(vendor, VendorType) else vendor

        # Convert list of Pydantic models to list of dicts
        payload = [workflow.model_dump(by_alias=True) for workflow in workflows]

        return self._api.post(
            f"/v1/vendors/{vendor_str}/workflows",
            VendorWorkflowInstallResponse,
            json_data=payload,
            wrap_response=False,
        )

    def uninstall_workflow(
        self,
        vendor: Union[VendorType, str],
        ai_run_id: str,
    ) -> VendorWorkflowUninstallResponse:
        """Uninstall/deactivate a vendor workflow.

        Args:
            vendor: Cloud vendor type (aws, azure, gcp). Can be VendorType enum or string.
            ai_run_id: AI run ID returned from the workflow alias (aiRunId field)

        Returns:
            VendorWorkflowUninstallResponse with success status

        Example:
            >>> # Get workflow aliases to find the aiRunId
            >>> aliases = client.vendor_workflows.get_workflow_aliases(
            ...     vendor=VendorType.AWS,
            ...     workflow_id="9HXLQ7J9YP",
            ...     setting_id="cac90788-39b7-4ffe-8b57-e8b047fa1f6c"
            ... )
            >>> # Find an installed alias with aiRunId
            >>> for alias in aliases.data:
            ...     if alias.aiRunId:
            ...         ai_run_id = alias.aiRunId
            ...         break
            >>>
            >>> # Uninstall the workflow using the AI run ID
            >>> response = client.vendor_workflows.uninstall_workflow(
            ...     vendor=VendorType.AWS,
            ...     ai_run_id="56fed66d-f66e-46e3-b420-bb3a8d93eed4"
            ... )
            >>> if response.success:
            ...     print("Workflow successfully uninstalled!")
        """
        # Convert enum to string value if needed
        vendor_str = vendor.value if isinstance(vendor, VendorType) else vendor

        return self._api.delete(
            f"/v1/vendors/{vendor_str}/workflows/{ai_run_id}",
            VendorWorkflowUninstallResponse,
            wrap_response=False,
        )
