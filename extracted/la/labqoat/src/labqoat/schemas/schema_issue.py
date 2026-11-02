"""Source-independent JSON Pointer diagnostics from schema validation."""

from dataclasses import dataclass


@dataclass(frozen=True)
class SchemaIssue:
    """Identify the invalid value, constraining schema, and diagnostic message."""

    pointer: str
    schema_pointer: str
    message: str
