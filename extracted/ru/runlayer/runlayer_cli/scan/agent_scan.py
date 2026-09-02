"""Agent-detection orchestration: the one entry point the scan calls.

Owns both agent-detection channels so :mod:`runlayer_cli.scan.service` doesn't
grow per-channel phases:

* **install** -- binary/service/port/container probes (currently OpenClaw),
* **static** -- dependency-manifest + source scoring over filesystem roots.

Both channels yield :class:`~runlayer_cli.scan.agents.detect.DiscoveredAgent`
objects; the scan submits them via ``POST /ai-watch/agents`` (see
``submit_discovered_agents``). The main scan flow never special-cases a specific
agent.

Standard-library + ``structlog`` only; safe for the frozen ``aiwatch`` bundle.
"""

from __future__ import annotations

import time
from collections.abc import Callable, Iterable, Mapping
from dataclasses import dataclass, field
from pathlib import Path

import structlog

from runlayer_cli.scan.agents.detect import (
    METHOD_STATIC,
    DiscoveredAgent,
    collect_agents,
)
from runlayer_cli.scan.agents.install import INSTALL_PROBES
from runlayer_cli.scan.agents.manifests import (
    ManifestInfo,
    manifest_kind,
    parse_manifest,
)
from runlayer_cli.scan.resource_governor import ScanResourceLimitExceeded

logger = structlog.get_logger(__name__)


@dataclass
class AgentScanResult:
    """Discovered agents from every enabled detection channel."""

    agents: list[DiscoveredAgent] = field(default_factory=list)


def discover_install_agents() -> AgentScanResult:
    """Run every registered install probe and return the discovered agents.

    Iterates the data-driven :data:`~runlayer_cli.scan.agents.install.INSTALL_PROBES`
    registry (probe -> build_agent), so adding an install-detected agent is a
    registration, not another branch here (F5).
    """
    result = AgentScanResult()
    for probe in INSTALL_PROBES:
        detection = probe.detect()
        if not detection.detected:
            logger.debug("install agent not detected", probe=probe.name)
            continue

        agent = probe.build_agent(detection)
        if agent:
            result.agents.append(agent)
        logger.info(
            "install agent detected",
            probe=probe.name,
            summary=detection.summary,
        )
    return result


def collect_static_roots(
    found_paths: Iterable[Path],
    mcp_project_paths: Iterable[Path],
    skill_paths: Iterable[Path],
) -> list[Path]:
    """Unify the roots static detection should walk.

    One root set drawn from every project-bearing signal the unified crawl
    already produced -- MCP config dirs, project skill dirs, and the parents of
    any agent manifest hit (``pyproject.toml`` / ``package.json`` / ...). This
    is what lets manifest-only and skill-only agent trees (no MCP config) be
    seen at all, instead of only dirs that happened to hold an MCP config.
    """
    roots: set[Path] = set()
    roots.update(Path(p) for p in mcp_project_paths)
    roots.update(Path(p) for p in skill_paths)
    for path in found_paths:
        path = Path(path)
        if manifest_kind(path.name) is not None:
            roots.add(path.parent)
    return _minimal_roots(roots)


def _minimal_roots(paths: Iterable[Path]) -> list[Path]:
    """Drop any path nested under another so each tree is walked once.

    Shallow-first order means a nested path always finds its ancestor already
    in ``kept``, so probing the candidate's own parent chain against the set is
    O(n * depth) — this runs over every project-bearing signal on the machine
    (thousands of roots on worktree-heavy hosts), where a per-candidate pass
    over the kept list is O(n^2 * depth) and dominates the whole scan.
    """
    resolved = sorted({p.resolve() for p in paths}, key=lambda p: len(p.parts))
    minimal: list[Path] = []
    kept: set[Path] = set()
    for path in resolved:
        if not any(parent in kept for parent in path.parents):
            minimal.append(path)
            kept.add(path)
    return minimal


def parse_crawl_manifests(found_paths: Iterable[Path]) -> dict[Path, ManifestInfo]:
    """Parse every dependency manifest the unified crawl already located, once.

    The Phase-2 ``find`` crawl already located each agent manifest; this parses
    them a single time (keyed by *resolved* path) so the static-detection walk
    can reuse them instead of re-parsing the same files (F2). The walk still
    owns *source* collection and still parses any manifest the crawl missed
    (e.g. nested deeper than the crawl depth), so coverage is unchanged.
    """
    seeds: dict[Path, ManifestInfo] = {}
    for path in found_paths:
        path = Path(path)
        if manifest_kind(path.name) is None:
            continue
        info = parse_manifest(path)
        if info is not None:
            seeds[path.resolve()] = info
    return seeds


def discover_static_agents(
    roots: Iterable[Path],
    *,
    seed_manifests: Mapping[Path, ManifestInfo] | None = None,
    time_budget_s: float | None = None,
    checkpoint: Callable[[], None] | None = None,
) -> list[DiscoveredAgent]:
    """Score agent frameworks over ``roots``; best-effort (never raises).

    Static detection must never fail the whole scan, so any error is logged and
    swallowed — except a resource-governor abort raised by *checkpoint*, which
    must stop the scan and so propagates. ``seed_manifests`` carries
    crawl-parsed manifests for reuse.

    ``time_budget_s`` bounds the source-tree walk (which reads every first-party
    file): without it, a shallow root over a big multi-repo home is unbounded
    I/O and can hang the scan. When set, the walk stops once the budget elapses
    and returns what it found so far. ``None`` means unbounded (used by tests /
    one-off tooling over small fixed roots).
    """
    root_list = list(roots)
    if not root_list:
        return []
    deadline = time.monotonic() + time_budget_s if time_budget_s else None
    logger.info(
        "Detecting AI-agent frameworks",
        root_count=len(root_list),
        time_budget_s=time_budget_s,
    )
    start = time.monotonic()
    try:
        agents = collect_agents(
            root_list,
            seed_manifests=seed_manifests,
            deadline=deadline,
            checkpoint=checkpoint,
        )
    except ScanResourceLimitExceeded:
        raise
    except Exception as exc:
        logger.warning(
            "agent_detection_failed",
            error=str(exc),
            error_type=type(exc).__name__,
        )
        return []
    truncated = deadline is not None and time.monotonic() >= deadline
    logger.info(
        "Agent detection complete",
        agents_found=len(agents),
        elapsed_s=round(time.monotonic() - start, 1),
        truncated=truncated,
    )
    return agents


def filter_static_skill_descendants(
    agents: Iterable[DiscoveredAgent],
    skill_paths: Iterable[Path],
) -> list[DiscoveredAgent]:
    """Drop static agents strictly nested under a reported skill.

    Probes each agent's parent chain against the skill-root set — O(depth) set
    lookups per agent, independent of how many skills the machine has (~2000
    at fleet-observed sizes).
    """
    skill_roots = {Path(path).resolve() for path in skill_paths}
    return [
        agent
        for agent in agents
        if agent.detection_method != METHOD_STATIC
        or not any(
            parent in skill_roots for parent in Path(agent.location).resolve().parents
        )
    ]


def discover_agents(
    *,
    found_paths: Iterable[Path] = (),
    mcp_project_paths: Iterable[Path] = (),
    skill_paths: Iterable[Path] = (),
    detect_static: bool = True,
    detect_install: bool = True,
    time_budget_s: float | None = None,
    checkpoint: Callable[[], None] | None = None,
) -> AgentScanResult:
    """Run the enabled agent-detection channels and return one combined result.

    The single seam the scan flow uses for all agent detection. ``time_budget_s``
    bounds only the static source walk (the install channel's probes are cheap
    and always run); see :func:`discover_static_agents`.
    """
    result = AgentScanResult()

    if detect_install:
        install = discover_install_agents()
        result.agents.extend(install.agents)

    if detect_static:
        # Materialize once: found_paths feeds both seed parsing and root derivation.
        found_list = list(found_paths)
        skill_list = list(skill_paths)
        prep_start = time.monotonic()
        seeds = parse_crawl_manifests(found_list)
        roots = collect_static_roots(found_list, mcp_project_paths, skill_list)
        # The prep and filter steps run outside discover_static_agents' time
        # budget, so they get their own timings — silent time here is invisible
        # in the per-phase durations otherwise.
        logger.debug(
            "static_agent_prep_complete",
            seed_count=len(seeds),
            root_count=len(roots),
            duration_ms=int((time.monotonic() - prep_start) * 1000),
        )
        static_agents = discover_static_agents(
            roots,
            seed_manifests=seeds,
            time_budget_s=time_budget_s,
            checkpoint=checkpoint,
        )
        filter_start = time.monotonic()
        kept = filter_static_skill_descendants(static_agents, skill_list)
        logger.debug(
            "static_skill_filter_complete",
            kept=len(kept),
            dropped=len(static_agents) - len(kept),
            duration_ms=int((time.monotonic() - filter_start) * 1000),
        )
        result.agents.extend(kept)

    return result
