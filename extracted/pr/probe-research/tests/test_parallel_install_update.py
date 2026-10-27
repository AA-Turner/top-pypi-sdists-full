"""Several coding agents' install and update steps run at once.

An Update used to repeat the whole update once per agent (the CLI's upgrade,
the manifest, `pi update`) and move each agent's plugins after the last one's;
an install refreshed and installed one agent after another. Measured on a
4-agent machine: an Update 18.4 s -> 6.1 s, an install 8.8 s -> 6.1 s.
"""

from __future__ import annotations

import os
import threading
import time
from types import SimpleNamespace

import pytest

from probe.cli import claude_cli, updater, upgrading
from probe.cli import setup as wizard
from probe.cli.capabilities import Capability


def _plugin_result(name: str) -> updater.PluginResult:
    return updater.PluginResult(
        attempted=True, confirmed=True, changed=False, before="1", after="1", message=f"{name} current"
    )


@pytest.fixture
def one_update(monkeypatch):
    """An update whose halves are stand-ins, counting what ran and on which thread."""
    ran: dict[str, list[str]] = {"cli": [], "pi": [], "plugins": []}
    both = threading.Barrier(2, timeout=5)
    monkeypatch.setattr(updater, "fetch_latest", lambda base: {})
    monkeypatch.setattr(updater, "detect_install", lambda: updater.Install(updater.Method.UV_TOOL))
    monkeypatch.setattr(upgrading, "_report_attempt", lambda *a, **k: None)
    monkeypatch.setattr(
        updater,
        "upgrade_cli",
        lambda install, current, target: ran["cli"].append(threading.current_thread().name)
        or updater.CliResult(ran=True, ok=True, changed=False, before=current, after=current, message="cli current"),
    )
    monkeypatch.setattr(
        upgrading, "_update_pi_package", lambda: ran["pi"].append(1) or upgrading._PiUpdate(["pi current"])
    )

    def plugins(name):
        def update(*_args):
            ran["plugins"].append(name)
            both.wait()  # BrokenBarrierError unless Claude Code's and Codex's overlap
            return _plugin_result(name)

        return update

    monkeypatch.setattr(updater, "update_plugin", plugins("claude_code"))
    monkeypatch.setattr(updater, "update_codex_plugins", plugins("codex"))
    monkeypatch.setattr(updater, "stale_tap_daemons", lambda *a, **k: ())
    monkeypatch.setattr(updater, "follows_without_restart", lambda *a, **k: False)
    monkeypatch.setattr(upgrading.root_skills, "refresh", lambda source: [])
    return ran


def test_an_update_for_several_agents_upgrades_the_cli_and_pi_once(one_update):
    outcomes = upgrading.perform_updates(["claude_code", "codex", "pi"], base_url="https://x")

    assert list(outcomes) == ["claude_code", "codex", "pi"]
    assert len(one_update["cli"]) == 1 and len(one_update["pi"]) == 1
    assert sorted(one_update["plugins"]) == ["claude_code", "codex"]  # at once (the barrier)
    # The CLI's lines once, on the first agent; pi's package on pi's own answer.
    assert any("cli current" in line for line in outcomes["claude_code"].lines)
    assert not any("cli current" in line for line in outcomes["codex"].lines)
    assert any("codex current" in line for line in outcomes["codex"].lines)
    assert outcomes["pi"].lines == ["pi current"]
    assert all(outcome.ok for outcome in outcomes.values())


@pytest.mark.parametrize(
    ("deferred_for", "forced", "updates"),
    [
        (None, None, False),  # a run that just started
        (60, None, False),
        # Without a service, a day of runs is the limit, as the service's (C3).
        (24 * 3600 + 60, None, True),
        # The service decided to go past a run (D33) ...
        (None, "run_in_flight", True),
        # ... or past a setup only (C1): that is no decision about a run.
        (None, "setup_running", False),
    ],
)
def test_a_live_run_defers_every_agents_update_for_a_day_at_most(
    one_update, monkeypatch, tmp_path, deferred_for, forced, updates
):
    import time

    from probe import version_policy
    from probe.cli import autoupdate, run_lock, update_report

    for name, sub in (("HOME", "home"), ("XDG_STATE_HOME", "state"), ("XDG_CONFIG_HOME", "config"),
                      ("CLAUDE_CONFIG_DIR", "claude"), ("CODEX_HOME", "codex"), ("PI_CODING_AGENT_DIR", "pi")):
        monkeypatch.setenv(name, str(tmp_path / sub))
    monkeypatch.setattr(run_lock, "any_live", lambda: True)
    monkeypatch.setattr(update_report, "flush", lambda *a, **k: None)
    if forced:
        monkeypatch.setenv(upgrading.FORCED_ENV, forced)
    else:
        monkeypatch.delenv(upgrading.FORCED_ENV, raising=False)
    if deferred_for is not None:  # runs held it off since then, the latest a minute ago
        version_policy.atomic_write_json(version_policy.state_path(), {
            autoupdate.RUN_DEFERRED_SINCE_KEY: time.time() - deferred_for,
            autoupdate.RUN_DEFERRED_LAST_KEY: time.time() - 60,
        })

    outcomes = upgrading.perform_updates(["claude_code", "codex"], base_url="https://x")

    ran = (len(one_update["cli"]), sorted(one_update["plugins"]))
    assert ran == ((1, ["claude_code", "codex"]) if updates else (0, []))
    assert all(("deferred" in outcome.lines[0]) is not updates for outcome in outcomes.values())


def test_the_install_batch_installs_each_agents_plugins_with_its_refresh(monkeypatch):
    """Both agents refresh and install at once, inside the first refresh; each
    agent's own install steps take those answers once (a retry installs for
    real); a capability the sign-in did not get a credential for is left to
    its own step, which the run then skips."""
    both = threading.Barrier(2, timeout=5)
    ran: list[tuple[str, str]] = []

    def refresh(source):
        both.wait()
        return claude_cli.Result(ok=True, detail=source)

    monkeypatch.setattr(wizard, "_refresh_marketplace_now", refresh)
    monkeypatch.setattr(
        wizard.plugin_cli, "install",
        lambda source, plugin_id: ran.append((source, plugin_id)) or claude_cli.Result(ok=True, detail=plugin_id),
    )
    plan = {
        "claude_code": [(Capability.TRACKING, "probe-research"), (Capability.CAPTURE, "probe-research-tap")],
        "codex": [(Capability.TRACKING, "probe-research"), (Capability.CAPTURE, "probe-research-tap")],
    }
    with wizard.marketplace_refreshes(["claude_code", "codex"], plan):
        wizard.allow_batch_installs([Capability.TRACKING])  # no capture credential
        assert wizard.refresh_marketplace(source="claude_code").ok
        assert sorted(ran) == [
            ("claude_code", "probe-research@research-os-agent"),
            ("codex", "probe-research@research-os-agent"),
        ]
        assert wizard.install_plugin("probe-research", source="codex").detail == "probe-research@research-os-agent"
        assert len(ran) == 2  # taken, not run again
        wizard.install_plugin("probe-research", source="codex")  # a second ask runs for real
        assert len(ran) == 3


def test_a_batch_without_an_allowance_installs_nothing_early(monkeypatch):
    monkeypatch.setattr(wizard, "_refresh_marketplace_now", lambda source: claude_cli.Result(ok=True))
    monkeypatch.setattr(wizard.plugin_cli, "install", lambda *a: pytest.fail("installed before its step"))
    with wizard.marketplace_refreshes(["claude_code"], {"claude_code": [(Capability.TRACKING, "probe-research")]}):
        assert wizard.refresh_marketplace(source="claude_code").ok


def test_the_install_plan_keeps_each_agents_order_and_leaves_a_legacy_tap_to_its_step(monkeypatch):
    import importlib

    from probe.cli import plugin_cli
    from probe.cli.capabilities import Capabilities

    main = importlib.import_module("probe.cli.main")
    monkeypatch.setattr(plugin_cli, "available", lambda source: True)
    caps = {
        "claude_code": Capabilities(agent_source="claude_code"),
        "codex": Capabilities(agent_source="codex", legacy_capture_plugin_installed=True),
        "pi": Capabilities(agent_source="pi"),
    }
    plan = main._install_plan(caps, SimpleNamespace(tracking=True, capture=True))
    assert [capability for capability, _ in plan["claude_code"]] == [Capability.TRACKING, Capability.CAPTURE]
    assert plan["codex"] == [(Capability.TRACKING, plan["codex"][0][1])]  # its tap after the legacy one goes
    assert "pi" not in plan  # no marketplace


def test_kimi_is_asked_its_version_once_per_binary(monkeypatch, tmp_path):
    from probe.cli import kimi_config

    binary = tmp_path / "kimi"
    binary.write_text("#!/bin/sh\necho 2.3.4\n")
    binary.chmod(0o755)
    monkeypatch.setenv("PATH", f"{tmp_path}{os.pathsep}{os.environ.get('PATH', '')}")
    asked: list[int] = []
    real_run = kimi_config.subprocess.run
    monkeypatch.setattr(
        kimi_config.subprocess, "run", lambda *a, **k: asked.append(1) or real_run(*a, **k)
    )
    kimi_config._version_of.cache_clear()

    first = kimi_config.kimi_version()
    assert kimi_config.kimi_version() == first and len(asked) == 1
    binary.write_text("#!/bin/sh\necho 2.3.50\n")  # a reinstall
    assert kimi_config.kimi_version() != first and len(asked) == 2


def test_a_pass_that_raises_fails_only_its_own_agent(one_update, monkeypatch):
    """The CLI moved and Claude Code's plugins too: those are recorded (the
    only failure record a detached update writes) and answered ok, and the
    pass that raised is recorded and answered as the failure, so the run's
    merged record and report do not say ok. Nothing rises (plan A3, I7): the
    update's other steps (the wizard's registration, its summary) go on."""
    from probe.cli import autoupdate, update_report

    recorded: list[tuple[str | None, autoupdate.Attempt]] = []
    reports: list[dict] = []
    monkeypatch.setattr(
        autoupdate, "record_attempt", lambda attempt, agent=None: recorded.append((agent, attempt))
    )
    monkeypatch.setattr(upgrading, "_report_attempt", lambda build, **k: reports.append(build()))
    monkeypatch.setattr(updater, "update_plugin", lambda *a: _plugin_result("claude_code"))

    def broken(*_args):
        raise RuntimeError("codex exploded")

    monkeypatch.setattr(updater, "update_codex_plugins", broken)
    outcomes = upgrading.perform_updates(["claude_code", "codex"], base_url="https://x")
    assert outcomes["claude_code"].ok and not outcomes["codex"].ok
    assert any("codex exploded" in line for line in outcomes["codex"].lines)
    assert any("codex exploded" in problem for problem in outcomes["codex"].problems)
    assert [agent for agent, _ in recorded] == ["Claude Code", "Codex"]
    merged = autoupdate.merge_attempts(recorded)
    assert not merged.plugin_ok and "codex exploded" in merged.plugin_detail
    report = update_report.merge_passes(reports)
    assert report["outcome"] == "failed"
    assert report["plugin"]["result"] == "error" and "codex exploded" in report["plugin"]["detail"]


@pytest.fixture
def short_deadline(monkeypatch):
    """Each component's deadline (plan A3) cut to half a second; a hung
    component's thread is let go when the test ends."""
    monkeypatch.setenv(upgrading.COMPONENT_DEADLINE_ENV, "0.5")
    release = threading.Event()
    yield release
    release.set()


def _recording(monkeypatch):
    from probe.cli import autoupdate

    recorded: list = []
    reports: list[dict] = []
    monkeypatch.setattr(autoupdate, "record_attempt", lambda attempt, agent=None: recorded.append((agent, attempt)))
    monkeypatch.setattr(upgrading, "_report_attempt", lambda build, **k: reports.append(build()))
    return recorded, reports


def test_a_hung_agent_fails_alone_at_its_deadline(one_update, monkeypatch, short_deadline):
    """Codex's plugin step hangs (`codex plugin list` that never answers):
    at its deadline it is failed and left running; the CLI's step and Claude
    Code's finish, and every pass is recorded and reported."""
    from probe.cli import update_report

    recorded, reports = _recording(monkeypatch)
    monkeypatch.setattr(updater, "update_plugin", lambda *a: _plugin_result("claude_code"))
    monkeypatch.setattr(updater, "update_codex_plugins", lambda *a: short_deadline.wait(30) and _plugin_result("codex"))

    outcomes = upgrading.perform_updates(["claude_code", "codex"], base_url="https://x")

    assert outcomes["claude_code"].ok and not outcomes["codex"].ok
    assert any("did not finish within 0.5 s" in line for line in outcomes["codex"].lines)
    assert len(one_update["cli"]) == 1 and len(one_update["pi"]) == 1
    assert [agent for agent, _ in recorded] == ["Claude Code", "Codex"]
    report = update_report.merge_passes(reports)
    assert report["outcome"] == "failed" and report["plugin"]["result"] == "error"
    assert "did not finish" in report["plugin"]["detail"]


@pytest.mark.skipif(os.name == "nt", reason="process groups")
def test_a_component_past_its_deadline_has_its_processes_stopped(one_update, monkeypatch, short_deadline, tmp_path):
    """Codex's step hangs inside `codex plugin list`: at the deadline that
    process's whole group is killed, and the step starts nothing more -- it
    must not go on changing plugins after the update has moved on."""
    from probe.cli import claude_cli

    _recording(monkeypatch)
    pidfile = tmp_path / "pid"
    after: list = []

    def hung_codex(*_args):
        try:
            claude_cli.capture(["sh", "-c", f"echo $$ > {pidfile}; exec sleep 30"], timeout=60)
        except OSError as exc:
            after.append(exc)
        try:
            claude_cli.capture(["true"], timeout=5)
        except claude_cli.StoppedError as exc:
            after.append(exc)
        return _plugin_result("codex")

    monkeypatch.setattr(updater, "update_plugin", lambda *a: _plugin_result("claude_code"))
    monkeypatch.setattr(updater, "update_codex_plugins", hung_codex)
    outcomes = upgrading.perform_updates(["claude_code", "codex"], base_url="https://x")

    assert not outcomes["codex"].ok and any("was stopped (1 process)" in line for line in outcomes["codex"].lines)
    pid = int(pidfile.read_text())
    deadline = time.monotonic() + 5
    while time.monotonic() < deadline and len(after) < 2:
        time.sleep(0.05)
    with pytest.raises(ProcessLookupError):
        os.kill(pid, 0)
    assert [type(exc) for exc in after] == [claude_cli.StoppedError, claude_cli.StoppedError]


_SIGNALLED_UPDATE = """
import sys
from pathlib import Path

from probe.cli import claude_cli, updater, upgrading

out = Path(sys.argv[1])
updater.fetch_latest = lambda base: {}
updater.detect_install = lambda: updater.Install(updater.Method.EDITABLE)
upgrading._update_pi_package = lambda: upgrading._PiUpdate([])
upgrading._report_attempt = lambda *a, **k: None


def hung(name):
    def run(*_args):
        claude_cli.capture(["sh", "-c", f"echo $$ > {out / name}; exec sleep 60"], timeout=120)
        return updater.PluginResult(True, True, False, "1", "1", "ok")
    return run


updater.update_plugin = hung("claude")
updater.update_codex_plugins = hung("codex")
upgrading.perform_updates(["claude_code", "codex"], base_url="https://x")
"""


@pytest.mark.skipif(os.name == "nt", reason="process groups and POSIX signals")
@pytest.mark.parametrize("sig", ["SIGINT", "SIGTERM"])
def test_ctrl_c_or_the_services_sigterm_leaves_no_tracked_process(tmp_path, sig):
    """Each agent's CLI runs in a session of its own (so its deadline can stop
    its whole group), out of reach of a signal to the update's group: Ctrl-C
    in a terminal, or the service's SIGTERM to its update child's group. The
    update stops them itself on the way out."""
    import signal
    import subprocess
    import sys

    from probe._shared import handoff

    script = tmp_path / "update.py"
    script.write_text(_SIGNALLED_UPDATE)
    update = subprocess.Popen([sys.executable, str(script), str(tmp_path)], start_new_session=True,
                              stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)
    try:
        deadline = time.monotonic() + 30
        while time.monotonic() < deadline and not all((tmp_path / n).exists() for n in ("claude", "codex")):
            assert update.poll() is None, update.stderr.read()
            time.sleep(0.05)
        pids = [int((tmp_path / name).read_text()) for name in ("claude", "codex")]
        assert all(handoff.proc_start(pid) for pid in pids)
        os.killpg(update.pid, getattr(signal, sig))
        update.wait(30)
        deadline = time.monotonic() + 10
        while time.monotonic() < deadline and any(handoff.proc_start(pid) for pid in pids):
            time.sleep(0.05)
        assert not any(handoff.proc_start(pid) for pid in pids), "a tracked process outlived the update"
    finally:
        if update.poll() is None:
            update.kill()
        for name in ("claude", "codex"):
            with __import__("contextlib").suppress(Exception):
                os.kill(int((tmp_path / name).read_text()), 9)


@pytest.mark.skipif(os.name == "nt", reason="POSIX signals")
def test_the_wait_leaves_an_existing_handler_alone_and_puts_the_default_back():
    """A handler someone set (the json session's `events._stop`) is theirs:
    left as it is. A default SIGTERM gets the wait's own handler, which
    ignores a second signal while the update stops, and the default is put
    back after the wait."""
    import signal

    def theirs(*_args):
        pass

    previous = signal.signal(signal.SIGHUP, theirs)
    term = signal.signal(signal.SIGTERM, signal.SIG_DFL)
    try:
        with upgrading._stopped_with_the_update([]):
            assert signal.getsignal(signal.SIGHUP) is theirs
            assert signal.getsignal(signal.SIGTERM) is upgrading._exit_on_signal
            with pytest.raises(SystemExit) as stopped:
                upgrading._exit_on_signal(signal.SIGTERM, None)
            assert stopped.value.code == 128 + signal.SIGTERM
            assert signal.getsignal(signal.SIGTERM) is signal.SIG_IGN  # a second one waits its turn
            assert signal.getsignal(signal.SIGHUP) is theirs
        assert signal.getsignal(signal.SIGTERM) is signal.SIG_DFL
        assert signal.getsignal(signal.SIGHUP) is theirs
    finally:
        signal.signal(signal.SIGHUP, previous)
        signal.signal(signal.SIGTERM, term)


def test_a_single_agent_update_whose_plugins_raise_still_answers(one_update, monkeypatch, short_deadline):
    """`perform_update` (one agent): its plugin step raising is that step's
    failure, recorded; the update answers instead of raising."""
    recorded, _reports = _recording(monkeypatch)
    monkeypatch.setattr(upgrading, "agent_source", lambda: "claude_code")

    def broken(*_args):
        raise RuntimeError("claude exploded")

    monkeypatch.setattr(updater, "update_plugin", broken)
    outcome = upgrading.perform_update(base_url="https://x")
    assert not outcome.ok and any("claude exploded" in line for line in outcome.lines)
    assert one_update["cli"] and recorded and not recorded[-1][1].plugin_ok


@pytest.mark.parametrize("how", ["raises", "hangs"])
def test_pi_failing_or_hanging_fails_only_pis_step(one_update, monkeypatch, short_deadline, how):
    """pi's package step used to run unguarded in the shared prelude: one that
    raised ended the whole update, one that hung held it. Now it is pi's step
    that fails (owed, so pi's next start tries again); the CLI's step and the
    agents' plugins finish."""
    from probe.cli import autoupdate

    _recording(monkeypatch)
    owed: list[bool] = []
    monkeypatch.setattr(autoupdate, "mark_pi_update_pending", lambda pending: owed.append(pending))
    monkeypatch.setattr(updater, "update_plugin", lambda *a: _plugin_result("claude_code"))
    monkeypatch.setattr(updater, "update_codex_plugins", lambda *a: _plugin_result("codex"))

    def pi():
        if how == "raises":
            raise OSError("npm exploded")
        short_deadline.wait(30)
        return upgrading._PiUpdate(["pi current"])

    monkeypatch.setattr(upgrading, "_update_pi_package", pi)
    outcomes = upgrading.perform_updates(["claude_code", "codex", "pi"], base_url="https://x")

    reason = "npm exploded" if how == "raises" else "did not finish within 0.5 s"
    assert any(reason in line for line in outcomes["pi"].lines)
    assert not outcomes["pi"].ok and owed == [True]
    assert one_update["cli"]
    for source in ("claude_code", "codex"):
        assert any(f"{source} current" in line for line in outcomes[source].lines)


def test_a_failed_cli_upgrade_is_named_on_every_agents_answer(one_update, monkeypatch):
    """Each agent's `ok` carries the CLI's failure, and `--json` sends each
    agent's lines as its reason: every row must say why."""
    monkeypatch.setattr(
        updater, "upgrade_cli",
        lambda install, current, target: updater.CliResult(
            ran=True, ok=False, changed=False, before=current, after=current, message="uv refused"
        ),
    )
    monkeypatch.setattr(updater, "update_plugin", lambda *a: _plugin_result("claude_code"))
    monkeypatch.setattr(updater, "update_codex_plugins", lambda *a: _plugin_result("codex"))
    outcomes = upgrading.perform_updates(["claude_code", "codex"], base_url="https://x")
    for outcome in outcomes.values():
        assert not outcome.ok and any("uv refused" in line for line in outcome.lines)


def test_an_install_that_raises_does_not_fail_the_refresh(monkeypatch):
    monkeypatch.setattr(wizard, "_refresh_marketplace_now", lambda source: claude_cli.Result(ok=True, detail="fresh"))

    def explode(source, plugin_id):
        raise OSError("disk full")

    monkeypatch.setattr(wizard.plugin_cli, "install", explode)
    with wizard.marketplace_refreshes(["claude_code"], {"claude_code": [(Capability.TRACKING, "probe-research")]}):
        wizard.allow_batch_installs([Capability.TRACKING])
        assert wizard.refresh_marketplace(source="claude_code").detail == "fresh"
        with pytest.raises(OSError, match="disk full"):  # the agent's own step installs for real
            wizard.install_plugin("probe-research", source="claude_code")


def test_kimi_is_run_by_its_path_name_for_a_version_managers_shim(monkeypatch, tmp_path):
    """A shim decides what to run by the name it is called with: run the PATH
    entry, never the program it links to."""
    from probe.cli import kimi_config

    shared = tmp_path / "shim"
    shared.write_text('#!/bin/sh\n[ "$(basename "$0")" = kimi ] && echo 2.3.4 || echo 9.9.9\n')
    shared.chmod(0o755)
    (tmp_path / "bin").mkdir()
    (tmp_path / "bin" / "kimi").symlink_to(shared)
    monkeypatch.setenv("PATH", f"{tmp_path / 'bin'}{os.pathsep}{os.environ.get('PATH', '')}")
    kimi_config._version_of.cache_clear()
    assert kimi_config.kimi_version() == (2, 3, 4)
