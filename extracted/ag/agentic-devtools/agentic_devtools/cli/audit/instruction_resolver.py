"""Instruction file resolver for the audit workflow.

Discovers and preloads the instruction files relevant to the file paths
referenced in PR review comments. Always includes the root
``.github/copilot-instructions.md`` and repository-root ``AGENTS.md``
entries, then walks up directory trees to find scoped instructions.

Directory-scoped instructions are resolved as ``AGENTS.md`` because that is
the only directory-local filename GitHub actually reads. A legacy
``<dir>/copilot-instructions.md`` file is still preloaded when it exists so
its content remains visible, but it is never offered as a creation target —
creating one would write guidance to a path no agent reads.

``.github/instructions/**/*.instructions.md`` files are also discovered and
preloaded when their ``applyTo`` frontmatter glob matches any reviewed path.
These are higher-precedence instruction sources; they are surfaced as
read-only context (``can_update=False``) so the audit agent does not create
duplicate guidance in ``AGENTS.md``.
"""

from __future__ import annotations

import re
from pathlib import Path

from agentic_devtools.cli.audit.models import InstructionFile

#: Legacy directory-local instruction filename. GitHub does not read it
#: outside ``.github/``; kept only to preload pre-migration files.
INSTRUCTION_FILENAME = "copilot-instructions.md"
#: Directory-local instruction filename that GitHub reads at any depth.
AGENT_INSTRUCTION_FILENAME = "AGENTS.md"
ROOT_INSTRUCTION_PATH = f".github/{INSTRUCTION_FILENAME}"
#: Directory that holds path-scoped ``.instructions.md`` files.
GITHUB_INSTRUCTIONS_DIR = ".github/instructions"


def resolve_instruction_files(file_paths: list[str], repo_root: str) -> list[InstructionFile]:
    """Resolve all relevant instruction files for the given file paths.

    Strategy:
    1. Always include ``.github/copilot-instructions.md`` (root).
    2. Always include repository-root ``AGENTS.md`` as creatable context.
    3. For each file path referenced in review comments, walk up the
       directory tree offering ``<dir>/AGENTS.md`` (whether or not it
       exists) and preloading any legacy ``<dir>/copilot-instructions.md``
       that does exist.
    4. Discover ``.github/instructions/**/*.instructions.md`` files whose
       ``applyTo`` globs match any reviewed path, and preload them as
       read-only context (can_update=False) so the audit agent does not
       create duplicate guidance in ``AGENTS.md``.
    5. Deduplicate results by path.

    Args:
        file_paths: Repo-relative file paths from PR review comments.
        repo_root: Absolute path to the repository root.

    Returns:
        List of InstructionFile instances with content preloaded.
    """
    root = Path(repo_root)
    seen_paths: set[str] = set()
    results: list[InstructionFile] = []

    # Always include root instruction file
    _add_instruction_file(ROOT_INSTRUCTION_PATH, root, seen_paths, results)
    _add_instruction_file(AGENT_INSTRUCTION_FILENAME, root, seen_paths, results)

    # Walk up directory tree for each referenced file
    for file_path in file_paths:
        _walk_up_for_instructions(file_path, root, seen_paths, results)

    # Preload matching .github/instructions/*.instructions.md files
    _load_github_instructions(file_paths, root, seen_paths, results)

    return results


def _walk_up_for_instructions(
    file_path: str,
    repo_root: Path,
    seen_paths: set[str],
    results: list[InstructionFile],
) -> None:
    """Walk up from a file path to find instruction files in parent dirs.

    Each ancestor directory contributes its ``AGENTS.md`` path — the
    directory-local file GitHub reads — regardless of whether it exists, so
    the audit agent may create it. A legacy ``copilot-instructions.md`` in
    the same directory is added only when it already exists.
    """
    # Normalize path separators
    normalized = file_path.replace("\\", "/")
    if normalized.startswith("/"):
        normalized = normalized[1:]

    # Guard against path traversal: reject paths containing '..' segments
    parts = normalized.split("/")
    if ".." in parts:
        return

    # Walk from file's directory up to repo root (including the root itself)
    for i in range(len(parts) - 1, -1, -1):
        dir_path = "/".join(parts[:i]) if i > 0 else ""
        agents_path = f"{dir_path}/{AGENT_INSTRUCTION_FILENAME}" if dir_path else AGENT_INSTRUCTION_FILENAME
        _add_instruction_file(agents_path, repo_root, seen_paths, results)
        legacy_path = f"{dir_path}/{INSTRUCTION_FILENAME}" if dir_path else INSTRUCTION_FILENAME
        _add_instruction_file(
            legacy_path,
            repo_root,
            seen_paths,
            results,
            only_if_exists=True,
            can_update=False,
        )


def _add_instruction_file(
    relative_path: str,
    repo_root: Path,
    seen_paths: set[str],
    results: list[InstructionFile],
    only_if_exists: bool = False,
    can_update: bool = True,
) -> None:
    """Add an instruction file if not already seen.

    When *only_if_exists* is true, a missing file is skipped entirely
    instead of being recorded as a creatable path.
    """
    if relative_path in seen_paths:
        return
    seen_paths.add(relative_path)

    abs_path = repo_root / relative_path
    # Defense-in-depth: ensure the resolved path stays within the repo root
    try:
        if not abs_path.resolve().is_relative_to(repo_root.resolve()):
            return
    except (OSError, ValueError):
        return

    if abs_path.is_file():
        try:
            content = abs_path.read_text(encoding="utf-8")
            results.append(
                InstructionFile(
                    path=relative_path,
                    exists=True,
                    can_update=can_update,
                    content=content,
                )
            )
        except (OSError, UnicodeDecodeError):
            results.append(
                InstructionFile(
                    path=relative_path,
                    exists=True,
                    can_update=can_update,
                    content="",
                )
            )
    elif not only_if_exists:
        results.append(
            InstructionFile(
                path=relative_path,
                exists=False,
                can_update=can_update,
                content="",
            )
        )


def _parse_apply_to(content: str) -> list[str]:
    """Parse comma-separated ``applyTo`` glob patterns from YAML front-matter.

    Returns an empty list when the file has no front-matter or no ``applyTo``
    key — meaning the file applies to all paths and should always be included.

    Args:
        content: Full text of a ``.instructions.md`` file.

    Returns:
        List of stripped glob pattern strings, or an empty list.
    """
    if not content.startswith("---"):
        return []
    end = content.find("---", 3)
    if end == -1:
        return []
    frontmatter = content[3:end]
    match = re.search(r'^applyTo:\s*["\']?(.*?)["\']?\s*$', frontmatter, re.MULTILINE)
    if not match:
        return []
    raw = match.group(1).strip()
    if not raw:
        return []
    return [p.strip() for p in raw.split(",") if p.strip()]


def _glob_to_regex(pattern: str) -> re.Pattern[str]:
    """Convert a glob pattern with ``**`` support to a compiled regex.

    ``*`` matches any sequence of non-separator characters; ``**`` matches
    any sequence of characters including path separators.

    Args:
        pattern: A glob pattern string (e.g. ``"**/*.py"`` or ``"specs/**"``).

    Returns:
        Compiled regex for use with ``re.Pattern.fullmatch``.
    """
    regex_parts: list[str] = []
    i = 0
    while i < len(pattern):
        if pattern.startswith("**/", i):
            # Globstar directory prefix: zero or more directories.
            regex_parts.append("(?:.*/)?")
            i += 3
            continue
        if pattern.startswith("**", i):
            regex_parts.append(".*")
            i += 2
            continue
        char = pattern[i]
        if char == "*":
            regex_parts.append("[^/]*")
        elif char == "?":
            regex_parts.append("[^/]")
        else:
            regex_parts.append(re.escape(char))
        i += 1
    return re.compile("".join(regex_parts))


def _any_path_matches(file_paths: list[str], patterns: list[str]) -> bool:
    """Return True if at least one file path fully matches any of the patterns.

    Args:
        file_paths: Repo-relative file paths (forward-slash separated).
        patterns: Glob patterns from an ``applyTo`` directive.

    Returns:
        True when any path matches any pattern; False otherwise.
    """
    compiled = [_glob_to_regex(p) for p in patterns]
    for path in file_paths:
        for regex in compiled:
            if regex.fullmatch(path):
                return True
    return False


def extract_apply_to_patterns(content: str) -> list[str]:
    """Return ``applyTo`` glob patterns from a ``.instructions.md`` file's frontmatter.

    Returns an empty list when the file has no frontmatter, the frontmatter
    cannot be parsed, or ``applyTo`` is absent or not a string value.
    """
    return _parse_apply_to(content)


def _load_github_instructions(
    file_paths: list[str],
    repo_root: Path,
    seen_paths: set[str],
    results: list[InstructionFile],
) -> None:
    """Discover ``.github/instructions/**/*.instructions.md`` and preload relevant ones.

    Each file's ``applyTo`` front-matter glob is matched against the reviewed
    file paths.  Files that match — or that carry no ``applyTo`` at all —
    are preloaded as read-only context (``can_update=False``) so the audit
    agent sees the higher-precedence guidance without being offered a
    duplicate write target in ``AGENTS.md``.

    Args:
        file_paths: Repo-relative file paths from PR review comments.
        repo_root: Absolute path to the repository root.
        seen_paths: Mutable set of already-recorded relative paths (dedup).
        results: Mutable list to append matching InstructionFile entries to.
    """
    instructions_dir = repo_root / GITHUB_INSTRUCTIONS_DIR
    if not instructions_dir.is_dir():
        return
    repo_root_resolved = repo_root.resolve()
    for instr_file in sorted(instructions_dir.rglob("*.instructions.md")):
        # Resolve symlinks and enforce repository confinement before reading content.
        # A symlink such as `.github/instructions/x.instructions.md -> /dev/zero` would
        # otherwise be dereferenced by read_text() before any confinement check.
        try:
            if not instr_file.resolve().is_relative_to(repo_root_resolved):
                continue
        except (OSError, ValueError):
            continue
        try:
            content = instr_file.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            content = ""
        apply_to = extract_apply_to_patterns(content)
        # No applyTo ⇒ applies everywhere; non-empty ⇒ only when paths match.
        if not apply_to or _any_path_matches(file_paths, apply_to):
            rel_path = str(instr_file.relative_to(repo_root)).replace("\\", "/")
            _add_instruction_file(rel_path, repo_root, seen_paths, results, can_update=False)
