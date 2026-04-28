"""OpenTelemetry bootstrap for the worker.

Activated only when OTEL_EXPORTER_OTLP_ENDPOINT is set. All other behaviour is
controlled by standard OTEL_* env vars so you can repoint this at Honeycomb (or
any OTLP backend) without code changes:

    OTEL_EXPORTER_OTLP_ENDPOINT=https://api.honeycomb.io
    OTEL_EXPORTER_OTLP_HEADERS=x-honeycomb-team=<api-key>

Pika's instrumentation extracts the W3C traceparent injected by cloud-api's
amqplib instrumentation, so each execution shows up as a child of the request
that enqueued it.
"""

import os


def init_tracing(service_name: str = "abstra-worker") -> None:
    if not os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT"):
        return

    from opentelemetry import trace
    from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
    from opentelemetry.instrumentation.pika import PikaInstrumentor
    from opentelemetry.instrumentation.requests import RequestsInstrumentor
    from opentelemetry.instrumentation.urllib3 import URLLib3Instrumentor
    from opentelemetry.sdk.resources import Resource
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor

    resource = Resource.create(
        {
            "service.name": os.getenv("OTEL_SERVICE_NAME", service_name),
        }
    )
    provider = TracerProvider(resource=resource)
    provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter()))
    trace.set_tracer_provider(provider)

    PikaInstrumentor().instrument()
    RequestsInstrumentor().instrument()
    URLLib3Instrumentor().instrument()
