"""Deterministic class-per-file generation for finite nested schema record graphs."""

import re

from labqoat.json_document import JsonValue
from labqoat.schema_codegen.field_name import FieldName
from labqoat.schema_codegen.field_type import FieldType
from labqoat.schema_codegen.record_fields import RecordFields
from labqoat.schema_codegen.record_source import RecordSource
from labqoat.schema_codegen.schema_projection import SchemaProjection
from labqoat.schema_codegen.schema_types import SchemaTypes


class RecordGraph:
    """Own one generated package, its names and its full captured-schema validation projections."""

    def __init__(self, schema: dict[str, JsonValue], name: str) -> None:
        """Bind generation to static JSON alone and reject unsafe public names before writing anything."""
        FieldName.module(name)
        self.root = name
        self.schema = schema
        self.projection = SchemaProjection(schema)
        self.types = SchemaTypes(schema, self.record, self.projection)
        self.names: set[str] = {name}
        self.sources: dict[str, str] = {}

    def generate(self) -> dict[str, str]:
        """Return all declarations and explicit public re-exports in deterministic order."""
        return self.render(self.root_record())

    def root_record(self) -> RecordSource:
        """Compile ordinary fields before a workload attaches its explicit input bindings."""
        return self._record_source(self.schema, "", 0, self.root)

    def render(self, root: RecordSource) -> dict[str, str]:
        """Render the root alongside every nested class discovered from the captured schema."""
        self.sources[FieldName.module(self.root) + ".py"] = root.render()
        exports = sorted(self.names)
        imports = "\n".join(f"from .{FieldName.module(name)} import {name}" for name in exports)
        self.sources["__init__.py"] = (
            f'"""Generated captured-schema public records."""\n\n{imports}\n\n__all__ = {exports!r}\n'
        )
        return dict(sorted(self.sources.items()))

    def record(self, value: JsonValue, pointer: str, depth: int) -> FieldType:
        """Allocate a stable explicit class for a nested object, including nullable objects and array items."""
        parts = re.findall(r"[a-zA-Z0-9]+", pointer)
        base = self.root + "".join(part[:1].upper() + part[1:] for part in parts if part != "properties")
        name, suffix = base, 2
        while name in self.names:
            name = f"{base}{suffix}"
            suffix += 1
        self.names.add(name)
        self.sources[FieldName.module(name) + ".py"] = self._record_source(value, pointer, depth + 1, name).render()
        return FieldType(name, f"ValueShape(('object',), record={name})", (name,))

    def _record_source(self, value: JsonValue, pointer: str, depth: int, name: str) -> RecordSource:
        """Keep original reference siblings in validation while resolving the structural field declaration."""
        node, location = self.types.locate(value, pointer)
        fields = RecordFields.compile(node, self.types, location, depth)
        return RecordSource(name, self.projection.capture(pointer), fields)
