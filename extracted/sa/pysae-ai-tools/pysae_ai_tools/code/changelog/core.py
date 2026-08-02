"""Pure changelog logic: entry generation, validation, markdown merge.

No Typer, no file writes — every function here takes explicit inputs (strings,
context) and returns values. The file-I/O orchestration (reading
``changelogs/``, writing ``CHANGELOG.md``) and the command layer live in
:mod:`.cli`. Version-tag semantics live in :mod:`..versioning`.

Validation enforces the strict conventional commits format, a mandatory trailing
issue reference, and the length budget:

    * <type>: <description> (#<iid>)

Type ∈ {feat, fix, tech, refactor, docs, chore, perf, build, ci, style, test,
revert}. The pattern is delegated to commitizen's ``ConventionalCommitsCz``
(with ``tech`` added for Pysae). The trailing issue reference — ``(#123)`` or a
cross-project ``(driver#16)`` — is **mandatory** for changelog entries (unlike
commit messages, where commitlint leaves it optional), so the release notes can
always link back to the ticket. The full bullet line (``* `` prefix included)
must also stay within ``MAX_ENTRY_LENGTH`` chars.
"""

import re
import subprocess
from dataclasses import dataclass
from pathlib import Path

from commitizen.config import BaseConfig
from commitizen.cz.conventional_commits.conventional_commits import ConventionalCommitsCz

from ...common.conventional import CHANGELOG_TYPES
from ...common.group import ensure_group_namespace, resolve_group
from ...internal.detect_context.detect import DetectArgs, detect

MAX_ENTRY_LENGTH = 200
"""Maximum total length of a changelog entry, prefix ``* `` included."""


@dataclass
class ChangelogEntry:
    file: str
    content: str
    type: str
    issue_iid: str
    branch: str
    description: str
    already_exists: bool = False


class ChangelogTooLongError(ValueError):
    """Raised when a generated changelog entry exceeds ``MAX_ENTRY_LENGTH``.

    Carries the budget breakdown so callers (in particular the changelog skill)
    can regenerate a shorter description without re-running the format math.

    Attributes:
        content: the over-budget formatted entry (``* type: desc (#iid)``).
        current_length: ``len(content)``.
        max_total_length: ``MAX_ENTRY_LENGTH``.
        max_description_length: maximum description length that would fit,
            given the resolved type/issue_iid (i.e. total budget minus the
            ``* type: `` prefix and the `` (#iid)`` suffix).
        change_type, issue_iid, description: the resolved fields used to
            build the failed entry.
    """

    def __init__(
        self,
        *,
        content: str,
        max_description_length: int,
        change_type: str,
        issue_iid: str,
        description: str,
    ) -> None:
        self.content = content
        self.current_length = len(content)
        self.max_total_length = MAX_ENTRY_LENGTH
        self.max_description_length = max_description_length
        self.change_type = change_type
        self.issue_iid = issue_iid
        self.description = description
        super().__init__(
            f"changelog entry is {self.current_length} chars, max is {MAX_ENTRY_LENGTH}; "
            f"regenerate the description with at most {max_description_length} chars"
        )


# Branch prefix -> changelog type
_PREFIX_MAP: dict[str, str] = {
    "feat": "feat",
    "fix": "fix",
    "tech": "tech",
    "refactor": "refactor",
    "docs": "docs",
    "chore": "chore",
    "perf": "perf",
}

# GitLab issue type label -> changelog type
_LABEL_TYPE_MAP: dict[str, str] = {
    "type::bug": "fix",
    "type::feature": "feat",
    "type::technical": "tech",
    "type::debt": "tech",
}


def _detect_type_from_labels(labels: list[str]) -> str:
    """Detect changelog type from GitLab issue type::* labels."""
    for label in labels:
        if label in _LABEL_TYPE_MAP:
            return _LABEL_TYPE_MAP[label]
    return ""


def _detect_type_from_branch(branch: str) -> str:
    """Detect changelog type from branch prefix (e.g. feat/123-slug -> feat)."""
    prefix = branch.split("/")[0] if "/" in branch else ""
    return _PREFIX_MAP.get(prefix, "")


def _detect_type_from_commits() -> str:
    """Detect changelog type from recent commit messages on the branch."""
    try:
        result = subprocess.run(
            ["git", "log", "--oneline", "--no-merges", "-10", "--format=%s"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=5,
        )
        if result.returncode != 0:
            return ""
        for line in result.stdout.strip().splitlines():
            match = re.match(r"^(\w+)[:(]", line)
            if match and match.group(1).lower() in _PREFIX_MAP:
                return _PREFIX_MAP[match.group(1).lower()]
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    return ""


def _extract_issue_iid(branch: str) -> str:
    """Extract issue IID from branch name (e.g. feat/123-slug -> 123)."""
    match = re.search(r"(\d+)", branch)
    return match.group(1) if match else ""


def _description_from_branch(branch: str) -> str:
    """Build a default description from branch slug."""
    # Remove prefix/ and IID, keep the slug
    slug = branch.split("/", 1)[-1] if "/" in branch else branch
    slug = re.sub(r"^\d+-", "", slug)  # Remove leading IID
    return slug.replace("-", " ").strip()


def _description_from_commits() -> str:
    """Get description from the first commit message on the branch."""
    try:
        result = subprocess.run(
            ["git", "log", "--oneline", "--no-merges", "-1", "--format=%s"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=5,
        )
        if result.returncode == 0 and result.stdout.strip():
            msg = result.stdout.strip()
            # Strip conventional commit prefix
            stripped = re.sub(r"^\w+(\(.+?\))?:\s*", "", msg)
            return stripped if stripped else msg
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    return ""


def generate_entry(
    description: str = "",
    branch: str = "",
    issue_iid: str = "",
    change_type: str = "",
    issue_labels: list[str] | None = None,
) -> ChangelogEntry:
    """Generate a changelog entry from context.

    Auto-detects branch, issue IID, type, and description if not provided.
    Type priority: explicit > issue label > branch prefix > commit prefix > "feat".
    """
    # Resolve context from detect_context (gives branch, issue IID, labels, titles)
    mr_title = ""
    issue_title = ""
    try:
        ctx_args = DetectArgs()
        ctx = detect(ctx_args)
        branch = branch or ctx.mr_source_branch or ctx.git_branch
        issue_iid = issue_iid or ctx.issue_iid
        mr_title = ctx.mr_title
        issue_title = ctx.issue_title
        if issue_labels is None:
            issue_labels = ctx.issue_labels
    except Exception:
        pass

    # Fallback: branch from git
    if not branch:
        try:
            result = subprocess.run(
                ["git", "branch", "--show-current"],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=5,
            )
            branch = result.stdout.strip() if result.returncode == 0 else ""
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass

    # Fallback: issue IID from branch name
    if not issue_iid:
        issue_iid = _extract_issue_iid(branch)

    # Resolve type: label > branch prefix > commit prefix > "feat"
    if not change_type:
        change_type = (
            _detect_type_from_labels(issue_labels or [])
            or _detect_type_from_branch(branch)
            or _detect_type_from_commits()
            or "tech"
        )

    # Resolve description: issue title > MR title > commits > branch slug
    if not description:
        raw = issue_title or mr_title
        if raw:
            # Strip conventional commit prefix if present (e.g. "feat: add export" -> "add export")
            description = re.sub(r"^\w+(\(.+?\))?:\s*", "", raw)
        if not description:
            description = _description_from_commits() or _description_from_branch(branch)

    # Clean description
    if description:
        # Strip trailing issue ref if present (e.g. "(#123)") — the script adds it automatically
        description = re.sub(r"\s*\(#\d+\)\s*$", "", description)
        # Ensure lowercase start, no trailing period
        description = description[0].lower() + description[1:]
        description = description.rstrip(".")

    # Build content line
    issue_ref = f" (#{issue_iid})" if issue_iid else ""
    content = f"* {change_type}: {description}{issue_ref}"

    if len(content) > MAX_ENTRY_LENGTH:
        max_desc = MAX_ENTRY_LENGTH - len(f"* {change_type}: {issue_ref}")
        raise ChangelogTooLongError(
            content=content,
            max_description_length=max_desc,
            change_type=change_type,
            issue_iid=issue_iid,
            description=description,
        )

    # Canonical entry filename: <type>-<iid>-<slug>.md — consistent with the
    # validation layer (``_filename_hints``) and independent of how the branch was
    # named. A bare "123" branch must not collapse to "123.md" (no type, just the
    # IID); the type prefix and IID are always emitted, the slug comes from the
    # branch (minus its type prefix and leading IID), falling back to the description.
    branch_slug = re.sub(r"^\d+-?", "", branch.split("/", 1)[-1]) if branch else ""
    slug = re.sub(r"[^a-z0-9]+", "-", (branch_slug or description).lower()).strip("-")[:50].rstrip("-")
    name_parts = [part for part in (change_type, issue_iid, slug) if part]
    filename = "-".join(name_parts) if name_parts else "changelog"
    filepath = f"changelogs/{filename}.md"
    already_exists = Path(filepath).exists()

    return ChangelogEntry(
        file=filepath,
        content=content,
        type=change_type,
        issue_iid=issue_iid,
        branch=branch,
        description=description,
        already_exists=already_exists,
    )


# ---------------------------------------------------------------------------
# Validation (commitizen-backed)
# ---------------------------------------------------------------------------


class _PysaeCz(ConventionalCommitsCz):  # type: ignore[misc, unused-ignore]
    """Conventional commits with Pysae's ``tech`` type added."""

    def schema_pattern(self) -> str:
        return r"(?s)" r"(" + "|".join(CHANGELOG_TYPES) + r")" r"(\(\S+\))?!?:" r"( [^\n\r]+)" r"((\n\n.*)|(\s*))?$"


_CZ = _PysaeCz(BaseConfig())  # type: ignore[no-untyped-call, unused-ignore]
_CZ_PATTERN = re.compile(_CZ.schema_pattern())


def _first_bullet(content: str) -> tuple[str, int] | None:
    """Return the first non-blank line and its index, or None if file is empty."""
    for i, line in enumerate(content.splitlines()):
        if line.strip():
            return line, i
    return None


def _strip_bullet(line: str) -> str | None:
    """Strip the leading ``* `` bullet. Returns None if missing."""
    if not line.startswith("* "):
        return None
    return line[2:].strip()


def _strip_iid_ref(body: str) -> str:
    """Strip a trailing ``(#123)`` issue reference."""
    return re.sub(r"\s*\(#\d+\)\s*$", "", body).strip()


# A trailing issue reference, mandatory on every changelog entry. Accepts both
# the current-project form ``(#123)`` and the cross-project form ``(driver#16)``
# / ``(pysae/driver#16)``. Unlike commit messages — where commitlint leaves the
# reference optional — a changelog entry MUST carry one so the release notes can
# always link back to the originating ticket.
_TRAILING_ISSUE_REF_RE = re.compile(r"\((?:[\w./-]+)?#\d+\)\s*$")


def _has_issue_ref(line: str) -> bool:
    """Return True if ``line`` ends with a ``(#123)`` / ``(project#123)`` reference."""
    return bool(_TRAILING_ISSUE_REF_RE.search(line.rstrip()))


def _validate_body(body: str) -> bool:
    """Return True if ``body`` (without bullet, without trailing iid) is valid."""
    return bool(_CZ_PATTERN.match(_strip_iid_ref(body)))


def _filename_hints(filename: str) -> tuple[str, str]:
    """Extract (type, iid) hints from a filename like ``feat-123-slug.md``."""
    stem = Path(filename).stem
    parts = stem.split("-")
    type_ = ""
    iid = ""
    if parts and parts[0] in _PREFIX_MAP:
        type_ = parts[0]
        parts = parts[1:]
    if parts and parts[0].isdigit():
        iid = parts[0]
    return type_, iid


def _try_fix(line: str, filename: str) -> str | None:
    """Reformat ``line`` to the strict format using filename hints when needed."""
    file_type, file_iid = _filename_hints(filename)
    body = line.lstrip()
    if body.startswith("*"):
        body = body[1:].lstrip()

    type_ = ""
    iid = ""
    desc = ""

    # Pattern: '#iid type: desc'
    m = re.match(r"^#(\d+)\s+(\w+):\s*(.+)$", body)
    if m and m.group(2).lower() in _PREFIX_MAP:
        iid = m.group(1)
        type_ = m.group(2).lower()
        desc = m.group(3)

    if not type_:
        # Pattern: 'type: desc'
        m = re.match(r"^(\w+):\s*(.+)$", body)
        if m and m.group(1).lower() in _PREFIX_MAP:
            type_ = m.group(1).lower()
            desc = m.group(2)

    if not type_:
        # Pattern: '#iid[:] desc'
        m = re.match(r"^#(\d+)[:\s]\s*(.+)$", body)
        if m:
            iid = m.group(1)
            desc = m.group(2)

    if not desc:
        # Free text fallback
        desc = body

    if not iid:
        iid = file_iid
    if not type_:
        type_ = file_type or "tech"

    desc = _strip_iid_ref(desc)
    if not desc:
        return None
    desc = desc[0].lower() + desc[1:]
    desc = desc.rstrip(".")

    iid_ref = f" (#{iid})" if iid else ""
    return f"* {type_}: {desc}{iid_ref}"


@dataclass
class _ValidationFailure:
    file: Path
    reason: str
    line: str


def _length_failure_reason(line: str) -> str | None:
    """Return a failure reason if ``line`` exceeds ``MAX_ENTRY_LENGTH``, else None.

    The budget is measured on the full bullet line (``* `` prefix included),
    matching :func:`generate_entry` which raises :class:`ChangelogTooLongError`
    on the same measure. Trailing whitespace is ignored so a stray space at the
    end of a file does not trip the check.
    """
    length = len(line.rstrip())
    if length > MAX_ENTRY_LENGTH:
        excess = length - MAX_ENTRY_LENGTH
        return f"entry is {length} chars, max is {MAX_ENTRY_LENGTH} (trim the description by {excess} char(s))"
    return None


# ---------------------------------------------------------------------------
# Merge — build the CHANGELOG.md release section (pure string transforms)
# ---------------------------------------------------------------------------

_CHANGELOG_HEADER = """# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
"""

_UNRELEASED_RE = re.compile(r"^##\s*\[?Unreleased\]?\s*$", re.MULTILINE)


# A cross-project ref ``(project#123)`` or ``(group/project#123)`` — at least one
# word char before the ``#`` distinguishes it from the current-project ``(#123)``
# form. The ``pysae`` group (and any subgroup) is optional in the source: a bare
# ``(driver#16)`` is treated as a cross-project ref and gets the ``pysae/`` prefix
# added when building the link.
_EXTERNAL_REF_RE = re.compile(r"\(([\w.-]+(?:/[\w.-]+)*)#(\d+)\)")
_INTERNAL_REF_RE = re.compile(r"\(#(\d+)\)")


def _gitlab_host(project_url: str) -> str:
    """Scheme + host of ``project_url`` (e.g. ``https://gitlab.com``), or empty."""
    match = re.match(r"(https?://[^/]+)", project_url)
    return match.group(1) if match else ""


def _linkify_issue_refs(body: str, project_url: str) -> str:
    """Linkify issue refs to markdown.

    - current project: ``(#123)`` → ``([#123](project_url/-/issues/123))``;
    - cross-project: ``(group/project#123)`` → ``([group/project#123](host/group/project/-/issues/123))``,
      where ``host`` is the scheme+host of ``project_url`` (so external tickets like
      ``(pysae/op#1705)`` become real links too). When the ref omits the group
      namespace (``(gtfsrt-to-siri#16)``, ``(op#1722)``), the resolved group is added to
      the link target — the displayed label keeps the author's text.
    """
    if not project_url or not body:
        return body
    host = _gitlab_host(project_url)
    if host:
        group = resolve_group()  # resolve once, not per matched ref
        body = _EXTERNAL_REF_RE.sub(
            lambda m: f"([{m.group(1)}#{m.group(2)}]"
            f"({host}/{ensure_group_namespace(m.group(1), group)}/-/issues/{m.group(2)}))",
            body,
        )
    return _INTERNAL_REF_RE.sub(
        lambda m: f"([#{m.group(1)}]({project_url}/-/issues/{m.group(1)}))",
        body,
    )


_LINKED_EXTERNAL_REF_RE = re.compile(r"\(\[([\w.-]+(?:/[\w.-]+)*#\d+)\]\([^)]+\)\)")
_LINKED_ISSUE_REF_RE = re.compile(r"\(\[#(\d+)\]\([^)]+\)\)")


def _delink_issue_refs(body: str) -> str:
    """Inverse of :func:`_linkify_issue_refs` — strip markdown links back to bare refs.

    Handles both ``([#123](url))`` → ``(#123)`` and the cross-project
    ``([group/project#123](url))`` → ``(group/project#123)``. Used in the
    re-release path of ``release`` to reconstruct ``section_raw`` (the
    bare-ref version meant for annotated git tag messages) from the already-linkified
    body that lives in ``CHANGELOG.md``.
    """
    body = _LINKED_EXTERNAL_REF_RE.sub(r"(\1)", body)
    return _LINKED_ISSUE_REF_RE.sub(r"(#\1)", body)


def _existing_section_pattern(tag: str) -> re.Pattern[str]:
    """Pattern that captures ``## [tag] DATE`` and its body up to the next ``##``.

    Groups: ``date`` (everything after the ``]`` on the heading line) and ``body``
    (the bullets between this heading and the next ``##`` heading, or EOF).
    """
    return re.compile(
        rf"^##\s*\[{re.escape(tag)}\]\s*(?P<date>[^\n]*)\n(?P<body>.*?)(?=^##\s|\Z)",
        re.MULTILINE | re.DOTALL,
    )


def find_existing_section(content: str, tag: str) -> re.Match[str] | None:
    """Locate a previously-written ``## [tag] DATE`` section in ``content``.

    Returns ``None`` when no such section exists (fresh release path).
    """
    return _existing_section_pattern(tag).search(content)


def _splice_section(existing: str, match: re.Match[str], new_section: str) -> str:
    """Replace the span of ``match`` in ``existing`` with ``new_section``, keeping layout.

    Guarantees a blank line between the rewritten section and whatever follows
    (the next ``## `` heading) so sections never get glued together.
    """
    remainder = existing[match.end() :]
    new_content = existing[: match.start()] + new_section.rstrip("\n")
    if remainder.strip():
        new_content += "\n\n" + remainder.lstrip("\n")
    if not new_content.endswith("\n"):
        new_content += "\n"
    return new_content


def _build_section(tag: str, body: str, today: str) -> str:
    """Build a ``## [tag] YYYY-MM-DD`` section. ``body`` may be empty."""
    section = f"## [{tag}] {today}"
    if body:
        section += "\n\n" + body
    return section


_RELEASE_HEADING_RE = re.compile(r"^##\s", re.MULTILINE)


def _strip_unreleased(content: str) -> str:
    """Remove any ``## Unreleased`` / ``## [Unreleased]`` heading and its (empty) body."""
    match = _UNRELEASED_RE.search(content)
    if not match:
        return content
    start = match.start()
    # Find the next ## heading after Unreleased — that's where Unreleased's body ends.
    next_match = _RELEASE_HEADING_RE.search(content, match.end())
    end = next_match.start() if next_match else len(content)
    return content[:start] + content[end:]


def merge_changelog(existing: str, section: str, header: str = _CHANGELOG_HEADER) -> str:
    """Merge a new release ``section`` into ``existing`` CHANGELOG-like content.

    - If ``existing`` is empty (or has no top-level ``#`` header), ``header`` is
      prepended (default: the Keep a Changelog header for ``CHANGELOG.md``).
    - Any existing ``## Unreleased`` / ``## [Unreleased]`` block is removed.
    - The new release section is inserted right after the top-level header,
      before the first ``##`` heading.

    A blank line is guaranteed before every ``##`` heading (Keep a Changelog style).

    The same algorithm is reused by ``release_notes.merge`` to maintain the
    per-language ``release-notes/RELEASE_NOTES.<lang>.md`` files, each with its
    own localized header.
    """
    content = _strip_unreleased(existing) if existing.strip() else ""

    # Ensure a top-level ``#`` header is present.
    has_top_header = bool(re.search(r"^#\s+\S", content, re.MULTILINE))
    if not has_top_header:
        content = header + (content.lstrip("\n") if content else "")

    if not content.endswith("\n"):
        content += "\n"

    # Insert point: right before the first ``## `` heading, else at end of file.
    match = _RELEASE_HEADING_RE.search(content)
    if match:
        prefix = content[: match.start()].rstrip("\n") + "\n\n"
        suffix = content[match.start() :]
    else:
        prefix = content.rstrip("\n") + "\n\n"
        suffix = ""

    block = section.rstrip("\n") + "\n"
    if suffix:
        block += "\n"
    return prefix + block + suffix
