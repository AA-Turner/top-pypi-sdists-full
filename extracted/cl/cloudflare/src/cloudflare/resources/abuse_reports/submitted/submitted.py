# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Type, Union, cast
from datetime import datetime
from typing_extensions import Literal

import httpx

from .emails import (
    EmailsResource,
    AsyncEmailsResource,
    EmailsResourceWithRawResponse,
    AsyncEmailsResourceWithRawResponse,
    EmailsResourceWithStreamingResponse,
    AsyncEmailsResourceWithStreamingResponse,
)
from ...._types import Body, Omit, Query, Headers, NotGiven, SequenceNotStr, omit, not_given
from ...._utils import path_template, maybe_transform
from ...._compat import cached_property
from ...._resource import SyncAPIResource, AsyncAPIResource
from ...._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ...._wrappers import ResultWrapper
from ....pagination import SyncV4PagePagination, AsyncV4PagePagination
from ...._base_client import AsyncPaginator, make_request_options
from ....types.abuse_reports import submitted_list_params
from ....types.abuse_reports.submitted_get_response import SubmittedGetResponse
from ....types.abuse_reports.submitted_list_response import SubmittedListResponse

__all__ = ["SubmittedResource", "AsyncSubmittedResource"]


class SubmittedResource(SyncAPIResource):
    @cached_property
    def emails(self) -> EmailsResource:
        return EmailsResource(self._client)

    @cached_property
    def with_raw_response(self) -> SubmittedResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cloudflare/cloudflare-python#accessing-raw-response-data-eg-headers
        """
        return SubmittedResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> SubmittedResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cloudflare/cloudflare-python#with_streaming_response
        """
        return SubmittedResourceWithStreamingResponse(self)

    def list(
        self,
        *,
        account_id: str,
        id: str | Omit = omit,
        created_after: Union[str, datetime] | Omit = omit,
        created_before: Union[str, datetime] | Omit = omit,
        domain: SequenceNotStr[str] | Omit = omit,
        page: int | Omit = omit,
        per_page: int | Omit = omit,
        sort: str | Omit = omit,
        status: List[Literal["submitted", "accepted", "denied"]] | Omit = omit,
        type: List[Literal["PHISH", "GEN", "THREAT", "DMCA", "EMER", "TM", "REG_WHO", "NCSEI", "NETWORK"]]
        | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SyncV4PagePagination[SubmittedListResponse]:
        """
        List abuse reports submitted by the account.

        Args:
          id: Filter by report code.

          created_after: Return reports submitted after this time.

          created_before: Return reports submitted before this time.

          domain: Filter by reported domain. This parameter can be specified multiple times.

          page: Page of submitted reports to return.

          per_page: Number of submitted reports per page.

          sort: A property and direction to sort by (id, cdate, domain, type, status).

          status: Filter by submitter-facing status. This parameter can be specified multiple
              times.

          type: Filter by report type. This parameter can be specified multiple times.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not account_id:
            raise ValueError(f"Expected a non-empty value for `account_id` but received {account_id!r}")
        return self._get_api_list(
            path_template("/accounts/{account_id}/abuse-reports/submitted", account_id=account_id),
            page=SyncV4PagePagination[SubmittedListResponse],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "id": id,
                        "created_after": created_after,
                        "created_before": created_before,
                        "domain": domain,
                        "page": page,
                        "per_page": per_page,
                        "sort": sort,
                        "status": status,
                        "type": type,
                    },
                    submitted_list_params.SubmittedListParams,
                ),
            ),
            model=SubmittedListResponse,
        )

    def get(
        self,
        report_id: str,
        *,
        account_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SubmittedGetResponse:
        """
        Retrieve a report submitted by the account.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not account_id:
            raise ValueError(f"Expected a non-empty value for `account_id` but received {account_id!r}")
        if not report_id:
            raise ValueError(f"Expected a non-empty value for `report_id` but received {report_id!r}")
        return self._get(
            path_template(
                "/accounts/{account_id}/abuse-reports/submitted/{report_id}", account_id=account_id, report_id=report_id
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                post_parser=ResultWrapper[SubmittedGetResponse]._unwrapper,
            ),
            cast_to=cast(Type[SubmittedGetResponse], ResultWrapper[SubmittedGetResponse]),
        )


class AsyncSubmittedResource(AsyncAPIResource):
    @cached_property
    def emails(self) -> AsyncEmailsResource:
        return AsyncEmailsResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncSubmittedResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cloudflare/cloudflare-python#accessing-raw-response-data-eg-headers
        """
        return AsyncSubmittedResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncSubmittedResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cloudflare/cloudflare-python#with_streaming_response
        """
        return AsyncSubmittedResourceWithStreamingResponse(self)

    def list(
        self,
        *,
        account_id: str,
        id: str | Omit = omit,
        created_after: Union[str, datetime] | Omit = omit,
        created_before: Union[str, datetime] | Omit = omit,
        domain: SequenceNotStr[str] | Omit = omit,
        page: int | Omit = omit,
        per_page: int | Omit = omit,
        sort: str | Omit = omit,
        status: List[Literal["submitted", "accepted", "denied"]] | Omit = omit,
        type: List[Literal["PHISH", "GEN", "THREAT", "DMCA", "EMER", "TM", "REG_WHO", "NCSEI", "NETWORK"]]
        | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[SubmittedListResponse, AsyncV4PagePagination[SubmittedListResponse]]:
        """
        List abuse reports submitted by the account.

        Args:
          id: Filter by report code.

          created_after: Return reports submitted after this time.

          created_before: Return reports submitted before this time.

          domain: Filter by reported domain. This parameter can be specified multiple times.

          page: Page of submitted reports to return.

          per_page: Number of submitted reports per page.

          sort: A property and direction to sort by (id, cdate, domain, type, status).

          status: Filter by submitter-facing status. This parameter can be specified multiple
              times.

          type: Filter by report type. This parameter can be specified multiple times.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not account_id:
            raise ValueError(f"Expected a non-empty value for `account_id` but received {account_id!r}")
        return self._get_api_list(
            path_template("/accounts/{account_id}/abuse-reports/submitted", account_id=account_id),
            page=AsyncV4PagePagination[SubmittedListResponse],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "id": id,
                        "created_after": created_after,
                        "created_before": created_before,
                        "domain": domain,
                        "page": page,
                        "per_page": per_page,
                        "sort": sort,
                        "status": status,
                        "type": type,
                    },
                    submitted_list_params.SubmittedListParams,
                ),
            ),
            model=SubmittedListResponse,
        )

    async def get(
        self,
        report_id: str,
        *,
        account_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SubmittedGetResponse:
        """
        Retrieve a report submitted by the account.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not account_id:
            raise ValueError(f"Expected a non-empty value for `account_id` but received {account_id!r}")
        if not report_id:
            raise ValueError(f"Expected a non-empty value for `report_id` but received {report_id!r}")
        return await self._get(
            path_template(
                "/accounts/{account_id}/abuse-reports/submitted/{report_id}", account_id=account_id, report_id=report_id
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                post_parser=ResultWrapper[SubmittedGetResponse]._unwrapper,
            ),
            cast_to=cast(Type[SubmittedGetResponse], ResultWrapper[SubmittedGetResponse]),
        )


class SubmittedResourceWithRawResponse:
    def __init__(self, submitted: SubmittedResource) -> None:
        self._submitted = submitted

        self.list = to_raw_response_wrapper(
            submitted.list,
        )
        self.get = to_raw_response_wrapper(
            submitted.get,
        )

    @cached_property
    def emails(self) -> EmailsResourceWithRawResponse:
        return EmailsResourceWithRawResponse(self._submitted.emails)


class AsyncSubmittedResourceWithRawResponse:
    def __init__(self, submitted: AsyncSubmittedResource) -> None:
        self._submitted = submitted

        self.list = async_to_raw_response_wrapper(
            submitted.list,
        )
        self.get = async_to_raw_response_wrapper(
            submitted.get,
        )

    @cached_property
    def emails(self) -> AsyncEmailsResourceWithRawResponse:
        return AsyncEmailsResourceWithRawResponse(self._submitted.emails)


class SubmittedResourceWithStreamingResponse:
    def __init__(self, submitted: SubmittedResource) -> None:
        self._submitted = submitted

        self.list = to_streamed_response_wrapper(
            submitted.list,
        )
        self.get = to_streamed_response_wrapper(
            submitted.get,
        )

    @cached_property
    def emails(self) -> EmailsResourceWithStreamingResponse:
        return EmailsResourceWithStreamingResponse(self._submitted.emails)


class AsyncSubmittedResourceWithStreamingResponse:
    def __init__(self, submitted: AsyncSubmittedResource) -> None:
        self._submitted = submitted

        self.list = async_to_streamed_response_wrapper(
            submitted.list,
        )
        self.get = async_to_streamed_response_wrapper(
            submitted.get,
        )

    @cached_property
    def emails(self) -> AsyncEmailsResourceWithStreamingResponse:
        return AsyncEmailsResourceWithStreamingResponse(self._submitted.emails)
