"""End-to-end install tests for ``aiwatch setup hooks install``.

Drives the real Typer CLI with ``install_client`` **not** mocked, then asserts
the on-disk client config contains exactly the expected event set. This closes
the gap left by the unit tests in ``tests/test_aiwatch_setup_hooks.py`` (which
mock ``install_client`` and never verify the written events) — i.e. the
ENG-3184 failure mode where the command returns 0 but the events are not
installed correctly.

Exercises every install option: all supported clients, ``--user`` / ``--mdm`` scope,
and enforcement-only vs full-pipeline event sets (default / ``Sessions=false``
/ ``--all-events``).
"""

from __future__ import annotations

import contextlib
import json
import platform
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
from runlayer_cli.scan.clients import get_client_by_name

pytestmark = pytest.mark.no_backend_e2e

runner = CliRunner()

# Patched stand-in for the on-disk aiwatch binary (no frozen bundle in CI; the
# real-binary path is covered by the Tier 2 frozen tests under tests/frozen/).
HOOK_COMMAND = "/usr/local/bin/aiwatch hook"
HOST = "https://t.example.com"

# Per-client user-scope config dir name (under HOME) + file name.
_USER_DIR: dict[Client, str] = {
    Client.CURSOR: ".cursor",
    Client.VSCODE: ".copilot/hooks",
    Client.CLAUDE_CODE: ".claude",
    Client.CODEX: ".codex",
    Client.HERMES: ".hermes",
    Client.GOOSE: ".agents/plugins/runlayer-hooks",
    Client.GITHUB_COPILOT_CLI: ".copilot",
    Client.WINDSURF: ".codeium/windsurf",
    Client.QWEN_CODE: ".qwen",
    Client.GEMINI_CLI: ".gemini",
    Client.GROK_CLI: ".grok",
    # Cline has no config file: this dir holds one executable script per event.
    Client.CLINE_CLI: ".cline/hooks",
    Client.DEVIN_CLI: ".config/devin",
}
_USER_FILE: dict[Client, str] = {
    Client.CURSOR: "hooks.json",
    Client.VSCODE: "runlayer.json",
    Client.CLAUDE_CODE: "settings.json",
    Client.CODEX: "hooks.json",
    Client.HERMES: "config.yaml",
    Client.GOOSE: "hooks/hooks.json",
    Client.GITHUB_COPILOT_CLI: "settings.json",
    Client.WINDSURF: "hooks.json",
    Client.QWEN_CODE: "settings.json",
    Client.GEMINI_CLI: "settings.json",
    Client.GROK_CLI: "hooks/runlayer.json",
    # Representative script (matches config_path_for); the real assertion walks
    # the whole directory.
    Client.CLINE_CLI: "PreToolUse",
    # Devin's standalone hooks.v1.json is project-scoped, so Runlayer merges
    # into the ``hooks`` key of the user's own config.json.
    Client.DEVIN_CLI: "config.json",
}
# MDM scope writes scope-specific filenames into the enterprise dir. Claude
# Code managed-settings hooks regressed (ENG-3204), so its MDM destination is
# the console user's ~/.claude/settings.json (user hooks still fire).
_MDM_FILE: dict[Client, str] = {
    Client.CURSOR: "hooks.json",
    Client.VSCODE: "runlayer.json",
    Client.CLAUDE_CODE: "settings.json",
    Client.CODEX: "hooks.json",
    Client.HERMES: "config.yaml",
    Client.GOOSE: "hooks/hooks.json",
    Client.GITHUB_COPILOT_CLI: "runlayer.json",
    # Cascade reads the same filename at every scope; only the dir differs.
    Client.WINDSURF: "hooks.json",
    # Qwen reads settings.json at every scope; MDM targets the system dir.
    Client.QWEN_CODE: "settings.json",
    # Gemini CLI reads the same ``settings.json`` name at system scope.
    Client.GEMINI_CLI: "settings.json",
    # Grok CLI has no enterprise hook dir; MDM targets the console user's home.
    Client.GROK_CLI: "hooks/runlayer.json",
    Client.CLINE_CLI: "PreToolUse",
    # Devin has no machine-wide settings file; MDM writes the console user's copy.
    Client.DEVIN_CLI: "config.json",
}
_ENTERPRISE_ATTR: dict[Client, str] = {
    Client.CURSOR: "enterprise_cursor_dir",
    Client.VSCODE: "enterprise_vscode_dir",
    Client.CLAUDE_CODE: "enterprise_claude_code_dir",
    Client.CODEX: "enterprise_codex_dir",
    Client.HERMES: "enterprise_hermes_dir",
    Client.GOOSE: "enterprise_goose_dir",
    Client.GITHUB_COPILOT_CLI: "enterprise_github_copilot_cli_dir",
    Client.WINDSURF: "enterprise_windsurf_dir",
    Client.QWEN_CODE: "enterprise_qwen_code_dir",
    Client.GEMINI_CLI: "enterprise_gemini_cli_dir",
    Client.GROK_CLI: "enterprise_grok_cli_dir",
    Client.CLINE_CLI: "enterprise_cline_cli_dir",
    Client.DEVIN_CLI: "enterprise_devin_cli_dir",
}

# (extra_args, managed_config, expected include_pipeline)
_EVENT_MODES = [
    pytest.param([], {"sessions": True}, True, id="sessions-enabled-full-pipeline"),
    pytest.param(
        [],
        {"enforcement": True, "sessions": False},
        False,
        id="sessions-false-enforcement-only",
    ),
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


def _install_fake_cli_binary(home: Path, client: Client) -> None:
    """Seed the executable-class evidence the install presence gate requires.

    Config files alone no longer prove a client is installed, so drop a real
    executable in the location the client's presence probe checks under *home*.
    """
    if client == Client.GROK_CLI:
        # The global detector deliberately omits the collision-prone bare
        # ``grok`` name; hook installation probes GROK_HOME/bin directly.
        binary_name = "grok.exe" if platform.system() == "Windows" else "grok"
        binary = home / ".grok" / "bin" / binary_name
    else:
        definition = get_client_by_name(client.value.replace("-", "_"))
        assert definition is not None, f"no scan definition for {client.value}"
        assert definition.install_probe is not None
        binaries = definition.install_probe.cli_binaries
        assert binaries, f"{client.value} has no CLI binary to seed"

        # Windows has no execute bit; there the suffix makes a file runnable.
        suffix = ".cmd" if platform.system() == "Windows" else ""
        binary = home / ".local" / "bin" / f"{binaries[0]}{suffix}"
    binary.parent.mkdir(parents=True, exist_ok=True)
    binary.write_text("#!/bin/sh\n", encoding="utf-8")
    binary.chmod(0o755)


def _mark_user_client_installed(home: Path, client: Client) -> None:
    """Create real scanner presence signals, not hook destination directories."""
    _install_fake_cli_binary(home, client)

    if client == Client.CURSOR:
        files = [(home / ".cursor" / "mcp.json", "{}")]
    elif client == Client.VSCODE:
        files = [
            (
                home / "Library" / "Application Support" / "Code" / "User" / "mcp.json",
                "{}",
            ),
            (home / ".config" / "Code" / "User" / "mcp.json", "{}"),
            (home / "AppData" / "Roaming" / "Code" / "User" / "mcp.json", "{}"),
        ]
    elif client == Client.CLAUDE_CODE:
        files = [(home / ".claude.json", "{}")]
    elif client == Client.CODEX:
        files = [(home / ".codex" / "config.toml", 'model = "gpt-5"\n')]
    elif client == Client.HERMES:
        files = [
            (home / ".hermes" / "config.yaml", "model: auto\n"),
            (
                home / "AppData" / "Local" / "hermes" / "config.yaml",
                "model: auto\n",
            ),
        ]
    elif client == Client.GOOSE:
        files = [
            (home / ".config" / "goose" / "config.yaml", "extensions: {}\n"),
            (
                home
                / "AppData"
                / "Roaming"
                / "Block"
                / "goose"
                / "config"
                / "config.yaml",
                "extensions: {}\n",
            ),
        ]
    elif client == Client.WINDSURF:
        files = [(home / ".codeium" / "windsurf" / "mcp_config.json", "{}")]
    elif client == Client.CLINE_CLI:
        # Same as Qwen: the seeded CLI binary is the executable-class evidence.
        files = []
    elif client == Client.DEVIN_CLI:
        # Devin's config dir is shared with the desktop app, so it is not a
        # presence signal; the seeded CLI binary is the evidence.
        files = []
    elif client == Client.QWEN_CODE:
        # Qwen's scan definition has no config paths; the seeded CLI binary is
        # the only executable-class evidence the presence gate needs.
        files = []
    elif client == Client.GEMINI_CLI:
        files = [(home / ".gemini" / "settings.json", "{}")]
    else:
        files = [(home / ".copilot" / "mcp-config.json", "{}")]

    for path, content in files:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")


def _load_hooks_section(client: Client, path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    data = yaml.safe_load(text) if client == Client.HERMES else json.loads(text)
    assert isinstance(data, dict), f"config at {path} is not a mapping"
    hooks = data.get("hooks", {})
    assert isinstance(hooks, dict)
    return hooks


def _runlayer_events(client: Client, hooks: dict) -> tuple[set[str], list[str]]:
    """Return ``(event_names, commands)`` for entries in *hooks*.

    Cursor / VS Code / Hermes carry a top-level ``command`` per entry; Claude
    Code / Codex / Goose / Gemini CLI nest under ``hooks[].command``; Copilot
    CLI carries per-shell ``bash``/``powershell`` keys (no ``command``). On a
    fresh dir every entry is ours.
    """
    names: set[str] = set()
    commands: list[str] = []
    for event, entries in hooks.items():
        for entry in entries:
            if client in (
                Client.CLAUDE_CODE,
                Client.CODEX,
                Client.GOOSE,
                Client.QWEN_CODE,
                Client.GEMINI_CLI,
                Client.GROK_CLI,
                Client.DEVIN_CLI,
            ):
                cmd = entry["hooks"][0]["command"]
            elif client == Client.GITHUB_COPILOT_CLI:
                assert entry["bash"] == entry["powershell"]
                assert "command" not in entry
                cmd = entry["bash"]
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


def _assert_cline_scripts(hooks_dir: Path, *, include_pipeline: bool) -> None:
    """Cline registers hooks as executable files named after the event.

    There is no ``hooks`` mapping to load, so the event set is the set of script
    file names and the command lives inside each script body.
    """
    assert hooks_dir.is_dir(), f"expected Cline hooks dir at {hooks_dir}"
    scripts = sorted(p for p in hooks_dir.iterdir() if p.is_file())
    names = {p.stem for p in scripts}

    expected = expected_event_names(Client.CLINE_CLI, include_pipeline=include_pipeline)
    assert names == expected

    for script in scripts:
        body = script.read_text(encoding="utf-8")
        assert f"hook --client {Client.CLINE_CLI.value}" in body, body
        # The file name is the authoritative event, so the script must pass it
        # through to the dispatcher.
        assert script.stem in body, body

    if not include_pipeline:
        pipeline_only = expected_event_names(
            Client.CLINE_CLI, include_pipeline=True
        ) - expected_event_names(Client.CLINE_CLI, include_pipeline=False)
        assert not (names & pipeline_only), (
            f"enforcement-only install leaked pipeline scripts: {names & pipeline_only}"
        )


def _assert_events(client: Client, path: Path, *, include_pipeline: bool) -> None:
    if client == Client.CLINE_CLI:
        _assert_cline_scripts(path.parent, include_pipeline=include_pipeline)
        return
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
    monkeypatch.setenv("USERPROFILE", str(tmp_path))
    monkeypatch.setenv("APPDATA", str(tmp_path / "AppData" / "Roaming"))
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path / "AppData" / "Local"))
    monkeypatch.setenv("HERMES_HOME", str(tmp_path / ".hermes"))
    monkeypatch.setenv("COPILOT_HOME", str(tmp_path / ".copilot"))
    monkeypatch.setenv("QWEN_HOME", str(tmp_path / ".qwen"))
    monkeypatch.setenv("CLINE_DIR", str(tmp_path / ".cline"))
    monkeypatch.delenv("GROK_HOME", raising=False)
    return tmp_path


class TestUserScopeInstall:
    @pytest.mark.parametrize("client", iter_supported_clients(), ids=lambda c: c.value)
    @pytest.mark.parametrize(
        "extra_args, managed_config, include_pipeline", _EVENT_MODES
    )
    def test_install_writes_expected_events(
        self, home, client, extra_args, managed_config, include_pipeline
    ):
        _mark_user_client_installed(home, client)

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
            _mark_user_client_installed(home, client)

        result = _run_install(
            args=["--user"],
            config=_config_with_secret(),
            managed_config={"sessions": True},
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
        _mark_user_client_installed(console_home, client)
        # Console-home clients write under the console user's home and their
        # ENG-3217 anchor is the console home.
        # Cursor/Codex target a real root-owned enterprise dir unrelated to the
        # console home.
        if client in CONSOLE_HOME_CLIENTS:
            enterprise_root = console_home / _USER_DIR[client]
        else:
            enterprise_root = home / "enterprise" / client.value
        monkeypatch.setattr(
            clients_module, _ENTERPRISE_ATTR[client], lambda: enterprise_root
        )

        # A managed OrgApiKey satisfies the MDM-scope install self-gate (no key
        # ⇒ exit 0 silently, nothing written). The credential itself is still
        # proven via the console user's enrollment marker (credential_gate reads
        # its own unpatched managed config). Sessions/Enforcement keys drive
        # include_pipeline independently of the org key.
        managed = {"org_api_key": "rl_org_x", **managed_config}

        result = _run_install(
            args=["--mdm", "--client", client.value, *extra_args],
            config=_config_no_secret(),
            managed_config=managed,
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
            _mark_user_client_installed(home, client)

        install = _run_install(
            args=["--user"], config=_config_with_secret(), managed_config={}
        )
        assert install.exit_code == 0, install.output

        check = _run_check(
            args=["--user"], config=_config_with_secret(), managed_config={}
        )
        assert check.exit_code == 0, check.output
