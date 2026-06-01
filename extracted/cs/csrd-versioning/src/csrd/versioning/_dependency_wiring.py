"""Dependency injection wiring for versioned FastAPI routes."""

import logging
import re
from collections.abc import AsyncIterator, Callable
from http import HTTPStatus
from typing import Any

from fastapi import Depends, FastAPI
from fastapi.routing import APIRoute
from fastapi.security import HTTPBearer
from starlette.requests import Request
from starlette.routing import Route, WebSocketRoute

from csrd.context import (
    PathValue,
    reset_path_params,
    reset_query_params,
    set_path_params,
    set_query_params,
)
from csrd.versioning._core import normalize_prefix, normalize_version

from ._dependencies import param_factory
from ._fastapi_types import (
    NormalizedDependencySpec,
    PathParamDependencies,
    VersionMap,
)
from ._helpers import (
    DependsParam,
    _dep_already_present,
    _extract_param_names,
    _normalize_dep,
    _rebuild_route,
    _route_has_param,
)

logger = logging.getLogger(__name__)

_PATH_PARAM_RE = re.compile(r"\{(\w+)(?::\w+)?\}")


def _get_route_param_names(route: APIRoute) -> set[str]:
    """Extract path parameter names from the route path template."""
    return set(_PATH_PARAM_RE.findall(route.path))


class PathParamParser:
    """FastAPI dependency that captures path/query params into core contextvars."""

    async def __call__(self, request: Request) -> AsyncIterator[None]:
        path_token = set_path_params(PathValue(request.path_params))
        query_token = set_query_params(PathValue(request.query_params))

        try:
            yield
        finally:
            reset_path_params(path_token)
            reset_query_params(query_token)


def _status_description(status_code: int) -> str:
    """Return a friendly description for an HTTP status code."""
    try:
        return HTTPStatus(status_code).phrase
    except ValueError:
        return f"HTTP {status_code}"


def _documented_error_statuses_from_handlers(
    resolved_handler_map: dict[int | type[Exception], Any],
) -> set[int]:
    """Extract numeric status codes from resolved exception handler keys."""
    status_codes = {key for key in resolved_handler_map if isinstance(key, int)}
    status_codes.update({401, 403})
    return status_codes


def _uncovered_route_params(
    route: APIRoute, existing: list[NormalizedDependencySpec] | None = None
) -> set[str]:
    if existing is None:
        existing = []

    covered: set[str] = set()
    for _, __, required_params in existing:
        if all(_route_has_param(route, name) for name in required_params):
            covered.update(required_params)

    return _get_route_param_names(route) - covered


def _route_bearer_guard_opt_out(route: APIRoute) -> bool:
    """Return True when a route opts out of bearer dependency enforcement."""
    openapi_extra = route.openapi_extra or {}
    return openapi_extra.get("x-bearer-guard") is False


def _remove_bearer_dependencies(
    dependencies: list[DependsParam],
) -> tuple[list[DependsParam], bool]:
    """Remove HTTPBearer-based dependencies from a dependency list."""
    filtered_dependencies: list[DependsParam] = []
    removed_any = False

    for dependency in dependencies:
        dep_callable = getattr(dependency, "dependency", None)
        if isinstance(dep_callable, HTTPBearer):
            removed_any = True
            continue
        filtered_dependencies.append(dependency)

    return filtered_dependencies, removed_any


def _has_dependency(dependencies: list[DependsParam], dependency: Callable[..., Any]) -> bool:
    """Return True when a dependency callable is already present by identity."""
    return any(dep.dependency is dependency for dep in dependencies)


def _build_normalized_dependency_specs(
    path_param_dependencies: PathParamDependencies | None,
) -> list[NormalizedDependencySpec]:
    """Normalize and filter path-param dependency specs for route injection."""
    normalized_specs: list[NormalizedDependencySpec] = []

    if path_param_dependencies:
        for spec in path_param_dependencies:
            dep_param, dep_callable = _normalize_dep(spec)
            required_params = _extract_param_names(dep_callable)
            if not required_params:
                continue
            normalized_specs.append((dep_param, dep_callable, required_params))

    return normalized_specs


def _strip_prefix_from_versioned_routes(versioned_app: FastAPI, prefix: str) -> None:
    """Remove already-present API prefix from mounted versioned route paths."""
    normalized_prefix = normalize_prefix(prefix)
    if normalized_prefix == "/":
        return

    for route in versioned_app.routes:
        if isinstance(route, (Route, WebSocketRoute)):
            if route.path == normalized_prefix:
                route.path = "/"
                continue

            if route.path.startswith(f"{normalized_prefix}/"):
                route.path = route.path[len(normalized_prefix) :]


def _apply_path_param_deps_to_route(
    route: APIRoute,
    dependencies: list[DependsParam],
    normalized_specs: list[NormalizedDependencySpec],
) -> bool:
    """Inject path-param dependencies for route-matching parameter names."""
    if not normalized_specs:
        return False

    changed = False
    route_specs = list(normalized_specs)
    params = _uncovered_route_params(route, route_specs)

    for param in params:
        factory = param_factory(param)
        route_specs.append((Depends(factory), factory, {param}))

    for dep_param, _dep_callable, required_params in route_specs:
        if all(
            _route_has_param(route, name) for name in required_params
        ) and not _dep_already_present(dependencies, dep_param):
            dependencies.append(dep_param)
            changed = True

    return changed


def _ensure_path_param_parser_dependency(dependencies: list[DependsParam]) -> bool:
    """Ensure `PathParamParser` exists in route dependencies."""
    if any(isinstance(dep.dependency, PathParamParser) for dep in dependencies):
        return False

    dependencies.append(Depends(PathParamParser()))
    return True


def _process_versioned_route(
    route: APIRoute,
    *,
    normalized_specs: list[NormalizedDependencySpec],
    documented_error_statuses: set[int] | None,
) -> tuple[list[DependsParam], bool]:
    """Apply dependency mutations to a single versioned route."""
    dependencies = list(route.dependencies or [])
    dependencies_changed = False

    if _route_bearer_guard_opt_out(route):
        dependencies, removed_bearer_dependency = _remove_bearer_dependencies(dependencies)
        if removed_bearer_dependency:
            dependencies_changed = True
            logger.debug("Bearer dependency removed (opt-out) from route: %s", route.path)

    if _apply_path_param_deps_to_route(
        route,
        dependencies,
        normalized_specs,
    ):
        dependencies_changed = True

    if _ensure_path_param_parser_dependency(dependencies):
        dependencies_changed = True

    return dependencies, dependencies_changed


def _apply_route_dependency_updates(
    app: FastAPI,
    versioned_app: FastAPI,
    route_index: int,
    route: APIRoute,
    dependencies: list[DependsParam],
) -> None:
    """Replace route with a new instance carrying updated dependencies."""
    versioned_app.routes[route_index] = _rebuild_route(route, dependencies)
    versioned_app.openapi_schema = None
    app.openapi_schema = None


def _mount_and_wire_versions(
    app: FastAPI,
    version_mapping: VersionMap,
    prefix: str,
    path_param_dependencies: PathParamDependencies | None = None,
    documented_error_statuses: set[int] | None = None,
) -> None:
    """Mount versioned apps and inject dependencies required for routing."""
    normalized_specs = _build_normalized_dependency_specs(path_param_dependencies)

    for api, versioned_app in version_mapping.items():
        _strip_prefix_from_versioned_routes(versioned_app, prefix)

        for i, route in enumerate(versioned_app.routes):
            if not isinstance(route, APIRoute):
                continue

            dependencies, dependencies_changed = _process_versioned_route(
                route,
                normalized_specs=normalized_specs,
                documented_error_statuses=documented_error_statuses,
            )

            if dependencies_changed:
                _apply_route_dependency_updates(
                    app,
                    versioned_app,
                    i,
                    route,
                    dependencies,
                )

        normalized_version = normalize_version(api)
        mount_prefix = (
            f"/{normalized_version}" if prefix == "/" else f"{prefix}/{normalized_version}"
        )
        app.include_router(versioned_app.router, prefix=mount_prefix)
        logger.debug(
            "Mounted version %s at %s/%s with %d routes",
            api,
            prefix,
            normalize_version(api),
            sum(1 for r in versioned_app.routes if isinstance(r, APIRoute)),
        )
