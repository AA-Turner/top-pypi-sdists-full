# Copyright © 2025 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from __future__ import annotations
from pathlib import Path

import functools

from copy import copy
from importlib import import_module
from types import FunctionType
from contrast_fireball import DiscoveredRoute
from django.urls import ResolverMatch, get_resolver
from django.urls.exceptions import Resolver404
from django.urls.resolvers import (
    URLPattern as RegexURLPattern,
    URLResolver as RegexURLResolver,
)

from contrast.agent.middlewares.route_coverage.common import (
    DEFAULT_ROUTE_METHODS,
    build_args_from_function,
)

from contrast_vendor import structlog as logging
from contrast.utils.decorators import fail_quietly

logger = logging.getLogger("contrast")


def get_required_http_methods(func: FunctionType) -> set | None:
    """
    Grabs the require_http_list closure variable from a view function through its code object.
    """

    if isinstance(func, functools.partial):
        func = getattr(func, "func", None)

    if func is None:
        return None

    method_types = _get_required_http_methods(func)

    if (wrapped := getattr(func, "__wrapped__", None)) and (
        restricted_methods := get_required_http_methods(wrapped)
    ) is not None:
        method_types = (
            set(restricted_methods)
            if method_types is None
            else method_types.intersection(restricted_methods)
        )

    return method_types


def _get_closure_variable(func: FunctionType, varname: str):
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
    if class_view := getattr(viewfunc, "view_class", None):
        # This is a class-based view,
        return {
            method.upper()
            for method in class_view.http_method_names
            if hasattr(class_view, method)
        }
    if not viewfunc.__code__.co_filename.endswith(DJANGO_HTTP_DECORATOR_PATH_SUFFIX):
        return None
    restricted_methods = _get_closure_variable(viewfunc, "request_method_list")
    if restricted_methods and isinstance(restricted_methods, list):
        return set(restricted_methods)
    return None


def get_method_info(pattern_or_resolver):
    if not (viewfunc := pattern_or_resolver.callback):
        return DEFAULT_ROUTE_METHODS, "()"

    method_arg_names = build_args_from_function(viewfunc)
    method_types = (
        required_methods
        if (required_methods := get_required_http_methods(viewfunc)) is not None
        else DEFAULT_ROUTE_METHODS
    )
    return method_types, method_arg_names


def create_routes(urlpatterns, url_prefix="/") -> set[DiscoveredRoute]:
    routes = set()

    def url_str(pattern: str):
        return f"{url_prefix.removesuffix('/')}/{pattern}"

    for urlpattern in reversed(urlpatterns):
        if isinstance(urlpattern, RegexURLResolver):
            routes.update(
                create_routes(urlpattern.url_patterns, url_str(str(urlpattern.pattern)))
            )

        elif isinstance(urlpattern, RegexURLPattern):
            method_types, method_arg_names = get_method_info(urlpattern)
            url = url_str(str(urlpattern.pattern))
            signature = build_django_signature(urlpattern, method_arg_names)
            for method_type in method_types:
                routes.add(
                    DiscoveredRoute(
                        verb=method_type,
                        url=url,
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
    elif hasattr(obj, "_func_path"):
        signature = obj._func_path
        obj = obj.func
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
def get_matched_resolver(path) -> ResolverMatch | None:
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
