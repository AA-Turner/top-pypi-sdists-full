import json
import shutil
from pathlib import Path

from tests.e2e.conftest import strip_ansi

from runlayer_cli.main import app

FIXTURE_ROOT = Path(__file__).resolve().parent.parent / "fixtures" / "full_plugin"


def _copy_plugin_fixture(tmp_path: Path) -> Path:
    plugins_root = tmp_path / "plugins-source"
    plugin_dir = plugins_root / "review-suite"
    shutil.copytree(FIXTURE_ROOT, plugin_dir)
    return plugins_root


def _patch_runtime_values(plugin_dir: Path, server_id: str, api_key: str) -> None:
    for path in [
        plugin_dir / ".mcp.json",
        plugin_dir / ".claude-plugin" / "plugin.json",
    ]:
        raw = path.read_text()
        raw = raw.replace("__SERVER_ID__", server_id).replace("__API_KEY__", api_key)
        path.write_text(raw)


def _remove_manifest_mcp(plugin_dir: Path) -> None:
    manifest_path = plugin_dir / ".claude-plugin" / "plugin.json"
    manifest = json.loads(manifest_path.read_text())
    manifest.pop("mcpServers", None)
    manifest_path.write_text(json.dumps(manifest, indent=2))


def _skill_by_path(api_client, namespace: str, path: str):
    skills = api_client.list_skills(namespace)
    return next(skill for skill in skills if skill.path == path)


def test_plugins_push_lifecycle(
    runner,
    cli_args,
    api_key,
    api_client,
    tmp_path,
    unique_id,
    create_e2e_server,
):
    namespace = f"e2e-plugin/{unique_id}"
    plugins_root = _copy_plugin_fixture(tmp_path)
    plugin_dir = plugins_root / "review-suite"
    server = create_e2e_server(
        {
            "name": "echo",
            "url": "npx",
            "transport_type": "stdio",
            "transport_config": {"args": ["-y", "mcp-echo-server"]},
        }
    )
    _patch_runtime_values(plugin_dir, server.id, api_key)

    result = runner.invoke(
        app,
        [*cli_args, "plugins", "push", str(plugins_root), "--namespace", namespace],
    )
    output = strip_ansi(result.output)
    assert result.exit_code == 0, output
    assert "3 skills created, 1 plugins created" in output
    assert (
        "Warning: review-suite: missing server 00000000-0000-0000-0000-000000000000 skipped"
        in output
    )

    plugins = api_client.list_plugins_detailed(namespace)
    assert len(plugins) == 1
    plugin = plugins[0]
    assert plugin.path == "review-suite"
    assert plugin.server_count == 1
    assert plugin.skill_count == 3

    skills = api_client.list_skills(namespace)
    assert {skill.path for skill in skills} == {
        "review-suite/__root__",
        "review-suite/code-review",
        "review-suite/ticket-triage",
    }
    root_skill = _skill_by_path(api_client, namespace, "review-suite/__root__")
    root_detail = api_client.get_skill(root_skill.id)
    root_titles = {f.title for f in root_detail.files}
    assert "commands/review.md" in root_titles
    assert "agents/code-reviewer.md" in root_titles
    assert "agents/README.md" in root_titles
    assert "hooks/hooks.json" in root_titles
    assert "scripts/deploy.sh" in root_titles
    assert "skillsets/reference.md" in root_titles
    assert "skills-v2/notes.md" in root_titles
    assert "README.md" not in root_titles
    assert ".lsp.json" not in root_titles
    assert "settings.json" not in root_titles

    second = runner.invoke(
        app,
        [*cli_args, "plugins", "push", str(plugins_root), "--namespace", namespace],
    )
    second_output = strip_ansi(second.output)
    assert second.exit_code == 0, second_output
    assert "everything up to date" in second_output

    (plugin_dir / "commands" / "review.md").write_text(
        "---\ndescription: Updated review\n---\nUpdated instructions.\n"
    )
    shutil.rmtree(plugin_dir / "skills" / "ticket-triage")

    update = runner.invoke(
        app,
        [*cli_args, "plugins", "push", str(plugins_root), "--namespace", namespace],
    )
    update_output = strip_ansi(update.output)
    assert update.exit_code == 0, update_output
    assert "Done, " in update_output
    assert "updated" in update_output
    assert {skill.path for skill in api_client.list_skills(namespace)} == {
        "review-suite/__root__",
        "review-suite/code-review",
    }

    survivor = api_client.create_skill(
        name=f"survivor-{unique_id}",
        namespace=namespace,
        path="standalone/survivor",
    )

    shutil.rmtree(plugin_dir)
    prune = runner.invoke(
        app,
        [
            *cli_args,
            "plugins",
            "push",
            str(plugins_root),
            "--namespace",
            namespace,
            "--prune",
        ],
    )
    prune_output = strip_ansi(prune.output)
    assert prune.exit_code == 0, prune_output
    assert "1 plugins deleted" in prune_output
    assert api_client.list_plugins_detailed(namespace) == []
    remaining_skills = api_client.list_skills(namespace)
    assert [skill.path for skill in remaining_skills] == ["standalone/survivor"]

    api_client.delete_skill(survivor.id)


def test_plugins_push_falls_back_to_mcp_json(
    runner,
    cli_args,
    api_key,
    api_client,
    tmp_path,
    unique_id,
    create_e2e_server,
):
    namespace = f"e2e-plugin-mcp/{unique_id}"
    plugins_root = _copy_plugin_fixture(tmp_path)
    plugin_dir = plugins_root / "review-suite"
    server = create_e2e_server(
        {
            "name": "echo",
            "url": "npx",
            "transport_type": "stdio",
            "transport_config": {"args": ["-y", "mcp-echo-server"]},
        }
    )
    _patch_runtime_values(plugin_dir, server.id, api_key)
    _remove_manifest_mcp(plugin_dir)

    result = runner.invoke(
        app,
        [*cli_args, "plugins", "push", str(plugins_root), "--namespace", namespace],
    )
    output = strip_ansi(result.output)
    assert result.exit_code == 0, output
    assert "3 skills created, 1 plugins created" in output


def test_plugins_push_then_add_uses_plugin_json_and_installs_runlayer_only(
    runner,
    cli_args,
    api_key,
    api_client,
    tmp_path,
    unique_id,
    create_e2e_server,
    monkeypatch,
):
    monkeypatch.chdir(tmp_path)
    namespace = f"e2e-plugin-install/{unique_id}"
    plugins_root = _copy_plugin_fixture(tmp_path)
    plugin_dir = plugins_root / "review-suite"
    server = create_e2e_server(
        {
            "name": "echo",
            "url": "npx",
            "transport_type": "stdio",
            "transport_config": {"args": ["-y", "mcp-echo-server"]},
        }
    )
    _patch_runtime_values(plugin_dir, server.id, api_key)

    push = runner.invoke(
        app,
        [*cli_args, "plugins", "push", str(plugins_root), "--namespace", namespace],
    )
    push_output = strip_ansi(push.output)
    assert push.exit_code == 0, push_output
    assert "3 skills created, 1 plugins created" in push_output
    assert (
        "Warning: review-suite: missing server 00000000-0000-0000-0000-000000000000 skipped"
        in push_output
    )
    assert (
        "Warning: review-suite: skipped MCP server external-http with non-Runlayer URL https://example.com/mcp"
        in push_output
    )

    plugins = api_client.list_plugins_detailed(namespace)
    assert len(plugins) == 1
    assert plugins[0].server_count == 1

    install = runner.invoke(
        app,
        [
            *cli_args,
            "plugins",
            "add",
            namespace,
            "--plugin",
            "review-suite",
            "--client",
            "claude_code",
        ],
    )
    install_output = strip_ansi(install.output)
    assert install.exit_code == 0, install_output
    assert "1 installed" in install_output

    manifest_path = (
        tmp_path
        / ".agents"
        / "plugins"
        / "review-suite"
        / ".claude-plugin"
        / "plugin.json"
    )
    manifest = json.loads(manifest_path.read_text())
    manifest_mcp = manifest["mcpServers"]
    assert len(manifest_mcp) == 1
    assert "missing-runlayer" not in manifest_mcp
    assert "external-http" not in manifest_mcp
    assert "plugin-reference" not in manifest_mcp
    assert "stdio-tool" not in manifest_mcp
    manifest_mcp_url = next(iter(manifest_mcp.values()))["url"]
    assert f"/api/v1/proxy/{server.id}/mcp" in manifest_mcp_url

    mcp_path = tmp_path / ".agents" / "plugins" / "review-suite" / ".mcp.json"
    mcp = json.loads(mcp_path.read_text())
    assert len(mcp["mcpServers"]) == 1
    assert "missing-runlayer" not in mcp["mcpServers"]
    assert "external-http" not in mcp["mcpServers"]
    assert "plugin-reference" not in mcp["mcpServers"]
    assert "stdio-tool" not in mcp["mcpServers"]
    mcp_url = next(iter(mcp["mcpServers"].values()))["url"]
    assert f"/api/v1/proxy/{server.id}/mcp" in mcp_url


def test_plugins_push_dry_run_does_not_mutate(
    runner,
    cli_args,
    api_key,
    api_client,
    tmp_path,
    unique_id,
    create_e2e_server,
):
    namespace = f"e2e-plugin-dry/{unique_id}"
    plugins_root = _copy_plugin_fixture(tmp_path)
    plugin_dir = plugins_root / "review-suite"
    server = create_e2e_server(
        {
            "name": "echo",
            "url": "npx",
            "transport_type": "stdio",
            "transport_config": {"args": ["-y", "mcp-echo-server"]},
        }
    )
    _patch_runtime_values(plugin_dir, server.id, api_key)

    result = runner.invoke(
        app,
        [
            *cli_args,
            "plugins",
            "push",
            str(plugins_root),
            "--namespace",
            namespace,
            "--dry-run",
        ],
    )
    output = strip_ansi(result.output)
    assert result.exit_code == 0, output
    assert "[dry run]" in output
    assert api_client.list_plugins_detailed(namespace) == []
    assert api_client.list_skills(namespace) == []
