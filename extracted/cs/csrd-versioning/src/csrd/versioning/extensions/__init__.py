"""Unified extension system for versioned FastAPI applications.

Extensions are composable units of functionality (actuator endpoints,
swagger docs, custom admin panels, etc.) that wire themselves into the
app during ``configure_versioned_api()``.
"""

from ._types import Extension, ExtensionContext
from .actuator import ActuatorExtension
from .swagger_ui import SwaggerDocsExtension

__all__ = (
    "ActuatorExtension",
    "Extension",
    "ExtensionContext",
    "SwaggerDocsExtension",
)
