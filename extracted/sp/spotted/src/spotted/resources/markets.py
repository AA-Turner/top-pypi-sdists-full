# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import typing_extensions

import httpx

from .._types import Body, Query, Headers, NotGiven, not_given
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import make_request_options
from ..types.market_list_response import MarketListResponse

__all__ = ["MarketsResource", "AsyncMarketsResource"]


class MarketsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> MarketsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cjavdev/spotted-py#accessing-raw-response-data-eg-headers
        """
        return MarketsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> MarketsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cjavdev/spotted-py#with_streaming_response
        """
        return MarketsResourceWithStreamingResponse(self)

    @typing_extensions.deprecated("deprecated")
    def list(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> MarketListResponse:
        """Get the list of markets where Spotify is available."""
        return self._get(
            "/markets",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=MarketListResponse,
        )


class AsyncMarketsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncMarketsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cjavdev/spotted-py#accessing-raw-response-data-eg-headers
        """
        return AsyncMarketsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncMarketsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cjavdev/spotted-py#with_streaming_response
        """
        return AsyncMarketsResourceWithStreamingResponse(self)

    @typing_extensions.deprecated("deprecated")
    async def list(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> MarketListResponse:
        """Get the list of markets where Spotify is available."""
        return await self._get(
            "/markets",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=MarketListResponse,
        )


class MarketsResourceWithRawResponse:
    def __init__(self, markets: MarketsResource) -> None:
        self._markets = markets

        self.list = (  # pyright: ignore[reportDeprecated]
            to_raw_response_wrapper(
                markets.list,  # pyright: ignore[reportDeprecated],
            )
        )


class AsyncMarketsResourceWithRawResponse:
    def __init__(self, markets: AsyncMarketsResource) -> None:
        self._markets = markets

        self.list = (  # pyright: ignore[reportDeprecated]
            async_to_raw_response_wrapper(
                markets.list,  # pyright: ignore[reportDeprecated],
            )
        )


class MarketsResourceWithStreamingResponse:
    def __init__(self, markets: MarketsResource) -> None:
        self._markets = markets

        self.list = (  # pyright: ignore[reportDeprecated]
            to_streamed_response_wrapper(
                markets.list,  # pyright: ignore[reportDeprecated],
            )
        )


class AsyncMarketsResourceWithStreamingResponse:
    def __init__(self, markets: AsyncMarketsResource) -> None:
        self._markets = markets

        self.list = (  # pyright: ignore[reportDeprecated]
            async_to_streamed_response_wrapper(
                markets.list,  # pyright: ignore[reportDeprecated],
            )
        )
