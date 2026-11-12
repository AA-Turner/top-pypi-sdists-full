from datetime import datetime
from typing import List, Optional

from anyscale._private.anyscale_client import AnyscaleClientInterface
from anyscale._private.sdk import sdk_docs
from anyscale._private.sdk.base_sdk import Timer
from anyscale.cli_logger import BlockLogger
from anyscale.logs._private.logs_sdk import DEFAULT_LIMIT, DEFAULT_MAX_LINES, PrivateLogsSDK
from anyscale.logs.commands import (
    _DOWNLOAD_ARG_DOCSTRINGS,
    _DOWNLOAD_EXAMPLE,
    _LIST_FILES_ARG_DOCSTRINGS,
    _LIST_FILES_EXAMPLE,
    _QUERY_ARG_DOCSTRINGS,
    _QUERY_EXAMPLE,
    _READ_ARG_DOCSTRINGS,
    _READ_EXAMPLE,
    _READ_PAGE_ARG_DOCSTRINGS,
    _READ_PAGE_EXAMPLE,
    download as download,
    list_files as list_files,
    query as query,
    read as read,
    read_page as read_page,
)
from anyscale.logs.models import (
    LogFileLine,
    LogFilesFilter,
    LogFilesPage,
    LogLine,
    LogLinesPage,
    LogsResource,
)


class LogsSDK:
    def __init__(
        self,
        *,
        client: Optional[AnyscaleClientInterface] = None,
        logger: Optional[BlockLogger] = None,
        timer: Optional[Timer] = None,
    ):
        self._private_sdk = PrivateLogsSDK(client=client, logger=logger, timer=timer)

    @sdk_docs(
        doc_py_example=_QUERY_EXAMPLE,
        arg_docstrings=_QUERY_ARG_DOCSTRINGS,
    )
    def query(  # noqa: F811, PLR0913
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
        """Search the logs of a cluster, workspace, job or service with a LogQL query."""
        return self._private_sdk.query(
            logql_query,
            resource,
            start=start,
            end=end,
            log_type=log_type,
            limit=limit,
            newest_first=newest_first,
        )

    @sdk_docs(
        doc_py_example=_LIST_FILES_EXAMPLE,
        arg_docstrings=_LIST_FILES_ARG_DOCSTRINGS,
    )
    def list_files(self, files_filter: LogFilesFilter) -> LogFilesPage:  # noqa: F811
        """List the log files a job, service, workspace or cluster wrote to its cloud bucket."""
        return self._private_sdk.list_files(files_filter)

    @sdk_docs(
        doc_py_example=_DOWNLOAD_EXAMPLE,
        arg_docstrings=_DOWNLOAD_ARG_DOCSTRINGS,
    )
    def download(  # noqa: F811
        self,
        files_filter: LogFilesFilter,
        *,
        download_dir: Optional[str] = None,
        unpack: bool = True,
    ) -> str:
        """Download the log files of a job, service, workspace or cluster to a directory."""
        return self._private_sdk.download(files_filter, download_dir=download_dir, unpack=unpack)

    @sdk_docs(
        doc_py_example=_READ_EXAMPLE,
        arg_docstrings=_READ_ARG_DOCSTRINGS,
    )
    def read(  # noqa: F811
        self, files_filter: LogFilesFilter, *, max_lines: int = DEFAULT_MAX_LINES
    ) -> List[LogFileLine]:
        """Read lines from the log files of a job, service, workspace or cluster."""
        return self._private_sdk.read(files_filter, max_lines=max_lines)

    @sdk_docs(
        doc_py_example=_READ_PAGE_EXAMPLE,
        arg_docstrings=_READ_PAGE_ARG_DOCSTRINGS,
    )
    def read_page(  # noqa: F811
        self,
        files_filter: LogFilesFilter,
        *,
        max_lines: int = DEFAULT_MAX_LINES,
        page_token: Optional[str] = None,
    ) -> LogLinesPage:
        """Read one page of lines from the log files of a resource, and a next token."""
        return self._private_sdk.read_page(
            files_filter, max_lines=max_lines, page_token=page_token
        )
