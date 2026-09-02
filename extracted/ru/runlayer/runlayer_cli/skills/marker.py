"""Stdlib-only marker helpers shared by skill installation and hooks."""

from pathlib import Path

INSTALLED_MARKER = ".installed"
MANAGED_MARKER_PREFIX = "managed:"

# client -> (project_rel, global_rel) skills dirs. Lives here (not
# installer_core) so the hook path can resolve skill dirs without dragging
# yaml/pydantic into its import closure.
SKILLS_DIR_MAP: dict[str, tuple[str, str]] = {
    "claude_code": (".claude/skills", ".claude/skills"),
    "codex": (".codex/skills", ".codex/skills"),
    "cursor": (".cursor/skills", ".cursor/skills"),
    # Goose recommends the shared Agent Skills standard dirs.
    "goose": (".agents/skills", ".agents/skills"),
    # OpenCode reads skills directly from `.agents/skills/<name>/SKILL.md`.
    # Use canonical dir as the editor dir (no symlinks needed).
    "opencode": (".agents/skills", ".agents/skills"),
    # VS Code reads project and user skills from `.agents/skills`.
    "vscode": (".agents/skills", ".agents/skills"),
    # Zed reads project and user skills directly from `.agents/skills`.
    "zed": (".agents/skills", ".agents/skills"),
}

CANONICAL_BASE = ".agents/skills"


def managed_marker(skill_dir: Path) -> str | None:
    """Raw ``managed:<skill_id>:<identifier>`` marker content, or ``None``.

    ``None`` for user installs (empty marker from ``runlayer skills add``),
    hand-made dirs (no marker), and unreadable markers. Copy-mode editor
    entries inherit the full marker, so comparing raw markers detects a
    stale copy after a content update.
    """
    try:
        content = (skill_dir / INSTALLED_MARKER).read_text(encoding="utf-8").strip()
    except OSError:
        return None
    if content.startswith(MANAGED_MARKER_PREFIX) and content != MANAGED_MARKER_PREFIX:
        return content
    return None


def managed_marker_skill_id(skill_dir: Path) -> str | None:
    marker = managed_marker(skill_dir)
    if marker is None:
        return None
    return marker[len(MANAGED_MARKER_PREFIX) :].split(":", 1)[0] or None
