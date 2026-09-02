"""Tier 2: run the real frozen ``aiwatch`` bundle and assert hook install.

The subprocess is the frozen PyInstaller exe (built by the ``frozen_aiwatch``
session fixture); the test process is a normal interpreter, so it imports the
canonical event tables (``expected_event_names``) as the assertion oracle.

Unlike the in-process Tier 1 tests, ``resolve_hook_command`` is NOT patched:
the installed command must point at the *real* bundled exe, which only a frozen
run can prove.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

from runlayer_cli.config import url_to_host_key
from runlayer_cli.hook_install.clients import Client, expected_event_names
from runlayer_cli.scan.clients import get_client_by_name

pytestmark = pytest.mark.frozen_binary

HOST = "https://t.example.com"
SECRET = "rl_user_frozen"

_USER_DIR: dict[Client, str] = {
    Client.CURSOR: ".cursor",
    Client.VSCODE: ".copilot/hooks",
    Client.CLAUDE_CODE: ".claude",
    Client.CODEX: ".codex",
    Client.HERMES: ".hermes",
}
_USER_FILE: dict[Client, str] = {
    Client.CURSOR: "hooks.json",
    Client.VSCODE: "runlayer.json",
    Client.CLAUDE_CODE: "settings.json",
    Client.CODEX: "hooks.json",
    Client.HERMES: "config.yaml",
}
# Linux enterprise dirs (the deterministic target for the rooted MDM run).
# VS Code, Claude Code, and Hermes are omitted: their MDM destinations are
# console-user files asserted separately below.
_MDM_DIR: dict[Client, Path] = {
    Client.CURSOR: Path("/etc/cursor"),
    Client.CODEX: Path("/etc/codex"),
}
_MDM_FILE: dict[Client, str] = {
    Client.CURSOR: "hooks.json",
    Client.CODEX: "hooks.json",
}


def _seed_config(home: Path) -> None:
    runlayer_dir = home / ".runlayer"
    runlayer_dir.mkdir(parents=True, exist_ok=True)
    (runlayer_dir / "config.yaml").write_text(
        yaml.safe_dump(
            {
                "default_host": HOST,
                "hosts": {
                    url_to_host_key(HOST): {"url": HOST, "secret": SECRET},
                },
            }
        ),
        encoding="utf-8",
    )


def _write_enrollment_marker(home: Path) -> None:
    marker = home / ".runlayer" / f".enrolled-{url_to_host_key(HOST)}"
    marker.parent.mkdir(parents=True, exist_ok=True)
    marker.touch()


def _install_fake_cli_binary(home: Path, client: Client) -> None:
    """Seed the executable-class evidence the install presence gate requires.

    Config files alone no longer prove a client is installed, so drop a real
    executable in a location ``locate_cli_binary`` probes under *home*. Binary
    names come from the scan definition so they can't drift from the probe.
    """
    definition = get_client_by_name(client.value.replace("-", "_"))
    assert definition is not None, f"no scan definition for {client.value}"
    assert definition.install_probe is not None
    binaries = definition.install_probe.cli_binaries
    assert binaries, f"{client.value} has no CLI binary to seed"

    # Windows has no execute bit; there the suffix is what makes a file runnable.
    suffix = ".cmd" if sys.platform == "win32" else ""
    binary = home / ".local" / "bin" / f"{binaries[0]}{suffix}"
    binary.parent.mkdir(parents=True, exist_ok=True)
    binary.write_text("#!/bin/sh\n", encoding="utf-8")
    binary.chmod(0o755)


def _mark_client_installed(home: Path, client: Client) -> None:
    """Seed meaningful install probes consumed by the real frozen scanner."""
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
    else:
        files = [
            (home / ".hermes" / "config.yaml", "model: auto\n"),
            (
                home / "AppData" / "Local" / "hermes" / "config.yaml",
                "model: auto\n",
            ),
        ]

    for path, content in files:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")


def _env(home: Path) -> dict[str, str]:
    env = dict(os.environ)
    env["HOME"] = str(home)
    env["USERPROFILE"] = str(home)
    env["APPDATA"] = str(home / "AppData" / "Roaming")
    env["LOCALAPPDATA"] = str(home / "AppData" / "Local")
    env.pop("RUNLAYER_API_KEY", None)
    env.pop("RUNLAYER_HOST", None)
    return env


def _run(exe: Path, args: list[str], env: dict[str, str]):
    return subprocess.run(
        [str(exe), *args], capture_output=True, text=True, env=env, timeout=120
    )


def _load_hooks(client: Client, path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    data = yaml.safe_load(text) if client == Client.HERMES else json.loads(text)
    return data.get("hooks", {})


def _events_and_commands(client: Client, hooks: dict) -> tuple[set[str], list[str]]:
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


def _assert_installed(client: Client, path: Path, exe: Path) -> None:
    assert path.exists(), f"expected config at {path}"
    names, commands = _events_and_commands(client, _load_hooks(client, path))

    assert names == expected_event_names(client, include_pipeline=True)
    assert commands, "no Runlayer hook commands written"
    for cmd in commands:
        assert cmd.endswith(f"hook --client {client.value}"), cmd
        # The frozen run must wire the REAL bundled exe (Tier 1 can't check this).
        assert str(exe) in cmd, f"command does not reference the bundled exe: {cmd}"


def test_frozen_user_scope_install(frozen_aiwatch, tmp_path):
    """Frozen exe, ``--user`` scope: rootless, runs on any platform.

    The aiwatch binary ignores ``~/.runlayer/config.yaml``, so the credential
    gate is satisfied by the enrollment marker ``aiwatch enroll`` drops, not a
    seeded YAML. Host comes from ``--host``.
    """
    home = tmp_path / "home"
    home.mkdir()
    _write_enrollment_marker(home)
    for client in _USER_DIR:
        _mark_client_installed(home, client)

    result = _run(
        frozen_aiwatch,
        ["setup", "hooks", "install", "--user", "--all-events", "--host", HOST],
        _env(home),
    )
    assert result.returncode == 0, f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"

    for client in _USER_DIR:
        path = home / _USER_DIR[client] / _USER_FILE[client]
        _assert_installed(client, path, frozen_aiwatch)

    toml = (home / _USER_DIR[Client.CODEX] / "config.toml").read_text()
    assert "[features]" in toml
    assert "hooks = true" in toml


@pytest.mark.skipif(
    not sys.platform.startswith("linux"),
    reason="MDM frozen test targets Linux enterprise dirs (/etc/<client>)",
)
@pytest.mark.skipif(
    not hasattr(os, "geteuid") or os.geteuid() != 0,
    reason="--mdm frozen install writes /etc/<client>; needs root",
)
def test_frozen_mdm_scope_install(frozen_aiwatch, tmp_path):
    """Frozen exe, ``--mdm`` scope as root: writes Linux enterprise dirs.

    Drives ``aiwatch bootstrap --mdm`` rather than ``setup hooks install --mdm``:
    the latter self-gates to exit 0 silently when no managed ``OrgApiKey`` is
    present (``commands/aiwatch_setup.py``), and ``read_managed_config()`` has no
    source on Linux (this test's CI host), so it could never wire the clients.
    ``bootstrap`` has no ``OrgApiKey`` gate and exercises the same real-exe
    ``install_client`` / ``resolve_hook_command`` enterprise-dir writes. POSIX
    ``find_console_user_home()`` falls back to ``$HOME``, so the credential gate
    is satisfied by an enrollment marker under the temp HOME (root skips the
    keychain enroll step and proceeds straight to the install).

    Capability settings fail closed (missing ``Sessions`` ⇒ scan-only, hooks
    removed), so the Linux managed config seeds ``Sessions: true`` — the same
    channel a real fleet uses to enable the hook install.
    """
    home = tmp_path / "home"
    home.mkdir()
    _seed_config(home)
    _write_enrollment_marker(home)
    for client in _USER_DIR:
        _mark_client_installed(home, client)

    created: list[Path] = []
    try:
        managed_config = Path("/etc/runlayer/aiwatch/config.json")
        created.append(managed_config)
        managed_config.parent.mkdir(parents=True, exist_ok=True)
        managed_config.write_text(
            json.dumps({"Host": HOST, "Sessions": True}), encoding="utf-8"
        )

        result = _run(
            frozen_aiwatch,
            ["bootstrap", "--mdm", "--host", HOST],
            _env(home),
        )
        assert result.returncode == 0, (
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )

        for client, enterprise_dir in _MDM_DIR.items():
            path = enterprise_dir / _MDM_FILE[client]
            created.append(path)
            _assert_installed(client, path, frozen_aiwatch)

        codex_toml = _MDM_DIR[Client.CODEX] / "managed_config.toml"
        created.append(codex_toml)
        toml = codex_toml.read_text()
        assert "[features]" in toml
        assert "hooks = true" in toml

        # Hermes MDM has no enterprise dir -> console user's ~/.hermes ($HOME).
        hermes_path = home / ".hermes" / "config.yaml"
        _assert_installed(Client.HERMES, hermes_path, frozen_aiwatch)

        # VS Code hooks are user-level Copilot hook files.
        vscode_path = home / ".copilot" / "hooks" / "runlayer.json"
        _assert_installed(Client.VSCODE, vscode_path, frozen_aiwatch)

        # Claude Code managed-settings hooks regressed (ENG-3204) -> console
        # user's ~/.claude/settings.json ($HOME).
        claude_path = home / ".claude" / "settings.json"
        _assert_installed(Client.CLAUDE_CODE, claude_path, frozen_aiwatch)
    finally:
        for path in created:
            try:
                path.unlink()
            except OSError:
                pass
