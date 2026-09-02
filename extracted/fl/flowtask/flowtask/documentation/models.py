"""Pydantic models for component documentation.

This module defines the data structures used to represent parsed component
documentation, including attributes, examples, and JSON schemas.
"""
from typing import List, Literal, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field


# Enum of values a component can consume or produce through Flowtask's
# implicit `_result` channel. Used by the factory validator to detect
# incompatible step boundaries (e.g. Download produces 'file' but the
# next step expects 'dataframe' — bridge with OpenWithPandas).
IOType = Literal[
    "none",      # component does not use _result on this side
    "file",      # path(s) on disk
    "dataframe", # pandas DataFrame
    "recordset", # list of dicts / raw records
    "iterator",  # iterable that drives downstream loop semantics
    "any",       # polymorphic / passthrough — disables boundary checks
]


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
        examples: List of YAML/JSON example strings.
        schema: Final JSON Schema dict for the component, populated by the
            generator. The schema carries ``properties``, ``required``, and
            the ``x-flowtask-io`` dataflow contract.
        attributes: Parsed attributes from the docstring. Kept in-memory for
            the required-field reconciliation but excluded from the serialised
            doc.json — consumers should read ``schema`` instead.
        consumes / produces: Docstring overrides for the dataflow contract.
            Excluded from serialised doc.json (the cascade-resolved values are
            embedded in ``schema['x-flowtask-io']``).
    """
    name: str = ""
    version: Optional[str] = None
    category: str = "Other"
    description: str = ""
    examples: List[str] = Field(default_factory=list)
    # Serialised key is "schema"; the Python attribute is `schema_` so it
    # doesn't shadow Pydantic's BaseModel.schema attribute.
    schema_: Optional[Dict[str, Any]] = Field(default=None, alias="schema")

    # Internal-only fields — kept on the model so the parser + generator can
    # cooperate, but excluded from `model_dump()` so they don't leak into the
    # final doc.json.
    attributes: List[ComponentAttribute] = Field(
        default_factory=list, exclude=True
    )
    consumes: Optional[IOType] = Field(default=None, exclude=True)
    produces: Optional[IOType] = Field(default=None, exclude=True)

    model_config = {
        "populate_by_name": True,
    }


class ComponentSchema(BaseModel):
    """JSON Schema representation of a component.

    Attributes:
        type: JSON Schema type (always "object" for components).
        title: Component name as schema title.
        description: Component description.
        properties: Dict mapping attribute names to their schema definitions.
        required: List of required attribute names.
        io: Dataflow contract {"consumes": IOType, "produces": IOType} —
            emitted under the ``x-flowtask-io`` extension key by
            :meth:`SchemaGenerator.to_dict`.
    """
    type: str = "object"
    title: str
    description: str = ""
    properties: Dict[str, Dict[str, Any]] = Field(default_factory=dict)
    required: List[str] = Field(default_factory=list)
    io: Dict[str, str] = Field(
        default_factory=lambda: {"consumes": "any", "produces": "any"}
    )


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
        components: Dict mapping component names to their entry, with keys
            ``file`` (relative path to the merged doc.json), ``category`` and
            ``description``.
    """
    updated_at: datetime
    components: Dict[str, Dict[str, str]] = Field(default_factory=dict)
