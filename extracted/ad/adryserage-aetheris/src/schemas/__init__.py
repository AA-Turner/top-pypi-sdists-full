"""
Aetheris JSON Schemas Module

Provides JSON schemas for task file validation and output formatting.
"""

from pathlib import Path

SCHEMAS_DIR = Path(__file__).parent


def get_task_file_schema_path() -> Path:
    """Return path to task file JSON schema."""
    return SCHEMAS_DIR / "task_file_schema.json"


def get_output_schema_path() -> Path:
    """Return path to output JSON schema."""
    return SCHEMAS_DIR / "output_schema.json"


__all__ = ["SCHEMAS_DIR", "get_task_file_schema_path", "get_output_schema_path"]
