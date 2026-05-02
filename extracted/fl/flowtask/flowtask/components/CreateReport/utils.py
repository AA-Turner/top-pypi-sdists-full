""" Utilities and Functions."""
from aiohttp import TCPConnector, ClientSession


async def get_json_data(url: str) -> dict:
    """Get a JSON data from a remote Source."""
    async with ClientSession(connector=TCPConnector(ssl=False)) as session:
        async with session.get(url=url) as response:
            return await response.json()
