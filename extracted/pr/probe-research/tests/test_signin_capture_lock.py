"""A sign-in's pending capture lock, and the Settings commit that tore it down.

Anthrogen, 2026-10-26: a machine with an older Probe install signed in from
the wizard's first screen. That sign-in minted capture credentials and parked
them behind `.disabled` = `capture.AWAITING_CONFIRMATION` until Install
confirmed. The person picked Update, which never lifted the lock, and the menu
called it "killswitch set". A minute later Settings committed automatic
updates, re-applied capture=False read off that lock, and the full turn-off
revoked the Claude Code credential minted 90 seconds earlier.
"""

from __future__ import annotations

import importlib
import os

import pytest
import typer
from typer.testing import CliRunner

from probe.cli import capabilities as capabilities_mod
from probe.cli import capture, doctor, setup, tui
from probe.cli.actions import Action
from probe.cli.capabilities import Capabilities, Capability, TokenSource, tap_plugin_dir
from probe.sdk.config import load_context, save_context
from tests.test_wizard_auth_entry import entry  # noqa: F401 -- a fixture: the wizard's menu, scripted

main = importlib.import_module("probe.cli.main")


@pytest.fixture
def home(tmp_path, monkeypatch):
    """Every state path in a tmpdir, and a record of every capture revoke."""
    monkeypatch.setenv("PROBE_RESEARCH_TAP_PLUGIN_DIR", str(tmp_path / "tap"))
    monkeypatch.setenv("PRBE_CODEX_TAP_PLUGIN_DIR", str(tmp_path / "codex-tap"))
    monkeypatch.setenv("PROBE_CONFIG_PATH", str(tmp_path / "probe" / "config.json"))
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    monkeypatch.setenv("PI_CODING_AGENT_DIR", str(tmp_path / "pi-agent"))
    for name in ("PROBE_AGENT", "PROBE_TOKEN", "PROBE_MCP_TOKEN", "PROBE_INGEST_TOKEN"):
        monkeypatch.delenv(name, raising=False)
    revoked: list[object] = []
    monkeypatch.setattr(capture, "revoke_capture_device", lambda *a, **k: revoked.append(a) or True)
    monkeypatch.setattr(capabilities_mod, "verify_mcp_credential", lambda **_: True)
    monkeypatch.setattr(main, "_register_local_capabilities", lambda caps, **_: [])
    monkeypatch.setattr(tui, "clear", lambda: None)
    monkeypatch.setenv(main.CAPTURE_QUESTION_ASKED_ENV, "")  # restored on teardown, unlike delenv of an unset name
    save_context({"token": "probe_pat_signed_in", "ingest_token": "ros_ing_claude_code"})
    return revoked


def _lock(source: str, text: str = capture.AWAITING_CONFIRMATION) -> None:
    directory = tap_plugin_dir(source)
    directory.mkdir(parents=True, exist_ok=True)
    (directory / ".disabled").write_text(text)


def _pending(source: str = "claude_code", **overrides) -> Capabilities:
    """An agent whose plugins were already installed when this sign-in parked
    its new capture credential behind the lock."""
    return Capabilities(
        **{
            "agent_source": source,
            "claude_available": True,
            "codex_available": True,
            "logged_in_as": "researcher@example.test",
            "api_credential_valid": True,
            "tracking_plugin_installed": True,
            "capture_plugin_installed": True,
            "capture_token_sources": (TokenSource.PROBE_CONFIG,),
            "capture_credential_valid": True,
            "capture_killswitched": True,
            "capture_awaiting_confirmation": True,
            "agent_rules_installed": True,
            "mcp_authenticated": True,
            **overrides,
        }
    )


# --- bug 2: Settings re-applied a read --------------------------------------


def test_a_settings_commit_leaves_capture_it_did_not_touch(home, monkeypatch):
    """Toggling automatic updates ran the configure with capture=False read
    off the lock; the work list turned capture off for any agent with the
    plugin installed, and `turn_off` revoked the parked credential."""
    _lock("claude_code")
    snapshot = _pending()
    monkeypatch.setattr(doctor, "collect", lambda: snapshot)
    updates: list[bool] = []
    monkeypatch.setattr(setup, "apply_auto_update", lambda want: updates.append(want) or [])

    main._apply_capability_settings(
        {setup.Setting.AUTO_UPDATE: True},
        caps_by_source={"claude_code": snapshot},
        base_now="https://api.test",
    )

    assert updates == [True], "the row that changed was applied"
    assert home == [], "no capture credential may be revoked by an automatic-updates toggle"
    assert load_context().get("ingest_token") == "ros_ing_claude_code"
    assert capture.awaiting_confirmation("claude_code"), "the lock is still the sign-in's, not a deliberate off"


def test_settings_hands_every_untouched_capability_over_as_preserved(home, monkeypatch):
    snapshot = _pending()
    handed = []
    monkeypatch.setattr(doctor, "collect", lambda: snapshot)
    monkeypatch.setattr(main, "_run_wizard_action", lambda a, **kw: handed.append(kw["selection_override"]) or [])

    main._apply_capability_settings(
        {setup.Setting.AUTO_UPDATE: True},
        caps_by_source={"claude_code": snapshot},
        base_now="https://api.test",
    )

    (target,) = handed
    assert target.auto_update is True and Capability.AUTO_UPDATE not in target.preserve
    assert target.keeps(Capability.CAPTURE) and target.keeps(Capability.TRACKING)
    assert setup.plan(snapshot, target) == ["enable automatic updates"]


def test_preserve_is_never_inferred_an_unticked_capture_still_turns_off():
    """`preserve` is the caller's word, never inferred: an Install that unticks
    capture still plans the turn-off."""
    snapshot = _pending(capture_killswitched=False, capture_awaiting_confirmation=False)
    assert snapshot.capture_on
    selection = setup.Selection(tracking=True, capture=False, auto_update=False, agent_rules=True)
    assert "disable Session capture" in setup.plan(snapshot, selection)


# --- bug 1: the lock nobody lifted -------------------------------------------


@pytest.mark.parametrize(
    ("text", "awaiting", "word"),
    [
        (capture.AWAITING_CONFIRMATION, True, "off (finish Install)"),
        ("disabled by the Probe Research wizard\n", False, "off (killswitch set)"),
    ],
)
def test_the_menu_names_what_lifts_a_sign_ins_lock(home, text, awaiting, word):
    _lock("claude_code", text)
    assert capture.awaiting_confirmation("claude_code") is awaiting
    snapshot = Capabilities(capture_killswitched=True, capture_awaiting_confirmation=awaiting)
    assert setup._capture_word(snapshot) == word


def test_updates_question_turns_on_only_capture_a_sign_in_left_waiting(home, monkeypatch):
    """Through the real configure: Claude Code holds its parked credential and
    gets capture back; Codex holds none of its own, which only Install's
    browser approval can mint, so it is neither asked about nor touched."""
    _lock("claude_code")
    _lock("codex")
    claude = _pending()
    codex = _pending("codex", capture_token_sources=())
    monkeypatch.setattr(doctor, "collect", lambda: claude)
    asked: list[tuple[str, ...]] = []
    monkeypatch.setattr(setup, "confirm_pending_capture", lambda sources: asked.append(tuple(sources)) or True)

    lines = main._confirm_pending_capture(
        {"claude_code": claude, "codex": codex}, base_now="https://api.test"
    )

    assert asked == [("claude_code",)]
    assert not (tap_plugin_dir("claude_code") / ".disabled").exists()
    assert capture.awaiting_confirmation("codex"), "an agent nobody was asked about keeps its lock"
    assert lines[-1] == "Session capture is on for Claude Code."
    assert home == []


def test_not_now_changes_nothing(home, monkeypatch):
    _lock("claude_code")
    monkeypatch.setattr(setup, "confirm_pending_capture", lambda sources: False)
    monkeypatch.setattr(main, "_run_wizard_action", lambda *a, **kw: pytest.fail("applied after Not now"))

    assert main._confirm_pending_capture({"claude_code": _pending()}, base_now="https://api.test") == []
    assert capture.awaiting_confirmation("claude_code")


def test_a_deliberate_off_is_never_asked_about(home, monkeypatch):
    _lock("claude_code", "disabled by the Probe Research wizard\n")
    monkeypatch.setattr(setup, "confirm_pending_capture", lambda sources: pytest.fail("asked"))

    snapshot = _pending(capture_awaiting_confirmation=False)
    assert main._confirm_pending_capture({"claude_code": snapshot}, base_now="https://api.test") == []


def test_the_menus_update_asks_before_it_hands_off(entry, monkeypatch):  # noqa: F811
    """Before the hand-off, which may exec the newest release and never come
    back to ask."""
    monkeypatch.setenv(main.CAPTURE_QUESTION_ASKED_ENV, "")  # restored on teardown, unlike delenv of an unset name
    save_context({"token": "probe_pat_existing", "base_url": "https://api.test"})
    picks = iter([Action.UPDATE, Action.EXIT])
    monkeypatch.setattr(setup, "run_action_menu", lambda _caps: next(picks))
    order: list[tuple] = []
    monkeypatch.setattr(
        main,
        "_confirm_pending_capture",
        lambda caps_by_source, **_: order.append(("ask", tuple(caps_by_source))) or [],
    )
    # One agent: its Update (and the hand-off inside it) is one
    # `_run_wizard_action`; several hand off first, then update each.
    monkeypatch.setattr(main, "_hand_off_update", lambda *a, **k: order.append(("update",)))
    monkeypatch.setattr(
        main, "_run_wizard_action", lambda action, **kw: order.append(("update",)) or ["Updated."]
    )

    result = CliRunner().invoke(main.app, ["wizard"])

    assert result.exit_code == 0, result.output
    assert order[:2] == [("ask", ("claude_code",)), ("update",)]


def test_an_update_with_yes_never_asks(entry, monkeypatch):  # noqa: F811
    save_context({"token": "probe_pat_existing", "base_url": "https://api.test"})
    monkeypatch.setattr(main, "_confirm_pending_capture", lambda *a, **k: pytest.fail("asked under --yes"))
    monkeypatch.setattr(main, "_hand_off_update", lambda *a, **k: None)

    result = CliRunner().invoke(main.app, ["wizard", "--action", "update", "--yes"])

    assert result.exit_code == 0, result.output


def test_collect_reads_a_sign_ins_lock_into_the_menu_and_doctor(home, monkeypatch):
    """The flag comes from the file, through the real `doctor.collect`."""
    from probe.cli.capabilities import PluginState

    monkeypatch.setenv("PROBE_AGENT", "claude_code")
    _lock("claude_code")
    caps = doctor.collect(local=True, plugins=PluginState(names=frozenset({"probe-research-tap"})))
    assert caps.capture_killswitched and caps.capture_awaiting_confirmation
    assert any("finish Install" in str(line) for line in setup.describe_state(caps))
    assert "waiting for Install to confirm capture" in doctor.render(caps)


def test_a_settings_commit_plans_nothing_for_a_signed_out_tracking_plugin(home, monkeypatch):
    """The box reads the plugin fact, `plan` reads `tracking_on` (plugin AND a
    login): signed out, they disagree, and only `preserve` keeps the commit to
    the row that changed."""
    signed_out = _pending(logged_in_as=None, api_credential_valid=False, mcp_authenticated=False)
    handed = []
    monkeypatch.setattr(doctor, "collect", lambda: signed_out)
    monkeypatch.setattr(main, "_run_wizard_action", lambda a, **kw: handed.append(kw["selection_override"]) or [])
    main._apply_capability_settings(
        {setup.Setting.AUTO_UPDATE: True}, caps_by_source={"claude_code": signed_out}, base_now="https://api.test"
    )
    assert setup.plan(signed_out, handed[0]) == ["enable automatic updates"]


def test_preserved_tracking_removes_no_skills(home, monkeypatch):
    snapshot = _pending(tracking_plugin_installed=False)
    monkeypatch.setattr(doctor, "collect", lambda: snapshot)
    monkeypatch.setattr(setup, "apply_auto_update", lambda want: [])
    monkeypatch.setattr(setup, "remove_root_skills", lambda *a, **k: pytest.fail("removed skills on a Settings toggle"))
    main._apply_capability_settings(
        {setup.Setting.AUTO_UPDATE: True}, caps_by_source={"claude_code": snapshot}, base_now="https://api.test"
    )


@pytest.mark.parametrize(
    "overrides",
    [{"capture_plugin_installed": False}, {"capture_credential_valid": False}, {"capture_token_sources": ()}],
    ids=["no-capture-plugin", "refused-credential", "no-credential"],
)
def test_only_an_agent_capture_can_actually_resume_on_is_asked_about(home, monkeypatch, overrides):
    _lock("claude_code")
    monkeypatch.setattr(setup, "confirm_pending_capture", lambda sources: pytest.fail("asked"))
    assert main._confirm_pending_capture({"claude_code": _pending(**overrides)}, base_now="https://api.test") == []


def test_a_failed_turn_on_says_capture_is_still_off(home, monkeypatch):
    _lock("claude_code")
    monkeypatch.setattr(setup, "confirm_pending_capture", lambda sources: True)

    def boom(*_a, **_kw):
        raise typer.Exit(1)

    monkeypatch.setattr(main, "_run_wizard_action", boom)
    lines = main._confirm_pending_capture({"claude_code": _pending()}, base_now="https://api.test")
    assert "! not finished — pick “Install Probe” to turn capture on." in lines
    assert lines[-1] == "! Session capture is still off for Claude Code."
    assert capture.awaiting_confirmation("claude_code")


@pytest.mark.parametrize("answer", [None, tui.BACK])
def test_esc_or_ctrl_c_at_the_question_is_handed_back_and_changes_nothing(home, monkeypatch, answer):
    _lock("claude_code")
    monkeypatch.setattr(setup, "confirm_pending_capture", lambda sources: answer)
    monkeypatch.setattr(main, "_run_wizard_action", lambda *a, **kw: pytest.fail("applied"))
    assert main._confirm_pending_capture({"claude_code": _pending()}, base_now="https://api.test") is answer
    assert capture.awaiting_confirmation("claude_code")
    assert not os.environ.get(main.CAPTURE_QUESTION_ASKED_ENV), "unanswered: the next Update asks again"


def test_the_question_marks_the_environment_the_hand_off_carries(home, monkeypatch):
    """The newest release the hand-off execs inherits this environment, and
    must not ask again after a "Not now" (`CAPTURE_QUESTION_ASKED_ENV`)."""
    _lock("claude_code")
    monkeypatch.setattr(setup, "confirm_pending_capture", lambda sources: False)
    main._confirm_pending_capture({"claude_code": _pending()}, base_now="https://api.test")
    assert os.environ.get(main.CAPTURE_QUESTION_ASKED_ENV) == "1"


def test_an_update_already_asked_upstream_does_not_ask_again(entry, monkeypatch):  # noqa: F811
    save_context({"token": "probe_pat_existing", "base_url": "https://api.test"})
    monkeypatch.setenv(main.CAPTURE_QUESTION_ASKED_ENV, "1")
    picks = iter([Action.UPDATE, Action.EXIT])
    monkeypatch.setattr(setup, "run_action_menu", lambda _caps: next(picks))
    monkeypatch.setattr(main, "_confirm_pending_capture", lambda *a, **k: pytest.fail("asked twice"))
    monkeypatch.setattr(main, "_run_wizard_action", lambda action, **kw: ["Updated."])
    result = CliRunner().invoke(main.app, ["wizard"])
    assert result.exit_code == 0, result.output


def test_esc_at_the_question_returns_to_the_menu_without_updating(entry, monkeypatch):  # noqa: F811
    monkeypatch.setenv(main.CAPTURE_QUESTION_ASKED_ENV, "")  # restored on teardown, unlike delenv of an unset name
    save_context({"token": "probe_pat_existing", "base_url": "https://api.test"})
    picks = iter([Action.UPDATE, Action.EXIT])
    menus: list[int] = []
    monkeypatch.setattr(setup, "run_action_menu", lambda _caps: menus.append(1) or next(picks))
    monkeypatch.setattr(main, "_confirm_pending_capture", lambda *a, **k: tui.BACK)
    monkeypatch.setattr(main, "_run_wizard_action", lambda *a, **k: pytest.fail("updated after Esc"))
    result = CliRunner().invoke(main.app, ["wizard"])
    assert result.exit_code == 0, result.output
    assert len(menus) == 2, "back at the menu"


def test_the_questions_result_reaches_the_result_page(entry, monkeypatch):  # noqa: F811
    monkeypatch.setenv(main.CAPTURE_QUESTION_ASKED_ENV, "")  # restored on teardown, unlike delenv of an unset name
    save_context({"token": "probe_pat_existing", "base_url": "https://api.test"})
    picks = iter([Action.UPDATE, Action.EXIT])
    monkeypatch.setattr(setup, "run_action_menu", lambda _caps: next(picks))
    monkeypatch.setattr(main, "_confirm_pending_capture", lambda *a, **k: ["Session capture is on for Claude Code."])
    monkeypatch.setattr(main, "_run_wizard_action", lambda action, **kw: ["Updated."])
    pages: list = []
    monkeypatch.setattr(tui, "page", lambda lines, **kw: pages.append(list(lines)))
    result = CliRunner().invoke(main.app, ["wizard"])
    assert result.exit_code == 0, result.output
    assert pages and pages[0][0] == "Session capture is on for Claude Code."


def test_a_two_agent_update_asks_before_the_hand_off(entry, monkeypatch):  # noqa: F811
    monkeypatch.setenv(main.CAPTURE_QUESTION_ASKED_ENV, "")  # restored on teardown, unlike delenv of an unset name
    save_context({"token": "probe_pat_existing", "base_url": "https://api.test"})
    monkeypatch.setattr(setup, "detectable_sources", lambda: ("claude_code", "codex"))
    monkeypatch.setattr(setup, "run_agent_menu", lambda *a, **k: ("claude_code", "codex"))
    picks = iter([Action.UPDATE, Action.EXIT])
    monkeypatch.setattr(setup, "run_action_menu", lambda _caps: next(picks))
    order: list[tuple] = []
    monkeypatch.setattr(
        main, "_confirm_pending_capture", lambda caps_by_source, **_: order.append(("ask", tuple(caps_by_source))) or []
    )
    monkeypatch.setattr(main, "_hand_off_update", lambda *a, **k: order.append(("hand-off",)))
    monkeypatch.setattr(main, "_update_agents", lambda *a, **k: {})
    monkeypatch.setattr(main, "_run_wizard_action", lambda action, **kw: ["Updated."])
    result = CliRunner().invoke(main.app, ["wizard"])
    assert result.exit_code == 0, result.output
    assert order[:2] == [("ask", ("claude_code", "codex")), ("hand-off",)]


# --- the scripted half of bug 2: an omitted flag keeps a pending lock pending ----


def test_an_omitted_capture_flag_leaves_a_pending_lock_pending():
    pending = _pending()
    kept = setup.resolve_selection(pending, tracking=None, capture=None, auto_update=None, configured=True)
    assert kept.keeps(Capability.CAPTURE)
    asked_off = setup.resolve_selection(pending, tracking=None, capture=False, auto_update=None, configured=True)
    assert not asked_off.keeps(Capability.CAPTURE), "an explicit --no-capture still turns it off"
    fresh = setup.resolve_selection(pending, tracking=None, capture=None, auto_update=None, configured=False)
    assert not fresh.keeps(Capability.CAPTURE) and fresh.capture, "a first install confirms it"


def test_a_scripted_re_run_with_other_work_never_revokes_a_pending_credential(home, monkeypatch):
    """`probe wizard --action configure --yes --auto-update` on the Anthrogen
    machine: the run has other work, so it does not stop at "Already set up"."""
    _lock("claude_code")
    snapshot = _pending()
    monkeypatch.setattr(doctor, "collect", lambda: snapshot)
    monkeypatch.setattr(setup, "apply_auto_update", lambda want: [])
    main._run_wizard_action(
        Action.CONFIGURE, caps=snapshot, base_now="https://api.test", yes=True,
        tracking=None, capture=None, auto_update=True, agent_rules=None,
        uninstall=False, configured=True, telemetry=None,
    )
    assert home == [], "the parked credential was revoked"
    assert capture.awaiting_confirmation("claude_code")


def test_a_scripted_two_agent_re_run_keeps_only_the_pending_agents_capture(entry, monkeypatch):  # noqa: F811
    save_context({"token": "probe_pat_existing", "base_url": "https://api.test"})
    monkeypatch.setattr(setup, "detectable_sources", lambda: ("claude_code", "codex"))
    snapshots = {
        "claude_code": _pending(capture_killswitched=False, capture_awaiting_confirmation=False),
        "codex": _pending("codex"),
    }
    monkeypatch.setattr(doctor, "collect", lambda: snapshots[os.environ.get("PROBE_AGENT", "claude_code")])
    handed: dict[str, object] = {}
    monkeypatch.setattr(
        main, "_run_wizard_action",
        lambda action, **kw: handed.setdefault(os.environ.get("PROBE_AGENT"), kw.get("selection_override")) and [],
    )
    result = CliRunner().invoke(
        main.app, ["wizard", "--action", "configure", "--yes", "--agent", "claude_code", "--agent", "codex"]
    )
    assert result.exit_code == 0, result.output
    assert handed["codex"].keeps(Capability.CAPTURE), "the union's capture=True must not lift Codex's lock"
    assert not handed["claude_code"].keeps(Capability.CAPTURE)


# --- the state matrix this diff touches: no lock kind is torn down by an apply
# that was not asked to change capture, and its text never changes ------------

_DELIBERATE = "disabled by the Probe Research wizard\n"
_KINDS = {
    "pending-ready": (capture.AWAITING_CONFIRMATION, {}),
    "pending-no-credential": (capture.AWAITING_CONFIRMATION, {"capture_token_sources": ()}),
    "pending-no-plugin": (capture.AWAITING_CONFIRMATION, {"capture_plugin_installed": False}),
    "deliberate-off": (_DELIBERATE, {"capture_awaiting_confirmation": False, "capture_token_sources": ()}),
    "capture-on": (None, {"capture_killswitched": False, "capture_awaiting_confirmation": False}),
}


@pytest.mark.parametrize("kind", sorted(_KINDS))
@pytest.mark.parametrize("action", ["settings-commit", "scripted-re-run"])
def test_no_lock_kind_is_torn_down_by_an_unrelated_apply(home, monkeypatch, kind, action):
    text, overrides = _KINDS[kind]
    if text is not None:
        _lock("claude_code", text)
    snapshot = _pending(**overrides)
    monkeypatch.setattr(doctor, "collect", lambda: snapshot)
    monkeypatch.setattr(setup, "apply_auto_update", lambda want: [])
    monkeypatch.setattr(setup, "install_plugin", lambda *a, **k: pytest.fail("installed a plugin"))
    if action == "settings-commit":
        lines = main._apply_capability_settings(
            {setup.Setting.AUTO_UPDATE: True}, caps_by_source={"claude_code": snapshot}, base_now="https://api.test"
        )
        assert not any("not finished" in line for line in lines)
    else:
        main._run_wizard_action(
            Action.CONFIGURE, caps=snapshot, base_now="https://api.test", yes=True,
            tracking=None, capture=None, auto_update=True, agent_rules=None,
            uninstall=False, configured=True, telemetry=None,
        )
    assert home == [], "a capture credential was revoked"
    marker = tap_plugin_dir("claude_code") / ".disabled"
    assert (marker.read_text() if marker.exists() else None) == text
    if kind != "pending-no-credential" and kind != "deliberate-off":
        assert load_context().get("ingest_token") == "ros_ing_claude_code"


def test_the_degraded_install_leaves_a_pending_lock_pending(home, monkeypatch):
    """No agent CLI on PATH: Install's degraded screen names only the CLI and
    the sign-in, so capture is kept, and the union's off is not applied."""
    _lock("claude_code")
    snapshot = _pending(claude_available=False, agent_rules_stale=True)
    monkeypatch.setattr(doctor, "collect", lambda: snapshot)
    monkeypatch.setattr(setup, "apply_agent_rules", lambda *a, **k: [])
    selection = setup.Selection(
        tracking=True, capture=False, auto_update=False, agent_rules=True,
        preserve=frozenset({Capability.CAPTURE}),
    )
    main._run_wizard_action(
        Action.CONFIGURE, caps=snapshot, base_now="https://api.test", yes=True,
        tracking=None, capture=None, auto_update=None, agent_rules=None,
        uninstall=False, configured=True, selection_override=selection,
        authorization_needs=[], capture_sources=[], telemetry=None,
    )
    assert home == [] and capture.awaiting_confirmation("claude_code")


def test_the_degraded_install_screen_hands_over_a_selection_that_keeps_capture(entry, monkeypatch):  # noqa: F811
    """The wizard's own degraded screen (no agent CLI on PATH) builds it."""
    save_context({"token": "probe_pat_existing", "base_url": "https://api.test"})
    monkeypatch.setattr(setup, "detectable_sources", lambda: ())
    handed = []
    monkeypatch.setattr(main, "_run_wizard_action", lambda action, **kw: handed.append(kw.get("selection_override")) or [])
    result = CliRunner().invoke(main.app, ["wizard", "--action", "configure", "--agent", "claude_code"])
    assert result.exit_code == 0, result.output
    assert handed and handed[0] is not None and handed[0].keeps(Capability.CAPTURE)


def test_a_failed_turn_on_is_shown_before_the_hand_off(entry, monkeypatch):  # noqa: F811
    """The hand-off may exec the newest release: a failure cannot wait for
    this process's result page."""
    monkeypatch.setenv(main.CAPTURE_QUESTION_ASKED_ENV, "")
    save_context({"token": "probe_pat_existing", "base_url": "https://api.test"})
    picks = iter([Action.UPDATE, Action.EXIT])
    monkeypatch.setattr(setup, "run_action_menu", lambda _caps: next(picks))
    failed = ["! Session capture is still off for Claude Code."]
    monkeypatch.setattr(main, "_confirm_pending_capture", lambda *a, **k: list(failed))
    order: list = []
    monkeypatch.setattr(tui, "page", lambda lines, **kw: order.append(("page", list(lines))))
    monkeypatch.setattr(main, "_run_wizard_action", lambda action, **kw: order.append(("update",)) or ["Updated."])
    result = CliRunner().invoke(main.app, ["wizard"])
    assert result.exit_code == 0, result.output
    shown = "Session capture is still off for Claude Code."  # the verdict as the page's title
    assert order[0] == ("page", [shown]) and order[1] == ("update",)
    assert all(shown not in lines for kind, *rest in order[2:] if kind == "page" for lines in rest), "shown once"


def test_the_json_row_names_a_kept_capture_as_not_asked_for(monkeypatch):
    from probe.cli import json_events

    rows = []
    monkeypatch.setattr(json_events, "enabled", lambda: True)
    monkeypatch.setattr(json_events, "agent_result", lambda source, **kw: rows.append(kw))
    selection = setup.Selection(
        tracking=True, capture=False, auto_update=False, agent_rules=True, preserve=frozenset({Capability.CAPTURE})
    )
    main._record_configure("claude_code", selection, _pending(), ok=True)
    assert rows[0]["requested"]["capture"] is None and rows[0]["ok"] is True
