# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable

import httpx

from ...types import rubric_list_params, rubric_create_params, rubric_update_params
from ..._types import Body, Omit, Query, Headers, NotGiven, SequenceNotStr, omit, not_given
from ..._utils import path_template, maybe_transform, async_maybe_transform
from .criteria import (
    CriteriaResource,
    AsyncCriteriaResource,
    CriteriaResourceWithRawResponse,
    AsyncCriteriaResourceWithRawResponse,
    CriteriaResourceWithStreamingResponse,
    AsyncCriteriaResourceWithStreamingResponse,
)
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ...pagination import SyncCursorPage, AsyncCursorPage
from ...types.chat import SortOrder
from ..._base_client import AsyncPaginator, make_request_options
from ...types.chat.sort_order import SortOrder
from ...types.rubric_response import RubricResponse
from ...types.rubric_archive_response import RubricArchiveResponse
from ...types.rubrics.rubric_criteria_input_param import RubricCriteriaInputParam

__all__ = ["RubricsResource", "AsyncRubricsResource"]


class RubricsResource(SyncAPIResource):
    @cached_property
    def criteria(self) -> CriteriaResource:
        return CriteriaResource(self._client)

    @cached_property
    def with_raw_response(self) -> RubricsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python-beta#accessing-raw-response-data-eg-headers
        """
        return RubricsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> RubricsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python-beta#with_streaming_response
        """
        return RubricsResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        title: str,
        criteria: Iterable[RubricCriteriaInputParam] | Omit = omit,
        tags: SequenceNotStr[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> RubricResponse:
        """
        Create Rubric

        Args:
          title: The rubric title

          criteria: Initial criteria to create with the rubric

          tags: The tags associated with the entity

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v5/rubrics",
            body=maybe_transform(
                {
                    "title": title,
                    "criteria": criteria,
                    "tags": tags,
                },
                rubric_create_params.RubricCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=RubricResponse,
        )

    def retrieve(
        self,
        rubric_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> RubricResponse:
        """
        Get Rubric

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not rubric_id:
            raise ValueError(f"Expected a non-empty value for `rubric_id` but received {rubric_id!r}")
        return self._get(
            path_template("/v5/rubrics/{rubric_id}", rubric_id=rubric_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=RubricResponse,
        )

    def update(
        self,
        rubric_id: str,
        *,
        rubric: rubric_update_params.Rubric,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> RubricResponse:
        """
        Update or Restore Rubric

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not rubric_id:
            raise ValueError(f"Expected a non-empty value for `rubric_id` but received {rubric_id!r}")
        return self._patch(
            path_template("/v5/rubrics/{rubric_id}", rubric_id=rubric_id),
            body=maybe_transform(rubric, rubric_update_params.RubricUpdateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=RubricResponse,
        )

    def list(
        self,
        *,
        ending_before: str | Omit = omit,
        limit: int | Omit = omit,
        sort_by: str | Omit = omit,
        sort_order: SortOrder | Omit = omit,
        starting_after: str | Omit = omit,
        tags: SequenceNotStr[str] | Omit = omit,
        title: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SyncCursorPage[RubricResponse]:
        """
        List Rubrics

        Args:
          tags: Filter by tags

          title: Filter by title (case-insensitive)

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v5/rubrics",
            page=SyncCursorPage[RubricResponse],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "ending_before": ending_before,
                        "limit": limit,
                        "sort_by": sort_by,
                        "sort_order": sort_order,
                        "starting_after": starting_after,
                        "tags": tags,
                        "title": title,
                    },
                    rubric_list_params.RubricListParams,
                ),
            ),
            model=RubricResponse,
        )

    def archive(
        self,
        rubric_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> RubricArchiveResponse:
        """
        Archive Rubric

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not rubric_id:
            raise ValueError(f"Expected a non-empty value for `rubric_id` but received {rubric_id!r}")
        return self._delete(
            path_template("/v5/rubrics/{rubric_id}", rubric_id=rubric_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=RubricArchiveResponse,
        )


class AsyncRubricsResource(AsyncAPIResource):
    @cached_property
    def criteria(self) -> AsyncCriteriaResource:
        return AsyncCriteriaResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncRubricsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python-beta#accessing-raw-response-data-eg-headers
        """
        return AsyncRubricsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncRubricsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python-beta#with_streaming_response
        """
        return AsyncRubricsResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        title: str,
        criteria: Iterable[RubricCriteriaInputParam] | Omit = omit,
        tags: SequenceNotStr[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> RubricResponse:
        """
        Create Rubric

        Args:
          title: The rubric title

          criteria: Initial criteria to create with the rubric

          tags: The tags associated with the entity

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v5/rubrics",
            body=await async_maybe_transform(
                {
                    "title": title,
                    "criteria": criteria,
                    "tags": tags,
                },
                rubric_create_params.RubricCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=RubricResponse,
        )

    async def retrieve(
        self,
        rubric_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> RubricResponse:
        """
        Get Rubric

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not rubric_id:
            raise ValueError(f"Expected a non-empty value for `rubric_id` but received {rubric_id!r}")
        return await self._get(
            path_template("/v5/rubrics/{rubric_id}", rubric_id=rubric_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=RubricResponse,
        )

    async def update(
        self,
        rubric_id: str,
        *,
        rubric: rubric_update_params.Rubric,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> RubricResponse:
        """
        Update or Restore Rubric

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not rubric_id:
            raise ValueError(f"Expected a non-empty value for `rubric_id` but received {rubric_id!r}")
        return await self._patch(
            path_template("/v5/rubrics/{rubric_id}", rubric_id=rubric_id),
            body=await async_maybe_transform(rubric, rubric_update_params.RubricUpdateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=RubricResponse,
        )

    def list(
        self,
        *,
        ending_before: str | Omit = omit,
        limit: int | Omit = omit,
        sort_by: str | Omit = omit,
        sort_order: SortOrder | Omit = omit,
        starting_after: str | Omit = omit,
        tags: SequenceNotStr[str] | Omit = omit,
        title: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[RubricResponse, AsyncCursorPage[RubricResponse]]:
        """
        List Rubrics

        Args:
          tags: Filter by tags

          title: Filter by title (case-insensitive)

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v5/rubrics",
            page=AsyncCursorPage[RubricResponse],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "ending_before": ending_before,
                        "limit": limit,
                        "sort_by": sort_by,
                        "sort_order": sort_order,
                        "starting_after": starting_after,
                        "tags": tags,
                        "title": title,
                    },
                    rubric_list_params.RubricListParams,
                ),
            ),
            model=RubricResponse,
        )

    async def archive(
        self,
        rubric_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> RubricArchiveResponse:
        """
        Archive Rubric

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not rubric_id:
            raise ValueError(f"Expected a non-empty value for `rubric_id` but received {rubric_id!r}")
        return await self._delete(
            path_template("/v5/rubrics/{rubric_id}", rubric_id=rubric_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=RubricArchiveResponse,
        )


class RubricsResourceWithRawResponse:
    def __init__(self, rubrics: RubricsResource) -> None:
        self._rubrics = rubrics

        self.create = to_raw_response_wrapper(
            rubrics.create,
        )
        self.retrieve = to_raw_response_wrapper(
            rubrics.retrieve,
        )
        self.update = to_raw_response_wrapper(
            rubrics.update,
        )
        self.list = to_raw_response_wrapper(
            rubrics.list,
        )
        self.archive = to_raw_response_wrapper(
            rubrics.archive,
        )

    @cached_property
    def criteria(self) -> CriteriaResourceWithRawResponse:
        return CriteriaResourceWithRawResponse(self._rubrics.criteria)


class AsyncRubricsResourceWithRawResponse:
    def __init__(self, rubrics: AsyncRubricsResource) -> None:
        self._rubrics = rubrics

        self.create = async_to_raw_response_wrapper(
            rubrics.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            rubrics.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            rubrics.update,
        )
        self.list = async_to_raw_response_wrapper(
            rubrics.list,
        )
        self.archive = async_to_raw_response_wrapper(
            rubrics.archive,
        )

    @cached_property
    def criteria(self) -> AsyncCriteriaResourceWithRawResponse:
        return AsyncCriteriaResourceWithRawResponse(self._rubrics.criteria)


class RubricsResourceWithStreamingResponse:
    def __init__(self, rubrics: RubricsResource) -> None:
        self._rubrics = rubrics

        self.create = to_streamed_response_wrapper(
            rubrics.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            rubrics.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            rubrics.update,
        )
        self.list = to_streamed_response_wrapper(
            rubrics.list,
        )
        self.archive = to_streamed_response_wrapper(
            rubrics.archive,
        )

    @cached_property
    def criteria(self) -> CriteriaResourceWithStreamingResponse:
        return CriteriaResourceWithStreamingResponse(self._rubrics.criteria)


class AsyncRubricsResourceWithStreamingResponse:
    def __init__(self, rubrics: AsyncRubricsResource) -> None:
        self._rubrics = rubrics

        self.create = async_to_streamed_response_wrapper(
            rubrics.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            rubrics.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            rubrics.update,
        )
        self.list = async_to_streamed_response_wrapper(
            rubrics.list,
        )
        self.archive = async_to_streamed_response_wrapper(
            rubrics.archive,
        )

    @cached_property
    def criteria(self) -> AsyncCriteriaResourceWithStreamingResponse:
        return AsyncCriteriaResourceWithStreamingResponse(self._rubrics.criteria)
