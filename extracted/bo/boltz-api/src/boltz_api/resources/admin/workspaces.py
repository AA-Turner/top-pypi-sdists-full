# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Literal

import httpx

from ..._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from ..._utils import path_template, maybe_transform, async_maybe_transform
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ...pagination import SyncCursorPage, AsyncCursorPage
from ...types.admin import (
    workspace_list_params,
    workspace_create_params,
    workspace_update_params,
    workspace_set_spending_limit_params,
)
from ..._base_client import AsyncPaginator, make_request_options
from ...types.admin.workspace_list_response import WorkspaceListResponse
from ...types.admin.workspace_create_response import WorkspaceCreateResponse
from ...types.admin.workspace_update_response import WorkspaceUpdateResponse
from ...types.admin.workspace_archive_response import WorkspaceArchiveResponse
from ...types.admin.workspace_retrieve_response import WorkspaceRetrieveResponse
from ...types.admin.workspace_set_spending_limit_response import WorkspaceSetSpendingLimitResponse
from ...types.admin.workspace_retrieve_spending_limit_response import WorkspaceRetrieveSpendingLimitResponse

__all__ = ["WorkspacesResource", "AsyncWorkspacesResource"]


class WorkspacesResource(SyncAPIResource):
    """
    Workspaces provide isolated environments for organizing predictions and pipeline runs across teams, projects, or customers. Each workspace has independent data retention settings, can be associated with workspace API keys, and can have a lifetime spending limit for tenant-level budget enforcement. Spending limits use milli-USD and begin tracking usage when first configured. Admin keys can create or change a limit; a workspace key can read the limit for its own workspace.
    """

    @cached_property
    def with_raw_response(self) -> WorkspacesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/boltz-bio/boltz-api-python#accessing-raw-response-data-eg-headers
        """
        return WorkspacesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> WorkspacesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/boltz-bio/boltz-api-python#with_streaming_response
        """
        return WorkspacesResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        data_retention: workspace_create_params.DataRetention | Omit = omit,
        name: str | Omit = omit,
        spending_limit: workspace_create_params.SpendingLimit | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> WorkspaceCreateResponse:
        """
        Create a workspace

        Args:
          data_retention: How long result data is retained before automatic deletion. Defaults to 7 days
              if not specified. Maximum retention is 14 days (336 hours).

          name: Workspace name

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/compute/v1/admin/workspaces",
            body=maybe_transform(
                {
                    "data_retention": data_retention,
                    "name": name,
                    "spending_limit": spending_limit,
                },
                workspace_create_params.WorkspaceCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=WorkspaceCreateResponse,
        )

    def retrieve(
        self,
        workspace_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> WorkspaceRetrieveResponse:
        """
        Get a workspace

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not workspace_id:
            raise ValueError(f"Expected a non-empty value for `workspace_id` but received {workspace_id!r}")
        return self._get(
            path_template("/compute/v1/admin/workspaces/{workspace_id}", workspace_id=workspace_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=WorkspaceRetrieveResponse,
        )

    def update(
        self,
        workspace_id: str,
        *,
        data_retention: workspace_update_params.DataRetention | Omit = omit,
        name: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> WorkspaceUpdateResponse:
        """
        Update a workspace

        Args:
          data_retention: How long result data is retained before automatic deletion. Defaults to 7 days
              if not specified. Maximum retention is 14 days (336 hours).

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not workspace_id:
            raise ValueError(f"Expected a non-empty value for `workspace_id` but received {workspace_id!r}")
        return self._post(
            path_template("/compute/v1/admin/workspaces/{workspace_id}", workspace_id=workspace_id),
            body=maybe_transform(
                {
                    "data_retention": data_retention,
                    "name": name,
                },
                workspace_update_params.WorkspaceUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=WorkspaceUpdateResponse,
        )

    def list(
        self,
        *,
        after_id: str | Omit = omit,
        before_id: str | Omit = omit,
        limit: int | Omit = omit,
        name: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SyncCursorPage[WorkspaceListResponse]:
        """
        List workspaces

        Args:
          after_id: Return results after this ID

          before_id: Return results before this ID

          limit: Max items to return

          name: Case-insensitive workspace name prefix to filter by

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/compute/v1/admin/workspaces",
            page=SyncCursorPage[WorkspaceListResponse],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "after_id": after_id,
                        "before_id": before_id,
                        "limit": limit,
                        "name": name,
                    },
                    workspace_list_params.WorkspaceListParams,
                ),
            ),
            model=WorkspaceListResponse,
        )

    def archive(
        self,
        workspace_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> WorkspaceArchiveResponse:
        """Archives a workspace and deactivates all its API keys.

        This action is
        irreversible.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not workspace_id:
            raise ValueError(f"Expected a non-empty value for `workspace_id` but received {workspace_id!r}")
        return self._post(
            path_template("/compute/v1/admin/workspaces/{workspace_id}/archive", workspace_id=workspace_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=WorkspaceArchiveResponse,
        )

    def retrieve_spending_limit(
        self,
        workspace_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Optional[WorkspaceRetrieveSpendingLimitResponse]:
        """
        Return the lifetime spending limit and accrued usage for a workspace, or null
        when no workspace-level limit is configured. Admin API keys can read any
        workspace in their organization; a workspace key can read its own limit.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not workspace_id:
            raise ValueError(f"Expected a non-empty value for `workspace_id` but received {workspace_id!r}")
        return self._get(
            path_template("/compute/v1/admin/workspaces/{workspace_id}/spending-limit", workspace_id=workspace_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=WorkspaceRetrieveSpendingLimitResponse,
        )

    def set_spending_limit(
        self,
        workspace_id: str,
        *,
        limit: workspace_set_spending_limit_params.Limit,
        type: Literal["lifetime"],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Optional[WorkspaceSetSpendingLimitResponse]:
        """
        Create or replace the absolute lifetime spending ceiling for a workspace.
        Tracking starts when the limit is first configured. The new limit cannot be
        lower than accrued usage plus spend reserved by active work. Requires an admin
        API key.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not workspace_id:
            raise ValueError(f"Expected a non-empty value for `workspace_id` but received {workspace_id!r}")
        return self._put(
            path_template("/compute/v1/admin/workspaces/{workspace_id}/spending-limit", workspace_id=workspace_id),
            body=maybe_transform(
                {
                    "limit": limit,
                    "type": type,
                },
                workspace_set_spending_limit_params.WorkspaceSetSpendingLimitParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=WorkspaceSetSpendingLimitResponse,
        )


class AsyncWorkspacesResource(AsyncAPIResource):
    """
    Workspaces provide isolated environments for organizing predictions and pipeline runs across teams, projects, or customers. Each workspace has independent data retention settings, can be associated with workspace API keys, and can have a lifetime spending limit for tenant-level budget enforcement. Spending limits use milli-USD and begin tracking usage when first configured. Admin keys can create or change a limit; a workspace key can read the limit for its own workspace.
    """

    @cached_property
    def with_raw_response(self) -> AsyncWorkspacesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/boltz-bio/boltz-api-python#accessing-raw-response-data-eg-headers
        """
        return AsyncWorkspacesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncWorkspacesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/boltz-bio/boltz-api-python#with_streaming_response
        """
        return AsyncWorkspacesResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        data_retention: workspace_create_params.DataRetention | Omit = omit,
        name: str | Omit = omit,
        spending_limit: workspace_create_params.SpendingLimit | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> WorkspaceCreateResponse:
        """
        Create a workspace

        Args:
          data_retention: How long result data is retained before automatic deletion. Defaults to 7 days
              if not specified. Maximum retention is 14 days (336 hours).

          name: Workspace name

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/compute/v1/admin/workspaces",
            body=await async_maybe_transform(
                {
                    "data_retention": data_retention,
                    "name": name,
                    "spending_limit": spending_limit,
                },
                workspace_create_params.WorkspaceCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=WorkspaceCreateResponse,
        )

    async def retrieve(
        self,
        workspace_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> WorkspaceRetrieveResponse:
        """
        Get a workspace

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not workspace_id:
            raise ValueError(f"Expected a non-empty value for `workspace_id` but received {workspace_id!r}")
        return await self._get(
            path_template("/compute/v1/admin/workspaces/{workspace_id}", workspace_id=workspace_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=WorkspaceRetrieveResponse,
        )

    async def update(
        self,
        workspace_id: str,
        *,
        data_retention: workspace_update_params.DataRetention | Omit = omit,
        name: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> WorkspaceUpdateResponse:
        """
        Update a workspace

        Args:
          data_retention: How long result data is retained before automatic deletion. Defaults to 7 days
              if not specified. Maximum retention is 14 days (336 hours).

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not workspace_id:
            raise ValueError(f"Expected a non-empty value for `workspace_id` but received {workspace_id!r}")
        return await self._post(
            path_template("/compute/v1/admin/workspaces/{workspace_id}", workspace_id=workspace_id),
            body=await async_maybe_transform(
                {
                    "data_retention": data_retention,
                    "name": name,
                },
                workspace_update_params.WorkspaceUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=WorkspaceUpdateResponse,
        )

    def list(
        self,
        *,
        after_id: str | Omit = omit,
        before_id: str | Omit = omit,
        limit: int | Omit = omit,
        name: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[WorkspaceListResponse, AsyncCursorPage[WorkspaceListResponse]]:
        """
        List workspaces

        Args:
          after_id: Return results after this ID

          before_id: Return results before this ID

          limit: Max items to return

          name: Case-insensitive workspace name prefix to filter by

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/compute/v1/admin/workspaces",
            page=AsyncCursorPage[WorkspaceListResponse],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "after_id": after_id,
                        "before_id": before_id,
                        "limit": limit,
                        "name": name,
                    },
                    workspace_list_params.WorkspaceListParams,
                ),
            ),
            model=WorkspaceListResponse,
        )

    async def archive(
        self,
        workspace_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> WorkspaceArchiveResponse:
        """Archives a workspace and deactivates all its API keys.

        This action is
        irreversible.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not workspace_id:
            raise ValueError(f"Expected a non-empty value for `workspace_id` but received {workspace_id!r}")
        return await self._post(
            path_template("/compute/v1/admin/workspaces/{workspace_id}/archive", workspace_id=workspace_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=WorkspaceArchiveResponse,
        )

    async def retrieve_spending_limit(
        self,
        workspace_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Optional[WorkspaceRetrieveSpendingLimitResponse]:
        """
        Return the lifetime spending limit and accrued usage for a workspace, or null
        when no workspace-level limit is configured. Admin API keys can read any
        workspace in their organization; a workspace key can read its own limit.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not workspace_id:
            raise ValueError(f"Expected a non-empty value for `workspace_id` but received {workspace_id!r}")
        return await self._get(
            path_template("/compute/v1/admin/workspaces/{workspace_id}/spending-limit", workspace_id=workspace_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=WorkspaceRetrieveSpendingLimitResponse,
        )

    async def set_spending_limit(
        self,
        workspace_id: str,
        *,
        limit: workspace_set_spending_limit_params.Limit,
        type: Literal["lifetime"],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Optional[WorkspaceSetSpendingLimitResponse]:
        """
        Create or replace the absolute lifetime spending ceiling for a workspace.
        Tracking starts when the limit is first configured. The new limit cannot be
        lower than accrued usage plus spend reserved by active work. Requires an admin
        API key.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not workspace_id:
            raise ValueError(f"Expected a non-empty value for `workspace_id` but received {workspace_id!r}")
        return await self._put(
            path_template("/compute/v1/admin/workspaces/{workspace_id}/spending-limit", workspace_id=workspace_id),
            body=await async_maybe_transform(
                {
                    "limit": limit,
                    "type": type,
                },
                workspace_set_spending_limit_params.WorkspaceSetSpendingLimitParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=WorkspaceSetSpendingLimitResponse,
        )


class WorkspacesResourceWithRawResponse:
    def __init__(self, workspaces: WorkspacesResource) -> None:
        self._workspaces = workspaces

        self.create = to_raw_response_wrapper(
            workspaces.create,
        )
        self.retrieve = to_raw_response_wrapper(
            workspaces.retrieve,
        )
        self.update = to_raw_response_wrapper(
            workspaces.update,
        )
        self.list = to_raw_response_wrapper(
            workspaces.list,
        )
        self.archive = to_raw_response_wrapper(
            workspaces.archive,
        )
        self.retrieve_spending_limit = to_raw_response_wrapper(
            workspaces.retrieve_spending_limit,
        )
        self.set_spending_limit = to_raw_response_wrapper(
            workspaces.set_spending_limit,
        )


class AsyncWorkspacesResourceWithRawResponse:
    def __init__(self, workspaces: AsyncWorkspacesResource) -> None:
        self._workspaces = workspaces

        self.create = async_to_raw_response_wrapper(
            workspaces.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            workspaces.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            workspaces.update,
        )
        self.list = async_to_raw_response_wrapper(
            workspaces.list,
        )
        self.archive = async_to_raw_response_wrapper(
            workspaces.archive,
        )
        self.retrieve_spending_limit = async_to_raw_response_wrapper(
            workspaces.retrieve_spending_limit,
        )
        self.set_spending_limit = async_to_raw_response_wrapper(
            workspaces.set_spending_limit,
        )


class WorkspacesResourceWithStreamingResponse:
    def __init__(self, workspaces: WorkspacesResource) -> None:
        self._workspaces = workspaces

        self.create = to_streamed_response_wrapper(
            workspaces.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            workspaces.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            workspaces.update,
        )
        self.list = to_streamed_response_wrapper(
            workspaces.list,
        )
        self.archive = to_streamed_response_wrapper(
            workspaces.archive,
        )
        self.retrieve_spending_limit = to_streamed_response_wrapper(
            workspaces.retrieve_spending_limit,
        )
        self.set_spending_limit = to_streamed_response_wrapper(
            workspaces.set_spending_limit,
        )


class AsyncWorkspacesResourceWithStreamingResponse:
    def __init__(self, workspaces: AsyncWorkspacesResource) -> None:
        self._workspaces = workspaces

        self.create = async_to_streamed_response_wrapper(
            workspaces.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            workspaces.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            workspaces.update,
        )
        self.list = async_to_streamed_response_wrapper(
            workspaces.list,
        )
        self.archive = async_to_streamed_response_wrapper(
            workspaces.archive,
        )
        self.retrieve_spending_limit = async_to_streamed_response_wrapper(
            workspaces.retrieve_spending_limit,
        )
        self.set_spending_limit = async_to_streamed_response_wrapper(
            workspaces.set_spending_limit,
        )
