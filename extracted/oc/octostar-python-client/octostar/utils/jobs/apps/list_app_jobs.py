import os
import logging

_logger = logging.getLogger(__name__)

from ....api.apps import list_app_jobs
from ....client import Client
from ...exceptions import ApiConnectionError


def sync(app_id: str = os.getenv("OS_APP_ID"), client: Client = None):
    """
    # List App Children

    List the jobs spawned by a app.

    ## Arguments
    - `app_id`: The running app ID.
    - `client`: The Client with which to connect to Octostar. If None, the default one is used.

    ## Returns
    A list of jobs, each containing their full info. Note the full info does not contain the job URL,
    use `get_job_url()` to retrieve it.

    ## Raises
    - `ApiConnectionError`: If the request was unsuccessful on the server.
    """
    response = list_app_jobs.sync_detailed(app_id=app_id, client=client)
    if response.status_code != 200:
        raise ApiConnectionError("list_app_jobs", response, client)
    content = response.parsed
    content = list(filter(lambda x: x.name != app_id, content))
    for elem in content:
        elem.labels = elem.labels.additional_properties
    return content


async def asyncio(app_id: str = os.getenv("OS_APP_ID"), client: Client = None):
    """
    # List App Children Asynchronously

    List asynchronously the jobs spawned by a app.

    ## Arguments
    - `app_id`: The running app ID.
    - `client`: The Client with which to connect to Octostar. If None, the default one is used.

    ## Returns
    A list of jobs, each containing their full info. Note the full info does not contain the job URL,
    use `get_job_url()` to retrieve it.

    ## Raises
    - `ApiConnectionError`: If the request was unsuccessful on the server.
    """
    response = await list_app_jobs.asyncio_detailed(app_id=app_id, client=client)
    if response.status_code != 200:
        raise ApiConnectionError("list_app_jobs", response, client)
    content = response.parsed
    content = list(filter(lambda x: x.name != app_id, content))
    for elem in content:
        elem.labels = elem.labels.additional_properties
    return content
