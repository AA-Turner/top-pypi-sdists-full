"""Tests for Claude Code plugin MCP server discovery."""

import json
from pathlib import Path

from runlayer_cli.scan.claude_code_plugins import (
    _substitute_plugin_root,
    scan_claude_code_plugins,
)
from runlayer_cli.scan.config_parser import compute_config_hash


def _write_installed_plugins(path: Path, plugins: dict) -> Path:
    """Helper: write installed_plugins.json and return its path."""
    installed = path / ".claude" / "plugins" / "installed_plugins.json"
    installed.parent.mkdir(parents=True, exist_ok=True)
    installed.write_text(json.dumps({"version": 2, "plugins": plugins}))
    return installed


def _create_plugin_dir(
    tmp_path: Path,
    marketplace: str,
    name: str,
    version: str,
    mcp_json: dict | None = None,
    plugin_json: dict | None = None,
) -> str:
    """Helper: create a plugin cache directory and return its path."""
    plugin_dir = (
        tmp_path / ".claude" / "plugins" / "cache" / marketplace / name / version
    )
    plugin_dir.mkdir(parents=True, exist_ok=True)
    if mcp_json is not None:
        (plugin_dir / ".mcp.json").write_text(json.dumps(mcp_json))
    if plugin_json is not None:
        manifest_dir = plugin_dir / ".claude-plugin"
        manifest_dir.mkdir(parents=True, exist_ok=True)
        (manifest_dir / "plugin.json").write_text(json.dumps(plugin_json))
    return str(plugin_dir)


class TestScanClaudeCodePlugins:
    def test_no_installed_plugins_file(self, tmp_path: Path):
        """Returns empty list when installed_plugins.json doesn't exist."""
        result = scan_claude_code_plugins(tmp_path / "nonexistent.json")
        assert result == []

    def test_malformed_json(self, tmp_path: Path):
        """Returns empty list when file is invalid JSON."""
        bad_file = tmp_path / "installed_plugins.json"
        bad_file.write_text("{invalid json")
        result = scan_claude_code_plugins(bad_file)
        assert result == []

    def test_non_dict_top_level(self, tmp_path: Path):
        """Returns empty list when top-level JSON is not a dict."""
        bad_file = tmp_path / "installed_plugins.json"
        bad_file.write_text(json.dumps([1, 2, 3]))
        result = scan_claude_code_plugins(bad_file)
        assert result == []

    def test_empty_plugins(self, tmp_path: Path):
        """Returns empty list when no plugins are installed."""
        installed = _write_installed_plugins(tmp_path, {})
        result = scan_claude_code_plugins(installed)
        assert result == []

    def test_plugin_without_mcp_config(self, tmp_path: Path):
        """Skips plugins that have no plugin.json mcpServers or .mcp.json."""
        install_path = _create_plugin_dir(
            tmp_path, "official", "no-mcp", "abc123", mcp_json=None
        )
        installed = _write_installed_plugins(
            tmp_path,
            {"no-mcp@official": [{"scope": "user", "installPath": install_path}]},
        )
        result = scan_claude_code_plugins(installed)
        assert result == []

    def test_plugin_with_stdio_server(self, tmp_path: Path):
        """Discovers stdio MCP servers from plugin.json."""
        install_path = _create_plugin_dir(
            tmp_path,
            "official",
            "context7",
            "abc123",
            plugin_json={
                "mcpServers": {
                    "context7": {
                        "command": "npx",
                        "args": ["-y", "@context7/mcp-server"],
                    }
                }
            },
        )
        installed = _write_installed_plugins(
            tmp_path,
            {"context7@official": [{"scope": "user", "installPath": install_path}]},
        )
        result = scan_claude_code_plugins(installed)
        assert len(result) == 1
        config = result[0]
        assert config.client == "claude_code"
        assert config.config_scope == "plugin"
        assert config.config_path == str(
            Path(install_path) / ".claude-plugin" / "plugin.json"
        )
        assert len(config.servers) == 1
        assert config.servers[0].name == "context7"
        assert config.servers[0].type == "stdio"
        assert config.servers[0].command == "npx"
        assert config.servers[0].args == ["-y", "@context7/mcp-server"]

    def test_falls_back_to_mcp_json_when_manifest_lacks_mcp_servers(
        self, tmp_path: Path
    ):
        install_path = _create_plugin_dir(
            tmp_path,
            "official",
            "fallback",
            "abc123",
            mcp_json={"mcpServers": {"ctx": {"command": "npx", "args": ["ctx"]}}},
            plugin_json={"name": "fallback"},
        )
        installed = _write_installed_plugins(
            tmp_path,
            {"fallback@official": [{"scope": "user", "installPath": install_path}]},
        )

        result = scan_claude_code_plugins(installed)

        assert len(result) == 1
        assert result[0].config_path == str(Path(install_path) / ".mcp.json")
        assert [server.name for server in result[0].servers] == ["ctx"]

    def test_plugin_with_http_server(self, tmp_path: Path):
        """Discovers http MCP servers from plugin .mcp.json."""
        install_path = _create_plugin_dir(
            tmp_path,
            "official",
            "github",
            "abc123",
            mcp_json={
                "mcpServers": {
                    "github-api": {
                        "url": "https://api.github.com/mcp",
                        "transport": "http",
                        "headers": {"Authorization": "Bearer token"},
                    }
                }
            },
        )
        installed = _write_installed_plugins(
            tmp_path,
            {"github@official": [{"scope": "user", "installPath": install_path}]},
        )
        result = scan_claude_code_plugins(installed)
        assert len(result) == 1
        server = result[0].servers[0]
        assert server.name == "github-api"
        assert server.type == "http"
        assert server.url == "https://api.github.com/mcp"

    def test_plugin_json_takes_precedence_over_mcp_json(self, tmp_path: Path):
        install_path = _create_plugin_dir(
            tmp_path,
            "official",
            "priority",
            "abc123",
            mcp_json={"mcpServers": {"sidecar": {"command": "node"}}},
            plugin_json={
                "mcpServers": {
                    "inline": {
                        "command": "npx",
                        "args": ["-y", "@context7/mcp-server"],
                    }
                }
            },
        )
        installed = _write_installed_plugins(
            tmp_path,
            {"priority@official": [{"scope": "user", "installPath": install_path}]},
        )

        result = scan_claude_code_plugins(installed)

        assert len(result) == 1
        assert result[0].config_path == str(
            Path(install_path) / ".claude-plugin" / "plugin.json"
        )
        assert [server.name for server in result[0].servers] == ["inline"]

    def test_plugin_with_type_key_for_transport(self, tmp_path: Path):
        """Resolves transport via "type" key, matching Cursor parser behavior."""
        install_path = _create_plugin_dir(
            tmp_path,
            "official",
            "linear",
            "abc123",
            mcp_json={
                "mcpServers": {
                    "linear-api": {
                        "type": "http",
                        "url": "https://mcp.linear.app",
                    }
                }
            },
        )
        installed = _write_installed_plugins(
            tmp_path,
            {"linear@official": [{"scope": "user", "installPath": install_path}]},
        )
        result = scan_claude_code_plugins(installed)
        assert len(result) == 1
        server = result[0].servers[0]
        assert server.type == "http"

    def test_plugin_with_server_url_field(self, tmp_path: Path):
        """Parses remote plugin server using serverUrl field."""
        install_path = _create_plugin_dir(
            tmp_path,
            "official",
            "windsurf-like",
            "abc123",
            mcp_json={
                "mcpServers": {
                    "remote-server": {
                        "serverUrl": "https://example.com/mcp",
                    }
                }
            },
        )
        installed = _write_installed_plugins(
            tmp_path,
            {
                "windsurf-like@official": [
                    {"scope": "user", "installPath": install_path}
                ]
            },
        )
        result = scan_claude_code_plugins(installed)
        assert len(result) == 1
        server = result[0].servers[0]
        assert server.type == "sse"
        assert server.url == "https://example.com/mcp"

    def test_plugin_transport_streamable_http_normalized(self, tmp_path: Path):
        """Normalizes streamable_http transport for plugin MCP entries."""
        install_path = _create_plugin_dir(
            tmp_path,
            "official",
            "streamable-http-plugin",
            "abc123",
            mcp_json={
                "mcpServers": {
                    "remote-server": {
                        "transport": "streamable_http",
                        "url": "https://example.com/mcp",
                    }
                }
            },
        )
        installed = _write_installed_plugins(
            tmp_path,
            {
                "streamable-http-plugin@official": [
                    {"scope": "user", "installPath": install_path}
                ]
            },
        )
        result = scan_claude_code_plugins(installed)
        assert len(result) == 1
        server = result[0].servers[0]
        assert server.type == "streamable-http"
        assert server.url == "https://example.com/mcp"

    def test_plugin_name_extracted_from_key(self, tmp_path: Path):
        """Plugin name is the part before @ in the key."""
        install_path = _create_plugin_dir(
            tmp_path,
            "my-marketplace",
            "my-plugin",
            "v1",
            mcp_json={
                "mcpServers": {"server": {"command": "node", "args": ["server.js"]}}
            },
        )
        installed = _write_installed_plugins(
            tmp_path,
            {
                "my-plugin@my-marketplace": [
                    {"scope": "user", "installPath": install_path}
                ]
            },
        )
        result = scan_claude_code_plugins(installed)
        assert result[0].servers[0].project_name == "my-plugin"

    def test_multiple_plugins(self, tmp_path: Path):
        """Discovers servers from multiple plugins."""
        path_a = _create_plugin_dir(
            tmp_path,
            "official",
            "plugin-a",
            "v1",
            mcp_json={"mcpServers": {"a": {"command": "node", "args": ["a.js"]}}},
        )
        path_b = _create_plugin_dir(
            tmp_path,
            "official",
            "plugin-b",
            "v1",
            mcp_json={"mcpServers": {"b": {"command": "python", "args": ["b.py"]}}},
        )
        installed = _write_installed_plugins(
            tmp_path,
            {
                "plugin-a@official": [{"scope": "user", "installPath": path_a}],
                "plugin-b@official": [{"scope": "user", "installPath": path_b}],
            },
        )
        result = scan_claude_code_plugins(installed)
        assert len(result) == 2
        names = {r.servers[0].name for r in result}
        assert names == {"a", "b"}

    def test_multiple_scopes_same_plugin(self, tmp_path: Path):
        """Reports separate configs for each scope installation."""
        path_user = _create_plugin_dir(
            tmp_path,
            "official",
            "context7",
            "v1-user",
            mcp_json={"mcpServers": {"ctx": {"command": "npx", "args": ["ctx"]}}},
        )
        path_project = _create_plugin_dir(
            tmp_path,
            "official",
            "context7",
            "v1-proj",
            mcp_json={"mcpServers": {"ctx": {"command": "npx", "args": ["ctx"]}}},
        )
        installed = _write_installed_plugins(
            tmp_path,
            {
                "context7@official": [
                    {"scope": "user", "installPath": path_user},
                    {
                        "scope": "project",
                        "installPath": path_project,
                        "projectPath": "/Users/dev/myproject",
                    },
                ]
            },
        )
        result = scan_claude_code_plugins(installed)
        assert len(result) == 2
        project_config = next((c for c in result if c.project_path is not None), None)
        assert project_config is not None
        assert project_config.project_path == "/Users/dev/myproject"

    def test_install_path_missing_on_disk(self, tmp_path: Path):
        """Skips plugins whose installPath doesn't exist."""
        installed = _write_installed_plugins(
            tmp_path,
            {
                "gone@official": [
                    {
                        "scope": "user",
                        "installPath": str(tmp_path / "nonexistent"),
                    }
                ]
            },
        )
        result = scan_claude_code_plugins(installed)
        assert result == []

    def test_config_path_points_to_mcp_json(self, tmp_path: Path):
        """MCPClientConfig.config_path points to plugin's .mcp.json."""
        install_path = _create_plugin_dir(
            tmp_path,
            "official",
            "test",
            "v1",
            mcp_json={"mcpServers": {"s": {"command": "echo"}}},
        )
        installed = _write_installed_plugins(
            tmp_path,
            {"test@official": [{"scope": "user", "installPath": install_path}]},
        )
        result = scan_claude_code_plugins(installed)
        assert result[0].config_path == str(Path(install_path) / ".mcp.json")

    def test_last_updated_propagated(self, tmp_path: Path):
        """config_modified_at is set from lastUpdated in the manifest."""
        install_path = _create_plugin_dir(
            tmp_path,
            "official",
            "test",
            "v1",
            mcp_json={"mcpServers": {"s": {"command": "echo"}}},
        )
        installed = _write_installed_plugins(
            tmp_path,
            {
                "test@official": [
                    {
                        "scope": "user",
                        "installPath": install_path,
                        "lastUpdated": "2026-02-26T20:21:39.820Z",
                    }
                ]
            },
        )
        result = scan_claude_code_plugins(installed)
        assert result[0].config_modified_at == "2026-02-26T20:21:39.820Z"

    def test_servers_have_config_hash(self, tmp_path: Path):
        """Each discovered server has a non-empty config_hash."""
        install_path = _create_plugin_dir(
            tmp_path,
            "official",
            "test",
            "v1",
            mcp_json={"mcpServers": {"s": {"command": "echo"}}},
        )
        installed = _write_installed_plugins(
            tmp_path,
            {"test@official": [{"scope": "user", "installPath": install_path}]},
        )
        result = scan_claude_code_plugins(installed)
        assert result[0].servers[0].config_hash != ""
        assert len(result[0].servers[0].config_hash) == 64

    def test_config_hash_matches_after_substitution(self, tmp_path: Path):
        """config_hash must match resolved values, not raw templates."""
        install_path = _create_plugin_dir(
            tmp_path,
            "official",
            "templ",
            "v1",
            mcp_json={
                "mcpServers": {
                    "srv": {
                        "command": "${CLAUDE_PLUGIN_ROOT}/bin/server",
                        "args": ["--config", "${CLAUDE_PLUGIN_ROOT}/config.json"],
                    }
                }
            },
        )
        installed = _write_installed_plugins(
            tmp_path,
            {"templ@official": [{"scope": "user", "installPath": install_path}]},
        )
        result = scan_claude_code_plugins(installed)
        server = result[0].servers[0]
        assert server.command == f"{install_path}/bin/server"
        assert compute_config_hash(server) == server.config_hash

    def test_non_dict_mcp_json(self, tmp_path: Path):
        """Returns empty list when .mcp.json is valid JSON but not a dict."""
        plugin_dir = (
            tmp_path / ".claude" / "plugins" / "cache" / "official" / "bad" / "v1"
        )
        plugin_dir.mkdir(parents=True, exist_ok=True)
        (plugin_dir / ".mcp.json").write_text(json.dumps([1, 2, 3]))
        install_path = str(plugin_dir)
        installed = _write_installed_plugins(
            tmp_path,
            {"bad@official": [{"scope": "user", "installPath": install_path}]},
        )
        result = scan_claude_code_plugins(installed)
        assert result == []

    def test_empty_mcp_servers(self, tmp_path: Path):
        """Skips plugins with empty mcpServers dict."""
        install_path = _create_plugin_dir(
            tmp_path,
            "official",
            "empty",
            "v1",
            mcp_json={"mcpServers": {}},
        )
        installed = _write_installed_plugins(
            tmp_path,
            {"empty@official": [{"scope": "user", "installPath": install_path}]},
        )
        result = scan_claude_code_plugins(installed)
        assert result == []

    def test_plugin_key_without_at_sign(self, tmp_path: Path):
        """Handles plugin keys without @ (uses full key as name)."""
        install_path = _create_plugin_dir(
            tmp_path,
            "local",
            "standalone",
            "v1",
            mcp_json={"mcpServers": {"s": {"command": "echo"}}},
        )
        installed = _write_installed_plugins(
            tmp_path,
            {"standalone-plugin": [{"scope": "user", "installPath": install_path}]},
        )
        result = scan_claude_code_plugins(installed)
        assert result[0].servers[0].project_name == "standalone-plugin"


class TestRootLevelServers:
    """Plugin .mcp.json files can have servers at root level (no mcpServers wrapper)."""

    def test_servers_at_root_level(self, tmp_path: Path):
        """Real-world format: servers directly at root, no mcpServers key."""
        install_path = _create_plugin_dir(
            tmp_path,
            "claude-plugins-official",
            "context7",
            "55b58ec6e564",
            mcp_json={
                "context7": {
                    "command": "npx",
                    "args": ["-y", "@upstash/context7-mcp"],
                }
            },
        )
        installed = _write_installed_plugins(
            tmp_path,
            {
                "context7@claude-plugins-official": [
                    {"scope": "user", "installPath": install_path}
                ]
            },
        )
        result = scan_claude_code_plugins(installed)
        assert len(result) == 1
        server = result[0].servers[0]
        assert server.name == "context7"
        assert server.type == "stdio"
        assert server.command == "npx"
        assert server.args == ["-y", "@upstash/context7-mcp"]

    def test_root_level_skips_non_server_entries(self, tmp_path: Path):
        """Root-level entries that aren't server configs are ignored."""
        install_path = _create_plugin_dir(
            tmp_path,
            "official",
            "test",
            "v1",
            mcp_json={
                "my-server": {"command": "node", "args": ["server.js"]},
                "version": "1.0.0",
                "description": "not a server",
            },
        )
        installed = _write_installed_plugins(
            tmp_path,
            {"test@official": [{"scope": "user", "installPath": install_path}]},
        )
        result = scan_claude_code_plugins(installed)
        assert len(result) == 1
        assert len(result[0].servers) == 1
        assert result[0].servers[0].name == "my-server"

    def test_mcp_servers_key_takes_precedence(self, tmp_path: Path):
        """If mcpServers key exists, use it instead of root-level extraction."""
        install_path = _create_plugin_dir(
            tmp_path,
            "official",
            "test",
            "v1",
            mcp_json={
                "mcpServers": {"wrapped": {"command": "echo"}},
                "stray": {"command": "should-be-ignored"},
            },
        )
        installed = _write_installed_plugins(
            tmp_path,
            {"test@official": [{"scope": "user", "installPath": install_path}]},
        )
        result = scan_claude_code_plugins(installed)
        assert len(result) == 1
        assert len(result[0].servers) == 1
        assert result[0].servers[0].name == "wrapped"


class TestSubstitutePluginRoot:
    def test_replaces_in_string(self):
        result = _substitute_plugin_root(
            "${CLAUDE_PLUGIN_ROOT}/bin/server",
            "/home/user/.claude/plugins/cache/mp/p/v1",
        )
        assert result == "/home/user/.claude/plugins/cache/mp/p/v1/bin/server"

    def test_no_placeholder(self):
        result = _substitute_plugin_root("npx", "/some/path")
        assert result == "npx"

    def test_substitution_in_server_command_and_args(self, tmp_path: Path):
        """${CLAUDE_PLUGIN_ROOT} is substituted in command, args, and env."""
        install_path = _create_plugin_dir(
            tmp_path,
            "official",
            "db-plugin",
            "v1",
            mcp_json={
                "mcpServers": {
                    "db": {
                        "command": "${CLAUDE_PLUGIN_ROOT}/bin/db-server",
                        "args": [
                            "--config",
                            "${CLAUDE_PLUGIN_ROOT}/config.json",
                        ],
                        "env": {
                            "DB_PATH": "${CLAUDE_PLUGIN_ROOT}/data",
                        },
                    }
                }
            },
        )
        installed = _write_installed_plugins(
            tmp_path,
            {"db-plugin@official": [{"scope": "user", "installPath": install_path}]},
        )
        result = scan_claude_code_plugins(installed)
        server = result[0].servers[0]
        assert server.command == f"{install_path}/bin/db-server"
        assert server.args == ["--config", f"{install_path}/config.json"]
        assert server.env == {"DB_PATH": f"{install_path}/data"}


class TestMultipleServersInPlugin:
    def test_plugin_with_multiple_servers(self, tmp_path: Path):
        """A single plugin can define multiple MCP servers."""
        install_path = _create_plugin_dir(
            tmp_path,
            "official",
            "multi",
            "v1",
            mcp_json={
                "mcpServers": {
                    "db": {"command": "db-server"},
                    "api": {"url": "https://api.example.com/mcp"},
                }
            },
        )
        installed = _write_installed_plugins(
            tmp_path,
            {"multi@official": [{"scope": "user", "installPath": install_path}]},
        )
        result = scan_claude_code_plugins(installed)
        assert len(result) == 1
        assert len(result[0].servers) == 2
        names = {s.name for s in result[0].servers}
        assert names == {"db", "api"}
