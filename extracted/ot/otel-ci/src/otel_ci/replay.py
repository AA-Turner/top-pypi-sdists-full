import datetime
import json
import pathlib

from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import ReadableSpan

from otel_ci.logging import logger
from otel_ci.trace import get_exporter


def replay(output_directory: pathlib.Path) -> None:
    """Replay the"""
    otlp_exporter = get_exporter()
    spans = []
    if not output_directory.exists():
        raise ValueError("Trace directory %s does not exist", output_directory)

    for f in output_directory.glob("*.trace"):
        span_data = json.loads(f.read_text())
        # Convert ISO time to datetime
        start_time = datetime.datetime.fromisoformat(
            span_data["start_time"].replace("Z", "+00:00")
        )
        end_time = datetime.datetime.fromisoformat(
            span_data["end_time"].replace("Z", "+00:00")
        )

        # Generate trace and span IDs if not present
        trace_id = int(span_data["context"]["trace_id"], 16)
        span_id = int(span_data["context"]["span_id"], 16)

        # Create a resource (optional, but recommended)
        resource = Resource.create(
            {**(span_data.get("resource", {}).get("attributes", {}))}
        )

        # Create a ReadableSpan
        status_code = span_data.get("status", {}).get("status_code", "UNSET")
        status = trace.Status(
            status_code=trace.StatusCode[status_code],
            description=span_data.get("status", {}).get("description"),
        )
        sdk_span = ReadableSpan(
            name=span_data["name"],
            context=trace.SpanContext(trace_id, span_id, is_remote=False),
            parent=None,
            resource=resource,
            attributes=span_data.get("attributes", {}),
            events=[],  # Convert events if needed
            links=[],
            start_time=int(start_time.timestamp() * 1e9),
            end_time=int(end_time.timestamp() * 1e9),
            status=status,
        )
        spans.append(sdk_span)

        logger.debug("original_sdk_span: %s", span_data)
        logger.debug("parsed_sdk_span: %s", sdk_span.to_json())

    otlp_exporter.export(spans)
