"""Tests for MCP client definitions."""

import json
import ntpath
import os
from pathlib import Path
from unittest import mock


from runlayer_cli.scan.clients import (
    ConfigPath,
    ExtensionsPath,
    MCPClientDefinition,
    PluginPath,
    _is_windows_with_wsl,
    _resolve_wsl_linux_paths,
    _wsl_homes,
    get_all_clients,
    get_client_by_name,
    get_clients_with_project_configs,
)
from runlayer_cli.scan.config_parser import parse_config_file
from runlayer_cli.scan.device import DiscoveredWSLDistro, WSLDistroInventory

PRESENCE_ONLY_CLIENTS = {
    "aider",
    "amazon_q",
    "amp",
    "anythingllm",
    "auggie",
    "chatgpt_desktop",
    "chatwise",
    "cherry_studio",
    "continue",
    "crush",
    "droid",
    "gpt4all",
    "grok_cli",
    "hermes",
    "intellij_idea_community",
    "jan",
    "kiro",
    "lm_studio",
    "mcp_inspector",
    "mcp_server_everything",
    "mcp_server_fetch",
    "mcp_server_filesystem",
    "mcp_server_git",
    "mcp_server_memory",
    "mcp_server_sequential_thinking",
    "mcp_server_time",
    "microsoft_copilot",
    "msty",
    "ollama",
    "openhands",
    "perplexity",
    "qoder",
    "qwen_code",
    "raycast",
    "replit_desktop",
    "smithery_cli",
    "tabnine",
    "trae",
    "traework",
    "void",
}

EXISTING_CLIENTS_WITH_INSTALL_PROBES = {
    "antigravity",
    "claude_code",
    "claude_desktop",
    "cline",
    "cline_cli",
    "codex",
    "cursor",
    "gemini_cli",
    "github_copilot_cli",
    "goose",
    "opencode",
    "vscode",
    "warp",
    "windsurf",
    "zed",
}

PRESENCE_SIGNAL_NA = {
    ("microsoft_copilot", "linux"): "Microsoft ships no Linux client.",
    ("openhands", "windows"): "Native Windows is unsupported; scan WSL homes.",
    ("perplexity", "linux"): "Perplexity ships no Linux client.",
    ("raycast", "linux"): "Raycast ships no Linux client.",
    ("raycast", "windows"): "Windows MSIX publisher hash is not verified.",
    ("replit_desktop", "linux"): "The redesigned app dropped Linux support.",
    ("traework", "linux"): "TraeWork ships no Linux client.",
}
PRESENCE_PLATFORMS = ("macos", "windows", "linux")


def _has_presence_signal(client: MCPClientDefinition, target: str) -> bool:
    path_groups = [
        client.paths,
        client.sqlite_paths or [],
        client.plugin_paths or [],
        client.extensions_paths or [],
    ]
    if any(path.platform in {"all", target} for paths in path_groups for path in paths):
        return True

    probe = client.install_probe
    if probe is None:
        return False
    if probe.cli_binaries or probe.npm_packages or probe.pip_packages:
        return True
    if any(
        path.platform in {"all", target}
        for path in [*probe.config_files, *probe.config_dirs]
    ):
        return True
    if target == "macos":
        return bool(probe.macos_app_bundles)
    if target == "windows":
        return bool(probe.windows_display_name_prefixes or probe.windows_install_dirs)
    return bool(probe.linux_desktop_ids)


class TestConfigPath:
    def test_resolve_home_expansion(self):
        """Test ~ expansion works."""
        config_path = ConfigPath("~/test/config.json", platform="all")
        result = config_path.resolve()
        assert result == Path.home() / "test" / "config.json"

    @mock.patch.dict("os.environ", {"APPDATA": "C:/Users/Test/AppData/Roaming"})
    def test_resolve_windows_env(self):
        """%VAR% expands on Windows; elsewhere it stays literal (relative) and is dropped."""
        config_path = ConfigPath("%APPDATA%/Test/config.json", platform="all")
        result = config_path.resolve()
        if os.name == "nt":
            assert result == Path("C:/Users/Test/AppData/Roaming/Test/config.json")
        else:
            assert result is None

    def test_resolve_skips_unexpanded_env_var(self, monkeypatch):
        """An unset $VAR must yield None, not a literal relative path.

        A literal "$CLINE_DIR/..." candidate is relative, so downstream
        exists()/open() resolve it against the process cwd — which crashes the
        all-users aiwatch scan when the cwd (e.g. /root under cron) is not
        searchable by the scanned user.
        """
        monkeypatch.delenv("CLINE_DIR", raising=False)
        config_path = ConfigPath(
            "$CLINE_DIR/data/settings/cline_mcp_settings.json", platform="all"
        )
        assert config_path.resolve() is None

    @mock.patch("platform.system", return_value="Darwin")
    def test_resolve_returns_none_for_wrong_platform(self, mock_system):
        """Test that wrong platform returns None."""
        config_path = ConfigPath("/test/config.json", platform="windows")
        result = config_path.resolve()
        assert result is None

    @mock.patch("platform.system", return_value="Darwin")
    def test_resolve_works_for_matching_platform(self, mock_system):
        """Test that matching platform resolves path."""
        config_path = ConfigPath("/test/config.json", platform="macos")
        result = config_path.resolve()
        assert result == Path("/test/config.json")

    @mock.patch("platform.system", return_value="Darwin")
    def test_resolve_works_for_all_platform(self, mock_system):
        """Test that 'all' platform always resolves."""
        config_path = ConfigPath("/test/config.json", platform="all")
        result = config_path.resolve()
        assert result == Path("/test/config.json")


class TestMCPClientDefinition:
    def test_get_config_paths_returns_list(self):
        """Test that get_config_paths returns a list."""
        client = MCPClientDefinition(
            name="test",
            display_name="Test",
            paths=[ConfigPath("/test/config.json", platform="all")],
        )
        paths = client.get_config_paths()
        assert isinstance(paths, list)
        assert len(paths) == 1

    def test_extract_servers_standard_format(self):
        """Test extracting servers from standard mcpServers key."""
        client = MCPClientDefinition(
            name="test",
            display_name="Test",
            paths=[],
            servers_key="mcpServers",
        )
        config_data = {
            "mcpServers": {
                "server1": {"command": "npx"},
                "server2": {"url": "https://example.com"},
            }
        }
        servers = client.extract_servers(config_data)
        assert len(servers) == 2
        assert "server1" in servers
        assert "server2" in servers

    def test_extract_servers_nested_key(self):
        """Test extracting servers from nested key like mcp.servers."""
        client = MCPClientDefinition(
            name="test",
            display_name="Test",
            paths=[],
            servers_key="mcp.servers",
        )
        config_data = {
            "mcp": {
                "servers": {
                    "server1": {"command": "npx"},
                }
            }
        }
        servers = client.extract_servers(config_data)
        assert len(servers) == 1
        assert "server1" in servers

    def test_extract_servers_root_level(self):
        """Test extracting servers from root level (empty servers_key)."""
        client = MCPClientDefinition(
            name="test",
            display_name="Test",
            paths=[],
            servers_key="",
        )
        config_data = {
            "server1": {"command": "npx"},
            "server2": {"url": "https://example.com"},
            "otherKey": "not a server",
        }
        servers = client.extract_servers(config_data)
        assert len(servers) == 2
        assert "server1" in servers
        assert "otherKey" not in servers

    def test_extract_servers_with_wildcard_key(self):
        """Test extracting servers from wildcard key like projects.*.mcpServers."""
        client = MCPClientDefinition(
            name="test",
            display_name="Test",
            paths=[],
            servers_key="mcpServers",
            additional_servers_keys=["projects.*.mcpServers"],
        )
        config_data = {
            "mcpServers": {
                "global-server": {"command": "npx"},
            },
            "projects": {
                "/path/to/project-a": {
                    "mcpServers": {
                        "project-a-server": {"command": "node"},
                    }
                },
                "/path/to/project-b": {
                    "mcpServers": {
                        "project-b-server": {"command": "python"},
                    }
                },
            },
        }
        servers = client.extract_servers(config_data)
        assert len(servers) == 3
        assert "global-server" in servers
        # Project servers use just the server name, no project prefix
        assert "project-a-server" in servers
        assert "project-b-server" in servers

    def test_extract_servers_with_wildcard_key_adds_project_name_field(self):
        """Test that wildcard extraction adds project_name field with full path as list."""
        client = MCPClientDefinition(
            name="test",
            display_name="Test",
            paths=[],
            servers_key="mcpServers",
            additional_servers_keys=["projects.*.mcpServers"],
        )
        config_data = {
            "mcpServers": {},
            "projects": {
                "/home/user/workspace/google-sheets": {
                    "mcpServers": {
                        "sheets-server": {"command": "node"},
                    }
                },
            },
        }
        servers = client.extract_servers(config_data)
        # Should be just "sheets-server", no project prefix in the name
        assert "sheets-server" in servers
        assert not any("/home/" in k for k in servers.keys())
        # Project should be the full path in the project_name field as a list
        assert servers["sheets-server"]["project_name"] == [
            "/home/user/workspace/google-sheets"
        ]
        assert servers["sheets-server"]["command"] == "node"

    def test_disabled_client_excluded(self):
        """Test that disabled clients are not returned by get_all_clients."""
        # This tests the registry behavior
        clients = get_all_clients()
        for client in clients:
            assert client.enabled is True


class TestGetAllClients:
    def test_returns_list(self):
        """Test that get_all_clients returns a list."""
        clients = get_all_clients()
        assert isinstance(clients, list)
        assert len(clients) > 0

    def test_includes_known_clients(self):
        """Test that known clients are included."""
        clients = get_all_clients()
        names = [c.name for c in clients]
        # v0 supported clients
        assert "cursor" in names
        assert "claude_desktop" in names
        assert "claude_code" in names
        assert "vscode" in names
        assert "windsurf" in names
        assert "goose" in names
        assert "zed" in names
        assert "opencode" in names
        assert "warp" in names
        assert "raycast" in names

    def test_npm_ai_clients_declare_exact_package_identities(self):
        clients = {client.name: client for client in get_all_clients()}
        expected = {
            "claude_code": ("@anthropic-ai/claude-code", "claude"),
            "codex": ("@openai/codex", "codex"),
            "github_copilot_cli": ("@github/copilot", "copilot"),
            "gemini_cli": ("@google/gemini-cli", "gemini"),
            "opencode": ("opencode-ai", "opencode"),
            "smithery_cli": ("@smithery/cli", "smithery"),
        }

        for client_name, identity in expected.items():
            client = clients[client_name]
            assert client.install_probe is not None
            packages = client.install_probe.npm_packages
            assert [(package.name, package.bin_name) for package in packages] == [
                identity
            ]

        smithery = clients["smithery_cli"]
        assert smithery.paths == []
        assert smithery.project_config is None

    def test_official_mcp_npm_tools_declare_exact_package_identities(self):
        clients = {client.name: client for client in get_all_clients()}
        expected = {
            "mcp_inspector": ("@modelcontextprotocol/inspector", "mcp-inspector"),
            "mcp_server_everything": (
                "@modelcontextprotocol/server-everything",
                "mcp-server-everything",
            ),
            "mcp_server_filesystem": (
                "@modelcontextprotocol/server-filesystem",
                "mcp-server-filesystem",
            ),
            "mcp_server_memory": (
                "@modelcontextprotocol/server-memory",
                "mcp-server-memory",
            ),
            "mcp_server_sequential_thinking": (
                "@modelcontextprotocol/server-sequential-thinking",
                "mcp-server-sequential-thinking",
            ),
        }

        for client_name, identity in expected.items():
            client = clients[client_name]
            assert client.install_probe is not None
            packages = client.install_probe.npm_packages
            assert [(package.name, package.bin_name) for package in packages] == [
                identity
            ]
            assert client.paths == []
            assert client.project_config is None

    def test_official_mcp_python_servers_declare_exact_distribution_identities(self):
        clients = {client.name: client for client in get_all_clients()}
        expected = {
            "mcp_server_fetch": ("mcp-server-fetch", "Fetch MCP Server"),
            "mcp_server_git": ("mcp-server-git", "Git MCP Server"),
            "mcp_server_time": ("mcp-server-time", "Time MCP Server"),
        }

        for client_name, (distribution, display_name) in expected.items():
            client = clients[client_name]
            assert client.display_name == display_name
            assert client.install_probe is not None
            assert [package.name for package in client.install_probe.pip_packages] == [
                distribution
            ]
            assert client.install_probe.cli_binaries == []
            assert client.paths == []
            assert client.project_config is None

    def test_presence_only_clients_are_registered_without_config_scanning(self):
        clients = {client.name: client for client in get_all_clients()}

        assert PRESENCE_ONLY_CLIENTS <= clients.keys()
        for name in PRESENCE_ONLY_CLIENTS:
            client = clients[name]
            assert client.install_probe is not None
            assert client.paths == []
            assert client.project_config is None
            assert client.iter_project_configs() == []

    def test_collision_prone_presence_signals_are_omitted(self):
        clients = {client.name: client for client in get_all_clients()}

        assert "amp" not in clients["amp"].install_probe.cli_binaries
        assert "grok" not in clients["grok_cli"].install_probe.cli_binaries
        assert "agent" not in clients["grok_cli"].install_probe.cli_binaries
        assert "hermes" not in clients["hermes"].install_probe.cli_binaries
        assert clients["hermes"].install_probe.config_dirs == []
        assert "~/.hermes/config.yaml" in {
            path.path for path in clients["hermes"].install_probe.config_files
        }
        assert "~/.config/amp" not in {
            path.path for path in clients["amp"].install_probe.config_dirs
        }
        assert all(
            path.path != "~/.augment"
            for path in clients["auggie"].install_probe.config_dirs
        )
        assert clients["codex"].install_probe.macos_app_bundles == []
        for name in {"claude_code", "cline_cli", "gemini_cli"}:
            assert clients[name].install_probe.config_dirs == []
            assert clients[name].install_probe.probe_config_parents is False

    def test_verified_desktop_presence_surfaces_are_registered(self):
        clients = {client.name: client for client in get_all_clients()}
        qwen = clients["qwen_code"].install_probe
        droid = clients["droid"].install_probe
        hermes = clients["hermes"].install_probe
        goose = clients["goose"].install_probe
        opencode = clients["opencode"].install_probe

        assert qwen.macos_app_bundles == ["Qwen Code Desktop.app"]
        assert qwen.windows_display_name_prefixes == ["Qwen Code Desktop"]
        assert qwen.linux_desktop_ids == ["qwen-code-desktop.desktop"]
        assert droid.macos_app_bundles == ["Factory.app"]
        assert hermes.macos_app_bundles == ["Hermes.app"]
        assert hermes.cli_binaries == ["hermes-agent", "hermes-acp"]
        assert goose.macos_app_bundles == ["Goose.app"]
        assert goose.linux_desktop_ids == ["goose.desktop", "Goose.desktop"]
        assert opencode.macos_app_bundles == ["OpenCode.app"]
        assert opencode.linux_desktop_ids == [
            "ai.opencode.desktop.desktop",
            "opencode-desktop.desktop",
        ]

    def test_wave_one_clients_have_researched_presence_signals(self):
        clients = {client.name: client for client in get_all_clients()}

        assert clients["ollama"].install_probe.cli_binaries == ["ollama"]
        assert clients["lm_studio"].install_probe.probe_cli_version is False
        assert clients["jan"].install_probe.probe_cli_version is False
        assert clients["chatwise"].install_probe.linux_desktop_ids == [
            "ChatWise.desktop"
        ]
        assert clients["gpt4all"].install_probe.windows_install_dirs == [
            "%USERPROFILE%/gpt4all/bin/chat.exe"
        ]
        assert clients["anythingllm"].install_probe.linux_desktop_ids == [
            "anythingllmdesktop.desktop"
        ]
        assert clients["cherry_studio"].install_probe.config_dirs
        assert clients["msty"].install_probe.macos_app_bundles == [
            "Msty.app",
            "MstyStudio.app",
            "Msty Studio.app",
        ]

    def test_wave_two_clients_have_researched_presence_signals(self):
        clients = {client.name: client for client in get_all_clients()}

        assert clients["chatgpt_desktop"].install_probe.linux_desktop_ids == [
            "chatgpt.desktop"
        ]
        assert clients["microsoft_copilot"].install_probe.linux_desktop_ids == []
        assert clients["perplexity"].install_probe.windows_install_dirs == [
            "%LOCALAPPDATA%/Programs/Perplexity/Perplexity.exe"
        ]
        assert clients["raycast"].install_probe.macos_app_bundles == ["Raycast.app"]
        assert clients["raycast"].install_probe.windows_install_dirs == []
        assert clients["replit_desktop"].install_probe.cli_binaries == []

    def test_wave_three_clients_have_researched_presence_signals(self):
        clients = {client.name: client for client in get_all_clients()}

        assert clients["continue"].install_probe.cli_binaries == []
        assert clients["amazon_q"].install_probe.cli_binaries == ["qchat", "qterm"]
        assert clients["amazon_q"].install_probe.probe_cli_version is False
        assert clients["tabnine"].install_probe.cli_binaries == ["tabnine"]
        roo = clients["roo_code"]
        assert roo.paths
        assert roo.project_config is not None
        assert roo.project_config.relative_path == ".roo/mcp.json"
        assert roo.install_probe.probe_cli_version is False
        assert "roo_code" not in PRESENCE_ONLY_CLIENTS

    def test_intellij_community_presence_is_independent_of_junie(self):
        intellij = get_client_by_name("intellij_idea_community")
        junie = get_client_by_name("junie")

        assert intellij is not None
        assert intellij.paths == []
        assert intellij.install_probe is not None
        assert intellij.install_probe.macos_app_bundles == ["IntelliJ IDEA CE.app"]
        assert intellij.install_probe.windows_display_name_prefixes == [
            "IntelliJ IDEA Community"
        ]
        assert intellij.install_probe.linux_desktop_ids == ["jetbrains-idea-ce.desktop"]
        assert junie is not None
        assert junie.paths

    def test_traework_presence_is_independent_of_trae(self):
        trae = get_client_by_name("trae")
        traework = get_client_by_name("traework")

        assert trae is not None
        assert traework is not None
        assert traework.paths == []
        assert traework.process_signatures == [
            "trae solo.app/contents/macos/electron",
            "\\programs\\trae solo\\trae solo.exe",
        ]
        assert traework.install_probe is not None
        assert traework.install_probe.macos_app_bundles == [
            "TRAE SOLO.app",
            "TRAE SOLO CN.app",
            "TraeWork.app",
        ]
        assert traework.install_probe.windows_display_name_prefixes == [
            "TraeWork (User)"
        ]
        assert traework.install_probe.windows_install_dirs == [
            "%LOCALAPPDATA%/Programs/TRAE SOLO/TRAE SOLO.exe"
        ]
        assert {
            (path.path, path.platform) for path in traework.install_probe.config_dirs
        } == {
            ("~/Library/Application Support/TRAE SOLO", "macos"),
            ("~/Library/Application Support/TRAE SOLO CN", "macos"),
            ("%APPDATA%/TRAE SOLO", "windows"),
        }
        assert trae.install_probe is not None
        assert set(trae.install_probe.macos_app_bundles).isdisjoint(
            traework.install_probe.macos_app_bundles
        )
        assert all(
            trae_signature not in traework_signature
            and traework_signature not in trae_signature
            for trae_signature in trae.process_signatures or []
            for traework_signature in traework.process_signatures
        )

    def test_verified_existing_client_windows_surfaces_are_registered(self):
        clients = {client.name: client for client in get_all_clients()}

        assert clients["claude_code"].install_probe.windows_display_name_prefixes == [
            "Claude Code"
        ]
        assert clients["goose"].install_probe.windows_install_dirs == [
            "%USERPROFILE%/.local/bin/goose.exe"
        ]
        assert clients["opencode"].install_probe.windows_display_name_prefixes == [
            "OpenCode"
        ]
        assert clients["codex"].install_probe.windows_display_name_prefixes == [
            "Codex CLI"
        ]
        assert clients[
            "github_copilot_cli"
        ].install_probe.windows_display_name_prefixes == [
            "Copilot CLI",
            "GitHub Copilot CLI",
        ]
        assert clients["void"].install_probe.windows_install_dirs == [
            "%LOCALAPPDATA%/Programs/Void/Void.exe",
            "%PROGRAMFILES%/Void/Void.exe",
        ]

    def test_per_os_audit_strengthens_grok_cli_unix_presence(self):
        probe = get_client_by_name("grok_cli").install_probe
        assert {(path.path, path.platform) for path in probe.config_files} == {
            ("~/.grok/bin/grok", "macos"),
            ("~/.grok/bin/grok", "linux"),
        }

    def test_claude_desktop_windows_msix_config_paths_are_registered(self):
        client = get_client_by_name("claude_desktop")
        assert client is not None
        path_templates = {path.path for path in client.paths}

        assert {
            "%LOCALAPPDATA%/Packages/Claude_pzs8sxrjxfjjc/LocalCache/Roaming/"
            "Claude/extensions-installations.json",
            "%LOCALAPPDATA%/Packages/Claude_pzs8sxrjxfjjc/LocalCache/Roaming/"
            "Claude/claude_desktop_config.json",
        } <= path_templates

    def test_verified_established_gui_surfaces_are_registered(self):
        clients = {client.name: client for client in get_all_clients()}

        assert clients["cursor"].install_probe.windows_display_name_prefixes == [
            "Cursor"
        ]
        assert clients["claude_desktop"].install_probe.linux_desktop_ids == [
            "com.anthropic.Claude.desktop"
        ]
        assert clients["windsurf"].install_probe.macos_app_bundles == [
            "Windsurf.app",
            "Devin.app",
        ]
        assert clients["windsurf"].install_probe.cli_binaries == [
            "windsurf",
            "devin-desktop",
        ]
        assert clients["zed"].install_probe.windows_install_dirs[0] == (
            "%LOCALAPPDATA%/Programs/Zed/Zed.exe"
        )
        assert clients["warp"].install_probe.macos_app_bundles == [
            "Warp.app",
            "WarpPreview.app",
        ]
        assert "%LOCALAPPDATA%/warp/WarpPreview/data/warp.sqlite" in {
            path.path for path in clients["warp"].sqlite_paths
        }
        assert clients["antigravity"].install_probe.cli_binaries == [
            "agy",
            "antigravity",
            "antigravity-ide",
        ]
        assert clients["antigravity"].install_probe.linux_desktop_ids == [
            "antigravity.desktop"
        ]
        cline = clients["cline"].install_probe
        assert (
            cline.macos_app_bundles
            == cline.cli_binaries
            == cline.windows_display_name_prefixes
            == cline.windows_install_dirs
            == cline.linux_desktop_ids
            == []
        )

    def test_gui_launcher_version_probes_are_disabled(self):
        clients = {client.name: client for client in get_all_clients()}
        gui_launchers = {
            "antigravity",
            "claude_desktop",
            "cursor",
            "kiro",
            "openhands",
            "qoder",
            "trae",
            "vscode",
            "warp",
            "windsurf",
            "zed",
        }

        assert all(
            clients[name].install_probe.probe_cli_version is False
            for name in gui_launchers
        )

    def test_existing_clients_have_install_probes(self):
        clients = {client.name: client for client in get_all_clients()}

        assert {
            name
            for name in EXISTING_CLIENTS_WITH_INSTALL_PROBES
            if clients[name].install_probe is None
        } == set()

    def test_every_client_has_per_os_presence_coverage_or_explicit_na(self):
        clients = get_all_clients()
        registered = {client.name for client in clients}
        unknown_allowlist_clients = {
            name for name, _platform in PRESENCE_SIGNAL_NA if name not in registered
        }
        assert unknown_allowlist_clients == set()

        missing = [
            (client.name, target)
            for client in clients
            for target in PRESENCE_PLATFORMS
            if (client.name, target) not in PRESENCE_SIGNAL_NA
            and not _has_presence_signal(client, target)
        ]
        assert missing == []


class TestGetClientByName:
    def test_claude_desktop_reads_windows_msix_config(
        self, tmp_path: Path, monkeypatch
    ):
        local_app_data = tmp_path / "AppData" / "Local"
        config_path = (
            local_app_data
            / "Packages"
            / "Claude_pzs8sxrjxfjjc"
            / "LocalCache"
            / "Roaming"
            / "Claude"
            / "claude_desktop_config.json"
        )
        config_path.parent.mkdir(parents=True)
        config_path.write_text(
            json.dumps(
                {
                    "mcpServers": {
                        "casey-gateway": {
                            "command": "mcp-remote",
                            "args": ["https://aigateway.caseys.local"],
                        }
                    }
                }
            )
        )
        monkeypatch.setattr("platform.system", lambda: "Windows")
        monkeypatch.setenv("LOCALAPPDATA", str(local_app_data))
        monkeypatch.setattr(
            "runlayer_cli.scan.clients.os.path.expandvars", ntpath.expandvars
        )

        client = get_client_by_name("claude_desktop")
        assert client is not None
        parsed_configs = [
            parsed
            for path in client.get_config_paths()
            if (parsed := parse_config_file(client, path)) is not None
        ]

        assert [
            server.name for config in parsed_configs for server in config.servers
        ] == ["casey-gateway"]

    def test_returns_client_if_exists(self):
        """Test that existing client is returned."""
        client = get_client_by_name("cursor")
        assert client is not None
        assert client.name == "cursor"

    def test_returns_none_if_not_exists(self):
        """Test that None is returned for unknown client."""
        client = get_client_by_name("nonexistent")
        assert client is None


class TestGetClientsWithProjectConfigs:
    def test_returns_only_clients_with_project_config(self):
        """Test that only clients with project configs are returned."""
        clients = get_clients_with_project_configs()
        for client in clients:
            assert client.project_config is not None

    def test_includes_expected_clients(self):
        """Test that expected clients with project configs are included."""
        clients = get_clients_with_project_configs()
        names = [c.name for c in clients]
        # These clients have project configs
        assert "cursor" in names
        assert "claude_code" in names
        assert "vscode" in names
        assert "windsurf" in names
        assert "zed" in names
        assert "opencode" in names
        assert "github_copilot_cli" in names
        assert "gemini_cli" in names
        assert "roo_code" in names
        # These don't
        assert "claude_desktop" not in names


class TestClientServersKey:
    """Test that each client has the correct servers_key configured."""

    def test_vscode_uses_servers_key(self):
        """VS Code uses 'servers' not 'mcpServers'."""
        client = get_client_by_name("vscode")
        assert client is not None
        assert client.servers_key == "servers", (
            "VS Code must use 'servers' key, not 'mcpServers'"
        )

    def test_cursor_uses_mcpservers_key(self):
        """Cursor uses standard 'mcpServers' key."""
        client = get_client_by_name("cursor")
        assert client is not None
        assert client.servers_key == "mcpServers"

    def test_claude_desktop_uses_extensions_key(self):
        """Claude Desktop uses 'extensions' key for extensions-installations.json."""
        client = get_client_by_name("claude_desktop")
        assert client is not None
        assert client.servers_key == "extensions"

    def test_claude_code_uses_mcpservers_key(self):
        """Claude Code uses standard 'mcpServers' key."""
        client = get_client_by_name("claude_code")
        assert client is not None
        assert client.servers_key == "mcpServers"

    def test_claude_code_has_additional_keys(self):
        """Claude Code has additional keys for projects.*.mcpServers."""
        client = get_client_by_name("claude_code")
        assert client is not None
        assert client.additional_servers_keys is not None
        assert "projects.*.mcpServers" in client.additional_servers_keys

    def test_windsurf_uses_mcpservers_key(self):
        """Windsurf uses standard 'mcpServers' key."""
        client = get_client_by_name("windsurf")
        assert client is not None
        assert client.servers_key == "mcpServers"

    def test_goose_uses_extensions_key(self):
        """Goose uses 'extensions' key for extensions."""
        client = get_client_by_name("goose")
        assert client is not None
        assert client.servers_key == "extensions"

    def test_goose_uses_yaml_format(self):
        """Goose uses YAML config format, not JSON."""
        client = get_client_by_name("goose")
        assert client is not None
        assert client.config_format == "yaml"

    def test_goose_has_no_project_config(self):
        """Goose only has global config, no project-level config."""
        client = get_client_by_name("goose")
        assert client is not None
        assert client.project_config is None

    def test_zed_uses_context_servers_key(self):
        """Zed uses 'context_servers' key for MCP servers."""
        client = get_client_by_name("zed")
        assert client is not None
        assert client.servers_key == "context_servers"

    def test_zed_has_project_config(self):
        """Zed has project-level config at .zed/settings.json."""
        client = get_client_by_name("zed")
        assert client is not None
        assert client.project_config is not None
        assert client.project_config.relative_path == ".zed/settings.json"
        assert client.project_config.servers_key == "context_servers"

    def test_zed_has_extensions_paths(self):
        """Zed has extensions_paths for scanning installed extensions."""
        client = get_client_by_name("zed")
        assert client is not None
        assert client.extensions_paths is not None
        assert len(client.extensions_paths) == 3
        # Check macOS path
        macos_path = next(
            (p for p in client.extensions_paths if p.platform == "macos"), None
        )
        assert macos_path is not None
        assert "extensions/installed" in macos_path.path
        assert macos_path.prefix == "mcp-server-"
        # Check Linux path
        linux_path = next(
            (p for p in client.extensions_paths if p.platform == "linux"), None
        )
        assert linux_path is not None
        assert ".local/share/zed/extensions/installed" in linux_path.path
        assert linux_path.prefix == "mcp-server-"
        # Check Windows path
        windows_path = next(
            (p for p in client.extensions_paths if p.platform == "windows"), None
        )
        assert windows_path is not None
        assert windows_path.prefix == "mcp-server-"

    def test_zed_extract_servers(self):
        """Zed extracts servers from context_servers key."""
        client = get_client_by_name("zed")
        assert client is not None
        config_data = {
            "context_servers": {
                "my-server": {"command": "node", "args": ["server.js"]},
                "remote-server": {"url": "https://example.com/mcp"},
            },
            "other_settings": {"theme": "dark"},
        }
        servers = client.extract_servers(config_data)
        assert len(servers) == 2
        assert "my-server" in servers
        assert "remote-server" in servers

    def test_cline_uses_mcpservers_key(self):
        client = get_client_by_name("cline")
        assert client is not None
        assert client.servers_key == "mcpServers"
        assert client.project_config is None

    def test_cline_has_linux_path(self):
        client = get_client_by_name("cline")
        assert client is not None
        linux_paths = [p for p in client.paths if p.platform == "linux"]
        assert len(linux_paths) == 1
        assert (
            ".config/Code/User/globalStorage/saoudrizwan.claude-dev"
            in linux_paths[0].path
        )

    def test_roo_code_uses_its_unrenamed_global_storage_id(self):
        client = get_client_by_name("roo_code")
        assert client is not None
        assert client.servers_key == "mcpServers"
        assert len(client.paths) == 3
        assert all(
            "rooveterinaryinc.roo-cline/settings/mcp_settings.json" in path.path
            for path in client.paths
        )

    def test_cline_cli_uses_mcpservers_key(self):
        client = get_client_by_name("cline_cli")
        assert client is not None
        assert client.servers_key == "mcpServers"
        assert client.project_config is None

    def test_gemini_cli_has_project_config(self):
        client = get_client_by_name("gemini_cli")
        assert client is not None
        assert client.servers_key == "mcpServers"
        assert client.project_config is not None
        assert client.project_config.relative_path == ".gemini/settings.json"

    def test_gemini_cli_extract_servers_ignores_other_settings(self):
        """Gemini CLI shares settings.json with non-MCP keys; only mcpServers should be picked up."""
        client = get_client_by_name("gemini_cli")
        assert client is not None
        config_data = {
            "mcpServers": {
                "context7": {"url": "https://mcp.context7.com/mcp"},
            },
            "theme": "Default",
            "selectedAuthType": "oauth-personal",
        }
        servers = client.extract_servers(config_data)
        assert list(servers.keys()) == ["context7"]

    def test_antigravity_global_only(self):
        client = get_client_by_name("antigravity")
        assert client is not None
        assert client.servers_key == "mcpServers"
        assert client.project_config is None

    def test_github_copilot_cli_uses_mcpservers_globally(self):
        client = get_client_by_name("github_copilot_cli")
        assert client is not None
        assert client.servers_key == "mcpServers"

    def test_github_copilot_cli_has_copilot_home_path(self):
        client = get_client_by_name("github_copilot_cli")
        assert client is not None
        env_paths = [p for p in client.paths if "$COPILOT_HOME" in p.path]
        assert len(env_paths) == 1

    def test_github_copilot_cli_no_xdg_path(self):
        client = get_client_by_name("github_copilot_cli")
        assert client is not None
        xdg_paths = [p for p in client.paths if "XDG_CONFIG_HOME" in p.path]
        assert len(xdg_paths) == 0

    def test_github_copilot_cli_primary_project_config(self):
        """Primary project config is .mcp.json with mcpServers."""
        client = get_client_by_name("github_copilot_cli")
        assert client is not None
        assert client.project_config is not None
        assert client.project_config.relative_path == ".mcp.json"
        assert client.project_config.servers_key == "mcpServers"
        assert client.project_config.requires_client_presence is True

    def test_github_copilot_cli_additional_project_configs(self):
        """Copilot's additional project config is .github/mcp.json."""
        client = get_client_by_name("github_copilot_cli")
        assert client is not None
        assert client.additional_project_configs is not None
        assert len(client.additional_project_configs) == 1
        github_pc = client.additional_project_configs[0]
        assert github_pc.relative_path == ".github/mcp.json"
        assert github_pc.servers_key == "mcpServers"

    def test_github_copilot_cli_iter_project_configs(self):
        """iter_project_configs yields primary + additional."""
        client = get_client_by_name("github_copilot_cli")
        assert client is not None
        all_pcs = client.iter_project_configs()
        assert len(all_pcs) == 2
        paths = [pc.relative_path for pc in all_pcs]
        assert ".mcp.json" in paths
        assert ".github/mcp.json" in paths
        assert ".vscode/mcp.json" not in paths


class TestExtensionsPath:
    """Tests for ExtensionsPath dataclass."""

    def test_resolve_home_expansion(self):
        """Test ~ expansion works."""
        ext_path = ExtensionsPath("~/test/extensions", platform="all")
        result = ext_path.resolve()
        assert result == Path.home() / "test" / "extensions"

    @mock.patch("platform.system", return_value="Darwin")
    def test_resolve_returns_none_for_wrong_platform(self, mock_system):
        """Test that wrong platform returns None."""
        ext_path = ExtensionsPath("/test/extensions", platform="windows")
        result = ext_path.resolve()
        assert result is None

    @mock.patch("platform.system", return_value="Darwin")
    def test_resolve_works_for_matching_platform(self, mock_system):
        """Test that matching platform resolves path."""
        ext_path = ExtensionsPath("/test/extensions", platform="macos")
        result = ext_path.resolve()
        assert result == Path("/test/extensions")

    def test_default_prefix_is_mcp_server(self):
        """Test default prefix is 'mcp-server-'."""
        ext_path = ExtensionsPath("/test/extensions")
        assert ext_path.prefix == "mcp-server-"

    def test_custom_prefix(self):
        """Test custom prefix can be set."""
        ext_path = ExtensionsPath("/test/extensions", prefix="custom-prefix")
        assert ext_path.prefix == "custom-prefix"


class TestPluginPath:
    """Tests for PluginPath dataclass."""

    def test_resolve_home_expansion(self):
        plugin_path = PluginPath("~/test/plugins", platform="all")
        result = plugin_path.resolve()
        assert result == Path.home() / "test" / "plugins"

    @mock.patch("platform.system", return_value="Darwin")
    def test_resolve_returns_none_for_wrong_platform(self, mock_system):
        plugin_path = PluginPath("/test/plugins", platform="windows")
        assert plugin_path.resolve() is None

    @mock.patch("platform.system", return_value="Darwin")
    def test_resolve_works_for_matching_platform(self, mock_system):
        plugin_path = PluginPath("/test/plugins", platform="macos")
        assert plugin_path.resolve() == Path("/test/plugins")

    def test_default_mcp_filenames(self):
        plugin_path = PluginPath("/test/plugins")
        assert plugin_path.mcp_filenames == ("mcp.json", ".mcp.json")

    def test_custom_mcp_filenames(self):
        plugin_path = PluginPath("/test/plugins", mcp_filenames=("custom.json",))
        assert plugin_path.mcp_filenames == ("custom.json",)


class TestCursorClientDefinition:
    """Tests for Cursor-specific client definition fields."""

    def test_cursor_has_plugin_paths(self):
        client = get_client_by_name("cursor")
        assert client is not None
        assert client.plugin_paths is not None
        assert len(client.plugin_paths) == 3
        macos = next(p for p in client.plugin_paths if p.platform == "macos")
        assert "plugins/cache/cursor-public" in macos.path
        linux = next(p for p in client.plugin_paths if p.platform == "linux")
        assert "plugins/cache/cursor-public" in linux.path

    def test_cursor_has_project_config(self):
        client = get_client_by_name("cursor")
        assert client is not None
        assert client.project_config is not None
        assert client.project_config.relative_path == ".cursor/mcp.json"
        assert client.project_config.servers_key == "mcpServers"

    def test_cursor_in_clients_with_project_configs(self):
        clients = get_clients_with_project_configs()
        names = [c.name for c in clients]
        assert "cursor" in names


class TestCodexClientDefinition:
    """Tests for Codex client definition."""

    def test_codex_in_all_clients(self):
        clients = get_all_clients()
        names = [c.name for c in clients]
        assert "codex" in names

    def test_codex_uses_mcp_servers_key(self):
        client = get_client_by_name("codex")
        assert client is not None
        assert client.servers_key == "mcp_servers"

    def test_codex_uses_toml_format(self):
        client = get_client_by_name("codex")
        assert client is not None
        assert client.config_format == "toml"

    def test_codex_has_project_config(self):
        client = get_client_by_name("codex")
        assert client is not None
        assert client.project_config is not None
        assert client.project_config.relative_path == ".codex/config.toml"
        assert client.project_config.servers_key == "mcp_servers"

    def test_codex_in_clients_with_project_configs(self):
        clients = get_clients_with_project_configs()
        names = [c.name for c in clients]
        assert "codex" in names

    def test_codex_has_plugin_paths(self):
        client = get_client_by_name("codex")
        assert client is not None
        assert client.plugin_paths is not None
        assert len(client.plugin_paths) >= 1

    def test_codex_extract_servers(self):
        client = get_client_by_name("codex")
        assert client is not None
        config_data = {
            "mcp_servers": {
                "my-server": {"command": "npx", "args": ["pkg"]},
                "remote": {"url": "https://example.com/mcp"},
            }
        }
        servers = client.extract_servers(config_data)
        assert len(servers) == 2
        assert "my-server" in servers
        assert "remote" in servers


class TestWarpClientDefinition:
    """Tests for Warp client definition."""

    def test_warp_in_all_clients(self):
        clients = get_all_clients()
        names = [c.name for c in clients]
        assert "warp" in names

    def test_warp_uses_mcpservers_key(self):
        client = get_client_by_name("warp")
        assert client is not None
        assert client.servers_key == "mcpServers"

    def test_warp_has_project_config(self):
        client = get_client_by_name("warp")
        assert client is not None
        assert client.project_config is not None
        assert client.project_config.relative_path == ".warp/.mcp.json"
        assert client.project_config.servers_key == "mcpServers"

    def test_warp_in_clients_with_project_configs(self):
        clients = get_clients_with_project_configs()
        names = [c.name for c in clients]
        assert "warp" in names

    def test_warp_extract_servers(self):
        client = get_client_by_name("warp")
        assert client is not None
        config_data = {
            "mcpServers": {
                "my-server": {"command": "npx", "args": ["pkg"]},
                "remote": {"url": "https://example.com/mcp"},
            }
        }
        servers = client.extract_servers(config_data)
        assert len(servers) == 2
        assert "my-server" in servers
        assert "remote" in servers


class TestLinuxPlatformPaths:
    """Verify every client has at least one Linux-resolvable config path."""

    CLIENTS_WITH_LINUX_PATHS = [
        "cursor",
        "claude_desktop",
        "claude_code",
        "vscode",
        "windsurf",
        "goose",
        "zed",
        "opencode",
        "codex",
        "warp",
    ]

    @mock.patch("platform.system", return_value="Linux")
    def test_all_clients_resolve_on_linux(self, _mock_system):
        for name in self.CLIENTS_WITH_LINUX_PATHS:
            client = get_client_by_name(name)
            assert client is not None, f"Client {name} not found"
            paths = client.get_config_paths()
            assert len(paths) > 0, f"Client {name} has no paths on Linux"

    @mock.patch("platform.system", return_value="Linux")
    def test_cursor_linux_path(self, _mock_system):
        config = ConfigPath("~/.cursor/mcp.json", platform="linux")
        result = config.resolve()
        assert result is not None
        assert str(result).endswith(".cursor/mcp.json")

    @mock.patch("platform.system", return_value="Linux")
    def test_claude_desktop_linux_path(self, _mock_system):
        config = ConfigPath(
            "~/.config/Claude/claude_desktop_config.json", platform="linux"
        )
        result = config.resolve()
        assert result is not None
        assert ".config/Claude" in str(result)

    @mock.patch("platform.system", return_value="Linux")
    def test_vscode_linux_path(self, _mock_system):
        config = ConfigPath("~/.config/Code/User/mcp.json", platform="linux")
        result = config.resolve()
        assert result is not None
        assert ".config/Code/User" in str(result)

    @mock.patch("platform.system", return_value="Linux")
    def test_zed_linux_extensions_path(self, _mock_system):
        client = get_client_by_name("zed")
        assert client is not None
        linux_ext = next(
            (p for p in client.extensions_paths if p.platform == "linux"), None
        )
        assert linux_ext is not None
        result = linux_ext.resolve()
        assert result is not None
        assert ".local/share/zed/extensions/installed" in str(result)


class TestWindowsWSLCrossScan:
    """Test Windows-host -> WSL-distro config path resolution."""

    def setup_method(self):
        _is_windows_with_wsl.cache_clear()
        _wsl_homes.cache_clear()

    def teardown_method(self):
        _is_windows_with_wsl.cache_clear()
        _wsl_homes.cache_clear()

    def test_resolve_wsl_linux_paths_expands_per_home(self):
        homes = [
            Path(R"\\wsl.localhost\Ubuntu\home\alex"),
            Path(R"\\wsl.localhost\Debian\home\sam"),
        ]
        with (
            mock.patch(
                "runlayer_cli.scan.clients._is_windows_with_wsl", return_value=True
            ),
            mock.patch("runlayer_cli.scan.clients._wsl_homes", return_value=homes),
        ):
            results = _resolve_wsl_linux_paths("~/.cursor/mcp.json")
            assert results == [home / ".cursor/mcp.json" for home in homes]

    def test_resolve_wsl_linux_paths_non_tilde_returns_empty(self):
        with (
            mock.patch(
                "runlayer_cli.scan.clients._is_windows_with_wsl", return_value=True
            ),
            mock.patch(
                "runlayer_cli.scan.clients._wsl_homes",
                return_value=[Path(R"\\wsl.localhost\Ubuntu\home\alex")],
            ),
        ):
            assert _resolve_wsl_linux_paths("%APPDATA%/Code/mcp.json") == []

    def test_resolve_wsl_linux_paths_no_wsl_returns_empty(self):
        with mock.patch(
            "runlayer_cli.scan.clients._is_windows_with_wsl", return_value=False
        ):
            assert _resolve_wsl_linux_paths("~/.cursor/mcp.json") == []

    @mock.patch("platform.system", return_value="Windows")
    @mock.patch.dict("os.environ", {"USERPROFILE": "/win/home"})
    def test_get_config_paths_includes_wsl_linux_paths(self, _system):
        homes = [
            Path(R"\\wsl.localhost\Ubuntu\home\alex"),
            Path(R"\\wsl.localhost\Ubuntu\home\sam"),
        ]
        with (
            mock.patch(
                "runlayer_cli.scan.clients._is_windows_with_wsl", return_value=True
            ),
            mock.patch("runlayer_cli.scan.clients._wsl_homes", return_value=homes),
        ):
            client = MCPClientDefinition(
                name="test",
                display_name="Test",
                paths=[
                    ConfigPath("~/.test/config.json", platform="linux"),
                    ConfigPath("$USERPROFILE/.test/config.json", platform="windows"),
                ],
            )
            paths = client.get_config_paths()
            # One native Windows path + one per WSL home.
            assert len(paths) == 3
            assert any("/win/home" in str(p) for p in paths)
            assert sum("wsl.localhost" in str(p) for p in paths) == 2

    @mock.patch("platform.system", return_value="Windows")
    @mock.patch.dict("os.environ", {"USERPROFILE": "/win/home"})
    def test_get_config_paths_no_wsl_only_native(self, _system):
        with mock.patch(
            "runlayer_cli.scan.clients._is_windows_with_wsl", return_value=False
        ):
            client = MCPClientDefinition(
                name="test",
                display_name="Test",
                paths=[
                    ConfigPath("~/.test/config.json", platform="linux"),
                    ConfigPath("$USERPROFILE/.test/config.json", platform="windows"),
                ],
            )
            paths = client.get_config_paths()
            assert len(paths) == 1
            assert not any("wsl.localhost" in str(p) for p in paths)

    @mock.patch("platform.system", return_value="Darwin")
    def test_is_windows_with_wsl_false_on_macos(self, _system):
        assert _is_windows_with_wsl() is False

    @mock.patch("platform.system", return_value="Windows")
    def test_incomplete_inventory_expands_no_wsl_homes(self, _system):
        incomplete = WSLDistroInventory(
            distros=(
                DiscoveredWSLDistro(name="Ubuntu", wsl_version=2, is_running=True),
            ),
            success=False,
        )
        with mock.patch(
            "runlayer_cli.scan.device.get_wsl_distro_inventory",
            return_value=incomplete,
        ):
            assert _is_windows_with_wsl() is False
            assert _wsl_homes() == []
            assert _resolve_wsl_linux_paths("~/.cursor/mcp.json") == []


class TestKimiCodeClientDefinition:
    """Kimi Code keys servers in mcp.json, not the sibling config.toml."""

    def test_registered_with_mcp_servers_key(self):
        client = get_client_by_name("kimi_code")
        assert client is not None
        assert client.display_name == "Kimi Code"
        assert client.servers_key == "mcpServers"
        assert client.config_format == "json"

    def test_honors_kimi_code_home_override(self):
        client = get_client_by_name("kimi_code")
        templates = [path.path for path in client.paths]
        assert "$KIMI_CODE_HOME/mcp.json" in templates
        assert "~/.kimi-code/mcp.json" in templates

    def test_config_toml_is_not_scanned_for_servers(self):
        """config.toml only carries MCP timeouts, so it must not be a config path."""
        client = get_client_by_name("kimi_code")
        assert all("config.toml" not in path.path for path in client.paths)

    def test_project_config(self):
        client = get_client_by_name("kimi_code")
        assert client.project_config is not None
        assert client.project_config.relative_path == ".kimi-code/mcp.json"

    def test_bare_kimi_binary_is_omitted(self):
        """Legacy Python kimi-cli ships the same command as a different product."""
        client = get_client_by_name("kimi_code")
        assert client.install_probe.cli_binaries == []

    def test_legacy_kimi_cli_home_is_not_claimed(self):
        client = get_client_by_name("kimi_code")
        templates = [path.path for path in client.paths]
        dirs = [path.path for path in client.install_probe.config_dirs]
        assert all(not t.startswith("~/.kimi/") for t in templates)
        assert "~/.kimi" not in dirs


class TestPiClientDefinition:
    """Pi's MCP support arrives through the pi-mcp-adapter extension."""

    def test_registered_with_mcp_servers_key(self):
        client = get_client_by_name("pi")
        assert client is not None
        assert client.display_name == "Pi Coding Agent"
        assert client.servers_key == "mcpServers"

    def test_honors_pi_coding_agent_dir_override(self):
        client = get_client_by_name("pi")
        templates = [path.path for path in client.paths]
        assert "$PI_CODING_AGENT_DIR/mcp.json" in templates
        assert "~/.pi/agent/mcp.json" in templates

    def test_project_config(self):
        client = get_client_by_name("pi")
        assert client.project_config is not None
        assert client.project_config.relative_path == ".pi/mcp.json"

    def test_pi_home_is_not_a_presence_signal(self):
        """Regression: third-party hosts pre-seed ~/.pi/agent/extensions/.

        A machine that never installed Pi can still have ~/.pi/agent populated
        by another tool, so neither a config_dir entry nor parent-directory
        tracing may stand in for a real install.
        """
        probe = get_client_by_name("pi").install_probe
        assert probe.probe_config_parents is False
        assert probe.config_dirs == []
        assert probe.config_files != []

    def test_bare_pi_binary_is_omitted(self):
        """`pi` is far too generic to execute or trust as a presence signal."""
        probe = get_client_by_name("pi").install_probe
        assert probe.cli_binaries == []

    def test_settings_json_is_the_install_signal(self):
        probe = get_client_by_name("pi").install_probe
        templates = {path.path for path in probe.config_files}
        assert "~/.pi/agent/settings.json" in templates


class TestJunieClientDefinition:
    """Junie writes JSON to ~/.junie, not into the IDE's XML options."""

    def test_registered_with_mcp_servers_key(self):
        client = get_client_by_name("junie")
        assert client is not None
        assert client.display_name == "JetBrains Junie"
        assert client.servers_key == "mcpServers"

    def test_nested_and_legacy_flat_paths(self):
        client = get_client_by_name("junie")
        templates = [path.path for path in client.paths]
        assert "~/.junie/mcp/mcp.json" in templates
        assert "~/.junie/mcp.json" in templates

    def test_no_jetbrains_ide_xml_paths(self):
        """MCP config never lives in the IDE config dir, so none may be listed."""
        client = get_client_by_name("junie")
        assert all(
            "JetBrains" not in path.path and not path.path.endswith(".xml")
            for path in client.paths
        )

    def test_project_config(self):
        client = get_client_by_name("junie")
        assert client.project_config is not None
        assert client.project_config.relative_path == ".junie/mcp/mcp.json"

    def test_no_invented_windows_uninstall_entry(self):
        """Junie ships via npm/brew/script, so no ARP DisplayName exists."""
        probe = get_client_by_name("junie").install_probe
        assert probe.windows_display_name_prefixes == []
        assert probe.cli_binaries == ["junie"]


class TestKiloCodeClientDefinition:
    """Kilo Code reads two config generations with different server keys."""

    def test_registered_with_both_server_keys(self):
        client = get_client_by_name("kilo_code")
        assert client is not None
        assert client.display_name == "Kilo Code"
        assert client.servers_key == "mcp"
        assert client.additional_servers_keys == ["mcpServers"]

    def test_global_config_is_xdg_rooted_on_every_platform(self):
        """Kilo resolves its root via xdg-basedir, which falls back to ~/.config."""
        client = get_client_by_name("kilo_code")
        jsonc = next(p for p in client.paths if p.path.endswith("kilo/kilo.jsonc"))
        assert jsonc.path == "~/.config/kilo/kilo.jsonc"
        assert jsonc.platform == "all"
        assert all("%APPDATA%/kilo" not in path.path for path in client.paths)

    def test_marketplace_writes_strict_json_variant(self):
        client = get_client_by_name("kilo_code")
        templates = [path.path for path in client.paths]
        assert "~/.config/kilo/kilo.json" in templates

    def test_global_config_json_alias(self):
        client = get_client_by_name("kilo_code")
        templates = [path.path for path in client.paths]
        assert "~/.config/kilo/config.json" in templates

    def test_legacy_vscode_global_storage_per_platform(self):
        client = get_client_by_name("kilo_code")
        legacy = {
            path.platform: path.path
            for path in client.paths
            if path.path.endswith("mcp_settings.json")
        }
        assert set(legacy) == {"macos", "windows", "linux"}
        assert all("kilocode.kilo-code" in path for path in legacy.values())
        assert legacy["macos"].startswith("~/Library/Application Support/Code/")
        assert legacy["windows"].startswith("%APPDATA%/Code/")
        assert legacy["linux"].startswith("~/.config/Code/")

    def test_project_configs_cover_both_generations(self):
        client = get_client_by_name("kilo_code")
        patterns = {
            p.relative_path: p.servers_key for p in client.iter_project_configs()
        }
        modern_paths = {
            "kilo.json",
            "kilo.jsonc",
            ".kilo/kilo.json",
            ".kilo/kilo.jsonc",
        }
        assert modern_paths <= patterns.keys()
        assert all(patterns[path] == "mcp" for path in modern_paths)
        assert patterns[".kilo/mcp.json"] == "mcpServers"
        assert patterns[".kilocode/mcp.json"] == "mcpServers"

    def test_bare_kilo_binary_is_omitted(self):
        probe = get_client_by_name("kilo_code").install_probe
        assert probe.cli_binaries == ["kilocode"]


class TestDevinCliClientDefinition:
    """Devin CLI is a separate config surface from Devin Desktop."""

    def test_registered_with_mcp_servers_key(self):
        client = get_client_by_name("devin_cli")
        assert client is not None
        assert client.display_name == "Devin CLI"
        assert client.servers_key == "mcpServers"

    def test_dedicated_mcp_config_and_legacy_config_paths(self):
        client = get_client_by_name("devin_cli")
        templates = [path.path for path in client.paths]
        assert "~/.config/devin/mcp_config.json" in templates
        assert "%APPDATA%/devin/mcp_config.json" in templates
        # Pre-v3000.3 hosts still keep servers in config.json.
        assert "~/.config/devin/config.json" in templates

    def test_does_not_claim_the_desktop_config(self):
        """Devin Desktop is the renamed Windsurf and stays on the windsurf entry."""
        client = get_client_by_name("devin_cli")
        assert all(".codeium" not in path.path for path in client.paths)
        windsurf = get_client_by_name("windsurf")
        assert any(".codeium/windsurf" in path.path for path in windsurf.paths)

    def test_shared_devin_home_is_not_a_signal(self):
        """~/.devin is created by the desktop app too, so it cannot stand alone."""
        probe = get_client_by_name("devin_cli").install_probe
        dirs = {path.path for path in probe.config_dirs}
        assert "~/.devin" not in dirs
        assert "~/.config/devin" in dirs

    def test_no_invented_windows_uninstall_entry(self):
        """The Windows package is a winget portable, so there is no ARP entry."""
        probe = get_client_by_name("devin_cli").install_probe
        assert probe.windows_display_name_prefixes == []


class TestNewlyAddedClientsAreConfigScanning:
    def test_all_five_clients_scan_config_and_carry_probes(self):
        clients = {client.name: client for client in get_all_clients()}
        added = ("kimi_code", "pi", "junie", "kilo_code", "devin_cli")

        assert set(added) <= clients.keys()
        for name in added:
            client = clients[name]
            assert client.paths, f"{name} should scan MCP config"
            assert client.install_probe is not None
            assert client.project_config is not None
            assert name not in PRESENCE_ONLY_CLIENTS

    def test_added_clients_have_project_configs_registered(self):
        names = {client.name for client in get_clients_with_project_configs()}
        assert {"kimi_code", "pi", "junie", "kilo_code", "devin_cli"} <= names
