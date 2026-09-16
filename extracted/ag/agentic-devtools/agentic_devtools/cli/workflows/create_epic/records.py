"""Atomic persistence for incremental create-epic mapping documents."""

from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit
from uuid import UUID

from agentic_devtools import state
from agentic_devtools.epic_tree.models import EpicTree


def _canonicalize_provider_target(provider_name: str, provider_target: str) -> str:
    """Return the provider-specific canonical form of a provider target."""
    target = provider_target.strip()
    if provider_name == "github":
        parts = target.split("/")
        if len(parts) != 2 or not all(parts):
            raise ValueError("GitHub provider_target must be in 'owner/repo' format")
        return "/".join(part.casefold() for part in parts)
    if provider_name == "jira":
        parsed = urlsplit(target)
        if parsed.scheme.casefold() not in {"http", "https"} or not parsed.hostname:
            raise ValueError("Jira provider_target must be an HTTP(S) URL")
        try:
            port = parsed.port
        except ValueError as exc:
            raise ValueError("Jira provider_target must contain a valid port") from exc
        host = parsed.hostname.casefold()
        if ":" in host and not host.startswith("["):
            host = f"[{host}]"
        if port is not None and port != {"http": 80, "https": 443}[parsed.scheme.casefold()]:
            host = f"{host}:{port}"
        return f"{parsed.scheme.casefold()}://{host}{parsed.path.rstrip('/')}"
    return target


def resolve_tree_id(tree: EpicTree | dict[str, Any] | str) -> str:
    """Return a canonical lowercase UUID from a tree model or document."""
    if isinstance(tree, EpicTree):
        value: Any = tree.treeId
    elif isinstance(tree, dict):
        value = tree.get("treeId")
    else:
        value = tree
    if value is None:
        raise ValueError("Epic-tree document does not contain treeId")
    try:
        return str(UUID(str(value)))
    except (ValueError, AttributeError, TypeError) as exc:
        raise ValueError(f"Invalid treeId: {value!r}") from exc


def resolve_mapping_path(tree: EpicTree | dict[str, Any] | str, *, create: bool = True) -> Path:
    """Resolve the mapping file beneath the active workflow state directory."""
    tree_id = resolve_tree_id(tree)
    return state.get_state_dir(create=create) / f"epic-create-mapping-{tree_id}"


def initialize_mapping_document(
    tree: EpicTree | dict[str, Any] | str,
    provider_name: str,
    provider_target: str,
) -> dict[str, Any]:
    """Build an empty schema-v2 mapping document."""
    if not isinstance(provider_name, str) or not provider_name.strip():
        raise ValueError("provider_name must be non-empty")
    if not isinstance(provider_target, str) or not provider_target.strip():
        raise ValueError("provider_target must be non-empty")
    canonical_provider_name = provider_name.strip().casefold()
    return {
        "schemaVersion": "2.0",
        "treeId": resolve_tree_id(tree),
        "provider": {
            "name": canonical_provider_name,
            "target": _canonicalize_provider_target(canonical_provider_name, provider_target),
        },
        "entries": {},
    }


def validate_mapping_document(
    document: Any,
    tree: EpicTree | dict[str, Any] | str | None = None,
    provider_name: str | None = None,
    provider_target: str | None = None,
) -> dict[str, Any]:
    """Validate and return a mapping document, optionally against active identity."""
    if not isinstance(document, dict):
        raise ValueError("Mapping document must be a JSON object")
    if document.get("schemaVersion") != "2.0":
        raise ValueError("Mapping document schemaVersion must be '2.0'")
    try:
        document_tree_id = resolve_tree_id(document)
    except ValueError as exc:
        raise ValueError("Mapping document has an invalid treeId") from exc
    if tree is not None and document_tree_id != resolve_tree_id(tree):
        raise ValueError("Mapping document treeId does not match the active tree")
    provider = document.get("provider")
    if (
        not isinstance(provider, dict)
        or not isinstance(provider.get("name"), str)
        or not provider["name"].strip()
        or not isinstance(provider.get("target"), str)
        or not provider["target"].strip()
    ):
        raise ValueError("Mapping document provider must contain non-empty name and target")
    canonical_provider_name = provider["name"].strip().casefold()
    if provider_name is not None and canonical_provider_name != provider_name.strip().casefold():
        raise ValueError("Mapping document provider name does not match the active provider")
    if provider_target is not None and provider["target"] != _canonicalize_provider_target(
        canonical_provider_name, provider_target
    ):
        raise ValueError("Mapping document provider target does not match the active target")
    if not isinstance(document.get("entries"), dict):
        raise ValueError("Mapping document entries must be an object")
    return document


def load_mapping_document(path: Path | str) -> dict[str, Any]:
    """Load and validate an existing mapping document."""
    document = json.loads(Path(path).read_text(encoding="utf-8"))
    return validate_mapping_document(document)


def atomic_write_mapping_document(path: Path | str, document: dict[str, Any]) -> None:
    """Write a valid mapping document using temp-file plus replace semantics."""
    validate_mapping_document(document)
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary_name = tempfile.mkstemp(prefix=f".{destination.name}.", dir=destination.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as temporary:
            json.dump(document, temporary, ensure_ascii=False, indent=2, sort_keys=True)
            temporary.write("\n")
            temporary.flush()
            os.fsync(temporary.fileno())
        os.replace(temporary_name, destination)
    except Exception:
        try:
            os.unlink(temporary_name)
        except OSError:
            pass
        raise
