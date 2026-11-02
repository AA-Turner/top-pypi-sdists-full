import logging

_logger = logging.getLogger(__name__)

from ...api.notifications import get_subscriptions
from ...client import Client
from ..exceptions import ApiConnectionError


def sync(client: Client = None):
    """
    # Get User Subscriptions

    Retrieves the subscriptions the user is listening to.

    ## Arguments
    - `client`: The Client with which to connect to Octostar. If None, the default one is used.

    ## Returns
    A list of subscription IDs.

    ## Raises
    - `ApiConnectionError`: If the request was unsuccessful on the server.
    """
    response = get_subscriptions.sync_detailed(client=client)
    if response.status_code != 200:
        raise ApiConnectionError("get_my_subscriptions", response, client)
    return response.parsed


async def asyncio(client: Client = None):
    """
    # Get User Subscriptions Asynchronously

    Asynchronously retrieves the subscriptions the user is listening to.

    ## Arguments
    - `client`: The Client with which to connect to Octostar. If None, the default one is used.

    ## Returns
    A list of subscription IDs.

    ## Raises
    - `ApiConnectionError`: If the request was unsuccessful on the server.
    """
    response = await get_subscriptions.asyncio_detailed(client=client)
    if response.status_code != 200:
        raise ApiConnectionError("get_my_subscriptions", response, client)
    return response.parsed
