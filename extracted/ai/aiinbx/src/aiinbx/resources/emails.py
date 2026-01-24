# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Iterable

import httpx

from ..types import email_send_params, email_reply_params
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
from ..types.email_send_response import EmailSendResponse
from ..types.email_reply_response import EmailReplyResponse
from ..types.email_retrieve_response import EmailRetrieveResponse

__all__ = ["EmailsResource", "AsyncEmailsResource"]


class EmailsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> EmailsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/aiinbx/aiinbx-py#accessing-raw-response-data-eg-headers
        """
        return EmailsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> EmailsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/aiinbx/aiinbx-py#with_streaming_response
        """
        return EmailsResourceWithStreamingResponse(self)

    def retrieve(
        self,
        email_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> EmailRetrieveResponse:
        """
        Retrieve a specific email by its ID using API key authentication

        Args:
          email_id: The unique identifier of the email

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not email_id:
            raise ValueError(f"Expected a non-empty value for `email_id` but received {email_id!r}")
        return self._get(
            f"/emails/{email_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EmailRetrieveResponse,
        )

    def reply(
        self,
        email_id: str,
        *,
        from_: str,
        html: str,
        attachments: Iterable[email_reply_params.Attachment] | Omit = omit,
        bcc: Union[str, SequenceNotStr[str]] | Omit = omit,
        cc: Union[str, SequenceNotStr[str]] | Omit = omit,
        from_name: str | Omit = omit,
        is_draft: bool | Omit = omit,
        reply_all: bool | Omit = omit,
        subject: str | Omit = omit,
        text: str | Omit = omit,
        to: Union[str, SequenceNotStr[str]] | Omit = omit,
        track_clicks: bool | Omit = omit,
        track_opens: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> EmailReplyResponse:
        """Reply to an existing email.

        Automatically handles reply headers (In-Reply-To,
        References) and thread association. The reply will be sent from a verified
        domain belonging to the organization.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not email_id:
            raise ValueError(f"Expected a non-empty value for `email_id` but received {email_id!r}")
        return self._post(
            f"/emails/{email_id}/reply",
            body=maybe_transform(
                {
                    "from_": from_,
                    "html": html,
                    "attachments": attachments,
                    "bcc": bcc,
                    "cc": cc,
                    "from_name": from_name,
                    "is_draft": is_draft,
                    "reply_all": reply_all,
                    "subject": subject,
                    "text": text,
                    "to": to,
                    "track_clicks": track_clicks,
                    "track_opens": track_opens,
                },
                email_reply_params.EmailReplyParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EmailReplyResponse,
        )

    def send(
        self,
        *,
        from_: str,
        html: str,
        subject: str,
        to: Union[str, SequenceNotStr[str]],
        attachments: Iterable[email_send_params.Attachment] | Omit = omit,
        bcc: Union[str, SequenceNotStr[str]] | Omit = omit,
        cc: Union[str, SequenceNotStr[str]] | Omit = omit,
        from_name: str | Omit = omit,
        in_reply_to: str | Omit = omit,
        is_draft: bool | Omit = omit,
        references: SequenceNotStr[str] | Omit = omit,
        reply_to: Union[str, SequenceNotStr[str]] | Omit = omit,
        text: str | Omit = omit,
        thread_id: str | Omit = omit,
        track_clicks: bool | Omit = omit,
        track_opens: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> EmailSendResponse:
        """Send an email from a verified domain belonging to the organization.

        Useful for
        transactional or conversational messages. Returns metadata including identifiers
        for further queries.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/emails/send",
            body=maybe_transform(
                {
                    "from_": from_,
                    "html": html,
                    "subject": subject,
                    "to": to,
                    "attachments": attachments,
                    "bcc": bcc,
                    "cc": cc,
                    "from_name": from_name,
                    "in_reply_to": in_reply_to,
                    "is_draft": is_draft,
                    "references": references,
                    "reply_to": reply_to,
                    "text": text,
                    "thread_id": thread_id,
                    "track_clicks": track_clicks,
                    "track_opens": track_opens,
                },
                email_send_params.EmailSendParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EmailSendResponse,
        )


class AsyncEmailsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncEmailsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/aiinbx/aiinbx-py#accessing-raw-response-data-eg-headers
        """
        return AsyncEmailsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncEmailsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/aiinbx/aiinbx-py#with_streaming_response
        """
        return AsyncEmailsResourceWithStreamingResponse(self)

    async def retrieve(
        self,
        email_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> EmailRetrieveResponse:
        """
        Retrieve a specific email by its ID using API key authentication

        Args:
          email_id: The unique identifier of the email

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not email_id:
            raise ValueError(f"Expected a non-empty value for `email_id` but received {email_id!r}")
        return await self._get(
            f"/emails/{email_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EmailRetrieveResponse,
        )

    async def reply(
        self,
        email_id: str,
        *,
        from_: str,
        html: str,
        attachments: Iterable[email_reply_params.Attachment] | Omit = omit,
        bcc: Union[str, SequenceNotStr[str]] | Omit = omit,
        cc: Union[str, SequenceNotStr[str]] | Omit = omit,
        from_name: str | Omit = omit,
        is_draft: bool | Omit = omit,
        reply_all: bool | Omit = omit,
        subject: str | Omit = omit,
        text: str | Omit = omit,
        to: Union[str, SequenceNotStr[str]] | Omit = omit,
        track_clicks: bool | Omit = omit,
        track_opens: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> EmailReplyResponse:
        """Reply to an existing email.

        Automatically handles reply headers (In-Reply-To,
        References) and thread association. The reply will be sent from a verified
        domain belonging to the organization.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not email_id:
            raise ValueError(f"Expected a non-empty value for `email_id` but received {email_id!r}")
        return await self._post(
            f"/emails/{email_id}/reply",
            body=await async_maybe_transform(
                {
                    "from_": from_,
                    "html": html,
                    "attachments": attachments,
                    "bcc": bcc,
                    "cc": cc,
                    "from_name": from_name,
                    "is_draft": is_draft,
                    "reply_all": reply_all,
                    "subject": subject,
                    "text": text,
                    "to": to,
                    "track_clicks": track_clicks,
                    "track_opens": track_opens,
                },
                email_reply_params.EmailReplyParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EmailReplyResponse,
        )

    async def send(
        self,
        *,
        from_: str,
        html: str,
        subject: str,
        to: Union[str, SequenceNotStr[str]],
        attachments: Iterable[email_send_params.Attachment] | Omit = omit,
        bcc: Union[str, SequenceNotStr[str]] | Omit = omit,
        cc: Union[str, SequenceNotStr[str]] | Omit = omit,
        from_name: str | Omit = omit,
        in_reply_to: str | Omit = omit,
        is_draft: bool | Omit = omit,
        references: SequenceNotStr[str] | Omit = omit,
        reply_to: Union[str, SequenceNotStr[str]] | Omit = omit,
        text: str | Omit = omit,
        thread_id: str | Omit = omit,
        track_clicks: bool | Omit = omit,
        track_opens: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> EmailSendResponse:
        """Send an email from a verified domain belonging to the organization.

        Useful for
        transactional or conversational messages. Returns metadata including identifiers
        for further queries.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/emails/send",
            body=await async_maybe_transform(
                {
                    "from_": from_,
                    "html": html,
                    "subject": subject,
                    "to": to,
                    "attachments": attachments,
                    "bcc": bcc,
                    "cc": cc,
                    "from_name": from_name,
                    "in_reply_to": in_reply_to,
                    "is_draft": is_draft,
                    "references": references,
                    "reply_to": reply_to,
                    "text": text,
                    "thread_id": thread_id,
                    "track_clicks": track_clicks,
                    "track_opens": track_opens,
                },
                email_send_params.EmailSendParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EmailSendResponse,
        )


class EmailsResourceWithRawResponse:
    def __init__(self, emails: EmailsResource) -> None:
        self._emails = emails

        self.retrieve = to_raw_response_wrapper(
            emails.retrieve,
        )
        self.reply = to_raw_response_wrapper(
            emails.reply,
        )
        self.send = to_raw_response_wrapper(
            emails.send,
        )


class AsyncEmailsResourceWithRawResponse:
    def __init__(self, emails: AsyncEmailsResource) -> None:
        self._emails = emails

        self.retrieve = async_to_raw_response_wrapper(
            emails.retrieve,
        )
        self.reply = async_to_raw_response_wrapper(
            emails.reply,
        )
        self.send = async_to_raw_response_wrapper(
            emails.send,
        )


class EmailsResourceWithStreamingResponse:
    def __init__(self, emails: EmailsResource) -> None:
        self._emails = emails

        self.retrieve = to_streamed_response_wrapper(
            emails.retrieve,
        )
        self.reply = to_streamed_response_wrapper(
            emails.reply,
        )
        self.send = to_streamed_response_wrapper(
            emails.send,
        )


class AsyncEmailsResourceWithStreamingResponse:
    def __init__(self, emails: AsyncEmailsResource) -> None:
        self._emails = emails

        self.retrieve = async_to_streamed_response_wrapper(
            emails.retrieve,
        )
        self.reply = async_to_streamed_response_wrapper(
            emails.reply,
        )
        self.send = async_to_streamed_response_wrapper(
            emails.send,
        )
