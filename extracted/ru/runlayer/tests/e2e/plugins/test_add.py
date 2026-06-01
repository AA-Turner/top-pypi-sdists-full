"""E2E tests for plugins add / list / update / remove lifecycle."""

import contextlib
import json

import yaml

from runlayer_cli.api import PluginServerRef
from runlayer_cli.main import app
from tests.e2e.conftest import strip_ansi


def test_plugins_add_by_namespace(
    runner, cli_args, tmp_path, monkeypatch, create_e2e_plugin
):
    """plugins add ORG/REPO installs native plugin files."""
    monkeypatch.chdir(tmp_path)
    plugin = create_e2e_plugin()

    result = runner.invoke(
        app,
        [
            *cli_args,
            "plugins",
            "add",
            plugin.namespace,
            "--plugin",
            plugin.name,
            "--client",
            "claude_code",
        ],
    )
    output = strip_ansi(result.output)
    assert result.exit_code == 0, output
    assert "1 installed" in output

    # .agents/plugins/<name>/.claude-plugin/plugin.json
    manifest = (
        tmp_path
        / ".agents"
        / "plugins"
        / plugin.name
        / ".claude-plugin"
        / "plugin.json"
    )
    assert manifest.exists()
    data = json.loads(manifest.read_text())
    assert data["name"] == plugin.name
    assert data["description"] == plugin.description
    assert data["version"] == "1.0.0"
    assert "id" not in data
    assert "namespace" not in data
    server_entry = plugin.servers[0]
    server_id = server_entry.get("server_id") or server_entry.get("id")
    assert server_id
    manifest_server_value = next(iter(data["mcpServers"].values()))
    assert f"proxy/{server_id}/mcp" in manifest_server_value["url"]
    assert manifest_server_value.get("type") == "http"

    # .agents/plugins/<name>/.mcp.json
    mcp_json = tmp_path / ".agents" / "plugins" / plugin.name / ".mcp.json"
    assert mcp_json.exists()
    mcp = json.loads(mcp_json.read_text())
    assert "mcpServers" in mcp
    server_value = next(iter(mcp["mcpServers"].values()))
    server_url = server_value["url"]
    assert f"proxy/{server_id}/mcp" in server_url
    assert server_value.get("type") == "http"

    # .agents/plugins/<name>/.installed marker
    installed = tmp_path / ".agents" / "plugins" / plugin.name / ".installed"
    assert installed.exists()

    # .claude/plugins/<name> symlink
    symlink = tmp_path / ".claude" / "plugins" / plugin.name
    assert symlink.is_symlink()

    # .runlayer/plugin-lock.yml
    lockfile = tmp_path / ".runlayer" / "plugin-lock.yml"
    assert lockfile.exists()
    lock = yaml.safe_load(lockfile.read_text())
    entries = lock["plugins"]
    match = [e for e in entries if e["id"] == plugin.id]
    assert len(match) == 1
    assert match[0]["install_mode"] == "native"
    assert match[0]["client"] == "claude_code"


def test_plugins_add_uses_api_install_name(
    runner, cli_args, tmp_path, monkeypatch, create_e2e_plugin
):
    """Native installs use backend install_name, not display name, for files."""
    monkeypatch.chdir(tmp_path)
    plugin = create_e2e_plugin(plugin_name="Plugin With Spaces")
    assert plugin.install_name is not None
    assert plugin.install_name != plugin.name

    result = runner.invoke(
        app,
        [
            *cli_args,
            "plugins",
            "add",
            plugin.namespace,
            "--plugin",
            plugin.name,
            "--client",
            "claude_code",
        ],
    )
    output = strip_ansi(result.output)
    assert result.exit_code == 0, output

    canonical = tmp_path / ".agents" / "plugins" / plugin.install_name
    assert (canonical / ".installed").exists()
    assert not (tmp_path / ".agents" / "plugins" / plugin.name).exists()

    manifest = json.loads((canonical / ".claude-plugin" / "plugin.json").read_text())
    assert manifest["name"] == plugin.install_name

    symlink = tmp_path / ".claude" / "plugins" / plugin.install_name
    assert symlink.is_symlink()
    assert not (tmp_path / ".claude" / "plugins" / plugin.name).exists()

    lockfile = tmp_path / ".runlayer" / "plugin-lock.yml"
    lock = yaml.safe_load(lockfile.read_text())
    match = [e for e in lock["plugins"] if e["id"] == plugin.id]
    assert len(match) == 1
    assert match[0]["name"] == plugin.name
    assert match[0]["install_name"] == plugin.install_name


def test_plugins_list_shows_installed(
    runner, cli_args, tmp_path, monkeypatch, create_e2e_plugin
):
    """After add, plugins list shows the plugin."""
    monkeypatch.chdir(tmp_path)
    plugin = create_e2e_plugin()

    runner.invoke(
        app,
        [
            *cli_args,
            "plugins",
            "add",
            plugin.namespace,
            "--plugin",
            plugin.name,
            "--client",
            "claude_code",
        ],
    )

    list_result = runner.invoke(
        app,
        ["plugins", "list", "--client", "claude_code"],
    )
    output = strip_ansi(list_result.output)
    assert list_result.exit_code == 0, output
    assert plugin.name in output
    assert "1 plugin(s) installed" in output


def test_plugins_list_defaults_to_all_clients_in_project_scope(
    runner, cli_args, tmp_path, monkeypatch, create_e2e_plugin
):
    """Plain plugins list shows one project-scoped row across installed clients."""
    monkeypatch.chdir(tmp_path)
    plugin = create_e2e_plugin()

    for client_name in ("claude_code", "cursor"):
        result = runner.invoke(
            app,
            [
                *cli_args,
                "plugins",
                "add",
                plugin.namespace,
                "--plugin",
                plugin.name,
                "--client",
                client_name,
            ],
        )
        output = strip_ansi(result.output)
        assert result.exit_code == 0, output

    list_result = runner.invoke(app, ["plugins", "list"])
    output = strip_ansi(list_result.output)
    assert list_result.exit_code == 0, output
    assert output.count(plugin.name) == 1
    assert "claude_code" in output
    assert "cursor" in output
    assert "1 plugin(s) installed" in output


def test_plugins_list_filters_project_scope_by_client(
    runner, cli_args, tmp_path, monkeypatch, create_e2e_plugin
):
    """Client filter narrows the project-scoped list output."""
    monkeypatch.chdir(tmp_path)
    plugin = create_e2e_plugin()

    for client_name in ("claude_code", "cursor"):
        result = runner.invoke(
            app,
            [
                *cli_args,
                "plugins",
                "add",
                plugin.namespace,
                "--plugin",
                plugin.name,
                "--client",
                client_name,
            ],
        )
        output = strip_ansi(result.output)
        assert result.exit_code == 0, output

    list_result = runner.invoke(app, ["plugins", "list", "--client", "claude_code"])
    output = strip_ansi(list_result.output)
    assert list_result.exit_code == 0, output
    assert plugin.name in output
    assert "claude_code" in output
    assert "cursor" not in output
    assert "1 plugin(s) installed" in output


def test_plugins_list_global_scope_is_separate_from_project(
    runner, cli_args, tmp_path, monkeypatch, create_e2e_plugin
):
    """Global installs appear only in --global list output."""
    home_dir = tmp_path / "home"
    project_dir = tmp_path / "project"
    home_dir.mkdir()
    project_dir.mkdir()
    monkeypatch.setenv("HOME", str(home_dir))
    monkeypatch.chdir(project_dir)
    plugin = create_e2e_plugin()

    add_result = runner.invoke(
        app,
        [
            *cli_args,
            "plugins",
            "add",
            plugin.namespace,
            "--plugin",
            plugin.name,
            "--global",
        ],
    )
    add_output = strip_ansi(add_result.output)
    assert add_result.exit_code == 0, add_output

    project_list = runner.invoke(app, ["plugins", "list"])
    project_output = strip_ansi(project_list.output)
    assert project_list.exit_code == 0, project_output
    assert "No plugins installed in project scope." in project_output

    global_list = runner.invoke(app, ["plugins", "list", "--global"])
    global_output = strip_ansi(global_list.output)
    assert global_list.exit_code == 0, global_output
    assert plugin.name in global_output
    assert "1 plugin(s) installed" in global_output


def test_plugins_add_claude_code_global_registers_marketplace_cache_and_skills(
    runner,
    cli_args,
    tmp_path,
    monkeypatch,
    unique_id,
    api_client,
    create_e2e_server,
):
    """Claude Code global install matches Claude's marketplace/cache model."""
    home_dir = tmp_path / "home"
    project_dir = tmp_path / "project"
    home_dir.mkdir()
    project_dir.mkdir()
    monkeypatch.setenv("HOME", str(home_dir))
    monkeypatch.chdir(project_dir)

    namespace = f"e2e-claude-code/{unique_id}"
    server = create_e2e_server(
        {
            "name": "plug-Marketing Plugin",
            "url": "npx",
            "transport_type": "stdio",
            "transport_config": {"args": ["-y", "mcp-echo-server"]},
        }
    )
    skill = api_client.create_skill(
        name="Sales Research Playbook",
        description="Sales research workflow",
        namespace=namespace,
        path="marketing/sales-research-playbook",
    )
    plugin = api_client.create_plugin(
        name=f"e2e-{unique_id}-Marketing Plugin",
        namespace=namespace,
        path="marketing-plugin",
        description=None,
        is_public=False,
        use_dynamic_tools=False,
        servers=[PluginServerRef(server_id=server.id)],
        skill_ids=[skill.id],
    )
    plugin_slug = plugin.name.lower().replace(" ", "-")

    try:
        result = runner.invoke(
            app,
            [
                *cli_args,
                "plugins",
                "add",
                plugin.id,
                "--client",
                "claude_code",
                "--global",
            ],
        )
        output = strip_ansi(result.output)
        assert result.exit_code == 0, output

        canonical = home_dir / ".agents" / "plugins" / plugin_slug
        cache = (
            home_dir
            / ".claude"
            / "plugins"
            / "cache"
            / "runlayer"
            / plugin_slug
            / "1.0.0"
        )
        assert (canonical / ".installed").exists()
        assert (cache / ".installed").exists()

        manifest = json.loads(
            (canonical / ".claude-plugin" / "plugin.json").read_text()
        )
        assert manifest["name"] == plugin_slug
        assert manifest["description"] == f"Runlayer plugin for {plugin.name}"
        assert manifest["version"] == "1.0.0"
        assert manifest["keywords"] == ["runlayer", "mcp"]
        manifest_server_value = next(iter(manifest["mcpServers"].values()))
        assert f"proxy/{server.id}/mcp" in manifest_server_value["url"]
        assert manifest_server_value.get("type") == "http"

        mcp = json.loads((cache / ".mcp.json").read_text())
        assert "mcpServers" in mcp
        server_value = next(iter(mcp["mcpServers"].values()))
        assert f"proxy/{server.id}/mcp" in server_value["url"]
        assert server_value.get("type") == "http"

        skill_file = cache / "skills" / "sales-research-playbook" / "SKILL.md"
        assert skill_file.exists()
        skill_content = skill_file.read_text()
        assert skill_content.startswith("---\nname: sales-research-playbook\n")
        assert "description: Runlayer plugin skill." in skill_content

        known = json.loads(
            (home_dir / ".claude" / "plugins" / "known_marketplaces.json").read_text()
        )
        assert known["runlayer"]["source"] == {
            "source": "directory",
            "path": str(home_dir / ".claude" / "plugins" / "marketplaces" / "runlayer"),
        }

        marketplace = json.loads(
            (
                home_dir
                / ".claude"
                / "plugins"
                / "marketplaces"
                / "runlayer"
                / ".claude-plugin"
                / "marketplace.json"
            ).read_text()
        )
        match = [p for p in marketplace["plugins"] if p["name"] == plugin_slug]
        assert match == [
            {
                "name": plugin_slug,
                "description": f"Runlayer plugin for {plugin.name}",
                "source": f"./plugins/{plugin_slug}",
                "category": "productivity",
            }
        ]

        installed = json.loads(
            (home_dir / ".claude" / "plugins" / "installed_plugins.json").read_text()
        )
        assert installed["plugins"][f"{plugin_slug}@runlayer"][0]["installPath"] == str(
            cache
        )

        settings = json.loads((home_dir / ".claude" / "settings.json").read_text())
        assert settings["enabledPlugins"][f"{plugin_slug}@runlayer"] is True

        lock = yaml.safe_load((home_dir / ".runlayer" / "plugin-lock.yml").read_text())
        match = [e for e in lock["plugins"] if e["id"] == plugin.id]
        assert len(match) == 1
        assert match[0]["install_name"] == plugin_slug
        assert match[0]["client"] == "claude_code"
    finally:
        with contextlib.suppress(Exception):
            api_client.delete_plugin(plugin.id)
        with contextlib.suppress(Exception):
            api_client.delete_skill(skill.id)


def test_plugins_update_refreshes(
    runner, cli_args, tmp_path, monkeypatch, create_e2e_plugin
):
    """After add, plugins update reports up-to-date."""
    monkeypatch.chdir(tmp_path)
    plugin = create_e2e_plugin()

    runner.invoke(
        app,
        [
            *cli_args,
            "plugins",
            "add",
            plugin.namespace,
            "--plugin",
            plugin.name,
            "--client",
            "claude_code",
        ],
    )

    update_result = runner.invoke(
        app,
        [
            *cli_args,
            "plugins",
            "update",
            "--client",
            "claude_code",
        ],
    )
    output = strip_ansi(update_result.output)
    assert update_result.exit_code == 0, output
    assert "up to date" in output.lower()


def test_plugins_add_codex_writes_marketplace_native_files(
    runner, cli_args, tmp_path, monkeypatch, create_e2e_plugin
):
    """plugins add --client codex writes Codex manifest + marketplace entry."""
    monkeypatch.chdir(tmp_path)
    plugin = create_e2e_plugin()

    result = runner.invoke(
        app,
        [
            *cli_args,
            "plugins",
            "add",
            plugin.namespace,
            "--plugin",
            plugin.name,
            "--client",
            "codex",
        ],
    )
    output = strip_ansi(result.output)
    assert result.exit_code == 0, output
    assert "1 installed" in output

    manifest = (
        tmp_path / ".agents" / "plugins" / plugin.name / ".codex-plugin" / "plugin.json"
    )
    assert manifest.exists()
    data = json.loads(manifest.read_text())
    assert data["name"] == plugin.name
    assert data["mcpServers"] == "./.mcp.json"

    mcp_json = tmp_path / ".agents" / "plugins" / plugin.name / ".mcp.json"
    assert mcp_json.exists()
    mcp = json.loads(mcp_json.read_text())
    assert "mcpServers" not in mcp
    assert "mcp_servers" in mcp
    for srv in mcp["mcp_servers"].values():
        assert "url" in srv
        assert "type" not in srv

    marketplace = tmp_path / ".agents" / "plugins" / "marketplace.json"
    assert marketplace.exists()
    marketplace_data = json.loads(marketplace.read_text())
    match = [p for p in marketplace_data["plugins"] if p["name"] == plugin.name]
    assert len(match) == 1
    assert match[0]["source"]["path"] == f"./.agents/plugins/{plugin.name}"

    installed = tmp_path / ".agents" / "plugins" / plugin.name / ".installed"
    assert installed.exists()
    assert not (tmp_path / ".codex" / "plugins" / plugin.name).exists()

    lockfile = tmp_path / ".runlayer" / "plugin-lock.yml"
    lock = yaml.safe_load(lockfile.read_text())
    match = [e for e in lock["plugins"] if e["id"] == plugin.id]
    assert len(match) == 1
    assert match[0]["install_mode"] == "native_codex_marketplace"
    assert match[0]["client"] == "codex"


def test_plugins_add_codex_global_writes_home_marketplace(
    runner, cli_args, tmp_path, monkeypatch, create_e2e_plugin
):
    """plugins add --client codex --global writes the home marketplace file."""
    home_dir = tmp_path / "home"
    project_dir = tmp_path / "project"
    home_dir.mkdir()
    project_dir.mkdir()
    monkeypatch.setenv("HOME", str(home_dir))
    monkeypatch.chdir(project_dir)
    plugin = create_e2e_plugin()

    result = runner.invoke(
        app,
        [
            *cli_args,
            "plugins",
            "add",
            plugin.namespace,
            "--plugin",
            plugin.name,
            "--client",
            "codex",
            "--global",
        ],
    )
    output = strip_ansi(result.output)
    assert result.exit_code == 0, output

    marketplace = home_dir / ".agents" / "plugins" / "marketplace.json"
    assert marketplace.exists()
    marketplace_data = json.loads(marketplace.read_text())
    match = [p for p in marketplace_data["plugins"] if p["name"] == plugin.name]
    assert len(match) == 1
    assert match[0]["source"]["path"] == f"./.agents/plugins/{plugin.name}"

    manifest = (
        home_dir / ".agents" / "plugins" / plugin.name / ".codex-plugin" / "plugin.json"
    )
    assert manifest.exists()


def test_plugins_add_codex_normalizes_spaced_plugin_name(
    runner, cli_args, tmp_path, monkeypatch, create_e2e_plugin
):
    """Codex installs use normalized plugin names for paths and manifest."""
    monkeypatch.chdir(tmp_path)
    plugin = create_e2e_plugin(plugin_name="plugin with spaces")
    normalized_name = plugin.name.lower().replace(" ", "-")

    result = runner.invoke(
        app,
        [
            *cli_args,
            "plugins",
            "add",
            plugin.namespace,
            "--plugin",
            plugin.name,
            "--client",
            "codex",
        ],
    )
    output = strip_ansi(result.output)
    assert result.exit_code == 0, output

    manifest = (
        tmp_path
        / ".agents"
        / "plugins"
        / normalized_name
        / ".codex-plugin"
        / "plugin.json"
    )
    assert manifest.exists()
    data = json.loads(manifest.read_text())
    assert data["name"] == normalized_name
    assert data["interface"] == {"displayName": plugin.name}

    marketplace = tmp_path / ".agents" / "plugins" / "marketplace.json"
    marketplace_data = json.loads(marketplace.read_text())
    match = [p for p in marketplace_data["plugins"] if p["name"] == normalized_name]
    assert len(match) == 1
    assert match[0]["source"]["path"] == f"./.agents/plugins/{normalized_name}"

    remove_result = runner.invoke(
        app,
        ["plugins", "remove", plugin.name, "--client", "codex"],
    )
    remove_output = strip_ansi(remove_result.output)
    assert remove_result.exit_code == 0, remove_output
    assert f"Removed: {plugin.name}" in remove_output
    assert not (tmp_path / ".agents" / "plugins" / normalized_name).exists()


def test_plugins_remove_cleans_up(
    runner, cli_args, tmp_path, monkeypatch, create_e2e_plugin
):
    """plugins remove NAME removes files, symlink, lockfile entry."""
    monkeypatch.chdir(tmp_path)
    plugin = create_e2e_plugin()

    runner.invoke(
        app,
        [
            *cli_args,
            "plugins",
            "add",
            plugin.namespace,
            "--plugin",
            plugin.name,
            "--client",
            "claude_code",
        ],
    )

    # Verify installed first
    assert (tmp_path / ".agents" / "plugins" / plugin.name / ".installed").exists()

    remove_result = runner.invoke(
        app,
        ["plugins", "remove", plugin.name, "--client", "claude_code"],
    )
    output = strip_ansi(remove_result.output)
    assert remove_result.exit_code == 0, output
    assert f"Removed: {plugin.name}" in output

    # Files gone
    assert not (tmp_path / ".agents" / "plugins" / plugin.name).exists()
    assert not (tmp_path / ".claude" / "plugins" / plugin.name).exists()

    # Lockfile updated
    lockfile = tmp_path / ".runlayer" / "plugin-lock.yml"
    lock = yaml.safe_load(lockfile.read_text())
    ids = [e["id"] for e in lock.get("plugins", [])]
    assert plugin.id not in ids


def test_plugins_remove_by_uuid_cleans_up(
    runner, cli_args, tmp_path, monkeypatch, create_e2e_plugin
):
    """plugins remove UUID removes files, symlink, lockfile entry."""
    monkeypatch.chdir(tmp_path)
    plugin = create_e2e_plugin()

    runner.invoke(
        app,
        [
            *cli_args,
            "plugins",
            "add",
            plugin.id,
            "--client",
            "claude_code",
        ],
    )

    assert (tmp_path / ".agents" / "plugins" / plugin.name / ".installed").exists()

    remove_result = runner.invoke(
        app,
        ["plugins", "remove", plugin.id, "--client", "claude_code"],
    )
    output = strip_ansi(remove_result.output)
    assert remove_result.exit_code == 0, output
    assert f"Removed: {plugin.name}" in output

    assert not (tmp_path / ".agents" / "plugins" / plugin.name).exists()
    assert not (tmp_path / ".claude" / "plugins" / plugin.name).exists()

    lockfile = tmp_path / ".runlayer" / "plugin-lock.yml"
    lock = yaml.safe_load(lockfile.read_text())
    ids = [e["id"] for e in lock.get("plugins", [])]
    assert plugin.id not in ids


def test_plugins_add_dry_run(
    runner, cli_args, tmp_path, monkeypatch, create_e2e_plugin
):
    """plugins add --dry-run reports 'would install' but writes nothing."""
    monkeypatch.chdir(tmp_path)
    plugin = create_e2e_plugin()

    result = runner.invoke(
        app,
        [
            *cli_args,
            "plugins",
            "add",
            plugin.namespace,
            "--plugin",
            plugin.name,
            "--client",
            "claude_code",
            "--dry-run",
        ],
    )
    output = strip_ansi(result.output)
    assert result.exit_code == 0, output
    assert "would install" in output

    # Nothing written
    assert not (tmp_path / ".agents" / "plugins" / plugin.name).exists()
    assert not (tmp_path / ".runlayer" / "plugin-lock.yml").exists()


def test_plugins_add_already_installed_skips(
    runner, cli_args, tmp_path, monkeypatch, create_e2e_plugin
):
    """Second plugins add skips already-installed plugin."""
    monkeypatch.chdir(tmp_path)
    plugin = create_e2e_plugin()

    add_args = [
        *cli_args,
        "plugins",
        "add",
        plugin.namespace,
        "--plugin",
        plugin.name,
        "--client",
        "claude_code",
    ]
    runner.invoke(app, add_args)

    second = runner.invoke(app, add_args)
    output = strip_ansi(second.output)
    assert second.exit_code == 0, output
    assert "1 skipped" in output


def test_plugins_remove_all(runner, cli_args, tmp_path, monkeypatch, create_e2e_plugin):
    """plugins remove --all --yes removes everything."""
    monkeypatch.chdir(tmp_path)
    plugin = create_e2e_plugin()

    runner.invoke(
        app,
        [
            *cli_args,
            "plugins",
            "add",
            plugin.namespace,
            "--plugin",
            plugin.name,
            "--client",
            "claude_code",
        ],
    )

    remove_result = runner.invoke(
        app,
        ["plugins", "remove", "--all", "--yes", "--client", "claude_code"],
    )
    output = strip_ansi(remove_result.output)
    assert remove_result.exit_code == 0, output
    assert "1 removed" in output

    # Files gone
    assert not (tmp_path / ".agents" / "plugins" / plugin.name).exists()


def test_plugins_remove_global_by_uuid_cleans_up(
    runner, cli_args, tmp_path, monkeypatch, create_e2e_plugin
):
    """plugins remove UUID --global removes only global install."""
    home_dir = tmp_path / "home"
    project_dir = tmp_path / "project"
    home_dir.mkdir()
    project_dir.mkdir()
    monkeypatch.setenv("HOME", str(home_dir))
    monkeypatch.chdir(project_dir)
    plugin = create_e2e_plugin()

    add_result = runner.invoke(
        app,
        [
            *cli_args,
            "plugins",
            "add",
            plugin.id,
            "--client",
            "claude_code",
            "--global",
        ],
    )
    add_output = strip_ansi(add_result.output)
    assert add_result.exit_code == 0, add_output

    assert (home_dir / ".agents" / "plugins" / plugin.name / ".installed").exists()

    remove_result = runner.invoke(
        app,
        [
            "plugins",
            "remove",
            plugin.id,
            "--client",
            "claude_code",
            "--global",
        ],
    )
    output = strip_ansi(remove_result.output)
    assert remove_result.exit_code == 0, output
    assert f"Removed: {plugin.name}" in output

    assert not (home_dir / ".agents" / "plugins" / plugin.name).exists()
    assert not (home_dir / ".claude" / "plugins" / plugin.name).exists()
    assert not (project_dir / ".agents" / "plugins" / plugin.name).exists()
    assert not (project_dir / ".claude" / "plugins" / plugin.name).exists()

    lockfile = home_dir / ".runlayer" / "plugin-lock.yml"
    lock = yaml.safe_load(lockfile.read_text())
    ids = [e["id"] for e in lock.get("plugins", [])]
    assert plugin.id not in ids


def test_plugins_add_vscode_native(
    runner, cli_args, tmp_path, monkeypatch, create_e2e_plugin
):
    """plugins add --client vscode installs native plugin with 'mcpServers' key."""
    monkeypatch.chdir(tmp_path)
    plugin = create_e2e_plugin()

    result = runner.invoke(
        app,
        [
            *cli_args,
            "plugins",
            "add",
            plugin.namespace,
            "--plugin",
            plugin.name,
            "--client",
            "vscode",
        ],
    )
    output = strip_ansi(result.output)
    assert result.exit_code == 0, output
    assert "1 installed" in output

    # .agents/plugins/<name>/.vscode-plugin/plugin.json
    manifest = (
        tmp_path
        / ".agents"
        / "plugins"
        / plugin.name
        / ".vscode-plugin"
        / "plugin.json"
    )
    assert manifest.exists()
    data = json.loads(manifest.read_text())
    assert data["id"] == plugin.id
    assert data["name"] == plugin.name

    # .agents/plugins/<name>/.mcp.json uses "mcpServers" key with type:http
    mcp_json = tmp_path / ".agents" / "plugins" / plugin.name / ".mcp.json"
    assert mcp_json.exists()
    mcp = json.loads(mcp_json.read_text())
    assert "mcpServers" in mcp
    assert "servers" not in mcp
    for srv_entry in mcp["mcpServers"].values():
        assert srv_entry.get("type") == "http"

    # .vscode/plugins/<name> symlink
    symlink = tmp_path / ".vscode" / "plugins" / plugin.name
    assert symlink.is_symlink()

    # .runlayer/plugin-lock.yml
    lockfile = tmp_path / ".runlayer" / "plugin-lock.yml"
    assert lockfile.exists()
    lock = yaml.safe_load(lockfile.read_text())
    match = [e for e in lock["plugins"] if e["id"] == plugin.id]
    assert len(match) == 1
    assert match[0]["install_mode"] == "native"
    assert match[0]["client"] == "vscode"


def test_plugins_update_vscode_preserves_mcpservers_key(
    runner, cli_args, tmp_path, monkeypatch, create_e2e_plugin
):
    """After add --client vscode, update preserves 'mcpServers' key in .mcp.json."""
    monkeypatch.chdir(tmp_path)
    plugin = create_e2e_plugin()

    runner.invoke(
        app,
        [
            *cli_args,
            "plugins",
            "add",
            plugin.namespace,
            "--plugin",
            plugin.name,
            "--client",
            "vscode",
        ],
    )

    update_result = runner.invoke(
        app,
        [
            *cli_args,
            "plugins",
            "update",
            "--client",
            "vscode",
        ],
    )
    output = strip_ansi(update_result.output)
    assert update_result.exit_code == 0, output

    # .mcp.json still uses "mcpServers" key after update
    mcp_json = tmp_path / ".agents" / "plugins" / plugin.name / ".mcp.json"
    assert mcp_json.exists()
    mcp = json.loads(mcp_json.read_text())
    assert "mcpServers" in mcp
    assert "servers" not in mcp


def test_plugins_add_codex_with_skills_injects_frontmatter(
    runner,
    cli_args,
    tmp_path,
    monkeypatch,
    unique_id,
    api_client,
    create_e2e_server,
):
    """Codex install rewrites SKILL.md with YAML frontmatter."""
    monkeypatch.chdir(tmp_path)

    namespace = f"e2e-codex-skills/{unique_id}"
    server = create_e2e_server(
        {
            "name": "plug-Codex Skill Plugin",
            "url": "npx",
            "transport_type": "stdio",
            "transport_config": {"args": ["-y", "mcp-echo-server"]},
        }
    )
    skill = api_client.create_skill(
        name="Codex Test Skill",
        description="Test skill for codex frontmatter",
        namespace=namespace,
        path="codex/test-skill",
    )
    plugin = api_client.create_plugin(
        name=f"e2e-{unique_id}-Codex Skill Plugin",
        namespace=namespace,
        path="codex-skill-plugin",
        description=None,
        is_public=False,
        use_dynamic_tools=False,
        servers=[PluginServerRef(server_id=server.id)],
        skill_ids=[skill.id],
    )
    plugin_slug = plugin.name.lower().replace(" ", "-")

    try:
        result = runner.invoke(
            app,
            [
                *cli_args,
                "plugins",
                "add",
                plugin.id,
                "--client",
                "codex",
            ],
        )
        output = strip_ansi(result.output)
        assert result.exit_code == 0, output

        plugin_dir = tmp_path / ".agents" / "plugins" / plugin_slug

        mcp = json.loads((plugin_dir / ".mcp.json").read_text())
        assert "mcpServers" not in mcp
        assert "mcp_servers" in mcp
        for srv in mcp["mcp_servers"].values():
            assert "url" in srv
            assert "type" not in srv

        skill_file = plugin_dir / "skills" / "codex-test-skill" / "SKILL.md"
        assert skill_file.exists()
        skill_content = skill_file.read_text()
        assert skill_content.startswith("---\n")
        assert "name:" in skill_content
    finally:
        with contextlib.suppress(Exception):
            api_client.delete_plugin(plugin.id)
        with contextlib.suppress(Exception):
            api_client.delete_skill(skill.id)


def test_plugins_add_cursor_mcp_json_structure(
    runner, cli_args, tmp_path, monkeypatch, create_e2e_plugin
):
    """Cursor plugin add writes mcpServers key with no type on entries."""
    monkeypatch.chdir(tmp_path)
    plugin = create_e2e_plugin()

    result = runner.invoke(
        app,
        [
            *cli_args,
            "plugins",
            "add",
            plugin.namespace,
            "--plugin",
            plugin.name,
            "--client",
            "cursor",
        ],
    )
    output = strip_ansi(result.output)
    assert result.exit_code == 0, output

    plugin_dir = tmp_path / ".agents" / "plugins" / plugin.name

    assert (plugin_dir / ".cursor-plugin" / "plugin.json").exists()
    assert (plugin_dir / ".mcp.json").exists()

    mcp = json.loads((plugin_dir / ".mcp.json").read_text())
    assert "mcpServers" in mcp
    for srv in mcp["mcpServers"].values():
        assert "url" in srv
        assert "type" not in srv

    symlink = tmp_path / ".cursor" / "plugins" / plugin.name
    assert symlink.is_symlink()

    lockfile = tmp_path / ".runlayer" / "plugin-lock.yml"
    assert lockfile.exists()
    lock = yaml.safe_load(lockfile.read_text())
    match = [e for e in lock["plugins"] if e["id"] == plugin.id]
    assert len(match) == 1
    assert match[0]["install_mode"] == "native"
    assert match[0]["client"] == "cursor"
