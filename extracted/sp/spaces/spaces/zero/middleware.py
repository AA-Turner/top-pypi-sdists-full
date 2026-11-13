"""
"""

import asyncio.threads
from typing import Any
from typing import Awaitable
from typing import Callable
from typing import Iterable
from typing import MutableMapping
from typing import cast

from .._vendor.asgiref.typing import ASGI3Application
from .._vendor.asgiref.typing import ASGIReceiveCallable
from .._vendor.asgiref.typing import ASGIReceiveEvent
from .._vendor.asgiref.typing import ASGISendCallable
from .._vendor.asgiref.typing import Scope as ASGIScope

from . import context
from .context import ConnectionState
from .context import ZeroGPUContext
from .lifecycle import zerogpu_mode_enabled
from .lifecycle import zerogpu_startup


Scope = MutableMapping[str, Any]
Message = MutableMapping[str, Any]
Receive = Callable[[], Awaitable[Message]]
Send = Callable[[Message], Awaitable[None]]
ASGIApp = Callable[[Scope, Receive, Send], Awaitable[None]]


class ZeroGPUMiddleware:

    def __init__(self, app: ASGIApp, *, skip_zerogpu_startup: bool = False):
        self.app = app
        self.skip_zerogpu_startup = skip_zerogpu_startup

    async def __call__(self, scope: Scope, receive: Receive, send: Send):

        asgi_app = cast(ASGI3Application, self.app)
        asgi_scope = cast(ASGIScope, scope)
        asgi_receive = cast(ASGIReceiveCallable, receive)
        asgi_send = cast(ASGISendCallable, send)

        if not zerogpu_mode_enabled():
            await asgi_app(asgi_scope, asgi_receive, asgi_send)
            return

        if asgi_scope['type'] == 'lifespan':
            async def wrapped_receive() -> ASGIReceiveEvent:
                message = await asgi_receive()
                if message['type'] == 'lifespan.startup' and not self.skip_zerogpu_startup:
                    await asyncio.threads.to_thread(zerogpu_startup)
                return message
            await asgi_app(asgi_scope, wrapped_receive, asgi_send)
            return # pragma: no cover

        connection_state = ConnectionState()

        async def wrapped_receive() -> ASGIReceiveEvent:
            message = await asgi_receive()
            if (False
                or message['type'] == 'http.disconnect'
                or message['type'] == 'websocket.disconnect'
            ):
                connection_state.alive = False
            return message

        with context.set_context_var(ZeroGPUContext(
            connection_state=connection_state,
            server_ports=get_server_ports(asgi_scope),
            headers=_decode_headers(asgi_scope.get('headers', [])),
        )):
            await asgi_app(asgi_scope, wrapped_receive, asgi_send)


def get_server_ports(scope: ASGIScope):
    match scope.get('server'):
        case (_, int() as port):
            return {port}
        case _: # pragma: no cover
            return set()


def _decode_headers(headers: Iterable[tuple[bytes, bytes]]):
    return {
        key.decode('latin-1').lower(): value.decode('latin-1')
        for key, value in headers
    }
