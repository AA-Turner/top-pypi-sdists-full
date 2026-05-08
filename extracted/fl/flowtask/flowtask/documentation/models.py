"""Pydantic models for component documentation.

This module defines the data structures used to represent parsed component
documentation, including attributes, examples, and JSON schemas.
"""
from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field


class ComponentAttribute(BaseModel):
    """Single attribute definition from a component docstring.

    Attributes:
        name: The attribute name (e.g., 'credentials', 'timeout').
        required: Whether the attribute is required (Yes/No in docs).
        description: Human-readable description of the attribute.
        default: Default value if specified in the description.
    """
    name: str
    required: bool
    description: str
    default: Optional[str] = None


class ComponentDoc(BaseModel):
    """Documentation for a single Flowtask component.

    Attributes:
        name: The component class name (e.g., 'DownloadFromBase').
        version: Component version if available from _version attribute.
        category: High-level grouping (e.g., 'Sources', 'Outputs', 'Filters').
        description: Overview description extracted from docstring.
        attributes: List of parsed attributes from the documentation table.
        examples: List of YAML/JSON example strings.
    """
    name: str = ""
    version: Optional[str] = None
    category: str = "Other"
    description: str = ""
    attributes: List[ComponentAttribute] = Field(default_factory=list)
    examples: List[str] = Field(default_factory=list)


class ComponentSchema(BaseModel):
    """JSON Schema representation of a component.

    Attributes:
        type: JSON Schema type (always "object" for components).
        title: Component name as schema title.
        description: Component description.
        properties: Dict mapping attribute names to their schema definitions.
        required: List of required attribute names.
    """
    type: str = "object"
    title: str
    description: str = ""
    properties: Dict[str, Dict[str, Any]] = Field(default_factory=dict)
    required: List[str] = Field(default_factory=list)


class ComponentDocResponse(BaseModel):
    """API response format for component documentation.

    This is the format returned by the HTTP API endpoint.

    Attributes:
        schema_: JSON schema as a string (aliased to 'schema' in JSON).
        doc: Markdown documentation string.
        example: YAML/JSON example with preserved formatting.
    """
    schema_: str = Field(alias="schema")
    doc: str
    example: str

    class Config:
        populate_by_name = True


class DocumentationIndex(BaseModel):
    """Index of all documented components.

    Attributes:
        updated_at: Timestamp of last index update.
        components: Dict mapping component names to their file references.
    """
    updated_at: datetime
    components: Dict[str, Dict[str, str]] = Field(default_factory=dict)
