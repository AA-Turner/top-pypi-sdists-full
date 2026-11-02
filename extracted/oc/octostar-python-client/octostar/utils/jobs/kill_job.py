import logging

_logger = logging.getLogger(__name__)

from ...api.apps import kill_job
from ...client import Client
from ..exceptions import ApiConnectionError


def sync(job_id: str, client: Client = None):
    """
    # Cancel a currently running job

    ## Arguments
    - `job_id`: The unique job ID to cancel.
    - `client`: The Client with which to connect to Octostar. If None, the default one is used.

    ## Returns
    An acknowledgment.

    ## Raises
    - `ApiConnectionError`: If the operation was unsuccessful on the server.
    """
    response = kill_job.sync_detailed(job_id=job_id, client=client)
    if response.status_code != 200:
        raise ApiConnectionError("kill_job", response, client)
    return response.parsed


async def asyncio(job_id: str, client: Client = None):
    """
    # Cancel asynchronously a currently running job

    ## Arguments
    - `job_id`: The job ID to cancel.
    - `client`: The Client with which to connect to Octostar. If None, the default one is used.

    ## Returns
    An acknowledgment.

    ## Raises
    - `ApiConnectionError`: If the operation was unsuccessful on the server.
    """
    response = await kill_job.asyncio_detailed(job_id=job_id, client=client)
    if response.status_code != 200:
        raise ApiConnectionError("kill_job", response, client)
    return response.parsed
