from ratio.http.response import Response
from ratio.router.resolvers.resolver import ResolvedRoute
from http import HTTPStatus


def _create_generic_route(status: HTTPStatus) -> ResolvedRoute:
    async def generic_route() -> Response:
        return Response.from_http_status(status)

    return generic_route


not_found: ResolvedRoute = _create_generic_route(HTTPStatus.NOT_FOUND)
internal_server_error: ResolvedRoute = _create_generic_route(
    HTTPStatus.INTERNAL_SERVER_ERROR
)
method_not_allowed: ResolvedRoute = _create_generic_route(HTTPStatus.METHOD_NOT_ALLOWED)
