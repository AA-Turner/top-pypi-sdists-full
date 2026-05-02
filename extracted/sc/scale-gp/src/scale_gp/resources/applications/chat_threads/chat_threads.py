# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ...._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from ...._utils import maybe_transform
from ...._compat import cached_property
from ...._resource import SyncAPIResource, AsyncAPIResource
from ...._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ....pagination import SyncTopLevelArray, AsyncTopLevelArray
from ...._base_client import AsyncPaginator, make_request_options
from ....types.chat_thread import ChatThread
from ....types.applications import chat_thread_list_params

__all__ = ["ChatThreadsResource", "AsyncChatThreadsResource"]


class ChatThreadsResource(SyncAPIResource):
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

    def list(
        self,
        application_variant_id: str,
        *,
        include_archived: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SyncTopLevelArray[ChatThread]:
        """
        List Application Threads

        Args:
          include_archived: Include archived threads in the response.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not application_variant_id:
            raise ValueError(
                f"Expected a non-empty value for `application_variant_id` but received {application_variant_id!r}"
            )
        return self._get_api_list(
            f"/v4/applications/{application_variant_id}/threads",
            page=SyncTopLevelArray[ChatThread],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {"include_archived": include_archived}, chat_thread_list_params.ChatThreadListParams
                ),
            ),
            model=ChatThread,
        )


class AsyncChatThreadsResource(AsyncAPIResource):
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

    def list(
        self,
        application_variant_id: str,
        *,
        include_archived: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[ChatThread, AsyncTopLevelArray[ChatThread]]:
        """
        List Application Threads

        Args:
          include_archived: Include archived threads in the response.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not application_variant_id:
            raise ValueError(
                f"Expected a non-empty value for `application_variant_id` but received {application_variant_id!r}"
            )
        return self._get_api_list(
            f"/v4/applications/{application_variant_id}/threads",
            page=AsyncTopLevelArray[ChatThread],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {"include_archived": include_archived}, chat_thread_list_params.ChatThreadListParams
                ),
            ),
            model=ChatThread,
        )


class ChatThreadsResourceWithRawResponse:
    def __init__(self, chat_threads: ChatThreadsResource) -> None:
        self._chat_threads = chat_threads

        self.list = to_raw_response_wrapper(
            chat_threads.list,
        )


class AsyncChatThreadsResourceWithRawResponse:
    def __init__(self, chat_threads: AsyncChatThreadsResource) -> None:
        self._chat_threads = chat_threads

        self.list = async_to_raw_response_wrapper(
            chat_threads.list,
        )


class ChatThreadsResourceWithStreamingResponse:
    def __init__(self, chat_threads: ChatThreadsResource) -> None:
        self._chat_threads = chat_threads

        self.list = to_streamed_response_wrapper(
            chat_threads.list,
        )


class AsyncChatThreadsResourceWithStreamingResponse:
    def __init__(self, chat_threads: AsyncChatThreadsResource) -> None:
        self._chat_threads = chat_threads

        self.list = async_to_streamed_response_wrapper(
            chat_threads.list,
        )
