from collections.abc import Generator

import httpx


# https://www.python-httpx.org/advanced/authentication/#custom-authentication-schemes
class HeaderTokenAuth(httpx.Auth):
    def __init__(self, token: str) -> None:
        self.token = token

    def auth_flow(self, request: httpx.Request) -> Generator[httpx.Request, httpx.Response, None]:
        """Send the request, with a custom ``X-Authentication`` header."""
        request.headers['X-Authentication'] = self.token
        yield request


class ParamsTokenAuth(httpx.Auth):
    def __init__(self, token: str) -> None:
        self.token = token

    def auth_flow(self, request: httpx.Request) -> Generator[httpx.Request, httpx.Response, None]:
        """Send the request, with a custom ``token`` url parameter."""
        request.url = request.url.copy_merge_params({'token': self.token})
        yield request
