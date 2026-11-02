import os
import logging

_logger = logging.getLogger(__name__)

from ...api.apps import set_job_progress
from ...client import Client
from ...models.progress_request import ProgressRequest
from ..exceptions import ApiConnectionError


def sync(
    progress_string: str, job_id: str = os.getenv("OS_JOB_ID"), client: Client = None
):
    """
    # Set Job Progress

    Set or update the progress status of a job.

    ## Arguments
    - `progress_string`: A string indicative of the progress status.
    - `job_id`: The running job ID.
    - `client`: The Client with which to connect to Octostar. If None, the default one is used.

    ## Returns
    `True` if progress update was successful.

    ## Raises
    - `ApiConnectionError`: If the request was unsuccessful on the server.
    """
    response = set_job_progress.sync_detailed(
        job_id=job_id,
        json_body=ProgressRequest(progress=progress_string),
        client=client,
    )
    if response.status_code != 200:
        raise ApiConnectionError("set_job_progress", response, client)
    return True


async def asyncio(
    progress_string: str, job_id: str = os.getenv("OS_JOB_ID"), client: Client = None
):
    """
    # Set Job Progress Asynchronously

    Set or update asynchronously the progress status of a job.

    ## Arguments
    - `progress_string`: A string indicative of the progress status.
    - `job_id`: The running job ID.
    - `client`: The Client with which to connect to Octostar. If None, the default one is used.

    ## Returns
    `True` if progress update was successful.

    ## Raises
    - `ApiConnectionError`: If the request was unsuccessful on the server.
    """
    response = await set_job_progress.asyncio_detailed(
        job_id=job_id,
        json_body=ProgressRequest(progress=progress_string),
        client=client,
    )
    if response.status_code != 200:
        raise ApiConnectionError("set_job_progress", response, client)
    return True
