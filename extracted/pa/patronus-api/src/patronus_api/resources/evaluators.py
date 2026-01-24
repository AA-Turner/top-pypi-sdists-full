# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional

import httpx

from ..types import evaluator_list_params
from .._types import NOT_GIVEN, Body, Query, Headers, NotGiven
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
from ..types.evaluator_list_response import EvaluatorListResponse
from ..types.evaluator_list_families_response import EvaluatorListFamiliesResponse

__all__ = ["EvaluatorsResource", "AsyncEvaluatorsResource"]


class EvaluatorsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> EvaluatorsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/patronus-ai/patronus-api-python#accessing-raw-response-data-eg-headers
        """
        return EvaluatorsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> EvaluatorsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/patronus-ai/patronus-api-python#with_streaming_response
        """
        return EvaluatorsResourceWithStreamingResponse(self)

    def list(
        self,
        *,
        by_alias_or_id: Optional[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EvaluatorListResponse:
        """
        List of available evaluators for Evaluation Runs and LLM Monitoring.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/v1/evaluators",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"by_alias_or_id": by_alias_or_id}, evaluator_list_params.EvaluatorListParams),
            ),
            cast_to=EvaluatorListResponse,
        )

    def list_families(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EvaluatorListFamiliesResponse:
        """List Evaluator Families"""
        return self._get(
            "/v1/evaluator-families",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EvaluatorListFamiliesResponse,
        )


class AsyncEvaluatorsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncEvaluatorsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/patronus-ai/patronus-api-python#accessing-raw-response-data-eg-headers
        """
        return AsyncEvaluatorsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncEvaluatorsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/patronus-ai/patronus-api-python#with_streaming_response
        """
        return AsyncEvaluatorsResourceWithStreamingResponse(self)

    async def list(
        self,
        *,
        by_alias_or_id: Optional[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EvaluatorListResponse:
        """
        List of available evaluators for Evaluation Runs and LLM Monitoring.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/v1/evaluators",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {"by_alias_or_id": by_alias_or_id}, evaluator_list_params.EvaluatorListParams
                ),
            ),
            cast_to=EvaluatorListResponse,
        )

    async def list_families(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EvaluatorListFamiliesResponse:
        """List Evaluator Families"""
        return await self._get(
            "/v1/evaluator-families",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EvaluatorListFamiliesResponse,
        )


class EvaluatorsResourceWithRawResponse:
    def __init__(self, evaluators: EvaluatorsResource) -> None:
        self._evaluators = evaluators

        self.list = to_raw_response_wrapper(
            evaluators.list,
        )
        self.list_families = to_raw_response_wrapper(
            evaluators.list_families,
        )


class AsyncEvaluatorsResourceWithRawResponse:
    def __init__(self, evaluators: AsyncEvaluatorsResource) -> None:
        self._evaluators = evaluators

        self.list = async_to_raw_response_wrapper(
            evaluators.list,
        )
        self.list_families = async_to_raw_response_wrapper(
            evaluators.list_families,
        )


class EvaluatorsResourceWithStreamingResponse:
    def __init__(self, evaluators: EvaluatorsResource) -> None:
        self._evaluators = evaluators

        self.list = to_streamed_response_wrapper(
            evaluators.list,
        )
        self.list_families = to_streamed_response_wrapper(
            evaluators.list_families,
        )


class AsyncEvaluatorsResourceWithStreamingResponse:
    def __init__(self, evaluators: AsyncEvaluatorsResource) -> None:
        self._evaluators = evaluators

        self.list = async_to_streamed_response_wrapper(
            evaluators.list,
        )
        self.list_families = async_to_streamed_response_wrapper(
            evaluators.list_families,
        )
