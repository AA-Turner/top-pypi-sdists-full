"""Auto-derivation of issueType and labels from tree depth."""

from __future__ import annotations

import copy
from typing import Any

from .config import EpicTreeConfig
from .normalization_models import NormalizationResult, NormalizationWarning


def normalize_tree(document: dict[str, Any], config: EpicTreeConfig) -> NormalizationResult:
    """Normalize an epic-tree document by auto-deriving missing fields.

    Walks the tree and fills in ``issueType`` and ``labels`` based on depth
    when they are absent, using config-provided defaults.  Normalizes existing
    labels (trim, lowercase, deduplicate) and emits warnings for mismatches.

    .. note::
        The ``effective_depth`` clamping (``min(depth, config.max_depth - 1)``) is a
        defensive measure for callers that invoke :func:`normalize_tree` directly without
        prior validation.  When called via :func:`~.loader.load_epic_tree`, nodes at
        depth ``>= config.max_depth`` are already rejected by :func:`~.validator.validate_epic_tree`
        before this function is reached, making the clamp a no-op for fully validated
        documents.

    Args:
        document: Parsed epic-tree JSON document (wrapper with schemaVersion + epic).
        config: Configuration providing default values per depth.

    Returns:
        A :class:`NormalizationResult` with the normalized document and any warnings.
    """
    result = copy.deepcopy(document)
    warnings: list[NormalizationWarning] = []
    epic = result.get("epic")
    if not isinstance(epic, dict):
        return NormalizationResult(document=result, warnings=warnings)
    _normalize_node(epic, depth=0, config=config, warnings=warnings)
    return NormalizationResult(document=result, warnings=warnings)


def _normalize_node(
    node: dict[str, Any],
    depth: int,
    config: EpicTreeConfig,
    warnings: list[NormalizationWarning],
) -> None:
    """Recursively normalize a single node in-place."""
    effective_depth = min(depth, config.max_depth - 1)

    # Check for mismatches before derivation (only on explicit values)
    _check_mismatch(node, effective_depth, config, warnings, raw_depth=depth)

    # Auto-derive issueType if absent or null
    if "issueType" not in node or node["issueType"] is None:
        if effective_depth in config.default_issue_types:
            node["issueType"] = config.default_issue_types[effective_depth]

    # Auto-derive labels if absent or null (empty list is explicit)
    if "labels" not in node or node["labels"] is None:
        if effective_depth in config.default_labels:
            node["labels"] = _normalize_labels(list(config.default_labels[effective_depth]))
    elif isinstance(node.get("labels"), list):
        # Normalize existing labels: trim, lowercase, deduplicate
        node["labels"] = _normalize_labels(node["labels"])

    # Recurse into children
    if depth == 0:
        for feature in node.get("features", []):
            if isinstance(feature, dict):
                _normalize_node(feature, depth=1, config=config, warnings=warnings)
    else:
        # depth >= 1: recurse into subtasks at any depth, applying clamping
        for subtask in node.get("subtasks", []):
            if isinstance(subtask, dict):
                _normalize_node(subtask, depth=depth + 1, config=config, warnings=warnings)


def _normalize_labels(labels: list[Any]) -> list[str]:
    """Trim whitespace, lowercase, and deduplicate labels preserving first-occurrence order.

    Args:
        labels: Raw list of label values.

    Returns:
        Normalized, deduplicated list of labels.
    """
    seen: set[str] = set()
    result: list[str] = []
    for label in labels:
        if not isinstance(label, str):
            continue
        normalized = label.strip().lower()
        if normalized and normalized not in seen:
            seen.add(normalized)
            result.append(normalized)
    return result


def _check_mismatch(
    node: dict[str, Any],
    effective_depth: int,
    config: EpicTreeConfig,
    warnings: list[NormalizationWarning],
    raw_depth: int | None = None,
) -> None:
    """Emit warnings when explicit values contradict the expected depth level.

    Only checks fields that are explicitly set (not absent/null).
    Uses whole-value equality (case-insensitive) for comparison.
    """
    raw_ref = node.get("ref")
    ref = str(raw_ref) if isinstance(raw_ref, str) else "<unknown>"
    raw_depth = effective_depth if raw_depth is None else raw_depth

    # Check issueType mismatch
    issue_type = node.get("issueType")
    if issue_type is not None and isinstance(issue_type, str):
        expected_issue_type = config.default_issue_types.get(effective_depth)
        if expected_issue_type is not None:
            actual_normalized = issue_type.strip().lower()
            expected_normalized = expected_issue_type.strip().lower()
            if actual_normalized != expected_normalized:
                warnings.append(
                    NormalizationWarning(
                        ref=ref,
                        depth=raw_depth,
                        field="issueType",
                        actual_value=actual_normalized,
                        expected_value=expected_normalized,
                    )
                )

    # Check labels mismatch
    labels = node.get("labels")
    if labels is not None and isinstance(labels, list):
        expected_labels = config.default_labels.get(effective_depth)
        if expected_labels is not None:
            expected_keywords = {lbl.strip().lower() for lbl in expected_labels}
            all_hierarchy_keywords = {
                depth_label.strip().lower()
                for depth_labels in config.default_labels.values()
                for depth_label in depth_labels
            }
            for actual_normalized in _normalize_labels(labels):
                # Only warn if the label matches a hierarchy keyword at the wrong level
                # (whole-value equality — "Feature Request" does NOT match "feature")
                if actual_normalized in all_hierarchy_keywords and actual_normalized not in expected_keywords:
                    expected_value = ", ".join(sorted(expected_keywords))
                    warnings.append(
                        NormalizationWarning(
                            ref=ref,
                            depth=raw_depth,
                            field="labels",
                            actual_value=actual_normalized,
                            expected_value=expected_value,
                        )
                    )
