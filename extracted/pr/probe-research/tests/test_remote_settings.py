"""Probe staff changed a setting on this machine (research-os control/074).

The server answers a device with an open settings request with
`X-Probe-Settings-Requested`; the client that got it leaves a mark
(`probe._shared.settings_request`), and a later `probe` command, a Probe service
child included, applies it once (`probe.cli.remote_settings.apply_pending`, run
by `probe.cli.main._settings_request_notice`). What each test pins would fail
silently: a request no command on a service machine ever applies, one applied
twice over a change the person made since, a value that turns recording ON, a
running session left recording, or a mark that keeps the CLI asking after the
server closed the request.
"""

from __future__ import annotations

import importlib
import json
import os
import time
import uuid

import httpx
import pytest

from probe import version_policy
from probe._shared import device_mark, settings_request
from probe.cli import remote_settings
from probe.cli import telemetry as tm
from probe.sdk import session_marker
from probe.sdk.config import save_context
from probe.sdk.transport import Transport

cli_main = importlib.import_module("probe.cli.main")

STAMP = "1793060000"
BASE = "http://test"
ASKED = "2026-10-27T12:00:00Z"
FETCH = remote_settings.FETCH_PATH
APPLIED = remote_settings.APPLIED_PATH
OFF = session_marker.STATE_OFF
READ = session_marker.STATE_READ_ONLY
FULL = session_marker.STATE_FULL


@pytest.fixture(autouse=True)
def fresh_process(monkeypatch):
    settings_request._reset_for_tests()
    for name in ("PROBE_TOKEN", "PROBE_BASE_URL", "PROBE_DAEMON_SESSION", "PROBE_SESSION_STATE",
                 "PROBE_SESSION_TRACKING", "PROBE_SERVICE_CHILD"):
        monkeypatch.delenv(name, raising=False)
    # No Probe service here: `capture_switched` would look for one.
    monkeypatch.setattr("probe.cli.service_calls._reachable", lambda: False)
    yield
    settings_request._reset_for_tests()


def _mark(seen_ago: float = 0.0) -> None:
    path = version_policy.state_dir() / settings_request.FILENAME
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"requested_at": int(STAMP), "seen_at": time.time() - seen_ago}))


def _sid() -> str:
    return str(uuid.uuid4())


def _session(state: str) -> str:
    sid = _sid()
    assert session_marker.set_session_state(sid, state)
    return sid


def _argv(monkeypatch, command: str) -> None:
    monkeypatch.setattr(cli_main.sys, "argv", ["probe", command])


@pytest.fixture
def server(monkeypatch):
    """The CLI's real Client and Transport over a fake fetch and report;
    `answers[path]` is that path's (status, body)."""
    calls: list[httpx.Request] = []
    answers: dict[str, tuple[int, dict]] = {
        FETCH: (200, {"requested_at": ASKED, "setting": "session_default", "value": "off"}),
        APPLIED: (200, {"state": "cleared", "clear_reason": "applied"}),
    }

    def handle(request: httpx.Request) -> httpx.Response:
        calls.append(request)
        status, body = answers.get(request.url.path, (404, {"detail": "no route"}))
        return httpx.Response(status, json=body)

    from probe.sdk import transport as transport_mod

    real_client = httpx.Client

    def client(*args, **kwargs):
        kwargs.pop("verify", None)
        kwargs.pop("transport", None)
        return real_client(*args, transport=httpx.MockTransport(handle), **kwargs)

    monkeypatch.setattr(transport_mod.httpx, "Client", client)
    monkeypatch.setattr(cli_main._conn, "base_url", BASE, raising=False)
    save_context({"token": "probe_pat_device", "base_url": BASE})
    return calls, answers


def _paths(calls) -> list[str]:
    return [call.url.path for call in calls]


def _report(calls) -> dict:
    (sent,) = [call for call in calls if call.url.path == APPLIED]
    return json.loads(sent.content)


def _apply() -> remote_settings.Outcome:
    client = cli_main._new_client(base_url=BASE)
    try:
        return remote_settings.apply_pending(client, base_url=BASE)
    finally:
        client.close()


def _stored() -> dict:
    return json.loads(session_marker.config_path().read_text()).get(session_marker.DEFAULTS_KEY, {})


# ---------------------------------------------------------------------------
# the mark
# ---------------------------------------------------------------------------


def test_the_sdk_transport_notes_every_staff_request_kind():
    def handle(_request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={}, headers={settings_request.HEADER: STAMP})

    Transport(
        __import__("probe.sdk.config", fromlist=["Settings"]).Settings(base_url=BASE, token="t"),
        client=httpx.Client(base_url=BASE, transport=httpx.MockTransport(handle)),
        max_retries=0,
    ).request("GET", "/v1/me")
    assert settings_request.fresh() is True


def test_note_all_leaves_only_the_marks_the_answer_carries():
    from probe._shared import capture_repair, update_request

    for mark in (update_request.MARK, capture_repair.MARK, settings_request.MARK):
        mark.reset_for_tests()
    device_mark.note_all({settings_request.HEADER: STAMP, "X-Other": "1"})
    assert settings_request.fresh() is True
    assert update_request.fresh() is False and capture_repair.fresh() is False


# ---------------------------------------------------------------------------
# apply_pending
# ---------------------------------------------------------------------------


def test_it_moves_the_default_and_every_louder_session_and_reports(server):
    calls, _answers = server
    on, read, off = _session(FULL), _session(READ), _session(OFF)
    daemon = _session(session_marker.STATE_DAEMON)
    _mark()

    assert _apply() is remote_settings.Outcome.APPLIED
    assert session_marker.default_session_state() == OFF
    stored = _stored()
    assert stored[session_marker.STATE_DEFAULT_KEY] == OFF and stored[session_marker.TRACKING_DEFAULT_KEY] == "off"
    assert stored[session_marker.DEFAULT_SET_BY_KEY]["by"] == "probe-staff"
    assert session_marker.set_by_note().startswith("set by Probe staff on 20")
    assert [session_marker.session_state(s) for s in (on, read, off, daemon)] == [OFF] * 4
    assert session_marker.state_source(on) == session_marker.SOURCE_EXPLICIT, "a reload keeps it"
    report = _report(calls)
    assert report["requested_at"] == ASKED and report["default_changed"] is True
    assert report["sessions_moved"] == 3 and set(report["moved_sessions"]) == {on, read, daemon}
    assert report["env_shadowed"] is False and report["unsupported"] is False
    assert settings_request.fresh() is False, "the server took it: the mark goes"


def test_a_new_session_then_starts_off(server, monkeypatch):
    _mark()
    _apply()
    default, _source = session_marker.resolve_state_default(None)
    assert default == OFF


def test_read_never_makes_an_off_machine_or_session_louder(server):
    calls, answers = server
    answers[FETCH] = (200, {"requested_at": ASKED, "setting": "session_default", "value": "read"})
    session_marker.write_default_state(OFF)
    off, on = _session(OFF), _session(FULL)
    _mark()

    assert _apply() is remote_settings.Outcome.APPLIED
    assert session_marker.default_session_state() == OFF, "already quieter: kept"
    assert session_marker.default_set_by() is None
    assert session_marker.session_state(off) == OFF
    assert session_marker.session_state(on) == READ
    report = _report(calls)
    assert report["default_changed"] is False and report["moved_sessions"] == [on]


@pytest.mark.parametrize(
    "setting,value",
    [("session_default", "on"), ("session_default", "daemon"), ("session_default", "full"),
     ("auto_update", "off"), (None, "off")],
)
def test_anything_outside_the_allow_list_changes_nothing_and_is_settled(server, setting, value):
    calls, answers = server
    answers[FETCH] = (200, {"requested_at": ASKED, "setting": setting, "value": value})
    session_marker.write_default_state(READ)
    on = _session(FULL)
    _mark()

    assert _apply() is remote_settings.Outcome.UNSUPPORTED
    assert session_marker.default_session_state() == READ
    assert session_marker.session_state(on) == FULL
    report = _report(calls)
    assert report["unsupported"] is True and report["default_changed"] is False and report["sessions_moved"] == 0
    assert settings_request.fresh() is False


def test_a_lost_report_is_resent_and_never_reapplied(server):
    calls, answers = server
    answers[APPLIED] = (503, {"detail": "down"})
    first = _session(FULL)
    _mark()
    assert _apply() is remote_settings.Outcome.APPLIED_UNREPORTED
    assert settings_request.fresh() is True, "unreported: the mark stays"

    # The person turns things back on before the next window.
    session_marker.write_default_state(FULL)
    assert session_marker.set_session_state(first, FULL)
    answers[APPLIED] = (200, {"state": "cleared"})
    calls.clear()

    assert _apply() is remote_settings.Outcome.RESENT
    assert session_marker.default_session_state() == FULL, "their change stays"
    assert session_marker.session_state(first) == FULL
    assert session_marker.default_set_by() is None, "a local change drops staff's mark"
    assert _report(calls)["moved_sessions"] == [first], "the original report, sent again"
    assert settings_request.fresh() is False


def test_a_request_closed_or_never_open_clears_the_mark(server):
    calls, answers = server
    answers[FETCH] = (404, {"detail": {"code": "none_open"}})
    _mark()
    assert _apply() is remote_settings.Outcome.NOT_OPEN
    assert settings_request.fresh() is False
    assert APPLIED not in _paths(calls)


def test_no_answer_changes_nothing_and_keeps_the_mark(server):
    _calls, answers = server
    answers[FETCH] = (503, {"detail": "down"})
    on = _session(FULL)
    _mark()
    assert _apply() is remote_settings.Outcome.UNREACHED
    assert session_marker.session_state(on) == FULL and settings_request.fresh() is True


def test_env_override_still_writes_the_file_and_says_so(server, monkeypatch):
    calls, _answers = server
    monkeypatch.setenv("PROBE_SESSION_STATE", "on")
    _mark()
    _apply()
    assert _stored()[session_marker.STATE_DEFAULT_KEY] == OFF
    assert _report(calls)["env_shadowed"] is True


def test_an_unreadable_config_writes_nothing_and_keeps_the_mark(server):
    calls, _answers = server
    # Signed in through the environment-free context first, then the file breaks.
    path = session_marker.config_path()
    _mark()
    client = cli_main._new_client(base_url=BASE)
    try:
        path.write_text("{ not json")
        outcome = remote_settings.apply_pending(client, base_url=BASE)
    finally:
        client.close()
    assert outcome is remote_settings.Outcome.FAILED
    assert path.read_text() == "{ not json", "never replaced"
    assert APPLIED not in _paths(calls) and settings_request.fresh() is True
    assert not (version_policy.state_dir() / remote_settings.APPLIED_NAME).exists()


def test_a_held_lock_skips(server):
    from probe._shared import oscompat

    calls, _answers = server
    _mark()
    path = version_policy.state_dir() / remote_settings.LOCK_NAME
    with open(path, "a+b") as handle:
        oscompat.flock(handle.fileno(), oscompat.LOCK_EX | oscompat.LOCK_NB)
        assert _apply() is remote_settings.Outcome.NONE
    assert calls == []


def _age(sid: str, at: float) -> None:
    for path in session_marker.sessions_dir().glob(sid + ".*"):
        os.utime(path, (at, at))


def test_the_probe_service_is_told_about_the_newest_sessions_switched_off(server, monkeypatch):
    told: list[tuple[str, bool]] = []
    monkeypatch.setattr(
        "probe.cli.service_calls.capture_switched",
        lambda sid, *, off: told.append((sid, off)) or True,
    )
    monkeypatch.setattr(remote_settings, "MAX_SWITCH_CALLS", 2)
    oldest, middle, newest = (_session(FULL) for _ in range(3))
    for at, sid in ((1_000_000, oldest), (2_000_000, middle), (3_000_000, newest)):
        _age(sid, at)
    _mark()
    _apply()
    assert told == [(newest, True), (middle, True)], "newest first, within the cap"


def test_read_tells_the_service_nothing(server, monkeypatch):
    _calls, answers = server
    answers[FETCH] = (200, {"requested_at": ASKED, "setting": "session_default", "value": "read"})
    told: list[str] = []
    monkeypatch.setattr("probe.cli.service_calls.capture_switched", lambda sid, *, off: told.append(sid))
    _session(FULL)
    _mark()
    _apply()
    assert told == [], "read never stopped capture: nothing for the service to hold"


# ---------------------------------------------------------------------------
# where it runs
# ---------------------------------------------------------------------------


def test_a_probe_service_child_applies_it(server, monkeypatch):
    """On a machine with the Probe service every hook-run `probe` is a service
    child (the team note's sync): if those skipped it, nothing would apply it."""
    from probe.service.paths import SERVICE_CHILD_ENV

    calls, _answers = server
    monkeypatch.setenv(SERVICE_CHILD_ENV, "1")
    _mark()
    _argv(monkeypatch, "notes")
    cli_main._settings_request_notice()
    assert _paths(calls) == [FETCH, APPLIED]
    assert session_marker.default_session_state() == OFF


@pytest.mark.parametrize("command", ["log", "run", "daemon", "mcp", "update", "wizard", "service", "status"])
def test_never_from_a_run_command_a_long_lived_one_or_a_read_only_one(server, monkeypatch, command):
    calls, _answers = server
    _mark()
    _argv(monkeypatch, command)
    cli_main._settings_request_notice()
    assert calls == []


def test_never_from_a_command_a_probe_daemon_runs(server, monkeypatch):
    calls, _answers = server
    monkeypatch.setenv("PROBE_DAEMON_SESSION", "1")
    _mark()
    _argv(monkeypatch, "notes")
    cli_main._settings_request_notice()
    assert calls == []


def test_never_under_another_accounts_token(server, monkeypatch):
    calls, _answers = server
    monkeypatch.setenv("PROBE_TOKEN", "probe_pat_someone_else")
    _mark()
    _argv(monkeypatch, "notes")
    cli_main._settings_request_notice()
    assert calls == []


def test_one_try_per_window(server, monkeypatch):
    calls, answers = server
    answers[FETCH] = (503, {"detail": "down"})
    _mark()
    _argv(monkeypatch, "notes")
    cli_main._settings_request_notice()
    cli_main._settings_request_notice()
    assert _paths(calls) == [FETCH]


def test_no_mark_or_a_stale_one_asks_nothing(server, monkeypatch):
    calls, _answers = server
    _argv(monkeypatch, "notes")
    cli_main._settings_request_notice()
    _mark(seen_ago=settings_request.FRESH_S + 5)
    cli_main._settings_request_notice()
    assert calls == []


def test_it_never_raises_and_prints_nothing_off_a_terminal(server, monkeypatch, capsys):
    _mark()
    _argv(monkeypatch, "notes")
    _session(FULL)
    cli_main._settings_request_notice()
    assert capsys.readouterr() == ("", "")

    _mark()

    def boom(**_kw):
        raise RuntimeError("no client")

    monkeypatch.setattr(cli_main, "_new_client", boom)
    monkeypatch.setattr(cli_main, "_claim_window", lambda *_a: True)
    cli_main._settings_request_notice()
    assert capsys.readouterr() == ("", "")


def test_a_terminal_gets_one_line(server, monkeypatch, capsys):
    monkeypatch.setattr(remote_settings.sys.stderr, "isatty", lambda: True, raising=False)
    _session(FULL)
    _mark()
    _apply()
    err = capsys.readouterr().err
    assert err.count("\n") == 1 and "new sessions on this machine start off" in err
    assert "1 session(s) switched to off" in err


def test_the_line_never_claims_a_default_it_kept(server, monkeypatch, capsys):
    _calls, answers = server
    answers[FETCH] = (200, {"requested_at": ASKED, "setting": "session_default", "value": "read"})
    session_marker.write_default_state(OFF)
    _session(FULL)
    monkeypatch.setattr(remote_settings.sys.stderr, "isatty", lambda: True, raising=False)
    _mark()
    _apply()
    err = capsys.readouterr().err
    assert "new sessions" not in err and "1 session(s) switched to read" in err


def test_every_command_runs_it_after_the_capture_repair(monkeypatch):
    from typer.testing import CliRunner

    order: list[str] = []
    monkeypatch.setattr(cli_main, "_outbox_notice", lambda **_: None)
    monkeypatch.setattr(cli_main, "_version_notice", lambda: None)
    monkeypatch.setattr(cli_main, "_remote_update_notice", lambda: order.append("remote"))
    monkeypatch.setattr(cli_main, "_capture_repair_notice", lambda: order.append("repair"))
    monkeypatch.setattr(cli_main, "_settings_request_notice", lambda: order.append("settings"))
    monkeypatch.setattr(cli_main, "_ensure_capture_notice", lambda _command: None)

    CliRunner().invoke(cli_main.app, ["ignore", "list"])
    assert order == ["remote", "repair", "settings"]


# ---------------------------------------------------------------------------
# who set it
# ---------------------------------------------------------------------------


def test_session_default_and_doctor_say_staff_set_it_until_a_local_change(server):
    from typer.testing import CliRunner

    from probe.cli import doctor

    _mark()
    _apply()
    shown = json.loads(CliRunner().invoke(cli_main.app, ["session", "default"]).stdout)
    assert shown["machine_default"] == "off" and shown["set_by"].startswith("set by Probe staff on ")
    assert any("set by Probe staff" in row for row in doctor._daemon_rows())

    session_marker.write_default_state(FULL)
    shown = json.loads(CliRunner().invoke(cli_main.app, ["session", "default"]).stdout)
    assert "set_by" not in shown
    assert session_marker.default_set_by() is None


def test_the_event_carries_words_and_counts_only(monkeypatch):
    records: list[dict] = []
    monkeypatch.setenv("PROBE_TELEMETRY", "on")
    monkeypatch.setattr(tm, "_sender", None)
    monkeypatch.setattr(tm, "_flush_registered", True)
    monkeypatch.setattr(tm._Sender, "start", lambda self: None)
    monkeypatch.setattr(tm._Sender, "put", lambda self, rec: records.append(rec))

    assert tm.emit_settings_remote_applied(
        setting="session_default", value="off", default_changed=True, sessions_moved=3, env_shadowed=False,
        unsupported=False, reported=True, base_url="https://api.research.prbe.ai",
    )
    (record,) = [r for r in records if r["event"] == tm.EVENT_SETTINGS_REMOTE_APPLIED]
    assert record["properties"]["sessions_moved"] == 3 and record["properties"]["value"] == "off"
    assert "moved_sessions" not in record["properties"], "never a session id"


# ---------------------------------------------------------------------------
# review fixes (2026-10-27)
# ---------------------------------------------------------------------------


def test_a_lost_read_report_is_resent_and_never_reapplied(server):
    calls, answers = server
    answers[FETCH] = (200, {"requested_at": ASKED, "setting": "session_default", "value": "read"})
    answers[APPLIED] = (503, {"detail": "down"})
    first = _session(FULL)
    _mark()
    assert _apply() is remote_settings.Outcome.APPLIED_UNREPORTED
    assert session_marker.set_session_state(first, FULL)
    answers[APPLIED] = (200, {"state": "cleared"})
    calls.clear()
    assert _apply() is remote_settings.Outcome.RESENT
    assert session_marker.session_state(first) == FULL
    assert _report(calls)["moved_sessions"] == [first]
    assert settings_request.fresh() is False


def test_a_lost_unsupported_report_is_resent_and_changes_nothing(server):
    calls, answers = server
    answers[FETCH] = (200, {"requested_at": ASKED, "setting": "session_default", "value": "on"})
    answers[APPLIED] = (503, {"detail": "down"})
    on = _session(FULL)
    _mark()
    assert _apply() is remote_settings.Outcome.UNSUPPORTED
    assert settings_request.fresh() is True, "unreported: the mark stays"
    answers[APPLIED] = (200, {"state": "cleared"})
    calls.clear()
    assert _apply() is remote_settings.Outcome.RESENT
    assert _report(calls)["unsupported"] is True
    assert session_marker.session_state(on) == FULL and settings_request.fresh() is False


def test_read_lowers_a_louder_default(server):
    calls, answers = server
    answers[FETCH] = (200, {"requested_at": ASKED, "setting": "session_default", "value": "read"})
    session_marker.write_default_state(FULL)
    _mark()
    assert _apply() is remote_settings.Outcome.APPLIED
    stored = _stored()
    assert stored[session_marker.STATE_DEFAULT_KEY] == READ and stored[session_marker.TRACKING_DEFAULT_KEY] == "off"
    assert session_marker.default_set_by()["value"] == READ
    assert _report(calls)["default_changed"] is True


def test_a_session_decided_by_a_legacy_file_is_switched_too(server):
    calls, _answers = server
    sid = _sid()
    path = session_marker.sessions_dir() / (sid + ".tracking")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("on")
    assert session_marker.session_state(sid) == FULL
    _mark()
    assert _apply() is remote_settings.Outcome.APPLIED
    assert session_marker.session_state(sid) == OFF
    assert _report(calls)["moved_sessions"] == [sid]


def test_a_session_already_quieter_is_never_raised_even_under_its_lock():
    off = _session(OFF)
    assert session_marker.lower_session_state(off, READ) is None
    assert session_marker.session_state(off) == OFF
    on = _session(FULL)
    assert session_marker.lower_session_state(on, READ) is True
    assert session_marker.session_state(on) == READ


def test_nothing_changes_when_the_claim_cannot_be_recorded(server, monkeypatch):
    calls, _answers = server
    monkeypatch.setattr(version_policy, "atomic_write_json", lambda *_a, **_k: False)
    on = _session(FULL)
    _mark()
    assert _apply() is remote_settings.Outcome.FAILED
    assert session_marker.session_state(on) == FULL
    assert session_marker.default_session_state() == FULL
    assert APPLIED not in _paths(calls) and settings_request.fresh() is True


def test_a_session_whose_switch_cannot_be_written_is_retried_alone_then_reported(server, monkeypatch):
    calls, _answers = server
    stuck, fine = _session(FULL), _session(FULL)
    real = session_marker.lower_session_state
    broken = {stuck}
    monkeypatch.setattr(
        session_marker, "lower_session_state",
        lambda sid, state: False if sid in broken else real(sid, state),
    )
    _mark()
    assert _apply() is remote_settings.Outcome.PENDING
    assert APPLIED not in _paths(calls), "not reported while a session still records"
    assert session_marker.session_state(fine) == OFF and session_marker.session_state(stuck) == FULL
    assert session_marker.set_session_state(fine, FULL)  # the person turns one back on

    broken.clear()
    assert _apply() is remote_settings.Outcome.RESENT
    assert session_marker.session_state(stuck) == OFF
    assert session_marker.session_state(fine) == FULL, "a session that moved is never touched again"
    report = _report(calls)
    assert sorted(report["moved_sessions"]) == sorted([fine, stuck]) and report["sessions_moved"] == 2


def test_a_session_that_never_takes_the_switch_is_reported_after_the_last_attempt(server, monkeypatch):
    calls, _answers = server
    stuck = _session(FULL)
    monkeypatch.setattr(session_marker, "lower_session_state", lambda sid, state: False)
    _mark()
    outcomes = [_apply() for _ in range(remote_settings.MAX_ATTEMPTS)]
    assert outcomes[:-1] == [remote_settings.Outcome.PENDING] * (remote_settings.MAX_ATTEMPTS - 1)
    assert outcomes[-1] is remote_settings.Outcome.RESENT
    assert _report(calls)["moved_sessions"] == [] and session_marker.session_state(stuck) == FULL


def test_staff_are_never_credited_with_a_value_they_did_not_set(server, monkeypatch):
    from probe.cli import doctor

    _mark()
    _apply()
    assert session_marker.set_by_note()
    monkeypatch.setenv("PROBE_SESSION_STATE", "on")
    assert session_marker.set_by_note() is None
    assert not any("set by Probe staff" in row for row in doctor._daemon_rows())
    monkeypatch.delenv("PROBE_SESSION_STATE")
    # A writer that does not know the key (an older CLI) moves the default back on.
    data = json.loads(session_marker.config_path().read_text())
    data[session_marker.DEFAULTS_KEY][session_marker.STATE_DEFAULT_KEY] = FULL
    session_marker.config_path().write_text(json.dumps(data))
    assert session_marker.default_set_by() is None and session_marker.set_by_note() is None


def _write_record(phase: str, moving_since: float | None = None, **report) -> None:
    from probe import version_policy as vp

    vp.atomic_write_json(
        vp.state_dir() / remote_settings.APPLIED_NAME,
        {"requested_at": ASKED, "report": {"requested_at": ASKED, **report}, "phase": phase,
         "pending": [], "attempts": 1, "reported": False,
         "moving_since": time.time() if moving_since is None else moving_since},
    )


def test_a_claim_left_with_nothing_changed_is_applied_afresh(server):
    calls, _answers = server
    on = _session(FULL)
    _write_record(remote_settings.PHASE_CLAIMED)
    _mark()
    assert _apply() is remote_settings.Outcome.APPLIED
    assert session_marker.session_state(on) == OFF and session_marker.default_session_state() == OFF
    report = _report(calls)
    assert report["default_changed"] is True and report["moved_sessions"] == [on]


def test_an_apply_stopped_after_the_default_moves_the_sessions_next_window(server):
    calls, _answers = server
    on = _session(FULL)
    _age(on, 1_000_000)
    session_marker.lower_default_state(OFF, by=session_marker.SET_BY_STAFF, at="2026-10-27T12:00:00Z")
    _write_record(remote_settings.PHASE_DEFAULT, default_changed=True)
    _mark()
    assert _apply() is remote_settings.Outcome.RESENT
    assert session_marker.session_state(on) == OFF
    report = _report(calls)
    assert report["default_changed"] is True and report["moved_sessions"] == [on]


def test_a_report_that_never_landed_is_sent_once_when_the_request_is_gone(server):
    calls, answers = server
    answers[APPLIED] = (503, {"detail": "down"})
    _session(FULL)
    _mark()
    assert _apply() is remote_settings.Outcome.APPLIED_UNREPORTED
    # Staff canceled (or it expired): the server has nothing open any more.
    answers[FETCH] = (404, {"detail": {"code": "none_open"}})
    answers[APPLIED] = (200, {"state": "cleared"})
    calls.clear()
    assert _apply() is remote_settings.Outcome.NOT_OPEN
    assert _paths(calls) == [FETCH, APPLIED] and _report(calls)["requested_at"] == ASKED
    assert settings_request.fresh() is False
    calls.clear()
    _mark()
    assert _apply() is remote_settings.Outcome.NOT_OPEN
    assert _paths(calls) == [FETCH], "once"


def test_the_line_says_an_environment_variable_still_decides(server, monkeypatch, capsys):
    monkeypatch.setenv("PROBE_SESSION_STATE", "on")
    monkeypatch.setattr(remote_settings.sys.stderr, "isatty", lambda: True, raising=False)
    _mark()
    _apply()
    err = capsys.readouterr().err
    assert "PROBE_SESSION_STATE still decides here" in err and "new sessions on this machine start" not in err


def test_a_session_turned_back_on_after_a_stopped_window_stays_on(server):
    """The window stopped while moving sessions; one it had moved the person turned
    back on before the next: that one is not switched again."""
    calls, _answers = server
    not_reached = _session(FULL)
    _age(not_reached, 1_000_000)
    since = 2_000_000
    turned_back_on = _session(FULL)  # written now: after the stopped window began
    _write_record(remote_settings.PHASE_DEFAULT, moving_since=since, default_changed=True)
    _mark()
    assert _apply() is remote_settings.Outcome.RESENT
    assert session_marker.session_state(not_reached) == OFF
    assert session_marker.session_state(turned_back_on) == FULL
    assert _report(calls)["moved_sessions"] == [not_reached]


def test_the_line_names_the_older_variable_when_that_is_the_one_set(server, monkeypatch, capsys):
    monkeypatch.setenv("PROBE_SESSION_TRACKING", "on")
    monkeypatch.setattr(remote_settings.sys.stderr, "isatty", lambda: True, raising=False)
    _mark()
    _apply()
    assert "PROBE_SESSION_TRACKING still decides here" in capsys.readouterr().err
