"""Discover skills (directories containing SKILL.md) on a device."""

from __future__ import annotations

import threading
from collections.abc import Callable, Sequence
from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath
from typing import Any

import structlog

from runlayer_cli.scan import scan_state
from runlayer_cli.scan.file_collector import CollectedFile, collect_files
from runlayer_cli.skill_identifier import SkillFileInput, compute_skill_identifier
from runlayer_cli.skills.discovery import (
    SUPPORTED_EXTENSIONS as REGISTRY_SUPPORTED_EXTENSIONS,
    parse_frontmatter,
)

from runlayer_cli.paths import strip_reported_path_prefix

logger = structlog.get_logger(__name__)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

SUPPORTED_EXTENSIONS = REGISTRY_SUPPORTED_EXTENSIONS | {".mdc"}

DEPENDENCY_DIRS = {"node_modules", ".venv", "venv", "vendor", "dist", ".tox"}

ARTIFACT_SKILL_MD = "skill_md"

SKILL_MARKER_NAME = "SKILL.md"

SKILL_SEARCH_FILENAMES: list[str] = [SKILL_MARKER_NAME]


def is_skill_marker_name(name: str) -> bool:
    """Case-insensitive SKILL.md basename check.

    Skills renamed to ``skill.md`` / ``Skill.md`` (case-insensitive
    filesystems, or deliberate casing evasion) must still be discovered; the
    backend normalizes the marker name on import.
    """
    return name.lower() == "skill.md"


def find_skill_marker(skill_dir: Path) -> Path | None:
    """Resolve the on-disk SKILL.md marker in *skill_dir*, any casing.

    Prefers the exact canonical name so a dir holding both ``SKILL.md`` and
    ``skill.md`` (case-sensitive filesystems) resolves deterministically.
    """
    exact = skill_dir / SKILL_MARKER_NAME
    try:
        if exact.is_file():
            return exact
        entries = sorted(skill_dir.iterdir())
    except OSError:
        return None
    for entry in entries:
        try:
            if is_skill_marker_name(entry.name) and entry.is_file():
                return entry
        except OSError:
            continue
    return None


def has_skill_structure(content: str) -> bool:
    """Content-level skill identity: frontmatter with name + description + body.

    The structural signature is the invariant a rename cannot change: a skill
    authored as loose markdown (or copied under a disguise name) still needs
    this shape to function as a skill.
    """
    lines = content.splitlines()
    if not lines or lines[0].strip() != "---":
        return False
    try:
        close_index = lines[1:].index("---") + 1
    except ValueError:
        return False
    frontmatter = parse_frontmatter(content)
    name = frontmatter.get("name")
    description = frontmatter.get("description")
    body = "\n".join(lines[close_index + 1 :]).strip()
    return (
        isinstance(name, str)
        and bool(name.strip())
        and isinstance(description, str)
        and bool(description.strip())
        and bool(body)
    )


# Per-run processing cap. Skill-heavy hosts (agent session copies) can hold
# 100k+ SKILL.md dirs; one run processes at most this many and a persisted
# rotation cursor (``scan_state``) covers the rest over successive runs.
MAX_SKILL_ARTIFACTS_PER_RUN = 1000

# Shared budget for retained skill file content across the global + project
# phases (they run in parallel). Past it, artifacts keep metadata only.
# Retained size uses ``len(str)`` as a cheap code-point approximation.
MAX_TOTAL_SKILL_FILE_BYTES = 64 * 1024 * 1024

# Bound small metadata reads that happen before ``collect_files`` applies its
# own per-file cap. Git pointers/configs are normally only a few KiB.
MAX_SCAN_METADATA_FILE_BYTES = 1_048_576

_ROTATION_CATEGORY = "skills"
_GLOBAL_ROTATION_CATEGORY = "global_skills"
_CONTENT_ROTATION_CATEGORY = "skill_content"

# Global (home-directory) skill paths: (relative_to_home, tool)
_GLOBAL_SKILL_DIRS: list[tuple[str, str]] = [
    (".claude/skills", "claude_code"),
    (
        "Library/Application Support/Claude/local-agent-mode-sessions/"
        "skills-plugin/*/*/skills",
        "claude_desktop",
    ),
    (
        "AppData/Roaming/Claude/local-agent-mode-sessions/skills-plugin/*/*/skills",
        "claude_desktop",
    ),
    (
        "AppData/Local/Packages/Claude_pzs8sxrjxfjjc/LocalCache/Roaming/"
        "Claude/local-agent-mode-sessions/skills-plugin/*/*/skills",
        "claude_desktop",
    ),
    (
        ".config/Claude/local-agent-mode-sessions/skills-plugin/*/*/skills",
        "claude_desktop",
    ),
    (".agents/skills", "multi"),
    (".codex/skills", "codex"),
    (".config/opencode/skills", "opencode"),
    (".agent/skills", "multi"),
    (".skillport/skills", "skillport"),
    (".copilot/skills", "github_copilot_cli"),
    (".cline/skills", "cline"),
    (".warp/skills", "warp"),
    (".kimi-code/skills", "kimi_code"),
    (".pi/agent/skills", "pi"),
    (".junie/skills", "junie"),
    (".kilo/skills", "kilo_code"),
    (".kilocode/skills", "kilo_code"),
    (".config/devin/skills", "devin_cli"),
    ("AppData/Roaming/devin/skills", "devin_cli"),
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
    ".kimi-code": "kimi_code",
    ".pi": "pi",
    ".junie": "junie",
    ".kilo": "kilo_code",
    ".kilocode": "kilo_code",
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
    container_id: str | None = None
    container_name: str | None = None
    container_image_ref: str | None = None
    container_image_digest: str | None = None
    container_runtime: str | None = None
    container_is_devcontainer: bool = False
    container_is_running: bool = True
    container_labels: dict[str, str] = field(default_factory=dict)
    container_mounts_host_home: bool = False
    wsl_distro: str | None = None
    wsl_user: str | None = None

    def to_api_payload(self) -> dict[str, Any]:
        is_container = self.container_id is not None
        path = self.path if is_container else strip_reported_path_prefix(self.path)
        project_path = (
            self.project_path
            if is_container
            else strip_reported_path_prefix(self.project_path)
        )
        symlinks_found = (
            list(self.symlinks_found)
            if is_container
            else [strip_reported_path_prefix(path) for path in self.symlinks_found]
        )
        payload: dict[str, Any] = {
            "identifier": self.identifier,
            "name": self.name,
            "path": path,
            "artifact_type": self.artifact_type,
            "scope": self.scope,
            "tool": self.tool,
            "project_path": project_path,
            "description": self.description,
            "has_scripts": self.has_scripts,
            "file_count": self.file_count,
            "oversized": self.oversized,
            "symlinks_found": symlinks_found,
            "git_remote_url": self.git_remote_url,
            "is_dependency": self.is_dependency,
            "source_type": self.source_type,
            "files": [{"title": f.title, "content": f.content} for f in self.files],
        }
        if self.source_plugin_identifier is not None:
            payload["source_plugin_identifier"] = self.source_plugin_identifier
        if self.wsl_distro is not None and self.container_id is None:
            payload["wsl"] = {
                "distro": self.wsl_distro,
                "user": self.wsl_user,
            }
        if self.container_id is not None:
            payload["container"] = {
                "container_id": self.container_id,
                "name": self.container_name,
                "image_ref": self.container_image_ref,
                "image_digest": self.container_image_digest,
                "runtime": self.container_runtime or "docker",
                "is_devcontainer": self.container_is_devcontainer,
                "is_running": self.container_is_running,
                "labels": dict(self.container_labels),
                "mounts_host_home": self.container_mounts_host_home,
            }
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


# Zero-fork git remote resolution. Forking ``git remote get-url`` per skill
# dir melts down on skill-heavy hosts (one process per 100k+ dirs), so the
# origin URL is read straight from ``.git/config`` with two caches: every
# visited ancestor dir -> repo root, and repo root -> origin URL.

_git_cache_lock = threading.Lock()
# Cleared per scan; starting directories are bounded by the global + project
# ``MAX_SKILL_ARTIFACTS_PER_RUN`` windows, plus their finite ancestor chains.
_repo_root_cache: dict[str, str | None] = {}
_origin_url_cache: dict[str, str | None] = {}


def _read_bounded_text(path: Path, *, errors: str = "strict") -> str | None:
    """Read at most ``MAX_SCAN_METADATA_FILE_BYTES`` from *path*."""
    try:
        if path.stat().st_size > MAX_SCAN_METADATA_FILE_BYTES:
            return None
        with path.open("rb") as handle:
            raw = handle.read(MAX_SCAN_METADATA_FILE_BYTES + 1)
        if len(raw) > MAX_SCAN_METADATA_FILE_BYTES:
            return None
        return raw.decode("utf-8", errors=errors)
    except (OSError, UnicodeDecodeError):
        return None


def clear_git_remote_cache() -> None:
    """Clear per-scan git-remote memoization before concurrent skill work."""
    with _git_cache_lock:
        _repo_root_cache.clear()
        _origin_url_cache.clear()


def _find_repo_root(start: Path) -> Path | None:
    """Walk up from *start* to the nearest dir containing ``.git``.

    Stat-only, and caches the answer for every visited ancestor so sibling
    skill dirs in the same repo resolve without touching the filesystem.
    """
    visited: list[str] = []
    current = start
    root: str | None = None
    while True:
        key = str(current)
        with _git_cache_lock:
            if key in _repo_root_cache:
                root = _repo_root_cache[key]
                break
        visited.append(key)
        try:
            if (current / ".git").exists():
                root = key
                break
        except OSError:
            # Provenance is best-effort. Cache this subtree's miss so a
            # transiently unreadable ancestor is not restatted for every skill.
            break
        parent = current.parent
        if parent == current:
            break
        current = parent
    if visited:
        with _git_cache_lock:
            for key in visited:
                _repo_root_cache[key] = root
    return Path(root) if root is not None else None


def _resolve_git_config_path(repo_root: Path) -> Path | None:
    """Locate the config file for *repo_root*, following gitdir indirection.

    Linked worktrees and submodules use a ``.git`` *file* with a ``gitdir:``
    pointer; linked worktrees additionally keep the shared config next to a
    ``commondir`` pointer inside that git dir.
    """
    dot_git = repo_root / ".git"
    if dot_git.is_dir():
        git_dir = dot_git
    elif dot_git.is_file():
        dot_git_text = _read_bounded_text(dot_git, errors="replace")
        if dot_git_text is None:
            return None
        first_line = dot_git_text.split("\n", 1)[0]
        if not first_line.startswith("gitdir:"):
            return None
        target = Path(first_line[len("gitdir:") :].strip())
        git_dir = target if target.is_absolute() else (repo_root / target).resolve()
    else:
        return None

    commondir = git_dir / "commondir"
    if commondir.is_file():
        commondir_text = _read_bounded_text(commondir, errors="replace")
        if commondir_text is None:
            return None
        rel = commondir_text.strip()
        common = Path(rel)
        if not common.is_absolute():
            common = (git_dir / rel).resolve()
        return common / "config"
    return git_dir / "config"


def _is_remote_origin_header(line: str) -> bool:
    end = line.find("]")
    inner = line[1:end] if end != -1 else line[1:]
    parts = inner.strip().split(None, 1)
    return (
        len(parts) == 2
        and parts[0].lower() == "remote"
        and parts[1].strip() == '"origin"'
    )


def _parse_origin_url(config_text: str) -> str | None:
    """Extract ``[remote "origin"] url`` from git-config text.

    Hand-rolled because git config is INI-*like* but not configparser
    compatible (tab-indented keys, duplicate sections, subsection quoting).
    """
    in_origin = False
    for raw_line in config_text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith(("#", ";")):
            continue
        if line.startswith("["):
            in_origin = _is_remote_origin_header(line)
            continue
        if in_origin:
            key, sep, value = line.partition("=")
            if sep and key.strip().lower() == "url":
                value = value.strip()
                in_quotes = False
                escaped = False
                for index, char in enumerate(value):
                    if escaped:
                        escaped = False
                    elif char == "\\":
                        escaped = True
                    elif char == '"':
                        in_quotes = not in_quotes
                    elif char in "#;" and not in_quotes:
                        value = value[:index].rstrip()
                        break
                if len(value) >= 2 and value.startswith('"') and value.endswith('"'):
                    value = value[1:-1]
                return value or None
    return None


def _read_origin_url(repo_root: Path) -> str | None:
    """Read opaque provenance metadata directly from the repo-local config.

    Deliberately skips config includes and ``url.*.insteadOf`` expansion; the
    value is reported as metadata and is never used for a Git operation.
    """
    config_path = _resolve_git_config_path(repo_root)
    if config_path is None:
        return None
    config_text = _read_bounded_text(config_path, errors="replace")
    return _parse_origin_url(config_text) if config_text is not None else None


def _get_git_remote(path: Path) -> str | None:
    """Return the ``origin`` remote URL for the repo containing *path*.

    Never forks: parse failures of any kind resolve to ``None``.
    """
    dir_path = path if path.is_dir() else path.parent
    repo_root = _find_repo_root(dir_path)
    if repo_root is None:
        return None
    root_key = str(repo_root)
    with _git_cache_lock:
        if root_key in _origin_url_cache:
            return _origin_url_cache[root_key]
    try:
        url = _read_origin_url(repo_root)
    except Exception:
        url = None
    with _git_cache_lock:
        _origin_url_cache[root_key] = url
    return url


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
    """Collect files from a skill directory with safety checks.

    Uses the default content skip set so dependency junk vendored *inside* a
    skill dir (``node_modules/``, ``.venv/``, ...) is never read into memory.
    Excluded content also stays out of the persisted skill fingerprint, keeping
    dependency churn from changing skill identity.
    """
    return collect_files(skill_dir, SUPPORTED_EXTENSIONS)


# Streaming retention state, shared across the global + project skill phases
# (which run in parallel pool threads). ``_retained_identifiers`` holds the
# identifiers whose file content is already retained by some artifact this
# scan, so duplicate copies drop their content at collection time instead of
# all staying resident until the phase-end strip.

_retention_lock = threading.Lock()
_retained_identifiers: set[str] = set()
_retained_bytes = 0
_content_offset = 0
_content_skip_remaining = 0
_content_admitted = 0
_content_capped = False


def reset_skill_scan_state(state_path: Path | None = None) -> None:
    """Reset per-scan retention state and load the cross-run content offset."""
    global _retained_bytes, _content_offset, _content_skip_remaining
    global _content_admitted, _content_capped
    offset = scan_state.load_content_offset(_CONTENT_ROTATION_CATEGORY, state_path)
    with _retention_lock:
        _retained_identifiers.clear()
        _retained_bytes = 0
        _content_offset = offset
        _content_skip_remaining = offset
        _content_admitted = 0
        _content_capped = False


def finalize_skill_scan_state(state_path: Path | None = None) -> None:
    """Advance content retention after a completed scan.

    Skill phases interleave in worker threads, so the exact retained slice can
    vary, but advancing by the contiguous admitted count still prevents a fixed
    sorted-order tail from starving across runs. Aborted scans never call this.
    """
    with _retention_lock:
        offset = _content_offset
        admitted = _content_admitted
        capped = _content_capped

    if capped:
        scan_state.save_content_offset(
            _CONTENT_ROTATION_CATEGORY,
            offset + admitted,
            state_path,
        )
    elif offset != 0:
        scan_state.save_content_offset(_CONTENT_ROTATION_CATEGORY, 0, state_path)


def apply_retention_policy(artifact: DiscoveredSkillArtifact) -> None:
    """Drop *artifact*'s file content when it is a duplicate or over budget.

    Metadata (identifier, file_count, paths) always survives. A persisted
    content offset advances the admitted slice after a completed capped run, so
    a deterministic scan order cannot starve the same tail forever.
    """
    global _retained_bytes, _content_skip_remaining, _content_admitted
    global _content_capped
    if not artifact.files:
        return
    size = sum(len(f.content) for f in artifact.files)
    with _retention_lock:
        identifier = artifact.identifier
        if identifier is not None and identifier in _retained_identifiers:
            artifact.files = []
            return
        if _content_capped:
            artifact.files = []
            artifact.oversized = True
            return
        if _content_skip_remaining > 0:
            _content_skip_remaining -= 1
            artifact.files = []
            artifact.oversized = True
            return
        if _retained_bytes + size > MAX_TOTAL_SKILL_FILE_BYTES:
            artifact.files = []
            artifact.oversized = True
            _content_capped = True
            return
        _retained_bytes += size
        _content_admitted += 1
        if identifier is not None:
            _retained_identifiers.add(identifier)


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


def build_skill_artifact_from_files(
    *,
    skill_path: str,
    files: list[SkillFile] | dict[str, bytes],
    scope: str,
    tool: str,
    marker_content: str | None = None,
    project_path: str | None = None,
    fallback_name: str | None = None,
    has_scripts: bool | None = None,
    oversized: bool = False,
    symlinks_found: list[str] | None = None,
    git_remote_url: str | None = None,
    is_dependency: bool = False,
    source_type: str = "user",
    container_id: str | None = None,
    container_name: str | None = None,
    container_image_ref: str | None = None,
    container_image_digest: str | None = None,
    container_runtime: str | None = None,
    container_is_devcontainer: bool = False,
    container_is_running: bool = True,
    container_labels: dict[str, str] | None = None,
    container_mounts_host_home: bool = False,
) -> DiscoveredSkillArtifact | None:
    """Build an artifact from collected text files or container file bytes."""
    if isinstance(files, dict):
        collected_files: list[SkillFile] = []
        for title, content in sorted(files.items()):
            if PurePosixPath(title).suffix.lower() not in SUPPORTED_EXTENSIONS:
                continue
            try:
                text = content.decode("utf-8")
            except UnicodeDecodeError:
                continue
            collected_files.append(SkillFile(title=title, content=text))
        files = collected_files

    if marker_content is None:
        marker_content = next(
            (file.content for file in files if file.title == SKILL_MARKER_NAME),
            None,
        )
    if marker_content is None:
        marker_content = next(
            (file.content for file in files if is_skill_marker_name(file.title)),
            None,
        )
    if marker_content is None:
        return None
    if has_scripts is None:
        has_scripts = any(file.title.startswith("scripts/") for file in files)

    fm = parse_frontmatter(marker_content)
    name = fm.get("name") or fallback_name or PurePosixPath(skill_path).name
    description = fm.get("description")
    if description is not None:
        description = str(description)[:1024]

    return DiscoveredSkillArtifact(
        name=str(name)[:100],
        path=skill_path,
        artifact_type=ARTIFACT_SKILL_MD,
        scope=scope,
        tool=tool,
        project_path=project_path,
        identifier=_compute_identifier(files),
        description=description,
        has_scripts=has_scripts,
        file_count=len(files),
        files=files,
        oversized=oversized,
        symlinks_found=list(symlinks_found or []),
        git_remote_url=git_remote_url,
        is_dependency=is_dependency,
        source_type=source_type,
        container_id=container_id,
        container_name=container_name,
        container_image_ref=container_image_ref,
        container_image_digest=container_image_digest,
        container_runtime=container_runtime,
        container_is_devcontainer=container_is_devcontainer,
        container_is_running=container_is_running,
        container_labels=dict(container_labels or {}),
        container_mounts_host_home=container_mounts_host_home,
    )


def strip_duplicate_skill_files(
    skills: list[DiscoveredSkillArtifact],
) -> list[DiscoveredSkillArtifact]:
    """Keep files only on the first artifact *with files* per identifier.

    Collection-time dedupe (``apply_retention_policy``) may already have
    emptied an earlier copy's files, so "first in list" is not necessarily the
    artifact carrying content; keying on the first that has files keeps
    exactly one content payload per identifier.
    """
    seen_identifiers: set[str] = set()
    for skill in skills:
        identifier = skill.identifier
        if identifier is None:
            continue
        if identifier in seen_identifiers:
            skill.files = []
        elif skill.files:
            seen_identifiers.add(identifier)
    return skills


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
    marker = find_skill_marker(skill_dir)
    if marker is None:
        return None
    marker_content = _read_bounded_text(marker)
    if marker_content is None:
        return None

    has_scripts = (skill_dir / "scripts").is_dir()
    files, symlinks, oversized = _collect_files_safe(skill_dir)
    # Canonicalize a case-variant marker title so content identity and
    # backend dedupe match the same skill discovered under the exact name.
    if not any(file.title == SKILL_MARKER_NAME for file in files):
        for file in files:
            if is_skill_marker_name(file.title):
                file.title = SKILL_MARKER_NAME
                break
    abs_path = Path(skill_dir).resolve()
    is_dependency = _is_dependency_path(abs_path)

    artifact = build_skill_artifact_from_files(
        skill_path=str(abs_path),
        marker_content=marker_content,
        files=files,
        scope=scope,
        tool=tool,
        project_path=project_path,
        has_scripts=has_scripts,
        oversized=oversized,
        symlinks_found=symlinks,
        git_remote_url=_get_git_remote(abs_path),
        is_dependency=is_dependency,
        source_type=_classify_source_type(abs_path, scope),
        fallback_name=skill_dir.name,
    )
    if artifact is not None:
        apply_retention_policy(artifact)
    return artifact


_LOOSE_MD_SNIFF_BYTES = 16


def _loose_md_has_frontmatter_prefix(path: Path) -> bool:
    """Cheap pre-filter so most junk markdown skips the bounded full read."""
    try:
        with path.open("rb") as handle:
            prefix = handle.read(_LOOSE_MD_SNIFF_BYTES)
    except OSError:
        return False
    lines = prefix.splitlines()
    return bool(lines) and lines[0].strip() == b"---"


def _loose_md_is_structural_skill(path: Path) -> bool:
    """Discovery gate: full structural identity before the rotation window.

    Directory candidates must hold a real SKILL.md marker to enter the
    rotation window; loose files must clear the equivalent content bar. A
    prefix-only sniff would let planted frontmatter junk consume
    ``MAX_SKILL_ARTIFACTS_PER_RUN`` slots shared with real skills, delaying
    their discovery across successive runs.
    """
    if not _loose_md_has_frontmatter_prefix(path):
        return False
    content = _read_bounded_text(path)
    return content is not None and has_skill_structure(content)


def _scan_loose_skill_md_file(
    md_file: Path,
    scope: str,
    tool: str,
) -> DiscoveredSkillArtifact | None:
    """Build an artifact from a loose markdown skill, classified by content.

    Skills authored directly under a known skill root (no wrapping directory,
    arbitrary filename) are identified by their structural signature, never by
    filename. The single file is normalized to the SKILL.md title so backend
    identity matches the same content discovered in canonical layout.
    """
    content = _read_bounded_text(md_file)
    if content is None or not has_skill_structure(content):
        return None
    abs_path = Path(md_file).resolve()
    artifact = build_skill_artifact_from_files(
        skill_path=str(abs_path),
        files=[SkillFile(title=SKILL_MARKER_NAME, content=content)],
        marker_content=content,
        scope=scope,
        tool=tool,
        fallback_name=md_file.stem or md_file.name,
        git_remote_url=_get_git_remote(abs_path.parent),
        is_dependency=_is_dependency_path(abs_path),
        source_type=_classify_source_type(abs_path, scope),
    )
    if artifact is not None:
        apply_retention_policy(artifact)
    return artifact


# ---------------------------------------------------------------------------
# Global (home-directory) skill scanning
# ---------------------------------------------------------------------------


def _expand_global_skill_dirs(home: Path, rel_dir: str) -> list[Path]:
    """Expand wildcard global roots while preserving direct path handling."""
    if not any(char in rel_dir for char in "*?["):
        return [home / rel_dir]
    try:
        return sorted(home.glob(rel_dir))
    except OSError:
        return []


def scan_global_skills(
    extra_home_roots: Sequence[Path] = (),
    *,
    checkpoint: Callable[[], None] | None = None,
    state_path: Path | None = None,
) -> list[DiscoveredSkillArtifact]:
    """Walk known home-directory skill paths and return discovered artifacts.

    At most ``MAX_SKILL_ARTIFACTS_PER_RUN`` directories are processed per run
    (independently of the project phase's cap, since the two run in parallel).
    Global dirs are normally a tiny set, but when they exceed the cap a
    rotation cursor persisted at *state_path* (default
    ``~/.runlayer/scan-state.json``, category ``global_skills``) picks this
    run's window so successive runs cover every directory — same contract as
    ``process_skill_paths``: the cursor advances only after the selected
    window completes, and under the cap no artifact-window cursor is read or
    written.
    *checkpoint* is the resource governor's cooperative throttle/abort hook,
    called once per skill directory.
    """
    candidates: list[tuple[str, Path, str, bool]] = []
    seen_skill_dirs: set[str] = set()

    for home in (Path.home(), *extra_home_roots):
        for rel_dir, tool in _GLOBAL_SKILL_DIRS:
            for skills_root in _expand_global_skill_dirs(home, rel_dir):
                if not skills_root.is_dir():
                    continue
                try:
                    entries = sorted(skills_root.iterdir())
                except OSError:
                    continue
                for entry in entries:
                    if entry.is_dir():
                        if find_skill_marker(entry) is None:
                            continue
                        is_loose_file = False
                    elif (
                        entry.suffix.lower() == ".md"
                        and entry.is_file()
                        and _loose_md_is_structural_skill(entry)
                    ):
                        # Loose markdown directly under a known skill root:
                        # a skill authored without its wrapping directory.
                        # Classified by content structure, never by filename.
                        is_loose_file = True
                    else:
                        continue
                    entry_key = str(entry.resolve())
                    if entry_key in seen_skill_dirs:
                        continue
                    seen_skill_dirs.add(entry_key)
                    candidates.append((entry_key, entry, tool, is_loose_file))

    total_found = len(candidates)
    new_cursor: str | None = None
    if total_found > MAX_SKILL_ARTIFACTS_PER_RUN:
        by_key = {
            key: (entry, tool, is_loose_file)
            for key, entry, tool, is_loose_file in candidates
        }
        cursor = scan_state.load_cursor(_GLOBAL_ROTATION_CATEGORY, state_path)
        window, new_cursor = scan_state.rotation_window(
            sorted(by_key), cursor, MAX_SKILL_ARTIFACTS_PER_RUN
        )
        candidates = [(key, *by_key[key]) for key in window]
        logger.warning(
            "global_skill_scan_window_rotated",
            total_found=total_found,
            processed=len(candidates),
            cursor=new_cursor,
        )

    results: list[DiscoveredSkillArtifact] = []
    for _entry_key, entry, tool, is_loose_file in candidates:
        if checkpoint is not None:
            checkpoint()
        artifact = (
            _scan_loose_skill_md_file(entry, scope="global", tool=tool)
            if is_loose_file
            else _scan_skill_md_dir(entry, scope="global", tool=tool)
        )
        if artifact:
            results.append(artifact)

    if new_cursor is not None:
        scan_state.save_cursor(_GLOBAL_ROTATION_CATEGORY, new_cursor, state_path)

    logger.info("Global skill scan complete", found=len(results))
    return strip_duplicate_skill_files(results)


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


def _infer_home_client_tool(
    fpath: Path,
    extra_home_roots: Sequence[Path] = (),
) -> str | None:
    """If *fpath* is under ``$HOME/.<client>/``, return the tool identifier."""
    resolved = fpath.resolve()
    for home in (Path.home(), *extra_home_roots):
        try:
            rel = resolved.relative_to(home.resolve())
        except ValueError:
            continue
        if rel.parts:
            return _HOME_CLIENT_TOOL_MAP.get(rel.parts[0])
    return None


def process_skill_paths(
    found_paths: list[Path],
    extra_home_roots: Sequence[Path] = (),
    *,
    checkpoint: Callable[[], None] | None = None,
    state_path: Path | None = None,
) -> list[DiscoveredSkillArtifact]:
    """Process pre-crawled paths and return project-level skill artifacts.

    Only SKILL.md files are recognised. Each SKILL.md triggers a scan of its
    parent directory as a skill.

    Paths under known global skill directories are excluded; those are
    handled separately by ``scan_global_skills``.

    At most ``MAX_SKILL_ARTIFACTS_PER_RUN`` directories are processed per run.
    When the candidate set exceeds the cap, a rotation cursor persisted at
    *state_path* (default ``~/.runlayer/scan-state.json``) picks this run's
    window so successive runs cover every directory. The cursor advances only
    after the selected window completes, so aborted windows are retried. Under
    the cap, no artifact-window cursor is read or written and input order is
    preserved.
    *checkpoint* is the resource governor's cooperative throttle/abort hook,
    called once per skill directory.
    """
    candidates: list[tuple[str, Path]] = []
    seen_skill_dirs: set[str] = set()
    global_prefixes = _get_global_skill_path_prefixes(extra_home_roots)

    for fpath in found_paths:
        if not is_skill_marker_name(fpath.name):
            continue

        if _is_under_global_prefix(fpath, global_prefixes):
            continue

        dir_key = str(fpath.parent.resolve())
        if dir_key in seen_skill_dirs:
            continue
        seen_skill_dirs.add(dir_key)
        candidates.append((dir_key, fpath))

    total_found = len(candidates)
    new_cursor: str | None = None
    if total_found > MAX_SKILL_ARTIFACTS_PER_RUN:
        marker_by_key = dict(candidates)
        cursor = scan_state.load_cursor(_ROTATION_CATEGORY, state_path)
        window, new_cursor = scan_state.rotation_window(
            sorted(marker_by_key), cursor, MAX_SKILL_ARTIFACTS_PER_RUN
        )
        candidates = [(key, marker_by_key[key]) for key in window]
        logger.warning(
            "skill_scan_window_rotated",
            total_found=total_found,
            processed=len(candidates),
            cursor=new_cursor,
        )

    results: list[DiscoveredSkillArtifact] = []
    for _dir_key, fpath in candidates:
        if checkpoint is not None:
            checkpoint()

        home_tool = _infer_home_client_tool(fpath, extra_home_roots)
        if home_tool is not None:
            scope = "user"
            tool = home_tool
            project_root = None
        else:
            scope = "project"
            tool = "multi"
            project_root = _infer_project_root(fpath)

        artifact = _scan_skill_md_dir(
            fpath.parent,
            scope=scope,
            tool=tool,
            project_path=project_root,
        )
        if artifact:
            results.append(artifact)

    if new_cursor is not None:
        scan_state.save_cursor(_ROTATION_CATEGORY, new_cursor, state_path)

    logger.info("Project skill scan complete", found=len(results))
    return strip_duplicate_skill_files(results)


def _get_global_skill_path_prefixes(
    extra_home_roots: Sequence[Path] = (),
) -> set[Path]:
    """Resolved paths that ``scan_global_skills`` owns.

    Any file under these prefixes should be excluded from
    ``process_skill_paths`` to avoid double-counting.
    """
    prefixes: set[Path] = set()
    for home in (Path.home(), *extra_home_roots):
        for rel_dir, _ in _GLOBAL_SKILL_DIRS:
            for skills_root in _expand_global_skill_dirs(home, rel_dir):
                prefixes.add(skills_root.resolve())
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
