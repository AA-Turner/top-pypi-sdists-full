from __future__ import annotations

import asyncio
import socket
import structlog
from dataclasses import dataclass

from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.routing import Route
from uvicorn import Config, Server

import anyio

import os

logger = structlog.get_logger(__name__)


def load_html_template(text1: str, text2: str) -> str:
    """
    Load the index.html template and replace placeholders.

    Args:
        text1: Text to replace #TEXT1# with
        text2: Text to replace #TEXT2# with

    Returns:
        The processed HTML string
    """
    # Get the directory where this script is located
    current_dir = os.path.dirname(os.path.abspath(__file__))
    html_path = os.path.join(current_dir, "index.html")

    with open(html_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    # Replace placeholders
    html_content = html_content.replace("#TEXT1#", text1)
    html_content = html_content.replace("#TEXT2#", text2)

    return html_content


@dataclass
class CallbackResponse:
    code: str | None = None
    state: str | None = None
    error: str | None = None
    error_description: str | None = None

    @classmethod
    def from_dict(cls, data: dict[str, str]) -> CallbackResponse:
        return cls(**{k: v for k, v in data.items() if k in cls.__annotations__})

    def to_dict(self) -> dict[str, str]:
        return {k: v for k, v in self.__dict__.items() if v is not None}


class OAuthCallbackServer(Server):
    async def startup(self, sockets: list[socket.socket] | None = None) -> None:
        # create_server() yields after installing its reader, before Uvicorn
        # records the listener. Defer caller cancellation across that handoff.
        with anyio.fail_after(2, shield=True):
            await super().startup(sockets=sockets)


async def serve_oauth_callback_server(server: Server, listener: socket.socket) -> None:
    """Release callback listeners and request tasks even when serving is cancelled.

    This boundary requires asyncio: Uvicorn owns asyncio request tasks and the
    callback resolves an asyncio Future. AnyIO provides structured lifecycle and
    shielded deadlines; asyncio.wait and direct cancellation operate on those
    Uvicorn-owned tasks.
    """
    try:
        await server.serve(sockets=[listener])
    finally:
        # Uvicorn's serve() does not run shutdown() when it is cancelled.
        # Shield teardown from the caller, but bound response draining.
        try:
            with anyio.move_on_after(2, shield=True):
                if hasattr(server, "servers"):
                    await server.shutdown(sockets=[listener])
        finally:
            for bound_server in getattr(server, "servers", ()):
                bound_server.close()
            listener.close()
            for connection in list(server.server_state.connections):
                connection.transport.abort()
            tasks = list(server.server_state.tasks)
            for task in tasks:
                task.cancel()
            if tasks:
                with anyio.CancelScope(shield=True):
                    done, _ = await asyncio.wait(tasks, timeout=1)
                for task in done:
                    if not task.cancelled():
                        task.exception()


def create_oauth_callback_server(
    port: int,
    callback_path: str = "/callback",
    server_url: str | None = None,
    response_future: asyncio.Future | None = None,
) -> Server:
    """
    Create an OAuth callback server.

    Args:
        port: The port to run the server on
        callback_path: The path to listen for OAuth redirects on
        server_url: Optional server URL to display in success messages
        response_future: Optional future to resolve when OAuth callback is received

    Returns:
        Configured uvicorn Server instance (not yet running)
    """

    async def callback_handler(request: Request):
        """Handle OAuth callback requests with proper HTML responses."""
        query_params = dict(request.query_params)
        callback_response = CallbackResponse.from_dict(query_params)

        if callback_response.error:
            error_desc = callback_response.error_description or "Unknown error"

            # Resolve future with exception if provided
            if response_future and not response_future.done():
                response_future.set_exception(
                    RuntimeError(
                        f"OAuth error: {callback_response.error} - {error_desc}"
                    )
                )

            return HTMLResponse(
                load_html_template(
                    text1="Runlayer OAuth Error",
                    text2=f"{callback_response.error}<br>{error_desc}",
                ),
                status_code=400,
            )

        if not callback_response.code:
            # Resolve future with exception if provided
            if response_future and not response_future.done():
                response_future.set_exception(
                    RuntimeError("OAuth callback missing authorization code")
                )

            return HTMLResponse(
                load_html_template(
                    text1="Runlayer OAuth Error",
                    text2="No authorization code received",
                ),
                status_code=400,
            )

        # Check for missing state parameter (indicates OAuth flow issue)
        if callback_response.state is None:
            # Resolve future with exception if provided
            if response_future and not response_future.done():
                response_future.set_exception(
                    RuntimeError(
                        "OAuth server did not return state parameter - authentication failed"
                    )
                )

            return HTMLResponse(
                load_html_template(
                    text1="Runlayer OAuth Error",
                    text2="Authentication failed<br>The OAuth server did not return the expected state parameter",
                ),
                status_code=400,
            )

        # Success case
        if response_future and not response_future.done():
            response_future.set_result(
                (callback_response.code, callback_response.state)
            )

        return HTMLResponse(
            load_html_template(
                text1="Runlayer OAuth login complete!",
                text2="You can close this window and return to the terminal.",
            )
        )

    app = Starlette(routes=[Route(callback_path, callback_handler)])

    return OAuthCallbackServer(
        Config(
            app=app,
            host="127.0.0.1",
            port=port,
            lifespan="off",
            log_level="warning",
            timeout_graceful_shutdown=1,
        )
    )
