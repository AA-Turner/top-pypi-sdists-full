# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..types import cli_version_params
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
from ..types.cli_version_response import CliVersionResponse

__all__ = ["CliResource", "AsyncCliResource"]


class CliResource(SyncAPIResource):
    """
    Check the installed boltz-api CLI version against the currently published CLI release and the minimum version supported by the Boltz API.
    """

    @cached_property
    def with_raw_response(self) -> CliResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/boltz-bio/boltz-api-python#accessing-raw-response-data-eg-headers
        """
        return CliResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> CliResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/boltz-bio/boltz-api-python#with_streaming_response
        """
        return CliResourceWithStreamingResponse(self)

    def version(
        self,
        *,
        current: str | Omit = omit,
        platform: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> CliVersionResponse:
        """
        Returns public boltz-api CLI version metadata for lightweight update checks.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/compute/v1/cli/version",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "current": current,
                        "platform": platform,
                    },
                    cli_version_params.CliVersionParams,
                ),
            ),
            cast_to=CliVersionResponse,
        )


class AsyncCliResource(AsyncAPIResource):
    """
    Check the installed boltz-api CLI version against the currently published CLI release and the minimum version supported by the Boltz API.
    """

    @cached_property
    def with_raw_response(self) -> AsyncCliResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/boltz-bio/boltz-api-python#accessing-raw-response-data-eg-headers
        """
        return AsyncCliResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncCliResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/boltz-bio/boltz-api-python#with_streaming_response
        """
        return AsyncCliResourceWithStreamingResponse(self)

    async def version(
        self,
        *,
        current: str | Omit = omit,
        platform: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> CliVersionResponse:
        """
        Returns public boltz-api CLI version metadata for lightweight update checks.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/compute/v1/cli/version",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "current": current,
                        "platform": platform,
                    },
                    cli_version_params.CliVersionParams,
                ),
            ),
            cast_to=CliVersionResponse,
        )


class CliResourceWithRawResponse:
    def __init__(self, cli: CliResource) -> None:
        self._cli = cli

        self.version = to_raw_response_wrapper(
            cli.version,
        )


class AsyncCliResourceWithRawResponse:
    def __init__(self, cli: AsyncCliResource) -> None:
        self._cli = cli

        self.version = async_to_raw_response_wrapper(
            cli.version,
        )


class CliResourceWithStreamingResponse:
    def __init__(self, cli: CliResource) -> None:
        self._cli = cli

        self.version = to_streamed_response_wrapper(
            cli.version,
        )


class AsyncCliResourceWithStreamingResponse:
    def __init__(self, cli: AsyncCliResource) -> None:
        self._cli = cli

        self.version = async_to_streamed_response_wrapper(
            cli.version,
        )
