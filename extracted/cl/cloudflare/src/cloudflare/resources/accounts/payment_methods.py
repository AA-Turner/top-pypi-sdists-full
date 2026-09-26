# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Any, Type, cast
from typing_extensions import Literal

import httpx

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
from ..._wrappers import ResultWrapper
from ...pagination import SyncV4PagePaginationArray, AsyncV4PagePaginationArray
from ..._base_client import AsyncPaginator, make_request_options
from ...types.accounts import payment_method_list_params, payment_method_create_params, payment_method_update_params
from ...types.accounts.payment_method_get_response import PaymentMethodGetResponse
from ...types.accounts.payment_method_list_response import PaymentMethodListResponse
from ...types.accounts.payment_method_create_response import PaymentMethodCreateResponse
from ...types.accounts.payment_method_delete_response import PaymentMethodDeleteResponse
from ...types.accounts.payment_method_update_response import PaymentMethodUpdateResponse
from ...types.accounts.payment_method_set_as_default_response import PaymentMethodSetAsDefaultResponse

__all__ = ["PaymentMethodsResource", "AsyncPaymentMethodsResource"]


class PaymentMethodsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> PaymentMethodsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cloudflare/cloudflare-python#accessing-raw-response-data-eg-headers
        """
        return PaymentMethodsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> PaymentMethodsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cloudflare/cloudflare-python#with_streaming_response
        """
        return PaymentMethodsResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        account_id: str,
        address: str | Omit = omit,
        address2: str | Omit = omit,
        bank_account_type: str | Omit = omit,
        bank_code: str | Omit = omit,
        bank_country: str | Omit = omit,
        bank_name: str | Omit = omit,
        bank_routing_number: str | Omit = omit,
        cashapp_cash_tag: str | Omit = omit,
        city: str | Omit = omit,
        country: str | Omit = omit,
        default: bool | Omit = omit,
        device_data: str | Omit = omit,
        first_name: str | Omit = omit,
        last_name: str | Omit = omit,
        nick_name: str | Omit = omit,
        payment_account_email: str | Omit = omit,
        payment_email: str | Omit = omit,
        payment_gateway: str | Omit = omit,
        payment_nonce: str | Omit = omit,
        state: str | Omit = omit,
        type: Literal["CREDIT_CARD", "PAYPAL", "CASHAPP", "SEPA_DEBIT", "LINK", "ACH_DIRECT_DEBIT"] | Omit = omit,
        zipcode: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> PaymentMethodCreateResponse:
        """
        Creates a new payment method for an account.

        Args:
          account_id: Identifier

          address: Billing address line 1.

          address2: Billing address line 2.

          bank_account_type: Bank account type.

          bank_code: Bank code.

          bank_country: Bank country.

          bank_name: Bank name for bank-based payment methods.

          bank_routing_number: Bank routing number.

          cashapp_cash_tag: Cash App cash tag.

          city: Billing city.

          country: Billing country.

          default: Whether this is the default payment method.

          device_data: Device data for fraud prevention.

          first_name: Billing first name.

          last_name: Billing last name.

          nick_name: A nickname for the payment method.

          payment_account_email: Email associated with the payment account.

          payment_email: Payment email address.

          payment_gateway: The payment gateway used.

          payment_nonce: Payment nonce for tokenized payments.

          state: Billing state.

          type: The payment method type.

          zipcode: Billing zip code.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not account_id:
            raise ValueError(f"Expected a non-empty value for `account_id` but received {account_id!r}")
        return self._post(
            path_template("/accounts/{account_id}/payment-methods", account_id=account_id),
            body=maybe_transform(
                {
                    "address": address,
                    "address2": address2,
                    "bank_account_type": bank_account_type,
                    "bank_code": bank_code,
                    "bank_country": bank_country,
                    "bank_name": bank_name,
                    "bank_routing_number": bank_routing_number,
                    "cashapp_cash_tag": cashapp_cash_tag,
                    "city": city,
                    "country": country,
                    "default": default,
                    "device_data": device_data,
                    "first_name": first_name,
                    "last_name": last_name,
                    "nick_name": nick_name,
                    "payment_account_email": payment_account_email,
                    "payment_email": payment_email,
                    "payment_gateway": payment_gateway,
                    "payment_nonce": payment_nonce,
                    "state": state,
                    "type": type,
                    "zipcode": zipcode,
                },
                payment_method_create_params.PaymentMethodCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                post_parser=ResultWrapper[PaymentMethodCreateResponse]._unwrapper,
            ),
            cast_to=cast(Type[PaymentMethodCreateResponse], ResultWrapper[PaymentMethodCreateResponse]),
        )

    def update(
        self,
        payment_method_id: str,
        *,
        account_id: str,
        address: str | Omit = omit,
        address2: str | Omit = omit,
        bank_account_type: str | Omit = omit,
        bank_code: str | Omit = omit,
        bank_country: str | Omit = omit,
        bank_name: str | Omit = omit,
        bank_routing_number: str | Omit = omit,
        cashapp_cash_tag: str | Omit = omit,
        city: str | Omit = omit,
        country: str | Omit = omit,
        default: bool | Omit = omit,
        device_data: str | Omit = omit,
        first_name: str | Omit = omit,
        last_name: str | Omit = omit,
        nick_name: str | Omit = omit,
        payment_account_email: str | Omit = omit,
        payment_email: str | Omit = omit,
        payment_gateway: str | Omit = omit,
        payment_nonce: str | Omit = omit,
        state: str | Omit = omit,
        type: Literal["CREDIT_CARD", "PAYPAL", "CASHAPP", "SEPA_DEBIT", "LINK", "ACH_DIRECT_DEBIT"] | Omit = omit,
        zipcode: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> PaymentMethodUpdateResponse:
        """
        Updates a payment method for an account.

        Args:
          account_id: Identifier

          payment_method_id: Identifier

          address: Billing address line 1.

          address2: Billing address line 2.

          bank_account_type: Bank account type.

          bank_code: Bank code.

          bank_country: Bank country.

          bank_name: Bank name for bank-based payment methods.

          bank_routing_number: Bank routing number.

          cashapp_cash_tag: Cash App cash tag.

          city: Billing city.

          country: Billing country.

          default: Whether this is the default payment method.

          device_data: Device data for fraud prevention.

          first_name: Billing first name.

          last_name: Billing last name.

          nick_name: A nickname for the payment method.

          payment_account_email: Email associated with the payment account.

          payment_email: Payment email address.

          payment_gateway: The payment gateway used.

          payment_nonce: Payment nonce for tokenized payments.

          state: Billing state.

          type: The payment method type.

          zipcode: Billing zip code.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not account_id:
            raise ValueError(f"Expected a non-empty value for `account_id` but received {account_id!r}")
        if not payment_method_id:
            raise ValueError(f"Expected a non-empty value for `payment_method_id` but received {payment_method_id!r}")
        return self._put(
            path_template(
                "/accounts/{account_id}/payment-methods/{payment_method_id}",
                account_id=account_id,
                payment_method_id=payment_method_id,
            ),
            body=maybe_transform(
                {
                    "address": address,
                    "address2": address2,
                    "bank_account_type": bank_account_type,
                    "bank_code": bank_code,
                    "bank_country": bank_country,
                    "bank_name": bank_name,
                    "bank_routing_number": bank_routing_number,
                    "cashapp_cash_tag": cashapp_cash_tag,
                    "city": city,
                    "country": country,
                    "default": default,
                    "device_data": device_data,
                    "first_name": first_name,
                    "last_name": last_name,
                    "nick_name": nick_name,
                    "payment_account_email": payment_account_email,
                    "payment_email": payment_email,
                    "payment_gateway": payment_gateway,
                    "payment_nonce": payment_nonce,
                    "state": state,
                    "type": type,
                    "zipcode": zipcode,
                },
                payment_method_update_params.PaymentMethodUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                post_parser=ResultWrapper[PaymentMethodUpdateResponse]._unwrapper,
            ),
            cast_to=cast(Type[PaymentMethodUpdateResponse], ResultWrapper[PaymentMethodUpdateResponse]),
        )

    def list(
        self,
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
    ) -> SyncV4PagePaginationArray[PaymentMethodListResponse]:
        """
        Lists all payment methods for an account.

        Args:
          account_id: Identifier

          page: Page number of paginated results.

          per_page: Number of items per page.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not account_id:
            raise ValueError(f"Expected a non-empty value for `account_id` but received {account_id!r}")
        return self._get_api_list(
            path_template("/accounts/{account_id}/payment-methods", account_id=account_id),
            page=SyncV4PagePaginationArray[PaymentMethodListResponse],
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
                    payment_method_list_params.PaymentMethodListParams,
                ),
            ),
            model=PaymentMethodListResponse,
        )

    def delete(
        self,
        payment_method_id: str,
        *,
        account_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> PaymentMethodDeleteResponse:
        """
        Deletes a payment method from an account.

        Args:
          account_id: Identifier

          payment_method_id: Identifier

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not account_id:
            raise ValueError(f"Expected a non-empty value for `account_id` but received {account_id!r}")
        if not payment_method_id:
            raise ValueError(f"Expected a non-empty value for `payment_method_id` but received {payment_method_id!r}")
        return cast(
            PaymentMethodDeleteResponse,
            self._delete(
                path_template(
                    "/accounts/{account_id}/payment-methods/{payment_method_id}",
                    account_id=account_id,
                    payment_method_id=payment_method_id,
                ),
                options=make_request_options(
                    extra_headers=extra_headers,
                    extra_query=extra_query,
                    extra_body=extra_body,
                    timeout=timeout,
                    post_parser=ResultWrapper[PaymentMethodDeleteResponse]._unwrapper,
                ),
                cast_to=cast(
                    Any, ResultWrapper[PaymentMethodDeleteResponse]
                ),  # Union types cannot be passed in as arguments in the type system
            ),
        )

    def get(
        self,
        payment_method_id: str,
        *,
        account_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> PaymentMethodGetResponse:
        """
        Gets a specific payment method for an account.

        Args:
          account_id: Identifier

          payment_method_id: Identifier

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not account_id:
            raise ValueError(f"Expected a non-empty value for `account_id` but received {account_id!r}")
        if not payment_method_id:
            raise ValueError(f"Expected a non-empty value for `payment_method_id` but received {payment_method_id!r}")
        return self._get(
            path_template(
                "/accounts/{account_id}/payment-methods/{payment_method_id}",
                account_id=account_id,
                payment_method_id=payment_method_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                post_parser=ResultWrapper[PaymentMethodGetResponse]._unwrapper,
            ),
            cast_to=cast(Type[PaymentMethodGetResponse], ResultWrapper[PaymentMethodGetResponse]),
        )

    def set_as_default(
        self,
        payment_method_id: str,
        *,
        account_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> PaymentMethodSetAsDefaultResponse:
        """
        Sets a payment method as the default for an account.

        Args:
          account_id: Identifier

          payment_method_id: Identifier

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not account_id:
            raise ValueError(f"Expected a non-empty value for `account_id` but received {account_id!r}")
        if not payment_method_id:
            raise ValueError(f"Expected a non-empty value for `payment_method_id` but received {payment_method_id!r}")
        return cast(
            PaymentMethodSetAsDefaultResponse,
            self._post(
                path_template(
                    "/accounts/{account_id}/payment-methods/{payment_method_id}/set-as-default",
                    account_id=account_id,
                    payment_method_id=payment_method_id,
                ),
                options=make_request_options(
                    extra_headers=extra_headers,
                    extra_query=extra_query,
                    extra_body=extra_body,
                    timeout=timeout,
                    post_parser=ResultWrapper[PaymentMethodSetAsDefaultResponse]._unwrapper,
                ),
                cast_to=cast(
                    Any, ResultWrapper[PaymentMethodSetAsDefaultResponse]
                ),  # Union types cannot be passed in as arguments in the type system
            ),
        )


class AsyncPaymentMethodsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncPaymentMethodsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cloudflare/cloudflare-python#accessing-raw-response-data-eg-headers
        """
        return AsyncPaymentMethodsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncPaymentMethodsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cloudflare/cloudflare-python#with_streaming_response
        """
        return AsyncPaymentMethodsResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        account_id: str,
        address: str | Omit = omit,
        address2: str | Omit = omit,
        bank_account_type: str | Omit = omit,
        bank_code: str | Omit = omit,
        bank_country: str | Omit = omit,
        bank_name: str | Omit = omit,
        bank_routing_number: str | Omit = omit,
        cashapp_cash_tag: str | Omit = omit,
        city: str | Omit = omit,
        country: str | Omit = omit,
        default: bool | Omit = omit,
        device_data: str | Omit = omit,
        first_name: str | Omit = omit,
        last_name: str | Omit = omit,
        nick_name: str | Omit = omit,
        payment_account_email: str | Omit = omit,
        payment_email: str | Omit = omit,
        payment_gateway: str | Omit = omit,
        payment_nonce: str | Omit = omit,
        state: str | Omit = omit,
        type: Literal["CREDIT_CARD", "PAYPAL", "CASHAPP", "SEPA_DEBIT", "LINK", "ACH_DIRECT_DEBIT"] | Omit = omit,
        zipcode: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> PaymentMethodCreateResponse:
        """
        Creates a new payment method for an account.

        Args:
          account_id: Identifier

          address: Billing address line 1.

          address2: Billing address line 2.

          bank_account_type: Bank account type.

          bank_code: Bank code.

          bank_country: Bank country.

          bank_name: Bank name for bank-based payment methods.

          bank_routing_number: Bank routing number.

          cashapp_cash_tag: Cash App cash tag.

          city: Billing city.

          country: Billing country.

          default: Whether this is the default payment method.

          device_data: Device data for fraud prevention.

          first_name: Billing first name.

          last_name: Billing last name.

          nick_name: A nickname for the payment method.

          payment_account_email: Email associated with the payment account.

          payment_email: Payment email address.

          payment_gateway: The payment gateway used.

          payment_nonce: Payment nonce for tokenized payments.

          state: Billing state.

          type: The payment method type.

          zipcode: Billing zip code.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not account_id:
            raise ValueError(f"Expected a non-empty value for `account_id` but received {account_id!r}")
        return await self._post(
            path_template("/accounts/{account_id}/payment-methods", account_id=account_id),
            body=await async_maybe_transform(
                {
                    "address": address,
                    "address2": address2,
                    "bank_account_type": bank_account_type,
                    "bank_code": bank_code,
                    "bank_country": bank_country,
                    "bank_name": bank_name,
                    "bank_routing_number": bank_routing_number,
                    "cashapp_cash_tag": cashapp_cash_tag,
                    "city": city,
                    "country": country,
                    "default": default,
                    "device_data": device_data,
                    "first_name": first_name,
                    "last_name": last_name,
                    "nick_name": nick_name,
                    "payment_account_email": payment_account_email,
                    "payment_email": payment_email,
                    "payment_gateway": payment_gateway,
                    "payment_nonce": payment_nonce,
                    "state": state,
                    "type": type,
                    "zipcode": zipcode,
                },
                payment_method_create_params.PaymentMethodCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                post_parser=ResultWrapper[PaymentMethodCreateResponse]._unwrapper,
            ),
            cast_to=cast(Type[PaymentMethodCreateResponse], ResultWrapper[PaymentMethodCreateResponse]),
        )

    async def update(
        self,
        payment_method_id: str,
        *,
        account_id: str,
        address: str | Omit = omit,
        address2: str | Omit = omit,
        bank_account_type: str | Omit = omit,
        bank_code: str | Omit = omit,
        bank_country: str | Omit = omit,
        bank_name: str | Omit = omit,
        bank_routing_number: str | Omit = omit,
        cashapp_cash_tag: str | Omit = omit,
        city: str | Omit = omit,
        country: str | Omit = omit,
        default: bool | Omit = omit,
        device_data: str | Omit = omit,
        first_name: str | Omit = omit,
        last_name: str | Omit = omit,
        nick_name: str | Omit = omit,
        payment_account_email: str | Omit = omit,
        payment_email: str | Omit = omit,
        payment_gateway: str | Omit = omit,
        payment_nonce: str | Omit = omit,
        state: str | Omit = omit,
        type: Literal["CREDIT_CARD", "PAYPAL", "CASHAPP", "SEPA_DEBIT", "LINK", "ACH_DIRECT_DEBIT"] | Omit = omit,
        zipcode: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> PaymentMethodUpdateResponse:
        """
        Updates a payment method for an account.

        Args:
          account_id: Identifier

          payment_method_id: Identifier

          address: Billing address line 1.

          address2: Billing address line 2.

          bank_account_type: Bank account type.

          bank_code: Bank code.

          bank_country: Bank country.

          bank_name: Bank name for bank-based payment methods.

          bank_routing_number: Bank routing number.

          cashapp_cash_tag: Cash App cash tag.

          city: Billing city.

          country: Billing country.

          default: Whether this is the default payment method.

          device_data: Device data for fraud prevention.

          first_name: Billing first name.

          last_name: Billing last name.

          nick_name: A nickname for the payment method.

          payment_account_email: Email associated with the payment account.

          payment_email: Payment email address.

          payment_gateway: The payment gateway used.

          payment_nonce: Payment nonce for tokenized payments.

          state: Billing state.

          type: The payment method type.

          zipcode: Billing zip code.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not account_id:
            raise ValueError(f"Expected a non-empty value for `account_id` but received {account_id!r}")
        if not payment_method_id:
            raise ValueError(f"Expected a non-empty value for `payment_method_id` but received {payment_method_id!r}")
        return await self._put(
            path_template(
                "/accounts/{account_id}/payment-methods/{payment_method_id}",
                account_id=account_id,
                payment_method_id=payment_method_id,
            ),
            body=await async_maybe_transform(
                {
                    "address": address,
                    "address2": address2,
                    "bank_account_type": bank_account_type,
                    "bank_code": bank_code,
                    "bank_country": bank_country,
                    "bank_name": bank_name,
                    "bank_routing_number": bank_routing_number,
                    "cashapp_cash_tag": cashapp_cash_tag,
                    "city": city,
                    "country": country,
                    "default": default,
                    "device_data": device_data,
                    "first_name": first_name,
                    "last_name": last_name,
                    "nick_name": nick_name,
                    "payment_account_email": payment_account_email,
                    "payment_email": payment_email,
                    "payment_gateway": payment_gateway,
                    "payment_nonce": payment_nonce,
                    "state": state,
                    "type": type,
                    "zipcode": zipcode,
                },
                payment_method_update_params.PaymentMethodUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                post_parser=ResultWrapper[PaymentMethodUpdateResponse]._unwrapper,
            ),
            cast_to=cast(Type[PaymentMethodUpdateResponse], ResultWrapper[PaymentMethodUpdateResponse]),
        )

    def list(
        self,
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
    ) -> AsyncPaginator[PaymentMethodListResponse, AsyncV4PagePaginationArray[PaymentMethodListResponse]]:
        """
        Lists all payment methods for an account.

        Args:
          account_id: Identifier

          page: Page number of paginated results.

          per_page: Number of items per page.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not account_id:
            raise ValueError(f"Expected a non-empty value for `account_id` but received {account_id!r}")
        return self._get_api_list(
            path_template("/accounts/{account_id}/payment-methods", account_id=account_id),
            page=AsyncV4PagePaginationArray[PaymentMethodListResponse],
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
                    payment_method_list_params.PaymentMethodListParams,
                ),
            ),
            model=PaymentMethodListResponse,
        )

    async def delete(
        self,
        payment_method_id: str,
        *,
        account_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> PaymentMethodDeleteResponse:
        """
        Deletes a payment method from an account.

        Args:
          account_id: Identifier

          payment_method_id: Identifier

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not account_id:
            raise ValueError(f"Expected a non-empty value for `account_id` but received {account_id!r}")
        if not payment_method_id:
            raise ValueError(f"Expected a non-empty value for `payment_method_id` but received {payment_method_id!r}")
        return cast(
            PaymentMethodDeleteResponse,
            await self._delete(
                path_template(
                    "/accounts/{account_id}/payment-methods/{payment_method_id}",
                    account_id=account_id,
                    payment_method_id=payment_method_id,
                ),
                options=make_request_options(
                    extra_headers=extra_headers,
                    extra_query=extra_query,
                    extra_body=extra_body,
                    timeout=timeout,
                    post_parser=ResultWrapper[PaymentMethodDeleteResponse]._unwrapper,
                ),
                cast_to=cast(
                    Any, ResultWrapper[PaymentMethodDeleteResponse]
                ),  # Union types cannot be passed in as arguments in the type system
            ),
        )

    async def get(
        self,
        payment_method_id: str,
        *,
        account_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> PaymentMethodGetResponse:
        """
        Gets a specific payment method for an account.

        Args:
          account_id: Identifier

          payment_method_id: Identifier

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not account_id:
            raise ValueError(f"Expected a non-empty value for `account_id` but received {account_id!r}")
        if not payment_method_id:
            raise ValueError(f"Expected a non-empty value for `payment_method_id` but received {payment_method_id!r}")
        return await self._get(
            path_template(
                "/accounts/{account_id}/payment-methods/{payment_method_id}",
                account_id=account_id,
                payment_method_id=payment_method_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                post_parser=ResultWrapper[PaymentMethodGetResponse]._unwrapper,
            ),
            cast_to=cast(Type[PaymentMethodGetResponse], ResultWrapper[PaymentMethodGetResponse]),
        )

    async def set_as_default(
        self,
        payment_method_id: str,
        *,
        account_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> PaymentMethodSetAsDefaultResponse:
        """
        Sets a payment method as the default for an account.

        Args:
          account_id: Identifier

          payment_method_id: Identifier

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not account_id:
            raise ValueError(f"Expected a non-empty value for `account_id` but received {account_id!r}")
        if not payment_method_id:
            raise ValueError(f"Expected a non-empty value for `payment_method_id` but received {payment_method_id!r}")
        return cast(
            PaymentMethodSetAsDefaultResponse,
            await self._post(
                path_template(
                    "/accounts/{account_id}/payment-methods/{payment_method_id}/set-as-default",
                    account_id=account_id,
                    payment_method_id=payment_method_id,
                ),
                options=make_request_options(
                    extra_headers=extra_headers,
                    extra_query=extra_query,
                    extra_body=extra_body,
                    timeout=timeout,
                    post_parser=ResultWrapper[PaymentMethodSetAsDefaultResponse]._unwrapper,
                ),
                cast_to=cast(
                    Any, ResultWrapper[PaymentMethodSetAsDefaultResponse]
                ),  # Union types cannot be passed in as arguments in the type system
            ),
        )


class PaymentMethodsResourceWithRawResponse:
    def __init__(self, payment_methods: PaymentMethodsResource) -> None:
        self._payment_methods = payment_methods

        self.create = to_raw_response_wrapper(
            payment_methods.create,
        )
        self.update = to_raw_response_wrapper(
            payment_methods.update,
        )
        self.list = to_raw_response_wrapper(
            payment_methods.list,
        )
        self.delete = to_raw_response_wrapper(
            payment_methods.delete,
        )
        self.get = to_raw_response_wrapper(
            payment_methods.get,
        )
        self.set_as_default = to_raw_response_wrapper(
            payment_methods.set_as_default,
        )


class AsyncPaymentMethodsResourceWithRawResponse:
    def __init__(self, payment_methods: AsyncPaymentMethodsResource) -> None:
        self._payment_methods = payment_methods

        self.create = async_to_raw_response_wrapper(
            payment_methods.create,
        )
        self.update = async_to_raw_response_wrapper(
            payment_methods.update,
        )
        self.list = async_to_raw_response_wrapper(
            payment_methods.list,
        )
        self.delete = async_to_raw_response_wrapper(
            payment_methods.delete,
        )
        self.get = async_to_raw_response_wrapper(
            payment_methods.get,
        )
        self.set_as_default = async_to_raw_response_wrapper(
            payment_methods.set_as_default,
        )


class PaymentMethodsResourceWithStreamingResponse:
    def __init__(self, payment_methods: PaymentMethodsResource) -> None:
        self._payment_methods = payment_methods

        self.create = to_streamed_response_wrapper(
            payment_methods.create,
        )
        self.update = to_streamed_response_wrapper(
            payment_methods.update,
        )
        self.list = to_streamed_response_wrapper(
            payment_methods.list,
        )
        self.delete = to_streamed_response_wrapper(
            payment_methods.delete,
        )
        self.get = to_streamed_response_wrapper(
            payment_methods.get,
        )
        self.set_as_default = to_streamed_response_wrapper(
            payment_methods.set_as_default,
        )


class AsyncPaymentMethodsResourceWithStreamingResponse:
    def __init__(self, payment_methods: AsyncPaymentMethodsResource) -> None:
        self._payment_methods = payment_methods

        self.create = async_to_streamed_response_wrapper(
            payment_methods.create,
        )
        self.update = async_to_streamed_response_wrapper(
            payment_methods.update,
        )
        self.list = async_to_streamed_response_wrapper(
            payment_methods.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            payment_methods.delete,
        )
        self.get = async_to_streamed_response_wrapper(
            payment_methods.get,
        )
        self.set_as_default = async_to_streamed_response_wrapper(
            payment_methods.set_as_default,
        )
