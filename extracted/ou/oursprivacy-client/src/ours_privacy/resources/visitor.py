# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional

import httpx

from ..types import visitor_upsert_params
from .._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
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
from ..types.visitor_upsert_response import VisitorUpsertResponse

__all__ = ["VisitorResource", "AsyncVisitorResource"]


class VisitorResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> VisitorResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/with-ours/ingest-sdk-python#accessing-raw-response-data-eg-headers
        """
        return VisitorResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> VisitorResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/with-ours/ingest-sdk-python#with_streaming_response
        """
        return VisitorResourceWithStreamingResponse(self)

    def upsert(
        self,
        *,
        token: str,
        user_properties: visitor_upsert_params.UserProperties,
        default_properties: Optional[visitor_upsert_params.DefaultProperties] | Omit = omit,
        email: Optional[str] | Omit = omit,
        external_id: Optional[str] | Omit = omit,
        identity_context: Optional[visitor_upsert_params.IdentityContext] | Omit = omit,
        user_id: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> VisitorUpsertResponse:
        """
        Set or update properties on an existing visitor, or create a new visitor if no
        match is found. This fires a $identify event, making the call visible in the
        event stream. Identity resolution runs in priority order: userId (direct, no
        lookup) → externalId → email → userProperties.phone_number. Each lookup runs
        only if earlier identifiers did not resolve a visitor. Phone matching ignores
        common formatting and an international + or 00 prefix, but does not infer a
        country code. When a visitor is found, their Ours Visitor ID is used going
        forward so all future events are attached to the same profile. For top-level
        visitor properties: null clears the existing value, while undefined, omitted
        fields, and empty strings are ignored. For entries inside custom_properties:
        null, undefined, and empty strings are all ignored (custom_properties use merge
        semantics). See https://docs.oursprivacy.com/docs/data-types for details and
        common pitfalls.

        Args:
          token: The token for your Source. You can find this in the dashboard.

          user_properties: User properties to associate with this user. The existing user properties will
              be updated. And all future events will have these properties associated with
              them.

          default_properties: These properties are used throughout the Ours app to pass known values onto
              destinations

          email: The email address of a user. When userId is absent and externalId does not
              resolve a visitor, we search your account for a visitor with this email. If no
              match is found, we try userProperties.phone_number before creating a new
              visitor.

          external_id: Your system's unique identifier for this user. When userId is absent, we search
              your account for an existing visitor with this externalId. If no match is found,
              we try email and then userProperties.phone_number before creating a new visitor.
              If you also have the userId from cookies or local storage, send both — it
              removes the lookup round-trip.

          identity_context: End-user network context for server-side calls. Required for probabilistic
              identity resolution when the caller is a backend server rather than an end-user
              browser.

          user_id: The Ours Visitor ID stored in local storage and cookies on your web properties.
              When present, this is used directly — no lookup by externalId, email, or phone
              is performed. If you have both a userId and an externalId, send both so the
              event is attached to the right visitor without any lookup overhead.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/identify" if self._client._base_url_overridden else "https://api.oursprivacy.com/api/v1/identify",
            body=maybe_transform(
                {
                    "token": token,
                    "user_properties": user_properties,
                    "default_properties": default_properties,
                    "email": email,
                    "external_id": external_id,
                    "identity_context": identity_context,
                    "user_id": user_id,
                },
                visitor_upsert_params.VisitorUpsertParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=VisitorUpsertResponse,
        )


class AsyncVisitorResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncVisitorResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/with-ours/ingest-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncVisitorResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncVisitorResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/with-ours/ingest-sdk-python#with_streaming_response
        """
        return AsyncVisitorResourceWithStreamingResponse(self)

    async def upsert(
        self,
        *,
        token: str,
        user_properties: visitor_upsert_params.UserProperties,
        default_properties: Optional[visitor_upsert_params.DefaultProperties] | Omit = omit,
        email: Optional[str] | Omit = omit,
        external_id: Optional[str] | Omit = omit,
        identity_context: Optional[visitor_upsert_params.IdentityContext] | Omit = omit,
        user_id: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> VisitorUpsertResponse:
        """
        Set or update properties on an existing visitor, or create a new visitor if no
        match is found. This fires a $identify event, making the call visible in the
        event stream. Identity resolution runs in priority order: userId (direct, no
        lookup) → externalId → email → userProperties.phone_number. Each lookup runs
        only if earlier identifiers did not resolve a visitor. Phone matching ignores
        common formatting and an international + or 00 prefix, but does not infer a
        country code. When a visitor is found, their Ours Visitor ID is used going
        forward so all future events are attached to the same profile. For top-level
        visitor properties: null clears the existing value, while undefined, omitted
        fields, and empty strings are ignored. For entries inside custom_properties:
        null, undefined, and empty strings are all ignored (custom_properties use merge
        semantics). See https://docs.oursprivacy.com/docs/data-types for details and
        common pitfalls.

        Args:
          token: The token for your Source. You can find this in the dashboard.

          user_properties: User properties to associate with this user. The existing user properties will
              be updated. And all future events will have these properties associated with
              them.

          default_properties: These properties are used throughout the Ours app to pass known values onto
              destinations

          email: The email address of a user. When userId is absent and externalId does not
              resolve a visitor, we search your account for a visitor with this email. If no
              match is found, we try userProperties.phone_number before creating a new
              visitor.

          external_id: Your system's unique identifier for this user. When userId is absent, we search
              your account for an existing visitor with this externalId. If no match is found,
              we try email and then userProperties.phone_number before creating a new visitor.
              If you also have the userId from cookies or local storage, send both — it
              removes the lookup round-trip.

          identity_context: End-user network context for server-side calls. Required for probabilistic
              identity resolution when the caller is a backend server rather than an end-user
              browser.

          user_id: The Ours Visitor ID stored in local storage and cookies on your web properties.
              When present, this is used directly — no lookup by externalId, email, or phone
              is performed. If you have both a userId and an externalId, send both so the
              event is attached to the right visitor without any lookup overhead.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/identify" if self._client._base_url_overridden else "https://api.oursprivacy.com/api/v1/identify",
            body=await async_maybe_transform(
                {
                    "token": token,
                    "user_properties": user_properties,
                    "default_properties": default_properties,
                    "email": email,
                    "external_id": external_id,
                    "identity_context": identity_context,
                    "user_id": user_id,
                },
                visitor_upsert_params.VisitorUpsertParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=VisitorUpsertResponse,
        )


class VisitorResourceWithRawResponse:
    def __init__(self, visitor: VisitorResource) -> None:
        self._visitor = visitor

        self.upsert = to_raw_response_wrapper(
            visitor.upsert,
        )


class AsyncVisitorResourceWithRawResponse:
    def __init__(self, visitor: AsyncVisitorResource) -> None:
        self._visitor = visitor

        self.upsert = async_to_raw_response_wrapper(
            visitor.upsert,
        )


class VisitorResourceWithStreamingResponse:
    def __init__(self, visitor: VisitorResource) -> None:
        self._visitor = visitor

        self.upsert = to_streamed_response_wrapper(
            visitor.upsert,
        )


class AsyncVisitorResourceWithStreamingResponse:
    def __init__(self, visitor: AsyncVisitorResource) -> None:
        self._visitor = visitor

        self.upsert = async_to_streamed_response_wrapper(
            visitor.upsert,
        )
