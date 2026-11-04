from datetime import datetime
from typing import List, Optional

from anyscale._private.sdk import sdk_command
from anyscale.logs._private.logs_sdk import DEFAULT_LIMIT, PrivateLogsSDK
from anyscale.logs.models import LogLine, LogsResource


_LOGS_SDK_SINGLETON_KEY = "logs_sdk"

_QUERY_EXAMPLE = """
from datetime import datetime, timedelta, timezone

import anyscale
from anyscale.logs.models import LogsResource

end = datetime.now(timezone.utc)
lines = anyscale.logs.query(
    '{} |= "OOM"',
    LogsResource(resource_type="job", resource_id="prodjob_abc123"),
    start=end - timedelta(hours=1),
    end=end,
)
for line in lines:
    print(line.timestamp, line.message)
"""

_QUERY_ARG_DOCSTRINGS = {
    "logql_query": "The LogQL log query, e.g. '{} |= \"OOM\"'. The backend pins its stream "
    "selector to the resource, so a selector may not name another resource.",
    "resource": "The cluster, workspace, job or service whose logs to search.",
    "start": "Start of the window.",
    "end": "End of the window.",
    "log_type": "'application' (default) searches the workload's own output; 'system' "
    "searches Ray's own files (raylet, gcs, core_worker), kept at WARNING and above.",
    "limit": "Maximum number of lines to return, 1 to 1000. Default 400.",
    "newest_first": "True (default) returns the newest lines of the window, newest first; "
    "False the oldest lines, oldest first. To continue, move the window past the last "
    "line's timestamp.",
}


@sdk_command(
    _LOGS_SDK_SINGLETON_KEY,
    PrivateLogsSDK,
    doc_py_example=_QUERY_EXAMPLE,
    arg_docstrings=_QUERY_ARG_DOCSTRINGS,
    # Not published yet, like the CLI command and the Log Queries docgen module. The
    # visible Logs module shares the `anyscale.logs` prefix, and
    # test_exported_sdk_commands_are_documented_or_hidden requires every exported,
    # non-hidden SDK command there to be in its sdk_commands.
    hidden=True,
)
def query(  # noqa: PLR0913
    logql_query: str,
    resource: LogsResource,
    *,
    start: datetime,
    end: datetime,
    log_type: str = "application",
    limit: int = DEFAULT_LIMIT,
    newest_first: bool = True,
    _private_sdk: Optional[PrivateLogsSDK] = None,
) -> List[LogLine]:
    """Search the logs of a cluster, workspace, job or service with a LogQL query."""
    return _private_sdk.query(  # type: ignore
        logql_query,
        resource,
        start=start,
        end=end,
        log_type=log_type,
        limit=limit,
        newest_first=newest_first,
    )
