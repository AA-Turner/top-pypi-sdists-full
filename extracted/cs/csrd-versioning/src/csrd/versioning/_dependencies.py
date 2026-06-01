"""FastAPI dependency functions for injecting versioning context values."""

from typing import Annotated
from uuid import UUID

from fastapi import Depends, HTTPException, Path

from csrd.context import get_api_version, get_app_id, get_hit_id


def param_factory(name: str = "value", validator=None):
    """Create a FastAPI dependency that extracts a string path parameter and,
    optionally, validates it using a user-provided callable.
    """

    def dependency(value: Annotated[str, Path(alias=name)]):
        if validator is not None:
            try:
                validator(value)
            except (ValueError, TypeError, AssertionError) as exc:
                raise HTTPException(
                    status_code=422, detail=f"Invalid path parameter {name}: {exc}"
                ) from exc
        return str(value)

    return dependency


def uuid_id_factory(name: str = "id"):
    def dependency(value: Annotated[str, Path(alias=name)]):
        try:
            return UUID(str(value))
        except (ValueError, TypeError, AttributeError) as exc:
            raise HTTPException(
                status_code=422, detail=f"{name} is not a valid UUID: {value}"
            ) from exc

    return dependency


def api_version_dependency() -> str | None:
    """Return the resolved API version for the current request context."""
    return get_api_version()


def app_id_dependency() -> str | None:
    """Return the current request app-id header value."""
    return get_app_id()


def hit_id_dependency() -> str | None:
    """Return the current request hit-id header value."""
    return get_hit_id()


ApiVersionDep = Annotated[str | None, Depends(api_version_dependency)]
AppIdDep = Annotated[str | None, Depends(app_id_dependency)]
HitIdDep = Annotated[str | None, Depends(hit_id_dependency)]


__all__ = (
    "ApiVersionDep",
    "AppIdDep",
    "HitIdDep",
    "param_factory",
    "uuid_id_factory",
)
