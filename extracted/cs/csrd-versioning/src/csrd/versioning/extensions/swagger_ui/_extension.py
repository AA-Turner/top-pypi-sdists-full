"""Swagger docs extension — built-in extension for per-version Swagger UI."""

from collections.abc import Sequence

from fastapi import FastAPI

from .._types import ExtensionContext
from ._base import SwaggerPlugin


class SwaggerDocsExtension:
    """Built-in extension that registers per-version Swagger UI and OpenAPI routes.

    Wraps :func:`_register_custom_docs` behind the unified
    :class:`Extension` protocol.  Consumers inject sub-plugins via
    ``VersionedApiConfig.swagger_plugins``; the orchestration layer
    calls :meth:`add_plugins` before :meth:`apply`.

    Parameters
    ----------
    enabled:
        Set to ``False`` to disable this extension.
    include_info_endpoints:
        Whether to register the ``/info`` introspection endpoints.
    include_root_favicon_alias:
        Whether to register a root ``/favicon.ico`` redirect.
    """

    name: str = "swagger_docs"
    order: int = 90
    enabled: bool = True

    def __init__(
        self,
        *,
        enabled: bool = True,
        include_info_endpoints: bool = True,
        include_root_favicon_alias: bool = True,
    ) -> None:
        self.enabled = enabled
        self._include_info_endpoints = include_info_endpoints
        self._include_root_favicon_alias = include_root_favicon_alias
        self._plugins: list[SwaggerPlugin] = []

    def add_plugins(self, plugins: Sequence[SwaggerPlugin]) -> None:
        """Inject consumer-provided swagger plugins.

        Called by the orchestration layer before :meth:`apply`.
        These plugins are merged with defaults inside
        :func:`_resolve_swagger_plugins` using by-name override.
        """
        self._plugins.extend(plugins)

    def apply(self, app: FastAPI, ctx: ExtensionContext) -> None:
        """Register Swagger UI, OpenAPI JSON, and ReDoc routes on *app*."""
        from ..._docs import _register_custom_docs

        _register_custom_docs(
            app,
            version_mapping=ctx.version_mapping,
            prefix=ctx.prefix,
            app_name=ctx.app_name,
            hit_id_header=ctx.hit_id_header,
            app_id_header=ctx.app_id_header,
            default_version=ctx.default_version,
            strict_version_matching=ctx.strict_version_matching,
            include_info_endpoints=self._include_info_endpoints,
            build_tag=ctx.build_tag,
            include_root_favicon_alias=self._include_root_favicon_alias,
            swagger_plugins=self._plugins or None,
        )
