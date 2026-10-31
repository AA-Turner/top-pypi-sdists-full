"""The JSON Schema files of the one input declaration — THE source of truth.

``schema/<slug>.schema.json`` (draft 2020-12, one file per kind, ``$ref`` between them) is the
only place the shape is written by hand. ``generated.py`` (Pydantic) and
``@ai-matrx/content-ir/input-declaration`` (TypeScript) are generated from these files, and the
registry row of each kind stores the file byte-for-byte as ``emitted_json_schema``.

Regenerate:  uv run python scripts/generate_input_declaration.py
Check:       uv run python scripts/generate_input_declaration.py --check
"""

from __future__ import annotations

import copy
import json
from functools import cache
from pathlib import Path
from typing import Any

SCHEMA_DIR = Path(__file__).parent / "schema"

#: Base every ``$id`` sits under; a relative ``$ref`` ("variable_component.schema.json") resolves
#: against it. ``relation.schema.json`` resolves to the registered ``relation`` kind.
SCHEMA_BASE_URI = "https://aimatrx.com/schemas/kinds/"

#: The four kinds this package owns, in dependency order (children first).
INPUT_DECLARATION_KINDS: tuple[str, ...] = (
    "variable_context_binding",
    "variable_record_binding",
    "variable_component",
    "variable_definition",
)

#: Kinds the files reference but do not own (resolved from the registry / the owning model).
REFERENCED_KINDS: tuple[str, ...] = ("relation",)


def schema_uri(slug: str) -> str:
    return f"{SCHEMA_BASE_URI}{slug}.schema.json"


def schema_path(slug: str) -> Path:
    if slug not in INPUT_DECLARATION_KINDS:
        raise KeyError(f"{slug!r} is not an input-declaration kind ({', '.join(INPUT_DECLARATION_KINDS)})")
    return SCHEMA_DIR / f"{slug}.schema.json"


@cache
def _load(slug: str) -> dict[str, Any]:
    return json.loads(schema_path(slug).read_text(encoding="utf-8"))


def source_schema(slug: str) -> dict[str, Any]:
    """The source JSON Schema of ``slug`` — a fresh copy, safe to mutate."""
    return copy.deepcopy(_load(slug))


def all_source_schemas() -> dict[str, dict[str, Any]]:
    return {slug: source_schema(slug) for slug in INPUT_DECLARATION_KINDS}


def variable_component_types() -> tuple[str, ...]:
    """The component ``type`` vocabulary, read from the schema (never restated)."""
    return tuple(_load("variable_component")["properties"]["type"]["enum"])


def media_variable_types() -> tuple[str, ...]:
    """Component types whose value is a MediaRef, read from the schema."""
    return tuple(_load("variable_component")["x-mediaTypes"])
