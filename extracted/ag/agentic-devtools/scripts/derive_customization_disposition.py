#!/usr/bin/env python3
"""Derive the disposition and slug map for every injected customization file (#3758).

Seven later issues each need to know which legacy file becomes which skill, under
which name, and which is deleted outright.  Re-deriving that per issue guarantees
they disagree, and the re-slug from ``agdt.x.y`` to ``agdt-x-y`` has to be decided
identically everywhere or names collide.  This script derives the answer once, from
the files on disk, and publishes it as
``docs/agent-customization/disposition-and-slug-map.md``.

The derivation applies the five form-selection tests T0-T4 of
``docs/agent-customization/authoring-standard.md`` in order, plus four rules the
standard implies but does not mechanise (family merge, collapse, residue deletion,
and the verbose-output limb of T4).  Every one of those four is a named constant
below carrying its own reason, so a reader can audit the judgement instead of
reverse-engineering it from the output.

Three modes:

``derive`` (default)
    Recompute the table and write it to the published path (or to ``--out``).
    Use ``--check`` to fail when the published table is stale.

``--verify-partition``
    Re-run the partition assertion against the *published* table rather than
    against a fresh derivation, so a later issue can prove the three retirement
    batches still partition the rows without trusting this script's own output.

``--verify-authored``
    Compare the table's surviving target slugs against what has actually been
    authored under the skill and subagent roots, and report both directions of
    the difference.

Usage:
    python scripts/derive_customization_disposition.py
    python scripts/derive_customization_disposition.py --check
    python scripts/derive_customization_disposition.py --verify-partition
    python scripts/derive_customization_disposition.py --verify-authored

All modes are offline and deterministic.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tomllib
from collections import Counter, defaultdict
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from pathlib import Path, PurePosixPath

REPO_ROOT = Path(__file__).resolve().parents[1]

AGENTS_DIR = ".github/agents"
PROMPTS_DIR = ".github/prompts"

#: The two manifests are not units; they index the directory they sit in.
MANIFEST_NAME = "agdt.README.md"

PUBLISHED_PATH = "docs/agent-customization/disposition-and-slug-map.md"

PROMPT_SUBAGENT_TO_SKILL_RECLASSIFICATIONS = {
    ".github/prompts/agdt.suppressed-comment-triage.evaluate.prompt.md": (
        "`agdt.suppressed-comment-triage.evaluate` now counts as a skill rather than as the prior prompt-side subagent."
    ),
}

#: Root ``--verify-authored`` scans for an authored skill - an ``agdt-*`` directory
#: holding a ``SKILL.md``.  Only the re-slugged ``agdt-*`` form counts; non-``agdt``
#: skills already present in the repository (e.g. ``run-targeted-checks``) are outside
#: the migration namespace and must not be treated as unexpected orphans.
#: ``.agents/skills/<name>/SKILL.md`` is the only supported skill root (see
#: ``.agents/skills/README.md:28``); ``.github/skills`` is not read by any runtime.
AUTHORED_SKILL_ROOTS = (".agents/skills",)

#: Root ``--verify-authored`` scans for an authored subagent.  Repository-authored
#: re-slugged subagents live alongside the legacy dot-named corpus under
#: ``.github/agents``, so only ``agdt-*.agent.md`` matches count here: the legacy
#: ``agdt.*.agent.md`` files remain the input to this table, and the repository's
#: non-``agdt`` agents are outside the migration namespace.
AUTHORED_AGENT_ROOTS = (".github/agents",)

DISPOSITIONS = ("delete", "merge", "skill", "subagent", "collapse")

GROUPS = (
    "work-on-jira-issue",
    "pull-request-review",
    "ai-pr-loop-supervisor",
    "review-response",
    "git-and-pr",
    "analysis-and-fork",
    "singleton-a",
    "singleton-b",
)

BATCHES = ("stubs", "wrappers", "residue")

EXPECTED_KIND_BY_DISPOSITION: dict[str, str] = {
    "merge": "skill",
    "skill": "skill",
    "subagent": "subagent",
}

#: Number of standalone procedure skills that fall in ``singleton-a``; the rest
#: fall in ``singleton-b``.  Alphabetical by legacy slug, as the group names say.
SINGLETON_A_SIZE = 6

#: T0's parenthetical proxy: "an ``## Actions`` section of four non-blank lines or
#: fewer".  Four is the length of the canonical wrapper shape - the numbered step,
#: the opening fence, the command, the closing fence - so fence delimiters count.
T0_MAX_ACTION_LINES = 4

#: T1's threshold: "the body is under 40 lines".
T1_MAX_BODY_LINES = 40

#: T3's threshold: "two or more numbered steps, or two or more distinct commands".
T3_MIN_STEPS = 2

#: A skill ``name`` must match this and be at most 64 characters (standard §4).
TARGET_SLUG_RE = re.compile(r"^[a-z0-9](-?[a-z0-9])*$")
TARGET_SLUG_MAX_LEN = 64

#: Slug prefixes whose members merge into one skill named after the family.
MERGE_FAMILIES = ("agdt.work-on-jira-issue", "agdt.pull-request-review", "agdt.ai-pr-loop-supervisor")

#: Units deleted for a reason other than T0.  T0 is a mechanical test; these three
#: are judgements, so each records why.  The script asserts none of them fires T0 -
#: a unit that fires T0 belongs to the wrapper batch, not here.
RESIDUE_DELETIONS = {
    "agdt.advance-workflow": (
        "Entry-point wrapper whose only addition over `agdt-advance-workflow` is a "
        "retry-and-diagnose loop. Standard §11: determinism belongs in code, so the "
        "retry belongs in the command, not in a customization file."
    ),
    "agdt.fix-workflow": (
        "Maintainer-facing procedure for repairing this repository's own workflow "
        "commands. It is injected into every consumer repository, where it can never "
        "apply, so it is deleted rather than re-published as a skill."
    ),
    "agdt.test-workflow": (
        "Maintainer-facing procedure for exercising and auditing this repository's own "
        "workflow commands. Same reason as `agdt.fix-workflow`: no consumer repository "
        "can act on it."
    ),
}

#: T4 has two limbs: the unit is dispatched by another unit **and** its output is
#: verbose intermediate work the parent does not need in full.  Dispatch is derived
#: mechanically (:func:`dispatched_slugs`); the verbosity limb is a judgement, so
#: every unit that satisfies it is listed here with its reason.  The script asserts
#: this mapping is a subset of the mechanically-derived dispatch set, so it can
#: narrow T4 but never invent a subagent.
T4_VERBOSE_OUTPUT = {
    "agdt.pull-request-review.orchestrator": (
        "Spawns one reviewer per file and every rubber duck; the parent needs the synthesis, not the per-file traffic."
    ),
    "agdt.pull-request-review.file-reviewer": (
        "Reads one whole file and returns a draft answer; the draft, not the reading, "
        "is what the orchestrator integrates."
    ),
    "agdt.pull-request-review.rubber-duck": (
        "Critiques one draft and returns a single verdict; the critique transcript is intermediate work."
    ),
    "agdt.pr-merge-execute": (
        "Retries and works around merge failures; the merge manager needs the outcome, not the attempt log."
    ),
    "agdt.review-feedback-audit.evaluate": (
        "Consumes a whole batch of review data and returns targeted instruction edits."
    ),
}

#: Family membership for units whose group is not implied by a slug prefix.  Group
#: names are fixed by #3758 because eight later issues select rows by them.
EXPLICIT_GROUPS = {
    "agdt.address-copilot-review": "review-response",
    "agdt.address-copilot-review.ci-repair": "review-response",
    "agdt.address-copilot-review.evaluate-and-respond": "review-response",
    "agdt.address-own-review-feedback": "review-response",
    "agdt.address-pr-review-comments": "review-response",
    "agdt.phase0-reviewing-agent": "review-response",
    "agdt.review-feedback-audit.evaluate": "review-response",
    "agdt.pr-merge-manager": "git-and-pr",
    "agdt.pr-merge-execute": "git-and-pr",
    "agdt.resolve-merge-conflicts": "git-and-pr",
    "agdt.resolve-merge-conflicts.cloud-agent": "git-and-pr",
    "agdt.resolve-thread": "git-and-pr",
    "agdt.squash-commits": "git-and-pr",
    "agdt.analyze-workflow": "analysis-and-fork",
    "agdt.create-issues-from-analysis": "analysis-and-fork",
    "agdt.suppressed-comment-triage.evaluate": "analysis-and-fork",
}

#: Phrases in a unit's own body that declare it is dispatched by another unit.
_DISPATCH_PHRASES = (
    r"\bspawned by\b",
    r"\bdispatched by\b",
    r"\breturn control to\b",
    r"\bhanded to you by\b",
    r"\bone-shot subagent\b",
    r"\byou were assigned\b",
    r"\bnarrowly-scoped agent\b",
    r"\bpre-structured files\b",
)
_DISPATCH_RE = re.compile("|".join(_DISPATCH_PHRASES), re.IGNORECASE)

#: ``handoffs:`` entries name their target with an ``agent:`` key.
_HANDOFF_RE = re.compile(r"^\s*(?:-\s*)?agent:\s*[\"']?(agdt\.[\w.-]+)[\"']?\s*$", re.MULTILINE)

#: A fenced block opener, e.g. ```` ```bash ````, capturing its info string.
_FENCE_RE = re.compile(r"^\s*```+\s*(\w*)")

#: Info strings whose fenced block holds commands rather than sample output.
SHELL_LANGUAGES = frozenset({"bash", "sh", "shell", "zsh", "console", "powershell", "pwsh"})

#: An inline ``code`` span.
_INLINE_CODE_RE = re.compile(r"`([^`\n]+)`")

#: An ``agdt-*`` command name.
_AGDT_COMMAND_RE = re.compile(r"agdt-[a-z0-9-]+")

#: A numbered step, e.g. ``1. Run the command:``.
_NUMBERED_STEP_RE = re.compile(r"^\s*\d+\.\s+\S")

#: A wildcard path-like token.
#:
#: This pattern is intentionally applied only to strings already extracted from
#: inline-code spans via ``_INLINE_CODE_RE.findall(...)``.
_GLOB_TOKEN_RE = re.compile(r"(?<![A-Za-z0-9_.\-/])(/?[A-Za-z0-9_.\-/]*\*+[A-Za-z0-9_.\-/\*]*)(?![A-Za-z0-9_.\-/])")

#: Provider names whose presence disqualifies T1.
_PROVIDER_RE = re.compile(r"\b(jira|azure devops|azure-devops|github|gitlab)\b", re.IGNORECASE)

_WORKFLOW_RE = re.compile(r"\bworkflow\b", re.IGNORECASE)


# --------------------------------------------------------------------------------------
# File parsing
# --------------------------------------------------------------------------------------


def split_frontmatter(text: str) -> tuple[str, str]:
    """Split a customization file into its YAML frontmatter and its body.

    Args:
        text: Full file text.

    Returns:
        A ``(frontmatter, body)`` pair. The frontmatter is empty when the file
        carries none; the body is then the whole file.
    """
    if not text.startswith("---"):
        return "", text
    parts = text.split("---", 2)
    if len(parts) != 3:
        return "", text
    return parts[1], parts[2]


def section(body: str, name: str) -> str | None:
    """Return the text of the ``## <name>`` section of *body*, or ``None``.

    Args:
        body: Unit body, frontmatter already removed.
        name: Section heading text, without the ``##`` marker.

    Returns:
        Everything between the heading and the next ``##`` heading, or ``None``
        when the section is absent.
    """
    match = re.search(rf"^## {re.escape(name)}\s*$(.*?)(?=^## |\Z)", body, re.MULTILINE | re.DOTALL)
    return match.group(1) if match else None


def count_non_blank(text: str) -> int:
    """Count the non-blank lines of *text*, fence delimiters included."""
    return sum(1 for line in text.splitlines() if line.strip())


def fenced_commands(text: str) -> list[str]:
    """Return the first token of every command line inside shell code blocks.

    Only blocks whose info string names a shell are read, because a ``text`` block
    holds sample output — ``Background task started: task-abc123`` is not a command
    the unit runs, and counting it as one would make every wrapper that shows its
    own output look as though it reached for a second tool.

    Args:
        text: Markdown containing zero or more fenced code blocks.

    Returns:
        One command name per command line, in order, with duplicates kept.
    """
    commands: list[str] = []
    language: str | None = None
    for line in text.splitlines():
        fence = _FENCE_RE.match(line)
        if fence:
            language = None if language is not None else fence.group(1).lower()
            continue
        if language not in SHELL_LANGUAGES:
            continue
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        commands.append(stripped.split()[0])
    return commands


def named_commands(text: str) -> set[str]:
    """Return the distinct commands *text* names - T3's second metric.

    A command is named either by a line inside a shell code block or by an inline
    ``code`` span holding an ``agdt-*`` invocation. Prerequisite sections state
    their setup commands inline rather than in a fenced block, and a procedure that
    tells the reader to run ``agdt-set jira.issue_key <KEY>`` before running the
    workflow command is naming two commands, not one.

    Args:
        text: Markdown body.

    Returns:
        The distinct command names.
    """
    commands = set(fenced_commands(text))
    for span in _INLINE_CODE_RE.findall(text):
        token = span.strip().split()[0] if span.strip() else ""
        if _AGDT_COMMAND_RE.fullmatch(token):
            commands.add(token)
    return commands


def count_numbered_steps(body: str) -> int:
    """Count top-level numbered steps in *body*, ignoring fenced code blocks."""
    count = 0
    in_fence = False
    for line in body.splitlines():
        if _FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if not in_fence and _NUMBERED_STEP_RE.match(line):
            count += 1
    return count


def path_globs(body: str) -> list[str]:
    """Return the backticked path globs named in *body*.

    A glob is a backticked token containing ``*`` together with a path separator
    or a file extension, which excludes Markdown emphasis and shell wildcards.

    Args:
        body: Unit body.

    Returns:
        The glob strings, in order of appearance.
    """
    globs = []
    for span in _INLINE_CODE_RE.findall(body):
        for candidate in _GLOB_TOKEN_RE.findall(span):
            if "/" in candidate or re.search(r"\*\.\w+$", candidate):
                globs.append(candidate)
    return globs


def tracked_files(repo_root: Path) -> frozenset[str]:
    """Return the relative POSIX paths of every file tracked by git.

    Args:
        repo_root: Repository root to run ``git ls-files`` in.

    Returns:
        A frozenset of relative POSIX paths.

    Raises:
        RuntimeError: When ``git ls-files`` is unavailable or fails.  The
            derivation must not continue with an empty tracked-file set, as
            that would silently suppress every T2 check and produce an
            environment-dependent, non-reproducible output.
    """
    try:
        result = subprocess.run(
            ["git", "ls-files"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=True,
            shell=False,
        )
        return frozenset(result.stdout.splitlines())
    except (subprocess.CalledProcessError, OSError) as exc:
        raise RuntimeError(
            f"git ls-files failed in {repo_root}; cannot derive T2 classifications without the tracked-file list"
        ) from exc


def glob_matches_tracked_file(glob: str, repo_root: Path, tracked: frozenset[str]) -> bool:
    """Return whether *glob* matches at least one tracked file under *repo_root*.

    Args:
        glob: A path glob pattern, optionally prefixed with ``/``.
        repo_root: Repository root used to expand the glob.
        tracked: The set of relative POSIX paths tracked by git.

    Returns:
        ``True`` when at least one tracked file matches the pattern.
    """
    pattern = glob.strip().lstrip("/")
    if not pattern:
        return False
    try:
        for path in repo_root.glob(pattern):
            try:
                rel = path.relative_to(repo_root).as_posix()
            except ValueError:
                continue
            if rel in tracked:
                return True
        # ``Path.glob`` only sees files present in the working tree.  T2 is defined
        # against tracked paths, so also match tracked entries that are currently
        # absent on disk (e.g. sparse checkout or local deletion).
        for tracked_path in tracked:
            if (repo_root / tracked_path).exists():
                continue
            if _tracked_path_matches_glob(tracked_path, pattern):
                return True
        return False
    except (ValueError, NotImplementedError, OSError):
        return False


def _tracked_path_matches_glob(path: str, pattern: str) -> bool:
    """Return whether tracked *path* matches *pattern* without filesystem access.

    Uses root-relative (left-anchored) matching to mirror how
    ``repo_root.glob(pattern)`` selects paths.  ``PurePosixPath.match()``
    right-anchors relative patterns, so ``nested/src/module.py`` would
    incorrectly satisfy ``src/*.py``; prefixing both sides with ``/`` forces
    absolute (left-anchored) semantics.
    """
    pure = PurePosixPath("/" + path)
    return any(pure.match("/" + candidate) for candidate in _glob_pattern_variants(pattern))


def _glob_pattern_variants(pattern: str) -> frozenset[str]:
    """Return match variants where ``**/`` may consume zero directory segments."""
    variants = {pattern}
    if "**/" in pattern:
        variants.update(_glob_pattern_variants(pattern.replace("**/", "", 1)))
    return frozenset(variants)


def is_registration_stub(frontmatter: str, body: str) -> bool:
    """Return whether a file is a pointer stub with no body of its own.

    A registration stub exists only to register a name: its frontmatter points at
    another unit with ``agent:`` and its body is empty.

    Args:
        frontmatter: The file's YAML frontmatter.
        body: The file's body.

    Returns:
        ``True`` when the file carries an ``agent:`` pointer and no body content.
    """
    if body.strip():
        return False
    return bool(re.search(r"^\s*agent:\s*\S", frontmatter, re.MULTILINE))


# --------------------------------------------------------------------------------------
# Slugs
# --------------------------------------------------------------------------------------


def entry_point_slugs(pyproject: Path) -> frozenset[str]:
    """Return the ``agdt-*`` console-script names declared in ``[project.scripts]``."""
    data = tomllib.loads(pyproject.read_text(encoding="utf-8"))
    scripts = data.get("project", {}).get("scripts", {})
    return frozenset(name for name in scripts if name.startswith("agdt-"))


def to_target_slug(slug: str) -> str:
    """Re-slug ``agdt.x.y`` to ``agdt-x-y`` and validate the result.

    Args:
        slug: Legacy slug, e.g. ``agdt.work-on-jira-issue.setup``.

    Returns:
        The portable skill name, e.g. ``agdt-work-on-jira-issue-setup``.

    Raises:
        ValueError: The result is longer than 64 characters or contains a
            character that is illegal in a skill name. A skill whose name is
            illegal fails to load silently, so this must fail loudly here.
    """
    target = slug.replace(".", "-").lower()
    if len(target) > TARGET_SLUG_MAX_LEN:
        raise ValueError(f"target slug {target!r} exceeds {TARGET_SLUG_MAX_LEN} characters")
    if not TARGET_SLUG_RE.fullmatch(target):
        raise ValueError(f"target slug {target!r} does not match {TARGET_SLUG_RE.pattern}")
    return target


# --------------------------------------------------------------------------------------
# Units
# --------------------------------------------------------------------------------------


@dataclass(frozen=True)
class Unit:
    """One injected customization file and the metrics T0-T4 read."""

    path: str
    slug: str
    kind: str
    frontmatter: str
    body: str

    @property
    def is_prompt(self) -> bool:
        """Whether the unit lives under ``.github/prompts/``."""
        return self.kind == "prompt"

    @property
    def body_lines(self) -> int:
        """Non-blank body lines, frontmatter excluded."""
        return count_non_blank(self.body)

    @property
    def total_body_lines(self) -> int:
        """Physical body lines (including blank), frontmatter excluded."""
        return len(self.body.splitlines())

    @property
    def actions(self) -> str | None:
        """The unit's ``## Actions`` section, or ``None`` when it has none."""
        return section(self.body, "Actions")

    @property
    def action_lines(self) -> int:
        """Non-blank lines of the ``## Actions`` section (0 when absent)."""
        actions = self.actions
        return 0 if actions is None else count_non_blank(actions)

    @property
    def action_commands(self) -> list[str]:
        """Command names invoked inside the ``## Actions`` section."""
        actions = self.actions
        return [] if actions is None else fenced_commands(actions)

    @property
    def distinct_commands(self) -> int:
        """Number of distinct commands the whole body names."""
        return len(named_commands(self.body))

    @property
    def numbered_steps(self) -> int:
        """Number of numbered steps in the whole body."""
        return count_numbered_steps(self.body)


def load_units(repo_root: Path) -> list[Unit]:
    """Load every ``agdt.*`` agent and prompt unit, excluding the two manifests.

    Args:
        repo_root: Repository root.

    Returns:
        Units sorted by path, agents before prompts.
    """
    units: list[Unit] = []
    for directory, suffix, kind in (
        (AGENTS_DIR, ".agent.md", "agent"),
        (PROMPTS_DIR, ".prompt.md", "prompt"),
    ):
        for path in sorted((repo_root / directory).glob(f"agdt.*{suffix}")):
            if path.name == MANIFEST_NAME:
                continue
            text = path.read_text(encoding="utf-8")
            frontmatter, body = split_frontmatter(text)
            units.append(
                Unit(
                    path=f"{directory}/{path.name}",
                    slug=path.name[: -len(suffix)],
                    kind=kind,
                    frontmatter=frontmatter,
                    body=body,
                )
            )
    return units


def dispatched_slugs(units: Sequence[Unit]) -> frozenset[str]:
    """Return the slugs of units another unit dispatches - T4's first limb.

    Dispatch is read two ways, both mechanical: a ``handoffs:`` entry in another
    unit's frontmatter that names this unit, and a declaration in the unit's own
    body that it was spawned, dispatched or handed its inputs by a parent.

    Args:
        units: Every loaded unit.

    Returns:
        The dispatched slugs.
    """
    known = {unit.slug for unit in units}
    dispatched: set[str] = set()
    for unit in units:
        for target in _HANDOFF_RE.findall(unit.frontmatter):
            if target in known and target != unit.slug:
                dispatched.add(target)
        if _DISPATCH_RE.search(unit.body):
            dispatched.add(unit.slug)
    return frozenset(dispatched)


# --------------------------------------------------------------------------------------
# Form selection
# --------------------------------------------------------------------------------------


def fires_t0(unit: Unit, entry_points: frozenset[str]) -> bool:
    """Return whether T0 fires: an entry-point wrapper whose body adds nothing.

    T0's operative test is that the body adds nothing to what the command already
    does. The standard operationalises it as an ``## Actions`` section of four
    non-blank lines or fewer - the canonical wrapper shape. That proxy misses the
    wrappers that spell out a second flag or a follow-up ``agdt-*`` call, so a
    second limb is applied: a body whose ``## Actions`` section invokes nothing
    but ``agdt-*`` commands introduces no capability the commands do not already
    have. A body reaching for any other tool does add something and fails T0.

    Args:
        unit: The unit under test.
        entry_points: ``agdt-*`` console-script names from ``[project.scripts]``.

    Returns:
        ``True`` when the unit is a wrapper to delete.
    """
    if unit.slug.replace(".", "-") not in entry_points:
        return False
    if unit.action_lines <= T0_MAX_ACTION_LINES:
        return True
    commands = unit.action_commands
    return bool(commands) and all(command.startswith("agdt-") for command in commands)


def fires_t1(unit: Unit) -> bool:
    """Return whether T1 fires: a short body naming no glob, workflow or provider."""
    if unit.total_body_lines >= T1_MAX_BODY_LINES:
        return False
    if path_globs(unit.body):
        return False
    return not (_WORKFLOW_RE.search(unit.body) or _PROVIDER_RE.search(unit.body))


def fires_t2(unit: Unit, repo_root: Path, tracked: frozenset[str]) -> bool:
    """Return whether T2 fires: the body names a glob matching a tracked file."""
    return any(glob_matches_tracked_file(glob, repo_root, tracked) for glob in path_globs(unit.body))


def fires_t3(unit: Unit) -> bool:
    """Return whether T3 fires: the body is an ordered procedure."""
    return unit.numbered_steps >= T3_MIN_STEPS or unit.distinct_commands >= T3_MIN_STEPS


def merge_family(slug: str) -> str | None:
    """Return the merge family a slug belongs to, or ``None``.

    Args:
        slug: Legacy slug.

    Returns:
        The family slug (e.g. ``agdt.work-on-jira-issue``) when the unit is a step
        of a merged workflow-step family, otherwise ``None``.
    """
    for family in MERGE_FAMILIES:
        if slug.startswith(f"{family}."):
            return family
    return None


# --------------------------------------------------------------------------------------
# Rows
# --------------------------------------------------------------------------------------


@dataclass(frozen=True)
class Row:
    """One published row: what happens to one legacy file."""

    path: str
    slug: str
    disposition: str
    group: str
    target: str
    batch: str
    reason: str


def _batch(disposition: str, unit: Unit, is_stub: bool, t0: bool) -> str:
    """Return the retirement batch, applying #3758's three rules in order.

    The third rule is a complement, not a third filter: three independent filters
    over five dispositions leave gaps, and a gap is a file no issue deletes while a
    later acceptance criterion asserts none survives.

    Args:
        disposition: The row's disposition.
        unit: The unit the row describes.
        is_stub: Whether the file is a registration stub.
        t0: Whether T0 fired for the file.

    Returns:
        One of ``stubs``, ``wrappers``, ``residue``.
    """
    if disposition == "delete" and unit.is_prompt and is_stub:
        return "stubs"
    if disposition == "delete" and not unit.is_prompt and t0:
        return "wrappers"
    return "residue"


def _group_for(slug: str, skill_singletons: Sequence[str]) -> str:
    """Return the group name for a surviving unit."""
    family = merge_family(slug)
    if family is not None:
        return family.removeprefix("agdt.")
    explicit = EXPLICIT_GROUPS.get(slug)
    if explicit is not None:
        return explicit
    index = skill_singletons.index(slug)
    return "singleton-a" if index < SINGLETON_A_SIZE else "singleton-b"


def derive_rows(repo_root: Path) -> list[Row]:
    """Derive one row per injected customization file.

    The rules are applied in order and the first match fixes the row, exactly as
    the authoring standard requires of T0-T4.

    Args:
        repo_root: Repository root.

    Returns:
        One row per unit, in load order.

    Raises:
        ValueError: A unit listed in :data:`RESIDUE_DELETIONS` fires T0, or a unit
            listed in :data:`T4_VERBOSE_OUTPUT` is not dispatched by another unit.
            Either would mean a constant is silently overriding a mechanical test.
    """
    units = load_units(repo_root)
    entry_points = entry_point_slugs(repo_root / "pyproject.toml")
    dispatched = dispatched_slugs(units)
    t2_tracked = tracked_files(repo_root)

    unknown_subagents = set(T4_VERBOSE_OUTPUT) - set(dispatched)
    if unknown_subagents:
        raise ValueError(f"T4_VERBOSE_OUTPUT names units nothing dispatches: {sorted(unknown_subagents)}")

    stubs = {unit.slug for unit in units if unit.is_prompt and is_registration_stub(unit.frontmatter, unit.body)}
    substantive_prompts = {unit.slug for unit in units if unit.is_prompt and unit.slug not in stubs}

    # First pass: disposition per unit.
    dispositions: dict[str, tuple[str, str]] = {}
    t0_by_path: dict[str, bool] = {}
    stub_by_path: dict[str, bool] = {}
    for unit in units:
        is_stub = unit.is_prompt and unit.slug in stubs
        t0 = fires_t0(unit, entry_points)
        stub_by_path[unit.path] = is_stub
        t0_by_path[unit.path] = t0
        dispositions[unit.path] = _classify(unit, is_stub, t0, dispatched, substantive_prompts, repo_root, t2_tracked)

    residue_firing_t0 = sorted(
        unit.slug
        for unit in units
        if unit.slug in RESIDUE_DELETIONS and t0_by_path[unit.path] and not stub_by_path[unit.path]
    )
    if residue_firing_t0:
        raise ValueError(
            f"RESIDUE_DELETIONS names units that fire T0 and belong to the wrapper batch: {residue_firing_t0}"
        )

    # Second pass: groups need the alphabetical list of standalone skills.
    skill_singletons = sorted(
        {
            unit.slug
            for unit in units
            if dispositions[unit.path][0] == "skill"
            and merge_family(unit.slug) is None
            and unit.slug not in EXPLICIT_GROUPS
        }
    )

    rows: list[Row] = []
    for unit in units:
        disposition, reason = dispositions[unit.path]
        if disposition == "delete":
            group, target = "-", "-"
        else:
            group = _group_for(unit.slug, skill_singletons)
            family = merge_family(unit.slug)
            target = to_target_slug(family if disposition == "merge" and family else unit.slug)
        rows.append(
            Row(
                path=unit.path,
                slug=unit.slug,
                disposition=disposition,
                group=group,
                target=target,
                batch=_batch(disposition, unit, stub_by_path[unit.path], t0_by_path[unit.path]),
                reason=reason,
            )
        )
    return rows


def _classify(
    unit: Unit,
    is_stub: bool,
    t0: bool,
    dispatched: frozenset[str],
    substantive_prompts: set[str],
    repo_root: Path,
    tracked: frozenset[str],
) -> tuple[str, str]:
    """Return the ``(disposition, reason)`` pair for one unit.

    Args:
        unit: The unit to classify.
        is_stub: Whether the unit is a registration stub.
        t0: Whether T0 fired for the unit.
        dispatched: Slugs another unit dispatches.
        substantive_prompts: Slugs whose prompt file carries a body of its own.
        repo_root: Repository root, for resolving T2's globs.
        tracked: Git-tracked relative paths, for T2's tracked-file check.

    Returns:
        The disposition and the reason recorded in the unit's row.
    """
    if is_stub:
        return "delete", "Registration stub: frontmatter pointer, no body of its own."
    if unit.slug in RESIDUE_DELETIONS:
        return "delete", RESIDUE_DELETIONS[unit.slug]
    if t0:
        return "delete", "T0: wraps an `agdt-*` entry point and adds nothing to it."
    carries_the_body = unit.is_prompt if unit.slug in substantive_prompts else not unit.is_prompt
    # T4 is evaluated before T3 because the dispatch relationship is the dominant trait: a
    # dispatched subagent that also has numbered steps is still a subagent, not a skill.
    if carries_the_body and unit.slug in T4_VERBOSE_OUTPUT and unit.slug in dispatched:
        return "subagent", f"T4: {T4_VERBOSE_OUTPUT[unit.slug]}"
    family = merge_family(unit.slug)
    if family is not None:
        return "merge", f"Step of the `{family}` workflow-step family; merges into one skill."
    if not unit.is_prompt and unit.slug in substantive_prompts:
        return (
            "collapse",
            "Agent shell over a substantive prompt of the same slug; collapses into that skill.",
        )
    if fires_t1(unit):
        return "collapse", "T1: short body naming no glob, workflow or provider; collapses into an instruction file."
    if fires_t2(unit, repo_root, tracked):
        return "collapse", "T2: names a path glob; collapses into an `applyTo` instruction file."
    if fires_t3(unit):
        return "skill", "T3: an ordered procedure that is one job."
    return "delete", "No test fired; the standard prefers nothing over a prompt file."


# --------------------------------------------------------------------------------------
# Assertions
# --------------------------------------------------------------------------------------


def assert_partition(rows: Sequence[Row], expected_total: int | None = None) -> None:
    """Assert the three retirement batches partition the rows.

    Args:
        rows: The derived or published rows.
        expected_total: Row count to reconcile against, when known.

    Raises:
        ValueError: A row carries no batch or an unknown one, the batch sizes do
            not sum to the row count, a file appears twice, or the row count does
            not equal *expected_total*.
    """
    unknown = sorted({row.batch for row in rows} - set(BATCHES))
    if unknown:
        raise ValueError(f"rows carry batches outside the partition: {unknown}")
    counts = Counter(row.batch for row in rows)
    if sum(counts.values()) != len(rows):
        raise ValueError(f"batch sizes {dict(counts)} do not sum to {len(rows)} rows")
    duplicates = sorted(path for path, count in Counter(row.path for row in rows).items() if count > 1)
    if duplicates:
        raise ValueError(f"files appearing more than once: {duplicates}")
    bad_disposition = sorted({row.disposition for row in rows} - set(DISPOSITIONS))
    if bad_disposition:
        raise ValueError(f"rows carry dispositions outside the vocabulary: {bad_disposition}")
    bad_group = sorted({row.group for row in rows} - set(GROUPS) - {"-"})
    if bad_group:
        raise ValueError(f"rows carry groups outside the eight names: {bad_group}")
    grouped_deletes = sorted(row.path for row in rows if row.disposition == "delete" and row.group != "-")
    if grouped_deletes:
        raise ValueError(f"delete rows must carry group '-': {grouped_deletes}")
    ungrouped_non_deletes = sorted(row.path for row in rows if row.disposition != "delete" and row.group == "-")
    if ungrouped_non_deletes:
        raise ValueError(f"non-delete rows must carry a named group (not '-'): {ungrouped_non_deletes}")
    if expected_total is not None and len(rows) != expected_total:
        raise ValueError(f"row count {len(rows)} does not equal the expected {expected_total}")


def collisions(rows: Sequence[Row]) -> dict[str, list[str]]:
    """Return target slugs claimed by more than one legacy slug, minus the merges.

    An agent file and a prompt stub of the same slug mapping to one target is the
    intended merge, and a workflow-step family collapsing onto its family name is
    the intended merge too. Anything else is a collision.

    Args:
        rows: The derived rows.

    Returns:
        A mapping of target slug to the conflicting legacy slugs.
    """
    by_target: dict[str, set[str]] = defaultdict(set)
    for row in rows:
        if row.target == "-":
            continue
        by_target[row.target].add(row.slug)
    found = {}
    for target, slugs in sorted(by_target.items()):
        if len(slugs) == 1:
            continue
        if all(merge_family(slug) is not None for slug in slugs):
            continue
        found[target] = sorted(slugs)
    return found


def count_files(repo_root: Path) -> tuple[int, int]:
    """Return the number of ``agdt.*`` agent and prompt units, manifests excluded."""
    agents = [p for p in (repo_root / AGENTS_DIR).glob("agdt.*.agent.md") if p.name != MANIFEST_NAME]
    prompts = [p for p in (repo_root / PROMPTS_DIR).glob("agdt.*.prompt.md") if p.name != MANIFEST_NAME]
    return len(agents), len(prompts)


# --------------------------------------------------------------------------------------
# Rendering and parsing
# --------------------------------------------------------------------------------------

#: The heading the row table sits under; every earlier table is a summary.
ROWS_HEADING = "## Rows"

#: A row line of the published table, as distinct from the summary tables above it.
_ROW_LINE_RE = re.compile(r"^\| `\.github/(?:agents|prompts)/agdt\.")

TABLE_HEADER = "| Legacy path | Slug | Disposition | Group | Target slug | Retirement batch |"
TABLE_RULE = "|---|---|---|---|---|---|"


def render_table(rows: Sequence[Row]) -> str:
    """Render the six-column row table as Markdown."""
    lines = [TABLE_HEADER, TABLE_RULE]
    for row in rows:
        lines.append(
            f"| `{row.path}` | `{row.slug}` | {row.disposition} | {row.group} | "
            f"{'-' if row.target == '-' else f'`{row.target}`'} | {row.batch} |"
        )
    return "\n".join(lines)


def parse_table(text: str) -> list[Row]:
    """Parse the published row table back into rows.

    ``--verify-partition`` re-runs the partition assertion against the published
    table rather than against a fresh derivation, so it must read the table the
    same way a later issue would.

    Args:
        text: The published Markdown document.

    Returns:
        The parsed rows, without their reasons.

    Raises:
        ValueError: The document carries no row table.
    """
    body = text.split(f"\n{ROWS_HEADING}\n", 1)
    if len(body) != 2:
        raise ValueError(f"the document carries no {ROWS_HEADING!r} section")
    rows: list[Row] = []
    for line in body[1].splitlines():
        if not _ROW_LINE_RE.match(line):
            continue
        cells = [cell.strip().strip("`") for cell in line.strip().strip("|").split("|")]
        if len(cells) != 6:
            raise ValueError(f"malformed row: {line}")
        rows.append(
            Row(
                path=cells[0],
                slug=cells[1],
                disposition=cells[2],
                group=cells[3],
                target=cells[4],
                batch=cells[5],
                reason="",
            )
        )
    if not rows:
        raise ValueError("no rows found in the published table")
    return rows


def _summary_table(rows: Sequence[Row]) -> str:
    """Render the disposition-by-batch summary."""
    counts: Counter[tuple[str, str]] = Counter((row.disposition, row.batch) for row in rows)
    lines = ["| Disposition | stubs | wrappers | residue | Total |", "|---|---|---|---|---|"]
    for disposition in DISPOSITIONS:
        cells = [counts[(disposition, batch)] for batch in BATCHES]
        lines.append(f"| {disposition} | {cells[0]} | {cells[1]} | {cells[2]} | {sum(cells)} |")
    totals = [sum(counts[(d, batch)] for d in DISPOSITIONS) for batch in BATCHES]
    lines.append(f"| **Total** | **{totals[0]}** | **{totals[1]}** | **{totals[2]}** | **{sum(totals)}** |")
    return "\n".join(lines)


def _group_table(rows: Sequence[Row]) -> str:
    """Render the surviving-target count per group."""
    targets: dict[str, set[str]] = defaultdict(set)
    row_counts: Counter[str] = Counter()
    for row in rows:
        if row.group == "-":
            continue
        targets[row.group].add(row.target)
        row_counts[row.group] += 1
    lines = ["| Group | Legacy rows | Target slugs |", "|---|---|---|"]
    for group in GROUPS:
        names = ", ".join(f"`{name}`" for name in sorted(targets[group]))
        lines.append(f"| {group} | {row_counts[group]} | {names} |")
    return "\n".join(lines)


def _reason_table(rows: Sequence[Row]) -> str:
    """Render the recorded reason for every row the naive selectors miss."""
    lines = ["| Legacy path | Disposition | Reason |", "|---|---|---|"]
    for row in rows:
        if row.disposition != "delete" or row.batch != "residue":
            continue
        lines.append(f"| `{row.path}` | {row.disposition} | {row.reason} |")
    return "\n".join(lines)


# --------------------------------------------------------------------------------------
# Reconciliation
# --------------------------------------------------------------------------------------

#: The figures the prior analysis this programme is built on concluded, quoted in
#: #3758.  They are reconciled against, never adjusted to.
PROMPT_SKILLS_FIGURE_LABEL = "Prompt skills (9 plain + 2 `context: fork`)"

PRIOR_ANALYSIS: dict[str, int] = {
    "Injected files": 259,
    "Agent files": 132,
    "Prompt files": 127,
    "Prompt registration stubs (delete)": 113,
    "Substantive prompts": 14,
    "Prompt deletions that are not stubs": 2,
    PROMPT_SKILLS_FIGURE_LABEL: 11,
    "Prompt subagents": 1,
    "Agent deletions": 90,
    "Agent merges": 15,
    "Agent skills": 11,
    "Agent collapses": 11,
    "Agent subagents": 5,
    "Surviving skill names": 24,
    "Surviving subagent names": 6,
    "Retirement batch `stubs`": 113,
    "Retirement batch `wrappers`": 87,
    "Retirement batch `residue`": 59,
}


def derived_figures(rows: Sequence[Row]) -> dict[str, int]:
    """Compute the figures :data:`PRIOR_ANALYSIS` is reconciled against.

    Args:
        rows: The derived rows.

    Returns:
        A mapping with the same keys as :data:`PRIOR_ANALYSIS`.
    """
    agents = [row for row in rows if row.path.startswith(AGENTS_DIR)]
    prompts = [row for row in rows if row.path.startswith(PROMPTS_DIR)]
    stubs = [row for row in prompts if row.batch == "stubs"]

    def count(subset: Sequence[Row], disposition: str) -> int:
        return sum(1 for row in subset if row.disposition == disposition)

    def targets(disposition: str) -> int:
        return len({row.target for row in rows if row.disposition == disposition})

    return {
        "Injected files": len(rows),
        "Agent files": len(agents),
        "Prompt files": len(prompts),
        "Prompt registration stubs (delete)": len(stubs),
        "Substantive prompts": len(prompts) - len(stubs),
        "Prompt deletions that are not stubs": count(prompts, "delete") - len(stubs),
        "Prompt skills (9 plain + 2 `context: fork`)": count(prompts, "skill"),
        "Prompt subagents": count(prompts, "subagent"),
        "Agent deletions": count(agents, "delete"),
        "Agent merges": count(agents, "merge"),
        "Agent skills": count(agents, "skill"),
        "Agent collapses": count(agents, "collapse"),
        "Agent subagents": count(agents, "subagent"),
        "Surviving skill names": targets("skill") + len({row.target for row in rows if row.disposition == "merge"}),
        "Surviving subagent names": targets("subagent"),
        "Retirement batch `stubs`": sum(1 for row in rows if row.batch == "stubs"),
        "Retirement batch `wrappers`": sum(1 for row in rows if row.batch == "wrappers"),
        "Retirement batch `residue`": sum(1 for row in rows if row.batch == "residue"),
    }


def _reconciliation_table(rows: Sequence[Row]) -> tuple[str, list[str]]:
    """Render the prior-versus-derived table and list the disagreements."""
    derived = derived_figures(rows)
    lines = ["| Figure | Prior analysis | Derived here | Agrees |", "|---|---|---|---|"]
    disagreements = []
    for label, prior in PRIOR_ANALYSIS.items():
        actual = derived[label]
        agrees = "yes" if actual == prior else "**no**"
        if actual != prior:
            disagreements.append(f"{label}: prior {prior}, derived {actual}")
        lines.append(f"| {label} | {prior} | {actual} | {agrees} |")
    return "\n".join(lines), disagreements


def literal_proxy_only(repo_root: Path) -> list[str]:
    """Return the units T0's second limb catches and its four-line proxy does not.

    Args:
        repo_root: Repository root.

    Returns:
        The slugs, sorted.
    """
    entry_points = entry_point_slugs(repo_root / "pyproject.toml")
    extra = []
    for unit in load_units(repo_root):
        if not fires_t0(unit, entry_points):
            continue
        if unit.action_lines > T0_MAX_ACTION_LINES:
            extra.append(unit.slug)
    return sorted(extra)


# --------------------------------------------------------------------------------------
# Document
# --------------------------------------------------------------------------------------


def render_document(rows: Sequence[Row], repo_root: Path) -> str:
    """Render the published Markdown document.

    Args:
        rows: The derived rows.
        repo_root: Repository root, for the file counts quoted in the method.

    Returns:
        The whole document, ending in a newline.
    """
    agents, prompts = count_files(repo_root)
    reconciliation, disagreements = _reconciliation_table(rows)
    derived = derived_figures(rows)
    extra_wrappers = literal_proxy_only(repo_root)
    extra_list = "\n".join(f"- `{slug}`" for slug in extra_wrappers)
    disagreement_list = (
        "\n".join(f"- {line}" for line in disagreements) if disagreements else "- None. Every figure above agrees."
    )
    prompt_skill_reconciliation = _prompt_skill_reconciliation(rows, derived)
    return f"""# Disposition and slug map

Every injected `agdt.*` customization file, what happens to it, what it is called
afterwards, and which retirement batch retires it. Seven later issues select rows from
this table by the **Group** and **Retirement batch** columns rather than re-deriving the
predicates, because three independent re-derivations disagree and a disagreement here is
a file that no issue deletes.

This document is generated. Do not edit it by hand:

```bash
python scripts/derive_customization_disposition.py            # regenerate
python scripts/derive_customization_disposition.py --check    # fail if stale
python scripts/derive_customization_disposition.py --verify-partition
python scripts/derive_customization_disposition.py --verify-authored
```

## Corpus

| Directory | `agdt.*` files | Manifest | Units |
|---|---|---|---|
| `.github/agents/` | {agents + 1} | `agdt.README.md` | {agents} |
| `.github/prompts/` | {prompts + 1} | `agdt.README.md` | {prompts} |
| **Total** | | | **{agents + prompts}** |

`{agents + prompts}` is also the number of entries in
`tests/fixtures/skill_classification_expected.json`, which the script asserts.

## Method

Each unit is measured — slug, whether the re-slugged name matches an `agdt-*` entry in
`[project.scripts]`, the non-blank line count of its `## Actions` section, its body
length, the path globs it names, its numbered steps and its distinct commands — and then
the rules below are applied **in order**, first match wins, exactly as
[the authoring standard](authoring-standard.md) requires of T0–T4.

1. **Registration stub** — a prompt whose frontmatter points at another unit with
   `agent:` and whose body is empty. Disposition `delete`.
2. **Residue deletion** — one of the three units deleted for a reason other than T0.
   Each reason is recorded in the row and repeated below. Disposition `delete`.
3. **T0** — the slug matches an `agdt-*` entry point and the body adds nothing.
   Disposition `delete`.
4. **T4** — another unit dispatches this one and its output is verbose intermediate work
   the parent does not need in full. Disposition `subagent`.
5. **Family merge** — a step of `agdt.work-on-jira-issue.*`,
   `agdt.pull-request-review.*`, or `agdt.ai-pr-loop-supervisor.*`. Disposition `merge`, onto the family's target slug.
6. **Collapse onto a prompt** — an agent shell whose prompt file of the same slug carries
   the substantive body. Disposition `collapse`.
7. **T1 / T2** — a short body naming no glob, workflow or provider, or a body naming a
   path glob that matches a tracked file. Disposition `collapse`, into an instruction
   file.
8. **T3** — an ordered procedure. Disposition `skill`.
9. Otherwise `delete`: no test fired and the standard prefers nothing to a prompt file.

### T0 has two limbs

T0's operative test is that *the body adds nothing to what the command already does*. The
standard operationalises it as "an `## Actions` section of four non-blank lines or fewer",
which is the length of the canonical wrapper shape — the numbered step, the opening fence,
the command, the closing fence. That proxy alone misses the wrappers that spell out a
second flag or a follow-up `agdt-*` call, so a second limb is applied: **an `## Actions`
section that invokes nothing but `agdt-*` commands introduces no capability the commands
do not already have**. A body reaching for any other tool does add something, and fails
T0.

The second limb is what moves these {len(extra_wrappers)} units into the wrapper batch:

{extra_list}

### The retirement batch column is a partition

Applied in order, stopping at the first match:

- `stubs` — `delete`, under `.github/prompts/`, and a registration stub.
- `wrappers` — `delete`, under `.github/agents/`, and T0 fired.
- `residue` — **everything else**, including the delete rows the first two rules did not
  match. It is a complement, not a third filter: three independent filters over five
  dispositions leave gaps, and a gap is a file that no issue deletes while a later
  acceptance criterion asserts that none survives.

`--verify-partition` re-runs the assertion against this published table, so a later issue
can prove the property without trusting a fresh derivation.

### Re-slug

`agdt.x.y` → `agdt-x-y`, lowercased, validated against `^[a-z0-9](-?[a-z0-9])*$` and a
64-character limit. A dot is illegal in a skill name and an illegal name fails to load
silently. An agent file and the prompt stub of the same slug map to one target slug —
that is the intended merge, not a collision — and so do the members of a merged
workflow-step family. Any other repeated target is reported as an error.

## Summary

{_summary_table(rows)}

## Groups

The eight group names are fixed by issue #3758; eight later issues select rows by them.

{_group_table(rows)}

## Deletions that a naive selector misses

The `stubs` and `wrappers` batches are selected by one predicate each. Everything below is
a `delete` row that neither predicate matches, so it is retired by the residue issue and
not by the stub or wrapper issue.

{_reason_table(rows)}

## Reconciliation

{reconciliation}

Disagreements:

{disagreement_list}

{prompt_skill_reconciliation}

Two judgements in this derivation are worth a reader's attention whatever the figures
above say.

- **The four-line proxy alone yields 77 wrappers, not 87.** Read literally, T0's
  parenthetical excludes the {len(extra_wrappers)} units listed under *T0 has two limbs*,
  and each of them would then reach T3 and become a standalone skill. Publishing a skill
  whose entire content is "run `agdt-vpn-status`, then run `agdt-task-wait`" is precisely
  the second-thing-to-keep-in-sync that T0 exists to prevent, so the second limb is the
  correct reading and the parenthetical is a proxy calibrated on the canonical shape. The
  literal count is recorded here so the choice is auditable rather than invisible.
- **`agdt.advance-workflow` is the one entry-point unit that is not a T0 wrapper.** Its
  `## Actions` section reaches for `python3` to implement a retry-and-diagnose loop, so
  its body does add something. It is still deleted, because standard §11 puts determinism
  in code: the retry belongs in `agdt-advance-workflow`, not in a customization file. It
  is therefore residue, not a wrapper, which is why the wrapper batch is 87 and the agent
  deletions are 90.

One nuance the totals cannot express: the prior analysis splits the surviving prompt-side
units into "9 skills plus 2 `context: fork` skills plus 1 subagent". `context: fork` is a
frontmatter key on a skill, not a disposition, so both of those forms are `skill` rows
here and the split is a later authoring decision. The `analysis-and-fork` group is where
the two `context: fork` skills live.

## Rows

{render_table(rows)}
"""


def _prompt_skill_reconciliation(rows: Sequence[Row], derived: dict[str, int]) -> str:
    """Explain the prompt-skill disagreement with the concrete causing files."""
    prior = PRIOR_ANALYSIS[PROMPT_SKILLS_FIGURE_LABEL]
    actual = derived[PROMPT_SKILLS_FIGURE_LABEL]
    if prior == actual:
        return ""

    collapsed_prompts = sorted(
        row.path
        for row in rows
        if row.path.startswith(PROMPTS_DIR) and row.disposition == "collapse" and row.reason.startswith("T2:")
    )
    if not collapsed_prompts:
        return ""

    files = "\n".join(f"- `{path}`" for path in collapsed_prompts)
    promoted_prompts = [
        path
        for path in sorted(PROMPT_SUBAGENT_TO_SKILL_RECLASSIFICATIONS)
        if any(row.path == path and row.disposition == "skill" for row in rows)
    ]
    promoted_notes = "\n".join(
        f"- `{path}` — {PROMPT_SUBAGENT_TO_SKILL_RECLASSIFICATIONS[path]}" for path in promoted_prompts
    )
    if promoted_prompts:
        arithmetic = f"{prior} - {len(collapsed_prompts)} + {len(promoted_prompts)} = {actual}"
        promoted_clause = (
            f"{len(promoted_prompts)} prompt unit now counts as a skill rather than as a subagent"
            if len(promoted_prompts) == 1
            else f"{len(promoted_prompts)} prompt units now count as skills rather than as subagents"
        )
        cause_summary = (
            f"The {prior}→{actual} prompt-skill disagreement has two causes:\n\n"
            f"- {len(collapsed_prompts)} prompt units now hit T2 and collapse instead of surviving as "
            "standalone skills.\n"
            f"- {promoted_clause} ({arithmetic}).\n\n"
        )
        promoted_block = f"{promoted_notes}\n\n"
    else:
        cause_summary = (
            f"The {prior}→{actual} prompt-skill disagreement is caused by "
            f"{len(collapsed_prompts)} prompt units that now hit T2 and collapse instead of "
            "surviving as standalone skills:\n\n"
        )
        promoted_block = ""
    return (
        cause_summary
        + f"{files}\n\n"
        + promoted_block
        + "That is expected under the ordered rules: a prompt naming tracked-file globs is an "
        "instruction-file collapse (T2), so it is counted as `collapse` rather than `skill`."
    )


# --------------------------------------------------------------------------------------
# Modes
# --------------------------------------------------------------------------------------


def _expected_authored_kinds_by_target(rows: Sequence[Row]) -> dict[str, set[str]]:
    """Return expected authored artifact kinds keyed by target slug."""
    expected_kinds_by_target: dict[str, set[str]] = defaultdict(set)
    for row in rows:
        if row.target == "-":
            continue
        expected_kind = EXPECTED_KIND_BY_DISPOSITION.get(row.disposition)
        if expected_kind is not None:
            expected_kinds_by_target[row.target].add(expected_kind)
    return expected_kinds_by_target


def verify_authored(rows: Sequence[Row], repo_root: Path) -> tuple[list[str], list[str], list[str]]:
    """Compare surviving target slugs against what has actually been authored.

    Args:
        rows: The derived or published rows.
        repo_root: Repository root.

    Returns:
        A ``(authored, missing, unexpected)`` triple: the names found on disk, the
        target slugs this table expects that nothing has authored yet, and the
        authored names this table does not expect.

    Raises:
        ValueError: The table maps one target slug to incompatible artifact kinds,
            one target is claimed by more than one authored artifact, or an authored
            artifact kind does not match what the table permits for that target.
    """
    expected_kinds_by_target = _expected_authored_kinds_by_target(rows)
    legacy_expected_kinds_by_slug: dict[str, set[str]] = defaultdict(set)
    for item in rows:
        if item.target == "-":
            continue
        expected_kinds = expected_kinds_by_target.get(item.target)
        if not expected_kinds:
            continue
        legacy_expected_kinds_by_slug[item.slug.replace(".", "-")].update(expected_kinds)
    legacy_slugs = set(legacy_expected_kinds_by_slug)
    for target, kinds in sorted(expected_kinds_by_target.items()):
        if len(kinds) > 1:
            listed = ", ".join(sorted(kinds))
            raise ValueError(f"target {target!r} has incompatible dispositions requiring both {listed}")

    authored_paths_by_slug: dict[str, list[tuple[str, str]]] = defaultdict(list)
    for root in AUTHORED_SKILL_ROOTS:
        for skill in sorted((repo_root / root).glob("agdt-*/SKILL.md")):
            authored_paths_by_slug[skill.parent.name].append(("skill", skill.relative_to(repo_root).as_posix()))
    for root in AUTHORED_AGENT_ROOTS:
        for agent in sorted((repo_root / root).glob("agdt-*.agent.md")):
            slug = agent.name.removesuffix(".agent.md")
            authored_paths_by_slug[slug].append(("subagent", agent.relative_to(repo_root).as_posix()))

    authored: set[str] = set()
    for slug, claims in sorted(authored_paths_by_slug.items()):
        if len(claims) > 1:
            rendered = ", ".join(f"{kind}:{path}" for kind, path in claims)
            raise ValueError(f"target {slug!r} is claimed by multiple authored artifacts: {rendered}")
        kind, path = claims[0]
        expected_kinds = expected_kinds_by_target.get(slug)
        if expected_kinds is None and slug in legacy_slugs:
            expected_kinds = legacy_expected_kinds_by_slug[slug]
        if expected_kinds is not None and kind not in expected_kinds:
            expected_kind = next(iter(expected_kinds))
            raise ValueError(
                f"target {slug!r} is authored as {kind} ({path}) but the table expects a {expected_kind} artifact"
            )
        authored.add(slug)

    expected = set(expected_kinds_by_target)
    recognized = expected | legacy_slugs
    return sorted(authored), sorted(expected - authored), sorted(authored - recognized)


def _fail(message: str) -> int:
    """Print *message* to stderr and return the failure exit code."""
    print(f"FAIL — {message}", file=sys.stderr)
    return 1


def _run_derive(repo_root: Path, out: Path, check: bool) -> int:
    """Derive the table and either write it or compare it with what is published."""
    rows = derive_rows(repo_root)
    agents, prompts = count_files(repo_root)
    assert_partition(rows, expected_total=agents + prompts)

    fixture = repo_root / "tests" / "fixtures" / "skill_classification_expected.json"
    if not fixture.is_file():
        return _fail(f"fixture {fixture} not found; cannot reconcile derived rows with expected corpus entries")
    entries = len(json.loads(fixture.read_text(encoding="utf-8")))
    if entries != len(rows):
        return _fail(f"{len(rows)} rows but {entries} entries in {fixture.name}")

    found = collisions(rows)
    if found:
        return _fail(f"target slug collisions: {found}")

    document = render_document(rows, repo_root)
    if check:
        if not out.is_file():
            return _fail(f"{out} does not exist; run the script without --check")
        if out.read_text(encoding="utf-8") != document:
            return _fail(f"{out} is stale; regenerate it with this script")
        print(f"OK — {out} is up to date ({len(rows)} rows).")
        return 0

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(document, encoding="utf-8")
    counts = Counter(row.batch for row in rows)
    print(f"Wrote {out} — {len(rows)} rows ({', '.join(f'{b}={counts[b]}' for b in BATCHES)}).")
    return 0


def _run_verify_partition(published: Path, expected_total: int | None = None) -> int:
    """Re-run the partition assertion against the published table."""
    if not published.is_file():
        return _fail(f"{published} does not exist")
    try:
        rows = parse_table(published.read_text(encoding="utf-8"))
        assert_partition(rows, expected_total=expected_total)
    except (RuntimeError, ValueError) as exc:
        return _fail(str(exc))
    counts = Counter(row.batch for row in rows)
    print(f"OK — {len(rows)} rows partition into {', '.join(f'{b}={counts[b]}' for b in BATCHES)}.")
    return 0


def _run_verify_authored(repo_root: Path, published: Path) -> int:
    """Compare the published table's surviving names against the authored units."""
    if not published.is_file():
        return _fail(f"{published} does not exist")
    try:
        rows = parse_table(published.read_text(encoding="utf-8"))
    except ValueError as exc:
        return _fail(str(exc))
    try:
        authored, missing, unexpected = verify_authored(rows, repo_root)
    except ValueError as exc:
        return _fail(str(exc))

    authored_set = set(authored)
    expected_by_group: dict[str, set[str]] = defaultdict(set)
    expected_kinds_by_target = _expected_authored_kinds_by_target(rows)
    for row in rows:
        if row.target != "-" and row.target in expected_kinds_by_target:
            expected_by_group[row.group].add(row.target)

    for group in GROUPS:
        group_expected = expected_by_group.get(group, set())
        group_authored = group_expected & authored_set
        print(f"Group {group}: {len(group_authored)}/{len(group_expected)} authored")
        for name in sorted(group_expected - authored_set):
            print(f"  - {name}")

    print(f"\nAll authored units found: {len(authored)}")
    for name in authored:
        print(f"  + {name}")
    print(f"\nTarget slugs not yet authored: {len(missing)}")
    for name in missing:
        print(f"  - {name}")
    print(f"\nAuthored units this table does not expect: {len(unexpected)}")
    for name in unexpected:
        print(f"  ? {name}")
    return 1 if unexpected else 0


def main(argv: Iterable[str] | None = None) -> int:
    """Parse arguments and run the requested mode.

    Args:
        argv: Command-line arguments, defaulting to ``sys.argv[1:]``.

    Returns:
        A process exit code: 0 on success, 1 on any failure.
    """
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--repo-root", type=Path, default=REPO_ROOT, help="Repository root to derive from.")
    parser.add_argument("--out", type=Path, default=None, help=f"Output path (default: {PUBLISHED_PATH}).")
    parser.add_argument("--check", action="store_true", help="Fail when the published table is stale.")
    parser.add_argument(
        "--verify-partition",
        action="store_true",
        help="Assert the three retirement batches partition the published table.",
    )
    parser.add_argument(
        "--expected-total",
        type=int,
        default=None,
        metavar="N",
        help="Expected row count for --verify-partition; fails when the table has a different number of rows.",
    )
    parser.add_argument(
        "--verify-authored",
        action="store_true",
        help="Compare the published table's surviving names against the authored units.",
    )
    args = parser.parse_args(list(argv) if argv is not None else None)

    repo_root = args.repo_root.resolve()
    out = args.out if args.out is not None else repo_root / PUBLISHED_PATH

    if args.verify_partition:
        expected_total = args.expected_total
        if expected_total is None:
            fixture = repo_root / "tests" / "fixtures" / "skill_classification_expected.json"
            if not fixture.is_file():
                return _fail(f"fixture {fixture} not found; pass --expected-total explicitly")
            expected_total = len(json.loads(fixture.read_text(encoding="utf-8")))
        return _run_verify_partition(out, expected_total=expected_total)
    if args.verify_authored:
        return _run_verify_authored(repo_root, out)
    try:
        return _run_derive(repo_root, out, args.check)
    except (RuntimeError, ValueError) as exc:
        return _fail(str(exc))


if __name__ == "__main__":
    raise SystemExit(main())
