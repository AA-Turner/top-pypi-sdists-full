import json
from pathlib import Path

from runlayer_cli.main import app
from tests.e2e.conftest import strip_ansi


def _opencode_config_path(home: Path) -> Path:
    return home / ".config" / "opencode" / "opencode.json"


def test_setup_install_opencode_remote_writes_mcp_config(
    runner, cli_args, tmp_path, monkeypatch, create_e2e_server
):
    """runlayer setup install --client opencode (remote/server proxy)."""
    monkeypatch.setenv("HOME", str(tmp_path))
    server = create_e2e_server(
        {
            "name": "deepwiki",
            "url": "https://mcp.deepwiki.com/mcp",
            "transport_type": "streaming-http",
            "transport_config": {},
        }
    )

    result = runner.invoke(
        app,
        [
            *cli_args,
            "setup",
            "install",
            "--client",
            "opencode",
            "--server-id",
            server.id,
            "--yes",
        ],
    )
    assert result.exit_code == 0, strip_ansi(result.output)

    cfg_path = _opencode_config_path(tmp_path)
    assert cfg_path.exists()
    cfg = json.loads(cfg_path.read_text())

    # install normalizes names; we only assert shape + proxy url
    assert "mcp" in cfg
    assert len(cfg["mcp"]) == 1
    name, entry = next(iter(cfg["mcp"].items()))
    assert name.startswith("e2e-"), name
    assert entry["enabled"] is True
    assert entry["type"] == "remote"
    assert entry["url"].endswith(f"/api/v1/proxy/{server.id}/mcp")


def test_setup_install_opencode_local_writes_command_array(
    runner, cli_args, tmp_path, monkeypatch, create_e2e_server
):
    """runlayer setup install --client opencode (local/stdio)."""
    monkeypatch.setenv("HOME", str(tmp_path))
    server = create_e2e_server(
        {
            "name": "echo",
            "url": "npx",
            "transport_type": "stdio",
            "transport_config": {"args": ["-y", "mcp-echo-server"]},
            "deployment_mode": "local",
        }
    )

    result = runner.invoke(
        app,
        [
            *cli_args,
            "setup",
            "install",
            "--client",
            "opencode",
            "--server-id",
            server.id,
            "--yes",
        ],
    )
    assert result.exit_code == 0, strip_ansi(result.output)

    cfg_path = _opencode_config_path(tmp_path)
    cfg = json.loads(cfg_path.read_text())
    name, entry = next(iter(cfg["mcp"].items()))
    assert name.startswith("e2e-"), name
    assert entry["enabled"] is True
    assert entry["type"] == "local"
    assert entry["command"][:3] == ["uvx", "runlayer", "run"]


def test_scan_dry_run_detects_opencode_config(runner, cli_args, tmp_path, monkeypatch):
    """runlayer scan --dry-run picks up ~/.config/opencode/opencode.json."""
    monkeypatch.setenv("HOME", str(tmp_path))
    cfg_path = _opencode_config_path(tmp_path)
    cfg_path.parent.mkdir(parents=True, exist_ok=True)
    cfg_path.write_text(
        json.dumps(
            {
                "$schema": "https://opencode.ai/config.json",
                "mcp": {
                    "my-opencode-server": {
                        "type": "remote",
                        "enabled": True,
                        "url": "https://example.com/mcp",
                    }
                },
            }
        )
        + "\n"
    )

    # Use --quiet so stdout is JSON only (scan command prints a progress line otherwise).
    result = runner.invoke(
        app, [*cli_args, "scan", "--dry-run", "--no-projects", "--quiet"]
    )
    assert result.exit_code == 0, strip_ansi(result.output)

    payload = json.loads(result.stdout)
    clients = {c["client"] for c in payload["configurations"]}
    assert "opencode" in clients
