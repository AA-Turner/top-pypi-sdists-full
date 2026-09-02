"""Budgeted project-artifact discovery across WSL home UNC paths."""

from __future__ import annotations

import os
import posixpath
import stat
import time
from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath

import structlog

from runlayer_cli.scan.agent_definition_scanner import (
    AGENT_DEFINITION_PATTERNS,
    DiscoveredAgentDefinition,
    dedupe_agent_definitions,
    parse_agent_definition,
)
from runlayer_cli.scan.clients import (
    MCPClientDefinition,
    _wsl_homes,
    get_all_clients,
)
from runlayer_cli.scan.config_parser import MCPClientConfig, parse_config_content
from runlayer_cli.scan.file_collector import MAX_SINGLE_FILE_BYTES, MAX_TOTAL_BYTES
from runlayer_cli.scan.project_tree_match import (
    MAX_PROJECT_TREE_DEPTH,
    _ConfigCandidate,
    _ProjectConfigSpec,
    _ProjectFileClassification,
    _iter_agent_matches,
    _iter_skill_groups,
    _project_agent_definition_match,
    _project_candidates_for_path,
    _project_config_specs,
    _project_skill_file_match,
)
from runlayer_cli.scan.scanner_primitives import (
    SymlinkFollowPolicy,
    has_link_or_reparse_component,
    link_or_reparse_status,
    read_bounded,
)
from runlayer_cli.scan.skip_dirs import find_excluded_directories
from runlayer_cli.scan.skill_scanner import (
    _GLOBAL_SKILL_DIRS,
    _HOME_CLIENT_TOOL_MAP,
    DiscoveredSkillArtifact,
    build_skill_artifact_from_files,
)
from runlayer_cli.scan.windows_users import is_windows_system_context

WSL_SCAN_BASE_TIME_BUDGET_S = 30
WSL_SCAN_PER_HOME_TIME_BUDGET_S = 10
WSL_SCAN_MAX_TIME_BUDGET_S = 300
MAX_WSL_PROJECT_MATCHED_FILES = 128
MAX_FOLLOWED_WSL_PROJECT_TARGETS = 64

logger = structlog.get_logger(__name__)

_LOGICAL_ROOT = "/"

_EXCLUDED_DIRECTORIES = find_excluded_directories()
_SKIP_DIR_NAMES = frozenset(
    excluded for excluded in _EXCLUDED_DIRECTORIES if "/" not in excluded
)
_SKIP_DIR_SUFFIXES = tuple(
    tuple(PurePosixPath(excluded).parts)
    for excluded in _EXCLUDED_DIRECTORIES
    if "/" in excluded
)

# Home-root dot-directories skipped wholesale during descent: known
# client/tool/OS state roots that never hold a user's project checkout. Derived
# from the client definitions (global skill dirs, user agent roots, home client
# dot-dirs) so the set stays in lockstep as clients are added, plus heavy state
# no client definition names (per-user language/tool installs, Remote-WSL server
# payloads). Any *other* home-root dot-directory (e.g. a versioned ``~/.dotfiles``
# repo) is still descended so nested project artifacts are discovered.
_SKIPPED_HOME_ROOT_DOT_DIRS = (
    frozenset(
        PurePosixPath(relative_root).parts[0] for relative_root, _ in _GLOBAL_SKILL_DIRS
    )
    | frozenset(
        PurePosixPath(template[2:]).parts[0]
        for pattern in AGENT_DEFINITION_PATTERNS
        for template in pattern.user_roots
        if template.startswith("~/")
    )
    | frozenset(_HOME_CLIENT_TOOL_MAP)
    | frozenset({".local", ".vscode-server", ".cursor-server"})
)


@dataclass
class WSLProjectScanResult:
    """Project artifacts found by walking WSL homes from the Windows host."""

    configurations: list[MCPClientConfig] = field(default_factory=list)
    skills: list[DiscoveredSkillArtifact] = field(default_factory=list)
    agent_definitions: list[DiscoveredAgentDefinition] = field(default_factory=list)


# Path matching, the classification type, and the drift-prone grouping/iteration
# skeletons are shared via project_tree_match. Classification and config building
# stay WSL-local: they exclude home-root artifacts and remap every logical POSIX
# path to its Windows UNC counterpart (_native_path) — orthogonal to the
# container walker's metadata threading, so sharing them buys nothing.
@dataclass
class _ArtifactByteBudget:
    total_bytes: int = 0

    def charge(self, size: int) -> None:
        if self.total_bytes + size > MAX_TOTAL_BYTES:
            raise _CollectionBudgetExhausted
        self.total_bytes += size


@dataclass
class _CollectedWSLProjectArtifacts:
    configurations: list[MCPClientConfig] = field(default_factory=list)
    skills: list[DiscoveredSkillArtifact] = field(default_factory=list)
    agent_definitions: list[DiscoveredAgentDefinition] = field(default_factory=list)


@dataclass
class _HomeWalkResult:
    artifacts: _CollectedWSLProjectArtifacts
    budget_exhausted: bool = False


@dataclass(frozen=True)
class _ClassifiedWslEntry:
    candidate: Path
    is_directory: bool
    is_file: bool
    followed: bool


class _CollectionBudgetExhausted(Exception):
    """Stop all remaining WSL-home collection after a global budget is spent."""


def _scaled_wsl_scan_time_budget(home_count: int) -> float:
    return min(
        WSL_SCAN_MAX_TIME_BUDGET_S,
        WSL_SCAN_BASE_TIME_BUDGET_S
        + max(home_count, 0) * WSL_SCAN_PER_HOME_TIME_BUDGET_S,
    )


def _logical_path(relative_parts: tuple[str, ...]) -> str:
    return posixpath.join(_LOGICAL_ROOT, *relative_parts)


def _native_path(home: Path, logical_path: str) -> Path:
    relative_parts = PurePosixPath(logical_path).parts[1:]
    return home.joinpath(*relative_parts)


def _is_excluded_directory(relative_parts: tuple[str, ...]) -> bool:
    if not relative_parts:
        return False
    if relative_parts[-1] in _SKIP_DIR_NAMES:
        return True
    return any(
        len(relative_parts) >= len(suffix) and relative_parts[-len(suffix) :] == suffix
        for suffix in _SKIP_DIR_SUFFIXES
    )


def _is_skipped_home_root_dot_directory(relative_parts: tuple[str, ...]) -> bool:
    """Skip a home-root dot-directory only when it is known client/tool/OS state.

    Such roots (``.claude``, ``.config``, ``.local``, ``.vscode-server``, ...)
    never hold a user's project checkout: their direct artifacts are user-scope
    (excluded from a project walk anyway) and their subtrees like
    ``.claude/projects`` are huge, so alphabetical DFS would explore them before
    any real project and burn the time budget over slow 9P mounts.

    Skipping *every* dot-directory instead would silently miss nested project
    configs, skills, and agents inside an unknown one (e.g. a versioned
    ``~/.dotfiles`` repo) — ``_classify_project_file`` only drops home-root
    artifacts (``project_path == "/"``), not nested ones — so those are descended.
    """
    return len(relative_parts) == 1 and relative_parts[0] in _SKIPPED_HOME_ROOT_DOT_DIRS


def _is_marker_ancestor(
    suffix: tuple[str, ...],
    marker: tuple[str, ...],
) -> bool:
    """The directory at *suffix* is the marker directory or on the path to it."""
    return len(suffix) <= len(marker) and suffix == marker[: len(suffix)]


def _can_descend_project_tree(
    relative_parts: tuple[str, ...],
    project_specs: list[_ProjectConfigSpec],
) -> bool:
    """Descent pruning gate: True if this directory can lead to a matched file.

    Superset invariant: this must return True for *every* ancestor directory of
    *every* path the project-tree matchers accept
    (``_project_candidates_for_path`` / ``_project_skill_file_match`` /
    ``_project_agent_definition_match``). It hand-re-encodes their structural
    rules — depth <= ``MAX_PROJECT_TREE_DEPTH``, config-marker ancestors,
    dot-dir-before-``skills``, and agent ``project_markers`` /
    ``project_recursive`` — in this module, separate from the matchers it must
    stay a superset of. Correct today, but if a matcher shape changes and this
    gate is not widened to match, it prunes too tight and the walk silently
    drops artifacts with no error — the worst failure mode. Staying a superset
    only costs a little extra walking. Enforced by
    ``test_descent_gate_is_superset_of_every_matcher_accepted_path``.
    """
    if len(relative_parts) <= MAX_PROJECT_TREE_DEPTH:
        return True

    for project_depth in range(MAX_PROJECT_TREE_DEPTH + 1):
        suffix = relative_parts[project_depth:]
        if not suffix:
            continue
        # Project configs live at an exact relative path, so only the marker
        # directory and its ancestors matter — never the marker's subtree.
        if any(
            _is_marker_ancestor(suffix, spec.relative_parts[:-1])
            for spec in project_specs
            if len(spec.relative_parts) > 1
        ):
            return True
        if len(suffix) == 1 and suffix[0].startswith("."):
            return True
        if (
            "skills" in suffix
            and (skills_index := suffix.index("skills")) <= 1
            and (skills_index == 0 or suffix[0].startswith("."))
        ):
            return True
        for pattern in AGENT_DEFINITION_PATTERNS:
            for marker in pattern.project_markers:
                if _is_marker_ancestor(suffix, marker):
                    return True
                # Only recursive patterns place files below the marker dir.
                if pattern.project_recursive and suffix[: len(marker)] == marker:
                    return True
    return False


def _classify_project_file(
    logical_path: str,
    *,
    project_specs: list[_ProjectConfigSpec],
) -> _ProjectFileClassification | None:
    config_candidates = tuple(
        candidate
        for candidate in _project_candidates_for_path(
            logical_path,
            root_path=_LOGICAL_ROOT,
            specs=project_specs,
        )
        if candidate.project_path != _LOGICAL_ROOT
    )
    skill_match = _project_skill_file_match(
        logical_path,
        root_path=_LOGICAL_ROOT,
    )
    if skill_match is not None and skill_match.project_path == _LOGICAL_ROOT:
        skill_match = None
    agent_match = _project_agent_definition_match(
        logical_path,
        root_path=_LOGICAL_ROOT,
    )
    if agent_match is not None and agent_match[1] == _LOGICAL_ROOT:
        agent_match = None
    if not config_candidates and skill_match is None and agent_match is None:
        return None
    return _ProjectFileClassification(
        config_candidates=config_candidates,
        skill_match=skill_match,
        agent_match=agent_match,
    )


def _can_descend_path(
    relative_parts: tuple[str, ...],
    project_specs: list[_ProjectConfigSpec],
) -> bool:
    return not (
        _is_excluded_directory(relative_parts)
        or _is_skipped_home_root_dot_directory(relative_parts)
        or not _can_descend_project_tree(relative_parts, project_specs)
    )


def _target_is_covered_by_walk_areas(
    target: Path,
    *,
    is_directory: bool,
    walk_areas: list[tuple[Path, tuple[str, ...]]],
    project_specs: list[_ProjectConfigSpec],
) -> bool:
    canonical_target = Path(os.path.realpath(target))
    for actual_root, logical_parts in walk_areas:
        canonical_root = Path(os.path.realpath(actual_root))
        try:
            relative = canonical_target.relative_to(canonical_root)
        except ValueError:
            continue
        directory_parts = relative.parts if is_directory else relative.parts[:-1]
        if any(
            not _can_descend_path(
                (*logical_parts, *directory_parts[:index]),
                project_specs,
            )
            for index in range(1, len(directory_parts) + 1)
        ):
            continue
        if is_directory:
            return True
        logical_path = _logical_path((*logical_parts, *relative.parts))
        if (
            _classify_project_file(logical_path, project_specs=project_specs)
            is not None
        ):
            return True
    return False


def _classify_wsl_entry(
    entry: os.DirEntry[str],
    *,
    classification: _ProjectFileClassification | None,
    can_descend: bool,
    walk_areas: list[tuple[Path, tuple[str, ...]]],
    project_specs: list[_ProjectConfigSpec],
    symlink_policy: SymlinkFollowPolicy,
) -> _ClassifiedWslEntry | None:
    entry_path = Path(entry.path)
    link_status = link_or_reparse_status(entry_path)
    if link_status is None:
        return None
    followed = link_status
    if not followed:
        try:
            return _ClassifiedWslEntry(
                candidate=entry_path,
                is_directory=entry.is_dir(follow_symlinks=False),
                is_file=entry.is_file(follow_symlinks=False),
                followed=False,
            )
        except OSError:
            return None
    if classification is None and not can_descend:
        return None
    target_hint = symlink_policy.inspect(entry_path)
    if target_hint is None:
        return None
    try:
        target_hint_mode = target_hint.stat().st_mode
    except OSError:
        return None
    target_is_file = stat.S_ISREG(target_hint_mode)
    target_is_directory = stat.S_ISDIR(target_hint_mode)
    target_is_usable = (target_is_file and classification is not None) or (
        target_is_directory and can_descend
    )
    if not target_is_usable:
        return None
    if _target_is_covered_by_walk_areas(
        target_hint,
        is_directory=target_is_directory,
        walk_areas=walk_areas,
        project_specs=project_specs,
    ):
        return None
    if target_is_directory and not symlink_policy.claim(target_hint):
        return None
    return _ClassifiedWslEntry(
        candidate=target_hint,
        is_directory=target_is_directory,
        is_file=target_is_file,
        followed=True,
    )


def _read_bounded_file(
    path: Path,
    *,
    byte_budget: _ArtifactByteBudget,
) -> bytes | None:
    if link_or_reparse_status(path) is not False:
        return None
    content = read_bounded(path, max_bytes=MAX_SINGLE_FILE_BYTES)
    if content is None:
        return None
    byte_budget.charge(len(content))
    return content


def _configuration_from_candidate(
    *,
    home: Path,
    candidate: _ConfigCandidate,
    content: bytes,
) -> MCPClientConfig | None:
    servers = parse_config_content(candidate.client, content)
    if not servers or candidate.project_path is None:
        return None
    config_path = str(_native_path(home, candidate.path))
    project_path = str(_native_path(home, candidate.project_path))
    for server in servers:
        server.project_name = project_path
    return MCPClientConfig(
        client=candidate.client.name,
        config_path=config_path,
        servers=servers,
        config_scope="project",
        project_path=project_path,
    )


def _skills_from_files(
    *,
    home: Path,
    files: dict[str, bytes],
    classifications: dict[str, _ProjectFileClassification],
) -> list[DiscoveredSkillArtifact]:
    skills: list[DiscoveredSkillArtifact] = []
    for logical_skill_path, logical_project_path, skill_files in _iter_skill_groups(
        files, classifications
    ):
        native_skill_path = _native_path(home, logical_skill_path)
        artifact = build_skill_artifact_from_files(
            skill_path=str(native_skill_path),
            files=skill_files,
            scope="project",
            tool="multi",
            project_path=str(_native_path(home, logical_project_path)),
            fallback_name=native_skill_path.name,
            source_type="user",
        )
        if artifact is not None:
            skills.append(artifact)
    return skills


def _agent_definitions_from_files(
    *,
    home: Path,
    files: dict[str, bytes],
    classifications: dict[str, _ProjectFileClassification],
) -> list[DiscoveredAgentDefinition]:
    definitions: list[DiscoveredAgentDefinition] = []
    for pattern, logical_path, logical_project_path, content in _iter_agent_matches(
        files, classifications
    ):
        definition = parse_agent_definition(
            client=pattern.client,
            path=str(_native_path(home, logical_path)),
            content=content,
            scope="project",
            project_path=str(_native_path(home, logical_project_path)),
        )
        if definition is not None:
            definitions.append(definition)
    return definitions


def _walk_wsl_home(
    *,
    home: Path,
    actual_home: Path,
    project_specs: list[_ProjectConfigSpec],
    deadline: float,
    byte_budget: _ArtifactByteBudget,
    symlink_policy: SymlinkFollowPolicy,
) -> _HomeWalkResult:
    files: dict[str, bytes] = {}
    classifications: dict[str, _ProjectFileClassification] = {}
    matched_file_count = 0
    pending: list[tuple[Path, tuple[str, ...]]] = [(actual_home, ())]
    walk_areas: list[tuple[Path, tuple[str, ...]]] = [(actual_home, ())]
    budget_exhausted = False
    try:
        while pending and matched_file_count < MAX_WSL_PROJECT_MATCHED_FILES:
            if time.monotonic() >= deadline:
                raise _CollectionBudgetExhausted
            directory, directory_parts = pending.pop()
            try:
                with os.scandir(directory) as entries:
                    bounded_entries = []
                    for entry in entries:
                        if time.monotonic() >= deadline:
                            raise _CollectionBudgetExhausted
                        bounded_entries.append(entry)
                    sorted_entries = sorted(
                        bounded_entries,
                        key=lambda entry: (entry.name.casefold(), entry.name),
                    )
            except OSError:
                continue

            child_directories: list[tuple[Path, tuple[str, ...]]] = []
            for entry in sorted_entries:
                if time.monotonic() >= deadline:
                    raise _CollectionBudgetExhausted
                relative_parts = (*directory_parts, entry.name)
                logical_path = _logical_path(relative_parts)
                classification = _classify_project_file(
                    logical_path,
                    project_specs=project_specs,
                )
                can_descend = _can_descend_path(relative_parts, project_specs)
                classified_entry = _classify_wsl_entry(
                    entry,
                    classification=classification,
                    can_descend=can_descend,
                    walk_areas=walk_areas,
                    project_specs=project_specs,
                    symlink_policy=symlink_policy,
                )
                if classified_entry is None:
                    continue
                candidate = classified_entry.candidate
                if classified_entry.is_directory:
                    if not can_descend:
                        continue
                    if classified_entry.followed:
                        symlink_policy.add_scan_area(candidate, 0)
                        walk_areas.append((candidate, relative_parts))
                    child_directories.append((candidate, relative_parts))
                    continue
                if not classified_entry.is_file or classification is None:
                    continue
                if matched_file_count >= MAX_WSL_PROJECT_MATCHED_FILES:
                    break
                content = _read_bounded_file(candidate, byte_budget=byte_budget)
                if content is None:
                    continue
                if classified_entry.followed and not symlink_policy.claim(candidate):
                    continue
                matched_file_count += 1
                classifications[logical_path] = classification
                files[logical_path] = content

            pending.extend(reversed(child_directories))
    except _CollectionBudgetExhausted:
        budget_exhausted = True

    artifacts = _CollectedWSLProjectArtifacts()
    for logical_path, content in files.items():
        for candidate in classifications[logical_path].config_candidates:
            configuration = _configuration_from_candidate(
                home=home,
                candidate=candidate,
                content=content,
            )
            if configuration is not None:
                artifacts.configurations.append(configuration)
    artifacts.skills.extend(
        _skills_from_files(
            home=home,
            files=files,
            classifications=classifications,
        )
    )
    artifacts.agent_definitions.extend(
        _agent_definitions_from_files(
            home=home,
            files=files,
            classifications=classifications,
        )
    )
    return _HomeWalkResult(
        artifacts=artifacts,
        budget_exhausted=budget_exhausted,
    )


def _scan_wsl_projects(
    *,
    clients: list[MCPClientDefinition],
    wsl_homes: list[Path],
    time_budget: float | None,
) -> WSLProjectScanResult:
    unique_homes = list(dict.fromkeys(wsl_homes))
    budget_seconds = (
        _scaled_wsl_scan_time_budget(len(unique_homes))
        if time_budget is None
        else max(time_budget, 0.0)
    )
    deadline = time.monotonic() + budget_seconds
    byte_budget = _ArtifactByteBudget()
    project_specs = _project_config_specs(clients)
    artifacts = _CollectedWSLProjectArtifacts()
    windows_system_context = is_windows_system_context()
    admissible_homes = [
        home
        for home in unique_homes
        if not (windows_system_context and has_link_or_reparse_component(home))
    ]
    direct_homes = []
    for home in admissible_homes:
        try:
            if link_or_reparse_status(home) is False and home.is_dir():
                direct_homes.append(home)
        except OSError:
            continue
    symlink_policy = SymlinkFollowPolicy(
        scan_areas=[(home, 0) for home in direct_homes],
        max_followed=MAX_FOLLOWED_WSL_PROJECT_TARGETS,
        windows_system_context=windows_system_context,
    )
    for home in admissible_homes:
        actual_home = home
        try:
            link_status = link_or_reparse_status(home)
            if link_status is None:
                continue
            if link_status:
                target_hint = symlink_policy.inspect(home)
                if target_hint is None:
                    continue
                target_hint_mode = target_hint.stat().st_mode
                if not stat.S_ISDIR(target_hint_mode):
                    continue
                if not symlink_policy.claim(target_hint):
                    continue
                actual_home = target_hint
                symlink_policy.add_scan_area(
                    actual_home,
                    0,
                )
            elif not home.is_dir():
                continue
        except OSError:
            continue
        walk_result = _walk_wsl_home(
            home=home,
            actual_home=actual_home,
            project_specs=project_specs,
            deadline=deadline,
            byte_budget=byte_budget,
            symlink_policy=symlink_policy,
        )
        artifacts.configurations.extend(walk_result.artifacts.configurations)
        artifacts.skills.extend(walk_result.artifacts.skills)
        artifacts.agent_definitions.extend(walk_result.artifacts.agent_definitions)
        if walk_result.budget_exhausted:
            break

    logger.info(
        "WSL project scan complete",
        home_count=len(unique_homes),
        config_count=len(artifacts.configurations),
        skill_count=len(artifacts.skills),
        agent_definition_count=len(artifacts.agent_definitions),
    )
    return WSLProjectScanResult(
        configurations=artifacts.configurations,
        skills=artifacts.skills,
        agent_definitions=dedupe_agent_definitions(artifacts.agent_definitions),
    )


def scan_wsl_projects(
    *,
    clients: list[MCPClientDefinition] | None = None,
    wsl_homes: list[Path] | None = None,
    time_budget: float | None = None,
) -> WSLProjectScanResult:
    """Discover project configs, skills, and agent definitions in WSL homes."""
    try:
        return _scan_wsl_projects(
            clients=clients if clients is not None else get_all_clients(),
            wsl_homes=wsl_homes if wsl_homes is not None else _wsl_homes(),
            time_budget=time_budget,
        )
    except Exception as exc:
        logger.warning(
            "WSL project scan failed",
            error_type=type(exc).__name__,
            exc_info=True,
        )
        return WSLProjectScanResult()
