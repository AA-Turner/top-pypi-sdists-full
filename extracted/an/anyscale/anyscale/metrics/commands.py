from datetime import datetime
from typing import List, Optional

from anyscale._private.sdk import sdk_command
from anyscale.metrics._private.metrics_sdk import PrivateMetricsSDK
from anyscale.metrics.models import MetricSeries, MetricsResource


_METRICS_SDK_SINGLETON_KEY = "metrics_sdk"

_NAMES_EXAMPLE = """
import anyscale
from anyscale.metrics.models import MetricsResource

names = anyscale.metrics.names(
    MetricsResource(resource_type="cluster", resource_id="ses_abc123"),
)
print(names)
"""

_NAMES_ARG_DOCSTRINGS = {
    "resource": "The cluster, workspace, job or service to list metric names for.",
    "start": "Only names with data at or after this time. None means the start of retention.",
    "end": "Only names with data at or before this time. None means now.",
}

_QUERY_EXAMPLE = """
import anyscale
from anyscale.metrics.models import MetricsResource

series = anyscale.metrics.query(
    "sum(ray_node_cpu_utilization)",
    MetricsResource(resource_type="cluster", resource_id="ses_abc123"),
)
for s in series:
    print(s.labels, s.samples[0].value)
"""

_QUERY_ARG_DOCSTRINGS = {
    "promql_query": "The PromQL expression to evaluate. The backend restricts it to the "
    "resource, so a selector may not name another resource.",
    "resource": "The cluster, workspace, job or service to evaluate it for.",
    "time": "Evaluate as of this moment. None means now.",
}

_QUERY_RANGE_EXAMPLE = """
from datetime import datetime, timedelta, timezone

import anyscale
from anyscale.metrics.models import MetricsResource

end = datetime.now(timezone.utc)
series = anyscale.metrics.query_range(
    "ray_node_mem_used",
    MetricsResource(resource_type="cluster", resource_id="ses_abc123"),
    start=end - timedelta(hours=2),
    end=end,
    step="1m",
)
for s in series:
    print(s.labels.get("instance"), [sample.value for sample in s.samples])
"""

_QUERY_RANGE_ARG_DOCSTRINGS = {
    "promql_query": "The PromQL expression to evaluate. The backend restricts it to the "
    "resource, so a selector may not name another resource.",
    "resource": "The cluster, workspace, job or service to evaluate it for.",
    "start": "Start of the window.",
    "end": "End of the window.",
    "step": "Distance between points, as a Prometheus duration such as 15s, 1m or 5m. "
    "None picks the larger of 15s and the window divided by 1000, so the result never "
    "has more than 1000 points per series.",
}


@sdk_command(
    _METRICS_SDK_SINGLETON_KEY,
    PrivateMetricsSDK,
    doc_py_example=_NAMES_EXAMPLE,
    arg_docstrings=_NAMES_ARG_DOCSTRINGS,
)
def names(
    resource: MetricsResource,
    *,
    start: Optional[datetime] = None,
    end: Optional[datetime] = None,
    _private_sdk: Optional[PrivateMetricsSDK] = None,
) -> List[str]:
    """List the metric names that have data for a cluster, workspace, job or service."""
    return _private_sdk.names(resource, start=start, end=end)  # type: ignore


@sdk_command(
    _METRICS_SDK_SINGLETON_KEY,
    PrivateMetricsSDK,
    doc_py_example=_QUERY_EXAMPLE,
    arg_docstrings=_QUERY_ARG_DOCSTRINGS,
)
def query(
    promql_query: str,
    resource: MetricsResource,
    *,
    time: Optional[datetime] = None,
    _private_sdk: Optional[PrivateMetricsSDK] = None,
) -> List[MetricSeries]:
    """Evaluate a PromQL expression at one moment for a cluster, workspace, job or service."""
    return _private_sdk.query(promql_query, resource, time=time)  # type: ignore


@sdk_command(
    _METRICS_SDK_SINGLETON_KEY,
    PrivateMetricsSDK,
    doc_py_example=_QUERY_RANGE_EXAMPLE,
    arg_docstrings=_QUERY_RANGE_ARG_DOCSTRINGS,
)
def query_range(
    promql_query: str,
    resource: MetricsResource,
    *,
    start: datetime,
    end: datetime,
    step: Optional[str] = None,
    _private_sdk: Optional[PrivateMetricsSDK] = None,
) -> List[MetricSeries]:
    """Evaluate a PromQL expression at every step across a time window."""
    return _private_sdk.query_range(  # type: ignore
        promql_query, resource, start=start, end=end, step=step
    )
