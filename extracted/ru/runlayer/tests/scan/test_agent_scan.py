"""Agent-scan orchestration: root unification and channel gating."""

from __future__ import annotations

import time
from pathlib import Path

from runlayer_cli.scan import agent_scan
from runlayer_cli.scan.agent_scan import (
    collect_static_roots,
    discover_agents,
    discover_install_agents,
    discover_static_agents,
    filter_static_skill_descendants,
    parse_crawl_manifests,
)
from runlayer_cli.scan.agents.detect import (
    METHOD_INSTALL,
    METHOD_STATIC,
    DiscoveredAgent,
)
from runlayer_cli.scan.agents import discover as discover_mod
from runlayer_cli.scan.agents.discover import discover
from runlayer_cli.scan.agents.install import INSTALL_PROBES, InstallProbe
from runlayer_cli.scan.agents.manifests import ManifestInfo
from runlayer_cli.scan.agents.openclaw_detector import (
    OpenClawDetection,
    build_openclaw_agent,
)

LANGCHAIN_PYPROJECT = """
[project]
name = "x"
dependencies = ["langchain>=0.3", "langchain-openai>=0.2"]
"""
LANGCHAIN_SOURCE = """
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

agent = create_tool_calling_agent(llm, tools, prompt)
executor = AgentExecutor(agent=agent, tools=tools)
executor.invoke({"input": "hi"})
"""


def _running_detection() -> OpenClawDetection:
    return OpenClawDetection(
        detected=True,
        summary="installed",
        cli_path="/usr/local/bin/openclaw",
        cli_version="2026.1.15",
    )


def _openclaw_probes(detection: OpenClawDetection) -> tuple[InstallProbe, ...]:
    """Single-probe registry yielding ``detection`` with the real OpenClaw
    builder, so install-channel tests drive the data-driven probe path (F5)."""
    return (
        InstallProbe(
            name="openclaw",
            detect=lambda: detection,
            build_agent=build_openclaw_agent,
            runtime=INSTALL_PROBES[0].runtime,
        ),
    )


def _make_langchain(root):
    root.mkdir(parents=True, exist_ok=True)
    (root / "pyproject.toml").write_text(LANGCHAIN_PYPROJECT)
    (root / "agent.py").write_text(LANGCHAIN_SOURCE)
    return root


# ── collect_static_roots: F2/F3 coverage seam ───────────────────────────────


def test_collect_static_roots_unions_all_signals(tmp_path):
    mcp = tmp_path / "mcp"
    skill = tmp_path / "skill"
    manifest_dir = tmp_path / "manifest_only"
    for d in (mcp, skill, manifest_dir):
        d.mkdir()

    roots = collect_static_roots(
        found_paths=[manifest_dir / "package.json"],
        mcp_project_paths=[mcp],
        skill_paths=[skill],
    )

    assert set(roots) == {mcp.resolve(), skill.resolve(), manifest_dir.resolve()}


def test_collect_static_roots_uses_manifest_parents_not_files(tmp_path):
    proj = tmp_path / "proj"
    proj.mkdir()

    roots = collect_static_roots(
        found_paths=[proj / "pyproject.toml"],
        mcp_project_paths=[],
        skill_paths=[],
    )

    assert roots == [proj.resolve()]


def test_collect_static_roots_ignores_non_manifest_hits(tmp_path):
    # A skill file or stray text hit is not a manifest -> contributes no root.
    roots = collect_static_roots(
        found_paths=[tmp_path / "proj" / "SKILL.md", tmp_path / "x" / "README.md"],
        mcp_project_paths=[],
        skill_paths=[],
    )

    assert roots == []


def test_collect_static_roots_prunes_nested_paths(tmp_path):
    parent = tmp_path / "proj"
    child = parent / "packages" / "inner"
    child.mkdir(parents=True)

    # Same tree reached via an MCP root (parent) and a skill root (nested child).
    roots = collect_static_roots(
        found_paths=[],
        mcp_project_paths=[parent],
        skill_paths=[child],
    )

    assert roots == [parent.resolve()]


# ── parse_crawl_manifests + seeding: F2 (no find→walk re-parse) ──────────────


def test_parse_crawl_manifests_keyed_by_resolved_path_ignores_non_manifests(tmp_path):
    proj = tmp_path / "proj"
    proj.mkdir()
    manifest = proj / "pyproject.toml"
    manifest.write_text("[project]\nname='x'\ndependencies=['langchain']\n")
    (proj / "README.md").write_text("hi")

    seeds = parse_crawl_manifests([manifest, proj / "README.md"])

    assert set(seeds) == {manifest.resolve()}
    assert "langchain" in seeds[manifest.resolve()].deps


def test_discover_reuses_seeded_manifest_instead_of_reparsing(tmp_path, monkeypatch):
    proj = tmp_path / "proj"
    proj.mkdir()
    manifest = proj / "pyproject.toml"
    manifest.write_text("[project]\nname='x'\ndependencies=['langchain']\n")
    (proj / "agent.py").write_text("x = 1\n")

    # Sentinel dep is NOT in the file: it can only appear if discover reused the
    # seed rather than re-parsing the manifest.
    seed = ManifestInfo(
        path=manifest, kind="pyproject.toml", ecosystem="python", deps=["sentinel-dep"]
    )
    calls: list[Path] = []
    real_parse = discover_mod.parse_manifest
    monkeypatch.setattr(
        discover_mod,
        "parse_manifest",
        lambda p: (calls.append(Path(p).resolve()), real_parse(p))[1],
    )

    units = discover(proj, seed_manifests={manifest.resolve(): seed})

    unit = next(u for u in units if u.root == proj)
    assert "sentinel-dep" in unit.deps
    assert manifest.resolve() not in calls  # reused, never re-parsed


def test_discover_still_parses_manifest_absent_from_seed(tmp_path):
    """Seeding must never drop coverage: a manifest the crawl didn't seed (e.g.
    nested deeper than crawl depth) is still parsed by the walk."""
    proj = tmp_path / "proj"
    sub = proj / "packages" / "inner"
    sub.mkdir(parents=True)
    (proj / "pyproject.toml").write_text("[project]\nname='x'\n")
    (sub / "package.json").write_text('{"dependencies": {"ai": "^5"}}')

    # Seed only the top-level manifest.
    seeds = parse_crawl_manifests([proj / "pyproject.toml"])
    units = discover(proj, seed_manifests=seeds)

    assert any("ai" in u.deps for u in units)


# ── discover_static_agents: best-effort, never raises ────────────────────────


def test_discover_static_agents_empty_roots_short_circuits(monkeypatch):
    # No roots -> never even loads the detector.
    def _boom(*_a, **_k):
        raise AssertionError("collect_agents must not run for empty roots")

    monkeypatch.setattr(agent_scan, "collect_agents", _boom)
    assert discover_static_agents([]) == []


def test_discover_static_agents_swallows_errors(monkeypatch, tmp_path):
    def _boom(*_a, **_k):
        raise RuntimeError("detector exploded")

    monkeypatch.setattr(agent_scan, "collect_agents", _boom)
    assert discover_static_agents([tmp_path]) == []


def test_discover_static_agents_detects_framework(tmp_path):
    proj = _make_langchain(tmp_path / "proj")

    agents = discover_static_agents([proj])

    assert any(a.framework_id == "langchain" for a in agents)


# ── discover_install_agents: the OpenClaw install probe (F1) ─────────────────


def test_install_agent_emitted_when_detected(monkeypatch):
    monkeypatch.setattr(
        agent_scan, "INSTALL_PROBES", _openclaw_probes(_running_detection())
    )

    result = discover_install_agents()

    assert [a.framework_id for a in result.agents] == ["openclaw"]
    assert result.agents[0].detection_method == "install"


def test_install_agents_empty_when_not_detected(monkeypatch):
    monkeypatch.setattr(
        agent_scan,
        "INSTALL_PROBES",
        _openclaw_probes(OpenClawDetection(detected=False)),
    )

    result = discover_install_agents()

    assert result.agents == []


# ── discover_agents: one flag, two channels (F4) ─────────────────────────────


def test_discover_agents_runs_both_channels(monkeypatch, tmp_path):
    monkeypatch.setattr(
        agent_scan, "INSTALL_PROBES", _openclaw_probes(_running_detection())
    )
    proj = _make_langchain(tmp_path / "proj")

    result = discover_agents(found_paths=[proj / "pyproject.toml"])

    framework_ids = {a.framework_id for a in result.agents}
    assert {"openclaw", "langchain"} <= framework_ids


def test_discover_agents_install_only(monkeypatch, tmp_path):
    monkeypatch.setattr(
        agent_scan, "INSTALL_PROBES", _openclaw_probes(_running_detection())
    )
    proj = _make_langchain(tmp_path / "proj")

    result = discover_agents(found_paths=[proj / "pyproject.toml"], detect_static=False)

    assert {a.framework_id for a in result.agents} == {"openclaw"}


def test_discover_agents_disabled_install_skips_detection(monkeypatch, tmp_path):
    # Even when OpenClaw IS present, detect_install=False must not run it.
    monkeypatch.setattr(
        agent_scan, "INSTALL_PROBES", _openclaw_probes(_running_detection())
    )
    proj = _make_langchain(tmp_path / "proj")

    result = discover_agents(
        found_paths=[proj / "pyproject.toml"],
        detect_install=False,
    )

    framework_ids = {a.framework_id for a in result.agents}
    assert "openclaw" not in framework_ids
    assert "langchain" in framework_ids


# ── scaling: minimization + skill filtering on worktree-heavy machines ───────


def _agent(location: Path, method: str = METHOD_STATIC) -> DiscoveredAgent:
    return DiscoveredAgent(
        location=str(location),
        name=location.name,
        framework_id="langchain",
        display_name="LangChain",
        language="python",
        confidence=1.0,
        margin=1.0,
        score=2.0,
        runner_up=None,
        runner_up_score=0.0,
        detection_method=method,
        evidence=[],
    )


def test_minimal_roots_name_prefix_is_not_ancestry(tmp_path):
    # "proj-extra" shares proj's string prefix but is a sibling tree.
    proj = tmp_path / "proj"
    sibling = tmp_path / "proj-extra"
    nested = proj / "inner"
    nested.mkdir(parents=True)
    sibling.mkdir()

    minimal = agent_scan._minimal_roots([proj, sibling, nested])

    assert set(minimal) == {proj.resolve(), sibling.resolve()}


def test_minimal_roots_scales_to_thousands_of_disjoint_roots(tmp_path):
    """Worktree-heavy machines yield thousands of disjoint roots. Probing each
    candidate's parent chain is O(n * depth); scanning every kept root per
    candidate is O(n^2 * depth) — whole minutes of CPU at fleet-observed sizes
    (root_count=3638)."""
    roots = [tmp_path / f"wt{i:04d}" / "repo" / "backend" for i in range(1200)]

    start = time.perf_counter()
    minimal = agent_scan._minimal_roots(roots)
    elapsed = time.perf_counter() - start

    assert len(minimal) == len(roots)
    assert elapsed < 3.0, f"_minimal_roots took {elapsed:.1f}s for 1200 roots"


def test_skill_filter_drops_only_strict_static_descendants(tmp_path):
    skill = tmp_path / "skills" / "writer"
    at_root = _agent(skill)
    nested = _agent(skill / "examples" / "demo")
    outside = _agent(tmp_path / "elsewhere")
    installed_under_skill = _agent(skill / "tool", method=METHOD_INSTALL)

    kept = filter_static_skill_descendants(
        [at_root, nested, outside, installed_under_skill], [skill]
    )

    assert kept == [at_root, outside, installed_under_skill]


def test_skill_filter_scales_to_many_agents_and_skills(tmp_path):
    """Per-agent work must be O(depth) set probes, not a pass over every skill
    root (fleet-observed sizes: ~480 agents x ~2000 skill roots)."""
    skills = [tmp_path / "skills" / f"s{i:04d}" for i in range(900)]
    agents = [_agent(tmp_path / "projects" / f"p{i:04d}" / "agent") for i in range(300)]

    start = time.perf_counter()
    kept = filter_static_skill_descendants(agents, skills)
    elapsed = time.perf_counter() - start

    assert len(kept) == len(agents)
    assert elapsed < 2.5, f"filter took {elapsed:.1f}s for 300 agents x 900 skills"
