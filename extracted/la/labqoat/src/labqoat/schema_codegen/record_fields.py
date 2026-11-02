"""Closed record field compilation shared by root and nested generated models."""

from labqoat.json_document import JsonDocument
from labqoat.schema_codegen.field_name import FieldName
from labqoat.schema_codegen.record_field import RecordField
from labqoat.schema_codegen.schema_types import SchemaTypes


class RecordFields:
    """Keep constructor limits and JSON-name allocation consistent at every record position."""

    @staticmethod
    def compile(root: JsonDocument, types: SchemaTypes, pointer: str, depth: int) -> tuple[RecordField, ...]:
        """Require explicit finite properties rather than introducing open untyped mappings."""
        raw = root.get("type")
        kinds = raw if isinstance(raw, list) else [raw]
        if "object" not in kinds or root.get("additionalProperties") is not False or root.get("patternProperties"):
            raise ValueError(f"{pointer or '/'}: Python records require a closed object with fixed properties")
        properties = JsonDocument.expect_dict(root.get("properties", {}))
        if len(properties) > 8:
            raise ValueError(f"{pointer}/properties: generated constructors support at most eight explicit fields")
        required = JsonDocument.expect_list(root.get("required", []))
        if any(name not in properties for name in required):
            raise ValueError(f"{pointer}/required: every required field must have a declared Python shape")
        used: set[str] = set()
        fields = []
        for name in sorted(properties):
            location = pointer + "/properties/" + name.replace("~", "~0").replace("/", "~1")
            fields.append(
                RecordField(
                    name,
                    FieldName.allocate(name, used),
                    types.field(properties[name], location, depth),
                    name in required,
                )
            )
        return tuple(fields)
