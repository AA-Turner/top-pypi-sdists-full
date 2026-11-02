import os
import logging
import re

_logger = logging.getLogger(__name__)

from ...api.apps import get_job_logs
from ...client import Client
from ..exceptions import ApiConnectionError


def sync(
    job_id: str = os.getenv("OS_JOB_ID"),
    since_seconds: int = None,
    tail_lines: int = None,
    client: Client = None,
):
    """
    # Get Job Logs

    Retrieves the logs of a running job given its ID.

    ## Arguments
    - `job_id`: The running job ID.
    - `since_seconds`: The maximum amount of seconds prior to now to get logs for.
    - `tail_lines`: The maximum amount of log lines to retrieve.

    - `client`: The Client with which to connect to Octostar. If None, the default one is used.

    ## Returns
    An UTF-8 string with the job logs, or in bytes if they could not be decoded.

    ## Raises
    - `ApiConnectionError`: If the request was unsuccessful on the server.
    """
    response = get_job_logs.sync_detailed(
        job_id=job_id,
        since_seconds=since_seconds,
        tail_lines=tail_lines,
        client=client,
    )
    if response.status_code != 200:
        raise ApiConnectionError("get_job_logs", response, client)
    logs = response.content
    try:
        escaped_logs = logs.decode("utf-8", "replace")
        escaped_logs = re.sub(
            r"\\.",
            lambda x: {
                "\\n": "\n",
                "\\t": "\t",
                "\\r": "\r",
                '\\"': '"',
                "\\'": "'",
            }.get(x[0], x[0]),
            escaped_logs,
        )
        return escaped_logs
    except Exception:
        _logger.warning("Could not decode logs! Returning raw bytes")
        return logs


async def asyncio(
    job_id: str = os.getenv("OS_JOB_ID"),
    since_seconds: int = None,
    tail_lines: int = None,
    client: Client = None,
):
    """
    # Get Job Logs Asynchronously

    Asynchronously retrieves the logs of a running job given its ID.

    ## Arguments
    - `job_id`: The running job ID.
    - `since_seconds`: The maximum amount of seconds prior to now to get logs for.
    - `tail_lines`: The maximum amount of log lines to retrieve.

    - `client`: The Client with which to connect to Octostar. If None, the default one is used.

    ## Returns
    An UTF-8 string with the job logs, or in bytes if they could not be decoded.

    ## Raises
    - `ApiConnectionError`: If the request was unsuccessful on the server.
    """
    response = await get_job_logs.asyncio_detailed(
        job_id=job_id,
        since_seconds=since_seconds,
        tail_lines=tail_lines,
        client=client,
    )
    if response.status_code != 200:
        raise ApiConnectionError("get_job_logs", response, client)
    logs = response.content
    try:
        escaped_logs = logs.decode("utf-8", "replace")
        escaped_logs = re.sub(
            r"\\.",
            lambda x: {
                "\\n": "\n",
                "\\t": "\t",
                "\\r": "\r",
                '\\"': '"',
                "\\'": "'",
            }.get(x[0], x[0]),
            escaped_logs,
        )
        return escaped_logs
    except Exception:
        _logger.warning("Could not decode logs! Returning raw bytes")
        return logs
