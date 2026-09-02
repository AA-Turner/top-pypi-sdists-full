"""Schema loading utilities for the epic-tree JSON Schema."""

from __future__ import annotations

import json
from pathlib import Path

#: Absolute path to the epic-tree JSON Schema file shipped with the package.
SCHEMA_PATH: Path = Path(__file__).resolve().parent.parent / "schemas" / "epic-tree.schema.json"

_cached_schema: dict | None = None


def load_schema() -> dict:
    """Load and return the epic-tree JSON Schema as a parsed dictionary.

    The schema is read from :data:`SCHEMA_PATH` on the first call and cached
    for subsequent calls within the same process.

    Raises:
        FileNotFoundError: If the schema file does not exist at the expected path.
        json.JSONDecodeError: If the schema file contains invalid JSON.
    """
    global _cached_schema  # noqa: PLW0603
    if _cached_schema is None:
        _cached_schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    return _cached_schema
