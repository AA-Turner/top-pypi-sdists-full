"""Agent-scan orchestration: static-root unification is the fix for the flag
that agent detection only ran over MCP-config-bearing project dirs.

These lock in that a project found by ITS DEPENDENCY MANIFEST (or a project
skill dir) -- with no MCP config at all -- is still scanned for agents, and that
overlapping/nested roots collapse so each tree is walked once.
"""

from __future__ import annotations

from pathlib import Path

from runlayer_cli.scan.agent_scan import collect_static_roots, discover_agents
from runlayer_cli.scan.agents.manifests import (
    MANIFEST_KINDS,
    agent_manifest_search_filenames,
)

FIXTURES = Path(__file__).resolve().parents[2] / "fixtures" / "agent_detection"
SAMPLES = FIXTURES / "samples"


# --------------------------------------------------------------------------- #
# agent_manifest_search_filenames
# --------------------------------------------------------------------------- #


def test_search_filenames_cover_every_ecosystem():
    names = agent_manifest_search_filenames()
    for expected in (
        "pyproject.toml",
        "package.json",
        "go.mod",
        "Cargo.toml",
        "pom.xml",
    ):
        assert expected in names
    # .csproj is a glob so any C#/.NET project (e.g. SemanticKernelAgent.csproj)
    # is crawlable without enumerating exact names.
    assert "*.csproj" in names


def test_search_filenames_sourced_from_manifest_kinds():
    """No drift from the parsers -- everything the detector parses is searched."""
    names = set(agent_manifest_search_filenames())
    assert set(MANIFEST_KINDS).issubset(names)


# --------------------------------------------------------------------------- #
# collect_static_roots
# --------------------------------------------------------------------------- #


def test_manifest_parent_becomes_a_root_without_any_mcp_config(tmp_path):
    """THE flag fix: a manifest hit alone yields a root (no MCP config needed)."""
    proj = tmp_path / "proj"
    proj.mkdir()
    manifest = proj / "pyproject.toml"
    manifest.write_text("[project]\nname='x'\n", encoding="utf-8")

    roots = collect_static_roots([manifest], [], [])

    assert roots == [proj.resolve()]


def test_non_manifest_crawl_hits_are_ignored(tmp_path):
    proj = tmp_path / "proj"
    proj.mkdir()
    not_a_manifest = proj / "README.md"
    not_a_manifest.write_text("hi", encoding="utf-8")

    assert collect_static_roots([not_a_manifest], [], []) == []


def test_roots_union_mcp_skill_and_manifest_dirs(tmp_path):
    mcp_dir = tmp_path / "mcp_proj"
    skill_dir = tmp_path / "skill_proj"
    manifest_dir = tmp_path / "manifest_proj"
    for d in (mcp_dir, skill_dir, manifest_dir):
        d.mkdir()
    (manifest_dir / "package.json").write_text("{}", encoding="utf-8")

    roots = collect_static_roots(
        [manifest_dir / "package.json"],
        [mcp_dir],
        [skill_dir],
    )

    assert set(roots) == {
        mcp_dir.resolve(),
        skill_dir.resolve(),
        manifest_dir.resolve(),
    }


def test_nested_roots_collapse_to_outermost(tmp_path):
    """A monorepo's nested manifests must not re-walk the same tree N times."""
    mono = tmp_path / "mono"
    mono.mkdir()
    (mono / "pyproject.toml").write_text("[project]\nname='x'\n", encoding="utf-8")
    sub = mono / "packages" / "sub"
    sub.mkdir(parents=True)
    (sub / "package.json").write_text("{}", encoding="utf-8")

    roots = collect_static_roots(
        [mono / "pyproject.toml", sub / "package.json"],
        [],
        [],
    )

    assert roots == [mono.resolve()]


def test_same_dir_from_multiple_signals_dedupes(tmp_path):
    proj = tmp_path / "proj"
    proj.mkdir()
    (proj / "go.mod").write_text("module x\n", encoding="utf-8")

    roots = collect_static_roots([proj / "go.mod"], [proj], [proj])

    assert roots == [proj.resolve()]


# --------------------------------------------------------------------------- #
# discover_agents (static channel)
# --------------------------------------------------------------------------- #


def test_detects_manifest_only_project_with_no_mcp_config():
    """End-to-end seam check: a manifest-only sample (no MCP config, no skill)
    is detected. Regression for the flagged MCP-config scoping limitation."""
    sample = SAMPLES / "sample_01"  # LangChain: pyproject.toml + agent.py only
    result = discover_agents(
        found_paths=[sample / "pyproject.toml"],
        mcp_project_paths=[],
        skill_paths=[],
        detect_install=False,
    )

    agents = [a for a in result.agents if a.is_agent]
    assert len(agents) == 1
    agent = agents[0]
    assert agent.framework_id == "langchain"
    assert agent.language == "Python"
    assert agent.detection_method == "static"
    assert Path(agent.location).resolve() == sample.resolve()


def test_detects_skill_only_project_root():
    """A project surfaced only by a skill dir (no MCP config, no manifest in the
    crawl hits) is still walked for agents."""
    sample = SAMPLES / "sample_01"
    result = discover_agents(
        found_paths=[],
        mcp_project_paths=[],
        skill_paths=[sample],
        detect_install=False,
    )

    agents = [a for a in result.agents if a.is_agent]
    assert len(agents) == 1
    assert agents[0].framework_id == "langchain"


def test_excludes_agent_unit_nested_inside_reported_skill(tmp_path):
    skill = tmp_path / ".agents" / "skills" / "runlayer-qa"
    scripts = skill / "scripts"
    scripts.mkdir(parents=True)
    (skill / "SKILL.md").write_text("# Runlayer QA", encoding="utf-8")
    manifest = scripts / "package.json"
    manifest.write_text(
        '{"dependencies":{"@modelcontextprotocol/sdk":"^1.0.0"}}',
        encoding="utf-8",
    )
    (scripts / "server.ts").write_text(
        'import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";',
        encoding="utf-8",
    )

    result = discover_agents(
        found_paths=[manifest],
        mcp_project_paths=[],
        skill_paths=[skill],
        detect_install=False,
    )

    assert result.agents == []


def test_static_disabled_yields_no_static_agents(tmp_path):
    proj = tmp_path / "proj"
    proj.mkdir()
    (proj / "pyproject.toml").write_text(
        "[project]\nname='x'\ndependencies=['langchain>=0.3']\n", encoding="utf-8"
    )
    (proj / "agent.py").write_text(
        "from langchain.agents import AgentExecutor\n", encoding="utf-8"
    )

    result = discover_agents(
        found_paths=[proj / "pyproject.toml"],
        mcp_project_paths=[],
        skill_paths=[],
        detect_static=False,
        detect_install=False,
    )

    assert result.agents == []
