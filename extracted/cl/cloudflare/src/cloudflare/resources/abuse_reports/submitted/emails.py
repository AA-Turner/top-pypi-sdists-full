# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ...._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from ...._utils import path_template, maybe_transform
from ...._compat import cached_property
from ...._resource import SyncAPIResource, AsyncAPIResource
from ...._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ....pagination import SyncV4PagePagination, AsyncV4PagePagination
from ...._base_client import AsyncPaginator, make_request_options
from ....types.abuse_reports.submitted import email_list_params
from ....types.abuse_reports.submitted.email_list_response import EmailListResponse

__all__ = ["EmailsResource", "AsyncEmailsResource"]


class EmailsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> EmailsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cloudflare/cloudflare-python#accessing-raw-response-data-eg-headers
        """
        return EmailsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> EmailsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cloudflare/cloudflare-python#with_streaming_response
        """
        return EmailsResourceWithStreamingResponse(self)

    def list(
        self,
        report_id: str,
        *,
        account_id: str,
        page: int | Omit = omit,
        per_page: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SyncV4PagePagination[EmailListResponse]:
        """
        List successful emails sent to the submitter of a report submitted by the
        account. Does not include emails sent to customers or hosts.

        Args:
          page: Page number to retrieve (default 1).

          per_page: Number of emails per page (default 20, max 100).

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not account_id:
            raise ValueError(f"Expected a non-empty value for `account_id` but received {account_id!r}")
        if not report_id:
            raise ValueError(f"Expected a non-empty value for `report_id` but received {report_id!r}")
        return self._get_api_list(
            path_template(
                "/accounts/{account_id}/abuse-reports/submitted/{report_id}/emails",
                account_id=account_id,
                report_id=report_id,
            ),
            page=SyncV4PagePagination[EmailListResponse],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "page": page,
                        "per_page": per_page,
                    },
                    email_list_params.EmailListParams,
                ),
            ),
            model=EmailListResponse,
        )


class AsyncEmailsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncEmailsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cloudflare/cloudflare-python#accessing-raw-response-data-eg-headers
        """
        return AsyncEmailsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncEmailsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cloudflare/cloudflare-python#with_streaming_response
        """
        return AsyncEmailsResourceWithStreamingResponse(self)

    def list(
        self,
        report_id: str,
        *,
        account_id: str,
        page: int | Omit = omit,
        per_page: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[EmailListResponse, AsyncV4PagePagination[EmailListResponse]]:
        """
        List successful emails sent to the submitter of a report submitted by the
        account. Does not include emails sent to customers or hosts.

        Args:
          page: Page number to retrieve (default 1).

          per_page: Number of emails per page (default 20, max 100).

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not account_id:
            raise ValueError(f"Expected a non-empty value for `account_id` but received {account_id!r}")
        if not report_id:
            raise ValueError(f"Expected a non-empty value for `report_id` but received {report_id!r}")
        return self._get_api_list(
            path_template(
                "/accounts/{account_id}/abuse-reports/submitted/{report_id}/emails",
                account_id=account_id,
                report_id=report_id,
            ),
            page=AsyncV4PagePagination[EmailListResponse],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "page": page,
                        "per_page": per_page,
                    },
                    email_list_params.EmailListParams,
                ),
            ),
            model=EmailListResponse,
        )


class EmailsResourceWithRawResponse:
    def __init__(self, emails: EmailsResource) -> None:
        self._emails = emails

        self.list = to_raw_response_wrapper(
            emails.list,
        )


class AsyncEmailsResourceWithRawResponse:
    def __init__(self, emails: AsyncEmailsResource) -> None:
        self._emails = emails

        self.list = async_to_raw_response_wrapper(
            emails.list,
        )


class EmailsResourceWithStreamingResponse:
    def __init__(self, emails: EmailsResource) -> None:
        self._emails = emails

        self.list = to_streamed_response_wrapper(
            emails.list,
        )


class AsyncEmailsResourceWithStreamingResponse:
    def __init__(self, emails: AsyncEmailsResource) -> None:
        self._emails = emails

        self.list = async_to_streamed_response_wrapper(
            emails.list,
        )
