"""Bounded marker-based probe for renamed plugin cache directories.

Plugin scanners key off well-known cache layouts (``~/.cursor/plugins/cache/
cursor-public/...``); a plugin copied or renamed elsewhere under the client
root escapes them while the client can still load it. This probe walks the
known client roots to a bounded depth and classifies directories by manifest
*content* markers regardless of directory name.

Coverage policy: probe explicit client plugin roots only. Never broaden this
into a home crawl or a generic marker sweep outside the allowlisted roots —
the same policy as the disguised-skills browser-cache probe. Opt-in and
default-off (CLI flag / MDM key), because renamed copies are usually benign
developer clutter; the probe exists for incident-response sweeps.
"""

from __future__ import annotations

import os
from collections import deque
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from pathlib import Path

import json5
import structlog

from runlayer_cli.scan.plugin_scanner import (
    DiscoveredPluginArtifact,
    _collect_mcp_server_refs,
    _collect_plugin_files,
    _detect_components,
    _extract_manifest_metadata,
    compute_plugin_identifier,
)
from runlayer_cli.scan.scanner_primitives import (
    SymlinkFollowPolicy,
    SymlinkLayoutResolver,
    is_contained_real_directory,
    is_link_or_reparse,
    is_real_directory,
    read_safe_relative_file,
    realpath_key,
)
from runlayer_cli.scan.windows_users import is_windows_system_context

logger = structlog.get_logger(__name__)

MAX_PROBE_DEPTH = 5
MAX_PROBE_DIRECTORIES = 512
MAX_ENTRIES_PER_DIRECTORY = 512
MAX_ARTIFACTS = 64
MAX_FOLLOWED_SYMLINK_TARGETS = 64
MAX_RESOLVED_INTERMEDIATE_LINKS = 64
MAX_MARKER_BYTES = 1024 * 1024

_SKIPPED_DIRECTORY_NAMES = frozenset({".git", "node_modules", "__pycache__"})


@dataclass(frozen=True)
class _RootSpec:
    """One allowlisted client root, relative to a home directory."""

    relative: str
    client: str
    plugin_type: str
    extra_marker_relatives: tuple[str, ...] = ()


_ROOT_SPECS: tuple[_RootSpec, ...] = (
    _RootSpec(".cursor/plugins", "cursor", "cursor_plugin"),
    _RootSpec(".claude/plugins", "claude_code", "claude_code_plugin"),
    _RootSpec(".codex/plugins", "codex", "codex_plugin"),
    _RootSpec(".copilot", "copilot", "copilot_plugin"),
    # OpenCode local plugins are plain npm-style packages; ``package.json`` is
    # their only reliable marker, so it applies to this root only.
    _RootSpec(".config/opencode", "opencode", "opencode_plugin", ("package.json",)),
)


@dataclass(frozen=True)
class _MarkerSpec:
    """A manifest file that classifies a directory as a plugin install.

    ``plugin_type``/``client`` of ``None`` fall back to the containing root's
    defaults (generic markers like ``mcp.json`` carry no client identity).
    """

    relative: str
    manifest_subdir: str | None = None
    plugin_type: str | None = None
    client: str | None = None


_MARKER_SPECS: tuple[_MarkerSpec, ...] = (
    _MarkerSpec(
        ".cursor-plugin/plugin.json", ".cursor-plugin", "cursor_plugin", "cursor"
    ),
    _MarkerSpec(
        ".claude-plugin/plugin.json",
        ".claude-plugin",
        "claude_code_plugin",
        "claude_code",
    ),
    _MarkerSpec(".codex-plugin/plugin.json", ".codex-plugin", "codex_plugin", "codex"),
    _MarkerSpec("gemini-extension.json", None, "gemini_extension", "gemini"),
    _MarkerSpec("mcp.json"),
    _MarkerSpec(".mcp.json"),
)

_SKIPPED_PROBE_DIRECTORY_NAMES = _SKIPPED_DIRECTORY_NAMES | frozenset(
    spec.manifest_subdir for spec in _MARKER_SPECS if spec.manifest_subdir is not None
)


@dataclass
class _ProbeBudget:
    directories: int = 0
    artifacts: int = 0
    truncated: bool = False


@dataclass
class _RootFrontier:
    root: _RootSpec
    pending: deque[tuple[Path, int]]


@dataclass(frozen=True)
class _ProbeScanArea:
    root_key: str
    max_depth: int


def _covered_by_probe_scan(
    target: Path,
    scan_areas: Sequence[_ProbeScanArea],
) -> bool:
    target_key = realpath_key(target)
    for scan_area in scan_areas:
        try:
            relative = os.path.relpath(target_key, scan_area.root_key)
        except ValueError:
            continue
        if relative == os.curdir:
            return True
        if relative == os.pardir or relative.startswith(os.pardir + os.sep):
            continue
        parts = Path(relative).parts
        if len(parts) <= scan_area.max_depth and not any(
            part in _SKIPPED_PROBE_DIRECTORY_NAMES for part in parts
        ):
            return True
    return False


def _has_redirected_component(install_root: Path, relative: Path) -> bool:
    current = install_root
    for index, part in enumerate(relative.parts):
        candidate = current / part
        if is_link_or_reparse(candidate):
            return True
        if index < len(relative.parts) - 1:
            if not is_real_directory(candidate):
                return False
            current = candidate
    return False


def _read_marker(
    directory: Path,
    relative: Path,
    *,
    resolver: SymlinkLayoutResolver,
) -> tuple[Path, dict[str, object] | None] | None:
    result = read_safe_relative_file(
        directory,
        relative,
        resolver=resolver,
        max_bytes=MAX_MARKER_BYTES,
    )
    if result is None:
        return None
    manifest_path = result["path"]
    content = result["content"]
    try:
        value = json5.loads(content.decode("utf-8"))
    except (UnicodeDecodeError, ValueError):
        value = None
    return manifest_path, value if isinstance(value, dict) else None


def _match_marker(
    directory: Path,
    markers: Sequence[_MarkerSpec],
    *,
    resolver: SymlinkLayoutResolver,
) -> tuple[_MarkerSpec, Path, dict[str, object] | None] | None:
    for spec in markers:
        marker = _read_marker(
            directory,
            Path(spec.relative),
            resolver=resolver,
        )
        if marker is not None:
            return spec, marker[0], marker[1]
    return None


def _artifact_for_directory(
    directory: Path,
    *,
    root: _RootSpec,
    marker: _MarkerSpec,
    manifest: dict[str, object] | None,
    windows_system_context: bool,
) -> DiscoveredPluginArtifact | None:
    if windows_system_context and any(
        _has_redirected_component(directory, Path(spec.relative))
        for spec in _MARKER_SPECS
    ):
        return None
    m_name, m_version, m_desc, m_author = (None, None, None, None)
    if manifest:
        m_name, m_version, m_desc, m_author = _extract_manifest_metadata(manifest)

    components = _detect_components(
        directory, marker.manifest_subdir or ".claude-plugin"
    )
    identifier = compute_plugin_identifier(directory)
    mcp_servers = _collect_mcp_server_refs(directory)
    p_files, p_symlinks, p_oversized = _collect_plugin_files(directory)

    return DiscoveredPluginArtifact(
        name=m_name or directory.name,
        plugin_type=marker.plugin_type or root.plugin_type,
        client=marker.client or root.client,
        install_path=str(directory),
        identifier=identifier,
        version=m_version,
        description=m_desc,
        author=m_author,
        scope="user",
        has_mcp_servers=components["has_mcp_servers"] or bool(mcp_servers),
        has_skills=components["has_skills"],
        has_rules=components["has_rules"],
        has_commands=components["has_commands"],
        has_hooks=components["has_hooks"],
        mcp_servers=mcp_servers,
        files=p_files,
        file_count=len(p_files),
        oversized=p_oversized,
        symlinks_found=p_symlinks,
    )


def _probe_root(
    frontiers: deque[_RootFrontier],
    *,
    budget: _ProbeBudget,
    symlink_policy: SymlinkFollowPolicy,
    resolver: SymlinkLayoutResolver,
    windows_system_context: bool,
    checkpoint: Callable[[], None] | None,
    scan_areas: list[_ProbeScanArea],
) -> list[DiscoveredPluginArtifact]:
    artifacts: list[DiscoveredPluginArtifact] = []
    seen_directories: set[str] = set()
    markers_by_root = {
        root: (
            *_MARKER_SPECS,
            *(_MarkerSpec(relative) for relative in root.extra_marker_relatives),
        )
        for root in _ROOT_SPECS
    }
    while frontiers and not budget.truncated:
        frontier = frontiers.popleft()
        if not frontier.pending:
            continue
        directory, depth = frontier.pending.popleft()
        directory_key = realpath_key(directory)
        if directory_key in seen_directories:
            if frontier.pending:
                frontiers.append(frontier)
            continue
        seen_directories.add(directory_key)
        symlink_policy.mark_visited(directory)
        if budget.directories >= MAX_PROBE_DIRECTORIES:
            budget.truncated = True
            break
        budget.directories += 1
        if checkpoint is not None:
            checkpoint()

        descend = depth < MAX_PROBE_DEPTH
        if depth > 0:
            markers = markers_by_root[frontier.root]
            matched = (
                None
                if windows_system_context
                and any(
                    _has_redirected_component(directory, Path(spec.relative))
                    for spec in markers
                )
                else _match_marker(
                    directory,
                    markers,
                    resolver=resolver,
                )
            )
            if matched is not None:
                if budget.artifacts >= MAX_ARTIFACTS:
                    budget.truncated = True
                    break
                artifact = _artifact_for_directory(
                    directory,
                    root=frontier.root,
                    marker=matched[0],
                    manifest=matched[2],
                    windows_system_context=windows_system_context,
                )
                if artifact is not None:
                    budget.artifacts += 1
                    artifacts.append(artifact)
                descend = False

        if descend:
            child_directories: list[Path] = []
            try:
                entries_seen = 0
                with os.scandir(directory) as entries:
                    for entry in entries:
                        if entries_seen >= MAX_ENTRIES_PER_DIRECTORY:
                            break
                        entries_seen += 1
                        try:
                            if entry.name in _SKIPPED_PROBE_DIRECTORY_NAMES:
                                continue
                        except OSError:
                            continue
                        entry_path = Path(entry.path)
                        if is_link_or_reparse(entry_path):
                            target = resolver.resolve_policy_link(
                                entry_path,
                                current=directory,
                                is_target_covered=lambda candidate: (
                                    _covered_by_probe_scan(candidate, scan_areas)
                                ),
                                target_is_usable=lambda candidate: (
                                    candidate.name not in _SKIPPED_PROBE_DIRECTORY_NAMES
                                ),
                            )
                            if target is None or not is_real_directory(target):
                                continue
                            scan_areas.append(
                                _ProbeScanArea(
                                    root_key=realpath_key(target),
                                    max_depth=MAX_PROBE_DEPTH - (depth + 1),
                                )
                            )
                            child_directories.append(target)
                            continue
                        try:
                            if not entry.is_dir(follow_symlinks=False):
                                continue
                        except OSError:
                            continue
                        child_directories.append(entry_path)
            except OSError:
                child_directories = []
            frontier.pending.extend(
                (path, depth + 1) for path in sorted(child_directories)
            )
        if frontier.pending:
            frontiers.append(frontier)
    return artifacts


def scan_renamed_plugin_caches(
    *,
    home: Path | None = None,
    extra_home_roots: Sequence[Path] = (),
    checkpoint: Callable[[], None] | None = None,
) -> list[DiscoveredPluginArtifact]:
    """Probe allowlisted client roots for renamed plugin cache directories."""
    budget = _ProbeBudget()
    artifacts: list[DiscoveredPluginArtifact] = []
    native_home = home or Path.home()
    windows_system_context = is_windows_system_context()
    root_candidates = [
        (current_home, root, current_home / root.relative)
        for current_home in (native_home, *extra_home_roots)
        for root in _ROOT_SPECS
    ]
    symlink_policy = SymlinkFollowPolicy(
        scan_areas=[],
        max_followed=MAX_FOLLOWED_SYMLINK_TARGETS,
        windows_system_context=windows_system_context,
    )
    resolver = SymlinkLayoutResolver(
        policy=symlink_policy,
        windows_system_context=windows_system_context,
        max_intermediate_links=MAX_RESOLVED_INTERMEDIATE_LINKS,
    )
    resolved_roots: list[tuple[_RootSpec, Path]] = []
    for current_home, root, root_dir in root_candidates:
        resolved_root = (
            root_dir.resolve(strict=True)
            if is_contained_real_directory(current_home, root_dir)
            else resolver.resolve_directory(
                current_home,
                Path(root.relative),
            )
        )
        if resolved_root is None:
            continue
        resolved_roots.append((root, resolved_root))

    scan_areas = [
        _ProbeScanArea(
            root_key=realpath_key(root_dir),
            max_depth=MAX_PROBE_DEPTH,
        )
        for _, root_dir in resolved_roots
    ]
    frontiers = deque(
        _RootFrontier(root=root, pending=deque([(root_dir, 0)]))
        for root, root_dir in resolved_roots
    )
    artifacts.extend(
        _probe_root(
            frontiers,
            budget=budget,
            symlink_policy=symlink_policy,
            resolver=resolver,
            windows_system_context=windows_system_context,
            checkpoint=checkpoint,
            scan_areas=scan_areas,
        )
    )
    logger.info(
        "Renamed plugin cache probe complete",
        found=len(artifacts),
        truncated=budget.truncated,
    )
    return artifacts


def filter_novel_plugin_artifacts(
    candidates: Sequence[DiscoveredPluginArtifact],
    existing: Sequence[DiscoveredPluginArtifact],
) -> list[DiscoveredPluginArtifact]:
    """Drop candidates already discovered by the layout-based scanners.

    Dedupe is by resolved install path and by the content-addressable plugin
    identifier: the probe re-walks the normal cache layouts too, so anything
    the layout-based scanners already reported (same directory, or a
    marketplace/cache copy with identical manifest content) is redundant.
    """
    existing_identifiers = {a.identifier for a in existing if a.identifier}
    existing_paths: set[str] = set()
    for artifact in existing:
        if not artifact.install_path:
            continue
        try:
            existing_paths.add(str(Path(artifact.install_path).resolve()))
        except OSError:
            continue

    novel: list[DiscoveredPluginArtifact] = []
    for candidate in candidates:
        try:
            candidate_path = str(Path(candidate.install_path).resolve())
        except OSError:
            candidate_path = candidate.install_path
        if candidate_path in existing_paths:
            continue
        if candidate.identifier and candidate.identifier in existing_identifiers:
            continue
        novel.append(candidate)
    return novel
