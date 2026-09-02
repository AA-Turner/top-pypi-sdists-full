"""Discover client-native agent definition files."""

from __future__ import annotations

import hashlib
import os
import platform
import stat
import sys
from collections import deque
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Literal

import yaml

from runlayer_cli.paths import strip_reported_path_prefix
from runlayer_cli.scan.scanner_primitives import (
    SymlinkFollowBudget,
    SymlinkFollowPolicy,
    has_link_or_reparse_component,
    link_or_reparse_status,
    read_bounded,
    realpath_key,
)
from runlayer_cli.scan.windows_users import is_windows_system_context

if sys.version_info >= (3, 11):
    import tomllib
else:  # pragma: no cover - Python < 3.11
    import tomli as tomllib

AgentDefinitionScope = Literal["user", "project"]
AgentDefinitionFormat = Literal["markdown", "toml", "yaml"]


@dataclass(frozen=True)
class AgentDefinitionPattern:
    """One client's native agent-definition locations and file format."""

    client: str
    file_format: AgentDefinitionFormat
    project_globs: tuple[str, ...]
    project_markers: tuple[tuple[str, ...], ...]
    user_roots: tuple[str, ...]
    filename_suffix: str
    fallback_suffix: str
    project_recursive: bool = False


AGENT_DEFINITION_PATTERNS: tuple[AgentDefinitionPattern, ...] = (
    AgentDefinitionPattern(
        client="claude_code",
        file_format="markdown",
        project_globs=(".claude/agents/*.md",),
        project_markers=((".claude", "agents"),),
        user_roots=("~/.claude/agents",),
        filename_suffix=".md",
        fallback_suffix=".md",
    ),
    AgentDefinitionPattern(
        client="cursor",
        file_format="markdown",
        project_globs=(".cursor/agents/*.md",),
        project_markers=((".cursor", "agents"),),
        user_roots=("~/.cursor/agents",),
        filename_suffix=".md",
        fallback_suffix=".md",
    ),
    AgentDefinitionPattern(
        client="codex",
        file_format="toml",
        project_globs=(".codex/agents/*.toml",),
        project_markers=((".codex", "agents"),),
        user_roots=("~/.codex/agents",),
        filename_suffix=".toml",
        fallback_suffix=".toml",
    ),
    AgentDefinitionPattern(
        client="gemini_cli",
        file_format="markdown",
        project_globs=(".gemini/agents/*.md",),
        project_markers=((".gemini", "agents"),),
        user_roots=("~/.gemini/agents",),
        filename_suffix=".md",
        fallback_suffix=".md",
    ),
    AgentDefinitionPattern(
        client="github_copilot_cli",
        file_format="markdown",
        project_globs=(".github/agents/*.agent.md",),
        project_markers=((".github", "agents"),),
        user_roots=("~/.copilot/agents", "~/.github/agents"),
        filename_suffix=".agent.md",
        fallback_suffix=".agent.md",
    ),
    AgentDefinitionPattern(
        client="opencode",
        file_format="markdown",
        project_globs=(
            ".opencode/agents/*.md",
            ".opencode/agents/**/*.md",
        ),
        project_markers=((".opencode", "agents"),),
        user_roots=("~/.config/opencode/agents",),
        filename_suffix=".md",
        fallback_suffix=".md",
        project_recursive=True,
    ),
    AgentDefinitionPattern(
        client="goose",
        file_format="yaml",
        # Goose reads project recipes from .goose/recipes/ and .agents/recipes/
        # (crates/goose/src/recipe/local_recipes.rs). A bare project-root
        # recipes/ dir is NOT a goose location, so it is deliberately excluded:
        # its single-segment marker matched any recipes/*.yaml under home and
        # misattributed unrelated files as goose agent definitions.
        project_globs=(".goose/recipes/*.yaml", ".agents/recipes/*.yaml"),
        project_markers=((".goose", "recipes"), (".agents", "recipes")),
        user_roots=(
            "~/.config/goose/recipes",
            "~/.agents/recipes",
            "%APPDATA%/Block/goose/recipes",
        ),
        filename_suffix=".yaml",
        fallback_suffix=".yaml",
    ),
)

MAX_AGENT_DEFINITION_FILE_BYTES = 1_048_576
MAX_AGENT_DEFINITION_FILES = 1_000
MAX_AGENT_DEFINITION_TOTAL_BYTES = 5_242_880
MAX_AGENT_DEFINITION_USER_DEPTH = 8
MAX_FOLLOWED_AGENT_DEFINITION_TARGETS = 64


@dataclass(frozen=True)
class DiscoveredAgentDefinition:
    """A client-native agent definition found on a host or in a container."""

    client: str
    name: str
    description: str | None
    scope: AgentDefinitionScope
    path: str
    project_path: str | None
    content_hash: str
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
        """Return the future agent-definition submission shape."""
        is_container = self.container_id is not None
        payload: dict[str, Any] = {
            "client": self.client,
            "name": self.name,
            "description": self.description,
            "scope": self.scope,
            "path": (
                self.path if is_container else strip_reported_path_prefix(self.path)
            ),
            "project_path": (
                self.project_path
                if is_container
                else strip_reported_path_prefix(self.project_path)
            ),
            "content_hash": self.content_hash,
        }
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


def _filename(path: str | Path) -> str:
    return str(path).replace("\\", "/").rsplit("/", 1)[-1]


def _fallback_name(pattern: AgentDefinitionPattern, path: str | Path) -> str:
    filename = _filename(path)
    if filename.casefold().endswith(pattern.fallback_suffix.casefold()):
        return filename[: -len(pattern.fallback_suffix)]
    return filename


def _pattern_for_client(client: str) -> AgentDefinitionPattern | None:
    return next(
        (pattern for pattern in AGENT_DEFINITION_PATTERNS if pattern.client == client),
        None,
    )


def _parse_markdown_metadata(text: str) -> dict[str, Any] | None:
    # A leading `---` with no closing delimiter is not a frontmatter block, so
    # treat it like a file with no frontmatter ({}; name falls back to the
    # filename) instead of dropping the definition. An empty/None block is also
    # {}. Only a delimited block that fails to parse or isn't a mapping is
    # genuinely broken and dropped (None).
    if not text.startswith("---"):
        return {}
    close = text.find("\n---", 3)
    if close == -1:
        return {}
    try:
        loaded = yaml.safe_load(text[3:close])
    except yaml.YAMLError:
        return None
    if loaded is None:
        return {}
    if not isinstance(loaded, dict):
        return None
    return loaded


def parse_agent_definition(
    *,
    client: str,
    path: str | Path,
    content: bytes,
    scope: AgentDefinitionScope,
    project_path: str | None = None,
    container_id: str | None = None,
    container_name: str | None = None,
    container_image_ref: str | None = None,
    container_image_digest: str | None = None,
    container_runtime: str | None = None,
    container_is_devcontainer: bool = False,
    container_is_running: bool = True,
    container_labels: dict[str, str] | None = None,
    container_mounts_host_home: bool = False,
) -> DiscoveredAgentDefinition | None:
    """Parse one known client-native agent definition from raw bytes."""
    pattern = _pattern_for_client(client)
    if pattern is None:
        return None
    try:
        text = content.decode("utf-8")
    except UnicodeDecodeError:
        return None

    try:
        if pattern.file_format == "markdown":
            metadata = _parse_markdown_metadata(text)
            if metadata is None:
                return None
        elif pattern.file_format == "toml":
            loaded = tomllib.loads(text)
            if not isinstance(loaded, dict):
                return None
            metadata = loaded
        else:
            loaded = yaml.safe_load(text)
            if loaded is None:
                metadata = {}
            elif not isinstance(loaded, dict):
                return None
            else:
                metadata = loaded
    except (ValueError, yaml.YAMLError):
        return None

    name = (
        metadata.get("title") or metadata.get("name")
        if pattern.file_format == "yaml"
        else metadata.get("name")
    )
    name = name or _fallback_name(pattern, path)
    description = metadata.get("description")

    return DiscoveredAgentDefinition(
        client=client,
        name=str(name)[:100],
        description=str(description)[:1024] if description is not None else None,
        scope=scope,
        path=str(path),
        project_path=project_path,
        content_hash=hashlib.sha256(content).hexdigest(),
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


def get_agent_definition_search_patterns() -> list[str]:
    """Return project path-suffix globs for the shared home crawl."""
    return list(
        dict.fromkeys(
            project_glob
            for pattern in AGENT_DEFINITION_PATTERNS
            for project_glob in pattern.project_globs
        )
    )


def _expanded_user_root(template: str) -> Path | None:
    if template.startswith("~/"):
        return Path.home() / template[2:]
    if template.startswith("%APPDATA%/"):
        if platform.system() != "Windows":
            return None
        appdata = os.environ.get("APPDATA")
        if not appdata:
            return None
        return Path(appdata) / template[len("%APPDATA%/") :]
    return None


def _user_root_groups(
    extra_home_roots: Sequence[Path] = (),
) -> list[list[tuple[AgentDefinitionPattern, Path]]]:
    """Group ``(pattern, root)`` pairs by home directory.

    The native home (including platform roots such as ``%APPDATA%``) is the
    first group; each extra home root (e.g. a WSL distro home) becomes its own
    group. Grouping lets ``scan_user_agent_definitions`` enforce the file/byte
    caps per home, so a saturated home cannot starve the remaining homes.
    """
    native: list[tuple[AgentDefinitionPattern, Path]] = []
    extra: list[list[tuple[AgentDefinitionPattern, Path]]] = [
        [] for _ in extra_home_roots
    ]
    for pattern in AGENT_DEFINITION_PATTERNS:
        for template in pattern.user_roots:
            root = _expanded_user_root(template)
            if root is not None:
                native.append((pattern, root.absolute()))
            if template.startswith("~/"):
                relative = template[2:]
                for index, home in enumerate(extra_home_roots):
                    extra[index].append((pattern, (home / relative).absolute()))
    return [native, *extra]


def _user_roots(
    extra_home_roots: Sequence[Path] = (),
) -> tuple[tuple[AgentDefinitionPattern, Path], ...]:
    return tuple(
        pair for group in _user_root_groups(extra_home_roots) for pair in group
    )


def _is_within(path: Path, root: Path) -> bool:
    try:
        path.absolute().relative_to(root.absolute())
    except ValueError:
        return False
    return True


def matches_agent_definition_filename(
    pattern: AgentDefinitionPattern,
    filename: str,
) -> bool:
    """Return whether a filename has the client's required suffix."""
    return filename.casefold().endswith(pattern.filename_suffix.casefold())


def match_project_marker(
    parts: tuple[str, ...],
    pattern: AgentDefinitionPattern,
) -> int | None:
    """Return the project-root prefix length for a matching project path."""
    if not parts or not matches_agent_definition_filename(pattern, parts[-1]):
        return None
    for marker in pattern.project_markers:
        marker_size = len(marker)
        for index in range(len(parts) - marker_size):
            if parts[index : index + marker_size] != marker:
                continue
            trailing_parts = parts[index + marker_size :]
            if not trailing_parts or (
                not pattern.project_recursive and len(trailing_parts) != 1
            ):
                continue
            return index
    return None


def _project_match(
    path: Path,
) -> tuple[AgentDefinitionPattern, Path] | None:
    parts = path.parts
    for pattern in AGENT_DEFINITION_PATTERNS:
        project_parts = match_project_marker(parts, pattern)
        if project_parts is not None:
            return pattern, Path(*parts[:project_parts])
    return None


def _read_bounded_file(path: Path) -> bytes | None:
    if link_or_reparse_status(path) is not False:
        return None
    return read_bounded(path, max_bytes=MAX_AGENT_DEFINITION_FILE_BYTES)


def process_agent_definition_paths(
    found_paths: list[Path],
    extra_home_roots: Sequence[Path] = (),
    *,
    logical_paths: Mapping[Path, Sequence[Path]] | None = None,
) -> list[DiscoveredAgentDefinition]:
    """Classify logical identities while reading each physical crawl path once."""
    results: list[DiscoveredAgentDefinition] = []
    seen_logical_paths: set[tuple[str, str]] = set()
    seen_physical_paths: set[str] = set()
    files_seen = 0
    total_bytes = 0
    user_roots = tuple(root for _, root in _user_roots(extra_home_roots))
    for path in found_paths:
        physical_path_key = os.path.normcase(os.path.abspath(str(path)))
        if physical_path_key in seen_physical_paths:
            continue
        seen_physical_paths.add(physical_path_key)

        identities = (
            logical_paths.get(path, (path,)) if logical_paths is not None else (path,)
        )
        classified: list[tuple[Path, AgentDefinitionPattern, Path]] = []
        for logical_path in identities:
            if any(_is_within(logical_path, user_root) for user_root in user_roots):
                continue
            matched = _project_match(logical_path)
            if matched is None:
                continue
            pattern, project_path = matched
            logical_path_key = os.path.normcase(os.path.abspath(str(logical_path)))
            key = (pattern.client, logical_path_key)
            if key in seen_logical_paths:
                continue
            seen_logical_paths.add(key)
            classified.append((logical_path, pattern, project_path))

        if not classified:
            continue
        if files_seen >= MAX_AGENT_DEFINITION_FILES:
            break
        files_seen += 1
        content = _read_bounded_file(path)
        if content is None:
            continue
        if total_bytes + len(content) > MAX_AGENT_DEFINITION_TOTAL_BYTES:
            break
        total_bytes += len(content)
        for logical_path, pattern, project_path in classified:
            definition = parse_agent_definition(
                client=pattern.client,
                path=logical_path,
                content=content,
                scope="project",
                project_path=str(project_path),
            )
            if definition is not None:
                results.append(definition)
    return results


@dataclass(frozen=True)
class _UserDefinitionWalkRoot:
    pattern: AgentDefinitionPattern
    actual_root: Path
    logical_root: Path


class _UserDefinitionRootGroupScanner:
    def __init__(
        self,
        *,
        group: Sequence[tuple[AgentDefinitionPattern, Path]],
        seen: set[tuple[str, str]],
        results: list[DiscoveredAgentDefinition],
        symlink_policies: dict[str, SymlinkFollowPolicy],
    ) -> None:
        self._group = group
        self._seen = seen
        self._results = results
        self._files_seen = 0
        self._total_bytes = 0
        self._read_cache: dict[str, bytes | None] = {}
        self._budget_exhausted = False
        self._pending: deque[_UserDefinitionWalkRoot] = deque()
        self._policies = symlink_policies

    def _inspect_follow_target(
        self,
        pattern: AgentDefinitionPattern,
        link_path: Path,
        *,
        require_directory: bool,
        logical_file_path: Path | None = None,
    ) -> Path | None:
        policy = self._policies[pattern.client]
        target = policy.inspect(link_path)
        if target is None:
            return None
        try:
            target_mode = target.stat().st_mode
        except OSError:
            return None
        if require_directory:
            supported = stat.S_ISDIR(target_mode)
        else:
            supported = stat.S_ISREG(target_mode) or stat.S_ISDIR(target_mode)
        if not supported:
            return None
        if (
            stat.S_ISREG(target_mode)
            and logical_file_path is not None
            and not matches_agent_definition_filename(
                pattern,
                logical_file_path.name,
            )
        ):
            return None
        return target

    def _claim_follow_target(
        self,
        pattern: AgentDefinitionPattern,
        link_path: Path,
        *,
        require_directory: bool,
        logical_file_path: Path | None = None,
    ) -> Path | None:
        target = self._inspect_follow_target(
            pattern,
            link_path,
            require_directory=require_directory,
            logical_file_path=logical_file_path,
        )
        policy = self._policies[pattern.client]
        return target if target is not None and policy.claim(target) else None

    def scan(self) -> None:
        for pattern, root in self._group:
            try:
                link_status = link_or_reparse_status(root)
                if link_status is None:
                    continue
                if link_status:
                    target = self._claim_follow_target(
                        pattern,
                        root,
                        require_directory=True,
                    )
                    if target is None:
                        continue
                    self._enqueue_root(pattern, target, root)
                elif root.is_dir():
                    self._enqueue_root(pattern, root, root)
                else:
                    continue
            except OSError:
                continue

        while self._pending and not self._budget_exhausted:
            self._walk_root(self._pending.popleft())

    def _enqueue_root(
        self,
        pattern: AgentDefinitionPattern,
        actual_root: Path,
        logical_root: Path,
    ) -> None:
        walk_root = _UserDefinitionWalkRoot(
            pattern=pattern,
            actual_root=actual_root,
            logical_root=logical_root,
        )
        self._policies[pattern.client].add_scan_area(
            actual_root,
            MAX_AGENT_DEFINITION_USER_DEPTH,
        )
        self._pending.append(walk_root)

    def _walk_root(self, walk_root: _UserDefinitionWalkRoot) -> None:
        for dirpath, dirnames, filenames in os.walk(
            walk_root.actual_root,
            followlinks=False,
        ):
            if self._budget_exhausted:
                return
            current = Path(dirpath)
            try:
                relative = current.relative_to(walk_root.actual_root)
            except ValueError:
                dirnames.clear()
                continue
            logical_directory = walk_root.logical_root.joinpath(*relative.parts)
            relative_depth = len(relative.parts)
            entries: list[tuple[str, Path, bool]] = []
            if relative_depth >= MAX_AGENT_DEFINITION_USER_DEPTH:
                dirnames.clear()
            else:
                real_directories: list[str] = []
                for dirname in sorted(dirnames):
                    path = current / dirname
                    link_status = link_or_reparse_status(path)
                    if link_status is None:
                        continue
                    if link_status:
                        entries.append((dirname, path, True))
                    else:
                        real_directories.append(dirname)
                dirnames[:] = real_directories

            for filename in sorted(filenames):
                path = current / filename
                link_status = link_or_reparse_status(path)
                if link_status is not None:
                    entries.append((filename, path, link_status))

            for name, path, is_link in sorted(entries, key=lambda item: item[0]):
                logical_path = logical_directory / name
                if is_link:
                    self._follow_link(walk_root.pattern, path, logical_path)
                else:
                    self._collect_file(walk_root.pattern, path, logical_path)
                if self._budget_exhausted:
                    return

    def _follow_link(
        self,
        pattern: AgentDefinitionPattern,
        link_path: Path,
        logical_path: Path,
    ) -> None:
        target = self._inspect_follow_target(
            pattern,
            link_path,
            require_directory=False,
            logical_file_path=logical_path,
        )
        if target is None:
            return
        try:
            target_mode = target.stat().st_mode
        except OSError:
            return
        if stat.S_ISREG(target_mode):
            self._collect_file(
                pattern,
                target,
                logical_path,
                followed_target=target,
            )
        elif stat.S_ISDIR(target_mode) and self._policies[pattern.client].claim(target):
            self._enqueue_root(pattern, target, logical_path)

    def _collect_file(
        self,
        pattern: AgentDefinitionPattern,
        read_path: Path,
        logical_path: Path,
        *,
        followed_target: Path | None = None,
    ) -> None:
        if not matches_agent_definition_filename(pattern, logical_path.name):
            return
        path_key = os.path.normcase(os.path.abspath(str(logical_path)))
        key = (pattern.client, path_key)
        if key in self._seen:
            return
        self._seen.add(key)
        read_path_key = realpath_key(read_path)
        cache_hit = read_path_key in self._read_cache
        if not cache_hit:
            if self._files_seen >= MAX_AGENT_DEFINITION_FILES:
                self._budget_exhausted = True
                return
            self._files_seen += 1
        if followed_target is None:
            self._policies[pattern.client].mark_visited(read_path)
        if cache_hit:
            content = self._read_cache[read_path_key]
        else:
            content = _read_bounded_file(read_path)
            self._read_cache[read_path_key] = content
        if content is None:
            return
        if not cache_hit:
            if self._total_bytes + len(content) > MAX_AGENT_DEFINITION_TOTAL_BYTES:
                self._budget_exhausted = True
                return
            self._total_bytes += len(content)
        if followed_target is not None and not self._policies[pattern.client].claim(
            followed_target
        ):
            return
        definition = parse_agent_definition(
            client=pattern.client,
            path=logical_path,
            content=content,
            scope="user",
        )
        if definition is not None:
            self._results.append(definition)


def _scan_user_root_group(
    group: Sequence[tuple[AgentDefinitionPattern, Path]],
    seen: set[tuple[str, str]],
    results: list[DiscoveredAgentDefinition],
    symlink_policies: dict[str, SymlinkFollowPolicy],
) -> None:
    """Scan one home's roots with one shared budget and symlink frontier."""
    _UserDefinitionRootGroupScanner(
        group=group,
        seen=seen,
        results=results,
        symlink_policies=symlink_policies,
    ).scan()


def scan_user_agent_definitions(
    extra_home_roots: Sequence[Path] = (),
) -> list[DiscoveredAgentDefinition]:
    """Recursively scan bounded, client-owned user definition roots.

    The file and byte caps are enforced per home so a saturated home (the
    native home or any extra/WSL home) cannot starve the remaining homes.
    """
    results: list[DiscoveredAgentDefinition] = []
    seen: set[tuple[str, str]] = set()
    groups = _user_root_groups(extra_home_roots)
    windows_system_context = is_windows_system_context()
    if windows_system_context:
        groups = [
            [
                (pattern, root)
                for pattern, root in group
                if not has_link_or_reparse_component(root)
            ]
            for group in groups
        ]

    direct_roots: list[tuple[AgentDefinitionPattern, Path]] = []
    for group in groups:
        for pattern, root in group:
            try:
                if link_or_reparse_status(root) is False and root.is_dir():
                    direct_roots.append((pattern, root))
            except OSError:
                continue
    follow_budget = SymlinkFollowBudget(MAX_FOLLOWED_AGENT_DEFINITION_TARGETS)
    symlink_policies = {
        pattern.client: SymlinkFollowPolicy(
            scan_areas=[
                (root, MAX_AGENT_DEFINITION_USER_DEPTH)
                for direct_pattern, root in direct_roots
                if direct_pattern.client == pattern.client
            ],
            windows_system_context=windows_system_context,
            follow_budget=follow_budget,
            scan_area_file_depth_delta=1,
        )
        for pattern in AGENT_DEFINITION_PATTERNS
    }
    for group in groups:
        _scan_user_root_group(
            group,
            seen,
            results,
            symlink_policies,
        )
    return results


def dedupe_agent_definitions(
    definitions: list[DiscoveredAgentDefinition],
) -> list[DiscoveredAgentDefinition]:
    """Dedupe one installation path per client and execution environment."""
    deduped: list[DiscoveredAgentDefinition] = []
    seen: set[tuple[str, str, str | None, str | None, str | None]] = set()
    for definition in definitions:
        key = (
            definition.client,
            definition.path,
            definition.container_id,
            definition.wsl_distro.casefold() if definition.wsl_distro else None,
            definition.wsl_user,
        )
        if key not in seen:
            seen.add(key)
            deduped.append(definition)
    return deduped
