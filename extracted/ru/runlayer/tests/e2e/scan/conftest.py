"""Fixtures for scan e2e tests with mock backend."""

import json
from pathlib import Path

import pytest


@pytest.fixture(autouse=True)
def telemetry_endpoint(httpserver):
    """Accept CLI trace exports so the OTLP flush at exit is instant.

    Without this the exporter gets a 500 for the unregistered route and
    retries with backoff, adding ~7s to every test.
    """
    httpserver.expect_request(
        "/api/v1/telemetry/traces", method="POST"
    ).respond_with_json({})


@pytest.fixture
def scan_home(tmp_path: Path, monkeypatch):
    """Create a temp HOME with one MCP server, one skill, and one plugin.

    Layout (all discovered by scan_all_clients with --no-projects):
      - OpenCode global config  -> 1 server
      - OpenCode global skill   -> 1 skill (SKILL.md)
      - Cursor native plugin    -> 1 plugin (.cursor-plugin/plugin.json)
    """
    monkeypatch.setenv("HOME", str(tmp_path))

    oc_dir = tmp_path / ".config" / "opencode"
    oc_dir.mkdir(parents=True)
    (oc_dir / "opencode.json").write_text(
        json.dumps(
            {
                "mcp": {
                    "test-server": {
                        "type": "remote",
                        "enabled": True,
                        "url": "https://example.com/mcp",
                    }
                }
            }
        )
    )

    skill_dir = oc_dir / "skills" / "my-skill"
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text("# My Skill\nA test skill for e2e.\n")

    plugin_dir = (
        tmp_path
        / ".cursor"
        / "plugins"
        / "cache"
        / "cursor-public"
        / "test-plugin"
        / "abc123"
    )
    manifest_dir = plugin_dir / ".cursor-plugin"
    manifest_dir.mkdir(parents=True)
    (manifest_dir / "plugin.json").write_text(
        json.dumps({"name": "test-plugin", "version": "1.0.0"})
    )

    return tmp_path
