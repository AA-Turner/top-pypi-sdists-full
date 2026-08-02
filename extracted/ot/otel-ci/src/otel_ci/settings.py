import os
from typing import Literal


def parse_key_val(key_val_str: str) -> dict[str, str]:
    return dict(h.split("=") for h in key_val_str.split(",") if "=" in h)


OTEL_TRACES_EXPORTER: Literal["otlp", "console", "file"] | None = os.environ.get(  # type: ignore
    "OTEL_TRACES_EXPORTER"
)
OTEL_EXPORTER_OTLP_PROTOCOL: Literal["grpc", "http/protobuf"] | None = os.environ.get(  # type: ignore
    "OTEL_EXPORTER_OTLP_PROTOCOL"
)
_headers = os.getenv("OTEL_EXPORTER_OTLP_HEADERS")
OTEL_EXPORTER_OTLP_HEADERS: dict | None = parse_key_val(_headers) if _headers else None

OTEL_EXPORTER_OTLP_INSECURE: bool = (
    os.getenv("OTEL_EXPORTER_OTLP_INSECURE", "false").lower() == "true"
)
OTEL_EXPORTER_FILE_DIRECTORY: str | None = os.getenv("OTEL_EXPORTER_FILE_DIRECTORY")
OTEL_EXPORTER_OTLP_ENDPOINT: str | None = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT")
OTEL_SERVICE_NAME: str | None = os.getenv(
    "OTEL_SERVICE_NAME", "github-action" if os.getenv("GITHUB_ACTION") else "otel-ci"
)
OTEL_SPAN_NAME: str | None = os.getenv("OTEL_SPAN_NAME")
_otel_resource_attributes = os.getenv("OTEL_RESOURCE_ATTRIBUTES")
OTEL_RESOURCE_ATTRIBUTES: dict[str, str] | None = (
    parse_key_val(_otel_resource_attributes) if _otel_resource_attributes else None
)
