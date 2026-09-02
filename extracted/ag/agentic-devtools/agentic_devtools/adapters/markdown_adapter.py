"""Markdown file-based issue adapter.

Stores issues as individual markdown files with YAML frontmatter under
``.agdt/issues/`` in the repository root.  Provides a lightweight
alternative for users who do not use Jira or GitHub Issues.
"""

from __future__ import annotations

import copy
import datetime
import re
import shutil
from pathlib import Path

import yaml

from agentic_devtools.adapters.base import (
    Comment,
    CommentResult,
    IssueAdapter,
    IssueDetailWithRaw,
    IssueFilters,
    IssueResult,
    IssueSummary,
    IssueTypeInfo,
    NormalizedIssue,
    PropertySchema,
)
from agentic_devtools.adapters.exceptions import AdapterValidationError

_ID_PATTERN = re.compile(r"^\d{3}$")
_ARCHIVE_PATTERN = re.compile(r"^A_(\d{3})$")

# ---------------------------------------------------------------------------
# Default schema constants
# ---------------------------------------------------------------------------

_DEFAULT_STATUS_VALUES: list[str] = ["open", "in-progress", "closed", "unknown"]

_DEFAULT_PROPERTIES: list[PropertySchema] = [
    {"name": "id", "type": "string", "required": False, "allowed_values": None},
    {"name": "title", "type": "string", "required": True, "allowed_values": None},
    {"name": "description", "type": "string", "required": False, "allowed_values": None},
    {"name": "status", "type": "string", "required": False, "allowed_values": _DEFAULT_STATUS_VALUES},
    {"name": "labels", "type": "array", "required": False, "allowed_values": None},
    {"name": "comments", "type": "array", "required": False, "allowed_values": None},
    {"name": "created_at", "type": "string", "required": False, "allowed_values": None},
]

_DEFAULT_TYPES: tuple[IssueTypeInfo, ...] = (
    {"name": "task", "description": "A general work item or action to complete"},
    {"name": "bug", "description": "A defect or unexpected behavior to fix"},
    {"name": "feature", "description": "A new capability or enhancement to implement"},
    {"name": "story", "description": "A user story describing desired functionality"},
)


def _coerce_str(value: object, default: str = "") -> str:
    """Coerce a YAML-loaded value to ``str``.

    Returns *default* when *value* is ``None``, otherwise ``str(value)``.
    Strings are returned as-is (no unnecessary conversion).
    """
    if value is None:
        return default
    return value if isinstance(value, str) else str(value)


def _resolve_str(raw: dict, key: str, structured_value: str, default: str = "") -> str:
    """Resolve a string field with raw-first priority.

    Returns the raw value (coerced to ``str``) when present and usable
    (non-None, non-whitespace-only after coercion), otherwise falls back
    to *structured_value*, then *default*.
    """
    raw_val = raw.get(key)
    if raw_val is not None:
        coerced = raw_val if isinstance(raw_val, str) else str(raw_val)
        if coerced.strip():
            return coerced
    # Fall back to structured value
    if isinstance(structured_value, str) and structured_value.strip():
        return structured_value
    return default


def _resolve_list(raw: dict, key: str, structured_value: object) -> list:
    """Resolve a list field with raw-first priority.

    Returns the raw value when it is a ``list`` instance (including an
    empty ``[]``), otherwise falls back to *structured_value* if it is a
    list, and finally returns ``[]``.
    """
    raw_val = raw.get(key)
    if isinstance(raw_val, list):
        return raw_val
    if isinstance(structured_value, list):
        return structured_value
    return []


def _normalize_comment_entry(entry: dict[str, object], index: int) -> Comment:
    """Normalize a single dict comment entry to a :class:`Comment` TypedDict.

    Callers are responsible for ensuring *entry* is a ``dict`` (non-dict
    entries should be filtered out before calling this function).  The comment
    ID is resolved from ``id``, then ``comment_id``, then a positional
    fallback ``c{index}`` (1-indexed, counting only valid dict entries).
    """
    comment_id = ""
    for key in ("id", "comment_id"):
        if key not in entry:
            continue
        candidate = _coerce_str(entry.get(key))
        candidate_stripped = candidate.strip()
        if candidate_stripped:
            comment_id = candidate_stripped
            break
    if not comment_id:
        comment_id = f"c{index}"
    body = _coerce_str(entry.get("body", ""))
    created_at = _coerce_str(entry.get("created_at", ""))
    return Comment(comment_id=comment_id, body=body, created_at=created_at)


def _is_frontmatter_delimiter(line: str) -> bool:
    """Return ``True`` when *line* is an unindented ``---`` delimiter."""
    return line.startswith("---") and line.rstrip("\r\n") == "---"


class MarkdownAdapter(IssueAdapter):
    """Issue adapter that reads/writes markdown files in ``.agdt/issues/``."""

    def __init__(self, repo_path: str, schema_override: object | None = None) -> None:
        self._issues_dir = Path(repo_path) / ".agdt" / "issues"
        self._build_schema(schema_override)

    # ------------------------------------------------------------------
    # Schema construction
    # ------------------------------------------------------------------

    def _build_schema(self, schema_override: object | None) -> None:
        """Build internal schema structures from defaults or override."""
        if schema_override is not None:
            self._validate_schema_override(schema_override)
            # schema_override is validated as dict with "types" list
            override_dict: dict = schema_override  # type: ignore[assignment]
            types_list: list[IssueTypeInfo] = []
            types_map: dict[str, list[PropertySchema]] = {}
            for entry in override_dict["types"]:
                display_name = entry["name"].strip()
                name = display_name.lower()
                types_list.append({"name": display_name, "description": entry["description"]})
                props: list[PropertySchema] = []
                for p in entry["properties"]:
                    prop_name = p["name"].strip()
                    prop_type = p["type"].strip()
                    props.append(
                        {
                            "name": prop_name,
                            "type": prop_type,
                            "required": p["required"],
                            "allowed_values": list(p["allowed_values"]) if p["allowed_values"] is not None else None,
                        }
                    )
                types_map[name] = props
            self._types_list = types_list
            self._types_map = types_map
        else:
            self._types_list = [{"name": t["name"], "description": t["description"]} for t in _DEFAULT_TYPES]
            self._types_map = {
                t["name"]: [
                    {
                        "name": p["name"],
                        "type": p["type"],
                        "required": p["required"],
                        "allowed_values": list(p["allowed_values"]) if p["allowed_values"] is not None else None,
                    }
                    for p in _DEFAULT_PROPERTIES
                ]
                for t in _DEFAULT_TYPES
            }

    def _validate_schema_override(self, override: object) -> None:
        """Validate schema override structure eagerly."""
        if not isinstance(override, dict):
            raise AdapterValidationError(f"schema_override must be a dict, got {type(override).__name__}")
        if "types" not in override:
            raise AdapterValidationError("schema_override must contain a 'types' key")
        types = override["types"]
        if not isinstance(types, list):
            raise AdapterValidationError(f"schema_override['types'] must be a list, got {type(types).__name__}")
        seen_names: set[str] = set()
        for i, entry in enumerate(types):
            if not isinstance(entry, dict):
                raise AdapterValidationError(f"schema_override['types'][{i}] must be a dict")
            if "name" not in entry:
                raise AdapterValidationError(f"schema_override['types'][{i}] must have a 'name' key")
            name = entry["name"]
            if not isinstance(name, str) or not name.strip():
                raise AdapterValidationError(f"schema_override['types'][{i}]['name'] must be a non-empty string")
            lower_name = name.strip().lower()
            if lower_name in seen_names:
                raise AdapterValidationError(f"Duplicate type name after case normalization: '{lower_name}'")
            seen_names.add(lower_name)
            if "description" not in entry:
                raise AdapterValidationError(f"schema_override['types'][{i}] must have a 'description' key")
            description = entry["description"]
            if not isinstance(description, str):
                raise AdapterValidationError(f"schema_override['types'][{i}]['description'] must be a string")
            if "properties" not in entry:
                raise AdapterValidationError(f"schema_override['types'][{i}] must have a 'properties' key")
            properties = entry["properties"]
            if not isinstance(properties, list):
                raise AdapterValidationError(f"schema_override['types'][{i}]['properties'] must be a list")
            for j, prop in enumerate(properties):
                if not isinstance(prop, dict):
                    raise AdapterValidationError(f"schema_override['types'][{i}]['properties'][{j}] must be a dict")
                for key in ("name", "type", "required", "allowed_values"):
                    if key not in prop:
                        raise AdapterValidationError(
                            f"schema_override['types'][{i}]['properties'][{j}] must have a '{key}' key"
                        )
                if not isinstance(prop["name"], str):
                    raise AdapterValidationError(
                        f"schema_override['types'][{i}]['properties'][{j}]['name'] must be a string"
                    )
                if not prop["name"].strip():
                    raise AdapterValidationError(
                        f"schema_override['types'][{i}]['properties'][{j}]['name'] must be a non-empty string"
                    )
                if not isinstance(prop["type"], str):
                    raise AdapterValidationError(
                        f"schema_override['types'][{i}]['properties'][{j}]['type'] must be a string"
                    )
                if not prop["type"].strip():
                    raise AdapterValidationError(
                        f"schema_override['types'][{i}]['properties'][{j}]['type'] must be a non-empty string"
                    )
                if not isinstance(prop["required"], bool):
                    raise AdapterValidationError(
                        f"schema_override['types'][{i}]['properties'][{j}]['required'] must be a bool"
                    )
                av = prop["allowed_values"]
                if av is not None:
                    if not isinstance(av, list):
                        raise AdapterValidationError(
                            f"schema_override['types'][{i}]['properties'][{j}]['allowed_values'] must be a list or None"
                        )
                    for k, v in enumerate(av):
                        if not isinstance(v, str):
                            raise AdapterValidationError(
                                f"schema_override['types'][{i}]['properties'][{j}]"
                                f"['allowed_values'][{k}] must be a string, "
                                f"got {type(v).__name__}"
                            )

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _next_id(self) -> str:
        """Determine the next 3-digit zero-padded issue ID.

        If the current max ID is 999, archives all existing files first.
        """
        if not self._issues_dir.exists():
            return "001"

        existing = sorted(int(p.stem) for p in self._issues_dir.glob("*.md") if _ID_PATTERN.match(p.stem))
        if not existing:
            return "001"

        max_id = existing[-1]
        if max_id >= 999:
            self._archive()
            return "001"

        return f"{max_id + 1:03d}"

    def _archive(self) -> None:
        """Archive issue ``.md`` files whose stem is a 3-digit ID into a new archive folder.

        Non-issue markdown files (for example, ``readme.md``) are left in place.
        """
        existing_archives = sorted(
            int(m.group(1)) for d in self._issues_dir.iterdir() if d.is_dir() and (m := _ARCHIVE_PATTERN.match(d.name))
        )
        next_archive_num = (existing_archives[-1] + 1) if existing_archives else 0
        archive_dir = self._issues_dir / f"A_{next_archive_num:03d}"

        if archive_dir.exists():
            raise FileExistsError(f"Archive directory already exists: {archive_dir}")

        archive_dir.mkdir(parents=True)

        # Only archive files whose stem matches the 3-digit issue ID pattern,
        # so user-maintained files (e.g. readme.md) are not relocated.
        for md_file in self._issues_dir.glob("*.md"):
            if _ID_PATTERN.match(md_file.stem):
                shutil.move(str(md_file), str(archive_dir / md_file.name))

    @staticmethod
    def _write_issue(path: Path, frontmatter: dict, description: str) -> None:
        """Write an issue file with YAML frontmatter and markdown body."""
        yaml_str = yaml.safe_dump(frontmatter, default_flow_style=False, sort_keys=False)
        path.write_text(f"---\n{yaml_str}---\n{description}\n", encoding="utf-8")

    @staticmethod
    def _read_issue(path: Path, issue_id: str) -> tuple[dict, str]:
        """Read and parse an issue file, returning (frontmatter, description).

        Uses line-based delimiter detection so that ``---`` inside YAML
        scalar values (e.g. a title containing ``---``) does not break
        the parser.
        """
        content = path.read_text(encoding="utf-8")
        lines = content.splitlines(keepends=True)
        if not lines or not _is_frontmatter_delimiter(lines[0]):
            raise ValueError(f"Invalid frontmatter in issue {issue_id}")

        # Collect YAML frontmatter lines until the closing '---' delimiter
        # line.  Only an *unindented* ``---`` (no leading whitespace) is
        # treated as the closing delimiter so that ``---`` inside indented
        # YAML block scalars is not misinterpreted.
        fm_lines: list[str] = []
        i = 1
        while i < len(lines) and not _is_frontmatter_delimiter(lines[i]):
            fm_lines.append(lines[i])
            i += 1

        if i >= len(lines):
            raise ValueError(f"Invalid frontmatter in issue {issue_id}")

        fm_str = "".join(fm_lines)
        try:
            fm = yaml.safe_load(fm_str)
        except yaml.YAMLError as exc:
            raise ValueError(f"Invalid frontmatter in issue {issue_id}") from exc
        if not isinstance(fm, dict):
            raise ValueError(f"Invalid frontmatter in issue {issue_id}")

        # The description starts after the closing '---' line.
        description = "".join(lines[i + 1 :]).strip()
        return fm, description

    # ------------------------------------------------------------------
    # IssueAdapter interface
    # ------------------------------------------------------------------

    def create_issue(self, title: str, description: str, labels: list[str] | None = None) -> IssueResult:
        """Create a new markdown issue file."""
        self._issues_dir.mkdir(parents=True, exist_ok=True)
        issue_id = self._next_id()
        now = datetime.datetime.now(datetime.UTC).isoformat()

        frontmatter: dict = {
            "id": issue_id,
            "title": title,
            "status": "open",
            "labels": labels or [],
            "created_at": now,
            "comments": [],
        }
        self._write_issue(self._issues_dir / f"{issue_id}.md", frontmatter, description)
        return IssueResult(issue_id=issue_id, url="")

    def get_issue(self, issue_id: str) -> IssueDetailWithRaw:
        """Read a markdown issue file and return an :class:`IssueDetailWithRaw`."""
        path = self._issues_dir / f"{issue_id}.md"
        if not path.exists():
            raise FileNotFoundError(f"Issue {issue_id} not found")

        fm, description = self._read_issue(path, issue_id)

        raw_comments = fm.get("comments")
        if raw_comments is None:
            raw_comments = []
        elif not isinstance(raw_comments, list):
            raise ValueError(
                f"Issue {issue_id}: 'comments' frontmatter must be a list, got {type(raw_comments).__name__}"
            )

        comments: list[Comment] = []
        for c in raw_comments:
            if not isinstance(c, dict):
                raise ValueError(
                    f"Issue {issue_id}: each entry in 'comments' must be a mapping, got {type(c).__name__}"
                )
            comments.append(
                Comment(
                    comment_id=str(c.get("id", "")),
                    body=_coerce_str(c.get("body", "")),
                    created_at=_coerce_str(c.get("created_at", "")),
                )
            )

        raw_labels = fm.get("labels")
        if raw_labels is None:
            labels: list[str] = []
        elif isinstance(raw_labels, list):
            # Coerce non-string entries to str, skip None values.
            labels = [str(v) for v in raw_labels if v is not None]
        else:
            raise ValueError(f"Issue {issue_id}: 'labels' frontmatter must be a list, got {type(raw_labels).__name__}")

        # Always use the filename stem as canonical issue_id.  YAML may
        # parse unquoted ``id: 001`` as ``int(1)`` and lose zero-padding,
        # making the returned ID inconsistent with the file-based lookup.
        return IssueDetailWithRaw(
            issue_id=issue_id,
            title=_coerce_str(fm.get("title", "")),
            description=description,
            status=_coerce_str(fm.get("status", "")),
            labels=labels,
            url="",
            comments=comments,
        )

    def add_comment(self, issue_id: str, comment: str) -> CommentResult:
        """Append a comment to an existing markdown issue file."""
        path = self._issues_dir / f"{issue_id}.md"
        if not path.exists():
            raise FileNotFoundError(f"Issue {issue_id} not found")

        fm, description = self._read_issue(path, issue_id)
        existing_comments = fm.get("comments")
        if existing_comments is None:
            existing_comments = []
        elif not isinstance(existing_comments, list):
            raise ValueError(
                f"Issue {issue_id}: 'comments' frontmatter must be a list, got {type(existing_comments).__name__}"
            )
        # Validate each existing entry is a mapping so we don't silently
        # append a dict next to a non-dict and corrupt the file.
        for entry in existing_comments:
            if not isinstance(entry, dict):
                raise ValueError(
                    f"Issue {issue_id}: each entry in 'comments' must be a mapping, got {type(entry).__name__}"
                )
        next_num = len(existing_comments) + 1
        new_id = f"c{next_num}"
        now = datetime.datetime.now(datetime.UTC).isoformat()

        existing_comments.append({"id": new_id, "body": comment, "created_at": now})
        fm["comments"] = existing_comments

        self._write_issue(path, fm, description)
        return CommentResult(comment_id=new_id)

    def list_issues(self, filters: IssueFilters | None = None) -> list[IssueSummary]:
        """List all non-archived markdown issues, optionally filtered."""
        if not self._issues_dir.exists():
            return []

        summaries: list[IssueSummary] = []
        for md_file in sorted(self._issues_dir.glob("*.md")):
            if not _ID_PATTERN.match(md_file.stem):
                continue
            try:
                fm, _ = self._read_issue(md_file, md_file.stem)
            except (ValueError, OSError):
                continue

            raw_labels = fm.get("labels")
            # Normalize to list[str] — coerce non-string entries to str and
            # skip None, matching get_issue() behaviour.
            issue_labels: list[str] = (
                [str(v) for v in raw_labels if v is not None] if isinstance(raw_labels, list) else []
            )

            if filters:
                state_filter = filters.get("state")
                if state_filter and _coerce_str(fm.get("status", "")) != state_filter:
                    continue
                label_filter = filters.get("labels")
                if label_filter and not set(label_filter) & set(issue_labels):
                    continue

            # Always use the filename stem as canonical issue_id (see
            # get_issue — YAML may drop zero-padding from ``id: 001``).
            summaries.append(
                IssueSummary(
                    issue_id=md_file.stem,
                    title=_coerce_str(fm.get("title", "")),
                    status=_coerce_str(fm.get("status", "")),
                    labels=issue_labels,
                    url="",
                )
            )
        return summaries

    def normalize(self, issue_detail: IssueDetailWithRaw) -> NormalizedIssue:
        """Normalize a Markdown issue detail into a provider-agnostic representation.

        Parses YAML frontmatter fields from the ``raw`` dict (when available),
        falls back to structured ``IssueDetailWithRaw`` fields, and applies
        sensible defaults for any missing values.

        Raises:
            AdapterValidationError: When ``issue_id`` is empty, non-canonical,
                or when
                ``title`` cannot be resolved to a non-empty string from
                either raw or structured sources.
        """
        _raw = issue_detail.get("raw")
        raw: dict = _raw if isinstance(_raw, dict) else {}

        # FR-006: issue_id always from structured field (filename stem), never from raw
        issue_id = _coerce_str(issue_detail.get("issue_id"))
        if not issue_id.strip():
            raise AdapterValidationError("MarkdownAdapter.normalize(): issue_id must be a non-empty string")
        if not _ID_PATTERN.match(issue_id):
            raise AdapterValidationError(
                "MarkdownAdapter.normalize(): issue_id must match the 3-digit Markdown ID format"
            )

        # FR-006: title resolved from raw first, then structured; raise if both empty
        title = _resolve_str(raw, "title", _coerce_str(issue_detail.get("title")))
        if not title.strip():
            raise AdapterValidationError("MarkdownAdapter.normalize(): title must be a non-empty string")

        # FR-004: URL construction
        url = f".agdt/issues/{issue_id}.md"

        # FR-002: defaults for optional string fields
        status = _resolve_str(raw, "status", _coerce_str(issue_detail.get("status")), default="unknown")
        description = _resolve_str(raw, "description", _coerce_str(issue_detail.get("description")))
        created_at = _resolve_str(raw, "created_at", _coerce_str(issue_detail.get("created_at", "")))
        updated_at = _resolve_str(raw, "updated_at", _coerce_str(issue_detail.get("updated_at", "")))

        # FR-005: labels list resolution with item coercion, None-skipping
        raw_labels = _resolve_list(raw, "labels", issue_detail.get("labels"))
        labels: list[str] = [str(item) for item in raw_labels if item is not None]

        # Comments resolution with entry normalization.
        # The positional counter increments only for accepted dict entries so
        # that skipped non-dict items do not create gaps in the fallback IDs
        # (matching the add_comment() convention of numbering valid comments
        # sequentially).
        raw_comments = _resolve_list(raw, "comments", issue_detail.get("comments"))
        comments: list[Comment] = []
        pos = 0
        for entry in raw_comments:
            if not isinstance(entry, dict):
                continue
            pos += 1
            comments.append(_normalize_comment_entry(entry, pos))

        # FR-003: provider always "markdown", FR-007: preserve raw dict
        return NormalizedIssue(
            issue_id=issue_id,
            title=title,
            url=url,
            provider="markdown",
            description=description,
            status=status,
            labels=labels,
            comments=comments,
            created_at=created_at,
            updated_at=updated_at,
            raw=raw,
        )

    def get_issue_types(self) -> list[IssueTypeInfo]:
        """Return available issue types for the Markdown adapter."""
        return copy.deepcopy(self._types_list)

    def get_type_properties(self, type_name: str) -> list[PropertySchema]:
        """Return field schema for a Markdown issue type.

        Args:
            type_name: Issue type name (case-insensitive lookup).

        Returns:
            Deep copy of the property schema list for the given type.

        Raises:
            ValueError: If type_name is empty/whitespace or not found.
        """
        if not type_name or not type_name.strip():
            raise ValueError("type_name must be a non-empty string")
        key = type_name.strip().lower()
        if key not in self._types_map:
            raise ValueError(f"Unknown issue type: '{type_name}'")
        return copy.deepcopy(self._types_map[key])
