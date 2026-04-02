from ratio.router.resolvers.resolver import RouteResolver, ResolvedRoute
from ratio.router.exceptions import PathAlreadyExistsError
from ratio.router.resolvers.util import wrap_bound_method
from ratio.router.resolvers.generic_routes import method_not_allowed
from ratio.router.route_path import RoutePath
from ratio.router.route import Route
from ratio.util.remove_none import remove_none
from ratio.http.request import Request
from typing import Type
import re
import copy


class DynamicResolver(RouteResolver):
    _collection: dict[str, Type[Route]]
    __registered_regex_formats: list[str]

    def __init__(self) -> None:
        super(DynamicResolver, self).__init__()
        self.__registered_regex_formats = []

    def resolve(self, request: Request) -> ResolvedRoute | None:
        matches = remove_none(
            map(
                lambda regex: re.fullmatch(regex, request.url_path),
                self._collection.keys(),
            ),
        )

        if len(matches) == 0:
            return None

        if len(matches) > 1:
            matches.sort(key=lambda item: str(item.re.pattern))

        matched_route = matches[0]
        matched_regex = str(matched_route.re.pattern)
        route = self._collection[matched_regex]

        instantiated_route = route()
        bound_method = getattr(instantiated_route, request.method.lower(), None)
        if bound_method is None:
            return method_not_allowed

        # We need to make a copy of the request, so we can set the path parameters.
        new_request = copy.deepcopy(request)
        new_request.path_parameters = matched_route.groupdict()
        return wrap_bound_method(bound_method, new_request)

    def register(self, route_path: RoutePath, route: Type[Route]) -> None:
        simplified_regex = route_path.as_simple_regex()

        if simplified_regex in self.__registered_regex_formats:
            raise PathAlreadyExistsError(str(route_path), simplified_regex)

        regex = route_path.as_regex()

        # To avoid we have to do this again, we save by regex, without the group ID:
        self.__registered_regex_formats.append(simplified_regex)
        self._collection[regex] = route
