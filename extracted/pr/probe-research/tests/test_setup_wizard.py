"""`probe setup` / `probe doctor`: the flag contract and the off switch.

The two things most likely to hurt someone are covered first: an omitted flag
silently revoking capture in CI, and "off" that does not actually turn capture
off.
"""

from __future__ import annotations

import dataclasses
import json
import os
import sys
import time

import pytest

from probe.cli import autoupdate, capture
from probe.cli import capabilities as capabilities_mod
from probe.cli import doctor, pi_config, setup
from probe.cli.capabilities import (
    ENV_INGEST_TOKEN,
    Capabilities,
    Capability,
    TokenSource,
    capture_token_sources,
)


@pytest.fixture(autouse=True)
def isolate(tmp_path, monkeypatch):
    """Point every state path at a tmpdir so tests never touch a real install."""
    monkeypatch.setenv("PROBE_RESEARCH_TAP_PLUGIN_DIR", str(tmp_path / "tap"))
    monkeypatch.setenv("PROBE_CONFIG_PATH", str(tmp_path / "probe" / "config.json"))
    # BOTH conventions: the tap honours PROBE_CONFIG_PATH, the SDK honours
    # XDG_CONFIG_HOME. They agree in production (~/.config/probe/config.json);
    # a test that sets only one writes to the developer's REAL config.
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    # pi_config reads this for its own settings.json -- without it, any test
    # that reaches installed_plugins("pi")/install_plugin("pi")/etc. touches
    # the REAL ~/.pi/agent/settings.json on the machine running the suite.
    monkeypatch.setenv("PI_CODING_AGENT_DIR", str(tmp_path / "pi-agent"))
    monkeypatch.delenv("PROBE_AGENT", raising=False)
    monkeypatch.delenv("PROBE_TAP_SOURCE", raising=False)
    monkeypatch.delenv(ENV_INGEST_TOKEN, raising=False)
    (tmp_path / "tap").mkdir(parents=True, exist_ok=True)
    (tmp_path / "probe").mkdir(parents=True, exist_ok=True)
    # `turn_off` now tells the SERVER before it wipes the local credential, and
    # these fixtures write a real-looking base_url. Without this stub the suite
    # would POST to whatever host the test happens to name -- production, from
    # any machine with a network. Default to the offline answer (None); a test
    # that cares about the revoke overrides it explicitly.
    monkeypatch.setattr(capture, "revoke_capture_device", lambda *a, **k: None)
    monkeypatch.setattr(capabilities_mod, "verify_mcp_credential", lambda **_kwargs: True)
    # This suite exercises the install/menu decisions after account sign-in.
    # The browser-before-menu contract has its own test_wizard_auth_entry suite;
    # old interactive menu fixtures must never open a real authorization here.
    def signed_in(**kwargs):
        from probe.sdk.config import save_context

        save_context({"token": "probe_pat_menu_test"})
        return setup.SignInResult(ok=True, lines=[])

    monkeypatch.setattr(setup, "sign_in", signed_in)
    return tmp_path


def _caps(**overrides) -> Capabilities:
    return Capabilities(**overrides)


# --- the flag truth table --------------------------------------------------


def test_fresh_machine_defaults_everything_on():
    """A fresh machine gets every capability, capture included.

    This INVERTS the original default and the inversion is deliberate, so the
    assertion is kept rather than deleted: capture used to default off, and a
    silent flip back would be a privacy regression nobody would notice. What
    now carries the consent is the confirm screen -- a labelled bullet saying
    what capture sends and where, on screen before the Install keystroke, with
    the browser approval as the grant itself.
    """
    selection = setup.resolve_selection(
        _caps(), tracking=None, capture=None, auto_update=None, configured=False
    )
    assert selection.tracking is True
    assert selection.capture is True
    assert selection.auto_update is True
    assert selection.agent_rules is True


def test_the_capture_row_still_says_what_it_sends_and_where():
    """Load-bearing now that capture ships ticked. The row IS the disclosure --
    if it stops naming what leaves the machine, a pre-ticked box becomes a
    grant made in silence, which is the thing the default-off used to prevent."""
    _, detail = setup.menu_copy("codex")[Capability.CAPTURE]
    blob = " ".join(detail)
    assert "this device's" in blob
    assert "Codex sessions" in blob
    assert "Claude" not in blob


def test_wizard_copy_names_exactly_the_selected_agents():
    claude = " ".join(setup.menu_copy("claude_code")[Capability.CAPTURE][1])
    codex = " ".join(setup.menu_copy("codex")[Capability.CAPTURE][1])
    both = " ".join(setup.menu_copy(("claude_code", "codex"))[Capability.CAPTURE][1])

    assert "Claude Code sessions" in claude and "Codex" not in claude
    assert "Codex sessions" in codex and "Claude" not in codex
    assert "Claude Code and Codex sessions" in both
    assert "CLAUDE.md" in setup.menu_copy("claude_code")[Capability.AGENT_RULES][0]
    assert "AGENTS.md" in setup.menu_copy("codex")[Capability.AGENT_RULES][0]
    assert "search and track research" in " ".join(
        setup.menu_copy("codex")[Capability.AGENT_RULES][1]
    )


def test_menu_copy_and_agent_label_name_pi_rather_than_falling_through():
    """pi is a third capture source; both helpers used to know only two.
    `agent_label` used to fall through to the generic "coding agent" for
    anything that was not claude_code/codex, and a per-source message built
    from it would silently describe a pi grant as belonging to nobody named.
    """
    assert setup.agent_label("pi") == "pi"
    assert setup.agent_label(("claude_code", "pi")) == "Claude Code and pi"

    detail = " ".join(setup.menu_copy("pi")[Capability.CAPTURE][1])
    assert "this device's pi sessions" in detail
    assert "Claude" not in detail and "Codex" not in detail


def test_installable_agent_sources_includes_pi_via_pi_config_not_a_marketplace():
    """pi now has a real install path through this wizard -- pi_config's
    settings.json `packages` entry, not a marketplace plugin (see
    INSTALLABLE_AGENT_SOURCES' docstring) -- so it belongs in this tuple too.
    It must still be a real entry in AGENT_LABELS for every other helper
    (agent_label, menu_copy, authorize's confirmation message) that names a
    capture source rather than installs one -- unaffected by this change."""
    assert set(setup.INSTALLABLE_AGENT_SOURCES) == {"claude_code", "codex", "pi", "kimi_code"}
    assert setup.AGENT_LABELS["pi"] == "pi"
    assert setup.AGENT_LABELS["kimi_code"] == "Kimi Code"


def test_agent_row_detail_is_per_source_and_pi_does_not_claim_a_marketplace():
    """The step-1 row detail used to be one shared string, "Install plugins
    and pair source-bound capture." -- accurate for claude_code/codex, wrong
    for pi the moment pi could appear in this picker: pi's install is one
    settings.json entry, never a plugin marketplace."""
    assert set(setup.AGENT_ROW_DETAIL) == {"claude_code", "codex", "pi", "kimi_code"}
    assert setup.AGENT_ROW_DETAIL["claude_code"] == setup.AGENT_ROW_DETAIL["codex"]
    assert setup.AGENT_ROW_DETAIL["kimi_code"] == setup.AGENT_ROW_DETAIL["codex"]
    pi_detail = " ".join(setup.AGENT_ROW_DETAIL["pi"])
    assert "plugin" not in pi_detail.lower()
    assert "settings.json" in pi_detail


def test_detectable_sources_finds_pi_without_routing_through_plugin_cli(monkeypatch):
    """pi detection is `shutil.which("pi")`, never `plugin_cli.available`
    (which raises for pi -- see `plugin_cli.binary_name`'s docstring). The
    autouse `_no_ambient_pi_binary` fixture pins `pi_binary_available` off by
    default; this test flips it on explicitly to prove the wiring."""
    from probe.cli import plugin_cli

    monkeypatch.setattr(setup, "pi_binary_available", lambda: True)
    monkeypatch.setattr(plugin_cli, "available", lambda source: source == "claude_code")

    assert setup.detectable_sources() == ("claude_code", "pi")


def test_a_scripted_yes_can_still_decline_capture():
    """`--yes` has no screen, so it is the path the new default changes most.
    The flag has to remain a real off switch for anyone automating installs."""
    selection = setup.resolve_selection(
        _caps(), tracking=None, capture=False, auto_update=None, configured=False
    )
    assert selection.capture is False, "--no-capture must beat the default"


def test_rerun_preserves_capture_when_the_flag_is_omitted():
    """The load-bearing case: `probe setup --yes` in CI, or a re-run naming only
    one flag, must never silently revoke a developer's pairing."""
    configured = _caps(
        capture_token_sources=(TokenSource.PAIRED_FILE,),
        tracking_plugin_installed=True,
        logged_in_as="richard@prbe.ai",
    )
    assert configured.capture_on is True

    selection = setup.resolve_selection(configured, tracking=None, capture=None, auto_update=None)
    assert selection.capture is True, "an omitted flag must preserve, never disable"


def test_rerun_preserves_auto_update_when_the_flag_is_omitted():
    configured = _caps(auto_update_enabled=True, logged_in_as="richard@prbe.ai")
    selection = setup.resolve_selection(configured, tracking=None, capture=None, auto_update=None)
    assert selection.auto_update is True


def test_explicit_flags_always_win():
    configured = _caps(capture_token_sources=(TokenSource.PAIRED_FILE,))
    selection = setup.resolve_selection(
        configured, tracking=False, capture=False, auto_update=False
    )
    assert (selection.tracking, selection.capture, selection.auto_update) == (
        False,
        False,
        False,
    )


def test_capture_only_asks_for_capture_alone():
    """Someone who ticked only session capture must not be handed a
    read/write/delete PAT they never asked for."""
    grants = setup.grants_for(
        setup.Selection(tracking=False, capture=True, auto_update=False, agent_rules=False)
    )
    assert grants == ["capture"]


def test_tracking_asks_for_a_separate_read_only_mcp_credential():
    grants = setup.grants_for(
        setup.Selection(tracking=True, capture=True, auto_update=False, agent_rules=False)
    )
    assert grants == ["api", "mcp", "capture"]


# --- capture off is a verified postcondition -------------------------------


def test_off_clears_the_probe_config_token_not_just_the_paired_file(isolate):
    """The bug: the uploader also accepts `ingest_token` from the CLI config,
    which `probe login --ingest-token` writes. Clearing only `.token` lets
    capture resume at the next session start while the menu says it is off."""
    (isolate / "tap" / ".token").write_text("ros_ing_paired")
    (isolate / "probe" / "config.json").write_text(
        json.dumps({"base_url": "https://api.research.prbe.ai", "ingest_token": "ros_ing_cfg"})
    )
    assert set(capture_token_sources()) == {
        TokenSource.PAIRED_FILE,
        TokenSource.PROBE_CONFIG,
    }

    result = capture.turn_off(capture.OffMode.DISABLE)

    assert result.verified is True
    assert capture_token_sources() == ()
    # Unrelated config survives: this is an off switch, not a reset.
    surviving = json.loads((isolate / "probe" / "config.json").read_text())
    assert surviving["base_url"] == "https://api.research.prbe.ai"
    assert "ingest_token" not in surviving


def test_off_sets_the_killswitch_so_the_next_session_does_not_respawn(isolate):
    (isolate / "tap" / ".token").write_text("ros_ing_paired")
    capture.turn_off(capture.OffMode.DISABLE)
    assert (isolate / "tap" / ".disabled").exists()


def test_off_refuses_to_claim_success_while_the_env_var_is_set(isolate, monkeypatch):
    """The one source the wizard cannot fix -- it cannot unset a variable in the
    parent shell. Reporting "off" here would be exactly the lie this guards."""
    (isolate / "tap" / ".token").write_text("ros_ing_paired")
    monkeypatch.setenv(ENV_INGEST_TOKEN, "ros_ing_from_env")

    result = capture.turn_off(capture.OffMode.DISABLE)

    assert result.verified is False
    assert TokenSource.ENVIRONMENT in result.remaining
    assert any(ENV_INGEST_TOKEN in warning for warning in result.warnings)
    assert "NOT fully off" in result.summary()


def test_turning_capture_back_on_clears_the_killswitch(isolate):
    (isolate / "tap" / ".token").write_text("ros_ing_paired")
    capture.turn_off(capture.OffMode.DISABLE)
    assert (isolate / "tap" / ".disabled").exists()
    capture.clear_killswitch()
    assert not (isolate / "tap" / ".disabled").exists()


def _pi_marker(text: str):
    pi_dir = capabilities_mod.tap_plugin_dir("pi")
    pi_dir.mkdir(parents=True, exist_ok=True)
    marker = pi_dir / ".disabled"
    marker.write_text(text)
    return pi_dir, marker


def test_stray_pi_sign_in_marker_is_swept_when_pi_holds_no_token(isolate, monkeypatch):
    """D4: a pre-D3 sign-in left "Awaiting confirmation" in pi's folder with no
    pi token behind it. Nothing for that barrier to protect, so it goes."""
    monkeypatch.delenv("PROBE_PI_TAP_TOKEN", raising=False)
    (isolate / "probe" / "config.json").write_text(json.dumps({"ingest_token": "ros_ing_claude"}))
    _, marker = _pi_marker(capture.AWAITING_CONFIRMATION)

    assert capture.clear_stray_pi_killswitch() is True
    assert not marker.exists()


def test_pi_sign_in_marker_is_kept_while_pi_holds_an_unconfirmed_token(isolate, monkeypatch):
    """The same text is a real consent barrier when pi has a token the person
    has not confirmed yet: an installed hook must not upload with it."""
    monkeypatch.delenv("PROBE_PI_TAP_TOKEN", raising=False)
    pi_dir, marker = _pi_marker(capture.AWAITING_CONFIRMATION)
    (pi_dir / ".token").write_text("ros_ing_paired_pi")

    assert capture.clear_stray_pi_killswitch() is False
    assert marker.exists()


def test_a_deliberate_pi_off_is_never_swept(isolate, monkeypatch):
    monkeypatch.delenv("PROBE_PI_TAP_TOKEN", raising=False)
    _, marker = _pi_marker("disabled by the Probe Research wizard\n")

    assert capture.clear_stray_pi_killswitch() is False
    assert marker.exists()


def test_another_agents_sign_in_marker_is_never_swept(isolate, monkeypatch):
    """Only pi's folder is ever swept: Claude Code's and Codex's markers are
    consent barriers for tokens they really read."""
    monkeypatch.delenv("PROBE_PI_TAP_TOKEN", raising=False)
    cc_marker = capabilities_mod.tap_plugin_dir("claude_code") / ".disabled"
    cc_marker.parent.mkdir(parents=True, exist_ok=True)
    cc_marker.write_text(capture.AWAITING_CONFIRMATION)

    assert capture.clear_stray_pi_killswitch() is False
    assert cc_marker.exists()


def test_the_wizard_sweeps_the_stray_pi_marker_on_every_run(isolate, monkeypatch):
    """Wired at the top of `probe wizard`, before any action, so a machine
    that never touches pi in the wizard still gets pi capture back."""
    from typer.testing import CliRunner

    from probe.cli.main import app

    monkeypatch.delenv("PROBE_PI_TAP_TOKEN", raising=False)
    calls = []
    monkeypatch.setattr(capture, "clear_stray_pi_killswitch", lambda: calls.append(1) or True)

    CliRunner().invoke(app, ["wizard", "--who-records", "bogus"])

    assert calls == [1]


def test_killswitch_alone_means_capture_is_not_on(isolate):
    """A paired device with the killswitch set ships nothing, so the menu must
    not show capture as on."""
    caps = _caps(capture_token_sources=(TokenSource.PAIRED_FILE,), capture_killswitched=True)
    assert caps.capture_on is False


def test_rejected_capture_credential_is_not_treated_as_live():
    caps = _caps(
        capture_token_sources=(TokenSource.PAIRED_FILE,),
        capture_credential_valid=False,
    )
    assert caps.capture_on is False
    selection = setup.Selection(tracking=False, capture=True, auto_update=False, agent_rules=False)
    assert setup.needs_authorization(caps, selection) == ["capture"]


def test_doctor_explains_a_rejected_capture_credential():
    report = doctor.render(
        _caps(
            capture_token_sources=(TokenSource.PAIRED_FILE,),
            capture_credential_valid=False,
        )
    )
    assert "rejected" in report
    assert "probe wizard" in report


def test_capture_credential_probe_distinguishes_rejection_from_offline(isolate, monkeypatch):
    import urllib.error

    (isolate / "tap" / ".token").write_text("ros_ing_test")
    (isolate / "tap" / ".config").write_text(json.dumps({"api_base_url": "https://api.test"}))

    def rejected(*_args, **_kwargs):
        raise urllib.error.HTTPError("https://api.test", 401, "no", {}, None)

    _opener_opens(monkeypatch, rejected)
    assert capabilities_mod.verify_capture_credential() is False

    _opener_opens(
        monkeypatch,
        lambda *_args, **_kwargs: (_ for _ in ()).throw(urllib.error.URLError("offline")),
    )
    assert capabilities_mod.verify_capture_credential() is None


def _opener_opens(monkeypatch, open_):
    """Credential-bearing requests go through `_credential_opener()` (no
    redirects, the environment's proxies), not `urllib.request.urlopen`."""
    from types import SimpleNamespace

    monkeypatch.setattr(capabilities_mod, "_credential_opener", lambda: SimpleNamespace(open=open_))


# --- auto-update -----------------------------------------------------------


def test_auto_update_defaults_off_and_round_trips(isolate):
    assert autoupdate.load().enabled is False
    autoupdate.save(enabled=True)
    assert autoupdate.load().enabled is True


def test_a_channel_written_by_an_older_cli_is_ignored_not_rejected(isolate):
    """There is one channel. `stable` was stored, passed and validated, and read
    by nothing — but the state file is also read by the plugin hook, which can
    be older than the CLI, so an existing key must not break loading."""
    autoupdate.save(enabled=True)
    raw = json.loads(autoupdate.state_path().read_text())
    raw["channel"] = "stable"
    autoupdate.state_path().write_text(json.dumps(raw))

    assert autoupdate.load().enabled is True
    assert not hasattr(autoupdate.load(), "channel")
    assert not hasattr(autoupdate, "Channel")


def test_corrupt_state_reads_as_off_rather_than_guessing_on(isolate):
    autoupdate.state_dir().mkdir(parents=True, exist_ok=True)
    autoupdate.state_path().write_text("{not json")
    assert autoupdate.load().enabled is False


def test_last_attempt_is_recorded_so_a_silent_failure_is_visible(isolate):
    autoupdate.record_attempt(
        autoupdate.Attempt(at=1_700_000_000, ok=False, detail="network unreachable")
    )
    described = autoupdate.load().last_attempt.describe()
    assert "FAILED" in described
    assert "network unreachable" in described


def test_only_one_session_may_upgrade_at_a_time(isolate):
    """Several Claude Code sessions starting at once would otherwise each spawn
    `uv tool upgrade` against the same install."""
    assert autoupdate.acquire_lock() is True
    assert autoupdate.acquire_lock() is False
    autoupdate.release_lock()
    assert autoupdate.acquire_lock() is True


def test_a_stale_lock_does_not_wedge_auto_update_forever(isolate):
    assert autoupdate.acquire_lock() is True
    stale = autoupdate.lock_path()
    os.utime(stale, (0, 0))
    assert autoupdate.acquire_lock() is True


# --- the plan is printed before anything is touched ------------------------


def test_the_plan_survives_the_answer_every_fresh_machine_gives():
    """The exact crash: a fresh install answers "yes" to auto-update, the plan
    has to name a capability that is not a checkbox row, and the wizard died
    with a KeyError before it had installed anything. Fresh is the WORST case,
    not an edge one -- auto-update defaults on and starts off, so it changes
    state on every machine that has never been set up."""
    selection = setup.resolve_selection(
        _caps(), tracking=None, capture=None, auto_update=None, configured=False
    )
    steps = setup.plan(_caps(), selection)

    assert any("automatic updates" in step for step in steps)
    assert all(step.startswith(("enable ", "disable ")) for step in steps)


def test_every_capability_can_be_named_in_a_plan():
    """PLAN_LABELS must stay TOTAL over Capability. A partial map is what broke
    the wizard, and the failure landed at a user's terminal rather than in CI
    because nothing here asserted the mapping covered the enum."""
    assert set(setup.PLAN_LABELS) == set(Capability)


def test_the_plan_lists_only_what_actually_changes():
    """It is an audit trail, so a run that changes one thing must not claim to
    change three."""
    caps = _caps(
        tracking_plugin_installed=True,
        logged_in_as="richard@prbe.ai",
        auto_update_enabled=True,
    )
    steps = setup.plan(
        caps, setup.Selection(tracking=True, capture=True, auto_update=True, agent_rules=False)
    )

    assert len(steps) == 1
    assert steps[0].startswith("enable ")
    assert "capture" in steps[0].lower()


def test_no_change_means_no_plan():
    caps = _caps(
        tracking_plugin_installed=True,
        capture_plugin_installed=True,
        logged_in_as="richard@prbe.ai",
        capture_token_sources=(TokenSource.PAIRED_FILE,),
        auto_update_enabled=True,
    )
    selection = setup.Selection(tracking=True, capture=True, auto_update=True, agent_rules=False)
    assert setup.plan(caps, selection) == []


# --- doctor ----------------------------------------------------------------


def test_wizard_doctor_copies_all_selected_agents_and_troubleshooting(monkeypatch):
    from types import SimpleNamespace

    from typer.testing import CliRunner

    from probe.cli import actions, bootstrap, plugin_cli, tui
    from probe.cli.main import app

    monkeypatch.setattr(
        bootstrap, "ensure_persistent_install", lambda **_: SimpleNamespace(message=None)
    )
    monkeypatch.setattr(plugin_cli, "available", lambda source: source in ("claude_code", "codex"))
    monkeypatch.setattr(
        doctor, "collect", lambda: _caps(agent_source=os.environ.get("PROBE_AGENT", "claude_code"))
    )
    monkeypatch.setattr(setup, "interactive", lambda: True)
    monkeypatch.setattr(tui, "clear", lambda: None)
    choices = iter([actions.Action.DIAGNOSE, None])
    monkeypatch.setattr(setup, "run_action_menu", lambda caps: next(choices))
    monkeypatch.setattr(setup, "run_agent_menu", lambda *a, **k: ("claude_code", "codex"))
    pages = []

    def page(lines, prompt=None, *, copyable=False):
        pages.append(("\n".join(lines), copyable))
        return ""

    monkeypatch.setattr(tui, "page", page)
    result = CliRunner().invoke(app, ["wizard", "--agent", "both"])
    assert result.exit_code == 0, result.output
    assert len(pages) == 1
    report, copyable = pages[0]
    assert copyable is True
    assert "Claude Code:" in report and "Codex:" in report
    assert report.count("Probe Research doctor") == 2
    assert report.count("If something is not working:") == 2


def test_doctor_notices_codex_holding_a_token_this_device_replaced(monkeypatch, tmp_path):
    """The health check used to report a rotated credential as authenticated.
    `codex mcp list` says `bearer_token` for any header at all, so the only
    local signal is the value itself."""
    from probe.cli import codex_config
    from probe.sdk import config as sdk_config

    monkeypatch.setenv("CODEX_HOME", str(tmp_path))
    codex_config.write_mcp_bearer(
        "probe-research", url="https://mcp.research.prbe.ai/mcp", token="probe_pat_old"
    )

    monkeypatch.setattr(sdk_config, "load_context", lambda: {"mcp_token": "probe_pat_new"})
    stale = doctor.stale_codex_token_warning()
    assert stale and "older read token" in stale

    monkeypatch.setattr(sdk_config, "load_context", lambda: {"mcp_token": "probe_pat_old"})
    assert doctor.stale_codex_token_warning() is None


def test_doctor_stays_quiet_when_there_is_nothing_to_compare(monkeypatch, tmp_path):
    """No entry, or no stored token, is not evidence of drift."""
    from probe.cli import codex_config
    from probe.sdk import config as sdk_config

    monkeypatch.setenv("CODEX_HOME", str(tmp_path))
    monkeypatch.setattr(sdk_config, "load_context", lambda: {"mcp_token": "probe_pat_new"})
    assert doctor.stale_codex_token_warning() is None, "no Codex entry to be stale"

    codex_config.write_mcp_bearer(
        "probe-research", url="https://mcp.research.prbe.ai/mcp", token="probe_pat_old"
    )
    monkeypatch.setattr(sdk_config, "load_context", lambda: {})
    assert doctor.stale_codex_token_warning() is None, "no token held to compare against"


def test_doctor_checks_codex_drift_even_when_codex_is_not_the_selected_agent(
    isolate, monkeypatch, tmp_path
):
    """A machine with BOTH agents installed still reports ONE `agent_source`.
    The drift check used to sit inside `if selected_agent == "codex"`, so on
    exactly those machines it never ran: doctor printed "CLI + MCP: ok" while
    every Codex call 401'd against a token login had already released.

    `isolate` clears PROBE_AGENT, so `agent_source()` really does return
    claude_code here -- the devbox's configuration, not a mocked stand-in.
    """
    from probe.cli import codex_config

    codex_home = tmp_path / "codex"
    codex_home.mkdir(parents=True, exist_ok=True)
    monkeypatch.setenv("CODEX_HOME", str(codex_home))
    codex_config.write_mcp_bearer(
        "probe-research", url="https://mcp.research.prbe.ai/mcp", token="probe_pat_old"
    )
    # The one probe in collect() that would otherwise make a real request.
    monkeypatch.setattr(capabilities_mod, "verify_capture_credential", lambda *a, **k: None)
    monkeypatch.setattr(setup, "current_mcp_token", lambda: "probe_pat_new")

    caps = doctor.collect()

    assert capabilities_mod.agent_source() == "claude_code", "the case under test"
    assert any("older read token" in warning for warning in caps.warnings), (
        f"drift went unreported; warnings were {caps.warnings}"
    )


def test_doctor_names_every_credential_source_not_just_the_winning_one():
    """A user who believes capture is off deserves to see what is keeping it
    alive."""
    report = doctor.render(
        _caps(
            capture_token_sources=(TokenSource.PAIRED_FILE, TokenSource.ENVIRONMENT),
            capture_plugin_installed=True,
        )
    )
    assert "paired device token" in report
    assert ENV_INGEST_TOKEN in report


def test_doctor_names_pis_own_env_var_not_the_claude_code_one():
    """REGRESSION: `_SOURCE_LABEL[TokenSource.ENVIRONMENT]` was a single
    static string (`PROBE_INGEST_TOKEN environment variable`), with only a
    codex override on top -- so a pi device with `PROBE_PI_TAP_TOKEN` set in
    the shell had `probe doctor` tell it that `PROBE_INGEST_TOKEN` was the
    variable overriding its pairing, which is the wrong name to `unset`."""
    from probe.cli.capabilities import ENV_PI_INGEST_TOKEN

    report = doctor.render(
        _caps(
            agent_source="pi",
            capture_token_sources=(TokenSource.ENVIRONMENT,),
            capture_plugin_installed=True,
        )
    )
    assert ENV_PI_INGEST_TOKEN in report
    assert ENV_INGEST_TOKEN not in report


def test_turn_off_names_pis_own_env_var_in_the_cannot_unset_warning(isolate, monkeypatch):
    """Same bug, the `capture.turn_off()` copy of it: the "this process cannot
    unset it for you" warning named `PROBE_INGEST_TOKEN` for a pi device too."""
    from probe.cli.capabilities import ENV_PI_INGEST_TOKEN

    monkeypatch.setenv("PROBE_AGENT", "pi")
    monkeypatch.setenv(ENV_PI_INGEST_TOKEN, "ros_ing_pi_shell")

    result = capture.turn_off(capture.OffMode.DISABLE)

    assert any(ENV_PI_INGEST_TOKEN in w for w in result.warnings)
    assert not any(ENV_INGEST_TOKEN in w and ENV_PI_INGEST_TOKEN not in w for w in result.warnings)


def test_doctor_names_the_selected_agents_global_instructions():
    assert "Global CLAUDE.md" in doctor.render(_caps(agent_source="claude_code"))
    assert "Global AGENTS.md" in doctor.render(_caps(agent_source="codex"))


def test_doctor_reports_a_never_run_updater_distinctly_from_a_working_one():
    assert "never run on this device" in doctor.render(_caps())
    assert "FAILED" in doctor.render(_caps(last_update_attempt="FAILED (2026-07-24 10:00): boom"))


def test_doctor_renders_on_a_bare_machine_without_raising():
    # The command people run when everything is already broken.
    assert "Probe Research doctor" in doctor.render(_caps())


def test_doctor_reports_pi_honestly_instead_of_asking_claude_codes_binary():
    """Before this fix the Install/Agent-rules sections both defaulted a pi
    snapshot's `else` branch to Claude Code -- "Claude Code CLI: ok" and
    "Global CLAUDE.md" for a run that was never about Claude Code, sourced
    from `caps.claude_available`/`CLAUDE.md`'s path, neither of which this
    device's pi setup has any relationship to."""
    report = doctor.render(_caps(agent_source="pi"))
    assert "Claude Code CLI" not in report
    assert "Codex CLI" not in report
    assert "CLAUDE.md" not in report
    # "pi CLI", not "pi extension": this is the row that REPLACES the
    # "Claude Code CLI" line above, so it names the binary. The extension has
    # its own rows now (see `_pi_capture_rows`), and two rows sharing one
    # label read as a contradiction -- the first says doctor does not track
    # the extension, the second tracks it.
    assert "pi CLI" in report


def test_menu_rows_are_capabilities_not_plugin_names():
    """Nobody knows what `probe-research-tap` is; the consent decision is about
    what the thing does."""
    # AUTO_UPDATE is asked separately now: it is a policy about the
    # capabilities, not one of them.
    assert set(setup.MENU_COPY) == {
        Capability.TRACKING,
        Capability.CAPTURE,
        Capability.AGENT_RULES,
    }
    for title, detail in setup.MENU_COPY.values():
        assert "probe-research" not in title
        assert not any("probe-research" in line for line in detail)


def test_capture_menu_copy_is_scoped_to_this_device():
    """The picker says WHAT and WHERE, in one line.

    The full disclosure -- prompts, file contents, tool output, server-side
    secret stripping -- lives on the BROWSER APPROVAL screen, which is where
    the grant is actually made and where research-os asserts it verbatim.
    Repeating three lines of it here made the shortest menu in the product the
    densest thing to read.
    """
    _, detail = setup.menu_copy(("claude_code", "codex"))[Capability.CAPTURE]
    blob = " ".join(detail)
    assert "this device's" in blob, "scope must be explicit"
    assert "Claude Code and Codex sessions" in blob
    # One line, not a wall.
    assert len(detail) == 1


# --- fixes from the adversarial review ------------------------------------


def test_config_credentials_read_the_active_context_like_the_uploader(isolate):
    """The uploader reads contexts[current_context] and does NOT fall back to
    the top level. Reading only the top level would miss the credential on every
    modern config, so teardown would clear nothing and still report success."""
    from probe.cli.capabilities import probe_config_credentials

    (isolate / "probe" / "config.json").write_text(
        json.dumps(
            {
                "ingest_token": "ros_ing_v1_should_be_ignored",
                "current_context": "work",
                "contexts": {
                    "work": {"ingest_token": "ros_ing_active"},
                    "other": {"ingest_token": "ros_ing_inactive"},
                },
            }
        )
    )
    assert probe_config_credentials()["ingest_token"] == "ros_ing_active"
    assert TokenSource.PROBE_CONFIG in capture_token_sources()


def test_off_clears_a_context_scoped_token_and_verifies(isolate):
    (isolate / "probe" / "config.json").write_text(
        json.dumps(
            {
                "current_context": "work",
                "contexts": {"work": {"ingest_token": "ros_ing_active"}},
            }
        )
    )
    assert TokenSource.PROBE_CONFIG in capture_token_sources()
    result = capture.turn_off(capture.OffMode.DISABLE)
    assert result.verified is True
    assert capture_token_sources() == ()


# --- an uninstall only uninstalls the coding agents we select --------------
#
# The probe-config `ingest_token` sits in a machine-wide file. Clearing it the
# moment any one source ran `turn_off` once broke Claude Code capture from a pi
# uninstall (proven live 2026-08-28, project note 18). Since D3 only Claude
# Code reads that token (`consumes_cli_capture_token`), so pi and Codex never
# touch it, and Claude Code turning off has no other reader to keep it for.


def test_off_preserves_the_shared_config_token_when_another_source_still_has_capture(
    isolate, monkeypatch
):
    """pi turning its own capture off must not strand Claude Code's, which
    reads the probe-config `ingest_token`. pi never reads it (D3), so its
    teardown leaves it alone without needing to "preserve" anything."""
    monkeypatch.setenv("PROBE_AGENT", "pi")
    (isolate / "probe" / "config.json").write_text(
        json.dumps(
            {
                "current_context": "work",
                "contexts": {
                    "work": {"ingest_token": "ros_ing_work"},
                    "other": {"ingest_token": "ros_ing_other"},
                },
            }
        )
    )
    pi_dir = capabilities_mod.tap_plugin_dir("pi")
    pi_dir.mkdir(parents=True, exist_ok=True)
    (pi_dir / ".token").write_text("ros_ing_paired_pi")
    monkeypatch.setattr(
        capture,
        "installed_plugins",
        lambda source=None: capabilities_mod.PluginState(
            names=(
                frozenset({capabilities_mod.TAP_PLUGIN_NAME})
                if source == "claude_code"
                else frozenset()
            ),
            verified=True,
        ),
    )

    result = capture.turn_off(capture.OffMode.DISABLE)

    assert result.verified is True
    assert result.preserved_for == []
    assert result.summary() == (
        "Session capture is off for pi: none of its credentials resolves on this device."
    )

    # The shared credential survives -- top level AND every context.
    surviving = json.loads((isolate / "probe" / "config.json").read_text())
    assert surviving["contexts"]["work"]["ingest_token"] == "ros_ing_work"
    assert surviving["contexts"]["other"]["ingest_token"] == "ros_ing_other"

    # pi's own, source-scoped teardown still ran in full: paired token gone,
    # killswitch set.
    assert not (pi_dir / ".token").exists()
    assert (pi_dir / ".disabled").exists()


def test_off_for_pi_never_clears_claude_codes_config_token(isolate, monkeypatch):
    """Even with no other source installed, pi turning its own capture off
    leaves the probe-config `ingest_token` alone: it is Claude Code's capture
    token, which pi never reads (D3). pi's own teardown still runs in full."""
    monkeypatch.setenv("PROBE_AGENT", "pi")
    (isolate / "probe" / "config.json").write_text(
        json.dumps(
            {
                "current_context": "work",
                "contexts": {"work": {"ingest_token": "ros_ing_work"}},
            }
        )
    )
    pi_dir = capabilities_mod.tap_plugin_dir("pi")
    pi_dir.mkdir(parents=True, exist_ok=True)
    (pi_dir / ".token").write_text("ros_ing_paired_pi")
    monkeypatch.setattr(
        capture,
        "installed_plugins",
        lambda source=None: capabilities_mod.PluginState(verified=True),
    )

    result = capture.turn_off(capture.OffMode.DISABLE)

    assert result.verified is True
    assert result.preserved_for == []
    assert result.summary() == (
        "Session capture is off for pi: none of its credentials resolves on this device."
    )

    surviving = json.loads((isolate / "probe" / "config.json").read_text())
    assert surviving["contexts"]["work"]["ingest_token"] == "ros_ing_work"
    assert not (pi_dir / ".token").exists()
    assert (pi_dir / ".disabled").exists()


def test_off_for_claude_code_clears_the_config_token_even_with_pi_installed(isolate, monkeypatch):
    """pi no longer reads the probe-config `ingest_token` (D3), so Claude Code
    turning its own capture off is the last reader out and clears it, even
    while pi's package is installed."""
    from probe.cli import pi_config

    (isolate / "probe" / "config.json").write_text(
        json.dumps({"base_url": "https://api.research.prbe.ai", "ingest_token": "ros_ing_cfg"})
    )
    (isolate / "tap" / ".token").write_text("ros_ing_paired_claude")
    monkeypatch.setattr(
        capture,
        "installed_plugins",
        lambda source=None: capabilities_mod.PluginState(verified=True),
    )
    monkeypatch.setattr(pi_config, "package_entry_installed", lambda *a, **kw: True)

    result = capture.turn_off(capture.OffMode.DISABLE)

    assert result.verified is True
    assert result.preserved_for == []
    assert result.summary() == (
        "Session capture is off for Claude Code: none of its credentials resolves on this device."
    )

    surviving = json.loads((isolate / "probe" / "config.json").read_text())
    assert "ingest_token" not in surviving
    assert not (isolate / "tap" / ".token").exists()
    assert (isolate / "tap" / ".disabled").exists()


def test_only_claude_code_falls_back_to_the_probe_config_token(isolate):
    """The probe CLI config's `ingest_token` is Claude Code's capture token;
    the server refuses it on pi's and Codex's routes (D3). Mirrors
    tap/config.py::load_token() and pairing.ts, which make the same cut."""
    (isolate / "probe" / "config.json").write_text(json.dumps({"ingest_token": "ros_ing_cfg"}))
    assert TokenSource.PROBE_CONFIG in capture_token_sources("claude_code")
    assert TokenSource.PROBE_CONFIG not in capture_token_sources("pi")
    assert TokenSource.PROBE_CONFIG not in capture_token_sources("codex")
    assert capabilities_mod.resolved_capture_credential("pi") is None


def test_capture_token_sources_reads_the_pi_specific_env_var(isolate, monkeypatch):
    monkeypatch.setenv("PROBE_PI_TAP_TOKEN", "ros_ing_pi_env")
    assert TokenSource.ENVIRONMENT in capture_token_sources("pi")
    # The claude_code/codex env vars must not cross-satisfy pi's check.
    monkeypatch.delenv("PROBE_PI_TAP_TOKEN")
    assert TokenSource.ENVIRONMENT not in capture_token_sources("pi")


def test_tap_plugin_dir_resolves_pis_own_state_root(isolate, monkeypatch):
    """Mirrors tap/sources.py::plugin_state_dir()'s pi row: pi lives under
    ~/.pi/agent/state, not ~/.claude/plugins (claude_code's default) and not
    ~/.codex/state (codex's) -- a wizard that assumed otherwise would write a
    paired token to a path pi's own daemon never reads."""
    monkeypatch.delenv("PROBE_PI_TAP_PLUGIN_DIR", raising=False)
    monkeypatch.setattr(capabilities_mod.Path, "home", lambda: isolate)
    resolved = capabilities_mod.tap_plugin_dir("pi")
    assert resolved == isolate / ".pi" / "agent" / "state" / "probe-research-tap"


def test_tap_plugin_dir_honours_the_pi_env_override(isolate, tmp_path, monkeypatch):
    override = tmp_path / "custom-pi-state"
    monkeypatch.setenv("PROBE_PI_TAP_PLUGIN_DIR", str(override))
    assert capabilities_mod.tap_plugin_dir("pi") == override


def test_every_non_default_tap_source_has_a_capabilities_env_mirror():
    """The exhaustiveness tripwire for harness #4: fail here, at test time,
    not only at runtime.

    capabilities.py's `_TAP_TOKEN_ENV_BY_SOURCE` / `_TAP_PLUGIN_DIR_ENV_BY_SOURCE`
    hand-mirror tap/sources.py's `token_env`/`plugin_dir_env` columns, and can
    only hand-mirror them: this package cannot import the tap plugin package
    (see the comment above those two dicts in capabilities.py). A source
    added to tap/sources.py with no matching row here does not raise -- it
    silently inherits claude_code's env var and plugin dir from
    `tap_token_env()`/`tap_plugin_dir()`'s own fallback, which is the exact
    "everything that is not codex is Claude Code" shape this whole audit is
    about, just one level up from any single call site. Mirrors
    prbe-knowledge's `test_all_sources_classified`: diff the two tables and
    fail closed on any gap, the moment the diff exists rather than whenever
    someone next reads doctor's output for the new harness.
    """
    import sys
    from pathlib import Path

    tap_root = Path(__file__).resolve().parents[1] / "plugins" / "probe-research-tap"
    assert tap_root.is_dir(), f"tap checkout not found at {tap_root}"
    if str(tap_root) not in sys.path:
        sys.path.insert(0, str(tap_root))
    import tap.sources as tap_sources

    non_default = {
        source_id for source_id in tap_sources.SOURCES if source_id != tap_sources.DEFAULT_SOURCE_ID
    }
    missing_token = non_default - set(capabilities_mod._TAP_TOKEN_ENV_BY_SOURCE)
    missing_dir = non_default - set(capabilities_mod._TAP_PLUGIN_DIR_ENV_BY_SOURCE)
    assert not missing_token, f"no capabilities.py token-env mirror for: {missing_token}"
    assert not missing_dir, f"no capabilities.py plugin-dir mirror for: {missing_dir}"


def test_off_is_not_verified_when_the_killswitch_could_not_be_written(isolate, monkeypatch):
    """Credentials gone is not enough: without the killswitch the next session
    respawns the uploader."""
    monkeypatch.setattr(capture, "_set_killswitch", lambda: False)
    result = capture.turn_off(capture.OffMode.DISABLE)
    assert result.verified is False
    assert "killswitch not set" in result.summary()


def test_off_is_not_verified_while_an_uploader_survives(isolate, monkeypatch):
    """A daemon that ignored SIGTERM still holds its bearer and its queue."""
    monkeypatch.setattr(capture, "_stop_daemon", lambda: (False, ["still running"]))
    result = capture.turn_off(capture.OffMode.DISABLE)
    assert result.verified is False
    assert "uploader still running" in result.summary()


def test_a_planted_pid_file_cannot_get_an_unrelated_process_killed(isolate, monkeypatch):
    """/tmp is world-writable, so the PID files there are untrusted input."""
    pid_dir = isolate / "pids"
    pid_dir.mkdir()
    (pid_dir / "probe-research-tap-watcher-planted.pid").write_text(str(os.getpid()))
    monkeypatch.setenv(capture.PID_DIR_ENV, str(pid_dir))
    killed: list[int] = []
    asked: list[int] = []
    monkeypatch.setattr(capture.os, "kill", lambda pid, sig: killed.append(pid))
    monkeypatch.setattr(capture, "_looks_like_the_uploader", lambda pid: asked.append(pid) or False)
    capture._stop_daemon()
    assert asked == [os.getpid()], "never reached the planted file"
    assert killed == [], "signalled a process that is not the uploader"


def test_the_suite_never_aims_stop_daemon_at_the_real_pid_dir(monkeypatch):
    """Every session's uploader has its pid file in /tmp; a test reaching it
    kills them all (conftest's `_no_real_capture_daemon_kill`)."""
    assert capture._pid_dir() != "/tmp"
    monkeypatch.delenv(capture.PID_DIR_ENV)
    assert capture._pid_dir() == "/tmp"


# --- stop-daemon forensics --------------------------------------------------
#
# The tap's third failure mode: a daemon found SIGTERM'd, pid file unlinked, no
# shutdown sentinel — a signature only _stop_daemon() produces, with no caller
# ever caught in the act. macOS cannot expose the signal sender to the dying
# process, so the KILLER journals every invocation, and these tests pin that
# journal down. The break-the-code companion proves the file-content assertion
# can actually fail (a forensic test that cannot fail certifies its own rot).

_FAKE_DAEMON_PID = 43210


def _stop_one_fake_daemon(tmp_path, monkeypatch) -> str:
    """Drive _stop_daemon() at a single fabricated pid file; return its path.

    The glob seam is patched so nothing under the real /tmp is ever touched,
    and os.kill is faked so no signal leaves the test: SIGTERM is swallowed and
    the liveness poll (signal 0) reports the process already gone.
    """
    import glob as glob_mod

    pid_file = tmp_path / f"probe-research-tap-watcher-{_FAKE_DAEMON_PID}.pid"
    pid_file.write_text(str(_FAKE_DAEMON_PID))
    monkeypatch.setattr(glob_mod, "glob", lambda _pattern: [str(pid_file)])
    monkeypatch.setattr(capture, "_looks_like_the_uploader", lambda _pid: True)

    def _fake_kill(pid: int, sig: int) -> None:
        assert pid == _FAKE_DAEMON_PID, "signalled a pid the test did not plant"
        if sig == 0:
            raise ProcessLookupError  # already exited — the desired state

    monkeypatch.setattr(capture.os, "kill", _fake_kill)

    stopped, warnings = capture._stop_daemon()
    assert stopped is True
    assert warnings == []
    return str(pid_file)


def test_stop_daemon_journals_the_kill_it_is_about_to_send(isolate, monkeypatch):
    """ts + own pid + own argv + each signalled pid land in the state-dir
    journal — asserted against the REAL file, not a mock, so silencing the
    logger fails this test (see the companion below)."""
    pid_file = _stop_one_fake_daemon(isolate, monkeypatch)

    journal = isolate / "tap" / "logs" / "stop-daemon.jsonl"
    assert journal == capture.stop_log_path()
    record = json.loads(journal.read_text(encoding="utf-8").strip().splitlines()[-1])
    assert record["pid"] == os.getpid()
    assert record["argv"] == list(sys.argv)
    assert record["signalled"] == [{"pid": _FAKE_DAEMON_PID, "pid_file": pid_file}]
    assert abs(record["ts"] - time.time()) < 60


def test_the_journal_assertion_really_depends_on_the_logger(isolate, monkeypatch):
    """BREAK-THE-CODE proof for the test above: with the logger silenced, the
    journal never materialises — so the file-content assertion CAN fail, and a
    future regression that unhooks the journal will be caught, not certified."""
    monkeypatch.setattr(capture, "_append_stop_log", lambda _record: None)
    _stop_one_fake_daemon(isolate, monkeypatch)
    assert not capture.stop_log_path().exists()


def test_a_broken_journal_never_blocks_the_stop(isolate, monkeypatch):
    """Forensics are strictly best-effort: a raising logger must not prevent or
    delay the stop, and the pid file is still cleaned up."""

    def _boom(_record: dict) -> None:
        raise RuntimeError("disk full")

    monkeypatch.setattr(capture, "_append_stop_log", _boom)
    pid_file = _stop_one_fake_daemon(isolate, monkeypatch)  # asserts stopped is True
    assert not os.path.exists(pid_file), "pid file should be unlinked despite the broken journal"


def test_doctor_surfaces_the_newest_stop_event(isolate):
    """`probe doctor` renders the LAST journal entry, so a "transcripts
    missing" report carries its own cause without anyone digging up the file."""
    capture._append_stop_log({"ts": 1700000000, "pid": 1, "argv": ["old"], "signalled": []})
    capture._append_stop_log(
        {
            "ts": 1755086400,
            "pid": 4242,
            "argv": ["probe", "wizard"],
            "signalled": [{"pid": 999, "pid_file": "/tmp/probe-research-tap-watcher-x.pid"}],
        }
    )
    described = capture.describe_last_stop()
    assert described is not None
    assert "probe wizard" in described
    assert "4242" in described
    assert "1 daemon signalled" in described
    assert "old" not in described, "must render the newest entry, not the first"

    rendered = doctor.render(_caps(capture_last_stop=described))
    assert "Last daemon stop" in rendered
    assert described in rendered
    assert "Last daemon stop" not in doctor.render(_caps())


def test_a_missing_or_garbled_journal_reads_as_no_event(isolate):
    assert capture.last_stop_event() is None
    capture.stop_log_path().parent.mkdir(parents=True, exist_ok=True)
    capture.stop_log_path().write_text("not json\n{broken\n", encoding="utf-8")
    assert capture.last_stop_event() is None
    assert capture.describe_last_stop() is None


def test_the_journal_is_bounded(isolate):
    """Crude rotation: past the size cap, only the newest lines survive."""
    entry = {"ts": 1700000000, "pid": 1, "argv": ["x" * 200], "signalled": []}
    for index in range(2000):
        entry["pid"] = index
        capture._append_stop_log(entry)
    assert capture.stop_log_path().stat().st_size < capture._STOP_LOG_MAX_BYTES + 65536
    lines = capture.stop_log_path().read_text(encoding="utf-8").splitlines()
    assert json.loads(lines[-1])["pid"] == 1999, "rotation must keep the newest entries"


def test_an_all_off_install_is_not_mistaken_for_a_fresh_machine():
    """Someone who ran setup and turned everything off has still configured this
    machine. Treating it as fresh lets `--yes` switch things back on."""
    all_off = _caps(capture_plugin_installed=True)
    assert all_off.enabled() == {
        Capability.TRACKING: False,
        Capability.CAPTURE: False,
        Capability.AUTO_UPDATE: False,
        Capability.AGENT_RULES: False,
    }
    assert all_off.configured is True

    selection = setup.resolve_selection(all_off, tracking=None, capture=None, auto_update=None)
    assert selection.tracking is False
    assert selection.auto_update is False


def test_a_genuinely_fresh_machine_still_gets_defaults():
    fresh = _caps()
    assert fresh.configured is False
    selection = setup.resolve_selection(fresh, tracking=None, capture=None, auto_update=None)
    assert selection.tracking is True
    assert selection.auto_update is True


def test_legacy_codex_tap_counts_as_an_existing_configuration():
    assert _caps(legacy_capture_plugin_installed=True).configured is True


# --- the pieces that make it actually work --------------------------------


def test_setup_requests_only_the_grants_it_still_needs():
    """A re-run where everything already works must not drag the user through
    another browser approval."""
    fully_set_up = _caps(
        tracking_plugin_installed=True,
        logged_in_as="richard@prbe.ai",
        mcp_token_held=True,
        capture_token_sources=(TokenSource.PAIRED_FILE,),
    )
    everything = setup.Selection(tracking=True, capture=True, auto_update=True, agent_rules=False)
    assert setup.needs_authorization(fully_set_up, everything) == []

    # Logged in, but capture was never paired: ask for capture ALONE.
    tracking_only = _caps(tracking_plugin_installed=True, logged_in_as="richard@prbe.ai", mcp_token_held=True)
    assert setup.needs_authorization(tracking_only, everything) == ["capture"]

    # Signed in with a pasted token (`probe wizard --action login --token`):
    # that minted no MCP token, so Install asks for it (R11).
    pasted = _caps(logged_in_as="richard@prbe.ai", capture_token_sources=(TokenSource.PAIRED_FILE,))
    assert setup.needs_authorization(pasted, everything) == ["mcp"]
    # Headless, that alone never holds the install on a browser nobody watches.
    assert setup.headless_needs(setup.needs_authorization(pasted, everything)) == []
    assert setup.headless_needs(setup.needs_authorization(_caps(), everything)) == ["api", "mcp", "capture"]

    # Nothing yet: ask for all three in one approval.
    assert setup.needs_authorization(_caps(), everything) == ["api", "mcp", "capture"]


def _no_reuse(monkeypatch):
    """Force the OAuth fallback: no read token means no shortcut to take."""
    from probe.cli import codex_config

    monkeypatch.setattr(codex_config, "plugin_mcp_url", lambda _name, **_kw: None)


def test_the_browser_approval_already_held_authorizes_the_codex_mcp(monkeypatch, tmp_path):
    """One approval, both agents. The run that gets here has just minted an
    `mcp` read token (grants_for asks for `api` and `mcp` together), and Codex
    accepts a static Authorization header on a user-level entry — so sending the
    user to a second page to mint a second token buys nothing, and it is the
    step that times out. `codex mcp login` must not be reached at all."""
    from probe.cli import codex_config, plugin_cli
    from probe.sdk import config as sdk_config

    monkeypatch.setenv("CODEX_HOME", str(tmp_path))
    monkeypatch.setattr(sdk_config, "load_context", lambda: {"mcp_token": "probe_pat_from_signin"})
    monkeypatch.setattr(
        codex_config, "plugin_mcp_url", lambda _name, **_kw: "https://mcp.research.prbe.ai/mcp"
    )
    statuses = iter(["not_logged_in", "bearer_token"])
    monkeypatch.setattr(plugin_cli, "codex_mcp_auth_status", lambda _name: next(statuses))

    def _must_not_run(_name):
        raise AssertionError("a second browser approval was requested")

    monkeypatch.setattr(plugin_cli, "login_codex_mcp", _must_not_run)

    assert setup.apply_codex_mcp_auth() == ["Codex MCP authorized from your Probe sign-in."]

    written = (tmp_path / "config.toml").read_text(encoding="utf-8")
    assert "Bearer probe_pat_from_signin" in written
    assert "bearer_token =" not in written  # the key that stops Codex booting


def test_a_codex_config_we_cannot_confirm_is_put_back_exactly_as_it_was(monkeypatch, tmp_path):
    """Falling back is not enough when the write itself may be the problem.

    `codex mcp list` failing is indistinguishable from a config Codex cannot
    load, and that state does not end when this command does -- every codex
    invocation is down until someone edits the file. So an unconfirmed write is
    reverted before the OAuth fallback runs, rather than left underneath it.
    """
    from probe.cli import claude_cli, codex_config, plugin_cli
    from probe.sdk import config as sdk_config

    monkeypatch.setenv("CODEX_HOME", str(tmp_path))
    before = 'model = "gpt-5.6"\n\n[tui]\ntheme = "dark"\n'
    (tmp_path / "config.toml").write_text(before, encoding="utf-8")

    monkeypatch.setattr(sdk_config, "load_context", lambda: {"mcp_token": "probe_pat_from_signin"})
    monkeypatch.setattr(
        codex_config, "plugin_mcp_url", lambda _name, **_kw: "https://mcp.research.prbe.ai/mcp"
    )
    # `not_logged_in` first (so the shortcut is attempted), then None -- what a
    # config Codex refuses to load actually looks like from here.
    statuses = iter(["not_logged_in", None, "o_auth"])
    monkeypatch.setattr(plugin_cli, "codex_mcp_auth_status", lambda _name: next(statuses))
    monkeypatch.setattr(
        plugin_cli,
        "login_codex_mcp",
        lambda _name: claude_cli.Result(ok=True, detail="Login successful"),
    )

    messages = setup.apply_codex_mcp_auth()

    assert (tmp_path / "config.toml").read_text(encoding="utf-8") == before
    assert any("back as it was" in message for message in messages)
    assert messages[-1] == "Codex MCP logged in (probe-research)."


def test_rotating_the_read_token_re_points_codex_at_the_new_one(monkeypatch, tmp_path):
    """A rotation used to leave Codex holding the revoked token, and nothing
    said so: `codex mcp list` answers `bearer_token` for any header at all, so
    the health check stayed green while every Codex call 401'd."""
    from probe.cli import codex_config, plugin_cli
    from probe.sdk import config as sdk_config

    monkeypatch.setenv("CODEX_HOME", str(tmp_path))
    codex_config.write_mcp_bearer(
        "probe-research", url="https://mcp.research.prbe.ai/mcp", token="probe_pat_old"
    )
    monkeypatch.setattr(sdk_config, "load_context", lambda: {"mcp_token": "probe_pat_new"})
    monkeypatch.setattr(
        codex_config, "plugin_mcp_url", lambda _name, **_kw: "https://mcp.research.prbe.ai/mcp"
    )
    monkeypatch.setattr(plugin_cli, "codex_mcp_auth_status", lambda _name: "bearer_token")

    messages = setup.sync_codex_mcp_token()

    assert codex_config.configured_bearer("probe-research") == "probe_pat_new"
    assert messages == ["Codex MCP updated to your current read token."]


def test_a_codex_entry_that_already_matches_is_left_untouched(monkeypatch, tmp_path):
    """A no-op re-run must not rewrite the user's config for nothing."""
    from probe.cli import codex_config, plugin_cli
    from probe.sdk import config as sdk_config

    monkeypatch.setenv("CODEX_HOME", str(tmp_path))
    codex_config.write_mcp_bearer(
        "probe-research", url="https://mcp.research.prbe.ai/mcp", token="probe_pat_same"
    )
    before = (tmp_path / "config.toml").read_text(encoding="utf-8")
    monkeypatch.setattr(sdk_config, "load_context", lambda: {"mcp_token": "probe_pat_same"})
    monkeypatch.setattr(plugin_cli, "codex_mcp_auth_status", lambda _name: "bearer_token")

    assert setup.sync_codex_mcp_token() == []
    assert (tmp_path / "config.toml").read_text(encoding="utf-8") == before


def test_rotation_does_not_create_a_codex_entry_on_a_machine_without_one(monkeypatch, tmp_path):
    """`probe mcp token set` on a Claude-only machine must stay a no-op.
    Creating the entry is an install decision, not a rotation one."""
    from probe.cli import codex_config
    from probe.sdk import config as sdk_config

    monkeypatch.setenv("CODEX_HOME", str(tmp_path))
    monkeypatch.setattr(sdk_config, "load_context", lambda: {"mcp_token": "probe_pat_new"})
    monkeypatch.setattr(
        codex_config, "plugin_mcp_url", lambda _name, **_kw: "https://mcp.research.prbe.ai/mcp"
    )

    assert setup.sync_codex_mcp_token() == []
    assert not (tmp_path / "config.toml").exists()


def test_a_wizard_rerun_after_a_rotation_repairs_the_codex_token(monkeypatch, tmp_path):
    """`bearer_token` used to end the step early. That is exactly the state a
    stale token is in, so the one command that should have fixed it did not."""
    from probe.cli import codex_config, plugin_cli
    from probe.sdk import config as sdk_config

    monkeypatch.setenv("CODEX_HOME", str(tmp_path))
    codex_config.write_mcp_bearer(
        "probe-research", url="https://mcp.research.prbe.ai/mcp", token="probe_pat_old"
    )
    monkeypatch.setattr(sdk_config, "load_context", lambda: {"mcp_token": "probe_pat_new"})
    monkeypatch.setattr(
        codex_config, "plugin_mcp_url", lambda _name, **_kw: "https://mcp.research.prbe.ai/mcp"
    )
    monkeypatch.setattr(plugin_cli, "codex_mcp_auth_status", lambda _name: "bearer_token")

    assert setup.apply_codex_mcp_auth() == ["Codex MCP updated to your current read token."]
    assert codex_config.configured_bearer("probe-research") == "probe_pat_new"


def test_signing_in_re_points_codex_without_a_separate_command(isolate, monkeypatch, tmp_path):
    """`authorize()` mints a new read token AND `revoke_replaced_token` releases
    the old one, so a Codex entry left on the old copy is not stale -- it is
    DEAD. The sync was wired only into `probe mcp token set`, so the wizard's
    sign-in and the guided install -- the two callers that mint through this
    function -- 401'd every Codex call afterwards while `codex mcp list` and
    `probe doctor` both reported healthy.

    NOT `probe login`: that command never writes `mcp_token`. See
    `sync_codex_mcp_token`'s docstring.
    """
    from probe.cli import codex_config, plugin_cli

    codex_home = tmp_path / "codex"
    codex_home.mkdir(parents=True, exist_ok=True)
    monkeypatch.setenv("CODEX_HOME", str(codex_home))
    codex_config.write_mcp_bearer(
        "probe-research", url="https://mcp.research.prbe.ai/mcp", token="probe_pat_old"
    )
    monkeypatch.setattr(
        codex_config, "plugin_mcp_url", lambda _name, **_kw: "https://mcp.research.prbe.ai/mcp"
    )
    monkeypatch.setattr(plugin_cli, "codex_mcp_auth_status", lambda _name: "bearer_token")
    monkeypatch.setattr(
        "probe.sdk.device.device_authorize",
        lambda base_url, **kwargs: {
            "token": "probe_pat_api",
            "id": "api-id",
            "grants": [
                {"grant": "api", "token": "probe_pat_api", "token_id": "api-id"},
                {"grant": "mcp", "token": "probe_pat_new", "token_id": "mcp-id"},
            ],
        },
    )

    _granted, messages = setup.authorize(
        ["api", "mcp"], base_url="https://api.research.prbe.ai", open_browser=False
    )

    assert codex_config.configured_bearer("probe-research") == "probe_pat_new"
    assert "Codex MCP updated to your current read token." in messages


def _codex_entry(monkeypatch, tmp_path, *, token="probe_pat_old", url=None):
    """An existing Codex entry plus a resolvable plugin URL — the precondition
    every sync test shares."""
    from probe.cli import codex_config

    codex_home = tmp_path / "codex"
    codex_home.mkdir(parents=True, exist_ok=True)
    monkeypatch.setenv("CODEX_HOME", str(codex_home))
    target = url or codex_config.PRODUCTION_MCP_URL
    codex_config.write_mcp_bearer("probe-research", url=target, token=token)
    monkeypatch.setattr(codex_config, "plugin_mcp_url", lambda _name, **_kw: target)
    return codex_home


def _mint(mcp_token="probe_pat_new"):
    """A device_authorize stand-in that mints an api + mcp pair."""
    return lambda base_url, **kwargs: {
        "token": "probe_pat_api",
        "id": "api-id",
        "grants": [
            {"grant": "api", "token": "probe_pat_api", "token_id": "api-id"},
            {"grant": "mcp", "token": mcp_token, "token_id": "mcp-id"},
        ],
    }


def test_the_sync_refuses_to_write_a_token_across_deployments(isolate, monkeypatch, tmp_path):
    """The token and the URL come from different places and can disagree about
    which deployment they belong to. Writing them into one table hands a live
    read credential to a server it was not minted for, on every connect."""
    from probe.cli import codex_config, plugin_cli
    from probe.sdk import config as sdk_config

    _codex_entry(monkeypatch, tmp_path)  # entry + plugin URL are the STOCK endpoint
    # ...but this device is signed in to a self-hosted deployment.
    monkeypatch.setattr(
        sdk_config,
        "load_context",
        lambda *a, **k: {"mcp_token": "probe_pat_new", "base_url": "https://probe.acme.com"},
    )
    monkeypatch.setattr(plugin_cli, "codex_mcp_auth_status", lambda _name: "bearer_token")

    messages = setup.sync_codex_mcp_token()

    assert codex_config.configured_bearer("probe-research") == "probe_pat_old", (
        "the self-hosted token must not be written under the stock endpoint"
    )
    assert any("different deployment" in m for m in messages)


def test_the_sync_still_writes_when_both_halves_are_the_stock_deployment(
    isolate, monkeypatch, tmp_path
):
    """The guard above must not reject the configuration nearly everyone has:
    production splits the API and the MCP across `api.` and `mcp.`, so equal
    hosts is the wrong test and would break every normal install."""
    from probe.cli import codex_config, plugin_cli
    from probe.sdk import config as sdk_config

    _codex_entry(monkeypatch, tmp_path)
    monkeypatch.setattr(
        sdk_config,
        "load_context",
        lambda *a, **k: {
            "mcp_token": "probe_pat_new",
            "base_url": "https://api.research.prbe.ai",
        },
    )
    monkeypatch.setattr(plugin_cli, "codex_mcp_auth_status", lambda _name: "bearer_token")

    assert setup.sync_codex_mcp_token() == ["Codex MCP updated to your current read token."]
    assert codex_config.configured_bearer("probe-research") == "probe_pat_new"


def test_authorize_reports_a_codex_config_write_it_could_not_make(isolate, monkeypatch, tmp_path):
    """The refuse-to-write branch now runs on every mint, and had no coverage.
    The credentials are already on disk by this point, so it must report and
    continue — never raise out of a sign-in that actually succeeded."""
    from probe.cli import codex_config

    _codex_entry(monkeypatch, tmp_path)

    def _boom(*a, **k):
        raise codex_config.ConfigError("disk full")

    monkeypatch.setattr(codex_config, "write_mcp_bearer", _boom)
    monkeypatch.setattr("probe.sdk.device.device_authorize", _mint())

    granted, messages = setup.authorize(
        ["api", "mcp"], base_url="https://api.research.prbe.ai", open_browser=False
    )

    assert set(granted) == {"api", "mcp"}, "the mint itself still succeeded"
    assert any("still using the previous read token" in m for m in messages)
    assert codex_config.configured_bearer("probe-research") == "probe_pat_old"


def test_authorize_restores_a_codex_config_it_cannot_confirm(isolate, monkeypatch, tmp_path):
    """The rollback branch, also uncovered. `codex mcp list` failing is exactly
    what a config Codex cannot load looks like, so an unconfirmable write goes
    back byte for byte rather than being left on a user's disk."""
    from probe.cli import plugin_cli

    codex_home = _codex_entry(monkeypatch, tmp_path)
    before = (codex_home / "config.toml").read_text(encoding="utf-8")
    monkeypatch.setattr(plugin_cli, "codex_mcp_auth_status", lambda _name: None)
    monkeypatch.setattr("probe.sdk.device.device_authorize", _mint())

    _granted, messages = setup.authorize(
        ["api", "mcp"], base_url="https://api.research.prbe.ai", open_browser=False
    )

    assert any("back as it was" in m for m in messages)
    assert (codex_home / "config.toml").read_text(encoding="utf-8") == before


def test_the_wizard_repairs_codex_drift_on_a_device_that_is_already_signed_in(
    isolate, monkeypatch, tmp_path
):
    """`probe doctor` tells people to run the wizard, and every other gate on
    that screen closes in exactly this state: needs_authorization() reads `mcp`
    as held once a read token is saved, and `codex mcp list` answers
    `bearer_token` for a DEAD header. The drift predicate is the wizard's own
    signal, independent of both."""
    from probe.cli import codex_config
    from probe.sdk import config as sdk_config

    _codex_entry(monkeypatch, tmp_path)
    monkeypatch.setattr(
        sdk_config,
        "load_context",
        lambda *a, **k: {
            "mcp_token": "probe_pat_new",
            "base_url": "https://api.research.prbe.ai",
        },
    )

    assert setup.codex_mcp_token_drifted() is True, (
        "a signed-in device with a dead Codex token is the case the wizard must see"
    )

    # And it goes quiet the moment the two agree, so a healthy machine schedules
    # no work.
    codex_config.write_mcp_bearer(
        "probe-research", url=codex_config.PRODUCTION_MCP_URL, token="probe_pat_new"
    )
    assert setup.codex_mcp_token_drifted() is False


def test_the_drift_predicate_is_silent_with_nothing_to_compare(isolate, monkeypatch, tmp_path):
    """No Codex entry, or no token held here, is not evidence of drift — this
    runs on every wizard run including on machines that never touched Codex."""
    from probe.sdk import config as sdk_config

    codex_home = tmp_path / "codex"
    codex_home.mkdir(parents=True, exist_ok=True)
    monkeypatch.setenv("CODEX_HOME", str(codex_home))
    monkeypatch.setattr(sdk_config, "load_context", lambda *a, **k: {"mcp_token": "probe_pat_new"})
    assert setup.codex_mcp_token_drifted() is False, "no Codex entry"

    _codex_entry(monkeypatch, tmp_path)
    monkeypatch.setattr(sdk_config, "load_context", lambda *a, **k: {})
    assert setup.codex_mcp_token_drifted() is False, "no token held here"


def test_signing_in_creates_no_codex_entry_on_a_machine_without_one(
    isolate, monkeypatch, tmp_path
):
    """The hook must stay a repair, never an install. Registering an entry a
    user never asked for would point Codex at a server on the strength of a
    login, and `plugin_mcp_url` is not consulted on this path at all."""
    from probe.cli import codex_config

    codex_home = tmp_path / "codex"
    codex_home.mkdir(parents=True, exist_ok=True)
    monkeypatch.setenv("CODEX_HOME", str(codex_home))
    monkeypatch.setattr(
        codex_config, "plugin_mcp_url", lambda _name, **_kw: "https://mcp.research.prbe.ai/mcp"
    )
    monkeypatch.setattr(
        "probe.sdk.device.device_authorize",
        lambda base_url, **kwargs: {
            "token": "probe_pat_api",
            "id": "api-id",
            "grants": [
                {"grant": "api", "token": "probe_pat_api", "token_id": "api-id"},
                {"grant": "mcp", "token": "probe_pat_new", "token_id": "mcp-id"},
            ],
        },
    )

    setup.authorize(["api", "mcp"], base_url="https://api.research.prbe.ai", open_browser=False)

    assert not (codex_home / "config.toml").exists()


def test_codex_falls_back_to_its_own_login_when_the_shortcut_cannot_apply(monkeypatch, tmp_path):
    """No manifest to read the URL from — registering a guessed URL with a live
    token is worse than the extra approval, so the old path must still run."""
    from probe.cli import claude_cli, codex_config, plugin_cli
    from probe.sdk import config as sdk_config

    monkeypatch.setenv("CODEX_HOME", str(tmp_path))
    monkeypatch.setattr(sdk_config, "load_context", lambda: {"mcp_token": "probe_pat_from_signin"})
    monkeypatch.setattr(codex_config, "plugin_mcp_url", lambda _name, **_kw: None)
    statuses = iter(["not_logged_in", "o_auth"])
    monkeypatch.setattr(plugin_cli, "codex_mcp_auth_status", lambda _name: next(statuses))
    monkeypatch.setattr(
        plugin_cli,
        "login_codex_mcp",
        lambda _name: claude_cli.Result(ok=True, detail="Login successful"),
    )

    assert setup.apply_codex_mcp_auth() == ["Codex MCP logged in (probe-research)."]
    assert not (tmp_path / "config.toml").exists()


def test_codex_mcp_login_is_verified_after_the_supported_oauth_flow(monkeypatch):
    from probe.cli import claude_cli, plugin_cli

    _no_reuse(monkeypatch)

    statuses = iter(["not_logged_in", "o_auth"])
    monkeypatch.setattr(plugin_cli, "codex_mcp_auth_status", lambda _name: next(statuses))
    monkeypatch.setattr(
        plugin_cli,
        "login_codex_mcp",
        lambda _name: claude_cli.Result(ok=True, detail="Login successful"),
    )
    assert setup.apply_codex_mcp_auth() == ["Codex MCP logged in (probe-research)."]


def test_codex_mcp_login_failure_is_actionable(monkeypatch):
    from probe.cli import claude_cli, plugin_cli

    _no_reuse(monkeypatch)

    monkeypatch.setattr(plugin_cli, "codex_mcp_auth_status", lambda _name: "not_logged_in")
    monkeypatch.setattr(
        plugin_cli,
        "login_codex_mcp",
        lambda _name: claude_cli.Result(ok=False, detail="browser cancelled"),
    )
    messages = setup.apply_codex_mcp_auth()
    assert "codex mcp login probe-research" in messages[0]


def test_codex_capture_retires_the_legacy_plugin_before_using_unified_tap(monkeypatch):
    from probe.cli import claude_cli, plugin_cli

    removed: list[str] = []
    monkeypatch.setattr(
        plugin_cli,
        "uninstall",
        lambda source, plugin_id: (
            removed.append(f"{source}:{plugin_id}") or claude_cli.Result(ok=True, detail="removed")
        ),
    )
    messages = setup.apply_capture(
        _caps(
            agent_source="codex",
            capture_plugin_installed=True,
            legacy_capture_plugin_installed=True,
        ),
        True,
        mode=capture.OffMode.DISABLE,
    )
    assert removed == ["codex:prbe-codex-tap-plugin@prbe-ai"]
    assert any("Removed legacy" in message for message in messages)


def test_authorize_persists_every_minted_credential(isolate, monkeypatch):
    """The gap this closes: computing a grant set and never sending it left
    capture off after a setup that said it turned it on."""
    sent = {}

    def fake_device_authorize(base_url, **kwargs):
        sent.update(kwargs)
        return {
            "token": "probe_pat_api",
            "id": "api-id",
            "grants": [
                {"grant": "api", "token": "probe_pat_api", "token_id": "api-id"},
                {"grant": "mcp", "token": "probe_pat_mcp", "token_id": "mcp-id"},
                {"grant": "capture", "token": "ros_ing_dev", "device_id": "dev-1"},
            ],
        }

    monkeypatch.setattr("probe.sdk.device.device_authorize", fake_device_authorize)

    by_grant, messages = setup.authorize(
        ["api", "mcp", "capture"],
        base_url="https://api.research.prbe.ai",
        open_browser=False,
    )

    assert sent["grants"] == ["api", "mcp", "capture"]
    assert sent["capture_source"] == "claude_code"
    assert set(by_grant) == {"api", "mcp", "capture"}
    assert any("paired" in m for m in messages)

    # The capture credential landed where the uploader actually looks for it.
    assert TokenSource.PROBE_CONFIG in capture_token_sources()
    from probe.cli.capabilities import probe_config_credentials

    creds = probe_config_credentials()
    assert creds["token"] == "probe_pat_api"
    assert creds["mcp_token"] == "probe_pat_mcp"
    assert creds["ingest_token"] == "ros_ing_dev"


def test_codex_authorization_is_source_bound_and_writes_the_codex_token(
    isolate, monkeypatch, tmp_path
):
    sent = {}

    def fake_device_authorize(base_url, **kwargs):
        sent.update(kwargs)
        return {"grants": [{"grant": "capture", "token": "ros_ing_codex", "device_id": "cx-1"}]}

    monkeypatch.setenv("PROBE_AGENT", "codex")
    monkeypatch.setenv("PRBE_CODEX_TAP_PLUGIN_DIR", str(tmp_path))
    monkeypatch.setattr("probe.sdk.device.device_authorize", fake_device_authorize)

    by_grant, _messages = setup.authorize(
        ["capture"], base_url="https://api.research.prbe.ai", open_browser=False
    )

    assert sent["capture_source"] == "codex"
    assert by_grant["capture"]["device_id"] == "cx-1"
    assert (tmp_path / ".token").read_text() == "ros_ing_codex"
    assert (tmp_path / ".token").stat().st_mode & 0o777 == 0o600


def test_one_authorization_pairs_claude_and_codex_with_distinct_tokens(
    isolate, monkeypatch, tmp_path
):
    sent = {}

    def fake_device_authorize(base_url, **kwargs):
        sent.update(kwargs)
        return {
            "grants": [
                {
                    "grant": "capture",
                    "capture_source": "claude_code",
                    "token": "ros_ing_claude",
                    "device_id": "cc-1",
                },
                {
                    "grant": "capture",
                    "capture_source": "codex",
                    "token": "ros_ing_codex",
                    "device_id": "cx-1",
                },
            ]
        }

    codex_state = tmp_path / "codex-tap"
    monkeypatch.setenv("PRBE_CODEX_TAP_PLUGIN_DIR", str(codex_state))
    monkeypatch.setattr("probe.sdk.device.device_authorize", fake_device_authorize)

    granted, messages = setup.authorize(
        ["capture"],
        capture_sources=["claude_code", "codex"],
        base_url="https://api.research.prbe.ai",
        open_browser=False,
    )

    assert sent["capture_sources"] == ["claude_code", "codex"]
    assert "capture_source" not in sent
    assert granted["capture"]["capture_source"] == "claude_code"
    assert capture_token_sources("claude_code") == (TokenSource.PROBE_CONFIG,)
    assert (codex_state / ".token").read_text() == "ros_ing_codex"
    assert any("Claude Code Session capture paired" in message for message in messages)
    assert any("Codex Session capture paired" in message for message in messages)


def test_pi_authorization_is_source_bound_and_writes_the_pi_token(isolate, monkeypatch, tmp_path):
    """The parity case for test_codex_authorization_is_source_bound_and_writes_the_codex_token:
    a pi-only capture grant must land in pi's OWN plugin dir, not fall through
    the old codex-only special case and land nowhere -- and the confirmation
    must name pi, not default to "Claude Code"."""
    sent = {}

    def fake_device_authorize(base_url, **kwargs):
        sent.update(kwargs)
        return {"grants": [{"grant": "capture", "token": "ros_ing_pi", "device_id": "pi-1"}]}

    monkeypatch.setenv("PROBE_PI_TAP_PLUGIN_DIR", str(tmp_path))
    monkeypatch.setattr("probe.sdk.device.device_authorize", fake_device_authorize)

    by_grant, messages = setup.authorize(
        ["capture"],
        capture_sources=["pi"],
        base_url="https://api.research.prbe.ai",
        open_browser=False,
    )

    assert sent["capture_source"] == "pi"
    assert by_grant["capture"]["device_id"] == "pi-1"
    assert (tmp_path / ".token").read_text() == "ros_ing_pi"
    assert (tmp_path / ".token").stat().st_mode & 0o777 == 0o600
    assert any("pi Session capture paired" in message for message in messages)
    assert not any("Claude Code Session capture paired" in message for message in messages)


def test_one_authorization_pairs_all_three_sources_with_distinct_tokens(
    isolate, monkeypatch, tmp_path
):
    sent = {}

    def fake_device_authorize(base_url, **kwargs):
        sent.update(kwargs)
        return {
            "grants": [
                {
                    "grant": "capture",
                    "capture_source": "claude_code",
                    "token": "ros_ing_claude",
                    "device_id": "cc-1",
                },
                {
                    "grant": "capture",
                    "capture_source": "codex",
                    "token": "ros_ing_codex",
                    "device_id": "cx-1",
                },
                {
                    "grant": "capture",
                    "capture_source": "pi",
                    "token": "ros_ing_pi",
                    "device_id": "pi-1",
                },
            ]
        }

    codex_state = tmp_path / "codex-tap"
    pi_state = tmp_path / "pi-tap"
    monkeypatch.setenv("PRBE_CODEX_TAP_PLUGIN_DIR", str(codex_state))
    monkeypatch.setenv("PROBE_PI_TAP_PLUGIN_DIR", str(pi_state))
    monkeypatch.setattr("probe.sdk.device.device_authorize", fake_device_authorize)

    granted, messages = setup.authorize(
        ["capture"],
        capture_sources=["claude_code", "codex", "pi"],
        base_url="https://api.research.prbe.ai",
        open_browser=False,
    )

    assert sent["capture_sources"] == ["claude_code", "codex", "pi"]
    assert granted["capture"]["capture_source"] == "claude_code"
    assert (codex_state / ".token").read_text() == "ros_ing_codex"
    assert (pi_state / ".token").read_text() == "ros_ing_pi"
    assert any("Claude Code Session capture paired" in message for message in messages)
    assert any("Codex Session capture paired" in message for message in messages)
    assert any("pi Session capture paired" in message for message in messages)
    # The bug this whole item fixes: exactly one message per paired source,
    # each under its own name -- never three sources collapsed onto "Claude
    # Code" by a ternary that only recognized codex as "not claude_code".
    paired_messages = [m for m in messages if "Session capture paired (device" in m]
    assert len(paired_messages) == 3


def _tap_config_module():
    """Import the REAL tap package's config module by path, not a
    re-implementation of it -- so this test fails if the two independently
    duplicated resolutions (capabilities.py here, tap/config.py there) ever
    disagree, rather than comparing capabilities.py against itself. Mirrors
    exactly how tapRuntime.ts / PROBE_PI_TAP_ROOT resolve a tap checkout in
    production: the tap package has zero dependencies (see its pyproject.toml),
    so this needs nothing beyond putting its directory on sys.path.
    """
    import importlib
    import sys
    from pathlib import Path

    tap_root = Path(__file__).resolve().parents[1] / "plugins" / "probe-research-tap"
    assert tap_root.is_dir(), f"tap checkout not found at {tap_root}"
    if str(tap_root) not in sys.path:
        sys.path.insert(0, str(tap_root))
    import tap.config as tap_config  # noqa: PLC0415

    # env vars change per-test; a cached module would answer from whichever
    # test imported it first.
    importlib.reload(tap_config)
    return tap_config


def test_pi_pairing_reaches_exactly_where_the_tap_daemon_will_look(
    isolate, monkeypatch, tmp_path
):
    """The full chain a real user exercises: `probe wizard --agent pi` at a
    shell, through doctor.collect() (REAL, not mocked -- this is what proves
    capabilities.agent_source()/installed_plugins() actually behave under
    PROBE_AGENT=pi rather than just being unit-testable in isolation), through
    the forced pi-only selection scoping in _run_wizard_action, to authorize()
    (only the network device-authorize call is mocked), to a token file --
    read back through the REAL tap/config.py::plugin_dir()/load_token(), not a
    second guess at what path or precedence those resolve to.

    Also proves the negative that made this item necessary: not one call
    reaches `claude`/`codex`'s plugin CLI. Before this item's fixes, a bare
    `--agent pi --yes` run on a fresh device (FRESH_DEFAULTS wanting tracking
    too) would have shelled out to `claude plugin install` -- installing INTO
    Claude Code as a side effect of pairing pi -- the moment Claude Code
    happened to also be on the machine, which is the common case, not an edge
    one.
    """
    import sys
    from types import SimpleNamespace

    from typer.testing import CliRunner

    from probe.cli import bootstrap, plugin_cli
    import probe.cli.main  # noqa: F401

    cli_main = sys.modules["probe.cli.main"]

    pi_state = tmp_path / "pi-state"
    monkeypatch.setenv("PROBE_PI_TAP_PLUGIN_DIR", str(pi_state))
    monkeypatch.setattr(
        bootstrap, "ensure_persistent_install", lambda **_: SimpleNamespace(message="")
    )
    # doctor.collect() runs for REAL in this test (see the docstring) --
    # everything except this one call: verify_capture_credential() does a
    # genuine urllib request to `{base_url}/ingest/v1/sessions/status`, and an
    # unmocked base_url defaults to the real production API
    # (probe.sdk.config.DEFAULT_BASE_URL). Without this, the fake token this
    # test mints gets a real 401 from prbe.ai on every run. None (unverifiable,
    # same as a genuinely offline machine) rather than True: a fabricated True
    # would hide a real drift in what this function does for source="pi".
    monkeypatch.setattr(capabilities_mod, "verify_capture_credential", lambda *a, **k: None)

    plugin_calls: list[str] = []
    for name in ("install", "uninstall", "list_plugins", "add_marketplace", "refresh_marketplace"):
        original = getattr(plugin_cli, name)

        def _spy(*args, _name=name, _orig=original, **kwargs):
            plugin_calls.append(_name)
            return _orig(*args, **kwargs)

        monkeypatch.setattr(plugin_cli, name, _spy)

    minted = {
        "grants": [{"grant": "capture", "token": "ros_ing_pi_e2e", "device_id": "pi-e2e-1"}]
    }
    sent: dict = {}

    def fake_device_authorize(base_url, **kwargs):
        sent.update(kwargs)
        return minted

    monkeypatch.setattr("probe.sdk.device.device_authorize", fake_device_authorize)

    result = CliRunner().invoke(
        cli_main.app,
        [
            "wizard",
            "--agent",
            "pi",
            "--action",
            "configure",
            "--capture",
            "--no-tracking",
            "--no-agent-rules",
            "--no-auto-update",
            "--yes",
        ],
    )

    assert result.exit_code == 0, result.output
    assert sent.get("capture_source") == "pi", sent
    assert not plugin_calls, (
        f"a pi-only pairing run touched claude/codex's plugin CLI: {plugin_calls}"
    )

    tap_config = _tap_config_module()
    os.environ["PROBE_TAP_SOURCE"] = "pi"
    try:
        real_token_file = tap_config.token_file()
        assert real_token_file == pi_state / ".token", (
            "capabilities.tap_plugin_dir('pi') and tap/config.py::plugin_dir() "
            f"disagree: {real_token_file} != {pi_state / '.token'}"
        )
        assert real_token_file.read_text(encoding="utf-8") == "ros_ing_pi_e2e"
        assert real_token_file.stat().st_mode & 0o777 == 0o600

        # The daemon's OWN load_token() (not a paraphrase of it) must find this
        # token, under the exact env the daemon runs with (PROBE_TAP_SOURCE=pi,
        # set by spawnDaemon() -- see probe-research-pi/src/core/daemon.ts).
        assert tap_config.load_token() == "ros_ing_pi_e2e"
    finally:
        del os.environ["PROBE_TAP_SOURCE"]


def test_agent_flag_accepts_pi_and_still_rejects_garbage():
    import sys

    from typer.testing import CliRunner

    import probe.cli.main  # noqa: F401

    cli_main = sys.modules["probe.cli.main"]
    result = CliRunner().invoke(cli_main.app, ["wizard", "--agent", "bogus"])
    assert result.exit_code != 0
    assert "must be claude, codex, pi, kimi, or both" in result.output


def test_agent_both_still_means_exactly_claude_and_codex_not_pi(monkeypatch):
    """The deliberate choice this item made explicit: `--agent both`/`--agent
    all` keep their EXISTING two-source meaning. pi is reachable only by
    naming it -- silently sweeping it into "both" would hand every existing
    scripted `--agent both` caller a third browser-approval grant, and a
    third plugin-install attempt, it never asked for."""
    import sys
    from types import SimpleNamespace

    from typer.testing import CliRunner

    from probe.cli import bootstrap
    from probe.cli import doctor as doctor_impl
    import probe.cli.main  # noqa: F401

    cli_main = sys.modules["probe.cli.main"]
    monkeypatch.setattr(bootstrap, "ensure_persistent_install", lambda **_: SimpleNamespace(message=""))
    monkeypatch.setattr(
        doctor_impl,
        "collect",
        lambda: _caps(agent_source=os.environ.get("PROBE_AGENT", "claude_code")),
    )
    calls: list[str] = []
    monkeypatch.setattr(
        cli_main,
        "_run_wizard_action",
        lambda action, **kwargs: calls.append(os.environ["PROBE_AGENT"]) or [],
    )

    for value in ("both", "all"):
        calls.clear()
        result = CliRunner().invoke(
            cli_main.app, ["wizard", "--agent", value, "--action", "configure", "--yes"]
        )
        assert result.exit_code == 0, result.output
        assert calls == ["claude_code", "codex"], f"--agent {value}: {calls}"


def test_agent_source_recognizes_pi_rather_than_defaulting_to_claude_code(monkeypatch):
    """Before this fix, PROBE_AGENT=pi silently resolved to claude_code here --
    the same "unrecognized value defaults to the wrong source" failure mode as
    the ternaries this whole item exists to close off, just one level lower."""
    monkeypatch.setenv("PROBE_AGENT", "pi")
    assert capabilities_mod.agent_source() == "pi"


def test_installed_plugins_never_asks_claude_or_codex_about_pi(monkeypatch):
    """pi has no plugin CLI (plugin_cli.py is deliberately claude/codex-only)
    -- installed_plugins(source="pi") must never shell out to it. Before this
    fix that mattered because falling through resolved pi's binary as
    "claude" (plugin_cli.binary_name()'s own codex-or-claude default) and
    reported on CLAUDE's actual plugin list under pi's name.

    Its real signal now (D7) is `pi_config.package_entry_installed()` -- a
    settings.json read, not a subprocess -- so this covers both outcomes:
    absent reads as not-installed-and-unverified (unchanged), present makes
    `capture_plugin_name("pi")` (== TAP_PLUGIN_NAME here) a member of
    `names`, which is what `Capabilities.capture_plugin_installed` and
    `probe doctor` actually key off. `verified` stays False either way --
    see `installed_plugins`'s own docstring on why a positive read is a fact
    worth standing behind but a negative one is not.
    """
    from probe.cli import pi_config, plugin_cli

    def _must_not_run(*_args, **_kwargs):
        raise AssertionError("installed_plugins('pi') must never shell out to claude/codex")

    monkeypatch.setattr(plugin_cli, "list_plugins", _must_not_run)

    monkeypatch.setattr(pi_config, "package_entry_installed", lambda: False)
    absent = capabilities_mod.installed_plugins(source="pi")
    assert absent.verified is False
    assert len(absent) == 0

    monkeypatch.setattr(pi_config, "package_entry_installed", lambda: True)
    present = capabilities_mod.installed_plugins(source="pi")
    assert present.verified is False
    assert capabilities_mod.TAP_PLUGIN_NAME in present


def test_apply_capture_installs_the_pi_package_entry(monkeypatch):
    """pi is installable now (INSTALLABLE_AGENT_SOURCES): apply_capture()'s
    old guard -- clear the killswitch and stop, never call install_plugin --
    is gone. Clearing the killswitch is still the first job, but a missing
    plugin now genuinely means calling through to `pi_config`, never
    `plugin_cli` (which would resolve pi's binary as "claude")."""
    from pathlib import Path

    from probe.cli import claude_cli, pi_config, plugin_cli

    def _must_not_run(*_args, **_kwargs):
        raise AssertionError("apply_capture() must never reach plugin_cli for pi")

    monkeypatch.setattr(plugin_cli, "install", _must_not_run)
    installed: list[tuple] = []
    fake_root = Path("/fake/probe-research-pi")
    # `install_package_entry` now picks the source itself (checkout or the
    # published mirror), so the wizard calls it with NO root -- that choice
    # belongs in one place, not at every call site.
    monkeypatch.setattr(pi_config, "local_package_root", lambda *a, **kw: fake_root)
    monkeypatch.setattr(
        pi_config,
        "install_package_entry",
        lambda *a, **kw: installed.append(a) or claude_cli.Result(ok=True, detail="added"),
    )
    monkeypatch.setattr(
        pi_config,
        "migrate_legacy_symlink",
        lambda root, **kw: claude_cli.Result(
            ok=True, detail="no legacy symlink; nothing to migrate"
        ),
    )

    caps = _caps(agent_source="pi", capture_plugin_installed=False)
    messages = setup.apply_capture(caps, True, mode=capture.OffMode.DISABLE)

    assert installed == [()]
    assert messages == []


def test_apply_capture_folds_in_the_migration_detail_when_one_happened(monkeypatch):
    """PackageRootError and a real migration both have to reach the wizard as
    prose, not silently -- the migration case specifically only when
    something actually changed on disk (plan D4), matching
    `_install_pi_package`'s own "removed legacy symlink" prefix check."""
    from pathlib import Path

    from probe.cli import claude_cli, pi_config

    fake_root = Path("/fake/probe-research-pi")
    monkeypatch.setattr(pi_config, "local_package_root", lambda *a, **kw: fake_root)
    monkeypatch.setattr(
        pi_config,
        "install_package_entry",
        lambda *a, **kw: claude_cli.Result(ok=True, detail="added probe-research-pi (root)"),
    )
    monkeypatch.setattr(
        pi_config,
        "migrate_legacy_symlink",
        lambda root, **kw: claude_cli.Result(
            ok=True, detail="removed legacy symlink /fake/extensions/probe-research-pi"
        ),
    )

    result = setup.install_plugin("probe-research-pi", source="pi")

    assert result.ok
    assert "added probe-research-pi" in result.detail
    assert "removed legacy symlink" in result.detail

    # The mirror install: nothing resolves locally, which is no longer a
    # failure -- it is the normal customer shape. D4 migration is skipped
    # (a legacy symlink could only ever point inside a checkout), so the
    # install's own detail is the whole result.
    monkeypatch.setattr(pi_config, "local_package_root", lambda *a, **kw: None)

    def _must_not_migrate(*_a, **_kw):
        raise AssertionError("no checkout means nothing D4 could match")

    monkeypatch.setattr(pi_config, "migrate_legacy_symlink", _must_not_migrate)
    mirrored = setup.install_plugin("probe-research-pi", source="pi")
    assert mirrored.ok is True
    assert "added probe-research-pi" in mirrored.detail

    # A BROKEN explicit override still reaches the wizard as a failed Result,
    # never as a raise out of the step runner.
    monkeypatch.setattr(
        pi_config,
        "install_package_entry",
        lambda *a, **kw: claude_cli.Result(
            ok=False, detail="PROBE_PI_PACKAGE_ROOT=/nope has no package.json in it", reachable=False
        ),
    )
    failure = setup.install_plugin("probe-research-pi", source="pi")
    assert failure.ok is False
    assert failure.reachable is False
    assert "PROBE_PI_PACKAGE_ROOT" in failure.detail


def test_install_plugin_family_routes_pi_through_pi_config(monkeypatch):
    """install_plugin()/uninstall_plugin() dispatch pi through pi_config, never
    plugin_cli (which would resolve pi's binary as "claude" and silently
    install into it instead) -- and refresh_marketplace() treats pi as a
    no-op success, since pi has no marketplace to refresh and main.py's
    `_refresh()` step would otherwise turn a non-ok Result here into a
    printed failure line for a run that did nothing wrong."""
    from pathlib import Path

    from probe.cli import claude_cli, pi_config, plugin_cli

    def _must_not_run(*_args, **_kwargs):
        raise AssertionError("must never reach plugin_cli for pi")

    monkeypatch.setattr(plugin_cli, "install", _must_not_run)
    monkeypatch.setattr(plugin_cli, "uninstall", _must_not_run)
    monkeypatch.setattr(plugin_cli, "add_marketplace", _must_not_run)
    monkeypatch.setattr(plugin_cli, "refresh_marketplace", _must_not_run)

    fake_root = Path("/fake/probe-research-pi")
    monkeypatch.setattr(pi_config, "local_package_root", lambda *a, **kw: fake_root)
    monkeypatch.setattr(
        pi_config,
        "install_package_entry",
        lambda *a, **kw: claude_cli.Result(ok=True, detail="added"),
    )
    monkeypatch.setattr(
        pi_config,
        "migrate_legacy_symlink",
        lambda root, **kw: claude_cli.Result(ok=True, detail="nothing to migrate"),
    )
    removed: list[str] = []
    monkeypatch.setattr(
        pi_config,
        "remove_package_entry",
        lambda **kw: removed.append("called") or claude_cli.Result(ok=True, detail="removed"),
    )

    install_result = setup.install_plugin("probe-research-pi", source="pi")
    assert install_result.ok is True

    uninstall_result = setup.uninstall_plugin("probe-research-pi", source="pi")
    assert uninstall_result.ok is True
    assert removed == ["called"]

    refresh_result = setup.refresh_marketplace(source="pi")
    assert refresh_result.ok is True, "no marketplace to refresh is a no-op, not a failure"


def test_a_pi_run_schedules_tracking_and_agent_rules_work(monkeypatch):
    """The core safety property main.py now enforces: whatever tracking/
    capture/auto_update/agent_rules FRESH_DEFAULTS or a guided-install force-on
    would otherwise resolve to, a pi-selected run is forced capture-only before
    plan()/the work list ever see it -- see _run_wizard_action's pi selection
    override. Asserted on the Selection plan() actually receives, mirroring
    test_every_capability_is_reachable_as_a_flag's own pattern."""
    import sys
    from types import SimpleNamespace

    from typer.testing import CliRunner

    from probe.cli import bootstrap
    from probe.cli import doctor as doctor_impl
    from probe.cli import setup as wizard
    import probe.cli.main  # noqa: F401

    cli_main = sys.modules["probe.cli.main"]
    seen: list = []
    monkeypatch.setattr(bootstrap, "ensure_persistent_install", lambda **_: SimpleNamespace(message=""))
    monkeypatch.setattr(doctor_impl, "collect", lambda: _caps(agent_source="pi"))
    monkeypatch.setattr(wizard, "plan", lambda caps, selection: seen.append(selection) or [])

    result = CliRunner().invoke(
        cli_main.app,
        ["wizard", "--agent", "pi", "--action", "configure", "--yes"],
    )

    assert result.exit_code == 0, result.output
    assert seen, "plan() was never reached"
    selection = seen[0]
    # pi is no longer forced capture-only: the packages entry installs the
    # extension/skills/MCP manifest, and agent_rules writes pi's own
    # ~/.pi/agent/AGENTS.md (which pi loads). Tracking is what requests the
    # `mcp` grant that mints the bearer token the extension reads, so refusing
    # it here was what forced every pi user through interactive OAuth.
    assert selection.tracking is True
    assert selection.agent_rules is True


def test_an_explicit_opt_out_cleans_a_note_an_older_opt_out_left(monkeypatch, tmp_path):
    """An older opt-out removed the pointer and left the team note. The pointer
    is what `agent_rules_installed` reads, so `--no-agent-rules` saw nothing to
    change and the note stayed."""
    import sys
    from types import SimpleNamespace

    from typer.testing import CliRunner

    from probe.cli import agent_rules, bootstrap
    from probe.cli import doctor as doctor_impl
    from probe.cli import setup as wizard
    import probe.cli.main  # noqa: F401

    cli_main = sys.modules["probe.cli.main"]
    monkeypatch.setenv("CLAUDE_CONFIG_DIR", str(tmp_path))
    path = agent_rules.memory_path("claude_code")
    path.write_text("mine\n", encoding="utf-8")
    agent_rules.install(path, spec=agent_rules.NOTE_BLOCK, block=agent_rules.render_note_block("## n", document="d"))
    calls: list = []
    monkeypatch.setattr(bootstrap, "ensure_persistent_install", lambda **_: SimpleNamespace(message=""))
    monkeypatch.setattr(
        doctor_impl,
        "collect",
        lambda: _caps(agent_source="claude_code", tracking_plugin_installed=True, auto_update_enabled=True),
    )
    monkeypatch.setattr(wizard, "apply_agent_rules", lambda want, stale=False: calls.append(want) or [])

    result = CliRunner().invoke(
        cli_main.app,
        ["wizard", "--agent", "claude", "--action", "configure", "--no-agent-rules", "--yes"],
    )

    assert result.exit_code == 0, result.output
    assert calls == [False]


def test_capture_credentials_are_indexed_by_source_without_collapsing():
    from probe.sdk.device import capture_credentials_by_source

    minted = {
        "grants": [
            {"grant": "capture", "capture_source": "claude_code", "token": "one"},
            {"grant": "capture", "capture_source": "codex", "token": "two"},
        ]
    }
    assert {
        source: credential["token"]
        for source, credential in capture_credentials_by_source(minted).items()
    } == {"claude_code": "one", "codex": "two"}


def test_codex_plugin_install_uses_codex_marketplace_commands(monkeypatch):
    calls: list[list[str]] = []
    monkeypatch.setenv("PROBE_AGENT", "codex")
    monkeypatch.setattr(
        setup.plugin_cli,
        "install",
        lambda source, plugin_id: (
            calls.append([source, plugin_id]) or setup.claude_cli.Result(ok=True, detail="ok")
        ),
    )

    assert setup.install_plugin("probe-research-tap").ok is True
    assert calls == [
        ["codex", "probe-research-tap@research-os-agent"],
    ]


def test_authorize_says_so_when_the_server_returns_nothing_for_a_grant(isolate, monkeypatch):
    """Approved but not minted must not read as success."""
    monkeypatch.setattr(
        "probe.sdk.device.device_authorize",
        lambda base_url, **kw: {"grants": [{"grant": "api", "token": "probe_pat_x"}]},
    )
    _, messages = setup.authorize(["api", "capture"], base_url="https://x", open_browser=False)
    assert any("capture" in m and "NOT active" in m for m in messages)


def test_authorize_reports_a_failed_approval_instead_of_claiming_success(isolate, monkeypatch):
    from probe.sdk.device import DeviceLoginError

    def boom(base_url, **kw):
        raise DeviceLoginError("the user denied this request")

    monkeypatch.setattr("probe.sdk.device.device_authorize", boom)
    by_grant, messages = setup.authorize(["api"], base_url="https://x", open_browser=False)
    assert by_grant == {}
    assert any("denied" in m for m in messages)


def test_older_backend_without_grants_still_yields_the_api_credential():
    """A backend that predates grants returns only the top-level PAT."""
    from probe.sdk.device import credentials_by_grant

    assert credentials_by_grant({"token": "probe_pat_old", "id": "t1"}) == {
        "api": {"grant": "api", "token": "probe_pat_old", "token_id": "t1"}
    }


def test_device_authorize_omits_grants_entirely_when_not_asked(monkeypatch):
    """Sending `grants: null` would fail validation on an older backend."""
    import httpx

    captured = {}

    class FakeClient:
        def post(self, path, json=None):
            captured.update(json or {})
            raise httpx.HTTPError("stop here")

        def close(self):
            pass

    from probe.sdk import device

    with pytest.raises(device.DeviceLoginError):
        device.device_authorize("https://x", client=FakeClient(), open_browser=False)
    assert "grants" not in captured


# --- the collapsed dashboard sections, now wizard actions ------------------


def test_manual_steps_are_generated_from_the_same_constants_the_wizard_uses():
    """The page's copy had already drifted from the commands printed beside it.
    A script generated from the real constants cannot drift."""
    from probe.cli.actions import manual_steps
    from probe.cli.capabilities import MARKETPLACE_REPO, PLUGIN_ID, TAP_PLUGIN_ID

    steps = manual_steps(base_url="https://api.research.prbe.ai")
    assert f"claude plugin marketplace add {MARKETPLACE_REPO}" in steps
    assert f"claude plugin install {PLUGIN_ID}" in steps
    assert f"claude plugin install {TAP_PLUGIN_ID}" in steps
    # `add` does not refresh an already-added marketplace; the update must be there.
    assert "marketplace update" in steps
    assert steps.index("marketplace add") < steps.index("marketplace update")
    assert "probe wizard --action login --base-url https://api.research.prbe.ai" in steps
    # Never a credential, and never a git URL (a moving branch nobody can name).
    assert "git+https://" not in steps
    assert "--token" not in steps


def test_manual_steps_use_codex_verbs_when_codex_is_selected():
    from probe.cli.actions import manual_steps

    steps = manual_steps(base_url="https://api.research.prbe.ai", agent_source="codex")
    assert "codex plugin marketplace upgrade research-os-agent" in steps
    assert "codex plugin add probe-research@research-os-agent" in steps
    assert "codex mcp login probe-research" in steps
    assert "claude plugin" not in steps


def test_manual_steps_include_each_selected_agent():
    from probe.cli.actions import manual_steps

    steps = manual_steps(
        base_url="https://api.research.prbe.ai",
        agent_source=("claude_code", "codex"),
    )
    assert "claude plugin marketplace update research-os-agent" in steps
    assert "codex plugin marketplace upgrade research-os-agent" in steps
    assert "claude plugin install probe-research@research-os-agent" in steps
    assert "codex plugin add probe-research@research-os-agent" in steps
    assert "codex mcp login probe-research" in steps


def test_troubleshooting_is_state_aware_not_a_static_list():
    """A static list makes the reader work out which item applies. The wizard
    already knows, so it should only say the relevant things."""
    from probe.cli.actions import troubleshooting

    no_claude = troubleshooting(_caps(cli_version="0.9.2"))
    assert any("not on PATH" in note for note in no_claude)

    healthy = troubleshooting(
        _caps(cli_version="0.9.2", claude_available=True, logged_in_as="a@b.c")
    )
    assert not any("not on PATH" in note for note in healthy)

    # The footgun that cannot heal itself is ALWAYS surfaced: nothing in the
    # product can unset a variable in the user's shell.
    for notes in (no_claude, healthy):
        assert any("PROBE_MCP_TOKEN" in note and "SHADOWS" in note for note in notes)


def test_codex_troubleshooting_uses_native_oauth_language():
    from probe.cli.actions import troubleshooting

    notes = troubleshooting(_caps(agent_source="codex", codex_available=True))
    blob = " ".join(notes)
    assert "codex mcp login probe-research" in blob
    assert "PROBE_MCP_TOKEN" not in blob


def test_pi_troubleshooting_never_tells_you_to_install_claude_code():
    """REGRESSION: `agent_binary`/`agent_name`/`agent_available` used to fall
    through to claude's ("codex" if ... else "claude"/"Claude Code"), so a
    `probe wizard --agent pi --action diagnose` on a machine with no Claude
    Code told a pi user to go install one -- for a run that was never about
    Claude Code, and the auto-update line named the wrong session-start too."""
    from probe.cli.actions import troubleshooting

    notes = troubleshooting(
        _caps(
            agent_source="pi",
            claude_available=False,
            codex_available=False,
            auto_update_enabled=True,
            last_update_attempt=None,
        )
    )
    blob = " ".join(notes)
    assert "Claude Code" not in blob
    assert "install" not in blob.lower() or "not on PATH" not in blob
    assert "not on PATH" not in blob
    # The generic PROBE_MCP_TOKEN footgun note still applies to pi (its MCP
    # bridge mirrors the same env-shadow precedence) and must stay.
    assert any("PROBE_MCP_TOKEN" in note and "SHADOWS" in note for note in notes)


def test_installed_but_not_logged_in_is_called_out():
    from probe.cli.actions import troubleshooting

    notes = troubleshooting(
        _caps(cli_version="0.9.2", claude_available=True, tracking_plugin_installed=True)
    )
    assert any("not logged in" in note for note in notes)


def test_every_menu_action_has_copy():
    from probe.cli.actions import ACTION_COPY, Action

    # MANUAL is deliberately absent: reachable via `--action manual` for
    # air-gapped users, but it is the rarest path and it made the menu longer
    # for everyone else. Signing in happens before this account-required menu;
    # Sign out is its direct account action. ACCOUNT and the individual import
    # lanes remain legacy flags; the menu shares one research-import selector.
    assert set(ACTION_COPY) == set(Action) - {
        Action.MANUAL, Action.SIGN_IN, Action.ACCOUNT, Action.BACKFILL, Action.TRANSCRIPTS,
    }
    for title, detail in ACTION_COPY.values():
        assert title and detail


def test_state_summary_shows_the_killswitch_rather_than_a_bare_off(isolate):
    """ "off" and "off because you disabled it" are different situations."""
    killswitched = _caps(
        capture_token_sources=(TokenSource.PAIRED_FILE,), capture_killswitched=True
    )
    assert any("killswitch" in line for line in setup.describe_state(killswitched))
    plain = _caps()
    assert not any("killswitch" in line for line in setup.describe_state(plain))


def test_self_host_notes_keep_the_hosted_endpoint_and_air_gap_path():
    from probe.cli.actions import self_host_notes

    notes = self_host_notes(
        base_url="https://api.research.prbe.ai",
        mcp_endpoint="https://mcp.research.prbe.ai/mcp",
    )
    assert "mcp.research.prbe.ai/mcp" in notes
    assert "PROBE_MCP_TOKEN=YOUR_READ_TOKEN" in notes
    assert "probe-research-mcp" in notes


# --- the wizard must leave a real binary behind ---------------------------


def test_ephemeral_launch_installs_the_cli_persistently(monkeypatch):
    """`npx probe-research` runs us through an EPHEMERAL `uv tool run`, which
    leaves nothing installed. Everything after the wizard assumes a real binary:
    `probe doctor`, the plugin's version-check hook, the MCP headers helper."""
    from probe.cli import bootstrap

    calls = []
    monkeypatch.setattr(bootstrap, "_resolves_on_path", lambda: False)
    monkeypatch.setattr(
        bootstrap.shutil, "which", lambda name: "/usr/bin/uv" if name == "uv" else None
    )

    class Done:
        returncode = 0
        stdout = ""
        stderr = ""

    monkeypatch.setattr(bootstrap.subprocess, "run", lambda cmd, **kw: calls.append(cmd) or Done())

    result = bootstrap.ensure_persistent_install()

    assert result.installed is True
    install = [c for c in calls if "install" in c][0]
    assert install[:4] == ["uv", "tool", "install", "--force"]
    # The legacy distribution owns the same `probe` binary, so it must be
    # removed FIRST or the old build keeps answering.
    assert calls[0][:3] == ["uv", "tool", "uninstall"]


def test_an_existing_install_is_left_alone(monkeypatch):
    """A re-run must not reinstall on every invocation."""
    from probe.cli import bootstrap

    monkeypatch.setattr(bootstrap, "_resolves_on_path", lambda: True)
    result = bootstrap.ensure_persistent_install()
    assert result.already_persistent is True
    assert result.installed is False
    assert result.message == ""


def test_binary_outside_PATH_still_counts_as_installed(monkeypatch, tmp_path):
    """Claude Code launched from the dock sources no profile, so ~/.local/bin
    can be missing from PATH while the binary is right there. The plugin hook
    checks the same fallbacks, so we must agree or we reinstall forever."""
    from probe.cli import bootstrap

    fake = tmp_path / ".local" / "bin" / "probe"
    fake.parent.mkdir(parents=True)
    fake.write_text("#!/bin/sh\n")
    fake.chmod(0o755)
    monkeypatch.setattr(bootstrap.shutil, "which", lambda _: None)
    monkeypatch.setattr(bootstrap.os.path, "expanduser", lambda _: str(tmp_path))

    # Found outside PATH — the plugin hook checks these same fallbacks.
    assert bootstrap._installed_binary() == str(fake)
    # And a new-enough one counts as installed.
    monkeypatch.setattr(bootstrap, "_version_of", lambda b: "99.0.0")
    assert bootstrap._resolves_on_path() is True


def test_no_uv_or_pipx_warns_instead_of_silently_continuing(monkeypatch):
    from probe.cli import bootstrap

    monkeypatch.setattr(bootstrap, "_resolves_on_path", lambda: False)
    monkeypatch.setattr(bootstrap.shutil, "which", lambda _: None)
    result = bootstrap.ensure_persistent_install()
    assert result.installed is False
    assert "neither uv nor pipx" in result.message
    assert "probe doctor" in result.message


def test_never_falls_back_to_bare_pip(monkeypatch):
    """On a researcher's machine bare pip usually means conda or system Python,
    and mutating that to run an installer breaks training runs days later."""
    from probe.cli import bootstrap

    monkeypatch.setattr(bootstrap, "_resolves_on_path", lambda: False)
    monkeypatch.setattr(bootstrap.shutil, "which", lambda _: None)
    result = bootstrap.ensure_persistent_install()
    assert "pip install" not in result.message


def test_setup_is_still_a_working_alias_for_wizard():
    """`probe setup` is on the live connect page and in shipped plugin copy.
    It is the SAME callable, so the alias can never lose a flag."""
    from probe.cli.main import app

    names = {c.name for c in app.registered_commands}
    assert {"wizard", "setup"} <= names
    by_name = {c.name: c for c in app.registered_commands}
    assert by_name["setup"].callback is by_name["wizard"].callback


def test_installing_a_plugin_tells_you_to_restart_claude_code():
    """Plugins and the MCP are read at session start, and `probe` cannot restart
    Claude Code. Without this the wizard says "done" and nothing works in the
    session the user is sitting in — the last mile of the exact problem this
    feature exists to solve."""
    fresh = _caps(claude_available=True)
    turning_on = setup.Selection(tracking=True, capture=False, auto_update=False, agent_rules=False)
    notice = setup.restart_notice(fresh, turning_on)
    assert notice and any("Restart Claude Code" in line for line in notice)
    # ...but a machine with no agent CLI has nothing to restart: the degraded
    # install already printed the install-agent-and-re-run recovery, and
    # restart guidance there reads as success for work that never ran.
    assert setup.restart_notice(_caps(), turning_on) == []


def test_capture_alone_also_needs_a_restart():
    notice = setup.restart_notice(
        _caps(claude_available=True),
        setup.Selection(tracking=False, capture=True, auto_update=False, agent_rules=False),
    )
    assert notice


def test_pi_capture_restart_notice_names_pi_not_claude_code():
    """REGRESSION: `agent = "Codex" if ... else "Claude Code"` used to fire
    here whenever a pi capture pairing changed a plugin_changed-worthy amount
    -- there is no `pi_available` capability field to gate the old
    codex_available/claude_available check on, so the branch fell straight
    through to "Restart Claude Code", telling a researcher who just paired
    pi's capture token to go restart a different agent entirely."""
    notice = setup.restart_notice(
        _caps(agent_source="pi", claude_available=False, codex_available=False),
        setup.Selection(tracking=False, capture=True, auto_update=False, agent_rules=False),
    )
    assert notice
    joined = " ".join(notice)
    assert "Claude Code" not in joined
    assert "Codex" not in joined
    assert "pi" in joined.lower()


def test_pi_capture_off_restart_notice_is_direction_aware():
    """REGRESSION: the pi branch used to return the SAME "restart to take
    effect" line regardless of direction, which is backwards when capture
    just turned OFF -- `apply_capture`'s teardown (`turn_off`) has already
    stopped any capture daemons and set the killswitch synchronously, so
    there is no pi session state left for a restart to pick up."""
    notice = setup.restart_notice(
        _caps(
            agent_source="pi",
            claude_available=False,
            codex_available=False,
            capture_plugin_installed=True,
            capture_token_sources=(TokenSource.PAIRED_FILE,),
        ),
        setup.Selection(tracking=False, capture=False, auto_update=False, agent_rules=False),
    )
    assert notice, "capture visibly changed; the line must say so, not go silent"
    joined = " ".join(notice)
    assert "take effect" not in joined, "nothing is pending a restart on the OFF direction"
    assert "off" in joined.lower()


def test_codex_capture_restart_notice_explains_hook_trust_boundary():
    notice = setup.restart_notice(
        _caps(agent_source="codex", codex_available=True),
        setup.Selection(tracking=False, capture=True, auto_update=False, agent_rules=False),
    )
    # Each line is one bullet, so the hook approval and its consequence are
    # separately readable rather than the tail of a paragraph.
    assert notice
    joined = " ".join(notice)
    assert "/hooks" in joined
    assert "capture is installed but sends nothing" in joined
    assert all(len(line) <= 80 for line in notice), f"a bullet ran long: {notice}"


def test_retiring_legacy_codex_tap_requires_a_restart_even_when_capture_stays_on():
    caps = _caps(
        agent_source="codex",
        codex_available=True,
        capture_plugin_installed=True,
        legacy_capture_plugin_installed=True,
        capture_token_sources=(TokenSource.PAIRED_FILE,),
        capture_credential_valid=True,
    )
    selection = setup.Selection(tracking=False, capture=True, auto_update=False, agent_rules=False)
    assert setup.restart_notice(caps, selection)


def test_an_auto_update_only_change_does_not_send_you_off_to_restart():
    """No plugin moved, so there is nothing for a restart to pick up."""
    already = _caps(
        tracking_plugin_installed=True,
        logged_in_as="richard@prbe.ai",
        capture_token_sources=(TokenSource.PAIRED_FILE,),
    )
    same_plugins = setup.Selection(tracking=True, capture=True, auto_update=True, agent_rules=False)
    assert setup.restart_notice(already, same_plugins) == []


def test_turning_a_plugin_OFF_also_needs_a_restart():
    already = _caps(
        claude_available=True, tracking_plugin_installed=True, logged_in_as="richard@prbe.ai"
    )
    turning_off = setup.Selection(
        tracking=False, capture=False, auto_update=False, agent_rules=False
    )
    assert setup.restart_notice(already, turning_off)


# --- menu readability ------------------------------------------------------


def test_a_grouping_that_forgot_a_row_is_an_error_not_a_missing_menu_entry():
    """ACTION_GROUPS and ACTION_COPY are separate tables and a row needs both.
    Drift shows up as a menu that quietly has the wrong number of things in it,
    so it is caught where the menu is built rather than left to a reviewer."""
    import probe.cli.actions as actions_mod

    original = actions_mod.ACTION_GROUPS
    try:
        actions_mod.ACTION_GROUPS = original[:-1]  # drop the final group
        with pytest.raises(AssertionError):
            actions_mod.grouped_actions()
    finally:
        actions_mod.ACTION_GROUPS = original


# --- the wizard DOES things, it does not print commands --------------------


def test_every_action_acts_rather_than_printing_a_command():
    """The Update action used to print "Run: probe update" and exit. Bouncing
    the user back to a shell to type a command themselves is exactly the
    failure a wizard exists to remove."""
    import inspect
    import sys

    # NOT `from probe.cli import main` -- probe/cli/__init__.py defines a main()
    # FUNCTION that shadows the submodule of the same name.
    import probe.cli.main  # noqa: F401

    cli_main = sys.modules["probe.cli.main"]

    source = inspect.getsource(cli_main._wizard_session) + inspect.getsource(cli_main._run_wizard_action)
    # The specific regression: a literal instruction to go run something.
    assert 'print("Run:' not in source
    assert "perform_update" in source, "Update must perform the update in-process"
    assert "remove_everything" in source


def test_update_command_is_hidden_but_still_works():
    """Deleting it outright would silently break auto-update on every machine
    whose plugin has not been refreshed — plugins update on the USER's
    schedule, not ours."""
    import sys

    import probe.cli.main  # noqa: F401

    app = sys.modules["probe.cli.main"].app

    by_name = {c.name: c for c in app.registered_commands}
    assert "update" in by_name, "the hook still spawns `probe update`"
    assert by_name["update"].hidden is True, "but it must not be discoverable"


def test_the_wizard_is_the_only_discoverable_entry_point():
    import sys

    import probe.cli.main  # noqa: F401

    app = sys.modules["probe.cli.main"].app

    visible = {c.name for c in app.registered_commands if not c.hidden}
    assert "wizard" in visible
    assert "update" not in visible
    assert "setup" not in visible


def test_perform_update_records_the_attempt(isolate, monkeypatch):
    """A detached auto-update has no terminal, so a recorded attempt is the only
    way a month of silent failures becomes visible."""
    from probe.cli import autoupdate, updater, upgrading

    monkeypatch.setattr(upgrading.updater, "fetch_latest", lambda base: {})
    monkeypatch.setattr(
        upgrading.updater, "detect_install", lambda: updater.Install(updater.Method.EDITABLE)
    )
    monkeypatch.setattr(
        upgrading.updater,
        "upgrade_cli",
        lambda i, c, t: updater.CliResult(
            ran=False, ok=True, changed=False, before=c, after=c, message="skipped"
        ),
    )
    outcome = upgrading.perform_update(base_url="https://x", include_plugin=False)
    assert outcome.ok is True
    assert autoupdate.load().last_attempt is not None


def test_the_auto_update_hook_targets_the_wizard():
    """New plugin versions must not depend on the deprecated command."""
    import pathlib

    hook = pathlib.Path("plugins/probe-research/hooks/version_check.py").read_text()
    assert '"wizard", "--action", "update"' in hook


# --- the wizard is a session, not a one-shot -------------------------------


def test_there_is_an_exit_action():
    from probe.cli.actions import ACTION_COPY, Action

    assert Action.EXIT in ACTION_COPY
    assert ACTION_COPY[Action.EXIT][0] == "Exit"


def test_the_menu_comes_back_after_an_action():
    """Dropping to a shell after one task is the same "go do it yourself"
    failure as printing a command."""
    import inspect
    import sys

    import probe.cli.main  # noqa: F401

    source = inspect.getsource(sys.modules["probe.cli.main"]._wizard_session)
    assert "while True" in source, "the menu must loop"
    assert "run_action_menu" in source, "and re-prompt after each action"


def test_a_flagged_action_does_not_loop_forever():
    """`--action manual` in a script must run once and exit."""
    import inspect
    import sys

    import probe.cli.main  # noqa: F401

    source = inspect.getsource(sys.modules["probe.cli.main"]._wizard_session)
    assert "if not looping:" in source


def test_an_ephemeral_uvx_env_is_not_mistaken_for_a_pip_install(monkeypatch):
    """`npx probe-research` runs us from uv's CACHE, which has no pip. Falling
    through to Method.PIP made the upgrade die with "No module named pip" —
    while there was nothing to upgrade anyway, since the env is discarded."""
    from pathlib import Path

    from probe.cli import updater

    monkeypatch.setattr(
        updater,
        "_probe_pkg_dir",
        lambda: Path("/Users/x/.cache/uv/archive-v0/abc123/lib/python3.13/site-packages/probe"),
    )
    assert updater.detect_install().method is updater.Method.EPHEMERAL


def test_an_ephemeral_env_is_never_package_managed(monkeypatch):
    from probe.cli import bootstrap, updater, upgrading, versions

    monkeypatch.setattr(versions, "_installed_cli", None)
    monkeypatch.setattr(bootstrap, "installed_version", lambda: None)
    monkeypatch.setattr(
        upgrading.updater,
        "detect_install",
        lambda: updater.Install(updater.Method.EPHEMERAL),
    )
    monkeypatch.setattr(upgrading.updater, "fetch_latest", lambda base: {})
    monkeypatch.setattr(
        "probe.cli.bootstrap.ensure_persistent_install",
        lambda **_: __import__("probe.cli.bootstrap", fromlist=["x"]).BootstrapResult(
            installed=True, already_persistent=False, message="Installed `probe` (uv tool)."
        ),
    )
    outcome = upgrading.perform_update(base_url="https://x", include_plugin=False)
    blob = " ".join(outcome.lines)
    assert "temporary environment" in blob
    assert "pip" not in blob


def _ephemeral_update(monkeypatch, boot, *, latest=None, installed=(), reinstall=None):
    """Run the npx/uvx Update. `installed` is what `probe --version` reports, in
    order; `reinstall` is what installing @latest returns (and records its spec)."""
    from probe.cli import bootstrap, run_lock, updater, upgrading, versions

    monkeypatch.setattr(versions, "_installed_cli", None)
    monkeypatch.setattr(run_lock, "any_live", lambda: False)
    monkeypatch.setattr(
        upgrading.updater,
        "detect_install",
        lambda: updater.Install(updater.Method.EPHEMERAL),
    )
    manifest = {"cli": {"latest": latest}} if latest else {}
    monkeypatch.setattr(upgrading.updater, "fetch_latest", lambda base: manifest)
    attempts: list = []
    monkeypatch.setattr(upgrading.autoupdate, "record_attempt", attempts.append)
    monkeypatch.setattr(bootstrap, "ensure_persistent_install", lambda **_: boot)
    reads = iter(installed)
    monkeypatch.setattr(bootstrap, "installed_version", lambda: next(reads, None))
    specs: list[str] = []
    monkeypatch.setattr(
        bootstrap, "install_persistent", lambda spec: specs.append(spec) or reinstall
    )
    outcome = upgrading.perform_update(base_url="https://x", include_plugin=False)
    return outcome, attempts[0], specs


def _current():
    from probe.cli import bootstrap

    return bootstrap.BootstrapResult(installed=False, already_persistent=True, message="")


def test_an_ephemeral_update_with_a_current_install_says_so(monkeypatch):
    """It printed "upgrading your installed copy instead" and then nothing, since
    bootstrap has no message for an install that is already current. A promise
    with no outcome after it read as the upgrade having failed."""
    from probe.cli import versions

    outcome, attempt, specs = _ephemeral_update(
        monkeypatch, _current(), latest="5.0.0", installed=["5.0.0"]
    )

    assert outcome.ok and attempt.ok and specs == []
    assert outcome.lines[1:] == [
        "  running from a temporary environment — your installed copy is "
        "already 5.0.0, nothing to upgrade"
    ]
    assert versions.cli_version() == "5.0.0", "the menu grades the installed copy"


def test_a_stale_installed_copy_is_upgraded_not_left_with_advice(monkeypatch):
    """Bootstrap proves only installed >= THIS copy, and a uvx/pipx cache can
    serve an old one. Sending the user back to a shell is what this module
    exists to stop, so it installs @latest itself."""
    from probe.cli import bootstrap

    outcome, attempt, specs = _ephemeral_update(
        monkeypatch,
        _current(),
        latest="5.0.0",
        installed=["4.0.0", "5.0.0"],
        reinstall=bootstrap.BootstrapResult(
            installed=True, already_persistent=False, message="Installed `probe` (uv tool)."
        ),
    )

    assert specs == ["probe-research[all]@latest"]
    assert outcome.lines[1:] == [
        "  running from a temporary environment — upgrading your installed copy "
        "(4.0.0 → 5.0.0)",
        "  Installed `probe` (uv tool).",
    ]
    assert outcome.ok and attempt.ok and attempt.to_version == "5.0.0"


def test_an_install_that_lands_behind_the_latest_is_not_a_success(monkeypatch):
    from probe.cli import bootstrap

    outcome, attempt, _ = _ephemeral_update(
        monkeypatch,
        _current(),
        latest="5.0.0",
        installed=["4.0.0", "4.0.0"],
        reinstall=bootstrap.BootstrapResult(
            installed=True, already_persistent=False, message="Installed `probe` (uv tool)."
        ),
    )

    assert not outcome.ok and not attempt.ok
    assert attempt.detail == "the installed copy is still 4.0.0 after installing 5.0.0"
    assert outcome.lines[-1] == "  the installed copy is still 4.0.0 after installing 5.0.0"


def test_an_install_it_cannot_confirm_is_not_a_success(monkeypatch):
    """Recording it as a success filled in the manifest's latest: doctor said
    "success -> CLI 5.0.0" for a version nobody observed."""
    from probe.cli import bootstrap

    outcome, attempt, _ = _ephemeral_update(
        monkeypatch,
        _current(),
        latest="5.0.0",
        installed=["4.0.0", None],
        reinstall=bootstrap.BootstrapResult(
            installed=True, already_persistent=False, message="Installed `probe` (uv tool)."
        ),
    )

    assert not outcome.ok and not attempt.ok and attempt.to_version is None
    assert outcome.lines[-1] == (
        "  installed, but no `probe` could be found to confirm its version"
    )


def test_a_failed_permanent_install_is_a_failed_update(monkeypatch):
    """It was recorded as a success: doctor said "success -> CLI <latest>" and
    `probe update` exited 0. Its detail is stored, so it is scrubbed, and it
    records no version rather than "still at <latest>"."""
    from probe.cli import bootstrap

    outcome, attempt, _ = _ephemeral_update(
        monkeypatch,
        bootstrap.BootstrapResult(
            installed=False,
            already_persistent=False,
            message="could not install `probe`: EACCES /home/alice/.local/bin",
        ),
        latest="5.0.0",
    )

    assert not outcome.ok and not attempt.ok
    assert outcome.lines[1] == (
        "  running from a temporary environment — installing a permanent copy"
    )
    assert "alice" not in attempt.detail and attempt.detail.startswith("could not install")
    assert "alice" not in outcome.lines[2], "scrubbed on screen too, not only when stored"
    assert attempt.to_version is None


def test_bootstrap_upgrades_an_OLD_install_not_just_a_missing_one(monkeypatch):
    """Existence is not enough: every existing user has an old `probe`, and
    checking only existence left them on it forever while the wizard ran a new
    version ephemerally."""
    from probe.cli import bootstrap

    monkeypatch.setattr(bootstrap, "_installed_binary", lambda: "/usr/local/bin/probe")
    monkeypatch.setattr(bootstrap, "_version_of", lambda b: "0.8.2")
    assert bootstrap._resolves_on_path() is False

    monkeypatch.setattr(bootstrap, "_version_of", lambda b: "99.0.0")
    assert bootstrap._resolves_on_path() is True


def test_a_failed_approval_does_not_claim_the_install_finished():
    """ "Restart Claude Code to finish" after a FAILED approval reads as success.
    The user restarts, finds the capability off, and has no idea why."""
    import inspect
    import sys

    import probe.cli.main  # noqa: F401

    source = inspect.getsource(sys.modules["probe.cli.main"]._run_wizard_action)
    # The restart notice must be reachable only when nothing is missing.
    assert "missing = [grant for grant in needs if grant not in granted]" in source
    assert "if missing:" in source
    assert "Not finished" in source
    # And it must sit in the else branch, not unconditionally after authorize().
    after = source.split("if missing:")[1]
    assert "restart_notice" in after, "the notice must be gated on success"


def test_authorize_result_is_used_not_discarded():
    """The bug was that authorize()'s return value was thrown away with `_`,
    so nothing downstream could tell success from failure."""
    import inspect
    import sys

    import probe.cli.main  # noqa: F401

    source = inspect.getsource(sys.modules["probe.cli.main"]._run_wizard_action)
    assert "granted, auth_messages = wizard.authorize(" in source
    assert "_, auth_messages = wizard.authorize(" not in source


def test_noop_wizard_rerun_still_refreshes_server_snapshot(monkeypatch):
    import sys

    import probe.cli.main  # noqa: F401
    from probe.cli.actions import Action

    cli_main = sys.modules["probe.cli.main"]
    caps = _caps(
        tracking_plugin_installed=True,
        logged_in_as="richard@prbe.ai",
        auto_update_enabled=True,
    )
    seen = []
    monkeypatch.setattr(
        cli_main,
        "_register_local_capabilities",
        lambda current, **kwargs: seen.append((current, kwargs["settings"])) or [],
    )

    lines = cli_main._run_wizard_action(
        Action.CONFIGURE,
        caps=caps,
        base_now="https://api.test",
        yes=True,
        tracking=True,
        capture=False,
        auto_update=True,
        agent_rules=False,
        uninstall=False,
        configured=True,
    )

    assert lines == ["Already set up the way you asked. Nothing to change."]
    assert seen[0][0] is caps
    assert seen[0][1].base_url == "https://api.test"


def test_update_publishes_to_the_explicit_wizard_backend(monkeypatch):
    import sys
    from types import SimpleNamespace

    import probe.cli.main  # noqa: F401
    from probe.cli import doctor
    from probe.cli.actions import Action

    cli_main = sys.modules["probe.cli.main"]
    updated_caps = _caps(tracking_plugin_installed=True)
    seen = []
    monkeypatch.setattr(
        "probe.cli.upgrading.perform_update",
        lambda **kwargs: SimpleNamespace(lines=["updated"], restart_needed=False),
    )
    monkeypatch.setattr(doctor, "collect", lambda: updated_caps)
    monkeypatch.setattr(
        cli_main,
        "_register_local_capabilities",
        lambda current, **kwargs: seen.append((current, kwargs["settings"])) or [],
    )

    lines = cli_main._run_wizard_action(
        Action.UPDATE,
        caps=_caps(),
        base_now="https://self-hosted.test",
        yes=True,
        tracking=None,
        capture=None,
        auto_update=None,
        agent_rules=None,
        uninstall=False,
        configured=False,
    )

    assert lines == ["updated"]
    assert seen[0][0] is updated_caps
    assert seen[0][1].base_url == "https://self-hosted.test"


def _update_action(monkeypatch, caps):
    """Run the UPDATE action against a stubbed updater, returning (lines, calls).

    `calls` records every apply_agent_rules invocation, so a test can assert the
    block was left ALONE as easily as it can assert it was rewritten.
    """
    import sys
    from types import SimpleNamespace

    import probe.cli.main  # noqa: F401
    from probe.cli import doctor, setup
    from probe.cli.actions import Action

    cli_main = sys.modules["probe.cli.main"]
    calls = []
    monkeypatch.setattr(
        "probe.cli.upgrading.perform_update",
        lambda **kwargs: SimpleNamespace(lines=["updated"], restart_needed=False),
    )
    monkeypatch.setattr(doctor, "collect", lambda: _caps())
    monkeypatch.setattr(cli_main, "_register_local_capabilities", lambda *a, **k: [])
    monkeypatch.setattr(
        setup,
        "apply_agent_rules",
        lambda want, **kwargs: calls.append((want, kwargs)) or ["refreshed"],
    )

    lines = cli_main._run_wizard_action(
        Action.UPDATE,
        caps=caps,
        base_now="https://api.test",
        yes=True,
        tracking=None,
        capture=None,
        auto_update=None,
        agent_rules=None,
        uninstall=False,
        configured=False,
    )
    return lines, calls


def test_update_refreshes_a_stale_pointer_block(monkeypatch):
    """The one copy no release can reach.

    POINTER_BODY ships inside the CLI, but the block it wrote lives in the
    researcher's home directory. Before this, UPDATE upgraded the CLI and left
    the block on whatever version it was first written at -- so a wording fix
    reached only machines that happened to re-run the CONFIGURE path.
    """
    lines, calls = _update_action(monkeypatch, _caps(agent_rules_stale=True))

    assert calls == [(True, {"stale": True})]
    assert "refreshed" in lines


def test_update_does_not_install_a_pointer_block_that_was_never_wanted(monkeypatch):
    """Declining the block must survive an upgrade.

    `agent_rules_stale` is `is_installed() and not is_current()`, so a machine
    that never took the block reads as not-stale. Refreshing on anything looser
    would write into a researcher's CLAUDE.md they deliberately kept clean.
    """
    _, calls = _update_action(monkeypatch, _caps(agent_rules_installed=False))

    assert calls == []


def test_uninstall_preserves_token_and_explicit_backend_for_final_snapshot(
    monkeypatch,
):
    import sys

    import probe.cli.main  # noqa: F401
    from probe.cli import doctor, setup
    from probe.cli.actions import Action
    from probe.sdk.config import Settings

    cli_main = sys.modules["probe.cli.main"]
    before = _caps(tracking_plugin_installed=True)
    after = _caps()
    seen = []
    monkeypatch.setattr(
        cli_main,
        "resolve",
        lambda **kwargs: Settings(
            base_url=kwargs["base_url"],
            token="preserved-api-secret",
        ),
    )
    monkeypatch.setattr(setup, "remove_everything", lambda caps: ["removed"])
    monkeypatch.setattr(doctor, "collect", lambda: after)
    monkeypatch.setattr(
        cli_main,
        "_register_local_capabilities",
        lambda current, **kwargs: seen.append((current, kwargs["settings"])) or [],
    )

    lines = cli_main._run_wizard_action(
        Action.UNINSTALL,
        caps=before,
        base_now="https://self-hosted.test",
        yes=True,
        tracking=None,
        capture=None,
        auto_update=None,
        agent_rules=None,
        uninstall=True,
        configured=True,
    )

    assert lines == ["removed"]
    assert seen[0][0] is after
    assert seen[0][1].base_url == "https://self-hosted.test"
    assert seen[0][1].token == "preserved-api-secret"


# --- the wizard is a screen, not a transcript ------------------------------


def test_escape_is_distinct_from_ctrl_c():
    """ "Go back one step" and "abandon the whole wizard" are different
    intentions. Collapsing both to None would make Escape quit."""
    from probe.cli import tui

    assert tui.BACK is not None
    import inspect

    assert "escape" in inspect.getsource(tui.bind_escape)


def test_clearing_never_fires_on_a_pipe(monkeypatch, capsys):
    """Escape codes in a CI log or a captured pipe are noise, and there is no
    screen to clear anyway."""
    from probe.cli import tui

    monkeypatch.setattr(tui, "interactive", lambda: False)
    tui.clear()
    assert capsys.readouterr().out == ""


def test_selected_is_green_and_the_highlight_is_not_inverted():
    """The default inverts a whole entry into a block of background colour,
    which on a three-line choice paints three solid lines."""
    from probe.cli import tui

    rules = {name: style for name, style in tui.style().style_rules}
    assert "noreverse" in rules["highlighted"]
    assert "#00af5f" in rules["selected"]


def test_checkmarks_replace_the_dots():
    from probe.cli import tui
    from questionary.prompts import common

    tui.use_checkmarks()
    assert common.INDICATOR_SELECTED == "✔"


def test_ctrl_c_and_back_stay_distinct_coming_out_of_the_confirm_screen(monkeypatch):
    """ "I chose wrong" and "get me out" must not collapse into each other —
    one rewinds to the agent screen, the other ends the wizard. The confirm
    screen reports them as distinct values and `wizard()` routes on that."""
    from probe.cli import tui

    monkeypatch.setattr(tui, "ask", lambda question, height=None, header=None, **kwargs: None)
    assert setup.run_confirm_install(("claude_code",)) is None

    monkeypatch.setattr(tui, "ask", lambda question, height=None, header=None, **kwargs: tui.BACK)
    assert setup.run_confirm_install(("claude_code",)) is tui.BACK

    monkeypatch.setattr(tui, "ask", lambda question, height=None, header=None, **kwargs: True)
    assert setup.run_confirm_install(("claude_code",)) is True


@pytest.mark.parametrize("selected_sources", [("claude_code",), ("claude_code", "codex")])
def test_install_is_a_verb_that_skips_the_action_menu(monkeypatch, selected_sources):
    """`npx probe-research install` is the sentence someone types when they
    have already decided, and the launcher forwards its arguments verbatim --
    so the verb has to exist on the CLI or it reaches typer as an unknown
    command and exits 2.

    Asserted on where it LANDS, not on the alias's existence: it has to reach
    the configure action without showing the action menu first.
    """
    import os
    import sys
    from types import SimpleNamespace

    from typer.testing import CliRunner

    from probe.cli import bootstrap
    from probe.cli import doctor as doctor_impl
    from probe.cli import plugin_cli
    from probe.cli import setup as wizard
    from probe.cli import tui
    import probe.cli.main  # noqa: F401

    cli_main = sys.modules["probe.cli.main"]
    monkeypatch.setattr(bootstrap, "ensure_persistent_install", lambda **_: SimpleNamespace(message=""))
    monkeypatch.setattr(plugin_cli, "available", lambda _source: True)
    monkeypatch.setattr(
        doctor_impl,
        "collect",
        lambda: _caps(agent_source=os.environ.get("PROBE_AGENT", "claude_code")),
    )
    monkeypatch.setattr(wizard, "interactive", lambda: True)
    monkeypatch.setattr(tui, "clear", lambda: None)
    monkeypatch.setattr(tui, "page", lambda *args, **kwargs: None)

    seen: list[str] = []
    bars: list[str] = []

    def no_menu(_caps):
        seen.append("action-menu")
        raise AssertionError("`install` must not open the action menu")

    monkeypatch.setattr(wizard, "run_action_menu", no_menu)
    monkeypatch.setattr(
        wizard, "run_agent_menu", lambda _d, action=None: seen.append("agents") or selected_sources
    )
    monkeypatch.setattr(wizard, "run_backfill_offer", lambda _s, **kw: set())
    monkeypatch.setattr(
        wizard, "run_confirm_install", lambda *a, **k: seen.append("confirm") or True
    )

    def apply(*args, **kwargs):
        seen.append("apply")
        header = kwargs["progress_header"](0.0)
        assert "Step 3 of 4" in header[0]
        assert "━" in header[1] and "─" in header[1]
        bars.append(header[1])
        return []

    monkeypatch.setattr(cli_main, "_run_wizard_action", apply)

    result = CliRunner().invoke(cli_main.app, ["install"])

    assert result.exit_code == 0, result.output
    assert "action-menu" not in seen, seen
    assert seen == ["agents", "confirm", *["apply"] * len(selected_sources)], seen
    assert [bar.count("━") for bar in bars] == sorted({bar.count("━") for bar in bars})


def test_install_takes_the_same_flags_as_the_wizard():
    """A thin alias is only useful if `--yes` and the capability flags still
    work; a scripted `npx probe-research install --yes --no-capture` is the
    whole point of having the verb."""
    import sys

    from typer.main import get_command

    import probe.cli.main  # noqa: F401
    from probe.cli.capabilities import Capability

    group = get_command(sys.modules["probe.cli.main"].app)
    assert "install" in group.commands, "the launcher forwards this verb verbatim"

    params = {p.name for p in group.commands["install"].params}
    for capability in Capability:
        assert capability.value in params, f"install cannot set --{capability.value}"
    assert "yes" in params and "agent" in params


def test_every_capability_is_reachable_as_a_flag():
    """The wizard's own contract: "Every capability is also a flag". Only the
    flags work headlessly, and agent_rules writes to a file OUTSIDE the repo --
    `--yes` on a fresh machine must have a way to decline it."""
    import inspect
    import sys

    import probe.cli.main  # noqa: F401
    from probe.cli.capabilities import Capability

    cli_main = sys.modules["probe.cli.main"]
    params = inspect.signature(cli_main.wizard).parameters
    for capability in Capability:
        assert capability.value in params, f"no --{capability.value.replace('_', '-')} flag"


def test_the_agent_rules_flag_actually_parses(monkeypatch):
    """A signature check proves the parameter exists, not that typer spells the
    option the way a user types it -- `--agent-rulez` would pass that one.

    Asserted on the Selection that reaches `plan()`, not on an apply: whether an
    apply fires depends on what this MACHINE already has installed, and a test
    that reads the developer's own ~/.claude is not a test.
    """
    from types import SimpleNamespace

    from typer.testing import CliRunner

    from probe.cli import bootstrap
    from probe.cli import doctor as doctor_impl
    from probe.cli import setup as wizard
    from probe.cli.main import app

    seen: list = []
    monkeypatch.setattr(bootstrap, "ensure_persistent_install", lambda **_: SimpleNamespace(message=""))
    monkeypatch.setattr(doctor_impl, "collect", lambda: _caps())
    monkeypatch.setattr(wizard, "interactive", lambda: False)
    monkeypatch.setattr(wizard, "plan", lambda caps, selection: seen.append(selection) or [])

    for flag, expected in (("--agent-rules", True), ("--no-agent-rules", False)):
        seen.clear()
        result = CliRunner().invoke(app, ["wizard", "--action", "configure", "--yes", flag])
        assert result.exit_code == 0, result.output
        assert seen and seen[0].agent_rules is expected, f"{flag} did not parse"


def test_agent_both_runs_one_shared_authorization_then_configures_each_agent(monkeypatch):
    import sys
    from types import SimpleNamespace

    from typer.testing import CliRunner

    from probe.cli import bootstrap
    from probe.cli import doctor as doctor_impl
    import probe.cli.main  # noqa: F401

    cli_main = sys.modules["probe.cli.main"]

    monkeypatch.setattr(bootstrap, "ensure_persistent_install", lambda **_: SimpleNamespace(message=""))
    monkeypatch.setattr(
        doctor_impl,
        "collect",
        lambda: _caps(agent_source=os.environ.get("PROBE_AGENT", "claude_code")),
    )
    calls: list[dict] = []

    def record(action, **kwargs):
        calls.append({"source": os.environ["PROBE_AGENT"], **kwargs})
        return []

    monkeypatch.setattr(cli_main, "_run_wizard_action", record)
    result = CliRunner().invoke(
        cli_main.app,
        ["wizard", "--agent", "both", "--action", "configure", "--yes"],
    )

    assert result.exit_code == 0, result.output
    assert [call["source"] for call in calls] == ["claude_code", "codex"]
    assert calls[0]["authorization_needs"] == ["api", "mcp", "capture"]
    assert calls[0]["capture_sources"] == ["claude_code", "codex"]
    assert calls[1]["authorization_needs"] is None


def test_adding_codex_to_a_configured_claude_machine_keeps_claude_switched_on(monkeypatch):
    """The second-agent install must not arrive with every box unticked.

    Everyone who set up Claude Code before Codex existed hits this path, and
    the wizard used to derive its preselection from the INTERSECTION of the two
    agents' state. Claude Code has everything, a fresh Codex has nothing, so
    every capability read as off -- and an off box is not neutral here: the
    apply path turns it into "remove the CLI + MCP plugin" and "turn Session
    capture off" against the agent that has them. Accepting the defaults tore
    down a working install on the way to adding a second agent.
    """
    import sys
    from types import SimpleNamespace

    from typer.testing import CliRunner

    from probe.cli import bootstrap
    from probe.cli import doctor as doctor_impl
    import probe.cli.main  # noqa: F401

    cli_main = sys.modules["probe.cli.main"]

    configured_claude = _caps(
        agent_source="claude_code",
        tracking_plugin_installed=True,
        capture_plugin_installed=True,
        capture_token_sources=(TokenSource.PAIRED_FILE,),
        agent_rules_installed=True,
        auto_update_enabled=True,
        logged_in_as="richard@prbe.ai",
    )
    fresh_codex = _caps(agent_source="codex", logged_in_as="richard@prbe.ai")
    assert configured_claude.capture_on and not fresh_codex.capture_on, "fixture is wrong"

    monkeypatch.setattr(bootstrap, "ensure_persistent_install", lambda **_: SimpleNamespace(message=""))
    monkeypatch.setattr(
        doctor_impl,
        "collect",
        lambda: fresh_codex if os.environ.get("PROBE_AGENT") == "codex" else configured_claude,
    )
    calls: list[dict] = []

    def record(action, **kwargs):
        calls.append({"source": os.environ["PROBE_AGENT"], **kwargs})
        return []

    monkeypatch.setattr(cli_main, "_run_wizard_action", record)
    result = CliRunner().invoke(
        cli_main.app,
        ["wizard", "--agent", "both", "--action", "configure", "--yes"],
    )

    assert result.exit_code == 0, result.output
    assert [call["source"] for call in calls] == ["claude_code", "codex"]
    for call in calls:
        selection = call["selection_override"]
        # Union, not intersection: what the DEVICE already does carries over,
        # and the lagging agent is brought up to it.
        assert selection.tracking is True, f"{call['source']} would lose tracking"
        assert selection.capture is True, f"{call['source']} would lose capture"
        assert selection.agent_rules is True, f"{call['source']} would lose its rules block"
        assert selection.auto_update is True


def test_agent_both_uses_one_dual_agent_uninstall_confirmation(monkeypatch):
    import sys
    from types import SimpleNamespace

    from typer.testing import CliRunner

    from probe.cli import bootstrap
    from probe.cli import doctor as doctor_impl
    from probe.cli import setup as wizard
    import probe.cli.main  # noqa: F401

    cli_main = sys.modules["probe.cli.main"]
    monkeypatch.setattr(bootstrap, "ensure_persistent_install", lambda **_: SimpleNamespace(message=""))
    monkeypatch.setattr(
        doctor_impl,
        "collect",
        lambda: _caps(
            agent_source=os.environ.get("PROBE_AGENT", "claude_code"),
            tracking_plugin_installed=True,
        ),
    )
    monkeypatch.setattr(wizard, "interactive", lambda: True)
    confirmations: list[tuple[str, ...]] = []
    monkeypatch.setattr(
        wizard,
        "confirm_removal",
        lambda sources: confirmations.append(tuple(sources)) or True,
    )
    calls: list[dict] = []
    monkeypatch.setattr(
        cli_main,
        "_run_wizard_action",
        lambda action, **kwargs: calls.append(kwargs) or [],
    )

    result = CliRunner().invoke(
        cli_main.app,
        ["wizard", "--agent", "both", "--action", "uninstall"],
    )

    assert result.exit_code == 0, result.output
    assert confirmations == [("claude_code", "codex")]
    assert len(calls) == 2
    assert all(call["yes"] is True for call in calls)


def test_interactive_wizard_asks_action_then_agent_then_runs_features(monkeypatch):
    import sys
    from types import SimpleNamespace

    from typer.testing import CliRunner

    from probe.cli import bootstrap
    from probe.cli import doctor as doctor_impl
    from probe.cli import plugin_cli
    from probe.cli import setup as wizard
    from probe.cli import tui
    from probe.cli.actions import Action
    import probe.cli.main  # noqa: F401

    cli_main = sys.modules["probe.cli.main"]
    monkeypatch.setattr(bootstrap, "ensure_persistent_install", lambda **_: SimpleNamespace(message=""))
    monkeypatch.setattr(plugin_cli, "available", lambda _source: True)
    monkeypatch.setattr(
        doctor_impl,
        "collect",
        lambda: _caps(agent_source=os.environ.get("PROBE_AGENT", "claude_code")),
    )
    monkeypatch.setattr(wizard, "interactive", lambda: True)
    monkeypatch.setattr(tui, "clear", lambda: None)
    monkeypatch.setattr(tui, "page", lambda *args, **kwargs: None)

    events: list[str] = []
    actions = iter((Action.CONFIGURE, Action.EXIT))

    def choose_action(_caps):
        events.append("action")
        return next(actions)

    def choose_agent(_defaults, action=None):
        events.append("agent")
        return ("codex",)

    def choose_confirm(_sources, **_kwargs):
        events.append("confirm")
        return True

    def run_features(_action, **_kwargs):
        events.append("features")
        return ["done"]

    monkeypatch.setattr(wizard, "run_action_menu", choose_action)
    monkeypatch.setattr(wizard, "run_agent_menu", choose_agent)
    monkeypatch.setattr(wizard, "run_backfill_offer", lambda _s, **kw: set())
    monkeypatch.setattr(wizard, "run_confirm_install", choose_confirm)
    monkeypatch.setattr(cli_main, "_run_wizard_action", run_features)

    result = CliRunner().invoke(cli_main.app, ["wizard"])

    assert result.exit_code == 0, result.output
    assert events[:4] == ["action", "agent", "confirm", "features"]


def _wizard_events(monkeypatch, *, confirms, actions, imports=None, argv=("wizard",)):
    """Drive `probe wizard` through stubbed screens and record what it showed.

    Every screen in the wizard is behind `interactive()`, which every other test
    stubs to False -- so the navigation BETWEEN screens is the part nothing was
    executing. That is where the bug this fixture exists for lived.
    """
    import os
    import sys
    from types import SimpleNamespace

    from typer.testing import CliRunner

    from probe.cli import bootstrap
    from probe.cli import doctor as doctor_impl
    from probe.cli import plugin_cli
    from probe.cli import setup as wizard
    from probe.cli import tui
    import probe.cli.main  # noqa: F401

    cli_main = sys.modules["probe.cli.main"]
    monkeypatch.setattr(bootstrap, "ensure_persistent_install", lambda **_: SimpleNamespace(message=""))
    monkeypatch.setattr(plugin_cli, "available", lambda _source: True)
    monkeypatch.setattr(
        doctor_impl,
        "collect",
        lambda: _caps(agent_source=os.environ.get("PROBE_AGENT", "claude_code")),
    )
    monkeypatch.setattr(wizard, "interactive", lambda: True)
    monkeypatch.setattr(tui, "clear", lambda: None)
    monkeypatch.setattr(tui, "page", lambda *args, **kwargs: None)

    events: list[str] = []
    action_answers = iter(actions)
    confirm_answers = iter(confirms)
    import_answers = iter(imports) if imports is not None else None

    def choose_action(_caps):
        events.append("action")
        return next(action_answers)

    def choose_agent(_defaults, action=None):
        events.append("agent")
        return ("claude_code",)

    def choose_confirm(_sources, **_kwargs):
        events.append("confirm")
        return next(confirm_answers)

    monkeypatch.setattr(wizard, "run_action_menu", choose_action)
    monkeypatch.setattr(wizard, "run_agent_menu", choose_agent)
    monkeypatch.setattr(wizard, "run_confirm_install", choose_confirm)
    def choose_imports(_sources, **kwargs):
        events.append("imports")
        answer = next(import_answers) if import_answers is not None else set()
        return answer

    monkeypatch.setattr(wizard, "run_backfill_offer", choose_imports)

    def apply(*_args, **_kwargs):
        events.append("apply")
        return ["done"]  # non-empty, so the result is PAGED rather than waiting on stdin

    monkeypatch.setattr(cli_main, "_run_wizard_action", apply)

    result = CliRunner().invoke(cli_main.app, list(argv))
    return result, events


def test_back_out_of_confirmation_returns_to_agent_choices(monkeypatch):
    """Back returns to the only choices that precede installation."""
    from probe.cli import tui
    from probe.cli.actions import Action

    result, events = _wizard_events(
        monkeypatch,
        # Back out of the confirm screen once, then install.
        confirms=[tui.BACK, True],
        actions=[Action.CONFIGURE, Action.EXIT],
    )

    assert result.exit_code == 0, result.output
    assert events == [
        "action",
        "agent",
        "confirm",
        "agent",
        "confirm",
        "apply",
        "imports",
        "action",
    ]


def test_back_with_an_agent_flag_lands_on_the_action_menu_not_a_second_agent_step(monkeypatch):
    """`--agent` already answered step 1, so there is no step 1 to go back TO.

    Back from confirmation returns to the action menu.
    """
    from probe.cli import tui
    from probe.cli.actions import Action

    result, events = _wizard_events(
        monkeypatch,
        argv=["wizard", "--agent", "both"],
        confirms=[tui.BACK, True],
        actions=[Action.CONFIGURE, Action.CONFIGURE, Action.EXIT],
    )

    assert result.exit_code == 0, result.output
    assert "agent" not in events, "--agent must not re-open the agent step"
    assert events[:3] == ["action", "confirm", "action"]


def test_back_from_import_choices_returns_to_the_menu_without_reinstalling(monkeypatch):
    from probe.cli import tui
    from probe.cli.actions import Action

    result, events = _wizard_events(
        monkeypatch,
        imports=[tui.BACK],
        confirms=[True],
        actions=[Action.CONFIGURE, Action.EXIT],
    )
    assert result.exit_code == 0, result.output
    assert events == ["action", "agent", "confirm", "apply", "imports", "action"]


def test_interactive_install_is_force_on_even_over_a_killswitch(monkeypatch):
    """D3, pinned from the interactive side: Install means install.

    The menu's Install row (and `probe install`) applies EVERYTHING — a
    killswitched capture included — because the confirm screen just put the
    capture disclosure in front of the user and they pressed Install anyway.
    The other side of the boundary is pinned by the flag tests: an omitted
    flag on a scripted re-run still PRESERVES, so `--yes` in CI can never
    re-enable a refusal (see test_rerun_preserves_capture_when_the_flag_is_
    omitted).
    """
    import os
    import sys
    from types import SimpleNamespace

    from typer.testing import CliRunner

    from probe.cli import bootstrap
    from probe.cli import doctor as doctor_impl
    from probe.cli import plugin_cli
    from probe.cli import setup as wizard
    from probe.cli import tui
    import probe.cli.main  # noqa: F401

    cli_main = sys.modules["probe.cli.main"]
    monkeypatch.setattr(bootstrap, "ensure_persistent_install", lambda **_: SimpleNamespace(message=""))
    monkeypatch.setattr(plugin_cli, "available", lambda _source: True)
    monkeypatch.setattr(
        doctor_impl,
        "collect",
        # The machine that most tests the rule: capture explicitly OFF.
        lambda: _caps(
            agent_source=os.environ.get("PROBE_AGENT", "claude_code"),
            capture_killswitched=True,
            tracking_plugin_installed=True,
            logged_in_as="x@y.z",
        ),
    )
    monkeypatch.setattr(wizard, "interactive", lambda: True)
    monkeypatch.setattr(tui, "clear", lambda: None)
    monkeypatch.setattr(tui, "page", lambda *args, **kwargs: None)
    monkeypatch.setattr(wizard, "run_agent_menu", lambda _d, action=None: ("claude_code",))
    monkeypatch.setattr(wizard, "run_backfill_offer", lambda _s, **kw: set())
    monkeypatch.setattr(wizard, "run_confirm_install", lambda *a, **k: True)

    handed: dict = {}

    def apply(_action, **kwargs):
        handed["selection"] = kwargs.get("selection_override")
        return ["done"]

    monkeypatch.setattr(cli_main, "_run_wizard_action", apply)

    result = CliRunner().invoke(cli_main.app, ["wizard", "--action", "configure"])

    assert result.exit_code == 0, result.output
    assert handed["selection"] == wizard.Selection(
        tracking=True, capture=True, auto_update=True, agent_rules=True
    ), "interactive Install must be force-on, killswitch included"


def test_ctrl_c_on_the_confirm_screen_still_abandons_the_wizard(monkeypatch):
    """Back and Ctrl-C are different intentions and must not collapse into each
    other: one is "I chose wrong", the other is "get me out". None is Ctrl-C."""
    from probe.cli.actions import Action

    result, events = _wizard_events(monkeypatch, confirms=[None], actions=[Action.CONFIGURE])

    assert result.exit_code == 0, result.output
    assert "apply" not in events, "Ctrl-C must not apply anything"
    assert events == ["action", "agent", "confirm"], "and must not re-prompt"


def test_action_menu_state_names_each_detected_agent():
    lines = setup.describe_state(
        {
            "claude_code": _caps(agent_source="claude_code"),
            "codex": _caps(agent_source="codex"),
        }
    )
    assert any("Claude Code" in line for line in lines)
    assert any("Codex" in line for line in lines)


def test_removing_probe_also_takes_the_block_out_of_claude_md(monkeypatch, tmp_path):
    """ "Removed." used to be false outside the repo: the plugin went, the
    credential went, and the global CLAUDE.md kept telling every agent in every
    repository to use the two skills this call had just uninstalled.

    It also pinned `Capabilities.configured` True forever, so a device that had
    removed everything could never look fresh again."""

    from probe.cli import agent_rules, claude_cli

    monkeypatch.setenv("CLAUDE_CONFIG_DIR", str(tmp_path))
    memory = tmp_path / "CLAUDE.md"
    memory.write_text("# mine\n", encoding="utf-8")
    agent_rules.install(memory)
    assert agent_rules.is_installed(memory)

    monkeypatch.setattr(
        setup,
        "turn_off",
        # The real dataclass, not a SimpleNamespace: `remove_everything` reads
        # `plugin_removed`/`verified` off it to decide whether the killswitch
        # marker is still guarding anything, and a stub shaped like the caller's
        # wishes rather than the callee's signature is how the `ok, detail =
        # uninstall_plugin(...)` TypeError survived a passing suite.
        lambda mode: capture.TurnOffResult(
            killswitch_set=True, daemon_stopped=True, plugin_removed=True
        ),
    )
    # A Result, which is what `uninstall_plugin` actually returns. The old stub
    # handed back a 2-tuple, matching the caller's broken unpacking rather than
    # the real signature -- so this test passed for as long as production
    # crashed.
    monkeypatch.setattr(
        setup,
        "uninstall_plugin",
        lambda name: claude_cli.Result(ok=True, detail="removed"),
    )

    messages = setup.remove_everything(_caps(agent_rules_installed=True))

    assert not agent_rules.is_installed(memory), "the block outlived 'Removed.'"
    assert memory.read_text() == "# mine\n", "and the user's own text survived"
    assert any("CLAUDE.md" in m for m in messages), "removal must be reported"


def test_removing_probe_takes_the_codex_mcp_entry_with_it(monkeypatch, tmp_path):
    """The entry we wrote holds a token this removal just orphaned.

    Left behind, Codex keeps a server that lists as configured and answers 401
    on every call. This runs at the END of `remove_everything`, which is why
    the TypeError two lines above it -- `ok, detail = uninstall_plugin(...)` --
    mattered so much: nothing down here ran at all.
    """

    from probe.cli import claude_cli, codex_config

    monkeypatch.setenv("CODEX_HOME", str(tmp_path))
    codex_config.write_mcp_bearer(
        "probe-research", url="https://mcp.research.prbe.ai/mcp", token="probe_pat_x"
    )
    config = tmp_path / "config.toml"
    assert "probe-research" in config.read_text(encoding="utf-8")

    monkeypatch.setattr(
        setup,
        "turn_off",
        # The real dataclass, not a SimpleNamespace: `remove_everything` reads
        # `plugin_removed`/`verified` off it to decide whether the killswitch
        # marker is still guarding anything, and a stub shaped like the caller's
        # wishes rather than the callee's signature is how the `ok, detail =
        # uninstall_plugin(...)` TypeError survived a passing suite.
        lambda mode: capture.TurnOffResult(
            killswitch_set=True, daemon_stopped=True, plugin_removed=True
        ),
    )
    monkeypatch.setattr(
        setup, "uninstall_plugin", lambda name: claude_cli.Result(ok=True, detail="removed")
    )

    messages = setup.remove_everything(_caps(agent_source="codex"))

    assert "probe-research" not in config.read_text(encoding="utf-8")
    assert any("MCP entry" in message for message in messages)


def test_a_stale_block_is_something_to_do_not_nothing_to_change():
    """`plan()` skipped any capability where want == have, and a STALE block is
    installed-and-wrong, so the refresh never made it into the plan: the wizard
    said "Nothing to change" while `probe doctor` said "re-run probe wizard".
    A POINTER_VERSION bump could not reach a machine at all."""
    stale = _caps(agent_rules_installed=True, agent_rules_stale=True)
    keep = setup.Selection(tracking=False, capture=False, auto_update=False, agent_rules=True)

    steps = setup.plan(stale, keep)

    assert steps and "refresh" in steps[0], f"stale block produced no plan: {steps}"
    # And a current block is still a no-op, or every run would rewrite the file.
    current = _caps(agent_rules_installed=True, agent_rules_stale=False)
    assert setup.plan(current, keep) == []


@pytest.mark.tui
def test_every_tui_reference_resolves():
    """The crash that shipped in 0.13.1: `tui.header` was deleted and one of
    its TWO call sites updated. Nothing caught it, because every call sits
    behind `interactive()`, which is False under pytest — so the only path real
    users take is the one with no coverage.

    This is a cheap static stand-in: every `tui.X(` in the package must name
    something `tui` actually defines.
    """
    import pathlib
    import re

    from probe.cli import tui

    src_root = pathlib.Path(tui.__file__).parent
    referenced = set()
    for path in src_root.glob("*.py"):
        referenced |= set(re.findall(r"\btui\.([a-z_]+)\s*\(", path.read_text()))

    missing = sorted(name for name in referenced if not hasattr(tui, name))
    assert not missing, f"tui has no: {missing}"


# --- reading a REAL screen back off a REAL pty ------------------------------
#
# The layout tests below used to be `inspect.getsource` greps -- "is the string
# `full_screen = True` in this function". A grep like that passes with the
# margin set to zero, set negative, or applied to the wrong edge: it certifies
# that a line of code EXISTS, not that a screen looks right. Everything from
# here down renders onto an actual pty and reads the rows back, so "the top two
# rows are blank" is a claim about what a user sees.


class _Screen:
    """The smallest VT100 that can read prompt_toolkit back.

    Not a terminal emulator so much as a transcript of one. prompt_toolkit's
    Vt100 output uses a narrow vocabulary -- SGR, erase-down, erase-line,
    relative cursor moves, CR/LF/BS and text -- so a grid plus those handlers
    reproduces exactly what would be on screen. Sequences outside the
    vocabulary are SKIPPED rather than guessed at: a wrong guess would move the
    cursor silently and every row after it would be fiction.

    Autowrap is off (prompt_toolkit emits `\\x1b[?7l`), so a long line clips at
    the right edge instead of consuming the row below it.
    """

    _CSI = __import__("re").compile(r"\x1b\[([0-9;?<>=!]*)([@-~])")

    def __init__(self, rows: int, cols: int) -> None:
        self.h, self.w = rows, cols
        self.grid = [[" "] * cols for _ in range(rows)]
        self.row = self.col = 0
        self.cursor_visible = True

    def _linefeed(self) -> None:
        if self.row + 1 < self.h:
            self.row += 1
        else:  # the bottom row scrolls, exactly as a terminal would
            self.grid.pop(0)
            self.grid.append([" "] * self.w)

    def _csi(self, params: str, final: str) -> None:
        if params.startswith("?") and final in ("h", "l") and "25" in params[1:].split(";"):
            self.cursor_visible = final == "h"
        if params[:1] in ("?", "<", ">", "=", "!"):
            return  # private modes: cursor visibility, bracketed paste, autowrap
        nums = [int(p) if p else 0 for p in params.split(";")] if params else []
        first = nums[0] if nums else 0
        step = first or 1
        blank = [" "] * self.w
        if final == "A":
            self.row = max(0, self.row - step)
        elif final == "B":
            self.row = min(self.h - 1, self.row + step)
        elif final == "C":
            self.col = min(self.w - 1, self.col + step)
        elif final == "D":
            self.col = max(0, self.col - step)
        elif final == "G":
            self.col = max(0, min(self.w - 1, step - 1))
        elif final in "Hf":
            self.row = max(0, min(self.h - 1, (nums[0] if nums else 1) - 1))
            self.col = max(0, min(self.w - 1, (nums[1] if len(nums) > 1 else 1) - 1))
        elif final == "J":
            if first == 0:
                self.grid[self.row][self.col :] = [" "] * (self.w - self.col)
                for r in range(self.row + 1, self.h):
                    self.grid[r] = list(blank)
            elif first == 1:
                self.grid[self.row][: self.col + 1] = [" "] * (self.col + 1)
                for r in range(self.row):
                    self.grid[r] = list(blank)
            else:
                self.grid = [list(blank) for _ in range(self.h)]
        elif final == "K":
            if first == 0:
                self.grid[self.row][self.col :] = [" "] * (self.w - self.col)
            elif first == 1:
                self.grid[self.row][: self.col + 1] = [" "] * (self.col + 1)
            else:
                self.grid[self.row] = list(blank)
        elif final == "X":
            end = min(self.w, self.col + step)
            self.grid[self.row][self.col : end] = [" "] * (end - self.col)

    def feed(self, data: bytes) -> _Screen:
        text = data.decode("utf8", "replace")
        i, size = 0, len(text)
        while i < size:
            ch = text[i]
            if ch == "\x1b":
                match = self._CSI.match(text, i)
                if match:
                    self._csi(match.group(1), match.group(2))
                    i = match.end()
                    continue
                nxt = text[i + 1] if i + 1 < size else ""
                if nxt == "]":  # OSC, terminated by BEL
                    end = text.find("\x07", i)
                    i = size if end < 0 else end + 1
                    continue
                i += 3 if nxt in "()#" else 2
                continue
            i += 1
            if ch == "\r":
                self.col = 0
            elif ch == "\n":
                self._linefeed()
            elif ch == "\x08":
                self.col = max(0, self.col - 1)
            elif ch == "\t":
                self.col = min(self.w - 1, (self.col // 8 + 1) * 8)
            elif ch >= " " and self.col < self.w:
                self.grid[self.row][self.col] = ch
                self.col += 1
        return self

    def lines(self) -> list[str]:
        return ["".join(row).rstrip() for row in self.grid]

    def dump(self) -> str:
        return "\n".join(f"{i:2d}|{line}|" for i, line in enumerate(self.lines()))


def _leading_blanks(lines: list[str]) -> int:
    return next((i for i, line in enumerate(lines) if line), len(lines))


def _trailing_blanks(lines: list[str]) -> int:
    return _leading_blanks(list(reversed(lines)))


def _assert_framed(screen) -> list[str]:
    """The margin claim, in the form a margin of ZERO cannot satisfy.

    The literal edge assertions carry the weight. `>= 1` alone is
    vacuous at MARGIN == 0 -- "at least zero blank rows" is true of content
    welded to row 0 -- so the depth check is written second, after the two
    claims that hold for any margin worth having. The bottom one also catches
    the other half of the bug: a margin applied to the top edge only.
    """

    lines = screen.lines()
    assert any(lines), f"nothing rendered at all\n{screen.dump()}"
    assert lines[0] == "", f"content is welded to the top row\n{screen.dump()}"
    assert lines[-1] == "", f"content is welded to the bottom row\n{screen.dump()}"
    assert _leading_blanks(lines) >= 1, screen.dump()
    assert _trailing_blanks(lines) >= 1, screen.dump()
    return lines


def _pty_screen(argv, *, rows, cols, keys=b"", boot=20.0, settle=6.0, quiet=0.5, env=None):
    """Run `argv` on a pty of exactly rows x cols; return the final `_Screen`.

    Sizing happens in the PARENT right after the fork. The pty starts at 0x0,
    so the ioctl is a real change and the child gets a SIGWINCH -- it redraws at
    the size we asked for even if it had already rendered once.
    """
    import fcntl
    import os
    import pty
    import select
    import struct
    import termios
    import time

    raw = bytearray()

    def drain(fd, budget, quiet=0.5):
        end, last = time.time() + budget, time.time()
        while time.time() < end:
            if select.select([fd], [], [], 0.1)[0]:
                try:
                    chunk = os.read(fd, 65536)
                except OSError:
                    return False
                if not chunk:
                    return False
                raw.extend(chunk)
                last = time.time()
                if b"\x1b[6n" in chunk:
                    # Answer the cursor-position request. Left unanswered,
                    # prompt_toolkit prints a CPR warning INTO the screen we are
                    # about to measure and every row below it is off by one.
                    try:
                        os.write(fd, b"\x1b[1;1R")
                    except OSError:
                        return False
            elif raw and time.time() - last > quiet:
                return True
        return True

    pid, fd = pty.fork()
    if pid == 0:  # pragma: no cover - child process
        # Screen navigation starts after sign-in. Keep these subprocesses
        # offline: monkeypatches in the parent do not cross an exec boundary.
        child_env = dict(os.environ, TERM="xterm-256color", PROBE_TOKEN="probe_pat_ui_test",
                         PROBE_BASE_URL="http://127.0.0.1:9")
        # xdist exports its log width as COLUMNS. The child owns a differently
        # sized real terminal; inherited dimensions would override its ioctl
        # size in shutil while prompt_toolkit measures the actual terminal.
        child_env.pop("COLUMNS", None)
        child_env.pop("LINES", None)
        child_env.update(env or {})
        os.execve(argv[0], argv, child_env)
    try:
        fcntl.ioctl(fd, termios.TIOCSWINSZ, struct.pack("HHHH", rows, cols, 0, 0))
        if drain(fd, boot) and keys:
            os.write(fd, keys)
            # `quiet` is what decides the whole key burst has been ANSWERED, and
            # a multi-screen walk needs a longer one than a single prompt: the
            # wizard re-collects capabilities between steps, which shells out to
            # the agent CLIs. A gap longer than the quiet window ends the capture
            # on an intermediate screen -- green on an idle box, red on a loaded
            # CI runner, and unreproducible either way.
            drain(fd, settle, quiet=quiet)
    finally:
        for closing in (lambda: os.write(fd, b"\x03"), lambda: os.close(fd)):
            try:
                closing()
            except OSError:
                pass
        try:
            os.waitpid(pid, 0)
        except OSError:
            pass
    return _Screen(rows, cols).feed(bytes(raw))


def _pty_screens(argv, *, rows, cols, bursts, boot=20.0, settle=6.0, quiet=0.5, env=None):
    """One child, one screen per burst -- `_pty_screen` walked N times, minus N-1 spawns.

    `test_every_action_row_is_reachable_on_an_80x24_screen` used to call
    `_pty_screen` once per scroll position: 11 pty forks, 11 Python interpreters,
    11 boot drains. Measured on two cores it was 35.5s, the single most expensive
    test in the suite, and every one of those interpreters was re-importing
    questionary and prompt_toolkit to render a menu that had not changed.

    Here the child starts ONCE and the bursts are sent to it in order. A burst
    still gets its own settle drain, so the quiet-window semantics that make this
    harness trustworthy are unchanged -- the thing removed is process startup.

    Screens come from PREFIXES of the same byte stream: the emulator replays
    bytes, so feeding everything received up to burst i reconstructs exactly what
    was on screen then. `bursts[0]` is normally b"" -- the screen at rest.

    Keys are cumulative, not absolute. Where the old loop sent `_DOWN * i` to a
    fresh menu, this sends one `_DOWN` per burst to a menu already at row i-1.
    Same cursor row, and it exercises continuous scrolling rather than 11 cold
    starts, which is closer to what a person does.
    """
    import fcntl
    import os
    import pty
    import select
    import struct
    import termios
    import time

    raw = bytearray()
    marks: list[int] = []

    def drain(fd, budget, quiet=0.5):
        end, last = time.time() + budget, time.time()
        while time.time() < end:
            if select.select([fd], [], [], 0.1)[0]:
                try:
                    chunk = os.read(fd, 65536)
                except OSError:
                    return False
                if not chunk:
                    return False
                raw.extend(chunk)
                last = time.time()
                if b"\x1b[6n" in chunk:
                    try:
                        os.write(fd, b"\x1b[1;1R")
                    except OSError:
                        return False
            elif raw and time.time() - last > quiet:
                return True
        return True

    pid, fd = pty.fork()
    if pid == 0:  # pragma: no cover - child process
        child_env = dict(os.environ, TERM="xterm-256color", PROBE_TOKEN="probe_pat_ui_test",
                         PROBE_BASE_URL="http://127.0.0.1:9")
        child_env.update(env or {})
        os.execve(argv[0], argv, child_env)
    try:
        fcntl.ioctl(fd, termios.TIOCSWINSZ, struct.pack("HHHH", rows, cols, 0, 0))
        if drain(fd, boot):
            for burst in bursts:
                if burst:
                    os.write(fd, burst)
                    drain(fd, settle, quiet=quiet)
                marks.append(len(raw))
    finally:
        for closing in (lambda: os.write(fd, b"\x03"), lambda: os.close(fd)):
            try:
                closing()
            except OSError:
                pass
        try:
            os.waitpid(pid, 0)
        except OSError:
            pass
    return [_Screen(rows, cols).feed(bytes(raw[:m])) for m in marks]


#: The confirm screen, rendered for real. Nothing is stubbed: this is
#: `run_confirm_install`, which is the screen a new user meets and the one
#: that now carries the capture disclosure.
_RENDER_CONFIRM = """
from probe.cli import setup as wizard

wizard.run_confirm_install(("claude_code",), step=wizard.STEP_CONFIRM)
"""

_HEADER = "Folder: /Users/example/research"


def _confirm_screen(*, rows=24, cols=80, keys=b""):
    import sys

    return _pty_screen([sys.executable, "-c", _RENDER_CONFIRM], rows=rows, cols=cols, keys=keys)


@pytest.mark.tui
def test_the_confirm_screen_shows_the_capture_grant_on_an_80x24_screen():
    """The consent surface, measured on a screen rather than in a token list.

    80x24 is the floor every terminal clears. The picker's checkbox is gone,
    so the disclosure block on this screen is what stands between a fresh user
    and the capture grant -- a row of it below the fold would be agreed to
    unseen, which is exactly why this is asserted and not assumed."""
    screen = _confirm_screen(keys=b"\x1b[6~" * 5)
    text = "\n".join(screen.lines())

    assert "Traceback" not in text, screen.dump()
    # The grant, on screen, named in full, before a single keystroke.
    assert "Session capture" in text, screen.dump()
    assert "Sends this device's" in text, screen.dump()
    assert "team" in text and "search" in text, screen.dump()
    # The way forward and the way back are both on screen.
    assert "Install" in text, screen.dump()
    assert "Back" in text, screen.dump()


#: The account-switch gate, which stands in front of a website install code on
#: a device that already holds a credential.
_RENDER_ACCOUNT_SWITCH = """
from probe.cli import setup as wizard

print("RESULT:", wizard.run_confirm_account_switch("previous.researcher@example.test"))
"""


@pytest.mark.tui
def test_the_account_switch_names_the_replaced_account_on_an_80x24_screen():
    """The account being replaced is on screen before the keystroke that replaces it.

    This gate exists because redeeming a website code is not reversible from
    the CLI -- the exchange detaches the credentials bound to this device -- so
    the email it names is the ONLY thing standing between someone and a silent
    switch. A row of it below the fold is the same as not having asked.
    """
    import sys

    screen = _pty_screen(
        [sys.executable, "-c", _RENDER_ACCOUNT_SWITCH], rows=24, cols=80, settle=12.0, quiet=2.0
    )
    text = "\n".join(screen.lines())

    assert "Traceback" not in text, screen.dump()
    assert "previous.researcher@example.test" in text, screen.dump()
    # What continuing costs, said before the keystroke that pays it.
    assert "the account saved here and releases this device" in text, screen.dump()
    assert "Continue with the account from the website code?" in text, screen.dump()


def _probe_binary():
    """THIS interpreter's probe, not whatever is on PATH — a stale global
    install would make the test report on code that is not under test."""
    import os
    import shutil
    import sys

    probe = str(pathlib.Path(sys.executable).parent / "probe")
    if not os.path.exists(probe):
        probe = shutil.which("probe") or ""
    if not probe or not os.path.exists(probe):
        pytest.skip("no probe binary on this machine")
    return probe


@pytest.mark.tui
def test_the_interactive_wizard_starts_without_crashing():
    """Actually run it on a pty, and walk a step INTO it.

    Every unit test stubs `interactive()` to False, so the branch that renders
    a menu is otherwise never executed. This used to stop at the first frame
    and only grep for "Traceback"; it now drives the pointer down and back up
    (harmless on both the action menu and the capability picker -- neither
    Enter nor Space is ever sent, so nothing installs) and measures the screen
    that comes back.

    The action menu follows authentication. It goes through `tui.ask`, so the
    margin claim holds against the real entry point rather than a rehearsal.
    """
    screen = _pty_screen([_probe_binary(), "wizard"], rows=24, cols=80, keys=b"\x1b[B\x1b[A")
    text = "\n".join(screen.lines())

    assert "Traceback" not in text, screen.dump()
    assert "AttributeError" not in text, screen.dump()
    # The margin, on the real binary rather than a rehearsal of it.
    _assert_framed(screen)


#: Arrow keys, as a real terminal sends them.
_RIGHT, _LEFT, _DOWN, _UP, _ENTER = b"\x1b[C", b"\x1b[D", b"\x1b[B", b"\x1b[A", b"\r"


def _filtered_real_path(*, exclude: tuple[str, ...] = ()) -> str:
    """The real PATH, with any directory carrying a REAL binary named in
    `exclude` dropped from what a stub env appends behind its own stubs.

    A PTY test spawns a genuine subprocess, so detection there cannot be
    monkeypatched the way an in-process test controls `plugin_cli.available`
    -- PATH is the only lever. `_agents_env` below prepends stubs for the
    agents it wants FOUND; without this filter, an agent it wants ABSENT can
    still be found further down the real PATH on a machine that genuinely has
    it installed -- which pi 0.84.3, on the machine this suite was written on,
    is (`which pi` resolves under nvm). Filtered, not merely "hope the stub
    shadows it": a stub only shadows a same-named real binary, and only
    because it is prepended, so "absent" needs the real one gone, not
    merely outranked.
    """
    import os

    kept = []
    for directory in os.environ.get("PATH", "").split(os.pathsep):
        if not directory:
            continue
        if any(os.path.isfile(os.path.join(directory, name)) for name in exclude):
            continue
        kept.append(directory)
    return os.pathsep.join(kept)


#: A PATH whose front carries stub binaries for exactly `present`, with any
#: OTHER agent's real binary filtered out of what is appended behind them
#: (see `_filtered_real_path`) -- so both "found" and "absent" are
#: deterministic on whatever machine runs the test, dev laptop or CI runner
#: alike. The stubs exit 0 saying nothing, which every capability probe
#: treats as its fail-soft answer.
def _agents_env(tmp_path, *present):
    import os
    import stat

    for name in present:
        stub = tmp_path / name
        # The pi stub must answer the impostor sniff (`pi --help` containing
        # "coding" -- see `pi_binary_available`); a bare `exit 0` shim is
        # exactly the unrelated-binary-named-pi case the sniff exists to
        # reject. claude/codex detection is `which`-only, so their stubs
        # don't care what they print.
        stub.write_text(
            '#!/bin/sh\necho "pi - AI coding assistant test stub"\nexit 0\n'
            if name == "pi"
            else "#!/bin/sh\nexit 0\n",
            encoding="utf-8",
        )
        stub.chmod(stub.stat().st_mode | stat.S_IEXEC)
    absent = tuple(name for name in ("claude", "codex", "pi", "kimi") if name not in present)
    real_path = _filtered_real_path(exclude=absent)
    return {"PATH": f"{tmp_path}{os.pathsep}{real_path}"}


#: The agent screen shows only when BOTH marketplace agents are found -- a CI
#: runner has neither while a dev laptop may have either -- so this pins
#: exactly that shape. pi is deliberately left OFF (see `_agents_env`'s
#: filtering): the two tests pinned to a 2-row picker rely on it staying a
#: 2-row picker regardless of whether pi is really installed here too.
def _both_agents_env(tmp_path):
    return _agents_env(tmp_path, "claude", "codex")


#: Action menu -> Install. The cursor opens on the Defaults row, the menu's
#: first; one `↓` reaches `★ Install Probe`, and Enter opens the flow.
# The menu opens on Defaults' first row, Who records; Install is two rows down.
# (Never ←/→ there: that switches who records, at once.)
_TO_INSTALL = _DOWN + _DOWN + _ENTER


@pytest.mark.tui
def test_an_empty_agent_step_refuses_to_advance_and_says_why(tmp_path):
    """ "At least one agent" used to be questionary's `validate=`, which only ever
    runs on questionary's submit — the exact path the enter-activates-the-row
    binding replaces. So the guard was live on a code path the wizard no longer
    took, and Next on an empty selection would have been a key that silently did
    nothing.

    It is enforced on the Next row now, and the row says so where you are
    pressing it.
    """
    # Enter opens the agent step. The cursor lands on `Next ›`, so reaching the
    # agents is `↑` -- once to the last one, again to the first -- and Enter on
    # each unticks it. Then → asks to continue with nothing chosen.
    screen = _pty_screen(
        [_probe_binary(), "wizard"],
        rows=26,
        cols=88,
        keys=_TO_INSTALL + _UP + _ENTER + _UP + _ENTER + _RIGHT,
        settle=30.0,
        quiet=3.0,
        env=_both_agents_env(tmp_path),
    )
    text = "\n".join(screen.lines())

    assert "Traceback" not in text, screen.dump()
    assert "Step 1 of 4" in text, f"an empty selection advanced anyway\n{screen.dump()}"
    assert "choose at least one agent" in text, screen.dump()


def test_an_empty_agent_answer_never_reaches_the_caller(monkeypatch):
    """The REAL degraded path, and the crash it caused.

    Every reach into questionary is guarded so a library reshuffle downgrades
    the prompt instead of breaking it. `checkbox_control()` returning None is
    that condition — and it is all-or-nothing: `_wire_picker` then installs NO
    bindings, so questionary's own enter-submits wins and `can_submit` (the
    Next-row guard) never runs at all.

    The old `validate=` covered exactly that path and was deleted as redundant
    when the guard moved onto the Next row. It was not redundant: with both
    gone, an empty selection submitted, `run_agent_menu` returned `()`, and
    `wizard()` read `agent_sources[0]` — IndexError, whole command dead, on the
    one path the guards exist to keep survivable.

    Asserted at the boundary rather than on the validator, so it holds however
    the guard is spelled.
    """
    from probe.cli import setup as wizard
    from probe.cli import tui

    # Pinned rather than left to this machine's real PATH: `run_agent_menu`
    # builds its row set from `detectable_sources()` now, and this test calls
    # it directly, bypassing the `len(available_sources) > 1` gate that
    # normally guarantees a non-empty picker. What this test actually checks
    # -- an empty ANSWER never reaching the caller -- does not depend on which
    # sources are offered, but pinning it keeps the test deterministic rather
    # than accidentally exercising a zero-row picker on a machine with
    # neither claude, codex, nor pi installed.
    monkeypatch.setattr(wizard, "detectable_sources", lambda: ("claude_code", "codex"))
    # The one condition every guard in this module exists for.
    monkeypatch.setattr(tui, "checkbox_control", lambda question: None)
    monkeypatch.setattr(tui, "ask", lambda question, height=None, header=None, **kwargs: [])

    answer = wizard.run_agent_menu(("claude_code",))

    assert answer is not None and answer != (), (
        "an empty answer reached the caller; wizard() indexes [0] on this"
    )
    assert answer is tui.BACK, "an answer of nothing is a non-answer, not a selection"


def test_the_wizard_survives_the_no_bindings_fallback_end_to_end(monkeypatch):
    """The same crash, asserted through the real command instead of the seam.

    The boundary test above pins `run_agent_menu`'s contract; this one proves
    the contract is the one `wizard()` actually needs. It runs the REAL agent
    step with questionary's control unreachable and an empty submit, and the
    command has to come back rather than die three frames up in
    `caps_by_source[agent_sources[0]]`.
    """
    import os
    import sys
    from types import SimpleNamespace

    from typer.testing import CliRunner

    from probe.cli import bootstrap
    from probe.cli import doctor as doctor_impl
    from probe.cli import plugin_cli
    from probe.cli import setup as wizard
    from probe.cli import tui
    from probe.cli.actions import Action
    import probe.cli.main  # noqa: F401

    cli_main = sys.modules["probe.cli.main"]
    monkeypatch.setattr(bootstrap, "ensure_persistent_install", lambda **_: SimpleNamespace(message=""))
    monkeypatch.setattr(plugin_cli, "available", lambda _source: True)
    monkeypatch.setattr(
        doctor_impl,
        "collect",
        lambda: _caps(agent_source=os.environ.get("PROBE_AGENT", "claude_code")),
    )
    monkeypatch.setattr(wizard, "interactive", lambda: True)
    monkeypatch.setattr(tui, "clear", lambda: None)
    monkeypatch.setattr(tui, "page", lambda *args, **kwargs: None)
    # The degraded condition, and an empty answer submitted through it.
    monkeypatch.setattr(tui, "checkbox_control", lambda question: None)
    monkeypatch.setattr(tui, "ask", lambda question, height=None, header=None, **kwargs: [])

    actions = iter((Action.CONFIGURE, Action.EXIT))
    monkeypatch.setattr(wizard, "run_action_menu", lambda _caps: next(actions))

    result = CliRunner().invoke(cli_main.app, ["wizard"])

    assert result.exit_code == 0, result.output
    assert "IndexError" not in result.output, result.output


@pytest.mark.tui
def test_the_agent_step_keeps_a_validator_for_the_no_bindings_fallback():
    """The guard above has two locks and this one names the first.

    `validate=` looks like dead weight — our Enter binding never reaches
    questionary's submit — so the next reader to notice that will delete it.
    This says why it stays: it is the ONLY guard left when the bindings are
    never installed.
    """
    import inspect

    source = inspect.getsource(setup.run_agent_menu)
    assert "validate=" in source, "the fallback path has no guard left"


def _promises_an_install(text: str) -> bool:
    """Does this copy say `install` where `uninstall` is not what it said?"""
    import re

    return "nstall" in re.sub(r"uninstall", "", text, flags=re.IGNORECASE).lower()


def test_every_action_that_reaches_the_agent_step_says_what_it_is():
    """A new Action defaults into the neutral copy, never the install's.

    The picker's gate in `wizard()` is stated as a pair of exclusions, so an
    action added to neither `IMPORT_ACTIONS` nor `DEVICE_ACTIONS` reaches this
    screen by DEFAULT -- silently, with no edit here. That is how the install
    copy came to sit on top of uninstall in the first place. Derived from the
    enum rather than listed, so the guard cannot go stale the way the screen
    did.
    """
    from probe.cli.actions import DEVICE_ACTIONS, IMPORT_ACTIONS, Action

    reachable = {
        action
        for action in Action
        if action not in IMPORT_ACTIONS
        and action not in DEVICE_ACTIONS
        and action is not Action.EXIT
    }
    assert reachable, "the gate this guard mirrors has stopped selecting anything"
    missing = reachable - set(setup.AGENT_SCREEN_COPY)
    assert not missing, f"no agent-step copy for {sorted(missing)} — it will read as generic"
    assert reachable <= set(setup.AGENT_ROW_DETAIL_BY_ACTION), "rows fall back to generic copy"

    # The row detail is keyed on BOTH axes, and the second one drifts the same
    # way: a fourth coding agent added to `INSTALLABLE_AGENT_SOURCES` gets a row
    # on every one of these screens, and would fall to the generic line on all
    # but whichever table someone remembered.
    sources = set(setup.INSTALLABLE_AGENT_SOURCES)
    for action, detail in setup.AGENT_ROW_DETAIL_BY_ACTION.items():
        assert sources <= set(detail), (
            f"{action} has no row detail for {sorted(sources - set(detail))}"
        )


def test_the_agent_step_falls_back_without_reaching_for_the_install_copy():
    """The two fallbacks, which are opposites and must stay so.

    `None` means "the caller did not say", and the only callers that do not are
    direct ones -- the install flow this screen was built for -- so it gets the
    install. An action the table does not KNOW is the other case entirely: it is
    a new action nobody has come here to describe, and handing it the install's
    copy is how a screen ends up promising the opposite of what it does. It gets
    copy that names no action at all.
    """
    assert setup.agent_screen_copy(None) == setup.AGENT_SCREEN_COPY["configure"]
    assert setup.agent_row_detail(None, "pi") == setup.AGENT_ROW_DETAIL["pi"]

    assert setup.agent_screen_copy("not-an-action") == setup.GENERIC_AGENT_SCREEN_COPY
    assert setup.agent_row_detail("not-an-action", "pi") == setup.GENERIC_AGENT_ROW_DETAIL
    # A source the action's own table has no line for -- a fourth coding agent
    # added to `detectable_sources()` before the copy tables hear about it.
    assert setup.agent_row_detail("uninstall", "some-new-agent") == setup.GENERIC_AGENT_ROW_DETAIL

    # And neither fallback may leak the install into a screen that is not one.
    assert not _promises_an_install(" ".join(setup.GENERIC_AGENT_SCREEN_COPY))
    assert not _promises_an_install(" ".join(setup.GENERIC_AGENT_ROW_DETAIL))


def test_only_the_install_promises_an_install_on_the_agent_step():
    """Every string this screen can draw, checked as copy rather than as a
    render: the title, the lede, the question, and every row's detail."""
    from probe.cli.actions import Action

    for action, copy in setup.AGENT_SCREEN_COPY.items():
        if action == Action.CONFIGURE:
            continue
        detail = setup.AGENT_ROW_DETAIL_BY_ACTION.get(action, {})
        blob = " ".join((*copy, *(line for lines in detail.values() for line in lines)))
        assert not _promises_an_install(blob), f"{action} offers to install: {blob}"


import pathlib  # noqa: E402  (used by the pty test above)


def test_every_prompt_in_the_wizard_uses_shared_sections():
    """One step used to print its detail and render a bare confirm underneath,
    so prompt_toolkit took a screen that already had two lines on it and the
    whole step sat welded to the top while every other step was centred.

    A prompt cannot be centred without a counted height, and it cannot own its
    own layout unless the whole block is handed to it as the message.
    """
    import inspect

    from probe.cli import setup as wizard

    for prompt in (
        wizard.run_agent_menu,
        wizard.run_confirm_install,
        wizard.run_action_menu,
        wizard.run_settings_menu,
        wizard.run_confirm_account_switch,
    ):
        source = inspect.getsource(prompt)
        assert "tui.framed(" in source, f"{prompt.__name__} must hand the block to the prompt"
        assert "height=tui.content_height(" in source, f"{prompt.__name__} renders uncentred"


def test_the_wizard_never_drops_to_a_bare_prompt():
    """`typer.confirm` prints at column 0 with no page around it — and the one
    that guarded uninstall was the single destructive action in the product."""
    import inspect
    import sys

    import probe.cli.main  # noqa: F401

    assert "typer.confirm" not in inspect.getsource(
        sys.modules["probe.cli.main"]._run_wizard_action
    )


def test_piped_output_stays_flush_left(monkeypatch, capsys):
    """An indent in a log is noise every grep has to strip, and CI is the one
    consumer that never sees the layout."""
    from probe.cli import tui

    monkeypatch.setenv("COLUMNS", "120")
    monkeypatch.setattr(tui, "interactive", lambda: False)

    tui.say("hello")
    tui.page(["one", "two"])
    assert capsys.readouterr().out == "hello\none\ntwo\n"


# --- the plugin half of an auto-update -------------------------------------


def _plugin_result(**kw):
    from probe.cli import updater

    base = dict(
        attempted=True, confirmed=True, changed=False, before=None, after="0.8.0", message="ok"
    )
    return updater.PluginResult(**{**base, **kw})


def _stub_cli_upgrade(monkeypatch, upgrading, updater):
    monkeypatch.setattr(upgrading.updater, "fetch_latest", lambda base: {})
    monkeypatch.setattr(
        upgrading.updater, "detect_install", lambda: updater.Install(updater.Method.UV_TOOL)
    )
    monkeypatch.setattr(
        upgrading.updater,
        "upgrade_cli",
        lambda i, c, t: updater.CliResult(
            ran=True, ok=True, changed=False, before=c, after=c, message="already at the latest"
        ),
    )


def test_a_failed_plugin_update_is_recorded(isolate, monkeypatch):
    """It used to live only in the printed lines, which a DETACHED run sends to
    /dev/null — so a plugin that had silently stopped updating looked exactly
    like one that worked. That is the failure this record exists to prevent."""
    from probe.cli import autoupdate, updater, upgrading

    _stub_cli_upgrade(monkeypatch, upgrading, updater)
    monkeypatch.setattr(
        upgrading.updater,
        "update_plugin",
        lambda target: _plugin_result(
            confirmed=False, after=None, message="`claude plugin update` did not complete"
        ),
    )

    outcome = upgrading.perform_update(base_url="https://x", include_plugin=True)
    attempt = autoupdate.load().last_attempt

    assert attempt.plugin_ok is False
    assert "did not complete" in attempt.plugin_detail
    assert attempt.succeeded is False
    assert "FAILED" in attempt.describe()
    assert "did not complete" in attempt.describe()
    # And the exit code means "the update worked", not "the CLI half worked".
    assert outcome.ok is False


def test_no_claude_on_path_is_not_a_plugin_failure(isolate, monkeypatch):
    """A CLI-only user has no `claude`. Recording that as a failure every
    session trains everyone to ignore the one line meant to mean something."""
    from probe.cli import autoupdate, updater, upgrading

    _stub_cli_upgrade(monkeypatch, upgrading, updater)
    monkeypatch.setattr(
        upgrading.updater,
        "update_plugin",
        lambda target: _plugin_result(
            attempted=False,
            confirmed=False,
            after=None,
            message="`claude` not found on PATH (skipping plugin update)",
        ),
    )

    outcome = upgrading.perform_update(base_url="https://x", include_plugin=True)
    attempt = autoupdate.load().last_attempt

    assert attempt.plugin_ok is True
    assert attempt.succeeded is True
    assert outcome.ok is True
    # Still SAID, though — silence about a skipped half is its own lie.
    assert "not found on PATH" in attempt.describe()


def test_a_pi_update_never_touches_claude_or_codex_plugins(isolate, monkeypatch):
    """REGRESSION for the bug this audit's blast radius was highest on.

    `perform_update`'s plugin half used to be a two-way
    `"Codex plugins:" if codex else "Claude Code plugins:"` ternary. A
    `probe wizard --agent pi --action update` run fell into the `else` and
    called `updater.update_plugin()` -- which shells out to the REAL `claude`
    binary (`claude plugin marketplace update`, `claude plugin update ...`)
    -- silently updating a researcher's Claude Code plugins as a side effect
    of updating pi, on any machine where `claude` also happens to be
    installed (the common case, not an edge one; see
    test_pi_pairing_reaches_exactly_where_the_tap_daemon_will_look's own
    framing of the sibling bug in `authorize()`).

    Both `update_plugin` and `update_codex_plugins` are poisoned to raise:
    a silent wrong answer would pass just as easily as a call count of zero
    would if this only checked a boolean.
    """
    from probe.cli import updater, upgrading

    monkeypatch.setenv("PROBE_AGENT", "pi")
    _stub_cli_upgrade(monkeypatch, upgrading, updater)

    def _boom(*a, **k):
        raise AssertionError("a pi update must never touch claude/codex's plugin CLI")

    monkeypatch.setattr(upgrading.updater, "update_plugin", _boom)
    monkeypatch.setattr(upgrading.updater, "update_codex_plugins", _boom)
    monkeypatch.setattr(upgrading, "_update_pi_package", lambda: upgrading._PiUpdate(["pi package:", "  updated 0.2.3 → 0.3.0"]))

    outcome = upgrading.perform_update(base_url="https://x", include_plugin=True)

    assert outcome.ok is True
    assert outcome.restart_needed is False
    assert "  updated 0.2.3 → 0.3.0" in outcome.lines, "pi's own package is pi's update"
    assert "Claude Code" not in "\n".join(outcome.lines)
    assert "Codex" not in "\n".join(outcome.lines)


def test_an_update_from_claude_code_moves_pis_package_too(isolate, monkeypatch):
    """An Update from a plain terminal (claude_code by default) or Claude
    Code's auto-update used to skip pi, so pi stayed on the package it was
    installed with (2026-10-02)."""
    from probe.cli import updater, upgrading

    monkeypatch.setenv("PROBE_AGENT", "claude_code")
    _stub_cli_upgrade(monkeypatch, upgrading, updater)
    monkeypatch.setattr(
        upgrading.updater, "update_plugin", lambda target: _plugin_result(confirmed=True, message="current")
    )
    monkeypatch.setattr(upgrading, "_update_pi_package", lambda: upgrading._PiUpdate(["pi package:", "  updated 0.2.3 → 0.3.0"]))

    outcome = upgrading.perform_update(base_url="https://x", include_plugin=True)

    assert "  updated 0.2.3 → 0.3.0" in outcome.lines


def test_a_codex_update_still_uses_the_codex_path(isolate, monkeypatch):
    """The pi guard above must not have collapsed codex into the claude_code
    branch on the way to excluding pi from it."""
    from probe.cli import updater, upgrading

    monkeypatch.setenv("PROBE_AGENT", "codex")
    _stub_cli_upgrade(monkeypatch, upgrading, updater)
    monkeypatch.setattr(
        upgrading.updater, "update_codex_plugins", lambda: _plugin_result(changed=True)
    )
    monkeypatch.setattr(
        upgrading.updater,
        "update_plugin",
        lambda target: (_ for _ in ()).throw(
            AssertionError("codex must not go through update_plugin")
        ),
    )

    outcome = upgrading.perform_update(base_url="https://x", include_plugin=True)

    assert outcome.restart_needed is True
    assert any("Codex plugins:" in line for line in outcome.lines)


def test_a_successful_plugin_update_names_the_version(isolate, monkeypatch):
    from probe.cli import autoupdate, updater, upgrading

    _stub_cli_upgrade(monkeypatch, upgrading, updater)
    monkeypatch.setattr(
        upgrading.updater, "update_plugin", lambda target: _plugin_result(changed=True)
    )

    upgrading.perform_update(base_url="https://x", include_plugin=True)
    described = autoupdate.load().last_attempt.describe()

    assert described.startswith("success")
    assert "plugin 0.8.0" in described


def test_an_old_record_without_plugin_fields_still_reads_as_success(isolate):
    """Records written before the plugin half was tracked must not start
    reporting a failure the moment the CLI is upgraded."""
    from probe.cli import autoupdate

    autoupdate.state_dir().mkdir(parents=True, exist_ok=True)
    autoupdate.state_path().write_text(
        json.dumps(
            {
                "enabled": True,
                "channel": "latest",
                "last_attempt": {"at": 1_700_000_000, "ok": True, "to_version": "0.14.1"},
            }
        )
    )
    attempt = autoupdate.load().last_attempt
    assert attempt.succeeded is True
    assert attempt.describe().startswith("success -> CLI 0.14.1")


def test_the_hook_no_longer_passes_a_channel(isolate):
    """One channel, so the flag is gone from the spawn — but newer CLIs must
    still ACCEPT it, because a plugin updates on the USER's schedule and older
    copies of the hook are still out there passing it."""
    import pathlib

    hook = pathlib.Path("plugins/probe-research/hooks/version_check.py").read_text()
    # Select the UPDATE spawn by name rather than by being the first Popen in the
    # file. The hook gained a second spawn (the detached session maintenance that
    # refreshes the instruction block and reconciles the team-note file), and
    # "the first Popen" silently became the wrong one.
    spawn = hook.split("def _spawn_autoupdate(")[1]
    argv = spawn.split("subprocess.Popen(")[1].split("stdin=")[0]
    assert '"--action", "update"' in argv, "wrong call site"
    assert "--channel" not in argv

    from typer.testing import CliRunner

    from probe.cli.main import app

    result = CliRunner().invoke(app, ["wizard", "--action", "diagnose", "--channel", "stable"])
    assert result.exit_code == 0, result.output + repr(result.exception)


# --- the 2026-08-04 install phase ------------------------------------------
#
# A `npx probe-research` run sat on "This run will:" for minutes, then reported
# two failed plugin installs and finished with "Restart Claude Code to finish".
# Four separate defects, each with its own test below:
#
#   1. the phase buffered every message until all four steps had returned
#   2. the marketplace refresh ran per-plugin and both results were discarded
#   3. a failed install never reached the verdict
#   4. the install was attempted at all -- both plugins were already present


def test_the_install_phase_streams_instead_of_buffering():
    """It used to collect every message into a list and print the lot after all
    four apply steps finished. Since a step shells out to `claude`, that showed
    a blank screen for as long as the subprocesses took -- which is the entire
    reported symptom."""
    import inspect
    import sys

    import probe.cli.main  # noqa: F401

    source = inspect.getsource(sys.modules["probe.cli.main"]._run_wizard_action)
    # The tell-tale of the old shape: one list, extended by every apply, drained
    # at the end.
    assert "messages: list[str] = []" not in source
    assert "for message in messages:" not in source
    assert "tui.Progress(" in source


def test_a_present_plugin_is_not_reinstalled(monkeypatch):
    """THE root cause. The install was gated on `caps.tracking_on`, which is
    "plugin installed AND logged in", and on `capture_on`, which does not look
    at the plugin at all. A machine with both plugins present but no credential
    yet therefore read as "both off" and reinstalled both -- and those installs
    are the ones that failed.

    Measured: `claude plugin install` on an already-installed plugin returns
    "already installed" and does NOT upgrade it, so the work had no upside.
    """
    import sys

    import probe.cli.main  # noqa: F401
    from probe.cli import doctor as doctor_impl
    from probe.cli import setup as wizard
    from probe.cli import tui
    from probe.cli.actions import Action

    cli_main = sys.modules["probe.cli.main"]
    installed: list[str] = []
    monkeypatch.setattr(tui, "interactive", lambda: False)
    monkeypatch.setattr(wizard, "interactive", lambda: False)
    monkeypatch.setattr(wizard, "install_plugin", lambda name, **kw: installed.append(name))
    monkeypatch.setattr(wizard, "needs_authorization", lambda caps, selection: [])
    monkeypatch.setattr(cli_main, "_register_local_capabilities", lambda *a, **k: [])

    # Exactly the reported machine: both plugins on disk, no credential.
    present = _caps(
        tracking_plugin_installed=True,
        capture_plugin_installed=True,
        logged_in_as=None,
    )
    monkeypatch.setattr(doctor_impl, "collect", lambda *a, **k: present)

    cli_main._run_wizard_action(
        Action.CONFIGURE,
        caps=present,
        base_now="https://api.test",
        yes=True,
        tracking=True,
        capture=True,
        auto_update=None,
        agent_rules=False,
        uninstall=False,
        configured=True,
    )

    assert installed == [], "already-present plugins must not be reinstalled"


def test_the_plan_says_sign_in_when_only_the_credential_is_missing():
    """ "enable CLI + MCP" on a machine whose plugin is already installed
    describes work the run will not do. It is also the COMMON first-run case,
    because capture_on is credential-only."""
    from probe.cli import setup as wizard
    from probe.cli.capabilities import Capability

    caps = _caps(tracking_plugin_installed=True, capture_plugin_installed=True)
    selection = wizard.Selection(tracking=True, capture=True, auto_update=False, agent_rules=False)
    steps = wizard.plan(caps, selection)

    assert any("sign in" in step for step in steps), steps
    assert not any(step.startswith("enable CLI + MCP") for step in steps), steps
    # And the sign-in wording exists for both capabilities that have a plugin.
    assert set(wizard.SIGN_IN_LABELS) == {Capability.TRACKING, Capability.CAPTURE}


def test_a_successful_install_does_no_marketplace_work(monkeypatch):
    """install_plugin used to run `marketplace add` + `update` itself, so a run
    installing both plugins refreshed the same marketplace twice -- and threw
    both results away, which is why a failed refresh surfaced as Claude's
    downstream "not found in marketplace".

    The refresh is now the caller's job, once per run. Only the RETRY path may
    refresh again, so a clean install must touch the marketplace zero times.
    """
    from probe.cli import claude_cli
    from probe.cli import setup as wizard

    calls: list[list[str]] = []
    monkeypatch.setattr(
        claude_cli,
        "run",
        lambda args, *, timeout: calls.append(args) or claude_cli.Result(ok=True),
    )

    assert wizard.install_plugin("probe-research").ok is True
    assert calls == [["plugin", "install", "probe-research@research-os-agent"]]
    assert not any("marketplace" in a for call in calls for a in call)


def test_refresh_marketplace_reports_the_update_result(monkeypatch):
    """Both results used to be discarded. `update` is the one whose success
    decides whether the catalog we install from is current, so it is the one
    that comes back."""
    from probe.cli import claude_cli
    from probe.cli import setup as wizard

    def fake_run(args, *, timeout):
        if "update" in args:
            return claude_cli.Result(ok=False, detail="network unreachable")
        return claude_cli.Result(ok=True)

    monkeypatch.setattr(claude_cli, "run", fake_run)

    result = wizard.refresh_marketplace()
    assert result.ok is False
    assert "network unreachable" in result.detail


def test_a_first_add_that_hits_a_blocked_git_is_the_reported_cause(monkeypatch):
    """On a machine that never added the marketplace, `add` is the clone that
    hits the Mac's blocked git; `update` then fails as "not found", which says
    nothing about the Xcode license that caused it."""
    from probe.cli import claude_cli
    from probe.cli import setup as wizard

    license_text = (
        "You have not agreed to the Xcode license agreements. Please run 'sudo xcodebuild "
        "-license' from within a Terminal window to review and agree to the Xcode and Apple "
        "SDKs license."
    )

    def fake_run(args, *, timeout):
        if "add" in args:
            return claude_cli.Result(ok=False, detail=license_text)
        return claude_cli.Result(ok=False, detail="Marketplace 'research-os-agent' not found")

    monkeypatch.setattr(claude_cli, "run", fake_run)

    result = wizard.refresh_marketplace()
    assert result.ok is False
    assert "Xcode license" in result.detail


def test_a_failed_install_retries_once_on_any_failure(monkeypatch):
    """Deliberately NOT gated on matching Claude's error prose: a retry that
    fires only on "not found in marketplace" stops firing the day Anthropic
    rewords it, silently, with every test still green."""
    from probe.cli import claude_cli
    from probe.cli import setup as wizard

    attempts: list[list[str]] = []
    refreshed: list[int] = []

    def fake_run(args, *, timeout):
        attempts.append(args)
        # Fail the first install, succeed the second.
        if args[:2] == ["plugin", "install"]:
            return claude_cli.Result(ok=len(refreshed) > 0, detail="whatever went wrong")
        return claude_cli.Result(ok=True)

    monkeypatch.setattr(claude_cli, "run", fake_run)
    monkeypatch.setattr(wizard, "refresh_marketplace", lambda **_kwargs: refreshed.append(1))

    budget = [1]

    def may_retry():
        if budget[0] <= 0:
            return False
        budget[0] -= 1
        return True

    result = wizard.install_plugin("probe-research", on_retry=may_retry)

    assert result.ok is True
    assert len(refreshed) == 1, "the retry must refresh first"
    installs = [a for a in attempts if a[:2] == ["plugin", "install"]]
    assert len(installs) == 2, "exactly one retry"


def test_the_retry_budget_is_per_run_not_per_plugin(monkeypatch):
    """Two plugins failing must not cost two refreshes and two reinstalls: that
    is how a fix for an 18-minute worst case becomes a 30-minute one."""
    from probe.cli import claude_cli
    from probe.cli import setup as wizard

    refreshed: list[int] = []
    monkeypatch.setattr(
        claude_cli, "run", lambda args, *, timeout: claude_cli.Result(ok=False, detail="no")
    )
    monkeypatch.setattr(wizard, "refresh_marketplace", lambda **_kwargs: refreshed.append(1))

    budget = [1]

    def may_retry():
        if budget[0] <= 0:
            return False
        budget[0] -= 1
        return True

    wizard.install_plugin("probe-research", on_retry=may_retry)
    wizard.install_plugin("probe-research-tap", on_retry=may_retry)

    assert len(refreshed) == 1, "the second plugin must find the budget spent"


def test_a_verified_absent_plugin_fails_the_run(monkeypatch):
    """ "Restart Claude Code to finish" after a failed install reads as success:
    the user restarts, finds Probe absent, and has no idea why."""
    import sys

    import typer

    import probe.cli.main  # noqa: F401
    from probe.cli import doctor as doctor_impl
    from probe.cli import setup as wizard
    from probe.cli import tui
    from probe.cli.actions import Action

    cli_main = sys.modules["probe.cli.main"]
    monkeypatch.setattr(tui, "interactive", lambda: False)
    monkeypatch.setattr(wizard, "interactive", lambda: False)
    monkeypatch.setattr(wizard, "apply_tracking", lambda want, **kw: [])
    monkeypatch.setattr(wizard, "needs_authorization", lambda caps, selection: [])
    monkeypatch.setattr(cli_main, "_register_local_capabilities", lambda *a, **k: [])
    # Verified: we asked, and the plugin is not there.
    monkeypatch.setattr(
        doctor_impl,
        "collect",
        lambda *a, **k: _caps(tracking_plugin_installed=False, plugins_verified=True),
    )

    with pytest.raises(typer.Exit) as excinfo:
        cli_main._run_wizard_action(
            Action.CONFIGURE,
            caps=_caps(),
            base_now="https://api.test",
            yes=True,
            tracking=True,
            capture=False,
            auto_update=None,
            agent_rules=False,
            uninstall=False,
            configured=True,
        )
    assert excinfo.value.exit_code == 1


def test_an_unverifiable_plugin_does_not_fail_the_run(monkeypatch):
    """`claude` absent is normal on a GPU pod. Swapping a silent failure for a
    false alarm on machines that are fine would be the worse bug -- it trains
    people to ignore the message."""
    import sys

    import probe.cli.main  # noqa: F401
    from probe.cli import doctor as doctor_impl
    from probe.cli import setup as wizard
    from probe.cli import tui
    from probe.cli.actions import Action

    cli_main = sys.modules["probe.cli.main"]
    monkeypatch.setattr(tui, "interactive", lambda: False)
    monkeypatch.setattr(wizard, "interactive", lambda: False)
    monkeypatch.setattr(wizard, "apply_tracking", lambda want, **kw: [])
    monkeypatch.setattr(wizard, "needs_authorization", lambda caps, selection: [])
    monkeypatch.setattr(cli_main, "_register_local_capabilities", lambda *a, **k: [])
    # We could NOT ask. Absent is an unanswered question, not a finding.
    monkeypatch.setattr(
        doctor_impl,
        "collect",
        lambda *a, **k: _caps(tracking_plugin_installed=False, plugins_verified=False),
    )

    # Must NOT raise.
    cli_main._run_wizard_action(
        Action.CONFIGURE,
        caps=_caps(),
        base_now="https://api.test",
        yes=True,
        tracking=True,
        capture=False,
        auto_update=None,
        agent_rules=False,
        uninstall=False,
        configured=True,
    )


def test_plugin_state_will_not_report_absence_it_did_not_verify():
    from probe.cli.capabilities import PluginState

    verified = PluginState(names=frozenset({"probe-research"}), verified=True)
    assert verified.missing(["probe-research", "probe-research-tap"]) == ["probe-research-tap"]

    unknown = PluginState(verified=False)
    assert unknown.missing(["probe-research"]) == [], "an unanswered question is not a no"


def test_installed_plugins_is_unverified_without_claude(monkeypatch):
    from probe.cli import capabilities

    monkeypatch.setattr(
        capabilities.plugin_cli,
        "list_plugins",
        lambda _source: capabilities.plugin_cli.claude_cli.Result(ok=False, reachable=False),
    )
    state = capabilities.installed_plugins()
    assert state.verified is False
    assert len(state) == 0


# --- the progress screen ----------------------------------------------------


def test_progress_marks_a_failed_step_distinctly(monkeypatch, capsys):
    from probe.cli import tui

    monkeypatch.setenv("COLUMNS", "120")
    monkeypatch.setattr(tui, "interactive", lambda: True)
    monkeypatch.setattr(tui, "clear", lambda: None)
    monkeypatch.setattr(tui, "rows", lambda: 40)

    progress = tui.Progress("This run will:", ["enable A", "enable B"])
    progress.finish(0, ok=True)
    progress.finish(1, ok=False)
    block = "\n".join(progress.block())

    assert "✔ enable A" in block
    assert "✗ enable B" in block, "a failure must not read as a tick"


def test_the_bar_tracks_completed_steps(monkeypatch):
    from probe.cli import tui

    monkeypatch.setattr(tui, "interactive", lambda: False)
    progress = tui.Progress("t", ["a", "b", "c", "d"])
    assert progress.bar().endswith("0/4")
    progress.finish(0)
    progress.finish(1)
    assert progress.bar().endswith("2/4")
    assert progress.bar().count("━") == progress.bar().count("─")
    assert progress.block().index(progress.bar()) < progress.block().index("  ✔ a")


@pytest.mark.parametrize("agent_screen_shown", [False, True])
def test_install_progress_continues_across_agents(monkeypatch, agent_screen_shown):
    from probe.cli import tui

    monkeypatch.setattr(tui, "interactive", lambda: False)
    sources = ("claude_code", "codex", "pi")
    bars = [setup.install_progress(setup.STEP_CONFIRM, agent_screen_shown=agent_screen_shown)]
    for index, source in enumerate(sources):
        header = setup.install_apply_header(
            agent_screen_shown=agent_screen_shown,
            agent_index=index,
            agent_count=len(sources),
            agent_source=source,
        )
        progress = tui.Progress("This run will:", ["sign in", "install"], overall=header)
        bars.append(progress.block()[1])
        assert f"Step {3 if agent_screen_shown else 2} of" in progress.block()[0]
        assert progress.block()[2] == progress.block()[4] == ""
        assert setup.agent_label(source) in progress.block()[3]
        progress.finish(0)
        bars.append(progress.block()[1])
        progress.finish(1)
        bars.append(progress.block()[1])
    counts = [bar.count("━") for bar in bars]
    assert counts == sorted(counts), "a new coding agent must not reset install progress"
    assert "─" in bars[-1], "the import offer still follows installation"
    assert bars[-1] == setup.install_progress(
        setup.STEP_IMPORTS, agent_screen_shown=agent_screen_shown
    )


def test_progress_appends_one_line_per_step_when_piped(monkeypatch, capsys):
    """A screen and a log want opposite things. page() skips the clear when it
    is not interactive, so redrawing into a pipe prints the whole growing block
    once per step -- log spam, not progress. And `probe wizard --yes` is the
    one path where a human is NOT watching, so its log is the only evidence of
    which step a wedged CI job died on."""
    from probe.cli import tui

    monkeypatch.setattr(tui, "interactive", lambda: False)

    progress = tui.Progress("This run will:", ["enable A", "enable B"])
    progress.start(0)
    progress.finish(0, ok=True)
    progress.start(1)
    progress.finish(1, ok=False)

    out = capsys.readouterr().out
    lines = [ln for ln in out.split("\n") if ln.strip()]
    assert lines == ["[1/2] enable A ... ok", "[2/2] enable B ... FAILED"]
    assert "This run will:" not in out, "the block must not be reprinted per step"


def test_results_persist_across_redraws(monkeypatch, capsys):
    """clear() emits \\033[3J, which drops the scrollback. Anything not
    re-drawn is gone for good, so a failure message from step 1 must still be
    on screen after step 4 redraws."""
    from probe.cli import tui

    monkeypatch.setenv("COLUMNS", "120")
    monkeypatch.setattr(tui, "interactive", lambda: True)
    monkeypatch.setattr(tui, "clear", lambda: None)
    monkeypatch.setattr(tui, "rows", lambda: 40)

    progress = tui.Progress("t", ["a", "b"])
    progress.note("could not install probe-research")
    progress.finish(1, ok=True)

    assert "could not install probe-research" in "\n".join(progress.block())


def test_ticking_capture_clears_the_killswitch_even_when_the_plugin_is_present(monkeypatch):
    """Regression introduced while fixing the reinstall bug, caught in review.

    Gating the capture step on "plugin absent" skipped `apply_capture(True)`
    entirely on a machine whose tap plugin was installed but killswitched. The
    `.disabled` file survived, capture stayed off, and the wizard reported
    success -- the inverse of the failure capture.py calls the worst available
    bug ("we told you it was off and it wasn't").
    """
    import sys

    import probe.cli.main  # noqa: F401
    from probe.cli import doctor as doctor_impl
    from probe.cli import setup as wizard
    from probe.cli import tui
    from probe.cli.actions import Action

    cli_main = sys.modules["probe.cli.main"]
    cleared: list[int] = []
    installed: list[str] = []
    monkeypatch.setattr(tui, "interactive", lambda: False)
    monkeypatch.setattr(wizard, "interactive", lambda: False)
    monkeypatch.setattr(wizard, "clear_killswitch", lambda: cleared.append(1))
    monkeypatch.setattr(wizard, "install_plugin", lambda name, **kw: installed.append(name))
    monkeypatch.setattr(wizard, "needs_authorization", lambda caps, selection: [])
    monkeypatch.setattr(cli_main, "_register_local_capabilities", lambda *a, **k: [])

    # Plugin installed, credential present, but the killswitch is ON -- so
    # capture_on is False and the user ticking it must actually turn it on.
    killswitched = _caps(
        capture_plugin_installed=True,
        capture_killswitched=True,
        capture_token_sources=(TokenSource.PAIRED_FILE,),
        plugins_verified=True,
    )
    monkeypatch.setattr(doctor_impl, "collect", lambda *a, **k: killswitched)

    cli_main._run_wizard_action(
        Action.CONFIGURE,
        caps=killswitched,
        base_now="https://api.test",
        yes=True,
        tracking=False,
        capture=True,
        auto_update=None,
        agent_rules=False,
        uninstall=False,
        configured=True,
    )

    assert cleared, "the killswitch must be cleared when capture is ticked on"
    assert installed == [], "a present plugin must still not be reinstalled"


def test_a_valid_pairing_does_not_hide_a_manually_removed_capture_plugin(monkeypatch):
    """A direct plugin removal intentionally leaves durable pairing state.

    The manager must inspect both halves of capture: a valid token is not a
    substitute for the hook plugin that starts the uploader.
    """
    import sys

    import probe.cli.main  # noqa: F401
    from probe.cli import claude_cli
    from probe.cli import doctor as doctor_impl
    from probe.cli import setup as wizard
    from probe.cli import tui
    from probe.cli.actions import Action

    cli_main = sys.modules["probe.cli.main"]
    installed: list[str] = []
    before = _caps(
        agent_source="codex",
        codex_available=True,
        capture_plugin_installed=False,
        capture_token_sources=(TokenSource.PAIRED_FILE,),
        capture_credential_valid=True,
        plugins_verified=True,
    )
    after = dataclasses.replace(before, capture_plugin_installed=True)

    monkeypatch.setenv("PROBE_AGENT", "codex")
    monkeypatch.setattr(tui, "interactive", lambda: False)
    monkeypatch.setattr(wizard, "interactive", lambda: False)
    monkeypatch.setattr(wizard, "needs_authorization", lambda caps, selection: [])
    monkeypatch.setattr(
        wizard,
        "install_plugin",
        lambda name, **kw: installed.append(name) or claude_cli.Result(ok=True),
    )
    monkeypatch.setattr(doctor_impl, "collect", lambda *a, **k: after)
    monkeypatch.setattr(cli_main, "_register_local_capabilities", lambda *a, **k: [])

    cli_main._run_wizard_action(
        Action.CONFIGURE,
        caps=before,
        base_now="https://api.test",
        yes=True,
        tracking=False,
        capture=True,
        auto_update=None,
        agent_rules=False,
        uninstall=False,
        configured=True,
    )

    assert installed == ["probe-research-tap"]


def test_every_failure_message_the_wizard_emits_is_classified_as_one():
    """The progress tick decides ✔ vs ✗ from these strings. If a message the
    apply_* helpers can emit is not recognised, the screen shows a tick over a
    line that says the step failed."""
    import inspect
    import re

    from probe.cli import setup as wizard

    source = inspect.getsource(wizard)
    # Every literal the module appends as a failure/warning message.
    emitted = re.findall(r'messages\.append\(\s*f?"([^"]+)"', source)
    emitted += re.findall(r'return \[\s*f?"(! [^"]+)"', source)
    assert emitted, "expected to find failure messages in setup.py"
    for template in emitted:
        rendered = template.replace("{", "").replace("}", "")
        if not rendered.startswith(("could not", "!")):
            continue  # a success message; nothing to assert
        assert wizard.reports_failure(rendered), f"unclassified failure: {template}"


def test_the_marketplace_is_refreshed_before_the_first_install(monkeypatch):
    """Caught by adversarial review of the hoist itself.

    Hoisting the refresh OUT of install_plugin is only half the change: the
    caller has to actually do it. Without that, the first attempt installs from
    whatever stale copy is on disk -- the exact failure the original code's
    comment warned about ("a fresh wizard run happily installs a stale plugin
    version ... how a newly published plugin appears to be missing") -- and on a
    machine that never added the marketplace at all, attempt one ALWAYS fails
    and only the retry repairs it.
    """
    import sys

    import probe.cli.main  # noqa: F401
    from probe.cli import doctor as doctor_impl
    from probe.cli import setup as wizard
    from probe.cli import tui
    from probe.cli.actions import Action

    cli_main = sys.modules["probe.cli.main"]
    order: list[str] = []
    monkeypatch.setattr(tui, "interactive", lambda: False)
    monkeypatch.setattr(wizard, "interactive", lambda: False)
    monkeypatch.setattr(wizard, "refresh_marketplace", lambda: order.append("refresh"))
    monkeypatch.setattr(
        wizard, "install_plugin", lambda name, **kw: order.append(f"install:{name}")
    )
    monkeypatch.setattr(wizard, "needs_authorization", lambda caps, selection: [])
    monkeypatch.setattr(cli_main, "_register_local_capabilities", lambda *a, **k: [])
    monkeypatch.setattr(
        doctor_impl,
        "collect",
        lambda *a, **k: _caps(tracking_plugin_installed=True, plugins_verified=True),
    )

    cli_main._run_wizard_action(
        Action.CONFIGURE,
        caps=_caps(claude_available=True),  # agent present, nothing installed -> real install
        base_now="https://api.test",
        yes=True,
        tracking=True,
        capture=False,
        auto_update=None,
        agent_rules=False,
        uninstall=False,
        configured=True,
    )

    assert "refresh" in order, "the marketplace must be refreshed before installing"
    assert order.index("refresh") < order.index("install:probe-research")


def test_a_mac_that_cannot_run_git_gets_the_fix_not_apples_paragraph(monkeypatch, capsys):
    """The install run's refresh step printed the child's raw output: on a Mac
    with the Xcode license unaccepted, Apple's whole paragraph, unscrubbed."""
    import sys

    import probe.cli.main  # noqa: F401
    from probe.cli import claude_cli
    from probe.cli import doctor as doctor_impl
    from probe.cli import setup as wizard
    from probe.cli import tui
    from probe.cli.actions import Action

    cli_main = sys.modules["probe.cli.main"]
    monkeypatch.setattr(tui, "interactive", lambda: False)
    monkeypatch.setattr(wizard, "interactive", lambda: False)
    monkeypatch.setattr(
        wizard,
        "refresh_marketplace",
        lambda: claude_cli.Result(
            ok=False,
            detail="✘ Failed to update marketplace(s): Failed to clone marketplace repository: "
            "You have not agreed to the Xcode license agreements. Please run 'sudo xcodebuild "
            "-license' from within a Terminal window to review and agree to the Xcode and "
            "Apple SDKs license.",
        ),
    )
    monkeypatch.setattr(wizard, "install_plugin", lambda name, **kw: claude_cli.Result(ok=True))
    monkeypatch.setattr(wizard, "needs_authorization", lambda caps, selection: [])
    monkeypatch.setattr(cli_main, "_register_local_capabilities", lambda *a, **k: [])
    monkeypatch.setattr(
        doctor_impl,
        "collect",
        lambda *a, **k: _caps(tracking_plugin_installed=True, plugins_verified=True),
    )

    lines = cli_main._run_wizard_action(
        Action.CONFIGURE,
        caps=_caps(claude_available=True),
        base_now="https://api.test",
        yes=True,
        tracking=True,
        capture=False,
        auto_update=None,
        agent_rules=False,
        uninstall=False,
        configured=True,
    )

    # Non-interactive, each step's messages print under its progress line.
    text = "\n".join([capsys.readouterr().out, *(lines or [])])
    assert (
        "! could not refresh the marketplace: git on this Mac is blocked until the Xcode "
        "license is accepted." in text
    )
    assert "You have not agreed" not in text

def test_no_install_means_no_marketplace_refresh(monkeypatch):
    """The refresh is two `claude` subprocesses. A run that installs nothing --
    the common re-run -- must not pay for them."""
    import sys

    import probe.cli.main  # noqa: F401
    from probe.cli import doctor as doctor_impl
    from probe.cli import setup as wizard
    from probe.cli import tui
    from probe.cli.actions import Action

    cli_main = sys.modules["probe.cli.main"]
    refreshed: list[int] = []
    monkeypatch.setattr(tui, "interactive", lambda: False)
    monkeypatch.setattr(wizard, "interactive", lambda: False)
    monkeypatch.setattr(wizard, "refresh_marketplace", lambda: refreshed.append(1))
    monkeypatch.setattr(wizard, "needs_authorization", lambda caps, selection: [])
    monkeypatch.setattr(cli_main, "_register_local_capabilities", lambda *a, **k: [])

    already = _caps(tracking_plugin_installed=True, logged_in_as="x@y.z", plugins_verified=True)
    monkeypatch.setattr(doctor_impl, "collect", lambda *a, **k: already)

    cli_main._run_wizard_action(
        Action.CONFIGURE,
        caps=already,
        base_now="https://api.test",
        yes=True,
        tracking=True,
        capture=False,
        auto_update=True,
        agent_rules=False,
        uninstall=False,
        configured=True,
    )

    assert refreshed == [], "a run with nothing to install must not refresh"


def test_the_credential_is_minted_before_the_plugin_is_installed(monkeypatch):
    """The tracking plugin publishes an MCP server it cannot yet authenticate.

    `plugins/probe-research/.mcp.json` points at the hosted MCP and resolves its
    bearer through a headers helper that reads the token this run mints. Install
    first and there is a window -- as long as a human takes to approve a browser
    prompt -- where the server is on disk with no credential behind it. A connect
    in that window is unauthenticated, the edge answers 401 with a
    `WWW-Authenticate` challenge, and Claude Code discovers an authorization
    server and pins the connection to OAuth. The user then has to open `/mcp` and
    authenticate a device the installer had already authorized, which is the
    symptom this ordering exists to prevent.

    Asserted on the observable call order, not on the work list, because the list
    is an implementation detail and the window is not.
    """
    import sys

    import probe.cli.main  # noqa: F401
    from probe.cli import claude_cli
    from probe.cli import doctor as doctor_impl
    from probe.cli import setup as wizard
    from probe.cli import tui
    from probe.cli.actions import Action

    cli_main = sys.modules["probe.cli.main"]
    order: list[str] = []

    def _install(name, **kw):
        order.append(f"install:{name}")
        # A real Result, not None. The step swallows an AttributeError and marks
        # itself failed, so a bare stub would leave this test passing on an
        # install that never ran the code path it is timing.
        return claude_cli.Result(ok=True)

    def _authorize(grants, **kw):
        order.append("authorize")
        return {grant: {"token": f"probe_pat_{grant}"} for grant in grants}, []

    monkeypatch.setattr(tui, "interactive", lambda: False)
    monkeypatch.setattr(wizard, "interactive", lambda: False)
    monkeypatch.setattr(wizard, "refresh_marketplace", lambda: order.append("refresh"))
    monkeypatch.setattr(wizard, "install_plugin", _install)
    monkeypatch.setattr(wizard, "authorize", _authorize)
    monkeypatch.setattr(cli_main, "_register_local_capabilities", lambda *a, **k: [])
    monkeypatch.setattr(
        doctor_impl,
        "collect",
        lambda *a, **k: _caps(
            tracking_plugin_installed=True, logged_in_as="x@y.z", plugins_verified=True
        ),
    )

    cli_main._run_wizard_action(
        Action.CONFIGURE,
        caps=_caps(claude_available=True),  # fresh machine, agent present: no plugin, no credential
        base_now="https://api.test",
        yes=True,
        tracking=True,
        capture=False,
        auto_update=None,
        agent_rules=False,
        uninstall=False,
        configured=False,
    )

    assert "authorize" in order, "a fresh machine must run the browser approval"
    assert order.index("authorize") < order.index("install:probe-research"), (
        f"the plugin was installed before it had a credential to serve: {order}"
    )


# --- the picker: enter activates, Next ends it ------------------------------


def _settings_defaults():
    from probe.cli import setup as wizard

    return dict.fromkeys(wizard.Setting, True)


def _settings_rows():
    """Every setting the settings SCREEN draws, in screen order."""
    return [s for _, group in setup.grouped_settings() for s in group]


def _built_menu(defaults=None):
    """Build the picker exactly as run_settings_menu does, and hand back its
    control. The settings screen is where the checkbox machinery lives now
    that the install has no picker, so it is the screen these key tests pin."""
    import questionary

    from probe.cli import setup as wizard
    from probe.cli import tui

    defaults = defaults or _settings_defaults()
    tui.use_checkmarks()
    indent = tui.body_indent()
    # The REAL row list, nav band included -- not a rehearsal of it. A hand-rolled
    # copy here is how a test keeps asserting the layout that shipped two
    # versions ago, which is exactly the claim these tests exist to make.
    choices, rows, copy, state_copy = wizard.settings_choices(defaults, indent)
    choices = [*choices, *wizard.nav_footer(next_title=wizard.APPLY_TITLE)]
    question = questionary.checkbox("m", choices=choices, style=tui.style(), pointer="»")
    cycles = {s: order for s, order in wizard.cycling_settings().items() if s in rows}
    wizard._bind_menu_keys(
        question,
        rows,
        copy=copy,
        indent=indent,
        state_copy=state_copy,
        cycles=cycles,
        cycle_state={s: wizard.cycle_value(s, defaults[s]) for s in cycles},
    )
    return question, tui.checkbox_control(question), rows


def _press_key(question, key):
    """Fire the handler prompt_toolkit would ACTUALLY run for `key`.

    `matches[-1]` is how prompt_toolkit resolves a key (key_processor.py) --
    the LAST binding registered wins, which is ours. A test that fired the
    first match would exercise questionary's handler and prove nothing.
    """
    exited = {}

    class FakeApp:
        def exit(self, result=None):
            exited["result"] = result

    class FakeEvent:
        app = FakeApp()

    matches = question.application.key_bindings.get_bindings_for_keys((key,))
    assert matches, f"no binding for {key}"
    matches[-1].handler(FakeEvent())
    return exited


def _press_enter(question, control):
    """Fire the enter handler prompt_toolkit would ACTUALLY run.

    questionary binds enter to submit and we bind it to activate-the-row, so
    both match. prompt_toolkit resolves that with `matches[-1]`
    (key_processor.py) -- the LAST binding registered wins, which is ours. A
    test that fired the first match would exercise questionary's handler and
    prove nothing about this feature.
    """
    from prompt_toolkit.keys import Keys

    exited = {}

    class FakeApp:
        def exit(self, result=None):
            exited["result"] = result

    class FakeEvent:
        app = FakeApp()

    matches = question.application.key_bindings.get_bindings_for_keys((Keys.ControlM,))
    assert matches, "no enter binding found"
    matches[-1].handler(FakeEvent())
    return exited


def test_the_forward_key_submits_exactly_the_ticked_rows():
    """`→` is the way forward now that the band is a label rather than two
    selectable rows, so it is what has to yield the answer -- and the answer
    must be the capabilities, with no nav sentinel riding along."""
    from prompt_toolkit.keys import Keys

    question, _control, _ = _built_menu()
    exited = _press_key(question, Keys.Right)

    assert "result" in exited, "the forward key must submit"
    assert set(exited["result"]) == set(_settings_rows())


def test_going_straight_forward_grants_exactly_the_defaults():
    """A visible way forward means people accept defaults without touching a
    row, so the defaults ARE the grant. Everything ships on now, capture included, so what
    this pins is that clicking through grants the defaults and NOTHING MORE --
    no row silently on that the screen did not show ticked."""
    defaults = _settings_defaults()
    defaults[setup.Setting.AUTO_UPDATE] = False  # deliberately off: it stays off
    from prompt_toolkit.keys import Keys

    question, _control, _ = _built_menu(defaults)
    granted = set(_press_key(question, Keys.Right)["result"])
    assert granted == set(_settings_rows()) - {setup.Setting.AUTO_UPDATE}
    assert setup.Setting.AUTO_UPDATE not in granted, "an unticked row must stay unticked"


def test_the_settings_screen_offers_no_part_of_probe_to_turn_off():
    """Probe is installed whole and removed whole. The screen used to carry a
    row each for the CLI + MCP, session capture and the instruction rules, and
    a row per part is how devices ended up running half of it -- so none of
    those words may come back, and every drawn row is automatic updates or a
    "Who records" row -- or the reasoning row beside them, the
    agents' own setting for the daemon rather than a part of Probe."""
    _, control, rows = _built_menu()

    rendered = "".join(t[1] for t in control._get_choice_tokens())
    for part in ("CLI + MCP", "Session capture", "Rules in your global"):
        assert part not in rendered, f"{part!r} is back on the settings screen"
    assert set(rows) == {setup.Setting.AUTO_UPDATE}
    assert setup.Setting.TRACKING_DEFAULT not in rows, "the default lives on the main menu"
    assert not set(rows) & set(setup.RECORDER_SETTINGS), "so does Who records (Richard 2026-09-29)"


def _said(detail):
    """The detail lines that carry words.

    The tracking row spaces itself with a blank line in its copy, and a test
    that indexed [0] blindly would be asserting against the spacer.
    """
    return [line for line in detail if line.strip()]


def test_the_cycle_order_is_the_switch_s_own():
    """The wizard walks `session_marker.SWITCH_STATES`, not a copy of it. The space
    bar here and the researcher's bare `/probe` are the same switch seen from two
    places, and a screen with its own order would make one of them wrong. The
    daemon is not on it: that is the "Who records" row (Richard 2026-09-29)."""
    from probe.sdk import session_marker

    assert setup.cycling_settings() == {
        setup.Setting.TRACKING_DEFAULT: session_marker.SWITCH_STATES,
        # "Who records" (daemon reads) walks its own two positions.
        **{setting: session_marker.RECORDERS for setting in setup.RECORDER_SETTINGS},
    }


def test_read_and_off_say_which_half_of_probe_they_stop():
    """The disclosure this row exists for, and the reason it has three states
    rather than a tick. `read` blocks the CLI's write commands
    (plugins/probe-research/hooks/tracking_guard.py) and leaves the search
    surface running; `off` stops the searching too. Copy that said only "off"
    would leave a reader guessing which of those they had chosen -- and the
    guess that costs them is believing they can still find prior work."""
    from probe.sdk import session_marker

    per_state = setup.SETTINGS_STATE_COPY[setup.Setting.TRACKING_DEFAULT]
    read = " ".join(_said(per_state[session_marker.STATE_READ_ONLY])).lower()
    off = " ".join(_said(per_state[session_marker.STATE_OFF])).lower()

    assert "blocked" in read, read
    assert "still works" in read, "read has to say the searching survives"
    assert "no probe calls at all" in off, off
    assert "either" in off, "off has to say the searching stops too"


def test_enter_on_each_band_end_does_that_end_s_job():
    """One key, and which of two things it does is what the rectangle says.

    The failure this pins is silent and severe: Enter on `‹ Back` submitting
    would apply the very settings the user was backing out of, and Enter on
    `Next ›` retreating would throw them away. Nothing else drives these.
    """
    from probe.cli import tui

    question, control, _ = _built_menu()
    control.pointed_at = control.choices.index(
        next(c for c in control.choices if getattr(c, "value", None) == setup.NAV_BAND)
    )

    assert setup.nav_focus(control) == setup.NAV_NEXT
    granted = _press_enter(question, control)
    assert "result" in granted, "enter on the forward end must submit"
    assert set(granted["result"]) == set(_settings_rows())
    assert setup.NAV_BAND not in granted["result"], "the band is not an answer"

    question, control, _ = _built_menu()
    control.pointed_at = control.choices.index(
        next(c for c in control.choices if getattr(c, "value", None) == setup.NAV_BAND)
    )
    control.probe_nav["focus"] = setup.NAV_BACK
    assert _press_enter(question, control)["result"] is tui.BACK


def test_bulk_select_keys_cannot_desync_the_screen_from_the_answer():
    """questionary binds bare `a` (all) and `i` (invert) and mutates the
    selection directly. That was harmless while IT drew the boxes; we turned its
    indicator off and paint the box into the title, so its handlers changed the
    ANSWER without changing the SCREEN.

    Reproduced before the fix: untick capture, press `a`, and the row still read
    `○ Session capture` while the returned Selection carried capture=True. A
    screen the answer disagrees with is the whole failure this gate exists to
    prevent.
    """
    from probe.cli import tui

    for key in ("a", "i"):
        question, control, rows = _built_menu()
        control.pointed_at = control.choices.index(rows[setup.Setting.AUTO_UPDATE])
        _press_enter(question, control)  # untick automatic updates

        matches = question.application.key_bindings.get_bindings_for_keys((key,))
        assert matches, f"no binding for {key!r}"

        class _App:
            def exit(self, result=None):
                pass

        class _Event:
            app = _App()

        matches[-1].handler(_Event())

        rendered = "".join(t[1] for t in control._get_choice_tokens())
        for capability, row in rows.items():
            line = next(
                ln for ln in rendered.split("\n") if str(row.title).split("\n")[0][2:] in ln
            )
            drawn = tui.TICK in line
            assert drawn is (capability in control.selected_options), (
                f"{key!r} left {capability} drawn={drawn} but selected="
                f"{capability in control.selected_options}"
            )


def test_the_nav_band_is_dropped_when_we_cannot_own_the_keys():
    """A row that says `‹ Back` and submits on Enter is worse than no row.

    When `checkbox_control()` is unreachable, no bindings are installed:
    questionary's Enter-submits wins and its cursor parks on the first
    selectable row — which would be Back. Pressing Enter on it would grant every
    ticked capability. Escape still goes back, so the band is removed rather
    than left to lie.
    """
    import questionary

    from probe.cli import tui

    choices, _rows, _copy, _off = setup.settings_choices(_settings_defaults(), tui.body_indent())
    choices = [*choices, *setup.nav_footer(next_title=setup.APPLY_TITLE)]

    stripped = setup.without_nav(choices)
    selectable = [c.value for c in stripped if not isinstance(c, questionary.Separator)]

    assert selectable == _settings_rows(), "every row survives the strip"
    assert not any(setup.BACK_TITLE in str(getattr(c, "title", "")) for c in stripped), (
        "the band goes, so no row advertises a key nothing is listening for"
    )
    assert not any(
        isinstance(c, questionary.Separator) and str(c.title).strip() for c in stripped
    ), "the heading goes with it"


def test_the_back_key_leaves_the_step_backwards():
    """The band says `‹ Back  ←`; pressing it has to retreat rather than submit.

    A regression that made `←` submit would apply the very settings the user
    was backing out of, and would ship green -- nothing else drives this key.
    """
    from prompt_toolkit.keys import Keys

    from probe.cli import tui

    question, _control, _ = _built_menu()
    exited = _press_key(question, Keys.Left)

    assert exited["result"] is tui.BACK, "the back key must retreat, not submit"


def test_back_is_reachable_on_every_install_step():
    """Two screens in a row, and each has to say there is a way back —
    Escape alone is invisible."""
    for step in (setup.STEP_AGENTS, setup.STEP_CONFIRM):
        band = setup.nav_row([*setup.step_heading(step), *setup.nav_footer()])
        assert band is not None, f"step {step} has no nav band"
        assert setup.BACK_TITLE in str(band.title), f"step {step} has no way back"
        assert "←" in str(band.title), f"step {step} does not say which key"


def test_every_install_step_is_numbered():
    """Installation counts alongside agent selection, review and the import offer."""
    titles = [setup.step_title(n) for n in range(1, len(setup.INSTALL_STEPS) + 1)]
    assert titles[0].endswith("Step 1 of 4")
    assert titles[-1].endswith("Step 4 of 4")
    assert len({*titles}) == len(titles), "two screens must not claim the same position"


# --- the credential gate --------------------------------------------------


def test_a_refused_approval_installs_nothing(monkeypatch):
    """A cancelled browser approval must not leave a plugin behind.

    The tracking plugin publishes an MCP server whose bearer comes from the
    credential this run failed to mint. Installing it anyway puts an `.mcp.json`
    on disk with nothing behind it, and the first unauthenticated connect is
    answered with a `WWW-Authenticate` challenge that pins Claude Code to OAuth --
    so the user is sent to `/mcp` to authenticate a device that was never
    authorized at all. Leaving the machine as it was is the honest outcome of a
    refused approval.
    """
    import sys

    import typer

    import probe.cli.main  # noqa: F401
    from probe.cli import claude_cli
    from probe.cli import doctor as doctor_impl
    from probe.cli import setup as wizard
    from probe.cli import tui
    from probe.cli.actions import Action

    cli_main = sys.modules["probe.cli.main"]
    order: list[str] = []

    def _install(name, **kw):
        order.append(f"install:{name}")
        return claude_cli.Result(ok=True)

    monkeypatch.setattr(tui, "interactive", lambda: False)
    monkeypatch.setattr(wizard, "interactive", lambda: False)
    monkeypatch.setattr(wizard, "refresh_marketplace", lambda: order.append("refresh"))
    monkeypatch.setattr(wizard, "install_plugin", _install)
    # The user closed the browser tab: approved nothing, minted nothing.
    monkeypatch.setattr(
        wizard, "authorize", lambda grants, **kw: (order.append("authorize"), ({}, []))[1]
    )
    monkeypatch.setattr(cli_main, "_register_local_capabilities", lambda *a, **k: [])
    monkeypatch.setattr(doctor_impl, "collect", lambda *a, **k: _caps())

    with pytest.raises(typer.Exit):
        cli_main._run_wizard_action(
            Action.CONFIGURE,
            caps=_caps(),
            base_now="https://api.test",
            yes=True,
            tracking=True,
            capture=False,
            auto_update=None,
            agent_rules=False,
            uninstall=False,
            configured=False,
        )

    assert "authorize" in order
    assert not [step for step in order if step.startswith("install:")], (
        f"a plugin was installed with no credential behind it: {order}"
    )


def test_a_partial_grant_installs_only_what_it_can_authenticate(monkeypatch):
    """One failed grant must not veto the capability that DID get its credential.

    Refusing both would punish someone whose tracking approval succeeded for a
    capture grant the server declined -- and the two are independent plugins with
    independent credentials.
    """
    import sys

    import typer

    import probe.cli.main  # noqa: F401
    from probe.cli import claude_cli
    from probe.cli import doctor as doctor_impl
    from probe.cli import setup as wizard
    from probe.cli import tui
    from probe.cli.actions import Action

    cli_main = sys.modules["probe.cli.main"]
    order: list[str] = []

    def _install(name, **kw):
        order.append(f"install:{name}")
        return claude_cli.Result(ok=True)

    def _authorize(grants, **kw):
        # api + mcp came back; capture did not.
        return {g: {"token": f"probe_pat_{g}"} for g in grants if g != "capture"}, []

    monkeypatch.setattr(tui, "interactive", lambda: False)
    monkeypatch.setattr(wizard, "interactive", lambda: False)
    monkeypatch.setattr(wizard, "refresh_marketplace", lambda: None)
    monkeypatch.setattr(wizard, "install_plugin", _install)
    monkeypatch.setattr(wizard, "authorize", _authorize)
    monkeypatch.setattr(wizard, "clear_killswitch", lambda: None)
    monkeypatch.setattr(cli_main, "_register_local_capabilities", lambda *a, **k: [])
    monkeypatch.setattr(
        doctor_impl,
        "collect",
        lambda *a, **k: _caps(tracking_plugin_installed=True, logged_in_as="x@y.z"),
    )

    with pytest.raises(typer.Exit):
        cli_main._run_wizard_action(
            Action.CONFIGURE,
            caps=_caps(claude_available=True),
            base_now="https://api.test",
            yes=True,
            tracking=True,
            capture=True,
            auto_update=None,
            agent_rules=False,
            uninstall=False,
            configured=False,
        )

    assert f"install:{capabilities_mod.TRACKING_PLUGIN_NAME}" in order, (
        f"tracking had its credential and must still install: {order}"
    )
    assert f"install:{capabilities_mod.TAP_PLUGIN_NAME}" not in order, (
        f"capture had no credential and must not install: {order}"
    )


def test_turning_a_capability_off_is_never_gated_on_a_credential(monkeypatch):
    """Removal must work when minting fails.

    Gating an uninstall on a grant would trap someone on the very plugin they
    just asked to remove -- and removal needs no credential to be correct.
    """
    import sys

    import probe.cli.main  # noqa: F401
    from probe.cli import claude_cli
    from probe.cli import doctor as doctor_impl
    from probe.cli import setup as wizard
    from probe.cli import tui
    from probe.cli.actions import Action

    cli_main = sys.modules["probe.cli.main"]
    order: list[str] = []

    monkeypatch.setattr(tui, "interactive", lambda: False)
    monkeypatch.setattr(wizard, "interactive", lambda: False)
    monkeypatch.setattr(
        wizard,
        "uninstall_plugin",
        lambda name: (order.append(f"uninstall:{name}"), claude_cli.Result(ok=True))[1],
    )
    monkeypatch.setattr(wizard, "authorize", lambda grants, **kw: ({}, []))
    monkeypatch.setattr(cli_main, "_register_local_capabilities", lambda *a, **k: [])
    monkeypatch.setattr(doctor_impl, "collect", lambda *a, **k: _caps())

    cli_main._run_wizard_action(
        Action.CONFIGURE,
        caps=_caps(tracking_plugin_installed=True, logged_in_as="x@y.z"),
        base_now="https://api.test",
        yes=True,
        tracking=False,
        capture=False,
        auto_update=None,
        agent_rules=False,
        uninstall=False,
        configured=True,
    )

    assert f"uninstall:{capabilities_mod.TRACKING_PLUGIN_NAME}" in order


def test_a_rerun_that_already_holds_its_grants_is_not_gated():
    """`granted` is empty on a healthy re-run -- nothing was requested. Reading
    that as failure would refuse to install on every machine already signed in."""
    from probe.cli.capabilities import Capability

    assert setup.blocked_by_missing_grants(Capability.TRACKING, needed=[], granted={}) == []
    assert (
        setup.blocked_by_missing_grants(
            Capability.TRACKING, needed=["api", "mcp"], granted={"api": {}, "mcp": {}}
        )
        == []
    )
    assert setup.blocked_by_missing_grants(
        Capability.TRACKING, needed=["api", "mcp"], granted={"api": {}}
    ) == ["mcp"]


def test_the_grant_table_is_the_only_source_of_what_a_capability_needs():
    """grants_for and the gate must read ONE table. Two hardcoded lists is how a
    third grant gets added to the request and not to the check."""
    from probe.cli.capabilities import Capability

    everything = setup.Selection(tracking=True, capture=True, auto_update=False, agent_rules=False)
    requested = set(setup.grants_for(everything))
    tabled = {g for grants in setup.CAPABILITY_GRANTS.values() for g in grants}
    assert requested == tabled

    for capability in (Capability.TRACKING, Capability.CAPTURE):
        needed = list(setup.CAPABILITY_GRANTS[capability])
        # Every grant the table names must be able to block its own capability.
        assert setup.blocked_by_missing_grants(capability, needed=needed, granted={}) == needed


# --- the settings screen ---------------------------------------------------


def _settings_main():
    import sys

    # NOT `from probe.cli import main` -- probe/cli/__init__.py defines a main()
    # FUNCTION that shadows the submodule of the same name.
    import probe.cli.main  # noqa: F401

    return sys.modules["probe.cli.main"]


def test_the_defaults_row_flips_the_machine_default_and_keeps_the_config(isolate, monkeypatch):
    """The one behavior the Defaults row exists for: the flip LANDS, device-wide.

    Device-wide means the file `session_marker.default_tracking()` reads --
    the same one `probe session default` writes -- and the write must go
    through the config writer, not replace the file: a config that also holds
    contexts and credentials has to come out the other side still holding them.
    """
    import json as jsonlib

    from probe.sdk import session_marker

    cli_main = _settings_main()
    monkeypatch.delenv("PROBE_SESSION_TRACKING", raising=False)

    path = session_marker.config_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        jsonlib.dumps({"contexts": {"default": {"base_url": "https://api.test"}}}),
        encoding="utf-8",
    )
    assert session_marker.default_tracking() is True  # shipped default

    monkeypatch.setattr(setup, "interactive", lambda: True)
    monkeypatch.setattr(setup, "daemon_availability", lambda base_url=None: (None, None))
    monkeypatch.setattr(setup, "run_defaults_menu", lambda current, **kw: "read-only")
    from probe.cli import tui

    monkeypatch.setattr(tui, "clear", lambda: None)

    assert cli_main._run_defaults_action(yes=False, base_now="https://api.test") == [
        "Probe in new sessions → read"
    ]

    data = jsonlib.loads(path.read_text(encoding="utf-8"))
    # BOTH keys, as `write_default_state` lays them down: the new one carries
    # the state, the old one the two-valued projection older clients read.
    assert data["defaults"]["session_state"] == "read-only"
    assert data["defaults"]["session_tracking"] == "off"
    assert data["contexts"]["default"]["base_url"] == "https://api.test", (
        "the toggle must edit the config, not replace it"
    )
    assert session_marker.default_tracking() is False


def test_folder_default_writer_changes_only_the_tracking_key(isolate, tmp_path):
    import json as jsonlib

    from probe.sdk import session_marker

    folder = tmp_path / "repo"
    config = folder / ".probe" / "config.json"
    config.parent.mkdir(parents=True)
    config.write_text(
        jsonlib.dumps(
            {
                "repo_setting": "keep",
                "defaults": {"session_tracking": "off", "future_default": 7},
            }
        ),
        encoding="utf-8",
    )
    config.chmod(0o644)

    written = session_marker.write_folder_tracking_default(folder, True)

    assert written == config
    # BOTH KEYS. Readers prefer `session_state`, so a boolean writer that moved
    # only `session_tracking` would leave a stale state winning and the screen
    # would report a setting that never took effect.
    assert jsonlib.loads(config.read_text(encoding="utf-8")) == {
        "repo_setting": "keep",
        "defaults": {
            "session_tracking": "on",
            "session_state": "full",
            "future_default": 7,
        },
    }
    assert config.stat().st_mode & 0o777 == 0o644


def test_folder_default_writer_creates_an_ordinary_repository_file(isolate, tmp_path):
    from probe.sdk import session_marker

    folder = tmp_path / "repo"
    folder.mkdir()

    config = session_marker.write_folder_tracking_default(folder, True)

    assert config.stat().st_mode & 0o777 == 0o644


def test_folder_default_writer_does_not_migrate_repository_json(isolate, tmp_path):
    import json as jsonlib

    from probe.sdk import session_marker

    folder = tmp_path / "repo"
    config = folder / ".probe" / "config.json"
    config.parent.mkdir(parents=True)
    config.write_text(jsonlib.dumps({"base_url": "repo-metadata"}), encoding="utf-8")

    session_marker.write_folder_tracking_default(folder, False)

    assert jsonlib.loads(config.read_text(encoding="utf-8")) == {
        "base_url": "repo-metadata",
        "defaults": {"session_tracking": "off", "session_state": "read-only"},
    }


def test_folder_default_writer_inherit_removes_only_its_key(isolate, tmp_path):
    import json as jsonlib

    from probe.sdk import session_marker

    folder = tmp_path / "repo"
    config = folder / ".probe" / "config.json"
    config.parent.mkdir(parents=True)
    config.write_text(
        jsonlib.dumps(
            {
                "repo_setting": "keep",
                "defaults": {"session_tracking": "on", "future_default": 7},
            }
        ),
        encoding="utf-8",
    )

    session_marker.write_folder_tracking_default(folder, None)

    assert jsonlib.loads(config.read_text(encoding="utf-8")) == {
        "repo_setting": "keep",
        "defaults": {"future_default": 7},
    }


def test_folder_default_writer_inherit_persists_empty_object(isolate, tmp_path):
    import json as jsonlib

    from probe.sdk import session_marker

    folder = tmp_path / "repo"
    config = folder / ".probe" / "config.json"
    config.parent.mkdir(parents=True)
    config.write_text(
        jsonlib.dumps({"defaults": {"session_tracking": "off"}}), encoding="utf-8"
    )

    session_marker.write_folder_tracking_default(folder, None)

    assert jsonlib.loads(config.read_text(encoding="utf-8")) == {}
    assert config.is_file()


@pytest.mark.parametrize("broken", ["{not json", "[1, 2]"])
def test_folder_default_writer_refuses_a_broken_file(isolate, tmp_path, broken):
    from probe.sdk import session_marker
    from probe.sdk.config import ConfigUnreadable

    folder = tmp_path / "repo"
    config = folder / ".probe" / "config.json"
    config.parent.mkdir(parents=True)
    config.write_text(broken, encoding="utf-8")

    with pytest.raises(ConfigUnreadable):
        session_marker.write_folder_tracking_default(folder, True)

    assert config.read_text(encoding="utf-8") == broken


def test_folder_default_writer_refuses_invalid_utf8(isolate, tmp_path):
    from probe.sdk import session_marker
    from probe.sdk.config import ConfigUnreadable

    folder = tmp_path / "repo"
    config = folder / ".probe" / "config.json"
    config.parent.mkdir(parents=True)
    broken = b'\xff{"defaults":{"session_tracking":"off"}}'
    config.write_bytes(broken)

    with pytest.raises(ConfigUnreadable):
        session_marker.write_folder_tracking_default(folder, True)

    assert config.read_bytes() == broken


def test_folder_default_writer_refuses_non_object_defaults(isolate, tmp_path):
    import json as jsonlib

    from probe.sdk import session_marker
    from probe.sdk.config import ConfigUnreadable

    folder = tmp_path / "repo"
    config = folder / ".probe" / "config.json"
    config.parent.mkdir(parents=True)
    original = {"repo_setting": "keep", "defaults": "future-format"}
    config.write_text(jsonlib.dumps(original), encoding="utf-8")

    with pytest.raises(ConfigUnreadable):
        session_marker.write_folder_tracking_default(folder, True)

    assert jsonlib.loads(config.read_text(encoding="utf-8")) == original


def test_folder_default_writer_refuses_a_fifo_without_replacing_it(isolate, tmp_path):
    import errno
    import os
    import stat
    import threading
    import time as time_module

    from probe.sdk import session_marker
    from probe.sdk.config import ConfigUnreadable

    folder = tmp_path / "repo"
    config = folder / ".probe" / "config.json"
    config.parent.mkdir(parents=True)
    fifo = tmp_path / "folder-config.fifo"
    os.mkfifo(fifo)
    config.symlink_to(fifo)

    def feed() -> None:
        deadline = time_module.monotonic() + 0.5
        while time_module.monotonic() < deadline:
            try:
                fd = os.open(fifo, os.O_WRONLY | os.O_NONBLOCK)
            except OSError as exc:
                if exc.errno != errno.ENXIO:
                    return
                time_module.sleep(0.01)
                continue
            try:
                os.write(fd, b"{}")
            except OSError:
                pass
            finally:
                os.close(fd)
            return

    feeder = threading.Thread(target=feed, daemon=True)
    feeder.start()

    with pytest.raises(ConfigUnreadable, match="regular file"):
        session_marker.write_folder_tracking_default(folder, True)
    feeder.join(timeout=1)

    assert config.is_symlink()
    assert stat.S_ISFIFO(fifo.stat().st_mode)


def test_folder_default_writer_refuses_an_oversized_file_unchanged(isolate, tmp_path):
    from probe.sdk import session_marker
    from probe.sdk.config import ConfigUnreadable

    folder = tmp_path / "repo"
    config = folder / ".probe" / "config.json"
    config.parent.mkdir(parents=True)
    original = b'{"defaults":{"session_tracking":"off"}}' + b" " * 70_000
    config.write_bytes(original)

    with pytest.raises(ConfigUnreadable, match="size limit"):
        session_marker.write_folder_tracking_default(folder, True)

    assert config.read_bytes() == original


def test_folder_default_writer_accepts_exact_size_limit_and_output_is_readable(
    isolate, tmp_path
):
    import json as jsonlib

    from probe.sdk import session_marker

    folder = tmp_path / "repo"
    config = folder / ".probe" / "config.json"
    config.parent.mkdir(parents=True)
    # THE LIMIT IS ON WHAT GETS WRITTEN, so the file is sized to land exactly
    # at it AFTER the write. The writer now puts down `session_state` beside
    # `session_tracking` (see write_folder_state_default), so the output is one
    # key larger than the input -- padding built against the input alone would
    # be testing that the cap is one key loose, which it is not.
    written = {
        "defaults": {"session_tracking": "off", "session_state": "read-only"},
        "future_padding": "",
    }
    empty = jsonlib.dumps(written, indent=2, sort_keys=True).encode("utf-8")
    padding = "x" * (65_536 - len(empty))

    data = {"defaults": {"session_tracking": "off"}, "future_padding": padding}
    config.write_bytes(jsonlib.dumps(data, indent=2, sort_keys=True).encode("utf-8"))

    session_marker.write_folder_tracking_default(folder, False)

    assert len(config.read_bytes()) == 65_536
    assert session_marker.folder_tracking_override(folder) is False


def test_folder_default_writer_refuses_output_above_size_limit_unchanged(
    isolate, tmp_path
):
    import json as jsonlib

    from probe.sdk import session_marker
    from probe.sdk.config import ConfigUnreadable

    folder = tmp_path / "repo"
    config = folder / ".probe" / "config.json"
    config.parent.mkdir(parents=True)
    data = {"defaults": {"future_default": 7}, "future_padding": ""}
    empty = jsonlib.dumps(data, indent=2, sort_keys=True).encode("utf-8")
    data["future_padding"] = "x" * (65_536 - len(empty))
    original = jsonlib.dumps(data, indent=2, sort_keys=True).encode("utf-8")
    assert len(original) == 65_536
    config.write_bytes(original)

    with pytest.raises(ConfigUnreadable, match="size limit"):
        session_marker.write_folder_tracking_default(folder, True)

    assert config.read_bytes() == original


def test_folder_default_writer_refuses_pretty_output_above_limit_unchanged(
    isolate, tmp_path
):
    import json as jsonlib

    from probe.sdk import session_marker
    from probe.sdk.config import ConfigUnreadable

    folder = tmp_path / "repo"
    config = folder / ".probe" / "config.json"
    config.parent.mkdir(parents=True)
    data = {
        "defaults": {"session_tracking": "off"},
        "future_settings": {f"key_{index:04d}": "v" for index in range(4_000)},
    }
    compact = jsonlib.dumps(data, separators=(",", ":")).encode("utf-8")
    pretty = jsonlib.dumps(data, indent=2, sort_keys=True).encode("utf-8")
    assert len(compact) < 65_536 < len(pretty)
    config.write_bytes(compact)

    with pytest.raises(ConfigUnreadable, match="size limit"):
        session_marker.write_folder_tracking_default(folder, True)

    assert config.read_bytes() == compact


def test_symlink_alias_writers_share_one_lock_and_preserve_both_updates(
    isolate, tmp_path, monkeypatch
):
    import json as jsonlib
    import threading

    from probe.sdk import config as sdk_config
    from probe.sdk import session_marker

    target = tmp_path / "shared" / "config.json"
    target.parent.mkdir()
    target.write_text(
        jsonlib.dumps(
            {
                "version": 2,
                "current_context": "default",
                "contexts": {"default": {}},
            }
        ),
        encoding="utf-8",
    )
    folder = tmp_path / "repo"
    folder_alias = folder / ".probe" / "config.json"
    folder_alias.parent.mkdir(parents=True)
    folder_alias.symlink_to(target)
    machine_alias = tmp_path / "machine-config.json"
    machine_alias.symlink_to(target)
    monkeypatch.setenv("PROBE_CONFIG_PATH", str(machine_alias))

    first_loaded = threading.Event()
    release_first = threading.Event()
    second_done = threading.Event()
    failures: list[BaseException] = []
    real_load = sdk_config._load_json_file

    def gated_load(path, **kwargs):
        data = real_load(path, **kwargs)
        if threading.current_thread().name == "folder-alias-writer":
            first_loaded.set()
            if not release_first.wait(timeout=3):
                raise AssertionError("test did not release first writer")
        return data

    monkeypatch.setattr(sdk_config, "_load_json_file", gated_load)

    def folder_write() -> None:
        try:
            session_marker.write_folder_tracking_default(folder, True)
        except BaseException as exc:
            failures.append(exc)

    def machine_write() -> None:
        try:
            sdk_config.save_context({"token": "probe_pat_KEEP"})
        except BaseException as exc:
            failures.append(exc)
        finally:
            second_done.set()

    first = threading.Thread(target=folder_write, name="folder-alias-writer")
    first.start()
    assert first_loaded.wait(timeout=1)
    second = threading.Thread(target=machine_write, name="machine-alias-writer")
    second.start()
    assert not second_done.wait(timeout=1), "second alias must wait on the target lock"
    release_first.set()
    first.join(timeout=3)
    second.join(timeout=3)

    assert failures == []
    assert not first.is_alive()
    assert not second.is_alive()
    assert folder_alias.is_symlink()
    assert machine_alias.is_symlink()
    assert jsonlib.loads(target.read_text(encoding="utf-8")) == {
        "version": 2,
        "current_context": "default",
        "contexts": {"default": {"token": "probe_pat_KEEP"}},
        "defaults": {"session_tracking": "on", "session_state": "full"},
    }


def test_folder_default_writer_follows_a_config_symlink(isolate, tmp_path):
    import json as jsonlib

    from probe.sdk import session_marker

    folder = tmp_path / "repo"
    config = folder / ".probe" / "config.json"
    target = tmp_path / "dotfiles" / "repo-probe.json"
    config.parent.mkdir(parents=True)
    target.parent.mkdir()
    target.write_text(jsonlib.dumps({"repo_setting": "keep"}), encoding="utf-8")
    config.symlink_to(target)

    session_marker.write_folder_tracking_default(folder, True)

    assert config.is_symlink()
    assert jsonlib.loads(target.read_text(encoding="utf-8")) == {
        "repo_setting": "keep",
        "defaults": {"session_tracking": "on", "session_state": "full"},
    }


def test_the_plugin_hooks_read_the_default_the_wizard_wrote(isolate, monkeypatch):
    """Device-wide includes the OTHER reader: the vendored hook copy.

    The status line and the session hooks run the plugin's `_session_marker`,
    not the SDK's, so a flip only counts if THAT copy sees it too. The parity
    test guards the files being identical; this guards the behavior end to
    end through a standalone import of the vendored file.
    """
    import importlib.util
    from pathlib import Path

    from probe.sdk import session_marker

    monkeypatch.delenv("PROBE_SESSION_TRACKING", raising=False)
    session_marker.write_default_tracking(False)

    copy = (
        Path(__file__).resolve().parent.parent
        / "plugins"
        / "probe-research"
        / "hooks"
        / "_session_marker.py"
    )
    spec = importlib.util.spec_from_file_location("vendored_session_marker", copy)
    vendored = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(vendored)
    assert vendored.default_tracking() is False

    session_marker.write_default_tracking(True)
    assert vendored.default_tracking() is True


def test_settings_headless_reports_instead_of_answering_for_you(isolate, monkeypatch):
    """`--yes` and a pipe both get the state and the command, never a flip."""
    from probe.sdk import session_marker

    cli_main = _settings_main()
    monkeypatch.delenv("PROBE_SESSION_TRACKING", raising=False)

    for kwargs in ({"yes": True},):
        lines = cli_main._run_settings_action(**kwargs)
        assert any("Probe in new sessions" in line for line in lines)
        assert any("probe session default" in line for line in lines)
    assert not session_marker.config_path().is_file(), "reporting must not write"


def test_defaults_headless_reports_instead_of_answering_for_you(isolate, monkeypatch):
    """`--action defaults` from a script gets the state and the command, and a
    held env override gets the state and why the picker is not drawn -- never a
    flip, and never a screen that would write under a variable that wins."""
    from probe.sdk import session_marker

    cli_main = _settings_main()
    monkeypatch.delenv("PROBE_SESSION_TRACKING", raising=False)
    monkeypatch.delenv("PROBE_SESSION_STATE", raising=False)

    lines = cli_main._run_defaults_action(yes=True)
    assert any("Probe in new sessions" in line for line in lines)
    assert any("probe session default" in line for line in lines)

    monkeypatch.setattr(setup, "interactive", lambda: True)
    monkeypatch.setattr(setup, "run_defaults_menu", lambda *a, **k: pytest.fail("drawn under env"))
    monkeypatch.setenv("PROBE_SESSION_STATE", "off")
    lines = cli_main._run_defaults_action(yes=False)
    assert any("env wins" in line for line in lines), lines
    assert any("Unset that variable" in line for line in lines), lines
    assert not session_marker.config_path().is_file(), "reporting must not write"


def test_choosing_the_current_default_or_backing_out_changes_nothing(isolate, monkeypatch):
    """The picker opens on the current state, so Enter straight away is a
    no-op -- and a no-op returns None, which sends the menu straight back
    without a page to press through or a config write."""
    from probe.cli import tui
    from probe.sdk import session_marker

    cli_main = _settings_main()
    monkeypatch.delenv("PROBE_SESSION_TRACKING", raising=False)
    monkeypatch.delenv("PROBE_SESSION_STATE", raising=False)
    monkeypatch.setattr(setup, "interactive", lambda: True)
    monkeypatch.setattr(setup, "daemon_availability", lambda base_url=None: (None, None))
    monkeypatch.setattr(tui, "clear", lambda: None)

    for answer in (session_marker.DEFAULT_STATE, tui.BACK, None):
        monkeypatch.setattr(setup, "run_defaults_menu", lambda current, _a=answer, **k: _a)
        assert cli_main._run_defaults_action(yes=False, base_now="https://api.test") is None
    assert not session_marker.config_path().is_file(), "nothing chosen, nothing written"


def test_a_state_saved_from_the_menu_row_skips_the_picker(isolate, monkeypatch):
    """`←`/`→` then Enter on the menu row hands the state straight to the
    save: no picker, and -- when saving is all that happened -- no page to
    press through either; the row coming back wearing the new state is the
    confirmation."""
    from probe.cli import tui
    from probe.sdk import session_marker

    cli_main = _settings_main()
    monkeypatch.delenv("PROBE_SESSION_TRACKING", raising=False)
    monkeypatch.delenv("PROBE_SESSION_STATE", raising=False)
    monkeypatch.setattr(setup, "interactive", lambda: True)
    monkeypatch.setattr(setup, "run_defaults_menu", lambda *a, **k: pytest.fail("picker drawn"))
    monkeypatch.setattr(
        setup, "daemon_availability", lambda base_url=None: pytest.fail("asked for no daemon")
    )
    monkeypatch.setattr(tui, "clear", lambda: None)

    assert cli_main._run_defaults_action(
        yes=False, base_now="https://api.test", chosen="read-only"
    ) is None
    assert session_marker.default_session_state() == session_marker.STATE_READ_ONLY


def test_the_menu_row_never_saves_daemon_and_asks_no_server(isolate, monkeypatch):
    """The row walks on / read / off; a `daemon` reaching it (an old caller) reads
    as `on` -- what the row already holds -- so nothing is written and no server
    is asked. The daemon is the "Who records" row's (Richard 2026-09-29)."""
    from probe.sdk import session_marker

    cli_main = _settings_main()
    asked = []
    monkeypatch.delenv("PROBE_SESSION_TRACKING", raising=False)
    monkeypatch.delenv("PROBE_SESSION_STATE", raising=False)
    monkeypatch.setattr(setup, "interactive", lambda: True)
    monkeypatch.setattr(setup, "daemon_availability", lambda base_url=None: asked.append(1) or (True, None))
    assert cli_main._run_defaults_action(yes=False, base_now="https://api.test", chosen="daemon") is None
    assert not session_marker.config_path().is_file(), "nothing written"
    assert asked == []


def test_settings_env_override_is_disclosed(isolate, monkeypatch):
    """PROBE_SESSION_TRACKING beats the file, so flipping under it changes
    nothing visible -- the screen must say so rather than let the toggle lie."""
    monkeypatch.setenv("PROBE_SESSION_TRACKING", "off")
    lines = setup.describe_settings()
    assert any("PROBE_SESSION_TRACKING" in line for line in lines)
    assert any("env wins" in line for line in lines)

    # A typo like `of` is IGNORED by default_tracking, so the screen must not
    # call it an override -- that would misdiagnose the typo as a broken toggle.
    monkeypatch.setenv("PROBE_SESSION_TRACKING", "of")
    lines = setup.describe_settings()
    assert any("unrecognized, ignored" in line for line in lines)
    assert not any("env wins" in line for line in lines)

    # And raw escape bytes from the environment never reach the terminal.
    monkeypatch.setenv("PROBE_SESSION_TRACKING", "\x1b]0;pwned\x07off")
    lines = setup.describe_settings()
    assert not any("\x1b" in line for line in lines)


def test_settings_is_a_device_action():
    """One config file: no agent question, one pass, exactly like Account."""
    from probe.cli.actions import ACCOUNT_ACTIONS, DEVICE_ACTIONS, Action

    assert Action.SETTINGS in DEVICE_ACTIONS
    assert Action.DEFAULTS in DEVICE_ACTIONS
    assert ACCOUNT_ACTIONS <= DEVICE_ACTIONS


def test_a_broken_config_fails_the_toggle_loudly_instead_of_being_replaced(isolate, monkeypatch):
    """`write_default_tracking` must never write through a failed read.

    A config file that will not parse holds credentials and contexts in some
    unknown state; falling back to `{}` and saving would replace all of it
    with just this preference. The contract is raise-and-touch-nothing.
    """
    import pytest as _pytest

    from probe.sdk import session_marker
    from probe.sdk.config import ConfigUnreadable

    monkeypatch.delenv("PROBE_SESSION_TRACKING", raising=False)
    path = session_marker.config_path()
    path.parent.mkdir(parents=True, exist_ok=True)

    # Malformed JSON and valid-but-non-object JSON are BOTH refusals: the
    # strict loader treats each as "a file I cannot safely rewrite".
    for broken in ("{not json", "[1, 2]"):
        path.write_text(broken, encoding="utf-8")
        with _pytest.raises(ConfigUnreadable):
            session_marker.write_default_tracking(False)
        assert path.read_text(encoding="utf-8") == broken, (
            "a failed read must leave the file byte-for-byte untouched"
        )


def _defaults_picker_rows(monkeypatch, current, **gate):
    """The Defaults picker's choices and default, as `run_defaults_menu` hands
    them to questionary -- captured, not rebuilt, so the test reads the real list."""
    import questionary

    from probe.cli import tui

    captured = {}
    real_checkbox = questionary.checkbox

    def spy_checkbox(message, *, choices, **kwargs):
        captured.update(message=message, choices=choices)
        return real_checkbox(message, choices=choices, **kwargs)

    monkeypatch.setattr(questionary, "checkbox", spy_checkbox)
    monkeypatch.setattr(tui, "ask", lambda q, height=None, **kw: tui.BACK)
    assert setup.run_defaults_menu(current, **gate) is tui.BACK
    values = [
        c.value
        for c in captured["choices"]
        if isinstance(c, questionary.Choice)
        and not isinstance(c, questionary.Separator)
        and c.value != setup.NAV_BAND
    ]
    return captured, values


def test_the_handler_skips_the_picker_under_a_recognized_env(isolate, monkeypatch):
    """The handler, not the screen, decides the lock -- from the parser's own
    recognition, so a typo like `of` still gets a working picker."""
    from probe.cli import tui

    cli_main = _settings_main()
    drawn = []

    monkeypatch.setattr(setup, "interactive", lambda: True)
    monkeypatch.setattr(setup, "daemon_availability", lambda base_url=None: (None, None))
    monkeypatch.setattr(
        setup, "run_defaults_menu", lambda current, **kw: drawn.append(current) or tui.BACK
    )
    monkeypatch.setattr(tui, "clear", lambda: None)
    monkeypatch.delenv("PROBE_SESSION_STATE", raising=False)

    monkeypatch.setenv("PROBE_SESSION_TRACKING", "on")
    assert cli_main._run_defaults_action(yes=False, base_now="https://api.test")
    assert drawn == [], "a recognized override holds the default down: no picker"

    monkeypatch.setenv("PROBE_SESSION_TRACKING", "of")  # a typo is not a lock
    assert cli_main._run_defaults_action(yes=False, base_now="https://api.test") is None
    assert len(drawn) == 1


def test_backing_out_and_empty_diffs_say_nothing_happened(isolate, monkeypatch):
    """None is the \"nothing happened\" signal the wizard loop acts on.

    It is what lets `←` land back on the menu INSTANTLY: no result page, no
    \"press enter\" pause, and no per-agent state re-collection -- the stall
    the first ship of this screen turned Back into. An apply whose boxes
    match what is already stored is the same nothing.
    """
    from probe.cli import tui
    from probe.sdk import session_marker

    cli_main = _settings_main()
    monkeypatch.delenv("PROBE_SESSION_TRACKING", raising=False)
    monkeypatch.setattr(setup, "interactive", lambda: True)
    monkeypatch.setattr(tui, "clear", lambda: None)

    monkeypatch.setattr(setup, "run_settings_menu", lambda current, **kw: tui.BACK)
    assert cli_main._run_settings_action(
        yes=False, caps_by_source={"claude_code": _caps()}, base_now="https://api.test"
    ) is None

    # Boxes returned exactly as they were: no write, not even a config file.
    monkeypatch.setattr(setup, "run_settings_menu", lambda current, **kw: dict(current))
    assert cli_main._run_settings_action(
        yes=False, caps_by_source={"claude_code": _caps()}, base_now="https://api.test"
    ) is None
    assert not session_marker.config_path().is_file(), "an unchanged apply must not write"


def test_a_v1_config_keeps_the_tracking_default_across_migration(isolate, monkeypatch):
    """CLIs through 0.95.1 wrote `defaults` into v1-shaped files raw.

    Without the migration hoist, the next canonical write wraps that key into
    the context -- where `default_tracking` never looks -- and a researcher's
    explicit `off` silently becomes `on`. The hoist is what keeps the
    already-shipped files honest.
    """
    import json as jsonlib

    from probe.sdk import config as sdk_config
    from probe.sdk import session_marker

    monkeypatch.delenv("PROBE_SESSION_TRACKING", raising=False)
    path = session_marker.config_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        jsonlib.dumps(
            {
                "base_url": "https://api.test",
                "token": "t1",
                "defaults": {"session_tracking": "off"},
            }
        ),
        encoding="utf-8",
    )

    data = sdk_config.load_file(strict=True)
    assert data["defaults"]["session_tracking"] == "off"
    assert "defaults" not in data["contexts"]["default"]

    sdk_config.save_context({"token": "t2"}, name="default")  # a later canonical write
    assert session_marker.default_tracking() is False, "the explicit off must survive"
    on_disk = jsonlib.loads(path.read_text(encoding="utf-8"))
    assert on_disk["contexts"]["default"]["token"] == "t2"


def test_the_settings_registry_cannot_drift_silently(monkeypatch):
    """Same guard the action menu carries: groups, copy, and the enum must
    agree, and a writer-less setting REFUSES instead of no-opping."""
    import pytest as _pytest

    assert setup.grouped_settings() == setup.SETTINGS_GROUPS

    monkeypatch.setattr(setup, "SETTINGS_COPY", {})
    with _pytest.raises(AssertionError):
        setup.grouped_settings()


def test_apply_settings_refuses_a_setting_it_has_no_writer_for():
    import pytest as _pytest

    ghost = "definitely_not_a_setting"
    with _pytest.raises(AssertionError):
        setup.apply_settings({ghost: True})


def test_apply_settings_reports_failures_in_place(isolate, monkeypatch):
    """Per-setting failure lines, never a raise: with two settings in one
    commit, raising after the first write would leave it silently applied
    while the screen reported only the failure."""
    from probe.sdk import session_marker

    def boom(value):
        raise OSError("disk said no")

    monkeypatch.setattr(session_marker, "write_default_state", boom)
    lines = setup.apply_settings({setup.Setting.TRACKING_DEFAULT: "read-only"})
    assert lines == ["! could not set the Probe default for new sessions: disk said no"]


def test_the_state_block_and_the_boxes_share_one_read(isolate, monkeypatch):
    """A write landing between two reads must not make the state line
    disagree with the box beside it -- the block derives from the SAME
    snapshot the boxes are drawn from."""
    monkeypatch.delenv("PROBE_SESSION_TRACKING", raising=False)
    # The file says nothing (fresh machine => on); the snapshot says off.
    lines = setup.describe_settings({setup.Setting.TRACKING_DEFAULT: "off"})
    assert any("Probe in new sessions" in line and "off" in line for line in lines)


def test_the_picker_answer_becomes_a_full_settings_map(isolate, monkeypatch):
    """A submitted answer must come back as a value for EVERY drawn setting --
    unticked is `False`, not absent, and a cycling row answers with its STATE.

    The checkbox rows read out of the submitted list. The cycling rows do not
    and must not: a state cannot be spelled in a membership list, so they
    answer from `probe_cycle` -- which is why a pick list that names one here
    still comes back as the state the row was actually left in. A setting the
    screen does not draw (the default for new sessions, Who records) is not in
    the answer; the daemon's page answers for its own rows only."""
    from probe.cli import tui

    current = _settings_defaults()

    monkeypatch.setattr(tui, "ask", lambda q, height=None: [setup.Setting.AUTO_UPDATE])
    assert setup.run_settings_menu(current) == {setup.Setting.AUTO_UPDATE: True}
    monkeypatch.setattr(tui, "ask", lambda q, height=None: [])
    assert setup.run_settings_menu(current) == {setup.Setting.AUTO_UPDATE: False}

    monkeypatch.setattr(tui, "ask", lambda q, height=None: [setup.Setting.REASONING_SUMMARIES])
    assert setup.run_settings_menu(current, groups=setup.DAEMON_GROUPS) == {
        setup.Setting.REASONING_SUMMARIES: True
    }


def test_the_settings_band_is_dropped_when_we_cannot_own_the_keys(isolate, monkeypatch):
    """Same rule as the capability picker: an unwirable band is a row that
    says `‹ Back` while Enter submits -- strip it and let the library's own
    keys run, with an instruction that tells the truth about them."""
    import questionary

    from probe.cli import tui

    monkeypatch.delenv("PROBE_SESSION_TRACKING", raising=False)
    monkeypatch.setattr(tui, "checkbox_control", lambda q: None)
    built = []
    real_checkbox = questionary.checkbox

    def spy_checkbox(message, *, choices, instruction=None, **kwargs):
        built.append((choices, instruction))
        return real_checkbox(message, choices=choices, instruction=instruction, **kwargs)

    monkeypatch.setattr(questionary, "checkbox", spy_checkbox)
    monkeypatch.setattr(tui, "ask", lambda q, height=None: [])

    # A cycling row cannot cycle on this path -- our keys never loaded -- so
    # it degrades to the two states a questionary box can spell. A "Who
    # records" box is ticked at `agent` (its first position), so an EMPTIED
    # box is the other position, `daemon`.
    result = setup.run_settings_menu(_settings_defaults())
    assert result == {
        setting: "daemon" if setting in setup.RECORDER_SETTINGS else False
        for setting in _settings_rows()
    }
    final_choices, final_instruction = built[-1]
    assert not any(setup.BACK_TITLE in str(getattr(c, "title", "")) for c in final_choices), (
        "the band goes, so no row advertises a key nothing is listening for"
    )
    assert "enter to apply" in final_instruction


def test_the_loop_distinguishes_backed_out_from_streamed():
    """The load-bearing comparison is `lines is not None`, twice -- once for
    the pause, once for the state re-read. `[]` means "streamed, state may
    have changed" (configure's return); None means "nothing happened".
    Simplifying either to truthiness passes every stubbed test and silently
    stops the menu reflecting what an install just changed -- so the exact
    spelling is pinned here."""
    import inspect

    cli_main = _settings_main()
    source = inspect.getsource(cli_main._wizard_session)
    assert source.count("lines is not None") >= 2, (
        "the pause gate and the re-read gate must both distinguish None from []"
    )


# --- the guided flow's new seams --------------------------------------------


def test_the_degraded_confirm_screen_is_honest_about_missing_agents():
    """A GPU pod has neither `claude` nor `codex`, so promising plugin rows
    would promise work this run cannot do -- and nothing is queued for later,
    so the honest line names the recovery: re-run and pick Install."""
    rows = setup.confirm_rows(("claude_code",), plugins_available=False)
    text = "\n".join(rows)

    assert "skipped" in text, text
    assert "probe wizard" in text and "Install Probe" in text, (
        "the degraded screen must name the recovery, not promise a queue"
    )
    assert "sign-in" in text, "what still happens is on screen too"
    assert "Session capture" not in text, "no row may promise what cannot install"


def test_the_degraded_confirm_screen_is_honest_about_pi_too():
    """A machine with Claude Code AND pi, but no `claude` binary: the degraded
    screen is computed from `MARKETPLACE_AGENT_SOURCES` alone (see main.py's
    `plugin_promising_sources`), so `plugins_available=False` reaches here
    even though pi's own install never depended on `claude` at all. Saying
    "Coding-agent plugins — skipped" about pi, the way it correctly does for
    Claude Code, would describe marketplace-plugin work pi's install does not
    do -- pi's `packages` entry still installs (tracking force-on reaches it
    regardless), so the screen must say that instead of "nothing is queued".
    """
    rows = setup.confirm_rows(
        ("claude_code", "pi"), plugins_available=False, unavailable=("claude_code",)
    )
    text = "\n".join(rows)

    assert "sign-in" in text
    assert "Claude Code" in text and "skipped" in text, "the absent marketplace agent is named"
    assert "settings.json" in text, "pi's own install mechanism is named, not silently dropped"
    assert "pi" in text.lower()


def test_a_pi_only_degraded_screen_never_claims_the_marketplace_bullet():
    """pi alone, `plugins_available=False`: there is no OTHER agent to call
    out as skipped, so the generic "Coding-agent plugins — skipped" bullet
    (which names Claude Code and Codex specifically) must not appear at all --
    pi is the only agent this run named, and pi's install is not skipped."""
    rows = setup.confirm_rows(("pi",), plugins_available=False)
    text = "\n".join(rows)

    assert "settings.json" in text
    assert "skipped" not in text, text
    assert "Neither Claude Code nor Codex" not in text, text


def test_the_confirm_screen_names_the_off_switch(monkeypatch):
    """The disclosure-gate's other half: with no boxes to untick, the screen
    must say how Probe comes off afterwards, or "complete by design" reads as
    "irreversible". It comes off WHOLE -- Uninstall -- since Settings stopped
    turning single capabilities off."""
    import questionary

    from probe.cli import tui

    captured = {}
    real_select = questionary.select

    def spy(message, **kwargs):
        captured["message"] = message
        return real_select(message, **kwargs)

    monkeypatch.setattr(questionary, "select", spy)
    monkeypatch.setattr(tui, "ask", lambda q, height=None, **kwargs: True)
    setup.run_confirm_install(("claude_code",))

    assert "Uninstall" in captured["message"], captured["message"]
    assert "Settings" not in captured["message"], "Settings no longer turns a part off"


def test_the_agent_screen_is_skipped_when_there_is_no_choice(monkeypatch):
    """The picker only appears when BOTH coding agents are on the machine: a
    question with one possible answer is a step for nothing."""
    import sys
    from types import SimpleNamespace

    from typer.testing import CliRunner

    from probe.cli import bootstrap
    from probe.cli import doctor as doctor_impl
    from probe.cli import plugin_cli
    from probe.cli import setup as wizard
    from probe.cli import tui
    from probe.cli.actions import Action
    import probe.cli.main  # noqa: F401

    cli_main = sys.modules["probe.cli.main"]
    monkeypatch.setattr(bootstrap, "ensure_persistent_install", lambda **_: SimpleNamespace(message=""))
    monkeypatch.setattr(plugin_cli, "available", lambda source: source == "claude_code")
    monkeypatch.setattr(
        doctor_impl,
        "collect",
        lambda: _caps(agent_source=os.environ.get("PROBE_AGENT", "claude_code")),
    )
    monkeypatch.setattr(wizard, "interactive", lambda: True)
    monkeypatch.setattr(tui, "clear", lambda: None)
    monkeypatch.setattr(tui, "page", lambda *args, **kwargs: None)

    events: list = []
    actions = iter((Action.CONFIGURE, Action.EXIT))
    monkeypatch.setattr(wizard, "run_action_menu", lambda _c: next(actions))
    monkeypatch.setattr(
        wizard, "run_agent_menu", lambda _d, action=None: events.append("agent") or ("claude_code",)
    )

    def confirm(sources, **kwargs):
        events.append(("confirm", tuple(sources), kwargs.get("step")))
        return True

    monkeypatch.setattr(wizard, "run_backfill_offer", lambda _s, **kw: set())
    monkeypatch.setattr(wizard, "run_confirm_install", confirm)

    def apply(*args, **kwargs):
        header = kwargs["progress_header"](0.0)
        assert "Step 2 of 3" in header[0]
        assert "━" in header[1] and "─" in header[1]
        return ["done"]

    monkeypatch.setattr(cli_main, "_run_wizard_action", apply)

    result = CliRunner().invoke(cli_main.app, ["wizard"])

    assert result.exit_code == 0, result.output
    assert "agent" not in events, "one agent on the machine means no agent screen"
    assert events == [("confirm", ("claude_code",), None)], (
        "the confirm screen opens the flow without counting the skipped agent screen"
    )


# --- settings: the capability rows' apply routes -----------------------------


def test_apply_settings_refuses_a_capability_setting():
    """By design, not drift: a capability applies through the CONFIGURE
    machinery (verification, the progress screen), so one landing in the bare
    config-write path must be loud."""
    import pytest as _pytest

    with _pytest.raises(AssertionError):
        setup.apply_settings({setup.Setting.AUTO_UPDATE: True})


def test_capability_settings_state_reads_the_union():
    """The box answers "does this device do X at all". Automatic updates is
    the only capability left with a row, and it is one device-wide file, so
    there is never a per-agent split to note."""
    caps_by_source = {
        "claude_code": _caps(auto_update_enabled=True),
        "codex": _caps(agent_source="codex"),
    }
    assert setup.capability_settings_state(caps_by_source) == {setup.Setting.AUTO_UPDATE: True}
    assert setup.capability_settings_state({"codex": _caps(agent_source="codex")}) == {
        setup.Setting.AUTO_UPDATE: False
    }


def test_settings_capability_toggles_route_through_the_configure_machinery(
    isolate, monkeypatch
):
    """Outside-voice finding #2, pinned: a Settings toggle and an Install apply
    are the same code asking for a different end state. Turning automatic
    updates on or off must reach `_run_wizard_action`'s CONFIGURE path per
    agent, and the target Selection must change ONLY the toggled row."""
    import os as _os

    from probe.cli import doctor as doctor_impl
    from probe.cli import tui
    from probe.cli.actions import Action

    cli_main = _settings_main()
    monkeypatch.delenv("PROBE_SESSION_TRACKING", raising=False)
    monkeypatch.setattr(setup, "interactive", lambda: True)
    monkeypatch.setattr(tui, "clear", lambda: None)

    claude = _caps(tracking_plugin_installed=True, logged_in_as="x@y.z")
    codex = _caps(agent_source="codex", tracking_plugin_installed=True, mcp_authenticated=True)
    caps_by_source = {"claude_code": claude, "codex": codex}
    monkeypatch.setattr(doctor_impl, "collect", lambda: claude)

    # The screen: automatic updates ticked ON (it was off everywhere).
    def menu(current, *, hidden=frozenset()):
        return {**current, setup.Setting.AUTO_UPDATE: True}

    monkeypatch.setattr(setup, "run_settings_menu", menu)

    calls: list[dict] = []

    def apply(action, **kwargs):
        calls.append(
            {
                "action": action,
                "agent": _os.environ.get("PROBE_AGENT"),
                "selection": kwargs.get("selection_override"),
                "yes": kwargs.get("yes"),
                "needs": kwargs.get("authorization_needs"),
            }
        )
        return ["ok"]

    monkeypatch.setattr(cli_main, "_run_wizard_action", apply)

    lines = cli_main._run_settings_action(
        yes=False, caps_by_source=caps_by_source, base_now="https://api.test"
    )

    assert [c["action"] for c in calls] == [Action.CONFIGURE, Action.CONFIGURE], (
        "capability toggles must run the CONFIGURE machinery, once per agent"
    )
    assert [c["agent"] for c in calls] == ["claude_code", "codex"], (
        "each agent's apply must run under its own PROBE_AGENT target"
    )
    for call in calls:
        assert call["yes"] is True, "the screen already answered; the apply must not re-ask"
        assert call["selection"].auto_update is True, "the toggled row changed"
        assert call["selection"].tracking is True, "a capability with no row kept its state"
        assert call["selection"].capture is False, "...and an OFF one stayed off"
        assert call["needs"] == [], "no row left on this screen needs a browser approval"
    assert lines and any("Claude Code" in line for line in lines), (
        "per-agent results are labelled"
    )


# --- the review's regression pins ------------------------------------------


def test_an_untouched_tracking_row_survives_an_unrelated_toggle(isolate, monkeypatch):
    """THE UNION-BASELINE BUG, pinned. Plugin installed, signed out. Toggling
    AUTO_UPDATE must not hand the apply tracking=False — that uninstalls a
    plugin nobody asked about. The screen's predicates and the preserve
    baseline must be the same read (`capability_state_for`), or exactly this
    diverges."""
    from probe.cli import doctor as doctor_impl
    from probe.cli import tui

    cli_main = _settings_main()
    monkeypatch.delenv("PROBE_SESSION_TRACKING", raising=False)
    monkeypatch.setattr(setup, "interactive", lambda: True)
    monkeypatch.setattr(tui, "clear", lambda: None)

    from probe.cli.capabilities import Capability

    snapshot = _caps(tracking_plugin_installed=True)  # no logged_in_as
    caps_by_source = {"claude_code": snapshot}
    monkeypatch.setattr(doctor_impl, "collect", lambda: snapshot)

    assert setup.capability_state_for(snapshot)[Capability.TRACKING] is True

    def menu(current, *, hidden=frozenset()):
        picked = dict(current)
        picked[setup.Setting.AUTO_UPDATE] = True  # the only touched row
        return picked

    monkeypatch.setattr(setup, "run_settings_menu", menu)
    handed = []
    monkeypatch.setattr(
        cli_main,
        "_run_wizard_action",
        lambda a, **kw: handed.append(kw["selection_override"]) or ["ok"],
    )

    cli_main._run_settings_action(
        yes=False, caps_by_source=caps_by_source, base_now="https://api.test"
    )

    assert handed and handed[0].tracking is True, (
        "an untouched ON box must stay on; tracking=False uninstalls the plugin"
    )


def test_an_unrelated_toggle_cannot_enable_capture_on_the_agent_that_had_it_off(
    isolate, monkeypatch
):
    """The mixed-device half of the same bug: Claude captures, Codex does not.
    Toggling only AUTO_UPDATE must hand Codex a target whose capture is still
    False — the union baseline used to normalize Codex up to Claude's on,
    which re-paired a transcript grant nobody touched."""
    from probe.cli import doctor as doctor_impl
    from probe.cli import tui
    from probe.cli.capabilities import TokenSource

    cli_main = _settings_main()
    monkeypatch.delenv("PROBE_SESSION_TRACKING", raising=False)
    monkeypatch.setattr(setup, "interactive", lambda: True)
    monkeypatch.setattr(tui, "clear", lambda: None)

    claude = _caps(
        tracking_plugin_installed=True,
        capture_plugin_installed=True,
        capture_token_sources=(TokenSource.PAIRED_FILE,),
        logged_in_as="x@y.z",
    )
    codex = _caps(agent_source="codex", tracking_plugin_installed=True, mcp_authenticated=True)
    caps_by_source = {"claude_code": claude, "codex": codex}
    monkeypatch.setattr(doctor_impl, "collect", lambda: claude)

    def menu(current, *, hidden=frozenset()):
        picked = dict(current)
        picked[setup.Setting.AUTO_UPDATE] = not picked[setup.Setting.AUTO_UPDATE]
        return picked

    monkeypatch.setattr(setup, "run_settings_menu", menu)
    handed = {}

    needs_seen = []

    def apply(_action, **kwargs):
        handed[os.environ.get("PROBE_AGENT")] = kwargs["selection_override"]
        if kwargs.get("authorization_needs") is not None:
            needs_seen.append(kwargs["authorization_needs"])
        return ["ok"]

    monkeypatch.setattr(cli_main, "_run_wizard_action", apply)

    cli_main._run_settings_action(
        yes=False, caps_by_source=caps_by_source, base_now="https://api.test"
    )

    assert handed["claude_code"].capture is True, "Claude's own on-state is preserved"
    assert handed["codex"].capture is False, (
        "an unrelated toggle must not enable capture on the agent that had it off"
    )
    assert needs_seen and not needs_seen[0], (
        "no grant may be requested for rows nobody touched — a union-derived "
        "needs computation minted a capture credential for the ambient agent"
    )


def test_a_failing_agent_does_not_kill_the_settings_commit(isolate, monkeypatch):
    """The CONFIGURE path reports failure by raising typer.Exit. Escaping here
    would end the whole wizard mid-Settings and silently skip the second
    agent — each agent's failure is contained and labelled instead, and with
    no shared approval to stand down for, the second agent still runs."""
    import typer as typer_mod

    from probe.cli import doctor as doctor_impl
    from probe.cli import tui

    cli_main = _settings_main()
    monkeypatch.setattr(setup, "interactive", lambda: True)
    monkeypatch.setattr(tui, "clear", lambda: None)

    claude = _caps(tracking_plugin_installed=True, logged_in_as="x@y.z")
    codex = _caps(agent_source="codex", tracking_plugin_installed=True, mcp_authenticated=True)
    caps_by_source = {"claude_code": claude, "codex": codex}
    monkeypatch.setattr(doctor_impl, "collect", lambda: claude)
    monkeypatch.setattr(
        setup,
        "run_settings_menu",
        lambda current, *, hidden=frozenset(): {**current, setup.Setting.AUTO_UPDATE: True},
    )
    order = []

    def apply(_action, **kwargs):
        order.append(os.environ.get("PROBE_AGENT"))
        if len(order) == 1:
            raise typer_mod.Exit(1)
        return ["applied"]

    monkeypatch.setattr(cli_main, "_run_wizard_action", apply)

    lines = cli_main._run_settings_action(
        yes=False, caps_by_source=caps_by_source, base_now="https://api.test"
    )

    assert order == ["claude_code", "codex"], "one agent's failure must not skip the other"
    assert any("not finished" in line for line in lines), "the failure is reported, labelled"
    assert any("applied" in line for line in lines)


def test_install_on_a_pluginless_machine_matches_the_degraded_screen(monkeypatch):
    """The degraded confirm screen discloses CLI + sign-in and says the
    plugins are skipped; pressing Install must apply exactly that — no
    capture grant a bullet never named, no auto-update or rules either."""
    import sys
    from types import SimpleNamespace

    from typer.testing import CliRunner

    from probe.cli import bootstrap
    from probe.cli import doctor as doctor_impl
    from probe.cli import plugin_cli
    from probe.cli import setup as wizard
    from probe.cli import tui
    import probe.cli.main  # noqa: F401

    cli_main = sys.modules["probe.cli.main"]
    monkeypatch.setattr(bootstrap, "ensure_persistent_install", lambda **_: SimpleNamespace(message=""))
    monkeypatch.setattr(plugin_cli, "available", lambda _source: False)  # the GPU-pod shape
    monkeypatch.setattr(doctor_impl, "collect", lambda: _caps())
    monkeypatch.setattr(wizard, "interactive", lambda: True)
    monkeypatch.setattr(tui, "clear", lambda: None)
    monkeypatch.setattr(tui, "page", lambda *a, **k: None)

    seen = {}

    def confirm(sources, **kwargs):
        seen["plugins_available"] = kwargs.get("plugins_available")
        return True

    monkeypatch.setattr(wizard, "run_backfill_offer", lambda _s, **kw: set())
    monkeypatch.setattr(wizard, "run_confirm_install", confirm)
    monkeypatch.setattr(
        cli_main,
        "_run_wizard_action",
        lambda a, **kw: seen.update(selection=kw["selection_override"]) or ["done"],
    )

    result = CliRunner().invoke(cli_main.app, ["wizard", "--action", "configure"])

    assert result.exit_code == 0, result.output
    assert seen["plugins_available"] is False, "the degraded screen must be the one shown"
    assert seen["selection"].tracking is True, "the sign-in the screen promised still happens"
    assert seen["selection"].capture is False, (
        "capture had no disclosure bullet on the degraded screen; it must not enable"
    )
    assert seen["selection"].auto_update is False and seen["selection"].agent_rules is False, (
        "nothing the degraded screen never named may enable"
    )


def test_a_degraded_install_preserves_what_it_never_disclosed(monkeypatch):
    """A configured machine whose agent binaries are temporarily missing: the
    degraded screen names CLI + sign-in only, so Install must PRESERVE the
    capture/rules/auto-update it never mentioned — all-off would killswitch a
    live capture from a screen that said 'skipped'."""
    import sys
    from types import SimpleNamespace

    from typer.testing import CliRunner

    from probe.cli import bootstrap
    from probe.cli import doctor as doctor_impl
    from probe.cli import plugin_cli
    from probe.cli import setup as wizard
    from probe.cli import tui
    from probe.cli.capabilities import TokenSource
    import probe.cli.main  # noqa: F401

    cli_main = sys.modules["probe.cli.main"]
    monkeypatch.setattr(bootstrap, "ensure_persistent_install", lambda **_: SimpleNamespace(message=""))
    monkeypatch.setattr(plugin_cli, "available", lambda _source: False)  # binaries gone
    configured = _caps(
        tracking_plugin_installed=True,
        capture_plugin_installed=True,
        capture_token_sources=(TokenSource.PAIRED_FILE,),
        auto_update_enabled=True,
        agent_rules_installed=True,
        logged_in_as="x@y.z",
    )
    monkeypatch.setattr(doctor_impl, "collect", lambda: configured)
    monkeypatch.setattr(wizard, "interactive", lambda: True)
    monkeypatch.setattr(tui, "clear", lambda: None)
    monkeypatch.setattr(tui, "page", lambda *a, **k: None)
    monkeypatch.setattr(wizard, "run_backfill_offer", lambda _s, **kw: set())
    monkeypatch.setattr(wizard, "run_confirm_install", lambda *a, **k: True)

    seen = {}
    monkeypatch.setattr(
        cli_main,
        "_run_wizard_action",
        lambda a, **kw: seen.update(selection=kw["selection_override"]) or ["done"],
    )

    result = CliRunner().invoke(cli_main.app, ["wizard", "--action", "configure"])

    assert result.exit_code == 0, result.output
    assert seen["selection"].capture is True, "a live capture survives the degraded install"
    assert seen["selection"].auto_update is True and seen["selection"].agent_rules is True, (
        "undisclosed capabilities are preserved, not zeroed"
    )


def test_the_degraded_apply_skips_the_plugin_steps_it_promised_to_skip(monkeypatch):
    """A selection that wants the tracking plugin on an agent-less machine
    must produce an honest skip step, not a doomed `claude plugin install`."""
    import sys

    import probe.cli.main  # noqa: F401
    from probe.cli import doctor as doctor_impl
    from probe.cli import setup as wizard
    from probe.cli import tui
    from probe.cli.actions import Action

    cli_main = sys.modules["probe.cli.main"]
    installs = []
    monkeypatch.setattr(
        wizard, "apply_tracking", lambda want, **kw: installs.append(want) or []
    )
    monkeypatch.setattr(wizard, "needs_authorization", lambda caps, selection: [])
    monkeypatch.setattr(cli_main, "_register_local_capabilities", lambda *a, **k: [])
    monkeypatch.setattr(tui, "clear", lambda: None)
    monkeypatch.setattr(tui, "say", lambda *a, **k: None)
    bare = _caps(claude_available=False, plugins_verified=False)
    monkeypatch.setattr(doctor_impl, "collect", lambda *a, **k: bare)

    result = cli_main._run_wizard_action(
        Action.CONFIGURE,
        caps=bare,
        base_now="https://api.test",
        yes=True,
        tracking=None,
        capture=None,
        auto_update=None,
        agent_rules=None,
        uninstall=False,
        configured=False,
        selection_override=wizard.Selection(
            tracking=True, capture=False, auto_update=False, agent_rules=False
        ),
    )

    assert installs == [], "no plugin install may run without the agent CLI on PATH"
    assert result == [], "the configure path streams; an empty list is its success shape"


def test_back_on_a_one_agent_machine_lands_on_the_action_menu(monkeypatch):
    """No agent screen was shown, so Back has only the menu to return to —
    it must not re-show the confirm screen it just left."""
    import sys
    from types import SimpleNamespace

    from typer.testing import CliRunner

    from probe.cli import bootstrap
    from probe.cli import doctor as doctor_impl
    from probe.cli import plugin_cli
    from probe.cli import setup as wizard
    from probe.cli import tui
    from probe.cli.actions import Action
    import probe.cli.main  # noqa: F401

    cli_main = sys.modules["probe.cli.main"]
    monkeypatch.setattr(bootstrap, "ensure_persistent_install", lambda **_: SimpleNamespace(message=""))
    monkeypatch.setattr(plugin_cli, "available", lambda source: source == "claude_code")
    monkeypatch.setattr(doctor_impl, "collect", lambda: _caps())
    monkeypatch.setattr(wizard, "interactive", lambda: True)
    monkeypatch.setattr(tui, "clear", lambda: None)
    monkeypatch.setattr(tui, "page", lambda *a, **k: None)

    events = []
    actions = iter((Action.CONFIGURE, Action.EXIT))
    monkeypatch.setattr(
        wizard, "run_action_menu", lambda _c: events.append("action") or next(actions)
    )
    monkeypatch.setattr(
        wizard, "run_confirm_install", lambda *a, **k: events.append("confirm") or tui.BACK
    )
    monkeypatch.setattr(
        wizard, "run_backfill_offer", lambda *a, **k: pytest.fail("installation was canceled")
    )
    monkeypatch.setattr(cli_main, "_run_wizard_action", lambda *a, **k: events.append("apply") or [])

    result = CliRunner().invoke(cli_main.app, ["wizard"])

    assert result.exit_code == 0, result.output
    assert events == ["action", "confirm", "action"], (
        "Back must land on the menu, not loop the confirm screen"
    )


def test_settings_wording_stays_coupled_to_the_install_screen():
    """The Automatic updates row echoes the install's own auto-update copy --
    same feature, same words, on and off. Nothing derives the coupling, so
    this pins the shared phrase: a copy edit to one that strands the other
    fails here instead of shipping a wizard that describes updates two ways."""
    phrase = "Updates the CLI and plugins"
    assert phrase in setup.AUTO_UPDATE_COPY[1]
    assert phrase in " ".join(setup.SETTINGS_COPY[setup.Setting.AUTO_UPDATE][1])


def test_a_partially_absent_selection_is_named_on_the_confirm_screen():
    """`--agent both` with one binary present: the screen keeps the full rows
    but names the absent agent's skipped plugins, so it promises exactly what
    the apply will do."""
    rows = setup.confirm_rows(("claude_code", "codex"), unavailable=("codex",))
    text = "\n".join(rows)

    assert "Session capture" in text, "the full disclosure stays"
    assert "Codex plugins — skipped" in text, "the absent agent is named"
    assert "not on this machine" in text


def test_the_wizard_names_the_absent_half_of_a_both_selection(monkeypatch):
    """`--agent both` on a Claude-only machine hands the confirm screen the
    absent agent, so the partial promise is on screen before the keystroke."""
    import sys
    from types import SimpleNamespace

    from typer.testing import CliRunner

    from probe.cli import bootstrap
    from probe.cli import doctor as doctor_impl
    from probe.cli import plugin_cli
    from probe.cli import setup as wizard
    from probe.cli import tui
    import probe.cli.main  # noqa: F401

    cli_main = sys.modules["probe.cli.main"]
    monkeypatch.setattr(bootstrap, "ensure_persistent_install", lambda **_: SimpleNamespace(message=""))
    monkeypatch.setattr(plugin_cli, "available", lambda source: source == "claude_code")
    monkeypatch.setattr(doctor_impl, "collect", lambda: _caps())
    monkeypatch.setattr(wizard, "interactive", lambda: True)
    monkeypatch.setattr(tui, "clear", lambda: None)
    monkeypatch.setattr(tui, "page", lambda *a, **k: None)

    seen = {}

    def confirm(sources, **kwargs):
        seen["unavailable"] = kwargs.get("unavailable")
        seen["plugins_available"] = kwargs.get("plugins_available")
        return True

    monkeypatch.setattr(wizard, "run_backfill_offer", lambda _s, **kw: set())
    monkeypatch.setattr(wizard, "run_confirm_install", confirm)
    monkeypatch.setattr(cli_main, "_run_wizard_action", lambda a, **kw: ["done"])

    result = CliRunner().invoke(
        cli_main.app, ["wizard", "--action", "configure", "--agent", "both"]
    )

    assert result.exit_code == 0, result.output
    assert seen["plugins_available"] is True, "one agent present keeps the full screen"
    assert seen["unavailable"] == ("codex",), "and the absent one is handed to the screen"


def test_a_pi_only_machine_auto_selects_pi_without_the_agent_flag(monkeypatch):
    """`available_sources` now comes from `detectable_sources()`, which
    includes pi -- a machine with no claude/codex binary but a real pi one
    must auto-select pi (not fall back to the claude_code default) and reach
    an UN-degraded confirm screen with no `--agent` flag needed: pi's install
    never depended on a marketplace binary, so it must not skip the screen
    the way a truly agent-less machine does."""
    import sys
    from types import SimpleNamespace

    from typer.testing import CliRunner

    from probe.cli import bootstrap
    from probe.cli import doctor as doctor_impl
    from probe.cli import plugin_cli
    from probe.cli import setup as wizard
    from probe.cli import tui
    import probe.cli.main  # noqa: F401

    cli_main = sys.modules["probe.cli.main"]
    monkeypatch.setattr(bootstrap, "ensure_persistent_install", lambda **_: SimpleNamespace(message=""))
    monkeypatch.setattr(plugin_cli, "available", lambda _source: False)
    monkeypatch.setattr(wizard, "pi_binary_available", lambda: True)
    monkeypatch.setattr(doctor_impl, "collect", lambda: _caps(agent_source="pi"))
    monkeypatch.setattr(wizard, "interactive", lambda: True)
    monkeypatch.setattr(tui, "clear", lambda: None)
    monkeypatch.setattr(tui, "page", lambda *a, **k: None)

    seen = {}

    def confirm(sources, **kwargs):
        seen["sources"] = sources
        seen["plugins_available"] = kwargs.get("plugins_available")
        return True

    monkeypatch.setattr(wizard, "run_backfill_offer", lambda _s, **kw: set())
    monkeypatch.setattr(wizard, "run_confirm_install", confirm)
    monkeypatch.setattr(cli_main, "_run_wizard_action", lambda a, **kw: ["done"])

    result = CliRunner().invoke(cli_main.app, ["wizard", "--action", "configure"])

    assert result.exit_code == 0, result.output
    assert seen["sources"] == ("pi",), "pi must be auto-selected, not the claude_code fallback"
    assert seen["plugins_available"] is True, "pi's install never depends on a marketplace binary"


# --- the browser-confirm install ---------------------------------------------


def test_device_authorize_carries_the_install_context(monkeypatch):
    """The approval page's identity warning and completion wait both hang off
    this field; omitted when None so older backends see the request shape
    they have always seen."""
    import httpx

    captured = {}

    class FakeClient:
        def post(self, path, json=None):
            captured.update(json or {})
            raise httpx.HTTPError("stop here")

        def close(self):
            pass

    from probe.sdk import device

    with pytest.raises(device.DeviceLoginError):
        device.device_authorize(
            "https://x",
            client=FakeClient(),
            open_browser=False,
            client_context={"install": True, "prior_email": "a@b.c"},
        )
    assert captured["client_context"] == {"install": True, "prior_email": "a@b.c"}

    captured.clear()
    with pytest.raises(device.DeviceLoginError):
        device.device_authorize("https://x", client=FakeClient(), open_browser=False)
    assert "client_context" not in captured


def test_install_client_context_claims_the_resolved_account_only():
    """`prior_email` is the verified login when one resolved; an offline
    device sends no claim rather than a guessed one."""
    signed_in = {
        "claude_code": _caps(logged_in_as="richard@prbe.ai"),
        "codex": _caps(agent_source="codex"),
    }
    context = setup.install_client_context(signed_in)
    assert context == {"install": True, "prior_email": "richard@prbe.ai"}

    offline = {"claude_code": _caps()}
    assert setup.install_client_context(offline) == {"install": True}


def test_the_replaced_token_is_revoked_only_when_it_actually_changed(monkeypatch):
    """The always-browser install re-mints on a signed-in device; the token it
    replaces must not stay valid server-side with nobody holding it — and a
    re-mint that returned the SAME token (or no api grant at all) must not
    revoke the credential the device is standing on."""
    revoked = []
    monkeypatch.setattr(
        setup, "_revoke", lambda token, *, base_url, what: revoked.append(token) or []
    )

    previous = {"token": "probe_pat_old", "base_url": "https://api.test"}
    setup.revoke_replaced_token(previous, {"api": {"token": "probe_pat_new"}}, base_url="https://x")
    assert revoked == ["probe_pat_old"]

    revoked.clear()
    setup.revoke_replaced_token(previous, {"api": {"token": "probe_pat_old"}}, base_url="https://x")
    assert revoked == [], "an unchanged token is not replaced"

    # The read token is replaced by the same write and leaks the same way.
    revoked.clear()
    setup.revoke_replaced_token(
        {"token": "probe_pat_old", "mcp_token": "probe_mcp_old"},
        {"api": {"token": "probe_pat_new"}, "mcp": {"token": "probe_mcp_new"}},
        base_url="https://x",
    )
    assert revoked == ["probe_pat_old", "probe_mcp_old"], (
        "both replaced credentials are revoked, PAT first"
    )

    revoked.clear()
    setup.revoke_replaced_token(previous, {}, base_url="https://x")
    assert revoked == [], "a refused approval leaves the standing credential alone"

    setup.revoke_replaced_token({}, {"api": {"token": "t"}}, base_url="https://x")
    assert revoked == [], "a fresh device had nothing to revoke"


def test_the_guided_install_authorizes_capture_missing_from_an_older_login(monkeypatch):
    """Older logins hold API/MCP credentials but never authorized capture.
    Renew the whole selection together because the browser can switch accounts.
    """
    import sys
    from types import SimpleNamespace

    from typer.testing import CliRunner

    from probe.cli import bootstrap
    from probe.cli import doctor as doctor_impl
    from probe.cli import plugin_cli
    from probe.cli import setup as wizard
    from probe.cli import tui
    import probe.cli.main  # noqa: F401

    cli_main = sys.modules["probe.cli.main"]
    monkeypatch.setattr(bootstrap, "ensure_persistent_install", lambda **_: SimpleNamespace(message=""))
    monkeypatch.setattr(plugin_cli, "available", lambda source: source == "claude_code")
    from probe.sdk.config import save_context

    save_context({"token": "probe_pat_existing", "mcp_token": "probe_pat_read"})
    # Installed plugins alone do not prove their credentials are present.
    monkeypatch.setattr(
        doctor_impl,
        "collect",
        lambda: _caps(
            claude_available=True,
            tracking_plugin_installed=True,
            capture_plugin_installed=True,
            logged_in_as="richard@prbe.ai",
        ),
    )
    monkeypatch.setattr(wizard, "interactive", lambda: True)
    monkeypatch.setattr(tui, "clear", lambda: None)
    monkeypatch.setattr(tui, "page", lambda *a, **k: None)
    monkeypatch.setattr(wizard, "run_backfill_offer", lambda _s, **kw: set())
    monkeypatch.setattr(wizard, "run_confirm_install", lambda *a, **k: True)

    handed = {}

    def apply(_action, **kwargs):
        handed["needs"] = kwargs.get("authorization_needs")
        handed["context"] = kwargs.get("authorization_context")
        handed["capture_sources"] = kwargs.get("capture_sources")
        return ["done"]

    monkeypatch.setattr(cli_main, "_run_wizard_action", apply)

    result = CliRunner().invoke(cli_main.app, ["wizard", "--action", "configure"])

    assert result.exit_code == 0, result.output
    assert handed["needs"] == ["api", "mcp", "capture"], (
        "a missing capture credential must be authorized before installing"
    )
    assert handed["context"] == {"install": True, "prior_email": "richard@prbe.ai"}
    assert handed["capture_sources"] == ["claude_code"]


# --- the closing import offer ------------------------------------------------


def test_the_backfill_offer_translates_its_answer(monkeypatch):
    from probe.cli import tui

    monkeypatch.setattr(
        tui, "ask", lambda q, height=None, **kwargs: [setup.BackfillChoice.PAST_SESSIONS]
    )
    assert setup.run_backfill_offer(("claude_code",)) == {setup.BackfillChoice.PAST_SESSIONS}

    monkeypatch.setattr(tui, "ask", lambda q, height=None, **kwargs: [])
    assert setup.run_backfill_offer(("claude_code",)) == set()

    monkeypatch.setattr(tui, "ask", lambda q, height=None, **kwargs: tui.BACK)
    assert setup.run_backfill_offer(("claude_code",)) is tui.BACK

    monkeypatch.setattr(tui, "ask", lambda q, height=None, **kwargs: None)
    assert setup.run_backfill_offer(("claude_code",)) is None


def test_the_offer_names_what_the_history_import_does():
    """PAST_SESSIONS opens a data-grant flow: the row must say the lane shows
    what it found and asks BEFORE anything uploads — the tick opens a gate,
    it is not itself the grant."""
    title, detail = setup.BACKFILL_OFFER_COPY[setup.BackfillChoice.PAST_SESSIONS]
    blob = " ".join((title, *detail)).lower()
    assert "transcripts" in blob and "asks before anything uploads" in blob


@pytest.mark.parametrize("stop_at", ["imports", "imports_back", "confirm", "second_agent"])
def test_canceled_or_failed_install_never_starts_selected_imports(monkeypatch, stop_at):
    import importlib
    from types import SimpleNamespace

    import typer
    from typer.testing import CliRunner

    from probe.cli import bootstrap, plugin_cli, tui

    cli_main = importlib.import_module("probe.cli.main")
    monkeypatch.setattr(bootstrap, "ensure_persistent_install", lambda **_: SimpleNamespace(message=""))
    monkeypatch.setattr(plugin_cli, "available", lambda source: True)
    monkeypatch.setattr(doctor, "collect", lambda: _caps())
    monkeypatch.setattr(setup, "interactive", lambda: True)
    monkeypatch.setattr(tui, "clear", lambda: None)
    offered = []

    def offer(*args, **kwargs):
        offered.append(True)
        return tui.BACK if stop_at == "imports_back" else None

    monkeypatch.setattr(setup, "run_backfill_offer", offer)
    monkeypatch.setattr(setup, "run_confirm_install", lambda *a, **kw:
                        None if stop_at == "confirm" else True)
    monkeypatch.setattr(cli_main, "_import_past_sessions", lambda **kw:
                        pytest.fail("an unfinished install must not import"))
    applied = []

    def apply(action, **kwargs):
        from probe.cli.actions import Action

        assert action is Action.CONFIGURE, "an unfinished install must not import folders"
        applied.append(action)
        if stop_at == "second_agent" and len(applied) == 2:
            raise typer.Exit(1)
        return []

    monkeypatch.setattr(cli_main, "_run_wizard_action", apply)
    result = CliRunner().invoke(cli_main.app, ["install", "--agent", "both"])
    assert result.exit_code == (1 if stop_at == "second_agent" else 0), result.output
    assert len(applied) == (0 if stop_at == "confirm" else 2)
    assert bool(offered) == (stop_at in {"imports", "imports_back"})


@pytest.mark.parametrize("choices", [set(), {setup.BackfillChoice.PAST_SESSIONS},
                                    {setup.BackfillChoice.PROJECT_FOLDER}, set(setup.BackfillChoice)])
@pytest.mark.parametrize("agent", ["claude", "codex", "pi", "both"])
@pytest.mark.parametrize("entry", [["install"], ["install", "ABCD234567"],
                                  ["wizard", "--action", "configure"]])
def test_guided_install_runs_only_selected_imports_after_setup(monkeypatch, choices, agent, entry):
    """The npx entry points reuse both import lanes once, after every apply."""
    import sys
    from types import SimpleNamespace

    from typer.testing import CliRunner

    from probe.cli import backfill as backfill_impl
    from probe.cli import backfill_transcripts as transcripts_mod
    from probe.cli import bootstrap
    from probe.cli import import_jobs_ui, onboarding_complete
    from probe.cli import doctor as doctor_impl
    from probe.cli import plugin_cli
    from probe.cli import setup as wizard
    from probe.cli import tui
    from probe.cli.actions import Action
    import probe.cli.main  # noqa: F401

    cli_main = sys.modules["probe.cli.main"]
    monkeypatch.setattr(bootstrap, "ensure_persistent_install", lambda **_: SimpleNamespace(message=""))
    monkeypatch.setattr(plugin_cli, "available", lambda source: source == "claude_code")
    monkeypatch.setattr(doctor_impl, "collect", lambda: _caps(claude_available=True))
    monkeypatch.setattr(wizard, "interactive", lambda: True)
    monkeypatch.setattr(tui, "clear", lambda: None)
    monkeypatch.setattr(tui, "page", lambda *a, **k: None)
    events = []
    monkeypatch.setattr(
        import_jobs_ui, "show_imports",
        lambda **kwargs: pytest.fail("Onboarding finishes with a dashboard handoff"),
    )
    monkeypatch.setattr(onboarding_complete, "show", lambda base: events.append("dashboard") or True)
    monkeypatch.setattr(
        wizard, "run_confirm_install", lambda *a, **k: events.append("confirm") or True
    )
    run_action = cli_main._run_wizard_action

    def apply(action, **kwargs):
        if action is Action.CONFIGURE:
            events.append("setup")
            kwargs["installation_completion"].remaining -= 1
            return ["done"]
        return run_action(action, **kwargs)

    monkeypatch.setattr(cli_main, "_run_wizard_action", apply)
    monkeypatch.setattr(cli_main, "_backfill_client", lambda: SimpleNamespace())

    offered = []
    lane_runs = []
    folder_runs = []

    def offer(sources, **kwargs):
        events.append("imports")
        offered.append(tuple(sources))
        return choices

    monkeypatch.setattr(wizard, "run_backfill_offer", offer)
    monkeypatch.setattr(
        transcripts_mod,
        "run_lane",
        lambda **kwargs: events.append("sessions") or lane_runs.append(kwargs) or ["imported"],
    )
    monkeypatch.setattr(
        backfill_impl, "run",
        lambda **kwargs: events.append("folder") or folder_runs.append(kwargs) or ["imported folder"],
    )

    result = CliRunner().invoke(cli_main.app, [*entry, "--agent", agent])

    assert result.exit_code == 0, result.output
    sources = {"claude": ("claude_code",), "codex": ("codex",), "pi": ("pi",),
               "both": ("claude_code", "codex")}[agent]
    assert offered == [sources]
    expected = ["confirm", *["setup"] * len(sources), "imports"]
    if setup.BackfillChoice.PAST_SESSIONS in choices:
        expected.append("sessions")
        assert len(lane_runs) == 1 and lane_runs[0]["interactive"] is True
    else:
        assert not lane_runs
    if setup.BackfillChoice.PROJECT_FOLDER in choices:
        expected.append("folder")
        assert len(folder_runs) == 1 and folder_runs[0]["transcripts"] is False
    else:
        assert not folder_runs
    expected.append("dashboard")
    assert events == expected

    # Headless: no screen, no offer, no lane.
    offered.clear()
    lane_runs.clear()
    folder_runs.clear()
    monkeypatch.setattr(wizard, "interactive", lambda: False)
    result = CliRunner().invoke(cli_main.app, ["wizard", "--action", "configure", "--yes"])
    assert result.exit_code == 0, result.output
    assert offered == [] and lane_runs == [] and folder_runs == []


# --- pi_binary_available's impostor guard -----------------------------------
#
# "pi" is two letters; `which` alone would let any unrelated binary of that
# name put a phantom pi checkbox in the picker. The sniff runs `pi --help`
# and requires "coding" in the output (loose on purpose: forks reword the
# line but keep the word). False negatives only hide the auto-detected row —
# `--agent pi` still works — so every failure mode below collapses to False.


# Captured at import time, BEFORE the autouse `_no_ambient_pi_binary`
# fixture replaces the module attribute for each test -- these tests are
# about the real sniff, so they must call the real function.
#
# `setup.pi_binary_available` is a re-export: the sniff itself lives in
# `pi_config`, where `backfill.which_agent` can also reach it. The name is
# still read off `setup` because that is the binding every caller uses, and
# the stubs below go to `pi_config`, where its `shutil`/`subprocess` are
# resolved.
_REAL_PI_BINARY_AVAILABLE = setup.pi_binary_available


class _FakeCompleted:
    def __init__(self, returncode: int, stdout: str) -> None:
        self.returncode = returncode
        self.stdout = stdout


@pytest.fixture
def fresh_sniff():
    """The sniff is `lru_cache`d (once per process -- see its docstring), so a
    test that stubs `which`/`run` and does not clear it reads whichever answer
    the FIRST test in the session happened to produce."""
    _REAL_PI_BINARY_AVAILABLE.cache_clear()
    yield
    _REAL_PI_BINARY_AVAILABLE.cache_clear()


def test_pi_detection_requires_the_help_sniff_not_just_which(monkeypatch, fresh_sniff):
    monkeypatch.setattr(pi_config.shutil, "which", lambda name: "/fake/bin/pi")
    monkeypatch.setattr(
        pi_config.subprocess,
        "run",
        lambda *a, **k: _FakeCompleted(0, "pi - AI coding assistant with read, bash, edit, write tools"),
    )
    assert _REAL_PI_BINARY_AVAILABLE() is True


def test_an_impostor_pi_binary_is_not_detected(monkeypatch, fresh_sniff):
    monkeypatch.setattr(pi_config.shutil, "which", lambda name: "/usr/local/bin/pi")
    monkeypatch.setattr(
        pi_config.subprocess,
        "run",
        lambda *a, **k: _FakeCompleted(0, "pi 3.14159 — arbitrary precision calculator"),
    )
    assert _REAL_PI_BINARY_AVAILABLE() is False


def test_no_pi_on_path_is_not_detected(monkeypatch, fresh_sniff):
    monkeypatch.setattr(pi_config.shutil, "which", lambda name: None)
    assert _REAL_PI_BINARY_AVAILABLE() is False


def test_a_hanging_or_broken_pi_binary_is_not_detected(monkeypatch, fresh_sniff):
    monkeypatch.setattr(pi_config.shutil, "which", lambda name: "/fake/bin/pi")

    def _boom(*a, **k):
        raise pi_config.subprocess.TimeoutExpired(cmd="pi --help", timeout=3)

    monkeypatch.setattr(pi_config.subprocess, "run", _boom)
    assert _REAL_PI_BINARY_AVAILABLE() is False


def test_a_nonzero_exit_from_pi_help_is_not_detected(monkeypatch, fresh_sniff):
    monkeypatch.setattr(pi_config.shutil, "which", lambda name: "/fake/bin/pi")
    monkeypatch.setattr(
        pi_config.subprocess, "run", lambda *a, **k: _FakeCompleted(1, "some coding error text")
    )
    assert _REAL_PI_BINARY_AVAILABLE() is False


# --- headless selection: what a run with nobody watching configures ---------
#
# Three properties, and the reason they are asserted together is that the bug
# they cover was ONE decision showing up in three places: a headless run had no
# picker, no confirm screen, and a hard-coded agent selection -- so it silently
# did something complete and told nobody which agents it did it to.


def _headless(monkeypatch, argv, *, detected=()):
    """Drive the wizard with no TTY and a pinned set of detected agents."""
    import sys
    from types import SimpleNamespace

    from typer.testing import CliRunner

    from probe.cli import bootstrap
    from probe.cli import doctor as doctor_impl
    from probe.cli import plugin_cli
    from probe.cli import setup as wizard
    import probe.cli.main  # noqa: F401

    cli_main = sys.modules["probe.cli.main"]
    monkeypatch.setattr(bootstrap, "ensure_persistent_install", lambda **_: SimpleNamespace(message=""))
    monkeypatch.setattr(doctor_impl, "collect", lambda: _caps())
    monkeypatch.setattr(wizard, "interactive", lambda: False)
    monkeypatch.setattr(plugin_cli, "available", lambda source: source in detected)

    calls: list[str] = []
    monkeypatch.setattr(
        cli_main,
        "_run_wizard_action",
        lambda action, **kwargs: calls.append(os.environ["PROBE_AGENT"]) or [],
    )
    return CliRunner().invoke(cli_main.app, argv), calls


def test_a_headless_install_configures_every_agent_it_finds(monkeypatch):
    """It used to configure Claude Code and only Claude Code, whatever was on
    the machine — so a Codex user's agent ran the installer from a tool call,
    got a green report, and had configured an agent they do not use. Detection
    is the same question a human's picker answers; a missing TTY does not
    change the answer."""
    result, calls = _headless(
        monkeypatch,
        ["wizard", "--action", "configure", "--yes"],
        detected=("claude_code", "codex"),
    )

    assert result.exit_code == 0, result.output
    assert calls == ["claude_code", "codex"]


def test_a_headless_install_says_which_agents_it_picked(monkeypatch):
    """Nothing else on this run will. The picker and the confirm screen are
    both gated on a TTY, so an implicit selection across a multi-agent machine
    would otherwise be reported nowhere — and "which agents did that
    configure?" is unanswerable afterwards from a log of green ticks."""
    result, _ = _headless(
        monkeypatch,
        ["wizard", "--action", "configure", "--yes"],
        detected=("claude_code", "codex"),
    )

    assert "Claude Code and Codex" in result.output
    assert "--agent" in result.output, "the line has to say how to choose"


def test_a_headless_install_is_silent_when_there_was_no_choice(monkeypatch):
    """One agent found is not a decision, and announcing it is noise on the
    common path."""
    result, _ = _headless(
        monkeypatch,
        ["wizard", "--action", "configure", "--yes"],
        detected=("claude_code",),
    )

    assert "every coding agent found" not in result.output


def test_an_explicit_agent_flag_is_not_second_guessed(monkeypatch):
    """`--agent claude` on a two-agent machine means claude. The announcement
    is for an IMPLICIT selection; naming one and then being told what was
    chosen reads as the flag having been overridden."""
    result, calls = _headless(
        monkeypatch,
        ["wizard", "--agent", "claude", "--action", "configure", "--yes"],
        detected=("claude_code", "codex"),
    )

    assert result.exit_code == 0, result.output
    assert calls == ["claude_code"]
    assert "every coding agent found" not in result.output


def test_bare_headless_wizard_refuses_instead_of_installing(monkeypatch):
    """`npx probe-research` with no verb, from an agent's shell tool.

    `chosen_action` defaults to CONFIGURE and BOTH screens that would turn that
    default into a decision — the action menu and `run_confirm_install`, which
    carries the capture disclosure — are gated on a TTY. So this ran a complete
    install, capture included, with no menu, no disclosure and no keystroke,
    and then reported success. Refusing is the only honest answer: capture
    ships prompts, file contents and tool output off the machine.
    """
    result, calls = _headless(monkeypatch, ["wizard"], detected=("claude_code", "codex"))

    assert result.exit_code == 2, result.output
    assert calls == [], "it must not configure anything"
    assert "Nothing has been changed" in result.output
    assert "probe wizard --action configure" in result.output, "refusal has to name the way forward"


def test_the_refusal_does_not_catch_a_caller_that_said_what_it_wanted(monkeypatch):
    """Narrow on purpose. `--yes`, a capability flag, `--agent` and `--action`
    are each a stated intent, and auto-update's own detached re-run
    (`--action update --yes`) must never hit this."""
    for argv in (
        ["wizard", "--yes"],
        ["wizard", "--no-capture"],
        ["wizard", "--agent", "claude"],
        ["wizard", "--action", "configure"],
    ):
        result, _ = _headless(monkeypatch, argv, detected=("claude_code",))
        assert result.exit_code == 0, f"{argv} was refused: {result.output}"


# --- telling the server the device is gone ---------------------------------


def test_off_revokes_server_side_before_it_deletes_the_local_token(isolate, monkeypatch):
    """THE ORDERING IS THE WHOLE FIX.

    `_clear_paired_token` deletes the same `<plugin>/.token` the revoke
    authenticates with. Run it first and the device can never be revoked
    server-side -- not here, and not by a later `python -m tap revoke`, which
    reads that file and skips its server call when it finds nothing. The row
    then sits at `revoked_at IS NULL` forever: the machine lingers in the
    dashboard's device list and its capture credential stays valid.

    Asserted as "the token still existed when we called", not merely "we
    called" -- a revoke that fires after the wipe is indistinguishable from
    this one at the call site and is exactly the bug.
    """
    token_file = isolate / "tap" / ".token"
    token_file.write_text("ros_ing_paired")
    token_present_at_call: list[bool] = []

    def _spy(*_args, **_kwargs):
        token_present_at_call.append(token_file.exists())
        return True

    monkeypatch.setattr(capture, "revoke_capture_device", _spy)

    result = capture.turn_off(capture.OffMode.UNINSTALL)

    assert token_present_at_call == [True], "revoke must run BEFORE the token is wiped"
    assert result.server_revoked is True
    assert not token_file.exists()


def test_off_still_succeeds_when_the_server_cannot_be_reached(isolate, monkeypatch):
    """Off is a promise about THIS machine. An unreachable server must never be
    the reason someone cannot turn capture off -- but they should be told the
    device may linger, since only they can clear it from the dashboard."""
    (isolate / "tap" / ".token").write_text("ros_ing_paired")
    monkeypatch.setattr(capture, "revoke_capture_device", lambda *a, **k: None)

    result = capture.turn_off(capture.OffMode.DISABLE)

    assert result.verified is True
    assert result.server_revoked is None
    assert any("linger" in warning for warning in result.warnings)


def test_off_does_not_warn_when_there_was_no_paired_device(isolate, monkeypatch):
    """No paired credential means nothing server-side to revoke. Warning about a
    device that never existed is noise in the one place people read carefully."""
    monkeypatch.setattr(capture, "revoke_capture_device", lambda *a, **k: None)

    result = capture.turn_off(capture.OffMode.DISABLE)

    assert not any("linger" in warning for warning in result.warnings)


def test_revoke_sends_the_uninstall_reason_to_the_right_endpoint(isolate, monkeypatch):
    """The same endpoint serves the re-pair path, which means the opposite
    thing. Without `reason` the churn channel reports a departure every time
    somebody repairs a laptop."""
    import json as _json

    (isolate / "tap" / ".token").write_text("ros_ing_paired")
    (isolate / "tap" / ".config").write_text(_json.dumps({"api_base_url": "https://example.test"}))
    seen: dict = {}

    class _Response:
        status = 200

        def __enter__(self):
            return self

        def __exit__(self, *_exc):
            return False

    def _fake_urlopen(request, timeout=None, context=None):
        seen["url"] = request.full_url
        seen["method"] = request.get_method()
        seen["body"] = _json.loads(request.data.decode("utf-8"))
        seen["auth"] = request.get_header("Authorization")
        return _Response()

    _opener_opens(monkeypatch, _fake_urlopen)

    assert capabilities_mod.revoke_capture_device() is True
    assert seen["url"] == "https://example.test/agent-tap/revoke"
    assert seen["method"] == "POST"
    assert seen["body"] == {"reason": "uninstall"}
    assert seen["auth"] == "Bearer ros_ing_paired"


def test_revoke_is_unknown_not_false_when_offline(isolate, monkeypatch):
    """False means the server answered and had nothing live to revoke. Offline
    is not that, and collapsing the two would warn on the wrong half."""
    import json as _json
    import urllib.error
    import urllib.request

    (isolate / "tap" / ".token").write_text("ros_ing_paired")
    (isolate / "tap" / ".config").write_text(_json.dumps({"api_base_url": "https://example.test"}))

    def _boom(*_a, **_k):
        raise urllib.error.URLError("no route to host")

    _opener_opens(monkeypatch, _boom)
    assert capabilities_mod.revoke_capture_device() is None

    def _already_revoked(*_a, **_k):
        raise urllib.error.HTTPError("u", 401, "unauthorized", {}, None)

    _opener_opens(monkeypatch, _already_revoked)
    assert capabilities_mod.revoke_capture_device() is False


def test_revoke_is_a_noop_without_a_resolvable_credential(isolate):
    """No token or no base URL means there is nothing to ask, and asking anyway
    would be a request with a blank bearer."""
    (isolate / "tap" / ".token").write_text("ros_ing_paired")
    # No base_url anywhere -> unresolvable.
    assert capabilities_mod.revoke_capture_device() is None


# --- the persistence predicate, driven rather than stubbed -------------------
#
# Every other bootstrap test monkeypatches `_resolves_on_path`, so it asserts
# what happens GIVEN an answer and never checks that the answer is right. The
# answer was wrong on exactly the path that matters -- a from-zero install --
# and that is why a green `npx probe-research install` could leave no `probe`
# on the machine at all.


def test_a_launchers_temporary_copy_is_not_an_install(monkeypatch, tmp_path):
    """`uv tool run` unpacks the CLI into its cache and puts that cache's bin on
    PATH, so `which("probe")` finds THIS process on a machine with nothing
    installed. Measured shape, from a fresh container:
    `~/.cache/uv/archive-v0/<hash>/bin/probe`."""
    from probe.cli import bootstrap

    home = tmp_path / "home"
    ephemeral = home / ".cache/uv/archive-v0/q6J9HkkgYO5GIi61/bin/probe"
    ephemeral.parent.mkdir(parents=True)
    ephemeral.write_text("#!/bin/sh\n")
    ephemeral.chmod(0o755)

    monkeypatch.setenv("HOME", str(home))
    monkeypatch.delenv("UV_CACHE_DIR", raising=False)
    monkeypatch.delenv("XDG_CACHE_HOME", raising=False)
    monkeypatch.setattr(bootstrap.shutil, "which", lambda name: str(ephemeral))

    assert bootstrap._is_throwaway(str(ephemeral)) is True
    assert bootstrap._installed_binary() is None, "a throwaway copy is not an install"
    assert bootstrap._resolves_on_path() is False, "a from-zero run must install"


def test_a_real_install_is_still_recognised(monkeypatch, tmp_path):
    """The counterweight, and the one a careless fix breaks. `~/.local/bin/probe`
    is a SYMLINK into `~/.local/share/uv/tools/probe-research`, which is also
    that process's own `sys.prefix` -- so judging by `realpath` or by prefix
    would call a healthy install throwaway and reinstall it on every run."""
    from probe.cli import bootstrap

    home = tmp_path / "home"
    tool = home / ".local/share/uv/tools/probe-research/bin/probe"
    tool.parent.mkdir(parents=True)
    tool.write_text("#!/bin/sh\n")
    tool.chmod(0o755)
    link = home / ".local/bin/probe"
    link.parent.mkdir(parents=True)
    link.symlink_to(tool)

    monkeypatch.setenv("HOME", str(home))
    monkeypatch.delenv("UV_CACHE_DIR", raising=False)
    monkeypatch.delenv("XDG_CACHE_HOME", raising=False)
    monkeypatch.setattr(bootstrap.shutil, "which", lambda name: str(link))

    assert bootstrap._is_throwaway(str(link)) is False
    assert bootstrap._installed_binary() == str(link)


def test_a_relocated_uv_cache_is_still_a_cache(monkeypatch, tmp_path):
    """uv lets the cache move. A hardcoded `~/.cache/uv` would quietly stop
    matching for anyone who moved it — the same silent wrong answer again."""
    from probe.cli import bootstrap

    cache = tmp_path / "somewhere-else"
    binary = cache / "archive-v0/abc/bin/probe"
    binary.parent.mkdir(parents=True)
    binary.write_text("#!/bin/sh\n")

    monkeypatch.setenv("HOME", str(tmp_path / "home"))
    monkeypatch.setenv("UV_CACHE_DIR", str(cache))
    assert bootstrap._is_throwaway(str(binary)) is True


# ---------------------------------------------------------------------------
# The wizard asks the server before it offers the daemon (Richard 2026-09-28:
# "build the gate in the install wizard"): the "Who records" rows are offered
# only where the server would serve it (every plan since 2026-10-02). The
# tracking row has no `daemon` since 2026-09-29.
# ---------------------------------------------------------------------------


def test_the_defaults_picker_offers_on_read_off_and_asks_no_server(isolate, monkeypatch):
    """The daemon left this row (Richard 2026-09-29): the picker lists the three
    switch states, whatever the server would say about the daemon."""
    from probe.cli import tui
    from probe.sdk import session_marker

    _captured, values = _defaults_picker_rows(monkeypatch, session_marker.STATE_FULL)
    assert values == list(session_marker.SWITCH_STATES)

    cli_main = _settings_main()
    asked = []
    monkeypatch.delenv("PROBE_SESSION_TRACKING", raising=False)
    monkeypatch.delenv("PROBE_SESSION_STATE", raising=False)
    monkeypatch.setattr(setup, "interactive", lambda: True)
    monkeypatch.setattr(setup, "run_defaults_menu", lambda current: tui.BACK)
    monkeypatch.setattr(setup, "daemon_availability", lambda base_url=None: asked.append(1) or (False, None))
    assert cli_main._run_defaults_action(yes=False, base_now="https://api.test") is None
    assert asked == []


def test_the_settings_screen_asks_the_server_nothing(isolate, monkeypatch):
    """Who records left this screen for the main menu (Richard 2026-09-29), so
    the server's answer is asked on the switch, never before this screen."""
    from probe.cli import tui

    cli_main = _settings_main()
    asked = []
    monkeypatch.setattr(setup, "interactive", lambda: True)
    monkeypatch.setattr(setup, "run_settings_menu", lambda current, *, hidden=frozenset(): tui.BACK)
    monkeypatch.setattr(tui, "clear", lambda: None)
    monkeypatch.setattr(
        setup, "daemon_availability", lambda base_url=None: asked.append(base_url) or (True, None)
    )
    cli_main._run_settings_action(
        yes=False,
        caps_by_source={"claude_code": _caps()},
        base_now="https://api.test",
    )
    assert asked == []


@pytest.mark.parametrize(
    ("status", "body", "answer"),
    [
        (200, {"available": True, "code": None, "message": None}, (True, None)),
        (
            200,
            {"available": False, "code": "companion_disabled", "message": "x"},
            (False, "Daemon recording is not enabled for this team."),
        ),
        (404, {"detail": "Not Found"}, (None, None)),
        (500, {"detail": "boom"}, (None, None)),
        (200, {"unexpected": 1}, (None, None)),
        (
            200,
            {"available": False, "code": "some_new_reason", "message": "x"},
            (False, "Daemon recording is not available for this team."),
        ),
    ],
    ids=["yes", "disabled", "older-server", "server-error", "garbled", "new-reason"],
)
def test_daemon_availability_reads_the_server_and_never_guesses_no(isolate, monkeypatch, status, body, answer):
    import httpx

    from probe.sdk import transport as transport_mod

    seen = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(
            (
                request.method,
                request.url.path,
                request.headers.get("authorization"),
                request.headers.get("x-probe-surface"),
                request.url.host,
            )
        )
        return httpx.Response(status, json=body)

    real_client = httpx.Client

    def client(*args, **kwargs):
        kwargs["transport"] = httpx.MockTransport(handler)
        return real_client(*args, **kwargs)

    monkeypatch.setenv("PROBE_TOKEN", "probe_pat_test")
    monkeypatch.setenv("PROBE_BASE_URL", "https://api.test")
    monkeypatch.setattr(transport_mod.httpx, "Client", client)
    assert setup.daemon_availability(base_url="https://staging.test") == answer
    assert seen and seen[0][:2] == ("GET", "/v1/companion/availability")
    assert seen[0][2] == "Bearer probe_pat_test"
    assert seen[0][3] == "cli", "the wizard asks as the CLI, not the SDK"
    assert seen[0][4] == "staging.test", "the API the wizard is pointed at"


def test_daemon_availability_gives_up_on_a_stalled_network(isolate, monkeypatch):
    """A lookup that never answers is "cannot tell" within the budget, not a
    Settings screen held for as long as the network stalls."""
    import threading
    import time

    from probe.sdk import transport as transport_mod

    release = threading.Event()

    class Stalled:
        def __init__(self, *args, **kwargs):
            pass

        def request(self, *args, **kwargs):
            release.wait(30)
            raise RuntimeError("stalled")

        def close(self):
            pass

    monkeypatch.setenv("PROBE_TOKEN", "probe_pat_test")
    monkeypatch.setattr(transport_mod, "Transport", Stalled)
    monkeypatch.setattr(setup, "DAEMON_AVAILABILITY_BUDGET_S", 0.2)
    started = time.monotonic()
    try:
        assert setup.daemon_availability() == (None, None)
        assert time.monotonic() - started < 2
    finally:
        release.set()


def test_daemon_availability_signed_out_asks_nothing(isolate, monkeypatch):
    from probe.sdk import transport as transport_mod

    def no_request(*args, **kwargs):
        raise AssertionError("a signed-out wizard must not ask the server anything")

    for name in ("PROBE_TOKEN", "PROBE_API_KEY"):
        monkeypatch.delenv(name, raising=False)
    monkeypatch.setattr(transport_mod, "Transport", no_request)
    assert setup.daemon_availability() == (None, None)


# -- setup only in the wizard: the account screen and Uninstall (R3/R4) -------


def test_uninstall_takes_the_status_line_back_to_what_it_wrapped(isolate, monkeypatch, tmp_path):
    from probe.cli import statusline

    settings = tmp_path / "claude-settings.json"
    ours = statusline.chain("mine", statusline.renderer_command("python3"))
    assert statusline.MARKER in ours
    settings.write_text(json.dumps({"statusLine": {"type": "command", "command": ours}}))
    monkeypatch.setattr(statusline, "settings_path", lambda: settings)

    assert setup.remove_statusline() == ["Status line: back to the command you had before."]
    assert json.loads(settings.read_text())["statusLine"] == {"type": "command", "command": "mine"}
    assert setup.remove_statusline() == [], "nothing of ours left: silent"


def test_the_account_screen_removes_another_saved_account_never_the_active_one(isolate):
    from probe.sdk.config import current_context_name, load_file, save_context, use_context

    save_context({"base_url": "https://a", "token": "probe_pat_a"}, name="work")
    save_context({"base_url": "https://b", "token": "probe_pat_b"}, name="side")
    use_context("work")

    assert setup.remove_account("work") == ["No other account is saved as “work”; nothing was removed."]
    assert setup.remove_account("side") == ["Removed the account saved as “side”."]
    assert set(load_file()["contexts"]) == {"work"} and current_context_name() == "work"
