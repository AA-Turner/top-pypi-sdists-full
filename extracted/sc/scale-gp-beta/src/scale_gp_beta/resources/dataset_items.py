# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Iterable

import httpx

from ..types import (
    dataset_item_list_params,
    dataset_item_update_params,
    dataset_item_retrieve_params,
    dataset_item_batch_create_params,
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
from ..pagination import SyncCursorPage, AsyncCursorPage
from ..types.chat import SortOrder
from .._base_client import AsyncPaginator, make_request_options
from ..types.dataset_item import DatasetItem
from ..types.chat.sort_order import SortOrder
from ..types.dataset_item_archive_response import DatasetItemArchiveResponse
from ..types.dataset_item_batch_create_response import DatasetItemBatchCreateResponse

__all__ = ["DatasetItemsResource", "AsyncDatasetItemsResource"]


class DatasetItemsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> DatasetItemsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python-beta#accessing-raw-response-data-eg-headers
        """
        return DatasetItemsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> DatasetItemsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python-beta#with_streaming_response
        """
        return DatasetItemsResourceWithStreamingResponse(self)

    def retrieve(
        self,
        dataset_item_id: str,
        *,
        version: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> DatasetItem:
        """Get Dataset Item

        Args:
          version: Optional dataset version.

        When unset, returns the latest version.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not dataset_item_id:
            raise ValueError(f"Expected a non-empty value for `dataset_item_id` but received {dataset_item_id!r}")
        return self._get(
            path_template("/v5/dataset-items/{dataset_item_id}", dataset_item_id=dataset_item_id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"version": version}, dataset_item_retrieve_params.DatasetItemRetrieveParams),
            ),
            cast_to=DatasetItem,
        )

    def update(
        self,
        dataset_item_id: str,
        *,
        data: Dict[str, object],
        files: Dict[str, str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> DatasetItem:
        """
        Update Dataset Item

        Args:
          data: Updated dataset item data

          files: Files to be associated to the dataset

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not dataset_item_id:
            raise ValueError(f"Expected a non-empty value for `dataset_item_id` but received {dataset_item_id!r}")
        return self._patch(
            path_template("/v5/dataset-items/{dataset_item_id}", dataset_item_id=dataset_item_id),
            body=maybe_transform(
                {
                    "data": data,
                    "files": files,
                },
                dataset_item_update_params.DatasetItemUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DatasetItem,
        )

    def list(
        self,
        *,
        dataset_id: str | Omit = omit,
        ending_before: str | Omit = omit,
        include_archived: bool | Omit = omit,
        limit: int | Omit = omit,
        sort_by: str | Omit = omit,
        sort_order: SortOrder | Omit = omit,
        starting_after: str | Omit = omit,
        version: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SyncCursorPage[DatasetItem]:
        """List Dataset Items

        Args:
          dataset_id: Optional dataset identifier.

        Must be provided if a specific version is
              requested.

          version: Optional dataset version. When unset, returns the latest version. Requires a
              valid dataset_id when set.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v5/dataset-items",
            page=SyncCursorPage[DatasetItem],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "dataset_id": dataset_id,
                        "ending_before": ending_before,
                        "include_archived": include_archived,
                        "limit": limit,
                        "sort_by": sort_by,
                        "sort_order": sort_order,
                        "starting_after": starting_after,
                        "version": version,
                    },
                    dataset_item_list_params.DatasetItemListParams,
                ),
            ),
            model=DatasetItem,
        )

    def archive(
        self,
        dataset_item_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> DatasetItemArchiveResponse:
        """
        Delete Dataset Item

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not dataset_item_id:
            raise ValueError(f"Expected a non-empty value for `dataset_item_id` but received {dataset_item_id!r}")
        return self._delete(
            path_template("/v5/dataset-items/{dataset_item_id}", dataset_item_id=dataset_item_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DatasetItemArchiveResponse,
        )

    def batch_create(
        self,
        *,
        data: Iterable[Dict[str, object]],
        dataset_id: str,
        files: Iterable[Dict[str, str]] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> DatasetItemBatchCreateResponse:
        """
        Batch Create Dataset Items

        Args:
          data: Items to be added to the dataset

          dataset_id: Identifier of the target dataset

          files: Files to be associated to the dataset

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v5/dataset-items/batch",
            body=maybe_transform(
                {
                    "data": data,
                    "dataset_id": dataset_id,
                    "files": files,
                },
                dataset_item_batch_create_params.DatasetItemBatchCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DatasetItemBatchCreateResponse,
        )


class AsyncDatasetItemsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncDatasetItemsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python-beta#accessing-raw-response-data-eg-headers
        """
        return AsyncDatasetItemsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncDatasetItemsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python-beta#with_streaming_response
        """
        return AsyncDatasetItemsResourceWithStreamingResponse(self)

    async def retrieve(
        self,
        dataset_item_id: str,
        *,
        version: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> DatasetItem:
        """Get Dataset Item

        Args:
          version: Optional dataset version.

        When unset, returns the latest version.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not dataset_item_id:
            raise ValueError(f"Expected a non-empty value for `dataset_item_id` but received {dataset_item_id!r}")
        return await self._get(
            path_template("/v5/dataset-items/{dataset_item_id}", dataset_item_id=dataset_item_id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {"version": version}, dataset_item_retrieve_params.DatasetItemRetrieveParams
                ),
            ),
            cast_to=DatasetItem,
        )

    async def update(
        self,
        dataset_item_id: str,
        *,
        data: Dict[str, object],
        files: Dict[str, str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> DatasetItem:
        """
        Update Dataset Item

        Args:
          data: Updated dataset item data

          files: Files to be associated to the dataset

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not dataset_item_id:
            raise ValueError(f"Expected a non-empty value for `dataset_item_id` but received {dataset_item_id!r}")
        return await self._patch(
            path_template("/v5/dataset-items/{dataset_item_id}", dataset_item_id=dataset_item_id),
            body=await async_maybe_transform(
                {
                    "data": data,
                    "files": files,
                },
                dataset_item_update_params.DatasetItemUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DatasetItem,
        )

    def list(
        self,
        *,
        dataset_id: str | Omit = omit,
        ending_before: str | Omit = omit,
        include_archived: bool | Omit = omit,
        limit: int | Omit = omit,
        sort_by: str | Omit = omit,
        sort_order: SortOrder | Omit = omit,
        starting_after: str | Omit = omit,
        version: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[DatasetItem, AsyncCursorPage[DatasetItem]]:
        """List Dataset Items

        Args:
          dataset_id: Optional dataset identifier.

        Must be provided if a specific version is
              requested.

          version: Optional dataset version. When unset, returns the latest version. Requires a
              valid dataset_id when set.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v5/dataset-items",
            page=AsyncCursorPage[DatasetItem],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "dataset_id": dataset_id,
                        "ending_before": ending_before,
                        "include_archived": include_archived,
                        "limit": limit,
                        "sort_by": sort_by,
                        "sort_order": sort_order,
                        "starting_after": starting_after,
                        "version": version,
                    },
                    dataset_item_list_params.DatasetItemListParams,
                ),
            ),
            model=DatasetItem,
        )

    async def archive(
        self,
        dataset_item_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> DatasetItemArchiveResponse:
        """
        Delete Dataset Item

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not dataset_item_id:
            raise ValueError(f"Expected a non-empty value for `dataset_item_id` but received {dataset_item_id!r}")
        return await self._delete(
            path_template("/v5/dataset-items/{dataset_item_id}", dataset_item_id=dataset_item_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DatasetItemArchiveResponse,
        )

    async def batch_create(
        self,
        *,
        data: Iterable[Dict[str, object]],
        dataset_id: str,
        files: Iterable[Dict[str, str]] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> DatasetItemBatchCreateResponse:
        """
        Batch Create Dataset Items

        Args:
          data: Items to be added to the dataset

          dataset_id: Identifier of the target dataset

          files: Files to be associated to the dataset

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v5/dataset-items/batch",
            body=await async_maybe_transform(
                {
                    "data": data,
                    "dataset_id": dataset_id,
                    "files": files,
                },
                dataset_item_batch_create_params.DatasetItemBatchCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DatasetItemBatchCreateResponse,
        )


class DatasetItemsResourceWithRawResponse:
    def __init__(self, dataset_items: DatasetItemsResource) -> None:
        self._dataset_items = dataset_items

        self.retrieve = to_raw_response_wrapper(
            dataset_items.retrieve,
        )
        self.update = to_raw_response_wrapper(
            dataset_items.update,
        )
        self.list = to_raw_response_wrapper(
            dataset_items.list,
        )
        self.archive = to_raw_response_wrapper(
            dataset_items.archive,
        )
        self.batch_create = to_raw_response_wrapper(
            dataset_items.batch_create,
        )


class AsyncDatasetItemsResourceWithRawResponse:
    def __init__(self, dataset_items: AsyncDatasetItemsResource) -> None:
        self._dataset_items = dataset_items

        self.retrieve = async_to_raw_response_wrapper(
            dataset_items.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            dataset_items.update,
        )
        self.list = async_to_raw_response_wrapper(
            dataset_items.list,
        )
        self.archive = async_to_raw_response_wrapper(
            dataset_items.archive,
        )
        self.batch_create = async_to_raw_response_wrapper(
            dataset_items.batch_create,
        )


class DatasetItemsResourceWithStreamingResponse:
    def __init__(self, dataset_items: DatasetItemsResource) -> None:
        self._dataset_items = dataset_items

        self.retrieve = to_streamed_response_wrapper(
            dataset_items.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            dataset_items.update,
        )
        self.list = to_streamed_response_wrapper(
            dataset_items.list,
        )
        self.archive = to_streamed_response_wrapper(
            dataset_items.archive,
        )
        self.batch_create = to_streamed_response_wrapper(
            dataset_items.batch_create,
        )


class AsyncDatasetItemsResourceWithStreamingResponse:
    def __init__(self, dataset_items: AsyncDatasetItemsResource) -> None:
        self._dataset_items = dataset_items

        self.retrieve = async_to_streamed_response_wrapper(
            dataset_items.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            dataset_items.update,
        )
        self.list = async_to_streamed_response_wrapper(
            dataset_items.list,
        )
        self.archive = async_to_streamed_response_wrapper(
            dataset_items.archive,
        )
        self.batch_create = async_to_streamed_response_wrapper(
            dataset_items.batch_create,
        )
