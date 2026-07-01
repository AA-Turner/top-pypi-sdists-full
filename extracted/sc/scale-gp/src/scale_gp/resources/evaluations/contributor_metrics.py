# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional

import httpx

from ..._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from ..._utils import path_template, maybe_transform
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ...pagination import SyncPageResponse, AsyncPageResponse
from ..._base_client import AsyncPaginator, make_request_options
from ...types.evaluations import contributor_metric_list_params
from ...types.evaluations.contributor_metrics import ContributorMetrics

__all__ = ["ContributorMetricsResource", "AsyncContributorMetricsResource"]


class ContributorMetricsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ContributorMetricsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python#accessing-raw-response-data-eg-headers
        """
        return ContributorMetricsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ContributorMetricsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python#with_streaming_response
        """
        return ContributorMetricsResourceWithStreamingResponse(self)

    def retrieve(
        self,
        contributor_id: str,
        *,
        evaluation_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Optional[ContributorMetrics]:
        """
        Get Contributor Metrics

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not evaluation_id:
            raise ValueError(f"Expected a non-empty value for `evaluation_id` but received {evaluation_id!r}")
        if not contributor_id:
            raise ValueError(f"Expected a non-empty value for `contributor_id` but received {contributor_id!r}")
        return self._get(
            path_template(
                "/v4/evaluations/{evaluation_id}/contributor-metrics/{contributor_id}",
                evaluation_id=evaluation_id,
                contributor_id=contributor_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ContributorMetrics,
        )

    def list(
        self,
        evaluation_id: str,
        *,
        limit: int | Omit = omit,
        page: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SyncPageResponse[ContributorMetrics]:
        """
        List Contributor Metrics

        Args:
          limit: Maximum number of artifacts to be returned by the given endpoint. Defaults to
              100 and cannot be greater than 10k.

          page: Page number for pagination to be returned by the given endpoint. Starts at page
              1

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not evaluation_id:
            raise ValueError(f"Expected a non-empty value for `evaluation_id` but received {evaluation_id!r}")
        return self._get_api_list(
            path_template("/v4/evaluations/{evaluation_id}/contributor-metrics", evaluation_id=evaluation_id),
            page=SyncPageResponse[ContributorMetrics],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "limit": limit,
                        "page": page,
                    },
                    contributor_metric_list_params.ContributorMetricListParams,
                ),
            ),
            model=ContributorMetrics,
        )


class AsyncContributorMetricsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncContributorMetricsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python#accessing-raw-response-data-eg-headers
        """
        return AsyncContributorMetricsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncContributorMetricsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python#with_streaming_response
        """
        return AsyncContributorMetricsResourceWithStreamingResponse(self)

    async def retrieve(
        self,
        contributor_id: str,
        *,
        evaluation_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Optional[ContributorMetrics]:
        """
        Get Contributor Metrics

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not evaluation_id:
            raise ValueError(f"Expected a non-empty value for `evaluation_id` but received {evaluation_id!r}")
        if not contributor_id:
            raise ValueError(f"Expected a non-empty value for `contributor_id` but received {contributor_id!r}")
        return await self._get(
            path_template(
                "/v4/evaluations/{evaluation_id}/contributor-metrics/{contributor_id}",
                evaluation_id=evaluation_id,
                contributor_id=contributor_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ContributorMetrics,
        )

    def list(
        self,
        evaluation_id: str,
        *,
        limit: int | Omit = omit,
        page: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[ContributorMetrics, AsyncPageResponse[ContributorMetrics]]:
        """
        List Contributor Metrics

        Args:
          limit: Maximum number of artifacts to be returned by the given endpoint. Defaults to
              100 and cannot be greater than 10k.

          page: Page number for pagination to be returned by the given endpoint. Starts at page
              1

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not evaluation_id:
            raise ValueError(f"Expected a non-empty value for `evaluation_id` but received {evaluation_id!r}")
        return self._get_api_list(
            path_template("/v4/evaluations/{evaluation_id}/contributor-metrics", evaluation_id=evaluation_id),
            page=AsyncPageResponse[ContributorMetrics],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "limit": limit,
                        "page": page,
                    },
                    contributor_metric_list_params.ContributorMetricListParams,
                ),
            ),
            model=ContributorMetrics,
        )


class ContributorMetricsResourceWithRawResponse:
    def __init__(self, contributor_metrics: ContributorMetricsResource) -> None:
        self._contributor_metrics = contributor_metrics

        self.retrieve = to_raw_response_wrapper(
            contributor_metrics.retrieve,
        )
        self.list = to_raw_response_wrapper(
            contributor_metrics.list,
        )


class AsyncContributorMetricsResourceWithRawResponse:
    def __init__(self, contributor_metrics: AsyncContributorMetricsResource) -> None:
        self._contributor_metrics = contributor_metrics

        self.retrieve = async_to_raw_response_wrapper(
            contributor_metrics.retrieve,
        )
        self.list = async_to_raw_response_wrapper(
            contributor_metrics.list,
        )


class ContributorMetricsResourceWithStreamingResponse:
    def __init__(self, contributor_metrics: ContributorMetricsResource) -> None:
        self._contributor_metrics = contributor_metrics

        self.retrieve = to_streamed_response_wrapper(
            contributor_metrics.retrieve,
        )
        self.list = to_streamed_response_wrapper(
            contributor_metrics.list,
        )


class AsyncContributorMetricsResourceWithStreamingResponse:
    def __init__(self, contributor_metrics: AsyncContributorMetricsResource) -> None:
        self._contributor_metrics = contributor_metrics

        self.retrieve = async_to_streamed_response_wrapper(
            contributor_metrics.retrieve,
        )
        self.list = async_to_streamed_response_wrapper(
            contributor_metrics.list,
        )
