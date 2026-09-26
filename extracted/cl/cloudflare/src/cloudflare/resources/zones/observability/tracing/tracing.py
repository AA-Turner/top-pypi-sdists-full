# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from .rules import (
    RulesResource,
    AsyncRulesResource,
    RulesResourceWithRawResponse,
    AsyncRulesResourceWithRawResponse,
    RulesResourceWithStreamingResponse,
    AsyncRulesResourceWithStreamingResponse,
)
from .settings import (
    SettingsResource,
    AsyncSettingsResource,
    SettingsResourceWithRawResponse,
    AsyncSettingsResourceWithRawResponse,
    SettingsResourceWithStreamingResponse,
    AsyncSettingsResourceWithStreamingResponse,
)
from ....._compat import cached_property
from ....._resource import SyncAPIResource, AsyncAPIResource

__all__ = ["TracingResource", "AsyncTracingResource"]


class TracingResource(SyncAPIResource):
    @cached_property
    def settings(self) -> SettingsResource:
        return SettingsResource(self._client)

    @cached_property
    def rules(self) -> RulesResource:
        return RulesResource(self._client)

    @cached_property
    def with_raw_response(self) -> TracingResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cloudflare/cloudflare-python#accessing-raw-response-data-eg-headers
        """
        return TracingResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> TracingResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cloudflare/cloudflare-python#with_streaming_response
        """
        return TracingResourceWithStreamingResponse(self)


class AsyncTracingResource(AsyncAPIResource):
    @cached_property
    def settings(self) -> AsyncSettingsResource:
        return AsyncSettingsResource(self._client)

    @cached_property
    def rules(self) -> AsyncRulesResource:
        return AsyncRulesResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncTracingResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cloudflare/cloudflare-python#accessing-raw-response-data-eg-headers
        """
        return AsyncTracingResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncTracingResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cloudflare/cloudflare-python#with_streaming_response
        """
        return AsyncTracingResourceWithStreamingResponse(self)


class TracingResourceWithRawResponse:
    def __init__(self, tracing: TracingResource) -> None:
        self._tracing = tracing

    @cached_property
    def settings(self) -> SettingsResourceWithRawResponse:
        return SettingsResourceWithRawResponse(self._tracing.settings)

    @cached_property
    def rules(self) -> RulesResourceWithRawResponse:
        return RulesResourceWithRawResponse(self._tracing.rules)


class AsyncTracingResourceWithRawResponse:
    def __init__(self, tracing: AsyncTracingResource) -> None:
        self._tracing = tracing

    @cached_property
    def settings(self) -> AsyncSettingsResourceWithRawResponse:
        return AsyncSettingsResourceWithRawResponse(self._tracing.settings)

    @cached_property
    def rules(self) -> AsyncRulesResourceWithRawResponse:
        return AsyncRulesResourceWithRawResponse(self._tracing.rules)


class TracingResourceWithStreamingResponse:
    def __init__(self, tracing: TracingResource) -> None:
        self._tracing = tracing

    @cached_property
    def settings(self) -> SettingsResourceWithStreamingResponse:
        return SettingsResourceWithStreamingResponse(self._tracing.settings)

    @cached_property
    def rules(self) -> RulesResourceWithStreamingResponse:
        return RulesResourceWithStreamingResponse(self._tracing.rules)


class AsyncTracingResourceWithStreamingResponse:
    def __init__(self, tracing: AsyncTracingResource) -> None:
        self._tracing = tracing

    @cached_property
    def settings(self) -> AsyncSettingsResourceWithStreamingResponse:
        return AsyncSettingsResourceWithStreamingResponse(self._tracing.settings)

    @cached_property
    def rules(self) -> AsyncRulesResourceWithStreamingResponse:
        return AsyncRulesResourceWithStreamingResponse(self._tracing.rules)
