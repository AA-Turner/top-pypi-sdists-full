"""Shared test fixtures for the OTLP-first observability SDK."""

from collections.abc import Callable, Iterable, Mapping, Sequence

import pytest
from opentelemetry.sdk._logs.export import InMemoryLogRecordExporter
from opentelemetry.sdk.metrics._internal.point import Histogram, HistogramDataPoint, Metric, MetricsData
from opentelemetry.sdk.metrics.export import InMemoryMetricReader
from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter
from opentelemetry.util.types import AttributeValue

from mistralai.observability.otel import (
    ChatCompletionAdapter,
    ObservabilityConfig,
    OperationDataTransformer,
    observability,
)
from mistralai.observability.otel.models import GenAiMessage
from mistralai.observability.otel.sdk import require_configured


class SDKHarness:
    """In-memory SDK harness for asserting emitted telemetry."""

    def __init__(
        self,
        *,
        operation_data_transformers: Sequence[OperationDataTransformer] | None = None,
    ) -> None:
        """Configure the SDK with isolated in-memory exporters."""
        self.span_exporter = InMemorySpanExporter()
        self.metric_reader = InMemoryMetricReader()
        self.log_exporter = InMemoryLogRecordExporter()
        observability.configure(
            ObservabilityConfig(service_name="test-service"),
            operation_data_transformers=operation_data_transformers,
            span_exporter=self.span_exporter,
            metric_reader=self.metric_reader,
            log_exporter=self.log_exporter,
        )
        self.observability = require_configured()

    def shutdown(self) -> None:
        """Shut down the configured SDK after a test."""
        observability.shutdown()


class FakeChatCompletionAdapter(ChatCompletionAdapter):
    """Static completion adapter used by generic adapter tests."""

    @property
    def response_model(self) -> str | None:
        """Return a fake response model."""
        return "response-model"

    @property
    def response_id(self) -> str | None:
        """Return a fake response identifier."""
        return "resp_123"

    @property
    def input_messages(self) -> Sequence[GenAiMessage] | None:
        """Return fake request messages."""
        return [{"role": "user", "content": "hello"}]

    @property
    def output_messages(self) -> Sequence[GenAiMessage]:
        """Return fake response messages."""
        return [{"role": "assistant", "content": "bonjour"}]

    @property
    def finish_reasons(self) -> Sequence[str] | None:
        """Return fake finish reasons."""
        return ["stop"]

    @property
    def input_tokens(self) -> int | None:
        """Return fake input token usage."""
        return 8

    @property
    def output_tokens(self) -> int | None:
        """Return fake output token usage."""
        return 3


@pytest.fixture
def harness() -> Iterable[SDKHarness]:
    """Provide an isolated SDK harness per test."""
    sdk_harness = SDKHarness()
    try:
        yield sdk_harness
    finally:
        sdk_harness.shutdown()


def metrics_by_name(metrics_data: MetricsData | None) -> dict[str, Metric]:
    """Index collected metrics by instrument name."""
    assert metrics_data is not None
    return {
        metric.name: metric
        for resource_metric in metrics_data.resource_metrics
        for scope_metric in resource_metric.scope_metrics
        for metric in scope_metric.metrics
    }


def histogram_points(metric: Metric) -> Sequence[HistogramDataPoint]:
    """Return histogram data points from a metric."""
    assert isinstance(metric.data, Histogram)
    return metric.data.data_points


def point_attributes(point: HistogramDataPoint) -> Mapping[str, AttributeValue]:
    """Return attributes attached to a histogram point."""
    assert point.attributes is not None
    return point.attributes


def fake_clock(values: list[float]) -> Callable[[], float]:
    """Build a deterministic clock for streaming timer tests."""
    iterator = iter(values)

    def clock() -> float:
        return next(iterator)

    return clock
