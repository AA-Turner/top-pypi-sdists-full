from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List

from ..state.errors import InvalidFile


CATALOG_FILENAME = "catalog.json"
MANIFEST_SCHEMA_PREFIX = "https://schemas.getdbt.com/dbt/manifest/"
# dbt 1.8 introduced manifest v12, and every release since has kept it. Older
# manifests lack fields the reader depends on, such as `attached_node` on every test.
SUPPORTED_MANIFEST_VERSIONS = frozenset({"v12"})


@dataclass
class DbtManifest:
    filename: str
    project_name: str
    nodes: Dict[str, Dict[str, Any]]
    sources: Dict[str, Dict[str, Any]]
    # unique_id -> lowercased column name -> warehouse type, from a sibling catalog.json
    column_types: Dict[str, Dict[str, str]] = field(default_factory=dict)
    # Tests turned off with `enabled: false`, which dbt moves out of `nodes`.
    disabled_tests: List[Dict[str, Any]] = field(default_factory=list)


def read_dbt_manifest(filename: str) -> DbtManifest | None:
    """The dbt manifest in `filename`, or None when the file isn't one.

    Only `.json` files are considered, and only ones whose metadata names a dbt
    manifest schema, so Anomalo state files keep going to their own drivers.
    """
    path = Path(filename)
    if path.suffix != ".json":
        return None
    document = _read_json(path)
    metadata = document.get("metadata") if isinstance(document, dict) else None
    schema = metadata.get("dbt_schema_version") if isinstance(metadata, dict) else None
    if not isinstance(schema, str) or not schema.startswith(MANIFEST_SCHEMA_PREFIX):
        return None
    version = schema[len(MANIFEST_SCHEMA_PREFIX) :].removesuffix(".json")
    if version not in SUPPORTED_MANIFEST_VERSIONS:
        raise InvalidFile(
            filename,
            f"dbt manifest schema {version} is not supported; build the manifest"
            " with dbt 1.8 or later",
        )
    project_name = metadata.get("project_name")
    if not project_name:
        raise InvalidFile(filename, "dbt manifest metadata has no project_name")
    catalog_path = path.with_name(CATALOG_FILENAME)
    return DbtManifest(
        filename=filename,
        project_name=project_name,
        nodes=document.get("nodes") or {},
        sources=document.get("sources") or {},
        column_types=_catalog_column_types(catalog_path)
        if catalog_path.exists()
        else {},
        disabled_tests=[
            node
            for versions in (document.get("disabled") or {}).values()
            for node in versions
            if node.get("resource_type") == "test"
        ],
    )


def _read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text())
    except (OSError, ValueError) as e:
        raise InvalidFile(str(path), str(e)) from e


def _catalog_column_types(path: Path) -> Dict[str, Dict[str, str]]:
    catalog = _read_json(path)
    entries = {**(catalog.get("nodes") or {}), **(catalog.get("sources") or {})}
    return {
        unique_id: {
            name.lower(): column.get("type") or ""
            for name, column in (entry.get("columns") or {}).items()
        }
        for unique_id, entry in entries.items()
    }
