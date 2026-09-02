import json
import shutil
from pathlib import Path
from unittest.mock import patch

from runlayer_cli.plugins.discovery import ROOT_SKILL_SUFFIX, discover_plugins


FIXTURE_ROOT = (
    Path(__file__).parent / "e2e" / "fixtures" / "full_plugin"
)


def _copy_fixture(tmp_path: Path) -> Path:
    plugin_root = tmp_path / "review-suite"
    shutil.copytree(FIXTURE_ROOT, plugin_root)
    _replace_fixture_placeholders(
        plugin_root,
        server_id="12345678-1234-1234-1234-123456789abc",
    )
    return plugin_root


def _replace_fixture_placeholders(
    plugin_root: Path, *, server_id: str, api_key: str = "__API_KEY__"
) -> None:
    for path in [
        plugin_root / ".mcp.json",
        plugin_root / ".claude-plugin" / "plugin.json",
    ]:
        raw = path.read_text()
        raw = raw.replace("__SERVER_ID__", server_id).replace("__API_KEY__", api_key)
        path.write_text(raw)


def _write_fixture_mcp_servers(plugin_root: Path, mcp_servers: dict[str, object]) -> None:
    mcp_payload = {"mcpServers": mcp_servers}
    (plugin_root / ".mcp.json").write_text(json.dumps(mcp_payload, indent=2))
    manifest_path = plugin_root / ".claude-plugin" / "plugin.json"
    manifest = json.loads(manifest_path.read_text())
    manifest["mcpServers"] = mcp_servers
    manifest_path.write_text(json.dumps(manifest, indent=2))


def test_discover_plugins_full_fixture(tmp_path: Path) -> None:
    _copy_fixture(tmp_path)

    plugins = discover_plugins(tmp_path)

    assert len(plugins) == 1
    plugin = plugins[0]
    assert plugin.path == "review-suite"
    assert plugin.name == "review-suite"
    assert plugin.description is not None
    assert plugin.version == "1.0.0"

    assert [(c.entry_name, c.server_id) for c in plugin.server_connectors] == [
        ("valid-runlayer", "12345678-1234-1234-1234-123456789abc"),
        ("missing-runlayer", "00000000-0000-0000-0000-000000000000"),
    ]

    assert [skill.path for skill in plugin.skills] == [
        "review-suite/code-review",
        "review-suite/ticket-triage",
        f"review-suite/{ROOT_SKILL_SUFFIX}",
    ]

    root_skill = next(
        skill for skill in plugin.skills if skill.path.endswith(f"/{ROOT_SKILL_SUFFIX}")
    )
    titles = {f.title for f in root_skill.files}
    assert {
        "agents/code-reviewer.md",
        "agents/README.md",
        "commands/review.md",
        "hooks/hooks.json",
        "hooks/validate.sh",
        "skillsets/reference.md",
        "skills-v2/notes.md",
        "scripts/deploy.sh",
        "notes.txt",
        "tool.ts",
        "config.json",
    } <= titles
    assert "README.md" not in titles
    assert ".lsp.json" not in titles
    assert "settings.json" not in titles
    assert ".claude-plugin/plugin.json" not in titles
    assert "skills/code-review/prompts.md" not in titles


def test_discover_plugins_truncates_long_description_and_warns(
    tmp_path: Path,
) -> None:
    plugin_root = tmp_path / "long-desc"
    manifest_dir = plugin_root / ".claude-plugin"
    manifest_dir.mkdir(parents=True)
    long_description = "x" * 1025
    (manifest_dir / "plugin.json").write_text(
        f'{{"name":"long-desc","version":"1.0.0","description":"{long_description}"}}'
    )

    with patch("runlayer_cli.plugins.discovery.logger.warning") as warning_mock:
        plugins = discover_plugins(tmp_path)

    assert len(plugins) == 1
    assert plugins[0].description == long_description[:1024]
    assert plugins[0].manifest_warnings == [
        "long-desc: truncated plugin description to 1024 characters"
    ]
    warning_mock.assert_not_called()


def test_discover_plugins_warns_for_non_runlayer_mcp_url(tmp_path: Path) -> None:
    plugin_root = _copy_fixture(tmp_path)
    _write_fixture_mcp_servers(
        plugin_root,
        {
            "external-http": {
                "type": "http",
                "url": "https://example.com/mcp",
            },
            "local-stdio": {
                "command": "npx",
                "args": ["some-local-server"],
            },
        },
    )

    plugins = discover_plugins(tmp_path)

    assert len(plugins) == 1
    assert plugins[0].server_connectors == []
    assert plugins[0].mcp_warnings == [
        "review-suite: skipped MCP server external-http with non-Runlayer URL https://example.com/mcp"
    ]


def test_discover_plugins_accepts_uppercase_runlayer_proxy_uuid(tmp_path: Path) -> None:
    plugin_root = _copy_fixture(tmp_path)
    _write_fixture_mcp_servers(
        plugin_root,
        {
            "uppercase-runlayer": {
                "url": "https://app.runlayer.com/api/v1/proxy/12345678-1234-1234-1234-123456789ABC/mcp"
            },
            "uppercase-plugin-proxy": {
                "url": "https://app.runlayer.com/api/v1/proxy/plugins/AAAAAAAA-AAAA-AAAA-AAAA-AAAAAAAAAAAA/mcp"
            },
        },
    )

    plugins = discover_plugins(tmp_path)

    assert len(plugins) == 1
    assert [(c.entry_name, c.server_id) for c in plugins[0].server_connectors] == [
        ("uppercase-runlayer", "12345678-1234-1234-1234-123456789abc"),
    ]
    assert plugins[0].mcp_warnings == []


def test_discover_plugins_skips_malformed_runlayer_proxy_uuid(tmp_path: Path) -> None:
    plugin_root = _copy_fixture(tmp_path)
    malformed_server_id = "12345678123412341234123456789abcdef0"
    _write_fixture_mcp_servers(
        plugin_root,
        {
            "bad-runlayer": {
                "url": (
                    "https://app.runlayer.com/api/v1/proxy/"
                    f"{malformed_server_id}/mcp"
                )
            }
        },
    )

    plugins = discover_plugins(tmp_path)

    assert len(plugins) == 1
    assert plugins[0].server_connectors == []
    assert plugins[0].mcp_warnings == [
        "review-suite: skipped MCP server bad-runlayer with malformed Runlayer "
        "server id 12345678123412341234123456789abcdef0"
    ]


def test_discover_plugins_falls_back_to_mcp_json_when_manifest_has_no_mcp(
    tmp_path: Path,
) -> None:
    plugin_root = _copy_fixture(tmp_path)
    manifest_path = plugin_root / ".claude-plugin" / "plugin.json"
    manifest = json.loads(manifest_path.read_text())
    del manifest["mcpServers"]
    manifest_path.write_text(json.dumps(manifest, indent=2))

    plugins = discover_plugins(tmp_path)

    assert len(plugins) == 1
    assert [(c.entry_name, c.server_id) for c in plugins[0].server_connectors] == [
        ("valid-runlayer", "12345678-1234-1234-1234-123456789abc"),
        ("missing-runlayer", "00000000-0000-0000-0000-000000000000"),
    ]
