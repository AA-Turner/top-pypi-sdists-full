"""Swagger UI plugin system for extending the custom docs rendering pipeline."""

from ._base import (
    SchemaContext,
    SwaggerPlugin,
    SwaggerPluginContribution,
    apply_schema_patchers,
)
from ._extension import SwaggerDocsExtension

__all__ = [
    "SchemaContext",
    "SwaggerDocsExtension",
    "SwaggerPlugin",
    "SwaggerPluginContribution",
    "apply_schema_patchers",
]
