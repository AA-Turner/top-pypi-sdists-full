"""Scoring / classification tests, including the false-positive corpus.

The core risk of a process channel is noise: every dev box runs dev servers,
browsers, and databases that listen on ports. These tests pin the RFC principle
that a bare listener (and bare client-parenthood) is too weak to surface on its
own, while an exact config correlation / client executable / unambiguous MCP or
agent marker is strong enough -- and that correlations carry the config_hash.
"""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from unittest import mock

import pytest

from runlayer_cli.scan.clients import (
    SettingsOverrideFlag,
    get_all_clients,
    get_client_by_name,
)
from runlayer_cli.scan.processes import classify as classify_module
from runlayer_cli.scan.processes.classify import (
    ClassifierContext,
    ResolvedAgentRuntimeSignature,
    W_CLIENT_SIGNATURE,
    build_context,
    classify_processes,
    classify_processes_with_overrides,
)
from runlayer_cli.scan.processes.models import ProcessCandidate

_CURSOR_SIG = "cursor.app/contents/macos/cursor"
_CURSOR_EXE = "/Applications/Cursor.app/Contents/MacOS/Cursor"


# ---------------------------------------------------------------------------
# build_context (duck-typed against the config-scan + client-registry shapes)
# ---------------------------------------------------------------------------
@dataclass
class _FakeServer:
    config_hash: str = ""
    url: str | None = None
    command: str | None = None
    args: list[str] | None = None
    type: str = "stdio"


@dataclass
class _FakeConfig:
    servers: list[_FakeServer] = field(default_factory=list)
    wsl_distro: str | None = None


@dataclass
class _FakeClient:
    name: str
    process_signatures: list[str] | None = None
    settings_override_flags: list[SettingsOverrideFlag] | None = None


@dataclass
class _FakeAgent:
    framework_id: str
    agent_fingerprint: str
    location: str


class TestBuildContext:
    def test_http_url_indexes_port(self):
        configs = [
            _FakeConfig(
                servers=[
                    _FakeServer(
                        config_hash="h1",
                        url="http://127.0.0.1:3000/mcp",
                        type="http",
                    )
                ]
            )
        ]
        ctx = build_context(configs, [])
        assert ctx.configured_ports[(None, 3000)] == ("h1", "http")

    def test_sse_url_transport(self):
        configs = [
            _FakeConfig(
                servers=[
                    _FakeServer(
                        config_hash="h2", url="http://127.0.0.1:9000", type="sse"
                    )
                ]
            )
        ]
        ctx = build_context(configs, [])
        assert ctx.configured_ports[(None, 9000)] == ("h2", "sse")

    def test_stdio_command_indexes_key(self):
        configs = [
            _FakeConfig(
                servers=[
                    _FakeServer(
                        config_hash="h3",
                        command="npx",
                        args=["-y", "@modelcontextprotocol/server-git"],
                    )
                ]
            )
        ]
        ctx = build_context(configs, [])
        key = (None, "npx", ("-y", "@modelcontextprotocol/server-git"))
        assert ctx.configured_commands[key] == "h3"

    def test_client_signatures_lowercased(self):
        ctx = build_context(
            [], [_FakeClient(name="cursor", process_signatures=["Cursor.App/X"])]
        )
        assert ctx.client_signatures["cursor"] == ("cursor.app/x",)

    def test_settings_override_flags_are_indexed_by_client(self):
        spec = SettingsOverrideFlag("--mcp-config", mcp_config="file")
        ctx = build_context(
            [],
            [
                _FakeClient(
                    name="claude_code",
                    settings_override_flags=[spec],
                )
            ],
        )

        assert ctx.client_override_flags["claude_code"] == (spec,)

    def test_npm_package_signatures_are_scoped_to_argv_paths(self):
        codex = get_client_by_name("codex")
        assert codex is not None

        ctx = build_context([], [codex], detect_agents=False)

        # node_modules markers live only in the scoped npm-package channel;
        # process_signatures carries just non-npm install paths.
        assert all(
            "node_modules" not in signature
            for signature in ctx.client_signatures.get("codex", ())
        )
        assert ctx.client_package_signatures["codex"] == ("@openai/codex",)

    def test_agent_installations_indexed_by_framework(self):
        ctx = build_context(
            [],
            [],
            [_FakeAgent("openclaw", "fp-openclaw", "/Users/dev/.openclaw")],
        )

        assert ctx.agent_installations["openclaw"][0].fingerprint == "fp-openclaw"

    @mock.patch("runlayer_cli.scan.processes.classify.runtime_signatures")
    def test_agent_opt_out_does_not_resolve_runtime_signatures(
        self,
        mock_signatures,
    ):
        context = build_context([], [], detect_agents=False)

        mock_signatures.assert_not_called()
        assert context.agent_runtime_signatures == ()


# ---------------------------------------------------------------------------
# False-positive corpus -- everyday listeners must be dropped
# ---------------------------------------------------------------------------
class TestFalsePositiveCorpus:
    def _ctx(self) -> ClassifierContext:
        return ClassifierContext(client_signatures={"cursor": (_CURSOR_SIG,)})

    def test_postgres_loopback_dropped(self):
        cand = ProcessCandidate(
            pid=100,
            exe="/usr/local/bin/postgres",
            argv=["postgres", "-D", "/data"],
            listening_ports=[5432],
            bind_scope="loopback",
        )
        assert classify_processes([cand], self._ctx()) == []

    def test_dev_server_all_interfaces_dropped(self):
        cand = ProcessCandidate(
            pid=101,
            exe="/usr/local/bin/node",
            argv=["node", "vite", "--host"],
            listening_ports=[5173],
            bind_scope="all_interfaces",
        )
        assert classify_processes([cand], self._ctx()) == []

    def test_redis_loopback_dropped(self):
        cand = ProcessCandidate(
            pid=102,
            exe="/usr/local/bin/redis-server",
            argv=["redis-server", "*:6379"],
            listening_ports=[6379],
            bind_scope="loopback",
        )
        assert classify_processes([cand], self._ctx()) == []

    def test_browser_helper_dropped(self):
        cand = ProcessCandidate(
            pid=103,
            exe="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome Helper",
            argv=["Google Chrome Helper", "--type=renderer"],
        )
        assert classify_processes([cand], self._ctx()) == []

    def test_script_path_client_signature_lookalikes_are_dropped(self):
        context = build_context([], get_all_clients(), detect_agents=False)
        candidates = [
            ProcessCandidate(
                pid=104,
                exe="/usr/bin/node",
                argv=["node", "/src/awesome-claude-code/lint.js"],
            ),
            ProcessCandidate(
                pid=105,
                exe="/usr/bin/node",
                argv=["node", "/tmp/claude-code.js"],
            ),
            ProcessCandidate(
                pid=106,
                exe="/usr/bin/python3",
                argv=["python3", "~/claude-code-notes.py"],
            ),
            ProcessCandidate(
                pid=107,
                exe=r"C:\Program Files\nodejs\node.exe",
                argv=["node.exe", r"C:\tmp\cursor.exe-tools.js"],
            ),
            ProcessCandidate(
                pid=108,
                exe=r"C:\Program Files\Python\python.exe",
                argv=["python.exe", r"C:\tmp\windsurf.exe-notes.py"],
            ),
        ]

        assert classify_processes(candidates, context) == []

    @pytest.mark.parametrize(
        "argument",
        [
            "--package=@openai/codex",
            "/hidden/node_modules/@openai/codex-malicious/bin/codex.js",
            "https://host/node_modules/@openai/codex/readme",
        ],
    )
    def test_package_name_without_exact_node_modules_path_is_dropped(self, argument):
        codex = get_client_by_name("codex")
        assert codex is not None
        context = build_context([], [codex], detect_agents=False)
        candidate = ProcessCandidate(
            pid=104,
            exe="/usr/local/bin/node",
            argv=["node", "script.js", argument],
        )

        assert classify_processes([candidate], context) == []

    def test_non_runtime_process_opening_package_file_is_dropped(self):
        codex = get_client_by_name("codex")
        assert codex is not None
        context = build_context([], [codex], detect_agents=False)
        candidate = ProcessCandidate(
            pid=105,
            exe="/bin/cat",
            argv=[
                "cat",
                "/tmp/node_modules/@openai/codex/README.md",
            ],
        )

        assert classify_processes([candidate], context) == []

    @pytest.mark.parametrize(
        "exe",
        [
            "/tmp/aider",
            "/usr/local/bin/codex",
            "/usr/local/bin/copilot",
            "/usr/local/bin/gemini",
            "/usr/local/bin/opencode",
            "/tmp/trae",
            "/usr/local/bin/zed",
        ],
    )
    def test_bare_client_name_lookalike_is_dropped(self, exe: str):
        context = build_context([], get_all_clients(), detect_agents=False)
        candidate = ProcessCandidate(pid=104, exe=exe, argv=[exe])

        assert classify_processes([candidate], context) == []

    def test_opencode_prefix_lookalike_is_dropped(self):
        context = build_context([], get_all_clients(), detect_agents=False)
        executable = "/srv/node_modules/opencode-helper/bin/opencode"
        candidate = ProcessCandidate(pid=106, exe=executable, argv=[executable])

        assert classify_processes([candidate], context) == []


# ---------------------------------------------------------------------------
# True positives -- strong signals stand alone
# ---------------------------------------------------------------------------
class TestStrongSignals:
    @pytest.mark.parametrize(
        "argv",
        [
            ["npx", "--yes", "mcp-server-filesystem", "--help"],
            ["npx", "--", "mcp-server-filesystem"],
            ["npx", "--package", "mcp-server-filesystem", "filesystem", "--help"],
            ["uvx", "mcp-server-fetch", "--help"],
            ["uvx", "--from", "mcp-server-fetch", "fetch", "--help"],
            ["pnpm", "dlx", "mcp-inspector", "--help"],
            ["bunx", "mcp-inspector", "--help"],
        ],
    )
    def test_transient_mcp_launcher_crosses_threshold(self, argv: list[str]):
        candidate = ProcessCandidate(
            pid=198, exe=f"/usr/local/bin/{argv[0]}", argv=argv
        )

        [sighting] = classify_processes([candidate], ClassifierContext())

        assert sighting.kind == "mcp_server"
        assert "transient_mcp_launcher" in sighting.ai_signals
        assert sighting.confidence >= 0.5

    def test_uvx_equals_value_option_preserves_transient_launcher_detection(self):
        candidate = ProcessCandidate(
            pid=199,
            exe="/usr/local/bin/uvx",
            argv=["uvx", "--python=3.12", "mcp-server-fetch", "--help"],
        )

        [sighting] = classify_processes([candidate], ClassifierContext())

        assert sighting.kind == "mcp_server"
        assert "transient_mcp_launcher" in sighting.ai_signals

    @pytest.mark.parametrize(
        ("exe", "argv"),
        [
            (
                "/usr/local/bin/node",
                [
                    "node",
                    "/usr/local/lib/node_modules/npm/bin/npx-cli.js",
                    "mcp-inspector",
                ],
            ),
            (
                "/usr/local/bin/node",
                [
                    "node",
                    "/usr/local/lib/node_modules/pnpm/bin/pnpm.cjs",
                    "dlx",
                    "mcp-server-fetch",
                ],
            ),
            ("/usr/local/bin/bun", ["bun", "x", "mcp-inspector"]),
            ("/usr/local/bin/bun", ["bunx", "mcp-inspector"]),
        ],
    )
    def test_runtime_backed_transient_launcher_crosses_threshold(
        self,
        exe: str,
        argv: list[str],
    ):
        candidate = ProcessCandidate(pid=198, exe=exe, argv=argv)

        [sighting] = classify_processes([candidate], ClassifierContext())

        assert "transient_mcp_launcher" in sighting.ai_signals

    @pytest.mark.parametrize(
        "argv",
        [
            ["npx", "vite"],
            ["uvx", "ruff"],
            ["pnpm", "dlx", "eslint"],
            ["bunx", "prettier"],
            ["npx", "eslint", "/tmp/mcp-server-notes.js"],
        ],
    )
    def test_transient_non_mcp_launcher_is_dropped(self, argv: list[str]):
        candidate = ProcessCandidate(
            pid=199, exe=f"/usr/local/bin/{argv[0]}", argv=argv
        )

        assert classify_processes([candidate], ClassifierContext()) == []

    @pytest.mark.parametrize(
        ("client", "exe", "argv"),
        [
            (
                "aider",
                "/Users/alex/.local/share/uv/python/cpython-3.12/bin/python3.12",
                ["/Users/alex/.local/share/uv/tools/aider-chat/bin/aider"],
            ),
            (
                "claude_code",
                "/opt/homebrew/bin/node",
                [
                    "node",
                    ("/opt/homebrew/lib/node_modules/@anthropic-ai/claude-code/cli.js"),
                ],
            ),
            (
                "codex",
                "/opt/homebrew/bin/node",
                [
                    "node",
                    "/opt/homebrew/lib/node_modules/@openai/codex/bin/codex.js",
                ],
            ),
            (
                "codex",
                "/Users/alex/.codex/packages/standalone/current/codex",
                ["/Users/alex/.local/bin/codex"],
            ),
            (
                "cursor",
                r"C:\Users\alice\AppData\Local\Programs\cursor\Cursor.exe",
                [r"C:\Users\alice\AppData\Local\Programs\cursor\Cursor.exe"],
            ),
            (
                "github_copilot_cli",
                "/usr/local/bin/node",
                [
                    "node",
                    "/usr/local/lib/node_modules/@github/copilot/index.js",
                ],
            ),
            (
                "github_copilot_cli",
                "/Users/alex/.local/bin/copilot",
                ["/Users/alex/.local/bin/copilot"],
            ),
            (
                "gemini_cli",
                "/usr/local/bin/node",
                [
                    "node",
                    "/usr/local/lib/node_modules/@google/gemini-cli/dist/index.js",
                ],
            ),
            (
                "opencode",
                "/Users/alex/.opencode/bin/opencode",
                ["/Users/alex/.opencode/bin/opencode"],
            ),
            (
                "opencode",
                "/opt/homebrew/Cellar/opencode/1.17.8/bin/opencode",
                ["/opt/homebrew/bin/opencode"],
            ),
            (
                "trae",
                "/Applications/Trae.app/Contents/MacOS/Electron",
                ["/Applications/Trae.app/Contents/MacOS/Electron"],
            ),
            (
                "windsurf",
                r"C:\Users\alice\AppData\Local\Programs\Windsurf\Windsurf.exe",
                [r"C:\Users\alice\AppData\Local\Programs\Windsurf\Windsurf.exe"],
            ),
            (
                "zed",
                "/Users/alex/.local/zed.app/bin/zed",
                ["/Users/alex/.local/zed.app/bin/zed"],
            ),
        ],
    )
    def test_package_specific_client_executable(
        self,
        client: str,
        exe: str,
        argv: list[str],
    ):
        context = build_context([], get_all_clients(), detect_agents=False)
        candidate = ProcessCandidate(pid=199, ppid=1, exe=exe, argv=argv)

        [sighting] = classify_processes([candidate], context)

        assert sighting.kind == "client"
        assert sighting.matched_client == client

    def test_official_mcp_marker(self):
        cand = ProcessCandidate(
            pid=200,
            exe="/usr/local/bin/npx",
            argv=["npx", "-y", "@modelcontextprotocol/server-filesystem", "/tmp"],
        )
        out = classify_processes([cand], ClassifierContext())
        assert len(out) == 1
        assert out[0].kind == "mcp_server"
        assert "mcp_official" in out[0].ai_signals
        assert out[0].confidence >= 0.5

    def test_wsl_attribution_reaches_wire_payload(self):
        cand = ProcessCandidate(
            pid=201,
            exe="/usr/local/bin/npx",
            argv=["npx", "-y", "@modelcontextprotocol/server-filesystem", "/tmp"],
            wsl_distro="Ubuntu",
        )

        out = classify_processes([cand], ClassifierContext())

        assert len(out) == 1
        assert out[0].wsl_distro == "Ubuntu"
        assert out[0].to_api_payload()["wsl_distro"] == "Ubuntu"

    def test_client_executable(self):
        cand = ProcessCandidate(
            pid=201, ppid=1, exe=_CURSOR_EXE, argv=[_CURSOR_EXE, "--enable-crashpad"]
        )
        ctx = ClassifierContext(client_signatures={"cursor": (_CURSOR_SIG,)})
        out = classify_processes([cand], ctx)
        assert len(out) == 1
        assert out[0].kind == "client"
        assert out[0].matched_client == "cursor"

    @pytest.mark.parametrize(
        ("client_name", "exe", "argv", "flag"),
        [
            (
                "cursor",
                _CURSOR_EXE,
                [_CURSOR_EXE, "--user-data-dir", "/tmp/cursor"],
                "--user-data-dir",
            ),
            (
                "vscode",
                "/Applications/Visual Studio Code.app/Contents/MacOS/Electron",
                [
                    "/Applications/Visual Studio Code.app/Contents/MacOS/Electron",
                    "--extensions-dir=/tmp/extensions",
                ],
                "--extensions-dir",
            ),
            (
                "windsurf",
                "/Applications/Windsurf.app/Contents/MacOS/Electron",
                [
                    "/Applications/Windsurf.app/Contents/MacOS/Electron",
                    "--user-data-dir",
                    "/tmp/windsurf",
                ],
                "--user-data-dir",
            ),
            (
                "claude_code",
                "/opt/homebrew/bin/node",
                [
                    "node",
                    "/opt/homebrew/lib/node_modules/@anthropic-ai/claude-code/cli.js",
                    "--settings",
                    "/tmp/settings.json",
                ],
                "--settings",
            ),
        ],
    )
    def test_client_override_flags_emit_signal_without_changing_score(
        self,
        client_name: str,
        exe: str,
        argv: list[str],
        flag: str,
    ):
        client = get_client_by_name(client_name)
        assert client is not None
        context = build_context([], [client], detect_agents=False)

        [sighting] = classify_processes(
            [ProcessCandidate(pid=211, exe=exe, argv=argv)],
            context,
        )

        assert f"settings_override:{flag}" in sighting.ai_signals
        assert sighting.confidence == W_CLIENT_SIGNATURE

    def test_override_path_is_sanitized_but_local_config_ref_is_raw(self):
        vscode = get_client_by_name("vscode")
        assert vscode is not None
        executable = "/Applications/Visual Studio Code.app/Contents/MacOS/Electron"
        candidate = ProcessCandidate(
            pid=212,
            exe=executable,
            argv=[
                executable,
                "--user-data-dir",
                "/Users/alice/custom-code",
            ],
            user="alice",
            cwd="/Users/alice/project",
        )

        result = classify_processes_with_overrides(
            [candidate],
            build_context([], [vscode], detect_agents=False),
            usernames=["alice"],
        )

        [sighting] = result.processes
        assert sighting.settings_overrides == [
            {
                "flag": "--user-data-dir",
                "value": "/Users/<redacted>/custom-code",
            }
        ]
        [ref] = result.override_config_refs
        assert ref.pid == 212
        assert ref.value == "/Users/alice/custom-code"
        assert ref.cwd == "/Users/alice/project"
        assert ref.user == "alice"
        assert ref.mcp_config == "user_data_dir"

    def test_wsl_override_config_ref_preserves_distro(self):
        claude = get_client_by_name("claude_code")
        assert claude is not None
        candidate = ProcessCandidate(
            pid=214,
            exe="/usr/bin/node",
            argv=[
                "node",
                "/usr/lib/node_modules/@anthropic-ai/claude-code/cli.js",
                "--mcp-config",
                "/home/alice/mcp.json",
            ],
            user="alice",
            wsl_distro="Ubuntu",
        )

        result = classify_processes_with_overrides(
            [candidate],
            build_context([], [claude], detect_agents=False),
        )

        [ref] = result.override_config_refs
        assert ref.wsl_distro == "Ubuntu"

    def test_inline_json_override_is_signal_only(self):
        claude = get_client_by_name("claude_code")
        assert claude is not None
        candidate = ProcessCandidate(
            pid=213,
            exe="/opt/homebrew/bin/node",
            argv=[
                "node",
                "/opt/homebrew/lib/node_modules/@anthropic-ai/claude-code/cli.js",
                "--mcp-config",
                '{"mcpServers":{"private":{"env":{"TOKEN":"secret"}}}}',
            ],
        )

        result = classify_processes_with_overrides(
            [candidate],
            build_context([], [claude], detect_agents=False),
        )

        assert result.processes[0].settings_overrides == [
            {"flag": "--mcp-config", "value": None}
        ]
        assert "settings_override:--mcp-config" in result.processes[0].ai_signals
        assert result.override_config_refs == []

    def test_renamed_node_launcher_matches_package_path_in_full_argv(self):
        codex = get_client_by_name("codex")
        assert codex is not None
        ctx = build_context([], [codex], detect_agents=False)
        cand = ProcessCandidate(
            pid=209,
            exe="/usr/local/bin/node",
            argv=[
                "renamed-launcher",
                "/hidden/lib/node_modules/@openai/codex/bin/codex.js",
            ],
        )

        out = classify_processes([cand], ctx)

        assert len(out) == 1
        assert out[0].kind == "client"
        assert out[0].matched_client == "codex"

    def test_windows_package_path_in_argv_identifies_renamed_launcher(self):
        codex = get_client_by_name("codex")
        assert codex is not None
        ctx = build_context([], [codex], detect_agents=False)
        cand = ProcessCandidate(
            pid=210,
            exe=r"C:\Program Files\nodejs\node.exe",
            argv=[
                "renamed.exe",
                (
                    r"C:\Users\alice\AppData\Roaming\npm\node_modules"
                    r"\@openai\codex\bin\codex.js"
                ),
            ],
        )

        out = classify_processes([cand], ctx)

        assert len(out) == 1
        assert out[0].kind == "client"
        assert out[0].matched_client == "codex"

    def test_config_command_match_carries_hash(self):
        cand = ProcessCandidate(
            pid=202,
            exe="/usr/local/bin/my-custom-server",
            argv=["my-custom-server", "--flag"],
        )
        ctx = ClassifierContext(
            configured_commands={(None, "my-custom-server", ("--flag",)): "cfg-abc"}
        )
        out = classify_processes([cand], ctx)
        assert len(out) == 1
        assert out[0].config_hash == "cfg-abc"
        assert out[0].transport == "stdio"
        assert out[0].kind == "mcp_server"

    def test_same_command_correlates_within_host_and_wsl_namespaces(self):
        server = _FakeServer(
            command="my-custom-server",
            args=["--flag"],
        )
        context = build_context(
            [
                _FakeConfig(
                    servers=[replace(server, config_hash="cfg-host")],
                ),
                _FakeConfig(
                    servers=[replace(server, config_hash="cfg-wsl")],
                    wsl_distro="Ubuntu",
                ),
            ],
            [],
            detect_agents=False,
        )
        candidates = [
            ProcessCandidate(
                pid=202,
                argv=["my-custom-server", "--flag"],
            ),
            ProcessCandidate(
                pid=202,
                argv=["my-custom-server", "--flag"],
                wsl_distro="ubuntu",
            ),
        ]

        sightings = classify_processes(candidates, context)

        assert {
            sighting.wsl_distro: sighting.config_hash for sighting in sightings
        } == {None: "cfg-host", "ubuntu": "cfg-wsl"}

    def test_conflicting_command_hashes_in_one_namespace_are_ambiguous(self):
        server = _FakeServer(
            command="my-custom-server",
            args=["--flag"],
        )
        context = build_context(
            [
                _FakeConfig(servers=[replace(server, config_hash="cfg-one")]),
                _FakeConfig(servers=[replace(server, config_hash="cfg-two")]),
            ],
            [],
            detect_agents=False,
        )
        candidate = ProcessCandidate(
            pid=202,
            argv=["my-custom-server", "--flag"],
        )

        assert classify_processes([candidate], context) == []

    def test_config_port_match_carries_hash_and_transport(self):
        cand = ProcessCandidate(
            pid=203,
            exe="/usr/local/bin/some-daemon",
            argv=["some-daemon"],
            listening_ports=[3000],
            bind_scope="loopback",
        )
        ctx = ClassifierContext(configured_ports={(None, 3000): ("cfg-port", "http")})
        out = classify_processes([cand], ctx)
        assert len(out) == 1
        assert out[0].config_hash == "cfg-port"
        assert out[0].transport == "http"
        assert "config_port_match:3000" in out[0].ai_signals

    def test_same_port_correlates_within_host_and_wsl_namespaces(self):
        server = _FakeServer(
            url="http://127.0.0.1:3000/mcp",
            type="http",
        )
        context = build_context(
            [
                _FakeConfig(
                    servers=[replace(server, config_hash="cfg-host")],
                ),
                _FakeConfig(
                    servers=[replace(server, config_hash="cfg-wsl")],
                    wsl_distro="Ubuntu",
                ),
            ],
            [],
            detect_agents=False,
        )
        candidates = [
            ProcessCandidate(
                pid=203,
                listening_ports=[3000],
                bind_scope="loopback",
            ),
            ProcessCandidate(
                pid=203,
                listening_ports=[3000],
                bind_scope="loopback",
                wsl_distro="ubuntu",
            ),
        ]

        sightings = classify_processes(candidates, context)

        assert {
            sighting.wsl_distro: sighting.config_hash for sighting in sightings
        } == {None: "cfg-host", "ubuntu": "cfg-wsl"}

    def test_conflicting_port_hashes_in_one_namespace_are_ambiguous(self):
        server = _FakeServer(
            url="http://127.0.0.1:3000/mcp",
            type="http",
        )
        context = build_context(
            [
                _FakeConfig(servers=[replace(server, config_hash="cfg-one")]),
                _FakeConfig(servers=[replace(server, config_hash="cfg-two")]),
            ],
            [],
            detect_agents=False,
        )
        candidate = ProcessCandidate(
            pid=203,
            listening_ports=[3000],
            bind_scope="loopback",
        )

        assert classify_processes([candidate], context) == []

    def test_openclaw_agent(self):
        cand = ProcessCandidate(
            pid=204, exe="/usr/local/bin/openclaw", argv=["openclaw", "serve"]
        )
        out = classify_processes([cand], ClassifierContext())
        assert len(out) == 1
        assert out[0].kind == "agent"
        assert out[0].agent_framework_id == "openclaw"
        assert out[0].agent_fingerprint is not None
        assert "agent_runtime:openclaw:argv" in out[0].ai_signals

    def test_registry_framework_agent(self):
        cand = ProcessCandidate(
            pid=205,
            exe="/usr/local/bin/python",
            argv=["python", "-m", "langgraph.api"],
        )

        out = classify_processes([cand], ClassifierContext())

        assert len(out) == 1
        assert out[0].kind == "agent"
        assert out[0].agent_framework_id == "langgraph"
        assert "agent_framework:langgraph" in out[0].ai_signals

    def test_registered_agent_gateway_port(self):
        cand = ProcessCandidate(
            pid=206,
            listening_ports=[18789],
            bind_scope="loopback",
            discovery_source="listening_port",
        )

        out = classify_processes([cand], ClassifierContext())

        assert len(out) == 1
        assert out[0].kind == "agent"
        assert "agent_runtime:openclaw:port:18789" in out[0].ai_signals

    def test_registered_service_probe_signal(self):
        cand = ProcessCandidate(
            pid=-1,
            discovery_source="runtime_probe",
            agent_runtime_signals={"openclaw": ["service:launchd"]},
        )

        out = classify_processes([cand], ClassifierContext())

        assert len(out) == 1
        assert out[0].kind == "agent"
        assert out[0].discovery_source == "runtime_probe"
        assert out[0].pid is None
        assert out[0].confidence >= 0.7
        assert "agent_runtime:openclaw:service:launchd" in out[0].ai_signals
        assert "discovery_source" not in out[0].to_api_payload()

    def test_custom_runtime_signature_drives_argv_classification(self):
        cand = ProcessCandidate(pid=207, argv=["acme-gateway", "serve"])
        ctx = ClassifierContext(
            agent_runtime_signatures=(
                ResolvedAgentRuntimeSignature(
                    framework_id="acme-agent",
                    argv_markers=("acme-gateway",),
                    gateway_ports=(4242,),
                ),
            )
        )

        out = classify_processes([cand], ctx)

        assert len(out) == 1
        assert out[0].kind == "agent"
        assert "agent_runtime:acme-agent:argv" in out[0].ai_signals

    def test_uncorrelated_listener_defaults_http(self):
        # An official MCP marker promotes it; the listener has no configured
        # match, so transport defaults to http (sse needs an active probe).
        cand = ProcessCandidate(
            pid=208,
            exe="/usr/local/bin/node",
            argv=["node", "@modelcontextprotocol/server-sse"],
            listening_ports=[8931],
            bind_scope="all_interfaces",
        )
        out = classify_processes([cand], ClassifierContext())
        assert out[0].transport == "http"


class TestAgentCorrelation:
    def test_single_framework_installation_attaches_fingerprint(self):
        candidate = ProcessCandidate(
            pid=701,
            argv=["openclaw", "serve"],
            cwd="/Users/dev/.openclaw",
        )
        context = build_context(
            [],
            [],
            [_FakeAgent("openclaw", "fp-openclaw", "/Users/dev/.openclaw")],
        )

        sighting = classify_processes([candidate], context)[0]

        assert sighting.agent_framework_id == "openclaw"
        assert sighting.agent_fingerprint == "fp-openclaw"
        assert sighting.to_dict()["agent_fingerprint"] == "fp-openclaw"

    def test_cwd_disambiguates_multiple_same_framework_installations(self):
        candidate = ProcessCandidate(
            pid=702,
            argv=["openclaw", "serve"],
            cwd="/Users/dev/project-b/runtime",
        )
        context = build_context(
            [],
            [],
            [
                _FakeAgent("openclaw", "fp-a", "/Users/dev/project-a"),
                _FakeAgent("openclaw", "fp-b", "/Users/dev/project-b"),
            ],
        )

        sighting = classify_processes([candidate], context, usernames=["dev"])[0]

        assert sighting.agent_fingerprint == "fp-b"
        assert sighting.agent_root_path == "/Users/<redacted>/project-b"
        assert sighting.to_dict()["agent_root_path"] == "/Users/<redacted>/project-b"

    def test_ambiguous_framework_without_cwd_stays_uncorrelated(self):
        candidate = ProcessCandidate(pid=703, argv=["openclaw", "serve"])
        context = build_context(
            [],
            [],
            [
                _FakeAgent("openclaw", "fp-a", "/Users/dev/project-a"),
                _FakeAgent("openclaw", "fp-b", "/Users/dev/project-b"),
            ],
        )

        sighting = classify_processes([candidate], context)[0]

        assert sighting.agent_framework_id == "openclaw"
        assert sighting.agent_fingerprint is None


# ---------------------------------------------------------------------------
# Combination signals -- weak-alone must combine to pass
# ---------------------------------------------------------------------------
class TestCombinationSignals:
    @pytest.mark.parametrize(
        "executable",
        [
            "/opt/.cache/PrintSpoolerCache/colorprofile",
            "/opt/.cache/updater/runtime",
        ],
    )
    def test_renamed_electron_main_with_ai_extension_tree_is_client(
        self, executable: str
    ):
        main = ProcessCandidate(
            pid=500,
            ppid=1,
            exe=executable,
            argv=[executable],
        )
        helper = ProcessCandidate(
            pid=501,
            ppid=500,
            exe="/opt/.cache/updater/runtime-helper",
            argv=["runtime-helper", "--type=renderer"],
        )
        extension_host = ProcessCandidate(
            pid=502,
            ppid=501,
            exe="/opt/.cache/updater/runtime-helper",
            argv=[
                "runtime-helper",
                "--type=extensionHost",
                "/home/dev/.vscode/extensions/anthropic.claude-code-1.2.3/out/main.js",
            ],
        )
        context = build_context([], get_all_clients(), detect_agents=False)

        sightings = classify_processes([main, helper, extension_host], context)

        discovered_main = next(item for item in sightings if item.pid == 500)
        assert discovered_main.kind == "client"
        assert "electron_main_helpers" in discovered_main.ai_signals
        assert "ai_child_tree" in discovered_main.ai_signals

    def test_topology_matched_client_extracts_settings_overrides(self):
        executable = "/opt/.cache/updater/runtime"
        main = ProcessCandidate(
            pid=503,
            ppid=1,
            exe=executable,
            argv=[
                executable,
                "--user-data-dir",
                "/Users/alice/custom-code",
            ],
            cwd="/Users/alice/project",
        )
        helper = ProcessCandidate(
            pid=504,
            ppid=503,
            exe="/Applications/Visual Studio Code.app/Contents/MacOS/Electron",
            argv=["Electron", "--type=renderer"],
        )
        extension_host = ProcessCandidate(
            pid=505,
            ppid=504,
            exe="/opt/.cache/updater/runtime-helper",
            argv=[
                "runtime-helper",
                "--type=extensionHost",
                "/home/dev/.vscode/extensions/anthropic.claude-code-1.2.3/out/main.js",
            ],
        )
        context = build_context([], get_all_clients(), detect_agents=False)

        result = classify_processes_with_overrides(
            [main, helper, extension_host],
            context,
            usernames=["alice"],
        )

        discovered_main = next(item for item in result.processes if item.pid == 503)
        assert discovered_main.matched_client == "vscode"
        assert discovered_main.settings_overrides == [
            {
                "flag": "--user-data-dir",
                "value": "/Users/<redacted>/custom-code",
            }
        ]
        assert "settings_override:--user-data-dir" in discovered_main.ai_signals
        assert [(ref.client, ref.value) for ref in result.override_config_refs] == [
            ("vscode", "/Users/alice/custom-code"),
        ]

    def test_generic_electron_topology_without_ai_child_is_dropped(self):
        main = ProcessCandidate(
            pid=510,
            ppid=1,
            exe="/opt/example/runtime",
            argv=["/opt/example/runtime"],
        )
        helper = ProcessCandidate(
            pid=511,
            ppid=510,
            exe="/opt/example/runtime-helper",
            argv=["runtime-helper", "--type=renderer"],
        )

        assert classify_processes([main, helper], ClassifierContext()) == []

    def test_generic_electron_renderer_with_mcp_url_is_dropped(self):
        main = ProcessCandidate(
            pid=520,
            ppid=1,
            exe="/opt/browser/runtime",
            argv=["/opt/browser/runtime"],
        )
        renderer = ProcessCandidate(
            pid=521,
            ppid=520,
            exe="/opt/browser/runtime-helper",
            argv=[
                "runtime-helper",
                "--type=renderer",
                "https://example.com/mcp-server-reference",
            ],
        )

        assert classify_processes([main, renderer], ClassifierContext()) == []

    def test_electron_descendant_mcp_text_without_ai_identity_is_not_a_client(self):
        main = ProcessCandidate(
            pid=530,
            ppid=1,
            exe="/opt/browser/runtime",
            argv=["/opt/browser/runtime"],
        )
        renderer = ProcessCandidate(
            pid=531,
            ppid=530,
            exe="/opt/browser/runtime-helper",
            argv=["runtime-helper", "--type=renderer"],
        )
        extension_host = ProcessCandidate(
            pid=532,
            ppid=531,
            exe="/opt/browser/runtime-helper",
            argv=[
                "runtime-helper",
                "--type=extensionHost",
                "/home/dev/.vscode/extensions/theme/out/main.js",
            ],
        )
        terminal = ProcessCandidate(
            pid=533,
            ppid=532,
            exe="/bin/bash",
            argv=["bash", "-lc", "cat /workspace/mcp-server-notes.txt"],
        )
        context = build_context([], get_all_clients(), detect_agents=False)

        sightings = classify_processes(
            [main, renderer, extension_host, terminal],
            context,
        )

        assert 530 not in {sighting.pid for sighting in sightings}

    def test_overlapping_electron_subtrees_evaluate_each_signal_once(self, monkeypatch):
        candidates = [
            ProcessCandidate(
                pid=540,
                ppid=1,
                exe="/opt/browser/runtime",
                argv=["runtime"],
            ),
            ProcessCandidate(
                pid=541,
                ppid=540,
                exe="/opt/browser/runtime-helper",
                argv=["runtime-helper", "--type=renderer"],
            ),
            ProcessCandidate(
                pid=550,
                ppid=540,
                exe="/opt/browser/nested-runtime",
                argv=["nested-runtime"],
            ),
            ProcessCandidate(
                pid=551,
                ppid=550,
                exe="/opt/browser/runtime-helper",
                argv=["runtime-helper", "--type=renderer"],
            ),
            ProcessCandidate(
                pid=552,
                ppid=551,
                exe="/opt/browser/runtime-helper",
                argv=["runtime-helper", "--type=extensionHost"],
            ),
        ]
        signal_evaluations: dict[int, int] = {}

        def no_signal(candidate, _signatures):
            signal_evaluations[candidate.pid] = (
                signal_evaluations.get(candidate.pid, 0) + 1
            )
            return False

        monkeypatch.setattr(
            classify_module,
            "_has_ai_child_tree_signal",
            no_signal,
        )

        classify_module._electron_ai_client_pids(candidates, ClassifierContext())

        assert max(signal_evaluations.values(), default=0) <= 1

    def test_client_child_with_marker_passes(self):
        client = ProcessCandidate(pid=501, ppid=1, exe=_CURSOR_EXE, argv=[_CURSOR_EXE])
        child = ProcessCandidate(
            pid=777,
            ppid=501,
            exe="/usr/local/bin/node",
            argv=["node", "mcp-server-foo", "--x"],
        )
        ctx = ClassifierContext(client_signatures={"cursor": (_CURSOR_SIG,)})
        out = classify_processes([client, child], ctx)
        by_pid = {p.pid: p for p in out}
        assert 777 in by_pid
        assert by_pid[777].discovery_source == "client_child"
        assert by_pid[777].matched_client == "cursor"

    def test_wsl_pid_namespace_does_not_inherit_host_parent(self):
        client = ProcessCandidate(pid=501, ppid=1, exe=_CURSOR_EXE, argv=[_CURSOR_EXE])
        unrelated_wsl_process = ProcessCandidate(
            pid=777,
            ppid=501,
            exe="/usr/local/bin/node",
            argv=["node", "mcp-server-foo", "--x"],
            wsl_distro="Ubuntu",
        )
        ctx = ClassifierContext(client_signatures={"cursor": (_CURSOR_SIG,)})

        out = classify_processes([client, unrelated_wsl_process], ctx)

        assert 777 not in {process.pid for process in out}

    def test_client_child_alone_dropped(self):
        # Parenthood alone (no MCP/agent marker, no config match) is too weak.
        client = ProcessCandidate(pid=501, ppid=1, exe=_CURSOR_EXE, argv=[_CURSOR_EXE])
        child = ProcessCandidate(
            pid=778, ppid=501, exe="/usr/local/bin/node", argv=["node", "helper.js"]
        )
        ctx = ClassifierContext(client_signatures={"cursor": (_CURSOR_SIG,)})
        out = classify_processes([client, child], ctx)
        assert 778 not in {p.pid for p in out}

    def test_electron_helper_not_classified_as_client(self):
        helper = ProcessCandidate(
            pid=888,
            ppid=501,
            exe=_CURSOR_EXE,
            argv=[_CURSOR_EXE, "--type=renderer"],
        )
        ctx = ClassifierContext(client_signatures={"cursor": (_CURSOR_SIG,)})
        out = classify_processes([helper], ctx)
        assert out == []


# ---------------------------------------------------------------------------
# Redaction is applied on the way out
# ---------------------------------------------------------------------------
class TestOutputRedaction:
    def test_argv_secret_scrubbed_in_output(self):
        token = "ghp_" + "z" * 36
        cand = ProcessCandidate(
            pid=300,
            exe="/usr/local/bin/npx",
            argv=["npx", "@modelcontextprotocol/server-x", "--token", token],
        )
        out = classify_processes([cand], ClassifierContext())
        assert token not in " ".join(out[0].argv_redacted)

    def test_exe_username_scrubbed_in_output(self):
        cand = ProcessCandidate(
            pid=301,
            exe="/Users/alice/.local/bin/uvx",
            argv=["uvx", "@modelcontextprotocol/server-fetch"],
        )
        out = classify_processes([cand], ClassifierContext(), usernames=["alice"])
        assert len(out) == 1
        assert out[0].exe is not None
        assert "alice" not in out[0].exe

    def test_sorted_by_confidence_desc(self):
        strong = ProcessCandidate(
            pid=400, exe="/x/npx", argv=["npx", "@modelcontextprotocol/server-a"]
        )
        medium = ProcessCandidate(
            pid=401,
            exe="/x/node",
            argv=["node", "mcp-server-b"],
            listening_ports=[7000],
            bind_scope="loopback",
        )
        out = classify_processes([medium, strong], ClassifierContext())
        confidences = [p.confidence for p in out]
        assert confidences == sorted(confidences, reverse=True)
