"""The ONE way to enumerate a FastAPI app's mounted routes.

Why this exists: FastAPI >= 0.139 (Starlette 1.x) no longer flattens
``include_router`` targets into ``app.routes``. It appends a single lazy
``_IncludedRouter`` wrapper instead, which carries the original router plus an
include context (prefix + dependencies) and has **no** ``.path`` attribute.

Every walker written against the old behavior therefore breaks in one of two
ways, and the silent one is the dangerous one:

* ``{route.path for route in app.routes}`` raises ``AttributeError``.
* ``{getattr(route, "path", "") for route in app.routes}`` silently yields
  nothing for every included router — an app with 900 mounted routes reports a
  handful, and any check built on it (auth coverage, capability inventory,
  exposure audits) passes fail-open while proving nothing.

Use :func:`iter_api_routes` / :func:`mounted_api_paths` instead of reading
``app.routes`` directly, and treat an empty result as "the walker cannot see
this FastAPI version's routing tree", never as "there are no routes".
"""

from __future__ import annotations

from collections.abc import Callable, Iterable, Iterator, Sequence
from dataclasses import dataclass, field
from typing import Any

from fastapi.routing import APIRoute

__all__ = [
    "AuthenticatedResourceRoute",
    "MountedRoute",
    "authenticated_resource_routes",
    "iter_api_routes",
    "mounted_api_paths",
]


@dataclass(frozen=True)
class AuthenticatedResourceRoute:
    """One literal method/path declaration allowed to defer org pre-refusal."""

    method: str
    path: str

    def __post_init__(self) -> None:
        if not isinstance(self.method, str) or not self.method or self.method != self.method.upper():
            raise ValueError("resource route method must be a nonempty uppercase HTTP method")
        if not isinstance(self.path, str) or not self.path.startswith("/"):
            raise ValueError("resource route path must be an absolute path")
        if self.path != "/" and self.path.endswith("/"):
            raise ValueError("resource route path must not have a trailing slash")
        if "//" in self.path:
            raise ValueError("resource route path must not contain empty segments")
        for segment in self.path.split("/")[1:]:
            if "{" in segment or "}" in segment:
                if not (
                    segment.startswith("{")
                    and segment.endswith("}")
                    and segment[1:-1].isidentifier()
                ):
                    raise ValueError("resource route parameters must be complete identifier segments")


def _has_dependency(dependency: Any, marker: Callable[..., Any]) -> bool:
    """Find a marker by object identity through FastAPI's dependency tree."""
    if getattr(dependency, "dependency", None) is marker or getattr(dependency, "call", None) is marker:
        return True
    return any(_has_dependency(child, marker) for child in getattr(dependency, "dependencies", ()) or ())


def authenticated_resource_routes(
    app_or_routes: Any,
    marker: Callable[..., Any],
) -> tuple[AuthenticatedResourceRoute, ...]:
    """Enumerate routes directly marked with the resource-bootstrap dependency.

    The host owns its explicit route shape; this package merely discovers the
    real mounted route and binds each declared method independently.
    """
    if not callable(marker):
        raise ValueError("resource bootstrap marker must be callable")
    declarations: set[AuthenticatedResourceRoute] = set()
    for mounted in iter_api_routes(app_or_routes):
        dependency_roots = (
            *mounted.dependencies,
            *(mounted.route.dependencies or ()),
            mounted.route.dependant,
        )
        if not any(_has_dependency(dependency, marker) for dependency in dependency_roots):
            continue
        for method in mounted.methods:
            declarations.add(AuthenticatedResourceRoute(method=method, path=mounted.path))
    return tuple(sorted(declarations, key=lambda entry: (entry.path, entry.method)))


@dataclass(frozen=True)
class MountedRoute:
    """One APIRoute as the app actually serves it.

    ``dependencies`` and ``tags`` merge what ``include_router(...)`` attached at
    mount time with what the route declared itself — neither of which is
    visible on the route object alone once FastAPI stopped flattening routers.
    """

    route: APIRoute
    path: str
    dependencies: tuple[Any, ...] = ()
    tags: tuple[Any, ...] = field(default=())

    @property
    def methods(self) -> set[str]:
        return set(self.route.methods or set())


def iter_api_routes(
    app_or_routes: Any,
    prefix: str = "",
    include_deps: Sequence[Any] = (),
    include_tags: Sequence[Any] = (),
) -> Iterator[MountedRoute]:
    """Yield a :class:`MountedRoute` for every ``APIRoute`` reachable from an
    app (or a raw routes iterable), recursing into included routers and
    Starlette mounts.

    Dependencies and tags attached at ``include_router(...)`` time never appear
    on the route's own ``dependant``/``tags``, so any check that ignores them
    under-reports.
    """
    routes: Iterable[Any] = getattr(app_or_routes, "routes", None) or app_or_routes
    for route in routes:
        if isinstance(route, APIRoute):
            yield MountedRoute(
                route=route,
                path=prefix + route.path,
                dependencies=tuple(include_deps),
                tags=tuple(include_tags) + tuple(route.tags or ()),
            )
            continue
        # FastAPI >= 0.139: include_router mounts an _IncludedRouter carrying
        # the original router plus an include context (prefix + dependencies).
        original = getattr(route, "original_router", None)
        if original is not None:
            ctx = getattr(route, "include_context", None)
            sub_prefix = prefix + (getattr(ctx, "prefix", "") or "")
            sub_deps = tuple(include_deps) + tuple(getattr(ctx, "dependencies", ()) or ())
            sub_tags = tuple(include_tags) + tuple(getattr(ctx, "tags", ()) or ())
            yield from iter_api_routes(original.routes, sub_prefix, sub_deps, sub_tags)
            continue
        # Starlette Mount / nested routers on older versions.
        sub_routes = getattr(route, "routes", None)
        if sub_routes:
            yield from iter_api_routes(
                sub_routes,
                prefix + (getattr(route, "path", "") or ""),
                include_deps,
                include_tags,
            )


def mounted_api_paths(app_or_routes: Any) -> set[str]:
    """Every full path an app actually serves, included routers included."""
    return {mounted.path for mounted in iter_api_routes(app_or_routes)}
