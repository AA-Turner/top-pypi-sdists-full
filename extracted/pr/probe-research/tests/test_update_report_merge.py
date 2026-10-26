"""One update RUN, one report: the wizard's per-agent passes are merged.

`probe wizard --action update` runs `perform_update` once per coding agent on
the machine, and the server keeps one row per machine. Sent pass by pass, the
LAST agent overwrote the rest: live on the devbox (CLI 0.224.1) Kimi Code ran
last with no Probe plugins, so the row read plugin `not_installed` and tap NULL
while Claude Code's tap was current and Codex had just verified its own. On a
customer machine that hides exactly the failure the report exists to show.

Nothing here reaches a real agent CLI or server: the plugin steps are faked,
and `update_report._deliver` records what would have been sent.
"""

from __future__ import annotations

import importlib
import time

import pytest

from probe.cli import autoupdate, update_report, updater, upgrading
from probe.cli.capabilities import Capabilities

MANIFEST = {
    "cli": {"latest": "0.224.1"},
    "plugin": {"latest": "0.120.0"},
    "tap": {"latest": "0.9.14"},
}
Result = update_report.Result


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


@pytest.fixture
def sent(monkeypatch):
    bodies: list[dict] = []

    def _accept(base_url, headers, body, timeout):
        bodies.append(body)
        return 202

    monkeypatch.setattr(update_report, "_deliver", _accept)
    return bodies


def _plugin(tap_before, tap_after, *, before="0.120.0", after="0.120.0", tap_detail="",
            confirmed=True, **extra):
    return updater.PluginResult(
        True, confirmed, False, before, after, "plugin already at the latest (0.120.0)",
        tap_before=tap_before, tap_after=tap_after, tap_detail=tap_detail, **extra,
    )


#: Kimi Code with no Probe plugins installed: what `update_kimi_plugins` says.
KIMI_NOTHING = updater.PluginResult(
    False, False, False, None, None, "no Probe plugins installed in Kimi Code"
)


def _stub_updater(monkeypatch, by_agent: dict[str, updater.PluginResult]):
    """The CLI is already current; each agent's plugin step answers from
    `by_agent`, keyed on the agent the step is for: each `update_*` is one
    agent's, and several agents' passes run at once (`perform_updates`)."""

    monkeypatch.setattr(upgrading.updater, "fetch_latest", lambda base: MANIFEST)
    monkeypatch.setattr(
        upgrading.updater, "detect_install", lambda: updater.Install(updater.Method.UV_TOOL)
    )
    monkeypatch.setattr(
        upgrading.updater,
        "upgrade_cli",
        lambda install, current, target: updater.CliResult(
            True, True, False, current, "0.224.1", "CLI already at the latest (0.224.1)"
        ),
    )
    monkeypatch.setattr(upgrading.updater, "update_plugin", lambda *args: by_agent["claude_code"])
    monkeypatch.setattr(upgrading.updater, "update_codex_plugins", lambda *args: by_agent["codex"])
    monkeypatch.setattr(upgrading.updater, "update_kimi_plugins", lambda *args: by_agent["kimi_code"])


def _pass(monkeypatch, agent: str):
    monkeypatch.setenv("PROBE_AGENT", agent)
    return upgrading.perform_update(
        base_url="https://api.test", include_plugin=True, trigger=update_report.Trigger.SESSION_START
    )


# ---------------------------------------------------------------------------
# The priority
# ---------------------------------------------------------------------------


def test_the_priority_ranks_every_result_exactly_once():
    assert sorted(update_report.RESULT_PRIORITY) == sorted(Result)
    assert len(set(update_report.RESULT_PRIORITY)) == len(Result)


def test_not_installed_loses_to_everything_and_a_failure_beats_a_success():
    order = update_report.RESULT_PRIORITY
    assert order[-1] is Result.NOT_INSTALLED
    assert order.index(Result.BEHIND) < order.index(Result.CURRENT)
    assert order.index(Result.ERROR) < order.index(Result.UPDATED)


# ---------------------------------------------------------------------------
# A run of real passes, merged
# ---------------------------------------------------------------------------


def test_kimi_with_no_plugins_no_longer_hides_a_current_tap(monkeypatch, sent):
    """The devbox case: Claude Code's tap current, Kimi Code last with nothing."""
    _stub_updater(monkeypatch, {
        "claude_code": _plugin("0.9.14", "0.9.14"),
        "kimi_code": KIMI_NOTHING,
    })

    with update_report.merged_run():
        _pass(monkeypatch, "claude_code")
        _pass(monkeypatch, "kimi_code")

    [report] = sent
    assert report["tap"]["result"] == Result.CURRENT
    assert report["tap"]["after"] == "0.9.14"
    assert report["tap"]["harness"] == "claude_code"
    assert report["plugin"]["result"] == Result.CURRENT
    assert report["plugin"]["harness"] == "claude_code"
    assert report["outcome"] == "ok"


def test_a_codex_tap_left_behind_is_reported_from_codex(monkeypatch, sent):
    _stub_updater(monkeypatch, {
        "claude_code": _plugin("0.9.14", "0.9.14"),
        "codex": _plugin("0.9.11", "0.9.11", tap_detail=updater.CODEX_TAP_NOOP,
                         before="probe-research=0.120.0", after="probe-research=0.120.0"),
    })

    with update_report.merged_run():
        _pass(monkeypatch, "claude_code")
        _pass(monkeypatch, "codex")

    [report] = sent
    assert report["tap"] == {
        "before": "0.9.11",
        "after": "0.9.11",
        "target": "0.9.14",
        "result": Result.BEHIND,
        "detail": updater.CODEX_TAP_NOOP,
        "harness": "codex",
    }
    assert report["outcome"] == "failed"  # the codex pass failed on its tap


def test_outside_a_run_each_pass_still_reports_on_its_own(monkeypatch, sent):
    """A single update (the detached auto-update, `probe update`) is one pass,
    sent at once, exactly as before."""
    _stub_updater(monkeypatch, {"claude_code": _plugin("0.9.14", "0.9.14")})
    _pass(monkeypatch, "claude_code")
    assert len(sent) == 1


def test_a_failed_merge_costs_the_report_never_the_run(monkeypatch, sent):
    _stub_updater(monkeypatch, {"claude_code": _plugin("0.9.14", "0.9.14")})

    def _boom(reports):
        raise RuntimeError("merge bug")

    monkeypatch.setattr(update_report, "merge_passes", _boom)
    with update_report.merged_run():
        outcome = _pass(monkeypatch, "claude_code")
    assert outcome.ok and sent == []


def test_a_run_a_stop_signal_ends_fails_and_names_the_stop(monkeypatch, sent):
    """SIGTERM or SIGHUP ends the run wherever it is (`probe.core.events._stop`
    raises SystemExit(128 + the signal)); the Probe service sends SIGTERM to an
    update past its time limit. The report and the local record say the run
    was stopped, beside the pass it finished: they used to send only what the
    finished passes said, which here was a success."""
    import signal

    _stub_updater(monkeypatch, {"claude_code": _plugin("0.9.14", "0.9.14")})
    with pytest.raises(SystemExit), update_report.merged_run():
        _pass(monkeypatch, "claude_code")
        raise SystemExit(128 + signal.SIGTERM)

    [report] = sent
    assert report["outcome"] == "failed"
    assert report["cli"]["result"] == Result.ERROR
    assert report["cli"]["detail"].startswith("stopped by SIGTERM after ")
    assert report["cli"]["detail"].endswith(", before the update finished")
    assert report["tap"]["result"] == Result.CURRENT and report["tap"]["harness"] == "claude_code"
    attempt = autoupdate.load().last_attempt
    assert attempt.ok is False and attempt.detail == report["cli"]["detail"]


def test_a_run_stopped_in_its_first_pass_still_reports(sent):
    import signal

    with pytest.raises(SystemExit), update_report.merged_run():
        raise SystemExit(128 + signal.SIGHUP)
    [report] = sent
    assert report["outcome"] == "failed" and report["cli"]["detail"].startswith("stopped by SIGHUP after ")


@pytest.mark.parametrize("code", [0, 1, 75, None])
def test_an_ordinary_exit_is_no_stop(monkeypatch, sent, code):
    _stub_updater(monkeypatch, {"claude_code": _plugin("0.9.14", "0.9.14")})
    with pytest.raises(SystemExit), update_report.merged_run():
        _pass(monkeypatch, "claude_code")
        raise SystemExit(code)
    [report] = sent
    assert report["outcome"] == "ok" and report["cli"]["result"] == Result.CURRENT


def test_nested_runs_send_once():
    passes = []
    with update_report.merged_run():
        with update_report.merged_run():
            update_report.submit_attempt({"schema_version": 1, "outcome": "ok"})
        passes.append(list(update_report._run_passes))
    assert len(passes[0]) == 1
    assert update_report._run_passes is None


# ---------------------------------------------------------------------------
# merge_passes, field by field
# ---------------------------------------------------------------------------


def _report(harness, *, outcome="ok", at=100, tap=None, plugin=None, legacy=()):
    return update_report.attempt_report(
        trigger=update_report.Trigger.CLI, ok=outcome == "ok", at=at, source=harness,
        cli=update_report._component("0.224.1", "0.224.1", "0.224.1", Result.CURRENT),
        plugin=plugin, tap=tap, legacy_ids=legacy,
    )


def test_merge_keeps_the_chosen_passs_fields_together():
    current = update_report._component("0.9.14", "0.9.14", "0.9.14", Result.CURRENT)
    missing = update_report._component(
        "0.9.3", "0.9.3", "0.9.14", Result.NOT_FOUND_ON_PATH, "`codex` not found on PATH"
    )
    merged = update_report.merge_passes([
        _report("claude_code", tap=current, at=200, legacy=("prbe-cc-tap-plugin",)),
        _report("codex", tap=missing, outcome="failed", at=150,
                legacy=("prbe-codex-tap-plugin", "prbe-cc-tap-plugin")),
        _report("pi", tap=None, at=300),
    ])
    assert merged["tap"] == {**missing, "harness": "codex"}
    assert merged["outcome"] == "failed"
    assert merged["attempted_at"] == 150
    assert merged["harness"] == "claude_code"  # the run's first pass
    assert merged["legacy_plugin_ids"] == ["prbe-cc-tap-plugin", "prbe-codex-tap-plugin"]


def test_a_tie_keeps_the_earlier_pass():
    a = update_report._component("0.9.14", "0.9.14", "0.9.14", Result.CURRENT)
    merged = update_report.merge_passes([_report("claude_code", tap=a), _report("codex", tap=a)])
    assert merged["tap"]["harness"] == "claude_code"


def test_a_component_no_pass_had_stays_absent():
    merged = update_report.merge_passes([_report("pi"), _report("pi")])
    assert merged["tap"] is None


# ---------------------------------------------------------------------------
# The wizard itself: one report for `probe wizard --action update --yes`
# ---------------------------------------------------------------------------


def test_the_wizard_update_sends_one_merged_report(monkeypatch, sent):
    """End to end through the wizard's per-agent loop. On main before this fix
    the loop sent one report per agent and the server kept the last: Kimi
    Code's "not installed"."""
    from probe.cli import capabilities, doctor, setup

    cli_main = importlib.import_module("probe.cli.main")
    _stub_updater(monkeypatch, {
        "claude_code": _plugin("0.9.14", "0.9.14"),
        "kimi_code": KIMI_NOTHING,
    })
    monkeypatch.setattr(setup, "detectable_sources", lambda: ("claude_code", "kimi_code"))

    def _offline(*args, **kwargs):
        raise OSError("no server in this test")

    monkeypatch.setattr(capabilities, "device_state_request", _offline)
    monkeypatch.setattr(doctor, "collect", lambda: Capabilities())
    monkeypatch.setattr(cli_main, "_register_local_capabilities", lambda *a, **k: [])

    assert cli_main.main(["wizard", "--yes", "--action", "update"]) == 0

    [report] = sent
    assert report["tap"]["result"] == Result.CURRENT
    assert report["tap"]["harness"] == "claude_code"
    assert report["plugin"]["harness"] == "claude_code"
    assert report["attempted_at"] <= int(time.time())


def test_the_wizard_update_registers_the_machine_once(monkeypatch, sent):
    """The capabilities registration had the same flaw. Live on a customer
    machine (2026-10-13 00:17 UTC) one auto-update registered capture `absent`
    from the agent without it, then `installed` 7 s later from the one with it,
    and the `absent` posted a false "Probe removed from a machine". On main
    before this fix the loop below registered twice: absent, then installed."""
    import os

    from probe.cli import capabilities, client_installation, doctor, setup
    from probe.cli.capabilities import TokenSource

    cli_main = importlib.import_module("probe.cli.main")
    _stub_updater(monkeypatch, {
        "claude_code": _plugin("0.9.14", "0.9.14"),
        "codex": _plugin("0.9.14", "0.9.14"),
    })
    # Codex first, so the agent WITHOUT capture runs first -- as it did live.
    monkeypatch.setattr(setup, "detectable_sources", lambda: ("codex", "claude_code"))

    def _offline(*args, **kwargs):
        raise OSError("no server in this test")

    def _collect():
        capturing = os.environ.get("PROBE_AGENT") == "claude_code"
        return Capabilities(
            agent_source=os.environ.get("PROBE_AGENT"),
            tracking_plugin_installed=True,
            capture_plugin_installed=capturing,
            capture_token_sources=(TokenSource.PAIRED_FILE,) if capturing else (),
            auto_update_enabled=True,
        )

    registered: list[dict] = []

    class _Client:
        def __init__(self, **kwargs):
            pass

        def __enter__(self):
            return self

        def __exit__(self, *exc):
            return None

        def register_client_capabilities(self, **body):
            registered.append(body)
            return {"installation_id": "install-1"}

        def name_client_installation(self, **kwargs):
            return {}

    monkeypatch.setattr(capabilities, "device_state_request", _offline)
    monkeypatch.setattr(doctor, "collect", _collect)
    monkeypatch.setattr(client_installation, "Client", _Client)

    assert cli_main.main(["wizard", "--yes", "--action", "update"]) == 0

    assert [(body["tracking"], body["capture"]) for body in registered] == [
        ("installed", "installed")
    ]


# ---------------------------------------------------------------------------
# The local record (`autoupdate.json`, `probe doctor`) merges the same passes.
# It had the flaw the server report had: each pass overwrote `last_attempt`.
# In a sandboxed Update on 2026-10-07 the Claude Code pass could not update its
# plugin, and pi, last with nothing to update, recorded success over it.
# ---------------------------------------------------------------------------

CLAUDE_PLUGIN_FAILED = updater.PluginResult(
    True, False, False, "0.112.3", "0.112.3",
    "`claude plugin update probe-research@research-os-agent` did not complete: "
    '✘ Failed to update plugin "probe-research@research-os-agent": '
    'Plugin "probe-research" is not installed',
    tap_before="0.9.3", tap_after="0.9.14", command_failed=True,
)


def test_the_wizard_update_records_one_merged_attempt_locally(monkeypatch, sent):
    from probe.cli import capabilities, doctor, setup

    cli_main = importlib.import_module("probe.cli.main")
    _stub_updater(monkeypatch, {"claude_code": CLAUDE_PLUGIN_FAILED, "kimi_code": KIMI_NOTHING})
    monkeypatch.setattr(setup, "detectable_sources", lambda: ("claude_code", "kimi_code"))

    def _offline(*args, **kwargs):
        raise OSError("no server in this test")

    monkeypatch.setattr(capabilities, "device_state_request", _offline)
    monkeypatch.setattr(doctor, "collect", lambda: Capabilities())
    monkeypatch.setattr(cli_main, "_register_local_capabilities", lambda *a, **k: [])

    cli_main.main(["wizard", "--yes", "--action", "update"])

    attempt = autoupdate.load().last_attempt
    assert attempt.plugin_ok is False, "Kimi Code, last with nothing to update, hid the failure"
    assert attempt.plugin_detail.startswith("Claude Code: `claude plugin update")
    assert attempt.plugin_version == "0.112.3"
    assert attempt.ok is True
    assert "FAILED" in attempt.describe()


def _attempt(**fields):
    base = dict(at=100, ok=True, from_version="0.224.1", to_version="0.225.0")
    return autoupdate.Attempt(**{**base, **fields})


def test_a_failed_plugin_pass_beats_a_later_pass_with_nothing_to_do():
    merged = autoupdate.merge_attempts([
        ("Claude Code", _attempt(plugin_ok=False, plugin_detail="refresh failed", plugin_version="0.120.0")),
        ("Codex", _attempt(at=90, plugin_version="probe-research=0.124.0")),
        ("Kimi Code", _attempt(at=110)),
    ])
    assert merged.plugin_ok is False
    assert merged.plugin_detail == "Claude Code: refresh failed"
    assert merged.plugin_version == "0.120.0"
    assert merged.at == 90, "dated by its first pass"


def test_every_failing_agent_is_named():
    merged = autoupdate.merge_attempts([
        ("Claude Code", _attempt(plugin_ok=False, plugin_detail="a")),
        ("Codex", _attempt(plugin_ok=False, plugin_detail="b")),
    ])
    assert merged.plugin_detail == "Claude Code: a; Codex: b"


def test_a_failed_cli_half_wins_over_a_later_success():
    merged = autoupdate.merge_attempts([
        ("Claude Code", _attempt(ok=False, detail="`uv` not found on PATH", to_version=None)),
        ("Codex", _attempt()),
    ])
    assert (merged.ok, merged.detail, merged.to_version) == (False, "`uv` not found on PATH", None)


def test_notes_from_a_successful_run_are_kept_with_their_agent():
    merged = autoupdate.merge_attempts([
        ("Claude Code", _attempt(
            plugin_detail="1 session started before the update still runs tap 0.9.3",
            plugin_version="0.124.0",
        )),
        # Nothing installed is not news in a success.
        ("Kimi Code", _attempt(plugin_detail="no Probe plugins installed in Kimi Code")),
    ])
    assert merged.plugin_ok is True
    assert merged.plugin_detail == "Claude Code: 1 session started before the update still runs tap 0.9.3"


def test_one_pass_is_recorded_as_it_was():
    only = _attempt(plugin_ok=False, plugin_detail="x")
    assert autoupdate.merge_attempts([("Claude Code", only)]) is only


def test_outside_a_run_each_attempt_is_written_at_once():
    autoupdate.record_attempt(_attempt(plugin_detail="first"), agent="Claude Code")
    assert autoupdate.load().last_attempt.plugin_detail == "first"


def test_a_merged_run_writes_once_at_its_end():
    with update_report.merged_run():
        autoupdate.record_attempt(_attempt(plugin_ok=False, plugin_detail="x"), agent="Codex")
        autoupdate.record_attempt(_attempt(), agent="pi")
        assert autoupdate.load().last_attempt is None, "nothing written mid-run"
    attempt = autoupdate.load().last_attempt
    assert (attempt.plugin_ok, attempt.plugin_detail) == (False, "Codex: x")
