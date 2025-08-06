"""
Schema Export Module for Unified Configuration System

This module provides standalone functions to export configuration schemas in various formats:
- OpenAPI schemas in YAML or JSON format
- JSON schemas in YAML or JSON format

Usage:
    from schema_export import export_schema, to_openapi_schema, to_json_schema, to_dict

    # Export schema to file
    export_schema(CoreConfig, "schema.yaml")
    export_schema(CoreConfig, "schema.json", schema_type="json", format="json")

    # Generate schema in memory
    openapi_schema = to_openapi_schema(CoreConfig)
    json_schema = to_json_schema(CoreConfig)

    # Export config instance to dict
    config_instance = CoreConfig(name="myapp", port=8000)
    config_dict = to_dict(config_instance)

No external dependencies required for basic functionality.
PyYAML is optional for YAML export support.
"""

import json
import textwrap
from collections import OrderedDict
from typing import Any, Dict

try:
    import yaml

    HAS_YAML = True
except ImportError:
    HAS_YAML = False


def to_openapi_schema(config_class) -> Dict[str, Any]:
    """Generate OpenAPI schema for a configuration class.

    Args:
        config_class: The configuration class to generate schema for

    Returns:
        OpenAPI schema dictionary
    """
    return _generate_openapi_schema(config_class)


def to_json_schema(config_class) -> Dict[str, Any]:
    """Generate JSON schema for a configuration class.

    Args:
        config_class: The configuration class to generate schema for

    Returns:
        JSON schema dictionary
    """
    return _generate_json_schema(config_class)


def export_schema(
    config_class, filepath: str, schema_type: str = "openapi", format: str = "yaml"
) -> None:
    """Export configuration schema to file.

    Args:
        config_class: The configuration class to export schema for
        filepath: Path to save the schema file
        schema_type: Type of schema to generate ('openapi' or 'json')
        format: Output format ('yaml' or 'json')

    Examples:
        # Export OpenAPI schema as YAML (default)
        export_schema(CoreConfig, "schema.yaml")

        # Export JSON schema as YAML
        export_schema(CoreConfig, "schema.yaml", schema_type="json")

        # Export OpenAPI schema as JSON
        export_schema(CoreConfig, "schema.json", schema_type="openapi", format="json")

        # Export JSON schema as JSON
        export_schema(CoreConfig, "schema.json", schema_type="json", format="json")
    """
    # Validate inputs
    if schema_type.lower() not in ["openapi", "json"]:
        raise ValueError(
            f"Unsupported schema type: {schema_type}. Use 'openapi' or 'json'."
        )

    if format.lower() not in ["yaml", "json"]:
        raise ValueError(f"Unsupported format: {format}. Use 'yaml' or 'json'.")

    # Generate the appropriate schema
    if schema_type.lower() == "openapi":
        base_schema = _generate_openapi_schema(config_class)
        # Wrap in OpenAPI document structure with proper ordering
        schema_data = OrderedDict(
            [
                ("openapi", "3.0.0"),
                (
                    "info",
                    OrderedDict(
                        [
                            ("title", f"{config_class.__name__} Configuration Schema"),
                            ("version", "1.0.0"),
                        ]
                    ),
                ),
                (
                    "components",
                    OrderedDict(
                        [
                            (
                                "schemas",
                                OrderedDict([(config_class.__name__, base_schema)]),
                            )
                        ]
                    ),
                ),
            ]
        )
    else:  # json schema
        schema_data = _generate_json_schema(config_class)

    # Export in the requested format
    if format.lower() == "yaml":
        if not HAS_YAML:
            raise ImportError(
                "PyYAML is required for YAML export. Install with: pip install pyyaml"
            )

        # Custom YAML representer for multiline strings
        def multiline_representer(dumper, data):
            if "\n" in data or len(data) > 80:
                style = "|"  # use literal block
            else:
                style = None  # normal flow
            return dumper.represent_scalar("tag:yaml.org,2002:str", data, style=style)

        # Custom YAML representer for OrderedDict to preserve order
        def ordered_dict_representer(dumper, data):
            return dumper.represent_dict(data.items())

        yaml.add_representer(str, multiline_representer)
        yaml.add_representer(OrderedDict, ordered_dict_representer)

        with open(filepath, "w") as f:
            yaml.dump(
                schema_data,
                f,
                default_flow_style=False,
                sort_keys=False,
                allow_unicode=True,
                width=120,
                indent=2,
            )
    else:  # json format
        with open(filepath, "w") as f:
            json.dump(schema_data, f, indent=2)


# Private helper functions
def _generate_openapi_schema(cls) -> Dict[str, Any]:
    """Generate OpenAPI schema for a configuration class."""
    # Clean up class docstring for better YAML formatting
    description = f"{cls.__name__} configuration"
    get_description = getattr(cls, "SCHEMA_DOC", None)
    if get_description:
        description = get_description
    elif cls.__doc__:
        # Remove common indentation and clean up whitespace
        cleaned_doc = textwrap.dedent(cls.__doc__).strip()
        # Replace multiple spaces with single spaces but preserve line breaks
        lines = [line.strip() for line in cleaned_doc.split("\n") if line.strip()]
        description = "\n".join(lines)

    # Create ordered schema with specific order: title, description, type, required, then properties
    schema = OrderedDict(
        [
            ("title", cls.__name__),
            ("description", description),
            ("type", "object"),
            ("required", []),
            ("properties", OrderedDict()),
        ]
    )

    for field_name, field_info in cls._fields.items():
        if field_name.startswith("_"):
            continue

        field_schema = _get_field_schema(field_info)
        schema["properties"][field_name] = field_schema

        # Add to required if field is required
        if field_info.required:
            schema["required"].append(field_name)

    return schema


def _generate_json_schema(cls) -> Dict[str, Any]:
    """Generate JSON schema for a configuration class."""
    openapi_schema = _generate_openapi_schema(cls)

    # Create ordered JSON schema with $schema first
    schema = OrderedDict(
        [
            ("$schema", "https://json-schema.org/draft/2020-12/schema"),
            ("title", openapi_schema["title"]),
            ("description", openapi_schema["description"]),
            ("type", openapi_schema["type"]),
            ("required", openapi_schema["required"]),
            ("properties", openapi_schema["properties"]),
        ]
    )

    return schema


def _get_field_schema(field_info) -> Dict[str, Any]:
    """Generate schema for a single field."""
    field_schema = OrderedDict()

    # Get description from ConfigField.help first, then CLI metadata
    description = field_info.help or (
        field_info.cli_meta.help if field_info.cli_meta else None
    )
    if description:
        field_schema["description"] = description

    # Handle field type
    if field_info.field_type == str:
        field_schema["type"] = "string"
    elif field_info.field_type == int:
        field_schema["type"] = "integer"
    elif field_info.field_type == float:
        field_schema["type"] = "number"
    elif field_info.field_type == bool:
        field_schema["type"] = "boolean"
    elif field_info.field_type == list:
        field_schema["type"] = "array"
        field_schema["items"] = {"type": "string"}  # Default to string items
    elif field_info.field_type == dict:
        field_schema["type"] = "object"
        field_schema["additionalProperties"] = True
    elif hasattr(field_info.field_type, "_fields"):
        # Nested configuration object
        field_schema = _generate_openapi_schema(field_info.field_type)
    else:
        # Fallback to string for unknown types
        field_schema["type"] = "string"

    # Add default value
    if field_info.default is not None and not callable(field_info.default):
        field_schema["default"] = field_info.default

    # Handle choices from CLI metadata
    if field_info.cli_meta and field_info.cli_meta.choices:
        if "type" in field_schema:
            field_schema["enum"] = field_info.cli_meta.choices

    # Add examples from ConfigField
    if field_info.example is not None:
        field_schema["example"] = field_info.example

    # Add experimental flag
    if field_info.is_experimental:
        field_schema["experimental"] = True

    # Add Field Behavior
    if field_info.behavior:
        field_schema["mutation_behavior"] = field_info.behavior

    if field_info.cli_meta is not None:
        field_schema["cli_option"] = field_info.cli_meta.cli_option_str

    # Handle validation from CLI metadata
    if field_info.cli_meta and field_info.validation_fn:
        # Add validation hints in description
        if "description" in field_schema:
            field_schema["description"] += " (validation applied)"

    return field_schema
