"""Capy capture: Capy's API -> local mirror files -> the shared upload journal.

The chain under test, end to end with real HTTP on loopback:
  `capy_fake_api.FakeCapy` (Capy's documented read routes and shapes)
  -> `capy_discovery.pull` (author filter, pages, subagents, append-only mirror)
  -> `capy_cli.upload` (live journal semantics, finalize, resume)
  -> `DoorWire` (the engine's receipts door, from test_transcript_protocol3).
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

from capy_fake_api import ME, TEAMMATE, FakeCapy, message, thread
from probe.cli import capy_cli
from probe.cli import capy_discovery as discovery
from probe.tap_core import atif_fragment, capy_sanitize
from probe.tap_core.session_identity import validate_identity
from probe.tap_core.session_journal import ReconciliationRequired
from test_transcript_protocol3 import DoorWire

AGENT = Path(__file__).resolve().parents[1]
VALIDATOR = Draft202012Validator(
    json.loads((AGENT / "src/probe/tap_core/probe-events-1.schema.json").read_text())
)
NOW = 1_791_800_000.0  # 2026-10-12T...: after every fake timestamp, within a day of most


def _api(fake: FakeCapy) -> discovery.CapyAPI:
    return discovery.CapyAPI(fake.key, base=fake.base, sleep=lambda _s: None)


def _lines(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_bytes().splitlines()]


@pytest.fixture
def home(tmp_path, monkeypatch):
    monkeypatch.setenv("HOME", str(tmp_path))
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    monkeypatch.setenv("PROBE_TRANSCRIPT_STATE_DIR", str(tmp_path / "journal"))
    monkeypatch.setenv("PROBE_CAPY_THREADS_DIR", str(tmp_path / "threads"))
    monkeypatch.setenv("PROBE_CAPY_TAP_PLUGIN_DIR", str(tmp_path / "capy-state"))
    monkeypatch.delenv(discovery.ENV_API_BASE, raising=False)
    monkeypatch.delenv(capy_cli.ENV_API_KEY, raising=False)
    monkeypatch.delenv("PROBE_CAPY_TAP_TOKEN", raising=False)
    return tmp_path


def _seed(fake: FakeCapy) -> None:
    fake.add_thread(
        thread("jam_mine"),
        [
            message("m1", "user", "train the baseline with lr 3e-4"),
            message("m2", "tool", "Running the training script\nsecond line never ships", tool="bash"),
            message("m3", "assistant", "Loss went from 2.3 to 1.1.", model="claude-x"),
        ],
    )
    fake.add_thread(thread("jam_theirs", author=TEAMMATE), [message("t1", "user", "not mine")])


# --- the sanitizer ---------------------------------------------------------------


def test_every_mirror_line_becomes_a_schema_valid_event():
    header = discovery.header_record(session_id=discovery.session_id_for(discovery.THREAD, "jam_x"), thread=thread("jam_x"))
    lines = [
        header,
        discovery.message_record(message("a", "user", "hello")),
        discovery.message_record(message("b", "assistant", "hi", model="m")),
        discovery.message_record(message("c", "tool", "Reading train.py", tool="read")),
        discovery.message_record(message("d", "user", "fixed prompt", editOf="a" * 26)),
        discovery.message_record(
            message("e", "user", "see plot", attachments=[
                {"file": {"fileId": "f1", "name": "loss.png", "mediaType": "image/png", "sizeBytes": 2048,
                          "sourcePath": "/home/secret/loss.png"}},
                {"file": {"fileId": "f2", "name": "notes.pdf", "mediaType": "application/pdf",
                          "sizeBytes": "Infinity"}},
            ])
        ),
        {"type": "capy_message", "id": "f", "source": "robot", "text": "x"},
        {"type": "something_new"},
        "not an object",
    ]
    for raw in lines:
        event = capy_sanitize.sanitize_event(raw)
        errors = list(VALIDATOR.iter_errors(event))
        assert not errors, (raw, event, errors)
        # The ATIF fragment builder (protocol 3) maps every event without error.
        built = atif_fragment.fragment({"line_no": 0, "raw": event})
        assert "error" not in built and "line_error" not in built, (event, built)


def test_the_translation_keeps_words_summaries_and_never_tool_output():
    tool = capy_sanitize.sanitize_event(
        discovery.message_record(message("c", "tool", "Running tests\nFAILED secret output", tool="bash"))
    )
    block = tool["message"]["content"][0]
    assert block == {"type": "tool_use", "id": "c", "name": "bash", "summary": "Running tests"}
    reply = capy_sanitize.sanitize_event(discovery.message_record(message("b", "assistant", "done", model="m")))
    assert reply["inference_id"] == "b" and reply["message"]["model"] == "m"
    edit = capy_sanitize.sanitize_event(discovery.message_record(message("d", "user", "v2", editOf="x" * 26)))
    assert edit["message"]["content"][0]["text"] == capy_sanitize.EDIT_LABEL + "v2"


def test_attachments_keep_name_type_and_size_only():
    record = discovery.message_record(
        message("e", "user", "", attachments=[
            {"file": {"fileId": "f1", "name": "loss.png", "mediaType": "image/png", "sizeBytes": 2048,
                      "sourcePath": "/home/secret/loss.png", "contentSha": "abc"}},
        ])
    )
    assert record["attachments"] == [{"media_type": "image/png", "name": "loss.png", "size_bytes": 2048}]
    event = capy_sanitize.sanitize_event(record)
    assert event["message"]["content"] == [{"type": "image", "mimeType": "image/png", "bytes": 2048}]


# --- identity ----------------------------------------------------------------------


def test_identity_reads_the_mirror_header(tmp_path):
    sid = discovery.session_id_for(discovery.THREAD, "jam_x")
    path = tmp_path / f"{sid}.jsonl"
    discovery.append_lines(path, [discovery.canonical_line(
        discovery.header_record(session_id=sid, thread=thread("jam_x"))
    )])
    proof = validate_identity(path, "capy", sid)
    assert proof["native_session_id"] == sid
    assert proof["source_cwd"] == "/capy/projects/proj_1"
    with pytest.raises(ReconciliationRequired):
        validate_identity(path, "capy", discovery.session_id_for(discovery.THREAD, "jam_other"))


# --- pulling ---------------------------------------------------------------------


def test_pull_mirrors_only_my_threads_across_pages(home):
    with FakeCapy() as fake:
        _seed(fake)
        state: dict = {}
        result = discovery.pull(_api(fake), root=home / "threads", me=ME, projects=["proj_1"], state=state, now=NOW)
    assert result.threads_seen == 2 and result.threads_mine == 1
    [session] = result.sessions
    assert session.session_id == discovery.session_id_for(discovery.THREAD, "jam_mine")
    records = _lines(session.path)
    assert records[0]["type"] == "capy_session" and records[0]["thread_id"] == "jam_mine"
    assert [r["id"] for r in records[1:]] == ["m1", "m2", "m3"]
    assert not any(p for p in fake.requests if "jam_theirs/messages" in p), "a teammate's thread was read"


def test_a_second_pull_appends_only_new_messages_and_skips_quiet_threads(home):
    with FakeCapy() as fake:
        _seed(fake)
        api, state = _api(fake), {}
        first = discovery.pull(api, root=home / "threads", me=ME, projects=["proj_1"], state=state, now=NOW)
        before = first.sessions[0].path.read_bytes()
        reads = len(fake.requests)
        discovery.pull(api, root=home / "threads", me=ME, projects=["proj_1"], state=state, now=NOW)
        assert [p for p in fake.requests[reads:] if "/messages" in p] == [], "an unchanged thread was re-read"
        fake.messages["jam_mine"].append(message("m4", "user", "now evaluate"))
        fake.threads["proj_1"][0]["lastActivityAt"] = "2026-10-12T11:00:00Z"
        third = discovery.pull(api, root=home / "threads", me=ME, projects=["proj_1"], state=state, now=NOW)
    after = third.sessions[0].path.read_bytes()
    assert after.startswith(before), "bytes already written changed"
    assert [r["id"] for r in _lines(third.sessions[0].path)[1:]] == ["m1", "m2", "m3", "m4"]


def test_a_mirror_rebuilt_from_scratch_is_byte_identical(home):
    with FakeCapy() as fake:
        _seed(fake)
        api = _api(fake)
        one = discovery.pull(api, root=home / "a", me=ME, projects=["proj_1"], state={}, now=NOW)
        fake.threads["proj_1"][0]["title"] = "Renamed later"
        fake.users[0]["firstName"] = "Renamed"
        two = discovery.pull(api, root=home / "b", me=ME, projects=["proj_1"], state={}, now=NOW)
    assert one.sessions[0].path.read_bytes() == two.sessions[0].path.read_bytes()


def test_subagents_get_their_own_session_files(home):
    with FakeCapy() as fake:
        _seed(fake)
        fake.add_subagent("jam_mine", "sub_1", [message("s1", "assistant", "split by directory")], status="done")
        result = discovery.pull(_api(fake), root=home / "threads", me=ME, projects=["proj_1"], state={}, now=NOW)
    by_id = {s.session_id: s for s in result.sessions}
    sub = by_id[discovery.session_id_for(discovery.SUBAGENT, "sub_1")]
    header = _lines(sub.path)[0]
    assert header["subagent_id"] == "sub_1" and header["thread_id"] == "jam_mine"
    assert sub.finished, "a done subagent's session is over"
    assert not by_id[discovery.session_id_for(discovery.THREAD, "jam_mine")].finished


def test_a_torn_tail_is_cut_back_before_appending(home):
    with FakeCapy() as fake:
        _seed(fake)
        api, state = _api(fake), {}
        first = discovery.pull(api, root=home / "threads", me=ME, projects=["proj_1"], state=state, now=NOW)
        path = first.sessions[0].path
        good = path.read_bytes()
        with path.open("ab") as handle:
            handle.write(b'{"type":"capy_message","id":"m4","sour')  # a crash mid-write
        fake.messages["jam_mine"].append(message("m4", "user", "again"))
        fake.threads["proj_1"][0]["lastActivityAt"] = "2026-10-12T12:00:00Z"
        discovery.pull(api, root=home / "threads", me=ME, projects=["proj_1"], state=state, now=NOW)
    data = path.read_bytes()
    assert data.startswith(good) and data.endswith(b"\n")
    assert [r["id"] for r in _lines(path)[1:]] == ["m1", "m2", "m3", "m4"]


def test_archived_or_day_quiet_threads_are_finished(home):
    with FakeCapy() as fake:
        fake.add_thread(thread("jam_old", activity="2026-10-01T00:00:00Z"), [message("o1", "user", "x")])
        fake.add_thread(thread("jam_arch", archived=True), [message("a1", "user", "y")])
        fake.add_thread(thread("jam_live"), [message("l1", "user", "z")])
        result = discovery.pull(_api(fake), root=home / "threads", me=ME, projects=["proj_1"], state={}, now=NOW)
    finished = {s.session_id: s.finished for s in result.sessions}
    assert finished[discovery.session_id_for(discovery.THREAD, "jam_old")]
    assert finished[discovery.session_id_for(discovery.THREAD, "jam_arch")]
    assert not finished[discovery.session_id_for(discovery.THREAD, "jam_live")]


def test_rate_limits_are_waited_out_and_a_refused_key_stops_the_pull(home):
    with FakeCapy() as fake:
        _seed(fake)
        fake.fail["/api/v1/threads"] = [429, 429]
        waits: list[float] = []
        api = discovery.CapyAPI(fake.key, base=fake.base, sleep=waits.append)
        result = discovery.pull(api, root=home / "threads", me=ME, projects=["proj_1"], state={}, now=NOW)
        assert result.sessions and waits.count(1.0) == 2
        bad = discovery.CapyAPI("capy_wrong", base=fake.base, sleep=lambda _s: None)
        refused = discovery.pull(bad, root=home / "x", me=ME, projects=["proj_1"], state={}, now=NOW)
    assert refused.auth_failed and not refused.sessions


def test_a_whole_sync_only_ever_reads_capy(home):
    with FakeCapy() as fake:
        _seed(fake)
        fake.add_subagent("jam_mine", "sub_1", [message("s1", "assistant", "x")])
        _pull(fake, home, {})
        _api(fake).users()
        _api(fake).projects()
    assert fake.methods and set(fake.methods) == {"GET"}


# --- uploading -------------------------------------------------------------------


def _pull(fake, home, state):
    return discovery.pull(_api(fake), root=home / "threads", me=ME, projects=["proj_1"], state=state, now=NOW)


def test_sync_uploads_live_then_finalizes_when_the_thread_ends_and_reopens(home):
    door = DoorWire(source="capy")
    with FakeCapy() as fake:
        _seed(fake)
        state: dict = {}
        uploaded: dict = {}
        sid = discovery.session_id_for(discovery.THREAD, "jam_mine")
        report = capy_cli.upload(_pull(fake, home, state).sessions, token="t", base_url=door.base_url,
                                 uploaded=uploaded, wire=door)
        assert report.batches >= 1 and not report.errors
        stream = door.streams[sid]
        assert not stream["finalized"]
        assert stream["source_byte_end"] == (home / "threads" / f"{sid}.jsonl").stat().st_size

        calls = len(door.calls)
        capy_cli.upload(_pull(fake, home, state).sessions, token="t", base_url=door.base_url,
                        uploaded=uploaded, wire=door)
        assert len(door.calls) == calls, "an unchanged session was sent again"

        fake.threads["proj_1"][0]["archived"] = True
        capy_cli.upload(_pull(fake, home, state).sessions, token="t", base_url=door.base_url,
                        uploaded=uploaded, wire=door)
        assert door.streams[sid]["finalized"]

        fake.threads["proj_1"][0]["archived"] = False
        fake.threads["proj_1"][0]["lastActivityAt"] = "2026-10-12T13:00:00Z"
        fake.messages["jam_mine"].append(message("m5", "user", "one more run"))
        report = capy_cli.upload(_pull(fake, home, state).sessions, token="t", base_url=door.base_url,
                                 uploaded=uploaded, wire=door)
    assert not report.errors
    assert not door.streams[sid]["finalized"], "the reopened thread streams live again"
    sent = [json.dumps(b) for b in door.bodies(sid)]
    assert any("one more run" in b for b in sent)
    assert not any("second line never ships" in b for b in sent)
    assert not any("not mine" in b for b in sent)


def test_sync_once_end_to_end_records_its_outcome(home, monkeypatch):
    door = DoorWire(source="capy")
    from probe.cli import capabilities

    monkeypatch.setattr(capabilities, "resolved_capture_credential", lambda s=None: ("t", door.base_url))
    with FakeCapy() as fake:
        _seed(fake)
        monkeypatch.setenv(discovery.ENV_API_BASE, fake.base)
        capy_cli.save_config(capy_cli.CapyConfig(
            api_key=fake.key, me_id=ME, me_email="me@lab.example",
            projects=[{"id": "proj_1", "name": "ml-research"}],
        ))
        report = capy_cli.sync_once(wire=door, now=NOW)
    assert report.ok, (report.errors, report.upload.errors)
    assert report.pulled_sessions == 1 and report.upload.batches >= 1
    last = json.loads(capy_cli.sync_state_path().read_text())["last_sync"]
    assert last["ok"] and last["sessions"] == 1
    assert oct(capy_cli.config_path().stat().st_mode & 0o777) == "0o600"


def test_a_second_concurrent_sync_does_nothing(home, monkeypatch):
    from probe.cli import capabilities

    monkeypatch.setattr(capabilities, "resolved_capture_credential", lambda s=None: ("t", "http://x"))
    capy_cli.save_config(capy_cli.CapyConfig(api_key="k", me_id=ME, me_email=None, projects=[]))
    held = capy_cli._try_lock()
    try:
        report = capy_cli.sync_once()
    finally:
        held.close()
    assert not report.ran and report.reason == "another sync is running"


def test_sync_refuses_without_connect_or_pairing(home, monkeypatch):
    from probe.cli import capabilities

    assert not capy_cli.sync_once().ran
    capy_cli.save_config(capy_cli.CapyConfig(api_key="k", me_id=ME, me_email=None, projects=[]))
    monkeypatch.setattr(capabilities, "resolved_capture_credential", lambda s=None: None)
    report = capy_cli.sync_once()
    assert not report.ran and "not paired" in report.reason


# --- the timer -------------------------------------------------------------------


def test_the_linux_timer_runs_the_installed_probe_every_ten_minutes(home, monkeypatch):
    monkeypatch.setattr(capy_cli.platform, "system", lambda: "Linux")
    monkeypatch.setattr(capy_cli.shutil, "which", lambda name: f"/opt/bin/{name}")
    monkeypatch.setenv("XDG_CONFIG_HOME", str(home / "cfg"))
    monkeypatch.setattr(capy_cli, "_installed_probe", lambda: "/opt/bin/probe")
    monkeypatch.setattr(capy_cli, "_run_output", lambda argv: "Linger=yes\n")
    monkeypatch.setenv("HTTPS_PROXY", "http://proxy.lab:3128")
    monkeypatch.setenv("AWS_SECRET_ACCESS_KEY", "never-copied")
    ran: list[list[str]] = []
    monkeypatch.setattr(capy_cli, "_run", lambda argv: ran.append(argv) or True)
    mode, line = capy_cli.install_timer()
    unit = home / "cfg/systemd/user"
    service = (unit / "probe-capy-sync.service").read_text()
    assert "ExecStart=/opt/bin/probe capy sync --quiet" in service
    assert f"TimeoutStartSec={capy_cli.SYNC_TIMEOUT_SECONDS}" in service
    assert "Environment=HTTPS_PROXY=http://proxy.lab:3128" in service
    assert "never-copied" not in service, "only the allowlisted environment reaches the timer"
    timer = (unit / "probe-capy-sync.timer").read_text()
    assert "OnCalendar=*:0/10" in timer and "Persistent=true" in timer
    assert ["systemctl", "--user", "enable", "--now", "probe-capy-sync.timer"] in ran
    assert mode is capy_cli.TimerMode.SYSTEMD and "10 minutes" in line
    assert capy_cli.timer_state(mode.value) == "installed"
    capy_cli.remove_timer(mode.value)
    assert capy_cli.timer_state(mode.value) == "not installed"


def test_no_timer_without_a_persistent_probe_that_knows_capy(home, monkeypatch):
    monkeypatch.setattr(capy_cli, "_installed_probe", lambda: None)
    mode, line = capy_cli.install_timer()
    assert mode is None and "No timer installed" in line


def test_the_mac_timer_is_a_launch_agent(home, monkeypatch):
    import plistlib

    monkeypatch.setattr(capy_cli.platform, "system", lambda: "Darwin")
    monkeypatch.setattr(capy_cli, "_installed_probe", lambda: "/opt/bin/probe")
    monkeypatch.setattr(capy_cli, "_run", lambda argv: True)
    mode, _ = capy_cli.install_timer()
    plist = plistlib.loads(capy_cli._launchd_plist().read_bytes())
    assert mode is capy_cli.TimerMode.LAUNCHD
    assert plist["ProgramArguments"] == ["/opt/bin/probe", "capy", "sync", "--quiet"]
    assert plist["StartInterval"] == capy_cli.SYNC_INTERVAL_SECONDS
    capy_cli.remove_timer(mode.value)
    assert not capy_cli._launchd_plist().exists()


def test_without_a_scheduler_the_cron_line_is_printed(home, monkeypatch):
    monkeypatch.setattr(capy_cli.platform, "system", lambda: "Linux")
    monkeypatch.setattr(capy_cli.shutil, "which", lambda name: None if name == "systemctl" else f"/opt/bin/{name}")
    monkeypatch.setattr(capy_cli, "_installed_probe", lambda: "/opt/bin/probe")
    mode, line = capy_cli.install_timer()
    assert mode is capy_cli.TimerMode.CRON
    cron = line.splitlines()[-1].strip()
    assert cron.startswith("*/10 * * * * ") and cron.endswith(" /opt/bin/probe capy sync --quiet")
    assert "PROBE_CAPY_THREADS_DIR=" in cron, "the sandbox's paths reach the cron job too"
    assert capy_cli.timer_state(mode.value).startswith("manual")


# --- probe doctor ----------------------------------------------------------------


def test_doctor_shows_nothing_until_capy_is_connected_then_names_a_refused_key(home, monkeypatch):
    from probe.cli import capabilities, doctor

    assert doctor._capy_rows() == []
    capy_cli.save_config(capy_cli.CapyConfig(
        api_key="k", me_id=ME, me_email="me@lab.example", projects=[{"id": "proj_1", "name": "ml-research"}],
    ))
    monkeypatch.setattr(capabilities, "resolved_capture_credential", lambda s=None: ("t", "http://x"))
    capy_cli._write_private_json(capy_cli.sync_state_path(), {"last_sync": {"at": "T", "ok": False, "auth_failed": True}})
    text = "\n".join(doctor._capy_rows())
    assert "Capy capture" in text and "me@lab.example" in text and "ml-research" in text
    assert "Capy refused the key" in text


# --- review regressions (written before their fixes) --------------------------------


def test_the_capture_killswitch_stops_sync(home, monkeypatch):
    """`.disabled` in a source's capture folder means "ship nothing", for every
    uploader. A sync with it present must not upload."""
    from probe.cli import capabilities

    door = DoorWire(source="capy")
    monkeypatch.setattr(capabilities, "resolved_capture_credential", lambda s=None: ("t", door.base_url))
    with FakeCapy() as fake:
        _seed(fake)
        monkeypatch.setenv(discovery.ENV_API_BASE, fake.base)
        capy_cli.save_config(capy_cli.CapyConfig(
            api_key=fake.key, me_id=ME, me_email="me@lab.example", projects=[{"id": "proj_1", "name": "ml-research"}],
        ))
        (capy_cli.state_dir() / ".disabled").write_text("disabled by the Probe Research wizard\n")
        report = capy_cli.sync_once(wire=door, now=NOW)
    assert not report.ran and "turned off" in (report.reason or "")
    assert door.calls == []


def test_a_newest_message_over_a_mebibyte_is_not_mirrored_twice(home):
    with FakeCapy() as fake:
        fake.add_thread(thread("jam_mine"), [message("m1", "user", "x" * (1024 * 1024 + 10))])
        state: dict = {}
        first = _pull(fake, home, state)
        fake.messages["jam_mine"].append(message("m2", "user", "next"))
        fake.threads["proj_1"][0]["lastActivityAt"] = "2026-10-12T11:00:00Z"
        _pull(fake, home, state)
    assert [r["id"] for r in _lines(first.sessions[0].path)[1:]] == ["m1", "m2"]


def test_a_torn_tail_longer_than_a_mebibyte_keeps_the_complete_lines(tmp_path):
    path = tmp_path / "s.jsonl"
    good = b'{"type":"capy_session"}\n'
    path.write_bytes(good + b"x" * (1024 * 1024 + 10))
    discovery._repair_torn_tail(path)
    assert path.read_bytes() == good


def test_a_lone_surrogate_is_mirrored_and_uploaded_not_fatal(home):
    """A reply cut mid-emoji carries a lone surrogate: it is replaced by U+FFFD
    (the same way everywhere), so neither the pull nor the upload (which
    re-encodes lines as UTF-8) fails on it."""
    door = DoorWire(source="capy")
    with FakeCapy() as fake:
        fake.add_thread(thread("jam_mine"), [message("m1", "assistant", "cut \ud83d here")])
        result = _pull(fake, home, {})
        report = capy_cli.upload(result.sessions, token="t", base_url=door.base_url, uploaded={}, wire=door)
    assert not result.errors and result.sessions
    assert _lines(result.sessions[0].path)[1]["text"] == "cut \ufffd here"
    assert not report.errors and report.batches >= 1


# --- review: cursors, settling, dedupe -----------------------------------------------


def test_message_reads_page_by_event_id_not_message_id(home):
    """Capy's `after` is a 26-character event cursor. A tool entry's id is its
    tool call id, which Capy would refuse (400) as a cursor."""
    with FakeCapy(page_size=2) as fake:
        fake.add_thread(thread("jam_mine"), [
            message(f"toolu_{i:02d}", "tool", f"step {i}", tool="bash") for i in range(5)
        ])
        state: dict = {}
        result = _pull(fake, home, state)
    assert not result.errors, result.errors
    assert [r["id"] for r in _lines(result.sessions[0].path)[1:]] == [f"toolu_{i:02d}" for i in range(5)]
    afters = [p.split("after=")[1].split("&")[0] for p in fake.requests if "/messages" in p and "after=" in p]
    assert afters and all(len(a) == 26 for a in afters)


def test_unsettled_messages_are_read_on_a_later_sync(home):
    with FakeCapy(page_size=2) as fake:
        fake.add_thread(thread("jam_mine"), [message(f"m{i}", "user", f"msg {i}") for i in range(4)])
        fake.unsettled_from["jam_mine"] = 3
        state: dict = {}
        first = _pull(fake, home, state)
        assert [r["id"] for r in _lines(first.sessions[0].path)[1:]] == ["m0", "m1", "m2"]
        del fake.unsettled_from["jam_mine"]
        _pull(fake, home, state)  # no activity change: re-read because it was unsettled
    assert [r["id"] for r in _lines(first.sessions[0].path)[1:]] == ["m0", "m1", "m2", "m3"]


def test_a_lost_cursor_record_reads_again_without_duplicating(home):
    with FakeCapy(page_size=2) as fake:
        fake.add_thread(thread("jam_mine"), [message(f"m{i}", "user", f"msg {i}") for i in range(5)])
        first = _pull(fake, home, {})
        fake.messages["jam_mine"].append(message("m5", "user", "after the loss"))
        _pull(fake, home, {})  # a fresh state record over the same mirror
    assert [r["id"] for r in _lines(first.sessions[0].path)[1:]] == [f"m{i}" for i in range(6)]


def test_a_deleted_mirror_is_rebuilt_identically(home):
    with FakeCapy() as fake:
        _seed(fake)
        state: dict = {}
        first = _pull(fake, home, state)
        before = first.sessions[0].path.read_bytes()
        first.sessions[0].path.unlink()
        _pull(fake, home, state)
    assert first.sessions[0].path.read_bytes() == before


def test_a_message_without_an_id_is_skipped(home):
    with FakeCapy() as fake:
        fake.add_thread(thread("jam_mine"), [
            {"source": "user", "text": "no id"}, message("m1", "user", "has one"),
        ])
        result = _pull(fake, home, {})
    assert [r["id"] for r in _lines(result.sessions[0].path)[1:]] == ["m1"]


# --- review: which threads, subagents, errors ------------------------------------------


def test_a_thread_filed_under_another_project_is_never_read(home):
    with FakeCapy() as fake:
        stray = thread("jam_stray", project="proj_2")
        fake.threads["proj_1"].append(stray)  # Capy's filter let it through
        fake.messages["jam_stray"] = [message("x", "user", "other project")]
        result = _pull(fake, home, {})
    assert result.threads_mine == 0 and not result.sessions
    assert not any("jam_stray/messages" in p for p in fake.requests)


def test_subagent_sessions_are_separate_ids_linked_to_their_thread(home):
    assert discovery.session_id_for(discovery.THREAD, "x") != discovery.session_id_for(discovery.SUBAGENT, "x")
    with FakeCapy() as fake:
        _seed(fake)
        fake.add_subagent("jam_mine", "sub_1", [message("s1", "assistant", "x")], status="done")
        result = _pull(fake, home, {})
    sub = next(s for s in result.sessions if s.session_id == discovery.session_id_for(discovery.SUBAGENT, "sub_1"))
    assert _lines(sub.path)[0]["parent_session_id"] == discovery.session_id_for(discovery.THREAD, "jam_mine")


def test_a_done_subagent_stays_done_and_unread_on_a_quiet_sync(home):
    with FakeCapy() as fake:
        _seed(fake)
        fake.add_subagent("jam_mine", "sub_1", [message("s1", "assistant", "x")], status="done")
        state: dict = {}
        _pull(fake, home, state)
        reads = len(fake.requests)
        again = _pull(fake, home, state)
    sub_sid = discovery.session_id_for(discovery.SUBAGENT, "sub_1")
    assert next(s for s in again.sessions if s.session_id == sub_sid).finished
    assert not [p for p in fake.requests[reads:] if "/subagents/sub_1/messages" in p]


def test_a_working_subagent_is_read_though_its_thread_did_not_move(home):
    with FakeCapy() as fake:
        _seed(fake)
        fake.add_subagent("jam_mine", "sub_1", [message("s1", "assistant", "first")])
        state: dict = {}
        _pull(fake, home, state)
        fake.subagent_messages["sub_1"].append(message("s2", "assistant", "second"))
        fake.subagents["jam_mine"][0]["updatedAt"] = "2026-10-12T09:50:00Z"
        result = _pull(fake, home, state)
    sub = next(s for s in result.sessions if s.session_id == discovery.session_id_for(discovery.SUBAGENT, "sub_1"))
    assert [r["id"] for r in _lines(sub.path)[1:]] == ["s1", "s2"]


def test_a_thread_going_quiet_finishes_without_a_re_read(home):
    with FakeCapy() as fake:
        _seed(fake)
        state: dict = {}
        assert not _pull(fake, home, state).sessions[0].finished
        reads = len(fake.requests)
        later = discovery.pull(_api(fake), root=home / "threads", me=ME, projects=["proj_1"],
                               state=state, now=NOW + discovery.QUIET_FINISH_SECONDS + 3600)
    assert later.sessions[0].finished
    assert not [p for p in fake.requests[reads:] if "/messages" in p]


def test_a_vanished_subagent_is_an_error_and_the_rest_continue(home):
    with FakeCapy() as fake:
        _seed(fake)
        fake.add_subagent("jam_mine", "sub_gone", [])
        fake.add_subagent("jam_mine", "sub_ok", [message("s1", "assistant", "fine")])
        del fake.subagent_messages["sub_gone"]
        result = _pull(fake, home, {})
    assert any("sub_gone" in e for e in result.errors)
    assert discovery.session_id_for(discovery.SUBAGENT, "sub_ok") in {s.session_id for s in result.sessions}


def test_a_failed_thread_read_is_retried_next_sync(home):
    with FakeCapy() as fake:
        _seed(fake)
        fake.fail["/api/v1/threads/jam_mine/messages"] = [500]
        state: dict = {}
        first = _pull(fake, home, state)
        assert any("jam_mine" in e for e in first.errors)
        second = _pull(fake, home, state)
    assert not second.errors
    assert [r["id"] for r in _lines(second.sessions[0].path)[1:]] == ["m1", "m2", "m3"]


def test_a_repeated_thread_list_cursor_is_an_error_not_a_loop(home, monkeypatch):
    with FakeCapy() as fake:
        _seed(fake)
        api = _api(fake)
        monkeypatch.setattr(api, "page", lambda path, params: discovery.Page([], "1:same"))
        result = discovery.pull(api, root=home / "threads", me=ME, projects=["proj_1"], state={}, now=NOW)
    assert any("repeated a page cursor" in e for e in result.errors)


# --- review: the API client ---------------------------------------------------------


def test_429s_past_the_retry_budget_are_an_error(home):
    with FakeCapy() as fake:
        fake.fail["/api/v1/projects"] = [429] * (discovery.MAX_429_RETRIES + 1)
        with pytest.raises(discovery.CapyError, match="429"):
            _api(fake).projects()


@pytest.mark.parametrize(
    ("header", "wait"),
    [("7", 7.0), ("9999", float(discovery.MAX_RETRY_AFTER_S)), (None, discovery.DEFAULT_RETRY_AFTER_S),
     ("soon", discovery.DEFAULT_RETRY_AFTER_S), ("-3", discovery.DEFAULT_RETRY_AFTER_S),
     ("nan", discovery.DEFAULT_RETRY_AFTER_S)],
)
def test_retry_after_is_honoured_and_capped(header, wait):
    assert discovery.retry_after_seconds(header) == wait


def test_the_call_budget_paces_a_burst():
    now = [0.0]
    waits: list[float] = []
    api = discovery.CapyAPI("k", base="http://x", sleep=lambda s: (waits.append(s), now.__setitem__(0, now[0] + s)),
                            clock=lambda: now[0])
    for _ in range(discovery.CALLS_PER_MINUTE + 1):
        api._pace()
    assert waits == [60.0]


def test_the_key_never_follows_a_redirect(home):
    """A 3xx is an error: the key is never sent to the redirect target."""
    import threading
    from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

    seen: list[str | None] = []

    class Elsewhere(BaseHTTPRequestHandler):
        def log_message(self, *a):
            pass

        def do_GET(self):  # noqa: N802
            seen.append(self.headers.get("Authorization"))
            self.send_response(200)
            self.end_headers()

    target = ThreadingHTTPServer(("127.0.0.1", 0), Elsewhere)
    threading.Thread(target=target.serve_forever, daemon=True).start()

    class Redirect(BaseHTTPRequestHandler):
        def log_message(self, *a):
            pass

        def do_GET(self):  # noqa: N802
            self.send_response(302)
            self.send_header("Location", f"http://127.0.0.1:{target.server_address[1]}/steal")
            self.end_headers()

    origin = ThreadingHTTPServer(("127.0.0.1", 0), Redirect)
    threading.Thread(target=origin.serve_forever, daemon=True).start()
    try:
        api = discovery.CapyAPI("capy_" + "s" * 43, base=f"http://127.0.0.1:{origin.server_address[1]}/api/v1")
        with pytest.raises(discovery.CapyError):
            api.projects()
    finally:
        origin.shutdown()
        target.shutdown()
    assert seen == []


def test_an_unsupported_mirror_version_is_marked_not_guessed():
    event = capy_sanitize.sanitize_event({"type": "capy_session", "version": 2, "id": "x"})
    assert event["subtype"] == "session_meta:unsupported_version"
    assert not list(VALIDATOR.iter_errors(event))


# --- review: uploading ----------------------------------------------------------------


@pytest.mark.parametrize(("code", "refused"), [(401, True), (403, True), (500, False), (409, False)])
def test_only_a_401_or_403_marks_the_capture_credential_refused(home, code, refused):
    from probe.tap_core.session_journal import Wire

    class Answering(Wire):
        def _request(self, path, body=None):
            return code, {"detail": "x"}

    with FakeCapy() as fake:
        _seed(fake)
        report = capy_cli.upload(_pull(fake, home, {}).sessions, token="t", base_url="http://door",
                                 uploaded={}, wire=Answering("http://door", "t", "capy"))
    assert report.credential_refused is refused and report.errors


def test_a_refused_credential_stops_later_syncs_until_reconnect(home, monkeypatch):
    from probe.cli import capabilities
    from probe.tap_core.session_journal import Wire

    class Refusing(Wire):
        def _request(self, path, body=None):
            return 401, {"detail": "x"}

    monkeypatch.setattr(capabilities, "resolved_capture_credential", lambda s=None: ("t", "http://x"))
    with FakeCapy() as fake:
        _seed(fake)
        monkeypatch.setenv(discovery.ENV_API_BASE, fake.base)
        capy_cli.save_config(capy_cli.CapyConfig(api_key=fake.key, me_id=ME, me_email=None,
                                                 projects=[{"id": "proj_1"}]))
        first = capy_cli.sync_once(wire=Refusing("http://x", "t", "capy"), now=NOW)
        assert first.upload.credential_refused
        assert capy_cli.sync_once(now=NOW).skipped is capy_cli.Skip.REFUSED
        # Another credential (a new pairing) is another destination: not refused.
        monkeypatch.setattr(capabilities, "resolved_capture_credential", lambda s=None: ("t2", "http://x"))
        assert capy_cli.sync_once(wire=DoorWire(source="capy"), now=NOW).skipped is None


def test_a_session_deleted_in_probe_is_recorded_and_not_resent(home):
    from probe.tap_core.session_journal import DELETED_REASON, DELETED_STATUS, Wire

    class Deleted(Wire):
        def _request(self, path, body=None):
            return DELETED_STATUS, {"detail": {"reason": DELETED_REASON}}

    uploaded: dict = {}
    with FakeCapy() as fake:
        _seed(fake)
        sessions = _pull(fake, home, {}).sessions
        report = capy_cli.upload(sessions, token="t", base_url="http://door", uploaded=uploaded,
                                 wire=Deleted("http://door", "t", "capy"))
    assert report.deleted == 1 and not report.errors
    assert sessions[0].session_id in uploaded


def test_the_batch_budget_leaves_the_rest_for_the_next_sync(home, monkeypatch):
    monkeypatch.setattr(capy_cli, "MAX_BATCHES_PER_SESSION", 1)
    door = DoorWire(source="capy")
    uploaded: dict = {}
    with FakeCapy() as fake:
        fake.add_thread(thread("jam_mine"), [
            message("m1", "user", "a" * 1_500_000), message("m2", "user", "b" * 1_500_000),
        ])
        state: dict = {}
        sessions = _pull(fake, home, state).sessions
        first = capy_cli.upload(sessions, token="t", base_url=door.base_url, uploaded=uploaded, wire=door)
        assert first.batches == 1 and sessions[0].session_id not in uploaded
        for _ in range(4):  # each later sync sends one more batch, until done
            if sessions[0].session_id in uploaded:
                break
            capy_cli.upload(_pull(fake, home, state).sessions, token="t", base_url=door.base_url,
                            uploaded=uploaded, wire=door)
    assert sessions[0].session_id in uploaded
    sid = sessions[0].session_id
    assert door.streams[sid]["source_byte_end"] == sessions[0].path.stat().st_size


def test_two_machines_take_turns_on_one_thread(home, monkeypatch):
    """Two computers with the same key sync the same thread in turn: each adopts
    what the other uploaded (their mirrors are byte-identical) and continues."""
    door = DoorWire(source="capy")
    machines = {name: {"state": {}, "uploaded": {}} for name in ("a", "b")}
    sid = discovery.session_id_for(discovery.THREAD, "jam_mine")

    def sync(name):
        monkeypatch.setenv("PROBE_TRANSCRIPT_STATE_DIR", str(home / name / "journal"))
        m = machines[name]
        pulled = discovery.pull(_api(fake), root=home / name / "threads", me=ME, projects=["proj_1"],
                                state=m["state"], now=NOW)
        return capy_cli.upload(pulled.sessions, token="t", base_url=door.base_url, uploaded=m["uploaded"], wire=door)

    with FakeCapy() as fake:
        _seed(fake)
        for turn, name in enumerate(["a", "b", "a", "b"]):
            fake.messages["jam_mine"].append(message(f"n{turn}", "user", f"turn {turn}"))
            fake.threads["proj_1"][0]["lastActivityAt"] = f"2026-10-12T1{turn}:30:00Z"
            report = sync(name)
            assert not report.errors, (name, report.errors)
    texts = json.dumps(door.bodies(sid))
    assert all(f"turn {t}" in texts for t in range(4))
    assert door.streams[sid]["source_byte_end"] == (home / "b" / "threads" / f"{sid}.jsonl").stat().st_size


def test_a_new_capture_credential_is_a_new_destination():
    assert capy_cli.destination_key("t1", "https://a") != capy_cli.destination_key("t2", "https://a")
    assert capy_cli.destination_key("t1", "https://a") != capy_cli.destination_key("t1", "https://b")


# --- review: connect, sync exit codes, disconnect ------------------------------------------


@pytest.fixture
def connect_env(home, monkeypatch):
    from probe.cli import capabilities, setup, tui

    calls: dict = {"authorize": 0}
    paired: list = [None]
    monkeypatch.setattr(capy_cli, "_probe_account", lambda: {"email": "Me@Lab.example", "customer_id": "team-a"})
    monkeypatch.setattr(capy_cli, "_capture_customer", lambda token, base: "team-a")
    monkeypatch.setattr(capabilities, "resolved_capture_credential", lambda s=None: paired[0])
    monkeypatch.setattr(tui, "interactive", lambda: False)

    def authorize(*args, **kwargs):
        calls["authorize"] += 1
        calls["sources"] = kwargs.get("capture_sources")
        paired[0] = ("t", "http://door")
        return None, []

    monkeypatch.setattr(setup, "authorize", authorize)
    return calls, paired


def _invoke(args, env=None, input=None):
    from typer.testing import CliRunner

    return CliRunner().invoke(capy_cli.capy_app, args, env=env, input=input)


def test_connect_pairs_finds_me_by_probe_email_and_saves_privately(home, connect_env, monkeypatch):
    calls, _ = connect_env
    with FakeCapy() as fake:
        monkeypatch.setenv(discovery.ENV_API_BASE, fake.base)
        (home / "capy-state").mkdir()
        (home / "capy-state" / ".disabled").write_text("off\n")
        result = _invoke(["connect", "--project", "ML-Research", "--no-timer", "--no-sync"],
                         env={capy_cli.ENV_API_KEY: fake.key})
    assert result.exit_code == 0, result.output
    assert calls["authorize"] == 1 and calls["sources"] == [capy_cli.SOURCE]
    config = capy_cli.load_config()
    assert config.me_id == ME and config.project_ids == ["proj_1"] and config.api_key == fake.key
    assert oct(capy_cli.config_path().stat().st_mode & 0o777) == "0o600"
    assert not capy_cli.killswitch_path().exists(), "connect turns capture back on"
    assert fake.key not in result.output
    assert "team-a" in result.output


def test_connect_reads_the_key_from_stdin(home, connect_env, monkeypatch):
    with FakeCapy() as fake:
        monkeypatch.setenv(discovery.ENV_API_BASE, fake.base)
        result = _invoke(["connect", "--api-key-stdin", "--project", "proj_1", "--no-timer", "--no-sync"],
                         input=fake.key + "\n")
    assert result.exit_code == 0, result.output
    assert capy_cli.load_config().api_key == fake.key


def test_connect_has_no_api_key_argument():
    result = _invoke(["connect", "--api-key", "capy_x"])
    assert result.exit_code != 0


def test_connect_refuses_a_key_capy_refuses(home, connect_env, monkeypatch):
    with FakeCapy() as fake:
        monkeypatch.setenv(discovery.ENV_API_BASE, fake.base)
        result = _invoke(["connect", "--project", "proj_1", "--no-timer", "--no-sync"],
                         env={capy_cli.ENV_API_KEY: "capy_wrong"})
    assert result.exit_code == 1 and "refused that key" in result.output
    assert capy_cli.load_config() is None


def test_connect_refuses_when_no_capy_member_has_my_probe_email(home, connect_env, monkeypatch):
    monkeypatch.setattr(capy_cli, "_probe_account", lambda: {"email": "someone@else.example", "customer_id": "t"})
    with FakeCapy() as fake:
        monkeypatch.setenv(discovery.ENV_API_BASE, fake.base)
        result = _invoke(["connect", "--project", "proj_1", "--no-timer", "--no-sync"],
                         env={capy_cli.ENV_API_KEY: fake.key})
    assert result.exit_code == 1 and "No member" in result.output
    assert capy_cli.load_config() is None


def test_connect_names_an_unknown_project(home, connect_env, monkeypatch):
    with FakeCapy() as fake:
        monkeypatch.setenv(discovery.ENV_API_BASE, fake.base)
        result = _invoke(["connect", "--project", "nope", "--no-timer", "--no-sync"],
                         env={capy_cli.ENV_API_KEY: fake.key})
    assert result.exit_code == 2 and "nope" in result.output


def test_connect_re_pairs_a_credential_for_another_team(home, connect_env, monkeypatch):
    calls, paired = connect_env
    paired[0] = ("old", "http://door")
    monkeypatch.setattr(capy_cli, "_capture_customer", lambda token, base: "team-b" if token == "old" else "team-a")
    with FakeCapy() as fake:
        monkeypatch.setenv(discovery.ENV_API_BASE, fake.base)
        result = _invoke(["connect", "--project", "proj_1", "--no-timer", "--no-sync"],
                         env={capy_cli.ENV_API_KEY: fake.key})
    assert result.exit_code == 0, result.output
    assert calls["authorize"] == 1


def test_connect_keeps_a_working_credential_for_my_team(home, connect_env, monkeypatch):
    calls, paired = connect_env
    paired[0] = ("ok", "http://door")
    with FakeCapy() as fake:
        monkeypatch.setenv(discovery.ENV_API_BASE, fake.base)
        result = _invoke(["connect", "--project", "proj_1", "--no-timer", "--no-sync"],
                         env={capy_cli.ENV_API_KEY: fake.key})
    assert result.exit_code == 0, result.output
    assert calls["authorize"] == 0


def test_sync_exit_codes(home, monkeypatch):
    assert _invoke(["sync", "--quiet"]).exit_code == 0, "the timer before connect is quiet"
    assert _invoke(["sync"]).exit_code == 1
    from probe.cli import capabilities

    monkeypatch.setattr(capabilities, "resolved_capture_credential", lambda s=None: ("t", "http://x"))
    with FakeCapy() as fake:
        monkeypatch.setenv(discovery.ENV_API_BASE, fake.base)
        capy_cli.save_config(capy_cli.CapyConfig(api_key="capy_wrong", me_id=ME, me_email=None,
                                                 projects=[{"id": "proj_1"}]))
        result = _invoke(["sync"])
    assert result.exit_code == 1 and "refused the key" in result.output


def test_disconnect_removes_key_record_and_credential(home, monkeypatch):
    from probe.cli import capabilities

    revoked: list = []
    monkeypatch.setattr(capabilities, "revoke_capture_device", lambda s=None: revoked.append(s))
    capy_cli.save_config(capy_cli.CapyConfig(api_key="k", me_id=ME, me_email=None, projects=[], timer="cron"))
    capy_cli._write_private_json(capy_cli.sync_state_path(), {"uploaded": {"x": {}}})
    (capy_cli.state_dir() / ".token").write_text("secret\n")
    result = _invoke(["disconnect"])
    assert result.exit_code == 0, result.output
    assert "crontab" in result.output
    assert not capy_cli.config_path().exists() and not capy_cli.sync_state_path().exists()
    assert not (capy_cli.state_dir() / ".token").exists() and revoked == [capy_cli.SOURCE]


def test_status_and_doctor_flag_a_stalled_timer(home, monkeypatch):
    from probe.cli import capabilities

    monkeypatch.setattr(capabilities, "resolved_capture_credential", lambda s=None: ("t", "http://x"))
    monkeypatch.setattr(capy_cli, "timer_state", lambda mode: "installed")
    capy_cli.save_config(capy_cli.CapyConfig(api_key="k", me_id=ME, me_email="me@lab.example", projects=[]))
    capy_cli._write_private_json(capy_cli.sync_state_path(), {"last_sync": {"at": "2026-01-01T00:00:00+00:00", "ok": True}})
    facts = dict(capy_cli.doctor_facts())
    assert "Stalled" in facts
    assert "Stalled" in _invoke(["status"]).output


def test_a_capy_key_pasted_into_a_prompt_is_redacted():
    from probe.tap_core import secrets

    key = "capy_" + "Ab3_-" * 8 + "xyz"
    assert len(key) == 48
    text, rules = secrets.redact(f"use this key: {key} thanks")
    assert key not in text and "capy-api-key" in rules
    redacted, _ = secrets.redact("capy_skill is a word, capy_" + "a" * 44 + " is too long")
    assert "capy_skill" in redacted


# --- review round 2: killed syncs, budgets, vanished threads, timer secrets -------------


def test_a_sync_killed_before_saving_its_record_never_duplicates(home):
    """Cursors are saved after each thread, but a kill can still land between a
    page's append and the save: the next read sees a mirror larger than its
    record says and checks every id it holds."""
    import copy

    with FakeCapy(page_size=2) as fake:
        fake.add_thread(thread("jam_mine"), [message("m0", "user", "start")])
        state: dict = {}
        first = _pull(fake, home, state)
        saved = copy.deepcopy(state)  # the last record that reached disk
        for i in range(1, 351):
            fake.messages["jam_mine"].append(message(f"m{i}", "user", f"msg {i}"))
        fake.threads["proj_1"][0]["lastActivityAt"] = "2026-10-12T11:00:00Z"
        _pull(fake, home, state)  # appended 350, then "killed": its record is lost
        fake.messages["jam_mine"].append(message("m351", "user", "after the kill"))
        fake.threads["proj_1"][0]["lastActivityAt"] = "2026-10-12T12:00:00Z"
        _pull(fake, home, saved)
        rebuilt = _pull(fake, home / "rebuild", {})
    ids = [r["id"] for r in _lines(first.sessions[0].path)[1:]]
    assert ids == [f"m{i}" for i in range(352)]
    assert first.sessions[0].path.read_bytes() == rebuilt.sessions[0].path.read_bytes()


def test_a_long_history_is_read_over_several_budgeted_syncs(home):
    with FakeCapy(page_size=2) as fake:
        for t in range(3):
            fake.add_thread(thread(f"jam_{t}"), [message(f"t{t}m{i}", "user", f"{t}/{i}") for i in range(7)])
        state: dict = {}
        rounds = 0
        while True:
            rounds += 1
            api = discovery.CapyAPI(fake.key, base=fake.base, max_calls=9, sleep=lambda _s: None)
            result = discovery.pull(api, root=home / "threads", me=ME, projects=["proj_1"], state=state, now=NOW)
            assert not result.errors, result.errors
            if not result.budget_spent:
                break
            assert rounds < 20
        whole = _pull(fake, home / "whole", {})
    assert rounds > 1
    for session in whole.sessions:
        assert (home / "threads" / session.path.name).read_bytes() == session.path.read_bytes()


def test_sync_keeps_what_it_read_when_the_upload_crashes(home, monkeypatch):
    from probe.cli import capabilities

    monkeypatch.setattr(capabilities, "resolved_capture_credential", lambda s=None: ("t", "http://x"))

    def boom(*args, **kwargs):
        raise KeyboardInterrupt

    monkeypatch.setattr(capy_cli, "upload", boom)
    with FakeCapy() as fake:
        _seed(fake)
        monkeypatch.setenv(discovery.ENV_API_BASE, fake.base)
        capy_cli.save_config(capy_cli.CapyConfig(api_key=fake.key, me_id=ME, me_email=None,
                                                 projects=[{"id": "proj_1"}]))
        with pytest.raises(KeyboardInterrupt):
            capy_cli.sync_once(wire=DoorWire(source="capy"), now=NOW)
    saved = json.loads(capy_cli.sync_state_path().read_text())
    assert saved["cursors"] and saved["threads"]["jam_mine"]["marker"]


def test_a_dropped_connection_is_a_capy_error(monkeypatch):
    import http.client

    from probe.cli import capabilities

    class Dropping:
        def open(self, request, timeout=None):
            raise http.client.IncompleteRead(b"partial")

    monkeypatch.setattr(capabilities, "_credential_opener", lambda: Dropping())
    with pytest.raises(discovery.CapyError, match="IncompleteRead"):
        discovery.CapyAPI("k", base="http://x").projects()


def test_a_thread_gone_from_the_listing_is_finished_not_read(home):
    with FakeCapy() as fake:
        _seed(fake)
        fake.add_subagent("jam_mine", "sub_1", [message("s1", "assistant", "x")])
        state: dict = {}
        first = _pull(fake, home, state)
        assert not any(s.finished for s in first.sessions)
        fake.threads["proj_1"] = [t for t in fake.threads["proj_1"] if t["id"] != "jam_mine"]
        reads = len(fake.requests)
        once = _pull(fake, home, state)
        assert not [s for s in once.sessions if s.finished], "one missing listing may be a shifted page"
        later = _pull(fake, home, state)
    assert {s.session_id for s in later.sessions if s.finished} == {
        discovery.session_id_for(discovery.THREAD, "jam_mine"),
        discovery.session_id_for(discovery.SUBAGENT, "sub_1"),
    }
    assert not [p for p in fake.requests[reads:] if "jam_mine" in p]


def test_the_timer_files_are_private_and_escape_percent(home, monkeypatch):
    monkeypatch.setattr(capy_cli.platform, "system", lambda: "Linux")
    monkeypatch.setattr(capy_cli.shutil, "which", lambda name: f"/opt/bin/{name}")
    monkeypatch.setenv("XDG_CONFIG_HOME", str(home / "cfg"))
    monkeypatch.setattr(capy_cli, "_installed_probe", lambda: "/opt/bin/probe")
    monkeypatch.setattr(capy_cli, "_run_output", lambda argv: "")
    monkeypatch.setattr(capy_cli, "_run", lambda argv: True)
    monkeypatch.setenv("HTTPS_PROXY", "http://user:p%40ss@proxy.lab:3128")
    monkeypatch.setenv("PROBE_CAPY_TAP_TOKEN", "ros_ing_" + "a" * 32)
    capy_cli.install_timer()
    service = home / "cfg/systemd/user/probe-capy-sync.service"
    text = service.read_text()
    assert oct(service.stat().st_mode & 0o777) == "0o600"
    assert "p%%40ss" in text and "ros_ing_" not in text
    assert "\\%40" in capy_cli._cron_line(["/opt/bin/probe", "capy", "sync", "--quiet"])


def test_connect_clears_a_refusal(home, connect_env, monkeypatch):
    with FakeCapy() as fake:
        monkeypatch.setenv(discovery.ENV_API_BASE, fake.base)
        capy_cli.state_dir().mkdir(parents=True, exist_ok=True)
        capy_cli.refused_path().write_text("x\n")
        result = _invoke(["connect", "--project", "proj_1", "--no-timer", "--no-sync"],
                         env={capy_cli.ENV_API_KEY: fake.key})
    assert result.exit_code == 0, result.output
    assert not capy_cli.refused_path().exists()


# --- review round 3 -------------------------------------------------------------------


def test_the_state_is_saved_only_after_threads_that_read_something(home):
    with FakeCapy() as fake:
        _seed(fake)
        fake.add_thread(thread("jam_two"), [message("x1", "user", "two")])
        fake.add_thread(thread("jam_old", activity="2026-10-01T00:00:00Z"), [message("o1", "user", "old")])
        state: dict = {}
        saves: list[int] = []
        discovery.pull(_api(fake), root=home / "threads", me=ME, projects=["proj_1"], state=state, now=NOW,
                       on_thread=lambda: saves.append(1))
        first = len(saves)
        saves.clear()
        discovery.pull(_api(fake), root=home / "threads", me=ME, projects=["proj_1"], state=state, now=NOW,
                       on_thread=lambda: saves.append(1))
    assert first == 3
    # The open threads still check their subagents (a call each); the finished one costs nothing.
    assert len(saves) == 2


def test_a_thread_deleted_between_listing_and_read_is_finished_as_mirrored(home):
    with FakeCapy() as fake:
        _seed(fake)
        state: dict = {}
        _pull(fake, home, state)
        del fake.messages["jam_mine"]
        fake.threads["proj_1"][0]["lastActivityAt"] = "2026-10-12T11:00:00Z"
        result = _pull(fake, home, state)
    sid = discovery.session_id_for(discovery.THREAD, "jam_mine")
    assert [s.finished for s in result.sessions if s.session_id == sid] == [True]
    assert "jam_mine" not in state["threads"]


def test_a_thread_moved_between_chosen_projects_is_never_finished(home):
    with FakeCapy() as fake:
        _seed(fake)
        state: dict = {}
        discovery.pull(_api(fake), root=home / "threads", me=ME, projects=["proj_1", "proj_2"], state=state, now=NOW)
        moved = fake.threads["proj_1"].pop(0)
        moved["projectId"] = "proj_2"
        fake.threads["proj_2"].append(moved)
        for _ in range(3):
            result = discovery.pull(_api(fake), root=home / "threads", me=ME, projects=["proj_1", "proj_2"],
                                    state=state, now=NOW)
            sid = discovery.session_id_for(discovery.THREAD, "jam_mine")
            assert [s.finished for s in result.sessions if s.session_id == sid] == [False]


def test_the_time_budget_stops_a_sync_held_up_by_rate_limits(home, monkeypatch):
    now = [0.0]
    monkeypatch.setattr(discovery, "retry_after_seconds", lambda _v: 50.0)
    with FakeCapy() as fake:
        _seed(fake)
        api = discovery.CapyAPI(fake.key, base=fake.base, max_seconds=60,
                                sleep=lambda s: now.__setitem__(0, now[0] + s), clock=lambda: now[0])
        fake.fail["/api/v1/threads/jam_mine/messages"] = [429, 429, 429]
        result = discovery.pull(api, root=home / "threads", me=ME, projects=["proj_1"], state={}, now=NOW)
    assert result.budget_spent and not result.errors


def test_a_mirror_shorter_than_its_record_is_read_from_the_start(home):
    with FakeCapy(page_size=2) as fake:
        fake.add_thread(thread("jam_mine"), [message(f"m{i}", "user", f"msg {i}") for i in range(6)])
        state: dict = {}
        first = _pull(fake, home, state)
        path = first.sessions[0].path
        lines = path.read_bytes().splitlines(keepends=True)
        path.write_bytes(b"".join(lines[:2]))  # header + m0: everything after was lost
        fake.threads["proj_1"][0]["lastActivityAt"] = "2026-10-12T11:00:00Z"
        _pull(fake, home, state)
    assert [r["id"] for r in _lines(path)[1:]] == [f"m{i}" for i in range(6)]


def test_status_follows_the_refusal_marker_not_the_old_record(home, monkeypatch):
    from probe.cli import capabilities

    monkeypatch.setattr(capabilities, "resolved_capture_credential", lambda s=None: ("t", "http://x"))
    capy_cli.save_config(capy_cli.CapyConfig(api_key="k", me_id=ME, me_email=None, projects=[]))
    capy_cli._write_private_json(capy_cli.sync_state_path(),
                                 {"last_sync": {"at": "T", "ok": False, "credential_refused": True}})
    capy_cli.refused_path().write_text(capy_cli.destination_key("t", "http://x") + "\n")
    assert "Probe refused the capture credential" in dict(capy_cli.doctor_facts())["Last sync"]
    capy_cli.refused_path().unlink()
    assert "reconnected since" in dict(capy_cli.doctor_facts())["Last sync"]


def test_connect_installs_no_timer_for_an_environment_only_token(home, connect_env, monkeypatch):
    from probe.cli import capabilities

    monkeypatch.setattr(capabilities, "capture_token_sources",
                        lambda s=None: (capabilities.TokenSource.ENVIRONMENT,))
    monkeypatch.setattr(capy_cli, "install_timer", lambda: pytest.fail("installed a timer it cannot feed"))
    _, paired = connect_env
    paired[0] = ("env-token", "http://door")
    with FakeCapy() as fake:
        monkeypatch.setenv(discovery.ENV_API_BASE, fake.base)
        result = _invoke(["connect", "--project", "proj_1", "--no-sync"], env={capy_cli.ENV_API_KEY: fake.key})
    assert result.exit_code == 0, result.output
    assert "No timer installed" in result.output
