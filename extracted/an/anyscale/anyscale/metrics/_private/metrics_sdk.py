from datetime import datetime, timezone
import math
from typing import Any, Dict, List, Optional, Sequence

from anyscale._private.sdk.base_sdk import BaseSDK
from anyscale.metrics.models import MetricSample, MetricSeries, MetricsResource


# What the SDK calls a resource -> the query parameter the backend expects. Exactly one
# is sent; the backend resolves it to the cloud, checks permission, and pins every
# selector in the query to that resource.
_RESOURCE_PARAM: Dict[str, str] = {
    "cluster": "cluster_id",
    "workspace": "workspace_id",
    "job": "ha_job_id",
    "service": "service_id",
}

# The default step is chosen so a range has at most this many points per series. Prometheus
# and Mimir reject a query_range that would return more than 11,000, and the CLI prints
# every point, so a much lower cap is the useful one.
_MAX_DEFAULT_POINTS = 1000
_MIN_STEP_SECONDS = 15


def default_step(start: datetime, end: datetime) -> str:
    """The step used when the caller gives none: the larger of 15s and window / 1000.

    A fixed 15s fails past about 46 hours (Mimir's 11,000-point limit), so the step
    grows with the window. Rounded up to whole seconds, e.g. ``15s`` for anything up to
    4h10m, ``173s`` for two days.
    """
    # Go through the epoch so a naive and an aware datetime can be mixed, as the wire
    # conversion already allows (naive means UTC).
    window_seconds = _epoch_required(end) - _epoch_required(start)
    seconds = max(_MIN_STEP_SECONDS, math.ceil(window_seconds / _MAX_DEFAULT_POINTS))
    return f"{seconds}s"


class PrivateMetricsSDK(BaseSDK):
    def names(
        self,
        resource: MetricsResource,
        *,
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
    ) -> List[str]:
        """Metric names with series for `resource`, sorted. Whole retention when no window."""
        response = self.client.get_metric_names(
            resource=_wire(resource), start=_epoch(start), end=_epoch(end)
        )
        return sorted(response.get("data") or [])

    def query(
        self,
        promql_query: str,
        resource: MetricsResource,
        *,
        time: Optional[datetime] = None,
    ) -> List[MetricSeries]:
        """Evaluate `promql_query` at one moment (now when `time` is None)."""
        response = self.client.query_metrics(
            promql_query=promql_query, resource=_wire(resource), time=_epoch(time)
        )
        return _to_series(response)

    def query_range(
        self,
        promql_query: str,
        resource: MetricsResource,
        *,
        start: datetime,
        end: datetime,
        step: Optional[str] = None,
    ) -> List[MetricSeries]:
        """Evaluate `promql_query` at every `step` across [start, end].

        `step` is sent as given; None becomes `default_step(start, end)`.
        """
        response = self.client.query_metrics_range(
            promql_query=promql_query,
            resource=_wire(resource),
            start=_epoch_required(start),
            end=_epoch_required(end),
            step=step if step is not None else default_step(start, end),
        )
        return _to_series(response)


def _wire(resource: MetricsResource) -> Dict[str, str]:
    return {_RESOURCE_PARAM[resource.resource_type]: resource.resource_id}


def _epoch(value: Optional[datetime]) -> Optional[float]:
    return None if value is None else _epoch_required(value)


def _epoch_required(value: datetime) -> float:
    # A naive datetime is taken as UTC, matching the CLI's time flags.
    aware = value if value.tzinfo else value.replace(tzinfo=timezone.utc)
    return aware.timestamp()


def _to_series(response: Dict[str, Any]) -> List[MetricSeries]:
    """The Prometheus response body -> models.

    `response` is what Mimir returned: ``{"status": "success", "data": {"resultType":
    ..., "result": ...}}``. A vector carries one ``value`` per series, a matrix a list
    of ``values``, and a scalar a single value with no labels.
    """
    data = response.get("data") or {}
    result = data.get("result")
    if data.get("resultType") == "scalar" and result is not None:
        return [MetricSeries(labels={}, samples=[_sample(result)])]

    series: List[MetricSeries] = []
    for item in result or []:
        labels = {str(key): str(value) for key, value in (item.get("metric") or {}).items()}
        if "value" in item:
            samples = [_sample(item["value"])]
        else:
            samples = [_sample(pair) for pair in item.get("values") or []]
        series.append(MetricSeries(labels=labels, samples=samples))
    return series


def _sample(pair: Sequence[Any]) -> MetricSample:
    # Prometheus sends [<unix seconds>, "<value as string>"]; the string may be NaN or +Inf.
    timestamp, value = pair
    return MetricSample(
        timestamp=datetime.fromtimestamp(float(timestamp), tz=timezone.utc),
        value=float(value),
    )
