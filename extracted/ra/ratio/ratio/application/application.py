from ratio.router.router import Router
from ratio.http.request import Request
from ratio.application.discover_routes import discover_routes
from asgiref.typing import (
    Scope,
    ASGIReceiveCallable,
    ASGISendCallable,
    HTTPResponseBodyEvent,
    HTTPResponseStartEvent,
)
import pathlib


class Ratio:
    application_root: pathlib.Path
    router: Router

    def __init__(self, root: pathlib.Path | None = None):
        self.application_root = root if root is not None else pathlib.Path.cwd()

        routes = discover_routes(self.application_root)
        self.router = Router(routes)

    async def __call__(
        self, scope: Scope, receive: ASGIReceiveCallable, send: ASGISendCallable
    ) -> None:
        if scope["type"] != "http":
            raise NotImplementedError

        # Temporarily use the receive variable here, to satisfy Ruff
        # TODO: remove this when we actually perform more ASGI logic, incorporating receive.
        _receive = receive

        request = Request.from_http_scope(scope)
        route = await self.router.resolve(request)
        response = await route()

        start: HTTPResponseStartEvent = {
            "type": "http.response.start",
            "status": response.code,
            "headers": response.headers.encode(),
            "trailers": False,
        }

        await send(start)

        body: HTTPResponseBodyEvent = {
            "type": "http.response.body",
            "body": str.encode(response.message),
            "more_body": False,
        }

        await send(body)
