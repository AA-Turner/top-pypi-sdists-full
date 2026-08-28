"""Auto-generated stub for module: jsonschema."""
from typing import Any

from .models import MANIFEST_SCHEMA_VERSION, PRIMITIVES, AppManifest

# Constants
SCHEMA_ID: str

# Functions
def build_json_schema() -> dict[str, Any]:
    """
    Return the JSON Schema for a manifest, in its on-disk shape.
    """
    ...
def main(argv: list[str] | None = None) -> int:
    """
    CLI: write the generated JSON Schema to a file (or stdout with ``-``).
    """
    ...
def write_json_schema(path: str | Any) -> Any:
    """
    Write the schema to *path* (parent directories are created). Returns the path written.
    """
    ...
