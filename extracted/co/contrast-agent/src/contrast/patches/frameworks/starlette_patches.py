# Copyright © 2025 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import sys

from contrast_fireball import DiscoveredRoute
from contrast_vendor import wrapt

import contrast
from contrast.agent import scope
from contrast.agent.assess.policy.analysis import analyze
from contrast.agent.policy import registry
from contrast.agent.policy import patch_manager
from contrast.agent.middlewares.route_coverage import common
from contrast.utils.decorators import fail_quietly
from contrast.utils.patch_utils import (
    build_and_apply_patch,
    register_module_patcher,
    unregister_module_patcher,
    wrap_and_watermark,
)

from contrast_vendor import structlog as logging

logger = logging.getLogger("contrast")

DEFAULT_STARLETTE_ROUTE_METHODS = common.DEFAULT_ROUTE_METHODS + ("HEAD",)

STARLETTE_ROUTING = "starlette.routing"
STARLETTE_REQUESTS = "starlette.requests"
SESSION = "session"


def build___call___patch(orig_func, patch_policy):
    """
    Patch for starlette.routing.Router.__call__

    This currently gives us route discovery and route observation. If in the future we
    need a reference to the actual FastAPI / Starlette application object, we'll need
    another patch (probably for one of those class's __call__ methods).

    The innermost application object in any Starlette-based application is a Router.
    The router is a valid ASGI application object. We cannot patch
    starlette.applications.Starlette.__call__ (or fastapi.FastAPI.__call__) because of
    the order in which these methods are invoked during request processing. Starlette's
    unique middleware installation procedure leads to the following call order:

    fastapi.FastAPI.__call__
      starlette.applications.Starlette.__call__
        each middleware's __call__
          starlette.routing.Router.__call__

    This differs from typical middleware installation, where the middleware __call__
    methods come first.

    We need to perform route discovery / observation while we're still somewhere inside
    of the agent middleware's __call__ method; otherwise we won't have this information
    in time for handle_ensure() at the end of agent request processing. The best option
    seems to be Router.__call__.
    """
    del patch_policy

    async def __call___patch(wrapped, instance, args, kwargs):
        do_starlette_route_discovery(instance)
        try:
            result = await wrapped(*args, **kwargs)
        finally:
            do_starlette_route_observation(instance, *args, **kwargs)
        return result

    return wrap_and_watermark(orig_func, __call___patch)


@fail_quietly("Failed to run starlette first-request analysis")
@scope.contrast_scope()
def do_starlette_route_discovery(starlette_router_instance):
    from contrast.agent import agent_state

    if not agent_state.is_first_request():
        return

    common.handle_route_discovery(
        "starlette", create_starlette_routes, (starlette_router_instance,)
    )


def create_starlette_routes(starlette_router) -> set[DiscoveredRoute]:
    """
    Returns all the routes registered to a Starlette router.
    """
    from starlette.routing import Mount, Route

    routes = set()

    for app_route in starlette_router.routes:
        if isinstance(app_route, Mount):
            mnt_routes = create_starlette_routes(app_route)
            routes.update(mnt_routes)
        elif isinstance(app_route, Route):
            view_func = app_route.endpoint

            signature = common.build_signature(app_route.name, view_func)
            path_template = app_route.path
            methods = app_route.methods or DEFAULT_STARLETTE_ROUTE_METHODS

            for method_type in methods:
                routes.add(
                    DiscoveredRoute(
                        verb=method_type,
                        url=path_template,
                        signature=signature,
                        framework="Starlette",
                    )
                )
        # In the future we may need more cases for other BaseRoute types we don't
        # currently support, such as WebSocketRoute

    return routes


@fail_quietly("unable to perform starlette route observation")
@scope.contrast_scope()
def do_starlette_route_observation(
    starlette_router_instance, asgi_scope, *args, **kwargs
):
    from starlette.staticfiles import StaticFiles

    context = contrast.REQUEST_CONTEXT.get()
    if context is None:
        return

    logger.debug("Performing starlette route observation")

    if not asgi_scope or not isinstance(asgi_scope, dict):
        logger.debug(
            "unable to get ASGI scope for route observation. args: %s, kwargs: %s",
            args,
            kwargs,
        )
        return

    if route := asgi_scope.get("route"):
        context.signature = common.build_signature(route.name, route.endpoint)
        context.path_template = route.path
    elif (endpoint := asgi_scope.get("endpoint")) and isinstance(endpoint, StaticFiles):
        context.signature = f"StaticFiles(directory={endpoint.directory})"
    else:
        logger.debug("WARNING: did not find endpoint for starlette route observation")
        return

    logger.debug(
        "Found starlette route",
        signature=context.signature,
        path_template=context.path_template,
    )


class ContrastSessionDictProxy(wrapt.ObjectProxy):
    """
    Custom ObjectProxy we use to wrap dicts returned by starlette's request.session
    property. These proxied dicts have a trigger for trust-boundary-violation on
    __setitem__.
    """

    def __setitem__(self, key, value):
        result = None
        try:
            result = self.__wrapped__.__setitem__(key, value)
        finally:
            analyze_setitem(result, (self, key, value))

        return result


@fail_quietly("Failed to analyze session dict __setitem__")
def analyze_setitem(result, args):
    policy = registry.get_policy_by_name("starlette.sessions.dict.__setitem__")
    analyze(policy, result, args, {})


def build_session_patch(orig_prop, patch_policy):
    def session_fget(*args, **kwargs):
        """
        Function used to replace fget for starlette's request.session property.
        This function returns proxied dictionaries - see ContrastSessionDictProxy.
        """
        session_dict = orig_prop.fget(*args, **kwargs)

        context = contrast.REQUEST_CONTEXT.get()
        if context is None:
            return session_dict

        return ContrastSessionDictProxy(session_dict)

    return property(session_fget, orig_prop.fset, orig_prop.fdel)


def patch_starlette_requests(starlette_requests_module):
    build_and_apply_patch(
        starlette_requests_module.Request, SESSION, build_session_patch
    )


def patch_starlette_routing(starlette_routing_module):
    build_and_apply_patch(
        starlette_routing_module.Router, "__call__", build___call___patch
    )


def reverse_patches():
    unregister_module_patcher(STARLETTE_REQUESTS)
    starlette_routing_module = sys.modules.get(STARLETTE_ROUTING)
    if starlette_routing_module:
        patch_manager.reverse_patches_by_owner(starlette_routing_module.Router)

    unregister_module_patcher(STARLETTE_REQUESTS)
    starlette_requests_module = sys.modules.get(STARLETTE_REQUESTS)
    if starlette_requests_module:
        patch_manager.reverse_patches_by_owner(starlette_requests_module.Request)


def register_patches():
    register_module_patcher(patch_starlette_requests, STARLETTE_REQUESTS)
    register_module_patcher(patch_starlette_routing, STARLETTE_ROUTING)
