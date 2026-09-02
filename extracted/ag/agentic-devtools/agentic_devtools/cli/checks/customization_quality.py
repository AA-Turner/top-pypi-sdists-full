"""Mechanical quality gate for the canonical agent-customization corpus.

Implements the Gate-venue rules of ``docs/agent-customization/authoring-standard.md``
— the rules that can be decided by a machine. The Review-venue rules (Q4, Q6, Q7,
Q12, Q14, Q15) are deliberately not implemented here.

Selection predicate
-------------------
This module reads *exactly* the canonical tree:

* ``.agents/skills/**/*.md``
* ``.github/instructions/**/*.md``
* ``docs/agent-customization/**/*.md``

and nothing else. ``.github/agents/**``, ``.github/prompts/**`` and
``.github/copilot-instructions.md`` are excluded by name, because that legacy
corpus cannot satisfy the boolean rules (every legacy slug contains dots, so no
threshold can admit it) and it is scheduled for deletion rather than migration.
Gating a file that is scheduled for deletion buys nothing and blocks everything.

Corpus-scoped rules
-------------------
Q3 (description similarity) and the duplication rule are relations *between*
files, so they read the whole corpus on every run and report only against the
changed set. Otherwise a changed file could silently collide with an unchanged
one.

This module is intentionally not wired into the checks runner; wiring is a
separate change.
"""

from __future__ import annotations

import re
from collections.abc import Iterable
from dataclasses import dataclass, field
from itertools import combinations
from pathlib import Path
from typing import Any

import yaml

# ---------------------------------------------------------------------------
# Selection predicate
# ---------------------------------------------------------------------------

SELECTED_ROOTS: tuple[str, ...] = (
    ".agents/skills",
    ".github/instructions",
    "docs/agent-customization",
)
"""Repository roots whose Markdown files this check reads."""

EXCLUDED_PATHS: tuple[str, ...] = (
    ".github/agents",
    ".github/prompts",
    ".github/copilot-instructions.md",
)
"""Legacy paths excluded by name; retired by a later wave rather than migrated."""

# ---------------------------------------------------------------------------
# Ratchet-seed constants (the numeric rules)
# ---------------------------------------------------------------------------

MAX_DESCRIPTION_JACCARD: float = 0.5
"""Q3 — pairwise Jaccard over description content words must stay strictly below this."""

ALWAYS_LOADED_MAX_BYTES: int = 32 * 1024
"""Q5 — byte cap for an always-loaded file."""

AGENT_BODY_MAX_CHARS: int = 30_000
"""Q5 — character cap for a custom-agent body."""

SKILL_BODY_MAX_WORDS: int = 5_000
"""Q5 — word cap for a skill body."""

MAX_EMPHATIC_PER_FILE: int = 1
"""Q9 — emphatic directives permitted per file."""

MAX_PROHIBITION_BULLETS: int = 2
"""Q10 — prohibition bullets permitted per file."""

MIN_DUPLICATE_BLOCK_CHARS: int = 40
"""DUP — shortest normalised block considered for cross-file duplication."""

# ---------------------------------------------------------------------------
# Boolean-rule constants (no threshold, so nothing to seed or ratchet)
# ---------------------------------------------------------------------------

DESCRIPTION_MAX_CHARS: int = 1024
"""Q1 — longest permitted ``description``."""

DESCRIPTION_MIN_EXTRA_WORDS: int = 3
"""Q1 — content words a description must add beyond the filename tokens."""

INVOCATION_CLAUSES: tuple[str, ...] = ("use when", "for when", "whenever")
"""Q1 — a description must carry one of these."""

NAME_PATTERN = re.compile(r"^[a-z0-9](-?[a-z0-9])*$")
"""Q2 — legal, portable slug."""

NAME_MAX_CHARS: int = 64
"""Q2 — longest permitted ``name``."""

RATIONALE_MARKERS: tuple[str, ...] = ("because", "so that", "otherwise", "rationale:")
"""Q8 — a prohibition block must carry one of these."""

_PROHIBITION_TOKENS: tuple[str, ...] = ("MUST", "NEVER", "DO NOT")
"""Q8 — tokens that make a block a prohibition block."""

_PROHIBITION_PATTERN = re.compile(r"\b(?:MUST|NEVER)\b|\bDO NOT\b")
"""Q8 — whole-token prohibition markers, avoiding substring false positives."""

_EMPHATIC_PATTERN = re.compile(r"\b(?:CRITICAL|MUST|NEVER|ALWAYS)\b|\u26a0")
"""Q9 — emphatic directive tokens, including the warning emoji."""

_BULLET_PATTERN = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s+")
"""Q10 — a Markdown bullet or numbered item (both ``.`` and ``)`` delimiters accepted)."""

_BULLET_PROHIBITION_PATTERN = re.compile(r"\bmust not\b|\bnever\b|\bdo not\b|\bdon't\b|\bprohibited\b", re.IGNORECASE)
"""Q10 — what makes a bullet a prohibition bullet."""

FORMAT_PRESCRIPTION_PHRASES: tuple[str, ...] = (
    "output format",
    "response format",
    "the following format",
    "in this format",
    "format your",
    "respond with",
    "reply with",
    "emit the following",
    "output the following",
)
"""Q11 — phrases that mean a file prescribes an output format."""

FRAGMENT_MARKERS: tuple[str, str] = ("<!-- agdt:fragment:start -->", "<!-- agdt:fragment:end -->")
"""DUP — blocks between these markers are exempt from the duplication rule."""

_MARKDOWN_LINK_PATTERN = re.compile(r"\[[^\]]*\]\(([^()]*(?:\([^()]*\)[^()]*)*)\)")
_REFERENCE_LINK_PATTERN = re.compile(r"\[([^\]]+)\]\[([^\]]*)\]")
_SHORTCUT_REFERENCE_PATTERN = re.compile(r"(?<![!\]])\[([^\]]+)\](?!\[)(?!\()(?!:)")
_SHORTCUT_IMAGE_PATTERN = re.compile(r"!\[([^\]]+)\](?!\[)(?!\()")
_REFERENCE_DEFINITION_PATTERN = re.compile(
    r"^[ \t]{0,3}\[([^\]]+)\]:[ \t]*(?:\r?\n[ \t]{0,3})?(.+)$",
    re.MULTILINE,
)
_PATH_CANDIDATE_PATTERN = re.compile(r"^[A-Za-z0-9_.\-]+(?:/[A-Za-z0-9_.\-]+)+/?$")
_URI_SCHEME_PATTERN = re.compile(r"^[A-Za-z][A-Za-z0-9+.\-]*:")
_FENCE_OPEN_PATTERN = re.compile(r"^[ \t]{0,3}(?P<fence>`{3,}|~{3,}).*$")
_ATX_HEADING_BOUNDARY_PATTERN = re.compile(r"^[ \t]{0,3}#{1,6}(?:[ \t]+|$)")
_BLOCK_QUOTE_BOUNDARY_PATTERN = re.compile(r"^[ \t]{0,3}>")
_UNORDERED_LIST_BOUNDARY_PATTERN = re.compile(r"^[ \t]{0,3}[-+*][ \t]+")
_ORDERED_LIST_BOUNDARY_PATTERN = re.compile(r"^[ \t]{0,3}1[.)][ \t]+")
_ORDERED_LIST_ITEM_PATTERN = re.compile(r"^[ \t]{0,3}\d+[.)][ \t]+")
_SETEXT_HEADING_BOUNDARY_PATTERN = re.compile(r"^[ \t]{0,3}(?:=+|-+)[ \t]*$")
_THEMATIC_BREAK_BOUNDARY_PATTERN = re.compile(r"^[ \t]{0,3}(?:(?:\*[ \t]*){3,}|(?:-[ \t]*){3,}|(?:_[ \t]*){3,})$")

_WORD_PATTERN = re.compile(r"[a-z0-9]+")
_STOPWORDS: frozenset[str] = frozenset(
    {
        "and",
        "are",
        "for",
        "from",
        "into",
        "its",
        "not",
        "that",
        "the",
        "this",
        "use",
        "when",
        "with",
        "you",
        "your",
    }
)

# Rule identifiers, used as the ``rule`` field of every violation.
RULE_DESCRIPTION = "Q1"
RULE_NAME = "Q2"
RULE_SIMILARITY = "Q3"
RULE_SIZE = "Q5"
RULE_RATIONALE = "Q8"
RULE_EMPHASIS = "Q9"
RULE_PROHIBITIONS = "Q10"
RULE_FORMAT_EXAMPLE = "Q11"
RULE_PATHS = "Q13"
RULE_DUPLICATION = "DUP"


# ---------------------------------------------------------------------------
# Result types
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Violation:
    """A single rule failure.

    Attributes:
        rule: Rule identifier, e.g. ``"Q9"`` or ``"DUP"``.
        path: Repository-relative POSIX path of the offending file.
        message: Human-readable explanation.
    """

    rule: str
    path: str
    message: str


@dataclass(frozen=True)
class CustomizationUnit:
    """One selected Markdown file, parsed into the parts the rules need.

    Attributes:
        path: Repository-relative POSIX path.
        listing: The selected root the unit belongs to (Q3 groups by listing).
        kind: One of ``"skill"``, ``"agent"``, ``"always_loaded"``,
            ``"scoped"`` or ``"document"``.
        frontmatter: Parsed YAML frontmatter (empty when absent or unusable).
        body: File content with the frontmatter block removed.
        size_bytes: Size of the whole file in UTF-8 bytes.
        source: Complete raw file content (frontmatter + body), used by Q9 so
            emphatic directives in frontmatter are not invisible to the rule.
    """

    path: str
    listing: str
    kind: str
    frontmatter: dict[str, Any]
    body: str
    size_bytes: int
    source: str


@dataclass
class CustomizationQualityResult:
    """Structured outcome of :func:`check_customization_quality`.

    Attributes:
        checked_files: Files the violations were reported against.
        corpus_files: Every selected file, including unchanged ones read only
            to evaluate the corpus-scoped rules.
        violations: Every violation found, sorted by path then rule.
    """

    checked_files: list[str] = field(default_factory=list)
    corpus_files: list[str] = field(default_factory=list)
    violations: list[Violation] = field(default_factory=list)

    @property
    def is_valid(self) -> bool:
        """Return ``True`` when no violation was found."""
        return not self.violations


# ---------------------------------------------------------------------------
# Selection and loading
# ---------------------------------------------------------------------------


def normalize_path(path: str) -> str:
    """Return *path* as a repository-relative POSIX path without a ``./`` prefix."""
    normalized = path.replace("\\", "/")
    while normalized.startswith("./"):
        normalized = normalized[2:]
    return normalized


def is_selected(path: str) -> bool:
    """Return ``True`` when *path* is inside the canonical selection.

    Only Markdown files under :data:`SELECTED_ROOTS` are selected, and anything
    under :data:`EXCLUDED_PATHS` is rejected first so the legacy corpus can
    never be read even if a root were widened by accident. Paths containing
    ``..`` segments are rejected before the prefix check so traversal strings
    such as ``.agents/skills/../../README.md`` cannot be admitted.
    """
    normalized = normalize_path(path)
    if not normalized.endswith(".md"):
        return False
    if any(seg == ".." for seg in normalized.split("/")):
        return False
    for excluded in EXCLUDED_PATHS:
        if normalized == excluded or normalized.startswith(f"{excluded}/"):
            return False
    return any(normalized.startswith(f"{root}/") for root in SELECTED_ROOTS)


def discover_customization_files(repo_root: Path | str) -> list[str]:
    """Return every selected Markdown file under *repo_root*, sorted.

    :data:`SELECTED_ROOTS` and :data:`EXCLUDED_PATHS` are disjoint, so walking
    the roots cannot reach an excluded path; :func:`is_selected` is what filters
    a caller-supplied changed set.
    """
    root = Path(repo_root)
    found: list[str] = []
    for selected_root in SELECTED_ROOTS:
        base = root / selected_root
        if not base.is_dir():
            continue
        for candidate in base.rglob("*.md"):
            if not candidate.is_file():
                continue
            found.append(candidate.relative_to(root).as_posix())
    return sorted(found)


def _split_frontmatter(content: str) -> tuple[dict[str, Any], str]:
    """Split YAML frontmatter from the body.

    Returns an empty mapping when the file has no frontmatter, when the block
    is unterminated, or when the block is not a YAML mapping. Malformed YAML is
    treated as absent frontmatter so the remaining rules still run.

    Line endings in the body are preserved exactly as they appear in *content*
    (CRLF files stay CRLF; LF files stay LF).
    """
    lines = content.splitlines(keepends=True)
    if not lines or lines[0].rstrip("\r\n") != "---":
        return {}, content
    close_idx = next(
        (i for i, line in enumerate(lines) if i > 0 and line.rstrip("\r\n") == "---"),
        None,
    )
    if close_idx is None:
        return {}, content
    body_start = sum(len(lines[i]) for i in range(close_idx + 1))
    body = content[body_start:]
    raw = "".join(lines[1:close_idx]).strip()
    if not raw:
        return {}, body
    try:
        parsed = yaml.safe_load(raw)
    except yaml.YAMLError:
        return {}, body
    if not isinstance(parsed, dict):
        return {}, body
    return parsed, body


def _classify_kind(path: str, frontmatter: dict[str, Any]) -> str:
    """Return the Q5 size-budget kind of the unit at *path*."""
    if path.endswith(".agent.md"):
        return "agent"
    if path.startswith(".agents/skills/") and path.endswith("/SKILL.md"):
        return "skill"
    if path.endswith(".instructions.md"):
        apply_to = frontmatter.get("applyTo")
        if apply_to in (None, "**", "**/*"):
            return "always_loaded"
        return "scoped"
    return "document"


def _listing_of(path: str) -> str:
    """Return the selected root *path* belongs to."""
    return next(root for root in SELECTED_ROOTS if path.startswith(f"{root}/"))


def load_unit(repo_root: Path | str, path: str) -> CustomizationUnit:
    """Read and parse a single selected file into a :class:`CustomizationUnit`.

    Args:
        repo_root: Repository root the path is relative to.
        path: Repository-relative path of a selected file.

    Raises:
        ValueError: When *path* is outside the canonical selection, or when the
            file resolves (via symlink or traversal) outside the repository root
            or outside the canonical selection.
        OSError: When the file cannot be read.
    """
    normalized = normalize_path(path)
    if not is_selected(normalized):
        raise ValueError(f"{normalized} is outside the agent-customization selection")
    root = Path(repo_root)
    target = root / normalized
    try:
        resolved = target.resolve()
        root_resolved = root.resolve()
        resolved_relative = resolved.relative_to(root_resolved).as_posix()
    except ValueError:
        raise ValueError(f"{normalized} resolves outside the repository root")
    if not is_selected(resolved_relative):
        raise ValueError(f"{normalized} resolves outside the agent-customization selection")
    raw = resolved.read_bytes()
    content = raw.decode("utf-8")
    frontmatter, body = _split_frontmatter(content)
    return CustomizationUnit(
        path=normalized,
        listing=_listing_of(normalized),
        kind=_classify_kind(normalized, frontmatter),
        frontmatter=frontmatter,
        body=body,
        size_bytes=len(raw),
        source=content,
    )


# ---------------------------------------------------------------------------
# Shared text helpers
# ---------------------------------------------------------------------------


def content_words(text: str) -> set[str]:
    """Return the lowercase content words of *text* (stopwords removed)."""
    return {word for word in _WORD_PATTERN.findall(text.lower()) if len(word) > 2 and word not in _STOPWORDS}


def _blocks(body: str) -> list[str]:
    """Split *body* into blank-line-separated blocks, dropping empty ones."""
    return [block for block in re.split(r"\n\s*\n", body) if block.strip()]


def _requires_metadata(unit: CustomizationUnit) -> bool:
    """Return ``True`` for kinds whose ``name``/``description`` are mandatory."""
    return unit.kind in ("skill", "agent")


def _description_of(unit: CustomizationUnit) -> str | None:
    """Return the unit's ``description`` when it is a string, else ``None``."""
    description = unit.frontmatter.get("description")
    return description if isinstance(description, str) else None


# ---------------------------------------------------------------------------
# Per-file rules
# ---------------------------------------------------------------------------


def check_description(unit: CustomizationUnit) -> list[Violation]:
    """Q1 — the ``description`` must say what the unit does and when to use it.

    Applies to skills and custom agents, whose frontmatter is mandatory. Other
    kinds are checked only when they declare a ``description``.
    """
    raw = unit.frontmatter.get("description")
    if raw is None:
        if not _requires_metadata(unit):
            return []
        return [Violation(RULE_DESCRIPTION, unit.path, "description is missing")]
    if not isinstance(raw, str):
        return [
            Violation(
                RULE_DESCRIPTION,
                unit.path,
                f"description has unexpected type {type(raw).__name__!r}; expected a string",
            )
        ]
    description = raw

    violations: list[Violation] = []
    stripped = description.strip()
    if not stripped:
        violations.append(Violation(RULE_DESCRIPTION, unit.path, "description is empty"))
        return violations
    if len(description) > DESCRIPTION_MAX_CHARS:
        violations.append(
            Violation(
                RULE_DESCRIPTION,
                unit.path,
                f"description is {len(description)} chars, over the {DESCRIPTION_MAX_CHARS}-char cap",
            )
        )
    lowered = stripped.lower()
    if not any(clause in lowered for clause in INVOCATION_CLAUSES):
        violations.append(
            Violation(
                RULE_DESCRIPTION,
                unit.path,
                f"description carries no invocation clause ({', '.join(INVOCATION_CLAUSES)})",
            )
        )
    filename_words = content_words(unit.path)
    extra = content_words(stripped) - filename_words
    if len(extra) <= DESCRIPTION_MIN_EXTRA_WORDS:
        violations.append(
            Violation(
                RULE_DESCRIPTION,
                unit.path,
                f"description adds only {len(extra)} content words beyond the filename; "
                f"more than {DESCRIPTION_MIN_EXTRA_WORDS} are required",
            )
        )
    return violations


def check_name(unit: CustomizationUnit) -> list[Violation]:
    """Q2 — ``name`` is a legal slug, at most 64 chars, equal to its directory.

    Applies to skills and custom agents. Other kinds are checked only when they
    declare a ``name``.
    """
    name = unit.frontmatter.get("name")
    if name is None:
        if not _requires_metadata(unit):
            return []
        return [Violation(RULE_NAME, unit.path, "name is missing")]
    if not isinstance(name, str):
        return [
            Violation(
                RULE_NAME,
                unit.path,
                f"name has unexpected type {type(name).__name__!r}; expected a string",
            )
        ]

    violations: list[Violation] = []
    if not NAME_PATTERN.match(name):
        violations.append(
            Violation(RULE_NAME, unit.path, f"name {name!r} is not a legal slug (^[a-z0-9](-?[a-z0-9])*$)")
        )
    if len(name) > NAME_MAX_CHARS:
        violations.append(
            Violation(RULE_NAME, unit.path, f"name is {len(name)} chars, over the {NAME_MAX_CHARS}-char cap")
        )
    parent = _parent_dir_name(unit.path)
    if name != parent:
        violations.append(Violation(RULE_NAME, unit.path, f"name {name!r} does not equal parent directory {parent!r}"))
    return violations


def _parent_dir_name(path: str) -> str:
    """Return the name of the directory containing *path*."""
    return Path(path).parent.name


def check_size(unit: CustomizationUnit) -> list[Violation]:
    """Q5 — per-kind size caps.

    Always-loaded files are capped in bytes, custom-agent bodies in characters
    and skill bodies in words. Scoped instruction files and plain documents
    carry no published cap, so they are not checked.
    """
    if unit.kind == "always_loaded" and unit.size_bytes > ALWAYS_LOADED_MAX_BYTES:
        return [
            Violation(
                RULE_SIZE,
                unit.path,
                f"always-loaded file is {unit.size_bytes} bytes, over the {ALWAYS_LOADED_MAX_BYTES}-byte cap",
            )
        ]
    if unit.kind == "agent" and len(unit.body) > AGENT_BODY_MAX_CHARS:
        return [
            Violation(
                RULE_SIZE,
                unit.path,
                f"agent body is {len(unit.body)} chars, over the {AGENT_BODY_MAX_CHARS}-char cap",
            )
        ]
    if unit.kind == "skill":
        words = len(unit.body.split())
        if words > SKILL_BODY_MAX_WORDS:
            return [
                Violation(
                    RULE_SIZE,
                    unit.path,
                    f"skill body is {words} words, over the {SKILL_BODY_MAX_WORDS}-word cap",
                )
            ]
    return []


def check_rationale(unit: CustomizationUnit) -> list[Violation]:
    """Q8 — every block carrying MUST, NEVER or DO NOT states its reason.

    The full file source (frontmatter + body) is scanned so that prohibition
    tokens in frontmatter values (e.g. ``description: Users MUST …``) are also
    checked.  Frontmatter blocks and body blocks are processed independently so
    that a rationale in the opening body paragraph cannot satisfy a prohibition
    in the frontmatter (or vice versa).
    """
    frontmatter_text = unit.source[: len(unit.source) - len(unit.body)]
    violations: list[Violation] = []
    for block in _blocks(frontmatter_text) + _blocks(unit.body):
        if not _PROHIBITION_PATTERN.search(block):
            continue
        lowered = block.lower()
        if any(marker in lowered for marker in RATIONALE_MARKERS):
            continue
        violations.append(
            Violation(
                RULE_RATIONALE,
                unit.path,
                f"prohibition block states no reason ({', '.join(RATIONALE_MARKERS)}): {_excerpt(block)}",
            )
        )
    return violations


def check_prohibitions(unit: CustomizationUnit) -> list[Violation]:
    """Q10 — at most two prohibition bullets per file."""
    visible = _strip_fenced_code(unit.body)
    bullets = [item for item in _iter_markdown_list_items(visible) if _BULLET_PROHIBITION_PATTERN.search(item)]
    if len(bullets) <= MAX_PROHIBITION_BULLETS:
        return []
    return [
        Violation(
            RULE_PROHIBITIONS,
            unit.path,
            f"{len(bullets)} prohibition bullets, over the cap of {MAX_PROHIBITION_BULLETS}",
        )
    ]


def _iter_markdown_list_items(body: str) -> list[str]:
    """Return Markdown list items with continuation lines folded into each item."""
    lines = body.splitlines()
    items: list[str] = []
    idx = 0
    while idx < len(lines):
        match = _BULLET_PATTERN.match(lines[idx])
        if match is None:
            idx += 1
            continue

        indent = len(lines[idx]) - len(lines[idx].lstrip())
        parts = [lines[idx][match.end() :].strip()]
        idx += 1
        while idx < len(lines):
            line = lines[idx]
            next_match = _BULLET_PATTERN.match(line)
            next_indent = len(line) - len(line.lstrip())
            if next_match is not None:
                break
            if line.strip() and next_indent <= indent:
                break
            stripped = line.strip()
            if stripped:
                parts.append(stripped)
            idx += 1

        items.append(" ".join(parts))
    return items


def _is_fence_close(line: str, fence: str, fence_len: int) -> bool:
    """Return ``True`` when *line* closes the active fenced code block."""
    return re.fullmatch(rf"[ \t]{{0,3}}{re.escape(fence)}{{{fence_len},}}[ \t]*", line) is not None


def _has_fenced_block(body: str) -> bool:
    """Return ``True`` when *body* contains at least one non-empty fenced code block.

    A matched pair (opening fence, at least one content line, closing fence
    of the same character) is required; a file ending with an unmatched
    opening fence returns ``False``.
    """
    inside = False
    fence: str = ""
    fence_len = 0
    has_content = False
    for raw_line in body.splitlines():
        if not inside:
            match = _FENCE_OPEN_PATTERN.fullmatch(raw_line)
            if match is not None:
                inside = True
                fence = match.group("fence")[0]
                fence_len = len(match.group("fence"))
                has_content = False
        else:
            if _is_fence_close(raw_line, fence, fence_len):
                if has_content:
                    return True
                inside = False
            elif raw_line.strip():
                has_content = True
    return False


def check_format_example(unit: CustomizationUnit) -> list[Violation]:
    """Q11 — a file prescribing an output format shows one concrete instance."""
    lowered = unit.body.lower()
    if not any(phrase in lowered for phrase in FORMAT_PRESCRIPTION_PHRASES):
        return []
    if _has_fenced_block(unit.body):
        return []
    return [
        Violation(
            RULE_FORMAT_EXAMPLE,
            unit.path,
            "file prescribes an output format but shows no fenced example",
        )
    ]


def check_path_references(unit: CustomizationUnit, repo_root: Path | str) -> list[Violation]:
    """Q13 — documented paths resolve, and resources sit one level deep.

    Relative Markdown link targets are resolved against the entry file and
    normally must also sit at most one directory level from it. Links that
    resolve into the repository's top-level ``docs/`` tree are treated as
    repository documentation cross-references and are checked for existence
    only, like repository-absolute links (leading ``/``), since they name a
    repository location rather than a bundled resource. Repository paths
    written in inline code are checked for existence only; a candidate is
    treated as a repository path only when its first segment exists at the
    repository root, so prose such as ``type/ISSUE-KEY/description`` is not
    mistaken for one.
    """
    root = Path(repo_root)
    root_resolved = root.resolve()
    entry_dir = Path(unit.path).parent
    violations: list[Violation] = []
    visible_body = _strip_fenced_code(unit.body)
    link_scan_body = _strip_inline_code(visible_body)

    for target in _iter_markdown_targets(link_scan_body):
        link = _link_target(target)
        if not link or link.startswith("#") or _URI_SCHEME_PATTERN.match(link):
            continue
        resolved = _resolve_link(entry_dir, link)
        if not _exists_within_repo(root, root_resolved, resolved):
            violations.append(Violation(RULE_PATHS, unit.path, f"linked path does not resolve: {link}"))
            continue
        if not link.startswith("/") and not _is_repo_docs_cross_reference(resolved) and _link_depth(link) > 1:
            violations.append(
                Violation(RULE_PATHS, unit.path, f"linked resource is more than one level from its entry file: {link}")
            )

    for _, _, span in _iter_inline_code_spans(visible_body):
        candidate = span.strip()
        if not _PATH_CANDIDATE_PATTERN.match(candidate):
            continue
        first_segment = candidate.split("/")[0]
        first_path = root / first_segment
        if first_segment not in (".", "..") and not (first_path.exists() or first_path.is_symlink()):
            continue
        if not _exists_within_repo(root, root_resolved, candidate.rstrip("/")):
            violations.append(Violation(RULE_PATHS, unit.path, f"documented path does not exist: {candidate}"))
    return violations


def _iter_markdown_targets(body: str) -> list[str]:
    """Return inline and reference-style Markdown destinations from *body*.

    Covers four link/image forms:
    * Inline links and images: ``[text](target)`` and ``![alt](src)``
    * Full/collapsed reference links and images: ``[text][label]``, ``[text][]``, ``![alt][label]``
    * Shortcut reference links: ``[guide]`` (resolved as ``[guide][guide]``)
    * Shortcut reference images: ``![diagram]`` (resolved as ``![diagram][diagram]``)
    """
    targets = list(_MARKDOWN_LINK_PATTERN.findall(body))
    definitions = {
        _normalize_reference_label(label): target for label, target in _REFERENCE_DEFINITION_PATTERN.findall(body)
    }
    for text, label in _REFERENCE_LINK_PATTERN.findall(body):
        key = _normalize_reference_label(label or text)
        target = definitions.get(key)
        if target is not None:
            targets.append(target)
    for text in _SHORTCUT_REFERENCE_PATTERN.findall(body):
        key = _normalize_reference_label(text)
        target = definitions.get(key)
        if target is not None:
            targets.append(target)
    for text in _SHORTCUT_IMAGE_PATTERN.findall(body):
        key = _normalize_reference_label(text)
        target = definitions.get(key)
        if target is not None:
            targets.append(target)
    return targets


def _strip_fenced_code(body: str) -> str:
    """Return *body* with fenced code blocks removed."""
    kept: list[str] = []
    inside = False
    fence: str = ""
    fence_len = 0
    for raw_line in body.splitlines(keepends=True):
        line = raw_line.rstrip("\r\n")
        if not inside:
            match = _FENCE_OPEN_PATTERN.fullmatch(line)
            if match is not None:
                inside = True
                fence = match.group("fence")[0]
                fence_len = len(match.group("fence"))
                kept.append(_line_break_only(raw_line))
                continue
            kept.append(raw_line)
            continue
        kept.append(_line_break_only(raw_line))
        if _is_fence_close(line, fence, fence_len):
            inside = False
    return "".join(kept)


def _strip_inline_code(body: str) -> str:
    """Return *body* with inline code spans replaced by spaces.

    Inline code contents must not be parsed for Markdown link syntax because
    they are literal text. The replacement preserves offsets and line
    structure so that reference-definition lines immediately before or after a
    span are still found at their original positions.
    """
    parts: list[str] = []
    last = 0
    for start, end, _ in _iter_inline_code_spans(body):
        parts.append(body[last:start])
        span = body[start:end]
        parts.append("".join(char if char in "\r\n`" else " " for char in span))
        last = end
    parts.append(body[last:])
    return "".join(parts)


def _line_break_only(line: str) -> str:
    """Return only the line break from *line* (if present)."""
    if line.endswith("\r\n"):
        return "\r\n"
    if line.endswith("\n"):
        return "\n"
    return ""


def _iter_inline_code_spans(body: str) -> list[tuple[int, int, str]]:
    """Return Markdown inline-code spans as ``(start, end, content)`` tuples.

    Matching is done per non-blank block so a code span may cross a line break
    inside one paragraph, but an unmatched backtick run cannot consume later
    paragraphs. Opening and closing delimiters must use the same backtick-run
    length.
    """
    spans: list[tuple[int, int, str]] = []
    for block_start, block_end in _nonblank_block_ranges(body):
        cursor = block_start
        while cursor < block_end:
            if body[cursor] != "`" or _is_escaped_backtick_run(body, cursor):
                cursor += 1
                continue
            open_start = cursor
            while cursor < block_end and body[cursor] == "`":
                cursor += 1
            delimiter_len = cursor - open_start
            close = _find_inline_code_close(body, cursor, block_end, delimiter_len)
            if close is None:
                continue
            spans.append((open_start, close + delimiter_len, body[cursor:close]))
            cursor = close + delimiter_len
    return spans


def _nonblank_block_ranges(body: str) -> list[tuple[int, int]]:
    """Return ``[start, end)`` ranges for non-blank line blocks in *body*.

    Consecutive block-quote lines (``> …``) at the same nesting depth are kept
    in the same range so that a multiline code span within one block-quoted
    paragraph is not split across separate ranges. A change in quote depth
    starts a new range so that a code span cannot cross a nesting boundary.
    A quote-only line (``>`` / ``> ``) is treated as blank and ends the current
    paragraph inside the block quote.

    Ordered list items (``2.``, ``3.``, …) that continue a list started by
    any digit are treated as block boundaries so that an unterminated backtick
    in one item cannot pair with a backtick in a later item.
    """
    ranges: list[tuple[int, int]] = []
    block_start: int | None = None
    offset = 0
    prev_quote_depth = 0
    in_ordered_list = False
    for line in body.splitlines(keepends=True):
        # Count block-quote depth and strip all ``>`` markers so that nested
        # quotes (``>>``, ``>>>``) do not leave a residual ``>`` that would look
        # like a new block boundary to ``_starts_markdown_block_boundary``.
        block_line = line
        quote_depth = 0
        while _BLOCK_QUOTE_BOUNDARY_PATTERN.match(block_line):
            block_line = _BLOCK_QUOTE_BOUNDARY_PATTERN.sub("", block_line, count=1)
            quote_depth += 1
        is_block_quote = quote_depth > 0
        if block_line.strip():
            if block_start is None:
                block_start = offset
                if _ORDERED_LIST_ITEM_PATTERN.match(block_line):
                    in_ordered_list = True
            elif (
                _starts_markdown_block_boundary(block_line)
                or (is_block_quote and prev_quote_depth == 0)
                or (is_block_quote and prev_quote_depth > 0 and quote_depth != prev_quote_depth)
                or (in_ordered_list and _ORDERED_LIST_ITEM_PATTERN.match(block_line))
            ):
                ranges.append((block_start, offset))
                block_start = offset
                if _ORDERED_LIST_BOUNDARY_PATTERN.match(block_line):
                    in_ordered_list = True
                elif not _ORDERED_LIST_ITEM_PATTERN.match(block_line):
                    in_ordered_list = False
            prev_quote_depth = quote_depth
        else:
            if block_start is not None:
                ranges.append((block_start, offset))
                block_start = None
            prev_quote_depth = 0
            in_ordered_list = False
        offset += len(line)
        # ATX headings are self-terminating single-line blocks.  Close the
        # range immediately so that an unmatched backtick inside the heading
        # cannot pair with a backtick in the following paragraph.
        if block_start is not None and _ATX_HEADING_BOUNDARY_PATTERN.match(block_line):
            ranges.append((block_start, offset))
            block_start = None
            prev_quote_depth = 0
            in_ordered_list = False
    if block_start is not None:
        ranges.append((block_start, len(body)))
    return ranges


def _starts_markdown_block_boundary(line: str) -> bool:
    """Return whether *line* starts a Markdown block that interrupts a paragraph."""
    return bool(
        _ATX_HEADING_BOUNDARY_PATTERN.match(line)
        or _BLOCK_QUOTE_BOUNDARY_PATTERN.match(line)
        or _UNORDERED_LIST_BOUNDARY_PATTERN.match(line)
        or _ORDERED_LIST_BOUNDARY_PATTERN.match(line)
        or _SETEXT_HEADING_BOUNDARY_PATTERN.match(line)
        or _THEMATIC_BREAK_BOUNDARY_PATTERN.match(line)
    )


def _find_inline_code_close(body: str, start: int, end: int, delimiter_len: int) -> int | None:
    """Return the start offset of the matching inline-code closer, if any.

    Backslash escaping does not apply inside a code span (CommonMark §6.1), so
    the ``_is_escaped_backtick_run`` check is intentionally absent here.  It is
    only used by the opener scanner in ``_iter_inline_code_spans``.
    """
    cursor = start
    while cursor < end:
        if body[cursor] != "`":
            cursor += 1
            continue
        run_start = cursor
        while cursor < end and body[cursor] == "`":
            cursor += 1
        if cursor - run_start == delimiter_len:
            return run_start
    return None


def _is_escaped_backtick_run(body: str, start: int) -> bool:
    """Return whether the backtick at *start* is escaped by an odd backslash run."""
    backslashes = 0
    cursor = start - 1
    while cursor >= 0 and body[cursor] == "\\":
        backslashes += 1
        cursor -= 1
    return backslashes % 2 == 1


def _normalize_reference_label(label: str) -> str:
    """Return a Markdown reference label in its normalized lookup form."""
    return " ".join(label.strip().split()).lower()


def _link_target(target: str) -> str:
    """Return the destination of a Markdown link *target*.

    Handles the pointy-bracket destination form (``[x](<a path>)``), and
    otherwise drops an optional link title and any ``#`` fragment.
    """
    raw = target.strip()
    if raw.startswith("<") and raw.endswith(">"):
        raw = raw[1:-1]
    else:
        raw = raw.split(" ")[0]
    return raw.split("#")[0].strip()


def _resolve_link(entry_dir: Path, link: str) -> str:
    """Resolve a Markdown *link* against *entry_dir*, keeping it repo-relative.

    ``..`` segments are clamped at the repository root in both the absolute-link
    and relative-link paths so a link such as ``/../../etc/passwd`` cannot
    escape the repository.
    """
    if link.startswith("/"):
        return "/".join(_collapse_segments([], link.lstrip("/").split("/")))
    return "/".join(_collapse_segments(list(entry_dir.parts), link.split("/")))


def _is_repo_docs_cross_reference(resolved: str) -> bool:
    """Return ``True`` when *resolved* names the repository's top-level docs tree."""
    return resolved == "docs" or resolved.startswith("docs/")


def _collapse_segments(parts: list[str], segments: list[str]) -> list[str]:
    """Return *parts* after applying ``.``/``..``-aware *segments* to it."""
    collapsed = list(parts)
    for segment in segments:
        if segment in ("", "."):
            continue
        if segment == "..":
            if collapsed:
                collapsed.pop()
            continue
        collapsed.append(segment)
    return collapsed


def _link_depth(link: str) -> int:
    """Return how many directory levels *link* travels from its entry file.

    Upward ``..`` segments that cannot be cancelled against a known directory
    are counted as directory hops; they must not be silently discarded.
    """
    up = 0
    collapsed: list[str] = []
    for segment in link.split("/"):
        if segment in ("", "."):
            continue
        if segment == "..":
            if collapsed:
                collapsed.pop()
            else:
                up += 1
            continue
        collapsed.append(segment)
    return up + max(len(collapsed) - 1, 0)


def _exists_within_repo(root: Path, root_resolved: Path, repo_relative: str) -> bool:
    """Return ``True`` when *repo_relative* exists and resolves inside *root*."""
    candidate = root / repo_relative
    if not candidate.exists():
        return False
    try:
        candidate.resolve().relative_to(root_resolved)
    except ValueError:
        return False
    return True


def _excerpt(text: str, limit: int = 60) -> str:
    """Return a single-line, length-limited excerpt of *text* for messages."""
    flattened = " ".join(text.split())
    return flattened if len(flattened) <= limit else f"{flattened[:limit]}…"


# ---------------------------------------------------------------------------
# Corpus-scoped rules
# ---------------------------------------------------------------------------


def check_emphasis(units: list[CustomizationUnit], reported: set[str]) -> list[Violation]:
    """Q9 — emphasis is rationed.

    Two parts: at most :data:`MAX_EMPHATIC_PER_FILE` emphatic directives in one
    file, and no emphatic line repeated across two or more files. The second
    part is a relation between files, so the whole corpus is read while only
    *reported* files are reported against.
    """
    violations: list[Violation] = []
    lines_by_file: dict[str, list[str]] = {}
    for unit in units:
        emphatic_lines = [line for line in unit.source.splitlines() if _EMPHATIC_PATTERN.search(line)]
        lines_by_file[unit.path] = [" ".join(line.split()).lower() for line in emphatic_lines]
        if unit.path not in reported:
            continue
        count = len(_EMPHATIC_PATTERN.findall(unit.source))
        if count > MAX_EMPHATIC_PER_FILE:
            violations.append(
                Violation(
                    RULE_EMPHASIS,
                    unit.path,
                    f"{count} emphatic directives, over the cap of {MAX_EMPHATIC_PER_FILE}",
                )
            )

    occurrences: dict[str, list[str]] = {}
    for path, normalized_lines in lines_by_file.items():
        for normalized in set(normalized_lines):
            occurrences.setdefault(normalized, []).append(path)
    for normalized, paths in sorted(occurrences.items()):
        if len(paths) < 2:
            continue
        for path in paths:
            if path not in reported:
                continue
            others = ", ".join(other for other in paths if other != path)
            violations.append(
                Violation(
                    RULE_EMPHASIS,
                    path,
                    f"emphatic line also appears in {others}: {_excerpt(normalized)}",
                )
            )
    return violations


def check_description_similarity(units: list[CustomizationUnit], reported: set[str]) -> list[Violation]:
    """Q3 — no two descriptions in one listing are confusably similar.

    Reads every unit in the corpus but reports only pairs that involve a file in
    *reported*, so a changed file cannot silently collide with an unchanged one.
    """
    violations: list[Violation] = []
    by_listing: dict[str, list[tuple[str, set[str]]]] = {}
    for unit in units:
        description = _description_of(unit)
        if description is None:
            continue
        words = content_words(description)
        if not words:
            continue
        by_listing.setdefault(unit.listing, []).append((unit.path, words))

    for entries in by_listing.values():
        ordered = sorted(entries, key=lambda entry: entry[0])
        for (left_path, left_words), (right_path, right_words) in combinations(ordered, 2):
            similarity = _jaccard(left_words, right_words)
            if similarity < MAX_DESCRIPTION_JACCARD:
                continue
            for path, other in ((left_path, right_path), (right_path, left_path)):
                if path in reported:
                    violations.append(
                        Violation(
                            RULE_SIMILARITY,
                            path,
                            f"description overlaps {other} (Jaccard {similarity:.2f}, cap {MAX_DESCRIPTION_JACCARD})",
                        )
                    )
    return violations


def _jaccard(left: set[str], right: set[str]) -> float:
    """Return the Jaccard similarity of two non-empty word sets."""
    return len(left & right) / len(left | right)


def check_duplicate_blocks(units: list[CustomizationUnit], reported: set[str]) -> list[Violation]:
    """DUP — no normalised block of 40+ chars appears in two or more files.

    Blocks between :data:`FRAGMENT_MARKERS` are exempt, because a fragment is
    the sanctioned way to share one body. Like Q3 this reads the whole corpus
    and reports only against *reported*.
    """
    occurrences: dict[str, list[str]] = {}
    for unit in units:
        for block in _fragment_free_blocks(unit.body):
            normalized = " ".join(block.split()).lower()
            if len(normalized) < MIN_DUPLICATE_BLOCK_CHARS:
                continue
            paths = occurrences.setdefault(normalized, [])
            if unit.path not in paths:
                paths.append(unit.path)

    violations: list[Violation] = []
    for normalized, paths in occurrences.items():
        if len(paths) < 2:
            continue
        for path in paths:
            if path not in reported:
                continue
            others = ", ".join(other for other in paths if other != path)
            violations.append(
                Violation(RULE_DUPLICATION, path, f"block also appears in {others}: {_excerpt(normalized)}")
            )
    return violations


def _fragment_free_blocks(body: str) -> list[str]:
    """Return the blocks of *body* that sit outside any fragment marker."""
    start_marker, end_marker = FRAGMENT_MARKERS
    kept: list[str] = []
    buffered: list[str] = []
    inside = False
    for line in body.splitlines():
        stripped = line.strip()
        if stripped == start_marker:
            inside = True
            buffered = []
            continue
        if stripped == end_marker and inside:
            inside = False
            buffered = []
            continue
        if inside:
            buffered.append(line)
            continue
        kept.append(line)
    if inside:
        kept.extend(buffered)
    return _blocks("\n".join(kept))


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def check_customization_quality(
    repo_root: Path | str,
    changed_files: Iterable[str] | None = None,
) -> CustomizationQualityResult:
    """Run every mechanically checkable authoring rule over the canonical tree.

    Args:
        repo_root: Repository root.
        changed_files: When given, violations are reported only against these
            files (after filtering them through the selection predicate). The
            whole corpus is still read, because Q3, the repeated-line half of
            Q9, and the duplication rule are all relations between files — an
            unchanged file can supply the collision that triggers a violation
            in a changed one. When ``None``, every selected file is reported
            against.

    Returns:
        A :class:`CustomizationQualityResult` whose violations are sorted by
        path then rule.
    """
    root = Path(repo_root)
    if not root.is_dir():
        raise ValueError(f"repo_root must be an existing directory, got: {repo_root!r}")
    corpus_paths = discover_customization_files(root)
    if changed_files is None:
        reported_paths = list(corpus_paths)
    else:
        selected = {normalize_path(path) for path in changed_files if is_selected(path)}
        reported_paths = [path for path in corpus_paths if path in selected]
    reported = set(reported_paths)

    units = [load_unit(root, path) for path in corpus_paths]
    violations: list[Violation] = []
    for unit in units:
        if unit.path not in reported:
            continue
        violations.extend(check_description(unit))
        violations.extend(check_name(unit))
        violations.extend(check_size(unit))
        violations.extend(check_rationale(unit))
        violations.extend(check_prohibitions(unit))
        violations.extend(check_format_example(unit))
        violations.extend(check_path_references(unit, root))
    violations.extend(check_emphasis(units, reported))
    violations.extend(check_description_similarity(units, reported))
    violations.extend(check_duplicate_blocks(units, reported))

    violations.sort(key=lambda violation: (violation.path, violation.rule, violation.message))
    return CustomizationQualityResult(
        checked_files=reported_paths,
        corpus_files=corpus_paths,
        violations=violations,
    )


# Alias required by issue #3757: the module must expose a ``validate`` function
# taking a repository root and an iterable of changed paths.
validate = check_customization_quality
