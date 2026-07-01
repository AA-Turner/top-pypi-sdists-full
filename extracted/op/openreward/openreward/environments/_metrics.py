"""OpenTelemetry metric emission for the env server.

Emits a tool-call counter via OTLP/gRPC. The exporter ships to whatever
endpoint ``OPENREWARD_OTLP_ENDPOINT`` points at — typically an in-cluster
OpenTelemetry Collector that owns the credentials and downstream routing.

Enabling: set ``OPENREWARD_OTLP_ENDPOINT`` to the collector's hostport
(e.g. ``opentelemetry-collector.opentelemetry.svc.cluster.local:4317``).
:meth:`openreward.environments.server.Server.run` calls
:func:`setup_metrics` unconditionally on startup; if the env var isn't
set, the call is a no-op and :func:`record_tool_call` stays silent.

TLS:
  - Endpoint ``https://host:port`` or port 443 → TLS handshake.
  - Anything else (``host:port`` or ``http://host:port``) → plaintext.
  - ``OPENREWARD_OTLP_INSECURE=1`` forces plaintext regardless of scheme.
"""

from __future__ import annotations

import logging
import os
from typing import Optional
from urllib.parse import urlparse

from opentelemetry import metrics as otel_metrics
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.metrics import Counter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.resources import Resource

logger = logging.getLogger(__name__)


# Set by setup_metrics(); None means metrics are disabled (record_tool_call
# is a no-op).
_counter: Optional[Counter] = None
_provider: Optional[MeterProvider] = None


def _resolve_insecure(endpoint: str) -> bool:
    """Decide whether the OTLP connection should be plaintext.

    Explicit ``OPENREWARD_OTLP_INSECURE`` env wins. Otherwise infer from
    the endpoint: https:// or :443 → TLS; everything else → plaintext.
    Cluster-internal collectors are typically plaintext, so the default
    has to handle the unprefixed-hostport form (``host:4317``).
    """
    override = os.environ.get("OPENREWARD_OTLP_INSECURE", "").lower()
    if override in ("1", "true", "yes"):
        return True
    if override in ("0", "false", "no"):
        return False

    parsed = urlparse(endpoint if "://" in endpoint else f"//{endpoint}", scheme="")
    if parsed.scheme == "https" or parsed.port == 443:
        return False
    return True


def setup_metrics(
    endpoint: Optional[str] = None,
    flush_interval_ms: int = 30_000,
    service_name: str = "openreward-env-server",
) -> None:
    """Install an OTLP exporter and create the tool-call counter.

    No-op when neither ``endpoint`` nor ``OPENREWARD_OTLP_ENDPOINT`` is
    set — this is how the SDK ships safely to external users who haven't
    opted into telemetry. Safe to call multiple times; only the first
    setup wins.

    ``flush_interval_ms`` controls how often the exporter ships batched
    points (default 30s). Tuned short because env-server pods are often
    short-lived (sandbox autoscaling tears them down within a few
    minutes of idle); a longer interval means the only export attempt
    happens during shutdown, when networking is being torn down
    concurrently and gRPC connections fail.
    """
    global _counter, _provider
    if _counter is not None:
        return

    endpoint = endpoint or os.environ.get("OPENREWARD_OTLP_ENDPOINT")
    if not endpoint:
        return

    insecure = _resolve_insecure(endpoint)
    exporter = OTLPMetricExporter(endpoint=endpoint, insecure=insecure)
    reader = PeriodicExportingMetricReader(
        exporter, export_interval_millis=flush_interval_ms
    )
    provider = MeterProvider(
        metric_readers=[reader],
        resource=Resource.create({"service.name": service_name}),
    )
    otel_metrics.set_meter_provider(provider)

    meter = otel_metrics.get_meter("openreward.environments.server")
    _counter = meter.create_counter(
        name="openreward.tool_calls",
        description="Count of tool calls by environment and outcome.",
        unit="1",
    )
    _provider = provider
    logger.info(
        "metrics_setup_complete endpoint=%s insecure=%s service_name=%s",
        endpoint, insecure, service_name,
    )


def record_tool_call(env_name: str, status: str) -> None:
    """Increment the tool-call counter. No-op if metrics aren't configured.

    ``tool_name`` was previously a label but has been dropped to control
    cardinality (~1000 envs × ~100 tools × 5 statuses ≈ 500K series,
    well over GMP's 200K/cluster soft limit). Per-tool drill-down stays
    available via the ``tool_call_completed`` structured logs in Cloud
    Logging — which carry env_name + tool + duration + sid.
    """
    if _counter is None:
        return
    _counter.add(
        1,
        attributes={
            "env_name": env_name,
            "status": status,
        },
    )


def shutdown_metrics(timeout_millis: int = 30_000) -> None:
    """Flush pending exports and stop the periodic reader.

    Called from the FastAPI lifespan teardown so we don't lose the last
    flush window on graceful shutdown. Safe to call even when metrics
    were never set up.
    """
    global _counter, _provider
    if _provider is None:
        return
    try:
        _provider.shutdown(timeout_millis=timeout_millis)
    except Exception as e:
        logger.warning("metrics_shutdown_failed: %s", e)
    _provider = None
    _counter = None
