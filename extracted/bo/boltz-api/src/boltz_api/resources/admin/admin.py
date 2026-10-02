# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from .usage import (
    UsageResource,
    AsyncUsageResource,
    UsageResourceWithRawResponse,
    AsyncUsageResourceWithRawResponse,
    UsageResourceWithStreamingResponse,
    AsyncUsageResourceWithStreamingResponse,
)
from .api_keys import (
    APIKeysResource,
    AsyncAPIKeysResource,
    APIKeysResourceWithRawResponse,
    AsyncAPIKeysResourceWithRawResponse,
    APIKeysResourceWithStreamingResponse,
    AsyncAPIKeysResourceWithStreamingResponse,
)
from ..._compat import cached_property
from .workspaces import (
    WorkspacesResource,
    AsyncWorkspacesResource,
    WorkspacesResourceWithRawResponse,
    AsyncWorkspacesResourceWithRawResponse,
    WorkspacesResourceWithStreamingResponse,
    AsyncWorkspacesResourceWithStreamingResponse,
)
from ..._resource import SyncAPIResource, AsyncAPIResource

__all__ = ["AdminResource", "AsyncAdminResource"]


class AdminResource(SyncAPIResource):
    """Manage workspaces and API keys.

    Requires an admin API key. Admin keys have full access to all management and compute operations across all workspaces in the organization.
    """

    @cached_property
    def workspaces(self) -> WorkspacesResource:
        """
        Workspaces provide isolated environments for organizing predictions and pipeline runs across teams, projects, or customers. Each workspace has independent data retention settings, can be associated with workspace API keys, and can have a lifetime spending limit for tenant-level budget enforcement. Spending limits use milli-USD and begin tracking usage when first configured. Admin keys can create or change a limit; a workspace key can read the limit for its own workspace.
        """
        return WorkspacesResource(self._client)

    @cached_property
    def api_keys(self) -> APIKeysResource:
        """API keys authenticate requests to the Boltz API.

        There are two key types: admin keys have full access to all management and compute operations across the organization, while workspace keys are scoped to a single workspace and can only perform compute operations (predictions, protein design, small molecule design) within that workspace. Keys can be created in live or test mode. Test keys (prefixed `sk_bc_*_test_`) create test-mode resources with synthetic data and no GPU cost. Every resource includes a `livemode` field indicating its mode.
        """
        return APIKeysResource(self._client)

    @cached_property
    def usage(self) -> UsageResource:
        """Retrieve aggregated usage data for the organization.

        Usage can be grouped by workspace and/or application, and filtered by time range, workspace, and application.
        """
        return UsageResource(self._client)

    @cached_property
    def with_raw_response(self) -> AdminResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/boltz-bio/boltz-api-python#accessing-raw-response-data-eg-headers
        """
        return AdminResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AdminResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/boltz-bio/boltz-api-python#with_streaming_response
        """
        return AdminResourceWithStreamingResponse(self)


class AsyncAdminResource(AsyncAPIResource):
    """Manage workspaces and API keys.

    Requires an admin API key. Admin keys have full access to all management and compute operations across all workspaces in the organization.
    """

    @cached_property
    def workspaces(self) -> AsyncWorkspacesResource:
        """
        Workspaces provide isolated environments for organizing predictions and pipeline runs across teams, projects, or customers. Each workspace has independent data retention settings, can be associated with workspace API keys, and can have a lifetime spending limit for tenant-level budget enforcement. Spending limits use milli-USD and begin tracking usage when first configured. Admin keys can create or change a limit; a workspace key can read the limit for its own workspace.
        """
        return AsyncWorkspacesResource(self._client)

    @cached_property
    def api_keys(self) -> AsyncAPIKeysResource:
        """API keys authenticate requests to the Boltz API.

        There are two key types: admin keys have full access to all management and compute operations across the organization, while workspace keys are scoped to a single workspace and can only perform compute operations (predictions, protein design, small molecule design) within that workspace. Keys can be created in live or test mode. Test keys (prefixed `sk_bc_*_test_`) create test-mode resources with synthetic data and no GPU cost. Every resource includes a `livemode` field indicating its mode.
        """
        return AsyncAPIKeysResource(self._client)

    @cached_property
    def usage(self) -> AsyncUsageResource:
        """Retrieve aggregated usage data for the organization.

        Usage can be grouped by workspace and/or application, and filtered by time range, workspace, and application.
        """
        return AsyncUsageResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncAdminResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/boltz-bio/boltz-api-python#accessing-raw-response-data-eg-headers
        """
        return AsyncAdminResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncAdminResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/boltz-bio/boltz-api-python#with_streaming_response
        """
        return AsyncAdminResourceWithStreamingResponse(self)


class AdminResourceWithRawResponse:
    def __init__(self, admin: AdminResource) -> None:
        self._admin = admin

    @cached_property
    def workspaces(self) -> WorkspacesResourceWithRawResponse:
        """
        Workspaces provide isolated environments for organizing predictions and pipeline runs across teams, projects, or customers. Each workspace has independent data retention settings, can be associated with workspace API keys, and can have a lifetime spending limit for tenant-level budget enforcement. Spending limits use milli-USD and begin tracking usage when first configured. Admin keys can create or change a limit; a workspace key can read the limit for its own workspace.
        """
        return WorkspacesResourceWithRawResponse(self._admin.workspaces)

    @cached_property
    def api_keys(self) -> APIKeysResourceWithRawResponse:
        """API keys authenticate requests to the Boltz API.

        There are two key types: admin keys have full access to all management and compute operations across the organization, while workspace keys are scoped to a single workspace and can only perform compute operations (predictions, protein design, small molecule design) within that workspace. Keys can be created in live or test mode. Test keys (prefixed `sk_bc_*_test_`) create test-mode resources with synthetic data and no GPU cost. Every resource includes a `livemode` field indicating its mode.
        """
        return APIKeysResourceWithRawResponse(self._admin.api_keys)

    @cached_property
    def usage(self) -> UsageResourceWithRawResponse:
        """Retrieve aggregated usage data for the organization.

        Usage can be grouped by workspace and/or application, and filtered by time range, workspace, and application.
        """
        return UsageResourceWithRawResponse(self._admin.usage)


class AsyncAdminResourceWithRawResponse:
    def __init__(self, admin: AsyncAdminResource) -> None:
        self._admin = admin

    @cached_property
    def workspaces(self) -> AsyncWorkspacesResourceWithRawResponse:
        """
        Workspaces provide isolated environments for organizing predictions and pipeline runs across teams, projects, or customers. Each workspace has independent data retention settings, can be associated with workspace API keys, and can have a lifetime spending limit for tenant-level budget enforcement. Spending limits use milli-USD and begin tracking usage when first configured. Admin keys can create or change a limit; a workspace key can read the limit for its own workspace.
        """
        return AsyncWorkspacesResourceWithRawResponse(self._admin.workspaces)

    @cached_property
    def api_keys(self) -> AsyncAPIKeysResourceWithRawResponse:
        """API keys authenticate requests to the Boltz API.

        There are two key types: admin keys have full access to all management and compute operations across the organization, while workspace keys are scoped to a single workspace and can only perform compute operations (predictions, protein design, small molecule design) within that workspace. Keys can be created in live or test mode. Test keys (prefixed `sk_bc_*_test_`) create test-mode resources with synthetic data and no GPU cost. Every resource includes a `livemode` field indicating its mode.
        """
        return AsyncAPIKeysResourceWithRawResponse(self._admin.api_keys)

    @cached_property
    def usage(self) -> AsyncUsageResourceWithRawResponse:
        """Retrieve aggregated usage data for the organization.

        Usage can be grouped by workspace and/or application, and filtered by time range, workspace, and application.
        """
        return AsyncUsageResourceWithRawResponse(self._admin.usage)


class AdminResourceWithStreamingResponse:
    def __init__(self, admin: AdminResource) -> None:
        self._admin = admin

    @cached_property
    def workspaces(self) -> WorkspacesResourceWithStreamingResponse:
        """
        Workspaces provide isolated environments for organizing predictions and pipeline runs across teams, projects, or customers. Each workspace has independent data retention settings, can be associated with workspace API keys, and can have a lifetime spending limit for tenant-level budget enforcement. Spending limits use milli-USD and begin tracking usage when first configured. Admin keys can create or change a limit; a workspace key can read the limit for its own workspace.
        """
        return WorkspacesResourceWithStreamingResponse(self._admin.workspaces)

    @cached_property
    def api_keys(self) -> APIKeysResourceWithStreamingResponse:
        """API keys authenticate requests to the Boltz API.

        There are two key types: admin keys have full access to all management and compute operations across the organization, while workspace keys are scoped to a single workspace and can only perform compute operations (predictions, protein design, small molecule design) within that workspace. Keys can be created in live or test mode. Test keys (prefixed `sk_bc_*_test_`) create test-mode resources with synthetic data and no GPU cost. Every resource includes a `livemode` field indicating its mode.
        """
        return APIKeysResourceWithStreamingResponse(self._admin.api_keys)

    @cached_property
    def usage(self) -> UsageResourceWithStreamingResponse:
        """Retrieve aggregated usage data for the organization.

        Usage can be grouped by workspace and/or application, and filtered by time range, workspace, and application.
        """
        return UsageResourceWithStreamingResponse(self._admin.usage)


class AsyncAdminResourceWithStreamingResponse:
    def __init__(self, admin: AsyncAdminResource) -> None:
        self._admin = admin

    @cached_property
    def workspaces(self) -> AsyncWorkspacesResourceWithStreamingResponse:
        """
        Workspaces provide isolated environments for organizing predictions and pipeline runs across teams, projects, or customers. Each workspace has independent data retention settings, can be associated with workspace API keys, and can have a lifetime spending limit for tenant-level budget enforcement. Spending limits use milli-USD and begin tracking usage when first configured. Admin keys can create or change a limit; a workspace key can read the limit for its own workspace.
        """
        return AsyncWorkspacesResourceWithStreamingResponse(self._admin.workspaces)

    @cached_property
    def api_keys(self) -> AsyncAPIKeysResourceWithStreamingResponse:
        """API keys authenticate requests to the Boltz API.

        There are two key types: admin keys have full access to all management and compute operations across the organization, while workspace keys are scoped to a single workspace and can only perform compute operations (predictions, protein design, small molecule design) within that workspace. Keys can be created in live or test mode. Test keys (prefixed `sk_bc_*_test_`) create test-mode resources with synthetic data and no GPU cost. Every resource includes a `livemode` field indicating its mode.
        """
        return AsyncAPIKeysResourceWithStreamingResponse(self._admin.api_keys)

    @cached_property
    def usage(self) -> AsyncUsageResourceWithStreamingResponse:
        """Retrieve aggregated usage data for the organization.

        Usage can be grouped by workspace and/or application, and filtered by time range, workspace, and application.
        """
        return AsyncUsageResourceWithStreamingResponse(self._admin.usage)
