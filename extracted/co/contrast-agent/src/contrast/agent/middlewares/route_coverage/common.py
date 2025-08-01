# Copyright © 2025 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
"""
Rules for coverage:

- new routes on init get count 0
- new routes after init get count 1 per context
- routes without a method type specified on init are ['GET', 'POST']
- a route needs verb, route, url, and count
- url should be normalized uri
- route should be the path to the view function (aka controller for Java people)
- one method type per route

Example:
      GET /blog/foo/bar - app.blogs.find(request, ) 0
"""

import functools
import inspect
from typing import Callable
import re

from contrast.utils.decorators import fail_quietly

from contrast_fireball import DiscoveredRoute
from contrast_vendor import structlog as logging

logger = logging.getLogger("contrast")


DEFAULT_ROUTE_METHODS = ("GET", "POST")
ROUTE_DISCOVERY_THREAD_NAME = "ContrastRouteDiscovery"

# A format template for constructing "path-component" regexps, ie between "/"-s in a URI
# This is used to build regexps for uri normalization
# We use a look-ahead to ensure correctness for back-to-back path components
_RE_PATH_COMPONENT_FORMAT = r"(^|/){regex}(?=(/|$))"

# examples:
# /123
# 123/
# 123
# /123/
# 123/123
RE_DIGITS_PATH_COMPONENT = _RE_PATH_COMPONENT_FORMAT.format(regex=r"\d+")

# example:
# /fd4b78312634a236d11da0f9c32526e5b8261afa
RE_HASH_PATH_COMPONENT = _RE_PATH_COMPONENT_FORMAT.format(
    regex=r"([a-fA-F0-9]{2}){16,}"
)

# example:
# /b09112a0-a58f-487a-ab4b-3608bd64fb3f/
RE_UUID_PATH_COMPONENT = _RE_PATH_COMPONENT_FORMAT.format(
    regex=r"[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}"
)

# Returns digits between '/' or end of string
FIND_REQEUST_PARAMS = r"(?<=\/)\d+(?=\/|$)"


def get_normalized_uri(path):
    """
    A best-effort to remove client-specific information from the path.

    Example:
    /user/123456/page/12 -> /user/{n}/page/{n}
    """
    result = path

    result = re.sub(RE_DIGITS_PATH_COMPONENT, r"\1{n}", result)
    result = re.sub(RE_HASH_PATH_COMPONENT, r"\1{hash}", result)
    result = re.sub(RE_UUID_PATH_COMPONENT, r"\1{uuid}", result)

    return result


def get_url_parameters(path):
    """
    A best-effort to remove client-specific information from the path.

    Example:
    /user/123456/page/12 -> /user/{n}/page/{n}
    """
    return re.findall(FIND_REQEUST_PARAMS, path)


def build_signature(view_func_name, view_func):
    view_func_args = build_args_from_function(view_func)
    return view_func_name + view_func_args


def build_args_from_function(func):
    """
    Attempts to grab argument names from the function definition.

    Defaults to () if none exist
    If there is no view function, like in the case of a pure WSGI app, then the func will
    be a string like '/sqli' and we just return that.

    """
    if isinstance(func, functools.partial):
        func = getattr(func, "func", None)

    func = inspect.unwrap(func)
    method_arg_names = "()"
    if func is not None and hasattr(func, "__code__"):
        method_arg_names = str(
            func.__code__.co_varnames[0 : func.__code__.co_argcount]
        ).replace("'", "")
    elif isinstance(func, str):
        method_arg_names = func

    return method_arg_names


@fail_quietly("Failed to perform route discovery")
def handle_route_discovery(
    framework: str, discovery_func: Callable[..., set[DiscoveredRoute]], args
) -> None:
    """
    Start the route discovery background thread if inventory is enabled.
    """
    from contrast.agent import agent_state

    if (
        settings := agent_state.get_settings()
    ) is None or not settings.is_inventory_enabled():
        logger.debug("Inventory disabled - will not perform route discovery")
        return

    logger.debug("Starting route discovery background thread", framework=framework)
    _do_route_discovery(framework, discovery_func, args)


@fail_quietly("Failed to perform route discovery in background thread")
def _do_route_discovery(
    framework: str,
    discovery_func: Callable[..., set[DiscoveredRoute]],
    args: tuple,
) -> None:
    """
    Top-level background thread function for route discovery.
    """
    from contrast.agent import agent_state

    discovered_routes = discovery_func(*args)
    agent_state.module.reporting_client.new_discovered_routes(discovered_routes)
    log_discovered_routes(framework, discovered_routes)


def log_discovered_routes(framework: str, routes: set[DiscoveredRoute]) -> None:
    logger.debug(
        "Discovered routes",
        framework=framework,
        routes=[f"{route.verb} {route.url}" for route in routes],
    )
