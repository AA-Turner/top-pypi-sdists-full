from __future__ import annotations

import hashlib
import json
import os
import platform
import sys
from pathlib import Path
from unittest.mock import Mock

import pytest

from runlayer_cli import aiwatch, aiwatch_credential, mdm_config
from runlayer_cli.aiwatch_config_cache import parse_aiwatch_config
from runlayer_cli.commands.aiwatch_setup import _effective_backend_settings
from runlayer_cli.hook_install import llm_routing, paths
from runlayer_cli.hook_install.paths import InstallScope


_CLAUDE_ENV = {
    "ANTHROPIC_BASE_URL": "https://gateway.example.com/anthropic",
    "CLAUDE_CODE_API_KEY_HELPER_TTL_MS": "240000",
    "ANTHROPIC_AUTH_TOKEN": "",
    "ANTHROPIC_API_KEY": "",
    "CLAUDE_CODE_OAUTH_TOKEN": "",
    "CLAUDE_CODE_USE_BEDROCK": "",
    "CLAUDE_CODE_USE_VERTEX": "",
    "CLAUDE_CODE_USE_FOUNDRY": "",
}
_CODEX_CONFIG = (
    'model_provider = "runlayer"\n'
    "\n"
    "[model_providers.runlayer]\n"
    'name = "Runlayer"\n'
    'base_url = "https://gateway.example.com/openai/v1"\n'
    'wire_api = "responses"\n'
    "\n"
    "[model_providers.runlayer.auth]\n"
    'command = "/usr/local/bin/aiwatch"\n'
    'args = ["credential", "codex"]\n'
    "timeout_ms = 5000\n"
    "refresh_interval_ms = 240000\n"
)


@pytest.fixture
def routing_paths(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> dict[str, Path]:
    claude_path = tmp_path / "claude" / "managed-settings.json"
    codex_path = tmp_path / "codex" / "managed_config.toml"
    credential_path = (
        tmp_path / "home" / ".runlayer" / "aiwatch" / "llm-routing-credential"
    )
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
    monkeypatch.setattr(
        llm_routing,
        "_credential_target",
        lambda _scope: {"path": credential_path, "home": None},
    )
    monkeypatch.setattr(
        llm_routing,
        "resolve_credential_helper",
        lambda _scope: {"executable": "/usr/local/bin/aiwatch", "args": []},
    )
    return {
        "claude": claude_path,
        "codex": codex_path,
        "credential": credential_path,
        "cache": credential_path.with_name("llm-routing-token"),
    }


def _client_paths(routing_paths: dict[str, Path]) -> tuple[Path, Path]:
    return routing_paths["claude"], routing_paths["codex"]


def test_client_refresh_interval_drives_both_writers() -> None:
    interval = aiwatch_credential.CLIENT_REFRESH_INTERVAL_SECONDS

    assert interval == 240
    assert llm_routing._CLAUDE_HELPER_TTL_MS == str(interval * 1000)
    assert llm_routing._CODEX_AUTH_REFRESH_MS == interval * 1000


def test_route_writes_missing_client_configs(routing_paths: dict[str, Path]) -> None:
    result = llm_routing.route(
        "https://gateway.example.com/",
        scope=InstallScope.MDM,
    )

    assert result is llm_routing.RouteResult.WRITTEN
    claude = json.loads(routing_paths["claude"].read_text())
    assert claude["apiKeyHelper"] == "/usr/local/bin/aiwatch credential claude"
    assert claude["env"] == _CLAUDE_ENV
    assert routing_paths["codex"].read_text() == _CODEX_CONFIG


def test_route_detailed_reports_per_client(
    routing_paths: dict[str, Path],
) -> None:
    first = llm_routing.route_detailed(
        "https://gateway.example.com",
        scope=InstallScope.MDM,
    )
    assert first == {
        "claude_code": llm_routing.RouteResult.WRITTEN,
        "codex": llm_routing.RouteResult.WRITTEN,
    }

    routing_paths["codex"].unlink()
    second = llm_routing.route_detailed(
        "https://gateway.example.com",
        scope=InstallScope.MDM,
    )
    assert second == {
        "claude_code": llm_routing.RouteResult.UNCHANGED,
        "codex": llm_routing.RouteResult.WRITTEN,
    }

    for path in _client_paths(routing_paths):
        path.unlink()
    invalid = llm_routing.route_detailed(
        "http://gateway.example.com",
        scope=InstallScope.MDM,
    )
    assert invalid == {
        "claude_code": llm_routing.RouteResult.FAILED,
        "codex": llm_routing.RouteResult.FAILED,
    }
    assert not any(path.exists() for path in _client_paths(routing_paths))


def test_route_detailed_marks_unapplied_pending_writes_failed(
    routing_paths: dict[str, Path],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    codex_path = routing_paths["codex"]
    original_path_check = llm_routing.is_unsafe_windows_mdm_path
    monkeypatch.setattr(
        llm_routing,
        "is_unsafe_windows_mdm_path",
        lambda path, **_kwargs: path == codex_path,
    )

    missing = llm_routing.route_detailed(
        "https://gateway.example.com",
        scope=InstallScope.MDM,
    )
    assert missing == {
        "claude_code": llm_routing.RouteResult.FAILED,
        "codex": llm_routing.RouteResult.FAILED,
    }
    assert not routing_paths["claude"].exists()
    assert not codex_path.exists()

    monkeypatch.setattr(
        llm_routing,
        "is_unsafe_windows_mdm_path",
        original_path_check,
    )
    llm_routing.route("https://gateway.example.com", scope=InstallScope.MDM)
    monkeypatch.setattr(
        llm_routing,
        "is_unsafe_windows_mdm_path",
        lambda path, **_kwargs: path == codex_path,
    )

    unchanged = llm_routing.route_detailed(
        "https://gateway.example.com",
        scope=InstallScope.MDM,
    )
    assert unchanged == {
        "claude_code": llm_routing.RouteResult.UNCHANGED,
        "codex": llm_routing.RouteResult.FAILED,
    }


def test_route_detailed_apply_failure_isolated_per_client(
    routing_paths: dict[str, Path],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    original_apply = llm_routing._apply_prepared_write

    def fail_codex(prepared: llm_routing._PreparedWrite) -> None:
        if prepared["path"] == routing_paths["codex"]:
            raise OSError("denied")
        original_apply(prepared)

    monkeypatch.setattr(llm_routing, "_apply_prepared_write", fail_codex)

    detailed = llm_routing.route_detailed(
        "https://gateway.example.com",
        scope=InstallScope.MDM,
    )
    assert detailed == {
        "claude_code": llm_routing.RouteResult.WRITTEN,
        "codex": llm_routing.RouteResult.FAILED,
    }
    assert routing_paths["claude"].exists()
    assert not routing_paths["codex"].exists()
    assert (
        llm_routing.route("https://gateway.example.com", scope=InstallScope.MDM)
        is llm_routing.RouteResult.FAILED
    )


def test_current_key_returns_none_without_credential_file(
    routing_paths: dict[str, Path],
) -> None:
    assert llm_routing.current_key(scope=InstallScope.MDM) is None


def test_current_key_ignores_legacy_keys_in_client_configs(
    routing_paths: dict[str, Path],
) -> None:
    claude, codex = _client_paths(routing_paths)
    claude.parent.mkdir(parents=True)
    claude.write_text(json.dumps({"env": {"ANTHROPIC_AUTH_TOKEN": "old"}}))
    codex.parent.mkdir(parents=True)
    codex.write_text('[model_providers.runlayer]\nexperimental_bearer_token = "old"\n')

    assert llm_routing.current_key(scope=InstallScope.MDM) is None


def test_store_credential_then_current_key_round_trips(
    routing_paths: dict[str, Path],
) -> None:
    path = routing_paths["credential"]

    assert (
        llm_routing.store_credential("rlk_abc", scope=InstallScope.MDM)
        is llm_routing.RouteResult.WRITTEN
    )
    assert llm_routing.current_key(scope=InstallScope.MDM) == "rlk_abc"
    assert path.read_text() == "rlk_abc\n"
    assert (
        llm_routing.store_credential("rlk_abc", scope=InstallScope.MDM)
        is llm_routing.RouteResult.UNCHANGED
    )
    assert (
        llm_routing.store_credential("rlk_def", scope=InstallScope.MDM)
        is llm_routing.RouteResult.DRIFTED
    )
    assert path.read_text() == "rlk_def\n"
    assert not list(path.parent.glob("*.backup_*"))


@pytest.mark.skipif(os.name != "posix", reason="requires POSIX permission bits")
def test_store_credential_writes_0600_and_repairs_mode(
    routing_paths: dict[str, Path],
) -> None:
    path = routing_paths["credential"]

    llm_routing.store_credential("rlk_abc", scope=InstallScope.MDM)
    assert path.stat().st_mode & 0o777 == 0o600
    path.chmod(0o644)

    assert (
        llm_routing.store_credential("rlk_abc", scope=InstallScope.MDM)
        is llm_routing.RouteResult.DRIFTED
    )
    assert path.stat().st_mode & 0o777 == 0o600


def test_store_credential_reowns_in_mdm_scope_only(
    routing_paths: dict[str, Path],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    reown = Mock()
    monkeypatch.setattr(llm_routing, "_reown_to_console_user", reown)

    llm_routing.store_credential("rlk_mdm", scope=InstallScope.MDM)
    reown.assert_called_once_with(routing_paths["credential"])
    reown.reset_mock()

    # An unchanged file is re-owned again so a failed re-own still converges.
    assert (
        llm_routing.store_credential("rlk_mdm", scope=InstallScope.MDM)
        is llm_routing.RouteResult.UNCHANGED
    )
    reown.assert_called_once_with(routing_paths["credential"])
    routing_paths["credential"].unlink()
    reown.reset_mock()

    llm_routing.store_credential("rlk_user", scope=InstallScope.USER)
    reown.assert_not_called()


@pytest.mark.skipif(os.name != "posix", reason="requires POSIX symlinks")
@pytest.mark.parametrize("scope", [InstallScope.USER, InstallScope.MDM])
def test_current_key_refuses_symlink(
    scope: InstallScope,
    routing_paths: dict[str, Path],
) -> None:
    path = routing_paths["credential"]
    target = path.parent / "real-credential"
    target.parent.mkdir(parents=True)
    target.write_text("rlk_abc\n")
    path.symlink_to(target)

    with pytest.raises(OSError):
        llm_routing.current_key(scope=scope)


@pytest.mark.parametrize(
    "content",
    [
        b"a b\n",
        b"",
        b"x" * (llm_routing.MAX_CREDENTIAL_BYTES + 1) + b"\n",
        b"\xff\xfe not utf-8\n",
    ],
)
def test_current_key_treats_malformed_credential_as_absent(
    content: bytes,
    routing_paths: dict[str, Path],
) -> None:
    path = routing_paths["credential"]
    path.parent.mkdir(parents=True)
    path.write_bytes(content)

    assert llm_routing.current_key(scope=InstallScope.MDM) is None
    assert (
        llm_routing.store_credential("rlk_new", scope=InstallScope.MDM)
        is not llm_routing.RouteResult.UNCHANGED
    )
    assert path.read_text() == "rlk_new\n"


def test_device_key_hash_matches_backend_sha256() -> None:
    assert (
        llm_routing.device_key_hash("llm-device-abc")
        == hashlib.sha256(b"llm-device-abc").hexdigest()
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
        scope=InstallScope.MDM,
    )

    assert result is llm_routing.RouteResult.DRIFTED
    assert "credential" in path.read_text()


def test_route_merges_foreign_claude_settings(routing_paths: dict[str, Path]) -> None:
    path = routing_paths["claude"]
    path.parent.mkdir(parents=True)
    path.write_text(
        json.dumps(
            {
                "permissions": {"allow": ["Read"]},
                "env": {"FOREIGN_ENV": "kept"},
            }
        )
    )

    result = llm_routing.route(
        "https://gateway.example.com",
        scope=InstallScope.MDM,
    )

    assert result is llm_routing.RouteResult.DRIFTED
    claude = json.loads(path.read_text())
    assert claude["permissions"] == {"allow": ["Read"]}
    assert claude["env"]["FOREIGN_ENV"] == "kept"
    assert claude["env"]["ANTHROPIC_BASE_URL"] == _CLAUDE_ENV["ANTHROPIC_BASE_URL"]
    assert claude["env"]["ANTHROPIC_AUTH_TOKEN"] == ""


def test_route_is_unchanged_when_both_configs_match(
    routing_paths: dict[str, Path],
) -> None:
    first = llm_routing.route(
        "https://gateway.example.com",
        scope=InstallScope.MDM,
    )
    second = llm_routing.route(
        "https://gateway.example.com",
        scope=InstallScope.MDM,
    )

    assert first is llm_routing.RouteResult.WRITTEN
    assert second is llm_routing.RouteResult.UNCHANGED
    assert not list(routing_paths["claude"].parent.glob("*.backup_*.json"))
    assert not list(routing_paths["codex"].parent.glob("*.backup_*.toml"))


def test_route_replaces_legacy_plaintext_configs(
    routing_paths: dict[str, Path],
) -> None:
    claude, codex = _client_paths(routing_paths)
    claude.parent.mkdir(parents=True)
    claude.write_text(
        json.dumps(
            {
                "env": {
                    "ANTHROPIC_AUTH_TOKEN": "old-key",
                    "ANTHROPIC_API_KEY": "old-key",
                }
            }
        )
    )
    codex.parent.mkdir(parents=True)
    codex.write_text(
        'model_provider = "runlayer"\n\n'
        "[model_providers.runlayer]\n"
        'name = "Runlayer"\n'
        'base_url = "https://gateway.example.com/openai/v1"\n'
        'wire_api = "responses"\n'
        'experimental_bearer_token = "old-key"\n'
    )

    result = llm_routing.route(
        "https://gateway.example.com",
        scope=InstallScope.MDM,
    )

    assert result is llm_routing.RouteResult.DRIFTED
    settings = json.loads(claude.read_text())
    assert settings["env"]["ANTHROPIC_AUTH_TOKEN"] == ""
    assert settings["env"]["ANTHROPIC_API_KEY"] == ""
    assert settings["apiKeyHelper"].endswith("credential claude")
    codex_text = codex.read_text()
    assert "[model_providers.runlayer.auth]" in codex_text
    for forbidden in (
        "experimental_bearer_token",
        "env_key",
        "requires_openai_auth",
        "old-key",
    ):
        assert forbidden not in codex_text


@pytest.mark.parametrize(
    "stale_line",
    ['env_key = "OPENAI_API_KEY"', '"experimental_bearer_token" = "stale"'],
)
def test_codex_route_repairs_extra_credential_slot(
    stale_line: str,
    routing_paths: dict[str, Path],
) -> None:
    llm_routing.route("https://gateway.example.com", scope=InstallScope.MDM)
    path = routing_paths["codex"]
    path.write_text(
        path.read_text().replace(
            "\n[model_providers.runlayer.auth]",
            f"\n{stale_line}\n\n[model_providers.runlayer.auth]",
        )
    )

    result = llm_routing.route(
        "https://gateway.example.com",
        scope=InstallScope.MDM,
    )

    assert result is llm_routing.RouteResult.DRIFTED
    assert "env_key" not in path.read_text()
    assert "experimental_bearer_token" not in path.read_text()


@pytest.mark.parametrize(
    "helper",
    [
        "/usr/local/bin/aiwatch credential claude",
        '"/Applications/Runlayer AIWatch/aiwatch" credential claude',
        "/opt/venv/bin/python -m runlayer_cli.aiwatch credential claude",
        "C:\\Program Files\\Runlayer\\aiwatch.exe credential claude",
    ],
)
def test_runlayer_helper_forms_are_recognized(helper: str) -> None:
    assert llm_routing._is_runlayer_helper(helper)


def test_codex_route_keeps_quoted_foreign_table_with_space(
    routing_paths: dict[str, Path],
) -> None:
    path = routing_paths["codex"]
    path.parent.mkdir(parents=True)
    foreign = '[model_providers."run layer"]\nname = "Foreign"\n'
    path.write_text(foreign)

    llm_routing.route("https://gateway.example.com", scope=InstallScope.MDM)
    assert foreign in path.read_text()

    llm_routing.unroute(scope=InstallScope.MDM)
    assert foreign in path.read_text()
    assert "[model_providers.runlayer]" not in path.read_text()


def test_codex_route_replaces_quoted_legacy_table(
    routing_paths: dict[str, Path],
) -> None:
    path = routing_paths["codex"]
    path.parent.mkdir(parents=True)
    path.write_text(
        'model_provider = "runlayer"\n\n'
        '[model_providers."runlayer"]\n'
        'name = "Runlayer"\n'
        'base_url = "https://gateway.example.com/openai/v1"\n'
        'wire_api = "responses"\n'
        'experimental_bearer_token = "old-key"\n'
    )

    result = llm_routing.route("https://gateway.example.com", scope=InstallScope.MDM)

    assert result is llm_routing.RouteResult.DRIFTED
    assert path.read_text() == _CODEX_CONFIG


def test_codex_route_repairs_missing_auth_table(
    routing_paths: dict[str, Path],
) -> None:
    llm_routing.route("https://gateway.example.com", scope=InstallScope.MDM)
    path = routing_paths["codex"]
    path.write_text(path.read_text().split("\n[model_providers.runlayer.auth]")[0])

    result = llm_routing.route(
        "https://gateway.example.com",
        scope=InstallScope.MDM,
    )

    assert result is llm_routing.RouteResult.DRIFTED
    assert "[model_providers.runlayer.auth]" in path.read_text()


@pytest.mark.parametrize("client", ["claude", "codex"])
def test_route_reports_and_repairs_client_drift(
    client: str,
    routing_paths: dict[str, Path],
) -> None:
    llm_routing.route("https://gateway.example.com", scope=InstallScope.MDM)
    path = routing_paths[client]
    path.write_text(
        path.read_text().replace("gateway.example.com", "other.example.com")
    )

    result = llm_routing.route(
        "https://gateway.example.com",
        scope=InstallScope.MDM,
    )

    assert result is llm_routing.RouteResult.DRIFTED
    assert "other.example.com" not in path.read_text()
    assert len(list(path.parent.glob(f"{path.stem}.backup_*{path.suffix}"))) == 1


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
    result = llm_routing.route(base_url, scope=scope)

    assert result is llm_routing.RouteResult.FAILED
    assert not any(path.exists() for path in _client_paths(routing_paths))


def test_route_allows_user_scope_loopback_http(
    routing_paths: dict[str, Path],
) -> None:
    result = llm_routing.route(
        "http://127.0.0.1:8190",
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
def test_route_user_scope_writes_private_config_files(
    routing_paths: dict[str, Path],
) -> None:
    for path in _client_paths(routing_paths):
        path.parent.mkdir(parents=True)
        path.write_text("{}" if path.suffix == ".json" else "")
        path.chmod(0o644)

    result = llm_routing.route(
        "https://gateway.example.com",
        scope=InstallScope.USER,
    )

    assert result is llm_routing.RouteResult.DRIFTED
    for path in _client_paths(routing_paths):
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
        scope=InstallScope.USER,
    )
    for path in _client_paths(routing_paths):
        path.chmod(0o644)

    second = llm_routing.route(
        "https://gateway.example.com",
        scope=InstallScope.USER,
    )

    assert first is llm_routing.RouteResult.WRITTEN
    assert second is llm_routing.RouteResult.DRIFTED
    for path in _client_paths(routing_paths):
        assert path.stat().st_mode & 0o777 == 0o600


def test_route_ignores_user_scope_mode_on_windows(
    routing_paths: dict[str, Path],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    real_read = llm_routing.maybe_safe_read_file

    def windows_read(path: Path, *, home: Path | None, max_bytes: int | None = None):
        existing = real_read(path, home=home, max_bytes=max_bytes)
        if existing is not None:
            existing["mode"] = 0o666
        return existing

    monkeypatch.setattr(platform, "system", lambda: "Windows")
    monkeypatch.setattr(llm_routing, "maybe_safe_read_file", windows_read)

    first = llm_routing.route(
        "https://gateway.example.com",
        scope=InstallScope.USER,
    )
    second = llm_routing.route(
        "https://gateway.example.com",
        scope=InstallScope.USER,
    )

    assert first is llm_routing.RouteResult.WRITTEN
    assert second is llm_routing.RouteResult.UNCHANGED
    for path in _client_paths(routing_paths):
        assert not list(path.parent.glob(f"{path.stem}.backup_*{path.suffix}"))


@pytest.mark.skipif(os.name != "posix", reason="requires POSIX permission bits")
def test_route_mdm_scope_keeps_targets_readable_and_backups_private(
    routing_paths: dict[str, Path],
) -> None:
    first = llm_routing.route(
        "https://gateway.example.com",
        scope=InstallScope.MDM,
    )
    second = llm_routing.route(
        "https://new-gateway.example.com",
        scope=InstallScope.MDM,
    )

    assert first is llm_routing.RouteResult.WRITTEN
    assert second is llm_routing.RouteResult.DRIFTED
    for path in _client_paths(routing_paths):
        assert path.stat().st_mode & 0o777 == 0o644
        backups = list(path.parent.glob(f"{path.stem}.backup_*{path.suffix}"))
        assert len(backups) == 1
        assert backups[0].stat().st_mode & 0o777 == 0o600


def test_unroute_removes_only_routing_config(
    routing_paths: dict[str, Path],
) -> None:
    claude, codex = _client_paths(routing_paths)
    claude.parent.mkdir(parents=True)
    claude.write_text(
        json.dumps(
            {
                "permissions": {"allow": ["Read"]},
                "env": {"FOREIGN_ENV": "kept"},
            }
        )
    )
    codex.parent.mkdir(parents=True)
    codex.write_text(
        'approval_policy = "on-request"\n[features]\nhooks = true\nmodel = "gpt-5"\n'
    )
    llm_routing.route("https://gateway.example.com", scope=InstallScope.MDM)

    llm_routing.unroute(scope=InstallScope.MDM)
    llm_routing.unroute(scope=InstallScope.MDM)

    assert json.loads(claude.read_text()) == {
        "permissions": {"allow": ["Read"]},
        "env": {"FOREIGN_ENV": "kept"},
    }
    codex_text = codex.read_text()
    assert "[model_providers.runlayer]" not in codex_text
    assert "[model_providers.runlayer.auth]" not in codex_text
    assert 'model_provider = "runlayer"' not in codex_text
    assert 'approval_policy = "on-request"' in codex_text
    assert "[features]\nhooks = true" in codex_text
    assert 'model = "gpt-5"' in codex_text


@pytest.mark.parametrize(
    "foreign_helper",
    ["/opt/foreign/helper", "/opt/acme/credential claude"],
)
def test_unroute_keeps_foreign_api_key_helper(
    foreign_helper: str,
    routing_paths: dict[str, Path],
) -> None:
    path = routing_paths["claude"]
    path.parent.mkdir(parents=True)
    content = (
        json.dumps(
            {
                "apiKeyHelper": foreign_helper,
                "env": {"FOREIGN_ENV": "kept"},
            },
            indent=2,
        )
        + "\n"
    )
    path.write_text(content)

    llm_routing.unroute(scope=InstallScope.MDM)

    assert path.read_text() == content


def test_unroute_deletes_credential_file(routing_paths: dict[str, Path]) -> None:
    llm_routing.store_credential("rlk_abc", scope=InstallScope.MDM)
    llm_routing.route("https://gateway.example.com", scope=InstallScope.MDM)

    llm_routing.unroute(scope=InstallScope.MDM)
    llm_routing.unroute(scope=InstallScope.MDM)

    assert not routing_paths["credential"].exists()


def test_unroute_deletes_token_cache_with_credential(
    routing_paths: dict[str, Path],
) -> None:
    llm_routing.store_credential("rlk_abc", scope=InstallScope.MDM)
    llm_routing.route("https://gateway.example.com", scope=InstallScope.MDM)
    routing_paths["cache"].write_bytes(b"cached")

    llm_routing.unroute(scope=InstallScope.MDM)
    llm_routing.unroute(scope=InstallScope.MDM)

    assert not routing_paths["cache"].exists()
    assert not routing_paths["credential"].exists()


def test_unroute_reports_credential_it_could_not_remove(
    routing_paths: dict[str, Path],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    llm_routing.store_credential("rlk_abc", scope=InstallScope.MDM)
    monkeypatch.setattr(llm_routing, "maybe_safe_unlink", lambda _path, *, home: False)

    with pytest.raises(OSError):
        llm_routing.unroute(scope=InstallScope.MDM)

    assert routing_paths["credential"].exists()


def test_unroute_reports_token_cache_it_could_not_remove(
    routing_paths: dict[str, Path],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    llm_routing.store_credential("rlk_abc", scope=InstallScope.MDM)
    routing_paths["cache"].write_bytes(b"cached")
    real_unlink = llm_routing.maybe_safe_unlink

    def unlink(path: Path, *, home: Path | None) -> bool:
        if path == routing_paths["cache"]:
            return False
        return real_unlink(path, home=home)

    monkeypatch.setattr(llm_routing, "maybe_safe_unlink", unlink)

    with pytest.raises(OSError):
        llm_routing.unroute(scope=InstallScope.MDM)

    # The cache failure is reported, but never leaves the credential on disk.
    assert not routing_paths["credential"].exists()


def test_store_credential_rewrite_leaves_token_cache_alone(
    routing_paths: dict[str, Path],
) -> None:
    """The cache is bound to its credential by fingerprint, so a rewrite never
    has to touch it: an undeletable cache must not block the new key."""
    assert (
        llm_routing.store_credential("rlk_a", scope=InstallScope.MDM)
        == llm_routing.RouteResult.WRITTEN
    )
    routing_paths["cache"].write_bytes(b"cached")
    assert (
        llm_routing.store_credential("rlk_b", scope=InstallScope.MDM)
        == llm_routing.RouteResult.DRIFTED
    )
    assert routing_paths["cache"].exists()
    assert routing_paths["credential"].read_text() == "rlk_b\n"


def test_credential_file_mdm_requires_console_user(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
    monkeypatch.setattr(
        "runlayer_cli.hook_install.console_user.find_console_user_home",
        lambda: None,
    )

    assert llm_routing.credential_file(InstallScope.USER) == (
        tmp_path / ".runlayer" / "aiwatch" / "llm-routing-credential"
    )
    with pytest.raises(OSError):
        llm_routing.credential_file(InstallScope.MDM)

    console_home = tmp_path / "console"
    monkeypatch.setattr(
        "runlayer_cli.hook_install.console_user.find_console_user_home",
        lambda: console_home,
    )
    monkeypatch.setattr(llm_routing.platform, "system", lambda: "Darwin")
    target = llm_routing._credential_target(InstallScope.MDM)
    assert target == {
        "path": console_home / ".runlayer" / "aiwatch" / "llm-routing-credential",
        "home": console_home,
    }


def test_unroute_is_noop_without_files(routing_paths: dict[str, Path]) -> None:
    llm_routing.unroute(scope=InstallScope.MDM)
    assert not any(path.exists() for path in routing_paths.values())


def test_unroute_preserves_foreign_codex_provider(
    routing_paths: dict[str, Path],
) -> None:
    path = routing_paths["codex"]
    path.parent.mkdir(parents=True)
    content = 'model_provider = "openai"\nmodel = "gpt-5"\n'
    path.write_text(content)

    llm_routing.unroute(scope=InstallScope.MDM)

    assert path.read_text() == content


def test_unroute_attempts_codex_when_claude_settings_are_invalid(
    routing_paths: dict[str, Path],
) -> None:
    llm_routing.route("https://gateway.example.com", scope=InstallScope.MDM)
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
        scope=InstallScope.MDM,
    )

    assert result is llm_routing.RouteResult.FAILED
    assert not any(path.exists() for path in _client_paths(routing_paths))


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


def test_resolve_credential_helper_mdm_uses_protected_symlink(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    symlink = tmp_path / "usr-local-bin-aiwatch"
    monkeypatch.setattr(paths.platform, "system", lambda: "Darwin")
    monkeypatch.setattr(paths, "_PREFERRED_SYMLINK_UNIX", symlink)
    monkeypatch.setattr(paths, "resolve_hook_binary", lambda: None)

    with pytest.raises(FileNotFoundError):
        paths.resolve_credential_helper(InstallScope.MDM)

    frozen = tmp_path / "bundle" / "aiwatch"
    monkeypatch.setattr(paths, "resolve_hook_binary", lambda: frozen)
    assert paths.resolve_credential_helper(InstallScope.MDM) == {
        "executable": str(frozen),
        "args": [],
    }

    symlink.touch()
    assert paths.resolve_credential_helper(InstallScope.MDM) == {
        "executable": str(symlink),
        "args": [],
    }


def test_route_fails_without_helper_binary(
    routing_paths: dict[str, Path],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def missing(_scope: InstallScope) -> paths.HelperCommand:
        raise FileNotFoundError("no aiwatch binary on disk for the helper")

    monkeypatch.setattr(llm_routing, "resolve_credential_helper", missing)

    result = llm_routing.route("https://gateway.example.com", scope=InstallScope.MDM)

    assert result is llm_routing.RouteResult.FAILED
    assert not routing_paths["claude"].exists()
    assert not routing_paths["codex"].exists()


def test_resolve_credential_helper_user_uses_invoked_aiwatch(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    invoked = tmp_path / "aiwatch"
    invoked.touch()
    monkeypatch.setattr(paths, "resolve_hook_binary", lambda: None)
    monkeypatch.setattr(paths.sys, "argv", [str(invoked)])
    monkeypatch.setattr(paths.sys, "frozen", False, raising=False)

    assert paths.resolve_credential_helper(InstallScope.USER) == {
        "executable": str(invoked.resolve()),
        "args": [],
    }


def test_resolve_credential_helper_user_falls_back_to_module(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(paths, "resolve_hook_binary", lambda: None)
    monkeypatch.setattr(paths.shutil, "which", lambda _name: None)
    monkeypatch.setattr(paths.sys, "argv", ["x.py"])

    assert paths.resolve_credential_helper(InstallScope.USER) == {
        "executable": sys.executable,
        "args": ["-m", "runlayer_cli.aiwatch"],
    }


def test_helper_command_rendering_quotes_and_appends_client() -> None:
    helper: paths.HelperCommand = {
        "executable": "/Applications/Runlayer AIWatch/aiwatch",
        "args": ["-m", "runlayer_cli.aiwatch"],
    }

    assert paths.render_claude_helper_command(helper) == (
        '"/Applications/Runlayer AIWatch/aiwatch" '
        "-m runlayer_cli.aiwatch credential claude"
    )
    assert paths.codex_helper_args(helper) == [
        "-m",
        "runlayer_cli.aiwatch",
        "credential",
        "codex",
    ]


def test_credential_subcommand_constants_agree() -> None:
    assert (
        aiwatch.CREDENTIAL_SUBCOMMAND
        == paths._CREDENTIAL_SUBCOMMAND
        == aiwatch_credential.CREDENTIAL_SUBCOMMAND
    )
