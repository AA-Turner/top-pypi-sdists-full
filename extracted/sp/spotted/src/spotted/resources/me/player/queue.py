# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ...._types import Body, Omit, Query, Headers, NoneType, NotGiven, omit, not_given
from ...._utils import maybe_transform, async_maybe_transform
from ...._compat import cached_property
from ...._resource import SyncAPIResource, AsyncAPIResource
from ...._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ...._base_client import make_request_options
from ....types.me.player import queue_add_params
from ....types.me.player.queue_get_response import QueueGetResponse

__all__ = ["QueueResource", "AsyncQueueResource"]


class QueueResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> QueueResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cjavdev/spotted-py#accessing-raw-response-data-eg-headers
        """
        return QueueResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> QueueResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cjavdev/spotted-py#with_streaming_response
        """
        return QueueResourceWithStreamingResponse(self)

    def add(
        self,
        *,
        uri: str,
        device_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> None:
        """Add an item to be played next in the user's current playback queue.

        This API
        only works for users who have Spotify Premium. The order of execution is not
        guaranteed when you use this API with other Player API endpoints.

        Args:
          uri: The uri of the item to add to the queue. Must be a track or an episode uri.

          device_id: The id of the device this command is targeting. If not supplied, the user's
              currently active device is the target.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._post(
            "/me/player/queue",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "uri": uri,
                        "device_id": device_id,
                    },
                    queue_add_params.QueueAddParams,
                ),
            ),
            cast_to=NoneType,
        )

    def get(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> QueueGetResponse:
        """Get the list of objects that make up the user's queue."""
        return self._get(
            "/me/player/queue",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=QueueGetResponse,
        )


class AsyncQueueResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncQueueResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cjavdev/spotted-py#accessing-raw-response-data-eg-headers
        """
        return AsyncQueueResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncQueueResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cjavdev/spotted-py#with_streaming_response
        """
        return AsyncQueueResourceWithStreamingResponse(self)

    async def add(
        self,
        *,
        uri: str,
        device_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> None:
        """Add an item to be played next in the user's current playback queue.

        This API
        only works for users who have Spotify Premium. The order of execution is not
        guaranteed when you use this API with other Player API endpoints.

        Args:
          uri: The uri of the item to add to the queue. Must be a track or an episode uri.

          device_id: The id of the device this command is targeting. If not supplied, the user's
              currently active device is the target.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._post(
            "/me/player/queue",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "uri": uri,
                        "device_id": device_id,
                    },
                    queue_add_params.QueueAddParams,
                ),
            ),
            cast_to=NoneType,
        )

    async def get(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> QueueGetResponse:
        """Get the list of objects that make up the user's queue."""
        return await self._get(
            "/me/player/queue",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=QueueGetResponse,
        )


class QueueResourceWithRawResponse:
    def __init__(self, queue: QueueResource) -> None:
        self._queue = queue

        self.add = to_raw_response_wrapper(
            queue.add,
        )
        self.get = to_raw_response_wrapper(
            queue.get,
        )


class AsyncQueueResourceWithRawResponse:
    def __init__(self, queue: AsyncQueueResource) -> None:
        self._queue = queue

        self.add = async_to_raw_response_wrapper(
            queue.add,
        )
        self.get = async_to_raw_response_wrapper(
            queue.get,
        )


class QueueResourceWithStreamingResponse:
    def __init__(self, queue: QueueResource) -> None:
        self._queue = queue

        self.add = to_streamed_response_wrapper(
            queue.add,
        )
        self.get = to_streamed_response_wrapper(
            queue.get,
        )


class AsyncQueueResourceWithStreamingResponse:
    def __init__(self, queue: AsyncQueueResource) -> None:
        self._queue = queue

        self.add = async_to_streamed_response_wrapper(
            queue.add,
        )
        self.get = async_to_streamed_response_wrapper(
            queue.get,
        )
