# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Union
from datetime import datetime
from typing_extensions import Literal

import httpx

from ..._types import Body, Omit, Query, Headers, NotGiven, SequenceNotStr, omit, not_given
from ..._utils import maybe_transform
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ...pagination import SyncOpaqueCursorPage, AsyncOpaqueCursorPage
from ...types.admin import usage_list_params
from ..._base_client import AsyncPaginator, make_request_options
from ...types.admin.usage_list_response import UsageListResponse

__all__ = ["UsageResource", "AsyncUsageResource"]


class UsageResource(SyncAPIResource):
    """Retrieve aggregated usage data for the organization.

    Usage can be grouped by workspace and/or application, and filtered by time range, workspace, and application.
    """

    @cached_property
    def with_raw_response(self) -> UsageResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/boltz-bio/boltz-api-python#accessing-raw-response-data-eg-headers
        """
        return UsageResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> UsageResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/boltz-bio/boltz-api-python#with_streaming_response
        """
        return UsageResourceWithStreamingResponse(self)

    def list(
        self,
        *,
        ending_at: Union[str, datetime],
        starting_at: Union[str, datetime],
        window_size: Literal["HOUR", "DAY"],
        applications: Union[
            Literal[
                "structure_and_binding",
                "small_molecule_design",
                "small_molecule_library_screen",
                "protein_design",
                "protein_redesign",
                "protein_library_screen",
                "adme",
            ],
            List[
                Literal[
                    "structure_and_binding",
                    "small_molecule_design",
                    "small_molecule_library_screen",
                    "protein_design",
                    "protein_redesign",
                    "protein_library_screen",
                    "adme",
                ]
            ],
        ]
        | Omit = omit,
        group_by: Union[Literal["workspace_id", "application"], List[Literal["workspace_id", "application"]]]
        | Omit = omit,
        limit: int | Omit = omit,
        page: str | Omit = omit,
        workspace_ids: Union[str, SequenceNotStr[str]] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SyncOpaqueCursorPage[UsageListResponse]:
        """
        Retrieve aggregated usage data across the organization, optionally grouped by
        workspace and/or application.

        Args:
          ending_at: End of the time range as an ISO 8601 date-time with timezone, for example
              2026-04-08T18:56:46Z

          starting_at: Start of the time range as an ISO 8601 date-time with timezone, for example
              2026-04-08T18:56:46Z

          window_size: Time window size. HOUR supports up to 31 days per query; DAY supports up to 365
              days per query.

          applications: Filter to specific applications

          group_by: Group results by workspace_id and/or application

          limit: Maximum number of buckets to return

          page: Cursor for pagination

          workspace_ids: Filter to specific workspace IDs

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/compute/v1/admin/usage",
            page=SyncOpaqueCursorPage[UsageListResponse],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "ending_at": ending_at,
                        "starting_at": starting_at,
                        "window_size": window_size,
                        "applications": applications,
                        "group_by": group_by,
                        "limit": limit,
                        "page": page,
                        "workspace_ids": workspace_ids,
                    },
                    usage_list_params.UsageListParams,
                ),
            ),
            model=UsageListResponse,
        )


class AsyncUsageResource(AsyncAPIResource):
    """Retrieve aggregated usage data for the organization.

    Usage can be grouped by workspace and/or application, and filtered by time range, workspace, and application.
    """

    @cached_property
    def with_raw_response(self) -> AsyncUsageResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/boltz-bio/boltz-api-python#accessing-raw-response-data-eg-headers
        """
        return AsyncUsageResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncUsageResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/boltz-bio/boltz-api-python#with_streaming_response
        """
        return AsyncUsageResourceWithStreamingResponse(self)

    def list(
        self,
        *,
        ending_at: Union[str, datetime],
        starting_at: Union[str, datetime],
        window_size: Literal["HOUR", "DAY"],
        applications: Union[
            Literal[
                "structure_and_binding",
                "small_molecule_design",
                "small_molecule_library_screen",
                "protein_design",
                "protein_redesign",
                "protein_library_screen",
                "adme",
            ],
            List[
                Literal[
                    "structure_and_binding",
                    "small_molecule_design",
                    "small_molecule_library_screen",
                    "protein_design",
                    "protein_redesign",
                    "protein_library_screen",
                    "adme",
                ]
            ],
        ]
        | Omit = omit,
        group_by: Union[Literal["workspace_id", "application"], List[Literal["workspace_id", "application"]]]
        | Omit = omit,
        limit: int | Omit = omit,
        page: str | Omit = omit,
        workspace_ids: Union[str, SequenceNotStr[str]] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[UsageListResponse, AsyncOpaqueCursorPage[UsageListResponse]]:
        """
        Retrieve aggregated usage data across the organization, optionally grouped by
        workspace and/or application.

        Args:
          ending_at: End of the time range as an ISO 8601 date-time with timezone, for example
              2026-04-08T18:56:46Z

          starting_at: Start of the time range as an ISO 8601 date-time with timezone, for example
              2026-04-08T18:56:46Z

          window_size: Time window size. HOUR supports up to 31 days per query; DAY supports up to 365
              days per query.

          applications: Filter to specific applications

          group_by: Group results by workspace_id and/or application

          limit: Maximum number of buckets to return

          page: Cursor for pagination

          workspace_ids: Filter to specific workspace IDs

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/compute/v1/admin/usage",
            page=AsyncOpaqueCursorPage[UsageListResponse],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "ending_at": ending_at,
                        "starting_at": starting_at,
                        "window_size": window_size,
                        "applications": applications,
                        "group_by": group_by,
                        "limit": limit,
                        "page": page,
                        "workspace_ids": workspace_ids,
                    },
                    usage_list_params.UsageListParams,
                ),
            ),
            model=UsageListResponse,
        )


class UsageResourceWithRawResponse:
    def __init__(self, usage: UsageResource) -> None:
        self._usage = usage

        self.list = to_raw_response_wrapper(
            usage.list,
        )


class AsyncUsageResourceWithRawResponse:
    def __init__(self, usage: AsyncUsageResource) -> None:
        self._usage = usage

        self.list = async_to_raw_response_wrapper(
            usage.list,
        )


class UsageResourceWithStreamingResponse:
    def __init__(self, usage: UsageResource) -> None:
        self._usage = usage

        self.list = to_streamed_response_wrapper(
            usage.list,
        )


class AsyncUsageResourceWithStreamingResponse:
    def __init__(self, usage: AsyncUsageResource) -> None:
        self._usage = usage

        self.list = async_to_streamed_response_wrapper(
            usage.list,
        )
