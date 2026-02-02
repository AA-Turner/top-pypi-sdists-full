"""
Space Configuration Validator

Comprehensive validation for Space configurations using JSON Schema.
Supports validation, default value filling, and structure checking for
Space YAML files.

The validation system is based on a comprehensive JSON Schema that defines:
- All possible fields and their types
- Default values for optional fields
- Required fields and validation rules
- Enum values for specific fields
- Nested object structures and arrays

This provides a robust, flexible, and maintainable validation system that can:
1. Validate YAML structure and content
2. Fill in missing default values automatically
3. Provide detailed error messages for validation failures
4. Support both simple tool collections and complex workspaces
"""

from typing import Any, Dict, List, Tuple
import yaml
import jsonschema
from jsonschema import validate


# Space JSON Schema Definition
# ================================
# This schema defines the complete structure and validation rules for
# Space configurations. It serves as the single source of truth for:
# - Field definitions and types
# - Default values
# - Required fields
# - Validation constraints
# - Enum values for specific fields
#
# The schema supports two main configuration types:
# 1. Simple tool collections (e.g., literature-search.yaml) - minimal config
# 2. Complete workspaces (e.g., full-workspace.yaml) - full config with LLM
#
# Key features:
# - Automatic default value filling
# - Comprehensive validation rules
# - Support for nested objects and arrays
# - Flexible tool selection (by name, category, type)
# - LLM configuration with provider and model settings
# - Hook system for output processing
# - Environment variable requirements documentation
SPACE_SCHEMA = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
            "description": "Space name - unique identifier for this configuration",
        },
        "version": {
            "type": "string",
            "default": "1.0.0",
            "description": "Space version - follows semantic versioning "
            "(e.g., 1.0.0, 1.2.3)",
        },
        "description": {
            "type": "string",
            "description": "Space description - explains what this "
            "configuration does and its purpose",
        },
        "tags": {
            "type": "array",
            "items": {"type": "string"},
            "default": [],
            "description": "Space tags - keywords for categorization and "
            'discovery (e.g., ["research", "biology", "literature"])',
        },
        "tools": {
            "type": "object",
            "properties": {
                "include_tools": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Tools to include by exact name - most precise "
                    "way to select specific tools",
                },
                "categories": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Tool categories to include - broader selection "
                    'based on tool categories (e.g., ["literature", "clinical"])',
                },
                "exclude_tools": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Tools to exclude by exact name - removes "
                    "specific tools from the selection",
                },
                "include_tool_types": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Tool types to include - filter by tool type "
                    '(e.g., ["api", "local", "agentic"])',
                },
                "exclude_tool_types": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Tool types to exclude - removes tools of "
                    "specific types from the selection",
                },
            },
            "additionalProperties": False,
            "description": "Tool configuration - defines which tools to load "
            "and how to filter them",
        },
        "llm_config": {
            "type": "object",
            "properties": {
                "mode": {
                    "type": "string",
                    "enum": ["default", "fallback", "env_override"],
                    "default": "default",
                    "description": 'LLM configuration mode - "default" uses this '
                    'config as primary, "fallback" uses as backup '
                    'when primary fails, "env_override" gives environment '
                    "variables highest priority",
                },
                "default_provider": {
                    "type": "string",
                    "description": "Default LLM provider - must match AgenticTool "
                    "API types (CHATGPT, GEMINI, OPENROUTER, VLLM, etc.)",
                },
                "models": {
                    "type": "object",
                    "additionalProperties": {"type": "string"},
                    "description": "Task-specific model mappings - maps task names "
                    'to model IDs (e.g., {"default": "gpt-4o", '
                    '"analysis": "gpt-4-turbo"})',
                },
                "temperature": {
                    "type": "number",
                    "minimum": 0,
                    "maximum": 2,
                    "description": "LLM temperature - controls randomness in "
                    "responses (0.0 = deterministic, 2.0 = very random)",
                },
            },
            "additionalProperties": False,
            "description": "LLM configuration - settings for AI-powered tools "
            "(AgenticTool) - only needed for complete workspaces",
        },
        "hooks": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "type": {
                        "type": "string",
                        "description": "Hook type - identifies the hook implementation "
                        '(e.g., "output_summarization", "file_save")',
                    },
                    "enabled": {
                        "type": "boolean",
                        "default": True,
                        "description": "Whether hook is enabled - allows enabling/"
                        "disabling hooks without removing them",
                    },
                    "config": {
                        "type": "object",
                        "description": "Hook configuration - specific settings for "
                        "this hook instance",
                    },
                },
                "required": ["type"],
                "additionalProperties": False,
            },
            "description": "Hook configurations - post-processing functions for "
            "tool outputs (e.g., summarization, file saving)",
        },
        "required_env": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Required environment variables - documents which "
            "environment variables should be set (for documentation "
            "purposes only)",
        },
    },
    "required": ["name", "version"],
    "additionalProperties": False,
    "description": "Space Configuration Schema - defines the structure for "
    "Space YAML configuration files",
}


class ValidationError(Exception):
    """Raised when configuration validation fails."""


def validate_space_config(config: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """
    Validate a Space configuration using JSON Schema.

    This is a legacy function that now uses the JSON Schema validation system.
    For new code, use validate_with_schema() instead.

    Args:
        config: Configuration dictionary

    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    # Convert dict to YAML string for validation
    yaml_content = yaml.dump(config, default_flow_style=False, allow_unicode=True)
    is_valid, errors, _ = validate_with_schema(yaml_content, fill_defaults_flag=False)
    return is_valid, errors


def validate_yaml_format_by_template(yaml_content: str) -> Tuple[bool, List[str]]:
    """
    Validate YAML format by comparing against default template format.

    This method uses the JSON Schema as a reference to validate
    the structure and content of Space YAML configurations.

    Args:
        yaml_content: YAML content string

    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    # Use the new JSON Schema validation instead
    is_valid, errors, _ = validate_with_schema(yaml_content, fill_defaults_flag=False)
    return is_valid, errors


def validate_yaml_file(file_path: str) -> Tuple[bool, List[str]]:
    """
    Validate a YAML file by comparing against default template format.

    Args:
        file_path: Path to YAML file

    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            yaml_content = f.read()
        return validate_yaml_format_by_template(yaml_content)
    except FileNotFoundError:
        return False, [f"File not found: {file_path}"]
    except Exception as e:
        return False, [f"Error reading file: {e}"]


def fill_defaults(data: Dict[str, Any], schema: Dict[str, Any]) -> Dict[str, Any]:
    """
    Recursively fill default values from JSON schema.

    Args:
        data: Configuration data
        schema: JSON schema with default values

    Returns:
        Configuration with default values filled
    """
    if not isinstance(data, dict) or not isinstance(schema, dict):
        return data

    result = data.copy()

    for key, value in schema.get("properties", {}).items():
        if key not in result and "default" in value:
            result[key] = value["default"]
        elif key in result and isinstance(value, dict) and "properties" in value:
            result[key] = fill_defaults(result[key], value)
        elif (
            key in result
            and isinstance(value, dict)
            and value.get("type") == "array"
            and "items" in value
        ):
            if isinstance(result[key], list) and value["items"].get("type") == "object":
                result[key] = [
                    fill_defaults(item, value["items"]) for item in result[key]
                ]

    return result


def validate_with_schema(
    yaml_content: str, fill_defaults_flag: bool = True
) -> Tuple[bool, List[str], Dict[str, Any]]:
    """
    Validate YAML content using JSON Schema and optionally fill default values.

    Args:
        yaml_content: YAML content string
        fill_defaults_flag: Whether to fill default values

    Returns:
        Tuple of (is_valid, list_of_errors, processed_config)
    """
    errors = []

    try:
        # Parse YAML
        config = yaml.safe_load(yaml_content)
        if not isinstance(config, dict):
            return False, ["YAML content must be a dictionary"], {}

        # Fill default values if requested
        if fill_defaults_flag:
            config = fill_defaults(config, SPACE_SCHEMA)

        # Validate against schema
        validate(instance=config, schema=SPACE_SCHEMA)

        return True, [], config

    except yaml.YAMLError as e:
        return False, [f"YAML parsing error: {e}"], {}
    except jsonschema.ValidationError as e:
        return (
            False,
            [f"Schema validation error: {e.message}"],
            (config if "config" in locals() else {}),
        )
    except Exception as e:
        return (
            False,
            [f"Validation error: {e}"],
            (config if "config" in locals() else {}),
        )


def validate_yaml_file_with_schema(
    file_path: str, fill_defaults_flag: bool = True
) -> Tuple[bool, List[str], Dict[str, Any]]:
    """
    Validate a YAML file using JSON Schema and optionally fill default values.

    Args:
        file_path: Path to YAML file
        fill_defaults_flag: Whether to fill default values

    Returns:
        Tuple of (is_valid, list_of_errors, processed_config)
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            yaml_content = f.read()
        return validate_with_schema(yaml_content, fill_defaults_flag)
    except FileNotFoundError:
        return False, [f"File not found: {file_path}"], {}
    except Exception as e:
        return False, [f"Error reading file: {e}"], {}
