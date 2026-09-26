# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Type, cast

import httpx

from ..._types import Body, Query, Headers, NotGiven, not_given
from ..._utils import path_template
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..._wrappers import ResultWrapper
from ..._base_client import make_request_options
from ...types.registrar.workflow_status import WorkflowStatus

__all__ = ["TransferInStatusResource", "AsyncTransferInStatusResource"]


class TransferInStatusResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> TransferInStatusResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cloudflare/cloudflare-python#accessing-raw-response-data-eg-headers
        """
        return TransferInStatusResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> TransferInStatusResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cloudflare/cloudflare-python#with_streaming_response
        """
        return TransferInStatusResourceWithStreamingResponse(self)

    def get(
        self,
        domain_name: str,
        *,
        account_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> WorkflowStatus:
        """
        Returns the current status of a domain transfer workflow.

        Use this endpoint to poll transfer progress after initiating a transfer with
        `POST /accounts/{account_id}/registrar/registrations/{domain_name}/transfer-in`.
        The URL is provided in the `links.self` field of the transfer response.

        ### Transfer timelines

        Transfers typically take 1–10 days due to ICANN-mandated approval windows.

        ### Workflow states

        **Terminal states:** `succeeded` and `failed` are terminal and always have
        `completed: true`.

        **Non-terminal states:**

        - `in_progress`: Transfer has been submitted to the registry and is being
          processed. Continue polling.
        - `blocked`: The workflow is waiting on the losing registrar or registry to
          release the domain. This is the **most common state** for transfers and is
          entirely normal — it means the ICANN transfer approval window is in effect.
          The losing registrar has up to 5 days to approve or reject. Continue polling
          with longer intervals (e.g., every 30–60 minutes).
        - `action_required`: The user needs to take action (e.g., the FOA email needs to
          be accepted). See `context` for details on what is needed.
        - `pending`: Transfer workflow created but not yet started processing.

        ### Polling guidance

        Adjust your polling interval based on the current workflow state:

        - `pending` or `in_progress`: Poll every 30 seconds.
        - `blocked`: The transfer is waiting on a third party (e.g., losing registrar
          approval). Poll every 30–60 minutes.
        - `action_required`: Stop polling. The workflow will not advance until the user
          takes action. Check `context` for details on what is needed.
        - `succeeded` or `failed`: Terminal — stop polling.

        Args:
          account_id: Identifier.

          domain_name: Provides a fully qualified domain name (FQDN), including the extension (e.g.,
              `example.com`, `mybrand.app`). The domain name uniquely identifies a
              registration. Cloudflare permits only one registration per domain, making the
              domain name a natural idempotency key for registration requests.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not account_id:
            raise ValueError(f"Expected a non-empty value for `account_id` but received {account_id!r}")
        if not domain_name:
            raise ValueError(f"Expected a non-empty value for `domain_name` but received {domain_name!r}")
        return self._get(
            path_template(
                "/accounts/{account_id}/registrar/registrations/{domain_name}/transfer-in-status",
                account_id=account_id,
                domain_name=domain_name,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                post_parser=ResultWrapper[WorkflowStatus]._unwrapper,
            ),
            cast_to=cast(Type[WorkflowStatus], ResultWrapper[WorkflowStatus]),
        )


class AsyncTransferInStatusResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncTransferInStatusResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cloudflare/cloudflare-python#accessing-raw-response-data-eg-headers
        """
        return AsyncTransferInStatusResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncTransferInStatusResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cloudflare/cloudflare-python#with_streaming_response
        """
        return AsyncTransferInStatusResourceWithStreamingResponse(self)

    async def get(
        self,
        domain_name: str,
        *,
        account_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> WorkflowStatus:
        """
        Returns the current status of a domain transfer workflow.

        Use this endpoint to poll transfer progress after initiating a transfer with
        `POST /accounts/{account_id}/registrar/registrations/{domain_name}/transfer-in`.
        The URL is provided in the `links.self` field of the transfer response.

        ### Transfer timelines

        Transfers typically take 1–10 days due to ICANN-mandated approval windows.

        ### Workflow states

        **Terminal states:** `succeeded` and `failed` are terminal and always have
        `completed: true`.

        **Non-terminal states:**

        - `in_progress`: Transfer has been submitted to the registry and is being
          processed. Continue polling.
        - `blocked`: The workflow is waiting on the losing registrar or registry to
          release the domain. This is the **most common state** for transfers and is
          entirely normal — it means the ICANN transfer approval window is in effect.
          The losing registrar has up to 5 days to approve or reject. Continue polling
          with longer intervals (e.g., every 30–60 minutes).
        - `action_required`: The user needs to take action (e.g., the FOA email needs to
          be accepted). See `context` for details on what is needed.
        - `pending`: Transfer workflow created but not yet started processing.

        ### Polling guidance

        Adjust your polling interval based on the current workflow state:

        - `pending` or `in_progress`: Poll every 30 seconds.
        - `blocked`: The transfer is waiting on a third party (e.g., losing registrar
          approval). Poll every 30–60 minutes.
        - `action_required`: Stop polling. The workflow will not advance until the user
          takes action. Check `context` for details on what is needed.
        - `succeeded` or `failed`: Terminal — stop polling.

        Args:
          account_id: Identifier.

          domain_name: Provides a fully qualified domain name (FQDN), including the extension (e.g.,
              `example.com`, `mybrand.app`). The domain name uniquely identifies a
              registration. Cloudflare permits only one registration per domain, making the
              domain name a natural idempotency key for registration requests.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not account_id:
            raise ValueError(f"Expected a non-empty value for `account_id` but received {account_id!r}")
        if not domain_name:
            raise ValueError(f"Expected a non-empty value for `domain_name` but received {domain_name!r}")
        return await self._get(
            path_template(
                "/accounts/{account_id}/registrar/registrations/{domain_name}/transfer-in-status",
                account_id=account_id,
                domain_name=domain_name,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                post_parser=ResultWrapper[WorkflowStatus]._unwrapper,
            ),
            cast_to=cast(Type[WorkflowStatus], ResultWrapper[WorkflowStatus]),
        )


class TransferInStatusResourceWithRawResponse:
    def __init__(self, transfer_in_status: TransferInStatusResource) -> None:
        self._transfer_in_status = transfer_in_status

        self.get = to_raw_response_wrapper(
            transfer_in_status.get,
        )


class AsyncTransferInStatusResourceWithRawResponse:
    def __init__(self, transfer_in_status: AsyncTransferInStatusResource) -> None:
        self._transfer_in_status = transfer_in_status

        self.get = async_to_raw_response_wrapper(
            transfer_in_status.get,
        )


class TransferInStatusResourceWithStreamingResponse:
    def __init__(self, transfer_in_status: TransferInStatusResource) -> None:
        self._transfer_in_status = transfer_in_status

        self.get = to_streamed_response_wrapper(
            transfer_in_status.get,
        )


class AsyncTransferInStatusResourceWithStreamingResponse:
    def __init__(self, transfer_in_status: AsyncTransferInStatusResource) -> None:
        self._transfer_in_status = transfer_in_status

        self.get = async_to_streamed_response_wrapper(
            transfer_in_status.get,
        )
