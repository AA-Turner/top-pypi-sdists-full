"""Tests for Claude Code plugin MCP server discovery."""

import json
from pathlib import Path, PureWindowsPath

from runlayer_cli.scan.claude_code_plugins import (
    _registry_install_dir,
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


def _create_marketplace_plugin_dir(
    tmp_path: Path,
    marketplace: str,
    collection: str,
    name: str,
    mcp_json: dict,
    manifest_name: str | None = None,
) -> Path:
    plugin_dir = (
        tmp_path
        / ".claude"
        / "plugins"
        / "marketplaces"
        / marketplace
        / collection
        / name
    )
    manifest_dir = plugin_dir / ".claude-plugin"
    manifest_dir.mkdir(parents=True)
    (manifest_dir / "plugin.json").write_text(
        json.dumps({"name": manifest_name or name})
    )
    (plugin_dir / ".mcp.json").write_text(json.dumps(mcp_json))
    return plugin_dir


def _write_marketplace_catalog(
    tmp_path: Path, marketplace: str, name: str, plugins: list[dict]
) -> None:
    """Write ``marketplaces/<marketplace>/.claude-plugin/marketplace.json``."""
    manifest_dir = (
        tmp_path
        / ".claude"
        / "plugins"
        / "marketplaces"
        / marketplace
        / ".claude-plugin"
    )
    manifest_dir.mkdir(parents=True, exist_ok=True)
    (manifest_dir / "marketplace.json").write_text(
        json.dumps({"name": name, "plugins": plugins})
    )


class TestRegistryInstallDir:
    """installed_plugins.json in a WSL home stores Linux-absolute installPaths.

    Scanned from Windows, ``Path("/home/alex/...")`` is drive-relative and never
    resolves, so registry-installed WSL plugins get skipped. They must be rebased
    onto the WSL distro's UNC root.
    """

    def test_linux_absolute_path_is_drive_relative_on_windows(self):
        """Documents the bug: a Linux installPath is not absolute on Windows."""
        assert not PureWindowsPath("/home/alex/.claude/plugins/p").is_absolute()

    def test_rebases_linux_install_path_onto_wsl_home(self):
        home = Path(R"\\wsl.localhost\Ubuntu\home\alex")

        rebased = _registry_install_dir(
            "/home/alex/.claude/plugins/cache/official/review/1.0.0", home
        )

        assert str(rebased) == (
            R"\\wsl.localhost\Ubuntu\home\alex\.claude\plugins\cache"
            R"\official\review\1.0.0"
        )

    def test_rebases_path_outside_home_onto_distro_root(self):
        """A distro-absolute path (not under the home) still resolves via UNC."""
        home = Path(R"\\wsl.localhost\Ubuntu\home\alex")

        rebased = _registry_install_dir("/opt/plugins/review", home)

        assert str(rebased) == R"\\wsl.localhost\Ubuntu\opt\plugins\review"

    def test_native_scan_returns_path_unchanged(self):
        assert _registry_install_dir("/opt/app/plugin", None) == Path("/opt/app/plugin")

    def test_non_wsl_home_returns_path_unchanged(self, tmp_path: Path):
        install = tmp_path / ".claude" / "plugins" / "review"

        assert _registry_install_dir(str(install), tmp_path) == Path(str(install))


class TestScanClaudeCodePlugins:
    def test_wsl_registry_plugin_is_discovered(self, monkeypatch, tmp_path: Path):
        """A registry entry with a Linux installPath is rebased and scanned.

        Regression for WSL homes scanned from Windows: the rebased UNC directory
        is where the plugin actually lives, so it must be located and parsed
        rather than skipped.
        """
        wsl_home = Path(R"\\wsl.localhost\Ubuntu\home\alex")
        real_dir = Path(
            _create_plugin_dir(
                tmp_path,
                "official",
                "review",
                "1.0.0",
                mcp_json={"mcpServers": {"review": {"command": "review-server"}}},
            )
        )
        linux_install_path = "/home/alex/.claude/plugins/cache/official/review/1.0.0"
        installed = _write_installed_plugins(
            tmp_path,
            {"review@official": [{"scope": "user", "installPath": linux_install_path}]},
        )

        def fake_rebase(install_path: str, home):
            assert install_path == linux_install_path
            assert home == wsl_home
            return real_dir

        monkeypatch.setattr(
            "runlayer_cli.scan.claude_code_plugins._registry_install_dir",
            fake_rebase,
        )

        result = scan_claude_code_plugins(installed, home=wsl_home)

        assert [config.config_path for config in result] == [
            str(real_dir / ".mcp.json")
        ]

    def test_home_override_rebases_registry_and_settings(self, tmp_path: Path):
        wsl_home = tmp_path / "wsl-home"
        plugin_dir = _create_marketplace_plugin_dir(
            wsl_home,
            "official",
            "plugins",
            "review",
            {"mcpServers": {"review": {"command": "review-server"}}},
        )
        settings = wsl_home / ".claude" / "settings.json"
        settings.write_text(json.dumps({"enabledPlugins": {"review@official": True}}))

        result = scan_claude_code_plugins(home=wsl_home)

        assert [config.config_path for config in result] == [
            str(plugin_dir / ".mcp.json")
        ]

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

    def test_enabled_marketplace_external_plugin_is_plugin_config(self, tmp_path: Path):
        plugin_dir = _create_marketplace_plugin_dir(
            tmp_path,
            "claude-plugins-official",
            "external_plugins",
            "linear",
            {
                "mcpServers": {
                    "linear": {
                        "command": "${CLAUDE_PLUGIN_ROOT}/bin/linear",
                    }
                }
            },
        )
        installed = _write_installed_plugins(tmp_path, {})

        result = scan_claude_code_plugins(
            installed,
            settings_override={"linear@claude-plugins-official": True},
        )

        assert len(result) == 1
        config = result[0]
        assert config.config_scope == "plugin"
        assert config.config_path == str(plugin_dir / ".mcp.json")
        assert config.project_path is None
        assert config.plugin_identifier is not None
        assert config.servers[0].command == str(plugin_dir / "bin" / "linear")

    def test_enabled_marketplace_plugin_does_not_require_registry(self, tmp_path: Path):
        plugin_dir = _create_marketplace_plugin_dir(
            tmp_path,
            "official",
            "external_plugins",
            "linear",
            {"mcpServers": {"linear": {"command": "linear-server"}}},
        )
        installed = tmp_path / ".claude" / "plugins" / "installed_plugins.json"

        result = scan_claude_code_plugins(
            installed,
            settings_override={"linear@official": True},
        )

        assert [config.config_path for config in result] == [
            str(plugin_dir / ".mcp.json")
        ]

    def test_registry_marketplace_plugin_is_not_duplicated(self, tmp_path: Path):
        plugin_dir = _create_marketplace_plugin_dir(
            tmp_path,
            "official",
            "plugins",
            "review",
            {"mcpServers": {"review": {"command": "review-server"}}},
        )
        installed = _write_installed_plugins(
            tmp_path,
            {
                "review@official": [
                    {
                        "scope": "user",
                        "installPath": str(plugin_dir),
                    }
                ]
            },
        )

        result = scan_claude_code_plugins(
            installed,
            settings_override={"review@official": True},
        )

        assert len(result) == 1
        assert result[0].config_path == str(plugin_dir / ".mcp.json")

    def test_enabled_marketplace_bundled_plugin_is_scanned(self, tmp_path: Path):
        plugin_dir = _create_marketplace_plugin_dir(
            tmp_path,
            "official",
            "plugins",
            "tunnels",
            {"mcpServers": {"tunnels": {"command": "tunnel-server"}}},
        )
        installed = _write_installed_plugins(tmp_path, {})

        result = scan_claude_code_plugins(
            installed,
            settings_override={"tunnels@official": True},
        )

        assert [config.config_path for config in result] == [
            str(plugin_dir / ".mcp.json")
        ]

    def test_marketplace_plugin_dir_differs_from_manifest_name(self, tmp_path: Path):
        """enabledPlugins key uses the manifest name, not the on-disk dir name."""
        plugin_dir = _create_marketplace_plugin_dir(
            tmp_path,
            "acme-tools",
            "plugins",
            "code-formatter",
            {"mcpServers": {"fmt": {"command": "fmt-server"}}},
            manifest_name="formatter",
        )
        installed = _write_installed_plugins(tmp_path, {})

        result = scan_claude_code_plugins(
            installed,
            settings_override={"formatter@acme-tools": True},
        )

        assert [config.config_path for config in result] == [
            str(plugin_dir / ".mcp.json")
        ]

    def test_marketplace_plugin_uses_catalog_name_over_dir_name(self, tmp_path: Path):
        """marketplace.json entry name is authoritative for the enabledPlugins key."""
        plugin_dir = _create_marketplace_plugin_dir(
            tmp_path,
            "acme-tools",
            "plugins",
            "code-formatter",
            {"mcpServers": {"fmt": {"command": "fmt-server"}}},
            manifest_name="code-formatter",
        )
        _write_marketplace_catalog(
            tmp_path,
            "acme-tools",
            "acme-tools",
            [{"name": "formatter", "source": "./plugins/code-formatter"}],
        )
        installed = _write_installed_plugins(tmp_path, {})

        result = scan_claude_code_plugins(
            installed,
            settings_override={"formatter@acme-tools": True},
        )

        assert [config.config_path for config in result] == [
            str(plugin_dir / ".mcp.json")
        ]

    def test_marketplace_plugin_project_name_uses_manifest_name(self, tmp_path: Path):
        """Bundled server project_name uses the manifest name, not the dir name."""
        _create_marketplace_plugin_dir(
            tmp_path,
            "acme-tools",
            "plugins",
            "code-formatter",
            {"mcpServers": {"fmt": {"command": "fmt-server"}}},
            manifest_name="formatter",
        )
        installed = _write_installed_plugins(tmp_path, {})

        result = scan_claude_code_plugins(
            installed,
            settings_override={"formatter@acme-tools": True},
        )

        assert len(result) == 1
        assert result[0].servers[0].project_name == "formatter"

    def test_marketplace_plugin_project_name_uses_catalog_name(self, tmp_path: Path):
        """Bundled server project_name uses the catalog entry name over the dir name."""
        _create_marketplace_plugin_dir(
            tmp_path,
            "acme-tools",
            "plugins",
            "code-formatter",
            {"mcpServers": {"fmt": {"command": "fmt-server"}}},
            manifest_name="code-formatter",
        )
        _write_marketplace_catalog(
            tmp_path,
            "acme-tools",
            "acme-tools",
            [{"name": "formatter", "source": "./plugins/code-formatter"}],
        )
        installed = _write_installed_plugins(tmp_path, {})

        result = scan_claude_code_plugins(
            installed,
            settings_override={"formatter@acme-tools": True},
        )

        assert len(result) == 1
        assert result[0].servers[0].project_name == "formatter"

    def test_marketplace_plugins_not_enabled_are_not_scanned(self, tmp_path: Path):
        _create_marketplace_plugin_dir(
            tmp_path,
            "official",
            "plugins",
            "disabled",
            {"mcpServers": {"disabled": {"command": "disabled-server"}}},
        )
        _create_marketplace_plugin_dir(
            tmp_path,
            "official",
            "external_plugins",
            "absent",
            {"mcpServers": {"absent": {"command": "absent-server"}}},
        )
        installed = _write_installed_plugins(tmp_path, {})

        result = scan_claude_code_plugins(
            installed,
            settings_override={"disabled@official": False},
        )

        assert result == []

    def test_marketplace_plugin_requires_boolean_true_in_settings(
        self, tmp_path: Path, monkeypatch
    ):
        monkeypatch.setattr(Path, "home", staticmethod(lambda: tmp_path))
        _create_marketplace_plugin_dir(
            tmp_path,
            "official",
            "external_plugins",
            "linear",
            {"mcpServers": {"linear": {"command": "linear-server"}}},
        )
        installed = _write_installed_plugins(tmp_path, {})
        settings = tmp_path / ".claude" / "settings.json"
        settings.write_text(json.dumps({"enabledPlugins": {"linear@official": "true"}}))

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
        assert server.type == "streaming-http"
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
        assert server.type == "streaming-http"

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
        assert server.type == "streaming-http"
        assert server.url == "https://example.com/mcp"

    def test_plugin_transport_streamable_http_normalized(self, tmp_path: Path):
        """Normalizes streamable_http input to streaming-http."""
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
        assert server.type == "streaming-http"
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
