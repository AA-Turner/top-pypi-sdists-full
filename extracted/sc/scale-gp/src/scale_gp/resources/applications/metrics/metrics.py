# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from .scalar import (
    ScalarResource,
    AsyncScalarResource,
    ScalarResourceWithRawResponse,
    AsyncScalarResourceWithRawResponse,
    ScalarResourceWithStreamingResponse,
    AsyncScalarResourceWithStreamingResponse,
)
from ...._compat import cached_property
from .timeseries import (
    TimeseriesResource,
    AsyncTimeseriesResource,
    TimeseriesResourceWithRawResponse,
    AsyncTimeseriesResourceWithRawResponse,
    TimeseriesResourceWithStreamingResponse,
    AsyncTimeseriesResourceWithStreamingResponse,
)
from ...._resource import SyncAPIResource, AsyncAPIResource

__all__ = ["MetricsResource", "AsyncMetricsResource"]


class MetricsResource(SyncAPIResource):
    @cached_property
    def scalar(self) -> ScalarResource:
        return ScalarResource(self._client)

    @cached_property
    def timeseries(self) -> TimeseriesResource:
        return TimeseriesResource(self._client)

    @cached_property
    def with_raw_response(self) -> MetricsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python#accessing-raw-response-data-eg-headers
        """
        return MetricsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> MetricsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python#with_streaming_response
        """
        return MetricsResourceWithStreamingResponse(self)


class AsyncMetricsResource(AsyncAPIResource):
    @cached_property
    def scalar(self) -> AsyncScalarResource:
        return AsyncScalarResource(self._client)

    @cached_property
    def timeseries(self) -> AsyncTimeseriesResource:
        return AsyncTimeseriesResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncMetricsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python#accessing-raw-response-data-eg-headers
        """
        return AsyncMetricsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncMetricsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python#with_streaming_response
        """
        return AsyncMetricsResourceWithStreamingResponse(self)


class MetricsResourceWithRawResponse:
    def __init__(self, metrics: MetricsResource) -> None:
        self._metrics = metrics

    @cached_property
    def scalar(self) -> ScalarResourceWithRawResponse:
        return ScalarResourceWithRawResponse(self._metrics.scalar)

    @cached_property
    def timeseries(self) -> TimeseriesResourceWithRawResponse:
        return TimeseriesResourceWithRawResponse(self._metrics.timeseries)


class AsyncMetricsResourceWithRawResponse:
    def __init__(self, metrics: AsyncMetricsResource) -> None:
        self._metrics = metrics

    @cached_property
    def scalar(self) -> AsyncScalarResourceWithRawResponse:
        return AsyncScalarResourceWithRawResponse(self._metrics.scalar)

    @cached_property
    def timeseries(self) -> AsyncTimeseriesResourceWithRawResponse:
        return AsyncTimeseriesResourceWithRawResponse(self._metrics.timeseries)


class MetricsResourceWithStreamingResponse:
    def __init__(self, metrics: MetricsResource) -> None:
        self._metrics = metrics

    @cached_property
    def scalar(self) -> ScalarResourceWithStreamingResponse:
        return ScalarResourceWithStreamingResponse(self._metrics.scalar)

    @cached_property
    def timeseries(self) -> TimeseriesResourceWithStreamingResponse:
        return TimeseriesResourceWithStreamingResponse(self._metrics.timeseries)


class AsyncMetricsResourceWithStreamingResponse:
    def __init__(self, metrics: AsyncMetricsResource) -> None:
        self._metrics = metrics

    @cached_property
    def scalar(self) -> AsyncScalarResourceWithStreamingResponse:
        return AsyncScalarResourceWithStreamingResponse(self._metrics.scalar)

    @cached_property
    def timeseries(self) -> AsyncTimeseriesResourceWithStreamingResponse:
        return AsyncTimeseriesResourceWithStreamingResponse(self._metrics.timeseries)
