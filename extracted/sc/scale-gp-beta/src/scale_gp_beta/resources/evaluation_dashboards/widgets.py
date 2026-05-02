# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict

import httpx

from ..._types import Body, Omit, Query, Headers, NoneType, NotGiven, omit, not_given
from ..._utils import path_template, maybe_transform, async_maybe_transform
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..._base_client import make_request_options
from ...types.evaluation_dashboards import EvaluationWidgetTypeEnum, widget_create_params, widget_update_params
from ...types.evaluation_dashboards.evaluation_widget_type_enum import EvaluationWidgetTypeEnum
from ...types.evaluation_dashboards.evaluation_dashboard_widget_with_result import EvaluationDashboardWidgetWithResult

__all__ = ["WidgetsResource", "AsyncWidgetsResource"]


class WidgetsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> WidgetsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python-beta#accessing-raw-response-data-eg-headers
        """
        return WidgetsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> WidgetsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python-beta#with_streaming_response
        """
        return WidgetsResourceWithStreamingResponse(self)

    def create(
        self,
        dashboard_id: str,
        *,
        title: str,
        type: EvaluationWidgetTypeEnum,
        config: Dict[str, object] | Omit = omit,
        query: widget_create_params.Query | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> EvaluationDashboardWidgetWithResult:
        """
        Create a new widget, add it to the dashboard, and compute its results

        Args:
          title: Widget title

          type: Widget type

          config: Chart-specific display configuration

          query: Structured query AST for metric computation (SeriesQuery or MetricQuery)

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not dashboard_id:
            raise ValueError(f"Expected a non-empty value for `dashboard_id` but received {dashboard_id!r}")
        return self._post(
            path_template("/v5/evaluation-dashboards/{dashboard_id}/widgets", dashboard_id=dashboard_id),
            body=maybe_transform(
                {
                    "title": title,
                    "type": type,
                    "config": config,
                    "query": query,
                },
                widget_create_params.WidgetCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EvaluationDashboardWidgetWithResult,
        )

    def update(
        self,
        widget_id: str,
        *,
        dashboard_id: str,
        config: Dict[str, object] | Omit = omit,
        query: widget_update_params.Query | Omit = omit,
        title: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> EvaluationDashboardWidgetWithResult:
        """Update a widget and compute its results.

        If the widget is only used by this
        dashboard, it is updated in place. If shared across multiple dashboards, a copy
        is created.

        Args:
          config: Chart-specific display configuration

          query: Structured query AST for metric computation (SeriesQuery or MetricQuery)

          title: Widget title

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not dashboard_id:
            raise ValueError(f"Expected a non-empty value for `dashboard_id` but received {dashboard_id!r}")
        if not widget_id:
            raise ValueError(f"Expected a non-empty value for `widget_id` but received {widget_id!r}")
        return self._patch(
            path_template(
                "/v5/evaluation-dashboards/{dashboard_id}/widgets/{widget_id}",
                dashboard_id=dashboard_id,
                widget_id=widget_id,
            ),
            body=maybe_transform(
                {
                    "config": config,
                    "query": query,
                    "title": title,
                },
                widget_update_params.WidgetUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EvaluationDashboardWidgetWithResult,
        )

    def remove(
        self,
        widget_id: str,
        *,
        dashboard_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> None:
        """
        Remove a widget from the dashboard (does not delete the widget)

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not dashboard_id:
            raise ValueError(f"Expected a non-empty value for `dashboard_id` but received {dashboard_id!r}")
        if not widget_id:
            raise ValueError(f"Expected a non-empty value for `widget_id` but received {widget_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._delete(
            path_template(
                "/v5/evaluation-dashboards/{dashboard_id}/widgets/{widget_id}",
                dashboard_id=dashboard_id,
                widget_id=widget_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class AsyncWidgetsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncWidgetsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python-beta#accessing-raw-response-data-eg-headers
        """
        return AsyncWidgetsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncWidgetsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python-beta#with_streaming_response
        """
        return AsyncWidgetsResourceWithStreamingResponse(self)

    async def create(
        self,
        dashboard_id: str,
        *,
        title: str,
        type: EvaluationWidgetTypeEnum,
        config: Dict[str, object] | Omit = omit,
        query: widget_create_params.Query | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> EvaluationDashboardWidgetWithResult:
        """
        Create a new widget, add it to the dashboard, and compute its results

        Args:
          title: Widget title

          type: Widget type

          config: Chart-specific display configuration

          query: Structured query AST for metric computation (SeriesQuery or MetricQuery)

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not dashboard_id:
            raise ValueError(f"Expected a non-empty value for `dashboard_id` but received {dashboard_id!r}")
        return await self._post(
            path_template("/v5/evaluation-dashboards/{dashboard_id}/widgets", dashboard_id=dashboard_id),
            body=await async_maybe_transform(
                {
                    "title": title,
                    "type": type,
                    "config": config,
                    "query": query,
                },
                widget_create_params.WidgetCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EvaluationDashboardWidgetWithResult,
        )

    async def update(
        self,
        widget_id: str,
        *,
        dashboard_id: str,
        config: Dict[str, object] | Omit = omit,
        query: widget_update_params.Query | Omit = omit,
        title: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> EvaluationDashboardWidgetWithResult:
        """Update a widget and compute its results.

        If the widget is only used by this
        dashboard, it is updated in place. If shared across multiple dashboards, a copy
        is created.

        Args:
          config: Chart-specific display configuration

          query: Structured query AST for metric computation (SeriesQuery or MetricQuery)

          title: Widget title

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not dashboard_id:
            raise ValueError(f"Expected a non-empty value for `dashboard_id` but received {dashboard_id!r}")
        if not widget_id:
            raise ValueError(f"Expected a non-empty value for `widget_id` but received {widget_id!r}")
        return await self._patch(
            path_template(
                "/v5/evaluation-dashboards/{dashboard_id}/widgets/{widget_id}",
                dashboard_id=dashboard_id,
                widget_id=widget_id,
            ),
            body=await async_maybe_transform(
                {
                    "config": config,
                    "query": query,
                    "title": title,
                },
                widget_update_params.WidgetUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EvaluationDashboardWidgetWithResult,
        )

    async def remove(
        self,
        widget_id: str,
        *,
        dashboard_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> None:
        """
        Remove a widget from the dashboard (does not delete the widget)

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not dashboard_id:
            raise ValueError(f"Expected a non-empty value for `dashboard_id` but received {dashboard_id!r}")
        if not widget_id:
            raise ValueError(f"Expected a non-empty value for `widget_id` but received {widget_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._delete(
            path_template(
                "/v5/evaluation-dashboards/{dashboard_id}/widgets/{widget_id}",
                dashboard_id=dashboard_id,
                widget_id=widget_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class WidgetsResourceWithRawResponse:
    def __init__(self, widgets: WidgetsResource) -> None:
        self._widgets = widgets

        self.create = to_raw_response_wrapper(
            widgets.create,
        )
        self.update = to_raw_response_wrapper(
            widgets.update,
        )
        self.remove = to_raw_response_wrapper(
            widgets.remove,
        )


class AsyncWidgetsResourceWithRawResponse:
    def __init__(self, widgets: AsyncWidgetsResource) -> None:
        self._widgets = widgets

        self.create = async_to_raw_response_wrapper(
            widgets.create,
        )
        self.update = async_to_raw_response_wrapper(
            widgets.update,
        )
        self.remove = async_to_raw_response_wrapper(
            widgets.remove,
        )


class WidgetsResourceWithStreamingResponse:
    def __init__(self, widgets: WidgetsResource) -> None:
        self._widgets = widgets

        self.create = to_streamed_response_wrapper(
            widgets.create,
        )
        self.update = to_streamed_response_wrapper(
            widgets.update,
        )
        self.remove = to_streamed_response_wrapper(
            widgets.remove,
        )


class AsyncWidgetsResourceWithStreamingResponse:
    def __init__(self, widgets: AsyncWidgetsResource) -> None:
        self._widgets = widgets

        self.create = async_to_streamed_response_wrapper(
            widgets.create,
        )
        self.update = async_to_streamed_response_wrapper(
            widgets.update,
        )
        self.remove = async_to_streamed_response_wrapper(
            widgets.remove,
        )
