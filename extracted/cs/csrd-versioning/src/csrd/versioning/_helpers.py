import inspect
from collections.abc import Callable
from http import HTTPStatus
from typing import Annotated, Any, get_args, get_origin

from fastapi import Depends, HTTPException
from fastapi.params import Depends as DependsParam
from fastapi.params import Param as PathParam
from fastapi.routing import APIRoute
from starlette.datastructures import Headers

from csrd.context import get_headers
from csrd.versioning._constants import AUTH_HEADER_NAME

HeadersGetter = Callable[[], Headers | dict] | Headers | dict


def find_bearer(
    headers_or_getter: HeadersGetter | None = None, *, fail_on_missing: bool = True
) -> str | None:
    """Return the bearer/authorization header value from provided or contextual headers."""
    if headers_or_getter is not None and callable(headers_or_getter):
        headers = headers_or_getter()
    elif headers_or_getter is not None and isinstance(headers_or_getter, (Headers, dict)):
        headers = headers_or_getter
    else:
        headers = get_headers()

    if headers:
        bearer = headers.get(AUTH_HEADER_NAME) or headers.get("Authorization")
        if bearer is not None:
            return bearer

    if fail_on_missing:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Unauthorized")

    return None


def find_token() -> str:
    """Extract and return raw token from bearer header value."""
    bearer = find_bearer()
    if bearer is None:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Unauthorized")

    bearer = bearer.strip()
    if bearer == "":
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Unauthorized")

    if bearer.lower() == "bearer":
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED)

    if bearer.lower().startswith("bearer "):
        token = bearer[7:].strip()
        if token == "":
            raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED)
        return token

    return bearer


def _route_path_template(route: APIRoute) -> str:
    """Return canonical route path template used for dependency calculations."""
    return str(getattr(route, "path_format", None) or route.path)


def _route_has_param(route: APIRoute, name: str) -> bool:
    """Return True when route path template contains a named path parameter."""
    return f"{{{name}}}" in _route_path_template(route)


def _unwrap_depends_from_annotated(obj: Any) -> DependsParam | None:
    """Extract `Depends` metadata from `typing.Annotated`, if present."""
    if get_origin(obj) is not Annotated:
        return None
    meta = get_args(obj)[1:]
    for m in meta:
        if isinstance(m, DependsParam):
            return m
    return None


def _normalize_dep(obj: Any) -> tuple[DependsParam, Callable[..., Any]]:
    """Normalize supported dependency forms into `(DependsParam, callable)`."""
    if isinstance(obj, DependsParam):
        if obj.dependency is None:
            raise TypeError("Depends(...) must wrap a callable dependency.")
        return obj, obj.dependency

    ann = _unwrap_depends_from_annotated(obj)
    if ann is not None:
        if ann.dependency is None:
            raise TypeError("Annotated Depends(...) must wrap a callable dependency.")
        return ann, ann.dependency

    if callable(obj):
        d = Depends(obj)
        return d, obj

    raise TypeError(f"Object is not a valid dependency: {obj!r}")


def _extract_param_names(dep_callable: Callable[..., Any]) -> set[str]:
    """Collect path-parameter names consumed by a dependency callable."""
    names: set[str] = set()
    sig = inspect.signature(dep_callable)

    for p in sig.parameters.values():
        if isinstance(p.default, PathParam):
            alias = getattr(p.default, "alias", None)
            names.add(alias or p.name)
            continue

        ann = p.annotation
        if get_origin(ann) is Annotated:
            meta = get_args(ann)[1:]
            for m in meta:
                if isinstance(m, PathParam):
                    alias = getattr(m, "alias", None)
                    names.add(alias or p.name)

    return names


def _dep_already_present(deps: list[Any], dep: DependsParam) -> bool:
    """Return True when dependency list already contains the same callable."""
    return any(isinstance(d, DependsParam) and d.dependency is dep.dependency for d in deps)


def _rebuild_route(route: APIRoute, dependencies: list[DependsParam]) -> APIRoute:
    """Create a new APIRoute with updated dependencies."""
    sig = inspect.signature(APIRoute.__init__)
    kwargs: dict[str, Any] = {}
    for name in sig.parameters:
        if name == "self":
            continue
        if name == "dependencies":
            kwargs["dependencies"] = dependencies
            continue
        if hasattr(route, name):
            kwargs[name] = getattr(route, name)
    return APIRoute(**kwargs)


__all__ = (
    "HeadersGetter",
    "find_bearer",
    "find_token",
)
