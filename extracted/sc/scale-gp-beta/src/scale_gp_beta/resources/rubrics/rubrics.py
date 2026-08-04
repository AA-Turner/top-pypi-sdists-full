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
        Create a rubric, optionally with its initial criteria in the same request.

        The rubric is created for the caller's account at version 1. If the optional
        `criteria` field is supplied it must contain at least one entry, and each entry
        is created as a criterion attached to the new rubric; omit it to create an empty
        rubric and add criteria later via the criteria endpoint. The response returns
        the created rubric together with the full detail of any criteria created in this
        call.

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
        Retrieve a single rubric with the full detail of its current criteria.

        Returns the latest version of the rubric along with all of its current
        (latest-version) criteria in full — not the slim title/weight summary returned
        by the list endpoint. Archived rubrics remain retrievable through this endpoint
        even though they are hidden from the list endpoint.

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
        Update a rubric's fields, or restore a previously archived rubric.

        The request body is a discriminated union. Send `{"restore": true}` to restore
        an archived rubric (clearing its archived state); send any other field set (such
        as `title` or `tags`) to update those fields, carrying forward any field not
        supplied. Both paths are append-only and produce a new version of the rubric
        rather than mutating the existing row. Updating the fields of an archived rubric
        is rejected — restore it first. Restoring a rubric that is not archived is a
        no-op that returns it unchanged without creating a new version.

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
        List the current account's rubrics, paginated.

        Only the latest version of each rubric is returned, and archived rubrics are
        excluded (this endpoint has no option to include them). The optional `title`
        filter matches as a case-insensitive substring, and the optional `tags` filter
        narrows results to rubrics carrying the given tags. Each returned rubric carries
        only a slim criteria summary (title and weight per criterion) rather than full
        criteria; use the get-rubric endpoint to retrieve full criteria detail.

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
        Archive a rubric (soft delete).

        This is a soft delete, not a permanent one: it records an archived timestamp on
        the rubric while retaining the rubric and its version history, so it can later
        be brought back via the restore variant of the update endpoint. An archived
        rubric is hidden from the list endpoint but stays retrievable by id. The
        rubric's criteria are left untouched — archiving does not cascade to or delete
        them. Archiving a rubric that is already archived is rejected.

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
        Create a rubric, optionally with its initial criteria in the same request.

        The rubric is created for the caller's account at version 1. If the optional
        `criteria` field is supplied it must contain at least one entry, and each entry
        is created as a criterion attached to the new rubric; omit it to create an empty
        rubric and add criteria later via the criteria endpoint. The response returns
        the created rubric together with the full detail of any criteria created in this
        call.

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
        Retrieve a single rubric with the full detail of its current criteria.

        Returns the latest version of the rubric along with all of its current
        (latest-version) criteria in full — not the slim title/weight summary returned
        by the list endpoint. Archived rubrics remain retrievable through this endpoint
        even though they are hidden from the list endpoint.

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
        Update a rubric's fields, or restore a previously archived rubric.

        The request body is a discriminated union. Send `{"restore": true}` to restore
        an archived rubric (clearing its archived state); send any other field set (such
        as `title` or `tags`) to update those fields, carrying forward any field not
        supplied. Both paths are append-only and produce a new version of the rubric
        rather than mutating the existing row. Updating the fields of an archived rubric
        is rejected — restore it first. Restoring a rubric that is not archived is a
        no-op that returns it unchanged without creating a new version.

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
        List the current account's rubrics, paginated.

        Only the latest version of each rubric is returned, and archived rubrics are
        excluded (this endpoint has no option to include them). The optional `title`
        filter matches as a case-insensitive substring, and the optional `tags` filter
        narrows results to rubrics carrying the given tags. Each returned rubric carries
        only a slim criteria summary (title and weight per criterion) rather than full
        criteria; use the get-rubric endpoint to retrieve full criteria detail.

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
        Archive a rubric (soft delete).

        This is a soft delete, not a permanent one: it records an archived timestamp on
        the rubric while retaining the rubric and its version history, so it can later
        be brought back via the restore variant of the update endpoint. An archived
        rubric is hidden from the list endpoint but stays retrievable by id. The
        rubric's criteria are left untouched — archiving does not cascade to or delete
        them. Archiving a rubric that is already archived is rejected.

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
