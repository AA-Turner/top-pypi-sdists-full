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

        return ComponentSchema(
            title=doc.name,
            description=doc.description,
            properties=properties,
            required=required
        )

    def to_json(self, schema: ComponentSchema) -> str:
        """Serialize schema to formatted JSON string.

        Args:
            schema: ComponentSchema to serialize.

        Returns:
            Formatted JSON string representation of the schema.
        """
        # Build the full JSON Schema document
        schema_dict = {
            "$schema": self.SCHEMA_DRAFT,
            "type": schema.type,
            "title": schema.title,
            "description": schema.description,
            "properties": schema.properties,
        }

        # Only include required array if there are required fields
        if schema.required:
            schema_dict["required"] = schema.required

        return orjson.dumps(
            schema_dict,
            option=orjson.OPT_INDENT_2
        ).decode('utf-8')

    def to_dict(self, schema: ComponentSchema) -> Dict[str, Any]:
        """Convert schema to dictionary for further processing.

        Args:
            schema: ComponentSchema to convert.

        Returns:
            Dictionary representation of the schema.
        """
        result = {
            "$schema": self.SCHEMA_DRAFT,
            "type": schema.type,
            "title": schema.title,
            "description": schema.description,
            "properties": schema.properties,
        }

        if schema.required:
            result["required"] = schema.required

        return result
