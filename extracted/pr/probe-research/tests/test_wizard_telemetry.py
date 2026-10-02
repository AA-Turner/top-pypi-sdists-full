"""Wizard + backfill funnel emission: the wiring, at the convergence points.

Every emission asserted here executes on the SAME code path a flag-driven run
uses — deliberately. The wizard's interactive menu cannot run under pytest,
so any telemetry line placed inside menu code would ship permanently
untested; the plan pinned emissions to interactive/non-interactive
convergence points precisely so these tests exercise the real lines.
"""

from __future__ import annotations

import dataclasses
import importlib
from contextlib import nullcontext
from types import SimpleNamespace

import pytest

from probe.cli import backfill as bf
from probe.cli import backfill_run
from probe.cli import bootstrap
from probe.cli import doctor as doctor_mod
from probe.cli import plugin_cli, setup, tui
from probe.cli import telemetry as tm
from probe.cli.capabilities import Capabilities

# `probe.cli.main` the MODULE is shadowed by the re-exported `main` function on
# the package (probe/cli/__init__.py) — import it by path, like test_atif does.
main_mod = importlib.import_module("probe.cli.main")


@pytest.fixture(autouse=True)
def isolate(tmp_path, monkeypatch):
    monkeypatch.setenv("PROBE_CONFIG_PATH", str(tmp_path / "probe" / "config.json"))
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    monkeypatch.delenv("PROBE_AGENT", raising=False)
    (tmp_path / "probe").mkdir(parents=True, exist_ok=True)
    return tmp_path


@pytest.fixture()
def captured(monkeypatch):
    """Telemetry ON, records captured at the queue seam — no thread, no network."""
    monkeypatch.setenv("PROBE_TELEMETRY", "on")
    records: list[dict] = []
    monkeypatch.setattr(tm, "_sender", None)
    monkeypatch.setattr(tm, "_flush_registered", True)
    monkeypatch.setattr(tm._Sender, "start", lambda self: None)
    monkeypatch.setattr(tm._Sender, "put", lambda self, rec: records.append(rec))
    return records


def _events(records: list[dict]) -> list[str]:
    return [r["event"] for r in records]


def _props(records: list[dict], event: str) -> dict:
    return next(r["properties"] for r in records if r["event"] == event)


# --- wizard command ---------------------------------------------------------


@pytest.fixture()
def wizard_stubs(monkeypatch):
    """The minimum reality a flag-driven wizard run touches."""
    monkeypatch.setattr(
        bootstrap, "ensure_persistent_install", lambda: SimpleNamespace(message=None)
    )
    monkeypatch.setattr(plugin_cli, "available", lambda source: source == "claude_code")

    collects: list[Capabilities] = []

    def fake_collect():
        return collects.pop(0) if len(collects) > 1 else collects[0]

    monkeypatch.setattr(doctor_mod, "collect", fake_collect)
    return collects


def test_flag_driven_wizard_emits_the_entry_funnel(captured, wizard_stubs):
    wizard_stubs.append(Capabilities())  # fresh machine: nothing installed
    rc = main_mod.main(["wizard", "--action", "diagnose", "--agent", "claude"])
    assert rc == 0
    assert _events(captured) == [
        tm.EVENT_WIZARD_INVOKED,
        tm.EVENT_WIZARD_STARTED,
        tm.EVENT_WIZARD_ACTION_CHOSEN,
    ]
    invoked = _props(captured, tm.EVENT_WIZARD_INVOKED)
    assert invoked["invoked_action"] == "diagnose"
    assert invoked["invoked_by"] == "automation"  # non-tty == robot, by definition
    started = _props(captured, tm.EVENT_WIZARD_STARTED)
    assert started["fresh_install"] is True
    chosen = _props(captured, tm.EVENT_WIZARD_ACTION_CHOSEN)
    assert chosen["action"] == "diagnose" and chosen["via_flag"] is True
    # one shared session id across the whole funnel
    assert len({r["properties"]["session_id"] for r in captured}) == 1


def test_agent_typo_is_a_usage_error_not_infrastructure_death(captured, monkeypatch):
    """--agent bogus raises BEFORE wizard.invoked: a typo must not land in the
    funnel's 'bootstrap died' bucket."""
    import typer

    with pytest.raises(typer.BadParameter):
        main_mod.app(
            args=["wizard", "--action", "diagnose", "--agent", "bogus"],
            prog_name="probe",
            standalone_mode=False,
        )
    assert captured == []


def test_action_flag_is_clamped_never_verbatim(captured, monkeypatch):
    """A mis-pasted --action value (path, secret) must never ride to the
    vendor: unknown values are clamped to the literal 'invalid'."""
    monkeypatch.setattr(
        bootstrap, "ensure_persistent_install", lambda: SimpleNamespace(message=None)
    )
    rc = main_mod.main(["wizard", "--action", "hunter2-oops-a-secret", "--agent", "claude"])
    assert rc == 2  # still the usage error it always was
    invoked = _props(captured, tm.EVENT_WIZARD_INVOKED)
    assert invoked["invoked_action"] == "invalid"


def test_invoked_fires_before_a_dying_bootstrap(captured, monkeypatch):
    """The D7 point: a broken npx→persistent install still enters the funnel."""

    def broken():
        raise RuntimeError("bootstrap died")

    monkeypatch.setattr(bootstrap, "ensure_persistent_install", broken)
    with pytest.raises(RuntimeError):
        main_mod.main(["wizard", "--action", "diagnose", "--agent", "claude"])
    # `invoked` FIRST is the D7 point -- entering the funnel must not depend on
    # the install surviving. The `$exception` behind it is crash reporting doing
    # its job: a RuntimeError out of bootstrap is a bug, and the assertion is on
    # the ordering rather than on the list being exactly one long.
    assert _events(captured)[0] == tm.EVENT_WIZARD_INVOKED
    assert _events(captured) == [tm.EVENT_WIZARD_INVOKED, "$exception"]


def test_killswitch_means_zero_records_and_no_sender(monkeypatch, wizard_stubs):
    monkeypatch.setenv("PROBE_TELEMETRY", "off")
    started: list[bool] = []
    monkeypatch.setattr(tm._Sender, "start", lambda self: started.append(True))
    puts: list[dict] = []
    monkeypatch.setattr(tm._Sender, "put", lambda self, rec: puts.append(rec))
    wizard_stubs.append(Capabilities())
    assert main_mod.main(["wizard", "--action", "diagnose", "--agent", "claude"]) == 0
    assert puts == [] and started == []


def test_menu_loop_emits_one_started_and_per_iteration_action_chosen(
    captured, wizard_stubs, monkeypatch
):
    """Drive the interactive menu loop with a scripted menu — the one wizard
    behavior (re-collect + re-choose) the flag paths never reach."""
    wizard_stubs.append(Capabilities())
    monkeypatch.setattr(setup, "interactive", lambda: True)
    def signed_in(**kwargs):
        from probe.sdk.config import save_context

        save_context({"token": "probe_pat_menu_test"})
        return setup.SignInResult(ok=True, lines=[])

    monkeypatch.setattr(setup, "sign_in", signed_in)
    monkeypatch.setattr(tui, "clear", lambda: None)
    monkeypatch.setattr(tui, "page", lambda lines, prompt=None, **kwargs: "")
    actions = iter(["diagnose", "diagnose", None])
    from probe.cli import actions as actions_mod

    def scripted_menu(_caps):
        nxt = next(actions)
        return actions_mod.Action(nxt) if nxt else None

    monkeypatch.setattr(setup, "run_action_menu", scripted_menu)
    monkeypatch.setattr(setup, "run_agent_menu", lambda defaults, action=None: ("claude_code",))
    with pytest.raises(SystemExit) as excinfo:
        main_mod.app(args=["wizard"], prog_name="probe", standalone_mode=True)
    assert excinfo.value.code == 0
    events = _events(captured)
    assert events.count(tm.EVENT_WIZARD_STARTED) == 1
    assert events.count(tm.EVENT_WIZARD_ACTION_CHOSEN) == 2  # one per menu pass
    assert _props(captured, tm.EVENT_WIZARD_ACTION_CHOSEN)["via_flag"] is False


def test_a_default_switched_on_the_menu_row_is_saved_by_the_loop(
    captured, wizard_stubs, monkeypatch
):
    """The menu answers `DefaultChoice` when its Defaults row was switched in
    place; the loop must run the Defaults action WITH that state -- saved, no
    picker -- and count it as the `defaults` action like any other pass."""
    from probe.sdk import session_marker

    wizard_stubs.append(Capabilities())
    monkeypatch.setattr(setup, "interactive", lambda: True)
    monkeypatch.delenv("PROBE_SESSION_STATE", raising=False)
    monkeypatch.delenv("PROBE_SESSION_TRACKING", raising=False)

    def signed_in(**kwargs):
        from probe.sdk.config import save_context

        save_context({"token": "probe_pat_menu_test"})
        return setup.SignInResult(ok=True, lines=[])

    monkeypatch.setattr(setup, "sign_in", signed_in)
    monkeypatch.setattr(tui, "clear", lambda: None)
    monkeypatch.setattr(tui, "page", lambda lines, prompt=None, **kwargs: "")
    monkeypatch.setattr(setup, "run_defaults_menu", lambda *a, **k: pytest.fail("picker drawn"))
    answers = iter([setup.DefaultChoice("off"), None])
    monkeypatch.setattr(setup, "run_action_menu", lambda _caps: next(answers))
    with pytest.raises(SystemExit) as excinfo:
        main_mod.app(args=["wizard"], prog_name="probe", standalone_mode=True)
    assert excinfo.value.code == 0
    assert session_marker.default_session_state() == session_marker.STATE_OFF
    assert _props(captured, tm.EVENT_WIZARD_ACTION_CHOSEN)["action"] == "defaults"


# --- configure path ---------------------------------------------------------


@pytest.fixture()
def registrations() -> list[bool]:
    """`complete=` as the wizard passed it to the capability registration, in
    call order. False means it told the server the run did not finish."""
    return []


@pytest.fixture()
def configure_stubs(monkeypatch, wizard_stubs, registrations):
    monkeypatch.setattr(setup, "needs_authorization", lambda caps, selection: [])
    monkeypatch.setattr(setup, "apply_tracking", lambda on, on_retry=None: ["installed"])
    monkeypatch.setattr(setup, "refresh_marketplace", lambda: None)
    # Records `complete` so the failure-branch tests can assert the wizard tells
    # the server the run did NOT finish -- the signal the dashboard reads to
    # decide an install completed.
    monkeypatch.setattr(
        main_mod,
        "_register_local_capabilities",
        lambda caps, settings=None, complete=True: (registrations.append(complete), [])[1],
    )
    return wizard_stubs


def _configure_argv() -> list[str]:
    return [
        "wizard",
        "--action",
        "configure",
        "--yes",
        "--agent",
        "claude",
        "--tracking",
        "--no-capture",
        "--no-auto-update",
        "--no-agent-rules",
    ]


def test_configure_success_reports_newly_installed(captured, configure_stubs):
    fresh = Capabilities()
    after = dataclasses.replace(fresh, tracking_plugin_installed=True)
    configure_stubs.extend([fresh, after])  # menu snapshot, then the post-configure re-read
    assert main_mod.main(_configure_argv()) == 0
    assert _events(captured) == [
        tm.EVENT_WIZARD_INVOKED,
        tm.EVENT_WIZARD_STARTED,
        tm.EVENT_WIZARD_ACTION_CHOSEN,
        tm.EVENT_WIZARD_CONFIGURE_STARTED,
        tm.EVENT_WIZARD_CONFIGURE_COMPLETED,
        # Per-agent verdict, then the installation's. A one-agent run makes
        # them look redundant; a two-agent run is why they are not.
        tm.EVENT_WIZARD_INSTALL_SETTLED,
    ]
    settled = _props(captured, tm.EVENT_WIZARD_INSTALL_SETTLED)
    assert settled["outcome"] == "settled" and settled["agent_count"] == 1
    assert settled["guided"] is False
    started = _props(captured, tm.EVENT_WIZARD_CONFIGURE_STARTED)
    assert started["tracking"] is True and started["capture"] is False
    assert started["plan_steps"] >= 1 and started["needs_authorization"] is False
    done = _props(captured, tm.EVENT_WIZARD_CONFIGURE_COMPLETED)
    assert done["outcome"] == "success"
    assert done["tracking_newly_installed"] is True
    assert done["tracking_already_present"] is False
    assert "duration_seconds" in done


def test_configure_failure_names_the_kind(captured, configure_stubs, registrations):
    fresh = Capabilities()
    configure_stubs.extend([fresh, fresh, fresh])  # after-collect: still absent
    assert main_mod.main(_configure_argv()) == 1
    # The dashboard reads this registration as the install completing, so a
    # run that ended here must report itself unfinished.
    assert registrations == [False]
    done = _props(captured, tm.EVENT_WIZARD_CONFIGURE_COMPLETED)
    assert done["outcome"] == "failed"
    assert done["failure_kind"] == "plugins_absent"


def test_configure_noop_still_completes_the_funnel(captured, configure_stubs, monkeypatch):
    monkeypatch.setattr(setup, "plan", lambda caps, selection: [])
    installed = Capabilities(tracking_plugin_installed=True)
    configure_stubs.append(installed)
    assert main_mod.main(_configure_argv()) == 0
    done = _props(captured, tm.EVENT_WIZARD_CONFIGURE_COMPLETED)
    assert done["outcome"] == "success" and done["no_changes"] is True


def test_signed_in_success_reaches_the_funnel(captured, configure_stubs, monkeypatch):
    monkeypatch.setattr(setup, "needs_authorization", lambda caps, selection: ["tracking"])
    monkeypatch.setattr(setup, "authorize", lambda needs, **kw: ({"tracking": object()}, []))
    monkeypatch.setattr(setup, "blocked_by_missing_grants", lambda gate, *, needed, granted: [])
    fresh = Capabilities()
    after = dataclasses.replace(fresh, tracking_plugin_installed=True)
    configure_stubs.extend([fresh, after])  # menu snapshot, then the post-configure re-read
    assert main_mod.main(_configure_argv()) == 0
    signed = _props(captured, tm.EVENT_WIZARD_SIGNED_IN)
    assert signed["outcome"] == "success" and signed["grants_needed"] == 1
    assert _props(captured, tm.EVENT_WIZARD_CONFIGURE_COMPLETED)["outcome"] == "success"


def test_signed_in_failure_names_missing_grants(captured, configure_stubs, monkeypatch, registrations):
    monkeypatch.setattr(setup, "needs_authorization", lambda caps, selection: ["tracking"])
    monkeypatch.setattr(setup, "authorize", lambda needs, **kw: ({}, []))
    monkeypatch.setattr(
        setup,
        "blocked_by_missing_grants",
        lambda gate, *, needed, granted: ["tracking"],
    )
    fresh = Capabilities()
    configure_stubs.extend([fresh, fresh, fresh])
    assert main_mod.main(_configure_argv()) == 1
    # The dashboard reads this registration as the install completing, so a
    # run that ended here must report itself unfinished.
    assert registrations == [False]
    assert _props(captured, tm.EVENT_WIZARD_SIGNED_IN)["outcome"] == "failed"
    done = _props(captured, tm.EVENT_WIZARD_CONFIGURE_COMPLETED)
    assert done["outcome"] == "failed"
    assert done["failure_kind"] == "missing_grants"


def test_configure_unverifiable_when_plugins_cannot_be_asked(
    captured, configure_stubs, monkeypatch
):
    fresh = Capabilities()
    unanswerable = dataclasses.replace(fresh, plugins_verified=False)
    configure_stubs.extend([fresh, unanswerable])  # menu snapshot, then the post-configure re-read
    assert main_mod.main(_configure_argv()) == 0
    assert _props(captured, tm.EVENT_WIZARD_CONFIGURE_COMPLETED)["outcome"] == "unverifiable"


def test_configure_runtime_failure_kind(captured, configure_stubs, monkeypatch, registrations):
    monkeypatch.setattr(setup, "apply_capture", lambda caps, on, mode=None, on_retry=None: ["ok"])
    fresh = Capabilities()
    after = dataclasses.replace(
        fresh, capture_plugin_installed=True, capture_credential_valid=False
    )
    configure_stubs.extend([fresh, after])  # menu snapshot, then the post-configure re-read
    argv = [
        "wizard",
        "--action",
        "configure",
        "--yes",
        "--agent",
        "claude",
        "--no-tracking",
        "--capture",
        "--no-auto-update",
        "--no-agent-rules",
    ]
    assert main_mod.main(argv) == 1
    done = _props(captured, tm.EVENT_WIZARD_CONFIGURE_COMPLETED)
    assert done["outcome"] == "failed" and done["failure_kind"] == "runtime"


# --- backfill funnel --------------------------------------------------------


def _ctx() -> tm.TelemetryContext:
    return tm.TelemetryContext(session_id="sess", via="wizard", invoked_by="human")


@pytest.fixture
def folder_harness(tmp_path, monkeypatch):
    from test_backfill_scoped_orchestration import make_harness

    return make_harness(tmp_path, monkeypatch)


def _run_folder(h, **kwargs):
    return backfill_run.execute(
        client_factory=lambda: nullcontext(h.client), folder=h.folder,
        agent=bf.Agent.CLAUDE, interactive=kwargs.pop("interactive", False),
        yes=kwargs.pop("yes", True), concurrency=1, telemetry=_ctx(), **kwargs,
    )


def test_backfill_empty_folder_emits_summary(captured, folder_harness):
    h = folder_harness
    (h.folder / "a.py").unlink()
    lines = _run_folder(h)
    assert any("no files" in line for line in lines)
    assert _events(captured) == [tm.EVENT_BACKFILL_STARTED, tm.EVENT_BACKFILL_SCANNED, tm.EVENT_BACKFILL_SUMMARY]
    summary = _props(captured, tm.EVENT_BACKFILL_SUMMARY)
    assert summary["outcome"] == "empty_folder" and "duration_seconds" in summary
    assert _props(captured, tm.EVENT_BACKFILL_SCANNED)["files"] == 0
    assert not h.classified and not h.created


def test_backfill_credentials_failure_emits_summary(captured, folder_harness, monkeypatch):
    h = folder_harness
    monkeypatch.setattr(h.client, "me", lambda: (_ for _ in ()).throw(RuntimeError("expired")))
    lines = _run_folder(h)
    assert any("Could not reach Probe" in line for line in lines)
    assert _events(captured) == [tm.EVENT_BACKFILL_STARTED, tm.EVENT_BACKFILL_SUMMARY]
    assert _props(captured, tm.EVENT_BACKFILL_SUMMARY)["outcome"] == "credentials_failed"
    assert not h.classified and not h.created


def test_backfill_abort_emits_summary(captured, tmp_path, monkeypatch):
    def interrupted(**kwargs):
        raise KeyboardInterrupt

    monkeypatch.setattr(backfill_run, "_execute", interrupted)
    monkeypatch.setattr(bf, "stop_all", lambda: None)
    lines = backfill_run.execute(
        client_factory=nullcontext,
        folder=tmp_path,
        agent=bf.Agent("claude"),
        interactive=False,
        yes=True,
        telemetry=_ctx(),
    )
    assert any("Stopped" in line for line in lines)
    assert _props(captured, tm.EVENT_BACKFILL_SUMMARY)["outcome"] == "aborted"


def test_backfill_success_emits_the_full_funnel(captured, folder_harness, monkeypatch):
    h = folder_harness
    # Drain through the real SDK before the final coverage join, so success
    # proves a durable receipt rather than merely the enqueue acknowledgment.
    monkeypatch.setattr(h.client, "_wake_delivery", h.drain)
    lines = _run_folder(h)
    assert any("Every observed file has a receipt" in line for line in lines)
    assert _events(captured) == [
        tm.EVENT_BACKFILL_STARTED, tm.EVENT_BACKFILL_SCANNED, tm.EVENT_BACKFILL_PLAN_READY,
        tm.EVENT_BACKFILL_APPROVED, tm.EVENT_BACKFILL_SUMMARY,
    ]
    assert _props(captured, tm.EVENT_BACKFILL_SCANNED)["files"] == 1
    approved = _props(captured, tm.EVENT_BACKFILL_APPROVED)
    assert approved["revision_count"] == 0 and approved["units_total"] == 1
    summary = _props(captured, tm.EVENT_BACKFILL_SUMMARY)
    assert summary["outcome"] == "success"
    assert summary["units_done"] == 1 and summary["coverage_pct"] == 100.0
    assert h.report()["delivered"] == ["a.py"] and len(h.remote.calls) == 1


def test_backfill_no_plan_emits_summary(captured, folder_harness, monkeypatch):
    monkeypatch.setattr(backfill_run, "classify", lambda *args, **kwargs: (None, "agent died", None))
    lines = _run_folder(folder_harness)
    assert any("usable plan" in line for line in lines)
    assert _props(captured, tm.EVENT_BACKFILL_SUMMARY)["outcome"] == "no_plan"
    assert not folder_harness.created


def test_backfill_untrusted_classification_emits_summary(captured, folder_harness, monkeypatch):
    from probe.cli.backfill_plan import Assignment, Plan, ProjectSpec

    plan = Plan([ProjectSpec("project")], [Assignment("ghost.py", "project")])
    monkeypatch.setattr(backfill_run, "classify", lambda *args, **kwargs: (plan, "", None))
    _run_folder(folder_harness)
    assert _props(captured, tm.EVENT_BACKFILL_PLAN_READY)["trustworthy"] is False
    assert _props(captured, tm.EVENT_BACKFILL_SUMMARY)["outcome"] == "untrusted_classification"
    assert not folder_harness.created


def test_backfill_project_create_failure_emits_summary(captured, folder_harness, monkeypatch):
    h = folder_harness
    monkeypatch.setattr(h.client, "create_project", lambda *args, **kwargs: (_ for _ in ()).throw(RuntimeError("refused")))
    lines = _run_folder(h)
    assert any("Could not create every project" in line for line in lines)
    summary = _props(captured, tm.EVENT_BACKFILL_SUMMARY)
    assert summary["outcome"] == "project_create_failed" and summary["projects_failed"] == 1
    assert tm.EVENT_BACKFILL_APPROVED in _events(captured)
    with h.coverage().writer() as coverage:
        assert coverage.meta("approved_request")["assigned"] == {"a.py": "project"}
    assert not h.manifested


def test_backfill_already_imported_emits_summary_and_resumed_flag(captured, folder_harness, monkeypatch):
    h = folder_harness
    monkeypatch.setattr(h.client, "_wake_delivery", h.drain)
    _run_folder(h)
    assert h.report()["delivered"] == ["a.py"]
    captured.clear()
    lines = _run_folder(h)
    assert any("already imported" in line for line in lines)
    assert _props(captured, tm.EVENT_BACKFILL_STARTED)["resumed"] is True
    assert _props(captured, tm.EVENT_BACKFILL_SUMMARY)["outcome"] == "already_imported"
    assert len(h.classified) == len(h.manifested) == len(h.remote.calls) == 1


def test_backfill_failed_units_report_partial_not_success(captured, folder_harness):
    h = folder_harness
    h.failed_model = True
    _run_folder(h)
    summary = _props(captured, tm.EVENT_BACKFILL_SUMMARY)
    assert summary["outcome"] == "partial" and summary["failed_units"] == 1
    assert summary["coverage_pct"] == 0.0 and h.report()["unresolved"] == ["a.py"]


def test_backfill_crash_emits_error_summary_and_reraises(captured, tmp_path, monkeypatch):
    """R3: a crash is countable and separable from abandonment — and still a crash."""

    def crash(**kwargs):
        raise RuntimeError("ledger exploded")

    monkeypatch.setattr(backfill_run, "_execute", crash)
    monkeypatch.setattr(bf, "stop_all", lambda: None)
    with pytest.raises(RuntimeError):
        backfill_run.execute(
            client_factory=nullcontext,
            folder=tmp_path,
            agent=bf.Agent("claude"),
            interactive=False,
            yes=True,
            telemetry=_ctx(),
        )
    summary = _props(captured, tm.EVENT_BACKFILL_SUMMARY)
    assert summary["outcome"] == "error"
    assert "ledger exploded" not in str(summary), "no error text on the wire"


def test_interrupt_after_summary_never_double_emits(captured, tmp_path, monkeypatch):
    """F1 regression: Ctrl-C at the post-success 'watch them upload?' prompt
    must not add an `aborted` summary after the `success` one."""

    def already_summarized(*, summary_state, telemetry, started_at, **kwargs):
        summary_state["emitted"] = True  # what _summary does on the success path
        raise KeyboardInterrupt

    monkeypatch.setattr(backfill_run, "_execute", already_summarized)
    monkeypatch.setattr(bf, "stop_all", lambda: None)
    backfill_run.execute(
        client_factory=nullcontext,
        folder=tmp_path,
        agent=bf.Agent("claude"),
        interactive=True,
        yes=False,
        telemetry=_ctx(),
    )
    assert [r["event"] for r in captured] == [], "no second terminal event"


def test_standalone_backfill_command_threads_a_command_context(monkeypatch, captured):
    """The `probe backfill` wiring: a dropped telemetry= pass-through would
    silently null the whole standalone funnel with every other test green."""
    monkeypatch.setattr(
        bootstrap, "ensure_persistent_install", lambda: SimpleNamespace(message=None)
    )
    seen: dict = {}

    def capture_run(**kwargs):
        seen["telemetry"] = kwargs.get("telemetry")
        return []

    monkeypatch.setattr(bf, "run", capture_run)  # main.py imports this module lazily
    rc = main_mod.main(["backfill", "--agent", "claude"])
    assert rc == 0
    ctx = seen["telemetry"]
    assert ctx is not None and ctx.via == "command"
    # R4: the pre-bootstrap entry event, like the wizard's — a bootstrap death
    # on the npx-distributed command must still enter the funnel.
    invoked = _props(captured, tm.EVENT_BACKFILL_INVOKED)
    assert invoked["via"] == "command"


def test_backfill_without_context_emits_nothing(captured, tmp_path):
    backfill_run.execute(
        client_factory=nullcontext,
        folder=tmp_path / "none",
        agent=bf.Agent("claude"),
        interactive=False,
        yes=True,
    )
    assert captured == []


def test_backfill_queued_files_remain_partial_until_receipted(captured, folder_harness):
    h = folder_harness
    _run_folder(h)
    summary = _props(captured, tm.EVENT_BACKFILL_SUMMARY)
    assert summary["outcome"] == "partial"
    assert summary["enqueued"] == summary["units_done"] == 1
    assert summary["coverage_pct"] == 0.0
    assert h.report()["queued"] == ["a.py"] and not h.remote.calls


def test_backfill_approved_event_counts_accepted_revisions(captured, folder_harness, monkeypatch):
    from probe.cli.backfill_plan import Assignment, Plan, ProjectSpec

    h = folder_harness
    decisions = iter(["revise", "import"])
    monkeypatch.setattr(
        tui, "review",
        lambda title, lines, choices: next(decisions) if title == "Review the import plan" else "skip",
    )
    monkeypatch.setattr(tui, "text", lambda *args: "put it in the reviewed project")
    revised = Plan([ProjectSpec("reviewed")], [Assignment("a.py", "reviewed")])
    monkeypatch.setattr(backfill_run, "revise", lambda *args, **kwargs: (revised, "", "session"))
    _run_folder(h, interactive=True, yes=False)
    assert _props(captured, tm.EVENT_BACKFILL_APPROVED)["revision_count"] == 1
    assert [row["slug"] for row in h.created] == ["reviewed"]


def test_backfill_real_interrupt_emits_one_aborted_summary(captured, folder_harness, monkeypatch):
    def interrupt(*args, **kwargs):
        raise KeyboardInterrupt

    monkeypatch.setattr(backfill_run, "classify", interrupt)
    lines = _run_folder(folder_harness)
    assert any("Stopped" in line for line in lines)
    assert _events(captured).count(tm.EVENT_BACKFILL_SUMMARY) == 1
    assert _props(captured, tm.EVENT_BACKFILL_SUMMARY)["outcome"] == "aborted"


def test_backfill_empty_after_delivery_updates_current_presence(captured, folder_harness, monkeypatch):
    h = folder_harness
    monkeypatch.setattr(h.client, "_wake_delivery", h.drain)
    _run_folder(h)
    (h.folder / "a.py").unlink()
    captured.clear()
    lines = _run_folder(h)
    assert any("no files" in line for line in lines)
    assert h.report()["vanished"] == ["a.py"] and not h.report()["delivered"]
    assert len(h.remote.calls) == 1
    assert _props(captured, tm.EVENT_BACKFILL_SUMMARY)["outcome"] == "empty_folder"
