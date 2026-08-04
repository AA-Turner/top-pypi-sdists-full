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
        trace_id: str,
        approval: ApprovalStatus | Omit = omit,
        comment: str | Omit = omit,
        metadata: Dict[str, object] | Omit = omit,
        overwrite: Dict[str, object] | Omit = omit,
        rating: int | Omit = omit,
        rubric: Dict[str, str] | Omit = omit,
        span_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SpanAssessment:
        """
        Attach a new assessment to a span within a trace.

        A span assessment records feedback on a single span's output. Its
        assessment_type selects one of comment, rating (an integer 1-5), approval
        (approved or rejected), rubric (key-value rule pairs), metadata (arbitrary
        JSON), or overwrite (a corrected span output), and exactly the content field
        matching that type must be supplied; a free-text comment may additionally
        accompany any type. trace_id is required, while span_id is optional and, when
        omitted, the assessment is attached to the trace's root span. The call returns
        404 if the given span_id and trace_id do not identify an existing span, or if no
        root span is found for the trace. At most one user per span may hold an
        overwrite assessment, so creating an overwrite for a span another user has
        already overwritten returns 409. Use the list endpoint to read a span's or
        trace's existing assessments.

        Args:
          assessment_type: Type of assessment

          trace_id: The ID of the trace this assessment is attached to

          approval: Approval status (approved/rejected)

          comment: Raw text feedback

          metadata: Arbitrary JSON object for additional data

          overwrite: User corrections to span output

          rating: Numerical rating (1-5)

          rubric: Rule key-value pairs for rubric evaluation

          span_id: The ID of the span this assessment is attached to. If omitted, the assessment is
              attached to the root span of the trace.

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
                    "trace_id": trace_id,
                    "approval": approval,
                    "comment": comment,
                    "metadata": metadata,
                    "overwrite": overwrite,
                    "rating": rating,
                    "rubric": rubric,
                    "span_id": span_id,
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
        Retrieve a single span assessment by its identifier.

        Returns the assessment's type and content fields, the span and trace it is
        attached to, and the identity that created it. Returns 404 if no assessment with
        that id exists for the caller's account. Use the list endpoint instead when you
        have a span or trace id rather than an assessment id.

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
        Update the content of an existing span assessment.

        Only the assessment's original creator may update it; a request from any other
        identity returns 403. Supplied fields overwrite the stored values and the merged
        result is re-validated against the assessment's type, so the content must stay
        consistent with assessment_type (the matching content field present and no
        conflicting fields set) or the call returns 422. The span and trace an
        assessment is attached to cannot be changed through this endpoint. Returns 404
        if no assessment with that id exists for the caller's account.

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
        Return the assessments attached to a given span or trace.

        Results are scoped to the caller's account. Exactly one of span_id or trace_id
        must be supplied as a query parameter, and a request providing neither
        returns 400. Filtering by trace_id returns assessments across every span of that
        trace, whereas span_id returns only that span's assessments; an optional
        assessment_type narrows the results to a single type. Use the get-by-id endpoint
        when you already have a specific assessment id.

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
        Permanently delete a span assessment by its identifier.

        This is a hard delete: the assessment row is removed rather than archived, so it
        cannot be restored afterward. The response echoes the deleted assessment's id.
        Returns 404 if no assessment with that id exists for the caller's account.

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
        trace_id: str,
        approval: ApprovalStatus | Omit = omit,
        comment: str | Omit = omit,
        metadata: Dict[str, object] | Omit = omit,
        overwrite: Dict[str, object] | Omit = omit,
        rating: int | Omit = omit,
        rubric: Dict[str, str] | Omit = omit,
        span_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SpanAssessment:
        """
        Attach a new assessment to a span within a trace.

        A span assessment records feedback on a single span's output. Its
        assessment_type selects one of comment, rating (an integer 1-5), approval
        (approved or rejected), rubric (key-value rule pairs), metadata (arbitrary
        JSON), or overwrite (a corrected span output), and exactly the content field
        matching that type must be supplied; a free-text comment may additionally
        accompany any type. trace_id is required, while span_id is optional and, when
        omitted, the assessment is attached to the trace's root span. The call returns
        404 if the given span_id and trace_id do not identify an existing span, or if no
        root span is found for the trace. At most one user per span may hold an
        overwrite assessment, so creating an overwrite for a span another user has
        already overwritten returns 409. Use the list endpoint to read a span's or
        trace's existing assessments.

        Args:
          assessment_type: Type of assessment

          trace_id: The ID of the trace this assessment is attached to

          approval: Approval status (approved/rejected)

          comment: Raw text feedback

          metadata: Arbitrary JSON object for additional data

          overwrite: User corrections to span output

          rating: Numerical rating (1-5)

          rubric: Rule key-value pairs for rubric evaluation

          span_id: The ID of the span this assessment is attached to. If omitted, the assessment is
              attached to the root span of the trace.

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
                    "trace_id": trace_id,
                    "approval": approval,
                    "comment": comment,
                    "metadata": metadata,
                    "overwrite": overwrite,
                    "rating": rating,
                    "rubric": rubric,
                    "span_id": span_id,
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
        Retrieve a single span assessment by its identifier.

        Returns the assessment's type and content fields, the span and trace it is
        attached to, and the identity that created it. Returns 404 if no assessment with
        that id exists for the caller's account. Use the list endpoint instead when you
        have a span or trace id rather than an assessment id.

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
        Update the content of an existing span assessment.

        Only the assessment's original creator may update it; a request from any other
        identity returns 403. Supplied fields overwrite the stored values and the merged
        result is re-validated against the assessment's type, so the content must stay
        consistent with assessment_type (the matching content field present and no
        conflicting fields set) or the call returns 422. The span and trace an
        assessment is attached to cannot be changed through this endpoint. Returns 404
        if no assessment with that id exists for the caller's account.

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
        Return the assessments attached to a given span or trace.

        Results are scoped to the caller's account. Exactly one of span_id or trace_id
        must be supplied as a query parameter, and a request providing neither
        returns 400. Filtering by trace_id returns assessments across every span of that
        trace, whereas span_id returns only that span's assessments; an optional
        assessment_type narrows the results to a single type. Use the get-by-id endpoint
        when you already have a specific assessment id.

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
        Permanently delete a span assessment by its identifier.

        This is a hard delete: the assessment row is removed rather than archived, so it
        cannot be restored afterward. The response echoes the deleted assessment's id.
        Returns 404 if no assessment with that id exists for the caller's account.

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
