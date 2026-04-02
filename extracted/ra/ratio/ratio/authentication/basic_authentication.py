from ratio.router.route import RouteMethod
from ratio.http.request import Request
from ratio.http.response import Response
from http import HTTPStatus
from typing import TypeVar, Callable, Any
import base64


# TODO: Add Self bound when Mypy supports it.
_T = TypeVar("_T")


def basic_authentication(
    *_args: Any, username: str, password: str, realm: str | None = None
) -> Callable[[RouteMethod], RouteMethod]:
    def decorator(method: RouteMethod) -> RouteMethod:
        async def wrapper(_self: _T, request: Request) -> Response:
            if (authorization_headers := request.headers.get("Authorization")) is None:
                response = Response.from_http_status(HTTPStatus.UNAUTHORIZED)

                header_value = (
                    f'Basic realm="{realm}"' if realm is not None else "Basic"
                )
                response.headers.put("WWW-Authenticate", {header_value})
                return response

            # We shouldn't have more than one authorization header
            if len(authorization_headers) != 1:
                return Response.from_http_status(HTTPStatus.UNAUTHORIZED)

            authorization_header = next(iter(authorization_headers))

            if _is_basic_auth(authorization_header) is False:
                return Response.from_http_status(HTTPStatus.UNAUTHORIZED)

            compare_credentials = base64.b64encode(
                f"{username}:{password}".encode("utf-8")
            ).decode("utf-8")

            if compare_credentials == authorization_header.replace("Basic ", ""):
                return await method(_self, request)

            return Response.from_http_status(HTTPStatus.UNAUTHORIZED)

        return wrapper

    return decorator


def _is_basic_auth(header_value: str) -> bool:
    return header_value.lower().startswith("basic ")
