"""Handle proxying frontend requests from the backend server."""

from __future__ import annotations

import asyncio
from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator
from urllib.parse import urlparse

from reflex.config import get_config
from reflex.utils import console
from starlette.applications import Starlette
from starlette.routing import Mount
from starlette.types import ASGIApp, Receive, Scope, Send

from reflex_enterprise.utils import is_new_session

try:
    import aiohttp
    from asgiproxy.config import BaseURLProxyConfigMixin, ProxyConfig
    from asgiproxy.context import ProxyContext
    from asgiproxy.proxies.http import proxy_http
    from asgiproxy.simple_proxy import make_simple_proxy_app
except ImportError:
    if is_new_session():
        console.warn("asgiproxy is not installed. Proxying will be disabled.")

    @asynccontextmanager
    async def proxy_middleware(*args, **kwargs) -> AsyncGenerator[None, None]:
        """A no-op proxy middleware for when asgiproxy is not installed.

        Args:
            *args: The positional arguments.
            **kwargs: The keyword arguments.

        Yields:
            None
        """
        yield
else:
    MAX_PROXY_RETRY = 25

    async def proxy_http_with_retry(
        *,
        context: ProxyContext,
        scope: Scope,
        receive: Receive,
        send: Send,
    ) -> Any:
        """Proxy an HTTP request with retries.

        Args:
            context: The proxy context.
            scope: The request scope.
            receive: The receive channel.
            send: The send channel.

        Returns:
            The response from `proxy_http`.
        """
        for _attempt in range(MAX_PROXY_RETRY):
            try:
                return await proxy_http(
                    context=context,
                    scope=scope,
                    receive=receive,
                    send=send,
                )
            except aiohttp.ClientError as err:  # noqa: PERF203
                console.debug(
                    f"Retrying request {scope['path']} due to client error {err!r}."
                )
                await asyncio.sleep(0.3)
            except Exception as ex:
                console.debug(
                    f"Retrying request {scope['path']} due to unhandled exception {ex!r}."
                )
                await asyncio.sleep(0.3)

    def _get_proxy_app_with_context(frontend_host: str) -> tuple[ProxyContext, ASGIApp]:
        """Get the proxy app with the given frontend host.

        Args:
            frontend_host: The frontend host to proxy requests to.

        Returns:
            The proxy context and app.
        """

        class LocalProxyConfig(BaseURLProxyConfigMixin, ProxyConfig):
            upstream_base_url = frontend_host
            rewrite_host_header = urlparse(upstream_base_url).netloc

        proxy_context = ProxyContext(LocalProxyConfig())
        proxy_app = make_simple_proxy_app(
            proxy_context, proxy_http_handler=proxy_http_with_retry
        )
        return proxy_context, proxy_app

    def _get_base_starlette_app(app: ASGIApp) -> Starlette | None:
        """Get the base Starlette app from the given ASGI app.

        Args:
            app: The ASGI app.

        Returns:
            The base Starlette app.
        """
        if isinstance(app, Starlette):
            for route in app.routes:
                if (
                    isinstance(route, Mount)
                    and route.path in ["", "/"]
                    and (base_app := _get_base_starlette_app(route.app)) is not None
                ):
                    return base_app
            return app

    @asynccontextmanager
    async def proxy_middleware(  # pyright: ignore[reportRedeclaration]
        app: Starlette,
    ) -> AsyncGenerator[None, None]:
        """A middleware to proxy requests to the separate frontend server.
        The proxy is installed on the / endpoint of the Starlette instance.

        Args:
            app: The Starlette instance.

        Yields:
            None
        """
        # Find the bottom level app to mount the proxy on
        base_app = _get_base_starlette_app(app)
        if base_app is None:
            console.error(
                "Unable to find the base Starlette app. Proxying will not be enabled."
            )
            yield
            return

        config = get_config()
        backend_port = config.backend_port
        frontend_host = f"http://localhost:{config.frontend_port}"
        proxy_context, proxy_app = _get_proxy_app_with_context(frontend_host)
        base_app.mount("/", proxy_app)
        console.debug(
            f"Proxying '/' requests on port {backend_port} to {frontend_host}"
        )
        async with proxy_context:
            yield
