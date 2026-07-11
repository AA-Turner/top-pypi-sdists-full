# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Iterable

import httpx

from .tasks import (
    TasksResource,
    AsyncTasksResource,
    TasksResourceWithRawResponse,
    AsyncTasksResourceWithRawResponse,
    TasksResourceWithStreamingResponse,
    AsyncTasksResourceWithStreamingResponse,
)
from ...types import (
    evaluation_list_params,
    evaluation_create_params,
    evaluation_filter_params,
    evaluation_update_params,
    evaluation_retrieve_params,
    evaluation_retrieve_schema_params,
)
from ..._types import Body, Omit, Query, Headers, NotGiven, SequenceNotStr, omit, not_given
from ..._utils import path_template, maybe_transform, async_maybe_transform
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
from ...types.evaluation import Evaluation
from ...types.chat.sort_order import SortOrder
from ...types.evaluation_views import EvaluationViews
from ...types.evaluation_schema_response import EvaluationSchemaResponse
from ...types.evaluation_retrieve_taxonomy_response import EvaluationRetrieveTaxonomyResponse

__all__ = ["EvaluationsResource", "AsyncEvaluationsResource"]


class EvaluationsResource(SyncAPIResource):
    @cached_property
    def tasks(self) -> TasksResource:
        return TasksResource(self._client)

    @cached_property
    def with_raw_response(self) -> EvaluationsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python-beta#accessing-raw-response-data-eg-headers
        """
        return EvaluationsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> EvaluationsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python-beta#with_streaming_response
        """
        return EvaluationsResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        evaluation: evaluation_create_params.Evaluation,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Evaluation:
        """
        Create an evaluation together with its items, optionally running test criteria
        against them.

        Accepts three request shapes: standalone (inline `data`), from an existing
        dataset (`dataset_id` with optional per-item references), or with a new reusable
        dataset created inline from `data`. When the evaluation includes tasks that
        require execution (for example an LLM judge or custom function), an async job
        and a Temporal workflow are started and the evaluation is returned immediately
        with status `running`; task results and `error_count` populate asynchronously.
        When it includes only contributor tasks, taxonomy-only input, or no tasks, no
        workflow runs and it is returned with status `completed`. Optional `tasks`,
        `metadata`, `tags`, and `taxonomy_params` are persisted alongside the evaluation
        and its items.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v5/evaluations",
            body=maybe_transform(evaluation, evaluation_create_params.EvaluationCreateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Evaluation,
        )

    def retrieve(
        self,
        evaluation_id: str,
        *,
        include_archived: bool | Omit = omit,
        views: List[EvaluationViews] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Evaluation:
        """
        Retrieve a single evaluation by ID.

        Returns the evaluation with its datasets, async-job progress, metadata, and
        task-error count. Archived evaluations are excluded unless `include_archived` is
        set. Pass the `tasks` view to include the evaluation's task configurations in
        the response.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not evaluation_id:
            raise ValueError(f"Expected a non-empty value for `evaluation_id` but received {evaluation_id!r}")
        return self._get(
            path_template("/v5/evaluations/{evaluation_id}", evaluation_id=evaluation_id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "include_archived": include_archived,
                        "views": views,
                    },
                    evaluation_retrieve_params.EvaluationRetrieveParams,
                ),
            ),
            cast_to=Evaluation,
        )

    def update(
        self,
        evaluation_id: str,
        *,
        evaluation: evaluation_update_params.Evaluation,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Evaluation:
        """
        Update an evaluation's mutable fields, or restore it from the archive.

        The action is selected by the request body: a restore request un-archives the
        evaluation and cascades the restore to its items and dashboards, while any other
        body applies a partial update to fields such as name, description, tags, and
        metadata (metadata is applied as an RFC 7396 merge patch). Updating an
        already-archived evaluation is rejected — restore it first. The evaluation row
        is locked for the duration of the write to avoid concurrent-update races.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not evaluation_id:
            raise ValueError(f"Expected a non-empty value for `evaluation_id` but received {evaluation_id!r}")
        return self._patch(
            path_template("/v5/evaluations/{evaluation_id}", evaluation_id=evaluation_id),
            body=maybe_transform(evaluation, evaluation_update_params.EvaluationUpdateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Evaluation,
        )

    def list(
        self,
        *,
        ending_before: str | Omit = omit,
        include_archived: bool | Omit = omit,
        limit: int | Omit = omit,
        name: str | Omit = omit,
        sort_by: str | Omit = omit,
        sort_order: SortOrder | Omit = omit,
        starting_after: str | Omit = omit,
        tags: SequenceNotStr[str] | Omit = omit,
        views: List[EvaluationViews] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SyncCursorPage[Evaluation]:
        """
        List evaluations for the account, with pagination.

        Supports filtering by case-insensitive name substring and by tags; archived
        evaluations are excluded unless `include_archived` is set. Pass the `tasks` view
        to include each evaluation's task configurations in the response. Use this for
        simple name or tag lookups; to filter on metadata key-value pairs or status, use
        the filter endpoint instead.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v5/evaluations",
            page=SyncCursorPage[Evaluation],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "ending_before": ending_before,
                        "include_archived": include_archived,
                        "limit": limit,
                        "name": name,
                        "sort_by": sort_by,
                        "sort_order": sort_order,
                        "starting_after": starting_after,
                        "tags": tags,
                        "views": views,
                    },
                    evaluation_list_params.EvaluationListParams,
                ),
            ),
            model=Evaluation,
        )

    def archive(
        self,
        evaluation_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Evaluation:
        """
        Archive (soft-delete) an evaluation.

        Sets the evaluation's archived timestamp rather than permanently deleting it,
        and cascades the archive to the evaluation's items and dashboards while removing
        it from any evaluation groups. The evaluation can later be brought back with a
        restore request to the update endpoint.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not evaluation_id:
            raise ValueError(f"Expected a non-empty value for `evaluation_id` but received {evaluation_id!r}")
        return self._delete(
            path_template("/v5/evaluations/{evaluation_id}", evaluation_id=evaluation_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Evaluation,
        )

    def filter(
        self,
        *,
        filters: Iterable[evaluation_filter_params.Filter],
        ending_before: str | Omit = omit,
        include_archived: bool | Omit = omit,
        limit: int | Omit = omit,
        sort_by: str | Omit = omit,
        sort_order: SortOrder | Omit = omit,
        starting_after: str | Omit = omit,
        views: List[EvaluationViews] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SyncCursorPage[Evaluation]:
        """
        Filter evaluations by metadata, status, and tags.

        Accepts up to 10 filters combined with AND logic, each comparing a key against a
        value with an operator (`==`, `!=`, `>=`, `<=`, `IN`, `NOT_IN`). Filter on
        metadata keys returned by the metadata-keys endpoint, plus the built-in `status`
        and `tag` keys. Archived evaluations are excluded unless `include_archived` is
        set, and the `tasks` view includes task configurations in each result. Use this
        for metadata or status filtering; for simple name or tag lookups the list
        endpoint is sufficient.

        Args:
          filters: List of metadata filters to apply (maximum 10)

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v5/evaluations/filter",
            page=SyncCursorPage[Evaluation],
            body=maybe_transform({"filters": filters}, evaluation_filter_params.EvaluationFilterParams),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "ending_before": ending_before,
                        "include_archived": include_archived,
                        "limit": limit,
                        "sort_by": sort_by,
                        "sort_order": sort_order,
                        "starting_after": starting_after,
                        "views": views,
                    },
                    evaluation_filter_params.EvaluationFilterParams,
                ),
            ),
            model=Evaluation,
            method="post",
        )

    def retrieve_schema(
        self,
        evaluation_id: str,
        *,
        include_archived: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> EvaluationSchemaResponse:
        """
        Describe the data schema of an evaluation's items.

        Inspects the item `data` and task-result fields and returns each discovered
        field with its flattened key path, JSON type, source, and the number of items
        containing it, ordered alphabetically by field name. For large evaluations the
        schema may be inferred from a sample of items, in which case `is_sampled` is set
        and `sample_size` reports how many were analyzed. Set `include_archived` to
        include archived items in the analysis.

        Args:
          include_archived: Include archived items in schema analysis

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not evaluation_id:
            raise ValueError(f"Expected a non-empty value for `evaluation_id` but received {evaluation_id!r}")
        return self._get(
            path_template("/v5/evaluations/{evaluation_id}/schema", evaluation_id=evaluation_id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {"include_archived": include_archived},
                    evaluation_retrieve_schema_params.EvaluationRetrieveSchemaParams,
                ),
            ),
            cast_to=EvaluationSchemaResponse,
        )

    def retrieve_taxonomy(
        self,
        evaluation_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> EvaluationRetrieveTaxonomyResponse:
        """
        Get the taxonomy JSON for an evaluation's contributor question tasks.

        Returns the raw taxonomy document stored for the evaluation. Responds with a
        not-found error if the evaluation has no taxonomy.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not evaluation_id:
            raise ValueError(f"Expected a non-empty value for `evaluation_id` but received {evaluation_id!r}")
        return self._get(
            path_template("/v5/evaluations/{evaluation_id}/taxonomy", evaluation_id=evaluation_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EvaluationRetrieveTaxonomyResponse,
        )


class AsyncEvaluationsResource(AsyncAPIResource):
    @cached_property
    def tasks(self) -> AsyncTasksResource:
        return AsyncTasksResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncEvaluationsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python-beta#accessing-raw-response-data-eg-headers
        """
        return AsyncEvaluationsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncEvaluationsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python-beta#with_streaming_response
        """
        return AsyncEvaluationsResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        evaluation: evaluation_create_params.Evaluation,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Evaluation:
        """
        Create an evaluation together with its items, optionally running test criteria
        against them.

        Accepts three request shapes: standalone (inline `data`), from an existing
        dataset (`dataset_id` with optional per-item references), or with a new reusable
        dataset created inline from `data`. When the evaluation includes tasks that
        require execution (for example an LLM judge or custom function), an async job
        and a Temporal workflow are started and the evaluation is returned immediately
        with status `running`; task results and `error_count` populate asynchronously.
        When it includes only contributor tasks, taxonomy-only input, or no tasks, no
        workflow runs and it is returned with status `completed`. Optional `tasks`,
        `metadata`, `tags`, and `taxonomy_params` are persisted alongside the evaluation
        and its items.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v5/evaluations",
            body=await async_maybe_transform(evaluation, evaluation_create_params.EvaluationCreateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Evaluation,
        )

    async def retrieve(
        self,
        evaluation_id: str,
        *,
        include_archived: bool | Omit = omit,
        views: List[EvaluationViews] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Evaluation:
        """
        Retrieve a single evaluation by ID.

        Returns the evaluation with its datasets, async-job progress, metadata, and
        task-error count. Archived evaluations are excluded unless `include_archived` is
        set. Pass the `tasks` view to include the evaluation's task configurations in
        the response.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not evaluation_id:
            raise ValueError(f"Expected a non-empty value for `evaluation_id` but received {evaluation_id!r}")
        return await self._get(
            path_template("/v5/evaluations/{evaluation_id}", evaluation_id=evaluation_id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "include_archived": include_archived,
                        "views": views,
                    },
                    evaluation_retrieve_params.EvaluationRetrieveParams,
                ),
            ),
            cast_to=Evaluation,
        )

    async def update(
        self,
        evaluation_id: str,
        *,
        evaluation: evaluation_update_params.Evaluation,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Evaluation:
        """
        Update an evaluation's mutable fields, or restore it from the archive.

        The action is selected by the request body: a restore request un-archives the
        evaluation and cascades the restore to its items and dashboards, while any other
        body applies a partial update to fields such as name, description, tags, and
        metadata (metadata is applied as an RFC 7396 merge patch). Updating an
        already-archived evaluation is rejected — restore it first. The evaluation row
        is locked for the duration of the write to avoid concurrent-update races.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not evaluation_id:
            raise ValueError(f"Expected a non-empty value for `evaluation_id` but received {evaluation_id!r}")
        return await self._patch(
            path_template("/v5/evaluations/{evaluation_id}", evaluation_id=evaluation_id),
            body=await async_maybe_transform(evaluation, evaluation_update_params.EvaluationUpdateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Evaluation,
        )

    def list(
        self,
        *,
        ending_before: str | Omit = omit,
        include_archived: bool | Omit = omit,
        limit: int | Omit = omit,
        name: str | Omit = omit,
        sort_by: str | Omit = omit,
        sort_order: SortOrder | Omit = omit,
        starting_after: str | Omit = omit,
        tags: SequenceNotStr[str] | Omit = omit,
        views: List[EvaluationViews] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[Evaluation, AsyncCursorPage[Evaluation]]:
        """
        List evaluations for the account, with pagination.

        Supports filtering by case-insensitive name substring and by tags; archived
        evaluations are excluded unless `include_archived` is set. Pass the `tasks` view
        to include each evaluation's task configurations in the response. Use this for
        simple name or tag lookups; to filter on metadata key-value pairs or status, use
        the filter endpoint instead.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v5/evaluations",
            page=AsyncCursorPage[Evaluation],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "ending_before": ending_before,
                        "include_archived": include_archived,
                        "limit": limit,
                        "name": name,
                        "sort_by": sort_by,
                        "sort_order": sort_order,
                        "starting_after": starting_after,
                        "tags": tags,
                        "views": views,
                    },
                    evaluation_list_params.EvaluationListParams,
                ),
            ),
            model=Evaluation,
        )

    async def archive(
        self,
        evaluation_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Evaluation:
        """
        Archive (soft-delete) an evaluation.

        Sets the evaluation's archived timestamp rather than permanently deleting it,
        and cascades the archive to the evaluation's items and dashboards while removing
        it from any evaluation groups. The evaluation can later be brought back with a
        restore request to the update endpoint.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not evaluation_id:
            raise ValueError(f"Expected a non-empty value for `evaluation_id` but received {evaluation_id!r}")
        return await self._delete(
            path_template("/v5/evaluations/{evaluation_id}", evaluation_id=evaluation_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Evaluation,
        )

    def filter(
        self,
        *,
        filters: Iterable[evaluation_filter_params.Filter],
        ending_before: str | Omit = omit,
        include_archived: bool | Omit = omit,
        limit: int | Omit = omit,
        sort_by: str | Omit = omit,
        sort_order: SortOrder | Omit = omit,
        starting_after: str | Omit = omit,
        views: List[EvaluationViews] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[Evaluation, AsyncCursorPage[Evaluation]]:
        """
        Filter evaluations by metadata, status, and tags.

        Accepts up to 10 filters combined with AND logic, each comparing a key against a
        value with an operator (`==`, `!=`, `>=`, `<=`, `IN`, `NOT_IN`). Filter on
        metadata keys returned by the metadata-keys endpoint, plus the built-in `status`
        and `tag` keys. Archived evaluations are excluded unless `include_archived` is
        set, and the `tasks` view includes task configurations in each result. Use this
        for metadata or status filtering; for simple name or tag lookups the list
        endpoint is sufficient.

        Args:
          filters: List of metadata filters to apply (maximum 10)

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v5/evaluations/filter",
            page=AsyncCursorPage[Evaluation],
            body=maybe_transform({"filters": filters}, evaluation_filter_params.EvaluationFilterParams),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "ending_before": ending_before,
                        "include_archived": include_archived,
                        "limit": limit,
                        "sort_by": sort_by,
                        "sort_order": sort_order,
                        "starting_after": starting_after,
                        "views": views,
                    },
                    evaluation_filter_params.EvaluationFilterParams,
                ),
            ),
            model=Evaluation,
            method="post",
        )

    async def retrieve_schema(
        self,
        evaluation_id: str,
        *,
        include_archived: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> EvaluationSchemaResponse:
        """
        Describe the data schema of an evaluation's items.

        Inspects the item `data` and task-result fields and returns each discovered
        field with its flattened key path, JSON type, source, and the number of items
        containing it, ordered alphabetically by field name. For large evaluations the
        schema may be inferred from a sample of items, in which case `is_sampled` is set
        and `sample_size` reports how many were analyzed. Set `include_archived` to
        include archived items in the analysis.

        Args:
          include_archived: Include archived items in schema analysis

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not evaluation_id:
            raise ValueError(f"Expected a non-empty value for `evaluation_id` but received {evaluation_id!r}")
        return await self._get(
            path_template("/v5/evaluations/{evaluation_id}/schema", evaluation_id=evaluation_id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {"include_archived": include_archived},
                    evaluation_retrieve_schema_params.EvaluationRetrieveSchemaParams,
                ),
            ),
            cast_to=EvaluationSchemaResponse,
        )

    async def retrieve_taxonomy(
        self,
        evaluation_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> EvaluationRetrieveTaxonomyResponse:
        """
        Get the taxonomy JSON for an evaluation's contributor question tasks.

        Returns the raw taxonomy document stored for the evaluation. Responds with a
        not-found error if the evaluation has no taxonomy.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not evaluation_id:
            raise ValueError(f"Expected a non-empty value for `evaluation_id` but received {evaluation_id!r}")
        return await self._get(
            path_template("/v5/evaluations/{evaluation_id}/taxonomy", evaluation_id=evaluation_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EvaluationRetrieveTaxonomyResponse,
        )


class EvaluationsResourceWithRawResponse:
    def __init__(self, evaluations: EvaluationsResource) -> None:
        self._evaluations = evaluations

        self.create = to_raw_response_wrapper(
            evaluations.create,
        )
        self.retrieve = to_raw_response_wrapper(
            evaluations.retrieve,
        )
        self.update = to_raw_response_wrapper(
            evaluations.update,
        )
        self.list = to_raw_response_wrapper(
            evaluations.list,
        )
        self.archive = to_raw_response_wrapper(
            evaluations.archive,
        )
        self.filter = to_raw_response_wrapper(
            evaluations.filter,
        )
        self.retrieve_schema = to_raw_response_wrapper(
            evaluations.retrieve_schema,
        )
        self.retrieve_taxonomy = to_raw_response_wrapper(
            evaluations.retrieve_taxonomy,
        )

    @cached_property
    def tasks(self) -> TasksResourceWithRawResponse:
        return TasksResourceWithRawResponse(self._evaluations.tasks)


class AsyncEvaluationsResourceWithRawResponse:
    def __init__(self, evaluations: AsyncEvaluationsResource) -> None:
        self._evaluations = evaluations

        self.create = async_to_raw_response_wrapper(
            evaluations.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            evaluations.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            evaluations.update,
        )
        self.list = async_to_raw_response_wrapper(
            evaluations.list,
        )
        self.archive = async_to_raw_response_wrapper(
            evaluations.archive,
        )
        self.filter = async_to_raw_response_wrapper(
            evaluations.filter,
        )
        self.retrieve_schema = async_to_raw_response_wrapper(
            evaluations.retrieve_schema,
        )
        self.retrieve_taxonomy = async_to_raw_response_wrapper(
            evaluations.retrieve_taxonomy,
        )

    @cached_property
    def tasks(self) -> AsyncTasksResourceWithRawResponse:
        return AsyncTasksResourceWithRawResponse(self._evaluations.tasks)


class EvaluationsResourceWithStreamingResponse:
    def __init__(self, evaluations: EvaluationsResource) -> None:
        self._evaluations = evaluations

        self.create = to_streamed_response_wrapper(
            evaluations.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            evaluations.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            evaluations.update,
        )
        self.list = to_streamed_response_wrapper(
            evaluations.list,
        )
        self.archive = to_streamed_response_wrapper(
            evaluations.archive,
        )
        self.filter = to_streamed_response_wrapper(
            evaluations.filter,
        )
        self.retrieve_schema = to_streamed_response_wrapper(
            evaluations.retrieve_schema,
        )
        self.retrieve_taxonomy = to_streamed_response_wrapper(
            evaluations.retrieve_taxonomy,
        )

    @cached_property
    def tasks(self) -> TasksResourceWithStreamingResponse:
        return TasksResourceWithStreamingResponse(self._evaluations.tasks)


class AsyncEvaluationsResourceWithStreamingResponse:
    def __init__(self, evaluations: AsyncEvaluationsResource) -> None:
        self._evaluations = evaluations

        self.create = async_to_streamed_response_wrapper(
            evaluations.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            evaluations.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            evaluations.update,
        )
        self.list = async_to_streamed_response_wrapper(
            evaluations.list,
        )
        self.archive = async_to_streamed_response_wrapper(
            evaluations.archive,
        )
        self.filter = async_to_streamed_response_wrapper(
            evaluations.filter,
        )
        self.retrieve_schema = async_to_streamed_response_wrapper(
            evaluations.retrieve_schema,
        )
        self.retrieve_taxonomy = async_to_streamed_response_wrapper(
            evaluations.retrieve_taxonomy,
        )

    @cached_property
    def tasks(self) -> AsyncTasksResourceWithStreamingResponse:
        return AsyncTasksResourceWithStreamingResponse(self._evaluations.tasks)
