"""Type aliases for versioned FastAPI application configuration.

Defines the public type vocabulary used by ``configure_versioned_api`` and
``compose_versioned_apps``: version maps, middleware specs, exception handler
providers, context-guard callables, and path-parameter dependency descriptors.
"""

from collections.abc import Callable, Mapping, Sequence
from contextlib import AbstractAsyncContextManager
from typing import Annotated, Any

from fastapi import FastAPI
from fastapi.params import Depends as DependsParam
from starlette.types import ExceptionHandler

from csrd.versioning._types import VersionedAppState, VersionKey

VersionMap = Mapping[VersionKey, FastAPI]
VersionedAppConfigurer = Callable[[FastAPI], None]
VersionedAppLifespan = Callable[[FastAPI], AbstractAsyncContextManager[Any]]

Middleware = type | tuple[type, dict[str, Any] | None]

ExHandler = tuple[int | type[Exception], ExceptionHandler]
ExceptionHandlerProvider = Callable[[], Mapping[int | type[Exception], ExceptionHandler]]


PathParamDependencySpec = DependsParam | Callable[..., Any] | Annotated[Any, DependsParam]
PathParamDependencies = Sequence[PathParamDependencySpec]
NormalizedDependencySpec = tuple[DependsParam, Callable[..., Any], set[str]]

__all__ = (
    "ExHandler",
    "ExceptionHandlerProvider",
    "Middleware",
    "NormalizedDependencySpec",
    "PathParamDependencies",
    "PathParamDependencySpec",
    "VersionKey",
    "VersionMap",
    "VersionedAppConfigurer",
    "VersionedAppLifespan",
    "VersionedAppState",
)
