from ratio.router.route import Route
from ratio.router.route_type import RouteType
from ratio.router.resolvers.resolver import ResolvedRoute
from ratio.router.resolvers.direct_resolver import DirectResolver
from ratio.router.resolvers.dynamic_resolver import DynamicResolver
from ratio.router.route_path import RoutePath
from ratio.http.request import Request
from typing import Type


class Router:
    __dynamic_resolver: DynamicResolver
    __direct_resolver: DirectResolver

    def __init__(self, routes: dict[RoutePath, Type[Route]]) -> None:
        self.__dynamic_resolver = DynamicResolver()
        self.__direct_resolver = DirectResolver()

        for path, route in routes.items():
            self.register_route(path, route)

    async def resolve(self, request: Request) -> ResolvedRoute:
        # First try direct route resolution
        if (route := self.__direct_resolver.resolve(request)) is not None:
            # Since this is an ABC, we know for sure these methods are implemented.
            # So there is no reason to take any additional precautions. It's fine to
            # throw an error when an HTTP method does not exist on the Route class.
            return route

        # Try dynamic resolution for this route
        if (dynamic_route := self.__dynamic_resolver.resolve(request)) is not None:
            return dynamic_route

        return self.__direct_resolver.not_found_route(request)

    def register_route(self, path: RoutePath, route: Type[Route]) -> None:
        # No dynamic parameters means that a path is considered direct
        if path.route_type == RouteType.DIRECT:
            return self.__direct_resolver.register(path, route)

        return self.__dynamic_resolver.register(path, route)
