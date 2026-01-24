# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.

from contrast.agent.middlewares.route_coverage.common import (
    build_signature,
    get_normalized_uri,
)

from aiohttp.web_urldispatcher import DynamicResource
from contrast_fireball import DiscoveredRoute


def create_aiohttp_routes(app) -> set[DiscoveredRoute]:
    """
    Returns all the routes registered to a AioHttp app as a dict
    :param app: AioHttp app instance
    :return: dict {route_id:  api.Route}
    """
    routes = set()

    for app_route in app.router._resources:
        for resource in app_route._routes:
            signature = build_signature(resource.handler.__name__, resource.handler)
            _route_attr = (
                app_route._formatter
                if isinstance(app_route, DynamicResource)
                else app_route._path
            )
            routes.add(
                DiscoveredRoute(
                    verb=resource.method,
                    url=get_normalized_uri(_route_attr),
                    signature=signature,
                    framework="AIOHTTP",
                )
            )

    return routes
