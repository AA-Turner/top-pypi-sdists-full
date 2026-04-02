from ratio.http.response import Response
from ratio.http.request import Request
from typing import Awaitable, Callable, TypeVar
from http import HTTPStatus

_T = TypeVar("_T")
RouteMethod = Callable[[_T, Request], Awaitable[Response]]
BoundRouteMethod = Callable[[Request], Awaitable[Response]]


class Route:
    async def get(self, _request: Request) -> Response:
        return Response.from_http_status(HTTPStatus.METHOD_NOT_ALLOWED)

    async def head(self, _request: Request) -> Response:
        return Response.from_http_status(HTTPStatus.METHOD_NOT_ALLOWED)

    async def patch(self, _request: Request) -> Response:
        return Response.from_http_status(HTTPStatus.METHOD_NOT_ALLOWED)

    async def post(self, _request: Request) -> Response:
        return Response.from_http_status(HTTPStatus.METHOD_NOT_ALLOWED)

    async def put(self, _request: Request) -> Response:
        return Response.from_http_status(HTTPStatus.METHOD_NOT_ALLOWED)

    async def delete(self, _request: Request) -> Response:
        return Response.from_http_status(HTTPStatus.METHOD_NOT_ALLOWED)

    async def trace(self, _request: Request) -> Response:
        return Response.from_http_status(HTTPStatus.METHOD_NOT_ALLOWED)

    async def options(self, _request: Request) -> Response:
        return Response.from_http_status(HTTPStatus.METHOD_NOT_ALLOWED)

    async def connect(self, _request: Request) -> Response:
        return Response.from_http_status(HTTPStatus.METHOD_NOT_ALLOWED)
