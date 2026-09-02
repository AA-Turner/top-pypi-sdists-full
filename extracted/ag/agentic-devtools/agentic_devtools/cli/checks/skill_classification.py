"""Skill classification CI guard: validates every agdt.* file against a fixture.

Discovers all ``agdt.*.agent.md`` and ``agdt.*.prompt.md`` files on disk, parses
their YAML frontmatter through ``parse_classification``, normalizes the result
to a fixture-format dict, and compares against the checked-in fixture JSON.

Detects:
- Unregistered files (on disk but absent from fixture).
- Bucket mismatches (normalized classification ≠ fixture value).
- Orphan fixture entries (in fixture but absent from disk).
- Parse warnings emitted by ``parse_classification`` (treated as errors).
- Parse errors (unparseable YAML frontmatter).
"""

from __future__ import annotations

import json
import warnings
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

from agentic_devtools.skill_classification import Classification, parse_classification

# ---------------------------------------------------------------------------
# Result dataclasses
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class MismatchEntry:
    """A file whose normalized classification diverges from the fixture."""

    file: str
    expected: dict[str, Any]
    actual: dict[str, Any]


@dataclass(frozen=True)
class ParseWarningEntry:
    """A warning emitted by ``parse_classification`` for a file."""

    file: str
    message: str


@dataclass(frozen=True)
class ParseErrorEntry:
    """A file whose YAML frontmatter could not be parsed."""

    file: str
    error: str


@dataclass
class SkillClassificationResult:
    """Structured result of skill classification validation."""

    validated_count: int = 0
    unregistered_files: list[str] = field(default_factory=list)
    mismatches: list[MismatchEntry] = field(default_factory=list)
    orphan_entries: list[str] = field(default_factory=list)
    parse_warnings: list[ParseWarningEntry] = field(default_factory=list)
    parse_errors: list[ParseErrorEntry] = field(default_factory=list)

    @property
    def is_valid(self) -> bool:
        """Return ``True`` when no violations were found."""
        return (
            not self.unregistered_files
            and not self.mismatches
            and not self.orphan_entries
            and not self.parse_warnings
            and not self.parse_errors
        )


# ---------------------------------------------------------------------------
# Discovery
# ---------------------------------------------------------------------------

_SEARCH_DIRS: list[str] = [".github/agents", ".github/prompts"]
_AGENT_GLOB = "agdt.*.agent.md"
_PROMPT_GLOB = "agdt.*.prompt.md"


def discover_skill_files(repo_root: Path) -> set[str]:
    """Discover all ``agdt.*`` skill files under search directories.

    Returns repo-root-relative paths with forward-slash separators.
    """
    found: set[str] = set()
    for search_dir_name in _SEARCH_DIRS:
        search_dir = repo_root / search_dir_name
        if not search_dir.is_dir():
            continue
        for pattern in (_AGENT_GLOB, _PROMPT_GLOB):
            for filepath in search_dir.glob(pattern):
                rel = filepath.relative_to(repo_root)
                found.add(rel.as_posix())
    return found


# ---------------------------------------------------------------------------
# Frontmatter loading
# ---------------------------------------------------------------------------


def _load_frontmatter(filepath: Path) -> dict[str, Any]:
    """Load YAML frontmatter from a markdown file.

    Uses a line-based scan so CRLF checkouts and files with a missing closing
    delimiter are handled gracefully.

    Raises ``yaml.YAMLError`` when the YAML block is syntactically invalid.
    Raises ``UnicodeDecodeError`` when the file is not valid UTF-8.
    """
    content = filepath.read_text(encoding="utf-8")
    if not content.startswith("---"):
        return {}
    lines = content.splitlines()
    close_idx = next(
        (i for i, line in enumerate(lines) if i > 0 and line == "---"),
        None,
    )
    if close_idx is None:
        return {}
    fm_raw = "\n".join(lines[1:close_idx]).strip()
    if not fm_raw:
        return {}
    result = yaml.safe_load(fm_raw)
    return result if isinstance(result, dict) else {}


# ---------------------------------------------------------------------------
# Normalization
# ---------------------------------------------------------------------------


def _normalize_classification(cls: Classification) -> dict[str, Any]:
    """Convert a ``Classification`` to its fixture-format dict.

    - ``always=True`` → ``{"always": true}`` (regardless of requires).
    - Has non-None requires axes → ``{"requires": {...}}`` (only non-None axes).
    - Default → ``{}``.
    """
    if cls.always:
        return {"always": True}

    requires: dict[str, str] = {}
    if cls.requires_issue_adapter is not None:
        requires["issue_adapter"] = cls.requires_issue_adapter
    if cls.requires_code_hosting is not None:
        requires["code_hosting"] = cls.requires_code_hosting

    if requires:
        return {"requires": requires}

    return {}


# ---------------------------------------------------------------------------
# Warning-capturing parser
# ---------------------------------------------------------------------------


def _parse_with_warning_capture(
    frontmatter: dict[str, Any],
) -> tuple[Classification, list[str]]:
    """Parse classification from frontmatter while capturing all warnings.

    Uses ``simplefilter("always")`` to ensure repeated warnings from the same
    location are also captured.
    """
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        cls = parse_classification(frontmatter)
    return cls, [str(w.message) for w in caught]


# ---------------------------------------------------------------------------
# Fixture loading
# ---------------------------------------------------------------------------


def _load_fixture(fixture_path: Path) -> dict[str, Any]:
    """Load the classification fixture JSON file.

    Raises ``FileNotFoundError`` when the fixture is missing and
    ``json.JSONDecodeError`` (or ``ValueError``) when the fixture is
    malformed.
    """
    text = fixture_path.read_text(encoding="utf-8")
    data = json.loads(text)
    if not isinstance(data, dict):
        msg = f"Fixture must be a JSON object, got {type(data).__name__}"
        raise ValueError(msg)
    return data


# ---------------------------------------------------------------------------
# Main validation
# ---------------------------------------------------------------------------


def validate_skill_classification(
    repo_root: Path | str,
    fixture_path: Path | str,
) -> SkillClassificationResult:
    """Validate every on-disk skill file against the classification fixture.

    Returns a structured :class:`SkillClassificationResult`.
    """
    repo_root = Path(repo_root)
    fixture_path = Path(fixture_path)

    result = SkillClassificationResult()

    on_disk = discover_skill_files(repo_root)
    fixture = _load_fixture(fixture_path)
    fixture_keys = set(fixture.keys())

    # Unregistered files (on disk but not in fixture).
    result.unregistered_files = sorted(on_disk - fixture_keys)

    # Orphan entries (in fixture but not on disk).
    result.orphan_entries = sorted(fixture_keys - on_disk)

    # Validate each file that exists both on disk and in the fixture.
    common = sorted(on_disk & fixture_keys)
    for rel_path in common:
        abs_path = repo_root / rel_path

        # Parse frontmatter.
        try:
            frontmatter = _load_frontmatter(abs_path)
        except (yaml.YAMLError, OSError, UnicodeDecodeError) as exc:
            result.parse_errors.append(ParseErrorEntry(file=rel_path, error=str(exc)))
            continue

        # Parse classification with warning capture.
        cls, caught_warnings = _parse_with_warning_capture(frontmatter)

        # Record any parse warnings as errors.
        for msg in caught_warnings:
            result.parse_warnings.append(ParseWarningEntry(file=rel_path, message=msg))

        # Normalize and compare.
        normalized = _normalize_classification(cls)
        expected = fixture[rel_path]
        if normalized != expected:
            result.mismatches.append(MismatchEntry(file=rel_path, expected=expected, actual=normalized))

    result.validated_count = len(common)
    return result
