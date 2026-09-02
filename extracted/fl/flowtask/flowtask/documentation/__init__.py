"""Flowtask component documentation utilities.

This package provides tools for extracting, generating, and serving
documentation for Flowtask components.

Modules:
    models: Pydantic models for documentation data structures.
    parser: DocstringParser for extracting docs from component classes.
    schema: SchemaGenerator for creating JSON Schemas from docs.
    generator: ComponentDocGenerator for orchestrating doc generation.
"""
from .models import (
    ComponentAttribute,
    ComponentDoc,
    ComponentSchema,
    ComponentDocResponse,
    DocumentationIndex,
)
from .parser import DocstringParser
from .schema import SchemaGenerator
from .generator import ComponentDocGenerator

__all__ = [
    "ComponentAttribute",
    "ComponentDoc",
    "ComponentSchema",
    "ComponentDocResponse",
    "DocumentationIndex",
    "DocstringParser",
    "SchemaGenerator",
    "ComponentDocGenerator",
]
