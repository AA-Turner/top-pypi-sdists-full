"""End-to-end install tests for ``aiwatch setup hooks install``.

Drives the real Typer CLI with ``install_client`` **not** mocked, then asserts
the on-disk client config contains exactly the expected event set. This closes
the gap left by the unit tests in ``tests/test_aiwatch_setup_hooks.py`` (which
mock ``install_client`` and never verify the written events) — i.e. the
ENG-3184 failure mode where the command returns 0 but the events are not
installed correctly.

Exercises every install option: all 4 clients, ``--user`` / ``--mdm`` scope,
and enforcement-only vs full-pipeline event sets (default / ``Sessions=false``
/ ``--all-events``).
"""

from __future__ import annotations

import contextlib
import json
from pathlib import Path
from unittest.mock import patch

import pytest
import yaml
from typer.testing import CliRunner

from runlayer_cli.aiwatch import app as aiwatch_app
from runlayer_cli.config import Config
from runlayer_cli.enrollment import enrollment_marker_path
from runlayer_cli.hook_install import clients as clients_module
from runlayer_cli.hook_install.clients import (
    CONSOLE_HOME_CLIENTS,
    Client,
    expected_event_names,
    iter_supported_clients,
)

pytestmark = pytest.mark.no_backend_e2e

runner = CliRunner()

# Patched stand-in for the on-disk aiwatch binary (no frozen bundle in CI; the
# real-binary path is covered by the Tier 2 frozen tests under tests/frozen/).
HOOK_COMMAND = "/usr/local/bin/aiwatch hook"
HOST = "https://t.example.com"

# Per-client user-scope config dir name (under HOME) + file name.
_USER_DIR: dict[Client, str] = {
    Client.CURSOR: ".cursor",
    Client.CLAUDE_CODE: ".claude",
    Client.CODEX: ".codex",
    Client.HERMES: ".hermes",
}
_USER_FILE: dict[Client, str] = {
    Client.CURSOR: "hooks.json",
    Client.CLAUDE_CODE: "settings.json",
    Client.CODEX: "hooks.json",
    Client.HERMES: "config.yaml",
}
# MDM scope writes scope-specific filenames into the enterprise dir. Claude
# Code managed-settings hooks regressed (ENG-3204), so its MDM destination is
# the console user's ~/.claude/settings.json (user hooks still fire).
_MDM_FILE: dict[Client, str] = {
    Client.CURSOR: "hooks.json",
    Client.CLAUDE_CODE: "settings.json",
    Client.CODEX: "hooks.json",
    Client.HERMES: "config.yaml",
}
_ENTERPRISE_ATTR: dict[Client, str] = {
    Client.CURSOR: "enterprise_cursor_dir",
    Client.CLAUDE_CODE: "enterprise_claude_code_dir",
    Client.CODEX: "enterprise_codex_dir",
    Client.HERMES: "enterprise_hermes_dir",
}

# (extra_args, managed_config, expected include_pipeline)
_EVENT_MODES = [
    pytest.param([], {}, True, id="default-full-pipeline"),
    pytest.param([], {"sessions": False}, False, id="sessions-false-enforcement-only"),
    pytest.param(
        ["--all-events"],
        {"sessions": False},
        True,
        id="all-events-overrides-sessions-false",
    ),
]


def _config_with_secret(host: str = HOST) -> Config:
    return Config(
        default_host=host,
        hosts={"t.example.com": {"url": host, "secret": "rl_user_existing"}},
    )


def _config_no_secret(host: str = HOST) -> Config:
    return Config(default_host=host)


def _write_console_user_enrolled(home: Path, host: str = HOST) -> None:
    """Drop the per-host enrollment marker (MDM credential-gate witness)."""
    marker = enrollment_marker_path(host, home=home)
    marker.parent.mkdir(parents=True, exist_ok=True)
    marker.touch()


def _load_hooks_section(client: Client, path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    data = yaml.safe_load(text) if client == Client.HERMES else json.loads(text)
    assert isinstance(data, dict), f"config at {path} is not a mapping"
    hooks = data.get("hooks", {})
    assert isinstance(hooks, dict)
    return hooks


def _runlayer_events(client: Client, hooks: dict) -> tuple[set[str], list[str]]:
    """Return ``(event_names, commands)`` for entries in *hooks*.

    Cursor / Hermes carry a top-level ``command`` per entry; Claude Code / Codex
    nest under ``hooks[].command``. On a fresh dir every entry is ours.
    """
    names: set[str] = set()
    commands: list[str] = []
    for event, entries in hooks.items():
        for entry in entries:
            if client in (Client.CLAUDE_CODE, Client.CODEX):
                cmd = entry["hooks"][0]["command"]
            else:
                cmd = entry["command"]
            commands.append(cmd)
            names.add(event)
    return names, commands


def _run_install(
    *,
    args: list[str],
    config: Config,
    managed_config: dict,
    console_home: Path | None = None,
):
    stack = contextlib.ExitStack()
    stack.enter_context(
        patch("runlayer_cli.commands.aiwatch_setup.load_config", return_value=config)
    )
    stack.enter_context(
        patch("runlayer_cli.enrollment.load_config", return_value=config)
    )
    stack.enter_context(
        patch("runlayer_cli.enrollment.read_managed_config", return_value={})
    )
    stack.enter_context(
        patch(
            "runlayer_cli.commands.aiwatch_setup.read_managed_config",
            return_value=managed_config,
        )
    )
    stack.enter_context(
        patch(
            "runlayer_cli.commands.aiwatch_setup.resolve_hook_command",
            return_value=HOOK_COMMAND,
        )
    )
    if console_home is not None:
        stack.enter_context(
            patch(
                "runlayer_cli.hook_install.credential_gate.find_console_user_home",
                return_value=console_home,
            )
        )
        # The ENG-3217 O_NOFOLLOW anchor (console_home_anchor) resolves the
        # console home from console_user.find_console_user_home; pin it too so
        # the anchor is the tmp console home, not the real machine's.
        stack.enter_context(
            patch(
                "runlayer_cli.hook_install.console_user.find_console_user_home",
                return_value=console_home,
            )
        )
    with stack:
        return runner.invoke(aiwatch_app, ["setup", "hooks", "install", *args])


def _run_check(
    *,
    args: list[str],
    config: Config,
    managed_config: dict,
    console_home: Path | None = None,
):
    stack = contextlib.ExitStack()
    stack.enter_context(
        patch("runlayer_cli.commands.aiwatch_setup.load_config", return_value=config)
    )
    stack.enter_context(
        patch("runlayer_cli.enrollment.load_config", return_value=config)
    )
    stack.enter_context(
        patch("runlayer_cli.enrollment.read_managed_config", return_value={})
    )
    stack.enter_context(
        patch(
            "runlayer_cli.commands.aiwatch_setup.read_managed_config",
            return_value=managed_config,
        )
    )
    stack.enter_context(
        patch(
            "runlayer_cli.hook_install.check.resolve_hook_command",
            return_value=HOOK_COMMAND,
        )
    )
    if console_home is not None:
        stack.enter_context(
            patch(
                "runlayer_cli.hook_install.credential_gate.find_console_user_home",
                return_value=console_home,
            )
        )
        # The ENG-3217 O_NOFOLLOW anchor (console_home_anchor) resolves the
        # console home from console_user.find_console_user_home; pin it too so
        # the anchor is the tmp console home, not the real machine's.
        stack.enter_context(
            patch(
                "runlayer_cli.hook_install.console_user.find_console_user_home",
                return_value=console_home,
            )
        )
    with stack:
        return runner.invoke(aiwatch_app, ["setup", "hooks", "check", *args])


def _assert_events(client: Client, path: Path, *, include_pipeline: bool) -> None:
    assert path.exists(), f"expected config at {path}"
    hooks = _load_hooks_section(client, path)
    names, commands = _runlayer_events(client, hooks)

    assert names == expected_event_names(client, include_pipeline=include_pipeline)
    assert commands, "no Runlayer hook commands written"
    for cmd in commands:
        assert cmd.endswith(f"hook --client {client.value}"), cmd

    if not include_pipeline:
        pipeline_only = expected_event_names(
            client, include_pipeline=True
        ) - expected_event_names(client, include_pipeline=False)
        assert pipeline_only, f"{client.value} has no pipeline-only events to exclude"
        assert not (names & pipeline_only), (
            f"enforcement-only install leaked pipeline events: {names & pipeline_only}"
        )


@pytest.fixture
def home(tmp_path, monkeypatch) -> Path:
    monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
    return tmp_path


class TestUserScopeInstall:
    @pytest.mark.parametrize("client", iter_supported_clients(), ids=lambda c: c.value)
    @pytest.mark.parametrize(
        "extra_args, managed_config, include_pipeline", _EVENT_MODES
    )
    def test_install_writes_expected_events(
        self, home, client, extra_args, managed_config, include_pipeline
    ):
        (home / _USER_DIR[client]).mkdir()

        result = _run_install(
            args=["--user", "--client", client.value, *extra_args],
            config=_config_with_secret(),
            managed_config=managed_config,
        )
        assert result.exit_code == 0, result.output

        path = home / _USER_DIR[client] / _USER_FILE[client]
        _assert_events(client, path, include_pipeline=include_pipeline)

        if client == Client.CODEX:
            toml = (home / _USER_DIR[client] / "config.toml").read_text()
            assert "[features]" in toml
            assert "hooks = true" in toml

    def test_install_all_clients_in_one_run(self, home):
        for client in iter_supported_clients():
            (home / _USER_DIR[client]).mkdir()

        result = _run_install(
            args=["--user"], config=_config_with_secret(), managed_config={}
        )
        assert result.exit_code == 0, result.output

        for client in iter_supported_clients():
            path = home / _USER_DIR[client] / _USER_FILE[client]
            _assert_events(client, path, include_pipeline=True)


class TestMDMScopeInstall:
    @pytest.mark.parametrize("client", iter_supported_clients(), ids=lambda c: c.value)
    @pytest.mark.parametrize(
        "extra_args, managed_config, include_pipeline", _EVENT_MODES
    )
    def test_install_writes_expected_events(
        self, home, monkeypatch, client, extra_args, managed_config, include_pipeline
    ):
        console_home = home / "ConsoleUser"
        _write_console_user_enrolled(console_home)
        # Console-home clients (Claude Code / Hermes) write into ~/.<client> and
        # their ENG-3217 anchor is the console home, so config_dir.parent must be
        # the console home (mirrors production). Cursor/Codex target a real
        # root-owned enterprise dir unrelated to the console home.
        if client in CONSOLE_HOME_CLIENTS:
            enterprise_root = console_home / _USER_DIR[client]
        else:
            enterprise_root = home / "enterprise" / client.value
        monkeypatch.setattr(
            clients_module, _ENTERPRISE_ATTR[client], lambda: enterprise_root
        )

        result = _run_install(
            args=["--mdm", "--client", client.value, *extra_args],
            config=_config_no_secret(),
            managed_config=managed_config,
            console_home=console_home,
        )
        assert result.exit_code == 0, result.output

        path = enterprise_root / _MDM_FILE[client]
        _assert_events(client, path, include_pipeline=include_pipeline)

        if client == Client.CODEX:
            toml = (enterprise_root / "managed_config.toml").read_text()
            assert "[features]" in toml
            assert "hooks = true" in toml


class TestInstallThenCheck:
    """Installing then checking the same configs must report no drift (exit 0)."""

    def test_user_scope_check_ok_after_install(self, home):
        for client in iter_supported_clients():
            (home / _USER_DIR[client]).mkdir()

        install = _run_install(
            args=["--user"], config=_config_with_secret(), managed_config={}
        )
        assert install.exit_code == 0, install.output

        check = _run_check(
            args=["--user"], config=_config_with_secret(), managed_config={}
        )
        assert check.exit_code == 0, check.output
