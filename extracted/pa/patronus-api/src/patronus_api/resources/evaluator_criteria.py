# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional

import httpx

from ..types import (
    evaluator_criterion_list_params,
    evaluator_criterion_create_params,
    evaluator_criterion_add_revision_params,
)
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
from ..types.evaluator_criterion_list_response import EvaluatorCriterionListResponse
from ..types.evaluator_criterion_create_response import EvaluatorCriterionCreateResponse
from ..types.evaluator_criterion_archive_response import EvaluatorCriterionArchiveResponse
from ..types.evaluator_criterion_add_revision_response import EvaluatorCriterionAddRevisionResponse

__all__ = ["EvaluatorCriteriaResource", "AsyncEvaluatorCriteriaResource"]


class EvaluatorCriteriaResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> EvaluatorCriteriaResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/patronus-ai/patronus-api-python#accessing-raw-response-data-eg-headers
        """
        return EvaluatorCriteriaResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> EvaluatorCriteriaResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/patronus-ai/patronus-api-python#with_streaming_response
        """
        return EvaluatorCriteriaResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        config: object,
        evaluator_family: str,
        name: str,
        description: Optional[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EvaluatorCriterionCreateResponse:
        """
        Create Evaluator Criteria

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v1/evaluator-criteria",
            body=maybe_transform(
                {
                    "config": config,
                    "evaluator_family": evaluator_family,
                    "name": name,
                    "description": description,
                },
                evaluator_criterion_create_params.EvaluatorCriterionCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EvaluatorCriterionCreateResponse,
        )

    def list(
        self,
        *,
        enabled: Optional[bool] | NotGiven = NOT_GIVEN,
        evaluator_family: Optional[str] | NotGiven = NOT_GIVEN,
        get_last_revision: bool | NotGiven = NOT_GIVEN,
        is_patronus_managed: Optional[bool] | NotGiven = NOT_GIVEN,
        limit: int | NotGiven = NOT_GIVEN,
        name: Optional[str] | NotGiven = NOT_GIVEN,
        offset: int | NotGiven = NOT_GIVEN,
        public_id: Optional[str] | NotGiven = NOT_GIVEN,
        revision: Optional[int] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EvaluatorCriterionListResponse:
        """
        List Evaluator Criteria

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/v1/evaluator-criteria",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "enabled": enabled,
                        "evaluator_family": evaluator_family,
                        "get_last_revision": get_last_revision,
                        "is_patronus_managed": is_patronus_managed,
                        "limit": limit,
                        "name": name,
                        "offset": offset,
                        "public_id": public_id,
                        "revision": revision,
                    },
                    evaluator_criterion_list_params.EvaluatorCriterionListParams,
                ),
            ),
            cast_to=EvaluatorCriterionListResponse,
        )

    def add_revision(
        self,
        public_id: str,
        *,
        config: object,
        description: Optional[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EvaluatorCriterionAddRevisionResponse:
        """
        Add Evaluator Criteria Revision

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not public_id:
            raise ValueError(f"Expected a non-empty value for `public_id` but received {public_id!r}")
        return self._post(
            f"/v1/evaluator-criteria/{public_id}/revision",
            body=maybe_transform(
                {
                    "config": config,
                    "description": description,
                },
                evaluator_criterion_add_revision_params.EvaluatorCriterionAddRevisionParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EvaluatorCriterionAddRevisionResponse,
        )

    def archive(
        self,
        public_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EvaluatorCriterionArchiveResponse:
        """
        Archive Evaluator Criteria

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not public_id:
            raise ValueError(f"Expected a non-empty value for `public_id` but received {public_id!r}")
        return self._patch(
            f"/v1/evaluator-criteria/{public_id}/archive",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EvaluatorCriterionArchiveResponse,
        )


class AsyncEvaluatorCriteriaResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncEvaluatorCriteriaResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/patronus-ai/patronus-api-python#accessing-raw-response-data-eg-headers
        """
        return AsyncEvaluatorCriteriaResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncEvaluatorCriteriaResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/patronus-ai/patronus-api-python#with_streaming_response
        """
        return AsyncEvaluatorCriteriaResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        config: object,
        evaluator_family: str,
        name: str,
        description: Optional[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EvaluatorCriterionCreateResponse:
        """
        Create Evaluator Criteria

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v1/evaluator-criteria",
            body=await async_maybe_transform(
                {
                    "config": config,
                    "evaluator_family": evaluator_family,
                    "name": name,
                    "description": description,
                },
                evaluator_criterion_create_params.EvaluatorCriterionCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EvaluatorCriterionCreateResponse,
        )

    async def list(
        self,
        *,
        enabled: Optional[bool] | NotGiven = NOT_GIVEN,
        evaluator_family: Optional[str] | NotGiven = NOT_GIVEN,
        get_last_revision: bool | NotGiven = NOT_GIVEN,
        is_patronus_managed: Optional[bool] | NotGiven = NOT_GIVEN,
        limit: int | NotGiven = NOT_GIVEN,
        name: Optional[str] | NotGiven = NOT_GIVEN,
        offset: int | NotGiven = NOT_GIVEN,
        public_id: Optional[str] | NotGiven = NOT_GIVEN,
        revision: Optional[int] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EvaluatorCriterionListResponse:
        """
        List Evaluator Criteria

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/v1/evaluator-criteria",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "enabled": enabled,
                        "evaluator_family": evaluator_family,
                        "get_last_revision": get_last_revision,
                        "is_patronus_managed": is_patronus_managed,
                        "limit": limit,
                        "name": name,
                        "offset": offset,
                        "public_id": public_id,
                        "revision": revision,
                    },
                    evaluator_criterion_list_params.EvaluatorCriterionListParams,
                ),
            ),
            cast_to=EvaluatorCriterionListResponse,
        )

    async def add_revision(
        self,
        public_id: str,
        *,
        config: object,
        description: Optional[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EvaluatorCriterionAddRevisionResponse:
        """
        Add Evaluator Criteria Revision

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not public_id:
            raise ValueError(f"Expected a non-empty value for `public_id` but received {public_id!r}")
        return await self._post(
            f"/v1/evaluator-criteria/{public_id}/revision",
            body=await async_maybe_transform(
                {
                    "config": config,
                    "description": description,
                },
                evaluator_criterion_add_revision_params.EvaluatorCriterionAddRevisionParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EvaluatorCriterionAddRevisionResponse,
        )

    async def archive(
        self,
        public_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EvaluatorCriterionArchiveResponse:
        """
        Archive Evaluator Criteria

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not public_id:
            raise ValueError(f"Expected a non-empty value for `public_id` but received {public_id!r}")
        return await self._patch(
            f"/v1/evaluator-criteria/{public_id}/archive",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EvaluatorCriterionArchiveResponse,
        )


class EvaluatorCriteriaResourceWithRawResponse:
    def __init__(self, evaluator_criteria: EvaluatorCriteriaResource) -> None:
        self._evaluator_criteria = evaluator_criteria

        self.create = to_raw_response_wrapper(
            evaluator_criteria.create,
        )
        self.list = to_raw_response_wrapper(
            evaluator_criteria.list,
        )
        self.add_revision = to_raw_response_wrapper(
            evaluator_criteria.add_revision,
        )
        self.archive = to_raw_response_wrapper(
            evaluator_criteria.archive,
        )


class AsyncEvaluatorCriteriaResourceWithRawResponse:
    def __init__(self, evaluator_criteria: AsyncEvaluatorCriteriaResource) -> None:
        self._evaluator_criteria = evaluator_criteria

        self.create = async_to_raw_response_wrapper(
            evaluator_criteria.create,
        )
        self.list = async_to_raw_response_wrapper(
            evaluator_criteria.list,
        )
        self.add_revision = async_to_raw_response_wrapper(
            evaluator_criteria.add_revision,
        )
        self.archive = async_to_raw_response_wrapper(
            evaluator_criteria.archive,
        )


class EvaluatorCriteriaResourceWithStreamingResponse:
    def __init__(self, evaluator_criteria: EvaluatorCriteriaResource) -> None:
        self._evaluator_criteria = evaluator_criteria

        self.create = to_streamed_response_wrapper(
            evaluator_criteria.create,
        )
        self.list = to_streamed_response_wrapper(
            evaluator_criteria.list,
        )
        self.add_revision = to_streamed_response_wrapper(
            evaluator_criteria.add_revision,
        )
        self.archive = to_streamed_response_wrapper(
            evaluator_criteria.archive,
        )


class AsyncEvaluatorCriteriaResourceWithStreamingResponse:
    def __init__(self, evaluator_criteria: AsyncEvaluatorCriteriaResource) -> None:
        self._evaluator_criteria = evaluator_criteria

        self.create = async_to_streamed_response_wrapper(
            evaluator_criteria.create,
        )
        self.list = async_to_streamed_response_wrapper(
            evaluator_criteria.list,
        )
        self.add_revision = async_to_streamed_response_wrapper(
            evaluator_criteria.add_revision,
        )
        self.archive = async_to_streamed_response_wrapper(
            evaluator_criteria.archive,
        )
