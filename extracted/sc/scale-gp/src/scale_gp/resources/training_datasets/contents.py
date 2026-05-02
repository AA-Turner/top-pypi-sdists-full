# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..._types import Body, Query, Headers, NotGiven, not_given
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ...pagination import SyncTopLevelArray, AsyncTopLevelArray
from ..._base_client import AsyncPaginator, make_request_options
from ...types.training_dataset_generation_item import TrainingDatasetGenerationItem

__all__ = ["ContentsResource", "AsyncContentsResource"]


class ContentsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ContentsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python#accessing-raw-response-data-eg-headers
        """
        return ContentsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ContentsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python#with_streaming_response
        """
        return ContentsResourceWithStreamingResponse(self)

    def list(
        self,
        training_dataset_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SyncTopLevelArray[TrainingDatasetGenerationItem]:
        """
        Get Training Dataset Contents

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not training_dataset_id:
            raise ValueError(
                f"Expected a non-empty value for `training_dataset_id` but received {training_dataset_id!r}"
            )
        return self._get_api_list(
            f"/v4/training-datasets/{training_dataset_id}/contents",
            page=SyncTopLevelArray[TrainingDatasetGenerationItem],
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            model=TrainingDatasetGenerationItem,
        )


class AsyncContentsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncContentsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python#accessing-raw-response-data-eg-headers
        """
        return AsyncContentsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncContentsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python#with_streaming_response
        """
        return AsyncContentsResourceWithStreamingResponse(self)

    def list(
        self,
        training_dataset_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[TrainingDatasetGenerationItem, AsyncTopLevelArray[TrainingDatasetGenerationItem]]:
        """
        Get Training Dataset Contents

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not training_dataset_id:
            raise ValueError(
                f"Expected a non-empty value for `training_dataset_id` but received {training_dataset_id!r}"
            )
        return self._get_api_list(
            f"/v4/training-datasets/{training_dataset_id}/contents",
            page=AsyncTopLevelArray[TrainingDatasetGenerationItem],
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            model=TrainingDatasetGenerationItem,
        )


class ContentsResourceWithRawResponse:
    def __init__(self, contents: ContentsResource) -> None:
        self._contents = contents

        self.list = to_raw_response_wrapper(
            contents.list,
        )


class AsyncContentsResourceWithRawResponse:
    def __init__(self, contents: AsyncContentsResource) -> None:
        self._contents = contents

        self.list = async_to_raw_response_wrapper(
            contents.list,
        )


class ContentsResourceWithStreamingResponse:
    def __init__(self, contents: ContentsResource) -> None:
        self._contents = contents

        self.list = to_streamed_response_wrapper(
            contents.list,
        )


class AsyncContentsResourceWithStreamingResponse:
    def __init__(self, contents: AsyncContentsResource) -> None:
        self._contents = contents

        self.list = async_to_streamed_response_wrapper(
            contents.list,
        )
