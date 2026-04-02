from ratio.application.load_local_module import load_local_module
from ratio.router.route import Route
from ratio.router.route_path import RoutePath
from ratio.router.is_route import is_route
import pathlib
from typing import Type


def _map_discovered_route_to_route(
    path: pathlib.Path,
) -> Type[Route] | None:
    resolved_path = path.resolve()

    module = load_local_module("route", resolved_path)
    module_attributes = [getattr(module, item) for item in dir(module)]
    potential_routes = [
        attribute for attribute in module_attributes if is_route(attribute)
    ]

    if len(potential_routes) != 1:
        return None

    return potential_routes[0]


def discover_routes(
    application_root: pathlib.Path,
) -> dict[RoutePath, Type[Route]]:
    routes_directory = application_root / "routes"
    if not routes_directory.exists() or not routes_directory.is_dir():
        return {}

    potential_routes = {
        RoutePath.from_path(
            path.relative_to(routes_directory).with_suffix("")
        ): _map_discovered_route_to_route(path)
        for path in routes_directory.glob("**/*.py")
    }

    return {
        route_path: path
        for route_path, path in potential_routes.items()
        if path is not None
    }
