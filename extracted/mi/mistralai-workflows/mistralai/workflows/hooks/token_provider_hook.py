import httpx

from mistralai.workflows.core.auth.provider import TokenProvider


def _set_authorization(request: httpx.Request, provider: TokenProvider) -> None:
    request.headers["Authorization"] = f"Bearer {provider.get_token()}"


class TokenProviderHook:
    """Sync httpx event hook that sets the Authorization header from a TokenProvider on each request."""

    def __init__(self, provider: TokenProvider) -> None:
        self._provider = provider

    def __call__(self, request: httpx.Request) -> None:
        _set_authorization(request, self._provider)


class AsyncTokenProviderHook:
    """Async httpx event hook that sets the Authorization header from a TokenProvider on each request."""

    def __init__(self, provider: TokenProvider) -> None:
        self._provider = provider

    async def __call__(self, request: httpx.Request) -> None:
        _set_authorization(request, self._provider)
