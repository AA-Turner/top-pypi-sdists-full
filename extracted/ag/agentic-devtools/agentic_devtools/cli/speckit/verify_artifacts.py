"""Pre-PR verification gate for SpecKit planning artifacts.

Composes the existing SpecKit validators into a single deterministic gate that
runs after artifact generation and **before** the commit/PR step, so that
defects which are mechanically checkable never reach the review loop.

The gate performs five checks, each reusing an existing validator rather than
reimplementing its rules:

===============  =========================================================
Check            Source of truth
===============  =========================================================
``referenced-path``      ``pass_g.reference_extractor`` + ``os.path.exists``
``unmapped-test-task``   ``pass_e2.validator.validate_test_coverage``
``fr-reference``         ``validate_frs.extract_frs``
``advertised-artifact``  directory listing vs. ``plan.md`` references
``checklist``            ``validate_checklists.validate_checklists``
===============  =========================================================

Each check silently no-ops when the artifact it inspects does not exist, so the
same command is safe to run after any pipeline phase. One exception applies to
``unmapped-test-task`` and ``fr-reference``: when ``tasks.md`` exists and either
check is enabled, a specification source (local ``spec.md`` or
``--spec-context``) is required, otherwise verification exits as an operational
error. Passing ``--phase`` restricts the run to the checks whose subject
artifact that phase produces, which keeps bounded regeneration coherent: a
reported violation always concerns an artifact the current phase is able to
rewrite.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

from .pass_e2.task_classifier import is_test_task
from .pass_e2.validator import _parse_tasks_from_content, validate_test_coverage
from .pass_g.models import Reference, ReferenceKind
from .pass_g.reference_extractor import classify_reference_kind, extract_references
from .validate_checklists import validate_checklists
from .validate_frs import extract_frs, sort_fr_ids

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

#: Check identifiers, used as the ``check`` field of every emitted violation.
CHECK_REFERENCED_PATH = "referenced-path"
CHECK_UNMAPPED_TEST_TASK = "unmapped-test-task"
CHECK_FR_REFERENCE = "fr-reference"
CHECK_ADVERTISED_ARTIFACT = "advertised-artifact"
CHECK_CHECKLIST = "checklist"

#: Every check, in execution order.
ALL_CHECKS: tuple[str, ...] = (
    CHECK_REFERENCED_PATH,
    CHECK_UNMAPPED_TEST_TASK,
    CHECK_FR_REFERENCE,
    CHECK_ADVERTISED_ARTIFACT,
    CHECK_CHECKLIST,
)

#: Checks enabled per generation step, keyed by the step number used by
#: ``generate-spec-from-issue.sh``.  A step maps to the checks whose subject
#: artifact that step writes, so regeneration can always fix a violation.
#: Steps 3 (plan), 4 (tasks) and 5 (analyze) all run inside pipeline phase 3,
#: which the gate scopes separately so each retry regenerates only the artifact
#: that failed.  Steps 1 (specify) and 5 (analyze) write no inspected artifact.
PHASE_CHECKS: dict[int, tuple[str, ...]] = {
    1: (),
    2: (CHECK_CHECKLIST,),
    3: (CHECK_REFERENCED_PATH, CHECK_ADVERTISED_ARTIFACT),
    4: (CHECK_REFERENCED_PATH, CHECK_UNMAPPED_TEST_TASK, CHECK_FR_REFERENCE),
    5: (),
}

#: Artifacts scanned for repository file-path references, per phase.  Any other
#: phase (and an unscoped run) scans both.
_PATH_REFERENCE_SOURCES: dict[int, tuple[str, ...]] = {
    3: ("plan.md",),
    4: ("tasks.md",),
}

#: Filenames the SpecKit pipeline itself writes into the spec directory.  A
#: reference to one of these from ``plan.md`` advertises a spec artifact.
SPEC_ARTIFACT_FILENAMES: frozenset[str] = frozenset(
    {
        "spec.md",
        "plan.md",
        "tasks.md",
        "research.md",
        "data-model.md",
        "quickstart.md",
        "analysis-report.md",
    }
)

#: When the plan step runs, ``plan.md`` may describe artifacts produced by the
#: later tasks and analyze steps.  Those outputs do not exist yet and must not
#: block the plan gate.
_PHASE3_ADVERTISED_ARTIFACT_FILENAMES: frozenset[str] = SPEC_ARTIFACT_FILENAMES.difference(
    {"tasks.md", "analysis-report.md"}
)

#: When the plan step runs, canonical ``generated/<name>`` diagnostics are
#: written by the later tasks/analyze steps and therefore not required yet.
_PHASE3_ADVERTISED_GENERATED_ARTIFACT_FILENAMES: frozenset[str] = frozenset()

#: Subdirectories of the spec directory that hold generated spec artifacts.
SPEC_ARTIFACT_DIRS: tuple[str, ...] = ("contracts/", "checklists/")

#: Subdirectory of the spec directory that holds machine-generated diagnostics
#: (``fr-coverage.json``, ``test-coverage.json``, ``analysis-report.md``).  The
#: name matches the ``**/generated/**/*`` pattern on GitHub's published Copilot
#: code review exclusion list, keeping analyser output out of the review
#: surface while it is still committed and still gates the phase.
GENERATED_ARTIFACT_SUBDIR: str = "generated"

#: Bare filenames that were relocated from the spec root into ``generated/``.
#: Only these names are eligible for the ``generated/`` fallback in
#: :func:`resolve_spec_artifact_path`; other bare names are never satisfied by
#: a same-named file under ``generated/``.
RELOCATED_GENERATED_ARTIFACT_FILENAMES: frozenset[str] = frozenset(
    {"fr-coverage.json", "test-coverage.json", "analysis-report.md"}
)

#: Characters that mark a reference as a template, glob or shell fragment
#: rather than a concrete path.
_UNCHECKABLE_CHARS = frozenset("<>{}$*?|\"'`()[]!")

#: Sigils that precede a variable interpolation.  A reference preceded by one
#: of these (for example ``$SPEC_DIR/spec.md`` inside a shell code fence) names
#: a runtime-expanded path, not a file that can be checked on disk.
_INTERPOLATION_SIGILS: tuple[str, ...] = ("$", "{", "%")

#: Key emitted by ``coverage_mapper.generate_task_scoped_findings`` for test
#: tasks that map to no functional requirement.
_UNMAPPED_TEST_TASK_KEY = "TASK:unmapped-test-task"

#: Matches the task IDs listed in an unmapped-test-task finding description.
_TASK_ID_RE = re.compile(r"\bT\d+\b")

#: Stricter set of verb markers used *only* by the gate's file-creation skip
#: logic.  Unlike ``pass_g.constants.NEW_SYMBOL_VERB_MARKERS`` (FR-006, 12
#: entries), this set is limited to verbs that unambiguously mean the file
#: ITSELF is being created, not merely worked on.  Generic verbs such as
#: "add", "implement", "write", "build", "register", and "wire up" commonly
#: appear in contexts like "Implement FR-001 in pkg/handler.py", where the
#: verb describes work done *in* an existing file, so they are intentionally
#: excluded here to keep the gate strict.
_GATE_FILE_CREATION_VERB_PATTERNS: tuple[re.Pattern[str], ...] = tuple(
    re.compile(r"\b" + re.escape(v) + r"\b")
    for v in (
        "create",
        "introduce",
        "define",
        "scaffold",
        "generate",
        "set up",
    )
)

_FILE_CREATION_CLAUSE_BOUNDARY_RE = re.compile(r"[,;]|\.\s+|\b(?:and|then|but|while)\b", re.IGNORECASE)
_MARKDOWN_LINK_DESTINATION_RE = re.compile(r"\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
_BARE_FILENAME_RE = re.compile(r"^[A-Za-z0-9_.-]+$")
#: Matches bare numeric or semver-like version strings such as ``3.12`` or
#: ``v1.2.3`` that are not valid repository filenames.
_VERSION_LIKE_RE = re.compile(r"^v?\d+(\.\d+)*$")
#: Matches Python class-attribute access expressions such as
#: ``HierarchyLevel.FEATURE`` or ``ReferenceKind.FILE_PATH`` that look like
#: bare filenames to ``_BARE_FILENAME_RE`` but are not repository paths.
_PYTHON_CLASS_ATTR_RE = re.compile(r"^[A-Z][a-zA-Z0-9]*\.[A-Z][A-Z0-9_]*$")
_PYTHON_MEMBER_ACCESS_RE = re.compile(r"^(?:[A-Z][a-z][A-Za-z0-9_]*|[a-z_][a-z0-9_]*)\.[a-z_][a-z0-9_]*$")
_PASSTHROUGH_EXT_RE = re.compile(r"\.(?:j2|lock|proto|ipynb|sql|css|html|xml|tf|env|conf|csv|in)$", re.IGNORECASE)
_NEGATED_ARTIFACT_STATEMENT_RES: tuple[re.Pattern[str], ...] = (
    re.compile(
        r"\bno\s+(?:separate\s+)?(?P<body>.+?)\bartifact(?:s)?\b\s+"
        r"(?:is|are|was|were)\s+(?:committed|generated|present|produced|created|written)\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"(?P<body>.+?)\bartifact(?:s)?\b\s+(?:is|are|was|were)\s+"
        r"not\s+(?:committed|generated|present|produced|created|written)\b",
        re.IGNORECASE,
    ),
)
_OPTIONAL_ARTIFACT_ANNOTATION_RE = re.compile(r"#\s*optional\s*[—–-]\s*only\s+when\b", re.IGNORECASE)

#: Common top-level domains treated as hostname-like when they appear in bare
#: prose tokens (for example ``example.com``).  This exclusion applies only to
#: root-level dotted tokens in the third bare-path pass and prevents ordinary
#: web-domain mentions from being misclassified as repository file references.
_HOSTNAME_LIKE_TLDS: frozenset[str] = frozenset(
    {
        "ai",
        "app",
        "biz",
        "ca",
        "ch",
        "co",
        "com",
        "de",
        "dev",
        "edu",
        "fr",
        "gov",
        "in",
        "info",
        "internal",
        "io",
        "jp",
        "local",
        "me",
        "mil",
        "net",
        "org",
        "uk",
        "us",
    }
)
_ROOT_FILENAME_TLD_EXEMPT_RE = re.compile(
    r"^(?:requirements|constraints)(?:[-_.][a-z0-9][a-z0-9_.-]*)?\.in$",
    re.IGNORECASE,
)

#: Text tolerated between a creation verb and the file reference when the
#: reference is still the object being created.  Only determiners, file nouns
#: and naming prepositions qualify ("create a new file at ``pkg/api.py``").
#: Any other word means the verb governs a different object — a noun phrase
#: ("create a service in ``pkg/typo.py``") or a subordinate clause ("create a
#: service that updates ``pkg/typo.py``") — so the reference is not exempted.
_CREATION_OBJECT_FILLER_RE = re.compile(
    r"^(?:[\s:;,._\-*\"'`\[(]"
    r"|\b(?:a|an|the|new|empty|blank|initial|file|files|module|script|directory|directories|path|paths|"
    r"at|named|called)\b)*$",
    re.IGNORECASE,
)

#: Conventional extensionless basenames that are valid repository files.  The
#: dot-in-basename check in :func:`is_checkable_path_reference` would otherwise
#: filter out references to ``Dockerfile``, ``Makefile``, etc.
_CONVENTIONAL_EXTENSIONLESS_FILENAMES: frozenset[str] = frozenset(
    {
        "Dockerfile",
        "Makefile",
        "Vagrantfile",
        "Procfile",
        "Jenkinsfile",
        "Brewfile",
        "Gemfile",
        "Pipfile",
        "Rakefile",
        "CMakeLists",
    }
)

#: Conventional extensionless filenames are also matched in the third bare-path
#: pass so ordinary prose like ``Update Makefile`` is verified without requiring
#: backticks or a Markdown link.
_BARE_ROOT_FILENAME_ALT = "|".join(re.escape(filename) for filename in sorted(_CONVENTIONAL_EXTENSIONLESS_FILENAMES))

#: Matches a bare (non-backtick, non-URL) repository path in ordinary Markdown
#: prose.  The match includes either a slash-containing path or a root-level
#: filename token.  The negative lookbehind ``(?<![`:\w/.])`` prevents matching
#: URL path segments (``://example.com/…``) — characters within a hostname like
#: ``example.com/…`` are preceded by a word character or a dot — and paths
#: already preceded by a backtick (handled by the backtick loop), a colon (for
#: example ``key:value`` pairs), or a slash.  The trailing ``\b`` prevents
#: greedily consuming trailing sentence-punctuation dots (e.g. the ``.`` in
#: ``runner.py.`` at end of a sentence).  Post-match filtering then rejects
#: templates, globs, absolute paths, module-like hostnames such as
#: ``example.com``, and other non-verifiable tokens.
_BARE_PATH_RE = re.compile(
    rf"(?<![`:\w/.])((?:[\w.-]+(?:/[\w.-]+)+)|(?:[\w.-]*\.[\w.-]+)|(?:{_BARE_ROOT_FILENAME_ALT}))\b"
)


def _normalize_reference_text(text: str) -> str:
    """Strip fragment/query suffixes and surrounding whitespace from *text*."""
    return text.split("#", 1)[0].split("?", 1)[0].strip()


def _is_hostname_like_root_token(text: str) -> bool:
    """Return ``True`` when *text* looks like a root-level hostname.

    This intentionally targets only bare dotted root tokens (no ``/``), so
    normal repository paths are unaffected.
    """
    token = _normalize_reference_text(text).lower()
    if not token or "/" in token or token.startswith(".") or "." not in token:
        return False
    if _ROOT_FILENAME_TLD_EXEMPT_RE.fullmatch(token):
        return False
    labels = token.split(".")
    if len(labels) < 2 or any(not label for label in labels):
        return False
    if any(label.startswith("-") or label.endswith("-") for label in labels):
        return False
    if any(re.fullmatch(r"[a-z0-9-]+", label) is None for label in labels):
        return False
    return labels[-1] in _HOSTNAME_LIKE_TLDS


def _reference_clause(reference: Reference) -> str:
    """Return the clause containing *reference* within its context sentence."""
    context = reference.context_sentence
    lower_context = context.lower()
    lower_reference = _normalize_reference_text(reference.text).lower()
    if not lower_reference:
        return ""
    all_starts = [start for start, _ in _ordered_reference_spans(lower_context, lower_reference)]
    if reference.occurrence_index >= len(all_starts):
        return ""
    start = all_starts[reference.occurrence_index]
    end = start + len(lower_reference)

    left = 0
    right = len(context)
    for match in _FILE_CREATION_CLAUSE_BOUNDARY_RE.finditer(context):
        if match.end() <= start:
            left = match.end()
            continue
        if match.start() >= end:
            right = match.start()
            break

    return lower_context[left:right]


def _has_file_creation_intent(reference: Reference) -> bool:
    """Return True if the reference context unambiguously describes a new file.

    Uses a stricter verb set than ``pass_g.intent_detector`` (FR-006) so that
    only references whose surrounding sentence clearly expresses that the
    referenced path is *itself* being created are skipped.  Ambiguous task
    verbs ("add", "implement", "write", etc.) are not considered.

    An additional guard requires the reference to be the *object* of that verb:
    everything between the verb and the reference must be determiner/file-noun
    filler ("create a new file at ``pkg/api.py``").  Any other wording means
    the verb governs something else — a different noun phrase ("create a
    service in ``pkg/missing.py``") or a subordinate clause ("create a service
    that updates ``pkg/missing.py``") — and the reference is not exempted.
    """
    clause = _reference_clause(reference)
    target = _normalize_reference_text(reference.text).lower()
    reference_start = clause.find(target)
    if reference_start == -1:
        return False
    prefix = clause[:reference_start]
    for pattern in _GATE_FILE_CREATION_VERB_PATTERNS:
        match = pattern.search(prefix)
        if not match:
            continue
        # Only the path itself may be the created object; anything else between
        # the verb and the reference means the verb governs a different object.
        if not _CREATION_OBJECT_FILLER_RE.match(prefix[match.end() :]):
            continue
        return True
    return False


# ---------------------------------------------------------------------------
# Data types
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Violation:
    """A single deterministic defect found in the generated artifacts."""

    check: str
    artifact: str
    detail: str

    def to_dict(self) -> dict[str, str]:
        """Return a JSON-serialisable dict."""
        return {"check": self.check, "artifact": self.artifact, "detail": self.detail}


@dataclass
class VerificationResult:
    """Aggregate result of running the pre-PR verification gate."""

    violations: list[Violation]
    checks_run: list[str]

    @property
    def passed(self) -> bool:
        """Return ``True`` when no violation was recorded."""
        return not self.violations

    def to_json(self) -> dict[str, object]:
        """Return a JSON-serialisable dict for machine consumption."""
        return {
            "passed": self.passed,
            "checks_run": list(self.checks_run),
            "violations": [v.to_dict() for v in self.violations],
        }


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _read_text(path: Path) -> str | None:
    """Return the text of *path*, or ``None`` when it cannot be read."""
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None


def is_checkable_path_reference(text: str) -> bool:
    """Return ``True`` when *text* is a concrete, verifiable repository path.

    Excludes shell fragments, templated placeholders, glob patterns, URLs,
    absolute paths, parent traversals, and non-filename tokens (for example
    ``P1/P2/P3``).  Root-level filenames are allowed.
    """
    text = _normalize_reference_text(text)
    if not text or any(ch.isspace() for ch in text):
        return False
    if _UNCHECKABLE_CHARS.intersection(text):
        return False
    if text.lower() == "e.g":
        return False
    if "://" in text or text.startswith(("/", "~")) or ".." in text:
        return False
    if "/" not in text and _is_hostname_like_root_token(text):
        return False
    # Reject bare numeric/version-shaped tokens such as "3.12" or "v1.2.3".
    # These are never valid repository filenames but do contain a dot, which
    # would otherwise pass the basename check below.
    if "/" not in text and _VERSION_LIKE_RE.fullmatch(text):
        return False
    # Reject Python class-attribute expressions such as ``HierarchyLevel.FEATURE``
    # or ``ReferenceKind.FILE_PATH``.  These match ``_BARE_FILENAME_RE`` because
    # they contain only alphanumerics and a dot, but they are Python symbols, not
    # file paths.
    if "/" not in text and _PYTHON_CLASS_ATTR_RE.fullmatch(text):
        return False
    # Extraction supplies reference-kind context for dotted tokens.  Preserve
    # that distinction here as well for callers checking a token directly.
    if "/" not in text and not text.startswith(".") and not _PASSTHROUGH_EXT_RE.search(text):
        reference_kind = classify_reference_kind(text)
        if reference_kind is ReferenceKind.MODULE_PATH:
            return False
        if reference_kind is ReferenceKind.METHOD_NAME and _PYTHON_MEMBER_ACCESS_RE.fullmatch(text):
            return False
    basename = text.rsplit("/", 1)[-1]
    if "." not in basename and basename not in _CONVENTIONAL_EXTENSIONLESS_FILENAMES:
        return False
    return "/" in text or _BARE_FILENAME_RE.fullmatch(text) is not None


def is_spec_artifact_reference(text: str) -> bool:
    """Return ``True`` when *text* names an artifact of the spec directory.

    Recognises bare filenames (``analysis-report.md``), ``contracts/`` and
    ``checklists/`` subtree paths, and canonical ``generated/<name>`` paths for
    the relocated machine-generated diagnostics.
    """
    if text in SPEC_ARTIFACT_FILENAMES:
        return True
    if text.startswith(SPEC_ARTIFACT_DIRS):
        return True
    # Canonical generated/ paths for relocated diagnostics.
    prefix = f"{GENERATED_ARTIFACT_SUBDIR}/"
    if text.startswith(prefix):
        return text[len(prefix) :] in RELOCATED_GENERATED_ARTIFACT_FILENAMES
    return False


def resolve_generated_artifact(spec_dir: Path, filename: str) -> Path:
    """Return the path of a machine-generated diagnostic inside *spec_dir*.

    The pipeline writes diagnostics under ``<spec_dir>/generated/``.  Spec
    directories produced before that relocation carry them at the spec-directory
    root, so the legacy location is returned when it holds the only copy.  When
    the file exists in neither place, the current (``generated/``) path is
    returned.
    """
    current = spec_dir / GENERATED_ARTIFACT_SUBDIR / filename
    if current.is_file():
        return current
    legacy = spec_dir / filename
    if legacy.is_file():
        return legacy
    return current


def resolve_spec_artifact_path(spec_dir: Path, text: str) -> Path | None:
    """Resolve an advertised spec artifact path when it stays inside *spec_dir*."""
    candidate = (spec_dir / text).resolve(strict=False)
    try:
        candidate.relative_to(spec_dir.resolve())
    except ValueError:
        return None
    if not candidate.is_file() and "/" not in text and text in RELOCATED_GENERATED_ARTIFACT_FILENAMES:
        # Machine-generated diagnostics moved into `generated/`; a plan that
        # names one bare still advertises a produced artifact.
        generated = (spec_dir / GENERATED_ARTIFACT_SUBDIR / text).resolve(strict=False)
        if generated.is_file():
            return generated
    return candidate


def is_gitignored(path: Path) -> bool:
    """Return ``True`` when *path* is excluded by any active ``.gitignore`` rule.

    Uses ``git -C <parent_dir> check-ignore --quiet`` so all gitignore layers
    (global, repo, and directory-level) are respected.  The ``-C`` flag ensures
    git discovers the working tree even when the process working directory lies
    outside the repository.  Returns ``False`` when *path* is not inside a git
    working tree, when ``git`` is unavailable, or when the command fails for any
    other reason — callers should treat the file as committable in that case
    (this can happen inside unit-test ``tmp_path`` directories).
    """
    try:
        completed = subprocess.run(  # noqa: S603 - fixed argv, no shell
            ["git", "-C", str(path.parent), "check-ignore", "--quiet", str(path)],
            capture_output=True,
            text=True,
            check=False,
            shell=False,
        )
    except OSError:
        return False
    return completed.returncode == 0


def is_variable_interpolation(reference: Reference) -> bool:
    """Return ``True`` when the reference is preceded by a variable sigil.

    The reference extractor strips the leading ``$`` from shell snippets, so
    ``"$SPEC_DIR/spec.md"`` surfaces as ``SPEC_DIR/spec.md``.  Such references
    are runtime-expanded paths and must not be checked against the filesystem.
    """
    context = reference.context_sentence
    normalized_reference = _normalize_reference_text(reference.text)
    if not normalized_reference:
        return False
    lower_context = context.lower()
    all_starts = [start for start, _ in _ordered_reference_spans(lower_context, normalized_reference.lower())]
    if reference.occurrence_index >= len(all_starts):
        return False
    start = all_starts[reference.occurrence_index]
    return start > 0 and context[start - 1] in _INTERPOLATION_SIGILS


def _is_negated_artifact_reference(reference: Reference) -> bool:
    """Return ``True`` when the surrounding sentence explicitly says no artifact exists."""
    sentence = reference.context_sentence.lower()
    target = _normalize_reference_text(reference.text).lower()
    if not sentence or not target:
        return False
    for pattern in _NEGATED_ARTIFACT_STATEMENT_RES:
        for match in pattern.finditer(sentence):
            if target in match.group("body"):
                return True
    return False


def _is_conditional_artifact_reference(reference: Reference) -> bool:
    """Return ``True`` when the surrounding context marks the artifact as optional.

    Recognises the ``# Optional — only when …`` annotation used in spec
    directory-tree blocks (e.g. plan-template generated output), where the
    absence of the file is expected and must not raise a violation.
    """
    sentence = reference.context_sentence
    if not sentence:
        return False
    return bool(_OPTIONAL_ARTIFACT_ANNOTATION_RE.search(sentence))


def _is_illustrative_example_reference(reference: Reference) -> bool:
    """Return ``True`` when *reference* appears in an illustrative example clause."""
    sentence = reference.context_sentence
    if not sentence:
        return False
    normalized_reference = _normalize_reference_text(reference.text)
    if not normalized_reference:
        return False
    lower_sentence = sentence.lower()
    lower_reference = normalized_reference.lower()

    # Collect all positions of the reference in the sentence and select the
    # one that matches this reference's occurrence index.  Using find() always
    # selects the *first* position, which is wrong when the same path appears
    # more than once in the same context sentence (e.g. when an illustrative
    # clause contains "inspect a.py and update a.py" — both occurrences receive
    # the full sentence as context, but the second should not be suppressed).
    all_starts = [start for start, _ in _ordered_reference_spans(lower_sentence, lower_reference)]
    if not all_starts:
        return False
    if reference.occurrence_index >= len(all_starts):
        return False
    reference_start = all_starts[reference.occurrence_index]

    prefix = lower_sentence[:reference_start]
    markers = list(
        re.finditer(
            r"(?:e\.g\.|for example)(?!\s+generation\b)"
            r"(?=\s*(?:$|[,;:]|[`(\[]|[a-z0-9_.-]+(?:/[a-z0-9_.-]+)*\.[a-z0-9]+))",
            prefix,
        )
    )
    if not markers:
        return False
    marker = markers[-1]

    # Build parenthetical ranges from the full sentence so that conjunctions
    # inside groups like "(e.g. `a.py` and `b.py`)" are not treated as
    # clause boundaries separating the reference from the illustrative marker.
    paren_ranges: list[tuple[int, int]] = []
    stack: list[int] = []
    for i, ch in enumerate(lower_sentence):
        if ch in "([":
            stack.append(i)
        elif ch in ")]" and stack:
            paren_ranges.append((stack.pop(), i + 1))

    def _inside_parens(pos: int) -> bool:
        return any(ps <= pos < pe for ps, pe in paren_ranges)

    tail_offset = marker.end()
    tail = prefix[tail_offset:]
    for m in re.finditer(r";|\.\s+|\b(?:and|then|but|while)\b", tail):
        if _inside_parens(tail_offset + m.start()):
            continue
        # "and" is a list conjunction when every token that follows it (up to
        # the reference) is a file-path-like token or another "and"/"," list
        # separator.  Split the text after "and" on commas and "and" and check
        # that all non-empty fragments match a file-path pattern.
        if m.group(0).lower() == "and":
            after_and_stripped = tail[m.end() :].strip()
            parts = [
                p.strip().strip("`")
                for p in re.split(r"\s*(?:,|and)\s*", after_and_stripped, flags=re.IGNORECASE)
                if p.strip()
            ]
            if all(re.match(r"^[a-z0-9_.-]+(?:/[a-z0-9_.-]+)*\.[a-z0-9]+$", p, re.IGNORECASE) for p in parts):
                continue
        return False
    return True


def _is_token_bounded_match(text: str, span: tuple[int, int]) -> bool:
    """Return whether *span* is surrounded by non-path-token characters."""
    start, end = span
    if start > 0:
        prev = text[start - 1]
        if prev.isalnum() or prev in "._/-":
            return False
    if end < len(text):
        next_char = text[end]
        if next_char.isalnum() or next_char in "_/-":
            return False
        if next_char == "." and end + 1 < len(text):
            trailing = text[end + 1]
            if trailing.isalnum() or trailing in "_-":
                return False
    return True


def _ordered_reference_spans(sentence: str, target: str) -> list[tuple[int, int]]:
    """Return bounded spans for *target*, preferring backtick-wrapped matches first."""
    plain_pattern = re.compile(re.escape(target), re.IGNORECASE)
    plain_spans = [
        match.span() for match in plain_pattern.finditer(sentence) if _is_token_bounded_match(sentence, match.span())
    ]

    backtick_pattern = re.compile(rf"`\s*({re.escape(target)})\s*`", re.IGNORECASE)
    backtick_spans = [match.span(1) for match in backtick_pattern.finditer(sentence)]
    backtick_positions = {start for start, _ in backtick_spans}
    return backtick_spans + [span for span in plain_spans if span[0] not in backtick_positions]


def _reference_context_bounds_for_occurrence(sentence: str, target: str, occurrence: int) -> tuple[int, int]:
    """Return raw slice bounds for the clause containing the selected occurrence."""
    ordered_spans = _ordered_reference_spans(sentence, target)
    if occurrence >= len(ordered_spans):
        return 0, len(sentence)

    start, end = ordered_spans[occurrence]
    left = 0
    right = len(sentence)

    # Build parenthetical ranges so that conjunctions inside groups like
    # "(e.g. `a.py` and `b.py`)" are treated as list separators, not as
    # action-clause boundaries.
    paren_ranges: list[tuple[int, int]] = []
    stack: list[int] = []
    for i, ch in enumerate(sentence):
        if ch in "([":
            stack.append(i)
        elif ch in ")]" and stack:
            paren_ranges.append((stack.pop(), i + 1))

    def _inside_parens(pos: int) -> bool:
        return any(ps <= pos < pe for ps, pe in paren_ranges)

    # If the target sits inside an illustrative clause ("for example" / "e.g."
    # with no strong boundary between the marker and the target start), bare
    # "and" within that clause is a list separator, not an action-clause
    # boundary.  Track whether such a clause is active so the loop below can
    # skip advancing `left` past an "and" that merely joins list items.
    _ILLUSTRATIVE_MARKER_RE = re.compile(
        r"(?:e\.g\.|for example)(?!\s+generation\b)",
        re.IGNORECASE,
    )
    illustrative_clause_start: int | None = None
    for _m in _ILLUSTRATIVE_MARKER_RE.finditer(sentence):
        if _m.start() >= start:
            break
        intervening = sentence[_m.end() : start]
        if not re.search(r";|\b(?:then|but|while)\b", intervening, re.IGNORECASE):
            illustrative_clause_start = _m.start()

    for boundary in re.finditer(r";|\b(?:and|then|but|while)\b", sentence, re.IGNORECASE):
        if _inside_parens(boundary.start()):
            continue
        if boundary.end() <= start:
            # Within an active illustrative clause "and" is a list separator,
            # not an action-clause boundary; skip it so `left` stays anchored
            # at the marker start and the reference keeps its full context.
            if boundary.group(0).lower() == "and" and illustrative_clause_start is not None:
                continue
            left = boundary.end()
            continue
        if boundary.start() >= end:
            right = boundary.start()
            break
    return left, right


def _reference_context_for_occurrence(sentence: str, target: str, occurrence: int) -> str:
    """Return the clause containing the selected occurrence of *target*."""
    left, right = _reference_context_bounds_for_occurrence(sentence, target, occurrence)
    return sentence[left:right].strip()


def _iter_file_path_references(content: str, *, dedup: bool = True) -> list[Reference]:
    """Return file-path references extracted from *content*.

    Includes file-path references from ``extract_references`` plus Markdown link
    destinations (``[label](path/to/file.ext)``).  When *dedup* is ``True``
    (the default) the list is deduplicated by reference text, preserving first
    occurrence order.  Pass ``dedup=False`` to retain every occurrence so
    callers can aggregate across occurrences (e.g. suppress only when *all*
    occurrences are conditional).
    """
    references: list[Reference] = []
    seen: set[str] = set()
    occurrences: dict[tuple[str, str], int] = {}

    # Strip complete Markdown link spans — ``[label](dest)`` and the backtick
    # variant ``[`label`](dest)`` — before the first extraction pass so that
    # code-formatted link labels are not mistaken for file-path references.
    # The second pass below reads *content* unchanged to collect destinations.
    content_without_links = _MARKDOWN_LINK_DESTINATION_RE.sub("", content)

    for ref in extract_references(content_without_links, dedup=False):
        text = _normalize_reference_text(ref.text)
        if not text:
            continue
        if ref.kind is not ReferenceKind.FILE_PATH and not is_checkable_path_reference(text):
            continue
        key = (ref.plan_location, text.lower())
        occurrence = occurrences.get(key, 0)
        occurrences[key] = occurrence + 1
        raw_left, raw_right = _reference_context_bounds_for_occurrence(ref.context_sentence, text, occurrence)
        raw_slice = ref.context_sentence[raw_left:raw_right]
        sliced = raw_slice.strip()
        ordered_spans = _ordered_reference_spans(ref.context_sentence, text)
        clause_occ = 0
        if occurrence < len(ordered_spans):
            selected_start = ordered_spans[occurrence][0] - (raw_left + len(raw_slice) - len(raw_slice.lstrip()))
            clause_occ = next(
                (
                    idx
                    for idx, (start, _) in enumerate(_ordered_reference_spans(sliced, text))
                    if start == selected_start
                ),
                0,
            )
        references.append(
            Reference(
                text=text,
                kind=ReferenceKind.FILE_PATH,
                plan_location=ref.plan_location,
                context_sentence=sliced,
                occurrence_index=clause_occ,
            )
        )

    for line_num, line in enumerate(content.splitlines(), start=1):
        for match in _MARKDOWN_LINK_DESTINATION_RE.finditer(line):
            text = _normalize_reference_text(match.group(1))
            if "://" in text:
                continue
            if classify_reference_kind(text) is not ReferenceKind.FILE_PATH and not is_checkable_path_reference(text):
                continue
            plan_location = f"L{line_num}"
            key = (plan_location, text.lower())
            occurrence = occurrences.get(key, 0)
            occurrences[key] = occurrence + 1
            # Compute the occurrence index using the actual destination span
            # position so that a backtick in the link label (e.g.
            # ``[`file.py`](file.py)``) does not shift the slice to the wrong
            # clause.  _reference_context_for_occurrence orders spans as
            # backtick-spans first then plain-spans, so we replicate that
            # ordering to find the span that corresponds to the destination.
            stripped_line = line.strip()
            leading_ws = len(line) - len(line.lstrip())
            dest_start = match.start(1) - leading_ws
            _bk_re = re.compile(rf"`\s*({re.escape(text)})\s*`", re.IGNORECASE)
            _pl_re = re.compile(re.escape(text), re.IGNORECASE)
            bk_spans = [_m.span(1) for _m in _bk_re.finditer(stripped_line)]
            bk_starts = {s for s, _ in bk_spans}
            pl_spans = [
                _m.span()
                for _m in _pl_re.finditer(stripped_line)
                if _is_token_bounded_match(stripped_line, _m.span()) and _m.start() not in bk_starts
            ]
            ordered_spans = bk_spans + pl_spans
            dest_occurrence = next((i for i, (s, _) in enumerate(ordered_spans) if s == dest_start), 0)
            raw_left, raw_right = _reference_context_bounds_for_occurrence(stripped_line, text, dest_occurrence)
            raw_slice = stripped_line[raw_left:raw_right]
            sliced = raw_slice.strip()
            selected_start = dest_start - (raw_left + len(raw_slice) - len(raw_slice.lstrip()))
            clause_occ = next(
                (
                    idx
                    for idx, (start, _) in enumerate(_ordered_reference_spans(sliced, text))
                    if start == selected_start
                ),
                0,
            )
            references.append(
                Reference(
                    text=text,
                    kind=ReferenceKind.FILE_PATH,
                    plan_location=plan_location,
                    context_sentence=sliced,
                    occurrence_index=clause_occ,
                )
            )

    # Compute fenced line numbers: code-fence content is already captured by
    # extract_references() in pass 1.  Re-scanning those lines here would bump
    # the shared occurrences counter and push occurrence_index out of range for
    # the sliced clause, causing the illustrative-example guard to return False
    # and report examples inside fences as missing files.
    _FENCE_RE = re.compile(r"```[^\n]*\n(.*?)```", re.DOTALL)
    fenced_lines: set[int] = set()
    for _fm in _FENCE_RE.finditer(content):
        fence_open_line = content[: _fm.start()].count("\n") + 1
        fence_close_line = content[: _fm.end()].count("\n") + 1
        fenced_lines.update(range(fence_open_line + 1, fence_close_line))

    # Third pass: bare path tokens in ordinary prose (not in backticks or
    # Markdown links).  ``extract_references`` only captures backtick-quoted
    # identifiers and code-fence content, so a plain task line like
    # "Update agentic_devtools/cli/runner.py to add the feature" is missed
    # by the first two loops.  The negative lookbehind ``(?<![`:/])`` prevents
    # matching URL path segments (``://…/``) and backtick-prefixed paths
    # (already handled above); ``is_checkable_path_reference`` then rejects
    # templates, globs, absolute paths, and other non-verifiable tokens.
    for line_num, line in enumerate(content.splitlines(), start=1):
        if line_num in fenced_lines:
            continue
        line_without_links = _MARKDOWN_LINK_DESTINATION_RE.sub("", line)
        for match in _BARE_PATH_RE.finditer(line_without_links):
            text = _normalize_reference_text(match.group(1))
            if "/" not in text and _is_hostname_like_root_token(text):
                continue
            if not is_checkable_path_reference(text):
                continue
            plan_location = f"L{line_num}"
            key = (plan_location, text.lower())
            occurrence = occurrences.get(key, 0)
            occurrences[key] = occurrence + 1
            stripped_line = line.strip()
            raw_left, raw_right = _reference_context_bounds_for_occurrence(stripped_line, text, occurrence)
            raw_slice = stripped_line[raw_left:raw_right]
            sliced = raw_slice.strip()
            ordered_spans = _ordered_reference_spans(stripped_line, text)
            clause_occ = 0
            if occurrence < len(ordered_spans):
                selected_start = ordered_spans[occurrence][0] - (raw_left + len(raw_slice) - len(raw_slice.lstrip()))
                clause_occ = next(
                    (
                        idx
                        for idx, (start, _) in enumerate(_ordered_reference_spans(sliced, text))
                        if start == selected_start
                    ),
                    0,
                )
            references.append(
                Reference(
                    text=text,
                    kind=ReferenceKind.FILE_PATH,
                    plan_location=plan_location,
                    context_sentence=sliced,
                    occurrence_index=clause_occ,
                )
            )

    references = _filter_shadowed_basename_references(content, references)
    if not dedup:
        return references

    deduplicated: list[Reference] = []
    for ref in references:
        if ref.text in seen:
            continue
        deduplicated.append(ref)
        seen.add(ref.text)
    return deduplicated


def _filter_shadowed_basename_references(content: str, references: list[Reference]) -> list[Reference]:
    """Drop basename-only references already covered by a same-line full path.

    ``extract_references()`` can emit a shadowed basename such as ``file.md`` for
    ``docs/file.md``. Drop that basename when it appears only as part of the full path, but
    keep it when the source line also contains a standalone reference (for example,
    ``docs/file.md`` and ``file.md``).
    """
    lines = content.splitlines()
    refs_by_location: dict[str, list[Reference]] = {}
    for ref in references:
        refs_by_location.setdefault(ref.plan_location, []).append(ref)

    filtered: list[Reference] = []
    for ref in references:
        if "/" in ref.text:
            filtered.append(ref)
            continue

        match = re.fullmatch(r"L(\d+)", ref.plan_location)
        if match is None:
            filtered.append(ref)
            continue

        line_number = int(match.group(1))
        if not 1 <= line_number <= len(lines):
            filtered.append(ref)
            continue

        line = lines[line_number - 1]
        if _has_standalone_reference_on_line(line, ref.text):
            filtered.append(ref)
            continue

        same_line_refs = refs_by_location.get(ref.plan_location, [])
        if any(
            "/" in other.text and other.text != ref.text and other.text.endswith(ref.text) for other in same_line_refs
        ):
            continue

        filtered.append(ref)

    return filtered


def _has_standalone_reference_on_line(line: str, text: str) -> bool:
    """Return ``True`` when *line* names *text* outside a larger slash path."""
    escaped = re.escape(text)
    if re.search(rf"`{escaped}`", line):
        return True
    if re.search(rf"\[[^\]]*\]\({escaped}(?:\s+\"[^\"]*\")?\)", line):
        return True
    # Strip complete Markdown link spans before the fallback boundary check.
    # Without this, a basename that appears only inside a link label such as
    # ``[README.md](docs/README.md)`` would match the boundary pattern and
    # produce a false-positive standalone reference.
    line_no_links = _MARKDOWN_LINK_DESTINATION_RE.sub("", line)
    return bool(re.search(rf"(?<![/\w.-]){escaped}(?![/\w.-])", line_no_links))


def list_tracked_files(repo_root: Path) -> tuple[str, ...]:
    """Return the repository-relative paths of every tracked file.

    Uses ``git ls-files`` so untracked build output, virtual environments and
    generated state directories never satisfy a reference.  Returns an empty
    tuple when *repo_root* is not a git working tree.
    """
    try:
        completed = subprocess.run(  # noqa: S603 - fixed argv, no shell
            ["git", "-C", str(repo_root), "ls-files", "-z"],
            capture_output=True,
            text=True,
            check=False,
            shell=False,
        )
    except OSError:
        return ()
    if completed.returncode != 0:
        return ()
    return tuple(path for path in completed.stdout.split("\0") if path)


def path_reference_exists(text: str, repo_root: Path, tracked: tuple[str, ...]) -> bool:
    """Return ``True`` when *text* names a file that exists in the repository.

    A reference resolves when it exists relative to *repo_root*, or when it is
    an unambiguous suffix of exactly one tracked path.  The suffix rule accepts the
    shorthand SpecKit plans routinely use — ``cli/runner.py`` for
    ``agentic_devtools/cli/runner.py`` — while still rejecting paths that name
    no file at all or that resolve to multiple tracked files.

    A leading ``.`` is also retried, because the extractor's word-boundary
    lookbehind cannot capture it: ``.github/agdt-config.json`` surfaces as
    ``github/agdt-config.json``.
    """
    for candidate in (text, "." + text):
        if (repo_root / candidate).exists():
            return True
        suffix = "/" + candidate
        matches = [tracked_path for tracked_path in tracked if tracked_path.endswith(suffix)]
        if len(matches) == 1:
            return True
    return False


# ---------------------------------------------------------------------------
# Individual checks
# ---------------------------------------------------------------------------


def check_referenced_paths(
    spec_dir: Path,
    repo_root: Path,
    artifacts: tuple[str, ...],
) -> list[Violation]:
    """Verify that every repository path referenced by *artifacts* exists.

    References whose surrounding sentence expresses creation intent are skipped
    when checking repository files — the plan is allowed to name files it
    intends to add.  Spec-directory artifact references in ``tasks.md`` are
    validated locally under ``spec_dir`` (and must be committable); all other
    spec-directory artifact references are handled by
    :func:`check_advertised_artifacts`.

    ``_iter_file_path_references`` is called with ``dedup=False`` so that every
    occurrence is available for per-occurrence context evaluation.  Once-per-path
    reporting is achieved by grouping occurrences in ``references_by_text`` and
    emitting at most one ``Violation`` per distinct path.
    """
    violations: list[Violation] = []
    tracked = list_tracked_files(repo_root)

    for artifact in artifacts:
        content = _read_text(spec_dir / artifact)
        if content is None:
            continue

        references = _iter_file_path_references(content, dedup=False)
        references_by_text: dict[str, list[Reference]] = {}
        for ref in references:
            references_by_text.setdefault(_normalize_reference_text(ref.text), []).append(ref)

        for occurrences in references_by_text.values():
            if all(_is_illustrative_example_reference(ref) for ref in occurrences):
                continue
            for ref in occurrences:
                normalized_text = _normalize_reference_text(ref.text)
                if not is_checkable_path_reference(normalized_text):
                    continue
                if is_spec_artifact_reference(normalized_text):
                    if artifact != "tasks.md":
                        continue
                    candidate = resolve_spec_artifact_path(spec_dir, normalized_text)
                    if candidate is not None and candidate.is_file() and not is_gitignored(candidate):
                        continue
                    violations.append(
                        Violation(
                            check=CHECK_REFERENCED_PATH,
                            artifact=artifact,
                            detail=(
                                f"{artifact} ({ref.plan_location}) references spec artifact "
                                f"'{ref.text}', which was not produced in {spec_dir.name}."
                            ),
                        )
                    )
                    break
                if is_variable_interpolation(ref) or _has_file_creation_intent(ref):
                    continue
                if _is_illustrative_example_reference(ref):
                    continue
                if path_reference_exists(normalized_text, repo_root, tracked):
                    continue
                violations.append(
                    Violation(
                        check=CHECK_REFERENCED_PATH,
                        artifact=artifact,
                        detail=(
                            f"{artifact} ({ref.plan_location}) references '{ref.text}', "
                            f"which does not exist in the repository and is not "
                            f"described as a file to create."
                        ),
                    )
                )
                break

    return violations


def check_unmapped_test_tasks(
    spec_dir: Path,
    spec_context: Path | None = None,
) -> list[Violation]:
    """Verify that every test task in ``tasks.md`` maps to a requirement.

    Runs the production E.2 pipeline (``validate_test_coverage``) so the
    coverage mapper is reached through the same ``is_test_task()`` filter the
    shipped validator uses; calling the mapper directly would classify
    implementation tasks as test tasks and over-report.

    Args:
        spec_dir: Directory holding the generated planning artifacts.
        spec_context: Optional path to a ``spec.md`` substitute (for example a
            parent spec when ``HIERARCHY_LEVEL=task`` produces no local
            ``spec.md``). When provided, ``spec_context`` is read instead of
            ``spec_dir / "spec.md"``.
    """
    spec_path = spec_context if spec_context is not None else spec_dir / "spec.md"
    spec_content = _read_text(spec_path)
    tasks_content = _read_text(spec_dir / "tasks.md")
    if spec_content is None or tasks_content is None:
        return []

    if not extract_frs(spec_content):
        task_ids = [
            task_id for task_id, description in _parse_tasks_from_content(tasks_content) if is_test_task(description)
        ]
        if not task_ids:
            return []
        return [
            Violation(
                check=CHECK_UNMAPPED_TEST_TASK,
                artifact="tasks.md",
                detail=(
                    f"Test task(s) {', '.join(task_ids)} cannot be traced because "
                    "the specification context defines no FR-NNN entries."
                ),
            )
        ]

    result = validate_test_coverage(spec_content, tasks_content)

    violations: list[Violation] = []
    for finding in result.findings:
        if finding.key != _UNMAPPED_TEST_TASK_KEY:
            continue
        task_list = ", ".join(_TASK_ID_RE.findall(finding.description))
        violations.append(
            Violation(
                check=CHECK_UNMAPPED_TEST_TASK,
                artifact="tasks.md",
                detail=(
                    f"Test task(s) {task_list} lack both an FR-NNN reference and a "
                    f"valid [USn] label, so they cannot be traced to a requirement."
                ),
            )
        )
    return violations


def check_fr_references(
    spec_dir: Path,
    spec_context: Path | None = None,
) -> list[Violation]:
    """Verify that every ``FR-NNN`` used downstream is defined in ``spec.md``.

    Args:
        spec_dir: Directory holding the generated planning artifacts.
        spec_context: Optional path to a ``spec.md`` substitute (for example a
            parent spec when ``HIERARCHY_LEVEL=task`` produces no local
            ``spec.md``). When provided, ``spec_context`` is read instead of
            ``spec_dir / "spec.md"``.
    """
    spec_path = spec_context if spec_context is not None else spec_dir / "spec.md"
    spec_content = _read_text(spec_path)
    if spec_content is None:
        return []

    known = {fr.upper() for fr in extract_frs(spec_content)}

    violations: list[Violation] = []
    for artifact in ("tasks.md", "test-coverage.json"):
        if artifact == "test-coverage.json":
            artifact_path = resolve_generated_artifact(spec_dir, artifact)
        else:
            artifact_path = spec_dir / artifact
        content = _read_text(artifact_path)
        if content is None:
            continue
        unknown = {fr.upper() for fr in extract_frs(content)} - known
        for fr_id in sort_fr_ids(sorted(unknown)):
            violations.append(
                Violation(
                    check=CHECK_FR_REFERENCE,
                    artifact=artifact,
                    detail=(f"{artifact} references {fr_id}, which is not defined in spec.md."),
                )
            )
    return violations


def check_advertised_artifacts(
    spec_dir: Path,
    allowed_named_artifacts: frozenset[str] = SPEC_ARTIFACT_FILENAMES,
    allowed_generated_artifacts: frozenset[str] = RELOCATED_GENERATED_ARTIFACT_FILENAMES,
) -> list[Violation]:
    """Verify that every spec artifact advertised by ``plan.md`` was written.

    ``allowed_named_artifacts`` filters only bare filename artifacts
    (``spec.md``, ``tasks.md``, ...). ``allowed_generated_artifacts`` applies
    the same phase-aware filter to canonical ``generated/<name>`` diagnostics.
    Directory artifacts like ``contracts/openapi.yaml`` are always checked.

    Each distinct artifact text produces at most one violation.  An occurrence
    is suppressed when it is conditional (annotated "Optional — only when …")
    or negated ("No … artifact is committed").  The check fires when at least
    one occurrence is neither conditional nor negated — i.e. an unconditional
    promise.  Consequently a negation followed by an unconditional promise still
    triggers the gate, and an optional-tree mention followed by a body-text
    promise also still triggers it regardless of which appeared first.
    """
    content = _read_text(spec_dir / "plan.md")
    if content is None:
        return []

    # Collect every occurrence (including duplicates) so we can aggregate
    # conditional and negation status across all mentions of the same text.
    refs_by_text: dict[str, list[Reference]] = {}
    for ref in _iter_file_path_references(content, dedup=False):
        text = _normalize_reference_text(ref.text)
        if not is_spec_artifact_reference(text):
            continue
        refs_by_text.setdefault(text, []).append(ref)

    violations: list[Violation] = []
    for text, occurrences in refs_by_text.items():
        # Suppress only when *every* occurrence is conditional or negated.
        # A single occurrence that is neither conditional nor negated is an
        # unconditional promise — even if other occurrences negate or qualify it.
        if all(_is_conditional_artifact_reference(ref) or _is_negated_artifact_reference(ref) for ref in occurrences):
            continue
        is_named_artifact = text in SPEC_ARTIFACT_FILENAMES
        if not is_named_artifact:
            # Canonical ``generated/<name>`` path — derive the bare name so the
            # phase filter applies to relocated diagnostics as well.
            # Only ``RELOCATED_GENERATED_ARTIFACT_FILENAMES`` are valid here;
            # other ``generated/<name>`` paths are not treated as spec artifacts.
            _prefix = f"{GENERATED_ARTIFACT_SUBDIR}/"
            if text.startswith(_prefix):
                _bare = text[len(_prefix) :]
                is_named_artifact = _bare in RELOCATED_GENERATED_ARTIFACT_FILENAMES
                if is_named_artifact and _bare not in allowed_generated_artifacts:
                    continue
        elif text not in allowed_named_artifacts:
            continue
        candidate = resolve_spec_artifact_path(spec_dir, text)
        if candidate is not None and candidate.is_file() and not is_gitignored(candidate):
            continue
        # Prefer the first unconditional, non-negated occurrence for the violation location.
        ref = next(
            (
                r
                for r in occurrences
                if not _is_conditional_artifact_reference(r) and not _is_negated_artifact_reference(r)
            ),
            occurrences[0],
        )
        violations.append(
            Violation(
                check=CHECK_ADVERTISED_ARTIFACT,
                artifact="plan.md",
                detail=(
                    f"plan.md ({ref.plan_location}) advertises the artifact "
                    f"'{text}', which was not produced in {spec_dir.name}."
                ),
            )
        )
    return violations


def check_checklists(spec_dir: Path) -> list[Violation]:
    """Verify that every generated checklist contains real checkbox items."""
    checklist_dir = spec_dir / "checklists"
    if not checklist_dir.is_dir():
        return []

    paths = sorted(str(p) for p in checklist_dir.glob("*.md") if p.is_file())
    if not paths:
        return []

    result = validate_checklists(paths)

    violations: list[Violation] = []
    for file_result in result.files:
        if file_result.classification.value == "valid":
            continue
        relative = os.path.relpath(file_result.path, str(spec_dir))
        violations.append(
            Violation(
                check=CHECK_CHECKLIST,
                artifact=relative.replace(os.sep, "/"),
                detail=file_result.explanation,
            )
        )
    return violations


# ---------------------------------------------------------------------------
# Orchestrator
# ---------------------------------------------------------------------------


def resolve_checks(phase: int | None) -> list[str]:
    """Return the check identifiers enabled for *phase*.

    ``None`` enables every check.  An unknown phase number also enables every
    check, so a future pipeline phase fails closed rather than silently
    verifying nothing.
    """
    if phase is None or phase not in PHASE_CHECKS:
        return list(ALL_CHECKS)
    return list(PHASE_CHECKS[phase])


def verify_artifacts(
    spec_dir: Path,
    repo_root: Path,
    phase: int | None = None,
    spec_context: Path | None = None,
) -> VerificationResult:
    """Run the pre-PR verification gate over *spec_dir*.

    Args:
        spec_dir: Directory holding the generated planning artifacts.
        repo_root: Repository root that referenced paths are resolved against.
        phase: Optional generation-step scope used to restrict enabled checks.
            This is keyed by ``PHASE_CHECKS`` (steps ``1``..``5`` from
            ``generate-spec-from-issue.sh``), not by external pipeline phases.
            Pipeline phase 3 merges steps 3/4/5 and should usually be verified
            unscoped so cross-step artifacts are validated together.
        spec_context: Optional path to a ``spec.md`` substitute.  Supply the
            parent feature's ``spec.md`` here when ``HIERARCHY_LEVEL=task`` so
            that ``check_unmapped_test_tasks`` and ``check_fr_references`` can
            resolve FR-NNN identifiers even though no local ``spec.md`` exists.

    Returns:
        A :class:`VerificationResult` listing every violation found.
    """
    checks = resolve_checks(phase)

    path_artifacts: tuple[str, ...] = ("plan.md", "tasks.md")
    if phase is not None:
        path_artifacts = _PATH_REFERENCE_SOURCES.get(phase, path_artifacts)

    spec_required_checks = tuple(check for check in (CHECK_UNMAPPED_TEST_TASK, CHECK_FR_REFERENCE) if check in checks)
    if spec_required_checks and (spec_dir / "tasks.md").is_file():
        spec_path = spec_context if spec_context is not None else spec_dir / "spec.md"
        if not spec_path.is_file():
            checks_text = ", ".join(spec_required_checks)
            if spec_context is None:
                raise ValueError(
                    "tasks.md exists but no specification context is available for "
                    f"{checks_text}. Provide spec.md or --spec-context."
                )
            raise ValueError(
                f"tasks.md exists but the provided spec-context path does not exist for {checks_text}: {spec_path}"
            )

    violations: list[Violation] = []
    if CHECK_REFERENCED_PATH in checks:
        violations.extend(check_referenced_paths(spec_dir, repo_root, path_artifacts))
    if CHECK_UNMAPPED_TEST_TASK in checks:
        violations.extend(check_unmapped_test_tasks(spec_dir, spec_context=spec_context))
    if CHECK_FR_REFERENCE in checks:
        violations.extend(check_fr_references(spec_dir, spec_context=spec_context))
    if CHECK_ADVERTISED_ARTIFACT in checks:
        advertised_filenames = _PHASE3_ADVERTISED_ARTIFACT_FILENAMES if phase == 3 else SPEC_ARTIFACT_FILENAMES
        advertised_generated_filenames = (
            _PHASE3_ADVERTISED_GENERATED_ARTIFACT_FILENAMES if phase == 3 else RELOCATED_GENERATED_ARTIFACT_FILENAMES
        )
        violations.extend(
            check_advertised_artifacts(
                spec_dir,
                allowed_named_artifacts=advertised_filenames,
                allowed_generated_artifacts=advertised_generated_filenames,
            )
        )
    if CHECK_CHECKLIST in checks:
        violations.extend(check_checklists(spec_dir))

    return VerificationResult(violations=violations, checks_run=checks)


def render_violations(result: VerificationResult) -> str:
    """Render *result* as a human-readable, markdown-compatible summary."""
    lines = ["## SpecKit Artifact Verification", ""]
    if not result.checks_run:
        lines.append("No checks apply to this phase — nothing to verify.")
        return "\n".join(lines)

    lines.append(f"Checks run: {', '.join(result.checks_run)}")
    lines.append("")

    if result.passed:
        lines.append("Result: PASS — all checks passed.")
        return "\n".join(lines)

    lines.append(f"Result: FAIL — {len(result.violations)} violation(s):")
    lines.append("")
    for violation in result.violations:
        lines.append(f"- [{violation.check}] {violation.artifact}: {violation.detail}")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------


def verify_artifacts_command(argv: list[str] | None = None) -> None:
    """CLI entry point for ``agdt-speckit-verify-artifacts``.

    Exit codes: ``0`` all checks passed, ``1`` violations found, ``2``
    operational error (for example a missing spec directory).
    """
    parser = argparse.ArgumentParser(
        prog="agdt-speckit-verify-artifacts",
        description=("Verify generated SpecKit artifacts before a pull request is opened."),
    )
    parser.add_argument(
        "--spec-dir",
        required=True,
        help="Path to the spec directory holding the generated artifacts",
    )
    parser.add_argument(
        "--repo-root",
        default=".",
        help="Repository root that referenced paths are resolved against (default: .)",
    )
    parser.add_argument(
        "--phase",
        type=int,
        default=None,
        help=(
            "Optional generation-step scope (PHASE_CHECKS keys from "
            "generate-spec-from-issue.sh). For merged pipeline phase 3, prefer "
            "an unscoped run (omit --phase) so steps 3/4/5 are validated together."
        ),
    )
    parser.add_argument(
        "--spec-context",
        default=None,
        help=(
            "Path to a spec.md substitute used by the FR and test-task checks. "
            "Supply the parent feature's spec.md when HIERARCHY_LEVEL=task so that "
            "FR-NNN identifiers can be resolved even though no local spec.md exists."
        ),
    )
    parser.add_argument(
        "--json",
        dest="json_output",
        action="store_true",
        default=False,
        help="Emit the violation list as JSON on stdout",
    )

    args = parser.parse_args(argv)

    spec_dir = Path(args.spec_dir)
    if not spec_dir.is_dir():
        print(f"Error: spec directory '{spec_dir}' not found.", file=sys.stderr)
        raise SystemExit(2)

    repo_root = Path(args.repo_root).resolve()

    spec_context: Path | None = None
    if args.spec_context is not None:
        spec_context = Path(args.spec_context)
        if not spec_context.is_file():
            print(f"Error: spec-context file '{spec_context}' not found.", file=sys.stderr)
            raise SystemExit(2)

    try:
        result = verify_artifacts(spec_dir, repo_root, args.phase, spec_context=spec_context)
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(2) from exc

    if args.json_output:
        print(json.dumps(result.to_json(), indent=2))
    else:
        print(render_violations(result))

    raise SystemExit(0 if result.passed else 1)
