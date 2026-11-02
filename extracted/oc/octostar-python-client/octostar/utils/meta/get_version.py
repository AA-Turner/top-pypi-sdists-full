import os

from ...api.metadata import get_version


def sync(client):
    """
    # Get the current Octostar version

    ## Arguments
    - `client`: The Client with which to connect to Octostar. If None, the default one is used.

    ## Returns
    The octostar version as a string.
    """
    return get_version.sync_detailed(client=client).parsed


async def asyncio(client):
    """
    # Get asynchronously the current Octostar version

    ## Arguments
    - `client`: The Client with which to connect to Octostar. If None, the default one is used.

    ## Returns
    A dictionary containing the username, its signed JWT and a few other info.
    """
    out = get_version.asyncio_detailed(client=client)
    return (await out).parsed
