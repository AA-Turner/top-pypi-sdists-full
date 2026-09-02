"""Loader for epic-tree JSON documents into typed Pydantic models.

Provides :func:`load_epic_tree` which reads, validates, and parses an
epic-tree JSON file into a fully populated :class:`~.models.EpicTree`
instance with aggregated validation errors.
"""

from __future__ import annotations

import json
import logging
import re
from pathlib import Path
from typing import Any

from .config import load_epic_tree_config
from .errors import EpicTreeLoadError, EpicTreeValidationError, ValidationReport
from .models import EpicTree
from .normalizer import normalize_tree
from .validator import check_schema_version, validate_epic_tree

logger = logging.getLogger(__name__)

_BRACKET_INDEX_RE = re.compile(r"\[(\d+)\]")


def _find_repo_root(start: Path) -> Path | None:
    """Walk up from *start* searching for a repository root.

    A directory is treated as the repo root when it contains a ``.git``
    entry (file or directory) **or** a ``.github/agdt-config.json`` file.
    Returns ``None`` when neither marker is found before the filesystem root.

    Args:
        start: Starting file or directory path.  When *start* is a file its
               parent directory is used as the initial candidate.
    """
    candidate = start if start.is_dir() else start.parent
    while True:
        if (candidate / ".git").exists() or (candidate / ".github" / "agdt-config.json").exists():
            return candidate
        parent = candidate.parent
        if parent == candidate:
            return None
        candidate = parent


def _normalize_validation_path(path: str) -> str:
    """Normalise a validation-error path to an RFC 6901 JSON Pointer.

    JSON Schema structural errors (Pass 1) already emit RFC 6901 Pointer
    strings (empty string ``""`` for the root, or a leading-``/`` path such
    as ``"/epic/features/0"``).  Semantic-check errors (Pass 2) use
    dot-notation with bracket indices, e.g. ``"epic.features[0].subtasks[1]"``.

    This function converts dot-notation paths to Pointer format so that
    all :class:`~.errors.EpicTreeValidationError` ``path`` values are
    consistently RFC 6901-compliant.
    """
    if not path or path.startswith("/"):
        # Empty string (root pointer) and paths that already start with /
        # are valid JSON Pointers; return unchanged.
        return path
    # Step 1: replace bracket indices [n] with /n
    result = _BRACKET_INDEX_RE.sub(r"/\1", path)
    # Step 2: replace dot separators with /
    result = result.replace(".", "/")
    # Step 3: prepend the leading /
    return "/" + result


def load_epic_tree(
    path: Path | str,
    config_path: Path | str | None = None,
    *,
    provider: str | None = None,
    skip_cycle_check: bool = False,
) -> EpicTree:
    """Load and parse an epic-tree JSON file into an :class:`EpicTree` instance.

    Pipeline:
    1. JSON parse
    2. Schema version presence/format check
    3. Config loading
    4. Schema validation + semantic validation
    5. Normalization (auto-derive issueType/labels)
    6. Pydantic model construction

    Args:
        path: File path to the epic-tree JSON document.
        config_path: Optional explicit path to the repository root for loading
            config.  When ``None`` (the default), the repo root is inferred by
            walking up from the epic-tree file's directory, looking for a
            ``.git`` entry or ``.github/agdt-config.json``.  Falls back to
            built-in defaults when no repo root is found.
        provider: Optional explicit provider name (e.g. ``"github"`` or
            ``"jira"``).  When supplied, the config selects the matching
            ``issueManagement`` block instead of resolving the active provider
            from ``platform.issue_adapter``.  This lets callers validate a
            document against the same effective provider they will mutate.
        skip_cycle_check: When ``True``, the semantic validation pass omits the
            blocking-dependency cycle-detection check while retaining every
            other check (including unresolved-reference detection).  Callers
            that defer cycle detection to a combined hierarchy/blocking graph
            use this to avoid duplicate — and potentially conflicting — cycle
            reporting.

    Returns:
        A fully populated :class:`EpicTree` model instance.

    Raises:
        FileNotFoundError: If the file does not exist.
        json.JSONDecodeError: If the file contains syntactically invalid JSON.
        VersionMismatchError: If the document's ``schemaVersion`` is not supported.
        ConfigError: If ``.github/agdt-config.json`` exists but contains an invalid
            ``epicTree`` configuration block.
        EpicTreeLoadError: If the document fails structural or semantic validation.
    """
    path = Path(path)
    text = path.read_text(encoding="utf-8")
    document: Any = json.loads(text)

    # Schema version pre-check
    if isinstance(document, dict) and "schemaVersion" in document and isinstance(document["schemaVersion"], str):
        try:
            check_schema_version(document)
        except ValueError:
            pass  # Invalid format deferred to validate_epic_tree

    # Load config — infer repo root from file location when not explicitly provided
    resolved_config_path = config_path if config_path is not None else _find_repo_root(path)
    config = load_epic_tree_config(resolved_config_path, provider=provider)

    # Validate (structural + semantic)
    report: ValidationReport = validate_epic_tree(document, config, skip_cycle_check=skip_cycle_check)
    if not report.valid:
        # Convert ValidationReport entries to EpicTreeValidationError objects.
        # Entries that carry multiple paths (e.g. duplicate_ref, cycle_detected)
        # produce one EpicTreeValidationError per path so that all locations are
        # surfaced to callers rather than only the first.
        # All paths are normalised to RFC 6901 JSON Pointer format: structural
        # errors (Pass 1) already carry Pointer strings; semantic errors (Pass 2)
        # use dot-notation which is converted here so the public contract is uniform.
        errors: list[EpicTreeValidationError] = [
            EpicTreeValidationError(
                path=_normalize_validation_path(path),
                message=entry.message,
                keyword=entry.category,
                property_name=entry.property_name,
            )
            for entry in report.errors
            for path in (entry.paths if entry.paths else [""])
        ]
        raise EpicTreeLoadError(errors)

    # Normalize (auto-derive missing issueType/labels)
    norm_result = normalize_tree(document, config)
    normalized = norm_result.document

    # Build Pydantic model
    return EpicTree.model_validate(normalized)
