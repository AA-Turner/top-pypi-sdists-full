"""Tests for `probe update` internals (cli/updater.py) + the command's --check codes.

Covers the hardening the eng review demanded: install detection from the running
package path (H4), the legacy probe-agent dance (H3), editable/managed guards
(H5/H6), the plugin post-condition + non-TTY spawn (H1/H2), and --check exit
codes distinct from main()'s 1/2 (H7).
"""

from __future__ import annotations

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


def test_upgrade_uv_tool_pinned_noop_then_force(monkeypatch):
    # `uv tool upgrade` no-ops on a version pin (exits 0, version unchanged) -> force @latest
    calls = _record_run(monkeypatch)
    _stub_installed(monkeypatch, ["0.8.1", "0.8.2"])  # after upgrade (no move), after force (moved)
    res = updater.upgrade_cli(updater.Install(updater.Method.UV_TOOL), "0.8.1", "0.8.2")
    assert res.ok and res.changed and res.after == "0.8.2"
    assert calls == [
        ["uv", "tool", "install", "probe-research[all]"],
        ["uv", "tool", "upgrade", "probe-research"],
        ["uv", "tool", "install", "--force", "--refresh-package", "probe-research", "probe-research[all]@latest"],
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
        if name == "pydantic_ai":
            raise ImportError(name)
        return real_import(name, *a, **kw)

    monkeypatch.setattr(builtins, "__import__", without_daemon)
    assert updater._dist() == "probe-research[all]"
    monkeypatch.setattr(builtins, "__import__", real_import)
    import sys
    import types

    monkeypatch.setitem(sys.modules, "pydantic_ai", types.ModuleType("pydantic_ai"))
    assert updater._dist() == "probe-research[all,daemon]"


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
    """`codex plugin list` failing and a plugin genuinely missing both leave the
    list empty, so the message claims neither."""
    _fake_codex(monkeypatch, {"plugin list --json": _failed_with("boom")})

    res = updater.update_codex_plugins()

    assert not res.confirmed
    assert res.message == (
        "could not confirm probe-research or probe-research-tap in "
        "`codex plugin list --json` after reinstalling"
    )


def test_a_codex_list_that_is_not_an_object_reads_as_empty(monkeypatch):
    _fake_codex(
        monkeypatch,
        {"plugin list --json": subprocess.CompletedProcess([], 0, stdout="[]", stderr="")},
    )
    assert updater._codex_plugin_versions() == {}


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
    monkeypatch.setattr(upgrading.autoupdate, "record_attempt", lambda attempt: None)
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
    assert ["uv", "tool", "install", "--force", "--refresh-package", "probe-research", "probe-research[all,daemon]@latest"] in calls
