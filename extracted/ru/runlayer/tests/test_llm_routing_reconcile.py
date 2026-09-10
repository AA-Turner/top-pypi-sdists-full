"""Hourly reconcile: LLM routing step + ``llm_routing`` check-ins."""

from __future__ import annotations

import errno
import json
import os
from pathlib import Path
from typing import TypedDict
from unittest.mock import Mock

import httpx
import pytest
from typer.testing import CliRunner

from runlayer_cli.aiwatch import app
from runlayer_cli.hook_install import llm_routing
from runlayer_cli.hook_install.clients import InstallResult
from runlayer_cli.symbols import WARN

pytestmark = pytest.mark.real_llm_routing


runner = CliRunner()
_ROUTING_ENV_KEYS = {
    "ANTHROPIC_BASE_URL",
    "CLAUDE_CODE_API_KEY_HELPER_TTL_MS",
    "ANTHROPIC_AUTH_TOKEN",
    "ANTHROPIC_API_KEY",
    "CLAUDE_CODE_OAUTH_TOKEN",
    "CLAUDE_CODE_USE_BEDROCK",
    "CLAUDE_CODE_USE_VERTEX",
    "CLAUDE_CODE_USE_FOUNDRY",
}


class _RoutingHarness(TypedDict):
    claude: Path
    codex: Path
    credential: Path
    cache: Path
    managed: dict[str, object]
    responses: list[object]
    payloads: list[dict[str, object]]
    submit: Mock
    install: Mock


def _managed_config() -> dict[str, object]:
    return {
        "host": "https://t.example.com",
        "org_api_key": "rl_org_secret",
        "sessions": True,
        "mode": "monitor",
        "llm_routing": True,
        "llm_routing_base_url": "https://gw.example.com",
    }


@pytest.fixture(autouse=True)
def routing_reconcile(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> _RoutingHarness:
    claude_path = tmp_path / "claude" / "managed-settings.json"
    codex_path = tmp_path / "codex" / "managed_config.toml"
    credential_path = (
        tmp_path / "home" / ".runlayer" / "aiwatch" / "llm-routing-credential"
    )
    managed = _managed_config()
    responses: list[object] = []
    payloads: list[dict[str, object]] = []

    def submit(payload: dict[str, object]) -> dict[str, object]:
        payloads.append(payload)
        response = responses.pop(0) if responses else {}
        if isinstance(response, Exception):
            raise response
        if callable(response):
            return response(payload)
        assert isinstance(response, dict)
        return response

    def install(client, **_kwargs) -> InstallResult:
        return InstallResult(
            client=client,
            config_path=tmp_path / f"fake-{client.value}.json",
            written=True,
        )

    install_mock = Mock(side_effect=install)
    submit_mock = Mock(side_effect=submit)
    monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
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
    monkeypatch.setattr(
        "runlayer_cli.commands.aiwatch_setup._install_browser_extension_step",
        lambda _managed: (False, False),
    )
    monkeypatch.setattr(
        "runlayer_cli.commands.aiwatch_setup._install_daemon_lifecycle_step",
        lambda _managed, **_kwargs: (False, False),
    )
    monkeypatch.setattr(
        "runlayer_cli.commands.aiwatch_setup._install_scan_lifecycle_step",
        lambda: (False, False),
    )
    monkeypatch.setattr(
        "runlayer_cli.commands.aiwatch_setup.sync_backend_config",
        lambda **_kwargs: False,
    )
    monkeypatch.setattr(
        "runlayer_cli.commands.aiwatch_setup.credential_present",
        lambda *_args: (True, None),
    )
    monkeypatch.setattr(
        "runlayer_cli.commands.aiwatch_setup.resolve_hook_command",
        lambda: "/usr/local/bin/aiwatch-hook",
    )
    monkeypatch.setattr(
        "runlayer_cli.commands.aiwatch_setup.install_client",
        install_mock,
    )
    monkeypatch.setattr(
        "runlayer_cli.commands.aiwatch_setup.read_managed_config",
        lambda: managed,
    )
    monkeypatch.setattr(
        "runlayer_cli.aiwatch_checkin._make_device_context",
        lambda: {
            "device_id": "device-1",
            "hostname": "DESKTOP-1",
            "os": "windows",
            "os_version": "11",
            "username": "alex",
            "org_device_id": None,
            "serial_number": "SERIAL-1",
        },
    )
    monkeypatch.setattr(
        "runlayer_cli.scan.device.get_installed_tools",
        lambda: [],
    )
    monkeypatch.setattr("runlayer_cli.aiwatch_checkin.time.sleep", lambda _delay: None)
    monkeypatch.setattr(
        "runlayer_cli.api.RunlayerClient.submit_aiwatch_checkin",
        submit_mock,
    )
    return {
        "claude": claude_path,
        "codex": codex_path,
        "credential": credential_path,
        "cache": credential_path.with_name("llm-routing-token"),
        "managed": managed,
        "responses": responses,
        "payloads": payloads,
        "submit": submit_mock,
        "install": install_mock,
    }


def _llm_payloads(routing_reconcile: _RoutingHarness) -> list[dict[str, object]]:
    return [
        payload
        for payload in routing_reconcile["payloads"]
        if payload["feature"] == "llm_routing"
    ]


def _invoke_mdm(*, client: bool = True):
    args = [
        "setup",
        "hooks",
        "install",
        "--mdm",
        "--host",
        "https://t.example.com",
    ]
    if client:
        args.extend(("--client", "cursor"))
    return runner.invoke(app, args)


def _seed_routed(harness: _RoutingHarness, key: str) -> None:
    assert (
        llm_routing.store_credential(key, scope=llm_routing.InstallScope.MDM)
        is llm_routing.RouteResult.WRITTEN
    )
    assert (
        llm_routing.route(
            "https://gw.example.com",
            scope=llm_routing.InstallScope.MDM,
        )
        is llm_routing.RouteResult.WRITTEN
    )


def test_mint_path_writes_both_clients_and_reports_twice(
    routing_reconcile: _RoutingHarness,
) -> None:
    responses = routing_reconcile["responses"]
    responses.extend(
        [
            {"device_key_status": "active", "device_key": "llm-device-abc"},
            {"device_key_status": "active", "device_key": None},
        ]
    )

    result = _invoke_mdm()

    assert result.exit_code == 0, result.output
    claude_path = routing_reconcile["claude"]
    codex_path = routing_reconcile["codex"]
    credential_path = routing_reconcile["credential"]
    claude = json.loads(claude_path.read_text())
    assert credential_path.read_text() == "llm-device-abc\n"
    if os.name == "posix":
        assert credential_path.stat().st_mode & 0o777 == 0o600
    assert claude["apiKeyHelper"] == "/usr/local/bin/aiwatch credential claude"
    assert claude["env"]["ANTHROPIC_AUTH_TOKEN"] == ""
    assert "[model_providers.runlayer.auth]" in codex_path.read_text()
    assert "experimental_bearer_token" not in codex_path.read_text()
    payloads = _llm_payloads(routing_reconcile)
    assert len(payloads) == 2
    assert payloads[0]["status"] == "ok"
    assert payloads[0]["device_key_hash"] is None
    assert "error_message" not in payloads[0]
    assert payloads[1]["status"] == "ok"
    assert payloads[1]["device_key_hash"] == llm_routing.device_key_hash(
        "llm-device-abc"
    )
    assert "error_message" not in payloads[1]


def test_absent_credential_requests_rotation_and_writes_minted_key(
    routing_reconcile: _RoutingHarness,
) -> None:
    routing_reconcile["responses"].extend(
        [
            {"device_key_status": "active", "device_key": "llm-device-new"},
            {"device_key_status": "active", "device_key": None},
        ]
    )

    result = _invoke_mdm()

    assert result.exit_code == 0, result.output
    payloads = _llm_payloads(routing_reconcile)
    assert payloads[0]["device_key_hash"] is None
    assert payloads[0]["rotate"] is True
    assert routing_reconcile["credential"].read_text() == "llm-device-new\n"
    assert routing_reconcile["claude"].exists()
    assert routing_reconcile["codex"].exists()
    assert "rotate" not in payloads[1]
    assert payloads[1]["device_key_hash"] == llm_routing.device_key_hash(
        "llm-device-new"
    )


def test_steady_state_sends_single_checkin(
    routing_reconcile: _RoutingHarness,
) -> None:
    _seed_routed(routing_reconcile, "llm-device-abc")
    before = {
        "claude": routing_reconcile["claude"].read_text(),
        "codex": routing_reconcile["codex"].read_text(),
        "credential": routing_reconcile["credential"].read_text(),
    }
    routing_reconcile["responses"].append(
        {"device_key_status": "active", "device_key": None}
    )

    result = _invoke_mdm()

    assert result.exit_code == 0, result.output
    payloads = _llm_payloads(routing_reconcile)
    assert len(payloads) == 1
    assert payloads[0]["device_key_hash"] == llm_routing.device_key_hash(
        "llm-device-abc"
    )
    assert "rotate" not in payloads[0]
    assert routing_reconcile["claude"].read_text() == before["claude"]
    assert routing_reconcile["codex"].read_text() == before["codex"]
    assert routing_reconcile["credential"].read_text() == before["credential"]


@pytest.mark.skipif(os.name != "posix", reason="requires POSIX symlinks")
def test_unreadable_credential_reports_error_without_fetch(
    routing_reconcile: _RoutingHarness,
) -> None:
    credential = routing_reconcile["credential"]
    credential.parent.mkdir(parents=True)
    elsewhere = credential.parent / "elsewhere"
    elsewhere.write_text("llm-device-elsewhere\n")
    credential.symlink_to(elsewhere)
    routing_reconcile["responses"].append(
        {"device_key_status": "active", "device_key": None}
    )

    result = _invoke_mdm()

    assert result.exit_code == 0, result.output
    payloads = _llm_payloads(routing_reconcile)
    assert len(payloads) == 1
    assert payloads[0]["status"] == "error"
    assert payloads[0]["error_message"].startswith("credential:")
    assert payloads[0]["device_key_hash"] is None
    assert "rotate" not in payloads[0]
    assert not routing_reconcile["claude"].exists()
    assert not routing_reconcile["codex"].exists()


@pytest.mark.parametrize(
    "response",
    [
        pytest.param(
            {"device_key_status": "not_eligible", "device_key": None},
            id="not_eligible",
        ),
        pytest.param(
            {"device_key_status": None, "device_key": None},
            id="null_status",
        ),
        pytest.param({}, id="missing_status"),
    ],
)
def test_not_eligible_unroutes_and_reports_disabled(
    response: dict[str, object],
    routing_reconcile: _RoutingHarness,
) -> None:
    _seed_routed(routing_reconcile, "llm-device-abc")
    routing_reconcile["cache"].write_bytes(b"cached")
    routing_reconcile["responses"].append(response)

    result = _invoke_mdm()

    assert result.exit_code == 0, result.output
    claude = json.loads(routing_reconcile["claude"].read_text())
    assert not _ROUTING_ENV_KEYS & claude["env"].keys()
    assert "[model_providers.runlayer]" not in routing_reconcile["codex"].read_text()
    assert not routing_reconcile["credential"].exists()
    assert not routing_reconcile["cache"].exists()
    payloads = _llm_payloads(routing_reconcile)
    assert len(payloads) == 2
    assert payloads[0]["status"] == "ok"
    assert payloads[0]["device_key_hash"] == llm_routing.device_key_hash(
        "llm-device-abc"
    )
    assert payloads[1]["status"] == "disabled"
    assert payloads[1]["device_key_hash"] is None


def test_routing_off_unroutes_without_fetch(
    routing_reconcile: _RoutingHarness,
) -> None:
    _seed_routed(routing_reconcile, "llm-device-abc")
    routing_reconcile["cache"].write_bytes(b"cached")
    routing_reconcile["managed"]["llm_routing"] = False

    result = _invoke_mdm()

    assert result.exit_code == 0, result.output
    claude = json.loads(routing_reconcile["claude"].read_text())
    assert not _ROUTING_ENV_KEYS & claude["env"].keys()
    assert "[model_providers.runlayer]" not in routing_reconcile["codex"].read_text()
    assert not routing_reconcile["credential"].exists()
    assert not routing_reconcile["cache"].exists()
    payloads = _llm_payloads(routing_reconcile)
    assert len(payloads) == 1
    assert payloads[0]["status"] == "disabled"
    assert payloads[0]["device_key_hash"] is None


def test_self_gate_unroutes_and_exits_zero_without_checkin(
    routing_reconcile: _RoutingHarness,
) -> None:
    _seed_routed(routing_reconcile, "llm-device-abc")
    routing_reconcile["cache"].write_bytes(b"cached")
    routing_reconcile["managed"].clear()

    result = _invoke_mdm()

    assert result.exit_code == 0, result.output
    claude = json.loads(routing_reconcile["claude"].read_text())
    assert not _ROUTING_ENV_KEYS & claude["env"].keys()
    assert "[model_providers.runlayer]" not in routing_reconcile["codex"].read_text()
    assert not routing_reconcile["credential"].exists()
    assert not routing_reconcile["cache"].exists()
    routing_reconcile["submit"].assert_not_called()
    routing_reconcile["install"].assert_not_called()


def test_scan_only_branch_runs_routing_step(
    routing_reconcile: _RoutingHarness,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    managed = routing_reconcile["managed"]
    managed["sessions"] = False
    managed.pop("mode")
    monkeypatch.setattr(
        "runlayer_cli.commands.aiwatch_setup._uninstall_targets",
        lambda *_args, **_kwargs: False,
    )
    routing_reconcile["responses"].extend(
        [
            {"device_key_status": "active", "device_key": "llm-device-abc"},
            {"device_key_status": "active", "device_key": None},
        ]
    )

    result = _invoke_mdm(client=False)

    assert result.exit_code == 0, result.output
    assert routing_reconcile["claude"].exists()
    assert routing_reconcile["codex"].exists()
    payloads = _llm_payloads(routing_reconcile)
    assert len(payloads) == 2
    assert payloads[0]["device_key_hash"] is None
    assert payloads[1]["device_key_hash"] == llm_routing.device_key_hash(
        "llm-device-abc"
    )


def test_half_written_state_converges_and_reports_drifted(
    routing_reconcile: _RoutingHarness,
) -> None:
    _seed_routed(routing_reconcile, "llm-device-abc")
    routing_reconcile["codex"].unlink()
    routing_reconcile["responses"].append(
        {"device_key_status": "active", "device_key": None}
    )

    result = _invoke_mdm()

    assert result.exit_code == 0, result.output
    assert routing_reconcile["claude"].exists()
    assert routing_reconcile["codex"].exists()
    payloads = _llm_payloads(routing_reconcile)
    assert len(payloads) == 2
    assert payloads[0]["device_key_hash"] == llm_routing.device_key_hash(
        "llm-device-abc"
    )
    assert payloads[1]["status"] == "drifted"
    assert payloads[1]["error_message"] == (
        "credential: unchanged; claude_code: unchanged; codex: written"
    )


def test_configs_without_credential_present_no_hash_and_remint(
    routing_reconcile: _RoutingHarness,
) -> None:
    llm_routing.route(
        "https://gw.example.com",
        scope=llm_routing.InstallScope.MDM,
    )
    routing_reconcile["responses"].extend(
        [
            {"device_key_status": "active", "device_key": "llm-device-abc"},
            {"device_key_status": "active", "device_key": None},
        ]
    )

    result = _invoke_mdm()

    assert result.exit_code == 0, result.output
    payloads = _llm_payloads(routing_reconcile)
    assert payloads[0]["device_key_hash"] is None
    assert routing_reconcile["credential"].read_text() == "llm-device-abc\n"
    assert payloads[1]["device_key_hash"] == llm_routing.device_key_hash(
        "llm-device-abc"
    )
    assert payloads[1]["status"] == "ok"
    assert "error_message" not in payloads[1]


def test_credential_write_failure_reports_error_and_skips_configs(
    routing_reconcile: _RoutingHarness,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    original_write = llm_routing._write_config

    def fail_credential(path: Path, *args, **kwargs) -> None:
        if path == routing_reconcile["credential"]:
            raise OSError(errno.EACCES, "denied")
        original_write(path, *args, **kwargs)

    monkeypatch.setattr(llm_routing, "_write_config", fail_credential)
    routing_reconcile["responses"].append(
        {"device_key_status": "active", "device_key": "llm-device-abc"}
    )

    result = _invoke_mdm()

    assert result.exit_code == 0, result.output
    assert not routing_reconcile["claude"].exists()
    assert not routing_reconcile["codex"].exists()
    payloads = _llm_payloads(routing_reconcile)
    assert payloads[1]["status"] == "error"
    assert payloads[1]["error_message"].startswith("credential:")
    assert payloads[1]["device_key_hash"] is None


@pytest.mark.skipif(os.name != "posix", reason="requires POSIX permission bits")
def test_credential_mode_drift_is_repaired_and_reported(
    routing_reconcile: _RoutingHarness,
) -> None:
    _seed_routed(routing_reconcile, "llm-device-abc")
    routing_reconcile["credential"].chmod(0o644)
    routing_reconcile["responses"].append(
        {"device_key_status": "active", "device_key": None}
    )

    result = _invoke_mdm()

    assert result.exit_code == 0, result.output
    payloads = _llm_payloads(routing_reconcile)
    assert payloads[1]["status"] == "drifted"
    assert payloads[1]["error_message"] == (
        "credential: drifted; claude_code: unchanged; codex: unchanged"
    )
    assert routing_reconcile["credential"].stat().st_mode & 0o777 == 0o600


def test_writer_failure_reports_error_without_failing_command(
    routing_reconcile: _RoutingHarness,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    original_apply = llm_routing._apply_prepared_write

    def fail_codex(prepared: llm_routing._PreparedWrite) -> None:
        if prepared["path"] == routing_reconcile["codex"]:
            raise OSError(errno.EACCES, "denied")
        original_apply(prepared)

    monkeypatch.setattr(llm_routing, "_apply_prepared_write", fail_codex)
    routing_reconcile["responses"].append(
        {"device_key_status": "active", "device_key": "llm-device-abc"}
    )

    result = _invoke_mdm()

    assert result.exit_code == 0, result.output
    payloads = _llm_payloads(routing_reconcile)
    assert len(payloads) == 2
    assert payloads[1]["status"] == "error"
    assert payloads[1]["error_message"] == (
        "credential: written; claude_code: written; codex: failed"
    )
    assert payloads[1]["device_key_hash"] == llm_routing.device_key_hash(
        "llm-device-abc"
    )
    assert "llm_routing" in result.output
    assert "error" in result.output


def test_backend_unreachable_leaves_disk_untouched(
    routing_reconcile: _RoutingHarness,
) -> None:
    routing_reconcile["submit"].side_effect = httpx.ConnectError("refused")

    result = _invoke_mdm()

    assert result.exit_code == 0, result.output
    assert not routing_reconcile["claude"].exists()
    assert not routing_reconcile["codex"].exists()
    assert not routing_reconcile["credential"].exists()
    assert routing_reconcile["submit"].call_count == 3
    assert "llm_routing" in result.output
    assert WARN in result.output


def test_user_scope_skips_routing(routing_reconcile: _RoutingHarness) -> None:
    from runlayer_cli.commands.aiwatch_setup import _llm_routing_step

    wrote = _llm_routing_step(
        routing_reconcile["managed"],
        scope=llm_routing.InstallScope.USER,
        host="https://t.example.com",
        key="rl_org_secret",
    )

    assert wrote is False
    routing_reconcile["submit"].assert_not_called()
    assert not routing_reconcile["claude"].exists()
    assert not routing_reconcile["codex"].exists()


def test_active_without_any_key_reports_error(
    routing_reconcile: _RoutingHarness,
) -> None:
    routing_reconcile["responses"].append(
        {"device_key_status": "active", "device_key": None}
    )

    result = _invoke_mdm()

    assert result.exit_code == 0, result.output
    assert not routing_reconcile["claude"].exists()
    assert not routing_reconcile["codex"].exists()
    payloads = _llm_payloads(routing_reconcile)
    assert len(payloads) == 2
    assert payloads[1]["status"] == "error"
    assert payloads[1]["error_message"] == (
        "backend reported active but no device key available"
    )


def test_unexpected_writer_failure_warns_without_failing_command(
    routing_reconcile: _RoutingHarness,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fail_route(*_args, **_kwargs):
        raise RuntimeError("unexpected writer failure")

    monkeypatch.setattr(llm_routing, "route_detailed", fail_route)
    routing_reconcile["responses"].append(
        {"device_key_status": "active", "device_key": "llm-device-abc"}
    )

    result = _invoke_mdm()

    assert result.exit_code == 0, result.output
    assert WARN in result.output
    assert "llm_routing" in result.output
    assert "unexpected writer failure" in result.output


def test_partial_claude_failure_reports_minted_key_hash(
    routing_reconcile: _RoutingHarness,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The status check-in must present the key the device holds.

    A hash that misses the active key makes the backend revoke-then-mint, so
    presenting None here would strand Codex on a just-revoked key every hour.
    """
    original_apply = llm_routing._apply_prepared_write

    def fail_claude(prepared: llm_routing._PreparedWrite) -> None:
        if prepared["path"] == routing_reconcile["claude"]:
            raise OSError(errno.EACCES, "denied")
        original_apply(prepared)

    monkeypatch.setattr(llm_routing, "_apply_prepared_write", fail_claude)
    routing_reconcile["responses"].append(
        {"device_key_status": "active", "device_key": "llm-device-abc"}
    )

    result = _invoke_mdm()

    assert result.exit_code == 0, result.output
    assert "[model_providers.runlayer.auth]" in routing_reconcile["codex"].read_text()
    payloads = _llm_payloads(routing_reconcile)
    assert len(payloads) == 2
    assert payloads[1]["status"] == "error"
    assert payloads[1]["error_message"] == (
        "credential: written; claude_code: failed; codex: written"
    )
    assert payloads[1]["device_key_hash"] == llm_routing.device_key_hash(
        "llm-device-abc"
    )


def test_unreadable_claude_file_still_presents_credential_hash(
    routing_reconcile: _RoutingHarness,
) -> None:
    _seed_routed(routing_reconcile, "llm-device-abc")
    routing_reconcile["claude"].write_text("{")
    routing_reconcile["responses"].append(
        {"device_key_status": "active", "device_key": None}
    )

    result = _invoke_mdm()

    assert result.exit_code == 0, result.output
    payloads = _llm_payloads(routing_reconcile)
    expected_hash = llm_routing.device_key_hash("llm-device-abc")
    assert len(payloads) == 2
    assert payloads[0]["status"] == "ok"
    assert payloads[0]["device_key_hash"] == expected_hash
    assert payloads[1]["status"] == "error"
    assert payloads[1]["error_message"] == (
        "credential: unchanged; claude_code: failed; codex: unchanged"
    )
    assert payloads[1]["device_key_hash"] == expected_hash
    assert "[model_providers.runlayer.auth]" in routing_reconcile["codex"].read_text()
