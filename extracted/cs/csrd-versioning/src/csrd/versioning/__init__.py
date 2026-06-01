"""API versioning, dispatch, docs, and actuator for FastAPI."""

from ._config import VersionedApiConfig, VersionedAppComposeConfig
from ._constants import (
    API_VERSION_HEADER_NAME,
    APP_ID_HEADER_NAME,
    AUTH_HEADER_NAME,
    HIT_ID_HEADER_NAME,
    HTTP_METHODS,
    UNVERSIONED,
    UNVERSIONED_DISPLAY_LABEL,
    VERSIONING_SETTINGS_STATE_KEY,
)
from ._core import (
    map_version_path,
    normalize_prefix,
    normalize_unversioned_label,
    normalize_version,
    resolve_prefix,
    resolve_version,
    validate_version_mapping_keys,
)
from ._dependencies import (
    ApiVersionDep,
    AppIdDep,
    HitIdDep,
    param_factory,
    uuid_id_factory,
)
from ._fastapi_types import (
    ExceptionHandlerProvider,
    ExHandler,
    Middleware,
    NormalizedDependencySpec,
    PathParamDependencies,
    PathParamDependencySpec,
    VersionedAppConfigurer,
    VersionedAppLifespan,
)
from ._helpers import (
    HeadersGetter,
    find_bearer,
    find_token,
)
from ._orchestration import (
    compose_versioned_apps,
    configure_versioned_api,
    default_exception_handlers_provider,
    get_current_user_claims,
)
from ._settings import VersioningSettings, load_app_name, load_versioning_settings
from ._swagger_ui_version import SWAGGER_UI_VERSION
from ._types import VersionedAppState, VersionKey, VersionMap
from .extensions import Extension, ExtensionContext
from .extensions.actuator import ActuatorExtension, register_actuator_router
from .extensions.swagger_ui import SwaggerDocsExtension

__all__ = (
    "API_VERSION_HEADER_NAME",
    "APP_ID_HEADER_NAME",
    "AUTH_HEADER_NAME",
    "HIT_ID_HEADER_NAME",
    "HTTP_METHODS",
    "SWAGGER_UI_VERSION",
    "UNVERSIONED",
    "UNVERSIONED_DISPLAY_LABEL",
    "VERSIONING_SETTINGS_STATE_KEY",
    "ActuatorExtension",
    "ApiVersionDep",
    "AppIdDep",
    "ExHandler",
    "ExceptionHandlerProvider",
    "Extension",
    "ExtensionContext",
    "HeadersGetter",
    "HitIdDep",
    "Middleware",
    "NormalizedDependencySpec",
    "PathParamDependencies",
    "PathParamDependencySpec",
    "SwaggerDocsExtension",
    "VersionKey",
    "VersionMap",
    "VersionedApiConfig",
    "VersionedAppComposeConfig",
    "VersionedAppConfigurer",
    "VersionedAppLifespan",
    "VersionedAppState",
    "VersioningSettings",
    "compose_versioned_apps",
    "configure_versioned_api",
    "default_exception_handlers_provider",
    "find_bearer",
    "find_token",
    "get_current_user_claims",
    "load_app_name",
    "load_versioning_settings",
    "map_version_path",
    "normalize_prefix",
    "normalize_unversioned_label",
    "normalize_version",
    "param_factory",
    "register_actuator_router",
    "resolve_prefix",
    "resolve_version",
    "uuid_id_factory",
    "validate_version_mapping_keys",
)
