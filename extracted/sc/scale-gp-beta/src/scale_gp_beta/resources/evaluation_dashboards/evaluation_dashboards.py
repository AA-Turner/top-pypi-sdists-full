# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal

import httpx

from ...types import (
    evaluation_dashboard_list_params,
    evaluation_dashboard_create_params,
    evaluation_dashboard_update_params,
    evaluation_dashboard_retrieve_params,
)
from .widgets import (
    WidgetsResource,
    AsyncWidgetsResource,
    WidgetsResourceWithRawResponse,
    AsyncWidgetsResourceWithRawResponse,
    WidgetsResourceWithStreamingResponse,
    AsyncWidgetsResourceWithStreamingResponse,
)
from ..._types import Body, Omit, Query, Headers, NotGiven, SequenceNotStr, omit, not_given
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
from ...types.chat import SortOrder
from ..._base_client import AsyncPaginator, make_request_options
from ...types.chat.sort_order import SortOrder
from ...types.evaluation_dashboard import EvaluationDashboard

__all__ = ["EvaluationDashboardsResource", "AsyncEvaluationDashboardsResource"]


class EvaluationDashboardsResource(SyncAPIResource):
    @cached_property
    def widgets(self) -> WidgetsResource:
        return WidgetsResource(self._client)

    @cached_property
    def with_raw_response(self) -> EvaluationDashboardsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python-beta#accessing-raw-response-data-eg-headers
        """
        return EvaluationDashboardsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> EvaluationDashboardsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python-beta#with_streaming_response
        """
        return EvaluationDashboardsResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        name: str,
        description: str | Omit = omit,
        evaluation_group_id: str | Omit = omit,
        evaluation_id: str | Omit = omit,
        tags: SequenceNotStr[str] | Omit = omit,
        template_dashboard_id: str | Omit = omit,
        widget_order: SequenceNotStr[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> EvaluationDashboard:
        """
        Create a new evaluation dashboard for an evaluation or evaluation group

        Args:
          name: Dashboard name

          description: Optional description of the dashboard

          evaluation_group_id: Evaluation group ID (XOR with evaluation_id)

          evaluation_id: Evaluation ID (XOR with evaluation_group_id)

          tags: The tags associated with the entity

          template_dashboard_id: Optional dashboard ID to use as template. Copies widget_order from template.

          widget_order: Ordered array of widget IDs to display on this dashboard

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v5/evaluation-dashboards",
            body=maybe_transform(
                {
                    "name": name,
                    "description": description,
                    "evaluation_group_id": evaluation_group_id,
                    "evaluation_id": evaluation_id,
                    "tags": tags,
                    "template_dashboard_id": template_dashboard_id,
                    "widget_order": widget_order,
                },
                evaluation_dashboard_create_params.EvaluationDashboardCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EvaluationDashboard,
        )

    def retrieve(
        self,
        dashboard_id: str,
        *,
        include_archived: bool | Omit = omit,
        views: List[Literal["widgets", "widget_results"]] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> EvaluationDashboard:
        """
        Get a single evaluation dashboard by ID

        Args:
          views: Optional relationships to include: 'widgets', 'widget_results'

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not dashboard_id:
            raise ValueError(f"Expected a non-empty value for `dashboard_id` but received {dashboard_id!r}")
        return self._get(
            path_template("/v5/evaluation-dashboards/{dashboard_id}", dashboard_id=dashboard_id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "include_archived": include_archived,
                        "views": views,
                    },
                    evaluation_dashboard_retrieve_params.EvaluationDashboardRetrieveParams,
                ),
            ),
            cast_to=EvaluationDashboard,
        )

    def update(
        self,
        dashboard_id: str,
        *,
        description: str | Omit = omit,
        name: str | Omit = omit,
        tags: SequenceNotStr[str] | Omit = omit,
        widget_order: SequenceNotStr[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> EvaluationDashboard:
        """
        Partially update dashboard metadata (name, description, widget_order)

        Args:
          description: Dashboard description

          name: Dashboard name

          tags: The tags associated with the entity

          widget_order: Ordered array of widget IDs (for reordering widgets)

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not dashboard_id:
            raise ValueError(f"Expected a non-empty value for `dashboard_id` but received {dashboard_id!r}")
        return self._patch(
            path_template("/v5/evaluation-dashboards/{dashboard_id}", dashboard_id=dashboard_id),
            body=maybe_transform(
                {
                    "description": description,
                    "name": name,
                    "tags": tags,
                    "widget_order": widget_order,
                },
                evaluation_dashboard_update_params.EvaluationDashboardUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EvaluationDashboard,
        )

    def list(
        self,
        *,
        created_by_ids: SequenceNotStr[str] | Omit = omit,
        ending_before: str | Omit = omit,
        evaluation_group_id: str | Omit = omit,
        evaluation_id: str | Omit = omit,
        include_archived: bool | Omit = omit,
        limit: int | Omit = omit,
        search: str | Omit = omit,
        sort_by: str | Omit = omit,
        sort_order: SortOrder | Omit = omit,
        starting_after: str | Omit = omit,
        tags: SequenceNotStr[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SyncCursorPage[EvaluationDashboard]:
        """
        List dashboards filtered by evaluation_id, evaluation_group_id, tags, creators,
        or search

        Args:
          created_by_ids: Filter by creator user IDs

          search: Search in name and tags

          tags: Filter by tags (case-insensitive)

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v5/evaluation-dashboards",
            page=SyncCursorPage[EvaluationDashboard],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "created_by_ids": created_by_ids,
                        "ending_before": ending_before,
                        "evaluation_group_id": evaluation_group_id,
                        "evaluation_id": evaluation_id,
                        "include_archived": include_archived,
                        "limit": limit,
                        "search": search,
                        "sort_by": sort_by,
                        "sort_order": sort_order,
                        "starting_after": starting_after,
                        "tags": tags,
                    },
                    evaluation_dashboard_list_params.EvaluationDashboardListParams,
                ),
            ),
            model=EvaluationDashboard,
        )

    def archive(
        self,
        dashboard_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> EvaluationDashboard:
        """
        Soft delete an evaluation dashboard

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not dashboard_id:
            raise ValueError(f"Expected a non-empty value for `dashboard_id` but received {dashboard_id!r}")
        return self._delete(
            path_template("/v5/evaluation-dashboards/{dashboard_id}", dashboard_id=dashboard_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EvaluationDashboard,
        )


class AsyncEvaluationDashboardsResource(AsyncAPIResource):
    @cached_property
    def widgets(self) -> AsyncWidgetsResource:
        return AsyncWidgetsResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncEvaluationDashboardsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python-beta#accessing-raw-response-data-eg-headers
        """
        return AsyncEvaluationDashboardsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncEvaluationDashboardsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python-beta#with_streaming_response
        """
        return AsyncEvaluationDashboardsResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        name: str,
        description: str | Omit = omit,
        evaluation_group_id: str | Omit = omit,
        evaluation_id: str | Omit = omit,
        tags: SequenceNotStr[str] | Omit = omit,
        template_dashboard_id: str | Omit = omit,
        widget_order: SequenceNotStr[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> EvaluationDashboard:
        """
        Create a new evaluation dashboard for an evaluation or evaluation group

        Args:
          name: Dashboard name

          description: Optional description of the dashboard

          evaluation_group_id: Evaluation group ID (XOR with evaluation_id)

          evaluation_id: Evaluation ID (XOR with evaluation_group_id)

          tags: The tags associated with the entity

          template_dashboard_id: Optional dashboard ID to use as template. Copies widget_order from template.

          widget_order: Ordered array of widget IDs to display on this dashboard

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v5/evaluation-dashboards",
            body=await async_maybe_transform(
                {
                    "name": name,
                    "description": description,
                    "evaluation_group_id": evaluation_group_id,
                    "evaluation_id": evaluation_id,
                    "tags": tags,
                    "template_dashboard_id": template_dashboard_id,
                    "widget_order": widget_order,
                },
                evaluation_dashboard_create_params.EvaluationDashboardCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EvaluationDashboard,
        )

    async def retrieve(
        self,
        dashboard_id: str,
        *,
        include_archived: bool | Omit = omit,
        views: List[Literal["widgets", "widget_results"]] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> EvaluationDashboard:
        """
        Get a single evaluation dashboard by ID

        Args:
          views: Optional relationships to include: 'widgets', 'widget_results'

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not dashboard_id:
            raise ValueError(f"Expected a non-empty value for `dashboard_id` but received {dashboard_id!r}")
        return await self._get(
            path_template("/v5/evaluation-dashboards/{dashboard_id}", dashboard_id=dashboard_id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "include_archived": include_archived,
                        "views": views,
                    },
                    evaluation_dashboard_retrieve_params.EvaluationDashboardRetrieveParams,
                ),
            ),
            cast_to=EvaluationDashboard,
        )

    async def update(
        self,
        dashboard_id: str,
        *,
        description: str | Omit = omit,
        name: str | Omit = omit,
        tags: SequenceNotStr[str] | Omit = omit,
        widget_order: SequenceNotStr[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> EvaluationDashboard:
        """
        Partially update dashboard metadata (name, description, widget_order)

        Args:
          description: Dashboard description

          name: Dashboard name

          tags: The tags associated with the entity

          widget_order: Ordered array of widget IDs (for reordering widgets)

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not dashboard_id:
            raise ValueError(f"Expected a non-empty value for `dashboard_id` but received {dashboard_id!r}")
        return await self._patch(
            path_template("/v5/evaluation-dashboards/{dashboard_id}", dashboard_id=dashboard_id),
            body=await async_maybe_transform(
                {
                    "description": description,
                    "name": name,
                    "tags": tags,
                    "widget_order": widget_order,
                },
                evaluation_dashboard_update_params.EvaluationDashboardUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EvaluationDashboard,
        )

    def list(
        self,
        *,
        created_by_ids: SequenceNotStr[str] | Omit = omit,
        ending_before: str | Omit = omit,
        evaluation_group_id: str | Omit = omit,
        evaluation_id: str | Omit = omit,
        include_archived: bool | Omit = omit,
        limit: int | Omit = omit,
        search: str | Omit = omit,
        sort_by: str | Omit = omit,
        sort_order: SortOrder | Omit = omit,
        starting_after: str | Omit = omit,
        tags: SequenceNotStr[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[EvaluationDashboard, AsyncCursorPage[EvaluationDashboard]]:
        """
        List dashboards filtered by evaluation_id, evaluation_group_id, tags, creators,
        or search

        Args:
          created_by_ids: Filter by creator user IDs

          search: Search in name and tags

          tags: Filter by tags (case-insensitive)

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v5/evaluation-dashboards",
            page=AsyncCursorPage[EvaluationDashboard],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "created_by_ids": created_by_ids,
                        "ending_before": ending_before,
                        "evaluation_group_id": evaluation_group_id,
                        "evaluation_id": evaluation_id,
                        "include_archived": include_archived,
                        "limit": limit,
                        "search": search,
                        "sort_by": sort_by,
                        "sort_order": sort_order,
                        "starting_after": starting_after,
                        "tags": tags,
                    },
                    evaluation_dashboard_list_params.EvaluationDashboardListParams,
                ),
            ),
            model=EvaluationDashboard,
        )

    async def archive(
        self,
        dashboard_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> EvaluationDashboard:
        """
        Soft delete an evaluation dashboard

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not dashboard_id:
            raise ValueError(f"Expected a non-empty value for `dashboard_id` but received {dashboard_id!r}")
        return await self._delete(
            path_template("/v5/evaluation-dashboards/{dashboard_id}", dashboard_id=dashboard_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EvaluationDashboard,
        )


class EvaluationDashboardsResourceWithRawResponse:
    def __init__(self, evaluation_dashboards: EvaluationDashboardsResource) -> None:
        self._evaluation_dashboards = evaluation_dashboards

        self.create = to_raw_response_wrapper(
            evaluation_dashboards.create,
        )
        self.retrieve = to_raw_response_wrapper(
            evaluation_dashboards.retrieve,
        )
        self.update = to_raw_response_wrapper(
            evaluation_dashboards.update,
        )
        self.list = to_raw_response_wrapper(
            evaluation_dashboards.list,
        )
        self.archive = to_raw_response_wrapper(
            evaluation_dashboards.archive,
        )

    @cached_property
    def widgets(self) -> WidgetsResourceWithRawResponse:
        return WidgetsResourceWithRawResponse(self._evaluation_dashboards.widgets)


class AsyncEvaluationDashboardsResourceWithRawResponse:
    def __init__(self, evaluation_dashboards: AsyncEvaluationDashboardsResource) -> None:
        self._evaluation_dashboards = evaluation_dashboards

        self.create = async_to_raw_response_wrapper(
            evaluation_dashboards.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            evaluation_dashboards.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            evaluation_dashboards.update,
        )
        self.list = async_to_raw_response_wrapper(
            evaluation_dashboards.list,
        )
        self.archive = async_to_raw_response_wrapper(
            evaluation_dashboards.archive,
        )

    @cached_property
    def widgets(self) -> AsyncWidgetsResourceWithRawResponse:
        return AsyncWidgetsResourceWithRawResponse(self._evaluation_dashboards.widgets)


class EvaluationDashboardsResourceWithStreamingResponse:
    def __init__(self, evaluation_dashboards: EvaluationDashboardsResource) -> None:
        self._evaluation_dashboards = evaluation_dashboards

        self.create = to_streamed_response_wrapper(
            evaluation_dashboards.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            evaluation_dashboards.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            evaluation_dashboards.update,
        )
        self.list = to_streamed_response_wrapper(
            evaluation_dashboards.list,
        )
        self.archive = to_streamed_response_wrapper(
            evaluation_dashboards.archive,
        )

    @cached_property
    def widgets(self) -> WidgetsResourceWithStreamingResponse:
        return WidgetsResourceWithStreamingResponse(self._evaluation_dashboards.widgets)


class AsyncEvaluationDashboardsResourceWithStreamingResponse:
    def __init__(self, evaluation_dashboards: AsyncEvaluationDashboardsResource) -> None:
        self._evaluation_dashboards = evaluation_dashboards

        self.create = async_to_streamed_response_wrapper(
            evaluation_dashboards.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            evaluation_dashboards.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            evaluation_dashboards.update,
        )
        self.list = async_to_streamed_response_wrapper(
            evaluation_dashboards.list,
        )
        self.archive = async_to_streamed_response_wrapper(
            evaluation_dashboards.archive,
        )

    @cached_property
    def widgets(self) -> AsyncWidgetsResourceWithStreamingResponse:
        return AsyncWidgetsResourceWithStreamingResponse(self._evaluation_dashboards.widgets)
