"""Capy as a first-class coding agent in the installer (Richard 2026-10-12: "it
should be under the exact same ui and stuff as claude code, codex").

Capy is in the picker, `--agent capy` and the device summary like every other
agent, but nothing of Probe's installs into it: its install prints the steps
for its own settings and connects its thread capture, with the key and the
projects asked BEFORE anything is applied (Codex review O4)."""

from __future__ import annotations

import importlib
import os
from types import SimpleNamespace

import pytest

from capy_fake_api import ME, FakeCapy
from probe.cli import capy_cli
from probe.cli import capy_discovery as discovery
from probe.cli.capabilities import Capabilities


@pytest.fixture
def home(tmp_path, monkeypatch):
    monkeypatch.setenv("HOME", str(tmp_path))
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    monkeypatch.delenv(capy_cli.ENV_API_KEY, raising=False)
    monkeypatch.delenv("PROBE_AGENT", raising=False)
    # Which Capy steps print depends on the deployment: never a developer's.
    monkeypatch.delenv("PROBE_BASE_URL", raising=False)
    monkeypatch.delenv("PROBE_MCP_URL", raising=False)
    return tmp_path


@pytest.fixture
def run(home, monkeypatch):
    """The installer with every boundary faked: no plugin CLI may run, the
    browser approval and Capy's connect are recorded, and the registration
    says whether the install counts as complete."""
    from probe.cli import bootstrap, plugin_cli
    from probe.cli import doctor as doctor_impl
    from probe.cli import setup as wizard

    cli_main = importlib.import_module("probe.cli.main")
    seen: dict = {"authorize": [], "connect": [], "complete": []}

    def must_not_run(*args, **kwargs):
        raise AssertionError(f"reached the plugin CLI for Capy: {args}")

    for name in ("install", "uninstall", "add_marketplace", "refresh_marketplace", "list_plugins"):
        monkeypatch.setattr(plugin_cli, name, must_not_run)
    monkeypatch.setattr(bootstrap, "ensure_persistent_install", lambda **_: SimpleNamespace(message=""))
    monkeypatch.setattr(
        doctor_impl,
        "collect",
        lambda: Capabilities(agent_source="capy", logged_in_as="me@lab.example", mcp_token_held=True),
    )

    def authorize(grants, **kwargs):
        seen["authorize"].append((list(grants), kwargs.get("capture_sources")))
        return {grant: {} for grant in grants}, []

    monkeypatch.setattr(wizard, "authorize", authorize)
    monkeypatch.setattr(wizard, "revoke_replaced_token", lambda *a, **k: [])
    monkeypatch.setattr(wizard, "apply_auto_update", lambda want: [])

    def connect(plan, **kwargs):
        seen["connect"].append(plan)
        return capy_cli.Connected(config=None, team="team-a", mode=None, lines=["Connected as me@lab.example"])

    monkeypatch.setattr(capy_cli, "connect", connect)
    monkeypatch.setattr(
        cli_main, "_register_local_capabilities",
        lambda caps, settings=None, complete=True, alongside=(): seen["complete"].append(complete) or [],
    )

    def invoke(*argv, env=None):
        from typer.testing import CliRunner

        return CliRunner().invoke(cli_main.app, list(argv), env=env)

    return invoke, seen


def _trace(result) -> str:
    import traceback

    return "".join(traceback.format_exception(*result.exc_info)) if result.exc_info else ""


def test_agent_capy_installs_its_capture_with_no_plugin_and_prints_its_settings_steps(run, monkeypatch):
    invoke, seen = run
    with FakeCapy() as fake:
        monkeypatch.setenv(discovery.ENV_API_BASE, fake.base)
        result = invoke(
            "wizard", "--agent", "capy", "--action", "configure", "--yes", "--tracking", "--capture",
            "--capy-project", "ml-research",
            env={capy_cli.ENV_API_KEY: fake.key},
        )
    if result.exit_code:
        print(_trace(result))
    assert result.exit_code == 0, result.output
    [plan] = seen["connect"]
    assert [p["id"] for p in plan.projects] == ["proj_1"]
    assert fake.key not in result.output, "the Capy key is never printed"
    assert "From GitHub repository" in result.output and capy_cli.PLUGIN_URL in result.output, (
        "its plugin step prints"
    )
    assert f"{capy_cli.PLUGIN_URL}/skills" not in result.output
    assert seen["complete"] == [True]


def test_without_a_key_capy_is_reported_unfinished_and_nothing_is_paired(run):
    invoke, seen = run
    result = invoke("wizard", "--agent", "capy", "--action", "configure", "--yes", "--capture")
    assert result.exit_code == 1, "a script learns the install did not finish"
    assert capy_cli.ENV_API_KEY in result.output and "Not finished" in result.output
    assert seen["connect"] == []
    assert all("capture" not in grants for grants, _ in seen["authorize"]), "no credential for a connection that will not exist"
    assert seen["complete"] == [False]


def test_agent_capy_is_parsed_from_the_registry():
    cli_main = importlib.import_module("probe.cli.main")
    assert cli_main._installable_agent("capy").id == "capy"
    assert "capy" in cli_main._AGENT_FLAGS


def test_an_unattended_install_naming_no_agent_leaves_a_detected_capy_out(run, monkeypatch):
    """Capy found only by its app is not configured by a run nobody watches:
    its key is not there, and including it would leave every such install
    unfinished (and Claude Code's with it)."""
    from probe.cli import cloud_agents, plugin_cli

    invoke, seen = run
    monkeypatch.setattr(cloud_agents, "found_here", lambda source: True)
    monkeypatch.setattr(plugin_cli, "available", lambda source: False)
    result = invoke("wizard", "--action", "configure", "--yes")
    assert result.exit_code == 0, result.output
    assert seen["connect"] == [] and seen["complete"] and seen["complete"][-1] is True


def test_a_crashing_capy_connect_leaves_the_install_unfinished(run, monkeypatch):
    invoke, seen = run

    def crash(plan, **kwargs):
        raise OSError("disk full")

    monkeypatch.setattr(capy_cli, "connect", crash)
    with FakeCapy() as fake:
        monkeypatch.setenv(discovery.ENV_API_BASE, fake.base)
        result = invoke(
            "wizard", "--agent", "capy", "--action", "configure", "--yes", "--capture",
            "--capy-project", "ml-research", env={capy_cli.ENV_API_KEY: fake.key},
        )
    assert result.exit_code == 1 and seen["complete"] == [False]


def test_signing_in_never_pairs_or_moves_capy_capture(home, monkeypatch):
    """A sign-in (wizard entry, or another account) must not mint or re-pair
    Capy's credential: its connection names one person's threads in one team."""
    from probe.cli import setup as wizard

    asked: list = []

    def authorize(grants, **kwargs):
        asked.append(kwargs.get("capture_sources"))
        return {grant: {"token": "t"} for grant in grants}, []

    monkeypatch.setattr(wizard, "authorize", authorize)
    monkeypatch.setattr(wizard, "locally_paired_capture", lambda sources: list(sources))
    monkeypatch.setattr(wizard, "account_email", lambda base_url: None)
    wizard.sign_in(base_url="https://api.example", sources=("claude_code", "capy"), prepare_install=True)
    assert asked and all("capy" not in (sources or []) for sources in asked)


def test_capy_applies_before_a_local_agent_in_one_install(run, monkeypatch):
    """The server keeps one capabilities record per device and the last write
    wins: a local agent's real state reports last, never Capy's (it has no
    plugin here to report)."""
    from probe.cli import doctor as doctor_impl
    from probe.cli import plugin_cli

    invoke, seen = run
    cli_main = importlib.import_module("probe.cli.main")
    monkeypatch.setattr(plugin_cli, "available", lambda source: source == "claude_code")
    monkeypatch.setattr(
        doctor_impl, "collect",
        lambda: Capabilities(agent_source=os.environ.get("PROBE_AGENT") or "claude_code", logged_in_as="me@lab.example"),
    )
    capy_cli.save_config(capy_cli.CapyConfig(api_key="k", me_id=ME, me_email=None, projects=[]))
    applied: list = []
    monkeypatch.setattr(cli_main, "_run_wizard_action", lambda action, **kw: applied.append(kw["caps"].agent_source) or [])
    result = invoke("wizard", "--action", "configure", "--yes", "--no-capture")
    assert result.exit_code == 0, result.output
    assert applied == ["capy", "claude_code"]


def test_inside_capy_only_when_no_local_agent_claims_the_shell(monkeypatch):
    from probe.cli import capabilities
    from probe.harness import get_registry

    for harness in get_registry().all():
        for name in harness.detect_env:
            monkeypatch.delenv(name, raising=False)
    capy_marker = get_registry().get("capy").detect_env[-1]
    monkeypatch.setenv(capy_marker, "Capy <capy@capy.ai>")
    assert capabilities.cloud_agent_here().id == "capy"
    monkeypatch.setenv(get_registry().get("claude_code").detect_env[0], "1")
    assert capabilities.cloud_agent_here() is None, "Claude Code started from a Capy shell is Claude Code"


def test_update_and_capture_uninstall_take_capys_own_path(home, monkeypatch):
    from probe.cli import capture, upgrading, updater

    monkeypatch.setenv("PROBE_AGENT", "capy")
    for name in ("update_plugin", "update_codex_plugins", "update_kimi_plugins"):
        monkeypatch.setattr(updater, name, lambda *a, **k: pytest.fail("updated a plugin for Capy"))
    monkeypatch.setattr(upgrading, "_update_pi_package", lambda: upgrading._PiUpdate([], code=upgrading.update_report.PiStep.NOT_INSTALLED))
    monkeypatch.setattr(updater, "fetch_latest", lambda base: {})
    monkeypatch.setattr(updater, "detect_install", lambda: updater.Install(updater.Method.EDITABLE))
    monkeypatch.setattr(
        updater, "upgrade_cli",
        lambda i, c, t: updater.CliResult(ran=False, ok=True, changed=False, before=c, after=c, message="skipped"),
    )
    lines = upgrading.perform_update(base_url="https://api.example", include_plugin=True).lines
    assert any("updates itself" in line for line in lines)
    capy_cli.save_config(capy_cli.CapyConfig(api_key="k", me_id=ME, me_email=None, projects=[]))
    monkeypatch.setattr(capy_cli, "remove_timer", lambda mode: None)
    removed, warnings = capture._uninstall_plugin()
    assert removed and not warnings and capy_cli.load_config() is None


def test_the_manual_steps_sign_in_before_connecting_capy():
    from probe.cli import actions

    text = actions.manual_steps(base_url="https://api.research.prbe.ai", agent_source="capy")
    assert text.index("--action login") < text.index("probe capy connect")


def test_the_picker_finds_capy_by_its_app_or_its_connection(home, monkeypatch):
    from probe.cli import cloud_agents, plugin_cli
    from probe.cli import setup as wizard

    monkeypatch.setattr(plugin_cli, "available", lambda source: False)
    assert "capy" not in wizard.detectable_sources()
    monkeypatch.setattr(cloud_agents, "found_here", lambda source: True)
    assert "capy" in wizard.detectable_sources()
    monkeypatch.setattr(cloud_agents, "found_here", lambda source: False)
    capy_cli.save_config(capy_cli.CapyConfig(api_key="k", me_id=ME, me_email=None, projects=[]))
    assert "capy" in wizard.detectable_sources(), "a machine that captures Capy lists it"


def test_the_registry_finds_the_app_on_disk(home):
    from probe.harness import get_registry

    capy = get_registry().get("capy")
    assert not capy.found_on_disk(home)
    (home / "Library" / "Application Support" / "Capy").mkdir(parents=True)
    assert capy.found_on_disk(home)


def test_the_review_screen_says_what_capy_gets(home):
    from probe.cli import setup as wizard

    text = "\n".join(wizard.confirm_rows(("capy",)))
    assert "Copies the Capy threads you start every 10 minutes" in text
    assert "settings" in text and "Rules in your global" not in text, "no instruction file of Capy's here"
    mixed = "\n".join(wizard.confirm_rows(("claude_code", "capy")))
    assert "Sends this device's Claude Code sessions" in mixed
    assert "this device's Claude Code and Capy sessions" not in mixed
    assert "Rules in your global CLAUDE.md" in mixed


def test_doctor_update_and_uninstall_never_treat_capy_as_claude_code(home, monkeypatch):
    from probe.cli import actions, capabilities, doctor
    from probe.cli import setup as wizard

    monkeypatch.setenv("PROBE_AGENT", "capy")
    caps = doctor.collect()
    assert caps.agent_source == "capy" and caps.agent_version is None
    assert not caps.agent_rules_installed
    text = doctor.render(caps)
    assert "Claude Code" not in text and "Capy app" in text and "Thread capture" in text
    notes = " ".join(actions.troubleshooting(caps))
    assert "claude" not in notes.lower() and "MCP & plugins" in notes
    assert capabilities.installed_plugins(source="capy").names == frozenset()
    assert wizard.install_plugin("probe-research", source="capy").ok is False
    assert wizard.apply_agent_rules(True) == []

    capy_cli.save_config(capy_cli.CapyConfig(api_key="k", me_id=ME, me_email=None, projects=[]))
    monkeypatch.setattr(capy_cli, "remove_timer", lambda mode: None)
    lines = wizard.remove_everything(Capabilities(agent_source="capy"))
    assert capy_cli.load_config() is None and any("settings" in line for line in lines)
    assert "updates itself" in " ".join(wizard.agent_row_detail("update", "capy"))


def test_a_machine_whose_only_agent_is_capy_offers_capy_to_a_person(home):
    """The unattended exclusion never narrows what a person is offered: a Mac
    with only the Capy app installs Capy, not an absent Claude Code."""
    cli_main = importlib.import_module("probe.cli.main")
    assert cli_main._default_agents(("capy",), unattended=False) == ("capy",)
    assert cli_main._default_agents(("claude_code", "capy"), unattended=False) == ("claude_code", "capy")
    assert cli_main._default_agents(("claude_code", "capy"), unattended=True) == ("claude_code",)


def test_a_leftover_credential_file_is_not_a_connection(home):
    cli_main = importlib.import_module("probe.cli.main")
    capy_cli._private_dir(capy_cli.state_dir())
    (capy_cli.state_dir() / ".token").write_text("t\n")
    assert capy_cli.connected_here() and not cli_main._cloud_agent_connected("capy")
    capy_cli.save_config(capy_cli.CapyConfig(api_key="k", me_id=ME, me_email=None, projects=[]))
    assert cli_main._default_agents(("capy",), unattended=True) == ("capy",)


@pytest.mark.parametrize(("owner", "turned_off"), [("team-b", True), ("team-a", False), (capy_cli.UNREACHABLE, False)])
def test_signing_in_to_another_team_turns_capy_capture_off(home, monkeypatch, owner, turned_off):
    from probe.cli import capabilities

    capy_cli.save_config(capy_cli.CapyConfig(api_key="k", me_id=ME, me_email=None, projects=[]))
    monkeypatch.setattr(capabilities, "resolved_capture_credential", lambda s=None: ("t", "http://door"))
    monkeypatch.setattr(capy_cli, "_probe_account", lambda: {"customer_id": "team-a"})
    monkeypatch.setattr(capy_cli, "_capture_customer", lambda token, base: owner)
    lines = capy_cli.after_sign_in()
    assert capy_cli.killswitch_path().exists() is turned_off
    assert bool(lines) is turned_off and (not lines or "probe capy connect" in lines[0])


def test_connect_keeps_a_credential_the_server_could_not_check(home, monkeypatch):
    from probe.cli import capabilities
    from probe.cli import setup as wizard

    monkeypatch.setattr(capabilities, "resolved_capture_credential", lambda s=None: ("t", "http://door"))
    monkeypatch.setattr(capy_cli, "_probe_account", lambda: {"email": "me@lab.example", "customer_id": "team-a"})
    monkeypatch.setattr(capy_cli, "_capture_customer", lambda token, base: capy_cli.UNREACHABLE)
    monkeypatch.setattr(wizard, "authorize", lambda *a, **k: pytest.fail("asked for a new approval while offline"))
    plan = capy_cli.CapturePlan(key="k", projects=[{"id": "proj_1"}], users=[{"id": ME, "email": "me@lab.example"}])
    capy_cli.connect(plan, timer=False, first_sync=False)
    assert capy_cli.load_config() is not None


def test_a_refused_check_of_a_saved_connection_turns_capture_off(home, monkeypatch):
    capy_cli.save_config(capy_cli.CapyConfig(api_key="k", me_id=ME, me_email=None, projects=[{"id": "p"}]))

    def refuse(plan, **kwargs):
        raise capy_cli.EmailNotFound("No member of this Capy organization has the email other@x")

    monkeypatch.setattr(capy_cli, "connect", refuse)
    plan = capy_cli.CapturePlan(key="k", projects=[{"id": "p"}], users=[])
    outcome, _ = capy_cli.apply_capture(capy_cli.CaptureAsk(capy_cli.CaptureOutcome.ALREADY, plan=plan))
    assert outcome is capy_cli.CaptureOutcome.REFUSED and capy_cli.killswitch_path().exists()


def test_an_exported_capture_token_is_never_revoked(home, monkeypatch):
    from probe.cli import capabilities

    monkeypatch.setenv("PROBE_CAPY_TAP_TOKEN", "exported")
    monkeypatch.setattr(capabilities, "revoke_capture_device", lambda s=None: pytest.fail("revoked the user's token"))
    capy_cli._drop_credential()


def test_a_connected_machine_reuses_its_saved_key_for_new_projects(home, monkeypatch):
    with FakeCapy() as fake:
        monkeypatch.setenv(discovery.ENV_API_BASE, fake.base)
        capy_cli.save_config(capy_cli.CapyConfig(api_key=fake.key, me_id=ME, me_email=None, projects=[{"id": "proj_1"}]))
        ask = capy_cli.ask_capture(interactive=False, projects=["infra"])
    assert ask.outcome is capy_cli.CaptureOutcome.CONNECTED
    assert [p["id"] for p in ask.plan.projects] == ["proj_2"]


@pytest.mark.parametrize(("retryable", "expect"), [(False, None), (True, capy_cli.UNREACHABLE)])
def test_a_refused_credential_is_not_an_unreachable_server(monkeypatch, retryable, expect):
    """A 401/403 must force a fresh approval in `probe capy connect`; only a
    server that could not answer keeps the credential."""
    from probe.tap_core import session_journal

    def receipts(self, sid):
        raise session_journal.DeliveryPending("HTTP 401" if not retryable else "HTTP 503", retryable=retryable)

    monkeypatch.setattr(session_journal.Wire, "receipts", receipts)
    assert capy_cli._capture_customer("t", "http://door") == expect


def test_an_unreachable_check_never_lifts_an_another_account_stop(home, monkeypatch):
    from probe.cli import capabilities
    from probe.cli import setup as wizard

    approved: list = []
    monkeypatch.setattr(capabilities, "resolved_capture_credential", lambda s=None: ("t", "http://door"))
    monkeypatch.setattr(capy_cli, "_probe_account", lambda: {"email": "me@lab.example", "customer_id": "team-a"})
    monkeypatch.setattr(capy_cli, "_capture_customer", lambda token, base: capy_cli.UNREACHABLE)
    monkeypatch.setattr(wizard, "authorize", lambda *a, **k: approved.append(1) or (None, []))
    capy_cli._turn_off(capy_cli.ANOTHER_ACCOUNT)
    plan = capy_cli.CapturePlan(key="k", projects=[{"id": "proj_1"}], users=[{"id": ME, "email": "me@lab.example"}])
    capy_cli.connect(plan, timer=False, first_sync=False)
    assert approved == [1], "only a fresh approval for this account lifts it"
    capy_cli._turn_off(capy_cli.ANOTHER_ACCOUNT)
    outcome, lines = capy_cli.apply_capture(capy_cli.CaptureAsk(capy_cli.CaptureOutcome.ALREADY))
    assert outcome is capy_cli.CaptureOutcome.REFUSED and capy_cli.killswitch_path().exists()


def test_signing_back_in_to_the_owning_team_turns_capy_back_on(home, monkeypatch):
    from probe.cli import capabilities

    capy_cli.save_config(capy_cli.CapyConfig(api_key="k", me_id=ME, me_email=None, projects=[]))
    capy_cli._turn_off(capy_cli.ANOTHER_ACCOUNT)
    monkeypatch.setattr(capabilities, "resolved_capture_credential", lambda s=None: ("t", "http://door"))
    monkeypatch.setattr(capy_cli, "_probe_account", lambda: {"customer_id": "team-a"})
    monkeypatch.setattr(capy_cli, "_capture_customer", lambda token, base: "team-a")
    assert "back on" in capy_cli.after_sign_in()[0] and not capy_cli.killswitch_path().exists()
    capy_cli._turn_off("turned off by the installer")
    assert capy_cli.after_sign_in() == [] and capy_cli.killswitch_path().exists(), "a person's own off stays off"


def test_a_failed_sign_in_check_never_turns_a_saved_connection_off(home, monkeypatch):
    capy_cli.save_config(capy_cli.CapyConfig(api_key="k", me_id=ME, me_email=None, projects=[{"id": "p"}]))

    def refuse(plan, **kwargs):
        raise capy_cli.ConnectRefused("Sign in to Probe first (`probe login`): your Capy user is found by your Probe email.")

    monkeypatch.setattr(capy_cli, "connect", refuse)
    plan = capy_cli.CapturePlan(key="k", projects=[{"id": "p"}], users=[])
    outcome, _ = capy_cli.apply_capture(capy_cli.CaptureAsk(capy_cli.CaptureOutcome.ALREADY, plan=plan))
    assert outcome is capy_cli.CaptureOutcome.REFUSED and not capy_cli.killswitch_path().exists()


def test_every_sign_in_path_runs_the_capy_team_check(home, monkeypatch):
    from probe.cli import setup as wizard

    calls: list = []
    monkeypatch.setattr(capy_cli, "after_sign_in", lambda: calls.append(1) or ["checked"])
    monkeypatch.setattr(wizard, "authorize", lambda grants, **k: ({g: {"token": "t"} for g in grants}, []))
    monkeypatch.setattr(wizard, "account_email", lambda base_url: None)
    result = wizard.sign_in(base_url="https://api.example", sources=("claude_code",))
    assert calls and "checked" in result.lines


def test_an_interactive_install_shows_a_blocked_capy_even_beside_another_agent(monkeypatch):
    """Each agent's apply is told yes=True in a multi-agent run; the page reads
    the session's own answer from the completion."""
    from probe.cli import tui

    cli_main = importlib.import_module("probe.cli.main")
    pages: list = []
    monkeypatch.setattr(tui, "interactive", lambda: True)
    monkeypatch.setattr(tui, "page", lambda lines, prompt=None, **k: pages.append(list(lines)))
    progress = SimpleNamespace(note=lambda *a: None, note_next=lambda *a: None, close=lambda: None)
    completion = cli_main._InstallationCompletion(2, unattended=False)
    cli_main._finish_cloud_configure(
        capy_cli, selection=SimpleNamespace(tracking=True), outcome=capy_cli.CaptureOutcome.REFUSED,
        missing=[], incomplete=False, after=None, progress=progress, register=lambda after, complete: [],
        telemetry=SimpleNamespace(emit=lambda *a, **k: None), started=0.0, completion=completion,
        ask_on_screen=not completion.unattended,
    )
    assert pages and "not connected" in pages[0][0] and completion.cloud_blocked
