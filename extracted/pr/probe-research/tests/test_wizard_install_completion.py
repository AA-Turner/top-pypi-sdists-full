"""The whole selected install settles before onboarding offers research imports."""

from contextlib import nullcontext
import os
from types import SimpleNamespace

import pytest
from typer.testing import CliRunner

from probe.cli import client_installation, doctor, import_jobs, onboarding_complete, setup, tui
from probe.cli.capabilities import Capabilities, TokenSource
from probe.sdk.config import save_context
from tests import test_wizard_auth_entry as auth

entry = auth.entry
main = auth.main


@pytest.fixture
def installation(entry, monkeypatch):
    """Use the real wizard and configure action; replace only external effects."""
    state = SimpleNamespace(
        ready=set(), modes={}, missing_rules=set(), work=[], registrations=[], offers=[], handoffs=[],
    )
    save_context({"token": "probe_pat_install_test", "mcp_token": "probe_pat_read_test"})
    monkeypatch.setattr(main, "_run_wizard_action", auth.apply_wizard_action)
    monkeypatch.setattr(setup, "detectable_sources", lambda: ("claude_code", "codex"))
    monkeypatch.setattr(main, "_install_grants_held", lambda *a, **k: True)
    monkeypatch.setattr(setup, "needs_authorization", lambda *a, **k: [])
    monkeypatch.setattr(setup, "codex_mcp_token_drifted", lambda: False)
    monkeypatch.setattr(setup, "refresh_marketplace", lambda: None)
    monkeypatch.setattr(setup, "authorize", lambda *a, **k: pytest.fail("unexpected authorization"))
    monkeypatch.setattr(main, "_run_selected_imports", lambda *a, **k: pytest.fail("imports were not selected"))
    monkeypatch.setattr(onboarding_complete, "show", lambda base: state.handoffs.append(base) or False)
    monkeypatch.setattr(tui, "working", lambda *a, **k: nullcontext())
    monkeypatch.setattr(tui, "say", lambda *a, **k: None)
    monkeypatch.setattr(tui, "Progress", lambda *a, **k: SimpleNamespace(**{
        name: lambda *a, **k: None
        for name in ("render", "start", "finish", "note", "note_next", "close")
    }))

    def collect():
        source = os.environ.get("PROBE_AGENT", "claude_code")
        attempted = source in state.ready
        mode = state.modes.get(source, "success")
        installed = attempted and mode == "success"
        return Capabilities(
            agent_source=source,
            claude_available=True,
            codex_available=True,
            logged_in_as="researcher@example.test",
            api_credential_valid=True,
            tracking_plugin_installed=installed,
            capture_plugin_installed=installed,
            plugins_verified=not (attempted and mode == "unverified"),
            capture_token_sources=(TokenSource.PAIRED_FILE,),
            capture_credential_valid=True,
            mcp_authenticated=True,
            auto_update_enabled=attempted,
            agent_rules_installed=attempted and source not in state.missing_rules,
        )

    def apply(kind):
        source = os.environ["PROBE_AGENT"]
        state.work.append((source, kind, [row[1] for row in state.registrations]))
        if kind == "tracking":
            state.ready.add(source)
        return ["Applied."]

    def register(caps, *, settings=None, complete=True):
        state.registrations.append((
            caps.agent_source, complete, client_installation.snapshot(caps, complete=complete),
        ))
        return []

    def offer(sources, **kwargs):
        state.offers.append((tuple(sources), [row[1] for row in state.registrations]))
        return set()

    monkeypatch.setattr(doctor, "collect", collect)
    monkeypatch.setattr(setup, "apply_tracking", lambda *a, **k: apply("tracking"))
    monkeypatch.setattr(setup, "apply_capture", lambda *a, **k: apply("capture"))
    monkeypatch.setattr(setup, "apply_auto_update", lambda *a, **k: apply("updates"))
    monkeypatch.setattr(setup, "apply_agent_rules", lambda *a, **k: apply("rules"))
    monkeypatch.setattr(main, "_register_local_capabilities", register)
    monkeypatch.setattr(setup, "run_backfill_offer", offer)
    return state


@pytest.mark.parametrize("agent,sources", [
    ("claude", ("claude_code",)),
    ("both", ("claude_code", "codex")),
])
def test_install_publishes_completion_after_all_agents_and_before_import_offer(
    installation, agent, sources,
):
    result = CliRunner().invoke(main.app, ["install", "--agent", agent])
    assert result.exit_code == 0, result.output
    assert [row[0] for row in installation.registrations] == list(sources)
    expected = [False] * (len(sources) - 1) + [True]
    assert [row[1] for row in installation.registrations] == expected
    assert all(not any(reports) for _, _, reports in installation.work)
    assert installation.offers == [(sources, expected)]
    assert len(installation.handoffs) == 1
    for _, complete, snapshot in installation.registrations:
        assert snapshot["tracking"] == ("installed" if complete else "unknown")
        assert snapshot["capture"] == ("installed" if complete else "unknown")


@pytest.mark.parametrize("failed_source", ["claude_code", "codex"])
def test_a_failed_selected_agent_never_settles_or_reaches_imports(installation, failed_source):
    installation.modes[failed_source] = "failed"
    result = CliRunner().invoke(main.app, ["install", "--agent", "both"])
    assert result.exit_code == 1, result.output
    assert installation.registrations
    assert all(not row[1] for row in installation.registrations)
    assert all(not any(reports) for _, _, reports in installation.work)
    assert not installation.offers
    assert installation.ready == (
        {"claude_code"} if failed_source == "claude_code" else {"claude_code", "codex"}
    )


@pytest.mark.parametrize("unverified_source", ["claude_code", "codex"])
def test_an_unverified_agent_keeps_later_success_from_settling_the_install(
    installation, unverified_source,
):
    installation.modes[unverified_source] = "unverified"
    result = CliRunner().invoke(main.app, ["install", "--agent", "both"])
    assert result.exit_code == 0, result.output
    assert [row[0] for row in installation.registrations] == ["claude_code", "codex"]
    assert [row[1] for row in installation.registrations] == [False, False]
    assert all(row[2]["tracking"] == row[2]["capture"] == "unknown"
               for row in installation.registrations)
    assert not installation.handoffs


def test_no_changes_still_settles_only_after_every_selected_agent(installation):
    installation.ready.update(("claude_code", "codex"))
    result = CliRunner().invoke(main.app, ["install", "--agent", "both"])
    assert result.exit_code == 0, result.output
    assert not installation.work
    assert [row[1] for row in installation.registrations] == [False, True]
    assert installation.offers == [(("claude_code", "codex"), [False, True])]


@pytest.mark.parametrize("imports", [set(), set(setup.BackfillChoice)])
def test_dashboard_handoff_follows_selected_imports_and_skips_the_menu(
    installation, monkeypatch, imports,
):
    events = []
    monkeypatch.setattr(setup, "run_backfill_offer", lambda *a, **k: imports)
    monkeypatch.setattr(main, "_run_selected_imports", lambda selected, **k: events.append(selected))
    monkeypatch.setattr(setup, "run_action_menu", lambda *a: pytest.fail("handoff must finish setup"))

    def handoff(_base):
        assert [row[1] for row in installation.registrations] == [False, True]
        events.append("dashboard")
        return True

    monkeypatch.setattr(onboarding_complete, "show", handoff)
    result = CliRunner().invoke(main.app, ["install", "--agent", "both"])
    assert result.exit_code == 0, result.output
    assert events == ([imports] if imports else []) + ["dashboard"]


def test_real_install_dashboard_handoff_preserves_saved_imports(installation, monkeypatch):
    monkeypatch.setattr(import_jobs, "_launch", import_jobs._read)
    job = import_jobs.enqueue("folder", {"approved": True}, "Saved import")
    monkeypatch.setattr(onboarding_complete, "show", lambda base: True)
    result = CliRunner().invoke(main.app, ["install", "--agent", "claude"])
    assert result.exit_code == 0, result.output
    assert import_jobs.get_job(job["id"])["id"] == job["id"]


def test_skipped_install_work_does_not_settle_despite_existing_plugins(installation, monkeypatch):
    installation.ready.update(("claude_code", "codex"))
    installation.missing_rules.add("codex")
    monkeypatch.setattr(setup, "PHASE_BUDGET_S", -1)
    result = CliRunner().invoke(main.app, ["install", "--agent", "both"])
    assert result.exit_code == 0, result.output
    assert not installation.work
    assert [row[1] for row in installation.registrations] == [False, False]
    assert not installation.handoffs


def test_wizard_signin_does_not_publish_install_completion_before_confirmation(entry, monkeypatch):
    from probe.sdk import device

    authorizations = []
    registrations = []

    def authorize(*args, **kwargs):
        authorizations.append(kwargs)
        return {"grants": [
            {"grant": "api", "token": "probe_pat_install_test"},
            {"grant": "mcp", "token": "probe_pat_read_test"},
            {"grant": "capture", "token": "ros_ing_install_test", "capture_source": "claude_code"},
        ]}

    monkeypatch.setattr(setup, "sign_in", auth.sign_in_to_account)
    monkeypatch.setattr(device, "device_authorize", authorize)
    monkeypatch.setattr(setup, "account_email", lambda *a: "researcher@example.test")
    monkeypatch.setattr(setup, "sync_codex_mcp_token", lambda: [])
    monkeypatch.setattr(client_installation, "register", lambda *a, **k: registrations.append(k) or [])
    result = CliRunner().invoke(main.app, ["wizard"])
    assert result.exit_code == 0, result.output
    assert len(authorizations) == 1
    assert [event for event, _ in entry] == ["menu"]
    assert registrations == []
