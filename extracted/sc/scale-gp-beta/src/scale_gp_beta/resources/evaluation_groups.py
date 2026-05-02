# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, List

import httpx

from ..types import (
    evaluation_group_list_params,
    evaluation_group_create_params,
    evaluation_group_update_params,
    evaluation_group_replace_params,
    evaluation_group_retrieve_params,
    evaluation_group_retrieve_schema_params,
)
from .._types import Body, Omit, Query, Headers, NotGiven, SequenceNotStr, omit, not_given
from .._utils import path_template, maybe_transform, async_maybe_transform
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..pagination import SyncCursorPage, AsyncCursorPage
from ..types.chat import SortOrder
from .._base_client import AsyncPaginator, make_request_options
from ..types.chat.sort_order import SortOrder
from ..types.evaluation_group import EvaluationGroup
from ..types.evaluation_group_views import EvaluationGroupViews
from ..types.evaluation_group_retrieve_schema_response import EvaluationGroupRetrieveSchemaResponse

__all__ = ["EvaluationGroupsResource", "AsyncEvaluationGroupsResource"]


class EvaluationGroupsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> EvaluationGroupsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python-beta#accessing-raw-response-data-eg-headers
        """
        return EvaluationGroupsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> EvaluationGroupsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python-beta#with_streaming_response
        """
        return EvaluationGroupsResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        evaluation_ids: SequenceNotStr[str],
        name: str,
        description: str | Omit = omit,
        metadata: Dict[str, object] | Omit = omit,
        row_identifiers: Dict[str, str] | Omit = omit,
        tags: SequenceNotStr[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> EvaluationGroup:
        """
        Create a new evaluation group

        Args:
          evaluation_ids: List of evaluation IDs to include in the group

          name: Name of the evaluation group

          description: Optional description

          metadata: Optional metadata key-value pairs

          row_identifiers: Optional mapping of evaluation_id to column name for cross-dataset joins

          tags: The tags associated with the entity

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v5/evaluation-groups",
            body=maybe_transform(
                {
                    "evaluation_ids": evaluation_ids,
                    "name": name,
                    "description": description,
                    "metadata": metadata,
                    "row_identifiers": row_identifiers,
                    "tags": tags,
                },
                evaluation_group_create_params.EvaluationGroupCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EvaluationGroup,
        )

    def retrieve(
        self,
        group_id: str,
        *,
        include_deleted: bool | Omit = omit,
        views: List[EvaluationGroupViews] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> EvaluationGroup:
        """
        Get a single evaluation group by ID

        Args:
          views: Optional relationships to include: 'members', 'row_identifiers'

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not group_id:
            raise ValueError(f"Expected a non-empty value for `group_id` but received {group_id!r}")
        return self._get(
            path_template("/v5/evaluation-groups/{group_id}", group_id=group_id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "include_deleted": include_deleted,
                        "views": views,
                    },
                    evaluation_group_retrieve_params.EvaluationGroupRetrieveParams,
                ),
            ),
            cast_to=EvaluationGroup,
        )

    def update(
        self,
        group_id: str,
        *,
        description: str | Omit = omit,
        metadata: Dict[str, object] | Omit = omit,
        name: str | Omit = omit,
        row_identifiers: Dict[str, str] | Omit = omit,
        tags: SequenceNotStr[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> EvaluationGroup:
        """
        Partial update of evaluation group attributes (name, description, tags,
        metadata). Members cannot be modified via PATCH.

        Args:
          description: Optional description

          metadata: Optional metadata key-value pairs

          name: Name of the evaluation group

          row_identifiers: Optional mapping of evaluation_id to column name for cross-dataset joins

          tags: The tags associated with the entity

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not group_id:
            raise ValueError(f"Expected a non-empty value for `group_id` but received {group_id!r}")
        return self._patch(
            path_template("/v5/evaluation-groups/{group_id}", group_id=group_id),
            body=maybe_transform(
                {
                    "description": description,
                    "metadata": metadata,
                    "name": name,
                    "row_identifiers": row_identifiers,
                    "tags": tags,
                },
                evaluation_group_update_params.EvaluationGroupUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EvaluationGroup,
        )

    def list(
        self,
        *,
        ending_before: str | Omit = omit,
        evaluation_id: str | Omit = omit,
        include_deleted: bool | Omit = omit,
        limit: int | Omit = omit,
        name: str | Omit = omit,
        sort_by: str | Omit = omit,
        sort_order: SortOrder | Omit = omit,
        starting_after: str | Omit = omit,
        tags: SequenceNotStr[str] | Omit = omit,
        views: List[EvaluationGroupViews] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SyncCursorPage[EvaluationGroup]:
        """
        List all evaluation groups for the current account

        Args:
          evaluation_id: Filter to groups containing this evaluation ID

          views: Optional relationships to include: 'members', 'row_identifiers'

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v5/evaluation-groups",
            page=SyncCursorPage[EvaluationGroup],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "ending_before": ending_before,
                        "evaluation_id": evaluation_id,
                        "include_deleted": include_deleted,
                        "limit": limit,
                        "name": name,
                        "sort_by": sort_by,
                        "sort_order": sort_order,
                        "starting_after": starting_after,
                        "tags": tags,
                        "views": views,
                    },
                    evaluation_group_list_params.EvaluationGroupListParams,
                ),
            ),
            model=EvaluationGroup,
        )

    def archive(
        self,
        group_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> EvaluationGroup:
        """
        Soft-delete an evaluation group and cascade to members, row identifiers, and
        charts

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not group_id:
            raise ValueError(f"Expected a non-empty value for `group_id` but received {group_id!r}")
        return self._delete(
            path_template("/v5/evaluation-groups/{group_id}", group_id=group_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EvaluationGroup,
        )

    def replace(
        self,
        group_id: str,
        *,
        description: str | Omit = omit,
        evaluation_ids: SequenceNotStr[str] | Omit = omit,
        metadata: Dict[str, object] | Omit = omit,
        name: str | Omit = omit,
        row_identifiers: Dict[str, str] | Omit = omit,
        tags: SequenceNotStr[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> EvaluationGroup:
        """Full update of evaluation group.

        All fields are replaced with provided values.
        Omitted optional fields are cleared.

        Args:
          description: Optional description

          evaluation_ids: Complete list of evaluation IDs to include in group (replaces existing members)

          metadata: Optional metadata key-value pairs

          name: Name of the evaluation group

          row_identifiers: Optional mapping of evaluation_id to column name for cross-dataset joins

          tags: The tags associated with the entity

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not group_id:
            raise ValueError(f"Expected a non-empty value for `group_id` but received {group_id!r}")
        return self._put(
            path_template("/v5/evaluation-groups/{group_id}", group_id=group_id),
            body=maybe_transform(
                {
                    "description": description,
                    "evaluation_ids": evaluation_ids,
                    "metadata": metadata,
                    "name": name,
                    "row_identifiers": row_identifiers,
                    "tags": tags,
                },
                evaluation_group_replace_params.EvaluationGroupReplaceParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EvaluationGroup,
        )

    def retrieve_schema(
        self,
        group_id: str,
        *,
        include_archived: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> EvaluationGroupRetrieveSchemaResponse:
        """Get per-evaluation schemas for all members of a group.

        Returns individual schema
        for each member evaluation, enabling the frontend to filter columns by selected
        eval subset.

        Args:
          include_archived: Include archived items in schema analysis

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not group_id:
            raise ValueError(f"Expected a non-empty value for `group_id` but received {group_id!r}")
        return self._get(
            path_template("/v5/evaluation-groups/{group_id}/schema", group_id=group_id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {"include_archived": include_archived},
                    evaluation_group_retrieve_schema_params.EvaluationGroupRetrieveSchemaParams,
                ),
            ),
            cast_to=EvaluationGroupRetrieveSchemaResponse,
        )


class AsyncEvaluationGroupsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncEvaluationGroupsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python-beta#accessing-raw-response-data-eg-headers
        """
        return AsyncEvaluationGroupsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncEvaluationGroupsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python-beta#with_streaming_response
        """
        return AsyncEvaluationGroupsResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        evaluation_ids: SequenceNotStr[str],
        name: str,
        description: str | Omit = omit,
        metadata: Dict[str, object] | Omit = omit,
        row_identifiers: Dict[str, str] | Omit = omit,
        tags: SequenceNotStr[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> EvaluationGroup:
        """
        Create a new evaluation group

        Args:
          evaluation_ids: List of evaluation IDs to include in the group

          name: Name of the evaluation group

          description: Optional description

          metadata: Optional metadata key-value pairs

          row_identifiers: Optional mapping of evaluation_id to column name for cross-dataset joins

          tags: The tags associated with the entity

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v5/evaluation-groups",
            body=await async_maybe_transform(
                {
                    "evaluation_ids": evaluation_ids,
                    "name": name,
                    "description": description,
                    "metadata": metadata,
                    "row_identifiers": row_identifiers,
                    "tags": tags,
                },
                evaluation_group_create_params.EvaluationGroupCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EvaluationGroup,
        )

    async def retrieve(
        self,
        group_id: str,
        *,
        include_deleted: bool | Omit = omit,
        views: List[EvaluationGroupViews] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> EvaluationGroup:
        """
        Get a single evaluation group by ID

        Args:
          views: Optional relationships to include: 'members', 'row_identifiers'

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not group_id:
            raise ValueError(f"Expected a non-empty value for `group_id` but received {group_id!r}")
        return await self._get(
            path_template("/v5/evaluation-groups/{group_id}", group_id=group_id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "include_deleted": include_deleted,
                        "views": views,
                    },
                    evaluation_group_retrieve_params.EvaluationGroupRetrieveParams,
                ),
            ),
            cast_to=EvaluationGroup,
        )

    async def update(
        self,
        group_id: str,
        *,
        description: str | Omit = omit,
        metadata: Dict[str, object] | Omit = omit,
        name: str | Omit = omit,
        row_identifiers: Dict[str, str] | Omit = omit,
        tags: SequenceNotStr[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> EvaluationGroup:
        """
        Partial update of evaluation group attributes (name, description, tags,
        metadata). Members cannot be modified via PATCH.

        Args:
          description: Optional description

          metadata: Optional metadata key-value pairs

          name: Name of the evaluation group

          row_identifiers: Optional mapping of evaluation_id to column name for cross-dataset joins

          tags: The tags associated with the entity

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not group_id:
            raise ValueError(f"Expected a non-empty value for `group_id` but received {group_id!r}")
        return await self._patch(
            path_template("/v5/evaluation-groups/{group_id}", group_id=group_id),
            body=await async_maybe_transform(
                {
                    "description": description,
                    "metadata": metadata,
                    "name": name,
                    "row_identifiers": row_identifiers,
                    "tags": tags,
                },
                evaluation_group_update_params.EvaluationGroupUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EvaluationGroup,
        )

    def list(
        self,
        *,
        ending_before: str | Omit = omit,
        evaluation_id: str | Omit = omit,
        include_deleted: bool | Omit = omit,
        limit: int | Omit = omit,
        name: str | Omit = omit,
        sort_by: str | Omit = omit,
        sort_order: SortOrder | Omit = omit,
        starting_after: str | Omit = omit,
        tags: SequenceNotStr[str] | Omit = omit,
        views: List[EvaluationGroupViews] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[EvaluationGroup, AsyncCursorPage[EvaluationGroup]]:
        """
        List all evaluation groups for the current account

        Args:
          evaluation_id: Filter to groups containing this evaluation ID

          views: Optional relationships to include: 'members', 'row_identifiers'

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v5/evaluation-groups",
            page=AsyncCursorPage[EvaluationGroup],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "ending_before": ending_before,
                        "evaluation_id": evaluation_id,
                        "include_deleted": include_deleted,
                        "limit": limit,
                        "name": name,
                        "sort_by": sort_by,
                        "sort_order": sort_order,
                        "starting_after": starting_after,
                        "tags": tags,
                        "views": views,
                    },
                    evaluation_group_list_params.EvaluationGroupListParams,
                ),
            ),
            model=EvaluationGroup,
        )

    async def archive(
        self,
        group_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> EvaluationGroup:
        """
        Soft-delete an evaluation group and cascade to members, row identifiers, and
        charts

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not group_id:
            raise ValueError(f"Expected a non-empty value for `group_id` but received {group_id!r}")
        return await self._delete(
            path_template("/v5/evaluation-groups/{group_id}", group_id=group_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EvaluationGroup,
        )

    async def replace(
        self,
        group_id: str,
        *,
        description: str | Omit = omit,
        evaluation_ids: SequenceNotStr[str] | Omit = omit,
        metadata: Dict[str, object] | Omit = omit,
        name: str | Omit = omit,
        row_identifiers: Dict[str, str] | Omit = omit,
        tags: SequenceNotStr[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> EvaluationGroup:
        """Full update of evaluation group.

        All fields are replaced with provided values.
        Omitted optional fields are cleared.

        Args:
          description: Optional description

          evaluation_ids: Complete list of evaluation IDs to include in group (replaces existing members)

          metadata: Optional metadata key-value pairs

          name: Name of the evaluation group

          row_identifiers: Optional mapping of evaluation_id to column name for cross-dataset joins

          tags: The tags associated with the entity

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not group_id:
            raise ValueError(f"Expected a non-empty value for `group_id` but received {group_id!r}")
        return await self._put(
            path_template("/v5/evaluation-groups/{group_id}", group_id=group_id),
            body=await async_maybe_transform(
                {
                    "description": description,
                    "evaluation_ids": evaluation_ids,
                    "metadata": metadata,
                    "name": name,
                    "row_identifiers": row_identifiers,
                    "tags": tags,
                },
                evaluation_group_replace_params.EvaluationGroupReplaceParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EvaluationGroup,
        )

    async def retrieve_schema(
        self,
        group_id: str,
        *,
        include_archived: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> EvaluationGroupRetrieveSchemaResponse:
        """Get per-evaluation schemas for all members of a group.

        Returns individual schema
        for each member evaluation, enabling the frontend to filter columns by selected
        eval subset.

        Args:
          include_archived: Include archived items in schema analysis

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not group_id:
            raise ValueError(f"Expected a non-empty value for `group_id` but received {group_id!r}")
        return await self._get(
            path_template("/v5/evaluation-groups/{group_id}/schema", group_id=group_id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {"include_archived": include_archived},
                    evaluation_group_retrieve_schema_params.EvaluationGroupRetrieveSchemaParams,
                ),
            ),
            cast_to=EvaluationGroupRetrieveSchemaResponse,
        )


class EvaluationGroupsResourceWithRawResponse:
    def __init__(self, evaluation_groups: EvaluationGroupsResource) -> None:
        self._evaluation_groups = evaluation_groups

        self.create = to_raw_response_wrapper(
            evaluation_groups.create,
        )
        self.retrieve = to_raw_response_wrapper(
            evaluation_groups.retrieve,
        )
        self.update = to_raw_response_wrapper(
            evaluation_groups.update,
        )
        self.list = to_raw_response_wrapper(
            evaluation_groups.list,
        )
        self.archive = to_raw_response_wrapper(
            evaluation_groups.archive,
        )
        self.replace = to_raw_response_wrapper(
            evaluation_groups.replace,
        )
        self.retrieve_schema = to_raw_response_wrapper(
            evaluation_groups.retrieve_schema,
        )


class AsyncEvaluationGroupsResourceWithRawResponse:
    def __init__(self, evaluation_groups: AsyncEvaluationGroupsResource) -> None:
        self._evaluation_groups = evaluation_groups

        self.create = async_to_raw_response_wrapper(
            evaluation_groups.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            evaluation_groups.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            evaluation_groups.update,
        )
        self.list = async_to_raw_response_wrapper(
            evaluation_groups.list,
        )
        self.archive = async_to_raw_response_wrapper(
            evaluation_groups.archive,
        )
        self.replace = async_to_raw_response_wrapper(
            evaluation_groups.replace,
        )
        self.retrieve_schema = async_to_raw_response_wrapper(
            evaluation_groups.retrieve_schema,
        )


class EvaluationGroupsResourceWithStreamingResponse:
    def __init__(self, evaluation_groups: EvaluationGroupsResource) -> None:
        self._evaluation_groups = evaluation_groups

        self.create = to_streamed_response_wrapper(
            evaluation_groups.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            evaluation_groups.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            evaluation_groups.update,
        )
        self.list = to_streamed_response_wrapper(
            evaluation_groups.list,
        )
        self.archive = to_streamed_response_wrapper(
            evaluation_groups.archive,
        )
        self.replace = to_streamed_response_wrapper(
            evaluation_groups.replace,
        )
        self.retrieve_schema = to_streamed_response_wrapper(
            evaluation_groups.retrieve_schema,
        )


class AsyncEvaluationGroupsResourceWithStreamingResponse:
    def __init__(self, evaluation_groups: AsyncEvaluationGroupsResource) -> None:
        self._evaluation_groups = evaluation_groups

        self.create = async_to_streamed_response_wrapper(
            evaluation_groups.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            evaluation_groups.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            evaluation_groups.update,
        )
        self.list = async_to_streamed_response_wrapper(
            evaluation_groups.list,
        )
        self.archive = async_to_streamed_response_wrapper(
            evaluation_groups.archive,
        )
        self.replace = async_to_streamed_response_wrapper(
            evaluation_groups.replace,
        )
        self.retrieve_schema = async_to_streamed_response_wrapper(
            evaluation_groups.retrieve_schema,
        )
