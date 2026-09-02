from __future__ import annotations

import json
import os
import platform
from pathlib import Path

import pytest

from runlayer_cli import mdm_config
from runlayer_cli.aiwatch_config_cache import parse_aiwatch_config
from runlayer_cli.commands.aiwatch_setup import _effective_backend_settings
from runlayer_cli.hook_install import llm_routing
from runlayer_cli.hook_install import paths
from runlayer_cli.hook_install.paths import InstallScope


@pytest.fixture
def routing_paths(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> dict[str, Path]:
    claude_path = tmp_path / "claude" / "managed-settings.json"
    codex_path = tmp_path / "codex" / "managed_config.toml"
    monkeypatch.setattr(
        llm_routing,
        "_claude_code_config_file",
        lambda _scope: claude_path,
    )
    monkeypatch.setattr(
        llm_routing,
        "_codex_features_toml_file",
        lambda _scope: codex_path,
    )
    return {"claude": claude_path, "codex": codex_path}


def test_route_writes_missing_client_configs(routing_paths: dict[str, Path]) -> None:
    result = llm_routing.route(
        "https://gateway.example.com/",
        "llm-device-key",
        scope=InstallScope.MDM,
    )

    assert result is llm_routing.RouteResult.WRITTEN
    claude = json.loads(routing_paths["claude"].read_text())
    assert claude["env"] == {
        "ANTHROPIC_BASE_URL": "https://gateway.example.com/anthropic",
        "ANTHROPIC_AUTH_TOKEN": "llm-device-key",
        "ANTHROPIC_API_KEY": "llm-device-key",
        "CLAUDE_CODE_OAUTH_TOKEN": "",
        "CLAUDE_CODE_USE_BEDROCK": "",
        "CLAUDE_CODE_USE_VERTEX": "",
        "CLAUDE_CODE_USE_FOUNDRY": "",
    }
    assert routing_paths["codex"].read_text() == (
        'model_provider = "runlayer"\n'
        "\n"
        "[model_providers.runlayer]\n"
        'name = "Runlayer"\n'
        'base_url = "https://gateway.example.com/openai/v1"\n'
        'wire_api = "responses"\n'
        'experimental_bearer_token = "llm-device-key"\n'
    )


@pytest.mark.parametrize("client", ["claude", "codex"])
def test_route_writes_empty_client_config(
    client: str,
    routing_paths: dict[str, Path],
) -> None:
    path = routing_paths[client]
    path.parent.mkdir(parents=True)
    path.write_text("")

    result = llm_routing.route(
        "https://gateway.example.com",
        "llm-device-key",
        scope=InstallScope.MDM,
    )

    assert result is llm_routing.RouteResult.DRIFTED
    assert "llm-device-key" in path.read_text()


def test_route_merges_foreign_claude_settings(routing_paths: dict[str, Path]) -> None:
    claude_path = routing_paths["claude"]
    claude_path.parent.mkdir(parents=True)
    claude_path.write_text(
        json.dumps(
            {
                "permissions": {"allow": ["Read"]},
                "env": {"FOREIGN_ENV": "kept"},
            }
        )
    )

    result = llm_routing.route(
        "https://gateway.example.com",
        "llm-device-key",
        scope=InstallScope.MDM,
    )

    assert result is llm_routing.RouteResult.DRIFTED
    claude = json.loads(claude_path.read_text())
    assert claude["permissions"] == {"allow": ["Read"]}
    assert claude["env"]["FOREIGN_ENV"] == "kept"
    assert claude["env"]["ANTHROPIC_BASE_URL"] == (
        "https://gateway.example.com/anthropic"
    )
    assert claude["env"]["ANTHROPIC_AUTH_TOKEN"] == "llm-device-key"


def test_route_is_unchanged_when_both_configs_match(
    routing_paths: dict[str, Path],
) -> None:
    first = llm_routing.route(
        "https://gateway.example.com",
        "llm-device-key",
        scope=InstallScope.MDM,
    )
    second = llm_routing.route(
        "https://gateway.example.com",
        "llm-device-key",
        scope=InstallScope.MDM,
    )

    assert first is llm_routing.RouteResult.WRITTEN
    assert second is llm_routing.RouteResult.UNCHANGED
    assert not list(routing_paths["claude"].parent.glob("*.backup_*.json"))
    assert not list(routing_paths["codex"].parent.glob("*.backup_*.toml"))


def test_route_repairs_codex_provider_missing_name(
    routing_paths: dict[str, Path],
) -> None:
    llm_routing.route(
        "https://gateway.example.com",
        "llm-device-key",
        scope=InstallScope.MDM,
    )
    codex_path = routing_paths["codex"]
    codex_path.write_text(codex_path.read_text().replace('name = "Runlayer"\n', ""))

    result = llm_routing.route(
        "https://gateway.example.com",
        "llm-device-key",
        scope=InstallScope.MDM,
    )

    assert result is llm_routing.RouteResult.DRIFTED
    assert '[model_providers.runlayer]\nname = "Runlayer"\n' in codex_path.read_text()


@pytest.mark.parametrize("client", ["claude", "codex"])
def test_route_reports_and_repairs_client_drift(
    client: str,
    routing_paths: dict[str, Path],
) -> None:
    llm_routing.route(
        "https://gateway.example.com",
        "llm-device-key",
        scope=InstallScope.MDM,
    )
    path = routing_paths[client]
    path.write_text(
        path.read_text().replace("gateway.example.com", "other.example.com")
    )

    result = llm_routing.route(
        "https://gateway.example.com",
        "llm-device-key",
        scope=InstallScope.MDM,
    )

    assert result is llm_routing.RouteResult.DRIFTED
    assert "other.example.com" not in path.read_text()
    if client == "claude":
        assert json.loads(path.read_text())["env"]["ANTHROPIC_BASE_URL"] == (
            "https://gateway.example.com/anthropic"
        )
    assert len(list(path.parent.glob(f"{path.stem}.backup_*{path.suffix}"))) == 1


def test_route_without_key_writes_nothing(
    routing_paths: dict[str, Path],
) -> None:
    result = llm_routing.route(
        "https://gateway.example.com",
        "",
        scope=InstallScope.MDM,
    )

    assert result is llm_routing.RouteResult.FAILED
    assert not routing_paths["claude"].exists()
    assert not routing_paths["codex"].exists()


@pytest.mark.parametrize(
    ("base_url", "scope"),
    [
        ("http://gateway.example.com", InstallScope.USER),
        ("gateway.example.com", InstallScope.USER),
        ("https://gateway.example.com/prefix", InstallScope.USER),
        ("https://gateway.example.com?tenant=other", InstallScope.USER),
        ("https://gateway.example.com?", InstallScope.USER),
        ("https://gateway.example.com#fragment", InstallScope.USER),
        ("https://gateway.example.com#", InstallScope.USER),
        ("https://user:password@gateway.example.com", InstallScope.USER),
        ("https://gateway.example.com:invalid", InstallScope.USER),
        ("https://gateway.example.com:0", InstallScope.USER),
        ("http://127.0.0.1:8190", InstallScope.MDM),
    ],
)
def test_route_rejects_unsafe_or_non_bare_gateway_url(
    base_url: str,
    scope: InstallScope,
    routing_paths: dict[str, Path],
) -> None:
    result = llm_routing.route(
        base_url,
        "llm-device-key",
        scope=scope,
    )

    assert result is llm_routing.RouteResult.FAILED
    assert not routing_paths["claude"].exists()
    assert not routing_paths["codex"].exists()


def test_route_allows_user_scope_loopback_http(
    routing_paths: dict[str, Path],
) -> None:
    result = llm_routing.route(
        "http://127.0.0.1:8190",
        "llm-device-key",
        scope=InstallScope.USER,
    )

    assert result is llm_routing.RouteResult.WRITTEN
    claude = json.loads(routing_paths["claude"].read_text())
    assert claude["env"]["ANTHROPIC_BASE_URL"] == ("http://127.0.0.1:8190/anthropic")
    assert (
        'base_url = "http://127.0.0.1:8190/openai/v1"'
        in routing_paths["codex"].read_text()
    )


@pytest.mark.skipif(os.name != "posix", reason="requires POSIX permission bits")
def test_route_user_scope_writes_private_credential_files(
    routing_paths: dict[str, Path],
) -> None:
    for path in routing_paths.values():
        path.parent.mkdir(parents=True)
        path.write_text("{}" if path.suffix == ".json" else "")
        path.chmod(0o644)

    result = llm_routing.route(
        "https://gateway.example.com",
        "llm-device-key",
        scope=InstallScope.USER,
    )

    assert result is llm_routing.RouteResult.DRIFTED
    for path in routing_paths.values():
        assert path.stat().st_mode & 0o777 == 0o600
        backups = list(path.parent.glob(f"{path.stem}.backup_*{path.suffix}"))
        assert len(backups) == 1
        assert backups[0].stat().st_mode & 0o777 == 0o600


@pytest.mark.skipif(os.name != "posix", reason="requires POSIX permission bits")
def test_route_repairs_user_scope_permission_drift(
    routing_paths: dict[str, Path],
) -> None:
    first = llm_routing.route(
        "https://gateway.example.com",
        "llm-device-key",
        scope=InstallScope.USER,
    )
    for path in routing_paths.values():
        path.chmod(0o644)

    second = llm_routing.route(
        "https://gateway.example.com",
        "llm-device-key",
        scope=InstallScope.USER,
    )

    assert first is llm_routing.RouteResult.WRITTEN
    assert second is llm_routing.RouteResult.DRIFTED
    for path in routing_paths.values():
        assert path.stat().st_mode & 0o777 == 0o600


def test_route_ignores_user_scope_mode_on_windows(
    routing_paths: dict[str, Path],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    real_read = llm_routing.maybe_safe_read_file

    def windows_read(path: Path, *, home: Path | None):
        existing = real_read(path, home=home)
        if existing is not None:
            existing["mode"] = 0o666
        return existing

    monkeypatch.setattr(platform, "system", lambda: "Windows")
    monkeypatch.setattr(llm_routing, "maybe_safe_read_file", windows_read)

    first = llm_routing.route(
        "https://gateway.example.com",
        "llm-device-key",
        scope=InstallScope.USER,
    )
    second = llm_routing.route(
        "https://gateway.example.com",
        "llm-device-key",
        scope=InstallScope.USER,
    )

    assert first is llm_routing.RouteResult.WRITTEN
    assert second is llm_routing.RouteResult.UNCHANGED
    for path in routing_paths.values():
        assert not list(path.parent.glob(f"{path.stem}.backup_*{path.suffix}"))


@pytest.mark.skipif(os.name != "posix", reason="requires POSIX permission bits")
def test_route_mdm_scope_keeps_targets_readable_and_backups_private(
    routing_paths: dict[str, Path],
) -> None:
    first = llm_routing.route(
        "https://gateway.example.com",
        "llm-device-key",
        scope=InstallScope.MDM,
    )
    second = llm_routing.route(
        "https://gateway.example.com",
        "replacement-key",
        scope=InstallScope.MDM,
    )

    assert first is llm_routing.RouteResult.WRITTEN
    assert second is llm_routing.RouteResult.DRIFTED
    for path in routing_paths.values():
        assert path.stat().st_mode & 0o777 == 0o644
        backups = list(path.parent.glob(f"{path.stem}.backup_*{path.suffix}"))
        assert len(backups) == 1
        assert backups[0].stat().st_mode & 0o777 == 0o600


def test_unroute_removes_only_routing_config(
    routing_paths: dict[str, Path],
) -> None:
    claude_path = routing_paths["claude"]
    claude_path.parent.mkdir(parents=True)
    claude_path.write_text(
        json.dumps(
            {
                "permissions": {"allow": ["Read"]},
                "env": {"FOREIGN_ENV": "kept"},
            }
        )
    )
    codex_path = routing_paths["codex"]
    codex_path.parent.mkdir(parents=True)
    codex_path.write_text(
        'approval_policy = "on-request"\n[features]\nhooks = true\nmodel = "gpt-5"\n'
    )
    llm_routing.route(
        "https://gateway.example.com",
        "llm-device-key",
        scope=InstallScope.MDM,
    )
    assert json.loads(claude_path.read_text())["env"]["ANTHROPIC_BASE_URL"] == (
        "https://gateway.example.com/anthropic"
    )

    llm_routing.unroute(scope=InstallScope.MDM)
    llm_routing.unroute(scope=InstallScope.MDM)

    claude = json.loads(claude_path.read_text())
    assert claude == {
        "permissions": {"allow": ["Read"]},
        "env": {"FOREIGN_ENV": "kept"},
    }
    codex = codex_path.read_text()
    assert "[model_providers.runlayer]" not in codex
    assert 'model_provider = "runlayer"' not in codex
    assert 'approval_policy = "on-request"' in codex
    assert "[features]\nhooks = true" in codex
    assert 'model = "gpt-5"' in codex


def test_unroute_preserves_foreign_codex_provider(
    routing_paths: dict[str, Path],
) -> None:
    codex_path = routing_paths["codex"]
    codex_path.parent.mkdir(parents=True)
    foreign_config = 'model_provider = "openai"\nmodel = "gpt-5"\n'
    codex_path.write_text(foreign_config)

    llm_routing.unroute(scope=InstallScope.MDM)

    assert codex_path.read_text() == foreign_config


def test_unroute_attempts_codex_when_claude_settings_are_invalid(
    routing_paths: dict[str, Path],
) -> None:
    llm_routing.route(
        "https://gateway.example.com",
        "llm-device-key",
        scope=InstallScope.MDM,
    )
    routing_paths["claude"].write_text("{")

    with pytest.raises(OSError):
        llm_routing.unroute(scope=InstallScope.MDM)

    codex = routing_paths["codex"].read_text()
    assert 'model_provider = "runlayer"' not in codex
    assert "[model_providers.runlayer]" not in codex


@pytest.mark.parametrize("unsafe_client", ["claude", "codex"])
def test_route_fails_closed_for_unsafe_windows_mdm_path(
    unsafe_client: str,
    routing_paths: dict[str, Path],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    unsafe_path = routing_paths[unsafe_client]
    monkeypatch.setattr(
        llm_routing,
        "is_unsafe_windows_mdm_path",
        lambda path, **_kwargs: path == unsafe_path,
    )

    result = llm_routing.route(
        "https://gateway.example.com",
        "llm-device-key",
        scope=InstallScope.MDM,
    )

    assert result is llm_routing.RouteResult.FAILED
    assert not routing_paths["claude"].exists()
    assert not routing_paths["codex"].exists()


@pytest.mark.parametrize(
    ("managed", "expected"),
    [
        ({"llm_routing": True, "llm_routing_base_url": "https://gw"}, True),
        ({"llm_routing": True}, False),
        ({"llm_routing_base_url": "https://gw"}, False),
        ({}, False),
        ({"llm_routing": True, "llm_routing_base_url": ""}, False),
    ],
)
def test_resolve_llm_routing_fails_closed(
    managed: mdm_config.ManagedConfig,
    expected: bool,
) -> None:
    assert mdm_config.resolve_llm_routing(managed) is expected


def test_backend_snapshot_fields_feed_managed_routing(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    backend_config = parse_aiwatch_config(
        {
            "version": 1,
            "mode": "monitor",
            "sessions": False,
            "mcp_usage_metadata": False,
            "browser_mode": "monitor",
            "browser_sessions": False,
            "detect_processes": False,
            "detect_containers": False,
            "project_depth": 7,
            "project_timeout": 60,
            "llm_routing": True,
            "llm_routing_base_url": "https://gateway.example.com",
        }
    )
    monkeypatch.setattr(mdm_config.platform, "system", lambda: "Darwin")
    monkeypatch.setattr(
        mdm_config,
        "_read_macos",
        lambda _paths: {"org_api_key": "rl_org_key"},
    )
    monkeypatch.setattr(
        mdm_config,
        "read_backend_config",
        lambda _org_api_key: backend_config,
    )

    managed = mdm_config.read_managed_config()

    assert managed["llm_routing"] is True
    assert managed["llm_routing_base_url"] == "https://gateway.example.com"
    assert mdm_config.resolve_llm_routing(managed) is True


def test_effective_backend_settings_include_raw_routing_values() -> None:
    settings = _effective_backend_settings(
        {
            "llm_routing": True,
            "llm_routing_base_url": "https://gateway.example.com",
        }
    )

    assert settings["llm_routing"] is True
    assert settings["llm_routing_base_url"] == "https://gateway.example.com"


@pytest.mark.parametrize(
    ("system", "expected"),
    [
        ("Darwin", Path("/Library/Application Support/ClaudeCode")),
        ("Windows", Path("C:/Program Files/ClaudeCode")),
        ("Linux", Path("/etc/claude-code")),
    ],
)
def test_enterprise_claude_code_managed_dir(
    system: str,
    expected: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(paths.platform, "system", lambda: system)

    assert paths.enterprise_claude_code_managed_dir() == expected
