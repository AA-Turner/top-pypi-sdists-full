"""Models for `anyscale logs query` and `anyscale.logs.query`."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List

from anyscale._private.models import ModelBase


# The resources logs can be read for. The private SDK maps each to the query parameter
# the backend expects (job -> ha_job_id, the others -> <type>_id).
RESOURCE_TYPES: List[str] = ["cluster", "workspace", "job", "service"]

# Which lines a query searches: the workload's own output, or Ray's own files (raylet,
# gcs, core_worker), which reach the store at WARNING and above only.
LOG_TYPES: List[str] = ["application", "system"]


@dataclass(frozen=True)
class LogsResource(ModelBase):
    """The cluster, workspace, job or service whose logs to read.

    The backend scopes every query to this resource, so logs of other resources in the
    same cloud are never returned.
    """

    __doc_py_example__ = """\
from anyscale.logs.models import LogsResource

# resource_type is one of: cluster, workspace, job, service.
resource = LogsResource(resource_type="job", resource_id="prodjob_abc123")
"""

    resource_type: str = field(
        metadata={"docstring": "The kind of resource: cluster, workspace, job or service."}
    )
    resource_id: str = field(metadata={"docstring": "ID of the resource, e.g. prodjob_abc123."})

    def _validate_resource_type(self, resource_type: str):
        if resource_type not in RESOURCE_TYPES:
            raise ValueError(
                f"resource_type must be one of {RESOURCE_TYPES}, got {resource_type!r}."
            )

    def _validate_resource_id(self, resource_id: str):
        if not isinstance(resource_id, str) or not resource_id:
            raise ValueError("resource_id must be a non-empty string.")


@dataclass(frozen=True)
class LogLine(ModelBase):
    """One log line matched by a query."""

    __doc_py_example__ = """\
from datetime import datetime, timedelta, timezone

import anyscale
from anyscale.logs.models import LogsResource

end = datetime.now(timezone.utc)
for line in anyscale.logs.query(
    '{} |= "OOM"',
    LogsResource(resource_type="job", resource_id="prodjob_abc123"),
    start=end - timedelta(hours=1),
    end=end,
):
    print(line.timestamp, line.fields.get("level"), line.message)
"""

    timestamp: datetime = field(
        metadata={"docstring": "When the line was written, as a timezone-aware UTC datetime."}
    )
    message: str = field(metadata={"docstring": "The line's text."})
    fields: Dict[str, Any] = field(
        metadata={
            "docstring": "Everything else the store holds for the line: its stream labels "
            "(instance_id, cluster_id, ...) and any fields parsed from a JSON line (level, "
            "component_name, ...)."
        }
    )

    def _validate_timestamp(self, timestamp: datetime):
        if not isinstance(timestamp, datetime):
            raise TypeError("timestamp must be a datetime.")

    def _validate_message(self, message: str):
        if not isinstance(message, str):
            raise TypeError("message must be a string.")

    def _validate_fields(self, fields: Dict[str, Any]):
        if not isinstance(fields, dict) or not all(isinstance(key, str) for key in fields):
            raise TypeError("fields must be a dict with string keys.")
