import os

from ...api.metadata import get_whoami


def sync(client):
    """
    # Get information about the user

    ## Arguments
    - `client`: The Client with which to connect to Octostar. If None, the default one is used.

    ## Returns
    A dictionary containing the username, its signed JWT and a few other info.
    """
    return get_whoami.sync_detailed(client=client).parsed


async def asyncio(client):
    """
    # Get asynchronously information about the user

    ## Arguments
    - `client`: The Client with which to connect to Octostar. If None, the default one is used.

    ## Returns
    A dictionary containing the username, its signed JWT and a few other info.
    """
    out = get_whoami.asyncio_detailed(client=client)
    return (await out).parsed
