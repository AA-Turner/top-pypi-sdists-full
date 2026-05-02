# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..._types import Body, Omit, Query, Headers, NotGiven, SequenceNotStr, omit, not_given
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
from ...types.models import reranking_create_params
from ...types.reranking_response import RerankingResponse
from ...types.parameter_bindings_param import ParameterBindingsParam

__all__ = ["RerankingsResource", "AsyncRerankingsResource"]


class RerankingsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> RerankingsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python#accessing-raw-response-data-eg-headers
        """
        return RerankingsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> RerankingsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python#with_streaming_response
        """
        return RerankingsResourceWithStreamingResponse(self)

    def create(
        self,
        model_deployment_id: str,
        *,
        chunks: SequenceNotStr[str],
        query: str,
        model_request_parameters: ParameterBindingsParam | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> RerankingResponse:
        """
        ### Description

        TODO: Documentation

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not model_deployment_id:
            raise ValueError(
                f"Expected a non-empty value for `model_deployment_id` but received {model_deployment_id!r}"
            )
        return self._post(
            f"/v4/models/{model_deployment_id}/rerankings",
            body=maybe_transform(
                {
                    "chunks": chunks,
                    "query": query,
                    "model_request_parameters": model_request_parameters,
                },
                reranking_create_params.RerankingCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=RerankingResponse,
        )


class AsyncRerankingsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncRerankingsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python#accessing-raw-response-data-eg-headers
        """
        return AsyncRerankingsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncRerankingsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python#with_streaming_response
        """
        return AsyncRerankingsResourceWithStreamingResponse(self)

    async def create(
        self,
        model_deployment_id: str,
        *,
        chunks: SequenceNotStr[str],
        query: str,
        model_request_parameters: ParameterBindingsParam | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> RerankingResponse:
        """
        ### Description

        TODO: Documentation

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not model_deployment_id:
            raise ValueError(
                f"Expected a non-empty value for `model_deployment_id` but received {model_deployment_id!r}"
            )
        return await self._post(
            f"/v4/models/{model_deployment_id}/rerankings",
            body=await async_maybe_transform(
                {
                    "chunks": chunks,
                    "query": query,
                    "model_request_parameters": model_request_parameters,
                },
                reranking_create_params.RerankingCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=RerankingResponse,
        )


class RerankingsResourceWithRawResponse:
    def __init__(self, rerankings: RerankingsResource) -> None:
        self._rerankings = rerankings

        self.create = to_raw_response_wrapper(
            rerankings.create,
        )


class AsyncRerankingsResourceWithRawResponse:
    def __init__(self, rerankings: AsyncRerankingsResource) -> None:
        self._rerankings = rerankings

        self.create = async_to_raw_response_wrapper(
            rerankings.create,
        )


class RerankingsResourceWithStreamingResponse:
    def __init__(self, rerankings: RerankingsResource) -> None:
        self._rerankings = rerankings

        self.create = to_streamed_response_wrapper(
            rerankings.create,
        )


class AsyncRerankingsResourceWithStreamingResponse:
    def __init__(self, rerankings: AsyncRerankingsResource) -> None:
        self._rerankings = rerankings

        self.create = async_to_streamed_response_wrapper(
            rerankings.create,
        )
