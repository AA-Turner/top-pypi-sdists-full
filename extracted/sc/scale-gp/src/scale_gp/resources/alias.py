# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..types import alias_execute_params
from .._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from .._utils import maybe_transform, async_maybe_transform
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import make_request_options
from ..types.generic_model_response import GenericModelResponse
from ..types.shared.model_server_info import ModelServerInfo

__all__ = ["AliasResource", "AsyncAliasResource"]


class AliasResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AliasResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python#accessing-raw-response-data-eg-headers
        """
        return AliasResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AliasResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python#with_streaming_response
        """
        return AliasResourceWithStreamingResponse(self)

    def retrieve(
        self,
        alias: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ModelServerInfo:
        """
        Fixed Server interface for Model execution by named alias

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not alias:
            raise ValueError(f"Expected a non-empty value for `alias` but received {alias!r}")
        return self._get(
            f"/v4/serving/a/{alias}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ModelServerInfo,
        )

    def execute(
        self,
        alias: str,
        *,
        stream: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> GenericModelResponse:
        """
        Fixed Server interface for Model execution by named alias

        Args:
          stream: Flag indicating whether to stream the completion response

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not alias:
            raise ValueError(f"Expected a non-empty value for `alias` but received {alias!r}")
        return self._post(
            f"/v4/serving/a/{alias}/execute",
            body=maybe_transform({"stream": stream}, alias_execute_params.AliasExecuteParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=GenericModelResponse,
        )


class AsyncAliasResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncAliasResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python#accessing-raw-response-data-eg-headers
        """
        return AsyncAliasResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncAliasResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python#with_streaming_response
        """
        return AsyncAliasResourceWithStreamingResponse(self)

    async def retrieve(
        self,
        alias: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ModelServerInfo:
        """
        Fixed Server interface for Model execution by named alias

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not alias:
            raise ValueError(f"Expected a non-empty value for `alias` but received {alias!r}")
        return await self._get(
            f"/v4/serving/a/{alias}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ModelServerInfo,
        )

    async def execute(
        self,
        alias: str,
        *,
        stream: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> GenericModelResponse:
        """
        Fixed Server interface for Model execution by named alias

        Args:
          stream: Flag indicating whether to stream the completion response

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not alias:
            raise ValueError(f"Expected a non-empty value for `alias` but received {alias!r}")
        return await self._post(
            f"/v4/serving/a/{alias}/execute",
            body=await async_maybe_transform({"stream": stream}, alias_execute_params.AliasExecuteParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=GenericModelResponse,
        )


class AliasResourceWithRawResponse:
    def __init__(self, alias: AliasResource) -> None:
        self._alias = alias

        self.retrieve = to_raw_response_wrapper(
            alias.retrieve,
        )
        self.execute = to_raw_response_wrapper(
            alias.execute,
        )


class AsyncAliasResourceWithRawResponse:
    def __init__(self, alias: AsyncAliasResource) -> None:
        self._alias = alias

        self.retrieve = async_to_raw_response_wrapper(
            alias.retrieve,
        )
        self.execute = async_to_raw_response_wrapper(
            alias.execute,
        )


class AliasResourceWithStreamingResponse:
    def __init__(self, alias: AliasResource) -> None:
        self._alias = alias

        self.retrieve = to_streamed_response_wrapper(
            alias.retrieve,
        )
        self.execute = to_streamed_response_wrapper(
            alias.execute,
        )


class AsyncAliasResourceWithStreamingResponse:
    def __init__(self, alias: AsyncAliasResource) -> None:
        self._alias = alias

        self.retrieve = async_to_streamed_response_wrapper(
            alias.retrieve,
        )
        self.execute = async_to_streamed_response_wrapper(
            alias.execute,
        )
