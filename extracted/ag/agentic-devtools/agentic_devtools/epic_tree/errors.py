"""Error types for epic-tree validation."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any

# --- Error category constants ---
CATEGORY_CYCLE_DETECTED = "cycle_detected"
CATEGORY_UNRESOLVED_REFERENCE = "unresolved_reference"
CATEGORY_DEPTH_EXCEEDED = "depth_exceeded"
CATEGORY_DISALLOWED_LABEL = "disallowed_label"
CATEGORY_INVALID_REF_FORMAT = "invalid_ref_format"
CATEGORY_DUPLICATE_REF = "duplicate_ref"
CATEGORY_DISALLOWED_ISSUE_TYPE = "disallowed_issue_type"
CATEGORY_MISSING_BODY_SECTION = "missing_body_section"


@dataclass(frozen=True)
class EpicTreeValidationError:
    """A single validation error from epic-tree schema or semantic checks.

    Attributes:
        path: RFC 6901 JSON Pointer to the failing instance location.
        message: Validator-provided error summary.
        keyword: For structural (Pass 1) errors this is the failed JSON Schema
            keyword (e.g. ``required``, ``type``, ``pattern``,
            ``additionalProperties``).  For semantic (Pass 2) errors it holds
            the semantic category identifier (e.g. ``duplicate_ref``,
            ``cycle_detected``).  Callers can distinguish the two origins by
            checking whether the value is a known JSON Schema keyword.
        property_name: Missing or unexpected property name, when available
            (populated only for ``required`` and ``additionalProperties``
            schema errors).
    """

    path: str
    message: str
    keyword: str
    property_name: str | None = None


@dataclass(frozen=True)
class ValidationReportEntry:
    """A single entry in a structured validation report.

    Attributes:
        category: Error category identifier.

            * **JSON Schema structural errors** (Pass 1) set this to the
              failed JSON Schema keyword, e.g. ``required``, ``type``,
              ``pattern``, ``additionalProperties``.
            * **Semantic-check errors** (Pass 2) set this to a semantic
              identifier, e.g. ``duplicate_ref``, ``unresolved_reference``,
              ``cycle_detected``, ``depth_exceeded``, ``disallowed_label``,
              ``disallowed_issue_type``, ``missing_body_section``,
              ``invalid_ref_format``.

        message: Human-readable error description.
        paths: List of locations where the error occurs.  The format depends
            on which validation pass produced the entry:

            * **JSON Schema structural errors** (Pass 1) use RFC 6901 JSON
              Pointer notation, e.g. ``"/epic/features/0"``.
            * **Semantic-check errors** (Pass 2) use dot-notation with bracket
              indices, e.g. ``"epic.features[0].subtasks[1]"``.

            Multi-location errors such as ``duplicate_ref`` and
            ``cycle_detected`` carry more than one path entry, one per
            affected node.
        property_name: Missing or unexpected property name.  Populated only
            for ``required`` and ``additionalProperties`` structural errors;
            ``None`` for all other error categories.
    """

    category: str
    message: str
    paths: list[str] = field(default_factory=list)
    property_name: str | None = None


@dataclass
class ValidationReport:
    """Aggregated validation report for an epic-tree document.

    Collects all errors found during validation (not fail-fast within a pass).
    A single report contains either structural JSON Schema errors (Pass 1) or
    semantic-rule errors (Pass 2), depending on where validation stops.

    Attributes:
        valid: Whether the document passed all validation checks.
        errors: List of all validation error entries.
        warnings: List of non-blocking warning entries (do not affect ``valid``).
    """

    valid: bool = True
    errors: list[ValidationReportEntry] = field(default_factory=list)
    warnings: list[ValidationReportEntry] = field(default_factory=list)

    def add_error(
        self,
        category: str,
        message: str,
        paths: list[str] | None = None,
        property_name: str | None = None,
    ) -> None:
        """Add an error entry and mark the report as invalid."""
        self.valid = False
        self.errors.append(
            ValidationReportEntry(
                category=category,
                message=message,
                paths=paths or [],
                property_name=property_name,
            )
        )

    def add_warning(
        self,
        category: str,
        message: str,
        paths: list[str] | None = None,
        property_name: str | None = None,
    ) -> None:
        """Add a warning entry without affecting ``valid``."""
        self.warnings.append(
            ValidationReportEntry(
                category=category,
                message=message,
                paths=paths or [],
                property_name=property_name,
            )
        )

    def sort_entries(self) -> None:
        """Sort errors and warnings in deterministic order.

        Sorts each entry's ``paths`` list first, then sorts both ``errors``
        and ``warnings`` using ``_entry_sort_key`` (primary: first path tokens,
        secondary: category, tertiary: message).
        """
        for entry in self.errors:
            entry.paths.sort(key=_path_sort_key)
        for entry in self.warnings:
            entry.paths.sort(key=_path_sort_key)
        self.errors.sort(key=_entry_sort_key)
        self.warnings.sort(key=_entry_sort_key)

    def to_dict(self) -> dict[str, Any]:
        """Serialize the report to a plain dictionary.

        Returns:
            Dict with ``valid``, ``errors``, and ``warnings`` keys.
            Each entry dict includes ``category``, ``message``, ``paths``,
            and ``property_name`` (present even when ``None``).
        """
        return {
            "valid": self.valid,
            "errors": [_entry_to_dict(e) for e in self.errors],
            "warnings": [_entry_to_dict(e) for e in self.warnings],
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ValidationReport:
        """Deserialize a report from a plain dictionary.

        Requires ``valid``, ``errors``, and ``warnings`` top-level keys.
        Each entry must have ``category``, ``message``, and ``paths``.
        Unknown top-level and per-entry keys are silently ignored.
        Unknown category values are accepted without error.

        Raises:
            ValueError: If a mandatory key is missing.
        """
        for key in ("valid", "errors", "warnings"):
            if key not in data:
                raise ValueError(f"Missing mandatory key: '{key}'")

        errors = [_entry_from_dict(e) for e in data["errors"]]
        warnings = [_entry_from_dict(e) for e in data["warnings"]]
        # Preserve the report invariant: non-empty errors always means invalid.
        valid = len(errors) == 0
        return cls(valid=valid, errors=errors, warnings=warnings)


def _entry_to_dict(entry: ValidationReportEntry) -> dict[str, Any]:
    """Convert a ValidationReportEntry to a serializable dict."""
    return {
        "category": entry.category,
        "message": entry.message,
        "paths": list(entry.paths),
        "property_name": entry.property_name,
    }


def _entry_from_dict(data: dict[str, Any]) -> ValidationReportEntry:
    """Reconstruct a ValidationReportEntry from a dict.

    Raises:
        ValueError: If a mandatory key (``category``, ``message``, or ``paths``) is missing.
    """
    try:
        return ValidationReportEntry(
            category=data["category"],
            message=data["message"],
            paths=list(data["paths"]),
            property_name=data.get("property_name"),
        )
    except KeyError as exc:
        raise ValueError(f"Missing mandatory entry key: {exc}") from exc


_DOT_SPLIT = re.compile(r"\.")
_BRACKET_SPLIT = re.compile(r"\[(\d+)\]")


def _parse_path_tokens(path: str) -> list[str | int]:
    """Parse a path string into a list of tokens for comparison.

    Supports two formats:
    - Dot-notation with bracket indices: ``epic.features[0].subtasks[1]``
    - JSON Pointer (RFC 6901): ``/epic/features/0``

    Returns:
        List of string or integer tokens. Integer tokens are used for
        array indices to ensure numeric (not lexicographic) sorting.
    """
    if not path:
        return []

    # JSON Pointer format: starts with /
    if path.startswith("/"):
        raw_parts = path[1:].split("/") if len(path) > 1 else []
        tokens: list[str | int] = []
        for part in raw_parts:
            # Unescape JSON Pointer: ~1 → /, ~0 → ~
            unescaped = part.replace("~1", "/").replace("~0", "~")
            try:
                tokens.append(int(unescaped))
            except ValueError:
                tokens.append(unescaped)
        return tokens

    # Dot-notation format: epic.features[0].subtasks[1]
    tokens = []
    for segment in _DOT_SPLIT.split(path):
        # Split bracket indices: "features[0]" → "features", "0"
        bracket_parts = _BRACKET_SPLIT.split(segment)
        for i, part in enumerate(bracket_parts):
            if not part:
                continue
            if i % 2 == 1:
                # Inside brackets — numeric index
                tokens.append(int(part))
            else:
                tokens.append(part)
    return tokens


def _path_sort_key(path: str) -> list[tuple[int, int | str]]:
    """Sort key for individual path strings within an entry's paths list."""
    tokens = _parse_path_tokens(path)
    # Use (0, int) for integers and (1, str) for strings to sort ints before strings
    return [(0, t) if isinstance(t, int) else (1, t) for t in tokens]


def _entry_sort_key(
    entry: ValidationReportEntry,
) -> tuple[list[tuple[int, int | str]], str, str]:
    """Compute a deterministic sort key for a validation report entry.

    Sort order:
    1. Primary: Tokens of the first path (numeric indices sort numerically).
    2. Secondary: Category (alphabetical).
    3. Tertiary: Message (alphabetical).
    """
    first_path = entry.paths[0] if entry.paths else ""
    return (_path_sort_key(first_path), entry.category, entry.message)


class EpicTreeLoadError(Exception):
    """Raised when loading an epic-tree document fails validation.

    Wraps an aggregated collection of :class:`EpicTreeValidationError` entries
    so that callers receive all problems at once rather than just the first.

    Attributes:
        errors: Tuple of all validation errors found in the document.
    """

    def __init__(self, errors: list[EpicTreeValidationError]) -> None:
        self._errors = tuple(errors)
        super().__init__(str(self))

    @property
    def errors(self) -> tuple[EpicTreeValidationError, ...]:
        """All validation errors found in the document."""
        return self._errors

    def __str__(self) -> str:
        count = len(self._errors)
        lines = [f"{count} validation error(s) in epic tree:"]
        for err in self._errors[:5]:
            lines.append(f"  {err.path}: {err.message}")
        if count > 5:
            lines.append(f"  ... and {count - 5} more")
        return "\n".join(lines)


class VersionMismatchError(Exception):
    """Raised when a document's ``schemaVersion`` is not supported.

    Attributes:
        found_version: The version string present in the document.
        supported_major: The major version number the consumer supports.
    """

    def __init__(self, found_version: str, supported_major: int) -> None:
        self.found_version = found_version
        self.supported_major = supported_major
        super().__init__(
            f"Unsupported schema version '{found_version}': only major version {supported_major} is supported"
        )


class UnresolvedRefError(KeyError):
    """Raised when a blocking ref cannot be resolved within the epic tree.

    Inherits from ``KeyError`` for backward compatibility with callers that
    catch ``KeyError``.  Overrides ``__str__`` to bypass ``KeyError``'s default
    quoting behaviour.

    Attributes:
        error_payload: Machine-parseable dict with structured error fields:
            ``unresolved_ref``, ``declaring_ref``, ``direction``,
            ``scope``, ``category``.
    """

    def __init__(
        self,
        message: str,
        *,
        unresolved_ref: str,
        declaring_ref: str,
        direction: str,
    ) -> None:
        self.error_payload: dict[str, str] = {
            "unresolved_ref": unresolved_ref,
            "declaring_ref": declaring_ref,
            "direction": direction,
            "scope": "intra_epic_v1",
            "category": CATEGORY_UNRESOLVED_REFERENCE,
        }
        super().__init__(message)

    def __str__(self) -> str:
        """Return human-readable message without KeyError quoting."""
        return str(self.args[0]) if self.args else ""


class ConfigError(Exception):
    """Raised when epic-tree configuration is invalid.

    Attributes:
        config_path: Path to the configuration file.
        field: The specific field that failed validation.
        message: Human-readable explanation of what went wrong.
    """

    def __init__(self, config_path: str, field_name: str, message: str) -> None:
        self.config_path = config_path
        self.field = field_name
        super().__init__(f"Config error in '{config_path}' at field '{field_name}': {message}")
