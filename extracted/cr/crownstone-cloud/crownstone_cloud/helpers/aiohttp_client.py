"""Functions to get or create an aiohttp clientsession."""
import ssl
from typing import Any

import aiohttp
import certifi


def create_clientsession(**kwargs: Any) -> aiohttp.ClientSession:
    """Create a new aiohttp clientsession."""
    connector = get_connector()

    clientsession = aiohttp.ClientSession(
        connector=connector,
        **kwargs,
    )

    return clientsession


def get_connector() -> aiohttp.BaseConnector:
    """Return the connector for aiohttp."""

    def client_context() -> ssl.SSLContext:
        """Return an SSL context for making requests."""
        context = ssl.create_default_context(
            purpose=ssl.Purpose.SERVER_AUTH, cafile=certifi.where()
        )
        return context

    connector = aiohttp.TCPConnector(enable_cleanup_closed=True, ssl=client_context())

    return connector
