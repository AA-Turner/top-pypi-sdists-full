# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Iterable

import httpx

from ..types import dataset_list_params, dataset_create_params, dataset_update_params, dataset_retrieve_params
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
from ..types.dataset import Dataset
from ..types.chat.sort_order import SortOrder
from ..types.dataset_archive_response import DatasetArchiveResponse

__all__ = ["DatasetsResource", "AsyncDatasetsResource"]


class DatasetsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> DatasetsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python-beta#accessing-raw-response-data-eg-headers
        """
        return DatasetsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> DatasetsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python-beta#with_streaming_response
        """
        return DatasetsResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        data: Iterable[Dict[str, object]],
        name: str,
        description: str | Omit = omit,
        files: Iterable[Dict[str, str]] | Omit = omit,
        tags: SequenceNotStr[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Dataset:
        """
        Create a dataset and populate it with its initial items in a single call.

        Use this when the dataset does not exist yet: it creates the dataset and seeds
        it with the items you provide. To add more items to a dataset that already
        exists, use POST /v5/dataset-items/batch instead. A name is required, and the
        request must include at least one item in `data`; the optional `files` field
        associates files with the created items. The provided items are inserted as
        dataset items as a side effect of creation, and any `tags` are attached to the
        dataset. The returned dataset is at version 1.

        Args:
          data: Items to be included in the dataset

          files: Files to be associated to the dataset

          tags: The tags associated with the entity

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v5/datasets",
            body=maybe_transform(
                {
                    "data": data,
                    "name": name,
                    "description": description,
                    "files": files,
                    "tags": tags,
                },
                dataset_create_params.DatasetCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Dataset,
        )

    def retrieve(
        self,
        dataset_id: str,
        *,
        include_archived: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Dataset:
        """
        Retrieve a single dataset by its id.

        By default an archived dataset is not returned; set `include_archived` to true
        to fetch a dataset regardless of whether it has been archived.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not dataset_id:
            raise ValueError(f"Expected a non-empty value for `dataset_id` but received {dataset_id!r}")
        return self._get(
            path_template("/v5/datasets/{dataset_id}", dataset_id=dataset_id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {"include_archived": include_archived}, dataset_retrieve_params.DatasetRetrieveParams
                ),
            ),
            cast_to=Dataset,
        )

    def update(
        self,
        dataset_id: str,
        *,
        dataset: dataset_update_params.Dataset,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Dataset:
        """
        Update a dataset's fields, or restore a previously archived dataset.

        The request body is a union discriminated by its contents: a body of
        `{"restore": true}` triggers a restore, and any other body is treated as a
        partial update of the dataset's `name`, `description`, and `tags`. Restore
        clears `archived_at` on the dataset and cascades the un-archival to its items
        and versions; restoring a dataset that is not archived returns it unchanged. A
        partial update on an archived dataset fails, since archived datasets cannot be
        modified.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not dataset_id:
            raise ValueError(f"Expected a non-empty value for `dataset_id` but received {dataset_id!r}")
        return self._patch(
            path_template("/v5/datasets/{dataset_id}", dataset_id=dataset_id),
            body=maybe_transform(dataset, dataset_update_params.DatasetUpdateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Dataset,
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
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SyncCursorPage[Dataset]:
        """
        Return a paginated list of the account's datasets.

        Archived datasets are excluded unless `include_archived` is set to true. Results
        can be narrowed by `tags` and by the standard filterable parameters; a `name`
        filter matches as a case-insensitive substring rather than an exact match.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v5/datasets",
            page=SyncCursorPage[Dataset],
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
                    },
                    dataset_list_params.DatasetListParams,
                ),
            ),
            model=Dataset,
        )

    def archive(
        self,
        dataset_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> DatasetArchiveResponse:
        """
        Soft-delete a dataset by archiving it; the row is retained and can be restored
        later.

        This sets the dataset's `archived_at` timestamp rather than permanently removing
        it, and cascades the same archival to the dataset's items and versions.
        Archiving is not idempotent: if the dataset is already archived the call fails.
        The dataset can be brought back with the PATCH restore request. The response
        reports the dataset id with `deleted` set to true.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not dataset_id:
            raise ValueError(f"Expected a non-empty value for `dataset_id` but received {dataset_id!r}")
        return self._delete(
            path_template("/v5/datasets/{dataset_id}", dataset_id=dataset_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DatasetArchiveResponse,
        )


class AsyncDatasetsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncDatasetsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python-beta#accessing-raw-response-data-eg-headers
        """
        return AsyncDatasetsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncDatasetsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python-beta#with_streaming_response
        """
        return AsyncDatasetsResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        data: Iterable[Dict[str, object]],
        name: str,
        description: str | Omit = omit,
        files: Iterable[Dict[str, str]] | Omit = omit,
        tags: SequenceNotStr[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Dataset:
        """
        Create a dataset and populate it with its initial items in a single call.

        Use this when the dataset does not exist yet: it creates the dataset and seeds
        it with the items you provide. To add more items to a dataset that already
        exists, use POST /v5/dataset-items/batch instead. A name is required, and the
        request must include at least one item in `data`; the optional `files` field
        associates files with the created items. The provided items are inserted as
        dataset items as a side effect of creation, and any `tags` are attached to the
        dataset. The returned dataset is at version 1.

        Args:
          data: Items to be included in the dataset

          files: Files to be associated to the dataset

          tags: The tags associated with the entity

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v5/datasets",
            body=await async_maybe_transform(
                {
                    "data": data,
                    "name": name,
                    "description": description,
                    "files": files,
                    "tags": tags,
                },
                dataset_create_params.DatasetCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Dataset,
        )

    async def retrieve(
        self,
        dataset_id: str,
        *,
        include_archived: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Dataset:
        """
        Retrieve a single dataset by its id.

        By default an archived dataset is not returned; set `include_archived` to true
        to fetch a dataset regardless of whether it has been archived.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not dataset_id:
            raise ValueError(f"Expected a non-empty value for `dataset_id` but received {dataset_id!r}")
        return await self._get(
            path_template("/v5/datasets/{dataset_id}", dataset_id=dataset_id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {"include_archived": include_archived}, dataset_retrieve_params.DatasetRetrieveParams
                ),
            ),
            cast_to=Dataset,
        )

    async def update(
        self,
        dataset_id: str,
        *,
        dataset: dataset_update_params.Dataset,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Dataset:
        """
        Update a dataset's fields, or restore a previously archived dataset.

        The request body is a union discriminated by its contents: a body of
        `{"restore": true}` triggers a restore, and any other body is treated as a
        partial update of the dataset's `name`, `description`, and `tags`. Restore
        clears `archived_at` on the dataset and cascades the un-archival to its items
        and versions; restoring a dataset that is not archived returns it unchanged. A
        partial update on an archived dataset fails, since archived datasets cannot be
        modified.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not dataset_id:
            raise ValueError(f"Expected a non-empty value for `dataset_id` but received {dataset_id!r}")
        return await self._patch(
            path_template("/v5/datasets/{dataset_id}", dataset_id=dataset_id),
            body=await async_maybe_transform(dataset, dataset_update_params.DatasetUpdateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Dataset,
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
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[Dataset, AsyncCursorPage[Dataset]]:
        """
        Return a paginated list of the account's datasets.

        Archived datasets are excluded unless `include_archived` is set to true. Results
        can be narrowed by `tags` and by the standard filterable parameters; a `name`
        filter matches as a case-insensitive substring rather than an exact match.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v5/datasets",
            page=AsyncCursorPage[Dataset],
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
                    },
                    dataset_list_params.DatasetListParams,
                ),
            ),
            model=Dataset,
        )

    async def archive(
        self,
        dataset_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> DatasetArchiveResponse:
        """
        Soft-delete a dataset by archiving it; the row is retained and can be restored
        later.

        This sets the dataset's `archived_at` timestamp rather than permanently removing
        it, and cascades the same archival to the dataset's items and versions.
        Archiving is not idempotent: if the dataset is already archived the call fails.
        The dataset can be brought back with the PATCH restore request. The response
        reports the dataset id with `deleted` set to true.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not dataset_id:
            raise ValueError(f"Expected a non-empty value for `dataset_id` but received {dataset_id!r}")
        return await self._delete(
            path_template("/v5/datasets/{dataset_id}", dataset_id=dataset_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DatasetArchiveResponse,
        )


class DatasetsResourceWithRawResponse:
    def __init__(self, datasets: DatasetsResource) -> None:
        self._datasets = datasets

        self.create = to_raw_response_wrapper(
            datasets.create,
        )
        self.retrieve = to_raw_response_wrapper(
            datasets.retrieve,
        )
        self.update = to_raw_response_wrapper(
            datasets.update,
        )
        self.list = to_raw_response_wrapper(
            datasets.list,
        )
        self.archive = to_raw_response_wrapper(
            datasets.archive,
        )


class AsyncDatasetsResourceWithRawResponse:
    def __init__(self, datasets: AsyncDatasetsResource) -> None:
        self._datasets = datasets

        self.create = async_to_raw_response_wrapper(
            datasets.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            datasets.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            datasets.update,
        )
        self.list = async_to_raw_response_wrapper(
            datasets.list,
        )
        self.archive = async_to_raw_response_wrapper(
            datasets.archive,
        )


class DatasetsResourceWithStreamingResponse:
    def __init__(self, datasets: DatasetsResource) -> None:
        self._datasets = datasets

        self.create = to_streamed_response_wrapper(
            datasets.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            datasets.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            datasets.update,
        )
        self.list = to_streamed_response_wrapper(
            datasets.list,
        )
        self.archive = to_streamed_response_wrapper(
            datasets.archive,
        )


class AsyncDatasetsResourceWithStreamingResponse:
    def __init__(self, datasets: AsyncDatasetsResource) -> None:
        self._datasets = datasets

        self.create = async_to_streamed_response_wrapper(
            datasets.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            datasets.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            datasets.update,
        )
        self.list = async_to_streamed_response_wrapper(
            datasets.list,
        )
        self.archive = async_to_streamed_response_wrapper(
            datasets.archive,
        )
