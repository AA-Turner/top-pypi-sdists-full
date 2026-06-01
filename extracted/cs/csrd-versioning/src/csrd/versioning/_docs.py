"""Custom Swagger UI, per-version OpenAPI JSON, and introspection endpoint registration."""

import asyncio
import copy
import json
import logging
import re
from collections.abc import Awaitable, Callable
from html import escape
from importlib.resources import files
from typing import Any

import httpx
from fastapi import APIRouter, FastAPI
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from fastapi.routing import APIRoute

from csrd.versioning._constants import API_VERSION_HEADER_NAME, HTTP_METHODS
from csrd.versioning._core import (
    normalize_prefix as _normalize_prefix,
)
from csrd.versioning._core import (
    normalize_unversioned_label as _normalize_unv,
)
from csrd.versioning._core import (
    normalize_version as _normalize_version,
)

from ._fastapi_types import VersionKey, VersionMap
from ._redoc import _register_redoc_routes
from ._swagger_ui_version import (
    SWAGGER_UI_CSS_SRI,
    SWAGGER_UI_JS_SRI,
    SWAGGER_UI_STANDALONE_JS_SRI,
    SWAGGER_UI_VERSION,
)
from .extensions.swagger_ui._base import (
    SchemaContext,
    SwaggerPlugin,
    _aggregate_bundle_plugins,
    _aggregate_css,
    _aggregate_js,
    _collect_contributions,
    _collect_schema_patchers,
    _resolve_swagger_plugins,
    _warn_css_conflicts,
    apply_schema_patchers,
)

logger = logging.getLogger(__name__)

_TEMPLATE_PACKAGE = "csrd.versioning.templates"


def _load_template(template_name: str) -> str:
    """Load a template or asset file from package templates."""
    return files(_TEMPLATE_PACKAGE).joinpath(template_name).read_text(encoding="utf-8")


def _build_version_options(version_list: list[str]) -> str:
    """Build HTML <option> entries for version select."""
    return "\n".join(
        f'<option value="{escape(version.lower())}">{escape(version)}</option>'
        for version in version_list
    )


def _build_swagger_urls_json(version_list: list[str]) -> str:
    """Build JSON list of version names for SwaggerUI `urls` config."""
    return json.dumps(version_list).replace("</", "<\\/")


def _render_swagger_ui_html(
    *,
    version_list: list[str],
    app_name: str,
    hit_id_header: str,
    app_id_header: str,
    default_version: str | None = None,
    build_tag: str | None = None,
    plugin_css: str = "",
    plugin_js: str = "",
    bundle_plugins: str = "",
) -> str:
    """Render Swagger UI HTML from combined template with plugin overrides."""
    template = _load_template("swagger_ui_template.html")
    swagger_urls_json = _build_swagger_urls_json(version_list)

    swagger_config_json = json.dumps(
        {
            "appName": app_name,
            "appIdHeader": app_id_header,
            "hitIdHeader": hit_id_header,
            "versionHeader": API_VERSION_HEADER_NAME,
            "defaultVersion": default_version,
        }
    ).replace("</", "<\\/")

    build_tag_value = (build_tag or "").strip()
    build_tag_segment = ""
    if build_tag_value:
        build_tag_segment = (
            f'<span class="docs-footer-build-tag">V: {escape(build_tag_value)}</span>'
        )

    bundle_plugins_value = bundle_plugins

    return (
        template.replace("__SWAGGER_UI_VERSION__", SWAGGER_UI_VERSION)
        .replace("__SRI_CSS__", SWAGGER_UI_CSS_SRI)
        .replace("__SRI_JS__", SWAGGER_UI_JS_SRI)
        .replace("__SRI_STANDALONE_JS__", SWAGGER_UI_STANDALONE_JS_SRI)
        .replace("__SWAGGER_URLS_JSON__", swagger_urls_json)
        .replace("__PLUGIN_CSS__", plugin_css)
        .replace("__PLUGIN_JS__", plugin_js)
        .replace("__SWAGGER_CONFIG_JSON__", swagger_config_json)
        .replace("__BUILD_TAG_SEGMENT__", build_tag_segment)
        .replace("__BUNDLE_PLUGINS__", bundle_plugins_value)
    )


def _deduplicate_operation_ids(app: FastAPI) -> None:
    """Ensure OpenAPI operation ids are unique within an app."""
    operation_ids: set[str] = set()
    for route in app.routes:
        if isinstance(route, APIRoute):
            base_id = route.operation_id or route.name
            if base_id not in operation_ids:
                route.operation_id = base_id
                operation_ids.add(base_id)
            else:
                counter = 2
                while f"{base_id}_{counter}" in operation_ids:
                    counter += 1
                deduped_id = f"{base_id}_{counter}"
                route.operation_id = deduped_id
                operation_ids.add(deduped_id)


def _extract_path_param_order(path: str) -> dict[str, int]:
    """Return path-parameter names mapped to their declaration order."""
    names = re.findall(r"{([^{}]+)}", path)
    return {name: i for i, name in enumerate(names)}


def _sort_openapi_path_params_inplace(schema: dict[str, Any]) -> None:
    """Sort OpenAPI operation parameters so path params follow URL template order."""
    paths = schema.get("paths", {})
    for path, path_item in paths.items():
        order = _extract_path_param_order(path)

        def _key(
            item: tuple[int, dict[str, Any]], order: dict[str, int] = order
        ) -> tuple[int, int, int]:
            idx, p = item
            loc = p.get("in")
            name = p.get("name", "")
            if loc == "path":
                return (0, order.get(name, 10_000), idx)
            return (1, 0, idx)

        for method, op in path_item.items():
            if method not in HTTP_METHODS:
                continue

            params: list[dict[str, Any]] = op.get("parameters", [])
            if not params:
                continue

            indexed = list(enumerate(params))
            op["parameters"] = [p for _, p in sorted(indexed, key=_key)]


def _normalized_version_labels(version_mapping: VersionMap) -> list[str]:
    """Return display labels for configured versions."""
    labels = [_normalize_unv(version) for version in version_mapping]

    def _key(label: str) -> tuple[int, tuple[int, ...], str]:
        normalized = _normalize_version(label)
        if normalized == "unv":
            return (0, (), "")

        numeric_parts = tuple(int(part) for part in re.findall(r"\d+", normalized))
        if numeric_parts:
            return (2, numeric_parts, "")

        return (1, (), normalized)

    return sorted(labels, key=_key)


def _build_version_openapi_schema(
    versioned_app: FastAPI,
    *,
    prefix: str,
    version_key: VersionKey,
    schema_patchers: list | None = None,
) -> dict[str, Any]:
    """Build a per-version OpenAPI schema with normalized paths/version info."""
    _deduplicate_operation_ids(versioned_app)

    normalized_prefix = _normalize_prefix(prefix)
    openapi_schema = copy.deepcopy(versioned_app.openapi())
    existing_paths = dict(openapi_schema.get("paths", {}))
    prefixed_paths: dict[str, Any] = {}

    for path, path_item in existing_paths.items():
        if path.startswith(normalized_prefix):
            prefixed_paths[path] = path_item
        else:
            prefixed_paths[f"{normalized_prefix}{path}"] = path_item

    openapi_schema["paths"] = prefixed_paths
    openapi_schema["info"]["version"] = _normalize_unv(version_key)
    _sort_openapi_path_params_inplace(openapi_schema)

    if schema_patchers:
        ctx = SchemaContext(
            app=versioned_app,
            version_key=version_key,
            prefix=normalized_prefix,
        )
        openapi_schema = apply_schema_patchers(openapi_schema, ctx, schema_patchers)

    return openapi_schema


def _build_openapi_doc_endpoint(
    *,
    version_mapping: VersionMap,
    version_key: VersionKey,
    prefix: str,
    schema_patchers: list | None = None,
) -> Callable[[], Awaitable[dict[str, Any]]]:
    cached_schema: dict[str, Any] | None = None

    async def _doc_endpoint() -> dict[str, Any]:
        nonlocal cached_schema
        if cached_schema is None:
            versioned_app = version_mapping[version_key]
            cached_schema = _build_version_openapi_schema(
                versioned_app,
                prefix=prefix,
                version_key=version_key,
                schema_patchers=schema_patchers,
            )
        return copy.deepcopy(cached_schema)

    return _doc_endpoint


def _register_swagger_ui_routes(
    app: FastAPI,
    *,
    version_list: list[str],
    app_name: str,
    hit_id_header: str,
    app_id_header: str,
    default_version: str | None = None,
    build_tag: str | None = None,
    include_root_favicon_alias: bool = True,
    plugin_css: str = "",
    plugin_js: str = "",
    bundle_plugins: str = "",
) -> None:
    _SECURITY_HEADERS = {
        "X-Content-Type-Options": "nosniff",
        "X-Frame-Options": "DENY",
    }

    def _has_get_route(path: str) -> bool:
        return any(
            isinstance(route, APIRoute) and route.path == path and "GET" in route.methods
            for route in app.routes
        )

    @app.get("/", include_in_schema=False)
    async def redirect_to_docs() -> RedirectResponse:
        return RedirectResponse(url="/swagger-ui/index.html")

    @app.get("/docs", include_in_schema=False)
    async def redirect_docs_to_swagger() -> RedirectResponse:
        return RedirectResponse(url="/swagger-ui/index.html")

    @app.get("/swagger-ui", include_in_schema=False)
    async def redirect_to_docs_() -> RedirectResponse:
        return RedirectResponse(url="/swagger-ui/index.html")

    _cached_html = _render_swagger_ui_html(
        version_list=version_list,
        app_name=app_name,
        hit_id_header=hit_id_header,
        app_id_header=app_id_header,
        default_version=default_version,
        build_tag=build_tag,
        plugin_css=plugin_css,
        plugin_js=plugin_js,
        bundle_plugins=bundle_plugins,
    )

    @app.get("/swagger-ui/index.html", include_in_schema=False)
    async def custom_docs() -> HTMLResponse:
        return HTMLResponse(_cached_html, headers=_SECURITY_HEADERS)

    _favicon_bytes = files(_TEMPLATE_PACKAGE).joinpath("favicon.png").read_bytes()

    @app.get("/swagger-ui/favicon.png", include_in_schema=False)
    async def favicon() -> Response:
        return Response(
            content=_favicon_bytes,
            media_type="image/png",
            headers={
                **_SECURITY_HEADERS,
                "Cache-Control": "public, max-age=86400",
            },
        )

    if include_root_favicon_alias and not _has_get_route("/favicon.ico"):

        @app.get("/favicon.ico", include_in_schema=False)
        async def root_favicon() -> Response:
            return Response(
                content=_favicon_bytes,
                media_type="image/png",
                headers={
                    **_SECURITY_HEADERS,
                    "Cache-Control": "public, max-age=86400",
                },
            )


def _register_openapi_json_routes(
    app: FastAPI,
    *,
    version_mapping: VersionMap,
    prefix: str,
    schema_patchers: list | None = None,
) -> None:
    """Register ``/openapi/{version}.json`` routes for each configured version."""
    doc_router = APIRouter(prefix="/openapi")

    for api in version_mapping:
        normalized_label = _normalize_unv(api)
        url = f"/{normalized_label.lower()}.json"
        name = f"version_{normalized_label.replace('-', '_')}"

        doc_router.add_api_route(
            url,
            _build_openapi_doc_endpoint(
                version_mapping=version_mapping,
                version_key=api,
                prefix=prefix,
                schema_patchers=schema_patchers,
            ),
            methods=["GET"],
            name=name,
            include_in_schema=False,
        )

    app.include_router(doc_router)


def _register_info_endpoints(
    app: FastAPI,
    *,
    version_list: list[str],
    prefix: str,
    app_name: str,
    default_version: VersionKey | None,
    strict_version_matching: bool,
) -> None:
    """Register ``/_info`` and ``/_info/health`` introspection routes."""

    @app.get("/_info", include_in_schema=False)
    async def versioning_info() -> dict[str, Any]:
        return {
            "app_name": app_name,
            "prefix": prefix,
            "versions": version_list,
            "default_version": (
                _normalize_unv(default_version) if default_version is not None else None
            ),
            "strict_version_matching": strict_version_matching,
            "docs": "/swagger-ui/index.html",
        }

    @app.get("/_info/health", include_in_schema=False)
    async def versioning_health() -> dict[str, Any]:
        health_path = f"{_normalize_prefix(prefix)}/health"

        async def _probe(label: str, client: httpx.AsyncClient) -> tuple[str, dict]:
            try:
                r = await client.get(
                    health_path,
                    headers={API_VERSION_HEADER_NAME: label.lower()},
                )
                if r.status_code == 200:
                    try:
                        body = r.json()
                    except Exception:
                        body = None
                    return label, {"status": "ok", "code": 200, "response": body}
                elif r.status_code == 404:
                    return label, {"status": "not_found", "code": 404, "response": None}
                else:
                    return label, {
                        "status": "error",
                        "code": r.status_code,
                        "response": None,
                    }
            except Exception:
                logger.warning("Health probe failed for version %s", label, exc_info=True)
                return label, {"status": "error", "code": 0, "response": None}

        transport = httpx.ASGITransport(app=app)
        async with httpx.AsyncClient(
            transport=transport, base_url="http://internal", timeout=1.0
        ) as client:
            pairs = await asyncio.gather(*(_probe(label, client) for label in version_list))

        return {label: result for label, result in pairs}


def _register_custom_docs(
    app: FastAPI,
    version_mapping: VersionMap,
    prefix: str,
    app_name: str,
    hit_id_header: str,
    app_id_header: str,
    default_version: "VersionKey | None" = None,
    strict_version_matching: bool = False,
    include_info_endpoints: bool = True,
    build_tag: str | None = None,
    include_root_favicon_alias: bool = True,
    swagger_plugins: list[SwaggerPlugin] | None = None,
) -> None:
    version_list = _normalized_version_labels(version_mapping)

    resolved_plugins = _resolve_swagger_plugins(swagger_plugins)
    contributions = _collect_contributions(resolved_plugins)
    _warn_css_conflicts(contributions)

    plugin_css = _aggregate_css(contributions)
    plugin_js = _aggregate_js(contributions)
    bundle_plugins = _aggregate_bundle_plugins(contributions)
    schema_patchers = _collect_schema_patchers(contributions)

    _register_swagger_ui_routes(
        app,
        version_list=version_list,
        app_name=app_name,
        hit_id_header=hit_id_header,
        app_id_header=app_id_header,
        default_version=(
            _normalize_unv(default_version).lower() if default_version is not None else None
        ),
        build_tag=build_tag,
        include_root_favicon_alias=include_root_favicon_alias,
        plugin_css=plugin_css,
        plugin_js=plugin_js,
        bundle_plugins=bundle_plugins,
    )

    if include_info_endpoints:
        _register_info_endpoints(
            app,
            version_list=version_list,
            prefix=prefix,
            app_name=app_name,
            default_version=default_version,
            strict_version_matching=strict_version_matching,
        )

    _register_openapi_json_routes(
        app,
        version_mapping=version_mapping,
        prefix=prefix,
        schema_patchers=schema_patchers or None,
    )

    _register_redoc_routes(
        app,
        version_list=version_list,
        default_version=(
            _normalize_unv(default_version).lower() if default_version is not None else None
        ),
    )
