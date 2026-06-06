"""Discover skills (directories containing SKILL.md) on a device."""

from __future__ import annotations

import functools
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import structlog

from runlayer_cli.scan.file_collector import CollectedFile, collect_files
from runlayer_cli.skill_identifier import SkillFileInput, compute_skill_identifier
from runlayer_cli.skills.discovery import _parse_frontmatter

logger = structlog.get_logger(__name__)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

SUPPORTED_EXTENSIONS = {".md", ".mdc", ".txt", ".sh", ".py", ".js", ".ts"}

DEPENDENCY_DIRS = {"node_modules", ".venv", "venv", "vendor", "dist", ".tox"}

ARTIFACT_SKILL_MD = "skill_md"

SKILL_SEARCH_FILENAMES: list[str] = ["SKILL.md"]

# Global (home-directory) skill paths: (relative_to_home, tool)
_GLOBAL_SKILL_DIRS: list[tuple[str, str]] = [
    (".claude/skills", "claude_code"),
    (".agents/skills", "multi"),
    (".codex/skills", "codex"),
    (".config/opencode/skills", "opencode"),
    (".agent/skills", "multi"),
    (".skillport/skills", "skillport"),
    (".copilot/skills", "github_copilot_cli"),
    (".cline/skills", "cline"),
    (".warp/skills", "warp"),
]

# Home-level dot-directories → tool identifier for user-scope skills
_HOME_CLIENT_TOOL_MAP: dict[str, str] = {
    ".cursor": "cursor",
    ".claude": "claude_code",
    ".codex": "codex",
    ".codeium": "windsurf",
    ".windsurf": "windsurf",
    ".agents": "multi",
    ".agent": "multi",
    ".skillport": "skillport",
    ".copilot": "github_copilot_cli",
    ".cline": "cline",
    ".warp": "warp",
}

# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------


SkillFile = CollectedFile


@dataclass
class DiscoveredSkillArtifact:
    """A skill artifact found on disk (directory containing SKILL.md)."""

    name: str
    path: str
    artifact_type: str
    scope: str  # "global" | "project" | "user"
    tool: str
    project_path: str | None = None
    identifier: str | None = None
    description: str | None = None
    has_scripts: bool = False
    file_count: int = 0
    files: list[SkillFile] = field(default_factory=list)
    oversized: bool = False
    symlinks_found: list[str] = field(default_factory=list)
    git_remote_url: str | None = None
    is_dependency: bool = False
    source_type: str = "user"
    source_plugin_identifier: str | None = None

    def to_api_payload(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "identifier": self.identifier,
            "name": self.name,
            "path": self.path,
            "artifact_type": self.artifact_type,
            "scope": self.scope,
            "tool": self.tool,
            "project_path": self.project_path,
            "description": self.description,
            "has_scripts": self.has_scripts,
            "file_count": self.file_count,
            "oversized": self.oversized,
            "symlinks_found": self.symlinks_found,
            "git_remote_url": self.git_remote_url,
            "is_dependency": self.is_dependency,
            "source_type": self.source_type,
            "files": [{"title": f.title, "content": f.content} for f in self.files],
        }
        if self.source_plugin_identifier is not None:
            payload["source_plugin_identifier"] = self.source_plugin_identifier
        return payload


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _is_dependency_path(path: Path) -> bool:
    parts = set(path.parts)
    return bool(parts & DEPENDENCY_DIRS)


def _classify_source_type(path: Path, scope: str) -> str:
    if _is_dependency_path(path):
        return "dependency"
    if scope == "global":
        return "installed"
    return "user"


@functools.lru_cache(maxsize=512)
def _git_remote_for_dir(dir_path_str: str) -> str | None:
    try:
        result = subprocess.run(
            ["git", "-C", dir_path_str, "remote", "get-url", "origin"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        return result.stdout.strip() if result.returncode == 0 else None
    except Exception:
        return None


def _get_git_remote(path: Path) -> str | None:
    """Return the ``origin`` remote URL for the repo containing *path*."""
    dir_path = path if path.is_dir() else path.parent
    return _git_remote_for_dir(str(dir_path))


def _find_owning_plugin(
    path: Path,
    plugin_path_map: dict[Path, str],
) -> str | None:
    """Longest-prefix match of *path* against known plugin install paths."""
    resolved = path.resolve()
    best: str | None = None
    best_len = 0
    for install_path, identifier in plugin_path_map.items():
        try:
            resolved.relative_to(install_path)
        except ValueError:
            continue
        if len(install_path.parts) > best_len:
            best_len = len(install_path.parts)
            best = identifier
    return best


def _collect_files_safe(
    skill_dir: Path,
) -> tuple[list[SkillFile], list[str], bool]:
    """Collect files from a skill directory with safety checks."""
    return collect_files(skill_dir, SUPPORTED_EXTENSIONS, skip_dirs=set())


def _compute_identifier(files: list[SkillFile]) -> str | None:
    if not files:
        return None
    try:
        inputs = [SkillFileInput(name=f.title, content=f.content) for f in files]
        result = compute_skill_identifier(inputs)
        return result.root
    except Exception:
        logger.warning("skill_identifier_failed", exc_info=True)
        return None


# ---------------------------------------------------------------------------
# SKILL.md directory scanner
# ---------------------------------------------------------------------------


def _scan_skill_md_dir(
    skill_dir: Path,
    scope: str,
    tool: str,
    project_path: str | None = None,
) -> DiscoveredSkillArtifact | None:
    """Build a ``DiscoveredSkillArtifact`` from a directory containing SKILL.md."""
    marker = skill_dir / "SKILL.md"
    try:
        marker_content = marker.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return None

    fm = _parse_frontmatter(marker_content)
    name = fm.get("name")
    if not name:
        name = skill_dir.name
    name = str(name)[:100]
    description = fm.get("description")
    if description is not None:
        description = str(description)[:1024]

    has_scripts = (skill_dir / "scripts").is_dir()
    files, symlinks, oversized = _collect_files_safe(skill_dir)
    identifier = _compute_identifier(files)
    abs_path = Path(skill_dir).resolve()

    return DiscoveredSkillArtifact(
        name=name,
        path=str(abs_path),
        artifact_type=ARTIFACT_SKILL_MD,
        scope=scope,
        tool=tool,
        project_path=project_path,
        identifier=identifier,
        description=description,
        has_scripts=has_scripts,
        file_count=len(files),
        files=files,
        oversized=oversized,
        symlinks_found=symlinks,
        git_remote_url=_get_git_remote(abs_path),
        is_dependency=_is_dependency_path(abs_path),
        source_type=_classify_source_type(abs_path, scope),
    )


# ---------------------------------------------------------------------------
# Global (home-directory) skill scanning
# ---------------------------------------------------------------------------


def scan_global_skills() -> list[DiscoveredSkillArtifact]:
    """Walk known home-directory skill paths and return discovered artifacts."""
    _git_remote_for_dir.cache_clear()
    home = Path.home()
    results: list[DiscoveredSkillArtifact] = []

    for rel_dir, tool in _GLOBAL_SKILL_DIRS:
        skills_root = home / rel_dir
        if not skills_root.is_dir():
            continue
        try:
            subdirs = sorted(skills_root.iterdir())
        except OSError:
            continue
        for subdir in subdirs:
            if not subdir.is_dir():
                continue
            if not (subdir / "SKILL.md").exists():
                continue
            artifact = _scan_skill_md_dir(subdir, scope="global", tool=tool)
            if artifact:
                results.append(artifact)

    logger.info("Global skill scan complete", found=len(results))
    return results


# ---------------------------------------------------------------------------
# Project-level skill scanning (from pre-crawled paths)
# ---------------------------------------------------------------------------


def _infer_project_root(fpath: Path) -> str:
    """Best-effort project root from a SKILL.md file path."""
    skill_dir = fpath.parent
    container = skill_dir.parent
    if container.name == "skills":
        tool_dir = container.parent
        if tool_dir.name.startswith("."):
            return str(tool_dir.parent)
        return str(tool_dir)
    return str(skill_dir.parent)


def _is_under_global_prefix(fpath: Path, prefixes: set[Path]) -> bool:
    resolved = fpath.resolve()
    return any(resolved == p or resolved.is_relative_to(p) for p in prefixes)


def _infer_home_client_tool(fpath: Path) -> str | None:
    """If *fpath* is under ``$HOME/.<client>/``, return the tool identifier."""
    home = Path.home()
    try:
        rel = fpath.resolve().relative_to(home.resolve())
    except ValueError:
        return None
    if rel.parts:
        return _HOME_CLIENT_TOOL_MAP.get(rel.parts[0])
    return None


def process_skill_paths(found_paths: list[Path]) -> list[DiscoveredSkillArtifact]:
    """Process pre-crawled paths and return project-level skill artifacts.

    Only SKILL.md files are recognised. Each SKILL.md triggers a scan of its
    parent directory as a skill.

    Paths under known global skill directories are excluded; those are
    handled separately by ``scan_global_skills``.
    """
    _git_remote_for_dir.cache_clear()
    results: list[DiscoveredSkillArtifact] = []
    seen_skill_dirs: set[str] = set()
    global_prefixes = _get_global_skill_path_prefixes()

    for fpath in found_paths:
        if fpath.name != "SKILL.md":
            continue

        if _is_under_global_prefix(fpath, global_prefixes):
            continue

        skill_dir = fpath.parent
        dir_key = str(skill_dir.resolve())
        if dir_key in seen_skill_dirs:
            continue
        seen_skill_dirs.add(dir_key)

        home_tool = _infer_home_client_tool(fpath)
        if home_tool is not None:
            scope = "user"
            tool = home_tool
            project_root = None
        else:
            scope = "project"
            tool = "multi"
            project_root = _infer_project_root(fpath)

        artifact = _scan_skill_md_dir(
            skill_dir,
            scope=scope,
            tool=tool,
            project_path=project_root,
        )
        if artifact:
            results.append(artifact)

    logger.info("Project skill scan complete", found=len(results))
    return results


def _get_global_skill_path_prefixes() -> set[Path]:
    """Resolved paths that ``scan_global_skills`` owns.

    Any file under these prefixes should be excluded from
    ``process_skill_paths`` to avoid double-counting.
    """
    home = Path.home()
    prefixes: set[Path] = set()
    for rel_dir, _ in _GLOBAL_SKILL_DIRS:
        prefixes.add((home / rel_dir).resolve())
    return prefixes


def tag_skills_with_plugins(
    skills: list[DiscoveredSkillArtifact],
    plugin_path_map: dict[Path, str],
) -> None:
    """Post-process: set source_plugin_identifier via longest-prefix match."""
    if not plugin_path_map:
        return
    for skill in skills:
        owner = _find_owning_plugin(Path(skill.path), plugin_path_map)
        if owner:
            skill.source_plugin_identifier = owner


def get_skill_search_filenames() -> list[str]:
    """Return the list of filenames the unified find crawl should include."""
    return list(SKILL_SEARCH_FILENAMES)
