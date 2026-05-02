# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from datetime import datetime

import httpx

from ..._types import Body, Query, Headers, NotGiven, not_given
from ..._utils import maybe_transform, async_maybe_transform
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..._base_client import make_request_options
from ...types.models import usage_statistic_retrieve_params
from ...types.shared.model_usage import ModelUsage

__all__ = ["UsageStatisticsResource", "AsyncUsageStatisticsResource"]


class UsageStatisticsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> UsageStatisticsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python#accessing-raw-response-data-eg-headers
        """
        return UsageStatisticsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> UsageStatisticsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python#with_streaming_response
        """
        return UsageStatisticsResourceWithStreamingResponse(self)

    def retrieve(
        self,
        model_name: str,
        *,
        chunks: int,
        end_date: Union[str, datetime],
        start_date: Union[str, datetime],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ModelUsage:
        """
        Get Model usage by model name

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not model_name:
            raise ValueError(f"Expected a non-empty value for `model_name` but received {model_name!r}")
        return self._get(
            f"/v4/models/{model_name}/usage-statistics",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "chunks": chunks,
                        "end_date": end_date,
                        "start_date": start_date,
                    },
                    usage_statistic_retrieve_params.UsageStatisticRetrieveParams,
                ),
            ),
            cast_to=ModelUsage,
        )


class AsyncUsageStatisticsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncUsageStatisticsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python#accessing-raw-response-data-eg-headers
        """
        return AsyncUsageStatisticsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncUsageStatisticsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python#with_streaming_response
        """
        return AsyncUsageStatisticsResourceWithStreamingResponse(self)

    async def retrieve(
        self,
        model_name: str,
        *,
        chunks: int,
        end_date: Union[str, datetime],
        start_date: Union[str, datetime],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ModelUsage:
        """
        Get Model usage by model name

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not model_name:
            raise ValueError(f"Expected a non-empty value for `model_name` but received {model_name!r}")
        return await self._get(
            f"/v4/models/{model_name}/usage-statistics",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "chunks": chunks,
                        "end_date": end_date,
                        "start_date": start_date,
                    },
                    usage_statistic_retrieve_params.UsageStatisticRetrieveParams,
                ),
            ),
            cast_to=ModelUsage,
        )


class UsageStatisticsResourceWithRawResponse:
    def __init__(self, usage_statistics: UsageStatisticsResource) -> None:
        self._usage_statistics = usage_statistics

        self.retrieve = to_raw_response_wrapper(
            usage_statistics.retrieve,
        )


class AsyncUsageStatisticsResourceWithRawResponse:
    def __init__(self, usage_statistics: AsyncUsageStatisticsResource) -> None:
        self._usage_statistics = usage_statistics

        self.retrieve = async_to_raw_response_wrapper(
            usage_statistics.retrieve,
        )


class UsageStatisticsResourceWithStreamingResponse:
    def __init__(self, usage_statistics: UsageStatisticsResource) -> None:
        self._usage_statistics = usage_statistics

        self.retrieve = to_streamed_response_wrapper(
            usage_statistics.retrieve,
        )


class AsyncUsageStatisticsResourceWithStreamingResponse:
    def __init__(self, usage_statistics: AsyncUsageStatisticsResource) -> None:
        self._usage_statistics = usage_statistics

        self.retrieve = async_to_streamed_response_wrapper(
            usage_statistics.retrieve,
        )
