"""Prometheus metrics for autonomous mode v2 (ADR 0001). All gauges/counters live here; other modules import them by name."""

from prometheus_client import Counter, Gauge  # noqa: F401

kytte_outcome_queue_dropped_total = Counter(
    "kytte_outcome_queue_dropped_total",
    "OutcomeReports dropped because the local queue was full while the platform was unreachable.",
)

kytte_directives_applied_total = Counter(
    "kytte_directives_applied_total",
    "Directives applied, by result and source.",
    labelnames=["result", "source"],
)

kytte_platform_unreachable_seconds = Gauge(
    "kytte_platform_unreachable_seconds",
    "Seconds elapsed since the control stream last had a healthy connection. Zero while connected.",
)
