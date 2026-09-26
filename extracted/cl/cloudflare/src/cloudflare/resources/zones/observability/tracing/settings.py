# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Type, cast
from typing_extensions import Literal

import httpx

from ....._types import Body, Omit, Query, Headers, NotGiven, SequenceNotStr, omit, not_given
from ....._utils import path_template, maybe_transform, async_maybe_transform
from ....._compat import cached_property
from ....._resource import SyncAPIResource, AsyncAPIResource
from ....._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ....._wrappers import ResultWrapper
from ....._base_client import make_request_options
from .....types.zones.observability.tracing import setting_update_params
from .....types.zones.observability.tracing.setting_get_response import SettingGetResponse
from .....types.zones.observability.tracing.setting_delete_response import SettingDeleteResponse
from .....types.zones.observability.tracing.setting_update_response import SettingUpdateResponse

__all__ = ["SettingsResource", "AsyncSettingsResource"]


class SettingsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> SettingsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cloudflare/cloudflare-python#accessing-raw-response-data-eg-headers
        """
        return SettingsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> SettingsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cloudflare/cloudflare-python#with_streaming_response
        """
        return SettingsResourceWithStreamingResponse(self)

    def update(
        self,
        *,
        zone_id: str,
        destinations: SequenceNotStr[str] | Omit = omit,
        enabled: bool | Omit = omit,
        forward_context: bool | Omit = omit,
        persist: bool | Omit = omit,
        propagation_policy: Literal["accept", "authenticated", "reject"] | Omit = omit,
        sampling_ratio: float | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SettingUpdateResponse:
        """
        Update the zone-level Cloudflare Traces settings.

        Args:
          zone_id: Specify the zone ID.

          destinations: Up to 100 OpenTelemetry destination identifiers that receive traces.

          enabled: Whether Cloudflare Traces is enabled for the zone.

          forward_context: Whether trace context is sent externally or across a zone boundary.

          persist: Whether traces are persisted in Cloudflare.

          propagation_policy: When inbound trace context may be continued. Authenticated propagation is not
              supported yet.

          sampling_ratio: The ratio of requests sampled for tracing, from 0 to 1.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not zone_id:
            raise ValueError(f"Expected a non-empty value for `zone_id` but received {zone_id!r}")
        return self._patch(
            path_template("/zones/{zone_id}/observability/tracing/settings", zone_id=zone_id),
            body=maybe_transform(
                {
                    "destinations": destinations,
                    "enabled": enabled,
                    "forward_context": forward_context,
                    "persist": persist,
                    "propagation_policy": propagation_policy,
                    "sampling_ratio": sampling_ratio,
                },
                setting_update_params.SettingUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                post_parser=ResultWrapper[SettingUpdateResponse]._unwrapper,
            ),
            cast_to=cast(Type[SettingUpdateResponse], ResultWrapper[SettingUpdateResponse]),
        )

    def delete(
        self,
        *,
        zone_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SettingDeleteResponse:
        """
        Reset the zone-level Cloudflare Traces settings to their defaults while
        preserving the sampling rules.

        Args:
          zone_id: Specify the zone ID.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not zone_id:
            raise ValueError(f"Expected a non-empty value for `zone_id` but received {zone_id!r}")
        return self._delete(
            path_template("/zones/{zone_id}/observability/tracing/settings", zone_id=zone_id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                post_parser=ResultWrapper[SettingDeleteResponse]._unwrapper,
            ),
            cast_to=cast(Type[SettingDeleteResponse], ResultWrapper[SettingDeleteResponse]),
        )

    def get(
        self,
        *,
        zone_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SettingGetResponse:
        """
        Retrieve the zone-level Cloudflare Traces settings.

        Args:
          zone_id: Specify the zone ID.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not zone_id:
            raise ValueError(f"Expected a non-empty value for `zone_id` but received {zone_id!r}")
        return self._get(
            path_template("/zones/{zone_id}/observability/tracing/settings", zone_id=zone_id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                post_parser=ResultWrapper[SettingGetResponse]._unwrapper,
            ),
            cast_to=cast(Type[SettingGetResponse], ResultWrapper[SettingGetResponse]),
        )


class AsyncSettingsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncSettingsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cloudflare/cloudflare-python#accessing-raw-response-data-eg-headers
        """
        return AsyncSettingsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncSettingsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cloudflare/cloudflare-python#with_streaming_response
        """
        return AsyncSettingsResourceWithStreamingResponse(self)

    async def update(
        self,
        *,
        zone_id: str,
        destinations: SequenceNotStr[str] | Omit = omit,
        enabled: bool | Omit = omit,
        forward_context: bool | Omit = omit,
        persist: bool | Omit = omit,
        propagation_policy: Literal["accept", "authenticated", "reject"] | Omit = omit,
        sampling_ratio: float | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SettingUpdateResponse:
        """
        Update the zone-level Cloudflare Traces settings.

        Args:
          zone_id: Specify the zone ID.

          destinations: Up to 100 OpenTelemetry destination identifiers that receive traces.

          enabled: Whether Cloudflare Traces is enabled for the zone.

          forward_context: Whether trace context is sent externally or across a zone boundary.

          persist: Whether traces are persisted in Cloudflare.

          propagation_policy: When inbound trace context may be continued. Authenticated propagation is not
              supported yet.

          sampling_ratio: The ratio of requests sampled for tracing, from 0 to 1.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not zone_id:
            raise ValueError(f"Expected a non-empty value for `zone_id` but received {zone_id!r}")
        return await self._patch(
            path_template("/zones/{zone_id}/observability/tracing/settings", zone_id=zone_id),
            body=await async_maybe_transform(
                {
                    "destinations": destinations,
                    "enabled": enabled,
                    "forward_context": forward_context,
                    "persist": persist,
                    "propagation_policy": propagation_policy,
                    "sampling_ratio": sampling_ratio,
                },
                setting_update_params.SettingUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                post_parser=ResultWrapper[SettingUpdateResponse]._unwrapper,
            ),
            cast_to=cast(Type[SettingUpdateResponse], ResultWrapper[SettingUpdateResponse]),
        )

    async def delete(
        self,
        *,
        zone_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SettingDeleteResponse:
        """
        Reset the zone-level Cloudflare Traces settings to their defaults while
        preserving the sampling rules.

        Args:
          zone_id: Specify the zone ID.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not zone_id:
            raise ValueError(f"Expected a non-empty value for `zone_id` but received {zone_id!r}")
        return await self._delete(
            path_template("/zones/{zone_id}/observability/tracing/settings", zone_id=zone_id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                post_parser=ResultWrapper[SettingDeleteResponse]._unwrapper,
            ),
            cast_to=cast(Type[SettingDeleteResponse], ResultWrapper[SettingDeleteResponse]),
        )

    async def get(
        self,
        *,
        zone_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SettingGetResponse:
        """
        Retrieve the zone-level Cloudflare Traces settings.

        Args:
          zone_id: Specify the zone ID.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not zone_id:
            raise ValueError(f"Expected a non-empty value for `zone_id` but received {zone_id!r}")
        return await self._get(
            path_template("/zones/{zone_id}/observability/tracing/settings", zone_id=zone_id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                post_parser=ResultWrapper[SettingGetResponse]._unwrapper,
            ),
            cast_to=cast(Type[SettingGetResponse], ResultWrapper[SettingGetResponse]),
        )


class SettingsResourceWithRawResponse:
    def __init__(self, settings: SettingsResource) -> None:
        self._settings = settings

        self.update = to_raw_response_wrapper(
            settings.update,
        )
        self.delete = to_raw_response_wrapper(
            settings.delete,
        )
        self.get = to_raw_response_wrapper(
            settings.get,
        )


class AsyncSettingsResourceWithRawResponse:
    def __init__(self, settings: AsyncSettingsResource) -> None:
        self._settings = settings

        self.update = async_to_raw_response_wrapper(
            settings.update,
        )
        self.delete = async_to_raw_response_wrapper(
            settings.delete,
        )
        self.get = async_to_raw_response_wrapper(
            settings.get,
        )


class SettingsResourceWithStreamingResponse:
    def __init__(self, settings: SettingsResource) -> None:
        self._settings = settings

        self.update = to_streamed_response_wrapper(
            settings.update,
        )
        self.delete = to_streamed_response_wrapper(
            settings.delete,
        )
        self.get = to_streamed_response_wrapper(
            settings.get,
        )


class AsyncSettingsResourceWithStreamingResponse:
    def __init__(self, settings: AsyncSettingsResource) -> None:
        self._settings = settings

        self.update = async_to_streamed_response_wrapper(
            settings.update,
        )
        self.delete = async_to_streamed_response_wrapper(
            settings.delete,
        )
        self.get = async_to_streamed_response_wrapper(
            settings.get,
        )
