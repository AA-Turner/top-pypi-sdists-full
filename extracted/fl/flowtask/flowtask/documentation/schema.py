"""JSON Schema generator for Flowtask components.

This module provides the SchemaGenerator class that creates JSON Schema
definitions from parsed ComponentDoc objects. The schemas can be used for
IDE autocomplete and validation of YAML task definitions.
"""
import orjson
from typing import Dict, Any
from .models import ComponentDoc, ComponentSchema


class SchemaGenerator:
    """Generate JSON Schema from ComponentDoc.

    This class transforms parsed component documentation into JSON Schema
    format (draft-07 compatible). The schema includes:
    - Component name as title
    - Component description
    - Properties for each attribute with descriptions
    - Required array for mandatory attributes

    Example usage::

        from flowtask.documentation import DocstringParser, SchemaGenerator

        parser = DocstringParser()
        generator = SchemaGenerator()

        doc = parser.parse(MyComponent.__doc__)
        schema = generator.generate(doc)
        json_str = generator.to_json(schema)
    """

    # JSON Schema draft version
    SCHEMA_DRAFT = "http://json-schema.org/draft-07/schema#"

    def generate(self, doc: ComponentDoc) -> ComponentSchema:
        """Generate JSON Schema from component documentation.

        Args:
            doc: Parsed component documentation.

        Returns:
            ComponentSchema with properties and required fields populated.
        """
        properties: Dict[str, Dict[str, Any]] = {}
        required: list = []

        for attr in doc.attributes:
            # Build property definition
            prop_def: Dict[str, Any] = {
                "type": "string",  # Default type for all attributes
                "description": attr.description
            }

            # Add default value if available
            if attr.default is not None:
                prop_def["default"] = attr.default

            properties[attr.name] = prop_def

            # Track required fields
            if attr.required:
                required.append(attr.name)

        schema = ComponentSchema(
            title=doc.name,
            description=doc.description,
            properties=properties,
            required=required
        )
        # Dataflow contract — non-standard but retained by every JSON Schema
        # validator (`x-` is the conventional extension namespace).
        schema.io = {
            "consumes": doc.consumes or "any",
            "produces": doc.produces or "any",
        }
        return schema

    def to_json(self, schema: ComponentSchema) -> str:
        """Serialize schema to formatted JSON string."""
        return orjson.dumps(
            self.to_dict(schema),
            option=orjson.OPT_INDENT_2,
        ).decode("utf-8")

    def to_dict(self, schema: ComponentSchema) -> Dict[str, Any]:
        """Convert schema to a JSON-Schema-compatible dict.

        Includes the ``x-flowtask-io`` extension carrying the component's
        ``{consumes, produces}`` dataflow contract — consumers that ignore
        extension keys (most standard validators) silently skip it.
        """
        result: Dict[str, Any] = {
            "$schema": self.SCHEMA_DRAFT,
            "type": schema.type,
            "title": schema.title,
            "description": schema.description,
            "properties": schema.properties,
        }

        if schema.required:
            result["required"] = schema.required

        # Non-standard extension. Keep it last so the standard sections
        # remain at the top of the file for human readers.
        result["x-flowtask-io"] = dict(schema.io)

        return result
