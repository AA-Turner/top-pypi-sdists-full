import asyncio
import webbrowser

import aiohttp
import dask.config
import rich

from .exceptions import AuthenticationError
from .utils import COILED_SERVER, handle_credentials


def get_local_user() -> str:
    try:
        import getpass
        import socket

        local_user = f"{getpass.getuser()}@{socket.gethostname()}"
    except Exception:
        local_user = ""
    return local_user


async def make_unattached_token(server, label=None) -> dict:
    url = server + "/api/v1/api-tokens-no-user/"
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data={"label": label}) as resp:
            return await resp.json()


async def client_token_grant_flow(server, browser, workspace=None):
    server = server or dask.config.get("coiled.server", COILED_SERVER)

    token_data = await make_unattached_token(server, label=get_local_user())

    token_identifier = token_data["identifier"]
    token_secret = token_data["token"]

    url = f"{server}/activate-token?id={token_identifier}"

    if browser:
        webbrowser.open(url, new=2)

    rich.print(f"""
[bold]Visit the following page to authorize this computer:[/bold]

  [link][cyan]{url}[/cyan][/link]

[bold]Validation code:[/bold] {token_identifier}
""")

    retries = 60 * 10  # sleep(1) between tries means this goes for 10 minutes, plus a little
    while retries > 0:
        try:
            return await handle_credentials(
                server=server,
                token=token_secret,
                workspace=workspace,
                save=True,
                retry=False,
                print_invalid_token_messages=False,
            )
        except AuthenticationError:
            # still waiting for user to authorize the token
            retries -= 1
            await asyncio.sleep(1)
