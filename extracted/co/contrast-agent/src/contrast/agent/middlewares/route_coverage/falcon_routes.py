# Copyright © 2025 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import copy
from contrast.utils.decorators import fail_quietly

from contrast.agent.middlewares.route_coverage.common import (
    DEFAULT_ROUTE_METHODS,
    build_args_from_function,
    get_normalized_uri,
)
from contrast_fireball import DiscoveredRoute

DEFAULT_ROUTE_METHODS = copy.copy(DEFAULT_ROUTE_METHODS) + ("PUT", "PATCH", "DELETE")


def create_falcon_routes(app) -> set[DiscoveredRoute]:
    """
    Given a Falcon app instance, use the private router
    to find all register routes. At this time, Falcon
    does not have a public API to get the app's routes.

    Borrowed from: https://stackoverflow.com/a/54510794

    :param app: class falcon.API or class falcon.APP instance
    """
    routes = set()

    def get_routes_from_children(node):
        if len(node.children):
            for child_node in node.children:
                get_routes_from_children(child_node)
        else:
            routes.update(create_routes(node.resource, node.uri_template))

    for node in app._router._roots:
        get_routes_from_children(node)

    return routes


def create_routes(endpoint_cls, path: str) -> set[DiscoveredRoute]:
    """
    Add to routes new items representing view functions for
    falcon class endpoint.
    """
    return set(
        DiscoveredRoute(
            verb=method,
            url=get_normalized_uri(str(path)),
            signature=_build_signature(view_func, endpoint_cls),
            framework="Falcon",
        )
        for method in DEFAULT_ROUTE_METHODS
        if (view_func := _get_view_method(endpoint_cls, method))
    )


def _get_view_method(cls_instance, request_method):
    """
    Falcon defines views like this
    ```
    class Cmdi(object):
        def on_get(self, request, response):
            response.status = falcon.HTTP_200
            response.body = "Result from CMDI"
    ```
    Given this class definition and the request_method string,
    we will look for the correct view method.

    Note that we need to get the unbound method because later on we
    will get the id of this method.

    :param cls_instance: instance of Falcon class endpoint such as Cmdi in the above example
    :param request_method: string such as GET or POST
    :return: function: view method for the request_method, such as on_get for example above
    """
    view_name = f"on_{request_method.lower()}"
    if hasattr(cls_instance, view_name):
        # use .__class__ and/or __func__ to get the unbound method
        view_func = getattr(cls_instance.__class__, view_name)

        return view_func

    return None


def _build_signature(view_func, endpoint_cls):
    view_func_args = build_args_from_function(view_func)
    return f"{endpoint_cls.__class__.__name__}.{view_func.__name__}{view_func_args}"


@fail_quietly()
def get_falcon_signature_and_template(request_path, falcon_app, request_method):
    if not request_path:
        return None, None

    route_info = falcon_app._router.find(request_path)
    if not route_info:
        return None, None

    endpoint_cls, _, _, path_template = route_info
    view_func = _get_view_method(endpoint_cls, request_method)
    return _build_signature(view_func, endpoint_cls), path_template
