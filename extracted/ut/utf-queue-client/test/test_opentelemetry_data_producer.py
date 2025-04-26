import pytest
from conftest import temporary_environment_variable_setter
from opentelemetry import trace
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import MetricExportResult
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    SimpleSpanProcessor,
)
from otel_extensions import (
    TelemetryOptions,
    flush_telemetry_data,
    get_tracer,
    init_telemetry_provider,
)

from utf_queue_client.clients.opentelemetry_data_producer import (
    OpenTelemetryDataProducer,
)
from utf_queue_client.exceptions import ValidationError
from utf_queue_client.utils.queue_metrics_exporter import (
    QueueMetricsExporter,
)
from utf_queue_client.utils.queue_span_exporter import (
    QUEUE_SPAN_EXPORTER_TYPE_NAME,
    QueueSpanExporter,
)


@pytest.fixture(params=[SimpleSpanProcessor, BatchSpanProcessor])
def queue_tracer_provider(request, amqp_url):
    resource = Resource(attributes={SERVICE_NAME: request.node.name})
    tracer_provider = TracerProvider(resource=resource)
    processor_type = request.param
    processor = processor_type(
        QueueSpanExporter(TelemetryOptions(OTEL_EXPORTER_OTLP_ENDPOINT=amqp_url))
    )
    tracer_provider.add_span_processor(processor)
    yield tracer_provider


@pytest.fixture()
def queue_metrics_provider(request, queue_metrics_exporter):
    resource = Resource(attributes={SERVICE_NAME: request.node.name})
    provider = MeterProvider(
        resource=resource, metric_readers=[queue_metrics_exporter.get_reader()]
    )
    yield provider


@pytest.fixture(params=[None, "gzip", "deflate"])
def queue_metrics_exporter(amqp_url, request):
    with temporary_environment_variable_setter(
        "OTEL_EXPORTER_OTLP_COMPRESSION", request.param
    ):
        yield QueueMetricsExporter(
            TelemetryOptions(OTEL_EXPORTER_OTLP_ENDPOINT=amqp_url)
        )


def test_data_producer_empty_url():
    with pytest.raises(RuntimeError):
        _ = OpenTelemetryDataProducer()


@pytest.mark.parametrize(
    "set_custom_queue_params",
    [
        {},
        {
            "UTF_QUEUE_USERNAME": "utfsilabs",
            "UTF_QUEUE_PASSWORD": "utfsilabs",
            "UTF_QUEUE_HOSTNAME": "ateaus002d.silabs.com",
            "UTF_QUEUE_SCHEME": "amqp",
            "UTF_QUEUE_PORT": "5672",
            "UTF_QUEUE_VIRTUAL_HOST": "%2f",
        },
    ],
    indirect=True,
)
def test_data_producer_central_queue(
    request,
    amqp_url,
    queue_consumer,
):  # noqa
    producer = OpenTelemetryDataProducer(
        url=amqp_url, producer_app_id=request.node.name
    )
    producer.publish_telemetry_data("LOGS", b"1234")
    queue_consumer.expect_messages(1)
    producer.publish_telemetry_data("METRICS", b"1234")
    queue_consumer.expect_messages(2)
    producer.publish_telemetry_data("TRACES", b"1234")
    queue_consumer.expect_messages(3)
    with pytest.raises(ValidationError):
        producer.publish_telemetry_data("SOMETHING", b"1234")


def test_queue_span_exporter_direct(
    request, amqp_url, queue_consumer, queue_tracer_provider
):
    for i in range(1, 10):
        with trace.get_tracer(
            __name__, tracer_provider=queue_tracer_provider
        ).start_as_current_span(request.node.name) as span:
            assert span.name == request.node.name
        queue_tracer_provider.force_flush()
        queue_consumer.expect_messages(i)


@pytest.mark.parametrize("compression", [None, "gzip", "deflate"])
def test_queue_span_exporter_indirect(request, amqp_url, queue_consumer, compression):
    with temporary_environment_variable_setter(
        "OTEL_EXPORTER_OTLP_COMPRESSION", compression
    ):
        options = TelemetryOptions(
            OTEL_EXPORTER_OTLP_ENDPOINT=amqp_url,
            OTEL_EXPORTER_OTLP_PROTOCOL="custom",
            OTEL_EXPORTER_CUSTOM_SPAN_EXPORTER_TYPE=QUEUE_SPAN_EXPORTER_TYPE_NAME,
            OTEL_SERVICE_NAME="foo",
            OTEL_PROCESSOR_TYPE="batch",
        )
        init_telemetry_provider(options)
        for i in range(1, 10):
            with get_tracer(__name__, "foo").start_as_current_span(
                request.node.name
            ) as span:
                assert span.name == request.node.name
            flush_telemetry_data()
            queue_consumer.expect_messages(i)


def test_invalid_compression(amqp_url):
    with temporary_environment_variable_setter(
        "OTEL_EXPORTER_OTLP_COMPRESSION", "crap"
    ):
        with pytest.raises(ValueError):
            QueueSpanExporter(TelemetryOptions(OTEL_EXPORTER_OTLP_ENDPOINT=amqp_url))
        with pytest.raises(ValueError):
            QueueMetricsExporter(TelemetryOptions(OTEL_EXPORTER_OTLP_ENDPOINT=amqp_url))
    with temporary_environment_variable_setter(
        "OTEL_EXPORTER_OTLP_TRACES_COMPRESSION", "crap"
    ):
        with pytest.raises(ValueError):
            QueueSpanExporter(TelemetryOptions(OTEL_EXPORTER_OTLP_ENDPOINT=amqp_url))
    with temporary_environment_variable_setter(
        "OTEL_EXPORTER_OTLP_METRICS_COMPRESSION", "crap"
    ):
        with pytest.raises(ValueError):
            QueueMetricsExporter(TelemetryOptions(OTEL_EXPORTER_OTLP_ENDPOINT=amqp_url))


def test_queue_metrics_exporter_direct(
    request, amqp_url, queue_metrics_exporter, queue_metrics_provider
):
    meter = queue_metrics_provider.get_meter(request.node.name)
    counter = meter.create_counter(
        "work.counter", unit="1", description="counts the amount of work done"
    )
    for _ in range(1, 10):
        counter.add(1, {"work.type": "testing"})
        assert queue_metrics_exporter.read_and_export() == MetricExportResult.SUCCESS

    queue_metrics_exporter.producer = None
    assert queue_metrics_exporter.read_and_export() == MetricExportResult.FAILURE
