from __future__ import annotations

from collections.abc import Callable

from fastapi import FastAPI
from matrx_connect import iter_api_routes

from matrx_files._config import IndependenceConfigError


def assert_route_auth_coverage(
    app: FastAPI,
    *,
    auth_dependency: Callable[..., object],
    public_paths: frozenset[str],
    public_prefixes: tuple[str, ...],
    public_operations: frozenset[str] = frozenset(),
) -> None:
    """Refuse to boot when a non-public HTTP route lacks the auth dependency.

    ``public_operations`` allowlists single ``"METHOD /path"`` pairs where only
    one verb on a shared path is legitimately anonymous (e.g. the TUS
    ``OPTIONS`` capabilities advertisement).

    Route enumeration goes through ``matrx_connect.iter_api_routes`` — the one
    walker that recurses into included/mounted routers (FastAPI >= 0.139 no
    longer flattens ``include_router`` targets into ``app.routes``). Reading
    ``app.routes`` directly would see ZERO APIRoutes and silently pass with
    every route uncovered, so this check additionally refuses to conclude
    anything when it finds no API routes at all.
    """
    uncovered: list[str] = []
    seen_api_routes = 0
    for mounted in iter_api_routes(app):
        route, path, include_deps = mounted.route, mounted.path, mounted.dependencies
        seen_api_routes += 1
        if path in public_paths or path.startswith(public_prefixes):
            continue
        methods = route.methods or set()
        if methods and all(f"{m} {path}" in public_operations for m in methods):
            continue
        covered = _dependency_tree_contains(route.dependant, auth_dependency) or any(
            getattr(dep, "dependency", None) is auth_dependency for dep in include_deps
        )
        if not covered:
            uncovered.append(f"{','.join(sorted(methods))} {path}")
    if seen_api_routes == 0:
        raise IndependenceConfigError(
            "matrx-files standalone auth-coverage check found ZERO API routes — "
            "the route walker cannot see this FastAPI version's routing tree, so "
            "coverage cannot be proven. Refusing to boot fail-open."
        )
    if uncovered:
        raise IndependenceConfigError(
            "matrx-files standalone refuses to boot with fail-open routes. "
            "Add the authenticated user dependency or explicitly allowlist a "
            f"public capability: {uncovered}"
        )


def _dependency_tree_contains(dependant: object, target: Callable[..., object]) -> bool:
    if getattr(dependant, "call", None) is target:
        return True
    return any(
        _dependency_tree_contains(child, target) for child in getattr(dependant, "dependencies", ())
    )
