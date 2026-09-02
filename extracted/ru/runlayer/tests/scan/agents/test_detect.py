"""Detector tests: scoring, evidence, language gate, unknowns, and fingerprint."""

from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

from runlayer_cli.scan.agents import detect as detect_module
from runlayer_cli.scan.agents.detect import (
    METHOD_INSTALL,
    METHOD_STATIC,
    UNKNOWN_LANGUAGE,
    DiscoveredAgent,
    Detector,
    Evidence,
    _needle_pattern,
    build_install_agent,
    collect_agents,
    compute_fingerprint,
    load_detector,
)
from runlayer_cli.scan.agents.discover import discover


def _detect_single(tmp_path, files: dict[str, str], detector: Detector):
    proj = tmp_path / "proj"
    proj.mkdir(parents=True, exist_ok=True)
    for name, content in files.items():
        path = proj / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    units = discover(proj)
    assert len(units) == 1
    return detector.detect(units[0])


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


def _write_typescript_mcp_project(root: Path) -> None:
    root.mkdir(parents=True)
    (root / "package.json").write_text(
        '{"dependencies":{"@modelcontextprotocol/sdk":"^1.0.0"}}',
        encoding="utf-8",
    )


def test_detects_langchain_with_evidence(tmp_path):
    detector = load_detector()
    result = _detect_single(
        tmp_path,
        {"pyproject.toml": LANGCHAIN_PYPROJECT, "agent.py": LANGCHAIN_SOURCE},
        detector,
    )

    assert result.is_agent
    assert result.framework_id == "langchain"
    assert result.display_name == "LangChain"
    assert result.language == "Python"
    assert result.detection_method == METHOD_STATIC
    assert result.confidence > 0.5
    assert result.margin > 0.5

    kinds = {e.kind for e in result.evidence}
    assert "package_dep" in kinds
    assert "import" in kinds
    assert "symbol" in kinds
    # Evidence carries the source file it was matched in.
    assert all(e.source for e in result.evidence)


def test_detect_only_scores_candidate_frameworks(tmp_path):
    """F3: a Python unit is scored against Python-family frameworks only, not the
    whole registry (no JS/Go/etc frameworks in the score list)."""
    detector = load_detector()
    result = _detect_single(
        tmp_path,
        {"pyproject.toml": LANGCHAIN_PYPROJECT, "agent.py": LANGCHAIN_SOURCE},
        detector,
    )

    assert result.framework_id == "langchain"
    scored_languages = {s.language for s in result.scores}
    assert scored_languages == {"Python"}
    # Pre-filter actually narrowed the set (the registry spans many languages).
    assert 0 < len(result.scores) < len(detector.frameworks)


def test_no_signal_dir_is_unknown(tmp_path):
    detector = load_detector()
    result = _detect_single(
        tmp_path,
        {
            "requirements.txt": "flask\nrequests\n",
            "app.py": "import flask\napp = flask.Flask(__name__)\n",
        },
        detector,
    )
    assert not result.is_agent
    assert result.framework_id is None
    assert result.confidence == 0.0
    assert result.agent_fingerprint is None


def test_single_weak_symbol_is_unknown(tmp_path):
    detector = load_detector()
    result = _detect_single(
        tmp_path,
        {
            "pyproject.toml": "[project]\nname='debug-adapter'\n",
            "adapter.py": "client.connect(address)\n",
        },
        detector,
    )

    assert not result.is_agent
    assert result.framework_id is None
    assert result.confidence == 0.0


def test_typescript_mcp_server_is_labeled_as_mcp_server(tmp_path):
    detector = load_detector()
    result = _detect_single(
        tmp_path,
        {
            "package.json": (
                '{"dependencies":{"@modelcontextprotocol/sdk":"^1.0.0","zod":"^3"}}'
            ),
            "server.ts": (
                'import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";\n'
                "const server = new McpServer({ name: 'example', version: '1' });\n"
                "server.registerTool('example', { inputSchema: {} }, () => ({}));\n"
            ),
        },
        detector,
    )

    assert result.is_agent
    assert result.framework_id == "mcp-server-typescript"
    assert result.display_name == "MCP Server"
    assert result.language == "TypeScript"


def test_single_evidence_confidence_is_capped(tmp_path):
    detector = load_detector()
    result = _detect_single(
        tmp_path,
        {
            "package.json": ('{"dependencies":{"@modelcontextprotocol/sdk":"^1.0.0"}}'),
        },
        detector,
    )

    assert result.framework_id == "mcp-server-typescript"
    assert len(result.evidence) == 1
    assert result.confidence == 0.75


def test_python_mcp_server_is_labeled_as_mcp_server(tmp_path):
    detector = load_detector()
    result = _detect_single(
        tmp_path,
        {
            "pyproject.toml": (
                "[project]\nname='example-mcp'\ndependencies=['mcp>=1.0']\n"
            ),
            "server.py": (
                "from mcp.server.fastmcp import FastMCP\n"
                "server = FastMCP('example')\n"
                "@server.tool()\n"
                "def example() -> str:\n"
                "    return 'ok'\n"
            ),
        },
        detector,
    )

    assert result.is_agent
    assert result.framework_id == "mcp-server-python"
    assert result.display_name == "MCP Server"
    assert result.language == "Python"


def test_low_level_python_mcp_server_without_manifest_is_detected(tmp_path):
    detector = load_detector()
    result = _detect_single(
        tmp_path,
        {
            "server.py": (
                "from mcp.server import Server\n"
                "server = Server('example')\n"
                "@server.list_tools()\n"
                "async def list_tools():\n"
                "    return []\n"
                "@server.call_tool()\n"
                "async def call_tool(name, arguments):\n"
                "    return []\n"
            )
        },
        detector,
    )

    assert result.is_agent
    assert result.framework_id == "mcp-server-python"
    assert result.display_name == "MCP Server"
    assert result.language == "Python"
    assert result.manifests == []


def test_java_mcp_server_is_labeled_as_mcp_server(tmp_path):
    detector = load_detector()
    result = _detect_single(
        tmp_path,
        {
            "pom.xml": (
                "<project><dependencies><dependency>"
                "<groupId>io.modelcontextprotocol.sdk</groupId>"
                "<artifactId>mcp</artifactId>"
                "</dependency></dependencies></project>"
            ),
            "Server.java": (
                "import io.modelcontextprotocol.server.McpServer;\n"
                "McpSyncServer server = McpServer.sync(transportProvider).build();\n"
            ),
        },
        detector,
    )

    assert result.is_agent
    assert result.framework_id == "mcp-server-java"
    assert result.display_name == "MCP Server"
    assert result.language == "Java"


def test_official_go_mcp_server_is_labeled_as_mcp_server(tmp_path):
    detector = load_detector()
    result = _detect_single(
        tmp_path,
        {
            "go.mod": (
                "module example.com/mcp-server\n\n"
                "require github.com/modelcontextprotocol/go-sdk v1.7.0\n"
            ),
            "main.go": (
                'import "github.com/modelcontextprotocol/go-sdk/mcp"\n'
                'server := mcp.NewServer(&mcp.Implementation{Name: "example"}, nil)\n'
                "mcp.AddTool(server, tool, handler)\n"
            ),
        },
        detector,
    )

    assert result.is_agent
    assert result.framework_id == "mcp-server-go"
    assert result.display_name == "MCP Server"
    assert result.language == "Go"


def test_mark3labs_go_mcp_server_is_labeled_as_mcp_server(tmp_path):
    detector = load_detector()
    result = _detect_single(
        tmp_path,
        {
            "go.mod": (
                "module example.com/mcp-server\n\n"
                "require github.com/mark3labs/mcp-go v0.42.0\n"
            ),
            "main.go": (
                'import "github.com/mark3labs/mcp-go/server"\n'
                'mcpServer := server.NewMCPServer("example", "1.0.0")\n'
                "server.ServeStdio(mcpServer)\n"
            ),
        },
        detector,
    )

    assert result.is_agent
    assert result.framework_id == "mcp-server-go"
    assert result.display_name == "MCP Server"
    assert result.language == "Go"


def test_csharp_mcp_server_is_labeled_as_mcp_server(tmp_path):
    detector = load_detector()
    result = _detect_single(
        tmp_path,
        {
            "Example.csproj": (
                '<Project Sdk="Microsoft.NET.Sdk">'
                "<ItemGroup>"
                '<PackageReference Include="ModelContextProtocol" Version="2.0.0" />'
                "</ItemGroup>"
                "</Project>"
            ),
            "Program.cs": (
                "using ModelContextProtocol.Server;\n"
                "builder.Services.AddMcpServer().WithStdioServerTransport();\n"
                "[McpServerToolType]\n"
                "public static class ExampleTools {}\n"
            ),
        },
        detector,
    )

    assert result.is_agent
    assert result.framework_id == "mcp-server-csharp"
    assert result.display_name == "MCP Server"
    assert result.language == "C#"


def test_language_gate_penalizes_wrong_family(tmp_path):
    """A Python framework's symbols sitting in a JS unit must not win.

    The unit is clearly TypeScript (package.json + agent.ts); even if some
    Python-ish symbol substring appears, the soft language gate keeps the
    incompatible Python framework from outscoring the JS framework.
    """
    detector = load_detector()
    result = _detect_single(
        tmp_path,
        {
            "package.json": '{"dependencies": {"ai": "^5", "@ai-sdk/openai": "^2"}}',
            "agent.ts": (
                'import { generateText, tool } from "ai";\n'
                'import { openai } from "@ai-sdk/openai";\n'
                "await generateText({ model: openai('gpt-4o') });\n"
            ),
        },
        detector,
    )
    assert result.is_agent
    assert result.language == "TypeScript"
    assert result.framework_id == "vercel-ai-sdk"


def test_fingerprint_is_stable_and_order_independent():
    a = compute_fingerprint("langchain", "Python", ["langchain", "langchain-openai"])
    b = compute_fingerprint("langchain", "Python", ["langchain-openai", "langchain"])
    assert a == b  # marker order does not matter
    assert len(a) == 64  # sha256 hex


def test_fingerprint_differs_by_framework():
    a = compute_fingerprint("langchain", "Python", ["x"])
    b = compute_fingerprint("langgraph", "Python", ["x"])
    assert a != b


def test_fingerprint_excludes_ephemeral_path(tmp_path):
    """Same project deps at two different paths -> identical fingerprint."""
    detector = load_detector()
    one = _detect_single(
        tmp_path / "one",
        {"pyproject.toml": LANGCHAIN_PYPROJECT, "agent.py": LANGCHAIN_SOURCE},
        detector,
    )
    two = _detect_single(
        tmp_path / "two",
        {"pyproject.toml": LANGCHAIN_PYPROJECT, "agent.py": LANGCHAIN_SOURCE},
        detector,
    )
    assert one.location != two.location  # different absolute paths
    assert one.agent_fingerprint == two.agent_fingerprint


def test_collect_agents_disambiguates_identical_dep_siblings(tmp_path):
    repo = tmp_path / "mcps-by-runlayer"
    _write_typescript_mcp_project(repo / "packages" / "gmail")
    _write_typescript_mcp_project(repo / "packages" / "google-calendar")

    results = collect_agents([repo])

    assert len(results) == 2
    assert len({result.agent_fingerprint for result in results}) == 2


def test_collect_agents_keeps_noncolliding_fingerprint_stable(tmp_path):
    repo = tmp_path / "repo"
    package = repo / "packages" / "gmail"
    _write_typescript_mcp_project(package)
    detector = load_detector()
    unit = discover(package)[0]
    baseline = detector.detect(unit).agent_fingerprint

    results = collect_agents([repo], detector=detector)

    assert len(results) == 1
    assert results[0].agent_fingerprint == baseline


def test_collect_agents_uses_relative_path_for_same_basename_collisions(tmp_path):
    fingerprints_by_repo: list[dict[str, str | None]] = []
    for checkout in ("checkout-one", "checkout-two"):
        repo = tmp_path / checkout
        for provider in ("google", "microsoft"):
            _write_typescript_mcp_project(
                repo / "connectors" / provider / "shared-name"
            )

        results = collect_agents([repo])
        fingerprints_by_repo.append(
            {
                Path(result.location).relative_to(repo).as_posix(): (
                    result.agent_fingerprint
                )
                for result in results
            }
        )

    assert len(set(fingerprints_by_repo[0].values())) == 2
    assert fingerprints_by_repo[0] == fingerprints_by_repo[1]


def test_needle_pattern_word_boundary_anchored():
    """F7: identifier needles only match on identifier boundaries; punctuation
    edges still match verbatim."""
    tool = _needle_pattern("tool")
    assert tool.search("from x import tool")
    assert tool.search("tool(x)")
    assert not tool.search("tools")  # not a prefix of a larger identifier
    assert not tool.search("mytool")  # not a suffix either
    assert not tool.search("toolbox")

    # Punctuation-edged needles keep matching as-is.
    assert _needle_pattern("openai(").search("m = openai(model)")
    assert _needle_pattern("@ai-sdk/openai").search('import "@ai-sdk/openai"')
    assert _needle_pattern("langchain.agents").search("from langchain.agents import X")


def test_symbol_substring_in_larger_identifier_does_not_score(tmp_path):
    """F7 end-to-end: a langchain symbol buried inside an unrelated identifier
    must not produce symbol evidence."""
    detector = load_detector()
    # 'AgentExecutor' appears only as a substring of 'MyAgentExecutorWrapper'.
    result = _detect_single(
        tmp_path,
        {
            "pyproject.toml": "[project]\nname='x'\n",
            "agent.py": "class MyAgentExecutorWrapperThing:\n    pass\n",
        },
        detector,
    )
    symbol_evidence = [e for e in result.evidence if e.kind == "symbol"]
    assert symbol_evidence == []


def test_collect_agents_deadline_stops_scoring_between_units(monkeypatch, tmp_path):
    """Once the deadline passes, remaining discovered units are not scored."""
    units = [SimpleNamespace(root=tmp_path / f"unit-{index}") for index in range(10)]
    monkeypatch.setattr(
        detect_module,
        "discover",
        lambda *_args, **_kwargs: units,
    )

    scored: list = []
    clock = {"now": 0.0}

    class CountingDetector:
        def detect(self, unit):
            scored.append(unit.root)
            # Trip the deadline after the third unit is scored; the loop's
            # per-unit check should then stop scoring the rest.
            if len(scored) >= 3:
                clock["now"] = 100.0
            return SimpleNamespace(location=str(unit.root), is_agent=False)

    monkeypatch.setattr(
        detect_module,
        "time",
        SimpleNamespace(monotonic=lambda: clock["now"]),
    )

    results = collect_agents(
        [tmp_path],
        detector=CountingDetector(),
        include_unknown=True,
        deadline=1.0,
    )

    assert len(scored) == 3
    assert len(results) == 3


def test_collect_agents_dedupes_by_location_in_discovery_order(monkeypatch, tmp_path):
    """Duplicate locations keep the first sighting in discovery order."""
    duplicate = tmp_path / "duplicate"
    units = [
        SimpleNamespace(root=tmp_path / "first", location=duplicate, marker="first"),
        SimpleNamespace(
            root=tmp_path / "alpha", location=tmp_path / "alpha", marker="alpha"
        ),
        SimpleNamespace(root=tmp_path / "second", location=duplicate, marker="second"),
    ]
    monkeypatch.setattr(
        detect_module,
        "discover",
        lambda *_args, **_kwargs: units,
    )

    class PassthroughDetector:
        def detect(self, unit):
            return SimpleNamespace(
                location=str(unit.location),
                is_agent=False,
                marker=unit.marker,
            )

    results = collect_agents(
        [tmp_path],
        detector=PassthroughDetector(),
        include_unknown=True,
    )

    # Results are sorted by location; the duplicate keeps the first sighting.
    assert [result.location for result in results] == [
        str(tmp_path / "alpha"),
        str(duplicate),
    ]
    by_location = {result.location: result for result in results}
    assert by_location[str(duplicate)].marker == "first"


def test_build_install_agent_shape():
    agent = build_install_agent(
        framework_id="openclaw",
        display_name="OpenClaw",
        location="/Users/dev/.openclaw",
        evidence=[Evidence("install_artifact", "/usr/local/bin/openclaw", "cli")],
        markers=["cli", "state"],
    )
    assert agent.is_agent
    assert agent.detection_method == METHOD_INSTALL
    assert agent.confidence == 1.0
    assert agent.margin == 1.0
    assert agent.framework_id == "openclaw"
    assert agent.agent_fingerprint and len(agent.agent_fingerprint) == 64
    assert agent.to_dict()["detection_method"] == "install"


class TestDiscoveredAgentApiPayload:
    """The redacted per-agent wire payload for POST /ai-watch/agents."""

    def _agent(self, **overrides) -> DiscoveredAgent:
        base = dict(
            location="/Users/alice/proj",
            name="proj",
            framework_id="langchain",
            display_name="LangChain",
            language="Python",
            confidence=0.9123,
            margin=0.5,
            score=3.0,
            runner_up=None,
            runner_up_score=0.0,
            detection_method=METHOD_STATIC,
            evidence=[Evidence("package_dep", "langchain", "pyproject.toml")],
            manifests=["pyproject.toml"],
            languages=["Python"],
            agent_fingerprint="f" * 64,
            scores=[],
        )
        base.update(overrides)
        return DiscoveredAgent(**base)

    def test_emits_only_redacted_fields(self):
        payload = self._agent().to_api_payload()
        assert set(payload) == {
            "agent_fingerprint",
            "framework_id",
            "language",
            "root_path",
            "confidence",
            "manifest_files",
            "evidence",
        }
        # Never raw score internals / language list / file contents.
        assert "scores" not in payload
        assert "languages" not in payload

    def test_root_path_home_username_redacted(self):
        payload = self._agent(location="/Users/alice/proj").to_api_payload()
        assert payload["root_path"] == "/Users/<redacted>/proj"

    def test_evidence_source_basename_and_value_passthrough(self):
        agent = self._agent(
            evidence=[
                Evidence("import", "from langchain", "/Users/alice/proj/agent.py"),
            ]
        )
        ev = agent.to_api_payload()["evidence"][0]
        assert ev["source"] == "agent.py"  # full path reduced to basename
        assert ev["value"] == "from langchain"  # safe token unchanged
        assert ev["kind"] == "import"

    def test_install_evidence_value_path_redacted(self):
        agent = self._agent(
            evidence=[
                Evidence("install_artifact", "/Users/alice/.openclaw", "state"),
            ]
        )
        ev = agent.to_api_payload()["evidence"][0]
        assert ev["value"] == "/Users/<redacted>/.openclaw"
        assert ev["source"] == "state"

    def test_confidence_rounded(self):
        assert self._agent(confidence=0.9123).to_api_payload()["confidence"] == 0.912

    def test_manifest_files_passthrough(self):
        payload = self._agent(
            manifests=["pyproject.toml", "package.json"]
        ).to_api_payload()
        assert payload["manifest_files"] == ["pyproject.toml", "package.json"]

    def test_missing_language_coerced_to_sentinel(self):
        # Install-channel agents (e.g. OpenClaw) carry no language; the backend
        # requires a non-null value, so the wire payload substitutes the sentinel.
        payload = self._agent(language=None).to_api_payload()
        assert payload["language"] == UNKNOWN_LANGUAGE

    def test_known_username_redacted_in_root_path(self):
        # A non-home layout the home-segment fallback would miss; threading the
        # known username scrubs it anyway.
        agent = self._agent(location="/opt/work/alice/proj")
        payload = agent.to_api_payload(usernames=["alice"])
        assert payload["root_path"] == "/opt/work/<redacted>/proj"

    def test_known_username_redacted_in_evidence_value(self):
        agent = self._agent(
            location="/opt/work/alice/proj",
            evidence=[Evidence("install_artifact", "/opt/work/alice/.state", "state")],
        )
        ev = agent.to_api_payload(usernames=["alice"])["evidence"][0]
        assert ev["value"] == "/opt/work/<redacted>/.state"

    def test_no_usernames_leaves_non_home_path_intact(self):
        # Default (no usernames) still scrubs the home layout but not arbitrary
        # ones -- documents why the caller threads the device username.
        agent = self._agent(location="/opt/work/alice/proj")
        assert agent.to_api_payload()["root_path"] == "/opt/work/alice/proj"
