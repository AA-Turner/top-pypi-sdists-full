import pathlib
import time
from typing import Any

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import (
    OTLPSpanExporter as GRPCSpanExporter,
)
from opentelemetry.exporter.otlp.proto.http.trace_exporter import (
    OTLPSpanExporter as HTTPSpanExporter,
)
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    ConsoleSpanExporter,
    SimpleSpanProcessor,
    SpanExporter,
)

from otel_ci import settings
from otel_ci.github import get_resource_attributes

otlp_exporter: SpanExporter | None = None


def get_otlp_exporter() -> SpanExporter:
    """
    Dynamically select OTLP exporter based on configuration.

    Support exporters:
    - 'otlp': Uses OTLP exporter
    - 'console': Uses console exporter
    - 'file': Uses file exporter
    - 'none': Uses no exporter

    Supported OTLP protocols:
    - 'grpc': Uses gRPC exporter
    - 'http/protobuf': Uses HTTP protobuf exporter
    - 'http/json': Uses HTTP JSON exporter (falls back to protobuf if not specified)
    """
    exporter = settings.OTEL_TRACES_EXPORTER
    protocol = settings.OTEL_EXPORTER_OTLP_PROTOCOL

    # Prepare exporter configuration
    exporter_kwargs: dict[str, Any] = {}

    if settings.OTEL_EXPORTER_OTLP_ENDPOINT:
        exporter_kwargs["endpoint"] = settings.OTEL_EXPORTER_OTLP_ENDPOINT
    if settings.OTEL_EXPORTER_OTLP_HEADERS:
        exporter_kwargs["headers"] = settings.OTEL_EXPORTER_OTLP_HEADERS
    if settings.OTEL_EXPORTER_OTLP_INSECURE:
        exporter_kwargs["insecure"] = settings.OTEL_EXPORTER_OTLP_INSECURE

    # Select exporter based on protocol
    if protocol == "grpc" and exporter == "otlp":
        # timeout is in seconds
        return GRPCSpanExporter(**exporter_kwargs, timeout=1, insecure=True)
    elif protocol in ["http/protobuf", "http/json"] and exporter == "otlp":
        return HTTPSpanExporter(**exporter_kwargs)
    elif exporter == "console":
        return ConsoleSpanExporter()
    elif exporter == "file":
        output_path = settings.OTEL_EXPORTER_FILE_DIRECTORY
        if not output_path:
            raise ValueError(
                "-o <output_directory> or `OTEL_EXPORTER_FILE_DIRECTORY` must be specified when using file export protocol"
            )
        pathlib.Path(output_path).mkdir(parents=True, exist_ok=True)
        filename = pathlib.Path(output_path) / f"{time.time()}.trace"
        output_file = open(filename, mode="w")
        return ConsoleSpanExporter(out=output_file)
    else:
        return SpanExporter()


def configure_tracer() -> None:
    global otlp_exporter
    assert settings.OTEL_SERVICE_NAME
    resource_attributes = {
        SERVICE_NAME: settings.OTEL_SERVICE_NAME,
        **get_resource_attributes(),
    }
    resource = Resource(attributes=resource_attributes)
    otlp_exporter = get_otlp_exporter()
    trace.set_tracer_provider(TracerProvider(resource=resource))
    span_processor = SimpleSpanProcessor(otlp_exporter)
    trace.get_tracer_provider().add_span_processor(span_processor)  # type: ignore


def get_exporter() -> SpanExporter:
    assert otlp_exporter
    return otlp_exporter
