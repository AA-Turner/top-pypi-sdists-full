import os
import logging

_logger = logging.getLogger(__name__)

from ...api.apps import get_job_progress
from ...client import Client
from ..exceptions import ApiConnectionError


def _format_progress_response(content: dict) -> str:
    """Format the new API response as a progress string for backward compatibility.

    The new API returns: {job_id, progress (float 0-1), status, message}
    The old API returned: a string message with the progress.

    Returns the message if set, otherwise formats the progress as a percentage.
    """
    if content.get("message"):
        return content["message"]
    progress = content.get("progress")
    if progress is not None:
        return f"{int(progress * 100)}%"
    return content.get("status", "unknown")


def sync(job_id: str = os.getenv("OS_JOB_ID"), client: Client = None):
    """
    # Get Job Progress

    Get the progress status of a job. Note the progress status is determined by the job
    and its behavior is dependant on the implementation of the job itself.

    ## Arguments
    - `job_id`: The running job ID.
    - `client`: The Client with which to connect to Octostar. If None, the default one is used.

    ## Returns
    A string containing the progress status (usually containing some percentage value).

    ## Raises
    - `ApiConnectionError`: If the request was unsuccessful on the server.
    """
    response = get_job_progress.sync_detailed(job_id=job_id, client=client)
    if response.status_code != 200:
        raise ApiConnectionError("get_job_progress", response, client)
    content = response.parsed
    if not content:
        raise ApiConnectionError("get_job_progress", response, client)
    return _format_progress_response(content)


async def asyncio(job_id: str = os.getenv("OS_JOB_ID"), client: Client = None):
    """
    # Get Job Progress Asynchronously

    Get asynchronously the progress status of a job. Note the progress status is determined by the job
    and its behavior is dependant on the implementation of the job itself.

    ## Arguments
    - `job_id`: The running app/job ID.
    - `client`: The Client with which to connect to Octostar. If None, the default one is used.

    ## Returns
    A string containing the progress status (usually containing some percentage value).

    ## Raises
    - `ApiConnectionError`: If the request was unsuccessful on the server.
    """
    response = await get_job_progress.asyncio_detailed(job_id=job_id, client=client)
    if response.status_code != 200:
        raise ApiConnectionError("get_job_progress", response, client)
    content = response.parsed
    if not content:
        raise ApiConnectionError("get_job_progress", response, client)
    return _format_progress_response(content)
