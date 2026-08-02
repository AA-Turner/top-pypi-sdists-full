#!/usr/bin/env python3
# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors
"""Azure Blob Storage metrics TUI for Geneva workloads.

A terminal dashboard for the Azure Monitor metrics that predict Geneva
backfill/apply health on a premium storage account: transaction volume by
operation, throttling, auth-request breakdown, throughput, latency,
availability and capacity. A separate data-plane panel inspects a single
container (blob count / bytes / top prefixes), since Azure Monitor metrics
are account-scoped and have no per-container dimension.

Panels
------
All metric panels except Container query the account-scoped ``Transactions``,
throughput, latency, availability and capacity metrics from Azure Monitor over
the selected time range (keys ``1``/``6``/``2``/``7``/``3`` switch ranges).

- ⚠ Throttling  — ``Transactions`` split by ``ResponseType``, filtered to the
  throttling responses (``ClientThrottlingError``, ``ServerBusyError``, etc.).
  Shows throttled request count and its share of all requests. The single best
  early-warning signal that a backfill is saturating the account.
- Transactions  — ``Transactions`` split by ``ApiName``. Header shows the total
  request count and success rate; the table ranks the top operations (e.g.
  ``GetBlob``, ``PutBlock``) by volume with a trend sparkline.
- Auth requests  — ``Transactions`` split by ``Authentication`` (AccountKey,
  OAuth, SAS, Anonymous). Header surfaces authorization-error count, so a
  credential/RBAC misconfiguration shows up immediately.
- Throughput  — ``Ingress`` / ``Egress`` totals (bytes moved in/out) with a
  sparkline of the trend across the window.
- Latency  — average ``SuccessE2ELatency`` (end-to-end, includes client/network
  round-trip) vs ``SuccessServerLatency`` (server-side processing only). A gap
  between the two points at network rather than storage as the bottleneck.
- Availability  — average ``Availability`` percent; green at ≥99.9%, red below.
- Capacity  — blob-service ``BlobCapacity`` (bytes) and ``BlobCount`` (number of
  blobs). These emit ~once a day, so the panel always shows the latest sample
  regardless of the selected range.
- Container  — data-plane only (no Azure Monitor). Press ``c`` to list a single
  container's blobs and aggregate count/bytes by top-level prefix; capped at
  ``MAX_BLOBS`` blobs. This is the only per-container view.

The account name and container are never hardcoded; pass them via flags or
environment variables.

Requires the `azure-metrics` extra:

    uv sync --extra azure-metrics

Authentication uses DefaultAzureCredential (Azure CLI login, managed/workload
identity, or service-principal env vars). The identity needs the
"Monitoring Reader" role for metrics, and "Storage Blob Data Reader" for the
container inspector.

Examples:
    az login
    uv run python tools/azure_storage_monitor.py \\
        --account <storage-account> --subscription <subscription-id>

    # explicit resource id (skips discovery)
    uv run python tools/azure_storage_monitor.py \\
        --resource-id /subscriptions/.../storageAccounts/<account>

    # via environment
    export AZURE_STORAGE_ACCOUNT_NAME=<account>
    export AZURE_SUBSCRIPTION_ID=<subscription-id>
    export AZURE_STORAGE_CONTAINER=<container>
    uv run python tools/azure_storage_monitor.py
"""

from __future__ import annotations

import argparse
import asyncio
import logging
import os
import sys
from dataclasses import dataclass, field
from datetime import timedelta
from typing import TYPE_CHECKING

from rich import box
from rich.console import Group, RenderableType
from rich.table import Table
from rich.text import Text
from textual import work
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container
from textual.widgets import Footer, Header, Static

if TYPE_CHECKING:
    from collections.abc import Callable, Iterable

    from azure.core.credentials import TokenCredential

_LOG = logging.getLogger(__name__)

ACCOUNT_NAMESPACE = "Microsoft.Storage/storageAccounts"
BLOB_NAMESPACE = "Microsoft.Storage/storageAccounts/blobServices"

TIME_RANGES = ["1h", "6h", "24h", "7d", "30d"]
TOP_N = 8
MAX_BLOBS = 50_000

# ResponseType dimension values that count as throttling. Any value containing
# "Throttling" is also treated as throttled (forward-compatible with new types).
THROTTLE_RESPONSE_TYPES = {
    "ClientThrottlingError",
    "ClientAccountRequestThrottlingError",
    "ClientAccountBandwidthThrottlingError",
    "ServerBusyError",
    "SuccessWithThrottling",
}

# (lookback, granularity) per selectable time range.
_GRANULARITY: dict[str, tuple[timedelta, timedelta]] = {
    "1h": (timedelta(hours=1), timedelta(minutes=1)),
    "6h": (timedelta(hours=6), timedelta(minutes=5)),
    "24h": (timedelta(hours=24), timedelta(minutes=15)),
    "7d": (timedelta(days=7), timedelta(hours=1)),
    "30d": (timedelta(days=30), timedelta(hours=6)),
}

_SPARK_CHARS = "▁▂▃▄▅▆▇█"


# --------------------------------------------------------------------------- #
# Pure helpers (unit-testable, no Azure required)
# --------------------------------------------------------------------------- #
def is_throttle(response_type: str | None) -> bool:
    """Return True if an Azure ResponseType value represents throttling."""
    value = response_type or ""
    return value in THROTTLE_RESPONSE_TYPES or "Throttling" in value


def granularity_for(time_range: str) -> tuple[timedelta, timedelta]:
    """Return the (lookback, granularity) pair for a time-range key."""
    return _GRANULARITY.get(time_range, _GRANULARITY["24h"])


def humanize_bytes(num: float | None) -> str:
    """Format a byte count with binary units; em dash when unknown."""
    if num is None:
        return "—"
    value = float(num)
    for unit in ("B", "KiB", "MiB", "GiB", "TiB", "PiB"):
        if abs(value) < 1024.0:
            return f"{value:.1f} {unit}"
        value /= 1024.0
    return f"{value:.1f} EiB"


def pct(part: float, whole: float) -> float:
    """Percentage of part within whole; 0.0 when whole is falsy."""
    return 100.0 * part / whole if whole else 0.0


def sparkline(values: Iterable[float | None], width: int = 20) -> str:
    """Render a unicode sparkline from the most recent ``width`` values."""
    nums = [float(v) for v in values if v is not None]
    if not nums:
        return ""
    data = nums[-width:]
    low, high = min(data), max(data)
    if high <= low:
        return _SPARK_CHARS[0] * len(data)
    span = high - low
    last = len(_SPARK_CHARS) - 1
    return "".join(_SPARK_CHARS[int((v - low) / span * last)] for v in data)


def resolve_resource_id(config: Config, credential: TokenCredential | None) -> str:
    """Resolve the storage account's ARM resource id.

    Order of precedence: explicit resource id, then a constructed id when the
    resource group is known, then discovery by account name within the
    subscription (requires ``azure-mgmt-storage`` and a credential).
    """
    if config.resource_id:
        return config.resource_id
    if not config.account_name:
        raise ValueError("provide --account (or AZURE_STORAGE_ACCOUNT_NAME)")
    if not config.subscription_id:
        raise ValueError(
            "provide --resource-id, or --subscription to discover it by account name"
        )
    if config.resource_group:
        return (
            f"/subscriptions/{config.subscription_id}"
            f"/resourceGroups/{config.resource_group}"
            f"/providers/{ACCOUNT_NAMESPACE}/{config.account_name}"
        )
    if credential is None:
        raise ValueError("a credential is required to discover the resource id")

    from azure.mgmt.storage import StorageManagementClient

    client = StorageManagementClient(credential, config.subscription_id)
    for account in client.storage_accounts.list():
        if account.name == config.account_name:
            return account.id
    raise ValueError(
        f"storage account '{config.account_name}' not found in subscription"
    )


def _clean(exc: BaseException) -> str:
    """Reduce an exception to a short, user-safe one-line message."""
    text = str(exc).strip()
    first = text.splitlines()[0] if text else exc.__class__.__name__
    return first[:200]


def access_hint(exc: BaseException) -> str:
    """Map common failures to a professional, actionable message."""
    if isinstance(exc, ModuleNotFoundError):
        return "Azure SDKs not installed. Run: uv sync --extra azure-metrics"
    if isinstance(exc, ImportError):
        # The module is present but a name is missing — almost always an
        # installed-but-incompatible SDK version, not a missing package.
        return f"Azure SDK version mismatch: {_clean(exc)}"
    text = str(exc)
    if "403" in text or "Forbidden" in text or "Authorization" in text:
        return (
            "No Azure Monitor access for this account. The signed-in identity "
            "needs the 'Monitoring Reader' role."
        )
    return _clean(exc)


# --------------------------------------------------------------------------- #
# Data models
# --------------------------------------------------------------------------- #
@dataclass
class Config:
    """Runtime configuration sourced from CLI flags and environment."""

    account_name: str | None = None
    container: str | None = None
    subscription_id: str | None = None
    resource_group: str | None = None
    resource_id: str | None = None
    time_range: str = "24h"
    refresh_seconds: int = 60
    account_key: str | None = None
    sas_token: str | None = None


@dataclass
class Series:
    """A single labelled metric time series."""

    label: str
    points: list[float | None] = field(default_factory=list)

    @property
    def total(self) -> float:
        """Sum of non-null points (for Total-aggregated metrics)."""
        return float(sum(p for p in self.points if p is not None))

    @property
    def mean(self) -> float:
        """Mean of non-null points (for Average-aggregated metrics)."""
        values = [p for p in self.points if p is not None]
        return float(sum(values) / len(values)) if values else 0.0


@dataclass
class Snapshot:
    """One refresh worth of account/service-level metrics."""

    time_range: str
    by_api: list[Series] = field(default_factory=list)
    by_response: list[Series] = field(default_factory=list)
    by_auth: list[Series] = field(default_factory=list)
    ingress: Series | None = None
    egress: Series | None = None
    e2e_latency: Series | None = None
    server_latency: Series | None = None
    availability: Series | None = None
    blob_capacity: float | None = None
    blob_count: float | None = None
    errors: dict[str, str] = field(default_factory=dict)


@dataclass
class ContainerStats:
    """Data-plane footprint of a single container."""

    container: str
    count: int
    total_bytes: int
    prefixes: list[tuple[str, int, int]] = field(default_factory=list)
    truncated: bool = False


# --------------------------------------------------------------------------- #
# Azure client layer
# --------------------------------------------------------------------------- #
def _latest(series: Series | None) -> float | None:
    """Return the most recent non-null point of a series."""
    if series is None:
        return None
    for point in reversed(series.points):
        if point is not None:
            return float(point)
    return None


def _value_of(point: object, aggregation: str) -> float | None:
    """Extract the total/average value from a metric data point."""
    attr = "total" if aggregation == "total" else "average"
    return getattr(point, attr, None)


def _metric_name(metric: object) -> str:
    name = getattr(metric, "name", "")
    if isinstance(name, str):
        return name
    return str(getattr(name, "value", name))


def _series_label(ts: object, metric: object) -> str:
    """Label a timeseries by its dimension value, else the metric name.

    Azure Monitor exposes the split dimension via ``metadata_values``. In
    azure-monitor-query 1.x this is a ``{dimension: value}`` dict; tolerate the
    older list-of-objects shape too. Falls back to the metric name when the
    series is not dimension-split.
    """
    meta = getattr(ts, "metadata_values", None)
    if isinstance(meta, dict):
        return str(next(iter(meta.values()))) if meta else _metric_name(metric)
    if meta:
        first = meta[0]
        return str(getattr(first, "value", first))
    return _metric_name(metric)


class AzureMetricsClient:
    """Thin wrapper over Azure Monitor and Blob storage for the dashboard."""

    def __init__(
        self, resource_id: str, config: Config, credential: TokenCredential
    ) -> None:
        self._resource_id = resource_id
        self._config = config
        self._credential = credential
        self._metrics_client: object | None = None

    def _client(self) -> object:
        if self._metrics_client is None:
            from azure.monitor.query import MetricsQueryClient

            self._metrics_client = MetricsQueryClient(self._credential)
        return self._metrics_client

    def _run(
        self,
        metric_names: list[str],
        aggregation: str,
        *,
        timespan: timedelta,
        granularity: timedelta,
        dim_filter: str | None = None,
        namespace: str = ACCOUNT_NAMESPACE,
        resource_uri: str | None = None,
    ) -> dict[str, list[Series]]:
        from azure.monitor.query import MetricAggregationType

        agg = (
            MetricAggregationType.TOTAL
            if aggregation == "total"
            else MetricAggregationType.AVERAGE
        )
        response = self._client().query_resource(  # type: ignore[attr-defined]
            resource_uri or self._resource_id,
            metric_names=metric_names,
            timespan=timespan,
            granularity=granularity,
            aggregations=[agg],
            filter=dim_filter,
            metric_namespace=namespace,
        )
        result: dict[str, list[Series]] = {}
        for metric in response.metrics:
            series_list: list[Series] = []
            for ts in metric.timeseries:
                label = _series_label(ts, metric)
                points = [_value_of(point, aggregation) for point in ts.data]
                series_list.append(Series(label=label, points=points))
            result[_metric_name(metric)] = series_list
        return result

    def _dim_series(
        self,
        metric: str,
        dimension: str,
        span: timedelta,
        gran: timedelta,
    ) -> list[Series]:
        result = self._run(
            [metric],
            "total",
            timespan=span,
            granularity=gran,
            dim_filter=f"{dimension} eq '*'",
        )
        return result.get(metric, [])

    def _plain_series(
        self,
        metrics: list[str],
        aggregation: str,
        span: timedelta,
        gran: timedelta,
        *,
        namespace: str = ACCOUNT_NAMESPACE,
        resource_uri: str | None = None,
    ) -> dict[str, Series]:
        result = self._run(
            metrics,
            aggregation,
            timespan=span,
            granularity=gran,
            namespace=namespace,
            resource_uri=resource_uri,
        )
        return {
            name: (series[0] if series else Series(name))
            for name, series in result.items()
        }

    def _capacity(self) -> tuple[float | None, float | None]:
        # Capacity metrics emit roughly daily but only support a 1-hour grain;
        # query a fixed wide window and take the latest sample regardless of
        # the selected time range.
        span, gran = timedelta(days=2), timedelta(hours=1)
        uri = f"{self._resource_id}/blobServices/default"
        series = self._plain_series(
            ["BlobCapacity", "BlobCount"],
            "average",
            span,
            gran,
            namespace=BLOB_NAMESPACE,
            resource_uri=uri,
        )
        return _latest(series.get("BlobCapacity")), _latest(series.get("BlobCount"))

    def fetch_all(self, time_range: str) -> Snapshot:
        """Query every account/service metric; isolate per-panel failures."""
        span, gran = granularity_for(time_range)
        snap = Snapshot(time_range=time_range)

        def safe(key: str, fn: Callable[[], None]) -> None:
            try:
                fn()
            except Exception as exc:  # noqa: BLE001 - surfaced per panel
                _LOG.warning("metric query %s failed: %s", key, exc)
                snap.errors[key] = access_hint(exc)

        safe(
            "transactions",
            lambda: setattr(
                snap, "by_api", self._dim_series("Transactions", "ApiName", span, gran)
            ),
        )
        safe(
            "throttle",
            lambda: setattr(
                snap,
                "by_response",
                self._dim_series("Transactions", "ResponseType", span, gran),
            ),
        )
        safe(
            "auth",
            lambda: setattr(
                snap,
                "by_auth",
                self._dim_series("Transactions", "Authentication", span, gran),
            ),
        )

        def _throughput() -> None:
            io = self._plain_series(["Ingress", "Egress"], "total", span, gran)
            snap.ingress = io.get("Ingress")
            snap.egress = io.get("Egress")

        def _latency() -> None:
            lat = self._plain_series(
                ["SuccessE2ELatency", "SuccessServerLatency"], "average", span, gran
            )
            snap.e2e_latency = lat.get("SuccessE2ELatency")
            snap.server_latency = lat.get("SuccessServerLatency")

        def _availability() -> None:
            avail = self._plain_series(["Availability"], "average", span, gran)
            snap.availability = avail.get("Availability")

        def _capacity() -> None:
            snap.blob_capacity, snap.blob_count = self._capacity()

        safe("throughput", _throughput)
        safe("latency", _latency)
        safe("availability", _availability)
        safe("capacity", _capacity)
        return snap


def fetch_container(config: Config, credential: TokenCredential) -> ContainerStats:
    """List a container and aggregate count/bytes by top-level prefix.

    Pure data plane: works with any blob-data role on the AAD identity
    (``--auth-mode login`` equivalent), or an explicit account key / SAS. It
    never touches Azure Resource Manager, so it runs even without
    control-plane access to the account.
    """
    container = config.container
    if not container:
        raise ValueError("set --container (or AZURE_STORAGE_CONTAINER) to inspect")

    from azure.storage.blob import BlobServiceClient

    account_url = f"https://{config.account_name}.blob.core.windows.net"
    blob_credential: object = credential
    if config.account_key:
        blob_credential = config.account_key
    elif config.sas_token:
        blob_credential = config.sas_token
    service = BlobServiceClient(account_url, credential=blob_credential)
    client = service.get_container_client(container)

    count = 0
    total_bytes = 0
    prefixes: dict[str, list[int]] = {}
    truncated = False
    for blob in client.list_blobs():
        count += 1
        size = int(getattr(blob, "size", 0) or 0)
        total_bytes += size
        top = blob.name.split("/", 1)[0]
        agg = prefixes.setdefault(top, [0, 0])
        agg[0] += 1
        agg[1] += size
        if count >= MAX_BLOBS:
            truncated = True
            break

    ranked = sorted(prefixes.items(), key=lambda kv: kv[1][1], reverse=True)
    top_prefixes = [(name, c, b) for name, (c, b) in ranked[:TOP_N]]
    return ContainerStats(
        container=container,
        count=count,
        total_bytes=total_bytes,
        prefixes=top_prefixes,
        truncated=truncated,
    )


def make_credential() -> TokenCredential:
    """Build a DefaultAzureCredential (imported lazily)."""
    from azure.identity import DefaultAzureCredential

    return DefaultAzureCredential()


# --------------------------------------------------------------------------- #
# Rendering helpers (Snapshot -> Rich renderables)
# --------------------------------------------------------------------------- #
def _error(message: str) -> Text:
    return Text(message, style="red")


def _series_table(
    series: Iterable[Series], head: str, value_label: str = "count"
) -> Table:
    table = Table(box=box.SIMPLE_HEAD, expand=True, pad_edge=False)
    table.add_column(head, style="cyan", no_wrap=True)
    table.add_column(value_label, justify="right")
    table.add_column("trend", justify="left", style="green")
    ranked = sorted(series, key=lambda s: s.total, reverse=True)
    for s in ranked[:TOP_N]:
        if s.total <= 0:
            continue
        table.add_row(s.label, f"{int(s.total):,}", sparkline(s.points))
    return table


def render_throttle(snap: Snapshot) -> RenderableType:
    if "throttle" in snap.errors:
        return _error(snap.errors["throttle"])
    total = sum(s.total for s in snap.by_response)
    throttled = [s for s in snap.by_response if is_throttle(s.label) and s.total > 0]
    throttled_total = sum(s.total for s in throttled)
    rate = pct(throttled_total, total)
    header = Text()
    style = "bold red" if throttled_total else "bold green"
    header.append(f"{int(throttled_total):,} throttled  ", style=style)
    header.append(f"({rate:.2f}% of {int(total):,} requests)", style="dim")
    if not throttled:
        return Group(header, Text("No throttling in window ✓", style="green"))
    return Group(header, _series_table(throttled, "response type"))


def render_transactions(snap: Snapshot) -> RenderableType:
    if "transactions" in snap.errors:
        return _error(snap.errors["transactions"])
    total = sum(s.total for s in snap.by_api)
    response_total = sum(s.total for s in snap.by_response)
    success = next((s.total for s in snap.by_response if s.label == "Success"), 0.0)
    rate = pct(success, response_total or total)
    header = Text()
    header.append(f"{int(total):,} total  ", style="bold")
    header.append(f"{rate:.2f}% success", style="dim")
    return Group(header, _series_table(snap.by_api, "operation"))


def render_auth(snap: Snapshot) -> RenderableType:
    if "auth" in snap.errors:
        return _error(snap.errors["auth"])
    authz = next(
        (s.total for s in snap.by_response if s.label == "AuthorizationError"), 0.0
    )
    header = Text()
    header.append("authorization errors: ", style="dim")
    header.append(f"{int(authz):,}", style="bold red" if authz else "green")
    return Group(header, _series_table(snap.by_auth, "auth method"))


def _metric_line(name: str, value: str, spark: str) -> Text:
    line = Text()
    line.append(f"{name:<8}", style="cyan")
    line.append(f"{value:>14}  ")
    line.append(spark, style="green")
    return line


def render_throughput(snap: Snapshot) -> RenderableType:
    if "throughput" in snap.errors:
        return _error(snap.errors["throughput"])
    ingress, egress = snap.ingress, snap.egress
    return Group(
        _metric_line(
            "Ingress",
            humanize_bytes(ingress.total if ingress else None),
            sparkline(ingress.points if ingress else []),
        ),
        _metric_line(
            "Egress",
            humanize_bytes(egress.total if egress else None),
            sparkline(egress.points if egress else []),
        ),
    )


def render_latency(snap: Snapshot) -> RenderableType:
    if "latency" in snap.errors:
        return _error(snap.errors["latency"])
    e2e, server = snap.e2e_latency, snap.server_latency
    return Group(
        _metric_line(
            "E2E",
            f"{e2e.mean:.1f} ms" if e2e else "—",
            sparkline(e2e.points if e2e else []),
        ),
        _metric_line(
            "Server",
            f"{server.mean:.1f} ms" if server else "—",
            sparkline(server.points if server else []),
        ),
    )


def render_availability(snap: Snapshot) -> RenderableType:
    if "availability" in snap.errors:
        return _error(snap.errors["availability"])
    avail = snap.availability
    if avail is None:
        return Text("—", style="dim")
    value = avail.mean
    style = "green" if value >= 99.9 else "bold red"
    return Group(
        Text(f"{value:.3f}%", style=style),
        Text(sparkline(avail.points), style="green"),
    )


def render_capacity(snap: Snapshot) -> RenderableType:
    if "capacity" in snap.errors:
        return _error(snap.errors["capacity"])
    return Group(
        _metric_line("Bytes", humanize_bytes(snap.blob_capacity), ""),
        _metric_line(
            "Blobs",
            f"{int(snap.blob_count):,}" if snap.blob_count is not None else "—",
            "",
        ),
    )


def render_container(stats: ContainerStats) -> RenderableType:
    header = Text()
    header.append(f"{stats.count:,} blobs  ", style="bold")
    header.append(humanize_bytes(stats.total_bytes), style="dim")
    if stats.truncated:
        header.append(f"  (capped at {MAX_BLOBS:,})", style="yellow")
    table = Table(box=box.SIMPLE_HEAD, expand=True, pad_edge=False)
    table.add_column("prefix", style="cyan", no_wrap=True)
    table.add_column("blobs", justify="right")
    table.add_column("size", justify="right")
    for name, count, size in stats.prefixes:
        table.add_row(name, f"{count:,}", humanize_bytes(size))
    return Group(header, table)


# --------------------------------------------------------------------------- #
# Textual application
# --------------------------------------------------------------------------- #
_PANEL_RENDERERS: dict[str, Callable[[Snapshot], RenderableType]] = {
    "throttle": render_throttle,
    "transactions": render_transactions,
    "auth": render_auth,
    "throughput": render_throughput,
    "latency": render_latency,
    "availability": render_availability,
    "capacity": render_capacity,
}

_PANEL_TITLES = {
    "throttle": "⚠ Throttling",
    "transactions": "Transactions",
    "auth": "Auth requests",
    "throughput": "Throughput",
    "latency": "Latency",
    "availability": "Availability",
    "capacity": "Capacity",
    "container": "Container",
}


class StorageMonitorApp(App):
    """Live Azure Monitor dashboard for a single storage account."""

    CSS = """
    #status {
        height: 1;
        padding: 0 1;
        background: $panel;
        color: $text;
    }
    #panels {
        layout: grid;
        grid-size: 3;
        grid-gutter: 1 1;
        padding: 1;
    }
    .panel {
        border: round $accent;
        padding: 0 1;
        height: 100%;
        overflow-y: auto;
    }
    """

    BINDINGS = [
        Binding("r", "refresh", "Refresh"),
        Binding("c", "container", "Inspect container"),
        Binding("1", "set_range('1h')", "1h"),
        Binding("6", "set_range('6h')", "6h"),
        Binding("2", "set_range('24h')", "24h"),
        Binding("7", "set_range('7d')", "7d"),
        Binding("3", "set_range('30d')", "30d"),
        Binding("q", "quit", "Quit"),
    ]

    def __init__(self, config: Config) -> None:
        super().__init__()
        self.config = config
        self._client: AzureMetricsClient | None = None
        self._resource_id: str | None = None
        self._credential: TokenCredential | None = None

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Static(id="status")
        with Container(id="panels"):
            yield Static(id="throttle", classes="panel")
            yield Static(id="transactions", classes="panel")
            yield Static(id="auth", classes="panel")
            yield Static(id="throughput", classes="panel")
            yield Static(id="latency", classes="panel")
            yield Static(id="availability", classes="panel")
            yield Static(id="capacity", classes="panel")
            yield Static(id="container", classes="panel")
        yield Footer()

    def on_mount(self) -> None:
        self.title = "Azure Storage Monitor"
        self.sub_title = self.config.account_name or "(no account)"
        for panel_id, title in _PANEL_TITLES.items():
            panel = self.query_one(f"#{panel_id}", Static)
            panel.border_title = title
            panel.update(Text("…", style="dim"))
        self.query_one("#container", Static).border_title = (
            f"Container: {self.config.container}"
            if self.config.container
            else "Container"
        )
        self.query_one("#container", Static).update(
            Text("press 'c' to inspect", style="dim")
        )
        self._set_status("connecting…")
        self.bootstrap()

    def _set_status(self, state: str) -> None:
        line = Text()
        line.append(f" {self.config.account_name or '—'} ", style="reverse")
        line.append(f"  range {self.config.time_range}")
        line.append(f"  refresh {self.config.refresh_seconds}s")
        line.append(f"  status: {state}")
        self.query_one("#status", Static).update(line)

    def _metrics_unavailable(self, message: str) -> None:
        """Show why metrics are unavailable without blocking the inspector."""
        self.query_one("#throttle", Static).update(_error(message))
        for panel_id in _PANEL_RENDERERS:
            if panel_id == "throttle":
                continue
            self.query_one(f"#{panel_id}", Static).update(
                Text("metrics unavailable", style="dim")
            )

    @work(exclusive=True, group="bootstrap")
    async def bootstrap(self) -> None:
        """Acquire a credential, start metrics if ARM access allows, and always
        keep the data-plane container inspector available."""
        try:
            credential = await asyncio.to_thread(make_credential)
        except Exception as exc:  # noqa: BLE001 - shown to the operator
            self._set_status("error")
            hint = access_hint(exc)
            self._metrics_unavailable(hint)
            self.query_one("#container", Static).update(_error(hint))
            return
        self._credential = credential

        # Metrics are control plane; the container inspector is not. A failure
        # to resolve the resource id (no ARM access) must not disable the
        # inspector, which works with the same data-plane credential.
        try:
            resource_id = await asyncio.to_thread(
                resolve_resource_id, self.config, credential
            )
        except Exception as exc:  # noqa: BLE001 - shown to the operator
            self._set_status("metrics unavailable · press 'c' to inspect container")
            self._metrics_unavailable(access_hint(exc))
            return
        self._client = AzureMetricsClient(resource_id, self.config, credential)
        self._resource_id = resource_id
        self.refresh_metrics()
        self.set_interval(self.config.refresh_seconds, self.refresh_metrics)

    @work(exclusive=True, group="metrics")
    async def refresh_metrics(self) -> None:
        if self._client is None:
            return
        self._set_status("refreshing…")
        try:
            snapshot = await asyncio.to_thread(
                self._client.fetch_all, self.config.time_range
            )
        except Exception as exc:  # noqa: BLE001 - shown to the operator
            self._set_status("error")
            self.query_one("#throttle", Static).update(_error(access_hint(exc)))
            return
        for panel_id, renderer in _PANEL_RENDERERS.items():
            self.query_one(f"#{panel_id}", Static).update(renderer(snapshot))
        self._set_status("ok")

    @work(exclusive=True, group="container")
    async def load_container(self) -> None:
        if self._credential is None:
            return
        panel = self.query_one("#container", Static)
        panel.update(Text("loading…", style="dim"))
        try:
            stats = await asyncio.to_thread(
                fetch_container, self.config, self._credential
            )
        except Exception as exc:  # noqa: BLE001 - shown to the operator
            panel.update(_error(access_hint(exc)))
            return
        panel.update(render_container(stats))

    def action_refresh(self) -> None:
        self.refresh_metrics()

    def action_container(self) -> None:
        self.load_container()

    def action_set_range(self, value: str) -> None:
        self.config.time_range = value
        self.sub_title = f"{self.config.account_name} · {value}"
        self.refresh_metrics()


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Azure Blob Storage metrics TUI for Geneva workloads."
    )
    parser.add_argument(
        "--account",
        default=os.environ.get("AZURE_STORAGE_ACCOUNT_NAME"),
        help="storage account name (or AZURE_STORAGE_ACCOUNT_NAME)",
    )
    parser.add_argument(
        "--container",
        default=os.environ.get("AZURE_STORAGE_CONTAINER"),
        help="container for the inspector (or AZURE_STORAGE_CONTAINER)",
    )
    parser.add_argument(
        "--subscription",
        default=os.environ.get("AZURE_SUBSCRIPTION_ID"),
        help="subscription id for resource-id discovery (or AZURE_SUBSCRIPTION_ID)",
    )
    parser.add_argument(
        "--resource-group",
        default=os.environ.get("AZURE_RESOURCE_GROUP"),
        help="resource group (or AZURE_RESOURCE_GROUP); skips discovery",
    )
    parser.add_argument(
        "--resource-id",
        default=os.environ.get("AZURE_STORAGE_RESOURCE_ID"),
        help="full ARM resource id; bypasses all discovery",
    )
    parser.add_argument(
        "--time-range", choices=TIME_RANGES, default="24h", help="initial time range"
    )
    parser.add_argument(
        "--refresh", type=int, default=60, help="auto-refresh interval in seconds"
    )
    parser.add_argument(
        "--account-key",
        default=os.environ.get("AZURE_STORAGE_ACCOUNT_KEY"),
        help="account key for the container inspector only (data plane)",
    )
    parser.add_argument(
        "--sas",
        default=os.environ.get("AZURE_STORAGE_SAS_TOKEN"),
        help="SAS token for the container inspector only (data plane)",
    )
    parser.add_argument("--log-level", default=None, help="enable file logging")
    parser.add_argument(
        "--log-file", default="azure_storage_monitor.log", help="log file path"
    )
    return parser


def config_from_args(args: argparse.Namespace) -> Config:
    return Config(
        account_name=args.account,
        container=args.container,
        subscription_id=args.subscription,
        resource_group=args.resource_group,
        resource_id=args.resource_id,
        time_range=args.time_range,
        refresh_seconds=args.refresh,
        account_key=args.account_key,
        sas_token=args.sas,
    )


def setup_logging(level: str | None, log_file: str) -> None:
    """Log to a file when a level is set; never write to the TUI screen."""
    if level:
        logging.basicConfig(
            level=level.upper(),
            filename=log_file,
            format="%(asctime)s %(levelname)s %(name)s %(message)s",
        )
    else:
        logging.getLogger().addHandler(logging.NullHandler())


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    setup_logging(args.log_level, args.log_file)
    config = config_from_args(args)

    if not config.resource_id and not config.account_name:
        sys.stderr.write(
            "error: provide --account (or AZURE_STORAGE_ACCOUNT_NAME), "
            "or --resource-id\n"
        )
        return 1

    StorageMonitorApp(config).run()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
