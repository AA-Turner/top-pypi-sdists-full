from ssl import create_default_context
from typing import Optional

from aiohttp import ClientSession, TCPConnector, CookieJar
from certifi import where


def create_client_session(headers: Optional[dict] = None) -> ClientSession:
    ssl_context = create_default_context(cafile=where())
    return ClientSession(
        connector=TCPConnector(ssl=ssl_context), cookie_jar=CookieJar(quote_cookie=False), headers=headers
    )
