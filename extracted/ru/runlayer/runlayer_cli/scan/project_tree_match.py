"""Shared path matching for bounded project-tree artifact scans.

The WSL walk prunes directories with
``wsl_projects._can_descend_project_tree``, which hand-re-encodes the structural
rules of the matchers below (depth, config-marker ancestors,
dot-dir-before-``skills``, agent ``project_markers`` / ``project_recursive``).
That gate must stay a *superset* of every path these matchers accept: if you
change a matcher's shape here, widen the gate to match, or the walk silently
drops artifacts with no error.
``test_descent_gate_is_superset_of_every_matcher_accepted_path`` enforces the
invariant.
"""

from __future__ import annotations

import posixpath
from collections.abc import Iterator
from dataclasses import dataclass, replace

from runlayer_cli.scan.agent_definition_scanner import (
    AGENT_DEFINITION_PATTERNS,
    AgentDefinitionPattern,
    match_project_marker,
)
from runlayer_cli.scan.clients import MCPClientDefinition
from runlayer_cli.scan.skill_scanner import (
    SUPPORTED_EXTENSIONS as SKILL_SUPPORTED_EXTENSIONS,
)

MAX_PROJECT_TREE_DEPTH = 4


@dataclass(frozen=True)
class _ConfigCandidate:
    client: MCPClientDefinition
    path: str
    project_path: str | None = None


@dataclass(frozen=True)
class _ProjectConfigSpec:
    client: MCPClientDefinition
    relative_parts: tuple[str, ...]


@dataclass(frozen=True)
class _SkillFileMatch:
    skill_path: str
    project_path: str
    relative_file: str


@dataclass(frozen=True)
class _ProjectFileClassification:
    """One work-tree file's config/skill/agent matches, computed once.

    Shared between a walker's file-selection predicate and its artifact builders
    so the path-matching logic runs in a single place (no drift, no recompute).
    """

    config_candidates: tuple[_ConfigCandidate, ...]
    skill_match: _SkillFileMatch | None
    agent_match: tuple[AgentDefinitionPattern, str] | None


def _posix_path_within(path: str, root: str) -> bool:
    normalized_path = posixpath.normpath(path)
    normalized_root = posixpath.normpath(root)
    return normalized_path == normalized_root or normalized_path.startswith(
        normalized_root.rstrip("/") + "/"
    )


def _project_config_specs(
    clients: list[MCPClientDefinition],
) -> list[_ProjectConfigSpec]:
    specs: list[_ProjectConfigSpec] = []
    seen: set[tuple[str, tuple[str, ...], str]] = set()
    for client in clients:
        for pattern in client.iter_project_configs():
            if pattern.relative_path.startswith("/"):
                continue
            relative_path = posixpath.normpath(pattern.relative_path)
            relative_parts = tuple(relative_path.split("/"))
            if (
                relative_path == "."
                or ".." in relative_parts
                or any(not part for part in relative_parts)
            ):
                continue
            key = (client.name, relative_parts, pattern.servers_key)
            if key in seen:
                continue
            seen.add(key)
            specs.append(
                _ProjectConfigSpec(
                    client=replace(
                        client,
                        paths=[],
                        servers_key=pattern.servers_key,
                        additional_servers_keys=None,
                    ),
                    relative_parts=relative_parts,
                )
            )
    return specs


def _project_candidates_for_path(
    path: str,
    *,
    root_path: str,
    specs: list[_ProjectConfigSpec],
) -> list[_ConfigCandidate]:
    root_path = posixpath.normpath(root_path)
    path = posixpath.normpath(path)
    if not _posix_path_within(path, root_path) or path == root_path:
        return []
    relative_parts = tuple(posixpath.relpath(path, root_path).split("/"))
    candidates: list[_ConfigCandidate] = []
    for spec in specs:
        pattern_size = len(spec.relative_parts)
        if (
            len(relative_parts) < pattern_size
            or relative_parts[-pattern_size:] != spec.relative_parts
        ):
            continue
        project_parts = relative_parts[:-pattern_size]
        if len(project_parts) > MAX_PROJECT_TREE_DEPTH:
            continue
        project_path = (
            posixpath.join(root_path, *project_parts) if project_parts else root_path
        )
        candidates.append(
            _ConfigCandidate(
                client=spec.client,
                path=path,
                project_path=project_path,
            )
        )
    return candidates


def _project_skill_file_match(
    path: str,
    *,
    root_path: str,
) -> _SkillFileMatch | None:
    """Match one supported file under ``*/skills/<name>`` in a project tree."""
    root_path = posixpath.normpath(root_path)
    path = posixpath.normpath(path)
    if (
        not _posix_path_within(path, root_path)
        or path == root_path
        or posixpath.splitext(path)[1].lower() not in SKILL_SUPPORTED_EXTENSIONS
    ):
        return None

    relative_parts = tuple(posixpath.relpath(path, root_path).split("/"))
    for skills_index, part in enumerate(relative_parts[:-2]):
        if part != "skills":
            continue
        prefix_parts = relative_parts[:skills_index]
        project_parts = (
            prefix_parts[:-1]
            if prefix_parts and prefix_parts[-1].startswith(".")
            else prefix_parts
        )
        if len(project_parts) > MAX_PROJECT_TREE_DEPTH:
            continue
        project_path = (
            posixpath.join(root_path, *project_parts) if project_parts else root_path
        )
        skill_path = posixpath.join(
            root_path,
            *relative_parts[: skills_index + 2],
        )
        relative_file = posixpath.join(*relative_parts[skills_index + 2 :])
        return _SkillFileMatch(
            skill_path=skill_path,
            project_path=project_path,
            relative_file=relative_file,
        )
    return None


def _project_agent_definition_match(
    path: str,
    *,
    root_path: str,
) -> tuple[AgentDefinitionPattern, str] | None:
    root_path = posixpath.normpath(root_path)
    path = posixpath.normpath(path)
    if not _posix_path_within(path, root_path) or path == root_path:
        return None
    relative_parts = tuple(posixpath.relpath(path, root_path).split("/"))
    for pattern in AGENT_DEFINITION_PATTERNS:
        project_parts_size = match_project_marker(relative_parts, pattern)
        if project_parts_size is None:
            continue
        project_parts = relative_parts[:project_parts_size]
        if len(project_parts) > MAX_PROJECT_TREE_DEPTH:
            continue
        project_path = (
            posixpath.join(root_path, *project_parts) if project_parts else root_path
        )
        return pattern, project_path
    return None


def _iter_skill_groups(
    files: dict[str, bytes],
    classifications: dict[str, _ProjectFileClassification],
) -> Iterator[tuple[str, str, dict[str, bytes]]]:
    """Yield ``(skill_path, project_path, files)`` per skill dir, sorted by skill_path.

    Buckets every skill-matched file under its ``skills/<name>`` dir, then yields
    deterministically so each walker's build loop differs only in the artifact it
    constructs (native-path remap vs. container metadata) — mirroring
    ``_iter_agent_matches`` so both builder families share one skeleton.
    """
    grouped: dict[str, tuple[str, dict[str, bytes]]] = {}
    for path, content in files.items():
        skill_match = classifications[path].skill_match
        if skill_match is None:
            continue
        _project_path, skill_files = grouped.setdefault(
            skill_match.skill_path,
            (skill_match.project_path, {}),
        )
        skill_files[skill_match.relative_file] = content
    for skill_path in sorted(grouped):
        project_path, skill_files = grouped[skill_path]
        yield skill_path, project_path, skill_files


def _iter_agent_matches(
    files: dict[str, bytes],
    classifications: dict[str, _ProjectFileClassification],
) -> Iterator[tuple[AgentDefinitionPattern, str, str, bytes]]:
    """Yield ``(pattern, path, project_path, content)`` per agent-matched file.

    Deterministically ordered by path so each walker's build loop only differs in
    the definition it constructs (native-path remap vs. container metadata).
    """
    for path in sorted(files):
        agent_match = classifications[path].agent_match
        if agent_match is None:
            continue
        pattern, project_path = agent_match
        yield pattern, path, project_path, files[path]
