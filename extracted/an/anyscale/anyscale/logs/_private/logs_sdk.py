from datetime import datetime, timezone
import json
from typing import Any, Dict, List

from anyscale._private.sdk.base_sdk import BaseSDK
from anyscale.logs.models import LOG_TYPES, LogLine, LogsResource


# What the SDK calls a resource -> the query parameter the backend expects. Exactly one
# is sent; the backend resolves it to the cloud, checks permission, and pins the query's
# stream selector to that resource.
_RESOURCE_PARAM: Dict[str, str] = {
    "cluster": "cluster_id",
    "workspace": "workspace_id",
    "job": "ha_job_id",
    "service": "service_id",
}

# The backend caps one query at this many lines (`limit`, le=1000).
MAX_LIMIT = 1000
DEFAULT_LIMIT = 400


class PrivateLogsSDK(BaseSDK):
    def query(  # noqa: PLR0913
        self,
        logql_query: str,
        resource: LogsResource,
        *,
        start: datetime,
        end: datetime,
        log_type: str = "application",
        limit: int = DEFAULT_LIMIT,
        newest_first: bool = True,
    ) -> List[LogLine]:
        """Lines of `resource` matching `logql_query` within [start, end].

        At most `limit` lines come back; `newest_first` reads from the end of the window
        backwards (the newest `limit` lines, newest first), else from the start forwards.
        """
        if log_type not in LOG_TYPES:
            raise ValueError(f"log_type must be one of {LOG_TYPES}, got {log_type!r}.")
        if not 1 <= limit <= MAX_LIMIT:
            raise ValueError(f"limit must be between 1 and {MAX_LIMIT}, got {limit}.")
        start_ns, end_ns = _epoch_ns(start), _epoch_ns(end)
        if end_ns <= start_ns:
            raise ValueError("end must be after start.")

        batch = self.client.query_logs(
            logql_query=logql_query,
            resource={_RESOURCE_PARAM[resource.resource_type]: resource.resource_id},
            start_ns=start_ns,
            end_ns=end_ns,
            source_type=log_type,
            limit=limit,
            reverse_sort=newest_first,
        )
        return [_to_line(item) for item in batch.items or []]


def _epoch_ns(value: datetime) -> int:
    # A naive datetime is taken as UTC, matching the CLI's time flags.
    aware = value if value.tzinfo else value.replace(tzinfo=timezone.utc)
    return int(aware.timestamp() * 1_000_000_000)


def _to_line(item: Any) -> LogLine:
    """A generated `LogItem` -> model.

    The backend's payload is the line parsed as JSON (or ``{"message": line}`` for plain
    text), merged with the stream's labels; `message` becomes the line's text and the
    rest its fields. A JSON line without a `message` key keeps its whole object as text,
    so nothing is lost.
    """
    fields: Dict[str, Any] = dict(item.payload or {})
    message = fields.pop("message", None)
    if message is None:
        message = json.dumps(fields, sort_keys=True)
    return LogLine(
        timestamp=datetime.fromtimestamp(item.timestamp_ns / 1_000_000_000, tz=timezone.utc),
        message=str(message),
        fields=fields,
    )
