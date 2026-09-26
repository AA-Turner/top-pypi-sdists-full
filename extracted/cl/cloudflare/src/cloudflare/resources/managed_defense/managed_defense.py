# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from .vulnerability_discovery.vulnerability_discovery import (
    VulnerabilityDiscoveryResource,
    AsyncVulnerabilityDiscoveryResource,
    VulnerabilityDiscoveryResourceWithRawResponse,
    AsyncVulnerabilityDiscoveryResourceWithRawResponse,
    VulnerabilityDiscoveryResourceWithStreamingResponse,
    AsyncVulnerabilityDiscoveryResourceWithStreamingResponse,
)

__all__ = ["ManagedDefenseResource", "AsyncManagedDefenseResource"]


class ManagedDefenseResource(SyncAPIResource):
    @cached_property
    def vulnerability_discovery(self) -> VulnerabilityDiscoveryResource:
        return VulnerabilityDiscoveryResource(self._client)

    @cached_property
    def with_raw_response(self) -> ManagedDefenseResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cloudflare/cloudflare-python#accessing-raw-response-data-eg-headers
        """
        return ManagedDefenseResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ManagedDefenseResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cloudflare/cloudflare-python#with_streaming_response
        """
        return ManagedDefenseResourceWithStreamingResponse(self)


class AsyncManagedDefenseResource(AsyncAPIResource):
    @cached_property
    def vulnerability_discovery(self) -> AsyncVulnerabilityDiscoveryResource:
        return AsyncVulnerabilityDiscoveryResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncManagedDefenseResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cloudflare/cloudflare-python#accessing-raw-response-data-eg-headers
        """
        return AsyncManagedDefenseResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncManagedDefenseResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cloudflare/cloudflare-python#with_streaming_response
        """
        return AsyncManagedDefenseResourceWithStreamingResponse(self)


class ManagedDefenseResourceWithRawResponse:
    def __init__(self, managed_defense: ManagedDefenseResource) -> None:
        self._managed_defense = managed_defense

    @cached_property
    def vulnerability_discovery(self) -> VulnerabilityDiscoveryResourceWithRawResponse:
        return VulnerabilityDiscoveryResourceWithRawResponse(self._managed_defense.vulnerability_discovery)


class AsyncManagedDefenseResourceWithRawResponse:
    def __init__(self, managed_defense: AsyncManagedDefenseResource) -> None:
        self._managed_defense = managed_defense

    @cached_property
    def vulnerability_discovery(self) -> AsyncVulnerabilityDiscoveryResourceWithRawResponse:
        return AsyncVulnerabilityDiscoveryResourceWithRawResponse(self._managed_defense.vulnerability_discovery)


class ManagedDefenseResourceWithStreamingResponse:
    def __init__(self, managed_defense: ManagedDefenseResource) -> None:
        self._managed_defense = managed_defense

    @cached_property
    def vulnerability_discovery(self) -> VulnerabilityDiscoveryResourceWithStreamingResponse:
        return VulnerabilityDiscoveryResourceWithStreamingResponse(self._managed_defense.vulnerability_discovery)


class AsyncManagedDefenseResourceWithStreamingResponse:
    def __init__(self, managed_defense: AsyncManagedDefenseResource) -> None:
        self._managed_defense = managed_defense

    @cached_property
    def vulnerability_discovery(self) -> AsyncVulnerabilityDiscoveryResourceWithStreamingResponse:
        return AsyncVulnerabilityDiscoveryResourceWithStreamingResponse(self._managed_defense.vulnerability_discovery)
