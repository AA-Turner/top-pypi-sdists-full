from ratio.router.route import BoundRouteMethod
from ratio.router.resolvers.resolver import ResolvedRoute
from ratio.http.response import Response
from ratio.http.request import Request


def wrap_bound_method(
    bound_method: BoundRouteMethod, request: Request
) -> ResolvedRoute:
    async def wrapped_method() -> Response:
        return await bound_method(request)

    return wrapped_method
