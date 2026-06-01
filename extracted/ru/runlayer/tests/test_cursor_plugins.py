"""Tests for Cursor plugin MCP server discovery."""

import json
from pathlib import Path


from runlayer_cli.scan.clients import MCPClientDefinition, ConfigPath, PluginPath
from runlayer_cli.scan.cursor_plugins import (
    discover_plugins,
    read_project_plugin_refs,
    scan_cursor_plugins,
)


def _make_client_def(plugin_base: Path) -> MCPClientDefinition:
    """Create a Cursor client def pointing at a tmp plugin cache."""
    return MCPClientDefinition(
        name="cursor",
        display_name="Cursor",
        paths=[ConfigPath(str(plugin_base / "mcp.json"), platform="all")],
        servers_key="mcpServers",
        plugin_paths=[
            PluginPath(str(plugin_base), platform="all"),
        ],
    )


def _create_plugin(
    base: Path,
    name: str,
    commit: str = "abc123",
    mcp_servers: dict | None = None,
    mcp_filename: str = "mcp.json",
    plugin_json: dict | None = None,
) -> Path:
    """Create a plugin directory structure and return the hash dir path."""
    plugin_dir = base / name / commit
    plugin_dir.mkdir(parents=True, exist_ok=True)

    if mcp_servers is not None:
        (plugin_dir / mcp_filename).write_text(json.dumps(mcp_servers))

    if plugin_json is not None:
        manifest_dir = plugin_dir / ".cursor-plugin"
        manifest_dir.mkdir(exist_ok=True)
        (manifest_dir / "plugin.json").write_text(json.dumps(plugin_json))

    return plugin_dir


def _create_settings_json(project_path: Path, plugins: dict) -> None:
    """Create .cursor/settings.json with plugins references."""
    settings_dir = project_path / ".cursor"
    settings_dir.mkdir(parents=True, exist_ok=True)
    (settings_dir / "settings.json").write_text(json.dumps({"plugins": plugins}))


class TestDiscoverPlugins:
    def test_no_plugin_paths(self):
        """Returns empty when client has no plugin_paths."""
        client = MCPClientDefinition(name="test", display_name="Test", paths=[])
        assert discover_plugins(client) == []

    def test_nonexistent_base_dir(self, tmp_path: Path):
        """Returns empty when plugin base dir doesn't exist."""
        client = _make_client_def(tmp_path / "nonexistent")
        assert discover_plugins(client) == []

    def test_plugin_with_mcpservers_key(self, tmp_path: Path):
        """Discovers servers from mcpServers key."""
        _create_plugin(
            tmp_path,
            "my-plugin",
            mcp_servers={
                "mcpServers": {
                    "server1": {"command": "npx", "args": ["-y", "my-server"]},
                }
            },
        )
        client = _make_client_def(tmp_path)
        result = discover_plugins(client)
        assert len(result) == 1
        assert result[0].name == "my-plugin"
        assert len(result[0].servers) == 1
        assert result[0].servers[0].name == "server1"
        assert result[0].servers[0].type == "stdio"
        assert result[0].servers[0].command == "npx"

    def test_plugin_with_root_level_servers(self, tmp_path: Path):
        """Discovers servers at root level (Notion-style)."""
        _create_plugin(
            tmp_path,
            "notion-workspace",
            mcp_servers={
                "notion": {
                    "type": "http",
                    "url": "https://mcp.notion.com/mcp",
                }
            },
        )
        client = _make_client_def(tmp_path)
        result = discover_plugins(client)
        assert len(result) == 1
        assert result[0].servers[0].name == "notion"
        assert result[0].servers[0].url == "https://mcp.notion.com/mcp"
        assert result[0].servers[0].type == "http"

    def test_plugin_with_dot_mcp_json(self, tmp_path: Path):
        """Discovers servers from .mcp.json filename."""
        _create_plugin(
            tmp_path,
            "dot-mcp-plugin",
            mcp_filename=".mcp.json",
            mcp_servers={
                "mcpServers": {
                    "server": {"command": "node", "args": ["server.js"]},
                }
            },
        )
        client = _make_client_def(tmp_path)
        result = discover_plugins(client)
        assert len(result) == 1
        assert result[0].servers[0].name == "server"

    def test_plugin_without_mcp_config(self, tmp_path: Path):
        """Skips plugins without any mcp config file."""
        plugin_dir = tmp_path / "rules-only" / "abc123"
        plugin_dir.mkdir(parents=True)
        client = _make_client_def(tmp_path)
        assert discover_plugins(client) == []

    def test_plugin_with_empty_servers(self, tmp_path: Path):
        """Skips plugins with empty mcpServers."""
        _create_plugin(tmp_path, "empty", mcp_servers={"mcpServers": {}})
        client = _make_client_def(tmp_path)
        assert discover_plugins(client) == []

    def test_multiple_plugins(self, tmp_path: Path):
        """Discovers servers from multiple plugins."""
        _create_plugin(
            tmp_path,
            "plugin-a",
            mcp_servers={"mcpServers": {"a": {"command": "a-server"}}},
        )
        _create_plugin(
            tmp_path,
            "plugin-b",
            mcp_servers={"b": {"url": "https://b.example.com/mcp"}},
        )
        client = _make_client_def(tmp_path)
        result = discover_plugins(client)
        assert len(result) == 2
        names = {p.name for p in result}
        assert names == {"plugin-a", "plugin-b"}

    def test_uses_first_hash_dir(self, tmp_path: Path):
        """Only parses first hash directory per plugin."""
        _create_plugin(
            tmp_path,
            "my-plugin",
            commit="aaa111",
            mcp_servers={"mcpServers": {"v1": {"command": "v1-server"}}},
        )
        _create_plugin(
            tmp_path,
            "my-plugin",
            commit="bbb222",
            mcp_servers={"mcpServers": {"v2": {"command": "v2-server"}}},
        )
        client = _make_client_def(tmp_path)
        result = discover_plugins(client)
        assert len(result) == 1

    def test_servers_have_config_hash(self, tmp_path: Path):
        """Discovered servers have non-empty config_hash."""
        _create_plugin(
            tmp_path,
            "test",
            mcp_servers={"mcpServers": {"s": {"command": "echo"}}},
        )
        client = _make_client_def(tmp_path)
        result = discover_plugins(client)
        assert result[0].servers[0].config_hash != ""
        assert len(result[0].servers[0].config_hash) == 64

    def test_config_path_points_to_mcp_file(self, tmp_path: Path):
        """config_path points to the actual mcp.json file."""
        _create_plugin(
            tmp_path,
            "test",
            mcp_servers={"mcpServers": {"s": {"command": "echo"}}},
        )
        client = _make_client_def(tmp_path)
        result = discover_plugins(client)
        assert result[0].config_path == tmp_path / "test" / "abc123" / "mcp.json"

    def test_malformed_json_skipped(self, tmp_path: Path):
        """Plugins with invalid JSON are skipped."""
        plugin_dir = tmp_path / "bad-json" / "abc123"
        plugin_dir.mkdir(parents=True)
        (plugin_dir / "mcp.json").write_text("{invalid json")
        client = _make_client_def(tmp_path)
        assert discover_plugins(client) == []

    def test_multiple_servers_in_plugin(self, tmp_path: Path):
        """A plugin can define multiple servers."""
        _create_plugin(
            tmp_path,
            "multi",
            mcp_servers={
                "mcpServers": {
                    "db": {"command": "db-server"},
                    "api": {"url": "https://api.example.com/mcp"},
                }
            },
        )
        client = _make_client_def(tmp_path)
        result = discover_plugins(client)
        assert len(result) == 1
        assert len(result[0].servers) == 2
        names = {s.name for s in result[0].servers}
        assert names == {"db", "api"}

    def test_server_project_name_is_plugin_name(self, tmp_path: Path):
        """Server project_name is set to plugin name."""
        _create_plugin(
            tmp_path,
            "notion-workspace",
            mcp_servers={"notion": {"url": "https://mcp.notion.com/mcp"}},
        )
        client = _make_client_def(tmp_path)
        result = discover_plugins(client)
        assert result[0].servers[0].project_name == "notion-workspace"


class TestReadProjectPluginRefs:
    def test_no_settings_json(self, tmp_path: Path):
        """Returns empty when no .cursor/settings.json exists."""
        result = read_project_plugin_refs([tmp_path])
        assert result == {}

    def test_settings_without_plugins_key(self, tmp_path: Path):
        """Returns empty when settings.json has no plugins key."""
        cursor_dir = tmp_path / ".cursor"
        cursor_dir.mkdir()
        (cursor_dir / "settings.json").write_text(json.dumps({"theme": "dark"}))
        result = read_project_plugin_refs([tmp_path])
        assert result == {}

    def test_enabled_plugin_detected(self, tmp_path: Path):
        """Detects enabled plugins in settings.json."""
        _create_settings_json(tmp_path, {"slack": {"enabled": True}})
        result = read_project_plugin_refs([tmp_path])
        assert tmp_path in result
        assert "slack" in result[tmp_path]

    def test_disabled_plugin_excluded(self, tmp_path: Path):
        """Plugins with enabled=false are excluded."""
        _create_settings_json(tmp_path, {"slack": {"enabled": False}})
        result = read_project_plugin_refs([tmp_path])
        assert result == {}

    def test_enabled_defaults_to_true(self, tmp_path: Path):
        """Plugins without explicit enabled field default to enabled."""
        _create_settings_json(tmp_path, {"slack": {}})
        result = read_project_plugin_refs([tmp_path])
        assert tmp_path in result
        assert "slack" in result[tmp_path]

    def test_multiple_projects(self, tmp_path: Path):
        """Reads settings from multiple project directories."""
        proj_a = tmp_path / "project-a"
        proj_b = tmp_path / "project-b"
        proj_a.mkdir()
        proj_b.mkdir()
        _create_settings_json(proj_a, {"slack": {"enabled": True}})
        _create_settings_json(proj_b, {"notion-workspace": {"enabled": True}})
        result = read_project_plugin_refs([proj_a, proj_b])
        assert len(result) == 2
        assert "slack" in result[proj_a]
        assert "notion-workspace" in result[proj_b]

    def test_malformed_settings_skipped(self, tmp_path: Path):
        """Malformed settings.json is skipped."""
        cursor_dir = tmp_path / ".cursor"
        cursor_dir.mkdir()
        (cursor_dir / "settings.json").write_text("{bad json")
        result = read_project_plugin_refs([tmp_path])
        assert result == {}

    def test_non_dict_settings_skipped(self, tmp_path: Path):
        """Non-dict settings.json (e.g. JSON array) is skipped."""
        cursor_dir = tmp_path / ".cursor"
        cursor_dir.mkdir()
        (cursor_dir / "settings.json").write_text(json.dumps([1, 2, 3]))
        result = read_project_plugin_refs([tmp_path])
        assert result == {}


class TestScanCursorPlugins:
    def test_no_plugins(self, tmp_path: Path):
        """Returns empty when no plugins exist."""
        base = tmp_path / "plugins"
        base.mkdir()
        client = _make_client_def(base)
        assert scan_cursor_plugins(client) == []

    def test_global_scope_when_no_project_refs(self, tmp_path: Path):
        """Plugin is global when not referenced by any project."""
        base = tmp_path / "plugins"
        _create_plugin(
            base,
            "notion-workspace",
            mcp_servers={"notion": {"url": "https://mcp.notion.com/mcp"}},
        )
        client = _make_client_def(base)
        result = scan_cursor_plugins(client, project_paths=[])
        assert len(result) == 1
        assert result[0].config_scope == "global"
        assert result[0].client == "cursor"
        assert result[0].project_path is None

    def test_global_scope_when_no_project_paths_provided(self, tmp_path: Path):
        """Plugin is global when project_paths is None."""
        base = tmp_path / "plugins"
        _create_plugin(
            base,
            "notion-workspace",
            mcp_servers={"notion": {"url": "https://mcp.notion.com/mcp"}},
        )
        client = _make_client_def(base)
        result = scan_cursor_plugins(client, project_paths=None)
        assert len(result) == 1
        assert result[0].config_scope == "global"

    def test_project_scope_when_referenced(self, tmp_path: Path):
        """Plugin is project-scoped when referenced in settings.json."""
        base = tmp_path / "plugins"
        _create_plugin(
            base,
            "slack",
            mcp_servers={"mcpServers": {"slack": {"url": "https://slack.com/mcp"}}},
        )
        project = tmp_path / "my-project"
        project.mkdir()
        _create_settings_json(project, {"slack": {"enabled": True}})

        client = _make_client_def(base)
        result = scan_cursor_plugins(client, project_paths=[project])
        assert len(result) == 1
        assert result[0].config_scope == "project"
        assert result[0].project_path == str(project)

    def test_project_scope_propagates_to_servers(self, tmp_path: Path):
        """Server project_name is set to project path for project-scoped."""
        base = tmp_path / "plugins"
        _create_plugin(
            base,
            "slack",
            mcp_servers={"mcpServers": {"slack": {"url": "https://slack.com/mcp"}}},
        )
        project = tmp_path / "my-project"
        project.mkdir()
        _create_settings_json(project, {"slack": {"enabled": True}})

        client = _make_client_def(base)
        result = scan_cursor_plugins(client, project_paths=[project])
        assert result[0].servers[0].project_name == str(project)

    def test_plugin_in_multiple_projects(self, tmp_path: Path):
        """Plugin referenced by two projects emits two entries."""
        base = tmp_path / "plugins"
        _create_plugin(
            base,
            "slack",
            mcp_servers={"mcpServers": {"slack": {"url": "https://slack.com/mcp"}}},
        )
        proj_a = tmp_path / "project-a"
        proj_b = tmp_path / "project-b"
        proj_a.mkdir()
        proj_b.mkdir()
        _create_settings_json(proj_a, {"slack": {"enabled": True}})
        _create_settings_json(proj_b, {"slack": {"enabled": True}})

        client = _make_client_def(base)
        result = scan_cursor_plugins(client, project_paths=[proj_a, proj_b])
        assert len(result) == 2
        paths = {r.project_path for r in result}
        assert paths == {str(proj_a), str(proj_b)}

    def test_disabled_plugin_not_project_scoped(self, tmp_path: Path):
        """Plugin with enabled=false in settings.json stays global."""
        base = tmp_path / "plugins"
        _create_plugin(
            base,
            "slack",
            mcp_servers={"mcpServers": {"slack": {"url": "https://slack.com/mcp"}}},
        )
        project = tmp_path / "my-project"
        project.mkdir()
        _create_settings_json(project, {"slack": {"enabled": False}})

        client = _make_client_def(base)
        result = scan_cursor_plugins(client, project_paths=[project])
        assert len(result) == 1
        assert result[0].config_scope == "global"

    def test_mixed_scopes(self, tmp_path: Path):
        """One plugin project-scoped, another global."""
        base = tmp_path / "plugins"
        _create_plugin(
            base,
            "slack",
            mcp_servers={"mcpServers": {"slack": {"url": "https://slack.com/mcp"}}},
        )
        _create_plugin(
            base,
            "notion-workspace",
            mcp_servers={"notion": {"url": "https://mcp.notion.com/mcp"}},
        )
        project = tmp_path / "my-project"
        project.mkdir()
        _create_settings_json(project, {"slack": {"enabled": True}})

        client = _make_client_def(base)
        result = scan_cursor_plugins(client, project_paths=[project])
        assert len(result) == 2

        slack_config = next(c for c in result if c.servers[0].name == "slack")
        assert slack_config.config_scope == "project"
        assert slack_config.project_path == str(project)

        notion_config = next(c for c in result if c.servers[0].name == "notion")
        assert notion_config.config_scope == "global"
        assert notion_config.project_path is None

    def test_config_path_in_output(self, tmp_path: Path):
        """MCPClientConfig.config_path points to plugin's mcp.json."""
        base = tmp_path / "plugins"
        _create_plugin(
            base,
            "test-plugin",
            mcp_servers={"mcpServers": {"s": {"command": "echo"}}},
        )
        client = _make_client_def(base)
        result = scan_cursor_plugins(client)
        expected = str(base / "test-plugin" / "abc123" / "mcp.json")
        assert result[0].config_path == expected
