"""Tests for `probe update` internals (cli/updater.py) + the command's --check codes.

Covers the hardening the eng review demanded: install detection from the running
package path (H4), the legacy probe-agent dance (H3), editable/managed guards
(H5/H6), the plugin post-condition + non-TTY spawn (H1/H2), and --check exit
codes distinct from main()'s 1/2 (H7).
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest

import probe
from probe import cli
from probe.cli import updater


# -- version compare --------------------------------------------------------
@pytest.mark.parametrize(
    ("a", "b", "expected"),
    [
        ("0.10.0", "0.9.0", True),  # NOT a string compare
        ("0.9.0", "0.10.0", False),
        ("0.7.0", "0.7.0", False),
        ("0.8.0", "0.8", False),  # 0.8 normalizes to 0.8.0
        (None, "0.7.0", False),
        ("0.7.0", None, False),
    ],
)
def test_is_newer(a, b, expected):
    assert updater.is_newer(a, b) is expected


# -- install detection (H4/H3) ---------------------------------------------
def _patch_pkg(monkeypatch, path: str):
    monkeypatch.setattr(updater, "_probe_pkg_dir", lambda: Path(path))


def test_detect_uv_tool(monkeypatch):
    _patch_pkg(
        monkeypatch,
        "/home/u/.local/share/uv/tools/probe-research/lib/python3.12/site-packages/probe",
    )
    assert updater.detect_install().method == updater.Method.UV_TOOL


def test_detect_uv_tool_legacy(monkeypatch):
    _patch_pkg(
        monkeypatch, "/home/u/.local/share/uv/tools/probe-agent/lib/python3.12/site-packages/probe"
    )
    assert updater.detect_install().method == updater.Method.UV_TOOL_LEGACY


def test_detect_pipx(monkeypatch):
    _patch_pkg(
        monkeypatch,
        "/home/u/.local/share/pipx/venvs/probe-research/lib/python3.12/site-packages/probe",
    )
    assert updater.detect_install().method == updater.Method.PIPX


def test_detect_editable_source_tree(monkeypatch):
    _patch_pkg(monkeypatch, "/home/u/dev/research-os-agent/src/probe")
    assert updater.detect_install().method == updater.Method.EDITABLE


def test_detect_pip_vs_managed(monkeypatch, tmp_path):
    # build a realistic venv layout: <proj>/.venv/lib/python3.12/site-packages/probe
    pkg = tmp_path / ".venv" / "lib" / "python3.12" / "site-packages" / "probe"
    pkg.mkdir(parents=True)
    _patch_pkg(monkeypatch, str(pkg))
    assert updater.detect_install().method == updater.Method.PIP  # no lockfile
    (tmp_path / "uv.lock").write_text("")  # now it's a managed project
    assert updater.detect_install().method == updater.Method.MANAGED


def test_detect_managed_out_of_project_poetry(monkeypatch):
    # Poetry/Pipenv keep the venv OUTSIDE the project, so no lockfile at venv.parent —
    # must still be recognized as managed (H6), not fall through to `pip install -U`.
    _patch_pkg(
        monkeypatch,
        "/home/u/.cache/pypoetry/virtualenvs/proj-abc123-py3.12/lib/python3.12/site-packages/probe",
    )
    assert updater.detect_install().method == updater.Method.MANAGED


@pytest.mark.parametrize(
    ("pkg", "managed"),
    [
        ("/home/u/.local/share/uv/tools/probe-research/lib/python3.12/site-packages/probe", True),
        ("/home/u/.local/share/uv/probe-versions/0.325.0/probe-research/lib/python3.12/site-packages/probe", True),
        ("/home/u/.local/share/uv/tools/probe-agent/lib/python3.12/site-packages/probe", True),
        ("/home/u/.local/share/pipx/venvs/probe-research/lib/python3.12/site-packages/probe", False),
        ("/home/u/dev/research-os-agent/src/probe", False),
        ("/home/u/.cache/pypoetry/virtualenvs/proj-abc123-py3.12/lib/python3.12/site-packages/probe", False),
        ("/home/u/proj/.venv/lib/python3.12/site-packages/probe", False),
    ],
)
def test_auto_update_is_on_by_default_for_the_uv_tool_installs_only(monkeypatch, pkg, managed):
    """The auto-update default (on unless turned off, plan C2) is the machine's
    managed CLI's alone: the installs `detect_install` names a uv tool, one
    version of it side by side included. A pipx, editable, project or pip
    install keeps its opt-in (D4), so `version_policy.managed_cli` must agree
    with `detect_install` on every one."""
    from probe import version_policy

    _patch_pkg(monkeypatch, pkg)
    uv_tool = updater.detect_install().method in {updater.Method.UV_TOOL, updater.Method.UV_TOOL_LEGACY}
    assert (uv_tool, version_policy.managed_cli(f"{pkg}/version_policy.py")) == (managed, managed)


def test_venv_root_both_layouts():
    assert updater._venv_root(Path("/home/u/app/.venv/lib/python3.12/site-packages/probe")) == Path(
        "/home/u/app/.venv"
    )
    # Windows Lib/site-packages is one level shallower — must not overshoot to the project.
    assert updater._venv_root(Path("/c/proj/.venv/Lib/site-packages/probe")) == Path(
        "/c/proj/.venv"
    )


# -- CLI upgrade dispatch (H3/H5/H6) ---------------------------------------
def _record_run(monkeypatch, *, daemon_extra: bool = False):
    calls: list[list[str]] = []
    monkeypatch.setattr(
        updater,
        "_run",
        lambda cmd, timeout: calls.append(cmd) or subprocess.CompletedProcess(cmd, 0),
    )
    # Whether this environment carries the daemon's AI libraries decides the spec.
    monkeypatch.setattr(
        updater,
        "_dist",
        lambda extras=(): "probe-research[%s]"
        % ",".join(sorted({"all", *extras} | ({"daemon"} if daemon_extra else set()))),
    )
    # No uv receipt to carry over (test_updater_keeps_user_packages.py covers it).
    monkeypatch.setattr(updater, "kept_from_uv_receipt", lambda prefix=None: updater.KeptInstall())
    return calls


def _stub_installed(monkeypatch, versions):
    """Feed _installed_cli_version() a sequence — what it reports after each upgrade."""
    it = iter(versions)
    monkeypatch.setattr(updater, "_installed_cli_version", lambda: next(it))


def test_upgrade_uv_tool_advances(monkeypatch):
    calls = _record_run(monkeypatch)
    _stub_installed(monkeypatch, ["0.8.2"])
    res = updater.upgrade_cli(updater.Install(updater.Method.UV_TOOL), "0.8.1", "0.8.2")
    assert res.ok and res.changed and res.after == "0.8.2"
    # `[all]` is restated FIRST, so the tool's receipt carries the extra before
    # the upgrade can land on the release that drops the CLI's dependencies
    # from core (plan 2.11; restating after left a window, #2043 review).
    assert calls == [
        ["uv", "tool", "install", "probe-research[all]"],
        ["uv", "tool", "upgrade", "probe-research"],
    ]


def test_upgrade_uv_tool_pinned_noop_then_latest(monkeypatch):
    # `uv tool upgrade` no-ops on a version pin (exits 0, version unchanged) -> install @latest,
    # without `--force`: that would delete and rebuild the environment under running workers
    calls = _record_run(monkeypatch)
    _stub_installed(monkeypatch, ["0.8.1", "0.8.2"])  # after upgrade (no move), after force (moved)
    res = updater.upgrade_cli(updater.Install(updater.Method.UV_TOOL), "0.8.1", "0.8.2")
    assert res.ok and res.changed and res.after == "0.8.2"
    assert calls == [
        ["uv", "tool", "install", "probe-research[all]"],
        ["uv", "tool", "upgrade", "probe-research"],
        ["uv", "tool", "install", "--refresh-package", "probe-research", "probe-research[all]@latest"],
    ]


def test_upgrade_uv_tool_stuck_is_honest_not_a_lie(monkeypatch):
    # even after the force reinstall the version never moves -> report failure, don't claim success
    _record_run(monkeypatch)
    _stub_installed(monkeypatch, ["0.8.1", "0.8.1"])
    res = updater.upgrade_cli(updater.Install(updater.Method.UV_TOOL), "0.8.1", "0.8.2")
    assert not res.ok and not res.changed and "still 0.8.1" in res.message


def test_upgrade_uv_tool_already_latest(monkeypatch):
    _record_run(monkeypatch)
    _stub_installed(monkeypatch, ["0.8.2"])  # already at target, nothing moved
    res = updater.upgrade_cli(updater.Install(updater.Method.UV_TOOL), "0.8.2", "0.8.2")
    assert res.ok and not res.changed and "already" in res.message


def test_upgrade_legacy_does_uninstall_then_install(monkeypatch):
    calls = _record_run(monkeypatch)
    _stub_installed(monkeypatch, ["0.8.2"])
    updater.upgrade_cli(updater.Install(updater.Method.UV_TOOL_LEGACY), "0.7.0", "0.8.2")
    assert calls == [
        ["uv", "tool", "uninstall", "probe-agent"],
        ["uv", "tool", "install", "--force", "probe-research[all]"],
    ]


def test_upgrade_pipx(monkeypatch):
    calls = _record_run(monkeypatch)
    _stub_installed(monkeypatch, ["0.8.2"])
    updater.upgrade_cli(updater.Install(updater.Method.PIPX), "0.8.1", "0.8.2")
    assert calls == [["pipx", "install", "--force", "probe-research[all]"]]


def test_every_install_asks_for_the_all_extra(monkeypatch):
    """Plan 2.11 (D29), release N: the next release moves the CLI's and MCP
    server's dependencies out of core, so every install spec asks for `[all]`
    now -- and keeps `daemon` when the environment has it."""
    import builtins

    real_import = builtins.__import__

    def without_daemon(name, *a, **kw):
        if name == "pydantic_ai_harness":
            raise ImportError(name)
        return real_import(name, *a, **kw)

    monkeypatch.setattr(builtins, "__import__", without_daemon)
    assert updater._dist() == "probe-research[all]"
    monkeypatch.setattr(builtins, "__import__", real_import)
    import sys
    import types

    monkeypatch.setitem(sys.modules, "pydantic_ai_harness", types.ModuleType("pydantic_ai_harness"))
    assert updater._dist() == "probe-research[all,daemon]"


def test_a_project_environment_with_its_own_pydantic_ai_is_not_handed_the_daemon_stack(monkeypatch):
    """`import pydantic_ai` succeeds in any project that uses Pydantic AI; only the
    daemon's own harness says these are the daemon's libraries."""
    import sys
    import types

    monkeypatch.setitem(sys.modules, "pydantic_ai", types.ModuleType("pydantic_ai"))
    monkeypatch.setitem(sys.modules, "pydantic_ai_harness", None)
    assert updater._dist() == "probe-research[all]"


def _without_daemon_libraries(monkeypatch):
    import sys

    monkeypatch.setitem(sys.modules, "pydantic_ai_harness", None)  # its import raises ImportError


def _installed_as(monkeypatch, method):
    monkeypatch.setattr(updater, "detect_install", lambda: updater.Install(method))


def test_a_tool_install_that_lost_the_daemon_extra_gets_it_back_where_the_daemon_records(monkeypatch):
    """2026-10-12: a bare `uv tool install --force probe-research` stripped the
    daemon's libraries, and every update after restated `[all]` alone because it
    only asked whether they were importable. Who records is the daemon, so the
    update puts them back."""
    from probe.sdk import session_marker

    _without_daemon_libraries(monkeypatch)
    _installed_as(monkeypatch, updater.Method.UV_TOOL)
    assert updater._dist() == "probe-research[all]"
    session_marker.write_recorder("codex", session_marker.RECORDER_DAEMON)
    assert updater._dist() == "probe-research[all,daemon]"
    session_marker.write_recorder("codex", session_marker.RECORDER_AGENT)
    assert updater._dist() == "probe-research[all]"


@pytest.mark.parametrize("method", [updater.Method.PIP, updater.Method.MANAGED, updater.Method.EDITABLE])
def test_a_pip_install_is_not_given_the_daemon_stack_by_the_setting(monkeypatch, method):
    """A pip install lives in a project or training environment: the daemon's
    pinned AI stack goes there only when someone asks (`probe daemon install`)."""
    from probe.sdk import session_marker

    _without_daemon_libraries(monkeypatch)
    _installed_as(monkeypatch, method)
    session_marker.write_recorder("claude_code", session_marker.RECORDER_DAEMON)
    assert updater._dist() == "probe-research[all]"


def _tool_env(tmp_path: Path, receipt: str, pyvenv: str | None, interpreters: tuple[str, ...] = ()) -> Path:
    env = tmp_path / "env"
    home = tmp_path / "home-bin"
    env.mkdir()
    home.mkdir()
    for name in interpreters:
        (home / name).write_text("")
    (env / "uv-receipt.toml").write_text(receipt)
    if pyvenv is not None:
        (env / "pyvenv.cfg").write_text(pyvenv.format(home=home))
    return env


_BARE_RECEIPT = '[tool]\nrequirements = [{ name = "probe-research", extras = ["all"] }]\n'
_PYVENV = "home = {home}\nimplementation = CPython\nuv = 0.12.5\nversion_info = 3.12.3\n"


def test_a_receipt_without_a_python_restates_the_exact_interpreter_the_environment_runs_on(tmp_path):
    """2026-10-12: with no Python in the receipt, `--force` (and a plain install on
    uv before 0.10) rebuilt the tool on the newest Python and deleted
    `lib/pythonX.Y` under a live daemon worker. `--python 3.12` is no cure: uv
    picked its managed 3.12 over the system one and rebuilt just the same. Only
    the exact path keeps the environment."""
    env = _tool_env(tmp_path, _BARE_RECEIPT, _PYVENV, ("python3.12", "python3"))
    kept = updater.kept_from_uv_receipt(env)
    assert kept.python == str(tmp_path / "home-bin" / "python3.12")
    assert updater.uv_tool_install_command(kept)[-2:] == ["--python", kept.python]


@pytest.mark.parametrize(
    "receipt, pyvenv, interpreters, python",
    [
        # What the receipt records is the user's choice, kept as it is.
        ('[tool]\nrequirements = [{ name = "probe-research" }]\npython = "3.11"\n', _PYVENV, ("python3.12",), "3.11"),
        # ...unless it is a path that no longer exists: the environment's own then.
        ('[tool]\nrequirements = [{ name = "probe-research" }]\npython = "/gone/python3.9"\n', _PYVENV,
         ("python3.12",), "HOME/python3.12"),
        # No `pythonX.Y` in `home`: a bare `python3` may be another version by now.
        (_BARE_RECEIPT, _PYVENV, ("python3", "python"), None),
        # No interpreter at `home`, no pyvenv.cfg: no pin, as before.
        (_BARE_RECEIPT, _PYVENV, (), None),
        (_BARE_RECEIPT, None, ("python3.12",), None),
    ],
)
def test_which_python_a_reinstall_restates(tmp_path, receipt, pyvenv, interpreters, python):
    env = _tool_env(tmp_path, receipt, pyvenv, interpreters)
    expected = python.replace("HOME", str(tmp_path / "home-bin")) if python else None
    assert updater.kept_from_uv_receipt(env).python == expected


def test_the_update_restates_the_daemon_extra_from_the_setting_alone(monkeypatch):
    from probe.sdk import session_marker

    _without_daemon_libraries(monkeypatch)
    _installed_as(monkeypatch, updater.Method.UV_TOOL)
    session_marker.write_recorder("claude_code", session_marker.RECORDER_DAEMON)
    calls: list[list[str]] = []
    monkeypatch.setattr(updater, "_run", lambda cmd, timeout: calls.append(cmd) or subprocess.CompletedProcess(cmd, 0))
    monkeypatch.setattr(updater, "kept_from_uv_receipt", lambda prefix=None: updater.KeptInstall())
    _stub_installed(monkeypatch, ["0.8.1", "0.8.2"])
    updater.upgrade_cli(updater.Install(updater.Method.UV_TOOL), "0.8.1", "0.8.2")
    assert calls[0] == ["uv", "tool", "install", "probe-research[all,daemon]"]


@pytest.mark.parametrize(
    "method", [updater.Method.EDITABLE, updater.Method.MANAGED, updater.Method.UNKNOWN]
)
def test_upgrade_refuses_and_never_runs(monkeypatch, method):
    calls = _record_run(monkeypatch)
    res = updater.upgrade_cli(updater.Install(method), "0.8.1", "0.8.2")
    assert not res.ran and calls == [] and res.message  # instruction, no mutation


# -- plugin update: post-condition + non-TTY (H1/H2) -----------------------
class _FakeRun:
    def __init__(self):
        self.kwargs = None

    def __call__(self, cmd, **kwargs):
        self.kwargs = kwargs
        return subprocess.CompletedProcess(cmd, 0, stdout="", stderr="")


def _seq(values):
    it = iter(values)
    return lambda: next(it)


def test_plugin_confirmed_when_version_advances(monkeypatch):
    fake = _FakeRun()
    monkeypatch.setattr(updater.shutil, "which", lambda _n: "/usr/bin/claude")
    monkeypatch.setattr(updater.subprocess, "run", fake)
    monkeypatch.setattr(updater, "installed_plugin_version", _seq(["0.6.0", "0.7.0"]))
    res = updater.update_plugin("0.7.0")
    assert res.confirmed and res.changed and res.after == "0.7.0"
    assert fake.kwargs["stdin"] is subprocess.DEVNULL  # H2: no TTY on the child


def test_plugin_noop_not_confirmed_even_on_zero_exit(monkeypatch):
    # claude exits 0 but the version never moves (nested-session no-op) -> NOT confirmed (H1)
    monkeypatch.setattr(updater.shutil, "which", lambda _n: "/usr/bin/claude")
    monkeypatch.setattr(
        updater.subprocess, "run", lambda cmd, **k: subprocess.CompletedProcess(cmd, 0)
    )
    monkeypatch.setattr(updater, "installed_plugin_version", lambda: "0.6.0")
    res = updater.update_plugin("0.7.0")
    assert res.attempted and not res.confirmed


def test_plugin_absent_claude(monkeypatch):
    monkeypatch.setattr(updater.shutil, "which", lambda _n: None)
    res = updater.update_plugin("0.7.0")
    assert not res.attempted and not res.confirmed


def test_plugin_already_current_is_confirmed_but_unchanged(monkeypatch):
    # at target already: confirmed=True (post-condition holds) but changed=False, so
    # the caller won't falsely tell the user to restart for a no-op.
    monkeypatch.setattr(updater.shutil, "which", lambda _n: "/usr/bin/claude")
    monkeypatch.setattr(
        updater.subprocess, "run", lambda cmd, **k: subprocess.CompletedProcess(cmd, 0)
    )
    monkeypatch.setattr(updater, "installed_plugin_version", lambda: "0.8.1")
    res = updater.update_plugin("0.8.1")
    assert res.confirmed and not res.changed and "already" in res.message


def test_plugin_failure_names_the_command_and_what_it_said(monkeypatch):
    """ "did not complete" alone gave a researcher nothing to act on: claude's own
    error was captured and dropped, and `probe doctor` recorded the same blank."""

    # The shape claude 2.1.280 printed with GitHub unreachable: progress on
    # stdout, one error split over its own summary and git's `fatal:` line.
    def fake_run(cmd, **kwargs):
        if cmd[1:3] == ["plugin", "marketplace"]:
            return subprocess.CompletedProcess(
                cmd,
                1,
                stdout="Updating marketplace: research-os-agent...\n",
                stderr="✘ Failed to refresh marketplace 'research-os-agent': "
                "Cloning into '/opt/cc/plugins/marketplaces/research-os-agent..clone'...\n"
                "fatal: unable to access 'https://github.com/prbe-ai/research-os-agent.git/': "
                "Couldn't connect to server\n\n",
            )
        return subprocess.CompletedProcess(cmd, 0, stdout="", stderr="")

    monkeypatch.setattr(updater.shutil, "which", lambda _n: "/usr/bin/claude")
    monkeypatch.setattr(updater.subprocess, "run", fake_run)
    monkeypatch.setattr(updater, "installed_plugin_version", lambda: "0.6.0")

    res = updater.update_plugin("0.7.0")

    assert not res.confirmed
    assert res.message == (
        "`claude plugin marketplace update research-os-agent` did not complete: "
        "✘ Failed to refresh marketplace 'research-os-agent': "
        "Cloning into '/opt/cc/plugins/marketplaces/research-os-agent..clone'... · "
        "fatal: unable to access 'https://github.com/prbe-ai/research-os-agent.git/': "
        "Couldn't connect to server"
    )


def test_a_failed_refresh_skips_both_installs_and_outlasts_claudes_120s(monkeypatch):
    """Claude gives its cache refresh 120s, so killing it at 90s failed a slow
    clone Claude was still waiting on. And once the refresh has failed there is
    nothing new to install: the tap step only cost a second timeout."""
    ran: dict[str, float] = {}

    def fake_run(cmd, **kwargs):
        ran[" ".join(cmd[1:])] = kwargs["timeout"]
        if cmd[1:3] == ["plugin", "marketplace"]:
            raise subprocess.TimeoutExpired(cmd, kwargs["timeout"])
        return subprocess.CompletedProcess(cmd, 0, stdout="", stderr="")

    monkeypatch.setattr(updater.shutil, "which", lambda _n: "/usr/bin/claude")
    monkeypatch.setattr(updater.subprocess, "run", fake_run)
    monkeypatch.setattr(updater, "installed_plugin_version", lambda: "0.6.0")

    res = updater.update_plugin("0.7.0")

    assert ran == {"plugin marketplace update research-os-agent": 150.0}
    assert res.message.endswith("did not complete: timed out after 150s")


def _fake_codex(monkeypatch, replies: dict[str, subprocess.CompletedProcess]):
    """Drive the REAL plugin_cli.run, so the command a message names is the
    argv that ran, not one a test (or updater) typed a second time."""
    ran: list[str] = []

    def fake_run(cmd, **kwargs):
        args = " ".join(cmd[1:])
        ran.append(args)
        return replies.get(args) or subprocess.CompletedProcess(cmd, 0, stdout="", stderr="")

    monkeypatch.setattr(updater.shutil, "which", lambda _n: "/usr/bin/codex")
    monkeypatch.setattr(updater.subprocess, "run", fake_run)
    return ran


def _failed_with(stderr: str) -> subprocess.CompletedProcess:
    return subprocess.CompletedProcess([], 1, stdout="", stderr=stderr)


def test_codex_failure_keeps_the_reason_not_just_the_count(monkeypatch):
    """codex-cli 0.156.0 with GitHub unreachable: a PATH-alias WARNING, the
    reason, then a bare count. The last line alone says nothing."""
    ran = _fake_codex(
        monkeypatch,
        {
            "plugin marketplace upgrade research-os-agent": _failed_with(
                "WARNING: proceeding, even though we could not create PATH aliases\n"
                "Failed to upgrade marketplace `research-os-agent`: git ls-remote marketplace "
                "source failed: Couldn't connect to server\n"
                "Error: 1 upgrade failure(s) occurred."
            )
        },
    )

    res = updater.update_codex_plugins()

    assert not res.confirmed
    assert res.message == (
        "`codex plugin marketplace upgrade research-os-agent` did not complete: "
        "Failed to upgrade marketplace `research-os-agent`: git ls-remote marketplace "
        "source failed: Couldn't connect to server · Error: 1 upgrade failure(s) occurred."
    )
    assert not [args for args in ran if args.startswith("plugin add")], (
        "never reinstall from a marketplace that did not refresh"
    )


def test_codex_add_failure_names_the_plugin_and_stops(monkeypatch):
    ran = _fake_codex(
        monkeypatch,
        {"plugin add probe-research@research-os-agent": _failed_with("Error: plugin not found")},
    )

    res = updater.update_codex_plugins()

    assert res.message == (
        "`codex plugin add probe-research@research-os-agent` did not complete: "
        "Error: plugin not found"
    )
    assert "plugin add probe-research-tap@research-os-agent" not in ran


def test_codex_reinstall_it_cannot_confirm_says_so(monkeypatch):
    """`codex plugin list` failing and a plugin genuinely missing both leave
    nothing listed: the message says which it was, and why the list could not
    be read (2026-10-25: two machines reported both plugins unconfirmed with
    nothing to tell the two apart)."""
    _fake_codex(monkeypatch, {"plugin list --json": _failed_with("boom")})

    res = updater.update_codex_plugins()

    assert not res.confirmed
    assert res.list_unreadable
    assert res.message == (
        "could not confirm probe-research or probe-research-tap: `codex plugin list --json` "
        "could not be read after reinstalling (boom)"
    )


def test_codex_reinstall_a_list_without_probe_says_what_it_lists(monkeypatch):
    listed = json.dumps({"installed": [{"name": "visualize", "version": "1.0.55"}]})
    _fake_codex(
        monkeypatch,
        {"plugin list --json": subprocess.CompletedProcess([], 0, stdout=listed, stderr="")},
    )

    res = updater.update_codex_plugins()

    assert not res.confirmed and not res.list_unreadable
    assert res.message == (
        "could not confirm probe-research or probe-research-tap in "
        "`codex plugin list --json` after reinstalling (it lists 1 plugin)"
    )


def test_a_codex_list_that_is_not_an_object_is_unread_not_empty(monkeypatch):
    """None, not {}: an empty list says no Probe plugin is installed, which is
    no failed update (`updater.nothing_installed`); a list it cannot read says
    nothing either way."""
    _fake_codex(
        monkeypatch,
        {"plugin list --json": subprocess.CompletedProcess([], 0, stdout="[]", stderr="")},
    )
    assert updater._codex_plugin_versions() is None


def _reason(detail: str) -> str:
    message = updater._failed(
        updater.claude_cli.Result(ok=False, detail=detail, command="claude plugin update x")
    )
    prefix = "`claude plugin update x` did not complete: "
    assert message.startswith(prefix)
    return message[len(prefix) :]


def test_a_long_reason_loses_its_middle_not_its_deciding_end():
    reason = _reason("HEAD " + "hint: x\n" * 400 + "fatal: the part that says why")
    assert len(reason) <= updater._REASON_MAX
    assert reason.startswith("HEAD ") and reason.endswith("fatal: the part that says why")
    assert " … " in reason


def test_a_reason_that_is_only_a_warning_is_kept():
    assert _reason("WARNING: the only thing it said") == "WARNING: the only thing it said"
    assert _reason("") == "no output"


def test_a_reason_is_scrubbed_before_it_is_printed_or_stored():
    """It is replayed by every later `probe doctor`, and agents run that inside
    captured sessions: no terminal escapes, no credentials, no home paths."""
    reason = _reason(
        "\x1b]52;c;Zm9v\x07fatal: unable to access "
        "'https://user:ghp_abcdefghijklmnopqrstuvwxyz0123456789@github.com/x.git/' "
        "from /home/alice/.claude/plugins"
    )
    assert "\x1b" not in reason and "\x07" not in reason
    assert "ghp_" not in reason and "user:" not in reason
    assert "alice" not in reason


def test_a_coloured_token_is_scrubbed_not_unmasked():
    """Dropping only the ESC byte left `[31m` glued to the token, which hid it
    from the scanner: the RAW text is scrubbed first."""
    reason = _reason("\x1b[31mghp_abcdefghijklmnopqrstuvwxyz0123456789\x1b[0m")
    assert "ghp_" not in reason and "[31m" not in reason


def test_a_coloured_warning_is_still_noise_and_tabs_stay_word_breaks():
    reason = _reason("\x1b[33mWARNING: noise\x1b[0m\nfatal:\tbad thing")
    assert reason == "fatal: bad thing"


def test_output_the_scrubber_cannot_bound_is_withheld_not_raised():
    """The scrubber raises on deeply nested percent-encoding. Raising here would
    abort the update before it records its outcome."""
    assert _reason("fetch %2525252525252541 failed") == "output withheld: it could not be scrubbed"


def test_codex_update_refreshes_and_readds_both_plugins_then_verifies(monkeypatch):
    calls: list[list[str]] = []
    monkeypatch.setattr(updater.shutil, "which", lambda name: "/usr/bin/codex")
    monkeypatch.setattr(
        updater.plugin_cli,
        "refresh_marketplace",
        lambda source, marketplace: (
            calls.append([source, "refresh", marketplace]) or updater.claude_cli.Result(ok=True)
        ),
    )
    monkeypatch.setattr(
        updater.plugin_cli,
        "install",
        lambda source, plugin_id: (
            calls.append([source, "install", plugin_id]) or updater.claude_cli.Result(ok=True)
        ),
    )
    versions = iter(
        [
            {"probe-research": "0.16.0", "probe-research-tap": "0.1.2"},
            {"probe-research": "0.16.1", "probe-research-tap": "0.1.3"},
        ]
    )
    monkeypatch.setattr(updater, "_codex_plugin_versions", lambda codex: next(versions))

    result = updater.update_codex_plugins()

    assert result.confirmed and result.changed
    assert calls == [
        ["codex", "refresh", "research-os-agent"],
        ["codex", "install", "probe-research@research-os-agent"],
        ["codex", "install", "probe-research-tap@research-os-agent"],
    ]


# -- the wizard's menu after an Update ---------------------------------------
def _upgrade_to(monkeypatch, result: updater.CliResult):
    from probe.cli import run_lock, upgrading, versions

    monkeypatch.setattr(versions, "_installed_cli", None)
    monkeypatch.setattr(run_lock, "any_live", lambda: False)
    monkeypatch.setattr(upgrading.autoupdate, "record_attempt", lambda attempt, **_: None)
    monkeypatch.setattr(updater, "fetch_latest", lambda base: {"cli": {"latest": "99.0.0"}})
    monkeypatch.setattr(updater, "detect_install", lambda: updater.Install(updater.Method.UV_TOOL))
    monkeypatch.setattr(updater, "upgrade_cli", lambda install, current, target: result)
    upgrading.perform_update(base_url="https://x", include_plugin=False)
    return versions


def test_the_menu_grades_the_cli_this_update_installed(monkeypatch):
    """The menu re-reads state after Update, but the running interpreter keeps
    its own __version__, so it went on showing "Update available" directly
    under "CLI upgraded"."""
    versions = _upgrade_to(
        monkeypatch,
        updater.CliResult(True, True, True, probe.__version__, "99.0.0", "CLI upgraded"),
    )

    assert versions.local_versions()["cli"] == "99.0.0"
    assert versions.local_versions()["sdk"] == "99.0.0", "same distribution, same number"
    assert versions.cli_version() == "99.0.0", "doctor's CLI version row reads this too"
    (cli,) = [row for row in versions.compare({"cli": {"latest": "99.0.0"}}) if row.kind == "cli"]
    assert not cli.behind


def test_a_stuck_upgrade_leaves_the_menu_on_the_running_version(monkeypatch):
    versions = _upgrade_to(
        monkeypatch,
        updater.CliResult(True, False, False, probe.__version__, "9.9.9", "still behind"),
    )

    assert versions.local_versions()["cli"] == probe.__version__


def test_the_upgrade_is_judged_by_the_upgraded_environment_not_path(monkeypatch):
    """The `probe` on PATH can be a conda or pipx copy nobody upgraded: judging
    by it reported "CLI upgraded" for an untouched install, or a failure for
    one that moved."""
    monkeypatch.setattr(updater, "env_cli_version", lambda: "2.0.0")
    monkeypatch.setattr(updater, "_path_cli_version", lambda: "1.0.0")
    assert updater._installed_cli_version() == "2.0.0"


def test_the_legacy_reinstall_falls_back_to_path(monkeypatch):
    """It deletes the running interpreter's own environment."""
    monkeypatch.setattr(updater, "env_cli_version", lambda: None)
    monkeypatch.setattr(updater, "_path_cli_version", lambda: "2.0.0")
    assert updater._installed_cli_version() == "2.0.0"


def test_env_cli_version_reads_this_interpreters_install():
    assert updater.env_cli_version() == probe.__version__


# -- --check exit codes (H7) -----------------------------------------------
def _patch_fetch(monkeypatch, manifest=None, exc=None):
    def fake(_base):
        if exc:
            raise exc
        return manifest

    monkeypatch.setattr(updater, "fetch_latest", fake)


def test_check_current_exit_0(monkeypatch):
    _patch_fetch(monkeypatch, {"cli": {"latest": probe.__version__}})
    assert cli.main(["update", "--check"]) == updater.CHECK_CURRENT


def test_check_behind_exit_10(monkeypatch):
    _patch_fetch(monkeypatch, {"cli": {"latest": "999.0.0"}})
    assert cli.main(["update", "--check"]) == updater.CHECK_BEHIND


def test_check_error_exit_1(monkeypatch):
    _patch_fetch(monkeypatch, exc=RuntimeError("network down"))
    assert cli.main(["update", "--check"]) == updater.CHECK_ERROR


def test_an_upgrade_keeps_the_daemon_extra(monkeypatch):
    """`probe update` must never strip the daemon's AI libraries (daemon v2, R3.4)."""
    calls = _record_run(monkeypatch, daemon_extra=True)
    _stub_installed(monkeypatch, ["0.8.1", "0.8.1", "0.8.2"])
    updater.upgrade_cli(updater.Install(updater.Method.UV_TOOL), "0.8.1", "0.8.2")
    assert ["uv", "tool", "install", "--refresh-package", "probe-research", "probe-research[all,daemon]@latest"] in calls


def test_an_update_required_beside_the_running_version_goes_past_a_live_run(monkeypatch):
    """The service let a run go on because the CLI is updated beside it (D6):
    the child's own run check must not defer it again (Codex R2 #9)."""
    from probe.cli import run_lock, upgrading

    asked = []
    monkeypatch.setattr(run_lock, "any_live", lambda: True)
    monkeypatch.setattr(upgrading.autoupdate, "record_attempt", lambda attempt, **_: None)
    monkeypatch.setattr(updater, "fetch_latest", lambda base: {"cli": {"latest": "99.0.0"}})
    monkeypatch.setattr(updater, "detect_install", lambda: updater.Install(updater.Method.UV_TOOL))
    monkeypatch.setattr(updater, "upgrade_cli", lambda install, current, target: asked.append(target) or
                        updater.CliResult(True, True, False, probe.__version__, "99.0.0", "beside"))
    monkeypatch.setenv(updater.REQUIRE_SIDE_BY_SIDE_ENV, "1")
    upgrading.perform_update(base_url="https://x", include_plugin=False)
    assert asked == ["99.0.0"]
    monkeypatch.delenv(updater.REQUIRE_SIDE_BY_SIDE_ENV)
    outcome = upgrading.perform_update(base_url="https://x", include_plugin=False)
    assert asked == ["99.0.0"] and "in flight" in " ".join(outcome.lines)


# -- installer fallbacks (plan A4) ------------------------------------------
@pytest.fixture
def side_by_side(monkeypatch, tmp_path):
    """A uv tool install that updates beside the running version, its
    `installs` steps stood in for: what each install was asked for, and what
    the switch recorded."""
    from probe._shared import installs
    from probe.core import adopt

    adopt.reset()
    seen = {"installs": [], "dropped": [], "activated": [], "fail_pin": True, "fail_with": True,
            "with_said": "No solution found when resolving tool dependencies: wandb conflicts with probe-research"}
    monkeypatch.setattr(installs, "tool_dir", lambda: tmp_path / "tools")
    monkeypatch.setattr(installs, "dropped_with", lambda tools=None: list(seen.get("dropped_before", [])))
    monkeypatch.setattr(installs, "usable", lambda tools=None: True)
    monkeypatch.setattr(installs, "rejected", lambda tools=None: {})
    monkeypatch.setattr(installs, "selftest", lambda env: None)
    monkeypatch.setattr(installs, "activate", lambda env, tools=None: seen["activated"].append(env) or {})
    monkeypatch.setattr(installs, "prune", lambda tools=None: [])
    monkeypatch.setattr(installs, "dropped_python", lambda tools=None: None)

    def record(packages, tools=None, *, python=None):
        seen["dropped"].append(list(packages))
        seen["dropped_python"] = python

    monkeypatch.setattr(installs, "record_dropped_with", record)
    old = updater.KeptInstall(with_packages=("wandb>=0.17",), python="/gone/bin/python3.12")
    # The running install's receipt, or the new env's: what its install got.
    monkeypatch.setattr(updater, "kept_from_uv_receipt", lambda prefix=None: seen.get("receipt", old)
                        if prefix is not None else seen.get("old", old))

    def install(version, spec, *, with_packages=(), python=None, tools=None, timeout=0):
        seen["installs"].append((tuple(with_packages), python))
        if python and seen["fail_pin"]:
            raise RuntimeError("the requested interpreter is gone")
        if with_packages and seen["fail_with"]:
            raise RuntimeError(f"`uv tool install` exited 1 and left nothing: {seen['with_said']}")
        seen["receipt"] = updater.KeptInstall(with_packages=tuple(with_packages),
                                              python=python or "/uv/python/cpython-3.13/bin/python3.13")
        return tmp_path / "probe-versions" / version / "probe-research"

    monkeypatch.setattr(installs, "install", install)
    yield seen
    adopt.reset()


def test_a_pin_uv_cannot_use_then_with_packages_that_will_not_resolve_are_left_out(side_by_side):
    result = updater.upgrade_side_by_side("0.1.0", "0.2.0")
    assert result.ok and result.changed
    assert side_by_side["installs"] == [
        (("wandb>=0.17",), "/gone/bin/python3.12"), (("wandb>=0.17",), None), ((), None)]
    assert side_by_side["dropped"] == [["wandb>=0.17"]]
    assert "left out --with wandb>=0.17" in result.message and "probe doctor" in result.message


@pytest.mark.parametrize("said", [
    "error: Distribution not found at: file:///home/u/src/mine",
    "error: Git operation failed: Repository not found",
    "error: Failed to build `mine`",
])
def test_with_packages_are_left_out_last_whatever_failed(side_by_side, said):
    side_by_side["with_said"] = said
    result = updater.upgrade_side_by_side("0.1.0", "0.2.0")
    assert result.ok and side_by_side["installs"][-1] == ((), None)
    assert side_by_side["dropped"] == [["wandb>=0.17"]]


def test_with_packages_left_out_before_are_tried_first_and_forgotten_once_back(side_by_side):
    side_by_side["fail_pin"] = side_by_side["fail_with"] = False
    side_by_side["dropped_before"] = ["torch==2.4", "wandb"]
    result = updater.upgrade_side_by_side("0.1.0", "0.2.0")
    assert result.ok and side_by_side["installs"] == [(("wandb>=0.17", "torch==2.4"), "/gone/bin/python3.12")]
    assert side_by_side["dropped"] == [[]]  # all back: the record is cleared


def test_a_pin_uv_cannot_use_alone_keeps_the_with_packages(side_by_side):
    side_by_side["fail_with"] = False
    result = updater.upgrade_side_by_side("0.1.0", "0.2.0")
    assert result.ok and side_by_side["installs"][-1] == (("wandb>=0.17",), None)
    # The packages are all there; the exact Python is not, and is said and recorded.
    assert side_by_side["dropped"] == [[]] and side_by_side["dropped_python"] == "/gone/bin/python3.12"
    assert "left out --python /gone/bin/python3.12" in result.message


def test_a_uv_that_times_out_ends_the_install(side_by_side, monkeypatch):
    """The machine or the network, not the package set: no other try now (four
    300 s tries would outlast the service's 30 min for the whole update)."""
    from probe._shared import installs

    calls = []

    def hangs(version, spec, *, with_packages=(), python=None, tools=None, timeout=0):
        calls.append(timeout)
        raise subprocess.TimeoutExpired(["uv"], timeout)

    monkeypatch.setattr(installs, "install", hangs)
    result = updater.upgrade_side_by_side("0.1.0", "0.2.0")
    assert not result.ok and "timed out after 300 s" in result.message and calls == [300.0]


def test_an_env_kept_from_an_earlier_install_loses_nothing_unsaid(side_by_side, monkeypatch, tmp_path):
    """An earlier install left wandb out and was never switched to (its check
    timed out), so nothing recorded the drop. Reusing that complete env (no
    install, nothing dropped now), what is left out is read from the
    receipts -- the running one has wandb, the new one does not -- and said."""
    from probe._shared import installs

    side_by_side["receipt"] = updater.KeptInstall(with_packages=(), python="/gone/bin/python3.12")
    monkeypatch.setattr(installs, "install", lambda version, *a, **k: tmp_path / "probe-versions" / version)
    result = updater.upgrade_side_by_side("0.1.0", "0.2.0")
    assert result.ok and side_by_side["dropped"] == [["wandb>=0.17"]]
    assert "left out --with wandb>=0.17" in result.message


def test_what_the_receipt_cannot_restate_is_said_not_a_reason_to_stay(side_by_side, monkeypatch):
    monkeypatch.setattr(updater, "kept_from_uv_receipt", lambda prefix=None: updater.KeptInstall(
        dropped=("--with mine",)))
    result = updater.upgrade_side_by_side("0.1.0", "0.2.0")
    assert result.ok and "not carried over from the uv receipt" in result.message and "--with mine" in result.message


def test_no_readable_release_on_a_side_by_side_machine_never_updates_in_place(side_by_side, monkeypatch):
    calls = []
    monkeypatch.setattr(updater, "_run", lambda cmd, timeout: calls.append(cmd) or subprocess.CompletedProcess(cmd, 0))
    monkeypatch.setattr(updater, "_finalize", lambda before, target, tool: updater.CliResult(
        True, True, True, before, "0.2.0", "upgraded in place"))
    result = updater.upgrade_cli(updater.Install(updater.Method.UV_TOOL), "0.1.0", None)
    assert not result.ok and "could not be read" in result.message and calls == []
    monkeypatch.setenv(updater.IN_PLACE_ENV, "1")  # a person who asked for in place still gets it
    assert updater.upgrade_cli(updater.Install(updater.Method.UV_TOOL), "0.1.0", None).ok and calls


@pytest.mark.parametrize("said, expected", [
    ({"result": "install_failed", "latest": "0.2.0", "detail": "no solution found"}, "no solution found"),
    ({"result": "busy", "detail": "another update holds it"}, "holds the install lock"),
])
def test_what_stage_one_could_not_do_is_reported_not_tried_again(side_by_side, said, expected):
    from probe.core import adopt

    adopt._answer = said
    result = updater.upgrade_side_by_side("0.1.0", "0.2.0")
    assert not result.ok and expected in result.message and result.before == "0.1.0"
    assert side_by_side["installs"] == []


def test_a_confirmed_codex_update_approves_probes_hooks(monkeypatch):
    """The path that heals machines installed before the wizard approved Probe's
    hooks, and any entry an update changed: every confirmed Codex plugin update
    approves them and says so."""
    from probe.cli import codex_hooks

    _fake_codex(monkeypatch, {})
    versions = {updater.tracking_plugin_name("codex"): "1.0.0", "probe-research-tap": "0.10.24"}
    monkeypatch.setattr(updater, "_codex_plugin_versions", lambda _codex=None: dict(versions))
    asked: list[int] = []

    def approve(*_a, **_k):
        asked.append(1)
        return codex_hooks.Approval(approved=("k",), done=True)

    monkeypatch.setattr(codex_hooks, "approve", approve)
    res = updater.update_codex_plugins()
    assert res.confirmed and asked == [1]
    assert res.message.endswith("; approved 1 Probe hook in Codex")
