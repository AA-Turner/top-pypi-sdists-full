# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict

import httpx

from ..types import (
    ApprovalStatus,
    AssessmentType,
    span_assessment_list_params,
    span_assessment_create_params,
    span_assessment_update_params,
)
from .._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from .._utils import path_template, maybe_transform, async_maybe_transform
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..pagination import SyncAPIListPage, AsyncAPIListPage
from .._base_client import AsyncPaginator, make_request_options
from ..types.approval_status import ApprovalStatus
from ..types.assessment_type import AssessmentType
from ..types.span_assessment import SpanAssessment
from ..types.span_assessment_delete_response import SpanAssessmentDeleteResponse

__all__ = ["SpanAssessmentsResource", "AsyncSpanAssessmentsResource"]


class SpanAssessmentsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> SpanAssessmentsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python-beta#accessing-raw-response-data-eg-headers
        """
        return SpanAssessmentsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> SpanAssessmentsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python-beta#with_streaming_response
        """
        return SpanAssessmentsResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        assessment_type: AssessmentType,
        span_id: str,
        trace_id: str,
        approval: ApprovalStatus | Omit = omit,
        comment: str | Omit = omit,
        metadata: Dict[str, object] | Omit = omit,
        overwrite: Dict[str, object] | Omit = omit,
        rating: int | Omit = omit,
        rubric: Dict[str, str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SpanAssessment:
        """
        Create new assessment for a span (comment, rating, approval, rubric, overwrite,
        or metadata)

        Args:
          assessment_type: Type of assessment

          span_id: The ID of the span this assessment is attached to

          trace_id: The ID of the trace this assessment is attached to

          approval: Approval status (approved/rejected)

          comment: Raw text feedback

          metadata: Arbitrary JSON object for additional data

          overwrite: User corrections to span output

          rating: Numerical rating (1-5)

          rubric: Rule key-value pairs for rubric evaluation

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v5/span-assessments",
            body=maybe_transform(
                {
                    "assessment_type": assessment_type,
                    "span_id": span_id,
                    "trace_id": trace_id,
                    "approval": approval,
                    "comment": comment,
                    "metadata": metadata,
                    "overwrite": overwrite,
                    "rating": rating,
                    "rubric": rubric,
                },
                span_assessment_create_params.SpanAssessmentCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SpanAssessment,
        )

    def retrieve(
        self,
        span_assessment_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SpanAssessment:
        """
        Get an assessment by ID

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not span_assessment_id:
            raise ValueError(f"Expected a non-empty value for `span_assessment_id` but received {span_assessment_id!r}")
        return self._get(
            path_template("/v5/span-assessments/{span_assessment_id}", span_assessment_id=span_assessment_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SpanAssessment,
        )

    def update(
        self,
        span_assessment_id: str,
        *,
        approval: ApprovalStatus | Omit = omit,
        assessment_type: AssessmentType | Omit = omit,
        comment: str | Omit = omit,
        metadata: Dict[str, object] | Omit = omit,
        overwrite: Dict[str, object] | Omit = omit,
        rating: int | Omit = omit,
        rubric: Dict[str, str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SpanAssessment:
        """
        Update existing assessment (only by the original creator)

        Args:
          approval: Approval status (approved/rejected)

          assessment_type: Type of assessment

          comment: Raw text feedback

          metadata: Arbitrary JSON object for additional data

          overwrite: User corrections to span output

          rating: Numerical rating (1-5)

          rubric: Rule key-value pairs for rubric evaluation

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not span_assessment_id:
            raise ValueError(f"Expected a non-empty value for `span_assessment_id` but received {span_assessment_id!r}")
        return self._patch(
            path_template("/v5/span-assessments/{span_assessment_id}", span_assessment_id=span_assessment_id),
            body=maybe_transform(
                {
                    "approval": approval,
                    "assessment_type": assessment_type,
                    "comment": comment,
                    "metadata": metadata,
                    "overwrite": overwrite,
                    "rating": rating,
                    "rubric": rubric,
                },
                span_assessment_update_params.SpanAssessmentUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SpanAssessment,
        )

    def list(
        self,
        *,
        assessment_type: AssessmentType | Omit = omit,
        span_id: str | Omit = omit,
        trace_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SyncAPIListPage[SpanAssessment]:
        """
        Get all assessments for a specific span or trace, optionally filtered by
        assessment type

        Args:
          assessment_type: Filter by assessment type

          span_id: Filter by span ID. Either span_id or trace_id must be provided as a query
              parameter.

          trace_id: Filter by trace ID. Either span_id or trace_id must be provided as a query
              parameter.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v5/span-assessments",
            page=SyncAPIListPage[SpanAssessment],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "assessment_type": assessment_type,
                        "span_id": span_id,
                        "trace_id": trace_id,
                    },
                    span_assessment_list_params.SpanAssessmentListParams,
                ),
            ),
            model=SpanAssessment,
        )

    def delete(
        self,
        span_assessment_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SpanAssessmentDeleteResponse:
        """
        Delete assessment

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not span_assessment_id:
            raise ValueError(f"Expected a non-empty value for `span_assessment_id` but received {span_assessment_id!r}")
        return self._delete(
            path_template("/v5/span-assessments/{span_assessment_id}", span_assessment_id=span_assessment_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SpanAssessmentDeleteResponse,
        )


class AsyncSpanAssessmentsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncSpanAssessmentsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python-beta#accessing-raw-response-data-eg-headers
        """
        return AsyncSpanAssessmentsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncSpanAssessmentsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python-beta#with_streaming_response
        """
        return AsyncSpanAssessmentsResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        assessment_type: AssessmentType,
        span_id: str,
        trace_id: str,
        approval: ApprovalStatus | Omit = omit,
        comment: str | Omit = omit,
        metadata: Dict[str, object] | Omit = omit,
        overwrite: Dict[str, object] | Omit = omit,
        rating: int | Omit = omit,
        rubric: Dict[str, str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SpanAssessment:
        """
        Create new assessment for a span (comment, rating, approval, rubric, overwrite,
        or metadata)

        Args:
          assessment_type: Type of assessment

          span_id: The ID of the span this assessment is attached to

          trace_id: The ID of the trace this assessment is attached to

          approval: Approval status (approved/rejected)

          comment: Raw text feedback

          metadata: Arbitrary JSON object for additional data

          overwrite: User corrections to span output

          rating: Numerical rating (1-5)

          rubric: Rule key-value pairs for rubric evaluation

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v5/span-assessments",
            body=await async_maybe_transform(
                {
                    "assessment_type": assessment_type,
                    "span_id": span_id,
                    "trace_id": trace_id,
                    "approval": approval,
                    "comment": comment,
                    "metadata": metadata,
                    "overwrite": overwrite,
                    "rating": rating,
                    "rubric": rubric,
                },
                span_assessment_create_params.SpanAssessmentCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SpanAssessment,
        )

    async def retrieve(
        self,
        span_assessment_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SpanAssessment:
        """
        Get an assessment by ID

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not span_assessment_id:
            raise ValueError(f"Expected a non-empty value for `span_assessment_id` but received {span_assessment_id!r}")
        return await self._get(
            path_template("/v5/span-assessments/{span_assessment_id}", span_assessment_id=span_assessment_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SpanAssessment,
        )

    async def update(
        self,
        span_assessment_id: str,
        *,
        approval: ApprovalStatus | Omit = omit,
        assessment_type: AssessmentType | Omit = omit,
        comment: str | Omit = omit,
        metadata: Dict[str, object] | Omit = omit,
        overwrite: Dict[str, object] | Omit = omit,
        rating: int | Omit = omit,
        rubric: Dict[str, str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SpanAssessment:
        """
        Update existing assessment (only by the original creator)

        Args:
          approval: Approval status (approved/rejected)

          assessment_type: Type of assessment

          comment: Raw text feedback

          metadata: Arbitrary JSON object for additional data

          overwrite: User corrections to span output

          rating: Numerical rating (1-5)

          rubric: Rule key-value pairs for rubric evaluation

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not span_assessment_id:
            raise ValueError(f"Expected a non-empty value for `span_assessment_id` but received {span_assessment_id!r}")
        return await self._patch(
            path_template("/v5/span-assessments/{span_assessment_id}", span_assessment_id=span_assessment_id),
            body=await async_maybe_transform(
                {
                    "approval": approval,
                    "assessment_type": assessment_type,
                    "comment": comment,
                    "metadata": metadata,
                    "overwrite": overwrite,
                    "rating": rating,
                    "rubric": rubric,
                },
                span_assessment_update_params.SpanAssessmentUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SpanAssessment,
        )

    def list(
        self,
        *,
        assessment_type: AssessmentType | Omit = omit,
        span_id: str | Omit = omit,
        trace_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[SpanAssessment, AsyncAPIListPage[SpanAssessment]]:
        """
        Get all assessments for a specific span or trace, optionally filtered by
        assessment type

        Args:
          assessment_type: Filter by assessment type

          span_id: Filter by span ID. Either span_id or trace_id must be provided as a query
              parameter.

          trace_id: Filter by trace ID. Either span_id or trace_id must be provided as a query
              parameter.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v5/span-assessments",
            page=AsyncAPIListPage[SpanAssessment],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "assessment_type": assessment_type,
                        "span_id": span_id,
                        "trace_id": trace_id,
                    },
                    span_assessment_list_params.SpanAssessmentListParams,
                ),
            ),
            model=SpanAssessment,
        )

    async def delete(
        self,
        span_assessment_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SpanAssessmentDeleteResponse:
        """
        Delete assessment

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not span_assessment_id:
            raise ValueError(f"Expected a non-empty value for `span_assessment_id` but received {span_assessment_id!r}")
        return await self._delete(
            path_template("/v5/span-assessments/{span_assessment_id}", span_assessment_id=span_assessment_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SpanAssessmentDeleteResponse,
        )


class SpanAssessmentsResourceWithRawResponse:
    def __init__(self, span_assessments: SpanAssessmentsResource) -> None:
        self._span_assessments = span_assessments

        self.create = to_raw_response_wrapper(
            span_assessments.create,
        )
        self.retrieve = to_raw_response_wrapper(
            span_assessments.retrieve,
        )
        self.update = to_raw_response_wrapper(
            span_assessments.update,
        )
        self.list = to_raw_response_wrapper(
            span_assessments.list,
        )
        self.delete = to_raw_response_wrapper(
            span_assessments.delete,
        )


class AsyncSpanAssessmentsResourceWithRawResponse:
    def __init__(self, span_assessments: AsyncSpanAssessmentsResource) -> None:
        self._span_assessments = span_assessments

        self.create = async_to_raw_response_wrapper(
            span_assessments.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            span_assessments.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            span_assessments.update,
        )
        self.list = async_to_raw_response_wrapper(
            span_assessments.list,
        )
        self.delete = async_to_raw_response_wrapper(
            span_assessments.delete,
        )


class SpanAssessmentsResourceWithStreamingResponse:
    def __init__(self, span_assessments: SpanAssessmentsResource) -> None:
        self._span_assessments = span_assessments

        self.create = to_streamed_response_wrapper(
            span_assessments.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            span_assessments.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            span_assessments.update,
        )
        self.list = to_streamed_response_wrapper(
            span_assessments.list,
        )
        self.delete = to_streamed_response_wrapper(
            span_assessments.delete,
        )


class AsyncSpanAssessmentsResourceWithStreamingResponse:
    def __init__(self, span_assessments: AsyncSpanAssessmentsResource) -> None:
        self._span_assessments = span_assessments

        self.create = async_to_streamed_response_wrapper(
            span_assessments.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            span_assessments.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            span_assessments.update,
        )
        self.list = async_to_streamed_response_wrapper(
            span_assessments.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            span_assessments.delete,
        )
