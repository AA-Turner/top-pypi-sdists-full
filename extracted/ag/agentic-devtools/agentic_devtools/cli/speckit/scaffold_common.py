"""
Shared feature-directory resolution helpers for SpecKit native scaffold commands.

Used by ``agdt-speckit-scaffold-plan``, ``agdt-speckit-scaffold-check-prereqs``,
and ``agdt-speckit-scaffold-update-agent-context`` to resolve the repository
root and the active feature directory under ``specs/`` natively in Python,
replacing the legacy ``.specify/scripts/bash/*.sh`` shell scripts (which do
not work reliably on Windows and are untested).
"""

from __future__ import annotations

import json
import os
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path

#: Environment variable holding the active feature directory name (or path).
SPECIFY_FEATURE_DIRECTORY_ENV = "SPECIFY_FEATURE_DIRECTORY"

#: Path, relative to the repo root, of the optional feature-metadata file.
FEATURE_METADATA_RELATIVE_PATH = Path(".specify") / "feature.json"

#: Matches the ``<number>-`` prefix or bare ``<number>`` used by SpecKit feature directories/branches.
FEATURE_DIR_PREFIX_RE = re.compile(r"^(\d+)(?:-|$)")

#: Matches the repository-standard ``type/ISSUE-KEY/description`` branch convention.
#: Group 1 captures the numeric portion of the issue key (GitHub or Jira-style).
_BRANCH_TYPE_KEY_RE = re.compile(
    r"^[^/]+/"
    r"(?:(\d+)|[A-Za-z][A-Za-z0-9]*-(\d+))"
    r"(?:/|$)"
)

__all__ = [
    "FEATURE_METADATA_RELATIVE_PATH",
    "SPECIFY_FEATURE_DIRECTORY_ENV",
    "ActiveFeature",
    "FeatureResolutionError",
    "get_current_branch",
    "get_repo_root",
    "has_git_repo",
    "resolve_active_feature",
]


class FeatureResolutionError(RuntimeError):
    """Raised when the active feature directory cannot be unambiguously resolved."""


@dataclass(frozen=True)
class ActiveFeature:
    """Resolved active feature context for SpecKit scaffold commands.

    Attributes:
        repo_root: Absolute path to the repository root.
        feature_dir: Absolute path to the active feature's ``specs/`` directory.
        branch: The resolved branch/feature name used for display purposes.
        has_git: Whether *repo_root* is inside a git working tree.
    """

    repo_root: Path
    feature_dir: Path
    branch: str
    has_git: bool


def _find_specify_project_root(start: Path | None = None) -> Path | None:
    """Walk up from *start* (default: cwd) looking for the nearest ``.specify`` directory.

    Returns the parent of the first ``.specify`` directory found, so that
    a SpecKit project nested inside a larger git repository uses its own
    ``.specify/feature.json`` and ``specs/`` tree rather than the outer
    repository's files.  Returns ``None`` when no ``.specify`` directory is
    found before reaching the filesystem root.

    The ``SPECIFY_INIT_DIR`` environment variable, when set, **pins** the
    project root rather than acting as a search start.  The specified path
    must be an existing directory that directly contains a ``.specify``
    subdirectory; if it does not, ``FeatureResolutionError`` is raised
    immediately so that a mis-configured override never silently falls
    through to an outer or unrelated project.
    """
    init_dir = os.environ.get("SPECIFY_INIT_DIR", "").strip()
    if init_dir:
        pinned = Path(init_dir).resolve()
        if not pinned.is_dir():
            raise FeatureResolutionError(f"SPECIFY_INIT_DIR={init_dir!r} is not an existing directory.")
        if not (pinned / ".specify").is_dir():
            raise FeatureResolutionError(f"SPECIFY_INIT_DIR={init_dir!r} does not contain a '.specify' directory.")
        return pinned
    candidate = (start or Path.cwd()).resolve()
    for directory in [candidate, *candidate.parents]:
        if (directory / ".specify").is_dir():
            return directory
    return None


def get_repo_root() -> Path:
    """Return the SpecKit project root, falling back to the git top-level, then cwd.

    Resolution order:

    1. Nearest ancestor that contains a ``.specify`` directory (honouring the
       ``SPECIFY_INIT_DIR`` env-var override), so a SpecKit sub-project inside
       a larger repository resolves to its own root rather than the outer
       repository root.
    2. Git repository top-level (``git rev-parse --show-toplevel``).
    3. Current working directory.
    """
    specify_root = _find_specify_project_root()
    if specify_root is not None:
        return specify_root
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode == 0 and result.stdout.strip():
            return Path(result.stdout.strip())
    except OSError:
        pass
    return Path.cwd()


def has_git_repo(repo_root: Path) -> bool:
    """Return True if *repo_root* is inside a git working tree."""
    try:
        result = subprocess.run(
            ["git", "-C", str(repo_root), "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True,
            check=False,
        )
    except OSError:
        return False
    return result.returncode == 0 and bool(result.stdout.strip())


def get_current_branch(repo_root: Path) -> str | None:
    """Return the current git branch name for *repo_root*, or None if unavailable."""
    try:
        result = subprocess.run(
            ["git", "-C", str(repo_root), "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True,
            text=True,
            check=False,
        )
    except OSError:
        return None
    if result.returncode == 0 and result.stdout.strip():
        return result.stdout.strip()
    return None


def _read_feature_metadata_snapshot(repo_root: Path) -> tuple[str | None, str | None]:
    """Read ``feature_directory`` and ``branch_name`` from a single JSON parse.

    Returns ``(feature_directory, branch_name)`` where either field may be ``None``.
    Reads the metadata file exactly once so that an atomic replacement by a
    concurrent scaffold cannot yield directory and branch from different writes.

    Raises:
        FeatureResolutionError: If the file exists but is unreadable (e.g. wrong
            encoding, permission denied), contains invalid JSON, has a non-object
            root, or has a present but invalid (non-string/blank) ``feature_directory``
            value, because ``feature_directory`` has higher precedence than the branch
            fallbacks and a silently-ignored malformed file would cause the wrong
            feature to be scaffolded. The absent file returns ``(None, None)``;
            when ``feature_directory`` is missing from an otherwise valid object,
            its tuple element is ``None`` and any valid ``branch_name`` is returned.
    """
    metadata_path = repo_root / FEATURE_METADATA_RELATIVE_PATH
    if not metadata_path.is_file():
        if metadata_path.exists() or metadata_path.is_symlink():
            raise FeatureResolutionError(
                f"{metadata_path} exists but is not a regular file. Fix or remove the path and try again."
            )
        return None, None
    try:
        raw = metadata_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        raise FeatureResolutionError(
            f"Cannot read {metadata_path}: {exc}. Fix or remove the file and try again."
        ) from exc
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise FeatureResolutionError(
            f"{metadata_path} contains invalid JSON: {exc}. Fix or remove the file and try again."
        ) from exc
    if not isinstance(data, dict):
        raise FeatureResolutionError(
            f"{metadata_path} must contain a JSON object but found {type(data).__name__}. "
            "Fix or remove the file and try again."
        )
    # --- feature_directory (required field, strict validation) ---
    dir_value = data.get("feature_directory")
    if isinstance(dir_value, str) and dir_value.strip():
        feature_directory: str | None = dir_value.strip()
    elif "feature_directory" in data:
        raise FeatureResolutionError(
            f"{metadata_path} contains an invalid 'feature_directory' value: {dir_value!r}. "
            "Expected a non-empty string. Fix or remove the file and try again."
        )
    else:
        feature_directory = None
    # --- branch_name (optional advisory field, no raise) ---
    branch_value = data.get("branch_name")
    branch_name: str | None = branch_value.strip() if isinstance(branch_value, str) and branch_value.strip() else None
    return feature_directory, branch_name


def _find_by_prefix(specs_dir: Path, prefix: str) -> Path | None:
    """Find a single existing ``specs/`` subdirectory matching numeric *prefix*.

    Comparison is numeric so that, for example, prefix ``"42"`` matches
    ``specs/042-feature`` and ``specs/42``.

    Raises:
        FeatureResolutionError: If more than one directory shares the prefix.
    """
    if not specs_dir.is_dir():
        return None
    try:
        target_number = int(prefix)
    except ValueError:
        return None
    matches: list[Path] = []
    for current_root, dirnames, _ in os.walk(specs_dir, followlinks=False):
        current_path = Path(current_root)
        child_dirs = [current_path / name for name in dirnames]
        dirnames[:] = [path.name for path in child_dirs if not path.is_symlink()]
        for path in child_dirs:
            if path.is_symlink():
                continue
            m = FEATURE_DIR_PREFIX_RE.match(path.name)
            if m and int(m.group(1)) == target_number:
                matches.append(path)
    if len(matches) == 1:
        return matches[0]
    if len(matches) > 1:
        names = ", ".join(sorted(match.relative_to(specs_dir).as_posix() for match in matches))
        raise FeatureResolutionError(
            f"Multiple spec directories found with prefix '{prefix}': {names}. "
            "Ensure only one spec directory exists per numeric prefix."
        )
    return None


def _latest_numbered_feature_dir(specs_dir: Path) -> str | None:
    """Return the repo-relative path to the highest-numbered feature directory under *specs_dir*, if any.

    Traverses the entire ``specs/`` tree (non-symlink directories only), so nested
    layouts such as ``specs/010-parent/042-child`` are handled correctly: the function
    returns ``"010-parent/042-child"`` rather than ``"010-parent"``.

    Raises:
        FeatureResolutionError: If two or more directories share the highest numeric
            prefix, because the result would be non-deterministic.
    """
    if not specs_dir.is_dir():
        return None
    best_number = -1
    best_rel: str | None = None
    tied_rels: list[str] = []
    for current_root, dirnames, _ in os.walk(specs_dir, followlinks=False):
        current_path = Path(current_root)
        child_dirs = [current_path / name for name in dirnames]
        dirnames[:] = [path.name for path in child_dirs if not path.is_symlink()]
        for child in child_dirs:
            if child.is_symlink():
                continue
            match = FEATURE_DIR_PREFIX_RE.match(child.name)
            if not match:
                continue
            number = int(match.group(1))
            rel = child.relative_to(specs_dir).as_posix()
            if number > best_number:
                best_number = number
                best_rel = rel
                tied_rels = []
            elif number == best_number:
                tied_rels.append(rel)
    if tied_rels:
        all_tied = ", ".join(sorted([best_rel or "", *tied_rels]))
        raise FeatureResolutionError(
            f"Multiple spec directories share the highest numeric prefix '{best_number:03d}' "
            f"under {specs_dir}: {all_tied}. "
            "Resolve the ambiguity by removing or renaming the duplicates."
        )
    return best_rel


def _resolve_env_directory(specs_dir: Path, repo_root: Path, env_value: str) -> Path:
    """Resolve a feature directory value to an absolute path."""
    directory = Path(env_value)
    if directory.is_absolute():
        return directory
    if len(directory.parts) == 1:
        # A bare name (no path separators) is relative to specs/.
        return specs_dir / env_value
    return repo_root / directory


def _extract_prefix_from_branch(branch: str) -> str | None:
    """Return the numeric spec-directory prefix encoded in *branch*, or ``None``.

    Understands two formats:

    - Legacy ``<number>-description`` (e.g. ``042-existing-feature``) — the prefix
      is the leading digit sequence before the first dash.
    - Repository-standard ``type/ISSUE-KEY/description`` (e.g. ``fix/2249/squash-fix``
      or ``feature/PROJECT-1234/add-webhook``) — the prefix is the numeric portion of
      the issue key in the second path segment.
    """
    # Legacy format: branch starts with <number>-
    m = FEATURE_DIR_PREFIX_RE.match(branch)
    if m:
        return m.group(1)
    # Repository-standard format: type/ISSUE-KEY/description
    m2 = _BRANCH_TYPE_KEY_RE.match(branch)
    if m2:
        # Group 1 is bare numeric, group 2 is the numeric part of a Jira-style key.
        return m2.group(1) or m2.group(2)
    return None


def _validate_within_specs(
    directory: Path,
    specs_dir: Path,
    *,
    source: str,
    repo_root: Path | None = None,
) -> None:
    """Raise FeatureResolutionError if *directory* resolves outside *specs_dir*.

    Uses ``Path.resolve()`` to follow symlinks so that symlink traversal attempts
    are caught as well as plain ``..`` path components.

    Args:
        directory: Candidate feature directory path to validate.
        specs_dir: The ``specs/`` directory that acts as the containment boundary.
        source: Human-readable label for the origin of the value (used in the
            error message).
        repo_root: Optional repository root. When provided, the resolved
            directory must also remain inside the repository root so symlinked
            ``specs/`` parents cannot redirect writes outside the repository.

    Raises:
        FeatureResolutionError: When the resolved *directory* is not inside the
            resolved *specs_dir*, or when *repo_root* is provided and the
            resolved *directory* escapes the resolved repository root.
    """
    resolved_directory = directory.resolve()
    resolved_specs_dir = specs_dir.resolve()
    try:
        resolved_directory.relative_to(resolved_specs_dir)
    except ValueError as exc:
        raise FeatureResolutionError(
            f"Feature directory from {source!r} resolves outside specs/: {directory!s}"
        ) from exc
    if repo_root is None:
        return
    try:
        resolved_directory.relative_to(repo_root.resolve())
    except ValueError as exc:
        raise FeatureResolutionError(
            f"Feature directory from {source!r} resolves outside the repository root: {directory!s}"
        ) from exc


def resolve_active_feature(repo_root: Path | None = None) -> ActiveFeature:
    """
    Resolve the active feature directory and branch for SpecKit scaffold commands.

    Resolution order:

    1. ``SPECIFY_FEATURE_DIRECTORY`` environment variable — a feature directory
       name (resolved under ``specs/``) or an explicit relative/absolute path.
    2. ``.specify/feature.json`` — the ``feature_directory`` key.
    3. The current git branch, matched against existing ``specs/<NNN>-*``
       directories by numeric prefix.  Both the legacy ``<number>-description``
       branch format and the repository-standard ``type/ISSUE-KEY/description``
       convention (e.g. ``fix/2249/squash-fix`` or
       ``feature/PROJECT-1234/add-webhook``) are supported.  When no matching
       directory exists yet, the fallback is ``specs/<branch>`` for legacy-format
       branches and ``specs/<number>`` for ``type/ISSUE-KEY/description`` branches.
    4. The highest-numbered existing ``specs/`` directory (non-git fallback).
    5. ``specs/main`` as a final fallback when nothing else resolves.

    Args:
        repo_root: Repository root to resolve against. Defaults to the git
            repository root (or the current working directory outside git).

    Returns:
        ActiveFeature describing the resolved repo root, feature directory,
        branch name, and whether a git repository was detected.

    Raises:
        FeatureResolutionError: If multiple ``specs/`` directories share the
            same numeric prefix as the current branch.
    """
    root = repo_root if repo_root is not None else get_repo_root()
    specs_dir = root / "specs"
    has_git = has_git_repo(root)

    def _build_active_feature(directory: Path, branch: str, *, source: str) -> ActiveFeature:
        _validate_within_specs(directory, specs_dir, source=source, repo_root=root)
        return ActiveFeature(repo_root=root, feature_dir=directory, branch=branch, has_git=has_git)

    env_value = os.environ.get(SPECIFY_FEATURE_DIRECTORY_ENV, "").strip()
    if env_value:
        directory = _resolve_env_directory(specs_dir, root, env_value)
        if len(Path(env_value).parts) == 1:
            return _build_active_feature(directory, directory.name, source=SPECIFY_FEATURE_DIRECTORY_ENV)
        return ActiveFeature(repo_root=root, feature_dir=directory, branch=directory.name, has_git=has_git)

    metadata_value, stored_branch = _read_feature_metadata_snapshot(root)
    if metadata_value:
        directory = _resolve_env_directory(specs_dir, root, metadata_value)
        branch_name = stored_branch if stored_branch else directory.name
        return _build_active_feature(directory, branch_name, source=".specify/feature.json")

    branch = get_current_branch(root) if has_git else None
    if branch:
        prefix = _extract_prefix_from_branch(branch)
        if prefix is not None:
            existing = _find_by_prefix(specs_dir, prefix)
            if existing is not None:
                return _build_active_feature(existing, branch, source="git branch prefix match")
            # For legacy <number>-description branches keep the full branch name as
            # the fallback directory so existing callers are unaffected.  For
            # type/ISSUE-KEY/description branches use just the numeric issue key so
            # the path stays inside specs/ and has a sensible name.
            fallback_dir_name = branch if FEATURE_DIR_PREFIX_RE.match(branch) else prefix
            return _build_active_feature(specs_dir / fallback_dir_name, branch, source="git branch fallback")

    latest = _latest_numbered_feature_dir(specs_dir)
    if latest:
        return _build_active_feature(specs_dir / latest, latest, source="latest numbered spec directory")

    return _build_active_feature(specs_dir / "main", "main", source="main fallback")
