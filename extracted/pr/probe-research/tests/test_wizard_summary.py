"""The final screen of an install or an Update: how many coding agents worked,
which, then Details with only what needs attention.

It used to be every agent's full report, one after another: "already at the
latest", "Refreshed the Probe block", "Status line: on" around the one line
that mattered (a Codex plugin that could not be confirmed, and what to run).
"""

from __future__ import annotations

import json
import subprocess

from probe.cli import codex_config, updater, upgrading
from probe.cli import setup as wizard
from probe.cli.setup import RunSummary, SummaryAction

from tests.test_parallel_install_update import _plugin_result, one_update  # noqa: F401 - fixture
from tests.test_updater import _failed_with, _fake_codex


def test_an_update_names_what_worked_then_only_what_needs_attention():
    summary = RunSummary(SummaryAction.UPDATE, ["claude_code", "codex", "kimi_code", "pi"])
    summary.subtitle = "Probe CLI 0.324.0"
    summary.record("claude_code", ok=True, summary="plugin 0.180.0 (updated), tap 0.10.23")
    summary.record(
        "codex",
        ok=False,
        notes=[
            "could not confirm probe-research-daemon: `codex plugin list --json` timed out",
            "Update them manually (Codex needs no restart):",
            "  codex plugin add probe-research-daemon@research-os-agent",
        ],
    )
    summary.record("kimi_code", ok=True, summary="plugin 0.180.0, tap 0.10.23")
    summary.record("pi", ok=True, summary="package 0.7.2")

    lines = summary.lines()

    assert lines[:2] == ["Updated 3 of 4 coding agents", "Probe CLI 0.324.0"]
    worked = [line for line in lines if line.startswith("  ✔")]
    assert [line.split()[1] for line in worked] == ["Claude", "Kimi", "pi"]
    assert "plugin 0.180.0 (updated), tap 0.10.23" in worked[0]
    details = lines[lines.index("Details:") + 1:]
    assert details == [
        "  Codex: could not confirm probe-research-daemon: `codex plugin list --json` timed out",
        "    Update them manually (Codex needs no restart):",
        "      codex plugin add probe-research-daemon@research-os-agent",
    ]
    assert not any("already" in line or "Status line" in line for line in lines)


def test_nothing_to_attend_to_has_no_details_section():
    summary = RunSummary(SummaryAction.UPDATE, ["claude_code", "codex"])
    summary.record("claude_code", ok=True, summary="plugin 0.180.0")
    summary.record("codex", ok=True, summary="plugin 0.180.0")
    lines = summary.lines()
    assert lines[0] == "Updated both coding agents"
    assert "Details:" not in lines


def test_a_run_wide_failure_is_named_once_and_does_not_fail_every_agent():
    summary = RunSummary(SummaryAction.UPDATE, ["claude_code", "codex"])
    for source in ("claude_code", "codex"):
        summary.note("Probe CLI: uv refused")
        summary.record(source, ok=True, summary="plugin 0.180.0")
    lines = summary.lines()
    assert lines[0] == "Updated both coding agents"
    assert lines.count("  Probe CLI: uv refused") == 1


def test_an_install_that_stopped_names_the_agents_it_never_reached():
    summary = RunSummary(SummaryAction.INSTALL, ["claude_code", "codex", "kimi_code"])
    summary.record("claude_code", ok=True, restart=True)
    summary.record("codex", ok=False, notes=["not finished: no credential for: capture."])
    lines = summary.lines()
    assert lines[0] == "Installed Probe in 1 of 3 coding agents"
    assert "  ✔ Claude Code" in lines
    details = lines[lines.index("Details:") + 1:]
    assert details == [
        "  Codex: not finished: no credential for: capture.",
        "  Kimi Code: not started (the run stopped at Codex)",
    ]
    assert "  Restart Claude Code to load Probe." in lines


def test_one_agent_is_named_not_counted():
    summary = RunSummary(SummaryAction.INSTALL, ["codex"])
    summary.record("codex", ok=True, summary="already set up")
    assert summary.lines()[:3] == ["Installed Probe in Codex", "", "  ✔ Codex   already set up"]
    failed = RunSummary(SummaryAction.UPDATE, ["codex"])
    failed.record("codex", ok=False)
    assert failed.lines()[0] == "Codex was not fully updated"
    assert failed.lines()[-1] == "  Codex: not updated"


def test_an_updates_outcome_carries_its_summary_and_what_failed(one_update, monkeypatch):  # noqa: F811
    monkeypatch.setattr(updater, "update_plugin", lambda *a: _plugin_result("claude_code"))
    monkeypatch.setattr(
        updater, "update_codex_plugins",
        lambda: updater.PluginResult(
            True, False, False, "probe-research=1", "probe-research=1", "could not confirm the plugins"
        ),
    )
    outcomes = upgrading.perform_updates(["claude_code", "codex"], base_url="https://x")
    assert outcomes["claude_code"].summary == "plugin 1" and outcomes["claude_code"].problems == []
    assert outcomes["codex"].problems[0] == "could not confirm the plugins"
    assert outcomes["codex"].problems[1].startswith("Update them manually")
    assert outcomes["codex"].cli.startswith("Probe CLI ")


def _codex_files(tmp_path, monkeypatch, plugins: dict[str, list[str]]):
    home = tmp_path / "codex"
    monkeypatch.setenv("CODEX_HOME", str(home))
    home.mkdir()
    (home / "config.toml").write_text(
        "".join(f'[plugins."{name}@research-os-agent"]\nenabled = true\n\n' for name in plugins)
    )
    for name, versions in plugins.items():
        for version in versions:
            manifest = home / "plugins" / "cache" / "research-os-agent" / name / version / ".codex-plugin"
            manifest.mkdir(parents=True)
            (manifest / "plugin.json").write_text(json.dumps({"name": name, "version": version}))


def test_codex_files_name_the_newest_copy_of_each_added_plugin(tmp_path, monkeypatch):
    _codex_files(tmp_path, monkeypatch, {"probe-research-daemon": ["0.9.0", "0.180.0"], "probe-research-tap": []})
    assert codex_config.installed_plugin_versions("research-os-agent") == {"probe-research-daemon": "0.180.0"}


def test_a_codex_list_that_times_out_is_answered_from_codexs_files(tmp_path, monkeypatch):
    """2026-10-26, a Mac: `codex plugin list --json` timed out after 20 s right
    after the reinstall, and the update reported both plugins missing."""
    _codex_files(
        tmp_path, monkeypatch, {"probe-research-daemon": ["0.180.0"], "probe-research-tap": ["0.10.23"]}
    )
    monkeypatch.setattr(updater, "tracking_plugin_name", lambda source=None: "probe-research-daemon")
    _fake_codex(monkeypatch, {})
    monkeypatch.setattr(
        updater.plugin_cli, "list_plugins",
        lambda source: updater.claude_cli.Result(ok=False, detail="timed out after 20s", reachable=False),
    )

    res = updater.update_codex_plugins()

    assert res.confirmed, res.message
    assert res.list_unreadable  # the report still says the list could not be read
    assert "read from Codex's plugin files" in res.message and "timed out after 20s" in res.message
    assert res.tap_after == "0.10.23"


def test_codexs_files_missing_a_plugin_still_fail_the_update(tmp_path, monkeypatch):
    _codex_files(tmp_path, monkeypatch, {"probe-research": ["0.180.0"]})
    _fake_codex(monkeypatch, {"plugin list --json": _failed_with("boom")})
    res = updater.update_codex_plugins()
    assert not res.confirmed
    assert "could not be read after reinstalling (boom)" in res.message


def test_a_readable_list_is_believed_over_the_files(tmp_path, monkeypatch):
    _codex_files(tmp_path, monkeypatch, {"probe-research": ["0.180.0"], "probe-research-tap": ["0.10.23"]})
    listed = json.dumps({"installed": [{"name": "visualize", "version": "1"}]})
    _fake_codex(monkeypatch, {"plugin list --json": subprocess.CompletedProcess([], 0, stdout=listed, stderr="")})
    assert not updater.update_codex_plugins().confirmed


# -- the review's findings: nothing the old report showed may go missing ------


def test_a_deferred_update_is_no_agent_updated(one_update, monkeypatch):  # noqa: F811
    from probe.cli import autoupdate, run_lock, update_report

    monkeypatch.setattr(run_lock, "any_live", lambda: True)
    monkeypatch.setattr(autoupdate, "record_skip", lambda *a, **k: None)
    monkeypatch.setattr(update_report, "flush", lambda *a, **k: None)
    monkeypatch.delenv(upgrading.FORCED_ENV, raising=False)
    outcomes = upgrading.perform_updates(["claude_code", "codex"], base_url="https://x")
    assert all(outcome.deferred for outcome in outcomes.values())


def test_a_failed_pi_package_is_pis_own_failure_named_once(one_update, monkeypatch):  # noqa: F811
    monkeypatch.setattr(updater, "update_plugin", lambda *a: _plugin_result("claude_code"))
    said = "! not updated (npm refused); run `pi update git:github.com/prbe-ai/research-os-agent`"
    monkeypatch.setattr(
        upgrading, "_update_pi_package",
        lambda: upgrading._PiUpdate(["pi package:", f"  {said}"], ok=False, detail="npm refused", ran=True),
    )
    outcomes = upgrading.perform_updates(["claude_code", "pi"], base_url="https://x")
    failure = "pi's Probe package: not updated (npm refused); run `pi update git:github.com/prbe-ai/research-os-agent`"
    assert outcomes["pi"].problems == [failure]  # the command to run included
    assert outcomes["claude_code"].problems == []
    assert outcomes["claude_code"].run_notes == [failure]

    summary = RunSummary(SummaryAction.UPDATE, ["claude_code", "pi"])
    for source, outcome in outcomes.items():
        summary.note(*outcome.run_notes)
        summary.record(source, ok=not outcome.problems, notes=outcome.problems)
    lines = summary.lines()
    assert lines[0] == "Updated 1 of 2 coding agents"
    assert sum("npm refused" in line for line in lines) == 1


def test_pis_reload_instruction_reaches_the_summary(one_update, monkeypatch):  # noqa: F811
    monkeypatch.setattr(updater, "update_plugin", lambda *a: _plugin_result("claude_code"))
    reload = "Run /reload in open pi sessions (or restart them) to apply the update."
    monkeypatch.setattr(
        upgrading, "_update_pi_package",
        lambda: upgrading._PiUpdate(["pi package:"], ran=True, before="0.7.1", after="0.7.2", action=reload),
    )
    outcomes = upgrading.perform_updates(["claude_code", "pi"], base_url="https://x")
    assert outcomes["pi"].summary == "package 0.7.2 (updated)"
    # Something to do, not a failure: pi still counts as updated.
    assert outcomes["pi"].problems == [] and outcomes["pi"].actions == [reload]
    # An Update without pi still moves its package: the instruction is the run's.
    alone = upgrading.perform_updates(["claude_code"], base_url="https://x")
    assert alone["claude_code"].run_actions == [reload] and alone["claude_code"].run_notes == []


def test_a_skills_refresh_that_failed_is_a_detail(one_update, monkeypatch):  # noqa: F811
    monkeypatch.setattr(updater, "update_plugin", lambda *a: _plugin_result("claude_code"))
    monkeypatch.setattr(updater, "update_codex_plugins", lambda: _plugin_result("codex"))
    monkeypatch.setattr(
        upgrading.root_skills, "refresh",
        lambda source: ["! could not refresh the skills in ~/.claude/skills: permission denied"],
    )
    outcomes = upgrading.perform_updates(["claude_code"], base_url="https://x")
    assert any("permission denied" in problem for problem in outcomes["claude_code"].problems)


def test_an_empty_cache_folder_is_no_install(tmp_path, monkeypatch):
    _codex_files(tmp_path, monkeypatch, {"probe-research-daemon": ["0.180.0"], "probe-research-tap": []})
    empty = tmp_path / "codex" / "plugins" / "cache" / "research-os-agent" / "probe-research-tap" / "9.9.9"
    empty.mkdir(parents=True)
    assert codex_config.installed_plugin_versions("research-os-agent") == {"probe-research-daemon": "0.180.0"}


def test_a_failed_screen_keeps_its_errors_not_its_routine_report(monkeypatch):
    from probe.cli import tui

    monkeypatch.setattr(tui, "interactive", lambda: False)
    progress = tui.Progress("This run will:", ["sign in", "install"])
    progress.note(
        "Claude Code Session capture paired (device ?).",
        "browser approval failed: expired",
        "Revoke the key at https://x/settings.",
        "Status line: on.",
    )
    progress.finish(0, ok=False)
    assert progress.problems() == [
        "sign in: failed", "browser approval failed: expired", "Revoke the key at https://x/settings.",
    ]


def test_details_hold_errors_only_and_next_holds_one_restart_sentence():
    """2026-10-26: "for the details section we don't want any of the normal
    stuff, only errors and things that actually matter"."""
    summary = RunSummary(SummaryAction.INSTALL, ["claude_code", "codex", "kimi_code", "pi"])
    summary.record("claude_code", ok=True, restart=True)
    hooks = "approve Probe Session Capture under `/hooks` in its new session; until then capture sends nothing."
    summary.record("codex", ok=True, restart=True, must=[hooks])
    summary.record("kimi_code", ok=True, restart=True)
    summary.record("pi", ok=True, restart=True)
    lines = summary.lines()
    assert "Details:" not in lines
    assert lines[lines.index("Next:") + 1:] == [
        "  Restart Claude Code, Codex, Kimi Code and pi to load Probe.",
        f"  Codex: {hooks}",
    ]


def test_an_updates_next_line_offers_reload_where_it_works():
    summary = RunSummary(SummaryAction.UPDATE, ["claude_code", "kimi_code", "pi"])
    summary.record("claude_code", ok=True, restart=True)
    summary.record("kimi_code", ok=True, restart=True)
    summary.record("pi", ok=True)
    summary.must_do("Run /reload in open pi sessions (or restart them) to apply the update.")
    lines = summary.lines()
    assert lines[lines.index("Next:") + 1:] == [
        "  Restart Claude Code and /reload (or restart) Kimi Code to apply the update.",
        "  Run /reload in open pi sessions (or restart them) to apply the update.",
    ]


def test_routine_lines_are_not_errors():
    for routine in (
        "Status line: on.", "Auto-update on.", "Probe tracking rule added to ~/.claude/CLAUDE.md.",
        "Installed 15 skills in ~/.claude/skills.", "Codex MCP authorized from your Probe sign-in.",
        "No restart needed: open sessions pick up the new plugin at their next prompt.",
        "Refreshed the Probe block in ~/.claude/CLAUDE.md.",
    ):
        assert not wizard.needs_attention(routine), routine
    for error in (
        "! could not refresh the marketplace: offline", "Could not update ~/.codex/AGENTS.md",
        "browser approval failed: expired", "Not finished — no credential for: capture.",
        "the capture credential is rejected",
        # `_record_login_account`'s own wording: the command is its second sentence.
        "This wizard uses the account selected by the website code. "
        "Run `unset PROBE_TOKEN` in your shell before future Probe commands.",
        "Status line: not configured (~/.claude/settings.json is not valid JSON)",
    ):
        assert wizard.needs_attention(error), error


def test_a_codex_capture_install_needs_its_hook_approved(monkeypatch):
    from probe.cli.capabilities import Capabilities

    caps = Capabilities(agent_source="codex", codex_available=True)
    restart, must = wizard.install_next(caps, wizard.Selection(tracking=True, capture=True, auto_update=False, agent_rules=False))
    assert restart and must == [
        "approve Probe Session Capture under `/hooks` in its new session; until then capture sends nothing."
    ]
    claude = Capabilities(agent_source="claude_code", claude_available=True)
    assert wizard.install_next(claude, wizard.Selection(tracking=True, capture=True, auto_update=False, agent_rules=False)) == (True, [])


def test_turning_tracking_off_says_open_sessions_keep_it_until_they_restart():
    from probe.cli.capabilities import Capabilities

    caps = Capabilities(
        agent_source="claude_code", claude_available=True, tracking_plugin_installed=True, logged_in_as="r@x"
    )
    off = wizard.Selection(tracking=False, capture=False, auto_update=False, agent_rules=False)
    restart, must = wizard.install_next(caps, off)
    assert not restart and any("keep Probe until they restart" in line for line in must)
