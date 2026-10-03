"""The guided install's own funnel: settle, import offer, handoff, removal.

`test_wizard_telemetry.py` covers the ENTRY funnel and the folder lane. What it
could not reach is everything the guided install added afterwards -- the point
where an installation settles, the import offer, the dashboard handoff, and
Uninstall, which had no client-side event at all.

Every emission asserted here runs on the real line, driven through the same
`install` / `wizard` entry points a person uses; only external effects are
stubbed. The wizard's questions are scripted, never simulated.
"""

from __future__ import annotations

import pytest
from typer.testing import CliRunner

from probe.cli import doctor, import_jobs_ui, onboarding_complete, setup, tui
from probe.cli import telemetry as tm
from probe.cli.actions import Action
from probe.cli.capabilities import Capabilities
from tests import test_wizard_auth_entry as auth
from tests import test_wizard_install_completion as completion

entry = auth.entry
installation = completion.installation
main = auth.main


@pytest.fixture()
def captured(monkeypatch):
    """Telemetry ON, records captured at the queue seam -- no thread, no network.

    Also re-points the base URL at the hosted service. The shared wizard
    fixtures use `https://api.test`, which the self-host egress gate reads as
    somebody else's backend and disables telemetry for outright -- so every
    assertion in this file would pass while proving nothing. Requested AFTER
    the wizard fixture in each signature, because that is what sets it.
    """
    monkeypatch.setenv("PROBE_BASE_URL", "https://api.research.prbe.ai")
    monkeypatch.setenv("PROBE_TELEMETRY", "on")
    records: list[dict] = []
    monkeypatch.setattr(tm, "_sender", None)
    monkeypatch.setattr(tm, "_flush_registered", True)
    monkeypatch.setattr(tm._Sender, "start", lambda self: None)
    monkeypatch.setattr(tm._Sender, "put", lambda self, rec: records.append(rec))
    return records


def _events(records):
    return [record["event"] for record in records]


def _props(records, event):
    return next(record["properties"] for record in records if record["event"] == event)


def _all_props(records, event):
    return [record["properties"] for record in records if record["event"] == event]


# --- the installation settling ---------------------------------------------


@pytest.mark.parametrize("agent,agent_count", [("claude", 1), ("both", 2)])
def test_install_settles_once_however_many_agents_were_selected(
    installation, captured, agent, agent_count,
):
    """`configure_completed` is per configure CALL. A two-agent install emits
    two of those and neither answers "is this machine set up?"."""
    result = CliRunner().invoke(main.app, ["install", "--agent", agent])
    assert result.exit_code == 0, result.output
    settled = _all_props(captured, tm.EVENT_WIZARD_INSTALL_SETTLED)
    assert len(settled) == 1
    assert settled[0]["outcome"] == tm.InstallSettledOutcome.SETTLED
    assert settled[0]["agent_count"] == agent_count
    assert settled[0]["guided"] is True


def test_an_unverified_agent_reports_the_install_unsettled(installation, captured):
    """The state the dashboard refuses to advance on, so the one the funnel
    must be able to count separately from a clean success."""
    installation.modes["codex"] = "unverified"
    result = CliRunner().invoke(main.app, ["install", "--agent", "both"])
    assert result.exit_code == 0, result.output
    assert _props(captured, tm.EVENT_WIZARD_INSTALL_SETTLED)["outcome"] == (
        tm.InstallSettledOutcome.UNSETTLED
    )


def test_a_failed_agent_never_reports_a_settled_install(installation, captured):
    installation.modes["codex"] = "failed"
    result = CliRunner().invoke(main.app, ["install", "--agent", "both"])
    assert result.exit_code == 1, result.output
    # The run dies before the per-agent loop finishes, so nothing claims the
    # installation settled -- in either direction.
    assert tm.EVENT_WIZARD_INSTALL_SETTLED not in _events(captured)


# --- what the import offer was answered with -------------------------------


@pytest.mark.parametrize("picked,choices,navigation", [
    (set(), [], "skip"),
    ({setup.BackfillChoice.PAST_SESSIONS}, ["past_sessions"], "continue"),
    ({setup.BackfillChoice.PROJECT_FOLDER}, ["project_folder"], "continue"),
    (set(setup.BackfillChoice), ["past_sessions", "project_folder"], "continue"),
])
def test_the_import_offer_reports_every_answer_including_skip(
    installation, captured, monkeypatch, picked, choices, navigation,
):
    """Skipping is the most common answer here. An event that only fired when
    a box was ticked would leave the single largest outcome invisible."""
    monkeypatch.setattr(setup, "run_backfill_offer", lambda *a, **k: picked)
    monkeypatch.setattr(main, "_run_selected_imports", lambda *a, **k: None)
    result = CliRunner().invoke(main.app, ["install", "--agent", "claude"])
    assert result.exit_code == 0, result.output
    chosen = _props(captured, tm.EVENT_WIZARD_IMPORTS_CHOSEN)
    assert chosen["choices"] == choices
    assert chosen["choice_count"] == len(choices)
    assert chosen["navigation"] == navigation
    assert chosen["onboarding"] is True
    assert chosen["offered_again"] is False


def test_backing_out_of_the_import_offer_is_not_an_answer(
    installation, captured, monkeypatch,
):
    monkeypatch.setattr(setup, "run_backfill_offer", lambda *a, **k: tui.BACK)
    result = CliRunner().invoke(main.app, ["install", "--agent", "claude"])
    assert result.exit_code == 0, result.output
    chosen = _props(captured, tm.EVENT_WIZARD_IMPORTS_CHOSEN)
    assert chosen["navigation"] == "back" and chosen["choice_count"] == 0
    # Back leaves the install standing but skips the handoff page.
    assert tm.EVENT_WIZARD_ONBOARDING_COMPLETED not in _events(captured)


def test_a_reopened_offer_says_it_is_a_second_pass(installation, captured, monkeypatch):
    """A lane that went Back reopens the offer with the unanswered choices.
    Without `offered_again` those re-asks inflate the selection counts."""
    answers = iter([{setup.BackfillChoice.PAST_SESSIONS}, set()])
    monkeypatch.setattr(setup, "run_backfill_offer", lambda *a, **k: next(answers))
    monkeypatch.setattr(main, "_run_selected_imports", lambda *a, **k: tui.BACK)
    result = CliRunner().invoke(main.app, ["install", "--agent", "claude"])
    assert result.exit_code == 0, result.output
    passes = _all_props(captured, tm.EVENT_WIZARD_IMPORTS_CHOSEN)
    assert [row["offered_again"] for row in passes] == [False, True]


# --- the dashboard handoff, the bottom of the funnel -----------------------


@pytest.mark.parametrize("opened,outcome", [
    (True, "dashboard_opened"),
    (False, "returned_to_menu"),
    (import_jobs_ui.Navigation.EXIT, "exited"),
])
def test_the_handoff_page_reports_which_way_it_ended(
    installation, captured, monkeypatch, opened, outcome,
):
    monkeypatch.setattr(onboarding_complete, "show", lambda base: opened)
    result = CliRunner().invoke(main.app, ["install", "--agent", "claude"])
    assert result.exit_code == 0, result.output
    done = _props(captured, tm.EVENT_WIZARD_ONBOARDING_COMPLETED)
    assert done["outcome"] == outcome
    assert done["imports_chosen"] == []


def test_abandoning_the_handoff_is_counted_without_stopping_imports(
    installation, captured, monkeypatch,
):
    """Ctrl-C records navigation away; it does not cancel approved imports."""

    def interrupted(_base):
        raise KeyboardInterrupt

    monkeypatch.setattr(onboarding_complete, "show", interrupted)
    CliRunner().invoke(main.app, ["install", "--agent", "claude"])
    assert _props(captured, tm.EVENT_WIZARD_ONBOARDING_COMPLETED)["outcome"] == (
        tm.OnboardingOutcome.ABANDONED
    )


def test_the_whole_guided_install_shares_one_session_id(installation, captured):
    result = CliRunner().invoke(main.app, ["install", "--agent", "both"])
    assert result.exit_code == 0, result.output
    assert len({record["properties"]["session_id"] for record in captured}) == 1


# --- removal ----------------------------------------------------------------


@pytest.fixture
def removal(entry, monkeypatch):
    """A machine with Probe on it, and a scripted Uninstall from the menu."""
    installed = Capabilities(
        claude_available=True,
        logged_in_as="researcher@example.test",
        api_credential_valid=True,
        tracking_plugin_installed=True,
        capture_plugin_installed=True,
        agent_rules_installed=True,
    )
    monkeypatch.setattr(doctor, "collect", lambda: installed)
    actions = iter((Action.UNINSTALL, Action.EXIT))
    monkeypatch.setattr(setup, "run_action_menu", lambda _caps: next(actions))
    monkeypatch.setattr(setup, "run_agent_menu", lambda *a, **k: ("claude_code",))
    monkeypatch.setattr(setup, "finish_removal", lambda: ["Signed out."])
    monkeypatch.setattr(setup, "remove_everything", lambda caps: ["Removed."])
    monkeypatch.setattr(main, "_register_local_capabilities", lambda *a, **k: [])
    # The REAL uninstall action, so the per-agent confirmation -- the gate a
    # one-agent removal actually goes through -- is the one being exercised.
    monkeypatch.setattr(main, "_run_wizard_action", auth.apply_wizard_action)
    return monkeypatch


def test_uninstall_reports_what_was_on_the_machine_before_it_was_removed(
    removal, captured,
):
    """After the per-agent loop the state being removed is unreadable by
    construction, so the `started` event has to carry it."""
    removal.setattr(setup, "confirm_removal", lambda *a, **k: True)
    result = CliRunner().invoke(main.app, ["wizard"])
    assert result.exit_code == 0, result.output
    started = _props(captured, tm.EVENT_WIZARD_UNINSTALL_STARTED)
    assert started["tracking_installed"] is True
    assert started["capture_installed"] is True
    assert started["agent_rules_installed"] is True
    assert started["was_signed_in"] is True
    assert started["confirmed_via"] == "prompt"
    done = _props(captured, tm.EVENT_WIZARD_UNINSTALL_COMPLETED)
    assert done["outcome"] == tm.UninstallOutcome.REMOVED
    assert done["warnings"] == 0
    assert done["agent_count"] == 1
    assert "duration_seconds" in done


@pytest.mark.parametrize("answer", [False, None, "back"])
def test_backing_out_of_the_confirmation_is_the_outcome_no_server_can_see(
    removal, captured, answer,
):
    """The device is still here, so nothing reports anything: no capability
    report changes, no credential is revoked. This is the only record."""
    removal.setattr(setup, "confirm_removal", lambda *a, **k: answer)
    CliRunner().invoke(main.app, ["wizard"])
    assert _props(captured, tm.EVENT_WIZARD_UNINSTALL_STARTED)["tracking_installed"] is True
    done = _props(captured, tm.EVENT_WIZARD_UNINSTALL_COMPLETED)
    assert done["outcome"] == tm.UninstallOutcome.DECLINED
    assert "warnings" not in done  # nothing ran, so there is nothing to grade


def test_a_removal_that_left_something_behind_is_not_a_clean_one(removal, captured):
    removal.setattr(setup, "confirm_removal", lambda *a, **k: True)
    removal.setattr(
        setup, "remove_everything",
        lambda caps: ["Removed.", "! left the Codex MCP entry in place"],
    )
    CliRunner().invoke(main.app, ["wizard"])
    done = _props(captured, tm.EVENT_WIZARD_UNINSTALL_COMPLETED)
    assert done["outcome"] == tm.UninstallOutcome.REMOVED and done["warnings"] == 1


def test_the_removal_is_still_attributable_after_the_credential_is_gone(
    removal, captured, monkeypatch,
):
    """The event that says a customer left must not arrive attached to nobody.

    `finish_removal` revokes this device's token and clears it, and the
    completion event is emitted after — so the sender, which resolves identity
    lazily, finds no token and falls back to `machine:<id>`. Every #probe-usage
    destination filters on a known person, so that is not mis-attribution, it
    is silence. The identity is resolved while the credential still exists and
    rides the record.
    """
    from probe.sdk import _telemetry_core as core

    monkeypatch.setattr(
        core, "resolve_identity",
        lambda cfg, **kw: {"distinct_id": "user-uuid", "email": "r@lab.test",
                           "customer_id": "lab", "authenticated": True},
    )
    removal.setattr(setup, "confirm_removal", lambda *a, **k: True)

    def release_everything():
        # What the real one does: the token is gone by the time the event fires.
        from probe.sdk.config import save_context

        save_context({})
        return ["Signed out."]

    removal.setattr(setup, "finish_removal", release_everything)
    result = CliRunner().invoke(main.app, ["wizard"])
    assert result.exit_code == 0, result.output
    record = next(
        row for row in captured if row["event"] == tm.EVENT_WIZARD_UNINSTALL_COMPLETED
    )
    assert record["identity"]["distinct_id"] == "user-uuid"
    assert record["identity_mode"] == tm.IdentityMode.AUTHENTICATED


def test_an_unresolvable_identity_never_fails_the_removal(removal, captured, monkeypatch):
    """Fail-soft: a pin that cannot resolve leaves the event as it was before,
    and above all does not raise into an uninstall."""
    from probe.sdk import _telemetry_core as core

    def unreachable(cfg, **kwargs):
        raise OSError("network down")

    monkeypatch.setattr(core, "resolve_identity", unreachable)
    removal.setattr(setup, "confirm_removal", lambda *a, **k: True)
    result = CliRunner().invoke(main.app, ["wizard"])
    assert result.exit_code == 0, result.output
    record = next(
        row for row in captured if row["event"] == tm.EVENT_WIZARD_UNINSTALL_COMPLETED
    )
    assert "identity" not in record


def test_a_declined_removal_needs_no_pin(removal, captured):
    """Nothing was released, so the ordinary lazy resolution still works — and
    pinning every event would put a /v1/me call on the hot path."""
    removal.setattr(setup, "confirm_removal", lambda *a, **k: False)
    CliRunner().invoke(main.app, ["wizard"])
    record = next(
        row for row in captured if row["event"] == tm.EVENT_WIZARD_UNINSTALL_COMPLETED
    )
    assert "identity" not in record


def test_unattended_uninstall_enters_the_funnel_without_a_prompt(captured, monkeypatch):
    """`--action uninstall --yes` never shows the confirmation. It is still a
    removal, and the fleet's scripted teardowns are exactly the population a
    `confirmed_via` breakdown exists to separate out."""
    from types import SimpleNamespace

    from probe.cli import bootstrap, plugin_cli

    monkeypatch.setattr(
        bootstrap, "ensure_persistent_install", lambda **_: SimpleNamespace(message=None)
    )
    monkeypatch.setattr(plugin_cli, "available", lambda source: source == "claude_code")
    monkeypatch.setattr(doctor, "collect", lambda: Capabilities(claude_available=True))
    monkeypatch.setattr(setup, "remove_everything", lambda caps: ["Removed."])
    monkeypatch.setattr(main, "_register_local_capabilities", lambda *a, **k: [])
    monkeypatch.setattr(setup, "finish_removal", lambda: [])
    assert main.main(["wizard", "--action", "uninstall", "--yes", "--agent", "claude"]) == 0
    assert _props(captured, tm.EVENT_WIZARD_UNINSTALL_STARTED)["confirmed_via"] == "flag"
    assert _props(captured, tm.EVENT_WIZARD_UNINSTALL_COMPLETED)["outcome"] == (
        tm.UninstallOutcome.REMOVED
    )
