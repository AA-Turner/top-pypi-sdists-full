"""Path validation and bundled-source resolution for skill injection."""

from __future__ import annotations

import re
from pathlib import Path, PurePosixPath

_MANAGED_PREFIX = "agdt."
_MANAGED_README = _MANAGED_PREFIX + "README.md"
_SPECKIT_PREFIX = "speckit."
_LEGACY_AGDT_ENTRY = ".agdt/"
_ALPHA_ONLY_RE = re.compile(r"[^a-zA-Z]")
_SKILLS_KIND = "skills"
_KINDS: tuple[str, ...] = ("agents", "prompts", _SKILLS_KIND)
_SKILL_ENTRY_FILE = "SKILL.md"
_SHARED_SKILL_RESOURCES = frozenset({"fingerprint.py"})
_SKILLS_MANIFEST_MARKER = "<!-- agdt:managed-skills-manifest:v1 -->"
_MANIFEST_ROW_RE = re.compile(r"^\|\s*`([^`]+)`\s*\|")
_SKILL_NAME_RE = re.compile(r"^[a-z0-9](?:-?[a-z0-9])*$")
_BUNDLED_DIR = Path(__file__).parent / "_bundled_skills"


def _flatten_filename(rel_path: Path) -> str:
    """Compute the flat target filename from its relative source path."""
    parts = rel_path.parts
    if len(parts) == 1:
        return parts[0]
    sanitized = [_ALPHA_ONLY_RE.sub("", part) for part in parts[:-1]]
    sanitized = [part for part in sanitized if part]
    if not sanitized:
        return parts[-1]
    return _MANAGED_PREFIX + ".".join(sanitized) + "." + parts[-1]


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
    """Return whether *path* is a managed skill or shared-resource path."""
    rel = PurePosixPath(path)
    if rel.is_absolute() or len(rel.parts) not in {1, 2}:
        return False
    if len(rel.parts) == 1:
        return rel.parts[0] in _SHARED_SKILL_RESOURCES
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
