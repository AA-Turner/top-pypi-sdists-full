from datetime import datetime
from typing import List, Optional

from anyscale._private.anyscale_client import AnyscaleClientInterface
from anyscale._private.sdk import sdk_docs
from anyscale._private.sdk.base_sdk import Timer
from anyscale.cli_logger import BlockLogger
from anyscale.logs._private.logs_sdk import DEFAULT_LIMIT, PrivateLogsSDK
from anyscale.logs.commands import (
    _QUERY_ARG_DOCSTRINGS,
    _QUERY_EXAMPLE,
    query as query,
)
from anyscale.logs.models import LogLine, LogsResource


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
