"""Data-driven label and issue-type mapping/translation layer.

Translates provider-neutral issue types (members of
:data:`~agentic_devtools.adapters.issue_provider.VALID_ISSUE_TYPES`) into
provider-native representations:

* **GitHub** — maps issue types to labels (``epic``, ``feature``, ``Subtask``,
  ``task``, ``bug``) and merges with declared labels.
* **Jira** — maps to real issue-type names (``Epic``, ``Story``, ``Sub-task``,
  ``Task``, ``Bug``) and routes hierarchy to ``epic-link`` / ``parent`` fields.

Mapping tables come from config (``platform.github.issue_type_labels`` and
``platform.jira.issue_type_names`` in ``.github/agdt-config.json``);
defaults are provided for all five canonical types.

All public mapping functions are **pure** (no side effects, no I/O) — see
FR-009 in the specification.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from agentic_devtools.adapters.issue_provider import (
    VALID_ISSUE_TYPES,
    IssueTypeMappingError,
)

# ---------------------------------------------------------------------------
# Type alias
# ---------------------------------------------------------------------------

TypeMapping = dict[str, str]  # Mapping from provider-neutral issue type to provider-native label or name.

# ---------------------------------------------------------------------------
# Default mapping tables (FR-002)
# ---------------------------------------------------------------------------

GITHUB_DEFAULT_LABELS: TypeMapping = {
    "epic": "epic",
    "feature": "feature",
    "subtask": "Subtask",
    "task": "task",
    "bug": "bug",
}

JIRA_DEFAULT_TYPE_NAMES: TypeMapping = {
    "epic": "Epic",
    "feature": "Story",
    "subtask": "Sub-task",
    "task": "Task",
    "bug": "Bug",
}

# ---------------------------------------------------------------------------
# Result dataclasses
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class GitHubMappingResult:
    """Result of mapping an issue type to GitHub labels.

    Attributes:
        merged_labels: Derived hierarchy label first, then declared labels
            with case-insensitive de-duplication applied.
    """

    merged_labels: list[str]


@dataclass(frozen=True)
class JiraMappingResult:
    """Result of mapping an issue type to Jira semantics.

    Attributes:
        type_name: Jira-native issue type name (e.g. ``"Sub-task"``).
        labels: Declared labels after normalization (trim, de-dup).
        route: Hierarchy routing hint — ``"parent"`` when the issue is a
            subtask and ``parent_issue_type`` is provided, ``"epic-link"``
            when the parent is an epic, or ``None`` for root nodes
            (``parent_issue_type is None``) and epics.
    """

    type_name: str
    labels: list[str]
    route: str | None


# ---------------------------------------------------------------------------
# Validation helpers
# ---------------------------------------------------------------------------


def _validate_issue_type(issue_type: str) -> None:
    """Reject invalid issue types with a clear error (FR-008).

    Raises:
        ValueError: If *issue_type* is empty, whitespace-only, or not a
            member of :data:`VALID_ISSUE_TYPES`.  The error message lists the
            canonical types in sorted order.
    """
    if not isinstance(issue_type, str) or not issue_type.strip():
        raise ValueError(f"issue_type must be a non-empty string. Valid types: {sorted(VALID_ISSUE_TYPES)}")
    if issue_type not in VALID_ISSUE_TYPES:
        raise ValueError(f"Unsupported issue_type {issue_type!r}. Valid types: {sorted(VALID_ISSUE_TYPES)}")


def _resolve_type(issue_type: str, mapping: TypeMapping) -> str:
    """Look up *issue_type* in *mapping* (FR-006).

    Raises:
        IssueTypeMappingError: If *issue_type* has no entry in *mapping*.
    """
    try:
        value = mapping[issue_type]
    except KeyError:
        raise IssueTypeMappingError(
            f"Cannot resolve issue type {issue_type!r}. Available mappings: {sorted(mapping.keys())}"
        ) from None

    if not isinstance(value, str):
        raise IssueTypeMappingError(
            f"Mapping value for {issue_type!r} must be a string, got {type(value).__name__}: {value!r}"
        )
    trimmed = value.strip()
    if not trimmed:
        raise IssueTypeMappingError(
            f"Resolved issue type {issue_type!r} to an empty mapping value."
            f" Available mappings: {sorted(mapping.keys())}"
        )
    return trimmed


# ---------------------------------------------------------------------------
# Label processing helpers
# ---------------------------------------------------------------------------


def _merge_github_labels(
    derived_label: str,
    declared_labels: list[str] | None,
) -> list[str]:
    """Merge derived hierarchy label with declared labels (FR-003).

    * Trims whitespace from each label and discards empty strings.
    * Case-insensitive de-duplication: derived label wins collisions.
    * Output order: derived label first, then declared labels preserving
      original order minus duplicates.
    """
    if isinstance(declared_labels, str):
        raise TypeError(
            f"declared_labels must be a list of strings, not a bare str {declared_labels!r}."
            f" Did you mean [{declared_labels!r}]?"
        )
    result: list[str] = [derived_label]
    seen: set[str] = {derived_label.lower()}
    for label in declared_labels or []:
        if not isinstance(label, str):
            raise ValueError(f"Each declared label must be a string, got {type(label).__name__}: {label!r}")
        trimmed = label.strip()
        if not trimmed:
            continue
        key = trimmed.lower()
        if key not in seen:
            seen.add(key)
            result.append(trimmed)
    return result


def _normalize_jira_labels(declared_labels: list[str] | None) -> list[str]:
    """Normalize declared labels for Jira (FR-004).

    * Trims whitespace and discards empty strings.
    * Case-sensitive de-duplication preserving first-occurrence order.
    """
    if isinstance(declared_labels, str):
        raise TypeError(
            f"declared_labels must be a list of strings, not a bare str {declared_labels!r}."
            f" Did you mean [{declared_labels!r}]?"
        )
    result: list[str] = []
    seen: set[str] = set()
    for label in declared_labels or []:
        if not isinstance(label, str):
            raise ValueError(f"Each declared label must be a string, got {type(label).__name__}: {label!r}")
        trimmed = label.strip()
        if not trimmed:
            continue
        if trimmed not in seen:
            seen.add(trimmed)
            result.append(trimmed)
    return result


# ---------------------------------------------------------------------------
# Hierarchy routing constants (FR-004)
# ---------------------------------------------------------------------------

_ROUTE_PARENT = "parent"
_ROUTE_EPIC_LINK = "epic-link"

# ---------------------------------------------------------------------------
# Pure mapping functions (FR-009)
# ---------------------------------------------------------------------------


def map_issue_type_to_github_labels(
    issue_type: str,
    declared_labels: list[str] | None = None,
    type_mapping: TypeMapping | None = None,
) -> GitHubMappingResult:
    """Map a neutral issue type to GitHub labels (FR-001, FR-003, FR-005).

    Args:
        issue_type: Provider-neutral type (member of ``VALID_ISSUE_TYPES``).
        declared_labels: User-specified labels to merge with the derived one.
        type_mapping: Custom mapping table; defaults to
            :data:`GITHUB_DEFAULT_LABELS`.

    Returns:
        A :class:`GitHubMappingResult` with merged, de-duplicated labels.

    Raises:
        ValueError: If *issue_type* is invalid (FR-008).
        IssueTypeMappingError: If *issue_type* cannot be resolved (FR-006).
    """
    _validate_issue_type(issue_type)
    mapping = type_mapping if type_mapping is not None else GITHUB_DEFAULT_LABELS
    derived_label = _resolve_type(issue_type, mapping)
    merged = _merge_github_labels(derived_label, declared_labels)
    return GitHubMappingResult(merged_labels=merged)


def map_issue_type_to_jira(
    issue_type: str,
    parent_issue_type: str | None = None,
    declared_labels: list[str] | None = None,
    type_mapping: TypeMapping | None = None,
) -> JiraMappingResult:
    """Map a neutral issue type to Jira semantics (FR-001, FR-004, FR-005).

    Args:
        issue_type: Provider-neutral type (member of ``VALID_ISSUE_TYPES``).
        parent_issue_type: Neutral type of the parent issue, or ``None``.
        declared_labels: User-specified labels to normalize.
        type_mapping: Custom mapping table; defaults to
            :data:`JIRA_DEFAULT_TYPE_NAMES`.

    Returns:
        A :class:`JiraMappingResult` with type name, normalized labels, and
        hierarchy routing hint.

    Raises:
        ValueError: If *issue_type* is invalid (FR-008), or if
            *parent_issue_type* is provided but is not a non-empty member of
            ``VALID_ISSUE_TYPES``.
        IssueTypeMappingError: If *issue_type* cannot be resolved (FR-006).
    """
    _validate_issue_type(issue_type)
    if parent_issue_type is not None:
        if not isinstance(parent_issue_type, str) or not parent_issue_type.strip():
            raise ValueError(
                f"parent_issue_type must be None or a non-empty string. Valid types: {sorted(VALID_ISSUE_TYPES)}"
            )
        if parent_issue_type not in VALID_ISSUE_TYPES:
            raise ValueError(
                f"unsupported parent_issue_type {parent_issue_type!r}. Valid types: {sorted(VALID_ISSUE_TYPES)}"
            )

    mapping = type_mapping if type_mapping is not None else JIRA_DEFAULT_TYPE_NAMES
    type_name = _resolve_type(issue_type, mapping)

    # Hierarchy routing (FR-004)
    # Note: comparisons against neutral type strings ("subtask", "epic") are
    # intentional — these are provider-agnostic identifiers from
    # VALID_ISSUE_TYPES, not provider-native strings (SC-003 / FR-005).
    route: str | None
    if parent_issue_type is None:
        # root node — no parent to link against (FR-004: route MUST be None)
        route = None
    elif issue_type == "subtask":
        # subtask routes to the standard parent field regardless of parent type
        route = _ROUTE_PARENT
    elif issue_type == "epic":
        # epics never have a parent route
        route = None
    elif parent_issue_type == "epic":
        route = _ROUTE_EPIC_LINK
    else:
        route = None

    labels = _normalize_jira_labels(declared_labels)
    return JiraMappingResult(type_name=type_name, labels=labels, route=route)


# ---------------------------------------------------------------------------
# Config validation and loaders (FR-007)
# ---------------------------------------------------------------------------


def _validate_mapping_config(
    raw_dict: dict[str, Any],
    field_name: str,
    config_path: str | None = None,
) -> TypeMapping:
    """Validate a raw config dict as a valid mapping table (FR-007).

    Keys must be lowercase members of :data:`VALID_ISSUE_TYPES` and values
    must be non-empty strings.

    Args:
        raw_dict: The dict parsed from config.
        field_name: Config field name for error messages.
        config_path: Config file path for error messages.

    Returns:
        The validated mapping as a :data:`TypeMapping`.

    Raises:
        ValueError: On invalid keys or values.
    """
    validated: TypeMapping = {}
    for key, value in raw_dict.items():
        location = f" in {config_path}" if config_path else ""
        if key not in VALID_ISSUE_TYPES:
            raise ValueError(f"Invalid key {key!r} in {field_name}{location}. Valid keys: {sorted(VALID_ISSUE_TYPES)}")
        if not isinstance(value, str) or not value.strip():
            raise ValueError(
                f"Invalid value for {key!r} in {field_name}{location}. Value must be a non-empty string, got {value!r}"
            )
        validated[key] = value.strip()
    return validated


def load_github_type_mapping(
    platform_config: dict[str, Any],
    config_path: str | None = None,
) -> TypeMapping:
    """Load GitHub issue-type-to-label mapping from platform config (FR-002).

    Extracts ``platform_config["github"]["issue_type_labels"]``, validates,
    and merges overrides over :data:`GITHUB_DEFAULT_LABELS`.

    Args:
        platform_config: The platform section of agdt-config.json.
        config_path: Path to the config file for error messages.

    Returns:
        Merged mapping with defaults for any unspecified types.
    """
    github = platform_config.get("github")
    if not isinstance(github, dict):
        return dict(GITHUB_DEFAULT_LABELS)
    raw = github.get("issue_type_labels")
    if not isinstance(raw, dict):
        return dict(GITHUB_DEFAULT_LABELS)
    overrides = _validate_mapping_config(raw, "platform.github.issue_type_labels", config_path)
    return {**GITHUB_DEFAULT_LABELS, **overrides}


def load_jira_type_mapping(
    platform_config: dict[str, Any],
    config_path: str | None = None,
) -> TypeMapping:
    """Load Jira issue-type-to-name mapping from platform config (FR-002).

    Extracts ``platform_config["jira"]["issue_type_names"]``, validates,
    and merges overrides over :data:`JIRA_DEFAULT_TYPE_NAMES`.

    Args:
        platform_config: The platform section of agdt-config.json.
        config_path: Path to the config file for error messages.

    Returns:
        Merged mapping with defaults for any unspecified types.
    """
    jira = platform_config.get("jira")
    if not isinstance(jira, dict):
        return dict(JIRA_DEFAULT_TYPE_NAMES)
    raw = jira.get("issue_type_names")
    if not isinstance(raw, dict):
        return dict(JIRA_DEFAULT_TYPE_NAMES)
    overrides = _validate_mapping_config(raw, "platform.jira.issue_type_names", config_path)
    return {**JIRA_DEFAULT_TYPE_NAMES, **overrides}
