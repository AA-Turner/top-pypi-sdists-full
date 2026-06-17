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

pytestmark = pytest.mark.frozen_binary

HOST = "https://t.example.com"
SECRET = "rl_user_frozen"

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
# Linux enterprise dirs (the deterministic target for the rooted MDM run).
# Claude Code is omitted: managed-settings hooks regressed (ENG-3204), so its
# MDM destination is the console user's ~/.claude/settings.json (like Hermes),
# asserted separately below.
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


def _env(home: Path) -> dict[str, str]:
    env = dict(os.environ)
    env["HOME"] = str(home)
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
        (home / _USER_DIR[client]).mkdir()

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

    POSIX ``find_console_user_home()`` falls back to ``$HOME``, so the MDM
    credential gate is satisfied by an enrollment marker under the temp HOME.
    """
    home = tmp_path / "home"
    home.mkdir()
    _seed_config(home)
    _write_enrollment_marker(home)

    created: list[Path] = []
    try:
        result = _run(
            frozen_aiwatch,
            ["setup", "hooks", "install", "--mdm", "--host", HOST],
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
