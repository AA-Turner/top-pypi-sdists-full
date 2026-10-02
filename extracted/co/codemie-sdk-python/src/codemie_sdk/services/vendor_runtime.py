"""Vendor service implementation for managing cloud vendor AgentCore runtimes."""

from typing import Union

from ..models.vendor_assistant import VendorType
from ..models.vendor_runtime import (
    VendorRuntimeSettingsResponse,
    VendorRuntimesResponse,
    VendorRuntime,
    VendorRuntimeEndpointsResponse,
    VendorRuntimeEndpointDetail,
    VendorRuntimeInstallRequest,
    VendorRuntimeInstallResponse,
    VendorRuntimeUninstallResponse,
)
from ..utils import ApiRequestHandler, TokenSource


class VendorRuntimeService:
    """Service for managing cloud vendor AgentCore runtimes (AWS Bedrock)."""

    def __init__(self, api_domain: str, token: TokenSource, verify_ssl: bool = True):
        self._api = ApiRequestHandler(api_domain, token, verify_ssl)

    def get_runtime_settings(
        self,
        vendor: Union[VendorType, str],
        page: int = 0,
        per_page: int = 10,
    ) -> VendorRuntimeSettingsResponse:
        """Get runtime settings for a specific cloud vendor.

        Args:
            vendor: Cloud vendor type (aws, azure, gcp).
            page: Page number for pagination (0-based)
            per_page: Number of items per page

        Returns:
            VendorRuntimeSettingsResponse containing list of settings and pagination info
        """
        vendor_str = vendor.value if isinstance(vendor, VendorType) else vendor
        params = {"page": page, "per_page": per_page}
        return self._api.get(
            f"/v1/vendors/{vendor_str}/agentcore-runtimes/settings",
            VendorRuntimeSettingsResponse,
            params=params,
            wrap_response=False,
        )

    def get_runtimes(
        self,
        vendor: Union[VendorType, str],
        setting_id: str,
        per_page: int = 10,
        next_token: str | None = None,
    ) -> VendorRuntimesResponse:
        """Get runtimes for a specific vendor setting.

        Args:
            vendor: Cloud vendor type.
            setting_id: ID of the vendor setting to retrieve runtimes for
            per_page: Number of items per page
            next_token: Token for pagination (optional, for retrieving next page)

        Returns:
            VendorRuntimesResponse containing list of runtimes and pagination token
        """
        vendor_str = vendor.value if isinstance(vendor, VendorType) else vendor
        params: dict = {"setting_id": setting_id, "per_page": per_page}
        if next_token:
            params["next_token"] = next_token
        return self._api.get(
            f"/v1/vendors/{vendor_str}/agentcore-runtimes",
            VendorRuntimesResponse,
            params=params,
            wrap_response=False,
        )

    def get_runtime(
        self,
        vendor: Union[VendorType, str],
        runtime_id: str,
        setting_id: str,
    ) -> VendorRuntime:
        """Get a specific runtime by ID.

        Args:
            vendor: Cloud vendor type.
            runtime_id: ID of the runtime to retrieve
            setting_id: ID of the vendor setting

        Returns:
            VendorRuntime containing runtime details
        """
        vendor_str = vendor.value if isinstance(vendor, VendorType) else vendor
        params = {"setting_id": setting_id}
        return self._api.get(
            f"/v1/vendors/{vendor_str}/agentcore-runtimes/{runtime_id}",
            VendorRuntime,
            params=params,
            wrap_response=False,
        )

    def get_endpoints(
        self,
        vendor: Union[VendorType, str],
        runtime_id: str,
        setting_id: str,
        per_page: int = 10,
        next_token: str | None = None,
    ) -> VendorRuntimeEndpointsResponse:
        """Get endpoints for a specific runtime.

        Args:
            vendor: Cloud vendor type.
            runtime_id: ID of the runtime whose endpoints to retrieve
            setting_id: ID of the vendor setting
            per_page: Number of items per page
            next_token: Token for pagination (optional)

        Returns:
            VendorRuntimeEndpointsResponse containing list of endpoints and pagination token
        """
        vendor_str = vendor.value if isinstance(vendor, VendorType) else vendor
        params: dict = {"setting_id": setting_id, "per_page": per_page}
        if next_token:
            params["next_token"] = next_token
        return self._api.get(
            f"/v1/vendors/{vendor_str}/agentcore-runtimes/{runtime_id}/endpoints",
            VendorRuntimeEndpointsResponse,
            params=params,
            wrap_response=False,
        )

    def install_endpoints(
        self,
        vendor: Union[VendorType, str],
        endpoints: list[VendorRuntimeInstallRequest],
    ) -> VendorRuntimeInstallResponse:
        """Install one or more vendor AgentCore runtime endpoints into CodeMie.

        Args:
            vendor: Cloud vendor type.
            endpoints: List of endpoint install requests.

        Returns:
            VendorRuntimeInstallResponse with per-endpoint aiRunId summaries.
        """
        vendor_str = vendor.value if isinstance(vendor, VendorType) else vendor
        payload = [e.model_dump(by_alias=True) for e in endpoints]
        return self._api.post(
            f"/v1/vendors/{vendor_str}/agentcore-runtimes",
            VendorRuntimeInstallResponse,
            json_data=payload,
            wrap_response=False,
        )

    def uninstall_endpoint(
        self,
        vendor: Union[VendorType, str],
        ai_run_id: str,
    ) -> VendorRuntimeUninstallResponse:
        """Uninstall a vendor AgentCore runtime endpoint from CodeMie.

        Args:
            vendor: Cloud vendor type.
            ai_run_id: CodeMie assistant ID returned from install.

        Returns:
            VendorRuntimeUninstallResponse with success flag.
        """
        vendor_str = vendor.value if isinstance(vendor, VendorType) else vendor
        return self._api.delete(
            f"/v1/vendors/{vendor_str}/agentcore-runtimes/{ai_run_id}",
            VendorRuntimeUninstallResponse,
            wrap_response=False,
        )

    def get_endpoint(
        self,
        vendor: Union[VendorType, str],
        runtime_id: str,
        endpoint_name: str,
        setting_id: str,
    ) -> VendorRuntimeEndpointDetail:
        """Get detail for a specific runtime endpoint by name.

        Args:
            vendor: Cloud vendor type.
            runtime_id: ID of the runtime that owns the endpoint.
            endpoint_name: Name of the endpoint (route uses name, not ID).
            setting_id: ID of the vendor setting.

        Returns:
            VendorRuntimeEndpointDetail with all list fields plus arn, runtimeArn, failureReason.
        """
        vendor_str = vendor.value if isinstance(vendor, VendorType) else vendor
        params = {"setting_id": setting_id}
        return self._api.get(
            f"/v1/vendors/{vendor_str}/agentcore-runtimes/{runtime_id}/{endpoint_name}",
            VendorRuntimeEndpointDetail,
            params=params,
            wrap_response=False,
        )
