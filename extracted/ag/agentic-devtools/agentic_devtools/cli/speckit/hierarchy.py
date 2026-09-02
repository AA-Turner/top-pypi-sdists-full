"""Hierarchy YAML schema and data models for SpecKit nested spec management.

Defines the ``hierarchy.yml`` schema used at each level of the nested spec
directory structure, along with Python data models that represent the hierarchy
in code.
"""

from __future__ import annotations

import re
import stat as _stat
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Protocol, runtime_checkable

import yaml

try:
    import jsonschema
except ImportError:  # pragma: no cover
    jsonschema = None  # type: ignore[assignment]

__all__ = [
    "HIERARCHY_SCHEMA",
    "ChildEntry",
    "HierarchyDetector",
    "HierarchyLevel",
    "HierarchyNode",
    "HierarchyValidationError",
    "get_child_position",
    "get_first_child",
    "get_next_child",
    "load_hierarchy",
    "save_hierarchy",
]


class HierarchyValidationError(ValueError):
    """Raised when a hierarchy YAML file fails validation.

    Attributes:
        field_name: The field that caused the validation failure.
        detail: Human-readable description of the violation.
    """

    def __init__(self, field_name: str, detail: str) -> None:
        self.field_name = field_name
        self.detail = detail
        super().__init__(f"Validation error on '{field_name}': {detail}")


@runtime_checkable
class HierarchyDetector(Protocol):
    """Protocol for detecting hierarchy from issue metadata.

    Downstream detector implementations (e.g., GitHub, Jira, Azure DevOps)
    should implement this protocol to provide a consistent interface for
    determining hierarchy level and constructing typed hierarchy nodes from
    issue metadata.

    This protocol defines the stable contract that hierarchy-aware components
    (cascade triggers, ordering logic, artifact generators) can depend on
    without coupling to specific issue management platforms.
    """

    def detect_hierarchy(self, issue_key: str) -> HierarchyNode:
        """Detect and construct hierarchy node from issue metadata.

        Args:
            issue_key: Issue identifier (e.g., GitHub issue number, Jira key).

        Returns:
            HierarchyNode representing the issue with its determined level,
            parent reference, and ordered list of children.

        Raises:
            HierarchyValidationError: If issue data is invalid or hierarchy
                cannot be determined from available metadata.
        """
        ...  # pragma: no cover


class HierarchyLevel(Enum):
    """Three-level hierarchy: Epic → Feature → Task."""

    EPIC = "epic"
    FEATURE = "feature"
    TASK = "task"


@dataclass
class ChildEntry:
    """An entry in the children list of a hierarchy node.

    Attributes:
        key: Child issue identifier (normalized to string).
        title: Human-readable issue title.
        order: Advisory integer for intended position (None if unset).
    """

    key: str
    title: str
    order: int | None

    def __post_init__(self) -> None:
        """Validate fields and normalize key to string."""
        if isinstance(self.key, bool):
            raise HierarchyValidationError("key", "Boolean values are not valid issue identifiers")
        if not isinstance(self.key, (str, int)):
            raise HierarchyValidationError("key", "Expected string or integer issue identifier")
        if not isinstance(self.title, str) or not self.title:
            raise HierarchyValidationError("title", "Expected non-empty string")
        if self.order is not None and (isinstance(self.order, bool) or not isinstance(self.order, int)):
            raise HierarchyValidationError("order", "Expected integer or None")
        self.key = str(self.key)

    def to_dict(self) -> dict[str, Any]:
        """Serialize to a dict with canonical key order."""
        return {
            "key": self.key,
            "title": self.title,
            "order": self.order,
        }


@dataclass
class HierarchyNode:
    """Represents a single node in the spec hierarchy tree.

    Attributes:
        title: Human-readable issue title.
        level: The hierarchy level (epic, feature, or task).
        parent: Parent issue key (None for top-level epics).
        children: Ordered list of child entries.
        processed_at: Timezone-aware datetime of last processing (None if unprocessed).
    """

    title: str
    level: HierarchyLevel
    parent: str | None = None
    children: list[ChildEntry] = field(default_factory=list)
    processed_at: datetime | None = None

    def __post_init__(self) -> None:
        """Validate fields and normalize parent to string."""
        if not isinstance(self.title, str) or not self.title:
            raise HierarchyValidationError("title", "Expected non-empty string")
        if not isinstance(self.level, HierarchyLevel):
            raise HierarchyValidationError("level", "Expected HierarchyLevel")
        if self.parent is not None:
            if isinstance(self.parent, bool):
                raise HierarchyValidationError(
                    "parent",
                    "Boolean values are not valid issue identifiers",
                )
            if not isinstance(self.parent, (str, int)):
                raise HierarchyValidationError("parent", "Expected string, integer, or null")
            self.parent = str(self.parent)
        if not isinstance(self.children, list):
            raise HierarchyValidationError("children", "Expected list of ChildEntry instances")
        for index, child in enumerate(self.children):
            if not isinstance(child, ChildEntry):
                raise HierarchyValidationError(
                    f"children.{index}",
                    "Expected ChildEntry instance",
                )
        if self.processed_at is not None and not isinstance(self.processed_at, datetime):
            raise HierarchyValidationError("processed_at", "Expected datetime or null")

    def to_dict(self) -> dict[str, Any]:
        """Serialize to a dict with canonical key order."""
        processed_at = self.processed_at
        if processed_at is not None and processed_at.tzinfo is None:
            processed_at = processed_at.replace(tzinfo=timezone.utc)

        return {
            "title": self.title,
            "level": self.level.value,
            "parent": self.parent,
            "children": [child.to_dict() for child in self.children],
            "processed_at": (processed_at.isoformat() if processed_at else None),
        }


# JSON Schema for hierarchy.yml validation
HIERARCHY_SCHEMA: dict[str, Any] = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Hierarchy YAML Schema",
    "description": "Schema for hierarchy.yml files in the SpecKit nested spec structure.",
    "type": "object",
    "required": ["title", "level", "children"],
    "properties": {
        "title": {
            "type": "string",
            "minLength": 1,
            "description": "Human-readable issue title.",
        },
        "level": {
            "type": "string",
            "enum": ["epic", "feature", "task"],
            "description": "Hierarchy level.",
        },
        "parent": {
            "description": "Parent issue key (null for top-level epics).",
            "oneOf": [
                {"type": "string"},
                {"type": "integer"},
                {"type": "null"},
            ],
        },
        "children": {
            "type": "array",
            "description": "Ordered list of child entries.",
            "items": {
                "type": "object",
                "required": ["key", "title"],
                "properties": {
                    "key": {
                        "description": "Child issue identifier.",
                        "oneOf": [
                            {"type": "string"},
                            {"type": "integer"},
                        ],
                    },
                    "title": {
                        "type": "string",
                        "minLength": 1,
                    },
                    "order": {
                        "type": ["integer", "null"],
                    },
                },
                "additionalProperties": False,
            },
        },
        "processed_at": {
            "description": "ISO-8601 timestamp of last processing.",
            "oneOf": [
                {
                    "type": "string",
                    "pattern": (
                        r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}"
                        r"(\.\d{1,6})?(Z|[+-]\d{2}:\d{2})?$"
                    ),
                },
                {"type": "null"},
            ],
        },
    },
    "additionalProperties": False,
}


def _get_validation_error_field(exc: Any) -> str:
    """Return the most actionable field path from a jsonschema validation error."""
    path_parts = [str(part) for part in exc.absolute_path]

    if exc.validator == "required" and isinstance(exc.instance, dict):
        missing_keys = [str(key) for key in exc.validator_value if key not in exc.instance]
        if missing_keys:
            path_parts.append(missing_keys[0])
    elif exc.validator == "additionalProperties":
        extra_key: str | None = None
        params = getattr(exc, "params", None)
        if isinstance(params, dict):
            raw_extra = params.get("additionalProperties")
            if raw_extra is not None:
                extra_key = str(raw_extra)
        if extra_key is None and isinstance(exc.instance, dict) and isinstance(exc.schema, dict):
            schema_properties = exc.schema.get("properties")
            if isinstance(schema_properties, dict):
                extras = [str(key) for key in exc.instance if key not in schema_properties]
                if extras:
                    extra_key = extras[0]
        if extra_key is None:
            message_match = re.search(r"[\"']([^\"']+)[\"']\s+was unexpected", str(exc.message))
            if message_match:
                extra_key = message_match.group(1)
        if extra_key:
            path_parts.append(extra_key)

    return ".".join(path_parts) or exc.validator


def _parse_timestamp(value: Any) -> datetime | None:
    """Parse an ISO-8601 timestamp into a timezone-aware datetime.

    Accepts a string, an already-parsed ``datetime`` (e.g. from PyYAML implicit
    scalar decoding), or ``None``.  Any other type raises
    ``HierarchyValidationError`` instead of propagating an ``AttributeError``.

    - Trailing 'Z' is replaced with '+00:00' for Python 3.10 compat.
    - Naive datetimes are assumed UTC.
    - Returns ``None`` if *value* is ``None``.

    Raises:
        HierarchyValidationError: If *value* cannot be parsed or is an unexpected type.
    """
    if value is None:
        return None

    if isinstance(value, datetime):
        # PyYAML may auto-parse unquoted ISO-8601 scalars to datetime objects;
        # handle them directly rather than crashing on .endswith().
        if value.tzinfo is None:
            return value.replace(tzinfo=timezone.utc)
        return value

    if not isinstance(value, str):
        raise HierarchyValidationError(
            "processed_at",
            f"Expected string or null, got {type(value).__name__}",
        )

    normalized = value
    if normalized.endswith("Z"):
        normalized = normalized[:-1] + "+00:00"

    try:
        dt = datetime.fromisoformat(normalized)
    except (ValueError, TypeError) as exc:
        raise HierarchyValidationError(
            "processed_at",
            f"Invalid ISO-8601 timestamp: {value!r}",
        ) from exc

    # Normalize naive datetimes to UTC
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)

    return dt


def load_hierarchy(path: Path) -> HierarchyNode:
    """Load a hierarchy.yml file and return a typed HierarchyNode.

    Args:
        path: Path to the hierarchy.yml file.

    Returns:
        A fully populated HierarchyNode instance.

    Raises:
        FileNotFoundError: If the file does not exist.
        HierarchyValidationError: If the file content is invalid.
    """
    # Use stat() rather than exists() so that OS errors like PermissionError on the
    # parent directory are wrapped in HierarchyValidationError instead of being silently
    # swallowed by exists() and misreported as FileNotFoundError.  The stat result is
    # also reused to check for a regular file (via S_ISREG), avoiding a second round-trip
    # and the TOCTOU window that a separate path.is_file() call would introduce.
    try:
        st = path.stat()
    except FileNotFoundError as exc:
        # Preserve errno and filename attributes when re-raising
        raise FileNotFoundError(exc.errno, f"Hierarchy file not found: {path}", str(path)) from exc
    except OSError as exc:
        raise HierarchyValidationError("file", f"Unable to read file: {exc}") from exc
    if not _stat.S_ISREG(st.st_mode):
        raise HierarchyValidationError("file", f"Expected a file path, got {path}")

    try:
        content = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        raise
    except UnicodeDecodeError as exc:
        raise HierarchyValidationError("file", "File is not valid UTF-8") from exc
    except OSError as exc:
        raise HierarchyValidationError("file", f"Unable to read file: {exc}") from exc

    if not content.strip():
        raise HierarchyValidationError("file", "File is empty")

    try:
        data = yaml.safe_load(content)
    except yaml.YAMLError as exc:
        raise HierarchyValidationError("file", f"YAML parse error: {str(exc).splitlines()[0]}") from exc

    if not isinstance(data, dict):
        raise HierarchyValidationError("file", f"Expected a YAML mapping, got {type(data).__name__}")

    # Normalize: PyYAML may auto-parse unquoted ISO-8601 scalars to datetime objects.
    # Convert to an ISO string so schema validation and _parse_timestamp receive a string.
    raw_ts = data.get("processed_at")
    if isinstance(raw_ts, datetime):
        data["processed_at"] = raw_ts.isoformat()

    # JSON Schema validation
    if jsonschema is not None:
        try:
            jsonschema.validate(data, HIERARCHY_SCHEMA)
        except jsonschema.ValidationError as exc:
            raise HierarchyValidationError(
                _get_validation_error_field(exc),
                exc.message,
            ) from exc
    else:
        # Fallback validation when jsonschema is not available
        for required in ("title", "level", "children"):
            if required not in data:
                raise HierarchyValidationError(required, "Missing required field")

        # Check for unexpected top-level keys to match JSON Schema behavior
        allowed_keys = {"title", "level", "parent", "children", "processed_at"}
        unexpected_keys = set(data.keys()) - allowed_keys
        if unexpected_keys:
            unexpected_key = sorted(unexpected_keys)[0]
            raise HierarchyValidationError(
                unexpected_key, f"Additional properties are not allowed ('{unexpected_key}' was unexpected)"
            )

    # Parse level
    level_str = data.get("level")
    try:
        level = HierarchyLevel(level_str)
    except (TypeError, ValueError, KeyError) as exc:  # pragma: no cover — guarded by schema
        valid = ", ".join(m.value for m in HierarchyLevel)
        raise HierarchyValidationError(
            "level",
            f"Invalid level {level_str!r}. Valid options: {valid}",
        ) from exc

    # Parse parent (normalize int to str)
    parent_raw = data.get("parent")
    is_valid_parent_type = isinstance(parent_raw, str) or (
        isinstance(parent_raw, int) and not isinstance(parent_raw, bool)
    )
    if parent_raw is not None and not is_valid_parent_type:
        raise HierarchyValidationError("parent", "Expected string, integer, or null")
    parent: str | None = str(parent_raw) if parent_raw is not None else None

    # Parse children
    children_raw = data.get("children")
    if not isinstance(children_raw, list):
        raise HierarchyValidationError("children", "Expected array")

    children: list[ChildEntry] = []
    for index, child_data in enumerate(children_raw):
        if not isinstance(child_data, dict):
            raise HierarchyValidationError(f"children.{index}", "Expected mapping")
        for required in ("key", "title"):
            if required not in child_data:
                raise HierarchyValidationError(
                    f"children.{index}.{required}",
                    "Missing required field",
                )
        # Check for unexpected child keys to match JSON Schema behavior
        allowed_child_keys = {"key", "title", "order"}
        unexpected_child_keys = set(child_data.keys()) - allowed_child_keys
        if unexpected_child_keys:
            unexpected_child_key = sorted(unexpected_child_keys)[0]
            raise HierarchyValidationError(
                f"children.{index}.{unexpected_child_key}",
                f"Additional properties are not allowed ('{unexpected_child_key}' was unexpected)",
            )
        if not isinstance(child_data["key"], str) and not (
            isinstance(child_data["key"], int) and not isinstance(child_data["key"], bool)
        ):
            raise HierarchyValidationError(f"children.{index}.key", "Expected string or integer")
        if not isinstance(child_data["title"], str) or not child_data["title"]:
            raise HierarchyValidationError(f"children.{index}.title", "Expected non-empty string")
        order_raw = child_data.get("order")
        if order_raw is not None and (not isinstance(order_raw, int) or isinstance(order_raw, bool)):
            raise HierarchyValidationError(f"children.{index}.order", "Expected integer or null")
        children.append(
            ChildEntry(
                key=str(child_data["key"]),
                title=child_data["title"],
                order=order_raw,
            )
        )

    # Parse processed_at
    processed_at = _parse_timestamp(data.get("processed_at"))

    title = data.get("title")
    if not isinstance(title, str) or not title:
        raise HierarchyValidationError("title", "Expected non-empty string")

    return HierarchyNode(
        title=title,
        level=level,
        parent=parent,
        children=children,
        processed_at=processed_at,
    )


def save_hierarchy(node: HierarchyNode, path: Path) -> None:
    """Save a HierarchyNode to a hierarchy.yml file.

    Creates parent directories if they do not exist. Produces canonical
    YAML output suitable for round-trip fidelity checks.

    Args:
        node: The hierarchy node to serialize.
        path: Destination file path.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    data = node.to_dict()
    content = yaml.safe_dump(
        data,
        default_flow_style=False,
        sort_keys=False,
        allow_unicode=True,
    )
    path.write_text(content, encoding="utf-8")


# ---------------------------------------------------------------------------
# Ordering helpers
# ---------------------------------------------------------------------------


def _child_sort_key(child: ChildEntry, effective_order_for_none: int) -> tuple[int, int, int, str]:
    """Return a composite sort key for deterministic child ordering.

    The tuple components are:
      1. Effective order (explicit value, or *effective_order_for_none* for None)
      2. Numeric parsability flag (0 = numeric key, 1 = non-numeric key)
      3. Numeric value of key (0 for non-numeric)
      4. Lexicographic string key (final tiebreaker)
    """
    order = child.order if child.order is not None else effective_order_for_none
    try:
        numeric_value = int(child.key)
        return (order, 0, numeric_value, child.key)
    except (ValueError, TypeError):
        return (order, 1, 0, child.key)


def _sorted_children(children: list[ChildEntry]) -> list[ChildEntry]:
    """Return children sorted by composite key (no mutation of input list).

    Children with explicit order values are sorted by those values first.
    Children with ``None`` order are placed after all explicitly-ordered
    children, using ``max_existing_order + 1`` as their effective order.
    Ties are broken by numeric key value, then lexicographic string key.
    """
    # Compute max existing explicit order (0 when none exist)
    explicit_orders = [c.order for c in children if c.order is not None]
    max_existing_order = max(explicit_orders) if explicit_orders else 0
    effective_order_for_none = max_existing_order + 1

    return sorted(children, key=lambda c: _child_sort_key(c, effective_order_for_none))


def get_first_child(hierarchy: HierarchyNode) -> str | None:
    """Return the key of the child with the lowest order value.

    Returns None if the node has no children.
    """
    if not hierarchy.children:
        return None
    sorted_kids = _sorted_children(hierarchy.children)
    return sorted_kids[0].key


def get_next_child(hierarchy: HierarchyNode, current_key: str | int) -> str | None:
    """Return the key of the next child after *current_key* in sorted order.

    Args:
        hierarchy: The parent node.
        current_key: The key of the current child (int or str, normalized).

    Returns:
        The next child's key, or None if *current_key* is the last child
        or not found in the children list.
    """
    normalized_key = str(current_key)
    sorted_kids = _sorted_children(hierarchy.children)
    for i, child in enumerate(sorted_kids):
        if child.key == normalized_key:
            if i + 1 < len(sorted_kids):
                return sorted_kids[i + 1].key
            return None
    return None


def get_child_position(hierarchy: HierarchyNode, key: str | int) -> tuple[int, int]:
    """Return the 1-indexed position and total children count for *key*.

    Args:
        hierarchy: The parent node.
        key: The child key to locate (int or str, normalized).

    Returns:
        A tuple of (position, total) where position is 1-indexed.

    Raises:
        ValueError: If *key* is not found among the children.
    """
    normalized_key = str(key)
    sorted_kids = _sorted_children(hierarchy.children)
    for i, child in enumerate(sorted_kids):
        if child.key == normalized_key:
            return (i + 1, len(sorted_kids))
    available_keys = [c.key for c in sorted_kids]
    raise ValueError(f"Key {normalized_key!r} not found in children. Available keys: {available_keys}")
