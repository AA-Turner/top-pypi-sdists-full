# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Type, Union, cast
from typing_extensions import Literal

import httpx

from ..._types import Body, Omit, Query, Headers, NotGiven, Base64FileInput, omit, not_given
from ..._utils import path_template, maybe_transform, strip_not_given, async_maybe_transform
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
from ...types.registrar import transfer_in_create_params
from ...types.registrar.workflow_status import WorkflowStatus

__all__ = ["TransferInResource", "AsyncTransferInResource"]


class TransferInResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> TransferInResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cloudflare/cloudflare-python#accessing-raw-response-data-eg-headers
        """
        return TransferInResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> TransferInResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cloudflare/cloudflare-python#with_streaming_response
        """
        return TransferInResourceWithStreamingResponse(self)

    def create(
        self,
        domain_name: str,
        *,
        account_id: str,
        auth_code: Union[str, Base64FileInput] | Omit = omit,
        auto_renew: bool | Omit = omit,
        contact_extensions: Dict[str, object] | Omit = omit,
        contacts: transfer_in_create_params.Contacts | Omit = omit,
        privacy_mode: Literal["off", "redaction"] | Omit = omit,
        prefer: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> WorkflowStatus:
        """Starts a domain transfer-in workflow.

        This is typically a billable operation —
        successful transfers charge the account's default payment method, except for
        extensions with zero transfer pricing (e.g. UK extensions). All successful
        domain transfers are non-refundable.

        ### How transfers work

        Domain transfers move a domain from another registrar to Cloudflare. Transfers
        typically take 1-10 days due to ICANN-mandated approval windows.

        ### Prerequisites

        - The domain must already have a zone in the Cloudflare account (added through
          the dashboard or zone API).
        - The zone must have DNSSec disabled.
        - For billable transfers (i.e. extensions with non-zero transfer pricing), the
          account must have a billing profile with a valid default payment method. Set
          this up at `https://dash.cloudflare.com/{account_id}/billing/payment-info`.
        - The domain must be unlocked at the current registrar.
        - An authorization/EPP code from the current registrar is required, except for
          UK extensions — see Auth code below.

        ### Auth code

        An authorization code (also called EPP code, transfer key, or auth-info code) is
        required for most extensions, with the exception of UK extensions. Obtain this
        from your current registrar's control panel.

        The auth code in the request body must be base64-encoded per RFC 4648 §4
        (standard alphabet, no line breaks).

        ### Response behavior

        Successful transfer initiation returns `202 Accepted`. Validation or initiation
        failures return the documented `4XX` responses. Poll
        `GET /accounts/{account_id}/registrar/registrations/{domain_name}/transfer-in-status`
        to track progress.

        ### Premium domains

        Premium domain transfers are not currently supported by this API. Please use the
        [dashboard](https://dash.cloudflare.com/) for now.

        ### Billing

        The account's default payment method is charged upon successful transfer
        completion, unless the extension has zero transfer pricing (e.g. UK extensions).
        The transfer adds time to the domain's existing expiration date (typically 1
        year).

        Args:
          account_id: Identifier.

          domain_name: Provides a fully qualified domain name (FQDN), including the extension (e.g.,
              `example.com`, `mybrand.app`). The domain name uniquely identifies a
              registration. Cloudflare permits only one registration per domain, making the
              domain name a natural idempotency key for registration requests.

          auth_code: The EPP/authorization code from your current registrar, base64-encoded per RFC
              4648 §4. Obtain this from your current registrar's control panel. Required for
              all extensions, except for UK.

          auto_renew: Enable or disable automatic renewal after transfer. Defaults to `false` if
              omitted.

          contact_extensions: Registry-specific contact extension values for the registrant.
              `GET /accounts/{account_id}/registrar/extensions/{extension}` documents the
              required keys and allowed values for each extension in the
              `transfer_schema.properties.contact_extensions` object.

              Examples include `.us` nexus fields, `.uk` registrant type fields, and `.ca`
              legal type fields. Include this object only when the extension's transfer schema
              defines `contact_extensions`.

          contacts: Provides contact data for the registration request.

              The per-extension schema from
              `GET /accounts/{account_id}/registrar/extensions/{extension}` defines the
              accepted contact roles. Every currently supported extension requires only
              `contacts.registrant` from API callers. Callers may provide additional roles
              such as `technical`, `administrator`, and `billing` when the extension schema
              includes them. When a registry requires an omitted role, Cloudflare may derive
              that contact from `contacts.registrant`.

              When the request omits either the entire `contacts` object or
              `contacts.registrant`, the system uses the account's default address book entry
              as the registrant contact. The account owner must configure this default at
              `https://dash.cloudflare.com/{account_id}/domains/registrations`, where they can
              create or update the address book entry and accept the required agreement.
              Dashboard settings currently provide the only way to manage address book
              entries.

              Without either a default address book entry or a registrant contact, the
              registration request fails validation.

          privacy_mode: WHOIS privacy mode to apply after transfer completes. Defaults to the
              extension's default privacy mode (typically `redaction`).

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not account_id:
            raise ValueError(f"Expected a non-empty value for `account_id` but received {account_id!r}")
        if not domain_name:
            raise ValueError(f"Expected a non-empty value for `domain_name` but received {domain_name!r}")
        extra_headers = {**strip_not_given({"Prefer": prefer}), **(extra_headers or {})}
        return self._post(
            path_template(
                "/accounts/{account_id}/registrar/registrations/{domain_name}/transfer-in",
                account_id=account_id,
                domain_name=domain_name,
            ),
            body=maybe_transform(
                {
                    "auth_code": auth_code,
                    "auto_renew": auto_renew,
                    "contact_extensions": contact_extensions,
                    "contacts": contacts,
                    "privacy_mode": privacy_mode,
                },
                transfer_in_create_params.TransferInCreateParams,
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


class AsyncTransferInResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncTransferInResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cloudflare/cloudflare-python#accessing-raw-response-data-eg-headers
        """
        return AsyncTransferInResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncTransferInResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cloudflare/cloudflare-python#with_streaming_response
        """
        return AsyncTransferInResourceWithStreamingResponse(self)

    async def create(
        self,
        domain_name: str,
        *,
        account_id: str,
        auth_code: Union[str, Base64FileInput] | Omit = omit,
        auto_renew: bool | Omit = omit,
        contact_extensions: Dict[str, object] | Omit = omit,
        contacts: transfer_in_create_params.Contacts | Omit = omit,
        privacy_mode: Literal["off", "redaction"] | Omit = omit,
        prefer: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> WorkflowStatus:
        """Starts a domain transfer-in workflow.

        This is typically a billable operation —
        successful transfers charge the account's default payment method, except for
        extensions with zero transfer pricing (e.g. UK extensions). All successful
        domain transfers are non-refundable.

        ### How transfers work

        Domain transfers move a domain from another registrar to Cloudflare. Transfers
        typically take 1-10 days due to ICANN-mandated approval windows.

        ### Prerequisites

        - The domain must already have a zone in the Cloudflare account (added through
          the dashboard or zone API).
        - The zone must have DNSSec disabled.
        - For billable transfers (i.e. extensions with non-zero transfer pricing), the
          account must have a billing profile with a valid default payment method. Set
          this up at `https://dash.cloudflare.com/{account_id}/billing/payment-info`.
        - The domain must be unlocked at the current registrar.
        - An authorization/EPP code from the current registrar is required, except for
          UK extensions — see Auth code below.

        ### Auth code

        An authorization code (also called EPP code, transfer key, or auth-info code) is
        required for most extensions, with the exception of UK extensions. Obtain this
        from your current registrar's control panel.

        The auth code in the request body must be base64-encoded per RFC 4648 §4
        (standard alphabet, no line breaks).

        ### Response behavior

        Successful transfer initiation returns `202 Accepted`. Validation or initiation
        failures return the documented `4XX` responses. Poll
        `GET /accounts/{account_id}/registrar/registrations/{domain_name}/transfer-in-status`
        to track progress.

        ### Premium domains

        Premium domain transfers are not currently supported by this API. Please use the
        [dashboard](https://dash.cloudflare.com/) for now.

        ### Billing

        The account's default payment method is charged upon successful transfer
        completion, unless the extension has zero transfer pricing (e.g. UK extensions).
        The transfer adds time to the domain's existing expiration date (typically 1
        year).

        Args:
          account_id: Identifier.

          domain_name: Provides a fully qualified domain name (FQDN), including the extension (e.g.,
              `example.com`, `mybrand.app`). The domain name uniquely identifies a
              registration. Cloudflare permits only one registration per domain, making the
              domain name a natural idempotency key for registration requests.

          auth_code: The EPP/authorization code from your current registrar, base64-encoded per RFC
              4648 §4. Obtain this from your current registrar's control panel. Required for
              all extensions, except for UK.

          auto_renew: Enable or disable automatic renewal after transfer. Defaults to `false` if
              omitted.

          contact_extensions: Registry-specific contact extension values for the registrant.
              `GET /accounts/{account_id}/registrar/extensions/{extension}` documents the
              required keys and allowed values for each extension in the
              `transfer_schema.properties.contact_extensions` object.

              Examples include `.us` nexus fields, `.uk` registrant type fields, and `.ca`
              legal type fields. Include this object only when the extension's transfer schema
              defines `contact_extensions`.

          contacts: Provides contact data for the registration request.

              The per-extension schema from
              `GET /accounts/{account_id}/registrar/extensions/{extension}` defines the
              accepted contact roles. Every currently supported extension requires only
              `contacts.registrant` from API callers. Callers may provide additional roles
              such as `technical`, `administrator`, and `billing` when the extension schema
              includes them. When a registry requires an omitted role, Cloudflare may derive
              that contact from `contacts.registrant`.

              When the request omits either the entire `contacts` object or
              `contacts.registrant`, the system uses the account's default address book entry
              as the registrant contact. The account owner must configure this default at
              `https://dash.cloudflare.com/{account_id}/domains/registrations`, where they can
              create or update the address book entry and accept the required agreement.
              Dashboard settings currently provide the only way to manage address book
              entries.

              Without either a default address book entry or a registrant contact, the
              registration request fails validation.

          privacy_mode: WHOIS privacy mode to apply after transfer completes. Defaults to the
              extension's default privacy mode (typically `redaction`).

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not account_id:
            raise ValueError(f"Expected a non-empty value for `account_id` but received {account_id!r}")
        if not domain_name:
            raise ValueError(f"Expected a non-empty value for `domain_name` but received {domain_name!r}")
        extra_headers = {**strip_not_given({"Prefer": prefer}), **(extra_headers or {})}
        return await self._post(
            path_template(
                "/accounts/{account_id}/registrar/registrations/{domain_name}/transfer-in",
                account_id=account_id,
                domain_name=domain_name,
            ),
            body=await async_maybe_transform(
                {
                    "auth_code": auth_code,
                    "auto_renew": auto_renew,
                    "contact_extensions": contact_extensions,
                    "contacts": contacts,
                    "privacy_mode": privacy_mode,
                },
                transfer_in_create_params.TransferInCreateParams,
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


class TransferInResourceWithRawResponse:
    def __init__(self, transfer_in: TransferInResource) -> None:
        self._transfer_in = transfer_in

        self.create = to_raw_response_wrapper(
            transfer_in.create,
        )


class AsyncTransferInResourceWithRawResponse:
    def __init__(self, transfer_in: AsyncTransferInResource) -> None:
        self._transfer_in = transfer_in

        self.create = async_to_raw_response_wrapper(
            transfer_in.create,
        )


class TransferInResourceWithStreamingResponse:
    def __init__(self, transfer_in: TransferInResource) -> None:
        self._transfer_in = transfer_in

        self.create = to_streamed_response_wrapper(
            transfer_in.create,
        )


class AsyncTransferInResourceWithStreamingResponse:
    def __init__(self, transfer_in: AsyncTransferInResource) -> None:
        self._transfer_in = transfer_in

        self.create = async_to_streamed_response_wrapper(
            transfer_in.create,
        )
