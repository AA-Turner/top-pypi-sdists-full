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
        Create a new evaluation group bundling one or more existing evaluations.

        The request must list at least one evaluation ID, and duplicate IDs are
        rejected. Every listed evaluation is validated for existence and account access
        before the group is created; an unknown or inaccessible evaluation ID fails the
        whole request with a 400 rather than creating a partial group. The named
        evaluations are added as group members in the same transaction, and any supplied
        row_identifiers (an evaluation_id-to-column-name mapping used for cross-dataset
        joins) are persisted alongside them, ignoring entries for evaluation IDs not in
        the group. The returned group includes its members enriched with each
        evaluation's name, tags, and creation time. Unlike the PUT and PATCH update
        endpoints, creation does not trigger any dashboard-widget recomputation.

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
        Fetch a single evaluation group by its ID.

        By default only non-archived groups are returned; set include_deleted to also
        resolve a soft-deleted group. The views parameter optionally expands the
        response with the group's members and/or row_identifiers, and when members are
        loaded they are enriched with each member evaluation's name, tags, and creation
        time. Use the schema endpoint instead when you need the per-evaluation column
        schemas of the group's members.

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
        Partially update an evaluation group's attributes.

        Only the fields present in the request are changed; unset fields are left
        untouched. Unlike the PUT endpoint, metadata is merged into the existing
        metadata key-by-key rather than replaced wholesale, and group membership
        (evaluation_ids) cannot be changed here -- use PUT to replace members. At least
        one field must be supplied or the request fails with a 400. Supplying
        row_identifiers replaces the group's entire row identifier set (an
        evaluation_id-to-column-name mapping for cross-dataset joins); passing an empty
        mapping clears it.

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
        List the calling account's evaluation groups with optional filters.

        Results are paginated and scoped to the authenticated account. The optional
        filters combine with AND semantics: name does a case-insensitive partial
        (substring) match on the group name, tags returns only groups whose tag list
        contains all of the supplied tags, and evaluation_id returns only groups that
        have the given evaluation as an active member. By default archived
        (soft-deleted) groups are excluded; set include_deleted to include them. The
        views parameter optionally expands each group with its members and/or
        row_identifiers, and returned members are enriched with each evaluation's name,
        tags, and creation time.

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
        Archive (soft-delete) an evaluation group and its dependent records.

        This is a soft delete: the group is marked deleted rather than removed, so it no
        longer appears in default list/get results but can still be fetched with the
        include-deleted flags. The same delete timestamp cascades as a soft delete to
        the group's members, row identifiers, and its dashboard charts and their chart
        columns; the member evaluations themselves are not affected. The archived group
        is returned in the response.

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
        """
        Replace an evaluation group's attributes and, optionally, its membership.

        This is a full replacement of the group's attributes: every attribute field
        (name, description, tags, metadata) is written from the request, so omitting an
        optional field clears it rather than leaving it unchanged. Use PATCH instead to
        update only selected fields and to merge (rather than overwrite) metadata.
        Membership is replaced only when evaluation_ids is supplied: the resulting
        members become exactly that set (added/removed by diff against the current
        members), it must contain at least one ID with no duplicates, and every ID is
        validated for existence and account access or the request fails with a 400. When
        membership actually changes, a best-effort Temporal workflow is started to
        recompute the group's dashboard widgets; this is fire-and-forget and its failure
        does not fail the request. Removing members hard-deletes the corresponding chart
        columns and any charts left with no columns.

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
        """
        Return a separate column schema for each active member evaluation of the group.

        Rather than a single merged schema, the response holds one schema entry per
        active member evaluation (each with its field list, total item count, and
        sampling info), which lets a caller filter columns down to a chosen subset of
        the group's evaluations. Schemas are computed from the member evaluations'
        items; include_archived controls whether archived items are counted in that
        analysis. A group with no active members returns an empty schema list. This
        differs from the plain get endpoint, which returns group metadata and members
        but not their column schemas.

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
        Create a new evaluation group bundling one or more existing evaluations.

        The request must list at least one evaluation ID, and duplicate IDs are
        rejected. Every listed evaluation is validated for existence and account access
        before the group is created; an unknown or inaccessible evaluation ID fails the
        whole request with a 400 rather than creating a partial group. The named
        evaluations are added as group members in the same transaction, and any supplied
        row_identifiers (an evaluation_id-to-column-name mapping used for cross-dataset
        joins) are persisted alongside them, ignoring entries for evaluation IDs not in
        the group. The returned group includes its members enriched with each
        evaluation's name, tags, and creation time. Unlike the PUT and PATCH update
        endpoints, creation does not trigger any dashboard-widget recomputation.

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
        Fetch a single evaluation group by its ID.

        By default only non-archived groups are returned; set include_deleted to also
        resolve a soft-deleted group. The views parameter optionally expands the
        response with the group's members and/or row_identifiers, and when members are
        loaded they are enriched with each member evaluation's name, tags, and creation
        time. Use the schema endpoint instead when you need the per-evaluation column
        schemas of the group's members.

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
        Partially update an evaluation group's attributes.

        Only the fields present in the request are changed; unset fields are left
        untouched. Unlike the PUT endpoint, metadata is merged into the existing
        metadata key-by-key rather than replaced wholesale, and group membership
        (evaluation_ids) cannot be changed here -- use PUT to replace members. At least
        one field must be supplied or the request fails with a 400. Supplying
        row_identifiers replaces the group's entire row identifier set (an
        evaluation_id-to-column-name mapping for cross-dataset joins); passing an empty
        mapping clears it.

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
        List the calling account's evaluation groups with optional filters.

        Results are paginated and scoped to the authenticated account. The optional
        filters combine with AND semantics: name does a case-insensitive partial
        (substring) match on the group name, tags returns only groups whose tag list
        contains all of the supplied tags, and evaluation_id returns only groups that
        have the given evaluation as an active member. By default archived
        (soft-deleted) groups are excluded; set include_deleted to include them. The
        views parameter optionally expands each group with its members and/or
        row_identifiers, and returned members are enriched with each evaluation's name,
        tags, and creation time.

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
        Archive (soft-delete) an evaluation group and its dependent records.

        This is a soft delete: the group is marked deleted rather than removed, so it no
        longer appears in default list/get results but can still be fetched with the
        include-deleted flags. The same delete timestamp cascades as a soft delete to
        the group's members, row identifiers, and its dashboard charts and their chart
        columns; the member evaluations themselves are not affected. The archived group
        is returned in the response.

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
        """
        Replace an evaluation group's attributes and, optionally, its membership.

        This is a full replacement of the group's attributes: every attribute field
        (name, description, tags, metadata) is written from the request, so omitting an
        optional field clears it rather than leaving it unchanged. Use PATCH instead to
        update only selected fields and to merge (rather than overwrite) metadata.
        Membership is replaced only when evaluation_ids is supplied: the resulting
        members become exactly that set (added/removed by diff against the current
        members), it must contain at least one ID with no duplicates, and every ID is
        validated for existence and account access or the request fails with a 400. When
        membership actually changes, a best-effort Temporal workflow is started to
        recompute the group's dashboard widgets; this is fire-and-forget and its failure
        does not fail the request. Removing members hard-deletes the corresponding chart
        columns and any charts left with no columns.

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
        """
        Return a separate column schema for each active member evaluation of the group.

        Rather than a single merged schema, the response holds one schema entry per
        active member evaluation (each with its field list, total item count, and
        sampling info), which lets a caller filter columns down to a chosen subset of
        the group's evaluations. Schemas are computed from the member evaluations'
        items; include_archived controls whether archived items are counted in that
        analysis. A group with no active members returns an empty schema list. This
        differs from the plain get endpoint, which returns group metadata and members
        but not their column schemas.

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
