from ratio.router.resolvers.resolver import RouteResolver, ResolvedRoute
from ratio.router.resolvers.generic_routes import not_found, method_not_allowed
from ratio.router.resolvers.util import wrap_bound_method
from ratio.router.exceptions import PathAlreadyExistsError
from ratio.router.route_path import RoutePath
from ratio.router.route import Route
from ratio.http.request import Request
from typing import Type


class DirectResolver(RouteResolver):
    def resolve(self, request: Request) -> ResolvedRoute | None:
        route = self._collection.get(request.url_path, None)

        if route is None:
            return None

        instantiated_route = route()
        bound_method = getattr(instantiated_route, request.method.lower(), None)
        if bound_method is None:
            return method_not_allowed

        return wrap_bound_method(bound_method, request)

    def register(self, route_path: RoutePath, route: Type[Route]) -> None:
        if (path := str(route_path)) in self._collection:
            raise PathAlreadyExistsError(path)

        self._collection[path] = route

    def not_found_route(self, request: Request) -> ResolvedRoute:
        route = self._collection.get("/404", None)

        if route is None:
            return not_found

        instantiated_route = route()
        bound_method = getattr(instantiated_route, request.method.lower(), None)

        if bound_method is None:
            return method_not_allowed

        return wrap_bound_method(bound_method, request)
