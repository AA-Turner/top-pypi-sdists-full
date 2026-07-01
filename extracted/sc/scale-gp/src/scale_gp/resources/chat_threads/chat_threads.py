# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict

import httpx

from ...types import chat_thread_update_params
from ..._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from ..._utils import path_template, maybe_transform, async_maybe_transform
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..._base_client import make_request_options
from .messages.messages import (
    MessagesResource,
    AsyncMessagesResource,
    MessagesResourceWithRawResponse,
    AsyncMessagesResourceWithRawResponse,
    MessagesResourceWithStreamingResponse,
    AsyncMessagesResourceWithStreamingResponse,
)
from ...types.chat_thread import ChatThread

__all__ = ["ChatThreadsResource", "AsyncChatThreadsResource"]


class ChatThreadsResource(SyncAPIResource):
    @cached_property
    def messages(self) -> MessagesResource:
        return MessagesResource(self._client)

    @cached_property
    def with_raw_response(self) -> ChatThreadsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python#accessing-raw-response-data-eg-headers
        """
        return ChatThreadsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ChatThreadsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python#with_streaming_response
        """
        return ChatThreadsResourceWithStreamingResponse(self)

    def update(
        self,
        thread_id: str,
        *,
        archived_at: str | Omit = omit,
        thread_metadata: Dict[str, object] | Omit = omit,
        title: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ChatThread:
        """
        Patch Chat Thread

        Args:
          archived_at: Date when the chat thread is archived, or None to un-archive.

          thread_metadata: The metadata associated with the thread

          title: The title of the chat thread.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not thread_id:
            raise ValueError(f"Expected a non-empty value for `thread_id` but received {thread_id!r}")
        return self._patch(
            path_template("/v4/threads/{thread_id}", thread_id=thread_id),
            body=maybe_transform(
                {
                    "archived_at": archived_at,
                    "thread_metadata": thread_metadata,
                    "title": title,
                },
                chat_thread_update_params.ChatThreadUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ChatThread,
        )

    def delete(
        self,
        thread_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> object:
        """
        Delete Chat Thread

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not thread_id:
            raise ValueError(f"Expected a non-empty value for `thread_id` but received {thread_id!r}")
        return self._delete(
            path_template("/v4/threads/{thread_id}", thread_id=thread_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )


class AsyncChatThreadsResource(AsyncAPIResource):
    @cached_property
    def messages(self) -> AsyncMessagesResource:
        return AsyncMessagesResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncChatThreadsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python#accessing-raw-response-data-eg-headers
        """
        return AsyncChatThreadsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncChatThreadsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python#with_streaming_response
        """
        return AsyncChatThreadsResourceWithStreamingResponse(self)

    async def update(
        self,
        thread_id: str,
        *,
        archived_at: str | Omit = omit,
        thread_metadata: Dict[str, object] | Omit = omit,
        title: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ChatThread:
        """
        Patch Chat Thread

        Args:
          archived_at: Date when the chat thread is archived, or None to un-archive.

          thread_metadata: The metadata associated with the thread

          title: The title of the chat thread.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not thread_id:
            raise ValueError(f"Expected a non-empty value for `thread_id` but received {thread_id!r}")
        return await self._patch(
            path_template("/v4/threads/{thread_id}", thread_id=thread_id),
            body=await async_maybe_transform(
                {
                    "archived_at": archived_at,
                    "thread_metadata": thread_metadata,
                    "title": title,
                },
                chat_thread_update_params.ChatThreadUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ChatThread,
        )

    async def delete(
        self,
        thread_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> object:
        """
        Delete Chat Thread

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not thread_id:
            raise ValueError(f"Expected a non-empty value for `thread_id` but received {thread_id!r}")
        return await self._delete(
            path_template("/v4/threads/{thread_id}", thread_id=thread_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )


class ChatThreadsResourceWithRawResponse:
    def __init__(self, chat_threads: ChatThreadsResource) -> None:
        self._chat_threads = chat_threads

        self.update = to_raw_response_wrapper(
            chat_threads.update,
        )
        self.delete = to_raw_response_wrapper(
            chat_threads.delete,
        )

    @cached_property
    def messages(self) -> MessagesResourceWithRawResponse:
        return MessagesResourceWithRawResponse(self._chat_threads.messages)


class AsyncChatThreadsResourceWithRawResponse:
    def __init__(self, chat_threads: AsyncChatThreadsResource) -> None:
        self._chat_threads = chat_threads

        self.update = async_to_raw_response_wrapper(
            chat_threads.update,
        )
        self.delete = async_to_raw_response_wrapper(
            chat_threads.delete,
        )

    @cached_property
    def messages(self) -> AsyncMessagesResourceWithRawResponse:
        return AsyncMessagesResourceWithRawResponse(self._chat_threads.messages)


class ChatThreadsResourceWithStreamingResponse:
    def __init__(self, chat_threads: ChatThreadsResource) -> None:
        self._chat_threads = chat_threads

        self.update = to_streamed_response_wrapper(
            chat_threads.update,
        )
        self.delete = to_streamed_response_wrapper(
            chat_threads.delete,
        )

    @cached_property
    def messages(self) -> MessagesResourceWithStreamingResponse:
        return MessagesResourceWithStreamingResponse(self._chat_threads.messages)


class AsyncChatThreadsResourceWithStreamingResponse:
    def __init__(self, chat_threads: AsyncChatThreadsResource) -> None:
        self._chat_threads = chat_threads

        self.update = async_to_streamed_response_wrapper(
            chat_threads.update,
        )
        self.delete = async_to_streamed_response_wrapper(
            chat_threads.delete,
        )

    @cached_property
    def messages(self) -> AsyncMessagesResourceWithStreamingResponse:
        return AsyncMessagesResourceWithStreamingResponse(self._chat_threads.messages)
