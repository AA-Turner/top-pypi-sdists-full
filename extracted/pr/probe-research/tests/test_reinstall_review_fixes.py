"""Findings of the review of #3513 (plan clean-uninstall-reinstall), each held by a test that fails without its fix.

P1: another update's install lock is no refusal (configure went on to wait
120 s and exit 2 during any auto-update); a check that could not finish is
UNKNOWN, never "broken" (a loaded box rebuilt `+gN` and restarted the shared
service); `probe repair` rebuilds the newer of the active and the running
release, never one below 0.328.0; `PROBE_SERVICE_TOKEN` is no sign-in to
hold; a pipx env a process uses is never removed. P2: the barrier is cleared
under the install lock and read again first; every install path honours it;
`keeper-off` stays while an uninstall runs; `UV_OFFLINE` reads as uv does; a
busy machine's install is "installed; switches over"; identity runs before
the same-version check; runtime.json after every switch; the guard's
`--to-env`; a dead owner's barrier never says "running"; a shadowing pip
`probe` is named with its exact uninstall; `probe repair` reports a disabled
plugin instead of turning it on.

The second review (`test_r2_*`): an env whose check could not finish is kept
only when it is the env in use, never switched to; only a timeout, SIGKILL,
SIGTERM, EAGAIN or ENOMEM is UNKNOWN (a crash is BROKEN); `probe daemon
install` says busy and waiting; the stale barrier is unlinked right after its
last read; the in-place update reads the barrier inside the lock; a waiting
install is no "already installed"; the pip hint names the script's own Python.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from pathlib import Path

import pytest
import typer

from probe._shared import handoff, installs, uninstall_barrier
from probe.cli import bootstrap, install_pipeline, repair
from tests.reinstall_harness import OLD_VERSION, reinstall_wheels, uv_machine  # noqa: F401 -- fixtures
from tests.test_wizard_json_events import device  # noqa: F401 -- a fixture

posix = pytest.mark.skipif(sys.platform == "win32", reason="the side-by-side layout is POSIX only")


def _layout(*versions: str) -> None:
    for version in versions:
        out = install_pipeline.install_cli(version)
        assert out.ok, out.problems


def _hold_lock(root: Path) -> subprocess.Popen:
    holder = subprocess.Popen(
        [sys.executable, "-c",
         f"import fcntl, os, time\nfd = os.open({str(handoff.lock_path(root))!r}, os.O_RDWR | os.O_CREAT)\n"
         "fcntl.flock(fd, fcntl.LOCK_EX)\nprint('held', flush=True)\ntime.sleep(120)\n"],
        stdout=subprocess.PIPE, text=True,
    )
    assert holder.stdout.readline().strip() == "held"
    return holder


# -- P1 --------------------------------------------------------------------------


@posix
def test_p1_another_updates_lock_is_no_refusal_and_is_not_waited_for(uv_machine):
    """P1.1: configure's same-version check during an auto-update."""
    m = uv_machine
    _layout("1.0.0")
    holder = _hold_lock(installs.versions_root(m.tools))
    try:
        started = time.monotonic()
        result = bootstrap.verify_installed()
        assert time.monotonic() - started < 30, "never waits for the update's lock"
        assert result is not None and not result.refused and result.already_persistent
        assert result.message == install_pipeline.BUSY
        out = install_pipeline.install_cli("1.0.0", lock_wait_s=0)
        assert out.busy == install_pipeline.BUSY and not out.refused
    finally:
        holder.kill()
        holder.wait()


@posix
def test_p1_a_check_that_times_out_keeps_the_env(uv_machine, monkeypatch):
    """P1.2: a 30 s import timeout on a loaded box is UNKNOWN: no `+g2`
    rebuild, no switch, no restart of the shared service."""
    m = uv_machine
    _layout("1.0.0")
    env = installs.active(m.tools)
    run = next(env.glob("lib/python3*/site-packages/probe/core/run.py"))
    run.unlink()  # a new file: uv links an env's files to its cache
    run.write_text("import time\ntime.sleep(10)\n")
    monkeypatch.setattr(handoff, "IMPORT_TIMEOUT_S", 1.0)
    problem, broken = installs.check(env, "1.0.0")
    assert problem and "timed out" in problem and broken is False
    out = install_pipeline.install_cli("1.0.0")
    assert out.ok and not out.changed, (out.lines, out.problems)
    assert any("could not be checked" in line for line in out.lines)
    assert not (m.versions / "1.0.0+g2").exists()
    assert installs.active(m.tools) == env


def test_p1_a_selftest_timeout_or_signal_is_unknown_and_a_failure_is_broken(tmp_path):
    env = tmp_path / "env"
    (env / "bin").mkdir(parents=True)
    python = env / "bin" / "python"
    python.write_text('#!/bin/sh\ncase "$*" in *--selftest*) sleep 5 ;; esac\nexit 0\n')
    python.chmod(0o755)
    problem, broken = installs.selftest_checked(env, timeout=0.5)
    assert "did not answer" in problem and broken is False
    python.write_text('#!/bin/sh\nkill -9 $$\n')
    problem, broken = installs.selftest_checked(env, timeout=5)
    assert "signal 9" in problem and broken is False
    python.write_text('#!/bin/sh\necho "ImportError: x" >&2\nexit 1\n')
    problem, broken = installs.selftest_checked(env, timeout=5)
    assert "would not start" in problem and broken is True


def test_p1_the_repair_target_is_the_newer_release_and_never_below_0_328():
    assert repair.target_version("0.320.0", "0.331.1") == "0.331.1"
    assert repair.target_version("0.340.0", "0.331.1") == "0.340.0"
    assert repair.target_version(None, "0.331.1") == "0.331.1"
    assert repair.target_version("0.330.0+g2", "0.331.1") == "0.331.1"


@posix
def test_p1_repair_replaces_an_active_release_too_old_to_check(uv_machine, monkeypatch):
    """P1.4: an active 0.320-like env (no `probe.core.adopt`) is replaced by
    the running release, never rebuilt as itself."""
    import probe

    m = uv_machine
    m.tools.mkdir(parents=True)
    old = installs.install(OLD_VERSION, f"probe-research[all]=={OLD_VERSION}", tools=m.tools)
    installs.activate(old, tools=m.tools)
    installs.ensure_shims(m.tools)
    monkeypatch.setattr(probe, "__version__", "1.0.1")
    part, out = repair.repair_cli()
    assert not part.problems, part.problems
    assert installs.env_version(installs.active(m.tools)) == "1.0.1"
    assert not any(p.name.startswith(f"{OLD_VERSION}+g") for p in m.versions.iterdir())


def test_p1_a_service_token_is_never_held_to_the_sign_in(monkeypatch):
    """P1.5: `/v1/me` refuses PROBE_SERVICE_TOKEN by design."""
    from probe.cli import identity_check
    from probe.sdk.config import save_context

    save_context({"base_url": "https://api.example", "token": "probe_pat_mine"})
    answers = {"probe_pat_mine": ("ok", {"customer_id": "a", "user_id": "u"})}
    monkeypatch.setattr(identity_check, "whoami", lambda token, url: answers.get(token, ("rejected", None)))
    for name in identity_check.override_variables():
        monkeypatch.delenv(name, raising=False)
    monkeypatch.delenv("PROBE_BASE_URL", raising=False)
    monkeypatch.setenv("PROBE_SERVICE_TOKEN", "svc_token")
    assert "PROBE_SERVICE_TOKEN" not in identity_check.override_variables()
    assert identity_check.reconcile().problems == []


@posix
def test_p1_a_pipx_env_a_process_uses_is_never_removed(uv_machine, tmp_path, monkeypatch):
    m = uv_machine
    venv = tmp_path / "pipx" / "venvs" / "probe-research"
    (venv / "bin").mkdir(parents=True)
    (venv / "bin" / "probe").write_text("#!/bin/sh\n")
    m.bins.mkdir(parents=True, exist_ok=True)
    (m.bins / "probe").symlink_to(venv / "bin" / "probe")
    ran = []
    real_run = install_pipeline.subprocess.run
    monkeypatch.setattr(install_pipeline.subprocess, "run",
                        lambda argv, **kw: ran.append(argv) if argv[:1] == ["pipx"] else real_run(argv, **kw))
    monkeypatch.setattr(install_pipeline.shutil, "which", lambda name: f"/usr/bin/{name}")
    user = subprocess.Popen(["sh", "-c", "sleep 30", str(venv / "bin" / "probe")])
    try:
        said = install_pipeline.migrate_foreign(("pipx", str(m.bins / "probe")))
    finally:
        user.kill()
        user.wait()
    assert said == ["the old pipx install is still in use; removed next time"] and ran == []
    assert (m.bins / "probe").is_symlink()


# -- P2 --------------------------------------------------------------------------


def _barrier(**fields) -> Path:
    path = uninstall_barrier.path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"v": 1, "at": time.time(), "plan": "x", **fields}))
    return path


@posix
def test_p2_a_stale_barrier_is_cleared_only_under_the_install_lock(uv_machine):
    m = uv_machine
    _layout("1.0.0")
    path = _barrier(pid=2 ** 22 - 3, start="1", phase="planned")
    holder = _hold_lock(installs.versions_root(m.tools))
    try:
        assert install_pipeline.clear_stale_barrier(m.tools) is None and path.exists()
        assert bootstrap._repair_layout() == "" and path.exists()  # noqa: SLF001
    finally:
        holder.kill()
        holder.wait()
    assert "cleared" in install_pipeline.clear_stale_barrier(m.tools) and not path.exists()


def test_p2_a_barrier_rewritten_between_read_and_unlink_is_kept(monkeypatch):
    path = _barrier(pid=2 ** 22 - 3, start="1", phase="planned")
    real = uninstall_barrier.read
    calls = []

    def read(at=None):
        calls.append(1)
        data = real(at)
        return data if len(calls) == 1 else {**data, "pid": os.getpid(), "start": "new"}

    monkeypatch.setattr(uninstall_barrier, "read", read)
    assert uninstall_barrier.clear_stale() is None and path.exists()


def test_p2_the_in_place_update_and_daemon_install_honour_the_barrier(monkeypatch):
    from probe.cli import daemon_cli, updater
    from probe.service import procid

    _barrier(pid=os.getpid(), start=procid.start_time(os.getpid()), phase="stopping")
    result = updater.upgrade_cli(updater.Install(updater.Method.PIPX), "1.0.0", "1.0.1")
    assert not result.ok and "uninstall of Probe is running" in result.message
    monkeypatch.setattr(daemon_cli, "daemon_install", _real_daemon_install())
    with pytest.raises(typer.Exit) as done:
        daemon_cli.daemon_install()
    assert done.value.exit_code == 2


def _real_daemon_install():
    """The command's own function (conftest swaps the module's name for a tripwire)."""
    from probe.cli import daemon_cli

    return next(c.callback for c in daemon_cli.daemon_app.registered_commands if c.name == "install")


def test_p2_keeper_off_stays_while_an_uninstall_runs():
    from probe.service import keeper, paths, procid

    off = paths.root_dir() / keeper.OFF_NAME
    off.parent.mkdir(parents=True, exist_ok=True)
    off.touch()
    _barrier(pid=os.getpid(), start=procid.start_time(os.getpid()), phase="state")
    install_pipeline.clear_keeper_off()
    assert off.exists()
    uninstall_barrier.path().unlink()
    install_pipeline.clear_keeper_off()
    assert not off.exists()


@pytest.mark.parametrize("value, offline", [
    ("1", True), ("true", True), ("TRUE", True), ("yes", True), ("on", True), ("t", True), ("Y", True),
    ("0", False), ("false", False), ("", False), ("off", False),
])
def test_p2_uv_offline_reads_as_uv_reads_it(value, offline):
    assert installs.uv_offline({"UV_OFFLINE": value}) is offline


def test_p2_a_busy_machines_install_is_installed_and_switches_over(monkeypatch):
    out = install_pipeline.CliOutcome(ok=False, waiting="the first switch waits for a quiet machine (run_in_flight)")
    monkeypatch.setattr(install_pipeline, "install_cli", lambda *a, **kw: out)
    monkeypatch.setattr(install_pipeline, "layout_usable", lambda tools: True)
    monkeypatch.setattr(bootstrap.shutil, "which", lambda name: f"/usr/bin/{name}")
    result = bootstrap._install_managed("==1.0.1")  # noqa: SLF001
    assert "installed; switches over when this computer is quiet (within 24 h)" in result.message
    assert "could not install" not in result.message and not result.refused


def test_p2_identity_runs_before_the_same_version_check(monkeypatch):
    """No daemon worker starts on another team's key: `reconcile` before the
    check that may restart the service."""
    import importlib

    from typer.testing import CliRunner

    from probe.cli import identity_check

    main = importlib.import_module("probe.cli.main")

    order: list[str] = []
    monkeypatch.setattr(bootstrap, "ensure_persistent_install", lambda **_: bootstrap.BootstrapResult(
        False, True, ""))
    monkeypatch.setattr(identity_check, "reconcile_once", lambda: order.append("identity"))

    def verify():
        order.append("verify")
        raise typer.Exit(0)

    monkeypatch.setattr(bootstrap, "verify_installed", verify)
    monkeypatch.setattr(main, "_version_notice", lambda: None)
    monkeypatch.setattr(main, "_outbox_notice", lambda **_: None)
    result = CliRunner().invoke(main.app, ["wizard", "--action", "configure", "--yes"])
    assert order == ["identity", "verify"], (order, result.output)


@posix
def test_p2_every_switch_writes_runtime_json(uv_machine):
    from probe.service import client

    m = uv_machine
    _layout("1.0.0", "1.0.1")
    assert client.runtime_python() == str(installs.env_python(installs.active(m.tools)))
    assert installs.active(m.tools).parent.name == "1.0.1"


def test_p2_the_guard_tells_a_generation_by_its_env(monkeypatch):
    from probe.service import client, guard

    class Conn:
        def close(self):
            pass

        def call(self, *a, **kw):
            return {}

    hello = {"service_version": "1.0.0", "pid": 7, "env": "/v/1.0.0/probe-research"}
    monkeypatch.setattr(client, "no_new_privs", lambda: False)
    monkeypatch.setattr(guard, "_lock_free", lambda: True)
    monkeypatch.setattr(guard, "_keepalive", lambda: (Conn(), hello))
    said = guard.check("1.0.0", watch_s=0, to_env="/v/1.0.0+g2/probe-research")
    assert said == "the service runs from /v/1.0.0/probe-research, not /v/1.0.0+g2/probe-research"
    hello["env"] = "/v/1.0.0+g2/probe-research"
    assert guard.check("1.0.0", watch_s=0, to_env="/v/1.0.0+g2/probe-research") is None


def test_p2_a_dead_owners_barrier_never_says_running():
    path = _barrier(pid=2 ** 22 - 3, start="1", phase="planned")
    data = json.loads(path.read_text())
    path.write_text(json.dumps({**data, "v": 2}))  # LIVE (another schema), its owner gone
    said = uninstall_barrier.refusal()
    assert said and "running (pid" not in said and "in progress" in said


def test_p2_a_shadowing_pip_probe_is_named_with_its_exact_uninstall(tmp_path, monkeypatch):
    env = tmp_path / "venv"
    (env / "bin").mkdir(parents=True)
    probe_bin = env / "bin" / "probe"
    probe_bin.write_text(f"#!{env / 'bin' / 'python3.12'}\nimport sys\n")
    probe_bin.chmod(0o755)
    monkeypatch.setattr(bootstrap.shutil, "which", lambda name: str(probe_bin) if name == "probe" else "/usr/bin/uv")
    monkeypatch.setattr(install_pipeline, "foreign_install", lambda: ("pip", str(probe_bin)))
    said = bootstrap._fix_command("1.0.1")  # noqa: SLF001
    assert str(probe_bin) in said and f"{env / 'bin' / 'python3.12'} -m pip uninstall probe-research" in said
    assert "npx" not in said


def test_p2_probe_repair_reports_a_disabled_plugin_and_leaves_it_off(tmp_path, monkeypatch):
    from probe.cli import capabilities, integration_repair, plugin_cli

    claude = tmp_path / "claude"
    monkeypatch.setenv("CLAUDE_CONFIG_DIR", str(claude))
    m = capabilities.MARKETPLACE
    cache = claude / "plugins" / "cache" / m / "probe-research" / "1.0.0"
    cache.mkdir(parents=True)
    (claude / "plugins" / "installed_plugins.json").write_text(json.dumps({"version": 2, "plugins": {
        f"probe-research@{m}": [{"scope": "user", "installPath": str(cache)}]}}))
    settings = claude / "settings.json"
    settings.write_text(json.dumps({"enabledPlugins": {f"probe-research@{m}": False}}))
    done = repair.repair_integrations([plugin_cli.CLAUDE])[plugin_cli.CLAUDE]
    assert json.loads(settings.read_text())["enabledPlugins"][f"probe-research@{m}"] is False
    assert done.problems == [] and done.lines == [
        "probe-research is disabled by you; `probe wizard` turns it back on"]
    # Configure, a person's install, still turns it back on.
    integration_repair.repair(plugin_cli.CLAUDE)
    assert json.loads(settings.read_text())["enabledPlugins"][f"probe-research@{m}"] is True


def test_p2_install_command_skips_the_refresh_offline(monkeypatch):
    monkeypatch.setenv("UV_OFFLINE", "on")
    assert "--refresh-package" not in installs.install_command("probe-research[all]==1.0.0")
    monkeypatch.setenv("UV_OFFLINE", "0")
    assert "--refresh-package" in installs.install_command("probe-research[all]==1.0.0")


# -- the second review ------------------------------------------------------------


@posix
def test_r2_p1_an_unchecked_env_beside_the_active_one_is_never_switched_to(uv_machine, monkeypatch):
    """A `1.0.1` env a run left beside the active `1.0.0` (a fresh install
    whose check could not finish) was activated by the next run unchecked,
    and runtime.json and the shared service followed it."""
    m = uv_machine
    _layout("1.0.0")
    active = installs.active(m.tools)
    env = installs.install("1.0.1", "probe-research[all]==1.0.1", tools=m.tools)
    assert installs.active(m.tools) == active
    run = next(env.glob("lib/python3*/site-packages/probe/core/run.py"))
    run.unlink()  # a new file: uv links an env's files to its cache
    run.write_text("import time\ntime.sleep(10)\n")
    monkeypatch.setattr(handoff, "IMPORT_TIMEOUT_S", 1.0)
    out = install_pipeline.install_cli("1.0.1")
    assert installs.active(m.tools) == active, "switched to an env whose check never finished"
    assert not out.ok and not out.changed
    assert any("1.0.1's check could not finish" in p and "tried again next time" in p for p in out.problems)
    assert not (m.versions / "1.0.1+g2").exists(), "never rebuilt for a check that could not finish"


def _fake_env(tmp_path: Path, python: str) -> Path:
    """A finished uv install of 1.0.0 whose interpreter is `python` (a shell script)."""
    env = tmp_path / "env"
    (env / "bin").mkdir(parents=True)
    (env / installs.RECEIPT).write_text("[tool]\n")
    (env / "lib" / "python3.12" / "site-packages" / "probe_research-1.0.0.dist-info").mkdir(parents=True)
    interpreter = env / "bin" / "python"
    interpreter.write_text(python)
    interpreter.chmod(0o755)
    return env


@pytest.mark.skipif(sys.platform == "win32", reason="POSIX signals")
@pytest.mark.parametrize("sig, broken", [
    ("SIGKILL", False), ("SIGTERM", False), ("SIGSEGV", True), ("SIGBUS", True), ("SIGABRT", True), ("SIGILL", True),
])
def test_r2_p2_only_a_kill_by_the_machine_is_unknown(tmp_path, monkeypatch, sig, broken):
    """A crash (SIGSEGV, SIGBUS, SIGABRT, SIGILL) is the env's own: BROKEN, so
    `probe repair` rebuilds it. SIGKILL and SIGTERM are the machine's. (The
    exit status is faked: a real crash would leave a core dump on the box.)"""
    import signal

    number = int(getattr(signal, sig))
    monkeypatch.setattr(subprocess, "run", lambda argv, **kw: subprocess.CompletedProcess(argv, -number, "", ""))
    env = _fake_env(tmp_path, "#!/bin/sh\nexit 0\n")
    problem, found = installs.selftest_checked(env, timeout=10)
    assert f"signal {number}" in problem and found is broken
    problem, found = installs.check(env, "1.0.0")  # through the frozen `handoff.starts`
    assert f"signal {number}" in problem and found is broken


def test_r2_p2_an_interpreter_that_cannot_run_is_broken(tmp_path):
    """ENOEXEC (no `#!`, not a binary) and EACCES (not executable) are the env's."""
    for name, python, mode in (("noexec", "not a program\n", 0o755), ("noaccess", "#!/bin/sh\nexit 0\n", 0o644)):
        env = _fake_env(tmp_path / name, python)
        installs.env_python(env).chmod(mode)
        problem, broken = installs.selftest_checked(env, timeout=10)
        assert "could not be checked" in problem and broken is True, (name, problem)
        problem, broken = installs.check(env, "1.0.0")
        assert problem and broken is True, (name, problem)


@pytest.mark.parametrize("code", ["EAGAIN", "ENOMEM"])
def test_r2_p2_a_spawn_the_machine_refused_is_unknown(tmp_path, monkeypatch, code):
    import errno

    env = _fake_env(tmp_path, "#!/bin/sh\nexit 0\n")

    def refuse(*a, **kw):
        raise OSError(getattr(errno, code), os.strerror(getattr(errno, code)))

    monkeypatch.setattr(subprocess, "run", refuse)  # what `handoff.starts` and the selftest both call
    problem, broken = installs.selftest_checked(env, timeout=10)
    assert problem and broken is False
    problem, broken = installs.check(env, "1.0.0")
    assert problem and broken is False


def test_r2_p2_daemon_install_says_busy_and_waiting(monkeypatch, capsys):
    """`probe daemon install` read another update's lock and a switch that
    waits for a quiet machine as "the install did not end up working"."""
    from probe.cli import daemon_cli, updater

    outcome = {}
    monkeypatch.setattr(daemon_cli, "daemon_install", _real_daemon_install())
    monkeypatch.setattr(daemon_cli, "_installed_copy", lambda: None)
    monkeypatch.setattr(daemon_cli, "ai_libraries", lambda: None)
    monkeypatch.setattr(updater, "detect_install", lambda: updater.Install(updater.Method.UV_TOOL))
    monkeypatch.setattr(install_pipeline, "install_cli", lambda *a, **kw: outcome["out"])

    outcome["out"] = install_pipeline.CliOutcome(ok=False, busy=install_pipeline.BUSY)
    with pytest.raises(typer.Exit) as done:
        daemon_cli.daemon_install()
    err = capsys.readouterr().err
    assert done.value.exit_code == 2 and install_pipeline.BUSY in err and "did not end up working" not in err

    why = "the first switch waits for a quiet machine (run_in_flight)"
    outcome["out"] = install_pipeline.CliOutcome(ok=False, waiting=why, lines=["installed CLI 1.0.0 in 1.0.0+g2"])
    daemon_cli.daemon_install()  # no Exit: the wizard's provisioning reads any, 0 too, as a failed install
    said = capsys.readouterr()
    assert install_pipeline.QUIET_SWITCH in said.out and why in said.out
    assert "did not end up working" not in said.err


def test_r2_p2_a_stale_barrier_is_unlinked_with_no_process_lookup_after_the_last_read(monkeypatch):
    """Between the last read and the unlink an uninstall could write its own
    barrier; a process lookup there widened that window for nothing."""
    from probe.service import procid

    path = _barrier(pid=2 ** 22 - 3, start="1", phase="planned")
    lookups = []

    def alive(pid, start):
        lookups.append(pid)
        if len(lookups) > 1:  # an uninstall writes its barrier during this lookup
            path.write_text(json.dumps({"v": 1, "pid": os.getpid(), "start": procid.start_time(os.getpid()),
                                        "at": time.time(), "plan": "x", "phase": "planned"}))
        return False

    monkeypatch.setattr(procid, "alive", alive)
    said = uninstall_barrier.clear_stale()
    assert len(lookups) == 1, "a process lookup between the last read and the unlink"
    assert said and "cleared" in said and not path.exists()


@pytest.mark.parametrize("method", ["uv_tool", "uv_tool_legacy"])
def test_r2_p2_the_in_place_update_reads_the_barrier_again_inside_the_lock(monkeypatch, method):
    """An uninstall that wrote its barrier while the update waited for the
    install lock: nothing is installed in place under it."""
    import contextlib

    from probe.cli import updater
    from probe.service import procid

    ran = []

    @contextlib.contextmanager
    def lock():
        _barrier(pid=os.getpid(), start=procid.start_time(os.getpid()), phase="stopping")
        yield

    monkeypatch.setattr(updater, "_install_lock", lock)
    monkeypatch.setattr(updater, "upgrade_side_by_side", lambda current, target: None)
    monkeypatch.setattr(updater, "_upgrade_in_place", lambda current, target: ran.append("in place"))
    monkeypatch.setattr(updater, "_run", lambda cmd, timeout: ran.append(cmd))
    monkeypatch.setattr(updater, "kept_from_uv_receipt", lambda prefix=None: updater.KeptInstall())
    monkeypatch.delenv(updater.REQUIRE_SIDE_BY_SIDE_ENV, raising=False)
    install = updater.Install(updater.Method.UV_TOOL if method == "uv_tool" else updater.Method.UV_TOOL_LEGACY)
    result = updater.upgrade_cli(install, "1.0.0", "1.0.1")
    assert ran == [] and not result.ok and "uninstall of Probe is running" in result.message


def test_r2_p2_a_waiting_install_is_installed_and_configure_never_checks_the_old_one(monkeypatch):
    """configure read "switches over when quiet" as "already installed", ran
    the same-version check on the old active version and dropped the line."""
    import importlib

    from typer.testing import CliRunner

    from probe.cli import identity_check, upgrading
    from probe.core import events

    main = importlib.import_module("probe.cli.main")
    why = "the first switch waits for a quiet machine (run_in_flight)"
    monkeypatch.setattr(install_pipeline, "install_cli", lambda *a, **kw: install_pipeline.CliOutcome(
        ok=False, waiting=why))
    monkeypatch.setattr(install_pipeline, "layout_usable", lambda tools: True)
    monkeypatch.setattr(install_pipeline, "refusal", lambda **_: None)
    monkeypatch.setattr(bootstrap.shutil, "which", lambda name: f"/usr/bin/{name}")
    monkeypatch.setattr(bootstrap, "_foreign_to_move", lambda: None)
    monkeypatch.setattr(bootstrap, "_resolves_on_path", lambda: False)
    monkeypatch.setattr(bootstrap, "installed_version", lambda: "1.0.0")
    result = bootstrap.ensure_persistent_install(target="1.0.1")
    assert result.installed and result.waiting and not result.already_persistent and not result.refused
    assert install_pipeline.QUIET_SWITCH in result.message and why in result.message

    order: list[str] = []
    monkeypatch.setattr(identity_check, "reconcile_once", lambda: order.append("identity"))
    monkeypatch.setattr(bootstrap, "verify_installed", lambda: order.append("verify"))

    def stop(boot):
        order.append("reported")
        raise typer.Exit(0)

    monkeypatch.setattr(events, "persistent_install", stop)
    monkeypatch.setattr(main, "_version_notice", lambda: None)
    monkeypatch.setattr(main, "_outbox_notice", lambda **_: None)
    ran = CliRunner().invoke(main.app, ["wizard", "--action", "configure", "--yes"])
    assert order == ["reported"], (order, ran.output)
    assert install_pipeline.QUIET_SWITCH in ran.output

    # `probe update` from npx: not done, and nothing moved.
    lines: list[str] = []
    res = upgrading._update_persistent_copy("1.0.1", lines)  # noqa: SLF001
    assert res is not None and not res.ok and not res.changed and install_pipeline.QUIET_SWITCH in res.message


@pytest.mark.parametrize("script, python", [
    ("#!/usr/bin/env python3\nimport sys\n", None),
    ("#!/bin/sh\necho hi\n", None),
    ("#!/bin/sh\n'''exec' \"/opt/my env/bin/python3\" \"$0\" \"$@\"\n' '''\n", "/opt/my env/bin/python3"),
    ("#!/opt/venv/bin/python3.11 -E\n", "/opt/venv/bin/python3.11"),
])
def test_r2_p2_the_pip_hint_names_the_python_from_the_scripts_own_line(tmp_path, monkeypatch, script, python):
    """The hint made up `<dir>/python`, which a venv may not have (python3.12
    only) and a `bin` shared by many environments never names."""
    probe_bin = tmp_path / "bin" / "probe"
    probe_bin.parent.mkdir()
    probe_bin.write_text(script)
    probe_bin.chmod(0o755)
    monkeypatch.setattr(bootstrap.shutil, "which", lambda name: str(probe_bin) if name == "probe" else "/usr/bin/uv")
    monkeypatch.setattr(install_pipeline, "foreign_install", lambda: ("pip", str(probe_bin)))
    said = bootstrap._fix_command("1.0.1")  # noqa: SLF001
    assert f"{tmp_path / 'bin' / 'python'} -m pip" not in said
    if python:
        assert f"`{python} -m pip uninstall probe-research`" in said
    else:
        assert f"`pip uninstall probe-research` run by the Python that owns {probe_bin}" in said


def test_r2_p2_an_unreadable_pip_script_names_the_python_that_owns_it(tmp_path, monkeypatch):
    probe_bin = tmp_path / "bin" / "probe"  # gone by the time it is read
    monkeypatch.setattr(bootstrap.shutil, "which", lambda name: str(probe_bin) if name == "probe" else "/usr/bin/uv")
    monkeypatch.setattr(install_pipeline, "foreign_install", lambda: ("pip", str(probe_bin)))
    said = bootstrap._fix_command("1.0.1")  # noqa: SLF001
    assert f"the Python that owns {probe_bin}" in said and "/bin/python -m pip" not in said


# -- V-T2: a fresh install leaves the service, keeper and lifeboat on (C5) ---------


def _ensure_spy(monkeypatch, outcome="running") -> list[float]:
    from probe.service import client

    waits: list[float] = []
    monkeypatch.setattr(client, "ensure", lambda *, wait=0.0: waits.append(wait) or outcome)
    return waits


def test_c5_a_fresh_install_through_configure_starts_the_service(device, real_service_start, monkeypatch):
    """`npx probe-research install --yes` on a fresh machine ended "ok" with no
    service, no keeper units and no lifeboat until the first agent session:
    the service's start installs both, and nothing started it."""
    import importlib

    from typer.testing import CliRunner

    main = importlib.import_module("probe.cli.main")
    monkeypatch.setattr(bootstrap, "ensure_persistent_install", lambda **_: bootstrap.BootstrapResult(
        installed=True, already_persistent=False, message="Installed `probe` 1.0.1 (uv, beside any running one)."))
    waits = _ensure_spy(monkeypatch)
    ran = CliRunner().invoke(main.app, ["wizard", "--action", "configure", "--yes", "--tracking", "--capture",
                                        "--auto-update", "--agent-rules", "--agent", "claude", "--agent", "codex"])
    assert ran.exit_code == 0, ran.output
    assert len(waits) == 1 and waits[0] > 0, "the install never started the Probe service"
    assert "not running yet" not in ran.output


def test_c5_a_service_that_cannot_start_is_one_line_and_never_a_failure(real_service_start, monkeypatch):
    from probe.service import keeper

    boats = []
    monkeypatch.setattr(keeper, "refresh_lifeboat", lambda: boats.append(1) or "installed")
    _ensure_spy(monkeypatch, "confined")
    said = install_pipeline.start_service(wait_s=0)
    assert said and "no_new_privs" in said and "next agent session starts it" in said and boats == [1]

    monkeypatch.setattr(keeper, "wanted", lambda: True)
    monkeypatch.setattr(keeper, "systemd_manager", lambda: False)
    _ensure_spy(monkeypatch, "running")
    expected = install_pipeline.NO_KEEPER if sys.platform.startswith("linux") else None
    assert install_pipeline.start_service(wait_s=0) == expected


def test_c5_no_service_starts_while_an_uninstall_runs(real_service_start, monkeypatch):
    from probe.service import procid

    _barrier(pid=os.getpid(), start=procid.start_time(os.getpid()), phase="stopping")
    waits = _ensure_spy(monkeypatch)
    assert install_pipeline.start_service() is None and waits == []


def test_c5_probe_daemon_install_starts_the_service(real_service_start, monkeypatch):
    from probe.cli import daemon_cli, updater

    monkeypatch.setattr(daemon_cli, "daemon_install", _real_daemon_install())
    monkeypatch.setattr(daemon_cli, "_installed_copy", lambda: None)
    monkeypatch.setattr(daemon_cli, "ai_libraries", lambda: None)
    monkeypatch.setattr(daemon_cli, "_fresh_ai_libraries", lambda python: "2.51.0")
    monkeypatch.setattr(updater, "detect_install", lambda: updater.Install(updater.Method.UV_TOOL))
    monkeypatch.setattr(install_pipeline, "install_cli", lambda *a, **kw: install_pipeline.CliOutcome(
        ok=True, env=Path("/v/1.0.0+g2/probe-research"), version="1.0.0", changed=True))
    waits = _ensure_spy(monkeypatch)
    daemon_cli.daemon_install()
    assert len(waits) == 1


def test_a_stopped_uninstall_names_its_finisher_only_once_it_is_there():
    """The refusal sent people to `uninstall/finisher.py`, which the uninstall
    copies in only at its "finishing" phase: before that, the file is not there."""
    path = _barrier(pid=2 ** 22 - 3, start="1", phase="server", plan="/s/uninstall/plan.json")
    said = uninstall_barrier.refusal()
    assert "`probe uninstall`" in said and "finisher.py" not in said
    finisher = path.parent / "finisher.py"
    finisher.write_text("# the uninstall's finisher\n")
    said = uninstall_barrier.refusal()
    assert "`probe uninstall`" in said and f"`python3 {finisher} --plan /s/uninstall/plan.json`" in said


# -- V-T2: identity first at every entry that installs or changes the sign-in (R-T4)


def _two_teams(monkeypatch, *, daemon: bool = True, interactive: bool = False) -> list[str]:
    """`/v1/me` for each credential: team-a's sign-in and daemon key, team-b's
    sign-in. The revoked keys, as `setup._revoke` was asked."""
    from probe.cli import identity_check
    from probe.cli import setup as wizard

    answers = {
        "probe_pat_a": ("ok", {"customer_id": "team-a", "user_id": "u-a"}),
        "probe_pat_daemon_a": ("ok", {"customer_id": "team-a", "user_id": "u-a"}),
        "probe_pat_b": ("ok", {"customer_id": "team-b", "user_id": "u-b"}),
        "probe_pat_daemon_b": ("ok", {"customer_id": "team-b", "user_id": "u-b"}),
    }
    monkeypatch.setattr(identity_check, "whoami", lambda token, url: answers.get(token, ("rejected", None)))
    for name in identity_check.override_variables():
        monkeypatch.delenv(name, raising=False)
    monkeypatch.delenv("PROBE_BASE_URL", raising=False)
    monkeypatch.setattr(identity_check, "_daemon_in_use", lambda: daemon)
    monkeypatch.setattr(identity_check, "_interactive", lambda: interactive)
    revoked: list[str] = []
    monkeypatch.setattr(wizard, "_revoke", lambda key, *, base_url, what: revoked.append(key) or [f"revoked {what}"])
    return revoked


@pytest.mark.parametrize("interactive", [False, True])
def test_vt2_daemon_install_holds_the_daemon_key_to_the_sign_in(monkeypatch, capsys, interactive):
    """team-b signed in over team-a's daemon key: `probe daemon install` (its
    "already installed" path returned before anything was checked) left the
    key, and daemon writes went to team-a."""
    import importlib

    from probe.cli import daemon_cli
    from probe.sdk.config import load_context, save_context

    main = importlib.import_module("probe.cli.main")
    save_context({"base_url": "https://api.example", "token": "probe_pat_b", "companion_token": "probe_pat_daemon_a"})
    revoked = _two_teams(monkeypatch, interactive=interactive)
    monkeypatch.setattr(main, "_authorize_companion", lambda url, open_browser=True: save_context(
        {"companion_token": "probe_pat_daemon_b"}) and ["approved a daemon key for team-b"])
    monkeypatch.setattr(daemon_cli, "daemon_install", _real_daemon_install())
    monkeypatch.setattr(daemon_cli, "_installed_copy", lambda: None)
    monkeypatch.setattr(daemon_cli, "ai_libraries", lambda: "2.51.0")
    if interactive:
        daemon_cli.daemon_install()
        assert load_context()["companion_token"] == "probe_pat_daemon_b", "a new key, approved for team-b"
    else:
        with pytest.raises(typer.Exit) as done:
            daemon_cli.daemon_install()
        assert done.value.exit_code == 1 and "INCOMPLETE" in capsys.readouterr().err
        assert not load_context().get("companion_token"), "dropped: nobody here can approve a new one"
    assert revoked == ["probe_pat_daemon_a"]


def test_vt2_probe_login_holds_the_daemon_key_to_the_new_sign_in(monkeypatch):
    import importlib

    from typer.testing import CliRunner

    from probe.sdk.config import load_context, save_context

    main = importlib.import_module("probe.cli.main")
    save_context({"base_url": "https://api.example", "token": "probe_pat_a", "companion_token": "probe_pat_daemon_a"})
    revoked = _two_teams(monkeypatch, daemon=False)

    class _Client:
        def __enter__(self):
            return self

        def __exit__(self, *exc):
            return False

        def me(self):
            return {"email": "b@example.test", "customer_id": "team-b", "user_id": "u-b"}

    monkeypatch.setattr(main, "_new_client", lambda **_: _Client())
    ran = CliRunner().invoke(main.app, ["login", "--token", "probe_pat_b", "--base-url", "https://api.example"])
    assert ran.exit_code == 0, ran.output
    assert revoked == ["probe_pat_daemon_a"] and not load_context().get("companion_token")


def test_vt2_switching_context_holds_its_daemon_key_to_its_sign_in(monkeypatch):
    import importlib

    from typer.testing import CliRunner

    from probe.sdk.config import load_context, save_context, use_context

    main = importlib.import_module("probe.cli.main")
    save_context({"base_url": "https://api.example", "token": "probe_pat_a", "companion_token": "probe_pat_daemon_a"},
                 name="a")
    # An earlier release's sign-in to team-b in this context kept team-a's key.
    save_context({"base_url": "https://api.example", "token": "probe_pat_b", "companion_token": "probe_pat_daemon_a"},
                 name="b")
    use_context("a")
    revoked = _two_teams(monkeypatch, daemon=False)
    ran = CliRunner().invoke(main.app, ["context", "use", "b"])
    assert ran.exit_code == 0, ran.output
    assert revoked == ["probe_pat_daemon_a"] and not load_context("b").get("companion_token")
    assert load_context("a")["companion_token"] == "probe_pat_daemon_a", "the other context's own key stays"
