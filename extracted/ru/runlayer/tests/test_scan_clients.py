"""Tests for MCP client definitions."""

from pathlib import Path
from unittest import mock


from runlayer_cli.scan.clients import (
    ConfigPath,
    ExtensionsPath,
    MCPClientDefinition,
    PluginPath,
    get_all_clients,
    get_client_by_name,
    get_clients_with_project_configs,
)


class TestConfigPath:
    def test_resolve_home_expansion(self):
        """Test ~ expansion works."""
        config_path = ConfigPath("~/test/config.json", platform="all")
        result = config_path.resolve()
        assert result == Path.home() / "test" / "config.json"

    @mock.patch.dict("os.environ", {"APPDATA": "C:/Users/Test/AppData/Roaming"})
    def test_resolve_windows_env(self):
        """Test Windows environment variable expansion."""
        config_path = ConfigPath("%APPDATA%/Test/config.json", platform="all")
        result = config_path.resolve()
        assert "Test" in str(result)

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
        # Descoped from v0
        assert "warp" not in names
        assert "raycast" not in names


class TestGetClientByName:
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
        assert len(client.extensions_paths) == 2
        # Check macOS path
        macos_path = next(
            (p for p in client.extensions_paths if p.platform == "macos"), None
        )
        assert macos_path is not None
        assert "extensions/installed" in macos_path.path
        assert macos_path.prefix == "mcp-server-"
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

    def test_github_copilot_cli_additional_project_configs(self):
        """Additional project configs: .github/mcp.json + .vscode/mcp.json."""
        client = get_client_by_name("github_copilot_cli")
        assert client is not None
        assert client.additional_project_configs is not None
        assert len(client.additional_project_configs) == 2
        github_pc = client.additional_project_configs[0]
        assert github_pc.relative_path == ".github/mcp.json"
        assert github_pc.servers_key == "mcpServers"
        vscode_pc = client.additional_project_configs[1]
        assert vscode_pc.relative_path == ".vscode/mcp.json"
        assert vscode_pc.servers_key == "servers"

    def test_github_copilot_cli_iter_project_configs(self):
        """iter_project_configs yields primary + additional."""
        client = get_client_by_name("github_copilot_cli")
        assert client is not None
        all_pcs = client.iter_project_configs()
        assert len(all_pcs) == 3
        paths = [pc.relative_path for pc in all_pcs]
        assert ".mcp.json" in paths
        assert ".github/mcp.json" in paths
        assert ".vscode/mcp.json" in paths


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
        assert len(client.plugin_paths) == 2
        macos = next(p for p in client.plugin_paths if p.platform == "macos")
        assert "plugins/cache/cursor-public" in macos.path

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
