"""
ToolUniverse Space Configuration Management

This module provides tools for loading, validating, and managing ToolUniverse Space configurations.
Space allows users to define collections of tools with specific configurations,
LLM settings, and hooks for advanced scientific workflows.

Main Components:
- SpaceLoader: Loads Space configurations from various sources (HuggingFace, local files, URLs)
- SpaceValidator: Validates Space configurations using JSON Schema
- ValidationError: Exception raised when configuration validation fails

Usage:
    from tooluniverse.space import SpaceLoader, validate_space_config

    # Load a Space configuration
    loader = SpaceLoader()
    config = loader.load("hf:user/repo")

    # Validate a configuration
    is_valid, errors = validate_space_config(config)
"""

from .loader import SpaceLoader
from .validator import (
    validate_space_config,
    validate_with_schema,
    validate_yaml_file_with_schema,
    validate_yaml_format_by_template,
    validate_yaml_file,
    fill_defaults,
    ValidationError,
    SPACE_SCHEMA,
)

__all__ = [
    "SpaceLoader",
    "validate_space_config",
    "validate_with_schema",
    "validate_yaml_file_with_schema",
    "validate_yaml_format_by_template",
    "validate_yaml_file",
    "fill_defaults",
    "ValidationError",
    "SPACE_SCHEMA",
]
