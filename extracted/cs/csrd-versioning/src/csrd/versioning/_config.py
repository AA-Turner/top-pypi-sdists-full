from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

from ._fastapi_types import (
    ExceptionHandlerProvider,
    ExHandler,
    Middleware,
    PathParamDependencies,
    VersionedAppConfigurer,
    VersionedAppLifespan,
)
from ._types import VersionedAppState, VersionKey
from .extensions import Extension
from .extensions.actuator.plugins import ActuatorPlugin
from .extensions.swagger_ui._base import SwaggerPlugin


@dataclass(slots=True)
class VersionedApiConfig:
    """Configuration for wiring version dispatch and docs into an existing FastAPI app."""

    default_version: VersionKey | None = None
    app_name: str | None = None
    middleware: list[Middleware] = field(default_factory=list)
    ex_handlers: list[ExHandler] = field(default_factory=list)
    exception_handler_provider: ExceptionHandlerProvider | None = None
    prefix: str | None = None
    hit_id_header: str | None = None
    app_id_header: str | None = None
    path_param_dependencies: PathParamDependencies = field(default_factory=tuple)
    current_user_claims_provider: Callable[[], Any] | None = None
    strict_version_matching: bool = False
    include_info_endpoints: bool = True
    include_root_favicon_alias: bool = True
    include_actuator_endpoints: bool = True

    # Plugin injection for built-in extensions
    actuator_plugins: list[ActuatorPlugin] = field(default_factory=list)
    swagger_plugins: list[SwaggerPlugin] = field(default_factory=list)

    # Custom / override extensions (merged with defaults by name)
    extensions: list[Extension] = field(default_factory=list)


@dataclass(slots=True)
class VersionedAppComposeConfig:
    """Configuration for composing a root dispatcher FastAPI app."""

    title: str | None = None
    lifespan: VersionedAppLifespan | None = None
    app_state: VersionedAppState | None = None
    configure_app: VersionedAppConfigurer | None = None
    api: VersionedApiConfig = field(default_factory=VersionedApiConfig)


__all__ = (
    "VersionedApiConfig",
    "VersionedAppComposeConfig",
)
