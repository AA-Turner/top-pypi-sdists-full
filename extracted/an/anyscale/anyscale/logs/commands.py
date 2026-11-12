from datetime import datetime
from typing import List, Optional

from anyscale._private.sdk import sdk_command
from anyscale.logs._private.logs_sdk import DEFAULT_LIMIT, DEFAULT_MAX_LINES, PrivateLogsSDK
from anyscale.logs.models import (
    LogFileLine,
    LogFilesFilter,
    LogFilesPage,
    LogLine,
    LogLinesPage,
    LogsResource,
)


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


_LIST_FILES_EXAMPLE = """
import anyscale
from anyscale.logs.models import LogFilesFilter

page = anyscale.logs.list_files(
    LogFilesFilter(entity_type="cluster", entity_id="ses_abc123", log_type="system"),
)
for chunk in page.chunks:
    print(chunk.node_ip, chunk.file_name, chunk.size)
"""

_LIST_FILES_ARG_DOCSTRINGS = {
    "files_filter": "Which resource to read log files for, and which of its files to keep.",
}

_DOWNLOAD_EXAMPLE = """
import anyscale
from anyscale.logs.models import LogFilesFilter

path = anyscale.logs.download(
    LogFilesFilter(entity_type="cluster", entity_id="ses_abc123", log_type="all"),
    download_dir="./logs",
)
print(f"Written under {path}")
"""

_DOWNLOAD_ARG_DOCSTRINGS = {
    "files_filter": "Which resource to read log files for, and which of its files to keep.",
    "download_dir": "Directory to write into. Defaults to the current working directory.",
    "unpack": "Split combined-worker.log into one file per worker after downloading. "
    "Default True.",
}

_READ_EXAMPLE = """
import anyscale
from anyscale.logs.models import LogFilesFilter

lines = anyscale.logs.read(
    LogFilesFilter(entity_type="job", entity_id="prodjob_abc123", latest=True),
    max_lines=200,
)
for line in lines:
    print(line.line)
"""

_READ_ARG_DOCSTRINGS = {
    "files_filter": "Which resource to read log files for, and which of its files to keep. "
    "With latest=True the newest chunks are read first and lines come newest first.",
    "max_lines": "Stop after this many lines. Default 1000.",
}

_READ_PAGE_EXAMPLE = """
import anyscale
from anyscale.logs.models import LogFilesFilter

files_filter = LogFilesFilter(entity_type="job", entity_id="prodjob_abc123", latest=True)
page = anyscale.logs.read_page(files_filter, max_lines=200)
for line in page.lines:
    print(line.line)
if page.next_page_token is not None:
    # The same filter, continued after the last line of the first page.
    page = anyscale.logs.read_page(files_filter, page_token=page.next_page_token)
"""

_READ_PAGE_ARG_DOCSTRINGS = {
    "files_filter": "Which resource to read log files for, and which of its files to keep. "
    "With latest=True the newest chunks are read first and lines come newest first.",
    "max_lines": "The page size in lines, at most 1000. Default 1000.",
    "page_token": "The next_page_token of an earlier page, used with the same filter. "
    "None starts at the first line.",
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


@sdk_command(
    _LOGS_SDK_SINGLETON_KEY,
    PrivateLogsSDK,
    doc_py_example=_LIST_FILES_EXAMPLE,
    arg_docstrings=_LIST_FILES_ARG_DOCSTRINGS,
    hidden=True,
)
def list_files(
    files_filter: LogFilesFilter, *, _private_sdk: Optional[PrivateLogsSDK] = None
) -> LogFilesPage:
    """List the log files a job, service, workspace or cluster wrote to its cloud bucket."""
    return _private_sdk.list_files(files_filter)  # type: ignore


@sdk_command(
    _LOGS_SDK_SINGLETON_KEY,
    PrivateLogsSDK,
    doc_py_example=_DOWNLOAD_EXAMPLE,
    arg_docstrings=_DOWNLOAD_ARG_DOCSTRINGS,
    hidden=True,
)
def download(
    files_filter: LogFilesFilter,
    *,
    download_dir: Optional[str] = None,
    unpack: bool = True,
    _private_sdk: Optional[PrivateLogsSDK] = None,
) -> str:
    """Download the log files of a job, service, workspace or cluster to a directory."""
    return _private_sdk.download(  # type: ignore
        files_filter, download_dir=download_dir, unpack=unpack
    )


@sdk_command(
    _LOGS_SDK_SINGLETON_KEY,
    PrivateLogsSDK,
    doc_py_example=_READ_EXAMPLE,
    arg_docstrings=_READ_ARG_DOCSTRINGS,
    hidden=True,
)
def read(
    files_filter: LogFilesFilter,
    *,
    max_lines: int = DEFAULT_MAX_LINES,
    _private_sdk: Optional[PrivateLogsSDK] = None,
) -> List[LogFileLine]:
    """Read lines from the log files of a job, service, workspace or cluster."""
    return _private_sdk.read(files_filter, max_lines=max_lines)  # type: ignore


@sdk_command(
    _LOGS_SDK_SINGLETON_KEY,
    PrivateLogsSDK,
    doc_py_example=_READ_PAGE_EXAMPLE,
    arg_docstrings=_READ_PAGE_ARG_DOCSTRINGS,
    hidden=True,
)
def read_page(
    files_filter: LogFilesFilter,
    *,
    max_lines: int = DEFAULT_MAX_LINES,
    page_token: Optional[str] = None,
    _private_sdk: Optional[PrivateLogsSDK] = None,
) -> LogLinesPage:
    """Read one page of lines from the log files of a resource, and a next token."""
    return _private_sdk.read_page(  # type: ignore
        files_filter, max_lines=max_lines, page_token=page_token
    )
