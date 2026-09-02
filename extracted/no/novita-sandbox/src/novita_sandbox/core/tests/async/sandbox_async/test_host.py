import asyncio

import httpx

from novita_sandbox.core import AsyncSandbox


async def test_ping_server(async_sandbox: AsyncSandbox, debug, helpers):
    cmd = await async_sandbox.commands.run(
        "python -m http.server 8000",
        background=True,
    )

    disable = helpers.catch_cmd_exit_error_in_background(cmd)

    try:
        host = async_sandbox.get_host(8000)

        status_code = None
        async with httpx.AsyncClient() as client:
            for _ in range(60):
                try:
                    res = await client.get(
                        f"{'http' if debug else 'https'}://{host}", timeout=5
                    )
                    status_code = res.status_code
                    if res.status_code == 200:
                        break
                except httpx.HTTPError:
                    pass
                await asyncio.sleep(1)
        assert status_code == 200
        disable()
    finally:
        await cmd.kill()
