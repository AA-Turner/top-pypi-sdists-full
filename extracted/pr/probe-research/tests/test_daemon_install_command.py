"""`probe daemon install`'s command (2026-10-12).

A `uv tool install --force` deletes and rebuilds the tool's environment (on the
newest Python uv has, unless told) under every running `probe`; a daemon worker
crashed reading its own files from the deleted tree. The install of the
daemon's libraries now adds packages to the environment it has, always asks for
the `daemon` extra (on a first switch to the daemon neither the libraries nor
the setting exist yet, so nothing could infer it), checks the result in a fresh
interpreter, and repairs the packages in place when the install was a no-op.

No real install runs here: `subprocess.run` is replaced and its argv read.
test_updater_keeps_user_packages.py runs real uv for the same commands.
"""

from __future__ import annotations

import subprocess
import sys

import pytest
import typer

from probe import __version__
from probe.cli import daemon_cli, updater

#: The real `probe daemon install`, taken before conftest swaps in its tripwire.
_REAL_DAEMON_INSTALL = daemon_cli.daemon_install


@pytest.fixture
def ran(monkeypatch):
    """Records install commands; the fresh-interpreter import check answers from
    `state["imports"]`, one answer per check (the last one repeats)."""
    commands: list[list[str]] = []
    state = {"code": 0, "imports": [True], "checked_with": []}

    def fake_run(cmd, timeout=None, **kw):
        if cmd[1:2] == ["-c"]:
            state["checked_with"].append(cmd[0])
            ok = state["imports"].pop(0) if len(state["imports"]) > 1 else state["imports"][0]
            return subprocess.CompletedProcess(cmd, 0 if ok else 1, stdout="2.51.0\n" if ok else "")
        commands.append(list(cmd))
        return subprocess.CompletedProcess(cmd, state["code"])

    monkeypatch.setattr(daemon_cli, "daemon_install", _REAL_DAEMON_INSTALL)
    monkeypatch.setattr(daemon_cli, "_installed_copy", lambda: None)
    monkeypatch.setattr(daemon_cli, "ai_libraries", lambda: None)
    monkeypatch.setattr(subprocess, "run", fake_run)
    monkeypatch.setattr(
        updater, "kept_from_uv_receipt",
        lambda prefix=None: updater.KeptInstall(extras=("mcp-http",), with_packages=("wandb",)),
    )
    return commands, state


def _method(monkeypatch, method):
    monkeypatch.setattr(updater, "detect_install", lambda: updater.Install(method))


def test_a_uv_tool_install_adds_the_libraries_without_rebuilding_the_environment(monkeypatch, ran):
    commands, _ = ran
    _method(monkeypatch, updater.Method.UV_TOOL)
    daemon_cli.daemon_install()
    assert commands == [[
        "uv", "tool", "install", f"probe-research[all,daemon,mcp-http]=={__version__}", "--with", "wandb",
    ]]


def test_the_first_switch_to_the_daemon_asks_for_the_extra_itself(monkeypatch, ran):
    """The libraries are missing and Who records is still `agent`: `_dist` alone
    infers `[all]`, so the extra must be asked for explicitly."""
    commands, _ = ran
    monkeypatch.setitem(sys.modules, "pydantic_ai_harness", None)
    _method(monkeypatch, updater.Method.UV_TOOL)
    monkeypatch.setattr(updater, "kept_from_uv_receipt", lambda prefix=None: updater.KeptInstall())
    assert updater._dist() == "probe-research[all]"
    daemon_cli.daemon_install()
    assert commands == [["uv", "tool", "install", f"probe-research[all,daemon]=={__version__}"]]


def test_the_old_probe_agent_tool_is_taken_over_and_checked_in_the_new_environment(monkeypatch, ran):
    """The install fills a NEW `probe-research` environment; this process still
    runs the old probe-agent one, which never gets the libraries."""
    commands, state = ran
    _method(monkeypatch, updater.Method.UV_TOOL_LEGACY)
    monkeypatch.setattr(daemon_cli, "_installed_python", lambda: "/tools/probe-research/bin/python")
    daemon_cli.daemon_install()
    assert commands[0][:4] == ["uv", "tool", "install", "--force"]
    assert state["checked_with"] == ["/tools/probe-research/bin/python"]


def test_an_already_installed_receipt_with_broken_packages_is_repaired_in_place(monkeypatch, ran):
    """The receipt already asks for `daemon`, so the plain install is a no-op
    ("already installed") while the packages are gone: reinstall just those."""
    commands, state = ran
    state["imports"] = [False, True]
    _method(monkeypatch, updater.Method.UV_TOOL)
    daemon_cli.daemon_install()
    assert len(commands) == 2
    assert commands[1][: len(commands[0])] == commands[0] and "--force" not in commands[1]
    assert commands[1][len(commands[0]):] == [
        "--reinstall-package", "pydantic-ai-slim",
        "--reinstall-package", "pydantic-ai-harness",
        "--reinstall-package", "pydantic-ai-skills",
    ]


def test_success_is_never_claimed_while_the_libraries_still_do_not_import(monkeypatch, ran, capsys):
    commands, state = ran
    state["imports"] = [False]
    _method(monkeypatch, updater.Method.UV_TOOL)
    with pytest.raises(typer.Exit) as stopped:
        daemon_cli.daemon_install()
    assert stopped.value.exit_code == 1 and len(commands) == 2
    out = capsys.readouterr()
    assert "still do not import" in out.err and "daemon mode can run" not in out.out


def test_a_receipt_it_cannot_restate_is_not_reinstalled_over(monkeypatch, ran, capsys):
    """An editable or local `--with` would be dropped by any reinstall; `probe
    update` refuses that receipt too."""
    commands, _ = ran
    _method(monkeypatch, updater.Method.UV_TOOL)
    monkeypatch.setattr(updater, "kept_from_uv_receipt", lambda prefix=None: None)
    with pytest.raises(typer.Exit) as stopped:
        daemon_cli.daemon_install()
    assert stopped.value.exit_code == 2 and commands == []
    assert "cannot be restated" in capsys.readouterr().err


def test_a_failed_install_stops_before_the_check(monkeypatch, ran, capsys):
    commands, state = ran
    state["code"] = 2
    _method(monkeypatch, updater.Method.UV_TOOL)
    with pytest.raises(typer.Exit) as stopped:
        daemon_cli.daemon_install()
    assert stopped.value.exit_code == 2 and len(commands) == 1
    assert "install failed" in capsys.readouterr().err
