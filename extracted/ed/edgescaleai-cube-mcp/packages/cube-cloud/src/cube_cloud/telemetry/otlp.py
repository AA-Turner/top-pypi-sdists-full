"""Groundcover OTLP export — the primary/hot tier + future correlation layer.

Emits ONE span per tool call over OTLP/HTTP. The span carries the same canonical
event as the S3 archive (attributes for the low-cardinality dimensions; span
duration = the dispatch latency; span status = ok/error). Modelled as a synthetic
service (`service.name = cube-cloud`, `span name = <tool>`) so the tool surface
is first-class in Groundcover's trace analytics and correlatable by `trace_id`.

Everything here is best-effort and never raises: a missing/invalid ingest secret
just disables export, and the BatchSpanProcessor exports asynchronously so a slow
or down collector never blocks a tool call. Endpoint + key come from the secret
`otlp_secret` (JSON: {"endpoint", "api_key", optional "api_key_header"}).

Live validation is deferred until the per-env Groundcover OTLP creds are
provisioned; the unit tests exercise the span shape with an in-memory exporter.
"""

from __future__ import annotations

import json
import logging
from typing import Any

from cube_cloud.config import settings
from cube_cloud.telemetry.events import ToolCallEvent

logger = logging.getLogger(__name__)

_MS_TO_NS = 1_000_000
# Span attributes are a bounded preview (full payload lives in the S3 row, linked
# by trace_id); keeps span size sane and within Groundcover's ingest limits.
_SPAN_PREVIEW_MAX = 8192


def _preview(text: str) -> str:
    if len(text) <= _SPAN_PREVIEW_MAX:
        return text
    return text[:_SPAN_PREVIEW_MAX] + f"…[+{len(text) - _SPAN_PREVIEW_MAX} chars; full in S3]"

# Lazily built once; None until first use, False if disabled after a failed build.
_tracer: Any = None
_disabled = False


def _load_secret() -> dict | None:
    """Read {endpoint, api_key, api_key_header?} from Secrets Manager."""
    import boto3

    client = boto3.client("secretsmanager", region_name=settings.aws_region)
    raw = client.get_secret_value(SecretId=settings.otlp_secret)["SecretString"]
    data = json.loads(raw)
    if not data.get("endpoint") or not data.get("api_key"):
        raise ValueError("otlp secret missing 'endpoint' or 'api_key'")
    return data


_SERVICE_NAME = "cube-cloud"
# Groundcover's "environment" is a company/customer grouping (EdgescaleAI, Lear,
# …) and dev/prod is already separated at the Groundcover *instance* level. So we
# do NOT stamp env_name (dev/prod) here. cube-cloud is the control plane — not a
# customer and not a single cube (cluster) — so it gets its own static
# environment. The per-call target cube is the `toolcall.cube` span attribute
# (these headers are per-export-batch, so they can't vary per span/cube), and no
# cluster header is set. dev/prod remains available as the `toolcall.env` attr.
_GC_ENVIRONMENT = "cube-mcp"


def _exporter_params(cfg: dict) -> tuple[str, dict]:
    """Derive the (endpoint, headers) for the OTLP/HTTP exporter from the secret.

    Groundcover's UI shows a *base* endpoint (e.g. https://x.platform.grcv.io)
    and relies on the OTel SDK env-var path to append `/v1/traces`. We pass the
    endpoint to the exporter constructor directly (no auto-append), so normalize
    it here — accept base or full. Groundcover buckets spans by the
    `x-groundcover-service-name` / `x-groundcover-env-name` headers, sent
    alongside the `apikey`."""
    endpoint = cfg["endpoint"].rstrip("/")
    if not endpoint.endswith("/v1/traces"):
        endpoint += "/v1/traces"
    headers = {
        cfg.get("api_key_header", "apikey"): cfg["api_key"],
        "x-groundcover-service-name": cfg.get("service_name", _SERVICE_NAME),
        "x-groundcover-env-name": cfg.get("gc_environment", _GC_ENVIRONMENT),
    }
    return endpoint, headers


def _build_tracer() -> Any:
    """Construct an isolated TracerProvider + OTLP/HTTP exporter. Not the global
    provider, so this never interferes with other tracing."""
    from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
    from opentelemetry.sdk.resources import Resource
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor

    from cube_cloud.telemetry.events import _CLOUD_VERSION

    cfg = _load_secret()
    endpoint, headers = _exporter_params(cfg)
    resource = Resource.create(
        {
            "service.name": _SERVICE_NAME,
            "service.version": _CLOUD_VERSION,
            "deployment.environment": settings.env_name,
        }
    )
    provider = TracerProvider(resource=resource)
    exporter = OTLPSpanExporter(endpoint=endpoint, headers=headers)
    provider.add_span_processor(BatchSpanProcessor(exporter))
    return provider.get_tracer("cube_cloud.telemetry")


def _get_tracer() -> Any:
    global _tracer, _disabled
    if _disabled:
        return None
    if _tracer is None:
        try:
            _tracer = _build_tracer()
        except Exception:
            logger.exception("telemetry: OTLP exporter init failed; disabling OTLP export")
            _disabled = True
            return None
    return _tracer


def emit_span(event: ToolCallEvent) -> None:
    """Emit one span for the tool call and stamp `event.trace_id` so the S3
    record links to the Groundcover trace. Never raises."""
    if not settings.otlp_enabled:
        return
    try:
        tracer = _get_tracer()
        if tracer is None:
            return

        from opentelemetry.trace import SpanKind, Status, StatusCode

        # Integer nanoseconds throughout — subtracting a float latency from a
        # large epoch-ns int would lose precision.
        end_ns = event.ts_epoch_ms * _MS_TO_NS
        start_ns = end_ns - int(round(event.latency_ms * _MS_TO_NS))

        span = tracer.start_span(event.tool, kind=SpanKind.SERVER, start_time=start_ns)
        try:
            span.set_attribute("toolcall.tool", event.tool)
            span.set_attribute("toolcall.tool_domain", event.tool_domain)
            span.set_attribute("toolcall.env", event.env)
            span.set_attribute("toolcall.source", event.source)
            span.set_attribute("toolcall.status", event.status)
            span.set_attribute("toolcall.latency_ms", event.latency_ms)
            span.set_attribute("toolcall.response_size_bytes", event.response_size_bytes)
            span.set_attribute("toolcall.response_dropped", event.response_dropped)
            for key, value in (
                ("toolcall.profile", event.profile),
                ("toolcall.key_id", event.key_id),
                ("toolcall.user_domain", event.user_domain),
                ("toolcall.user_email_hash", event.user_email_hash),
                # actor_type/bot_name were on the S3 row from issue #231 but never on
                # the span, so "who ran it" could not be asked in Groundcover at all —
                # noticed when the test-account classification landed and was
                # invisible there. Both sinks carry the same identity now.
                ("toolcall.actor_type", event.actor_type),
                ("toolcall.bot_name", event.bot_name),
                ("toolcall.cube", event.cube),
                ("toolcall.error_class", event.error_class),
                ("toolcall.caller_ip", event.caller_ip),
                ("toolcall.call_id", event.call_id),
                ("toolcall.error_message", event.error_message),
            ):
                if value is not None:
                    span.set_attribute(key, value)

            # Bounded, already-redacted preview of the command + response so the
            # call is inspectable in Groundcover without bouncing to S3. Full
            # fidelity lives in the S3 row (linked by trace_id); response-dropped
            # tools already have response == "".
            span.set_attribute("toolcall.args", _preview(json.dumps(event.args, default=str)))
            if event.response:
                span.set_attribute("toolcall.response", _preview(event.response))

            if event.status == "error":
                span.set_status(Status(StatusCode.ERROR, event.error_class or "error"))
            else:
                span.set_status(Status(StatusCode.OK))

            event.trace_id = format(span.get_span_context().trace_id, "032x")
        finally:
            span.end(end_time=end_ns)
    except Exception:
        logger.exception("telemetry: OTLP emit_span failed (swallowed)")
