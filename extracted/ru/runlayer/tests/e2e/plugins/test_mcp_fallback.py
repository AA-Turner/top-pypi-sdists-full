"""E2E tests for plugins add/remove with MCP fallback clients (non-claude_code)."""

from __future__ import annotations

import json
import platform

import pytest
import yaml

from runlayer_cli.main import app
from tests.e2e.conftest import strip_ansi

MACOS_CLIENTS = [
    pytest.param(
        "windsurf",
        ".codeium/windsurf/mcp_config.json",
        "mcpServers",
        "json",
        id="windsurf",
    ),
    pytest.param(
        "goose",
        ".config/goose/config.yaml",
        "extensions",
        "yaml",
        id="goose",
    ),
    pytest.param(
        "zed",
        ".config/zed/settings.json",
        "context_servers",
        "json",
        id="zed",
    ),
]

# Per-client URL key used in the config entry
_URL_KEY: dict[str, str] = {
    "windsurf": "serverUrl",
    "goose": "uri",
    "zed": "url",
    "opencode": "url",
}

# Per-client expected entry shape (subset checked after install)
_EXPECTED_ENTRY: dict[str, dict[str, object]] = {
    "windsurf": {},  # no type field
    "goose": {"type": "streamable_http", "enabled": True},
    "zed": {},  # no type field
    "opencode": {"type": "remote", "enabled": True},
}


def _find_proxy_entry(
    entries: dict[str, dict], proxy_suffix: str, client_name: str
) -> dict | None:
    url_key = _URL_KEY.get(client_name, "url")
    for v in entries.values():
        if proxy_suffix in v.get(url_key, ""):
            return v
    return None


def _read_config(path, fmt):
    text = path.read_text()
    if fmt == "yaml":
        return yaml.safe_load(text)
    return json.loads(text)


@pytest.mark.skipif(
    platform.system() != "Darwin",
    reason="MCP client config paths are macOS-only",
)
@pytest.mark.parametrize(
    "client_name,config_rel,servers_key,config_fmt",
    MACOS_CLIENTS,
)
def test_plugin_add_writes_client_config(
    client_name,
    config_rel,
    servers_key,
    config_fmt,
    runner,
    cli_args,
    tmp_path,
    monkeypatch,
    create_e2e_plugin,
):
    monkeypatch.setenv("HOME", str(tmp_path))
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
            client_name,
        ],
    )
    output = strip_ansi(result.output)
    assert result.exit_code == 0, output
    assert "1 installed" in output

    config_path = tmp_path / config_rel
    assert config_path.exists(), f"expected {config_path}"

    cfg = _read_config(config_path, config_fmt)
    assert servers_key in cfg

    proxy_suffix = f"/proxy/plugins/{plugin.id}/mcp"
    entries = cfg[servers_key]
    entry = _find_proxy_entry(entries, proxy_suffix, client_name)
    assert entry, f"no entry with {proxy_suffix} in {entries}"

    expected = _EXPECTED_ENTRY.get(client_name, {})
    for k, v in expected.items():
        assert entry.get(k) == v, f"{client_name}: expected {k}={v}, got {entry.get(k)}"

    lockfile = tmp_path / ".runlayer" / "plugin-lock.yml"
    assert lockfile.exists()
    lock = yaml.safe_load(lockfile.read_text())
    match = [e for e in lock["plugins"] if e["id"] == plugin.id]
    assert len(match) == 1
    assert match[0]["install_mode"] == "mcp_fallback"
    assert match[0]["client"] == client_name


@pytest.mark.skipif(
    platform.system() != "Darwin",
    reason="MCP client config paths are macOS-only",
)
@pytest.mark.parametrize(
    "client_name,config_rel,servers_key,config_fmt",
    MACOS_CLIENTS,
)
def test_plugin_remove_cleans_client_config(
    client_name,
    config_rel,
    servers_key,
    config_fmt,
    runner,
    cli_args,
    tmp_path,
    monkeypatch,
    create_e2e_plugin,
):
    monkeypatch.setenv("HOME", str(tmp_path))
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
            client_name,
        ],
    )

    config_path = tmp_path / config_rel
    assert config_path.exists()

    remove_result = runner.invoke(
        app,
        ["plugins", "remove", plugin.name, "--client", client_name],
    )
    output = strip_ansi(remove_result.output)
    assert remove_result.exit_code == 0, output
    assert f"Removed: {plugin.name}" in output

    cfg = _read_config(config_path, config_fmt)
    proxy_suffix = f"/proxy/plugins/{plugin.id}/mcp"
    entries = cfg.get(servers_key, {})
    assert not _find_proxy_entry(entries, proxy_suffix, client_name)

    lockfile = tmp_path / ".runlayer" / "plugin-lock.yml"
    lock = yaml.safe_load(lockfile.read_text())
    ids = [e["id"] for e in lock.get("plugins", [])]
    assert plugin.id not in ids


def test_opencode_plugin_add_writes_client_config(
    runner,
    cli_args,
    tmp_path,
    monkeypatch,
    create_e2e_plugin,
):
    monkeypatch.setenv("HOME", str(tmp_path))
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
            "opencode",
        ],
    )
    output = strip_ansi(result.output)
    assert result.exit_code == 0, output
    assert "1 installed" in output

    config_path = tmp_path / ".config" / "opencode" / "opencode.json"
    assert config_path.exists()

    cfg = json.loads(config_path.read_text())
    assert "mcp" in cfg

    proxy_suffix = f"/proxy/plugins/{plugin.id}/mcp"
    entries = cfg["mcp"]
    entry = _find_proxy_entry(entries, proxy_suffix, "opencode")
    assert entry, f"no entry with {proxy_suffix} in {entries}"
    assert entry["type"] == "remote"
    assert entry["enabled"] is True

    lockfile = tmp_path / ".runlayer" / "plugin-lock.yml"
    lock = yaml.safe_load(lockfile.read_text())
    match = [e for e in lock["plugins"] if e["id"] == plugin.id]
    assert len(match) == 1
    assert match[0]["install_mode"] == "mcp_fallback"
    assert match[0]["client"] == "opencode"


def test_opencode_plugin_remove_cleans_client_config(
    runner,
    cli_args,
    tmp_path,
    monkeypatch,
    create_e2e_plugin,
):
    monkeypatch.setenv("HOME", str(tmp_path))
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
            "opencode",
        ],
    )

    config_path = tmp_path / ".config" / "opencode" / "opencode.json"
    assert config_path.exists()

    remove_result = runner.invoke(
        app,
        ["plugins", "remove", plugin.name, "--client", "opencode"],
    )
    output = strip_ansi(remove_result.output)
    assert remove_result.exit_code == 0, output
    assert f"Removed: {plugin.name}" in output

    cfg = json.loads(config_path.read_text())
    proxy_suffix = f"/proxy/plugins/{plugin.id}/mcp"
    entries = cfg.get("mcp", {})
    assert not _find_proxy_entry(entries, proxy_suffix, "opencode")

    lockfile = tmp_path / ".runlayer" / "plugin-lock.yml"
    lock = yaml.safe_load(lockfile.read_text())
    ids = [e["id"] for e in lock.get("plugins", [])]
    assert plugin.id not in ids
