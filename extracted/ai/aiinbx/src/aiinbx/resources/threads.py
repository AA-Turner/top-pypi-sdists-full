# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Iterable
from typing_extensions import Literal

import httpx

from ..types import thread_search_params, thread_forward_params
from .._types import Body, Omit, Query, Headers, NotGiven, SequenceNotStr, omit, not_given
from .._utils import maybe_transform, async_maybe_transform
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import make_request_options
from ..types.thread_search_response import ThreadSearchResponse
from ..types.thread_forward_response import ThreadForwardResponse
from ..types.thread_retrieve_response import ThreadRetrieveResponse

__all__ = ["ThreadsResource", "AsyncThreadsResource"]


class ThreadsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ThreadsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/aiinbx/aiinbx-py#accessing-raw-response-data-eg-headers
        """
        return ThreadsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ThreadsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/aiinbx/aiinbx-py#with_streaming_response
        """
        return ThreadsResourceWithStreamingResponse(self)

    def retrieve(
        self,
        thread_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ThreadRetrieveResponse:
        """
        Retrieve a specific thread with all its emails by thread ID using API key
        authentication

        Args:
          thread_id: The unique identifier of the thread

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not thread_id:
            raise ValueError(f"Expected a non-empty value for `thread_id` but received {thread_id!r}")
        return self._get(
            f"/threads/{thread_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ThreadRetrieveResponse,
        )

    def forward(
        self,
        thread_id: str,
        *,
        to: Union[str, SequenceNotStr[str]],
        attachments: Iterable[thread_forward_params.Attachment] | Omit = omit,
        bcc: Union[str, SequenceNotStr[str]] | Omit = omit,
        cc: Union[str, SequenceNotStr[str]] | Omit = omit,
        from_: str | Omit = omit,
        from_name: str | Omit = omit,
        include_attachments: bool | Omit = omit,
        is_draft: bool | Omit = omit,
        note: str | Omit = omit,
        track_clicks: bool | Omit = omit,
        track_opens: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ThreadForwardResponse:
        """
        Forward the entire thread as a readable transcript.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not thread_id:
            raise ValueError(f"Expected a non-empty value for `thread_id` but received {thread_id!r}")
        return self._post(
            f"/threads/{thread_id}/forward",
            body=maybe_transform(
                {
                    "to": to,
                    "attachments": attachments,
                    "bcc": bcc,
                    "cc": cc,
                    "from_": from_,
                    "from_name": from_name,
                    "include_attachments": include_attachments,
                    "is_draft": is_draft,
                    "note": note,
                    "track_clicks": track_clicks,
                    "track_opens": track_opens,
                },
                thread_forward_params.ThreadForwardParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ThreadForwardResponse,
        )

    def search(
        self,
        *,
        conversation_state: Literal["awaiting_reply", "needs_reply", "active", "stale"] | Omit = omit,
        created_after: str | Omit = omit,
        created_before: str | Omit = omit,
        has_email_from_address: str | Omit = omit,
        has_email_to_address: str | Omit = omit,
        has_participant_emails: SequenceNotStr[str] | Omit = omit,
        last_email_after: str | Omit = omit,
        last_email_before: str | Omit = omit,
        limit: float | Omit = omit,
        offset: float | Omit = omit,
        some_email_has_direction: Literal["INBOUND", "OUTBOUND"] | Omit = omit,
        some_email_has_status: Literal[
            "DRAFT",
            "QUEUED",
            "ACCEPTED",
            "SENT",
            "RECEIVED",
            "FAILED",
            "BOUNCED",
            "COMPLAINED",
            "REJECTED",
            "READ",
            "ARCHIVED",
        ]
        | Omit = omit,
        sort_by: Literal["createdAt", "lastEmailAt", "subject"] | Omit = omit,
        sort_order: Literal["asc", "desc"] | Omit = omit,
        stale_threshold_days: float | Omit = omit,
        subject_contains: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ThreadSearchResponse:
        """
        Search threads with various filtering options optimized for AI agents

        Args:
          conversation_state: Filter threads by conversation state

          created_after: Filter threads created after this date

          created_before: Filter threads created before this date

          has_email_from_address: Filter threads with emails from this address

          has_email_to_address: Filter threads with emails to this address

          has_participant_emails: Filter threads that include all of these email addresses as participants

          last_email_after: Filter threads with last email after this date

          last_email_before: Filter threads with last email before this date

          limit: Number of threads to return (1-100)

          offset: Number of threads to skip

          some_email_has_direction: Filter threads containing emails with this direction

          some_email_has_status: Filter threads containing emails with this status

          sort_by: Field to sort by

          sort_order: Sort order

          stale_threshold_days: Days to consider a thread stale (used with conversationState=stale)

          subject_contains: Filter threads where subject contains this text

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/threads/search",
            body=maybe_transform(
                {
                    "conversation_state": conversation_state,
                    "created_after": created_after,
                    "created_before": created_before,
                    "has_email_from_address": has_email_from_address,
                    "has_email_to_address": has_email_to_address,
                    "has_participant_emails": has_participant_emails,
                    "last_email_after": last_email_after,
                    "last_email_before": last_email_before,
                    "limit": limit,
                    "offset": offset,
                    "some_email_has_direction": some_email_has_direction,
                    "some_email_has_status": some_email_has_status,
                    "sort_by": sort_by,
                    "sort_order": sort_order,
                    "stale_threshold_days": stale_threshold_days,
                    "subject_contains": subject_contains,
                },
                thread_search_params.ThreadSearchParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ThreadSearchResponse,
        )


class AsyncThreadsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncThreadsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/aiinbx/aiinbx-py#accessing-raw-response-data-eg-headers
        """
        return AsyncThreadsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncThreadsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/aiinbx/aiinbx-py#with_streaming_response
        """
        return AsyncThreadsResourceWithStreamingResponse(self)

    async def retrieve(
        self,
        thread_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ThreadRetrieveResponse:
        """
        Retrieve a specific thread with all its emails by thread ID using API key
        authentication

        Args:
          thread_id: The unique identifier of the thread

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not thread_id:
            raise ValueError(f"Expected a non-empty value for `thread_id` but received {thread_id!r}")
        return await self._get(
            f"/threads/{thread_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ThreadRetrieveResponse,
        )

    async def forward(
        self,
        thread_id: str,
        *,
        to: Union[str, SequenceNotStr[str]],
        attachments: Iterable[thread_forward_params.Attachment] | Omit = omit,
        bcc: Union[str, SequenceNotStr[str]] | Omit = omit,
        cc: Union[str, SequenceNotStr[str]] | Omit = omit,
        from_: str | Omit = omit,
        from_name: str | Omit = omit,
        include_attachments: bool | Omit = omit,
        is_draft: bool | Omit = omit,
        note: str | Omit = omit,
        track_clicks: bool | Omit = omit,
        track_opens: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ThreadForwardResponse:
        """
        Forward the entire thread as a readable transcript.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not thread_id:
            raise ValueError(f"Expected a non-empty value for `thread_id` but received {thread_id!r}")
        return await self._post(
            f"/threads/{thread_id}/forward",
            body=await async_maybe_transform(
                {
                    "to": to,
                    "attachments": attachments,
                    "bcc": bcc,
                    "cc": cc,
                    "from_": from_,
                    "from_name": from_name,
                    "include_attachments": include_attachments,
                    "is_draft": is_draft,
                    "note": note,
                    "track_clicks": track_clicks,
                    "track_opens": track_opens,
                },
                thread_forward_params.ThreadForwardParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ThreadForwardResponse,
        )

    async def search(
        self,
        *,
        conversation_state: Literal["awaiting_reply", "needs_reply", "active", "stale"] | Omit = omit,
        created_after: str | Omit = omit,
        created_before: str | Omit = omit,
        has_email_from_address: str | Omit = omit,
        has_email_to_address: str | Omit = omit,
        has_participant_emails: SequenceNotStr[str] | Omit = omit,
        last_email_after: str | Omit = omit,
        last_email_before: str | Omit = omit,
        limit: float | Omit = omit,
        offset: float | Omit = omit,
        some_email_has_direction: Literal["INBOUND", "OUTBOUND"] | Omit = omit,
        some_email_has_status: Literal[
            "DRAFT",
            "QUEUED",
            "ACCEPTED",
            "SENT",
            "RECEIVED",
            "FAILED",
            "BOUNCED",
            "COMPLAINED",
            "REJECTED",
            "READ",
            "ARCHIVED",
        ]
        | Omit = omit,
        sort_by: Literal["createdAt", "lastEmailAt", "subject"] | Omit = omit,
        sort_order: Literal["asc", "desc"] | Omit = omit,
        stale_threshold_days: float | Omit = omit,
        subject_contains: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ThreadSearchResponse:
        """
        Search threads with various filtering options optimized for AI agents

        Args:
          conversation_state: Filter threads by conversation state

          created_after: Filter threads created after this date

          created_before: Filter threads created before this date

          has_email_from_address: Filter threads with emails from this address

          has_email_to_address: Filter threads with emails to this address

          has_participant_emails: Filter threads that include all of these email addresses as participants

          last_email_after: Filter threads with last email after this date

          last_email_before: Filter threads with last email before this date

          limit: Number of threads to return (1-100)

          offset: Number of threads to skip

          some_email_has_direction: Filter threads containing emails with this direction

          some_email_has_status: Filter threads containing emails with this status

          sort_by: Field to sort by

          sort_order: Sort order

          stale_threshold_days: Days to consider a thread stale (used with conversationState=stale)

          subject_contains: Filter threads where subject contains this text

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/threads/search",
            body=await async_maybe_transform(
                {
                    "conversation_state": conversation_state,
                    "created_after": created_after,
                    "created_before": created_before,
                    "has_email_from_address": has_email_from_address,
                    "has_email_to_address": has_email_to_address,
                    "has_participant_emails": has_participant_emails,
                    "last_email_after": last_email_after,
                    "last_email_before": last_email_before,
                    "limit": limit,
                    "offset": offset,
                    "some_email_has_direction": some_email_has_direction,
                    "some_email_has_status": some_email_has_status,
                    "sort_by": sort_by,
                    "sort_order": sort_order,
                    "stale_threshold_days": stale_threshold_days,
                    "subject_contains": subject_contains,
                },
                thread_search_params.ThreadSearchParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ThreadSearchResponse,
        )


class ThreadsResourceWithRawResponse:
    def __init__(self, threads: ThreadsResource) -> None:
        self._threads = threads

        self.retrieve = to_raw_response_wrapper(
            threads.retrieve,
        )
        self.forward = to_raw_response_wrapper(
            threads.forward,
        )
        self.search = to_raw_response_wrapper(
            threads.search,
        )


class AsyncThreadsResourceWithRawResponse:
    def __init__(self, threads: AsyncThreadsResource) -> None:
        self._threads = threads

        self.retrieve = async_to_raw_response_wrapper(
            threads.retrieve,
        )
        self.forward = async_to_raw_response_wrapper(
            threads.forward,
        )
        self.search = async_to_raw_response_wrapper(
            threads.search,
        )


class ThreadsResourceWithStreamingResponse:
    def __init__(self, threads: ThreadsResource) -> None:
        self._threads = threads

        self.retrieve = to_streamed_response_wrapper(
            threads.retrieve,
        )
        self.forward = to_streamed_response_wrapper(
            threads.forward,
        )
        self.search = to_streamed_response_wrapper(
            threads.search,
        )


class AsyncThreadsResourceWithStreamingResponse:
    def __init__(self, threads: AsyncThreadsResource) -> None:
        self._threads = threads

        self.retrieve = async_to_streamed_response_wrapper(
            threads.retrieve,
        )
        self.forward = async_to_streamed_response_wrapper(
            threads.forward,
        )
        self.search = async_to_streamed_response_wrapper(
            threads.search,
        )
