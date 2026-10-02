# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Optional

import httpx

from ..types import track_event_params
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
from ..types.track_event_response import TrackEventResponse

__all__ = ["TrackResource", "AsyncTrackResource"]


class TrackResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> TrackResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/with-ours/ingest-sdk-python#accessing-raw-response-data-eg-headers
        """
        return TrackResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> TrackResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/with-ours/ingest-sdk-python#with_streaming_response
        """
        return TrackResourceWithStreamingResponse(self)

    def event(
        self,
        *,
        token: str,
        event: str,
        default_properties: Optional[track_event_params.DefaultProperties] | Omit = omit,
        distinct_id: Optional[str] | Omit = omit,
        email: Optional[str] | Omit = omit,
        event_properties: Optional[Dict[str, Optional[str]]] | Omit = omit,
        external_id: Optional[str] | Omit = omit,
        identity_context: Optional[track_event_params.IdentityContext] | Omit = omit,
        time: Optional[float] | Omit = omit,
        user_id: Optional[str] | Omit = omit,
        user_properties: Optional[track_event_params.UserProperties] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> TrackEventResponse:
        """Track events from your server.

        Include userId, externalId, email, or
        userProperties.phone_number to associate the event with an existing visitor.
        Identity resolution runs in priority order: userId (direct, no lookup) →
        externalId → email → userProperties.phone_number. Each lookup runs only if
        earlier identifiers did not resolve a visitor. Phone matching ignores common
        formatting and an international + or 00 prefix, but does not infer a country
        code. If you know both userId and externalId, send both. For top-level visitor
        properties: null clears the existing value, while undefined, omitted fields, and
        empty strings are ignored. For entries inside custom_properties: null,
        undefined, and empty strings are all ignored (custom_properties use merge
        semantics). See https://docs.oursprivacy.com/docs/data-types for details and
        common pitfalls.

        Args:
          token: The token for your Source. You can find this in the dashboard.

          event: The name of the event you're tracking. This must be whitelisted in the Ours
              dashboard.

          default_properties: These properties are used throughout the Ours app to pass known values onto
              destinations

          distinct_id: A unique identifier for this event used for deduplication. Highly recommended —
              if omitted, Ours will generate one for you, but supplying your own gives you
              stronger idempotency guarantees (e.g. a Stripe payment intent ID or your
              internal order ID).

          email: The email address of a user. When userId is absent and externalId does not
              resolve a visitor, we search your account for a visitor with this email. If no
              match is found, we try userProperties.phone_number before creating a new
              visitor.

          event_properties: Any additional event properties you want to pass along.

          external_id: Your system's unique identifier for this user. When userId is absent, we search
              your account for an existing visitor with this externalId. If no match is found,
              we try email and then userProperties.phone_number before creating a new visitor.
              If you also have the userId from cookies or local storage, send both — it
              removes the lookup round-trip.

          identity_context: End-user network context for server-side calls. Required for probabilistic
              identity resolution when the caller is a backend server rather than an end-user
              browser.

          time: The time at which the event occurred in milliseconds since UTC epoch. The time
              must be in the past and within the last 7 days.

          user_id: The Ours Visitor ID stored in local storage and cookies on your web properties.
              When present, this is used directly — no lookup by externalId, email, or phone
              is performed. If you have both a userId and an externalId, send both so the
              event is attached to the right visitor without any lookup overhead.

          user_properties: Properties to set on the visitor. (optional) You can also update these
              properties via the identify endpoint.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/track" if self._client._base_url_overridden else "https://api.oursprivacy.com/api/v1/track",
            body=maybe_transform(
                {
                    "token": token,
                    "event": event,
                    "default_properties": default_properties,
                    "distinct_id": distinct_id,
                    "email": email,
                    "event_properties": event_properties,
                    "external_id": external_id,
                    "identity_context": identity_context,
                    "time": time,
                    "user_id": user_id,
                    "user_properties": user_properties,
                },
                track_event_params.TrackEventParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TrackEventResponse,
        )


class AsyncTrackResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncTrackResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/with-ours/ingest-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncTrackResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncTrackResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/with-ours/ingest-sdk-python#with_streaming_response
        """
        return AsyncTrackResourceWithStreamingResponse(self)

    async def event(
        self,
        *,
        token: str,
        event: str,
        default_properties: Optional[track_event_params.DefaultProperties] | Omit = omit,
        distinct_id: Optional[str] | Omit = omit,
        email: Optional[str] | Omit = omit,
        event_properties: Optional[Dict[str, Optional[str]]] | Omit = omit,
        external_id: Optional[str] | Omit = omit,
        identity_context: Optional[track_event_params.IdentityContext] | Omit = omit,
        time: Optional[float] | Omit = omit,
        user_id: Optional[str] | Omit = omit,
        user_properties: Optional[track_event_params.UserProperties] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> TrackEventResponse:
        """Track events from your server.

        Include userId, externalId, email, or
        userProperties.phone_number to associate the event with an existing visitor.
        Identity resolution runs in priority order: userId (direct, no lookup) →
        externalId → email → userProperties.phone_number. Each lookup runs only if
        earlier identifiers did not resolve a visitor. Phone matching ignores common
        formatting and an international + or 00 prefix, but does not infer a country
        code. If you know both userId and externalId, send both. For top-level visitor
        properties: null clears the existing value, while undefined, omitted fields, and
        empty strings are ignored. For entries inside custom_properties: null,
        undefined, and empty strings are all ignored (custom_properties use merge
        semantics). See https://docs.oursprivacy.com/docs/data-types for details and
        common pitfalls.

        Args:
          token: The token for your Source. You can find this in the dashboard.

          event: The name of the event you're tracking. This must be whitelisted in the Ours
              dashboard.

          default_properties: These properties are used throughout the Ours app to pass known values onto
              destinations

          distinct_id: A unique identifier for this event used for deduplication. Highly recommended —
              if omitted, Ours will generate one for you, but supplying your own gives you
              stronger idempotency guarantees (e.g. a Stripe payment intent ID or your
              internal order ID).

          email: The email address of a user. When userId is absent and externalId does not
              resolve a visitor, we search your account for a visitor with this email. If no
              match is found, we try userProperties.phone_number before creating a new
              visitor.

          event_properties: Any additional event properties you want to pass along.

          external_id: Your system's unique identifier for this user. When userId is absent, we search
              your account for an existing visitor with this externalId. If no match is found,
              we try email and then userProperties.phone_number before creating a new visitor.
              If you also have the userId from cookies or local storage, send both — it
              removes the lookup round-trip.

          identity_context: End-user network context for server-side calls. Required for probabilistic
              identity resolution when the caller is a backend server rather than an end-user
              browser.

          time: The time at which the event occurred in milliseconds since UTC epoch. The time
              must be in the past and within the last 7 days.

          user_id: The Ours Visitor ID stored in local storage and cookies on your web properties.
              When present, this is used directly — no lookup by externalId, email, or phone
              is performed. If you have both a userId and an externalId, send both so the
              event is attached to the right visitor without any lookup overhead.

          user_properties: Properties to set on the visitor. (optional) You can also update these
              properties via the identify endpoint.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/track" if self._client._base_url_overridden else "https://api.oursprivacy.com/api/v1/track",
            body=await async_maybe_transform(
                {
                    "token": token,
                    "event": event,
                    "default_properties": default_properties,
                    "distinct_id": distinct_id,
                    "email": email,
                    "event_properties": event_properties,
                    "external_id": external_id,
                    "identity_context": identity_context,
                    "time": time,
                    "user_id": user_id,
                    "user_properties": user_properties,
                },
                track_event_params.TrackEventParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TrackEventResponse,
        )


class TrackResourceWithRawResponse:
    def __init__(self, track: TrackResource) -> None:
        self._track = track

        self.event = to_raw_response_wrapper(
            track.event,
        )


class AsyncTrackResourceWithRawResponse:
    def __init__(self, track: AsyncTrackResource) -> None:
        self._track = track

        self.event = async_to_raw_response_wrapper(
            track.event,
        )


class TrackResourceWithStreamingResponse:
    def __init__(self, track: TrackResource) -> None:
        self._track = track

        self.event = to_streamed_response_wrapper(
            track.event,
        )


class AsyncTrackResourceWithStreamingResponse:
    def __init__(self, track: AsyncTrackResource) -> None:
        self._track = track

        self.event = async_to_streamed_response_wrapper(
            track.event,
        )
