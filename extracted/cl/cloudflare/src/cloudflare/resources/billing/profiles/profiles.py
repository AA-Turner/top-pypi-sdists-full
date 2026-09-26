# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Type, cast

import httpx

from ...._types import Body, Omit, Query, Headers, NoneType, NotGiven, omit, not_given
from ...._utils import path_template, maybe_transform, async_maybe_transform
from ...._compat import cached_property
from ...._resource import SyncAPIResource, AsyncAPIResource
from ...._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ...._wrappers import ResultWrapper
from .payment_method import (
    PaymentMethodResource,
    AsyncPaymentMethodResource,
    PaymentMethodResourceWithRawResponse,
    AsyncPaymentMethodResourceWithRawResponse,
    PaymentMethodResourceWithStreamingResponse,
    AsyncPaymentMethodResourceWithStreamingResponse,
)
from ...._base_client import make_request_options
from ....types.billing import profile_create_params, profile_update_params, profile_update_billing_email_params
from ....types.billing.profile_get_response import ProfileGetResponse
from ....types.billing.profile_create_response import ProfileCreateResponse
from ....types.billing.profile_update_response import ProfileUpdateResponse
from ....types.billing.profile_update_billing_email_response import ProfileUpdateBillingEmailResponse

__all__ = ["ProfilesResource", "AsyncProfilesResource"]


class ProfilesResource(SyncAPIResource):
    @cached_property
    def payment_method(self) -> PaymentMethodResource:
        return PaymentMethodResource(self._client)

    @cached_property
    def with_raw_response(self) -> ProfilesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cloudflare/cloudflare-python#accessing-raw-response-data-eg-headers
        """
        return ProfilesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ProfilesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cloudflare/cloudflare-python#with_streaming_response
        """
        return ProfilesResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        account_id: str,
        address: str | Omit = omit,
        address2: str | Omit = omit,
        billing_email: str | Omit = omit,
        buying_rate_plan: str | Omit = omit,
        captcha_challenge_jwt: str | Omit = omit,
        cf_turnstile_response: str | Omit = omit,
        city: str | Omit = omit,
        company: str | Omit = omit,
        country: str | Omit = omit,
        first_name: str | Omit = omit,
        h_captcha_response: str | Omit = omit,
        last_name: str | Omit = omit,
        preferred_locale: str | Omit = omit,
        secondary_billing_email: str | Omit = omit,
        state: str | Omit = omit,
        tax_id_type: str | Omit = omit,
        telephone: str | Omit = omit,
        vat: str | Omit = omit,
        zipcode: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ProfileCreateResponse:
        """
        Creates a billing profile for an account.

        Args:
          account_id: Identifier

          address: Street address line 1.

          address2: Street address line 2 (apt, suite, etc.).

          billing_email: Primary billing email address.

          buying_rate_plan: Rate plan being purchased right after profile setup.

          captcha_challenge_jwt: Captcha challenge JWT issued during onboarding.

          cf_turnstile_response: Cloudflare Turnstile response.

          city: City on the billing profile.

          company: Company name on the billing profile.

          country: ISO 3166-1 alpha-2 country code.

          first_name: First name on the billing profile.

          h_captcha_response: hCaptcha response.

          last_name: Last name on the billing profile.

          preferred_locale: Preferred locale for invoice rendering (BCP 47).

          secondary_billing_email: Secondary billing email address for CC on invoices.

          state: State or region on the billing profile.

          tax_id_type: Type of tax ID provided.

          telephone: Contact phone number.

          vat: VAT identifier.

          zipcode: ZIP or postal code.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not account_id:
            raise ValueError(f"Expected a non-empty value for `account_id` but received {account_id!r}")
        return self._post(
            path_template("/accounts/{account_id}/billing/profile", account_id=account_id),
            body=maybe_transform(
                {
                    "address": address,
                    "address2": address2,
                    "billing_email": billing_email,
                    "buying_rate_plan": buying_rate_plan,
                    "captcha_challenge_jwt": captcha_challenge_jwt,
                    "cf_turnstile_response": cf_turnstile_response,
                    "city": city,
                    "company": company,
                    "country": country,
                    "first_name": first_name,
                    "h_captcha_response": h_captcha_response,
                    "last_name": last_name,
                    "preferred_locale": preferred_locale,
                    "secondary_billing_email": secondary_billing_email,
                    "state": state,
                    "tax_id_type": tax_id_type,
                    "telephone": telephone,
                    "vat": vat,
                    "zipcode": zipcode,
                },
                profile_create_params.ProfileCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                post_parser=ResultWrapper[ProfileCreateResponse]._unwrapper,
            ),
            cast_to=cast(Type[ProfileCreateResponse], ResultWrapper[ProfileCreateResponse]),
        )

    def update(
        self,
        *,
        account_id: str,
        address: str | Omit = omit,
        address2: str | Omit = omit,
        billing_email: str | Omit = omit,
        buying_rate_plan: str | Omit = omit,
        captcha_challenge_jwt: str | Omit = omit,
        cf_turnstile_response: str | Omit = omit,
        city: str | Omit = omit,
        company: str | Omit = omit,
        country: str | Omit = omit,
        first_name: str | Omit = omit,
        h_captcha_response: str | Omit = omit,
        last_name: str | Omit = omit,
        preferred_locale: str | Omit = omit,
        secondary_billing_email: str | Omit = omit,
        state: str | Omit = omit,
        tax_id_type: str | Omit = omit,
        telephone: str | Omit = omit,
        vat: str | Omit = omit,
        zipcode: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ProfileUpdateResponse:
        """
        Updates the billing profile for an account.

        Args:
          account_id: Identifier

          address: Street address line 1.

          address2: Street address line 2 (apt, suite, etc.).

          billing_email: Primary billing email address.

          buying_rate_plan: Rate plan being purchased right after profile setup.

          captcha_challenge_jwt: Captcha challenge JWT issued during onboarding.

          cf_turnstile_response: Cloudflare Turnstile response.

          city: City on the billing profile.

          company: Company name on the billing profile.

          country: ISO 3166-1 alpha-2 country code.

          first_name: First name on the billing profile.

          h_captcha_response: hCaptcha response.

          last_name: Last name on the billing profile.

          preferred_locale: Preferred locale for invoice rendering (BCP 47).

          secondary_billing_email: Secondary billing email address for CC on invoices.

          state: State or region on the billing profile.

          tax_id_type: Type of tax ID provided.

          telephone: Contact phone number.

          vat: VAT identifier.

          zipcode: ZIP or postal code.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not account_id:
            raise ValueError(f"Expected a non-empty value for `account_id` but received {account_id!r}")
        return self._put(
            path_template("/accounts/{account_id}/billing/profile", account_id=account_id),
            body=maybe_transform(
                {
                    "address": address,
                    "address2": address2,
                    "billing_email": billing_email,
                    "buying_rate_plan": buying_rate_plan,
                    "captcha_challenge_jwt": captcha_challenge_jwt,
                    "cf_turnstile_response": cf_turnstile_response,
                    "city": city,
                    "company": company,
                    "country": country,
                    "first_name": first_name,
                    "h_captcha_response": h_captcha_response,
                    "last_name": last_name,
                    "preferred_locale": preferred_locale,
                    "secondary_billing_email": secondary_billing_email,
                    "state": state,
                    "tax_id_type": tax_id_type,
                    "telephone": telephone,
                    "vat": vat,
                    "zipcode": zipcode,
                },
                profile_update_params.ProfileUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                post_parser=ResultWrapper[ProfileUpdateResponse]._unwrapper,
            ),
            cast_to=cast(Type[ProfileUpdateResponse], ResultWrapper[ProfileUpdateResponse]),
        )

    def delete(
        self,
        *,
        account_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> None:
        """
        Deletes the billing profile for an account.

        Args:
          account_id: Identifier

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not account_id:
            raise ValueError(f"Expected a non-empty value for `account_id` but received {account_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._delete(
            path_template("/accounts/{account_id}/billing/profile", account_id=account_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    def get(
        self,
        *,
        account_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ProfileGetResponse:
        """
        Gets the current billing profile for the account.

        Args:
          account_id: Identifier

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not account_id:
            raise ValueError(f"Expected a non-empty value for `account_id` but received {account_id!r}")
        return self._get(
            path_template("/accounts/{account_id}/billing/profile", account_id=account_id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                post_parser=ResultWrapper[ProfileGetResponse]._unwrapper,
            ),
            cast_to=cast(Type[ProfileGetResponse], ResultWrapper[ProfileGetResponse]),
        )

    def update_billing_email(
        self,
        *,
        account_id: str,
        billing_email: str | Omit = omit,
        preferred_locale: str | Omit = omit,
        secondary_billing_email: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ProfileUpdateBillingEmailResponse:
        """
        Updates the billing email addresses and preferred locale for an account.

        Args:
          account_id: Identifier

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not account_id:
            raise ValueError(f"Expected a non-empty value for `account_id` but received {account_id!r}")
        return self._patch(
            path_template("/accounts/{account_id}/billing/profile", account_id=account_id),
            body=maybe_transform(
                {
                    "billing_email": billing_email,
                    "preferred_locale": preferred_locale,
                    "secondary_billing_email": secondary_billing_email,
                },
                profile_update_billing_email_params.ProfileUpdateBillingEmailParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                post_parser=ResultWrapper[ProfileUpdateBillingEmailResponse]._unwrapper,
            ),
            cast_to=cast(Type[ProfileUpdateBillingEmailResponse], ResultWrapper[ProfileUpdateBillingEmailResponse]),
        )


class AsyncProfilesResource(AsyncAPIResource):
    @cached_property
    def payment_method(self) -> AsyncPaymentMethodResource:
        return AsyncPaymentMethodResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncProfilesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cloudflare/cloudflare-python#accessing-raw-response-data-eg-headers
        """
        return AsyncProfilesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncProfilesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cloudflare/cloudflare-python#with_streaming_response
        """
        return AsyncProfilesResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        account_id: str,
        address: str | Omit = omit,
        address2: str | Omit = omit,
        billing_email: str | Omit = omit,
        buying_rate_plan: str | Omit = omit,
        captcha_challenge_jwt: str | Omit = omit,
        cf_turnstile_response: str | Omit = omit,
        city: str | Omit = omit,
        company: str | Omit = omit,
        country: str | Omit = omit,
        first_name: str | Omit = omit,
        h_captcha_response: str | Omit = omit,
        last_name: str | Omit = omit,
        preferred_locale: str | Omit = omit,
        secondary_billing_email: str | Omit = omit,
        state: str | Omit = omit,
        tax_id_type: str | Omit = omit,
        telephone: str | Omit = omit,
        vat: str | Omit = omit,
        zipcode: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ProfileCreateResponse:
        """
        Creates a billing profile for an account.

        Args:
          account_id: Identifier

          address: Street address line 1.

          address2: Street address line 2 (apt, suite, etc.).

          billing_email: Primary billing email address.

          buying_rate_plan: Rate plan being purchased right after profile setup.

          captcha_challenge_jwt: Captcha challenge JWT issued during onboarding.

          cf_turnstile_response: Cloudflare Turnstile response.

          city: City on the billing profile.

          company: Company name on the billing profile.

          country: ISO 3166-1 alpha-2 country code.

          first_name: First name on the billing profile.

          h_captcha_response: hCaptcha response.

          last_name: Last name on the billing profile.

          preferred_locale: Preferred locale for invoice rendering (BCP 47).

          secondary_billing_email: Secondary billing email address for CC on invoices.

          state: State or region on the billing profile.

          tax_id_type: Type of tax ID provided.

          telephone: Contact phone number.

          vat: VAT identifier.

          zipcode: ZIP or postal code.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not account_id:
            raise ValueError(f"Expected a non-empty value for `account_id` but received {account_id!r}")
        return await self._post(
            path_template("/accounts/{account_id}/billing/profile", account_id=account_id),
            body=await async_maybe_transform(
                {
                    "address": address,
                    "address2": address2,
                    "billing_email": billing_email,
                    "buying_rate_plan": buying_rate_plan,
                    "captcha_challenge_jwt": captcha_challenge_jwt,
                    "cf_turnstile_response": cf_turnstile_response,
                    "city": city,
                    "company": company,
                    "country": country,
                    "first_name": first_name,
                    "h_captcha_response": h_captcha_response,
                    "last_name": last_name,
                    "preferred_locale": preferred_locale,
                    "secondary_billing_email": secondary_billing_email,
                    "state": state,
                    "tax_id_type": tax_id_type,
                    "telephone": telephone,
                    "vat": vat,
                    "zipcode": zipcode,
                },
                profile_create_params.ProfileCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                post_parser=ResultWrapper[ProfileCreateResponse]._unwrapper,
            ),
            cast_to=cast(Type[ProfileCreateResponse], ResultWrapper[ProfileCreateResponse]),
        )

    async def update(
        self,
        *,
        account_id: str,
        address: str | Omit = omit,
        address2: str | Omit = omit,
        billing_email: str | Omit = omit,
        buying_rate_plan: str | Omit = omit,
        captcha_challenge_jwt: str | Omit = omit,
        cf_turnstile_response: str | Omit = omit,
        city: str | Omit = omit,
        company: str | Omit = omit,
        country: str | Omit = omit,
        first_name: str | Omit = omit,
        h_captcha_response: str | Omit = omit,
        last_name: str | Omit = omit,
        preferred_locale: str | Omit = omit,
        secondary_billing_email: str | Omit = omit,
        state: str | Omit = omit,
        tax_id_type: str | Omit = omit,
        telephone: str | Omit = omit,
        vat: str | Omit = omit,
        zipcode: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ProfileUpdateResponse:
        """
        Updates the billing profile for an account.

        Args:
          account_id: Identifier

          address: Street address line 1.

          address2: Street address line 2 (apt, suite, etc.).

          billing_email: Primary billing email address.

          buying_rate_plan: Rate plan being purchased right after profile setup.

          captcha_challenge_jwt: Captcha challenge JWT issued during onboarding.

          cf_turnstile_response: Cloudflare Turnstile response.

          city: City on the billing profile.

          company: Company name on the billing profile.

          country: ISO 3166-1 alpha-2 country code.

          first_name: First name on the billing profile.

          h_captcha_response: hCaptcha response.

          last_name: Last name on the billing profile.

          preferred_locale: Preferred locale for invoice rendering (BCP 47).

          secondary_billing_email: Secondary billing email address for CC on invoices.

          state: State or region on the billing profile.

          tax_id_type: Type of tax ID provided.

          telephone: Contact phone number.

          vat: VAT identifier.

          zipcode: ZIP or postal code.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not account_id:
            raise ValueError(f"Expected a non-empty value for `account_id` but received {account_id!r}")
        return await self._put(
            path_template("/accounts/{account_id}/billing/profile", account_id=account_id),
            body=await async_maybe_transform(
                {
                    "address": address,
                    "address2": address2,
                    "billing_email": billing_email,
                    "buying_rate_plan": buying_rate_plan,
                    "captcha_challenge_jwt": captcha_challenge_jwt,
                    "cf_turnstile_response": cf_turnstile_response,
                    "city": city,
                    "company": company,
                    "country": country,
                    "first_name": first_name,
                    "h_captcha_response": h_captcha_response,
                    "last_name": last_name,
                    "preferred_locale": preferred_locale,
                    "secondary_billing_email": secondary_billing_email,
                    "state": state,
                    "tax_id_type": tax_id_type,
                    "telephone": telephone,
                    "vat": vat,
                    "zipcode": zipcode,
                },
                profile_update_params.ProfileUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                post_parser=ResultWrapper[ProfileUpdateResponse]._unwrapper,
            ),
            cast_to=cast(Type[ProfileUpdateResponse], ResultWrapper[ProfileUpdateResponse]),
        )

    async def delete(
        self,
        *,
        account_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> None:
        """
        Deletes the billing profile for an account.

        Args:
          account_id: Identifier

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not account_id:
            raise ValueError(f"Expected a non-empty value for `account_id` but received {account_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._delete(
            path_template("/accounts/{account_id}/billing/profile", account_id=account_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    async def get(
        self,
        *,
        account_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ProfileGetResponse:
        """
        Gets the current billing profile for the account.

        Args:
          account_id: Identifier

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not account_id:
            raise ValueError(f"Expected a non-empty value for `account_id` but received {account_id!r}")
        return await self._get(
            path_template("/accounts/{account_id}/billing/profile", account_id=account_id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                post_parser=ResultWrapper[ProfileGetResponse]._unwrapper,
            ),
            cast_to=cast(Type[ProfileGetResponse], ResultWrapper[ProfileGetResponse]),
        )

    async def update_billing_email(
        self,
        *,
        account_id: str,
        billing_email: str | Omit = omit,
        preferred_locale: str | Omit = omit,
        secondary_billing_email: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ProfileUpdateBillingEmailResponse:
        """
        Updates the billing email addresses and preferred locale for an account.

        Args:
          account_id: Identifier

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not account_id:
            raise ValueError(f"Expected a non-empty value for `account_id` but received {account_id!r}")
        return await self._patch(
            path_template("/accounts/{account_id}/billing/profile", account_id=account_id),
            body=await async_maybe_transform(
                {
                    "billing_email": billing_email,
                    "preferred_locale": preferred_locale,
                    "secondary_billing_email": secondary_billing_email,
                },
                profile_update_billing_email_params.ProfileUpdateBillingEmailParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                post_parser=ResultWrapper[ProfileUpdateBillingEmailResponse]._unwrapper,
            ),
            cast_to=cast(Type[ProfileUpdateBillingEmailResponse], ResultWrapper[ProfileUpdateBillingEmailResponse]),
        )


class ProfilesResourceWithRawResponse:
    def __init__(self, profiles: ProfilesResource) -> None:
        self._profiles = profiles

        self.create = to_raw_response_wrapper(
            profiles.create,
        )
        self.update = to_raw_response_wrapper(
            profiles.update,
        )
        self.delete = to_raw_response_wrapper(
            profiles.delete,
        )
        self.get = to_raw_response_wrapper(
            profiles.get,
        )
        self.update_billing_email = to_raw_response_wrapper(
            profiles.update_billing_email,
        )

    @cached_property
    def payment_method(self) -> PaymentMethodResourceWithRawResponse:
        return PaymentMethodResourceWithRawResponse(self._profiles.payment_method)


class AsyncProfilesResourceWithRawResponse:
    def __init__(self, profiles: AsyncProfilesResource) -> None:
        self._profiles = profiles

        self.create = async_to_raw_response_wrapper(
            profiles.create,
        )
        self.update = async_to_raw_response_wrapper(
            profiles.update,
        )
        self.delete = async_to_raw_response_wrapper(
            profiles.delete,
        )
        self.get = async_to_raw_response_wrapper(
            profiles.get,
        )
        self.update_billing_email = async_to_raw_response_wrapper(
            profiles.update_billing_email,
        )

    @cached_property
    def payment_method(self) -> AsyncPaymentMethodResourceWithRawResponse:
        return AsyncPaymentMethodResourceWithRawResponse(self._profiles.payment_method)


class ProfilesResourceWithStreamingResponse:
    def __init__(self, profiles: ProfilesResource) -> None:
        self._profiles = profiles

        self.create = to_streamed_response_wrapper(
            profiles.create,
        )
        self.update = to_streamed_response_wrapper(
            profiles.update,
        )
        self.delete = to_streamed_response_wrapper(
            profiles.delete,
        )
        self.get = to_streamed_response_wrapper(
            profiles.get,
        )
        self.update_billing_email = to_streamed_response_wrapper(
            profiles.update_billing_email,
        )

    @cached_property
    def payment_method(self) -> PaymentMethodResourceWithStreamingResponse:
        return PaymentMethodResourceWithStreamingResponse(self._profiles.payment_method)


class AsyncProfilesResourceWithStreamingResponse:
    def __init__(self, profiles: AsyncProfilesResource) -> None:
        self._profiles = profiles

        self.create = async_to_streamed_response_wrapper(
            profiles.create,
        )
        self.update = async_to_streamed_response_wrapper(
            profiles.update,
        )
        self.delete = async_to_streamed_response_wrapper(
            profiles.delete,
        )
        self.get = async_to_streamed_response_wrapper(
            profiles.get,
        )
        self.update_billing_email = async_to_streamed_response_wrapper(
            profiles.update_billing_email,
        )

    @cached_property
    def payment_method(self) -> AsyncPaymentMethodResourceWithStreamingResponse:
        return AsyncPaymentMethodResourceWithStreamingResponse(self._profiles.payment_method)
