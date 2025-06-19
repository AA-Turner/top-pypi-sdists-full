# Copyright © 2025 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from inspect import isclass
from pathlib import Path
from typing import Optional

import functools

from collections import deque
from copy import copy
from importlib import import_module
from types import FunctionType, MethodType
from contrast_fireball import DiscoveredRoute
from django.urls import ResolverMatch, get_resolver
from django.urls.exceptions import Resolver404

from contrast.agent.middlewares.route_coverage.common import (
    DEFAULT_ROUTE_METHODS,
    build_args_from_function,
)

from contrast_vendor import structlog as logging
from contrast.utils.decorators import fail_quietly

logger = logging.getLogger("contrast")


def get_required_http_methods(func: FunctionType) -> Optional[set]:
    """
    Grabs the require_http_list closure variable from a view function through its code object.
    """

    if isinstance(func, functools.partial):
        func = getattr(func, "func", None)

    if func is None:
        return None

    method_types = _get_required_http_methods(func)

    if wrapped := getattr(func, "__wrapped__", None):
        if (restricted_methods := get_required_http_methods(wrapped)) is not None:
            method_types = (
                set(restricted_methods)
                if method_types is None
                else method_types.intersection(restricted_methods)
            )

    return method_types


def get_closure_variable(func: FunctionType, varname: str):
    if not (closure := getattr(func, "__closure__", None)):
        return None
    if varname not in func.__code__.co_freevars:
        return None
    index = func.__code__.co_freevars.index(varname)
    return closure[index].cell_contents


DJANGO_HTTP_DECORATOR_PATH_SUFFIX = str(
    Path("django", "views", "decorators", "http.py")
)


def _get_required_http_methods(viewfunc: FunctionType):
    if not viewfunc.__code__.co_filename.endswith(DJANGO_HTTP_DECORATOR_PATH_SUFFIX):
        return None
    restricted_methods = get_closure_variable(viewfunc, "request_method_list")
    if restricted_methods and isinstance(restricted_methods, list):
        return set(restricted_methods)
    return None


def get_lowest_function_call(func):
    if isclass(func) or func.__closure__ is None:
        return func
    closure = (c.cell_contents for c in func.__closure__)
    return next((c for c in closure if isinstance(c, (FunctionType, MethodType))), None)


def get_method_info(pattern_or_resolver):
    if not (viewfunc := pattern_or_resolver.callback):
        return DEFAULT_ROUTE_METHODS, "()"

    method_arg_names = build_args_from_function(get_lowest_function_call(viewfunc))
    method_types = (
        required_methods
        if (required_methods := get_required_http_methods(viewfunc)) is not None
        else DEFAULT_ROUTE_METHODS
    )
    return method_types, method_arg_names


def create_routes(urlpatterns) -> set[DiscoveredRoute]:
    from django.urls.resolvers import (
        URLPattern as RegexURLPattern,
        URLResolver as RegexURLResolver,
    )

    routes = set()

    urlpatterns_deque = deque(urlpatterns)

    while urlpatterns_deque:
        url_pattern = urlpatterns_deque.popleft()

        if isinstance(url_pattern, RegexURLResolver):
            urlpatterns_deque.extend(url_pattern.url_patterns)

        elif isinstance(url_pattern, RegexURLPattern):
            method_types, method_arg_names = get_method_info(url_pattern)
            path_template = url_pattern.pattern.regex.pattern
            signature = build_django_signature(url_pattern, method_arg_names)
            for method_type in method_types:
                routes.add(
                    DiscoveredRoute(
                        verb=method_type,
                        url=path_template,
                        signature=signature,
                        framework="Django",
                    )
                )
    return routes


def create_django_routes() -> set[DiscoveredRoute]:
    """
    Grabs all URL's from the root settings and searches for possible required_method decorators

    In Django there is no implicit declaration of GET or POST. Often times decorators are used to fix this.

    Returns a dict of key = id, value = api.Route.
    """

    from django.conf import settings

    if not settings.ROOT_URLCONF:
        logger.info("Application does not define settings.ROOT_URLCONF")
        logger.debug("Skipping enumeration of urlpatterns")
        return set()

    try:
        root_urlconf = import_module(settings.ROOT_URLCONF)
    except Exception as exception:
        logger.debug("Failed to import ROOT_URLCONF: %s", exception)
        return set()

    try:
        urlpatterns = root_urlconf.urlpatterns or []
    except Exception as exception:
        logger.debug("Failed to get urlpatterns: %s", exception)
        return set()

    url_patterns = copy(urlpatterns)
    return create_routes(url_patterns)


def _function_loc(func):
    """Return the function's module and name"""
    return f"{func.__module__}.{func.__name__}"


def build_django_signature(obj, method_arg_names=None):
    if hasattr(obj, "lookup_str"):
        signature = obj.lookup_str
    elif hasattr(obj, "callback"):
        cb = obj.callback
        signature = _function_loc(cb)
    elif callable(obj):
        signature = _function_loc(obj)
    else:
        logger.debug(
            "WARNING: can't build django signature for object type %s", type(obj)
        )
        return ""

    if method_arg_names is None:
        method_arg_names = build_args_from_function(obj)

    signature += method_arg_names
    return signature


@fail_quietly("Failed to get view function for django application")
def get_matched_resolver(path) -> Optional[ResolverMatch]:
    from django.conf import settings

    try:
        result = get_resolver().resolve(path or "/")
    except Resolver404:
        return None

    if (
        result is None
        and not path.endswith("/")
        and "django.middleware.common.CommonMiddleware" in settings.MIDDLEWARE
        and settings.APPEND_SLASH
    ):
        result = get_matched_resolver(f"{path}/")
    if result is None:
        return None

    return result
