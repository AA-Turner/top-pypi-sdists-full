"""Tests for Copilot CLI plugin scanner."""

import json

from runlayer_cli.scan import copilot_plugins as copilot_plugins_module
from runlayer_cli.scan.copilot_plugins import scan_copilot_plugins


class TestScanCopilotPlugins:
    def test_home_override_rebases_installed_plugins(self, tmp_path, monkeypatch):
        wsl_home = tmp_path / "wsl-home"
        plugin_dir = (
            wsl_home / ".copilot" / "installed-plugins" / "marketplace" / "review"
        )
        plugin_dir.mkdir(parents=True)
        (plugin_dir / ".mcp.json").write_text(
            json.dumps({"mcpServers": {"review": {"command": "review-server"}}})
        )
        monkeypatch.setenv("COPILOT_HOME", str(tmp_path / "other-home"))

        configs, artifacts = scan_copilot_plugins(home=wsl_home)

        assert [config.config_path for config in configs] == [str(plugin_dir)]
        assert [artifact.install_path for artifact in artifacts] == [str(plugin_dir)]

    def test_discovers_marketplace_plugin_with_mcp_json(self, tmp_path):
        """Plugin with .mcp.json at root (verified real-world layout)."""
        plugin_dir = tmp_path / "work-iq" / "workiq"
        plugin_dir.mkdir(parents=True)
        mcp_data = {
            "mcpServers": {
                "workiq": {
                    "command": "npx",
                    "args": ["-y", "@microsoft/workiq@latest", "mcp"],
                    "tools": ["*"],
                }
            }
        }
        (plugin_dir / ".mcp.json").write_text(json.dumps(mcp_data))

        configs, artifacts = scan_copilot_plugins(tmp_path)
        assert len(configs) == 1
        assert configs[0].client == "github_copilot_cli"
        assert configs[0].config_scope == "plugin"
        assert len(configs[0].servers) == 1
        assert configs[0].servers[0].name == "workiq"
        assert configs[0].servers[0].command == "npx"

        assert len(artifacts) == 1
        assert artifacts[0].plugin_type == "copilot_plugin"
        assert artifacts[0].marketplace == "work-iq"
        assert artifacts[0].has_mcp_servers is True

    def test_discovers_plugin_with_github_mcp_json(self, tmp_path):
        """Plugin with .github/mcp.json."""
        plugin_dir = tmp_path / "marketplace" / "plugin-a"
        (plugin_dir / ".github").mkdir(parents=True)
        mcp_data = {
            "mcpServers": {"server-a": {"command": "node", "args": ["server.js"]}}
        }
        (plugin_dir / ".github" / "mcp.json").write_text(json.dumps(mcp_data))

        configs, artifacts = scan_copilot_plugins(tmp_path)
        assert len(configs) == 1
        assert len(configs[0].servers) == 1
        assert configs[0].servers[0].name == "server-a"

    def test_discovers_plugin_with_inline_manifest(self, tmp_path):
        """Plugin with inline mcpServers in .github/plugin/plugin.json."""
        plugin_dir = tmp_path / "marketplace" / "inline-plugin"
        (plugin_dir / ".github" / "plugin").mkdir(parents=True)
        manifest = {
            "name": "inline-plugin",
            "version": "1.0.0",
            "mcpServers": {
                "inline-server": {"command": "python", "args": ["serve.py"]}
            },
        }
        (plugin_dir / ".github" / "plugin" / "plugin.json").write_text(
            json.dumps(manifest)
        )

        configs, artifacts = scan_copilot_plugins(tmp_path)
        assert len(configs) == 1
        assert configs[0].servers[0].name == "inline-server"

    def test_plugin_without_mcp_servers(self, tmp_path):
        """Plugin with no MCP config at all."""
        plugin_dir = tmp_path / "marketplace" / "no-mcp"
        (plugin_dir / ".github" / "plugin").mkdir(parents=True)
        manifest = {"name": "no-mcp", "version": "1.0.0"}
        (plugin_dir / ".github" / "plugin" / "plugin.json").write_text(
            json.dumps(manifest)
        )

        configs, artifacts = scan_copilot_plugins(tmp_path)
        assert configs == []
        assert len(artifacts) == 1
        assert artifacts[0].has_mcp_servers is False

    def test_discovers_direct_plugins(self, tmp_path):
        """Plugins under _direct/<source-id>/."""
        direct_dir = tmp_path / "_direct" / "my-source"
        direct_dir.mkdir(parents=True)
        mcp_data = {
            "mcpServers": {"direct-server": {"command": "cargo", "args": ["run"]}}
        }
        (direct_dir / ".mcp.json").write_text(json.dumps(mcp_data))

        configs, artifacts = scan_copilot_plugins(tmp_path)
        assert len(configs) == 1
        assert configs[0].servers[0].name == "direct-server"
        assert len(artifacts) == 1
        assert artifacts[0].marketplace == "_direct"

    def test_detects_skills_directory(self, tmp_path):
        """has_skills is True when skills/ directory exists."""
        plugin_dir = tmp_path / "marketplace" / "with-skills"
        plugin_dir.mkdir(parents=True)
        (plugin_dir / "skills" / "my-skill").mkdir(parents=True)
        (plugin_dir / "skills" / "my-skill" / "SKILL.md").write_text("# Skill")

        configs, artifacts = scan_copilot_plugins(tmp_path)
        assert len(artifacts) == 1
        assert artifacts[0].has_skills is True

    def test_empty_plugins_dir(self, tmp_path):
        configs, artifacts = scan_copilot_plugins(tmp_path)
        assert configs == []
        assert artifacts == []

    def test_missing_plugins_dir(self, tmp_path):
        nonexistent = tmp_path / "no-such-dir"
        configs, artifacts = scan_copilot_plugins(nonexistent)
        assert configs == []
        assert artifacts == []

    def test_multiple_plugins_under_marketplace(self, tmp_path):
        """Multiple plugins under a single marketplace dir."""
        for name in ("plugin-a", "plugin-b"):
            pdir = tmp_path / "my-market" / name
            pdir.mkdir(parents=True)
            mcp = {"mcpServers": {f"{name}-server": {"command": "node"}}}
            (pdir / ".mcp.json").write_text(json.dumps(mcp))

        configs, artifacts = scan_copilot_plugins(tmp_path)
        assert len(configs) == 2
        assert len(artifacts) == 2
        server_names = {c.servers[0].name for c in configs}
        assert server_names == {"plugin-a-server", "plugin-b-server"}

    def test_copilot_home_honored_on_windows(self, tmp_path, monkeypatch):
        """$COPILOT_HOME must override USERPROFILE on Windows."""
        copilot_home = tmp_path / "custom-copilot"
        plugins_base = copilot_home / "installed-plugins"
        plugin_dir = plugins_base / "market" / "p"
        plugin_dir.mkdir(parents=True)
        (plugin_dir / ".mcp.json").write_text(
            json.dumps({"mcpServers": {"s": {"command": "node"}}})
        )

        userprofile = tmp_path / "userprofile"
        (userprofile / ".copilot" / "installed-plugins").mkdir(parents=True)

        monkeypatch.setattr(
            copilot_plugins_module.platform, "system", lambda: "Windows"
        )
        monkeypatch.setenv("COPILOT_HOME", str(copilot_home))
        monkeypatch.setenv("USERPROFILE", str(userprofile))

        configs, artifacts = scan_copilot_plugins()
        assert len(configs) == 1
        assert configs[0].servers[0].name == "s"
        assert str(plugins_base) in configs[0].config_path

    def test_copilot_home_honored_on_macos(self, tmp_path, monkeypatch):
        """$COPILOT_HOME must override ~/.copilot on macOS/Linux."""
        copilot_home = tmp_path / "custom-copilot"
        plugins_base = copilot_home / "installed-plugins"
        plugin_dir = plugins_base / "market" / "p"
        plugin_dir.mkdir(parents=True)
        (plugin_dir / ".mcp.json").write_text(
            json.dumps({"mcpServers": {"s": {"command": "node"}}})
        )

        monkeypatch.setattr(copilot_plugins_module.platform, "system", lambda: "Darwin")
        monkeypatch.setenv("COPILOT_HOME", str(copilot_home))

        configs, _ = scan_copilot_plugins()
        assert len(configs) == 1
        assert configs[0].servers[0].name == "s"

    def test_mcp_json_takes_precedence_over_manifest(self, tmp_path):
        """.mcp.json should be preferred over inline mcpServers in manifest."""
        plugin_dir = tmp_path / "market" / "precedence"
        (plugin_dir / ".github" / "plugin").mkdir(parents=True)
        mcp_data = {"mcpServers": {"from-mcp-json": {"command": "a"}}}
        (plugin_dir / ".mcp.json").write_text(json.dumps(mcp_data))
        manifest = {"mcpServers": {"from-manifest": {"command": "b"}}}
        (plugin_dir / ".github" / "plugin" / "plugin.json").write_text(
            json.dumps(manifest)
        )

        configs, _ = scan_copilot_plugins(tmp_path)
        assert len(configs) == 1
        assert configs[0].servers[0].name == "from-mcp-json"

    def test_skips_non_plugin_directory_under_marketplace(self, tmp_path):
        """Dirs without a plugin marker (e.g. .git) are not reported as plugins."""
        real_plugin = tmp_path / "my-market" / "real-plugin"
        real_plugin.mkdir(parents=True)
        (real_plugin / ".mcp.json").write_text(
            json.dumps({"mcpServers": {"s": {"command": "node"}}})
        )

        junk_dir = tmp_path / "my-market" / ".git"
        (junk_dir / "hooks").mkdir(parents=True)
        (junk_dir / "config").write_text("[core]\n")
        (junk_dir / "HEAD").write_text("ref: refs/heads/main\n")

        configs, artifacts = scan_copilot_plugins(tmp_path)

        artifact_names = {a.name for a in artifacts}
        assert ".git" not in artifact_names
        assert len(artifacts) == 1
        assert artifacts[0].name == "real-plugin"
        assert len(configs) == 1

    def test_skips_direct_source_with_only_marketplace_manifest(self, tmp_path):
        """A _direct source with only marketplace.json is not a plugin."""
        marketplace_only = tmp_path / "_direct" / "some-marketplace"
        marketplace_only.mkdir(parents=True)
        (marketplace_only / "marketplace.json").write_text(
            json.dumps({"name": "some-marketplace", "plugins": []})
        )

        configs, artifacts = scan_copilot_plugins(tmp_path)
        assert configs == []
        assert artifacts == []
