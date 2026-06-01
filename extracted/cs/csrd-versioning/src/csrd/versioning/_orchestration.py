import inspect
import logging
from collections.abc import Mapping
from typing import Any

from fastapi import FastAPI
from starlette.types import ExceptionHandler

from csrd.context import (
    configure_headers_context_provider,
    get_api_version,
)
from csrd.context._fastapi_headers import get_headers as fastapi_get_headers
from csrd.context._fastapi_headers import headers_context as fastapi_headers_context
from csrd.context.platform import user_info_context
from csrd.models.claims import UserClaims
from csrd.versioning._constants import (
    APP_ID_HEADER_NAME,
    HIT_ID_HEADER_NAME,
    UNVERSIONED,
    VERSIONING_SETTINGS_STATE_KEY,
)
from csrd.versioning._core import (
    normalize_version,
    resolve_prefix,
    validate_version_mapping_keys,
)
from csrd.versioning._settings import load_app_name, load_versioning_settings

from . import _dependency_wiring as dependency_wiring
from ._config import VersionedApiConfig, VersionedAppComposeConfig
from ._dispatch import VersionDispatchMiddleware
from ._fastapi_types import (
    ExceptionHandlerProvider,
    ExHandler,
    Middleware,
    VersionKey,
    VersionMap,
)
from .extensions._types import Extension, ExtensionContext
from .extensions.actuator._extension import ActuatorExtension
from .extensions.swagger_ui._extension import SwaggerDocsExtension

logger = logging.getLogger(__name__)

_VERSIONING_CONFIGURED_KEY = "_versioning_configured"


def _default_extensions() -> list[Extension]:
    """Return the built-in extensions included by default."""
    return [ActuatorExtension(), SwaggerDocsExtension()]


def _resolve_extensions(config: VersionedApiConfig) -> list[Extension]:
    """Merge default extensions with user-provided overrides.

    Resolution rules:
    - Defaults load first.
    - User extensions override by name (last wins).
    - ``include_actuator_endpoints=False`` disables the actuator extension.
    - Consumer plugins are injected into built-ins via ``add_plugins()``.
    - Extensions with ``enabled=False`` are filtered out.
    - Remaining extensions are sorted by order (ascending).
    """
    resolved: dict[str, Extension] = {e.name: e for e in _default_extensions()}

    # User extensions override by name
    for ext in config.extensions:
        resolved[ext.name] = ext

    # Backward compat: include_actuator_endpoints=False disables actuator
    if not config.include_actuator_endpoints:
        act = resolved.get("actuator")
        if act is not None:
            act.enabled = False

    # Inject consumer plugins into built-in extensions
    act = resolved.get("actuator")
    if act is not None and config.actuator_plugins and hasattr(act, "add_plugins"):
        act.add_plugins(config.actuator_plugins)

    swag = resolved.get("swagger_docs")
    if swag is not None and config.swagger_plugins and hasattr(swag, "add_plugins"):
        swag.add_plugins(config.swagger_plugins)

    # Forward config options to swagger docs extension
    if swag is not None and isinstance(swag, SwaggerDocsExtension):
        swag._include_info_endpoints = config.include_info_endpoints
        swag._include_root_favicon_alias = config.include_root_favicon_alias

    return sorted(
        [e for e in resolved.values() if e.enabled],
        key=lambda e: e.order,
    )


def default_exception_handlers_provider() -> Mapping[int | type[Exception], ExceptionHandler]:
    """Return the default exception-handler map used by versioning integrations."""
    from csrd.versioning.exception_handlers import EXCEPTION_HANDLERS

    return EXCEPTION_HANDLERS  # type: ignore[return-value]


def get_current_user_claims() -> UserClaims | None:
    """Return current request user claims from FastAPI/platform contextvars."""
    return user_info_context.get()  # type: ignore[return-value]


def configure_versioned_api(
    app: FastAPI,
    version_mapping: VersionMap,
    config: VersionedApiConfig | None = None,
) -> None:
    """Configure versioned routing, docs, middleware, and exception handling."""
    config = config or VersionedApiConfig()

    if getattr(app.state, _VERSIONING_CONFIGURED_KEY, False):
        logger.warning("configure_versioned_api() already called on this app; skipping.")
        return

    exception_handler_provider = config.exception_handler_provider
    current_user_claims_provider = config.current_user_claims_provider
    if exception_handler_provider is None:
        exception_handler_provider = default_exception_handlers_provider
    if current_user_claims_provider is None:
        current_user_claims_provider = get_current_user_claims

    configure_headers_context_provider(
        get_headers=fastapi_get_headers,
        set_headers=fastapi_headers_context.set,
        reset_headers=fastapi_headers_context.reset,
    )

    if getattr(app.state, VERSIONING_SETTINGS_STATE_KEY, None) is None:
        setattr(app.state, VERSIONING_SETTINGS_STATE_KEY, load_versioning_settings())
    versioning_settings = getattr(app.state, VERSIONING_SETTINGS_STATE_KEY, None)

    if not version_mapping:
        raise ValueError("version_mapping cannot be empty. Provide at least one version mapping.")

    validate_version_mapping_keys(version_mapping)
    _propagate_state_to_versioned_apps(app, version_mapping)

    app_name = load_app_name(config.app_name)
    prefix = resolve_prefix(config.prefix)

    logger.info(
        "Configuring versioned API: app_name=%s, prefix=%s, versions=%s",
        app_name,
        prefix,
        [str(k) for k in version_mapping],
    )

    default_version = config.default_version
    if default_version is None:
        default_version = UNVERSIONED

    path_param_dependencies = list(config.path_param_dependencies)

    hit_id_header = config.hit_id_header
    if hit_id_header is None:
        hit_id_header = HIT_ID_HEADER_NAME

    app_id_header = config.app_id_header
    if app_id_header is None:
        app_id_header = APP_ID_HEADER_NAME

    resolved_handler_map = _resolve_exception_handlers(
        exception_handler_provider=exception_handler_provider,
        version_mapping=version_mapping,
        exception_handlers=list(config.ex_handlers) if config.ex_handlers else None,
    )

    documented_error_statuses = dependency_wiring._documented_error_statuses_from_handlers(
        resolved_handler_map=resolved_handler_map,
    )

    # Resolve and apply extensions (actuator, swagger docs, custom)
    resolved_extensions = _resolve_extensions(config)
    ext_ctx = ExtensionContext(
        app_name=app_name,
        prefix=prefix,
        version_mapping=version_mapping,
        hit_id_header=hit_id_header,
        app_id_header=app_id_header,
        default_version=default_version,
        strict_version_matching=config.strict_version_matching,
        build_tag=getattr(versioning_settings, "build_tag", None),
        settings=versioning_settings,
    )

    for ext in resolved_extensions:
        logger.debug("Applying extension '%s' (order=%d)", ext.name, ext.order)
        ext.apply(app, ext_ctx)

    dependency_wiring._mount_and_wire_versions(
        app=app,
        version_mapping=version_mapping,
        prefix=prefix,
        path_param_dependencies=path_param_dependencies,
        documented_error_statuses=documented_error_statuses,
    )
    _apply_middleware(
        app,
        prefix,
        version_mapping,
        list(config.middleware) if config.middleware else None,
        default_version,
        hit_id_header,
        app_id_header,
        config.strict_version_matching,
    )
    _apply_exception_handlers(app, resolved_handler_map)

    setattr(app.state, _VERSIONING_CONFIGURED_KEY, True)


def compose_versioned_apps(
    version_mapping: VersionMap,
    config: VersionedAppComposeConfig | None = None,
) -> FastAPI:
    """Compose multiple versioned FastAPI apps into a single root dispatcher.

    Takes a mapping of version keys to FastAPI instances and creates a root FastAPI app
    that dispatches incoming requests to the appropriate version based on routing rules.
    The root app handles version-aware middleware, exception handlers, docs, and actuator
    endpoints.
    """
    config = config or VersionedAppComposeConfig()

    app_kwargs: dict[str, Any] = {"title": config.title or load_app_name()}
    if config.lifespan is not None:
        app_kwargs["lifespan"] = config.lifespan

    # Disable FastAPI's built-in /docs — the versioning framework registers
    # its own per-version OpenAPI schemas at /openapi/{version}.json and a
    # custom Swagger UI at /swagger-ui/.
    # Disable FastAPI's built-in /docs and /redoc — the versioning framework
    # registers its own per-version equivalents at /swagger-ui/ and /redoc.
    app_kwargs.setdefault("docs_url", None)
    app_kwargs.setdefault("redoc_url", None)

    app = FastAPI(**app_kwargs)

    if config.app_state is not None:
        for state_key, state_value in config.app_state.items():
            setattr(app.state, state_key, state_value)

    if config.configure_app is not None:
        config.configure_app(app)

    configure_versioned_api(
        app=app,
        version_mapping=version_mapping,
        config=config.api,
    )

    return app


def _apply_middleware(
    app: FastAPI,
    prefix: str,
    version_mapping: VersionMap,
    middleware: list[Middleware] | None = None,
    default_version: VersionKey | None = None,
    hit_id_header: str = HIT_ID_HEADER_NAME,
    app_id_header: str = APP_ID_HEADER_NAME,
    strict_version_matching: bool = False,
) -> None:
    _register_middleware(app, middleware)

    app.add_middleware(
        VersionDispatchMiddleware,
        prefix=prefix,
        version_mapping=version_mapping,
        default_version=default_version,
        hit_id_header=hit_id_header,
        app_id_header=app_id_header,
        strict_version_matching=strict_version_matching,
    )


def _register_middleware(
    app: FastAPI,
    middleware: list[Middleware] | None,
) -> None:
    if middleware is None:
        return

    for m in middleware:
        if isinstance(m, tuple):
            cls, kwargs = m
            app.add_middleware(cls, **(kwargs or {}))  # type: ignore[arg-type]
        elif isinstance(m, type):
            app.add_middleware(m)  # type: ignore[arg-type]
        else:
            raise TypeError(
                f"middleware entries must be a class or (class, kwargs) tuple, got {type(m).__name__}"
            )

    logger.debug("Registered %d user-provided middleware entries", len(middleware))


def _is_builtin_exception_handler(handler: ExceptionHandler) -> bool:
    return getattr(handler, "__module__", "").startswith("fastapi.")


def _resolve_exception_handlers(
    *,
    exception_handler_provider: ExceptionHandlerProvider,
    version_mapping: VersionMap,
    exception_handlers: list[ExHandler] | None,
) -> dict[int | type[Exception], ExceptionHandler]:
    resolved_handler_map = dict(exception_handler_provider())

    per_version_handlers = _collect_sub_app_exception_handlers(version_mapping)
    for exc_key, version_handlers in per_version_handlers.items():
        fallback = resolved_handler_map.get(exc_key)
        resolved_handler_map[exc_key] = _make_version_scoped_handler(version_handlers, fallback)

    if exception_handlers is not None:
        for ex in exception_handlers:
            resolved_handler_map[ex[0]] = ex[1]

    return resolved_handler_map


def _make_version_scoped_handler(
    version_handlers: dict[str, ExceptionHandler],
    fallback: ExceptionHandler | None,
) -> ExceptionHandler:
    async def handler(request: Any, exc: Any) -> Any:
        version = get_api_version()
        version_handler = version_handlers.get(version) if version else None
        if version_handler is not None:
            result = version_handler(request, exc)
            return await result if inspect.isawaitable(result) else result
        if fallback is not None:
            result = fallback(request, exc)
            return await result if inspect.isawaitable(result) else result
        raise exc

    return handler


def _collect_sub_app_exception_handlers(
    version_mapping: VersionMap,
) -> dict[int | type[Exception], dict[str, ExceptionHandler]]:
    collected: dict[int | type[Exception], dict[str, ExceptionHandler]] = {}

    for version_key, versioned_app in version_mapping.items():
        normalized = normalize_version(version_key)
        for exc_key, handler in versioned_app.exception_handlers.items():
            if _is_builtin_exception_handler(handler):
                continue
            if exc_key not in collected:
                collected[exc_key] = {}
            collected[exc_key][normalized] = handler

    if collected:
        logger.debug(
            "Collected %d version-scoped exception handler(s) from sub-apps: %s",
            len(collected),
            [str(k) for k in collected],
        )

    return collected


def _apply_exception_handlers(
    app: FastAPI,
    resolved_handler_map: dict[int | type[Exception], ExceptionHandler],
) -> None:
    for exception_key, handler in resolved_handler_map.items():
        app.add_exception_handler(exception_key, handler)

    logger.debug(
        "Registered %d exception handlers: %s",
        len(resolved_handler_map),
        [str(k) for k in resolved_handler_map],
    )


def _propagate_state_to_versioned_apps(
    app: FastAPI,
    version_mapping: VersionMap,
) -> None:
    if not len(app.state):
        return

    for versioned_app in version_mapping.values():
        for key in app.state:
            if not hasattr(versioned_app.state, key):
                setattr(versioned_app.state, key, app.state[key])


__all__ = (
    "VersionMap",
    "VersionedApiConfig",
    "VersionedAppComposeConfig",
    "compose_versioned_apps",
    "configure_versioned_api",
    "default_exception_handlers_provider",
    "get_current_user_claims",
)
