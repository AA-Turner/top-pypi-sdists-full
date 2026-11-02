import logging
from typing import Union

_logger = logging.getLogger(__name__)

from ....api.apps import get_apps_url
from ....models.get_apps_url_json_body import GetAppsUrlJsonBody
from ....client import Client
from ...exceptions import ApiConnectionError


def sync(app_id: Union[str, list[str]], client: Client = None):
    """
    # Get App URL

    Get the app URL for a app ID.

    ## Arguments
    - `app_id`: The ID of the app. Can also be a list of such IDs.
    - `client`: The Client with which to connect to Octostar. If None, the default one is used.

    ## Returns
    One or a list of app urls.

    ## Raises
    - `ApiConnectionError`: If the request was unsuccessful on the server.
    """
    as_list = True
    if not isinstance(app_id, list):
        app_id = [app_id]
        as_list = False
    response = get_apps_url.sync_detailed(
        json_body=GetAppsUrlJsonBody(app_id), client=client
    )
    if response.status_code != 200:
        raise ApiConnectionError("get_apps_url", response, client)
    content = response.parsed
    content = [app.app_url for app in content]
    if not as_list:
        content = content[0]
    return content


async def asyncio(app_id: Union[str, list[str]], client: Client = None):
    """
    # Get App URL Asynchronously

    Get asynchronously the app URL for a app ID.

    ## Arguments
    - `app_id`: The ID of the app. Can also be a list of such IDs.
    - `client`: The Client with which to connect to Octostar. If None, the default one is used.

    ## Returns
    One or a list of app urls.

    ## Raises
    - `ApiConnectionError`: If the request was unsuccessful on the server.
    """
    as_list = True
    if not isinstance(app_id, list):
        app_id = [app_id]
        as_list = False
    response = await get_apps_url.asyncio_detailed(
        json_body=GetAppsUrlJsonBody(app_id), client=client
    )
    if response.status_code != 200:
        raise ApiConnectionError("get_apps_url", response, client)
    content = response.parsed
    content = [app.app_url for app in content]
    if not as_list:
        content = content[0]
    return content
