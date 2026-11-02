"""Render deterministic typed records from already checked schema field descriptions."""

from dataclasses import dataclass

from labqoat.schema_codegen.field_name import FieldName
from labqoat.schema_codegen.record_field import RecordField
from labqoat.schema_codegen.schema_expression import SchemaExpression
from labqoat.schemas.schema_document import SchemaDocument


@dataclass(frozen=True)
class RecordSource:
    """Emit ordinary inspectable Python declarations with full schema validation metadata."""

    name: str
    schema: SchemaDocument
    fields: tuple[RecordField, ...]

    def render(self) -> str:
        """Keep output independent of data revision selection, source order and timestamps."""
        sections = [self._imports(), self._declaration(), self._encoder(), self._decoder()]
        return "\n\n".join(sections) + "\n"

    def _imports(self) -> str:
        """Import only declarations needed by this generated record."""
        types = "ClassVar, Self, cast" if self.fields else "ClassVar, Self"
        if any("Literal[" in field.type.annotation for field in self.fields):
            types += ", Literal"
        record = "Missing, SchemaRecord" if any(not field.required for field in self.fields) else "SchemaRecord"
        shape = self._shape_imports()
        references = self._reference_imports()
        records = sorted({name for field in self.fields for name in field.type.records})
        imports = "".join(f"\nfrom .{FieldName.module(name)} import {name}" for name in records)
        return (
            f'"""Generated {self.name} schema record; regenerate from its captured schema."""\n\n'
            "from dataclasses import dataclass\nfrom types import MappingProxyType\n"
            f"from typing import {types}\nfrom collections.abc import Mapping\n\n"
            "from labqoat.json_document import JsonDocument\n"
            f"from labqoat.schemas import Identity, {record}\n"
            f"from labqoat.schemas.schema_document import SchemaDocument{shape}{references}{imports}"
        )

    def _declaration(self) -> str:
        """Bind the complete canonical schema and an explicit JSON-to-Python name mapping."""
        mapping = {field.name: field.python_name for field in self.fields}
        schema = SchemaExpression.render(self.schema)
        declarations = [
            "@dataclass(frozen=True, slots=True, kw_only=True)",
            f"class {self.name}(SchemaRecord):",
            f'    """Generated validated {self.name} fields and constructor."""',
            f"    _schema: ClassVar[SchemaDocument] = {schema}",
            f"    schema_digest: ClassVar[str] = {self.schema.digest!r}",
            f"    field_names: ClassVar[Mapping[str, str]] = MappingProxyType({mapping!r})",
        ]
        if self.fields:
            shapes = ", ".join(field.type.shape for field in self.fields)
            declarations.append(f"    _shapes: ClassVar[tuple[ValueDecoder, ...]] = ({shapes},)")
        return "\n".join([*declarations, *(field.declaration() for field in self.fields)])

    def _shape_imports(self) -> str:
        """Import union decoding only for shapes that actually contain structural alternatives."""
        if not self.fields:
            return ""
        imports = "\nfrom labqoat.schemas.value_decoder import ValueDecoder"
        for name in ("ValueShape", "ValueUnion"):
            if any(name + "(" in field.type.shape for field in self.fields):
                module = {"ValueShape": "value_shape", "ValueUnion": "value_union"}[name]
                imports += f"\nfrom labqoat.schemas.{module} import {name}"
        return imports

    def _reference_imports(self) -> str:
        """Keep external reference imports explicit and free of unused declarations."""
        references = [name for name in ("AssetRef",) if any(name in field.type.annotation for field in self.fields)]
        return "\nfrom labqoat.references import " + ", ".join(references) if references else ""

    def _encoder(self) -> str:
        """Serialize exact JSON property names while preserving optional missing fields."""
        lines = [
            "    def _encode(self) -> dict[str, object]:",
            '        """Encode declared fields without coercion or implicit defaults."""',
        ]
        if not self.fields:
            return "\n".join([*lines, "        return {}"])
        lines.append("        values: dict[str, object] = {")
        lines.extend(f"            {field.name!r}: self.{field.python_name}," for field in self.fields)
        lines.append("        }")
        encoded = "values"
        if any(not field.required for field in self.fields):
            encoded = "{name: value for name, value in values.items() if not isinstance(value, Missing)}"
        return "\n".join([*lines, f"        return {encoded}"])

    def _decoder(self) -> str:
        """Construct a fully typed record from values already checked against its entire schema."""
        lines = [
            "    @classmethod",
            "    def _decode(cls, values: JsonDocument) -> Self:",
            '        """Restore generated field types from fully validated JSON values."""',
            "        return cls(",
            *(field.decoder(index) for index, field in enumerate(self.fields)),
            "        )",
        ]
        return "\n".join(lines)
