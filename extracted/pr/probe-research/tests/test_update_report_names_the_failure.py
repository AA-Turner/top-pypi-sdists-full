"""A failed update report always names the step that failed.

Production, 2026-10-23: two Macs sent `outcome = failed` while the CLI, the
plugin and the tap each read `updated` or `current` with no detail (and the
0.285.0 updater did the same on 10-22). The outcome and the components come
from two different rules -- `upgrading._perform_update`'s `plugin_ok` and
`update_report`'s `*_component` -- and wherever the first said "failed" while
the second found nothing wrong, the report could not say what failed:

  * the pi package failing on a Claude Code or Codex pass fails that pass, but
    its plugin component is the marketplace plugin's, which worked;
  * an agent with none of Probe's plugins in it ("nothing to update" in the
    component rule) failed the pass anyway;
  * an agent whose plugin list could not be read looked like one with nothing
    installed;
  * in a run merged from several agents' passes (the wizard's Update, which the
    Probe service runs on every Mac with Codex and Claude Code), an agent that
    failed lost each component to a pass that did not.

The other way round, a tap the update removed read `error` on a report whose
outcome said `ok`.

Every test here drives the real `perform_update` (and `merged_run`) with the
plugin steps faked; nothing reaches a real agent CLI or the server.
"""

from __future__ import annotations

import itertools
import json
import os

import pytest

from probe.cli import autoupdate, claude_cli, kimi_config, update_report, updater, upgrading

MANIFEST = {
    "cli": {"latest": "0.296.0"},
    "plugin": {"latest": "0.168.0"},
    "tap": {"latest": "0.10.13"},
}
Result = update_report.Result
#: The results that say a component did not end where the update meant it to.
FAILING = {Result.ERROR, Result.REFRESH_FAILED, Result.BEHIND, Result.NOT_FOUND_ON_PATH}
_REAL_UPDATE_CODEX = updater.update_codex_plugins


@pytest.fixture(autouse=True)
def isolate(tmp_path, monkeypatch):
    monkeypatch.setenv("HOME", str(tmp_path / "home"))
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))
    monkeypatch.setenv("PROBE_CONFIG_PATH", str(tmp_path / "config" / "probe" / "config.json"))
    monkeypatch.setenv("PROBE_DEVICE_ID_PATH", str(tmp_path / "state" / "device.json"))
    monkeypatch.setenv("PROBE_TOKEN", "probe_pat_" + "0" * 32)
    monkeypatch.delenv("PROBE_BASE_URL", raising=False)
    monkeypatch.delenv("PROBE_AGENT", raising=False)
    monkeypatch.delenv(autoupdate.WAIT_FOR_PID_ENV, raising=False)
    monkeypatch.delenv(autoupdate.TRIGGER_ENV, raising=False)
    monkeypatch.setattr(updater, "fetch_latest", lambda base: MANIFEST)
    monkeypatch.setattr(updater, "detect_install", lambda: updater.Install(updater.Method.UV_TOOL))
    monkeypatch.setattr(upgrading, "__version__", "0.292.0")
    _cli(monkeypatch, ok=True)
    # No live capture daemons: this machine's own must not leak into a report.
    monkeypatch.setattr(updater, "stale_tap_daemons", lambda source, installed: ())
    # No pi package unless a test installs one.
    monkeypatch.setattr(upgrading, "_update_pi_package", lambda: _pi(update_report.PiStep.NOT_INSTALLED))


@pytest.fixture
def sent(monkeypatch):
    bodies: list[dict] = []

    def _accept(base_url, headers, body, timeout):
        bodies.append(body)
        return 202

    monkeypatch.setattr(update_report, "_deliver", _accept)
    return bodies


def _cli(monkeypatch, *, ok: bool):
    def _upgrade(install, current, target):
        if ok:
            return updater.CliResult(True, True, True, current, target, f"CLI upgraded {current} → {target}")
        return updater.CliResult(True, False, False, current, current, "`uv tool upgrade` did not complete: offline")

    monkeypatch.setattr(updater, "upgrade_cli", _upgrade)


def _pi(code, *, detail=""):
    ok = code is not update_report.PiStep.FAILED
    return upgrading._PiUpdate(
        ["pi package:", f"  {detail or code.value}"], ok=ok,
        detail=detail if not ok else "", ran=code is not update_report.PiStep.NOT_INSTALLED,
        code=code, before="0.5.0", after="0.5.0",
    )


PI_FAILED = _pi(update_report.PiStep.FAILED, detail="pi package not updated: npm ERR! network")


def _plugins(monkeypatch, by_agent: dict[str, updater.PluginResult]):
    """Each agent's plugin step answers from `by_agent`, keyed on the agent the
    pass runs for (PROBE_AGENT)."""
    step = lambda *args: by_agent[os.environ["PROBE_AGENT"]]  # noqa: E731
    monkeypatch.setattr(updater, "update_plugin", step)
    monkeypatch.setattr(updater, "update_codex_plugins", step)
    monkeypatch.setattr(updater, "update_kimi_plugins", step)


def _pass(monkeypatch, agent: str):
    monkeypatch.setenv("PROBE_AGENT", agent)
    return upgrading.perform_update(
        base_url="https://api.test", include_plugin=True, trigger=update_report.Trigger.SESSION_START
    )


def _ok_plugin(*, before="0.167.0", tap_before="0.10.11"):
    """What Claude Code's pass said on kimball-jaguars: everything moved."""
    return updater.PluginResult(
        True, True, before != "0.168.0", before, "0.168.0", "plugin updated to 0.168.0",
        tap_before=tap_before, tap_after="0.10.13",
    )


def _named(report: dict) -> list[tuple[str, str, str]]:
    """Every component of `report` whose result is a failing one."""
    return [
        (name, report[name]["result"], report[name]["detail"])
        for name in ("cli", "plugin", "tap")
        if report.get(name) and Result(report[name]["result"]) in FAILING
    ]


def _assert_names_its_failure(report: dict) -> None:
    named = _named(report)
    if report["outcome"] == "failed":
        assert named, f"failed, and no component says what failed: {report}"
        assert all(detail for _n, _r, detail in named), f"a failing component with no detail: {report}"
    else:
        hard = [n for n in named if Result(n[1]) in (Result.ERROR, Result.REFRESH_FAILED)]
        assert not hard, f"ok, while a component reads failed: {report}"


# ---------------------------------------------------------------------------
# The paths that sent "failed" with nothing failing
# ---------------------------------------------------------------------------


def test_a_failed_pi_package_on_a_claude_code_pass_is_named(monkeypatch, sent):
    """pi's package is updated on every pass, whatever agent runs it, and its
    failure fails the pass -- but the plugin slot carried Claude Code's plugin,
    which had moved, so the report read updated/updated/updated, failed."""
    _plugins(monkeypatch, {"claude_code": _ok_plugin()})
    monkeypatch.setattr(upgrading, "_update_pi_package", lambda: PI_FAILED)

    outcome = _pass(monkeypatch, "claude_code")

    assert not outcome.ok
    [report] = sent
    assert report["outcome"] == "failed"
    assert report["harness"] == "claude_code"
    assert report["plugin"]["result"] == Result.ERROR
    assert report["plugin"]["harness"] == "pi"
    assert "npm ERR! network" in report["plugin"]["detail"]
    assert report["tap"]["result"] == Result.UPDATED
    assert report["tap"]["harness"] == "claude_code"


def test_a_plugin_failure_beside_a_pi_failure_keeps_the_plugins_own(monkeypatch, sent):
    _plugins(monkeypatch, {"claude_code": updater.PluginResult(
        True, False, False, "0.167.0", "0.167.0", "`claude plugin update` did not complete: EACCES",
        tap_before="0.10.13", tap_after="0.10.13", command_failed=True,
    )})
    monkeypatch.setattr(upgrading, "_update_pi_package", lambda: PI_FAILED)

    _pass(monkeypatch, "claude_code")

    [report] = sent
    assert report["plugin"]["result"] == Result.ERROR
    assert report["plugin"]["harness"] == "claude_code"
    assert "EACCES" in report["plugin"]["detail"]


def test_a_pi_package_that_waits_on_another_update_changes_nothing(monkeypatch, sent):
    """A locked pi step is not a failure, and it must not stand in for a
    plugin that moved."""
    _plugins(monkeypatch, {"claude_code": _ok_plugin()})
    monkeypatch.setattr(upgrading, "_update_pi_package", lambda: _pi(update_report.PiStep.LOCKED))

    _pass(monkeypatch, "claude_code")

    [report] = sent
    assert report["outcome"] == "ok"
    assert report["plugin"]["result"] == Result.UPDATED
    assert report["plugin"]["harness"] == "claude_code"


def _ledger(plugins: dict[str, str]) -> None:
    path = os.path.join(os.environ["HOME"], ".claude", "plugins", "installed_plugins.json")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as handle:
        json.dump({"plugins": {key: [{"version": v}] for key, v in plugins.items()}}, handle)


def _claude(monkeypatch, *, fail_on: str | None = None, then=None):
    """A fake `claude` on PATH: fails the command containing `fail_on`, and
    calls `then(command)` after each one (to change the ledger under it)."""
    monkeypatch.setattr(
        updater.shutil, "which", lambda name: f"/usr/local/bin/{name}" if name == "claude" else None
    )

    def _run(args, *, timeout):
        command = " ".join(["claude", *args])
        if then is not None:
            then(command)
        if fail_on and fail_on in command:
            return claude_cli.Result(ok=False, detail="Error: plugin not installed", command=command)
        return claude_cli.Result(ok=True, command=command)

    monkeypatch.setattr(updater.claude_cli, "run", _run)


def test_claude_code_without_probes_plugins_is_not_a_failed_update(monkeypatch, sent):
    """Claude Code on PATH, Probe's marketplace added, none of Probe's plugins
    installed: `claude plugin update` fails because there is nothing to update.
    The component rule always read that `not_installed` ("its command failing
    then is the consequence"); the outcome rule called it a failure, every
    session, on a machine where nothing is wrong."""
    _ledger({})
    _claude(monkeypatch, fail_on="update probe-research@")

    outcome = _pass(monkeypatch, "claude_code")

    assert outcome.ok
    [report] = sent
    assert report["outcome"] == "ok"
    assert report["plugin"]["result"] == Result.NOT_INSTALLED
    assert report["tap"]["result"] == Result.NOT_INSTALLED
    assert autoupdate.load().last_attempt.plugin_ok is True


def test_a_tap_left_without_its_plugin_is_still_a_failure(monkeypatch, sent):
    """Only the tap installed: the update had something to move, so a failed
    plugin command is a failure, and the plugin component says so."""
    _ledger({"probe-research-tap@research-os-agent": "0.10.13"})
    _claude(monkeypatch, fail_on="update probe-research@")

    _pass(monkeypatch, "claude_code")

    [report] = sent
    assert report["outcome"] == "failed"
    assert report["plugin"]["result"] == Result.ERROR
    assert "plugin not installed" in report["plugin"]["detail"]
    _assert_names_its_failure(report)


def _codex(monkeypatch, *, listing, add_fails=False):
    """A fake `codex` on PATH whose `plugin list --json` prints `listing` (a
    dict), or fails when `listing` is None."""
    monkeypatch.setattr(
        updater.shutil, "which", lambda name: f"/usr/local/bin/{name}" if name == "codex" else None
    )
    ok = claude_cli.Result(ok=True)

    def _list(source):
        if listing is None:
            return claude_cli.Result(ok=False, detail="error: unrecognized subcommand", command="codex plugin list --json")
        return claude_cli.Result(ok=True, detail=json.dumps(listing))

    def _install(source, plugin_id):
        if add_fails:
            return claude_cli.Result(ok=False, detail="Error: plugin not found", command=f"codex plugin add {plugin_id}")
        return ok

    monkeypatch.setattr(updater.plugin_cli, "refresh_marketplace", lambda source, market: ok)
    monkeypatch.setattr(updater.plugin_cli, "install", _install)
    monkeypatch.setattr(updater.plugin_cli, "list_plugins", _list)


def test_codex_without_probes_plugins_is_not_a_failed_update(monkeypatch, sent):
    _codex(monkeypatch, listing={"installed": []}, add_fails=True)

    outcome = _pass(monkeypatch, "codex")

    assert outcome.ok
    [report] = sent
    assert report["outcome"] == "ok"
    assert report["plugin"]["result"] == Result.NOT_INSTALLED
    assert report["tap"]["result"] == Result.NOT_INSTALLED


def test_a_codex_plugin_list_it_cannot_read_is_a_named_failure(monkeypatch, sent):
    """An unreadable list is not an empty one: nothing says Probe is absent,
    and nothing confirmed the reinstall. It read `not_installed` beside a
    failed outcome."""
    _codex(monkeypatch, listing=None)

    outcome = _pass(monkeypatch, "codex")

    assert not outcome.ok
    [report] = sent
    assert report["outcome"] == "failed"
    assert report["plugin"]["result"] == Result.ERROR
    assert "codex plugin list --json" in report["plugin"]["detail"]


def test_a_kimi_plugin_list_that_fails_is_a_named_failure(monkeypatch, sent):
    monkeypatch.setattr(kimi_config, "binary_available", lambda: True)
    monkeypatch.setattr(
        updater.plugin_cli, "list_plugins",
        lambda source: claude_cli.Result(ok=False, detail="kimi: config.toml is not valid TOML",
                                         command="kimi plugin list"),
    )

    outcome = _pass(monkeypatch, "kimi_code")

    assert not outcome.ok
    [report] = sent
    assert report["plugin"]["result"] == Result.ERROR
    assert "not valid TOML" in report["plugin"]["detail"]


def test_a_first_codex_install_that_stops_halfway_is_a_failure(monkeypatch, sent):
    """Nothing listed before; the tracking plugin's add worked and the tap's
    failed. Probe is in Codex now, so this is not "nothing installed"."""
    listings = iter([{"installed": []},
                     {"installed": [{"name": "probe-research", "version": "0.168.0"}]}])
    _codex(monkeypatch, listing={})
    monkeypatch.setattr(
        updater.plugin_cli, "list_plugins",
        lambda source: claude_cli.Result(ok=True, detail=json.dumps(next(listings))),
    )
    monkeypatch.setattr(
        updater.plugin_cli, "install",
        lambda source, plugin_id: (
            claude_cli.Result(ok=False, detail="Error: EACCES", command=f"codex plugin add {plugin_id}")
            if plugin_id.startswith("probe-research-tap@")
            else claude_cli.Result(ok=True)
        ),
    )

    outcome = _pass(monkeypatch, "codex")

    assert not outcome.ok
    [report] = sent
    assert report["outcome"] == "failed"
    assert report["plugin"]["result"] == Result.ERROR
    assert report["plugin"]["after"] == "0.168.0"
    assert "EACCES" in report["plugin"]["detail"]


def test_a_claude_ledger_it_cannot_read_is_not_nothing_installed(monkeypatch, sent):
    """`_ledger_version` reads a corrupt ledger as "not installed"; the update
    cannot tell, so a failed command stays a failure."""
    path = os.path.join(os.environ["HOME"], ".claude", "plugins", "installed_plugins.json")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as handle:
        handle.write('{"plugins": {"probe-research@research-os-agent": [{"vers')
    _claude(monkeypatch, fail_on="update probe-research@")

    outcome = _pass(monkeypatch, "claude_code")

    assert not outcome.ok
    [report] = sent
    assert report["outcome"] == "failed"
    assert report["plugin"]["result"] == Result.ERROR
    assert "plugin not installed" in report["plugin"]["detail"]


def test_a_tap_the_update_removed_fails_the_update(monkeypatch, sent):
    """The tap was installed before and is gone after: capture stops at the
    next session. The component always read `error`; the outcome said ok and
    the screen said "not installed (skipped)"."""
    _ledger({"probe-research@research-os-agent": "0.168.0",
             "probe-research-tap@research-os-agent": "0.10.12"})

    def _drop_tap(command):
        if "update probe-research-tap@" in command:
            _ledger({"probe-research@research-os-agent": "0.168.0"})

    _claude(monkeypatch, then=_drop_tap)

    outcome = _pass(monkeypatch, "claude_code")

    assert not outcome.ok
    assert any("transcript tap 0.10.12 is gone after the update" in line for line in outcome.lines)
    [report] = sent
    assert report["outcome"] == "failed"
    assert report["tap"]["result"] == Result.ERROR
    assert report["tap"]["detail"]


def test_a_codex_tap_it_could_not_list_afterwards_is_not_called_gone(monkeypatch, sent):
    listings = iter([
        {"installed": [{"name": "probe-research", "version": "0.168.0"},
                       {"name": "probe-research-tap", "version": "0.10.12"}]},
        None,
    ])
    _codex(monkeypatch, listing={})
    monkeypatch.setattr(
        updater.plugin_cli, "list_plugins",
        lambda source, listing=None: (
            claude_cli.Result(ok=True, detail=json.dumps(listing))
            if (listing := next(listings)) is not None
            else claude_cli.Result(ok=False, detail="boom", command="codex plugin list --json")
        ),
    )

    outcome = _pass(monkeypatch, "codex")

    assert any("transcript tap 0.10.12 could not be confirmed after the update" in line
               for line in outcome.lines)
    [report] = sent
    assert report["outcome"] == "failed"
    assert report["tap"]["result"] == Result.ERROR
    assert "could not be confirmed" in report["tap"]["detail"]
    assert report["plugin"]["result"] == Result.ERROR


def test_a_tap_that_moved_but_not_far_enough_says_so(monkeypatch, sent):
    """Moved, so no command failed and no no-op was named: the behind tap had
    an empty detail."""
    _ledger({"probe-research@research-os-agent": "0.168.0",
             "probe-research-tap@research-os-agent": "0.10.11"})

    def _move_tap(command):
        if "update probe-research-tap@" in command:
            _ledger({"probe-research@research-os-agent": "0.168.0",
                     "probe-research-tap@research-os-agent": "0.10.12"})

    _claude(monkeypatch, then=_move_tap)

    _pass(monkeypatch, "claude_code")

    [report] = sent
    assert report["outcome"] == "failed"
    assert report["tap"]["result"] == Result.BEHIND
    assert "0.10.13" in report["tap"]["detail"]


# ---------------------------------------------------------------------------
# A run merged from several agents' passes
# ---------------------------------------------------------------------------


def test_the_production_shape_names_the_codex_pass(monkeypatch, sent):
    """kimball-jaguars, 2026-10-23 14:39Z: the Probe service's update ran the
    wizard's Update, one pass for Claude Code (all three moved) and one for
    Codex. The report read cli/plugin/tap updated, all from claude_code, outcome
    failed: Codex's failure ranked below Claude Code's "updated"."""
    _plugins(monkeypatch, {"claude_code": _ok_plugin()})
    with update_report.merged_run():
        _pass(monkeypatch, "claude_code")
        _codex(monkeypatch, listing=None)
        _pass_real_codex(monkeypatch)

    [report] = sent
    assert report["outcome"] == "failed"
    assert report["plugin"]["result"] == Result.ERROR
    assert report["plugin"]["harness"] == "codex"
    assert report["tap"]["result"] == Result.UPDATED
    assert report["tap"]["harness"] == "claude_code"
    _assert_names_its_failure(report)


def _pass_real_codex(monkeypatch):
    """The Codex pass through the real `update_codex_plugins` (over `_codex`'s
    fakes), after `_plugins` replaced it for the Claude Code pass."""
    monkeypatch.setattr(updater, "update_codex_plugins", _REAL_UPDATE_CODEX)
    return _pass(monkeypatch, "codex")


def test_a_codex_without_probe_no_longer_fails_the_run(monkeypatch, sent):
    _plugins(monkeypatch, {"claude_code": _ok_plugin()})
    with update_report.merged_run():
        _pass(monkeypatch, "claude_code")
        _codex(monkeypatch, listing={"installed": []}, add_fails=True)
        _pass_real_codex(monkeypatch)

    [report] = sent
    assert report["outcome"] == "ok"
    assert report["plugin"]["result"] == Result.UPDATED


def test_a_failed_pass_is_never_hidden_by_a_pass_that_did_not_fail(monkeypatch, sent):
    """Claude Code's tap stayed behind (the pass failed); Codex is not on the
    updater's PATH (not a failure). `not_found_on_path` outranks `behind`, so
    the merged tap said Codex was missing and nothing said what failed."""
    behind = updater.PluginResult(
        True, True, False, "0.168.0", "0.168.0", "plugin already at the latest (0.168.0)",
        tap_before="0.10.12", tap_after="0.10.12", tap_detail=updater.TAP_NOOP,
    )
    missing = updater.PluginResult(
        False, False, False, None, None, "`codex` not found on PATH (skipping plugin update)",
        missing_binary=True,
    )
    _plugins(monkeypatch, {"claude_code": behind, "codex": missing})
    with update_report.merged_run():
        _pass(monkeypatch, "claude_code")
        _pass(monkeypatch, "codex")

    [report] = sent
    assert report["outcome"] == "failed"
    assert report["tap"]["result"] == Result.BEHIND
    assert report["tap"]["harness"] == "claude_code"
    assert report["tap"]["detail"] == updater.TAP_NOOP


# ---------------------------------------------------------------------------
# The invariant, over every shape a pass can end in
# ---------------------------------------------------------------------------


def _shape(attempted, confirmed, before, after, message, **tap):
    return lambda: updater.PluginResult(attempted, confirmed, False, before, after, message, **tap)


#: Built when a test runs (each is a factory), so a field this file needs
#: fails that test, not the whole module's collection.
PLUGIN_SHAPES = {
    "current": _shape(True, True, "0.168.0", "0.168.0", "plugin already at the latest",
                      tap_before="0.10.13", tap_after="0.10.13"),
    "tap_noop_behind": _shape(True, True, "0.168.0", "0.168.0", "plugin already at the latest",
                              tap_before="0.10.12", tap_after="0.10.12", tap_detail=updater.TAP_NOOP),
    "tap_command_failed": _shape(True, True, "0.168.0", "0.168.0", "plugin already at the latest",
                                 tap_before="0.10.12", tap_after="0.10.12",
                                 tap_detail="`claude plugin update` did not complete: EACCES"),
    "tap_moved_short": _shape(True, True, "0.168.0", "0.168.0", "plugin already at the latest",
                              tap_before="0.10.11", tap_after="0.10.12"),
    "tap_removed": _shape(True, True, "0.168.0", "0.168.0", "plugin already at the latest",
                          tap_before="0.10.12", tap_after=None, tap_detail=updater.TAP_NOOP),
    "legacy_tap": _shape(True, True, "0.168.0", "0.168.0", "plugin already at the latest",
                         legacy_ids=("prbe-cc-tap-plugin@prbe-ai",)),
    "binary_missing": _shape(False, False, None, None, "`claude` not found on PATH",
                             tap_before="0.10.12", tap_after="0.10.12", missing_binary=True),
    "nothing_in_kimi": _shape(False, False, None, None, "no Probe plugins installed in Kimi Code"),
    "refresh_failed": _shape(True, False, "0.167.0", "0.167.0", "`claude plugin marketplace update` failed",
                             tap_before="0.10.12", tap_after="0.10.12", tap_detail="refresh failed",
                             refresh_failed=True, command_failed=True),
    "refresh_failed_nothing_installed": _shape(True, False, None, None, "refresh failed: no marketplace",
                                               refresh_failed=True, command_failed=True),
    "command_failed": _shape(True, False, "0.167.0", "0.167.0", "`claude plugin update` failed: EACCES",
                             tap_before="0.10.13", tap_after="0.10.13", command_failed=True),
    "nothing_installed": _shape(True, False, None, None, "`claude plugin update` failed: not installed",
                                tap_detail="not installed", command_failed=True),
    "only_the_tap": _shape(True, False, None, None, "`claude plugin update` failed: not installed",
                           tap_before="0.10.13", tap_after="0.10.13", command_failed=True),
    "list_unreadable": _shape(True, False, None, None, "could not confirm in `codex plugin list --json`",
                              list_unreadable=True),
    "no_advance": _shape(True, False, "0.167.0", "0.167.0", "`claude` returned success but did not advance",
                         tap_before="0.10.13", tap_after="0.10.13"),
}
PI_SHAPES = {
    "none": _pi(update_report.PiStep.NOT_INSTALLED),
    "current": _pi(update_report.PiStep.CURRENT),
    "locked": _pi(update_report.PiStep.LOCKED),
    "unreachable": _pi(update_report.PiStep.UNREACHABLE),
    "failed": PI_FAILED,
}


def _single(monkeypatch, plugin: str, pi: str, cli_ok: bool, agent: str = "claude_code") -> dict:
    _cli(monkeypatch, ok=cli_ok)
    _plugins(monkeypatch, {agent: PLUGIN_SHAPES[plugin]()})
    monkeypatch.setattr(upgrading, "_update_pi_package", lambda: PI_SHAPES[pi])
    held: list[dict] = []
    monkeypatch.setattr(update_report, "_send", lambda report, base_url: held.append(report))
    _pass(monkeypatch, agent)
    [report] = held
    return report


@pytest.mark.parametrize("cli_ok", [True, False])
@pytest.mark.parametrize("pi", sorted(PI_SHAPES))
@pytest.mark.parametrize("plugin", sorted(PLUGIN_SHAPES))
def test_every_failed_pass_names_its_failure(monkeypatch, plugin, pi, cli_ok):
    _assert_names_its_failure(_single(monkeypatch, plugin, pi, cli_ok))


def test_every_failed_pi_pass_names_its_failure(monkeypatch):
    for pi, cli_ok in itertools.product(sorted(PI_SHAPES), (True, False)):
        _cli(monkeypatch, ok=cli_ok)
        monkeypatch.setattr(upgrading, "_update_pi_package", lambda pi=pi: PI_SHAPES[pi])
        held: list[dict] = []
        monkeypatch.setattr(update_report, "_send", lambda report, base_url: held.append(report))
        _pass(monkeypatch, "pi")
        [report] = held
        _assert_names_its_failure(report)


def test_every_failed_merged_run_names_its_failure(monkeypatch):
    """Every pair of passes, Claude Code then Codex, merged as the wizard's
    Update merges them."""
    passes = {
        (agent, plugin, pi): _single(monkeypatch, plugin, pi, True, agent)
        for agent in ("claude_code", "codex")
        for plugin in PLUGIN_SHAPES
        for pi in ("none", "failed")
    }
    claude = [report for (agent, *_), report in passes.items() if agent == "claude_code"]
    codex = [report for (agent, *_), report in passes.items() if agent == "codex"]
    for first, second in itertools.product(claude, codex):
        _assert_names_its_failure(update_report.merge_passes([first, second]))
        _assert_names_its_failure(update_report.merge_passes([second, first]))
