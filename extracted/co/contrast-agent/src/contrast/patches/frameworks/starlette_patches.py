# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from __future__ import annotations

import inspect
import sys
from collections.abc import Iterable
from contextvars import ContextVar
from copy import copy
from typing import TYPE_CHECKING, Callable

from contrast_fireball import DiscoveredRoute

import contrast
from contrast.agent import scope
from contrast.agent.assess.policy.analysis import analyze
from contrast.agent.assess.policy.source_policy import cs__apply_source
from contrast.agent.middlewares.route_coverage import common
from contrast.agent.policy import patch_manager, registry
from contrast.utils.decorators import fail_quietly
from contrast.utils.patch_utils import (
    build_and_apply_patch,
    register_module_patcher,
    unregister_module_patcher,
    wrap_and_watermark,
)
from contrast_vendor import wrapt

if TYPE_CHECKING:
    from starlette.routing import Route, Router
    from starlette.types import ASGIApp

from contrast_vendor import structlog as logging

logger = logging.getLogger("contrast")

DEFAULT_STARLETTE_ROUTE_METHODS = common.DEFAULT_ROUTE_METHODS + ("HEAD",)

STARLETTE_ROUTING = "starlette.routing"
STARLETTE_REQUESTS = "starlette.requests"


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

    context = ContextVar("starlette_router_call_context", default=False)

    async def __call___patch(wrapped, instance, args, kwargs):
        if context.get():
            # Avoid reporting route coverage from inner Routers,
            # possible from mounting sub-applications.
            return await wrapped(*args, **kwargs)
        token = context.set(True)
        # PERF: avoid extra try/finally while manipulating context var.
        # We want to do this because this patch is hit on every request.
        # We can safely do this because route discovery and observation
        # functions are already protected with fail_quietly. There's also
        # a unit test to ensure this.
        do_starlette_route_discovery(instance)
        try:
            result = await wrapped(*args, **kwargs)
        finally:
            do_starlette_route_observation(instance, *args, **kwargs)
            context.reset(token)
        return result

    return wrap_and_watermark(orig_func, __call___patch)


@fail_quietly("Failed to run starlette first-request analysis")
@scope.contrast_scope()
def do_starlette_route_discovery(starlette_router_instance: Router):
    from contrast.agent import agent_state

    if not agent_state.is_first_request():
        return

    common.handle_route_discovery(
        "starlette", create_starlette_routes, (starlette_router_instance,)
    )


def _generic_asgi_signature(asgi_app: Callable) -> str:
    view_name = asgi_app.__module__
    if not inspect.isfunction(asgi_app):
        view_name += f".{asgi_app.__class__.__qualname__}"
    else:
        view_name += f".{asgi_app.__qualname__}"

    signature = common.build_signature(view_name, asgi_app)
    return signature


def create_starlette_routes(asgi_app: ASGIApp, prefix="") -> set[DiscoveredRoute]:
    """
    Returns all the routes registered to a Starlette router.
    """
    from starlette.routing import Host, Mount, Route, Router, WebSocketRoute
    from starlette.staticfiles import StaticFiles

    if isinstance(asgi_app, Router):
        routes = set()
        for app_route in asgi_app.routes:
            routes.update(create_starlette_routes(app_route, prefix=prefix))
        return routes

    if isinstance(asgi_app, Route):
        app_route = asgi_app
        view_func = app_route.endpoint

        signature = common.build_signature(app_route.name, view_func)
        path_template = app_route.path
        methods = starlette_route_methods(app_route)
        if methods is None:
            # If methods is None, it means all methods are allowed.
            # The backend considers a missing method to mean "any method",
            methods = [None]

        return {
            DiscoveredRoute(
                verb=method_type,
                url=prefix + path_template,
                signature=signature,
                framework="Starlette",
            )
            for method_type in methods
        }

    if isinstance(asgi_app, StaticFiles):
        # StaticFiles aren't registered as routes on the Router, but we still
        # want to report them. They return 405 for non-GET/HEAD requests.
        return {
            DiscoveredRoute(
                verb="GET",
                url=prefix + "/{path:path}",
                signature=f"StaticFiles(directory={asgi_app.directory})",
                framework="Starlette",
            ),
            DiscoveredRoute(
                verb="HEAD",
                url=prefix + "/{path:path}",
                signature=f"StaticFiles(directory={asgi_app.directory})",
                framework="Starlette",
            ),
        }

    if isinstance(asgi_app, Mount):
        return create_starlette_routes(asgi_app.app, prefix=prefix + asgi_app.path)
    if isinstance(asgi_app, Host):
        return create_starlette_routes(asgi_app.app, prefix=prefix)

    if isinstance(asgi_app, WebSocketRoute):
        # We don't support instrumenting WebSockets, so we don't report them.
        return set()

    # Fallback for any other ASGI app.

    signature = _generic_asgi_signature(asgi_app)
    return {
        DiscoveredRoute(
            verb=None,  # We don't know the allowed methods here, so fail open.
            url=prefix + "/{path:path}",
            signature=signature,
            framework="Starlette",
        )
    }


def starlette_route_methods(route: Route) -> Iterable[str] | None:
    """
    Returns the allowed HTTP methods for a given Starlette Route.
    If the route allows all methods, returns None.
    """
    from starlette.endpoints import HTTPEndpoint

    methods = route.methods
    if inspect.isclass(route.endpoint) and issubclass(route.endpoint, HTTPEndpoint):
        # Starlette is very permissive about HTTP method routing. If the HTTP method
        # (a.k.a. verb) matches a method on the endpoint class, that method will be
        # called. If not, the endpoint's method_not_allowed() method will be called.
        # This means that internal methods like _some_helper could be called if a
        # request was sent with HTTP method "_SOME_HELPER". In most cases, reporting
        # this would be noise to the user because these methods might have different
        # calling conventions (e.g. not accepting a request parameter or requiring
        # other parameters), and sending a request with a non-standard HTTP method
        # will result in a 500 Internal Server Error from unhandled TypeErrors.
        # To avoid this noise, we only report methods that are explicitly defined on
        # the endpoint class with the signature suggested in the Starlette docs:
        #     https://starlette.dev/endpoints/#httpendpoint
        allowed_methods = [
            name.upper()
            for (name, member) in inspect.getmembers(
                route.endpoint,
                predicate=(inspect.isfunction),
            )
            if name != "method_not_allowed"
            and (
                list(inspect.signature(member).parameters.keys()) == ["self", "request"]
            )
        ]
        if methods is None:
            methods = allowed_methods
        else:
            methods.intersection_update(allowed_methods)
    return methods


@fail_quietly("unable to perform starlette route observation")
@scope.contrast_scope()
def do_starlette_route_observation(
    starlette_router_instance, asgi_scope, *args, **kwargs
):
    from starlette.endpoints import HTTPEndpoint
    from starlette.routing import Host, Match, Mount
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
        # This is the common FastAPI case. Starlette won't set the route key.
        context.signature = common.build_signature(route.name, route.endpoint)
        context.path_template = route.path

    elif endpoint := asgi_scope.get("endpoint"):
        if router := asgi_scope.get("router"):
            asgi_scope = copy(asgi_scope)
            if "root_path" in asgi_scope:
                del asgi_scope["root_path"]

            def _get_route_name(scope, routes, route_name=None):
                for route in routes:
                    match, child_scope = route.matches(scope)
                    if match == Match.FULL:
                        route_name = getattr(route, "path", "")
                        child_scope = {**scope, **child_scope}
                        if isinstance(route, (Host, Mount)) and route.routes:
                            child_route_name = _get_route_name(
                                child_scope, route.routes, route_name
                            )
                            if child_route_name is None:
                                route_name = None
                            else:
                                route_name += child_route_name
                        return route_name

            context.path_template = _get_route_name(asgi_scope, router.routes)

        if isinstance(endpoint, StaticFiles):
            context.signature = f"StaticFiles(directory={endpoint.directory})"
        elif inspect.isclass(endpoint) and issubclass(endpoint, HTTPEndpoint):
            context.signature = common.build_signature(endpoint.__name__, endpoint)
        elif callable(endpoint):
            if func_name := getattr(endpoint, "__name__", None):
                context.signature = common.build_signature(func_name, endpoint)
            else:
                context.signature = _generic_asgi_signature(endpoint)
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


safe_cs__apply_source = fail_quietly()(cs__apply_source)


def build_stream_patch(orig_func, patch_policy):
    assert len(patch_policy.source_nodes) == 1
    source_node = patch_policy.source_nodes[0]

    async def stream_patch(wrapped, instance, args, kwargs):
        """
        Make starlette.requests.Request.stream a source. Policy patches are not equipped
        to handle generator functions, so we're using a custom monkeypatch here.

        Conveniently, the original generator does not have a return value (it only
        yields) and does not expect any values from `send()` / `asend()`, which
        simplifies this implementation significantly.
        """
        if not ((context := contrast.REQUEST_CONTEXT.get()) and context.assess_enabled):
            async for item in wrapped(*args, **kwargs):
                yield item
            return

        async for item in wrapped(*args, **kwargs):
            safe_cs__apply_source(
                context,
                source_node,
                item,
                instance,
                item,
                args,
                kwargs,
            )
            yield item

    return wrap_and_watermark(orig_func, stream_patch)


def patch_starlette_requests(starlette_requests_module):
    build_and_apply_patch(
        starlette_requests_module.Request, "session", build_session_patch
    )
    build_and_apply_patch(
        starlette_requests_module.Request, "stream", build_stream_patch
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
