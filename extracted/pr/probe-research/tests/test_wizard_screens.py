"""Every wizard result page: what was asked, then Next (must-dos) and Details
(errors), never the routine report each helper prints.

2026-10-26: "audit all possible screens on the wizard and basically the rule is
to remove all massive walls of text and data dumps that dont mean anything",
after a Who records page that said "Installed 11 skill(s) in <path>: <every
name>" as its title and "Takes effect in new X sessions." four times.
"""

from __future__ import annotations

import importlib

from probe.cli import doctor, tui
from probe.cli import setup as wizard
from probe.cli.capabilities import Capabilities
from probe.cli.setup import RunSummary, SummaryAction
from probe.sdk import session_marker
from tests.test_wizard_auth_entry import entry  # noqa: F401 -- a fixture: the wizard's menu, scripted
from typer.testing import CliRunner

main = importlib.import_module("probe.cli.main")


def test_attention_lines_keep_errors_and_what_follows_them_only():
    lines = [
        "Refreshed 2 skills in ~/.claude/skills.",
        "Who records in Claude Code → the agent",
        "! could not remove probe-research-tap for Codex: busy",
        "  Both plugins are installed; remove probe-research-tap from Codex by hand.",
        "Takes effect in new Codex sessions.",
        "  They also show in your terminal.",
    ]
    assert wizard.attention_lines(lines) == [
        "could not remove probe-research-tap for Codex: busy",
        "  Both plugins are installed; remove probe-research-tap from Codex by hand.",
    ]


def test_a_result_page_says_only_what_there_is_to_say():
    assert wizard.result_page("Done") == ["Done"]
    assert wizard.result_page(["Done", "sub"], next_steps=["Restart", "Restart"], details=["x"]) == [
        "Done", "sub", "", "Next:", "  Restart", "", "Details:", "  x",
    ]


def _who_records_report(value: str) -> list[str]:
    report = ["Installed 11 skills in ~/.claude/skills.", "Refreshed 2 skills in ~/.claude/skills."]
    for label in ("Claude Code", "Codex", "pi", "Kimi Code"):
        report += [
            f"Who records in {label} → {value}",
            f"{label}'s reasoning summaries → back to {label}'s default.",
            f"Takes effect in new {label} sessions.",
        ]
    return report


def test_who_records_is_one_answer_not_every_step_for_every_agent():
    sources = ["claude_code", "codex", "pi", "kimi_code"]
    report = [*_who_records_report("the daemon"), "In the new Codex session: `/hooks` › approve the Probe hooks."]
    page = main._recorder_page(
        session_marker.RECORDER_DAEMON, sources, sources, report,
        daemon_page=["Daemon sees the agent's reasoning → on (Claude Code, Codex; new sessions)"], left_alone=[],
    )
    assert page == [
        "The Probe daemon now records for all 4 coding agents",
        "Daemon sees the agent's reasoning → on (Claude Code, Codex; new sessions)",
        "",
        "Next:",
        "  Start new sessions to use it: open ones keep recording as before.",
        "  In the new Codex session: `/hooks` › approve the Probe hooks.",
    ]


def test_who_records_back_to_the_agent_counts_and_names_the_error():
    sources = ["claude_code", "codex", "pi", "kimi_code"]
    report = [*_who_records_report("the agent"), "! could not record who records in pi: disk full",
              "  Nothing else changed. Switch Who records again to retry."]
    page = main._recorder_page(
        session_marker.RECORDER_AGENT, sources, ["claude_code", "codex", "kimi_code"], report,
        daemon_page=[], left_alone=[],
    )
    assert page[0] == "3 of 4 coding agents record for themselves again"
    assert page[page.index("Details:") + 1:] == [
        "  could not record who records in pi: disk full",
        "    Nothing else changed. Switch Who records again to retry.",
    ]
    assert not any("skills" in line or "Takes effect" in line for line in page)


def test_an_uninstall_counts_agents_and_keeps_the_device_errors():
    summary = RunSummary(SummaryAction.UNINSTALL, ["claude_code", "codex"])
    summary.record("claude_code", ok=True)
    summary.record("codex", ok=True)
    summary.subtitle = "This device is signed out."
    summary.note(*wizard.attention_lines([
        "Revoked this device's read-only MCP token.",
        "! could not release this device's API token (offline). Revoke it in the dashboard.",
        "Setting Probe up again will ask you to sign in.",
    ]))
    assert summary.lines() == [
        "Removed Probe from both coding agents",
        "This device is signed out.",
        "",
        "  ✔ Claude Code",
        "  ✔ Codex",
        "",
        "Details:",
        "  could not release this device's API token (offline). Revoke it in the dashboard.",
    ]


def _caps(source: str, **kw) -> Capabilities:
    defaults = dict(agent_source=source, logged_in_as="r@x", cli_version="0.330.0", claude_available=True,
                    codex_available=False)
    return Capabilities(**{**defaults, **kw})


def test_diagnose_leads_with_the_verdict_and_says_a_shared_warning_once(monkeypatch):
    warning = "could not verify the capture credential (offline or endpoint unavailable)"
    by_source = {
        "claude_code": _caps("claude_code", warnings=(warning,)),
        "kimi_code": _caps("kimi_code", warnings=(warning, "Kimi Code: the tap is behind")),
    }
    page = doctor.summary(by_source, recorder="agent")
    assert page[0] == "Probe Research doctor: 2 problems"
    problems = page[page.index("Problems:") + 1:page.index("Problems:") + 3]
    assert problems == [f"  {warning}", "  Kimi Code: the tap is behind"]
    assert page[-1] == "c copies the full report; `probe doctor` prints it."
    assert len(page) < 15


def test_diagnose_with_nothing_wrong_says_so(monkeypatch):
    page = doctor.summary({"claude_code": _caps("claude_code")}, recorder="agent")
    assert page[0] == "Probe Research doctor: no problems found"
    assert "Problems:" not in page


def test_the_install_screen_says_paired_once():
    assert tui._merged_pairings([
        "Claude Code Session capture paired (device ?).",
        "Codex Session capture paired (device 7).",
        "pi Session capture paired (device ?).",
        "Status line: on.",
    ]) == ["Session capture paired: Claude Code, Codex and pi.", "Status line: on."]


def test_a_who_records_switch_that_moved_nobody_does_not_claim_one():
    page = main._recorder_page(
        session_marker.RECORDER_DAEMON, ["claude_code"], [],
        ["! could not install probe-research-daemon for Claude Code: offline",
         "  Nothing else changed. Switch Who records again to retry."],
        daemon_page=[], left_alone=[],
    )
    assert page[0] == "Who records did not change"
    assert "Next:" not in page


def test_a_kept_daemon_key_is_a_next_step_not_an_error():
    kept = ("Kept the daemon's key: 2 open session(s) still use it. "
            "Revoke it in the dashboard under Settings › Connected clients once they end.")
    page = main._recorder_page(
        session_marker.RECORDER_AGENT, ["claude_code"], ["claude_code"], [kept],
        daemon_page=[], left_alone=[],
    )
    assert f"  {kept}" in page and "Details:" not in page


def test_settings_never_claims_a_change_that_failed_everywhere(monkeypatch):
    from probe.cli import setup as wizard

    def stopped(changes, **_kw):
        return ["Claude Code:", "! not finished — re-run `probe wizard` › Settings to retry.", "",
                "Codex:", "! not finished — re-run `probe wizard` › Settings to retry.", ""]

    monkeypatch.setattr(main, "_apply_capability_settings", stopped)
    monkeypatch.setattr(main, "_capability_setting_now", lambda setting: False)  # still off on disk
    monkeypatch.setattr(wizard, "interactive", lambda: True)
    monkeypatch.setattr(tui, "clear", lambda: None)
    monkeypatch.setattr(wizard, "read_settings", lambda caps: {wizard.Setting.AUTO_UPDATE: False})
    monkeypatch.setattr(wizard, "run_settings_menu", lambda current, **k: {wizard.Setting.AUTO_UPDATE: True})
    caps = {"claude_code": _caps("claude_code"), "codex": _caps("codex")}
    lines = main._run_settings_action(yes=False, caps_by_source=caps, base_now="https://x")
    assert lines[0] == "Automatic updates did not change"


def test_an_error_named_by_its_exception_needs_attention():
    from probe.cli import setup as wizard

    assert wizard.needs_attention("W&B history pending (ConnectError). File delivery continues.")
    assert wizard.needs_attention("reconstruction stage incomplete (OSError); saved work retained.")
    assert not wizard.needs_attention("All sessions imported.")


def test_diagnose_names_an_mcp_that_needs_a_login_and_a_stuck_outbox(monkeypatch):
    from probe.cli.capabilities import McpState

    caps = _caps("claude_code", tracking_plugin_installed=True, outbox_status={"failed": 3})
    monkeypatch.setattr(type(caps), "mcp_state", property(lambda self: McpState.LOGIN_NEEDED))
    page = doctor.summary({"claude_code": caps}, recorder="agent")
    assert page[0] == "Probe Research doctor: 2 problems"
    assert any(line.startswith("  Claude Code: MCP login needed") for line in page)
    assert "  Outbox: 3 write(s) dead-lettered (`probe outbox status`)." in page


def test_settings_reports_what_the_device_holds_after_a_partial_apply(monkeypatch):
    """Configure can write the device-wide file, then fail on one agent's
    MCP: the setting did change, and the error is still shown."""
    from probe.cli import setup as wizard

    monkeypatch.setattr(main, "_apply_capability_settings", lambda changes, **k: [
        "Codex:", "! not finished — re-run `probe wizard` › Settings to retry.", ""])
    monkeypatch.setattr(main, "_capability_setting_now", lambda setting: True)
    monkeypatch.setattr(wizard, "interactive", lambda: True)
    monkeypatch.setattr(tui, "clear", lambda: None)
    monkeypatch.setattr(wizard, "read_settings", lambda caps: {wizard.Setting.AUTO_UPDATE: False})
    monkeypatch.setattr(wizard, "run_settings_menu", lambda current, **k: {wizard.Setting.AUTO_UPDATE: True})
    lines = main._run_settings_action(yes=False, caps_by_source={"codex": _caps("codex")}, base_now="https://x")
    assert lines[0] == "Automatic updates → on"
    assert "  Codex: not finished — re-run `probe wizard` › Settings to retry." in lines


def test_updates_capture_answer_is_the_verdict_and_the_errors_only():
    """Update's "Turn on session capture?" (sign-in lock): its page said each
    agent's whole configure report above the Update's headline."""
    lines = [
        "Claude Code:", "Session capture: on.", "Status line: on.", "",
        "Codex:", "! not finished — pick “Install Probe” to turn capture on.", "",
        "Session capture is on for Claude Code.",
        "! Session capture is still off for Codex.",
    ]
    verdict, problems = main._capture_answer(lines)
    assert verdict == ["Session capture is on for Claude Code.", "Session capture is still off for Codex."]
    assert problems == ["Codex: not finished — pick “Install Probe” to turn capture on."]


def test_diagnose_says_what_lifts_a_sign_ins_capture_lock():
    page = doctor.summary({"claude_code": _caps("claude_code", capture_awaiting_confirmation=True)}, recorder="agent")
    assert any(line.endswith("capture off (finish Install)") for line in page)


def test_diagnose_counts_a_daemon_with_no_key(monkeypatch):
    """Recording through the daemon with no daemon key: nothing records, and
    the full report's "Daemon key: none" was the only place that said so."""
    monkeypatch.setattr(wizard, "companion_token_held", lambda: False)
    page = doctor.summary({"claude_code": _caps("claude_code")}, recorder=session_marker.RECORDER_DAEMON)
    assert page[0] == "Probe Research doctor: 1 problem"
    assert "  The Probe daemon has no key: press Enter on Who records to approve one." in page


def test_an_import_keeps_its_never_silent_lines():
    assert wizard.needs_attention("codex sessions were not looked at — no paired device for that agent on this machine.")
    assert wizard.needs_attention("3 identities unverified · 0 conflicting copies · 2 unreadable")


def test_diagnose_names_each_problem_once_with_every_agent_that_has_it(monkeypatch):
    """Seen in a real terminal (0.333.0): the same capture warning under
    Claude Code and again under Codex, and Codex's MCP login said twice."""
    from probe.cli.capabilities import McpState

    warning = "could not verify the capture credential (offline or endpoint unavailable)"
    codex = _caps("codex", codex_available=True, warnings=(warning, "the probe-research MCP is installed but not logged in; "
                                              "re-run `probe wizard` to complete Codex OAuth"))
    monkeypatch.setattr(type(codex), "mcp_state", property(
        lambda self: McpState.LOGIN_NEEDED if self.agent_source == "codex" else McpState.ON))
    by_source = {"claude_code": _caps("claude_code", warnings=(warning,)), "codex": codex,
                 "pi": _caps("pi")}
    page = doctor.summary(by_source, recorder="agent")
    problems = page[page.index("Problems:") + 1:-2]
    assert problems == [
        f"  Claude Code and Codex: {warning}",
        "  Codex: the probe-research MCP is installed but not logged in; re-run `probe wizard` to complete Codex OAuth",
    ]


def test_three_agents_are_a_list_not_a_chain_of_ands():
    assert wizard.agent_label(["claude_code", "codex", "pi", "kimi_code"]) == "Claude Code, Codex, pi and Kimi Code"
    assert wizard.agent_label(["claude_code", "codex"]) == "Claude Code and Codex"


def test_a_page_after_signing_out_says_finish_not_menu(entry, monkeypatch):  # noqa: F811
    """Seen in a real terminal (0.333.0): Uninstall's page said "return to the
    menu", then the wizard ended because the device was signed out."""
    from probe.cli.actions import Action
    from probe.sdk.config import save_context

    save_context({"token": "probe_pat_existing", "base_url": "https://api.test"})
    picks = iter([Action.UNINSTALL, Action.EXIT])
    monkeypatch.setattr(wizard, "run_action_menu", lambda _caps: next(picks))
    monkeypatch.setattr(wizard, "interactive", lambda: True)
    monkeypatch.setattr(tui, "clear", lambda: None)

    def removed(action, **_kw):
        save_context({"token": None})  # what finishing a removal does to this device
        return ["Removed."]

    monkeypatch.setattr(main, "_run_wizard_action", removed)
    monkeypatch.setattr(wizard, "finish_removal", lambda: iter(()))
    prompts: list[str] = []
    monkeypatch.setattr(tui, "page", lambda lines, **kw: prompts.append(kw.get("prompt")))
    CliRunner().invoke(main.app, ["wizard"])
    assert prompts[-1] == "Press enter to finish…"
