"""Validation-guided structural union decoding for generated Python models."""

from dataclasses import dataclass

from labqoat.json_document import JsonValue
from labqoat.schemas.schema_document import SchemaDocument
from labqoat.schemas.schema_validation_error import SchemaValidationError
from labqoat.schemas.value_decoder import ValueDecoder


@dataclass(frozen=True)
class ValueUnion:
    """Select the first valid structural branch; the full schema owns anyOf/oneOf cardinality."""

    branches: tuple[tuple[SchemaDocument, ValueDecoder], ...]

    def decode(self, value: JsonValue) -> object:
        """Retain branch constraints when scalar kinds overlap or objects use discriminating literals."""
        for schema, shape in self.branches:
            try:
                schema.validate(value)
            except SchemaValidationError:
                continue
            return shape.decode(value)
        raise ValueError("Value has no representable generated union branch")
