"""Several coding agents' install and update steps run at once.

An Update used to repeat the whole update once per agent (the CLI's upgrade,
the manifest, `pi update`) and move each agent's plugins after the last one's;
an install refreshed and installed one agent after another. Measured on a
4-agent machine: an Update 18.4 s -> 6.1 s, an install 8.8 s -> 6.1 s.
"""

from __future__ import annotations

import os
import threading
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


def test_a_live_run_defers_every_agents_update(one_update, monkeypatch):
    from probe.cli import autoupdate, run_lock, update_report

    monkeypatch.setattr(run_lock, "any_live", lambda: True)
    monkeypatch.setattr(autoupdate, "record_skip", lambda *a, **k: None)
    monkeypatch.setattr(update_report, "flush", lambda *a, **k: None)
    monkeypatch.delenv(upgrading.FORCED_ENV, raising=False)

    outcomes = upgrading.perform_updates(["claude_code", "codex"], base_url="https://x")

    assert one_update["cli"] == [] and one_update["plugins"] == []
    assert all("deferred" in outcome.lines[0] for outcome in outcomes.values())


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


def test_a_pass_that_raises_still_lets_the_others_be_recorded(one_update, monkeypatch):
    """The CLI moved and Claude Code's plugins too: those are recorded (the
    only failure record a detached update writes) before the error rises, and
    the pass that raised is recorded as the failure, so the run's merged
    record and report do not say ok."""
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
    with pytest.raises(RuntimeError, match="codex exploded"):
        upgrading.perform_updates(["claude_code", "codex"], base_url="https://x")
    assert [agent for agent, _ in recorded] == ["Claude Code", "Codex"]
    merged = autoupdate.merge_attempts(recorded)
    assert not merged.plugin_ok and "codex exploded" in merged.plugin_detail
    report = update_report.merge_passes(reports)
    assert report["outcome"] == "failed"
    assert report["plugin"]["result"] == "error" and "codex exploded" in report["plugin"]["detail"]


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
