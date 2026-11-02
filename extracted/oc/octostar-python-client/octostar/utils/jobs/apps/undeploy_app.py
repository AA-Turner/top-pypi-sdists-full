import os
import logging

_logger = logging.getLogger(__name__)

from ....api.apps import undeploy_app
from ....client import Client
from ...exceptions import ApiConnectionError


def sync(
    app_id: str = os.getenv("OS_APP_ID"),
    client: Client = None,
):
    """
    # Undeploys an App.

    ## Arguments
    - `app_id`: The ID of the app to undeploy.
    - `client`: The Client with which to connect to Octostar. If None, the default one is used.

    ## Raises
    - `ApiConnectionError`: If the request was unsuccessful on the server.
    """
    response = undeploy_app.sync_detailed(app_id=app_id, client=client)
    if response.status_code not in (200, 202):
        raise ApiConnectionError("undeploy_app", response, client)
    return response.parsed


async def asyncio(
    app_id: str = os.getenv("OS_APP_ID"),
    client: Client = None,
):
    """
    # Undeploys an App.

    ## Arguments
    - `app_id`: The ID of the app to undeploy.
    - `client`: The Client with which to connect to Octostar. If None, the default one is used.

    ## Raises
    - `ApiConnectionError`: If the request was unsuccessful on the server.
    """
    response = await undeploy_app.asyncio_detailed(app_id=app_id, client=client)
    if response.status_code not in (200, 202):
        raise ApiConnectionError("undeploy_app", response, client)
    return response.parsed
