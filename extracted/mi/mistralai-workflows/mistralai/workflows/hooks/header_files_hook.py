import httpx

from mistralai.workflows.core.auth.header_files import HeaderFiles


def refresh_header_files(request: httpx.Request, header_files: HeaderFiles) -> None:
    """Replace header-file values already on the request with the files' current content.

    Only headers the request already carries are touched, so the headers go exactly where the
    deployment headers were attached; this only keeps long-lived clients from sending a stale value.
    """
    if not any(name in request.headers for name in header_files.names):
        return
    for name, value in header_files.read().items():
        if name in request.headers:
            request.headers[name] = value


class _RefreshHeaderFilesHook:
    def __init__(self, header_files: HeaderFiles) -> None:
        self._header_files = header_files


class RefreshHeaderFilesHook(_RefreshHeaderFilesHook):
    """Sync httpx event hook running ``refresh_header_files`` on each request."""

    def __call__(self, request: httpx.Request) -> None:
        refresh_header_files(request, self._header_files)


class AsyncRefreshHeaderFilesHook(_RefreshHeaderFilesHook):
    """Async httpx event hook running ``refresh_header_files`` on each request."""

    async def __call__(self, request: httpx.Request) -> None:
        refresh_header_files(request, self._header_files)
