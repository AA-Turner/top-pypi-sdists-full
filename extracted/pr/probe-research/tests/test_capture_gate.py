"""The capture gate's own pieces (`probe.service.capture_gate`): the gaps, the
switch it reads, and the drains it wraps in the loaded tap. The whole path, a
real service recording a real tap against a stub server, is
`test_probe_off_capture.py`."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import threading
import types
from pathlib import Path

import pytest

from probe.service import capture_gate as gate

TAP_ROOT = Path(__file__).resolve().parents[1] / "plugins" / "probe-research-tap"


# -- gaps -------------------------------------------------------------------------


def test_a_gap_opens_closes_and_never_closes_before_it_opened():
    gaps = gate.opened([], 100)
    assert gaps == [[100, None]] and gate.is_open(gaps)
    assert gate.opened(gaps, 500) == gaps  # one open gap at a time
    closed = gate.closed(gaps, 40)
    assert closed == [[100, 100]] and not gate.is_open(closed)
    assert gate.closed(gate.opened(closed, 200), 300) == [[100, 100], [200, 300]]


def test_a_line_is_in_a_gap_by_where_it_starts():
    gaps = [[10, 20], [30, None]]
    assert [gate.in_gap(gaps, offset) for offset in (9, 10, 19, 20, 29, 30, 10**9)] == [
        False, True, True, False, False, True, True]


def test_too_many_gaps_merge_the_oldest_and_drop_what_lay_between():
    gaps: list = []
    for start in range(0, (gate.MAX_GAPS + 2) * 10, 10):
        gaps = gate.closed(gate.opened(gaps, start), start + 5)
    assert len(gaps) <= gate.MAX_GAPS
    assert gaps[0][0] == 0  # the oldest stretch still starts where it did
    assert gate.in_gap(gaps, 7)  # what lay between two merged gaps is dropped, never sent


def test_a_saved_record_of_gaps_that_does_not_read_is_dropped_piece_by_piece():
    params = {gate.GAPS_KEY: [[0, 10], ["x", 3], [5, 2], [7, None], [True, 9], "junk"]}
    assert gate.gaps_of(params) == [[0, 10], [7, None]]
    assert gate.gaps_of({}) == [] and gate.gaps_of({gate.GAPS_KEY: "no"}) == []


# -- the switch ---------------------------------------------------------------------


def _session(tmp_path: Path, sid: str = "s-0123456789", **env) -> dict:
    state = tmp_path / "state" / "probe"
    return {"sid": sid, "state_dir": str(state), "cwd": str(tmp_path),
            "env": {"HOME": str(tmp_path / "home"), "XDG_CONFIG_HOME": str(tmp_path / "config"), **env}}


def _store(tmp_path: Path, sid: str, name: str, value: str) -> None:
    folder = tmp_path / "state" / "probe" / "sessions"
    folder.mkdir(parents=True, exist_ok=True)
    (folder / f"{sid}.{name}").write_text(value + "\n")


def test_the_switch_is_the_sessions_own_state_read_where_its_registrant_keeps_it(tmp_path):
    params = _session(tmp_path)
    assert gate.switch(params) == "full"  # nobody decided: the shipped default
    _store(tmp_path, params["sid"], "state", "off")
    assert gate.is_off(params)
    _store(tmp_path, params["sid"], "state", "read-only")
    assert gate.switch(params) == "read-only" and not gate.is_off(params)


def test_a_legacy_off_marker_is_read_only_never_off(tmp_path):
    """`session_marker.session_state`'s migration: the old two-valued `off`
    meant "stop recording, keep searching", which is `read-only`."""
    params = _session(tmp_path)
    _store(tmp_path, params["sid"], "tracking", "off")
    assert gate.switch(params) == "read-only"


def test_an_undecided_session_takes_the_machine_default_from_its_own_environment(tmp_path):
    params = _session(tmp_path)
    config = tmp_path / "config" / "probe" / "config.json"
    config.parent.mkdir(parents=True)
    config.write_text(json.dumps({"defaults": {"session_state": "off"}}))
    assert gate.is_off(params)
    # The environment's override beats the file, as everywhere in the client.
    assert gate.switch({**params, "env": {**params["env"], "PROBE_SESSION_STATE": "read"}}) == "read-only"
    # The service's own process environment decides nothing.
    assert "PROBE_SESSION_STATE" not in os.environ or os.environ["PROBE_SESSION_STATE"] != "read"


def test_a_switch_that_cannot_be_read_is_never_off():
    assert gate.switch({"sid": None, "env": {}}) is None
    assert gate.switch({"sid": "no/such/../id", "env": {}}) is None


# -- the drains, wrapped ----------------------------------------------------------------


def _fake_tap(lines: list[bytes]):
    """A stand-in tap: `session_journal` whose `stage` reads `lines` as the real
    one does (its `end` is each line's start offset), and `reconcile`."""
    sj = types.ModuleType("fake_session_journal")
    reconcile = types.ModuleType("fake_reconcile")

    def _sanitizer(source):
        return lambda line: {"kept": line}

    def _title_reader(source):
        return lambda line: ("title of " + line, False)

    class Journal:
        pending_body = None

        def pending(self, sid):
            return self.pending_body

        def stage(self, sid, **_kw):
            sanitize, read_title = sj._sanitizer("x"), sj._title_reader("x")
            out, end = [], 0
            for raw in lines:
                value = sanitize(raw.decode().strip())
                read_title(raw.decode().strip())
                if value is not None:
                    out.append(value["kept"])
                end += len(raw)
            return out

    sj._sanitizer, sj._title_reader, sj.Journal = _sanitizer, _title_reader, Journal
    reconcile.find_gaps = lambda *a, **k: [types.SimpleNamespace(session_id=s) for s in ("a-0123456789", "b-0123456789")]
    return types.SimpleNamespace(session_journal=sj, reconcile=reconcile)


@pytest.fixture
def clean_unsettled():
    with gate._LOCK:
        gate._UNSETTLED.clear()
        gate._LIVE.clear()
    yield
    with gate._LOCK:
        gate._UNSETTLED.clear()
        gate._LIVE.clear()


def test_a_drain_of_this_process_never_stages_a_session_with_a_gap_not_settled(clean_unsettled, monkeypatch):
    tap = _fake_tap([b"one\n", b"two\n"])
    assert gate.install(tap)
    assert gate.install(tap)  # once
    monkeypatch.setattr(gate, "_read_switch", lambda sid: None)
    journal = tap.session_journal.Journal()
    assert journal.stage("a-0123456789") == ["one", "two"]
    gate.unsettled("a-0123456789", [[0, None]])
    assert journal.stage("a-0123456789") is None
    # A batch staged before the switch moved still goes (it may flush; nothing is deleted).
    journal.pending_body = b"{}"
    assert journal.stage("a-0123456789") == ["one", "two"]
    journal.pending_body = None
    assert [g.session_id for g in tap.reconcile.find_gaps()] == ["b-0123456789"]
    gate.unsettled("a-0123456789", [])  # an empty publish lifts nothing
    assert journal.stage("a-0123456789") is None
    gate.settled("a-0123456789")  # only a settle does
    assert journal.stage("a-0123456789") == ["one", "two"]


def test_a_session_whose_switch_reads_off_is_left_alone_by_every_drain(clean_unsettled, monkeypatch):
    tap = _fake_tap([b"one\n"])
    gate.install(tap)
    monkeypatch.setattr(gate, "_read_switch", lambda sid: "off" if sid == "b-0123456789" else "full")
    assert tap.session_journal.Journal().stage("b-0123456789") is None
    assert [g.session_id for g in tap.reconcile.find_gaps()] == ["a-0123456789"]


def test_settling_drops_exactly_the_lines_that_start_in_a_gap_and_only_on_its_own_thread(clean_unsettled, monkeypatch):
    lines = [b"on-1\n", b"off-1\n", b"off-2\n", b"on-2\n"]
    tap = _fake_tap(lines)
    gate.install(tap)
    monkeypatch.setattr(gate, "_read_switch", lambda sid: None)
    gap = [[len(lines[0]), len(lines[0]) + len(lines[1]) + len(lines[2])]]
    gate.unsettled("a-0123456789", gap)
    journal = tap.session_journal.Journal()
    seen: dict = {}

    def other_thread():
        seen["other"] = journal.stage("a-0123456789")

    with gate._catchup("a-0123456789", gap):
        settled = journal.stage("a-0123456789")
        thread = threading.Thread(target=other_thread)
        thread.start()
        thread.join()
    assert settled == ["on-1", "on-2"]
    assert seen["other"] is None  # another drain still leaves it alone meanwhile


def test_a_tap_without_what_the_gate_wraps_is_not_gated():
    tap = types.SimpleNamespace(session_journal=types.ModuleType("bare"), reconcile=types.ModuleType("bare2"))
    assert gate.install(tap) is False


_PIN = (
    "import inspect, sys; sys.path.insert(0, sys.argv[1]);"
    "from tap import session_journal as sj, reconcile, main, threadenv, config, record_client, session_identity, hosted;"
    "code = sj.Journal.stage.__code__; assert 'end' in code.co_varnames, 'stage keeps no end';"
    "src = inspect.getsource(sj.Journal.stage);"
    "assert all(f in src for f in ('sanitize = _sanitizer(self.source)', 'read_title = _title_reader(self.source)',"
    " 'value = sanitize(line)', 'named = read_title(line)', 'end += length')), 'stage reads lines another way';"
    "missing = [n for n in ('_sanitizer', '_title_reader', 'Wire', 'Journal', 'ProtocolRestarted',"
    " 'ReconciliationRequired', 'recoverable', 'SessionDeleted', 'state_root', 'complete_line_end')"
    " if not callable(getattr(sj, n, None))];"
    "missing += ['Journal.' + n for n in ('claim_live', 'get', 'ensure', 'update', 'pending', 'stage', 'deliver',"
    " 'reconcile_pending', 'close') if not callable(getattr(sj.Journal, n, None))];"
    "missing += [] if 'directory' in inspect.signature(sj.Journal.__init__).parameters else ['Journal(directory=)'];"
    "ensure = inspect.signature(sj.Journal.ensure).parameters; stage = inspect.signature(sj.Journal.stage).parameters;"
    "missing += [] if all(k in ensure for k in ('historical', 'provenance', 'cwd')) else ['ensure(...)'];"
    "missing += [] if all(k in stage for k in ('cwd', 'finalize')) else ['stage(...)'];"
    "missing += ['config.' + n for n in ('killswitch_active', 'cwd_disabled', 'load_token', 'api_base_url',"
    " 'capture_source', 'hosted_file', 'token_file') if not callable(getattr(config, n, None))];"
    "missing += [] if callable(getattr(sj.Wire, '_request', None)) else ['Wire._request'];"
    "missing += [] if callable(getattr(sj, 'DeliveryPending', None)) else ['DeliveryPending'];"
    "missing += [m for m, f in (('reconcile.find_gaps', getattr(reconcile, 'find_gaps', None)),"
    " ('main._resolve_codex_transcript', getattr(main, '_resolve_codex_transcript', None)),"
    " ('threadenv.install', getattr(threadenv, 'install', None)),"
    " ('record_client._write_hosted', getattr(record_client, '_write_hosted', None)),"
    " ('session_identity.validate_identity', getattr(session_identity, 'validate_identity', None)),"
    " ('hosted.Controls', getattr(hosted, 'Controls', None)), ('hosted.record', getattr(hosted, 'record', None)))"
    " if not callable(f)];"
    "assert not missing, missing; print('ok')"
)


def _released_taps() -> list[tuple[str, str]]:
    """`(version, commit)`: the first commit of each tap 0.10.x (the service
    hosts taps from 0.10.0), from this checkout's history; none in a shallow one."""
    init = "agent/plugins/probe-research-tap/tap/__init__.py"
    try:
        root = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=TAP_ROOT, capture_output=True, text=True,
                              timeout=30, check=True).stdout.strip()
        commits = subprocess.run(["git", "log", "--format=%H", "--reverse", "--", init], cwd=root,
                                 capture_output=True, text=True, timeout=60, check=True).stdout.split()
    except (OSError, subprocess.SubprocessError):
        return []
    found: dict[str, str] = {}
    for commit in commits:
        try:
            text = subprocess.run(["git", "show", f"{commit}:{init}"], cwd=root, capture_output=True,
                                  text=True, timeout=30, check=True).stdout
        except (OSError, subprocess.SubprocessError):
            continue
        for line in text.splitlines():
            if line.startswith("__version__") and '"0.10.' in line:
                found.setdefault(line.split('"')[1], commit)
    return sorted(found.items(), key=lambda pair: tuple(int(p) for p in pair[0].split(".")))


_RELEASED = _released_taps()


def test_the_checkout_knows_the_released_taps():
    if not _RELEASED:
        pytest.skip("no tap history here (a shallow checkout)")
    versions = [v for v, _c in _RELEASED]
    assert versions[0] == "0.10.0" and "0.10.17" in versions


@pytest.mark.parametrize("version, commit", _RELEASED or [("in-tree", "")], ids=[v for v, _c in _RELEASED] or ["in-tree"])
def test_every_released_tap_has_what_the_gate_reads_and_wraps(version, commit, tmp_path):
    """The gate reads `stage`'s own `end` (each line's start offset) from its
    frame, wraps `_sanitizer`, `_title_reader`, `Journal.stage` and
    `reconcile.find_gaps`, and settles and claims through the journal, the
    wire and the tap's config: true of every tap the service can host, 0.10.0
    to now (`Journal.release_live` is from 0.10.13; before it `close()`
    releases the claim, which the gate always calls after it). A tap that
    renames one fails here first."""
    root = TAP_ROOT
    if commit:
        top = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=TAP_ROOT, capture_output=True, text=True,
                             timeout=30, check=True).stdout.strip()
        archive = subprocess.run(["git", "archive", commit, "agent/plugins/probe-research-tap/tap"], cwd=top,
                                 capture_output=True, timeout=60, check=True).stdout
        subprocess.run(["tar", "-x", "-C", str(tmp_path)], input=archive, check=True, timeout=60)
        root = tmp_path / "agent" / "plugins" / "probe-research-tap"
    done = subprocess.run([sys.executable, "-I", "-c", _PIN, str(root)], capture_output=True, text=True, timeout=60)
    assert done.returncode == 0 and done.stdout.strip() == "ok", (version, done.stderr[-2000:])


def test_the_in_tree_tap_has_what_the_gate_reads_and_wraps():
    done = subprocess.run([sys.executable, "-I", "-c", _PIN, str(TAP_ROOT)], capture_output=True, text=True, timeout=60)
    assert done.returncode == 0 and done.stdout.strip() == "ok", done.stderr[-2000:]


def test_a_tap_from_before_destination_name_still_finds_its_journal(tmp_path, monkeypatch):
    """Taps 0.10.0-0.10.6 write `destination.json` with no constant naming it:
    the claim of a held session is found there too."""
    import hashlib

    sj = types.SimpleNamespace(state_root=lambda: tmp_path)  # no DESTINATION_NAME
    destination = {"base_url": "http://x", "customer_id": "c", "source": "claude_code"}
    name = hashlib.sha256(json.dumps([destination["base_url"], "c", "claude_code"]).encode()).hexdigest()
    folder = tmp_path / name
    folder.mkdir()
    (folder / "destination.json").write_text(json.dumps(destination))
    import sqlite3

    conn = sqlite3.connect(folder / "state.sqlite3")
    conn.execute("CREATE TABLE sessions(session_id TEXT PRIMARY KEY, state TEXT NOT NULL)")
    conn.execute("INSERT INTO sessions VALUES ('s-0123456789', '{}')")
    conn.commit()
    conn.close()
    assert gate._journals_holding(sj, "s-0123456789") == [(tmp_path, destination)]


# -- reading the switch: the same answer as the session marker, cheaply ---------------


@pytest.mark.parametrize("case", [
    {}, {"state": "off"}, {"state": "full"}, {"state": "read-only"}, {"state": "daemon"}, {"state": "junk"},
    {"tracking": "off"}, {"tracking": "on"}, {"off_file": True}, {"config": {"defaults": {"session_state": "off"}}},
    {"config": {"defaults": {"tracking": "off"}}}, {"config": "not json"}, {"env": {"PROBE_SESSION_STATE": "off"}},
    {"env": {"PROBE_SESSION_TRACKING": "off"}}, {"env": {"PROBE_SESSION_STATE": "read"}, "state": None},
])
def test_the_switch_reads_as_the_session_marker_reads_it(tmp_path, monkeypatch, case):
    from probe.sdk import session_marker

    sid = "s-0123456789"
    state_home, config_home = tmp_path / "state", tmp_path / "config"
    sessions = state_home / "probe" / "sessions"
    sessions.mkdir(parents=True)
    if case.get("state"):
        (sessions / f"{sid}.state").write_text(case["state"] + "\n")
    if case.get("tracking"):
        (sessions / f"{sid}.tracking").write_text(case["tracking"] + "\n")
    if case.get("off_file"):
        (sessions / f"{sid}.off").write_text("")
    if "config" in case:
        (config_home / "probe").mkdir(parents=True)
        value = case["config"]
        (config_home / "probe" / "config.json").write_text(value if isinstance(value, str) else json.dumps(value))
    env = {"HOME": str(tmp_path / "home"), "XDG_STATE_HOME": str(state_home), "XDG_CONFIG_HOME": str(config_home),
           **case.get("env", {})}
    for name in ("PROBE_SESSION_STATE", "PROBE_SESSION_TRACKING", "PROBE_CONFIG_PATH"):
        monkeypatch.delenv(name, raising=False)
    for name, value in env.items():
        monkeypatch.setenv(name, value)
    expected = session_marker.session_state(sid) or session_marker.resolve_state_default(None)[0]
    assert gate.read_switch(sid, sessions, env) == expected


def test_the_switch_is_read_again_only_when_its_files_change(tmp_path, monkeypatch):
    params = _session(tmp_path)
    reads = []
    real = gate._ladder
    monkeypatch.setattr(gate, "_ladder", lambda *a: reads.append(1) or real(*a))
    for _ in range(50):
        gate.switch(params)
    assert len(reads) == 1
    _store(tmp_path, params["sid"], "state", "off")
    assert gate.is_off(params) and len(reads) == 2
    for _ in range(50):
        gate.is_off(params)
    assert len(reads) == 2


# -- the gap file -----------------------------------------------------------------------


def test_the_gap_file_round_trips_in_its_documented_shape(tmp_path):
    sessions = tmp_path / "sessions"
    assert gate.read_gap_file(sessions, "s-0123456789") == []
    assert gate.write_gap_file(sessions, "s-0123456789", [[30, None], [0, 10], [0, 10]], "/t/x.jsonl")
    path = sessions / "s-0123456789.gaps"
    data = json.loads(path.read_text())
    assert data["v"] == 1 and data["sid"] == "s-0123456789" and data["transcript"] == "/t/x.jsonl"
    assert data["gaps"] == [[0, 10], [30, None]] and isinstance(data["updated_at"], float)
    assert oct(path.stat().st_mode & 0o777) == "0o600"
    assert gate.read_gap_file(sessions, "s-0123456789") == [[0, 10], [30, None]]
    assert gate.write_gap_file(sessions, "s-0123456789", [])
    assert not path.exists() and gate.read_gap_file(sessions, "s-0123456789") == []


def test_a_gap_starting_past_an_open_one_adds_nothing():
    assert gate.normalized([[50, 60], [10, None], [5, 8]]) == [[5, 8], [10, None]]


def test_a_first_look_never_lifts_what_an_earlier_recording_left_unsettled(clean_unsettled):
    gate.unsettled("a-0123456789", [[0, None]])
    gate.unsettled("a-0123456789", [])  # a fresh recording of it, reading on, publishes nothing
    with gate._LOCK:
        assert gate._UNSETTLED["a-0123456789"] == [[0, None]]
    gate.settled("a-0123456789")
    with gate._LOCK:
        assert "a-0123456789" not in gate._UNSETTLED


def test_a_drain_leaves_alone_a_session_whose_gap_file_holds_a_gap(clean_unsettled, monkeypatch, tmp_path):
    """Its record in `recorders.json` gone, its `.state` pruned: the gap file
    still keeps every drain of this process off it."""
    tap = _fake_tap([b"one\n"])
    gate.install(tap)
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    sessions = gate.sessions_dir_for(os.environ)
    gate.write_gap_file(sessions, "a-0123456789", [[0, None]], None)
    monkeypatch.setattr(gate, "_read_switch", lambda sid: "full")
    assert tap.session_journal.Journal().stage("a-0123456789") is None
    assert [g.session_id for g in tap.reconcile.find_gaps()] == ["b-0123456789"]


def test_a_gap_opened_while_a_settle_runs_is_skipped_by_it(clean_unsettled, monkeypatch):
    """Off, on (the settle starts with the gaps it had), off again before it
    ends: the lines from the new gap on are sent as nothing by that settle too."""
    lines = [b"on-1\n", b"off-1\n", b"on-2\n", b"off-again\n"]
    tap = _fake_tap(lines)
    gate.install(tap)
    monkeypatch.setattr(gate, "_read_switch", lambda sid: None)
    first = [[len(lines[0]), len(lines[0]) + len(lines[1])]]
    gate.unsettled("a-0123456789", first)
    with gate._catchup("a-0123456789", first):
        again = sum(len(line) for line in lines[:3])
        gate.unsettled("a-0123456789", first + [[again, None]])
        settled = tap.session_journal.Journal().stage("a-0123456789")
    assert settled == ["on-1", "on-2"]


def test_prune_keeps_the_files_of_a_session_whose_gap_file_holds_a_gap(tmp_path, monkeypatch):
    from probe.sdk import session_marker

    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    sessions = session_marker.sessions_dir()
    sessions.mkdir(parents=True)
    transcript = tmp_path / "t.jsonl"
    transcript.write_text("{}\n")
    for sid, gaps, named in (("kept-0123456789", [[0, None]], transcript), ("gone-0123456789", [[0, 5]], tmp_path / "x"),
                             ("plain-0123456789", None, None)):
        (sessions / f"{sid}.state").write_text("off\n")
        if gaps is not None:
            gate.write_gap_file(sessions, sid, gaps, named)
    old = 1_000_000_000
    for entry in sessions.iterdir():
        os.utime(entry, (old, old))
    session_marker.prune()
    left = sorted(p.name for p in sessions.iterdir())
    assert left == ["kept-0123456789.gaps", "kept-0123456789.state"]


def test_prune_keeps_only_the_gap_file_and_state_of_a_kept_session_and_drops_finished_gap_files(tmp_path, monkeypatch):
    """A kept session keeps its gap file and `.state`; its other files age out
    as any session's do. A gap file whose transcript is gone goes at once,
    however new; one naming no transcript (or not readable) goes after 90 days."""
    import time as _time

    from probe.sdk import session_marker

    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    sessions = session_marker.sessions_dir()
    sessions.mkdir(parents=True)
    transcript = tmp_path / "t.jsonl"
    transcript.write_text("{}\n")
    gate.write_gap_file(sessions, "kept-0123456789", [[0, None]], transcript)
    for name in ("kept-0123456789.state", "kept-0123456789.tracking", "kept-0123456789.title"):
        (sessions / name).write_text("x\n")
    gate.write_gap_file(sessions, "done-0123456789", [[0, 5]], tmp_path / "gone.jsonl")
    gate.write_gap_file(sessions, "young-0123456789", [[0, None]], None)
    (sessions / "young-0123456789.state").write_text("off\n")
    gate.write_gap_file(sessions, "aged-0123456789", [[0, None]], None)
    (sessions / "aged-0123456789.state").write_text("off\n")
    (sessions / "unread-0123456789.gaps").write_text("{trunc")
    old = 1_000_000_000
    for entry in sessions.iterdir():
        if not entry.name.startswith(("done-", "young-", "unread-")):
            os.utime(entry, (old, old))  # 30 days and 90 days past
    month = _time.time() - 40 * 86400  # past the 30 days, inside the 90
    os.utime(sessions / "young-0123456789.gaps", (month, month))
    os.utime(sessions / "young-0123456789.state", (month, month))

    session_marker.prune()

    assert sorted(p.name for p in sessions.iterdir()) == [
        "kept-0123456789.gaps", "kept-0123456789.state", "unread-0123456789.gaps",
        "young-0123456789.gaps", "young-0123456789.state",
    ]


def test_removing_a_gap_file_that_is_not_there_is_no_failure(tmp_path):
    assert gate.write_gap_file(tmp_path / "sessions", "s-0123456789", []) is True


@pytest.mark.parametrize("body", [
    '{"v": 1, "gaps": [[0, ', "not json", "null", '{"v": 2, "gaps": [[0, 5]]}', '{"v": 1, "gaps": "all"}',
    '{"v": 1, "gaps": [["a", "b"]]}', '{"v": 1, "gaps": [[0, 5], [9]]}', '{"v": 1}',
], ids=["truncated", "not-json", "null", "other-version", "gaps-not-a-list", "gaps-unreadable", "one-gap-unreadable",
        "no-gaps"])
def test_a_gap_file_that_does_not_read_covers_the_whole_session(body, tmp_path, monkeypatch, clean_unsettled):
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    sessions = gate.sessions_dir_for(os.environ)
    sessions.mkdir(parents=True)
    (sessions / "s-0123456789.gaps").write_text(body)
    assert gate.read_gap_file(sessions, "s-0123456789") == [[0, None]]
    monkeypatch.setattr(gate, "_read_switch", lambda sid: "full")
    assert gate.blocked("s-0123456789") is True


def test_an_empty_gap_file_holds_no_gaps(tmp_path):
    (tmp_path / "s-0123456789.gaps").write_text('{"v": 1, "gaps": []}')
    assert gate.read_gap_file(tmp_path, "s-0123456789") == []


def test_a_session_recorded_here_goes_by_its_record_not_a_gap_file_left_behind(tmp_path, monkeypatch, clean_unsettled):
    """A removal that failed leaves its gap file: the session's own recorder
    (its record settled) is not shut out by it; any other process is."""
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    gate.write_gap_file(gate.sessions_dir_for(os.environ), "s-0123456789", [[0, 9]], None)
    monkeypatch.setattr(gate, "_read_switch", lambda sid: "full")
    gate.live("s-0123456789", True)
    try:
        assert gate.blocked("s-0123456789") is False
    finally:
        gate.live("s-0123456789", False)
    assert gate.blocked("s-0123456789") is True


def test_a_mark_that_cannot_be_read_is_none_not_the_first_byte(tmp_path):
    def unreadable(path, size):
        raise OSError("EIO")

    tap = types.SimpleNamespace(session_journal=types.SimpleNamespace(complete_line_end=unreadable))
    there = tmp_path / "t.jsonl"
    there.write_text("{}\n")
    assert gate.mark_now(tap, there) is None
    assert gate.mark_now(tap, tmp_path / "not-yet.jsonl") == 0  # no transcript yet: all of it is after
    assert gate.mark_now(tap, None) == 0


# -- the recorder host's gate -----------------------------------------------------------------


SID = "s-0123456789"


class _Controls:
    def __init__(self):
        self.stop, self.pause = threading.Event(), threading.Event()


def _host(tmp_path, monkeypatch, *, switch: dict, mark=lambda path, size: size):
    from probe.service import recorders

    host = recorders.RecorderHost(log=lambda m: None, loop_getter=lambda: None)
    host.gated = True
    host._tapns = types.SimpleNamespace(session_journal=types.SimpleNamespace(complete_line_end=mark))
    monkeypatch.setattr(host, "_save", lambda: None)
    monkeypatch.setattr(gate, "switch", lambda params: switch["now"])
    transcript = tmp_path / "t.jsonl"
    transcript.write_text("line-1\nline-2\n")
    rec = _recording(tmp_path, transcript)
    host.recordings[SID] = rec
    return host, rec


def _recording(tmp_path, transcript):
    from probe.service import recorders

    rec = recorders.Recording(SID, {"sid": SID, "state_dir": str(tmp_path / "state"), "env": {}}, _Controls())
    rec.transcript = transcript
    return rec


def _gap_file(tmp_path) -> Path:
    return tmp_path / "state" / "sessions" / f"{SID}.gaps"


def test_a_gap_whose_end_cannot_be_read_stays_open_until_it_can(tmp_path, monkeypatch, clean_unsettled):
    """Switched on while the transcript cannot be read: closing the gap at 0
    (or its start) would send the whole stretch. It stays open (held) and the
    next look closes it where the transcript is."""
    readable = {"now": False}

    def mark(path, size):
        if not readable["now"]:
            raise OSError("EIO")
        return size

    switch = {"now": "full"}
    host, rec = _host(tmp_path, monkeypatch, switch=switch, mark=mark)
    rec.params[gate.GAPS_KEY] = [[3, None]]
    assert host._gate(rec) is False
    assert gate.gaps_of(rec.params) == [[3, None]]
    readable["now"] = True
    host._gate(rec)
    assert gate.gaps_of(rec.params) == [[3, rec.transcript.stat().st_size]]
    # Opening on a mark that does not read starts at 0: nothing after it goes.
    readable["now"] = False
    switch["now"] = "off"
    rec.params[gate.GAPS_KEY] = []
    host._gate(rec)
    assert gate.gaps_of(rec.params) == [[0, None]]


def test_a_gap_file_left_behind_by_a_failed_removal_is_removed_at_the_next_look(tmp_path, monkeypatch,
                                                                                clean_unsettled):
    """Its record took the file in, then settled every gap; the removal
    failed. The next look removes it."""
    host, rec = _host(tmp_path, monkeypatch, switch={"now": "full"})
    rec.file_merged = True
    rec.settled_gaps.add((0, 7))
    gate.write_gap_file(_gap_file(tmp_path).parent, SID, [[0, 7]], None)
    host._gate(rec)
    assert not _gap_file(tmp_path).exists()


def test_the_gap_file_is_written_off_the_shared_lock_and_never_on_the_loop(tmp_path, monkeypatch, clean_unsettled):
    """Every session's gate and the service's loop take `_gate_lock`: a gap
    file's fsync under it stalls them all. An RPC's look (`on_loop`) leaves the
    write to the recorder thread or the monitor."""
    host, rec = _host(tmp_path, monkeypatch, switch={"now": "off"})
    writes = []
    real = gate.write_gap_file

    def write(*args, **kwargs):
        writes.append(host._gate_lock.locked())
        return real(*args, **kwargs)

    monkeypatch.setattr(gate, "write_gap_file", write)
    assert host._gate(rec, on_loop=True) is True
    assert writes == [] and rec.gap_file_due
    with gate._LOCK:
        assert gate._UNSETTLED[SID] == [[rec.transcript.stat().st_size, None]]  # the drains hold off at once
    host._gate(rec)
    assert writes == [False]
    assert gate.read_gap_file(_gap_file(tmp_path).parent, SID) == [[rec.transcript.stat().st_size, None]]


def test_a_recording_a_resume_replaced_touches_nothing_of_the_session(tmp_path, monkeypatch, clean_unsettled):
    """Ended while off and not finished (the server down), then resumed: the
    resume's fresh recording carries the gaps on. The old one never closes its
    stale gap, never settles or finalizes, never lifts the session's gaps."""
    switch = {"now": "full"}
    host, old = _host(tmp_path, monkeypatch, switch=switch)
    old.params[gate.GAPS_KEY] = [[3, None]]
    new = _recording(tmp_path, old.transcript)
    new.params[gate.GAPS_KEY] = [[3, 7]]
    host.recordings[SID] = new
    gate.unsettled(SID, [[3, 7]])
    gate.write_gap_file(_gap_file(tmp_path).parent, SID, [[3, 7]], None)
    monkeypatch.setattr(gate, "settle", lambda *a, **k: pytest.fail("a replaced recording settled"))
    monkeypatch.setattr(gate, "write_marker", lambda *a, **k: pytest.fail("a replaced recording wrote the marker"))

    with old.transcript.open("a") as handle:
        handle.write("on-after-resume-1\n")
    assert host._gate(old) is False
    host._settled(old, [[3, None]], everything=True)
    old.controls.stop.set()
    from probe.service import recorders

    assert host._hold(old) == recorders.ENDED_STEP
    assert gate.gaps_of(old.params) == [[3, None]]
    with gate._LOCK:
        assert gate._UNSETTLED[SID] == [[3, 7]]
    assert gate.read_gap_file(_gap_file(tmp_path).parent, SID) == [[3, 7]]


# -- settling: refused for good, replaced ----------------------------------------------------


class _Refusal(RuntimeError):
    def __init__(self, message, *, retryable=False):
        super().__init__(message)
        self.retryable = retryable


class _Wire:
    """The tap's `Wire` as the gate sees it: every answer through `_request`."""

    def __init__(self, receipts=None, answer=None):
        self.base_url, self.source = "http://x", "claude_code"
        self._receipts, self.answer = receipts, answer

    def _request(self, path, body=None):
        return self.answer

    def receipts(self, sid):
        if self._receipts is not None:
            return self._receipts(sid)
        code, body = self._request(f"/ingest/v1/sessions/claude_code/{sid}/receipts")
        if code != 200 or body.get("protocol_version") not in (2, 3):
            raise _Refusal(f"stream receipts unavailable (http {code}); nothing newly staged",
                           retryable=code in (408, 429) or 500 <= code < 600)
        return body


class _TokenFile:
    def __init__(self, there=False, readable=True):
        self.there, self.readable = there, readable

    def is_file(self):
        return self.there

    def read_text(self, encoding=None):
        if not self.readable:
            raise PermissionError(13, "denied")
        return "token\n"


def _settle_tap(*, token="t", receipts=None, journal=None, answer=None, token_file=None):
    import contextlib as _contextlib

    sj = types.SimpleNamespace(
        DeliveryPending=_Refusal, ReconciliationRequired=type("RR", (RuntimeError,), {"status_code": None}),
        SessionDeleted=type("SD", (Exception,), {}), ProtocolRestarted=type("PR", (Exception,), {}),
        Wire=lambda *a: _Wire(receipts, answer),
        Journal=lambda *a, **k: journal,
    )
    cfg = types.SimpleNamespace(killswitch_active=lambda: False, cwd_disabled=lambda p: False,
                                load_token=lambda: token, api_base_url=lambda: "http://x",
                                capture_source=lambda: "claude_code", pasted_images_on=lambda: False,
                                token_file=lambda: token_file or _TokenFile())
    env = types.SimpleNamespace(session=lambda e: _contextlib.nullcontext())
    return types.SimpleNamespace(session_journal=sj, config=cfg, threadenv=types.SimpleNamespace(install=lambda: env))


def _settle_params(tmp_path):
    transcript = tmp_path / "t.jsonl"
    transcript.write_text("line-1\n")
    return {"sid": SID, "cwd": str(tmp_path), "env": {}, "transcript": str(transcript)}


@pytest.mark.parametrize("code, body, expected", [
    (401, {"detail": "device not paired"}, gate.REFUSED),
    (403, {"detail": "receipt source does not match the paired device"}, gate.REFUSED),
    (404, {"detail": "Not Found"}, gate.REFUSED),
    (422, {"detail": [{"loc": ["body"], "msg": "invalid"}]}, gate.REFUSED),
    # Not the Probe gateway's own refusal, or not for good: tried again.
    (403, {"detail": "invalid error response"}, gate.RETRY),  # a proxy's page
    (407, {"detail": "invalid error response"}, gate.RETRY),
    (413, {"detail": "too large"}, gate.RETRY),
    (400, {"detail": "bad request"}, gate.RETRY),
    (403, {"error": "forbidden"}, gate.RETRY),  # JSON, but not the gateway's shape
    (200, {"protocol_version": 9}, gate.RETRY),  # a protocol this tap does not know
    (0, {"detail": "timed out"}, gate.RETRY),
    (503, {"detail": "busy"}, gate.RETRY),
], ids=["401", "403", "404", "422", "proxy-403", "407", "413", "400", "json-403", "unknown-protocol", "no-answer", "503"])
def test_only_the_probe_gateways_own_refusal_is_for_good(code, body, expected, tmp_path):
    log = []
    done = gate.settle(_settle_tap(answer=(code, body)), _settle_params(tmp_path), [[2, None]], finalize=True,
                       log=log.append)
    assert done == expected


def test_no_login_is_refused_for_good_but_a_token_that_cannot_be_read_now_is_not(tmp_path):
    params, gaps = _settle_params(tmp_path), [[2, None]]
    assert gate.settle(_settle_tap(token=None), params, gaps, finalize=True, log=lambda m: None) == gate.REFUSED
    unreadable = _TokenFile(there=True, readable=False)
    assert gate.settle(_settle_tap(token=None, token_file=unreadable), params, gaps, finalize=True,
                       log=lambda m: None) == gate.RETRY


def test_a_local_error_after_a_good_answer_is_tried_again(tmp_path):
    """The tap's own refusals (a batch over its budget) come after the server
    answered 2xx: never for good."""
    def receipts(sid):
        raise _Refusal("sanitized event exceeds the gateway batch budget", retryable=False)

    tap = _settle_tap(receipts=receipts, answer=(202, {"status": "accepted"}))
    assert gate.settle(tap, _settle_params(tmp_path), [[2, None]], finalize=True, log=lambda m: None) == gate.RETRY


def test_a_settle_a_newer_recording_took_over_from_leaves_the_row_unfinalized(tmp_path):
    """A resume replaced the ended recording while its settle ran: it stops
    before its next batch, and the FINALIZE it asked for is taken back, so the
    live resumed session's loop never sends one."""
    calls = []

    class Journal:
        def claim_live(self, sid):
            return True

        def get(self, sid):
            return {"source_byte_end": 0}

        def ensure(self, *a, **k):
            calls.append("ensure")

        def update(self, sid, **fields):
            calls.append(fields)

        def stage(self, *a, **k):
            pytest.fail("staged after it was replaced")

        def pending(self, sid):
            return None

        def release_live(self, sid):
            calls.append("released")

        def close(self):
            pass

    answers = iter([True, False])
    tap = _settle_tap(receipts=lambda sid: {"customer_id": "c", "stream": {"last_seq": 0}}, journal=Journal())
    done = gate.settle(tap, _settle_params(tmp_path), [[2, None]], finalize=True, log=lambda m: None,
                       current=lambda: next(answers))
    assert done == gate.RETRY
    assert calls == ["ensure", {"finalize_requested": True}, {"finalize_requested": False}, "released"]
    tap = _settle_tap(receipts=lambda sid: {"customer_id": "c", "stream": {"last_seq": 0}}, journal=Journal())
    calls.clear()
    assert gate.settle(tap, _settle_params(tmp_path), [[2, None]], finalize=True, log=lambda m: None,
                       current=lambda: False) == gate.RETRY
    assert "ensure" not in calls


# -- round 2: reads that fail now, the first look, write failures, Codex rollouts -------------


def _failing_reads(monkeypatch, path: Path, times: int):
    """`path.read_text` raises EMFILE `times` times, then reads."""
    real = Path.read_text
    left = {"n": times}

    def read_text(self, *args, **kwargs):
        if self == path and left["n"] > 0:
            left["n"] -= 1
            raise OSError(24, "Too many open files")
        return real(self, *args, **kwargs)

    monkeypatch.setattr(Path, "read_text", read_text)


def test_a_gap_file_read_that_fails_now_is_not_remembered(tmp_path, monkeypatch):
    sessions = tmp_path / "sessions"
    gate.write_gap_file(sessions, SID, [[3, 7]], None)
    _failing_reads(monkeypatch, sessions / f"{SID}.gaps", 1)
    assert gate.read_gap_file(sessions, SID) == [[0, None]]  # closed while it cannot be read
    assert gate.read_gap_file(sessions, SID) == [[3, 7]]  # and read again, not the failure cached
    _failing_reads(monkeypatch, sessions / f"{SID}.gaps", 1)
    gate._GAP_FILES.clear()
    assert gate.read_gap_file_raw(sessions, SID) is None


def test_a_first_look_whose_gap_file_read_fails_holds_the_session_and_reads_again(tmp_path, monkeypatch,
                                                                                  clean_unsettled):
    """Never "everything is a gap" into its own record (which would send its
    unsent on-lines as nothing): held, the file deciding for the drains,
    until a look reads it."""
    host, rec = _host(tmp_path, monkeypatch, switch={"now": "full"})
    monkeypatch.setattr(gate, "_read_switch", lambda sid: "full")
    monkeypatch.setattr(gate, "sessions_dir_for", lambda env, state_dir=None: _gap_file(tmp_path).parent)
    gate.write_gap_file(_gap_file(tmp_path).parent, SID, [[3, 7]], None)
    gate._GAP_FILES.clear()
    _failing_reads(monkeypatch, _gap_file(tmp_path), 3)  # two looks' reads and a drain's
    host._gate(rec, first=True)
    assert gate.gaps_of(rec.params) == []
    assert host._needs_hold(rec) is True  # held: its loop does not run
    assert not rec.file_merged and gate.blocked(SID) is True
    assert gate.read_gap_file(_gap_file(tmp_path).parent, SID) == [[3, 7]]  # the file is untouched
    host._gate(rec)
    assert gate.gaps_of(rec.params) == [[3, 7]] and rec.file_merged


def _start_host(tmp_path, monkeypatch, *, mark):
    from probe.service import recorders

    host = recorders.RecorderHost(log=lambda m: None, loop_getter=lambda: None)
    host.gated = True
    host._tapns = types.SimpleNamespace(session_journal=types.SimpleNamespace(complete_line_end=mark))
    host.hosted = types.SimpleNamespace(Controls=_Controls)
    monkeypatch.setattr(host, "_save", lambda: None)
    monkeypatch.setattr(host, "_guard", lambda rec, delay=0.0: None)
    monkeypatch.setattr(host, "_ensure_monitor", lambda: None)
    monkeypatch.setattr(gate, "switch", lambda params: "full")
    monkeypatch.setattr(gate, "_read_switch", lambda sid: "full")
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "xdg"))
    transcript = tmp_path / "t.jsonl"
    transcript.write_text("line-1\nline-2\n")
    session = {"sid": SID, "state_dir": str(tmp_path / "state"), "env": {}, "transcript": str(transcript)}
    return host, session


def test_a_session_starting_here_is_never_open_to_the_drains_while_its_first_look_runs(tmp_path, monkeypatch,
                                                                                       clean_unsettled):
    """Its gaps are in its gap file only (`recorders.json` lost): until its
    first look has merged them, every drain here still reads that file."""
    seen = []

    def mark(path, size):
        seen.append(gate.blocked(SID))
        return size

    host, session = _start_host(tmp_path, monkeypatch, mark=mark)
    monkeypatch.setattr(gate, "sessions_dir_for", lambda env, state_dir=None: tmp_path / "state" / "sessions")
    gate.write_gap_file(tmp_path / "state" / "sessions", SID, [[0, 9]], None)
    rec = host._start(session)
    assert seen == [True]
    assert gate.gaps_of(rec.params) == [[0, 9]] and gate.blocked(SID) is True


def test_a_first_look_that_fails_never_lets_the_next_one_drop_the_gap_file(tmp_path, monkeypatch, clean_unsettled):
    calls = {"n": 0}

    def mark(path, size):
        calls["n"] += 1
        if calls["n"] == 1:
            raise RuntimeError("the first look fails")
        return size

    host, session = _start_host(tmp_path, monkeypatch, mark=mark)
    monkeypatch.setattr(gate, "sessions_dir_for", lambda env, state_dir=None: tmp_path / "state" / "sessions")
    gate.write_gap_file(tmp_path / "state" / "sessions", SID, [[0, 9]], None)
    rec = host._start(session)
    host._flush_gap_file(rec)
    assert gate.read_gap_file(tmp_path / "state" / "sessions", SID) == [[0, 9]]
    host._gate(rec)
    assert gate.gaps_of(rec.params) == [[0, 9]]
    assert gate.read_gap_file(tmp_path / "state" / "sessions", SID) == [[0, 9]]


def test_a_gap_file_that_cannot_be_written_is_said_once_and_once_it_can_again(tmp_path, monkeypatch,
                                                                              clean_unsettled):
    from probe.service import recorders

    lines = []
    host, rec = _host(tmp_path, monkeypatch, switch={"now": "off"})
    host.log = lines.append
    writes = {"ok": False, "n": 0}
    real = gate.write_gap_file

    def write(*args, **kwargs):
        writes["n"] += 1
        return real(*args, **kwargs) if writes["ok"] else False

    monkeypatch.setattr(gate, "write_gap_file", write)
    for _ in range(5):
        host._gate(rec)
    assert writes["n"] == 5  # one try per look
    writes["ok"] = True
    host._gate(rec)
    host._gate(rec)
    said = [line for line in lines if "gap file" in line]
    assert len(said) == 2 and "could not be written" in said[0] and "written again" in said[1]
    assert recorders.RecorderHost._watch_switches.__code__.co_names.count("_flush_gap_file") == 0


def test_a_codex_rollout_that_could_not_be_looked_for_never_closes_a_gap_at_zero(tmp_path, monkeypatch,
                                                                                 clean_unsettled):
    """Off from its first look, its rollout never looked for; switched on
    while its sessions folder is not there (or the look fails): the gap stays
    open (it is held) until it can be found, never `[[0, 0]]`."""
    host, rec = _host(tmp_path, monkeypatch, switch={"now": "full"})
    folder = tmp_path / "codex-sessions"
    rec.params.update({"transcript": None, "transcript_dir": str(folder), gate.GAPS_KEY: [[0, None]]})
    rec.transcript = None
    rec.file_merged = True
    rollout = folder / "2026" / "10" / "24" / f"rollout-{SID}.jsonl"
    host._tapns.main = types.SimpleNamespace(
        _resolve_codex_transcript=lambda d, sid: next(iter(sorted(d.rglob(f"*{sid}.jsonl"))), None))
    host._gate(rec)
    assert gate.gaps_of(rec.params) == [[0, None]]
    assert gate.find_transcript(host._tapns, rec.params) == (None, False)
    rollout.parent.mkdir(parents=True)
    assert gate.find_transcript(host._tapns, rec.params) == (None, True)  # the folder, no rollout yet
    rollout.write_text("line-1\n")

    def broken(d, sid):
        raise OSError("the look failed")

    host._tapns.main._resolve_codex_transcript, working = broken, host._tapns.main._resolve_codex_transcript
    host._gate(rec)
    assert gate.gaps_of(rec.params) == [[0, None]]
    host._tapns.main._resolve_codex_transcript = working
    host._gate(rec)
    assert gate.gaps_of(rec.params) == [[0, rollout.stat().st_size]]


def test_a_settle_whose_rollout_could_not_be_looked_for_settles_nothing(tmp_path):
    class Journal:
        def claim_live(self, sid):
            return True

        def get(self, sid):
            return None

        def release_live(self, sid):
            pass

        def close(self):
            pass

    params = {"sid": SID, "cwd": str(tmp_path), "env": {}, "transcript": None,
              "transcript_dir": str(tmp_path / "not-there")}
    tap = _settle_tap(receipts=lambda sid: {"customer_id": "c"}, journal=Journal())
    tap.main = types.SimpleNamespace(_resolve_codex_transcript=lambda d, sid: None)
    assert gate.settle(tap, params, [[0, 40]], finalize=False, log=lambda m: None) == gate.RETRY
    (tmp_path / "not-there").mkdir()
    assert gate.settle(tap, params, [[0, 0]], finalize=False, log=lambda m: None) == gate.DONE


# -- tap 0.10.19: the tap's own gate, and a `tap watch` writing the gap file too ----------


def test_a_tap_that_gates_its_own_drains_is_not_wrapped_and_gets_this_process_gaps(clean_unsettled):
    """From tap 0.10.19 the tap reads the switch and the gap file in its own
    drains (`tap/capture_gate.py`): the service wraps none of them and hands
    the tap its in-memory gaps instead (`host`), a moment ahead of the file."""
    tap = _fake_tap([b"one\n"])
    hosts: list = []
    tap.capture_gate = types.SimpleNamespace(NATIVE=1, host=hosts.append)
    stage, find_gaps = tap.session_journal.Journal.stage, tap.reconcile.find_gaps
    assert gate.install(tap) is True
    assert gate.native(tap) is tap.capture_gate
    assert tap.session_journal.Journal.stage is stage and tap.reconcile.find_gaps is find_gaps
    assert not getattr(tap.session_journal, "_probe_capture_gate", False)
    [gaps_of] = hosts
    gate.unsettled("a-0123456789", [[0, 5]])
    assert gaps_of("a-0123456789") == [[0, 5]] and gaps_of("b-0123456789") == []


def test_an_older_tap_is_still_wrapped(clean_unsettled):
    """Taps 0.10.0-0.10.18 have no gate of their own: wrapped as before."""
    tap = _fake_tap([b"one\n"])
    tap.capture_gate = None
    stage = tap.session_journal.Journal.stage
    assert gate.native(tap) is None
    assert gate.install(tap) is True
    assert tap.session_journal.Journal.stage is not stage
    assert tap.session_journal._probe_capture_gate is True


def test_the_in_tree_tap_gates_its_own_drains():
    code = ("import sys; sys.path.insert(0, sys.argv[1]); from tap import capture_gate as g, session_journal as sj;"
            "assert g.NATIVE >= 1; assert all(callable(getattr(g, n)) for n in ('verdict', 'settling', 'host',"
            " 'record_off', 'record_on', 'locked', 'Recorder'));"
            "assert sj.capture_gate is g; print('ok')")
    done = subprocess.run([sys.executable, "-I", "-c", code, str(TAP_ROOT)], capture_output=True, text=True, timeout=60)
    assert done.returncode == 0 and done.stdout.strip() == "ok", done.stderr[-2000:]


def test_a_gap_a_tap_watch_wrote_after_the_first_look_is_merged_never_written_over(tmp_path, monkeypatch,
                                                                                   clean_unsettled):
    """A `tap watch` of the session (tap 0.10.19) records its own off stretch in
    the gap file while the service also records the session (a hand-over): the
    service's next write keeps it, and its record takes it in."""
    host, rec = _host(tmp_path, monkeypatch, switch={"now": "full"})
    sessions = _gap_file(tmp_path).parent
    host._gate(rec, first=True)
    assert rec.file_merged and not _gap_file(tmp_path).exists()
    assert gate.write_gap_file(sessions, SID, [[0, 7]], None)  # the watch's write (same format)
    host._gate(rec)  # its next look writes the file (its gap file is "behind" it): the watch's gap stays
    assert gate.read_gap_file(sessions, SID) == [[0, 7]]
    assert gate.gaps_of(rec.params) == [[0, 7]]
    with gate._LOCK:
        assert gate._UNSETTLED[SID] == [[0, 7]]  # the drains here hold off its lines too
    host._ask_hold = lambda r: None
    monkeypatch.setattr(gate, "switch", lambda params: "off")
    host._gate(rec)
    assert gate.read_gap_file(sessions, SID) == [[0, 7], [rec.transcript.stat().st_size, None]]


def test_the_service_waits_for_a_watchs_write_in_progress_and_keeps_both(tmp_path, monkeypatch, clean_unsettled):
    """Every writer takes the session's lock for its read-modify-write: the
    service's flush waits while a watch writes, then merges what it wrote."""
    from probe.tap_core import capture_gate as tap_gate

    host, rec = _host(tmp_path, monkeypatch, switch={"now": "full"})
    sessions = _gap_file(tmp_path).parent
    host._gate(rec, first=True)
    switch = {"now": "off"}
    monkeypatch.setattr(gate, "switch", lambda params: switch["now"])
    done = threading.Event()
    with tap_gate.locked(SID, sessions):
        thread = threading.Thread(target=lambda: (host._gate(rec), done.set()))
        thread.start()
        assert not done.wait(0.5)  # its gap file write waits for the lock
        assert tap_gate.write_gaps(SID, [[0, 3]], None, sessions)
    thread.join(10)
    assert done.is_set()
    size = rec.transcript.stat().st_size
    assert gate.read_gap_file(sessions, SID) == [[0, 3], [size, None]]
    assert gate.gaps_of(rec.params) == [[0, 3], [size, None]]


def test_a_gap_the_service_settled_is_never_taken_back_from_a_watchs_older_write(tmp_path, monkeypatch,
                                                                                clean_unsettled):
    from probe.tap_core import capture_gate as tap_gate

    host, rec = _host(tmp_path, monkeypatch, switch={"now": "full"})
    sessions = _gap_file(tmp_path).parent
    host._gate(rec, first=True)
    with host._gate_lock:
        host._keep_gaps(rec, [[0, 7]])
    host._flush_gap_file(rec)
    host._settled(rec, [[0, 7]])
    assert not _gap_file(tmp_path).exists()
    with tap_gate.locked(SID, sessions):  # a watch's write that still held it
        assert tap_gate.write_gaps(SID, [[0, 7], [20, 30]], None, sessions)
    host._gate(rec)
    assert gate.gaps_of(rec.params) == [[20, 30]]
    assert gate.read_gap_file(sessions, SID) == [[20, 30]]
