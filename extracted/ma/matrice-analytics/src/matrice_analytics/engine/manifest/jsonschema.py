"""JSON Schema for ``app.yaml``, generated from the Pydantic models.

**This is an artefact, never a source of truth** (``08`` §1). The models in
:mod:`matrice_analytics.engine.manifest.models` decide what a manifest may contain; this module
only re-describes them in a form editors understand, so an app author gets completion and inline
errors while typing rather than a stack trace at deploy time.

Regenerate with::

    python -m matrice_analytics.engine.manifest.jsonschema app.schema.json

and point an editor at it::

    # yaml-language-server: $schema=./app.schema.json

One transformation is applied to Pydantic's output. Internally a pipeline stage is a tagged model
(``{"kind": "detect", "classes": [...]}``) so the union is a real discriminated union; on disk it
is a single-key mapping (``- detect: {classes: [...]}``). The generated schema describes the
on-disk form, because that is what the editor is validating.
"""

from __future__ import annotations

import argparse
import copy
import json
import sys
from pathlib import Path
from typing import Any

from .models import MANIFEST_SCHEMA_VERSION, PRIMITIVES, AppManifest

__all__ = ["build_json_schema", "main", "write_json_schema"]

SCHEMA_ID = "https://schemas.matrice.ai/analytics/app-manifest-v1.json"

_DESCRIPTION = (
    "Matrice analytics app manifest (app.yaml), schema_version "
    f"{MANIFEST_SCHEMA_VERSION}. The Pydantic models in "
    "matrice_analytics.engine.manifest.models are the source of truth; this file is generated "
    "from them. Field reference: ml-applications/guidelines/FIELD_REFERENCE.md."
)


def build_json_schema() -> dict[str, Any]:
    """Return the JSON Schema for a manifest, in its on-disk shape."""
    schema = AppManifest.model_json_schema(mode="validation")
    schema = copy.deepcopy(schema)

    defs: dict[str, Any] = schema.get("$defs", {})
    _strip_internal_discriminator(defs)
    _rewrite_pipeline_items(schema, defs)

    ordered: dict[str, Any] = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": SCHEMA_ID,
        "title": "Matrice analytics app manifest",
        "description": _DESCRIPTION,
    }
    ordered.update(schema)
    return ordered


def _strip_internal_discriminator(defs: dict[str, Any]) -> None:
    """Remove the ``kind`` tag from every primitive config definition.

    ``kind`` exists only so Pydantic can discriminate the union in Python. On disk the primitive
    is named by the mapping key, and leaving ``kind`` in the schema would invite authors to write
    it — which ``extra="forbid"`` would then reject only for stages parsed the other way.
    """
    for config_model in PRIMITIVES.values():
        definition = defs.get(config_model.__name__)
        if not isinstance(definition, dict):  # pragma: no cover - name mismatch would be a bug
            continue
        definition.get("properties", {}).pop("kind", None)
        required = definition.get("required")
        if isinstance(required, list) and "kind" in required:
            required.remove("kind")
            if not required:
                definition.pop("required")


def _rewrite_pipeline_items(schema: dict[str, Any], defs: dict[str, Any]) -> None:
    """Replace the tagged-union item schema with the single-key mapping form."""
    pipeline = schema.get("properties", {}).get("pipeline")
    if not isinstance(pipeline, dict):  # pragma: no cover - the field is required on the model
        return

    options: list[dict[str, Any]] = []
    for primitive, config_model in PRIMITIVES.items():
        definition = defs.get(config_model.__name__, {})
        options.append(
            {
                "title": f"{primitive} stage",
                "description": (definition.get("description") or "").split("\n")[0],
                "type": "object",
                "additionalProperties": False,
                "required": [primitive],
                "properties": {primitive: {"$ref": f"#/$defs/{config_model.__name__}"}},
            }
        )

    pipeline["items"] = {
        "title": "Pipeline stage",
        "description": (
            "One primitive and its settings, as a single-key mapping: "
            "'- detect: {classes: [person]}'. The list order is the execution order."
        ),
        "oneOf": options,
    }


def write_json_schema(path: str | Path, *, indent: int = 2) -> Path:
    """Write the schema to *path* (parent directories are created). Returns the path written."""
    target = Path(path).expanduser()
    if target.parent != Path():
        target.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(build_json_schema(), indent=indent, sort_keys=False)
    target.write_text(payload + "\n", encoding="utf-8")
    return target


def main(argv: list[str] | None = None) -> int:
    """CLI: write the generated JSON Schema to a file (or stdout with ``-``)."""
    parser = argparse.ArgumentParser(
        prog="python -m matrice_analytics.engine.manifest.jsonschema",
        description="Generate the app.yaml JSON Schema from the Pydantic manifest models.",
    )
    parser.add_argument(
        "output",
        nargs="?",
        default="app.schema.json",
        help="Where to write the schema. Use '-' for stdout. Default: app.schema.json",
    )
    parser.add_argument("--indent", type=int, default=2, help="JSON indent. Default: 2")
    args = parser.parse_args(argv)

    if args.output == "-":
        json.dump(build_json_schema(), sys.stdout, indent=args.indent)
        sys.stdout.write("\n")
        return 0

    written = write_json_schema(args.output, indent=args.indent)
    print(f"wrote {written}")
    return 0


if __name__ == "__main__":  # pragma: no cover - CLI entry point
    raise SystemExit(main())
