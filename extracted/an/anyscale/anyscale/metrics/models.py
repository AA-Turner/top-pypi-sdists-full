"""Models for `anyscale metrics ...` and `anyscale.metrics.*`."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List

from anyscale._private.models import ModelBase


# The resources metrics can be read for. The private SDK maps each to the query
# parameter the backend expects (job -> ha_job_id, the others -> <type>_id).
RESOURCE_TYPES: List[str] = ["cluster", "workspace", "job", "service"]


@dataclass(frozen=True)
class MetricsResource(ModelBase):
    """The cluster, workspace, job or service whose metrics to read.

    The backend restricts every query to this resource, so metrics of other resources
    in the same cloud are never returned.
    """

    __doc_py_example__ = """\
from anyscale.metrics.models import MetricsResource

# resource_type is one of: cluster, workspace, job, service.
resource = MetricsResource(resource_type="cluster", resource_id="ses_abc123")
"""

    resource_type: str = field(
        metadata={"docstring": "The kind of resource: cluster, workspace, job or service."}
    )
    resource_id: str = field(metadata={"docstring": "ID of the resource, e.g. ses_abc123."})

    def _validate_resource_type(self, resource_type: str):
        if resource_type not in RESOURCE_TYPES:
            raise ValueError(
                f"resource_type must be one of {RESOURCE_TYPES}, got {resource_type!r}."
            )

    def _validate_resource_id(self, resource_id: str):
        if not isinstance(resource_id, str) or not resource_id:
            raise ValueError("resource_id must be a non-empty string.")


@dataclass(frozen=True)
class MetricSample(ModelBase):
    """One value of a series at one moment."""

    __doc_py_example__ = """\
import anyscale
from anyscale.metrics.models import MetricsResource

resource = MetricsResource(resource_type="cluster", resource_id="ses_abc123")
for series in anyscale.metrics.query("ray_node_cpu_utilization", resource):
    sample = series.samples[0]
    print(series.labels.get("instance"), sample.timestamp, sample.value)
"""

    timestamp: datetime = field(
        metadata={"docstring": "When the value was observed, as a timezone-aware UTC datetime."}
    )
    value: float = field(
        metadata={
            "docstring": "The value. Prometheus's NaN, +Inf and -Inf arrive as the matching "
            "floats."
        }
    )

    def _validate_timestamp(self, timestamp: datetime):
        if not isinstance(timestamp, datetime):
            raise TypeError("timestamp must be a datetime.")

    def _validate_value(self, value: float):
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError("value must be a number.")


@dataclass(frozen=True)
class MetricSeries(ModelBase):
    """One time series: a set of labels and its samples.

    An instant query yields one sample per series; a range query yields one per step.
    """

    __doc_py_example__ = """\
from datetime import datetime, timedelta, timezone

import anyscale
from anyscale.metrics.models import MetricsResource

resource = MetricsResource(resource_type="cluster", resource_id="ses_abc123")
end = datetime.now(timezone.utc)
for series in anyscale.metrics.query_range(
    "ray_node_mem_used", resource, start=end - timedelta(hours=1), end=end, step="1m"
):
    print(series.labels.get("__name__"), [sample.value for sample in series.samples])
"""

    labels: Dict[str, str] = field(
        metadata={
            "docstring": "The series' labels. __name__ holds the metric name unless the "
            "query dropped it (aggregations do)."
        }
    )
    samples: List[MetricSample] = field(
        metadata={"docstring": "The values, oldest first. Exactly one for an instant query."}
    )

    def _validate_labels(self, labels: Dict[str, str]):
        if not isinstance(labels, dict) or not all(
            isinstance(key, str) and isinstance(value, str) for key, value in labels.items()
        ):
            raise TypeError("labels must be a dict of str to str.")

    def _validate_samples(self, samples: List[MetricSample]):
        if not isinstance(samples, list) or not all(
            isinstance(sample, MetricSample) for sample in samples
        ):
            raise TypeError("samples must be a list of MetricSample.")
