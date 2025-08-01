# Copyright © 2025 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from __future__ import annotations
from contrast.utils.decorators import fail_quietly
from contrast.agent.middlewares.route_coverage.common import (
    DEFAULT_ROUTE_METHODS,
    build_signature,
)
from contrast_fireball import DiscoveredRoute
from pyramid.interfaces import IView, IViewClassifier, IRouteRequest, IRoutesMapper
from zope.interface import Interface

from contrast_vendor import structlog as logging

logger = logging.getLogger("contrast")


def get_iface_for_route(registry, pyramid_route):
    return registry.queryUtility(IRouteRequest, name=pyramid_route.name)


def _get_view_func(registry, pyramid_route):
    request_iface = get_iface_for_route(registry, pyramid_route)

    if request_iface is None:
        view_func = None
    else:
        view_func = registry.adapters.lookup(
            (IViewClassifier, request_iface, Interface), IView, name="", default=None
        )
    return view_func


def create_pyramid_routes(registry) -> set[DiscoveredRoute]:
    """
    Returns all the routes registered to a pyramid app registry
    """
    routes = set()
    mapper = registry.queryUtility(IRoutesMapper)

    if mapper is None:
        return routes

    for pyramid_route in mapper.get_routes():
        view_func = _get_view_func(registry, pyramid_route)

        if view_func is not None:
            signature = build_signature(pyramid_route.name, view_func)
            path_template = pyramid_route.path
            methods = pyramid_route.predicates or DEFAULT_ROUTE_METHODS
            for method_type in methods:
                routes.add(
                    DiscoveredRoute(
                        verb=method_type,
                        url=path_template,
                        signature=signature,
                        framework="Pyramid",
                    )
                )
        else:
            logger.debug("Unable to add %s to route discovery.", pyramid_route.path)

    return routes


@fail_quietly()
def get_signature_and_path_template(
    request_path, routes_list, registry
) -> tuple[str | None, str | None]:
    if not request_path:
        logger.debug("No path info for pyramid request")
        return None, None

    # Ideally we would like to call get_route but
    # there is no direct relationship between the wsgi
    # request path and the name of the route so we must
    # iterate over all the routes to find it by the path
    # pyramid_route = mapper.get_route(name)

    # TODO: PYT-3826 this is not a robust route matching strategy
    matching_routes = [x for x in routes_list if x.path == request_path]

    if not matching_routes:
        return None, None

    pyramid_route = matching_routes[0]
    if (view_func := _get_view_func(registry, pyramid_route)) is None:
        return None, None
    return build_signature(pyramid_route.name, view_func), pyramid_route.path
