from collections.abc import Iterable

import httpx


def _parse_origin(origin: str | None) -> httpx.URL | None:
    if not origin:
        return None
    url = httpx.URL(origin)
    return url if url.host else None


def _same_origin(request_url: httpx.URL, trusted: httpx.URL) -> bool:
    return (
        request_url.scheme == trusted.scheme and request_url.host == trusted.host and request_url.port == trusted.port
    )


class _CrossOriginAuthGuard:
    """Drops credential headers when a request leaves the trusted origin.

    httpx strips Authorization on cross-origin redirects but copies every other header, and request
    event hooks re-run on every redirect hop, so a credential-setting hook would re-add its headers on
    the foreign host. This guard removes Authorization and the given credential headers whenever the
    request origin does not match the trusted server.

    MUST be registered as the LAST request hook so it runs after every token-setting hook; placed
    earlier, a later hook would re-add the header it just removed.
    """

    def __init__(self, trusted_origin: str | None, credential_headers: Iterable[str] = ()) -> None:
        self._trusted_origin = _parse_origin(trusted_origin)
        self._credential_headers = {"Authorization", *credential_headers}

    def _strip_if_cross_origin(self, request: httpx.Request) -> None:
        if self._trusted_origin is not None and not _same_origin(request.url, self._trusted_origin):
            for name in self._credential_headers:
                request.headers.pop(name, None)


class CrossOriginAuthGuardHook(_CrossOriginAuthGuard):
    """Sync guard hook. MUST be registered as the last request hook (see base class)."""

    def __call__(self, request: httpx.Request) -> None:
        self._strip_if_cross_origin(request)


class AsyncCrossOriginAuthGuardHook(_CrossOriginAuthGuard):
    """Async guard hook. MUST be registered as the last request hook (see base class)."""

    async def __call__(self, request: httpx.Request) -> None:
        self._strip_if_cross_origin(request)
