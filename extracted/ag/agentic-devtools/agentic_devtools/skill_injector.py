"""Mirrors bundled agent/prompt/skill files into a target repository.

Three kinds are mirrored:

* ``agents`` and ``prompts`` are placed directly into ``.github/agents/`` and
  ``.github/prompts/`` in the target repo (flat layout — no subdirectories).
  Files from source subdirectories are flattened by encoding the directory
  name into the filename (e.g. ``sub/foo.agent.md`` → ``agdt.sub.foo.agent.md``).
* ``skills`` mirrors the canonical ``.agents/skills/`` tree **verbatim**: one
  directory per skill, carrying its ``SKILL.md`` entry file and any one-level
  deep bundled resources.  Skill directory names are never flattened, because
  a skill name must match ``^[a-z0-9](-?[a-z0-9])*$`` and a name containing a
  dot makes the skill silently fail to load.

Each target directory carries a managed ``agdt.README.md`` manifest.
"""

from __future__ import annotations

import os
import re
import shutil
import sys
import tempfile
import warnings
from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath

import yaml

from agentic_devtools.config import VALID_CODE_HOSTING, VALID_ISSUE_ADAPTERS
from agentic_devtools.skill_classification import parse_classification, should_inject

_MANAGED_PREFIX = "agdt."
_MANAGED_README = _MANAGED_PREFIX + "README.md"
_SPECKIT_PREFIX = "speckit."
_LEGACY_AGDT_ENTRY = ".agdt/"
_ALPHA_ONLY_RE = re.compile(r"[^a-zA-Z]")

# The directory-shaped kind: mirrored verbatim from ``.agents/skills/``.
_SKILLS_KIND = "skills"
_SKILL_ENTRY_FILE = "SKILL.md"
_KINDS: tuple[str, ...] = ("agents", "prompts", _SKILLS_KIND)
_SKILLS_MANIFEST_MARKER = "<!-- agdt:managed-skills-manifest:v1 -->"

# A manifest row rendered by :func:`_generate_readme`, e.g. ``| `a/SKILL.md` | … |``.
_MANIFEST_ROW_RE = re.compile(r"^\|\s*`([^`]+)`\s*\|")
_SKILL_NAME_RE = re.compile(r"^[a-z0-9](?:-?[a-z0-9])*$")

# ---------------------------------------------------------------------------
# Bundled-source resolution
# ---------------------------------------------------------------------------

_BUNDLED_DIR = Path(__file__).parent / "_bundled_skills"


def _get_source_dir(kind: str) -> Path | None:
    """Return the directory that contains the bundled *kind* files.

    For wheel installs the files live under ``_bundled_skills/<kind>/``.
    For editable installs the ``force-include`` has not run, so we fall
    back to the repo-level source directory — ``.github/<kind>/`` for the
    flat kinds and ``.agents/skills/`` for the ``skills`` kind.

    Returns ``None`` when neither location exists (corrupted install).
    """
    bundled = _BUNDLED_DIR / kind
    # Wheel install — has actual .md files (possibly in subdirs) besides __init__.py
    if bundled.is_dir() and any(bundled.rglob("*.md")):
        return bundled

    # Editable-install fallback: climb to the repo root
    repo_root = Path(__file__).resolve().parent.parent
    if kind == _SKILLS_KIND:
        fallback = repo_root / ".agents" / "skills"
    else:
        fallback = repo_root / ".github" / kind
    if fallback.is_dir():
        return fallback

    # Corrupted / minimal install — return None
    return None


def _target_dir(git_root: Path, kind: str) -> Path:
    """Return the destination directory in *git_root* for *kind*.

    The flat kinds land under ``.github/<kind>/``; the ``skills`` kind lands in
    the consumer's canonical skills path, ``.agents/skills/``.
    """
    if kind == _SKILLS_KIND:
        return git_root / ".agents" / "skills"
    return git_root / ".github" / kind


def _is_supported_skill_resource_name(name: str) -> bool:
    """Return ``True`` when *name* is a supported skill resource filename.

    Rejects names that are empty, start with a dot (hidden), or contain any
    character that would corrupt the backtick-delimited Markdown manifest row
    (backtick, newline, carriage-return) or act as a path separator (forward-
    or back-slash).
    """
    return (
        bool(name)
        and not name.startswith(".")
        and "/" not in name
        and "\\" not in name
        and "`" not in name
        and "\n" not in name
        and "\r" not in name
    )


def _is_managed_skill_relative_path(path: str) -> bool:
    """Return whether *path* has managed shape ``<skill-name>/<resource>``."""
    rel = PurePosixPath(path)
    if rel.is_absolute() or len(rel.parts) != 2:
        return False
    skill_name, resource = rel.parts
    return bool(_SKILL_NAME_RE.fullmatch(skill_name)) and _is_supported_skill_resource_name(resource)


def _resolve_skill_target_path(target_dir: Path, skill_relative_path: str) -> Path:
    """Resolve a managed skill destination path under *target_dir* safely.

    Rejects any path that is not in managed ``<skill-name>/<resource>`` shape,
    that traverses through an existing symlinked or non-directory intermediate
    component, or whose resolved destination escapes *target_dir*.  Also
    rejects an existing directory at the final destination (which would cause
    ``shutil.copy2`` to write a nested file instead of overwriting the target).
    """
    if not _is_managed_skill_relative_path(skill_relative_path):
        raise OSError(f"Invalid managed skill path: {skill_relative_path!r}")

    parts = PurePosixPath(skill_relative_path).parts
    resolved_root = target_dir.resolve()
    current = target_dir
    for part in parts[:-1]:
        current = current / part
        if current.is_symlink():
            raise OSError(f"Refusing managed skill path via symlinked directory: {current!s}")
        if current.exists() and not current.is_dir():
            raise OSError(f"Refusing managed skill path via non-directory component: {current!s}")

    dest = target_dir.joinpath(*parts)
    if dest.is_symlink():
        raise OSError(f"Refusing managed skill path to symlinked file: {dest!s}")
    if dest.is_dir():
        raise OSError(f"Refusing managed skill path to existing directory: {dest!s}")

    # Defensive TOCTOU backstop: with the symlink checks above this should be
    # unreachable in normal execution, but keep the containment check as a
    # final guard if the filesystem changes concurrently.
    if not dest.resolve().is_relative_to(resolved_root):  # pragma: no cover
        raise OSError(f"Refusing managed skill path outside skills target directory: {skill_relative_path!r}")
    return dest


def _is_self_repo(git_root: Path) -> bool:
    """Return ``True`` when *git_root* is the agentic-devtools repository itself.

    Injecting into this repository is destructive: ``.github/agents/`` and
    ``.github/prompts/`` are *tracked source* here (they are force-included
    into the wheel), so stale cleanup would delete every classification-filtered
    file and a wheel install would additionally overwrite the survivors with
    older released content.

    Two independent signals are used so both install shapes are covered:

    * Editable install — the running package's repo root is *git_root*.
    * Wheel install — *git_root* carries the agentic-devtools package source
      (``agentic_devtools/skill_injector.py``) and a ``pyproject.toml`` whose
      ``[project]`` table declares ``name = "agentic-devtools"``.
    """
    try:
        resolved_root = git_root.resolve()
        # Editable install: the installed package lives inside this checkout.
        if Path(__file__).resolve().parent.parent == resolved_root:
            return True
    except OSError:
        return False

    if not (resolved_root / "agentic_devtools" / "skill_injector.py").is_file():
        return False

    pyproject = resolved_root / "pyproject.toml"
    try:
        content = pyproject.read_bytes()
    except OSError:
        return False

    try:
        try:
            import tomllib  # stdlib on 3.11+
        except ImportError:  # pragma: no cover
            import tomli as tomllib  # type: ignore[no-redef]  # pragma: no cover

        data = tomllib.loads(content.decode("utf-8"))
        return data.get("project", {}).get("name") == "agentic-devtools"
    except Exception:
        return False


def _ensure_github_gitignore_unignores_agdt(git_root: Path) -> None:
    """Ensure `.github/.gitignore` does not ignore injected `.agdt` skills.

    Many repositories have a blanket `.agdt/` rule in their root `.gitignore`.
    That would also ignore `.github/agents/.agdt/` and `.github/prompts/.agdt/`,
    which prevents injected skills from being committed. To avoid mutating the
    root ignore file, we maintain a `.github/.gitignore` file with explicit
    un-ignore rules for these managed directories.

    .. note::

        This function is no longer called by :func:`inject_skills` after the
        migration from ``.agdt/`` subdirectories to a flat layout.  It is
        retained for backward compatibility in case external code references it.
    """

    github_dir = git_root / ".github"
    github_dir.mkdir(parents=True, exist_ok=True)
    github_gitignore = github_dir / ".gitignore"

    # Desired lines (order matters: comment followed by un-ignore rules).
    desired_lines = [
        "# Managed by agentic-devtools: ensure injected skills under .github are tracked.",
        "!agents/.agdt/",
        "!agents/.agdt/**",
        "!prompts/.agdt/",
        "!prompts/.agdt/**",
    ]

    existing_lines: list[str] = []
    if github_gitignore.exists():
        try:
            existing_lines = github_gitignore.read_text(encoding="utf-8").splitlines()
        except OSError as exc:
            warnings.warn(
                f"agentic-devtools: failed to read {github_gitignore!s}; "
                "injected skills under .github may remain ignored. "
                f"Underlying error: {exc}",
                RuntimeWarning,
            )
            # Injection should still proceed, even if skills remain ignored.
            return

    # Append any missing desired lines, preserving existing content.
    updated = False
    for line in desired_lines:
        if line not in existing_lines:
            existing_lines.append(line)
            updated = True

    if updated:
        try:
            github_gitignore.write_text(
                "\n".join(existing_lines) + "\n",
                encoding="utf-8",
            )
        except OSError as exc:
            warnings.warn(
                f"agentic-devtools: failed to write {github_gitignore!s}; "
                "injected skills under .github may remain ignored. "
                f"Underlying error: {exc}",
                RuntimeWarning,
            )
            # Callers treat injection I/O errors as a best-effort operation.
            return


def _list_md_files(source_dir: Path, kind: str) -> list[Path]:
    """Return the ``.md`` files that should be injected for *kind*.

    Uses ``rglob`` so that future subdirectory structures are preserved.

    * ``agents`` → all non-hidden ``*.md`` files (excluding hidden files/dirs).
    * ``prompts`` → only ``*.prompt.md`` files (excluding hidden files/dirs).
    """
    if kind == "agents":
        return sorted(
            p
            for p in source_dir.rglob("*.md")
            if p.is_file() and not any(part.startswith(".") for part in p.relative_to(source_dir).parts)
        )
    # prompts
    return sorted(
        p
        for p in source_dir.rglob("*.prompt.md")
        if p.is_file() and not any(part.startswith(".") for part in p.relative_to(source_dir).parts)
    )


def _select_skill_sources(
    source_dir: Path,
    *,
    issue_adapter: str | None,
    code_hosting: str | None,
) -> tuple[dict[str, Path], dict[Path, dict[str, object]], int]:
    """Select the skill files to mirror from *source_dir*.

    A skill is a non-hidden directory directly under *source_dir* that holds a
    ``SKILL.md`` entry file.  Its entry file plus every non-hidden file one
    level deep inside it are mirrored.  Directory names are preserved verbatim
    — never flattened — because a dot in a skill name makes the skill silently
    fail to load.

    The classification filter runs over each skill's ``SKILL.md`` exactly as it
    runs over the flat kinds, and prunes the **whole** skill (entry file and
    resources) when the declared axes do not match the consumer.  Filtering is
    skipped entirely when neither axis is resolved (legacy inject-all).

    Args:
        source_dir: The packaged/checked-out skills tree.
        issue_adapter: Resolved issue adapter, or ``None`` when unrestricted.
        code_hosting: Resolved code hosting platform, or ``None`` when unrestricted.

    Returns:
        A ``(origins, fm_cache, pruned)`` tuple where *origins* maps the
        repo-relative POSIX destination path (e.g. ``my-skill/SKILL.md``) to its
        source file, *fm_cache* holds already-parsed ``SKILL.md`` front-matter,
        and *pruned* counts the skills removed by the classification filter.
    """
    origins: dict[str, Path] = {}
    fm_cache: dict[Path, dict[str, object]] = {}
    pruned = 0
    filtering = issue_adapter is not None or code_hosting is not None

    skill_dirs = sorted(
        p
        for p in source_dir.iterdir()
        if p.is_dir() and not p.name.startswith(".") and (p / _SKILL_ENTRY_FILE).is_file()
    )
    for skill_dir in skill_dirs:
        entry = skill_dir / _SKILL_ENTRY_FILE
        if filtering:
            try:
                content: str | None = entry.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                # Keep the skill — no frontmatter cached; the copy phase
                # re-attempts read_text and handles the error.
                content = None
            if content is not None:
                fm = _parse_frontmatter(content)
                if not should_inject(
                    parse_classification(fm),
                    issue_adapter=issue_adapter,
                    code_hosting=code_hosting,
                ):
                    pruned += 1
                    continue
                fm_cache[entry] = fm

        resources = sorted(
            p
            for p in skill_dir.iterdir()
            if p.is_file() and p.name != _SKILL_ENTRY_FILE and _is_supported_skill_resource_name(p.name)
        )
        # Detect case-fold collisions among resources (e.g. Guide.md vs guide.md).
        # On a case-insensitive filesystem both would resolve to the same destination,
        # silently overwriting one.  Skip the entire skill to prevent silent data loss.
        seen_cf: dict[str, str] = {_SKILL_ENTRY_FILE.casefold(): _SKILL_ENTRY_FILE}
        collision: str | None = None
        for r in resources:
            cf = r.name.casefold()
            if cf in seen_cf:
                collision = r.name
                break
            seen_cf[cf] = r.name
        if collision is not None:
            warnings.warn(
                f"agentic-devtools: skipping skill '{skill_dir.name}' — "
                "resource name collision on a case-insensitive filesystem: "
                f"'{seen_cf[collision.casefold()]}' vs '{collision}'",
                RuntimeWarning,
            )
            continue
        for src in (entry, *resources):
            origins[src.relative_to(source_dir).as_posix()] = src

    return origins, fm_cache, pruned


def _read_managed_skill_manifest(target_dir: Path) -> set[str]:
    """Return the skill paths recorded in *target_dir*'s managed manifest.

    The generated ``agdt.README.md`` is the record of what a previous injection
    wrote, so it is the only basis for stale cleanup of the directory-shaped
    kind: skills the consumer authored themselves are never listed there and
    therefore can never be deleted.  Only a *missing* manifest yields an empty
    set (first-run state); unreadable/non-UTF-8 or untrusted manifest content
    raises :class:`OSError` so callers abort without mutating files.

    Entries that do not have the shape ``<skill-name>/<resource>`` are ignored,
    which also rejects absolute paths and ``..`` segments.
    """
    manifest_path = target_dir / _MANAGED_README
    try:
        content = manifest_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return set()
    except (UnicodeDecodeError, OSError) as exc:
        raise OSError(f"Unreadable managed skills manifest: {manifest_path!s}") from exc
    if _SKILLS_MANIFEST_MARKER not in content:
        raise OSError(f"Refusing untrusted skills manifest without managed marker: {manifest_path!s}")
    return {
        match.group(1)
        for line in content.splitlines()
        if (match := _MANIFEST_ROW_RE.match(line)) and _is_managed_skill_relative_path(match.group(1))
    }


# ---------------------------------------------------------------------------
# YAML front-matter parsing
# ---------------------------------------------------------------------------


def _derive_fallback_description_from_markdown(content: str) -> str | None:
    """Derive a short description from Markdown *content*.

    Prefers the first heading line (``#``-prefixed); otherwise uses the first
    non-empty line. Returns ``None`` when no suitable line is found.
    """
    for line in content.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("#"):
            heading = stripped.lstrip("#").strip()
            if heading:
                return heading
        else:
            return stripped
    return None


def _parse_frontmatter(content: str) -> dict[str, object]:
    """Extract YAML front-matter from *content*.

    Returns a dictionary of parsed front-matter keys. When no valid
    front-matter block is found (missing, empty, malformed, or containing
    non-mapping YAML), the returned dict may still contain a derived
    ``_agdt_fallback_description`` entry based on the first Markdown
    heading or first non-empty line in the body. If no fallback
    description can be derived, an empty dict is returned.
    """
    if not content.startswith("---"):
        # No front-matter block; derive a fallback description from the whole
        # content so callers can still present something meaningful.
        fallback = _derive_fallback_description_from_markdown(content)
        return {"_agdt_fallback_description": fallback} if fallback else {}

    # Use splitlines() so that both LF and CRLF line endings are handled
    # identically — content.find("\n---") would miss "\r\n---" on Windows.
    lines = content.splitlines()
    close_idx = next(
        (i for i, line in enumerate(lines) if i > 0 and line == "---"),
        None,
    )
    if close_idx is None:
        # Malformed front-matter; derive a fallback description from the body
        # after the opening delimiter (if any) so we do not return the leading
        # '---' line itself as the description.
        body_without_delimiter = "\n".join(lines[1:]) if len(lines) > 1 else ""
        source_for_fallback = body_without_delimiter or content
        fallback = _derive_fallback_description_from_markdown(source_for_fallback)
        return {"_agdt_fallback_description": fallback} if fallback else {}

    raw = "\n".join(lines[1:close_idx]).strip()
    body = "\n".join(lines[close_idx + 1 :])
    fallback = _derive_fallback_description_from_markdown(body) if body else None
    if not raw:
        return {"_agdt_fallback_description": fallback} if fallback else {}
    try:
        result = yaml.safe_load(raw)
        if not isinstance(result, dict):
            result = {}
    except yaml.YAMLError:
        result = {}
    if fallback and "_agdt_fallback_description" not in result:
        result["_agdt_fallback_description"] = fallback
    return result


def _extract_description(frontmatter: dict[str, object], kind: str) -> str:
    """Return a human-readable description from *frontmatter*.

    * For ``prompts``: uses the ``agent`` key.
    * For ``agents`` and ``skills``: uses the ``description`` key.

    Falls back to a derived description from the Markdown body when available,
    otherwise to ``"—"``.
    """
    if kind == "prompts":
        desc = frontmatter.get("agent")
    else:
        desc = frontmatter.get("description")
    if not desc:
        desc = frontmatter.get("_agdt_fallback_description")
    return str(desc) if desc else "\u2014"


# ---------------------------------------------------------------------------
# README generation
# ---------------------------------------------------------------------------


def _generate_readme(files: list[tuple[str, str]], kind: str) -> str:
    """Produce a managed ``agdt.README.md`` for the target directory.

    Args:
        files: list of ``(filename, description)`` tuples.  For the ``skills``
            kind the first element is the skill-relative path (e.g.
            ``my-skill/SKILL.md``), which also serves as the stale-cleanup
            record read back by :func:`_read_managed_skill_manifest`.
        kind: ``"agents"``, ``"prompts"`` or ``"skills"``.
    """
    title = {
        "agents": "Managed Agent Skills",
        "prompts": "Managed Prompt Skills",
        _SKILLS_KIND: "Managed Skills",
    }.get(kind, "Managed Skill Files")
    lines = [
        f"# {title}",
        "",
    ]
    if kind == _SKILLS_KIND:
        lines.extend([_SKILLS_MANIFEST_MARKER, ""])
        body_lines: list[str] = [
            "> **This folder is managed by [agentic-devtools](https://github.com/ayaiayorg/agentic-devtools).**",
            "> Do **not** edit the files listed in this manifest — they are overwritten by `agdt-setup`.",
            "> Skills you author yourself are not touched.",
            "",
            "The files below are mirrored from the `agentic-devtools` package into",
            "`.agents/skills/` so that Copilot CLI and similar tools can discover and",
            "use them by convention.  They should be checked into source control, and",
            "any local edits to the managed files listed here will be overwritten the",
            "next time `agdt-setup` is run.",
            "",
        ]
    else:
        body_lines = [
            "> **This folder is managed by [agentic-devtools](https://github.com/ayaiayorg/agentic-devtools).**",
            "> Do **not** edit these files manually — they are overwritten by `agdt-setup`.",
            "",
            "The files below are mirrored from the `agentic-devtools` package so that",
            "Copilot CLI and similar tools can discover and use them by convention.",
            "They should be checked into source control like any other `.github`",
            "configuration, and any local edits will be overwritten the next time",
            "`agdt-setup` is run.",
            "",
        ]
    lines.extend(body_lines)
    lines.extend(
        [
            "## File Manifest",
            "",
            "| File | Description |",
            "| ---- | ----------- |",
        ]
    )
    for filename, desc in files:
        safe_desc = desc.splitlines()[0].replace("`", "'") if desc else "\u2014"
        lines.append(f"| `{filename}` | {safe_desc} |")
    lines.extend(
        [
            "",
            "## Regeneration",
            "",
            "Run `agdt-setup` to update these files.  Stale files (removed in newer",
            "package versions) are automatically cleaned up.",
            "",
        ]
    )
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Filename flattening
# ---------------------------------------------------------------------------


def _flatten_filename(rel_path: Path) -> str:
    """Compute the flat target filename for a source file.

    Root-level files keep their name unchanged.
    Files in subdirectories get the managed prefix (``_MANAGED_PREFIX``)
    followed by sanitized directory parts and the original filename.
    Only a-zA-Z characters are kept from directory names.
    """
    parts = rel_path.parts
    if len(parts) == 1:
        return parts[0]
    dir_parts = parts[:-1]
    sanitized = [_ALPHA_ONLY_RE.sub("", p) for p in dir_parts]
    sanitized = [s for s in sanitized if s]  # drop empty after sanitization
    if not sanitized:
        return parts[-1]
    return _MANAGED_PREFIX + ".".join(sanitized) + "." + parts[-1]


# ---------------------------------------------------------------------------
# Private helpers
# ---------------------------------------------------------------------------


def _normalize_platform_arg(
    value: str | None,
    arg_name: str,
    valid_values: frozenset[str],
) -> str | None:
    """Normalize a platform argument to ``None`` if empty, whitespace, or unknown.

    Empty strings and whitespace-only strings are silently normalized to ``None``
    (unresolved / inject-all for that axis).

    Unknown (non-allowlist) values emit a :class:`RuntimeWarning` and are also
    normalized to ``None``, matching the "unresolved ⇒ inject-all" contract.
    This prevents callers that accidentally pass a stale or mis-spelled platform
    value from silently excluding or deleting constrained skill files.
    """
    if value is None:
        return None
    stripped = value.strip()
    if not stripped:
        return None
    if stripped not in valid_values:
        warnings.warn(
            f"inject_skills: unknown {arg_name} value {value!r}; "
            f"valid options are {sorted(valid_values)}. "
            "Treating as unresolved (inject-all for this axis).",
            RuntimeWarning,
            stacklevel=3,
        )
        return None
    return stripped


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class InjectionPlan:
    """The manifest diff computed for one kind (``agents``/``prompts``/``skills``).

    Attributes:
        kind: ``"agents"``, ``"prompts"`` or ``"skills"``.
        added: Destination names present in the source set and absent from the
            target directory.  Writing them is harmless.  Flat kinds use the
            flattened filename; the ``skills`` kind uses the skill-relative
            POSIX path (e.g. ``my-skill/SKILL.md``).
        overwritten: Destination names present in both, with different bytes.
            Under a wheel install these silently replace target content with
            the installed wheel's content.
        deleted: Planned deletion entries in the target directory.  For the flat
            kinds this includes managed ``agdt.*`` filenames absent from the
            source set (including files the classification filter pruned), plus
            ``".agdt/"`` when the legacy migration would remove that
            subdirectory or symlink.  For the ``skills`` kind it lists the
            previously-injected skill files (as recorded in the managed
            manifest) that the current source set no longer carries; a skill
            directory left empty by those deletions is removed too.
        case_renames: Pairs of ``(old_name, new_name)`` where both names share
            the same casefold and resolved to the same inode on the target
            filesystem (case-insensitive rename detected during planning).
            Only populated for the ``skills`` kind.  The execution phase uses
            this to perform a two-step rename so the directory-entry casing is
            updated before the new content is written.
    """

    kind: str
    added: tuple[str, ...]
    overwritten: tuple[str, ...]
    deleted: tuple[str, ...]
    case_renames: tuple[tuple[str, str], ...] = ()


@dataclass(frozen=True)
class InjectionSummary:
    """Counts describing the outcome of a skill-injection pass.

    Attributes:
        injected: Total number of units selected for injection across the three
            kinds — the managed ``agdt.*`` files for ``agents`` and ``prompts``
            (de-duplicated by flattened filename within each kind, excluding the
            generated ``agdt.README.md`` manifests) plus one unit per mirrored
            skill for ``skills`` (its bundled resources are not counted
            separately).  This is a best-effort count and can include files
            counted before a later write-time ``OSError``.
        pruned: Total number of source units removed by the classification
            filter across the three kinds.  Always ``0`` when neither platform
            axis is resolved (legacy inject-all), because filtering is skipped
            entirely in that case.
        plans: The per-kind manifest diff (adds / overwrites / deletes) computed
            by the planning phase.  Excluded from equality comparisons so that
            summaries continue to compare by their counts.
        deletions_blocked: ``True`` when the pass refused to run because it
            would have deleted planned entries and the caller did not pass
            ``assume_yes``.  Nothing was written, copied or unlinked.
    """

    injected: int
    pruned: int
    plans: tuple[InjectionPlan, ...] = field(default=(), compare=False)
    deletions_blocked: bool = field(default=False, compare=False)


def _diff_against_target(
    target_dir: Path,
    origins: dict[str, Path],
) -> tuple[list[str], list[str]]:
    """Split *origins* into the entries to add and the entries to overwrite.

    An entry is an *add* when no file exists at the destination, and an
    *overwrite* when one exists with different bytes.  Identical bytes are
    reported as neither.
    """
    added: list[str] = []
    overwritten: list[str] = []
    for name, src in origins.items():
        dest = target_dir / name
        if not dest.is_file():
            added.append(name)
        elif src.read_bytes() != dest.read_bytes():
            overwritten.append(name)
    return added, overwritten


def _plan_kind(
    kind: str,
    target_dir: Path,
    flat_name_origins: dict[str, Path],
) -> InjectionPlan:
    """Compute the manifest diff for *kind* without writing anything.

    Args:
        kind: ``"agents"`` or ``"prompts"``.
        target_dir: Destination directory in the target repository.  It does
            not need to exist yet.
        flat_name_origins: Mapping of flattened destination filename → source
            file, as resolved by the selection and classification phases.

    Returns:
        An :class:`InjectionPlan` whose three lists are sorted for stable output.
    """
    added, overwritten = _diff_against_target(target_dir, flat_name_origins)

    deleted: list[str] = []
    managed_names_exact = set(flat_name_origins.keys())
    managed_name_casefolds = {name.casefold(): name for name in managed_names_exact}
    if target_dir.is_dir():
        for existing in target_dir.iterdir():
            if (
                existing.is_file()
                and existing.name.startswith(_MANAGED_PREFIX)
                and existing.name != _MANAGED_README
                and existing.name not in managed_names_exact
            ):
                # A case-only variant whose casefold matches a source name is
                # only suppressed when the target filesystem actually resolves
                # both spellings to the same file (i.e. case-insensitive).  On
                # case-sensitive filesystems the candidate path won't exist, so
                # stat() raises OSError and the variant is planned as stale.
                casefolded = existing.name.casefold()
                if casefolded in managed_name_casefolds:
                    source_spelling = managed_name_casefolds[casefolded]
                    suppressed = False
                    try:
                        existing_stat = existing.stat()
                        cand_stat = (target_dir / source_spelling).stat()
                        if cand_stat.st_ino == existing_stat.st_ino and cand_stat.st_dev == existing_stat.st_dev:
                            suppressed = True
                    except OSError:
                        pass
                    if suppressed:
                        continue
                deleted.append(existing.name)
    old_agdt = target_dir / ".agdt"
    if old_agdt.is_symlink() or old_agdt.is_dir():
        deleted.append(_LEGACY_AGDT_ENTRY)

    return InjectionPlan(
        kind=kind,
        added=tuple(sorted(added)),
        overwritten=tuple(sorted(overwritten)),
        deleted=tuple(sorted(deleted)),
    )


def _validate_skills_target_dir(target_dir: Path) -> None:
    """Validate that the skills target directory and manifest are not symlinks.

    Called before any read of the managed manifest so that a symlinked
    ``.agents``, ``skills``, or ``agdt.README.md`` cannot redirect or block
    the manifest read before planning runs its own checks.

    Args:
        target_dir: The consumer's canonical skills directory.

    Raises:
        OSError: If ``target_dir``, its parent, or the managed manifest file
            is a symbolic link.
    """
    for _component in (target_dir.parent, target_dir):
        if _component.is_symlink():
            raise OSError(f"Refusing skills target with symlinked component: {_component!s}")
    _manifest_path = target_dir / _MANAGED_README
    if _manifest_path.is_symlink():
        raise OSError(f"Refusing skills manifest through symlink: {_manifest_path!s}")


def _plan_skills_kind(target_dir: Path, origins: dict[str, Path]) -> InjectionPlan:
    """Compute the manifest diff for the ``skills`` kind without writing.

    Adds and overwrites are computed exactly as for the flat kinds, but keyed by
    the skill-relative POSIX path so directory structure is preserved.

    Deletions are derived from the managed ``agdt.README.md`` manifest written
    by the previous run: an entry recorded there, still present on disk, and no
    longer in the source set is stale.  Anything the manifest does not name —
    including consumer-authored skills sharing the same tree — is never
    deleted.

    Args:
        target_dir: The consumer's canonical skills directory.  It does not
            need to exist yet.
        origins: Mapping of skill-relative POSIX path → source file.

    Returns:
        An :class:`InjectionPlan` whose three lists are sorted for stable output.
    """
    # Validate that target_dir, its parent, and the manifest are not symlinks.
    # Extracted into _validate_skills_target_dir so the same guard runs before
    # the early manifest read in the planning loop.
    _validate_skills_target_dir(target_dir)
    added: list[str] = []
    overwritten: list[str] = []
    for name, src in origins.items():
        dest = _resolve_skill_target_path(target_dir, name)
        if not dest.is_file():
            added.append(name)
        elif src.read_bytes() != dest.read_bytes():
            overwritten.append(name)

    # Build a casefold → exact-key map so that case-only renames on
    # case-insensitive filesystems (e.g. macOS, Windows) can be detected.
    origins_casefolds = {name.casefold(): name for name in origins}
    deleted: list[str] = []
    case_renames: list[tuple[str, str]] = []
    for name in _read_managed_skill_manifest(target_dir):
        if name in origins:
            continue
        dest = _resolve_skill_target_path(target_dir, name)
        if not dest.is_file():
            continue
        # Detect case-only renames: when the same inode is reachable via the
        # new spelling, the file is being renamed rather than deleted.  On a
        # case-sensitive filesystem the new path either does not exist or is a
        # distinct file, so stat() will raise OSError or return a different
        # inode and the entry remains a deletion candidate.
        name_cf = name.casefold()
        if name_cf in origins_casefolds:
            new_name = origins_casefolds[name_cf]
            try:
                new_dest = _resolve_skill_target_path(target_dir, new_name)
                old_st = dest.stat()
                new_st = new_dest.stat()
                if old_st.st_ino == new_st.st_ino and old_st.st_dev == new_st.st_dev:
                    # Same inode: this is a case rename on a case-insensitive FS.
                    # Record it so the execution phase can update the directory-
                    # entry casing via a two-step rename; do NOT add to deleted.
                    case_renames.append((name, new_name))
                    continue
            except OSError:
                pass
        deleted.append(name)
    return InjectionPlan(
        kind=_SKILLS_KIND,
        added=tuple(sorted(added)),
        overwritten=tuple(sorted(overwritten)),
        deleted=tuple(sorted(deleted)),
        case_renames=tuple(sorted(case_renames)),
    )


def _format_plans(plans: tuple[InjectionPlan, ...]) -> str:
    """Render *plans* as a human-readable manifest diff.

    Each kind gets a count header followed by three separately labelled lists
    (adds, overwrites, deletes); an empty list renders as ``(none)`` so the
    reader can tell "nothing to do" apart from "not reported".
    """
    lines: list[str] = []
    for plan in plans:
        lines.append(
            f"  Manifest diff — {plan.kind}: "
            f"{len(plan.added)} add(s), "
            f"{len(plan.overwritten)} overwrite(s), "
            f"{len(plan.deleted)} delete(s)"
        )
        for label, marker, names in (
            ("adds", "+", plan.added),
            ("overwrites", "~", plan.overwritten),
            ("deletes", "-", plan.deleted),
        ):
            lines.append(f"    {label} ({len(names)}):")
            if names:
                lines.extend(f"      {marker} {name}" for name in names)
            else:
                lines.append("      (none)")
    return "\n".join(lines)


def inject_skills_with_summary(
    git_root: Path | None,
    *,
    issue_adapter: str | None = None,
    code_hosting: str | None = None,
    dry_run: bool = False,
    assume_yes: bool = False,
) -> tuple[bool, InjectionSummary]:
    """Mirror bundled agent/prompt/skill files into the target repo.

    Places files directly into ``{git_root}/.github/agents/`` and
    ``{git_root}/.github/prompts/`` (flat layout), copying all relevant
    ``.md`` files and generating a managed ``agdt.README.md`` manifest in
    each.  Files from source subdirectories are flattened by encoding the
    directory name into the filename.

    The ``skills`` kind is mirrored differently: each skill directory under the
    packaged ``.agents/skills/`` tree is copied verbatim into
    ``{git_root}/.agents/skills/``, carrying its ``SKILL.md`` and its one-level
    deep resources.  Skill names are never flattened.

    A planning phase runs first and computes, per kind, the files that would be
    added, overwritten with different bytes, and deleted by stale cleanup.  The
    resulting manifest diff is printed on every run — including the executed
    one — so the operation is auditable after the fact.

    As a one-time migration, any old ``.agdt/`` subdirectories/symlinks inside
    the target kind directories are removed.  That migration is represented in
    the manifest diff as ``.agdt/`` and runs only when execution proceeds.

    When *git_root* is the agentic-devtools repository itself (see
    :func:`_is_self_repo`) the whole operation is skipped — nothing is copied
    or deleted — because those directories are tracked source there.

    Args:
        git_root: Repository/worktree root.  When ``None`` (not in a git
            repo) no files are written and the function returns ``False``.
        issue_adapter: Resolved issue adapter for the target repo (e.g.
            ``"jira"``, ``"github"``).  When ``None``, empty, whitespace-only,
            or an unrecognised value, the issue-adapter axis is unrestricted
            (all files pass).  Unrecognised values emit a :class:`RuntimeWarning`.
        code_hosting: Resolved code hosting platform for the target repo
            (e.g. ``"github"``, ``"azure_devops"``).  When ``None``, empty,
            whitespace-only, or an unrecognised value, the code-hosting axis is
            unrestricted (all files pass).  Unrecognised values emit a
            :class:`RuntimeWarning`.
        dry_run: When ``True``, print the manifest diff and return without
            writing, copying or unlinking anything (not even the target
            directories or the ``agdt.README.md`` manifests).
        assume_yes: Explicit opt-in required before any planned deletion is
            executed.  When deletions are pending and this is ``False``, the
            delete list is
            printed, nothing is executed for any kind, and the returned
            summary carries ``deletions_blocked=True``.  Ignored under
            *dry_run*, which never deletes anything anyway.

    Returns:
        A ``(success, summary)`` tuple.  ``success`` is ``True`` when all three
        kinds (agents/prompts/skills) were injected successfully, and ``False``
        when:
        - ``git_root`` is ``None``,
        - a source directory for a required kind cannot be resolved,
        - deletions are pending without *assume_yes*,
        - a ``UnicodeDecodeError`` occurs while reading source files (non-UTF8
          content), or
        - an ``OSError`` occurs while writing mirrored files or manifests.
        ``summary`` is an :class:`InjectionSummary` carrying best-effort counts
        of injected and pruned files (populated even on the ``OSError`` path)
        plus the per-kind manifest diff.
        When *git_root* is the agentic-devtools repository itself the result is
        ``(True, InjectionSummary(0, 0))`` and a :class:`RuntimeWarning` is
        emitted.
    """
    if git_root is None:
        return False, InjectionSummary(injected=0, pruned=0)

    if _is_self_repo(git_root):
        # The agentic-devtools repository is the *source* of these files:
        # ``.github/agents/`` and ``.github/prompts/`` are tracked source that
        # is force-included into the wheel.  Injecting here would delete every
        # classification-filtered file via stale cleanup and (under a wheel
        # install) overwrite the survivors with released content.  Skip
        # entirely and report success so callers do not surface a failure.
        warnings.warn(
            "agentic-devtools: skipping skill injection — the target repository "
            "is the agentic-devtools repository itself, where .github/agents/ and "
            ".github/prompts/ are tracked source rather than injected output.",
            RuntimeWarning,
        )
        return True, InjectionSummary(injected=0, pruned=0)

    injected_total = 0
    pruned_total = 0

    # Normalize both axes: strip whitespace; treat empty strings and
    # unrecognised values as None (unresolved / inject-all for that axis).
    issue_adapter = _normalize_platform_arg(issue_adapter, "issue_adapter", VALID_ISSUE_ADAPTERS)
    code_hosting = _normalize_platform_arg(code_hosting, "code_hosting", VALID_CODE_HOSTING)

    try:
        overall_success = True
        plans: list[InjectionPlan] = []
        plans_tuple: tuple[InjectionPlan, ...] = ()
        # (plan, target_dir, flat_name_origins, fm_cache) per planned kind,
        # carried from the planning phase into the execution phase.
        pending: list[tuple[InjectionPlan, Path, dict[str, Path], dict[Path, dict[str, object]]]] = []
        for kind in _KINDS:
            source_dir = _get_source_dir(kind)
            if source_dir is None:
                # Missing source for this kind (e.g. corrupted/minimal install) —
                # do not treat this as an empty snapshot, and do not delete or
                # overwrite any existing injected files. Mark overall result as
                # failure so callers can surface a warning.
                overall_success = False
                continue

            target_dir = _target_dir(git_root, kind)

            if kind == _SKILLS_KIND:
                # Directory-shaped kind: mirror each skill verbatim, never
                # flattened, and count one injected unit per skill.
                skill_origins, skill_fm_cache, skill_pruned = _select_skill_sources(
                    source_dir,
                    issue_adapter=issue_adapter,
                    code_hosting=code_hosting,
                )
                pruned_total += skill_pruned
                # Guard against symlinked .agents, .agents/skills, or the manifest
                # before reading it; _plan_skills_kind() repeats this check for the
                # planning read, but we need it here too because this read happens
                # earlier (for collision detection).
                _validate_skills_target_dir(target_dir)
                managed_before = _read_managed_skill_manifest(target_dir)
                managed_skills = {PurePosixPath(name).parts[0] for name in managed_before}
                managed_before_casefolds = {name.casefold(): name for name in managed_before}
                colliding_skills: set[str] = set()
                for name in skill_origins:
                    skill_name = PurePosixPath(name).parts[0]
                    dest = _resolve_skill_target_path(target_dir, name)
                    # File-level collision: dest exists but is not in the managed manifest.
                    # A case-only rename on a case-insensitive filesystem shares the same
                    # inode and must not be treated as a consumer collision.
                    not_in_manifest = name not in managed_before
                    if not_in_manifest:
                        name_cf = name.casefold()
                        if name_cf in managed_before_casefolds:
                            prior_spelling = managed_before_casefolds[name_cf]
                            try:
                                prior_dest = _resolve_skill_target_path(target_dir, prior_spelling)
                                ds = dest.stat()
                                ps = prior_dest.stat()
                                if ds.st_ino == ps.st_ino and ds.st_dev == ps.st_dev:
                                    not_in_manifest = False
                            except OSError:
                                pass
                    if (skill_name not in managed_skills and dest.parent.exists()) or (
                        not_in_manifest and dest.exists()
                    ):
                        colliding_skills.add(skill_name)
                if colliding_skills:
                    warnings.warn(
                        "agentic-devtools: skipping bundled skills that collide with "
                        "consumer-authored files not listed in the previous managed "
                        f"manifest: {', '.join(sorted(colliding_skills))}",
                        RuntimeWarning,
                    )
                    skill_origins = {
                        name: src
                        for name, src in skill_origins.items()
                        if PurePosixPath(name).parts[0] not in colliding_skills
                    }
                    selected_skill_names = {
                        PurePosixPath(name).parts[0]
                        for name, src in skill_origins.items()
                        if src.name == _SKILL_ENTRY_FILE
                    }
                    allowed_sources = set(skill_origins.values())
                    skill_fm_cache = {src: fm for src, fm in skill_fm_cache.items() if src in allowed_sources}
                    for managed_name in sorted(managed_before):
                        if PurePosixPath(managed_name).parts[0] not in colliding_skills:
                            continue
                        managed_dest = _resolve_skill_target_path(target_dir, managed_name)
                        if managed_dest.is_file():
                            skill_origins[managed_name] = managed_dest
                else:
                    selected_skill_names = {
                        PurePosixPath(name).parts[0]
                        for name, src in skill_origins.items()
                        if src.name == _SKILL_ENTRY_FILE
                    }

                injected_total += len(selected_skill_names)
                skills_plan = _plan_skills_kind(target_dir, skill_origins)
                plans.append(skills_plan)
                pending.append((skills_plan, target_dir, skill_origins, skill_fm_cache))
                continue

            # Determine which files to inject
            source_files = _list_md_files(source_dir, kind)
            # Exclude root-level ``agdt.README.md`` — the managed manifest
            # file generated by a previous run.  In editable-install scenarios
            # the repo's own ``.github/<kind>`` serves as source, so a leftover
            # manifest would otherwise be picked up as an injectable skill.
            # Only the *root-level* manifest is excluded; a nested file with the
            # same name (e.g. ``sub/agdt.README.md``) is legitimate and should
            # not be silently skipped.
            # Note: a plain ``README.md`` (without the managed prefix) is
            # already excluded by the ``p.name.startswith(_MANAGED_PREFIX)``
            # filter below, so no separate check is needed.
            source_files = [p for p in source_files if p.relative_to(source_dir) != Path(_MANAGED_README)]
            # Exclude speckit.* files — they reference .specify/ scripts not
            # available in target repos and are non-functional without the
            # full speckit scaffold.
            source_files = [p for p in source_files if not p.name.startswith(_SPECKIT_PREFIX)]
            # Only inject files whose *source* filename starts with the
            # managed prefix (``agdt.``).  Root-level files without the prefix
            # (e.g. ``copilot-instructions.md``) are repo-specific and must
            # not be copied into target repos where they could overwrite
            # user-authored files.  This also keeps the injected file set
            # aligned with stale cleanup, which only removes ``agdt.*`` files.
            source_files = [p for p in source_files if p.name.startswith(_MANAGED_PREFIX)]

            # Classification filter phase: apply frontmatter-based filtering
            # when at least one platform axis is resolved.  Files whose
            # classification does not match the resolved platform are excluded
            # before flat-name computation, so collision detection and the
            # README manifest reflect only actually-injected files.
            fm_cache: dict[Path, dict[str, object]] = {}
            if issue_adapter is not None or code_hosting is not None:
                pre_filter_count = len(source_files)
                filtered: list[Path] = []
                for src in source_files:
                    try:
                        content = src.read_text(encoding="utf-8")
                    except UnicodeDecodeError:
                        # Keep file — no frontmatter cached; copy phase
                        # re-attempts read_text and handles the error.
                        filtered.append(src)
                        continue
                    fm = _parse_frontmatter(content)
                    classification = parse_classification(fm)
                    if should_inject(
                        classification,
                        issue_adapter=issue_adapter,
                        code_hosting=code_hosting,
                    ):
                        fm_cache[src] = fm
                        filtered.append(src)
                source_files = filtered
                pruned_total += pre_filter_count - len(source_files)

            # Build set of flattened filenames for stale-cleanup comparison.
            # Also detect duplicate flat names — would cause silent overwriting.
            # The check uses ``casefold()`` so collisions on case-insensitive
            # filesystems (Windows, macOS default) are caught too.
            source_rel_names: set[str] = set()
            flat_name_origins: dict[str, Path] = {}
            _casefold_to_flat: dict[str, str] = {}  # casefold → first flat_name
            for src in source_files:
                flat_name = _flatten_filename(src.relative_to(source_dir))
                key = flat_name.casefold()
                prev_flat = _casefold_to_flat.get(key)
                if prev_flat is not None and prev_flat != flat_name:
                    # Case-insensitive collision (different casing)
                    warnings.warn(
                        f"agentic-devtools: duplicate flat filename {flat_name!r} "
                        f"(case-insensitive match of {prev_flat!r}) "
                        f"from {src!s} (first seen from {flat_name_origins[prev_flat]!s}); "
                        "only the last source will be injected on "
                        "case-insensitive filesystems.",
                        RuntimeWarning,
                    )
                    # Evict old casing entry so the latest variant wins
                    flat_name_origins.pop(prev_flat, None)
                    source_rel_names.discard(prev_flat)
                elif flat_name in flat_name_origins:
                    # Exact duplicate
                    warnings.warn(
                        f"agentic-devtools: duplicate flat filename {flat_name!r} "
                        f"from {src!s} (first seen from {flat_name_origins[flat_name]!s}); "
                        "only the last source will be injected.",
                        RuntimeWarning,
                    )
                _casefold_to_flat[key] = flat_name
                flat_name_origins[flat_name] = src
                source_rel_names.add(flat_name)

            injected_total += len(source_rel_names)

            # Planning phase: compute the manifest diff before anything is
            # written, so the dry run and the deletion gate can both act on it.
            plan = _plan_kind(kind, target_dir, flat_name_origins)
            plans.append(plan)
            pending.append((plan, target_dir, flat_name_origins, fm_cache))

        plans_tuple = tuple(plans)
        if plans_tuple:
            print(_format_plans(plans_tuple))

        if dry_run:
            # Nothing has been written, copied or unlinked up to this point.
            return overall_success, InjectionSummary(
                injected=injected_total,
                pruned=pruned_total,
                plans=plans_tuple,
            )

        pending_deletions = sum(len(plan.deleted) for plan in plans_tuple)
        if pending_deletions and not assume_yes:
            print(
                f"agentic-devtools: refusing to delete {pending_deletions} managed skill entries "
                "without confirmation — re-run with assume_yes=True (`agdt-setup --yes`) to allow "
                "deletions, or dry_run=True (`agdt-setup --dry-run`) to preview the manifest diff. "
                "Nothing was changed.",
                file=sys.stderr,
            )
            for plan in plans_tuple:
                if not plan.deleted:
                    continue
                print(f"  {plan.kind} deletes ({len(plan.deleted)}):", file=sys.stderr)
                for name in plan.deleted:
                    print(f"    - {name}", file=sys.stderr)
            return False, InjectionSummary(
                injected=injected_total,
                pruned=pruned_total,
                plans=plans_tuple,
                deletions_blocked=True,
            )

        # Execution phase — only reached when deletions are absent or approved.
        for plan, target_dir, flat_name_origins, fm_cache in pending:
            kind = plan.kind
            target_dir.mkdir(parents=True, exist_ok=True)

            # One-time migration: remove old .agdt/ subdirectory.
            # Guard against symlinks to avoid recursively deleting a
            # symlink target — just remove the link itself.
            if _LEGACY_AGDT_ENTRY in plan.deleted:
                old_agdt = target_dir / ".agdt"
                if old_agdt.is_symlink():
                    old_agdt.unlink()
                elif old_agdt.is_dir():
                    shutil.rmtree(old_agdt)

            # Copy files.  Flat kinds have their subdirectory structure encoded
            # in the filename; the skills kind keeps its directory, so the
            # destination parent is created when it does not exist yet.
            # Iterate the de-duplicated mapping so each destination is written
            # exactly once (the last source wins, consistent with the warning).
            # Track files created in this run so they can be rolled back if the
            # kind-level write fails before the manifest is updated.  Without
            # rollback, a partially-written skill would be absent from the old
            # manifest and the next run would treat it as consumer-authored,
            # permanently blocking injection of that skill.
            # Build new-name → old-name lookup from the plan's case_renames so
            # the copy loop can perform a two-step rename on case-insensitive FSes
            # where shutil.copy2 alone would preserve the old directory-entry casing.
            case_rename_new_to_old = {new: old for old, new in plan.case_renames}
            newly_created: list[Path] = []
            try:
                manifest: list[tuple[str, str]] = []
                for flat_name, src in flat_name_origins.items():
                    if kind == _SKILLS_KIND:
                        dest = _resolve_skill_target_path(target_dir, flat_name)
                    else:
                        dest = target_dir / flat_name
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    # Guard against SameFileError when source and target resolve
                    # to the same file — happens for editable installs targeting
                    # this repo's own source directory for the kind.
                    if src.resolve() != dest.resolve():
                        # For case renames detected during planning, perform a
                        # two-step rename (old → temp → new) so the directory-entry
                        # casing is updated before the new content is written.
                        # Without this, shutil.copy2 on a case-insensitive filesystem
                        # (macOS/Windows) updates the content but keeps the old
                        # capitalisation in the directory entry; subsequent checkouts
                        # on a case-sensitive filesystem would then expose the old
                        # spelling as an unmanaged orphan.
                        if kind == _SKILLS_KIND and flat_name in case_rename_new_to_old:
                            old_name = case_rename_new_to_old[flat_name]
                            old_path = _resolve_skill_target_path(target_dir, old_name)
                            if old_path.is_file() and not old_path.is_symlink():
                                _tmp_cr_fd, _tmp_cr_name = tempfile.mkstemp(dir=old_path.parent)
                                os.close(_tmp_cr_fd)
                                os.replace(old_path, _tmp_cr_name)
                                try:
                                    shutil.copy2(src, dest)
                                except Exception:
                                    try:
                                        os.replace(_tmp_cr_name, old_path)
                                    except OSError:
                                        pass
                                    raise
                                else:
                                    try:
                                        os.unlink(_tmp_cr_name)
                                    except OSError:  # pragma: no cover
                                        pass
                            else:
                                # Old path gone or changed between planning and
                                # execution; fall back to a normal copy.
                                existed_before = dest.exists()
                                if not existed_before:
                                    newly_created.append(dest)
                                shutil.copy2(src, dest)
                        else:
                            existed_before = dest.exists()
                            if not existed_before:
                                newly_created.append(dest)
                            shutil.copy2(src, dest)
                    if src in fm_cache:
                        desc = _extract_description(fm_cache[src], kind)
                    elif kind == _SKILLS_KIND and src.name != _SKILL_ENTRY_FILE:
                        # Skill resources are arbitrary files and may not be valid
                        # UTF-8 (e.g. images or binaries).  Use the filename as the
                        # manifest description to avoid a spurious UnicodeDecodeError
                        # that would set overall_success=False.
                        desc = src.name
                    else:
                        try:
                            content = src.read_text(encoding="utf-8")
                        except UnicodeDecodeError:
                            # Keep processing remaining files, but surface non-UTF8
                            # source content as an overall injection failure. Still
                            # include the file in the manifest with a fallback
                            # description so the managed README stays accurate.
                            overall_success = False
                            desc = "Non-UTF-8 source; description unavailable."
                        else:
                            fm = _parse_frontmatter(content)
                            desc = _extract_description(fm, kind)
                    manifest.append((flat_name, desc))

                # Remove exactly the stale entries the plan predicted.  For the
                # skills kind a skill directory emptied by those removals is
                # pruned too, so a retired skill leaves nothing behind.
                for stale_name in plan.deleted:
                    if stale_name == _LEGACY_AGDT_ENTRY:
                        continue
                    if kind == _SKILLS_KIND:
                        stale_path = _resolve_skill_target_path(target_dir, stale_name)
                    else:
                        stale_path = target_dir / stale_name
                    stale_path.unlink()
                    stale_parent = stale_path.parent
                    if stale_parent != target_dir and not any(stale_parent.iterdir()):
                        stale_parent.rmdir()

                # Generate agdt.README.md
                readme_path = target_dir / _MANAGED_README
                # TOCTOU backstop: _plan_skills_kind rejects a symlinked manifest
                # before mutations; this path is only reachable via a race where a
                # symlink is created between planning and execution.
                if kind == _SKILLS_KIND and readme_path.is_symlink():  # pragma: no cover
                    raise OSError(f"Refusing to write skills manifest through symlink: {readme_path!s}")
                # Atomic write: write to a sibling temp file then rename, so a
                # partial write never leaves a truncated/corrupt manifest behind.
                readme_content = _generate_readme(manifest, kind)
                tmp_fd, tmp_name = tempfile.mkstemp(dir=target_dir, prefix=".agdt.README.", suffix=".tmp")
                _tmp_replaced = False
                try:
                    with os.fdopen(tmp_fd, "w", encoding="utf-8") as fh:
                        fh.write(readme_content)
                    os.replace(tmp_name, readme_path)
                    _tmp_replaced = True
                finally:
                    if not _tmp_replaced:
                        try:
                            os.unlink(tmp_name)
                        except OSError:
                            pass
            except OSError:
                # Roll back files created in this run so the on-disk state
                # still matches the old manifest.  This ensures the next run
                # can re-attempt injection rather than treating the orphaned
                # files as consumer-authored.
                for new_file in newly_created:
                    try:
                        new_file.unlink()
                    except OSError:
                        pass
                    stale_parent = new_file.parent
                    while stale_parent != target_dir:
                        try:
                            stale_parent.rmdir()
                        except OSError:
                            break
                        stale_parent = stale_parent.parent
                raise

        return overall_success, InjectionSummary(
            injected=injected_total,
            pruned=pruned_total,
            plans=plans_tuple,
        )
    except OSError:
        return False, InjectionSummary(
            injected=injected_total,
            pruned=pruned_total,
            plans=plans_tuple or tuple(plans),
        )


# Private-name alias kept for internal/test imports that reference
# ``_inject_skills_with_summary``.
_inject_skills_with_summary = inject_skills_with_summary


def inject_skills(
    git_root: Path | None,
    *,
    issue_adapter: str | None = None,
    code_hosting: str | None = None,
    dry_run: bool = False,
    assume_yes: bool = False,
) -> bool:
    """Mirror bundled agent/prompt/skill files into the target repo (bool wrapper).

    Thin backward-compatible wrapper around
    :func:`inject_skills_with_summary` that discards the
    :class:`InjectionSummary` and returns only the success flag.  See
    :func:`inject_skills_with_summary` for full argument and behavior details.

    Returns:
        ``True`` when all three kinds (agents/prompts/skills) were injected
        successfully,
        ``False`` otherwise (see :func:`inject_skills_with_summary`) — including
        when pending deletions were blocked for want of *assume_yes*.
    """
    success, _summary = inject_skills_with_summary(
        git_root,
        issue_adapter=issue_adapter,
        code_hosting=code_hosting,
        dry_run=dry_run,
        assume_yes=assume_yes,
    )
    return success
