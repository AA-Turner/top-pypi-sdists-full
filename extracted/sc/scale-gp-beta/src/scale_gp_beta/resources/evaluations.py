# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Iterable

import httpx

from ..types import (
    evaluation_list_params,
    evaluation_create_params,
    evaluation_filter_params,
    evaluation_update_params,
    evaluation_retrieve_params,
    evaluation_retrieve_schema_params,
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
from ..types.evaluation import Evaluation
from ..types.chat.sort_order import SortOrder
from ..types.evaluation_views import EvaluationViews
from ..types.evaluation_schema_response import EvaluationSchemaResponse
from ..types.evaluation_retrieve_taxonomy_response import EvaluationRetrieveTaxonomyResponse

__all__ = ["EvaluationsResource", "AsyncEvaluationsResource"]


class EvaluationsResource(SyncAPIResource):
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
        Create Evaluation

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
        Get Evaluation

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
        Update or Restore Evaluation

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
        List Evaluations

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
        Archive Evaluation

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
        """Filter evaluations using metadata and other criteria.

        Supports up to 10 filters
        with AND logic.

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
        Get schema information for evaluation item data, including field names, types,
        and occurrence counts.

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
        Get taxonomy JSON for contributor evaluation question tasks.

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
        Create Evaluation

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
        Get Evaluation

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
        Update or Restore Evaluation

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
        List Evaluations

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
        Archive Evaluation

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
        """Filter evaluations using metadata and other criteria.

        Supports up to 10 filters
        with AND logic.

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
        Get schema information for evaluation item data, including field names, types,
        and occurrence counts.

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
        Get taxonomy JSON for contributor evaluation question tasks.

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
