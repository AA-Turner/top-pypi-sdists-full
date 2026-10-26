"""A pause ends (Tokenless, 2026-10-26).

`probe outbox pause` used to hold delivery until someone ran `resume`, and
nothing ever did. A folder import's abort screen suggested it, it was typed
20 s later, and the import's last 800 writes -- with every write the machine
made after them -- sat queued. Each test names a contract that kept them there:
the marker had no end, the banner trusted status.json's copy of it, an older
release reads only whether the marker exists, and nothing ever looked again.
An update releases such an outbox at once (Richard's call): an older CLI's
endless pause is over, the next `probe` command lifts it, and so does the Probe
service, which starts after every update and looks again every minute.
"""

from __future__ import annotations

import asyncio
import importlib
import json
import os
import threading
import time
from contextlib import contextmanager
from datetime import datetime, timedelta, timezone

import pytest

from probe import cli
from probe.cli import telemetry as tm
from probe.sdk import journal as jmod
from probe.sdk import outbox_worker
from probe.sdk.journal import DEFAULT_PAUSE_HOURS, PAUSE_SCHEMA, Journal

HOSTED = "https://api.research.prbe.ai"


@pytest.fixture(autouse=True)
def isolate(tmp_path, monkeypatch):
    monkeypatch.setenv("PROBE_CONFIG_PATH", str(tmp_path / "probe" / "config.json"))
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    for var in ("PROBE_BASE_URL", "PROBE_TOKEN", "PROBE_MCP_TOKEN", "PROBE_OUTBOX_DIR"):
        monkeypatch.delenv(var, raising=False)
    (tmp_path / "probe").mkdir(parents=True, exist_ok=True)


@pytest.fixture()
def captured(monkeypatch):
    records: list[dict] = []
    monkeypatch.setenv("PROBE_TELEMETRY", "on")
    monkeypatch.setattr(tm, "_sender", None)
    monkeypatch.setattr(tm, "_flush_registered", True)
    monkeypatch.setattr(tm._Sender, "start", lambda self: None)
    monkeypatch.setattr(tm._Sender, "put", lambda self, rec: records.append(rec))
    return records


def seeded(tmp_path) -> Journal:
    journal = Journal(str(tmp_path / "outbox"), context={"name": None, "base_url": HOSTED})
    journal.append_http("POST", "/v1/runs/r/metrics", {"k": 1})
    return journal


def _ago(hours: float) -> str:
    return (datetime.now(timezone.utc) - timedelta(hours=hours)).isoformat()


def _expire(journal: Journal) -> None:
    marker = json.loads(journal.paused_file.read_text())
    marker.update(at=_ago(2), until=_ago(1))
    journal.paused_file.write_text(json.dumps(marker) + "\n")


def _older_clis_pause(journal: Journal, minutes_ago: float = 1) -> None:
    """What `probe outbox pause` wrote before this release (Tokenless's), and
    the status.json it left saying paused."""
    journal.pause()
    journal.paused_file.write_text(_ago(minutes_ago / 60) + "\n")


def _status(journal: Journal) -> dict:
    return Journal.read_status(str(journal.dir))


def _stored_paused(journal: Journal) -> bool:
    return json.loads(journal.status_file.read_text())["paused"]


def _lifted(records) -> list[dict]:
    return [r["properties"] for r in records if r["event"] == tm.EVENT_OUTBOX_PAUSE_LIFTED]


def _hours_left(until: str) -> float:
    return (datetime.fromisoformat(until) - datetime.now(timezone.utc)).total_seconds() / 3600


# -- what a marker means --------------------------------------------------------


def test_a_pause_ends_and_status_json_does_not_outlive_it(tmp_path):
    """The banner, the spawn gate and the Probe service read `paused` through
    `read_status`, which used to return status.json's copy: written True at the
    pause and never rewritten by its end. The marker decides."""
    journal = seeded(tmp_path)
    journal.pause(hours=1)
    assert journal.paused and _status(journal)["paused"] is True

    _expire(journal)

    assert _stored_paused(journal) is True, "the stale copy this test is about"
    assert not journal.paused
    assert _status(journal)["paused"] is False and _status(journal)["paused_until"] is None


def test_an_older_clis_endless_pause_is_over_however_fresh(tmp_path):
    """Richard's call (2026-10-26): an update releases what an older CLI's
    endless pause held at once -- a minute old or a month. The price: a pause
    an older CLI still on the machine types afterwards is over too."""
    journal = seeded(tmp_path)
    _older_clis_pause(journal, minutes_ago=1)
    assert not journal.paused
    assert _status(journal)["paused"] is False


@pytest.mark.parametrize("raw", [b"not a timestamp", b"\xff\xfe not utf-8", b"", b'"a json string"'])
def test_a_marker_that_is_not_a_json_object_is_an_older_clis_and_over(tmp_path, raw):
    """`paused` runs inside every append: reading such a marker never raises,
    holds nothing, and the next look deletes it."""
    journal = seeded(tmp_path)
    journal.paused_file.write_bytes(raw)
    assert not journal.paused
    journal.append_http("POST", "/v1/runs/r/metrics", {"k": 2})
    assert journal.lift_stale_pause() is True and not journal.paused_file.exists()


def _unreadable_marker(journal: Journal, kind: str) -> None:
    if kind == "directory":
        journal.paused_file.mkdir()
    elif kind == "symlink":
        target = journal.dir / "elsewhere"
        target.write_text(json.dumps({"until": _ago(1)}))
        journal.paused_file.symlink_to(target)
    elif kind == "past-the-calendar":
        journal.paused_file.write_text(json.dumps({"until": "9999-12-31T23:59:59-23:00"}))
    elif kind == "no-permission":
        journal.paused_file.write_text(json.dumps({"until": _ago(1)}))
        journal.paused_file.chmod(0)
    elif kind == "oversized":
        journal.paused_file.write_text(json.dumps({"until": _ago(1), "reason": "x" * 5000}))


@pytest.mark.parametrize("kind", ["directory", "symlink", "past-the-calendar", "no-permission", "oversized"])
def test_a_marker_that_cannot_be_read_holds_and_is_never_lifted(tmp_path, kind):
    """Unknown is paused (security review): a read error on shared storage, a
    root-owned marker, a planted symlink or one cut at the read cap must not
    release a deliberate hold. Only `resume` deletes it. Appends still work."""
    if kind in ("symlink", "no-permission") and os.name == "nt":
        pytest.skip("POSIX symlinks and modes")
    if kind == "no-permission" and os.geteuid() == 0:
        pytest.skip("root reads a 000 file")
    journal = seeded(tmp_path)
    _unreadable_marker(journal, kind)
    try:
        assert journal.paused
        journal.append_http("POST", "/v1/runs/r/metrics", {"k": 2})
        assert journal.lift_stale_pause() is False and os.path.lexists(journal.paused_file)
        assert _status(journal)["paused"] is True and _status(journal)["paused_until"] is None
    finally:
        if kind == "no-permission":
            journal.paused_file.chmod(0o600)


def test_a_json_marker_without_a_readable_end_holds_a_day_from_its_start(tmp_path):
    """A newer release's shape is never ended early here: no `until`, or one
    that will not parse, holds DEFAULT_PAUSE_HOURS from `at`, else from when
    the file was written."""
    journal = seeded(tmp_path)
    for marker in ({"schema": "probe.outbox.pause/2", "at": _ago(0.1), "ends": None},
                   {"schema": "probe.outbox.pause/2", "until": "when the sweep ends"}):
        journal.paused_file.write_text(json.dumps(marker))
        assert journal.paused and journal.lift_stale_pause() is False
        left = _hours_left(_status(journal)["paused_until"])
        assert DEFAULT_PAUSE_HOURS - 0.2 < left <= DEFAULT_PAUSE_HOURS
    os.utime(journal.paused_file, (time.time() - (DEFAULT_PAUSE_HOURS + 1) * 3600,) * 2)
    assert not journal.paused and journal.lift_stale_pause() is True


def test_until_resume_holds_however_long(tmp_path):
    journal = seeded(tmp_path)
    journal.pause(hours=None)
    marker = json.loads(journal.paused_file.read_text())
    marker["at"] = _ago(24 * 30)
    journal.paused_file.write_text(json.dumps(marker))

    assert journal.paused
    assert _status(journal)["paused_until"] is None
    assert journal.lift_stale_pause() is False and journal.paused_file.exists()


def test_a_newer_releases_until_null_is_not_ended_early(tmp_path):
    journal = seeded(tmp_path)
    journal.paused_file.write_text(json.dumps({"schema": "probe.outbox.pause/2", "at": _ago(48), "until": None}))
    assert journal.paused
    assert journal.lift_stale_pause() is False


def test_the_queues_under_the_root_end_with_it(tmp_path):
    """`probe outbox pause` pauses the root; a credential queue and the
    delivery namespace are paused through it, and released with it."""
    journal = seeded(tmp_path)
    queues = [Journal(str(journal.dir / "delivery-v1")), Journal(str(journal.dir / "credential-v1" / "ab12"))]
    journal.pause(hours=1)
    assert all(q.paused for q in queues)
    _expire(journal)
    assert not any(q.paused for q in queues)


# -- lifting ---------------------------------------------------------------------


def test_lifting_deletes_only_a_pause_that_no_longer_holds(tmp_path):
    """An older release (an SDK pinned in a job's venv) reads only whether the
    marker EXISTS, so a pause that ended holds for it until the file is gone."""
    journal = seeded(tmp_path)
    journal.pause(hours=1)
    assert journal.lift_stale_pause() is False and journal.paused_file.exists()

    _expire(journal)

    assert journal.lift_stale_pause() is True
    assert not journal.paused_file.exists()
    assert _stored_paused(journal) is False
    assert journal.lift_stale_pause() is False


def test_a_pause_written_while_the_lift_waits_for_the_lock_is_kept(tmp_path, monkeypatch):
    """`pause` writes under the append lock and the lift looks again under it:
    a `probe outbox pause` landing between the lift's first look and its lock
    survives."""
    journal = seeded(tmp_path)
    _older_clis_pause(journal)
    real = jmod.file_lock

    @contextmanager
    def fresh_pause_then_lock(path, *a, **k):
        journal.paused_file.write_text(json.dumps({"schema": PAUSE_SCHEMA, "at": _ago(0), "until": None}))
        with real(path, *a, **k):
            yield

    monkeypatch.setattr(jmod, "file_lock", fresh_pause_then_lock)
    assert journal.lift_stale_pause() is False
    assert journal.paused_file.exists() and journal.paused


def test_a_lift_that_must_not_wait_skips_a_held_lock(tmp_path):
    """The Probe service lifts with `wait=False`: a writer stopped mid-append
    (Ctrl-Z, a stale NFS lock) must not hang the service's exit. It lifts on
    a later look."""
    journal = seeded(tmp_path)
    _older_clis_pause(journal)
    with jmod._try_lock(journal.append_lock) as held:
        assert held
        assert journal.lift_stale_pause(wait=False) is False and journal.paused_file.exists()
    assert journal.lift_stale_pause(wait=False) is True and not journal.paused_file.exists()


MARKERS = {
    "absent": (lambda j: None, False, False),
    "older-cli": (lambda j: _older_clis_pause(j), False, True),
    "timed": (lambda j: j.pause(hours=2), True, False),
    "until-resume": (lambda j: j.pause(hours=None), True, False),
    "ended": (lambda j: (j.pause(hours=1), _expire(j)), False, True),
    "directory": (lambda j: j.paused_file.mkdir(), True, False),
}


@pytest.mark.parametrize("kind", sorted(MARKERS))
def test_every_kind_of_marker_reads_lifts_and_resumes_as_documented(tmp_path, monkeypatch, kind):
    """The state matrix (review): what each marker reads as, whether a look
    lifts it, and that `resume` clears every one."""
    make, paused, liftable = MARKERS[kind]
    journal = seeded(tmp_path)
    make(journal)
    assert journal.paused is paused and _status(journal)["paused"] is paused
    if kind != "directory":
        snapshot = journal.paused_file.read_bytes() if journal.paused_file.exists() else None
        assert journal.lift_stale_pause() is liftable
        if snapshot is not None and liftable:
            journal.paused_file.write_bytes(snapshot)
    monkeypatch.setattr(importlib.import_module("probe.cli.main"), "_kick_drainer", lambda: None)
    if kind == "directory":
        journal.paused_file.rmdir()  # `resume` deletes files; nothing writes a directory there
    assert cli.main(["--spool-dir", str(journal.dir), "outbox", "resume"]) == 0
    assert not os.path.lexists(journal.paused_file) and not journal.paused
    assert _status(journal)["paused"] is False


# -- the CLI ---------------------------------------------------------------------


def _notice(main, monkeypatch, journal, *, base_url=HOSTED, lift=True):
    kicked: list[bool] = []
    monkeypatch.setattr(main._conn, "spool_dir", str(journal.dir))
    monkeypatch.setattr(main._conn, "base_url", base_url)
    monkeypatch.setattr(main, "_kick_drainer", lambda: kicked.append(True))
    monkeypatch.setattr(outbox_worker, "maybe_rescue", lambda *a, **k: None)
    main._outbox_notice(lift=lift)
    return kicked


def test_tokenless_is_sent_on_the_first_command_after_the_update(tmp_path, monkeypatch, captured, capsys):
    """Tokenless's machine after the update: an older CLI's marker, a
    status.json that says paused, one write held, a rescue put off while
    paused. The first `probe` command of any kind deletes the marker, says
    once why uploads start again, kicks the drainer, lets the rescue look
    again and reports it."""
    main = importlib.import_module("probe.cli.main")
    journal = seeded(tmp_path)
    _older_clis_pause(journal)
    stamp = outbox_worker._rescue_stamp(journal)
    stamp.write_text("later")

    assert _notice(main, monkeypatch, journal) == [True]

    assert not journal.paused_file.exists()
    assert not stamp.exists(), "a rescue put off while paused looks again now"
    (props,) = _lifted(captured)
    assert props["pending"] == 1
    err = capsys.readouterr().err
    assert "an earlier `probe outbox pause` has ended — sending 1 queued write(s)" in err
    assert "paused until" not in err


def test_the_banner_says_when_a_pause_ends_and_how_to_end_it_sooner(tmp_path, monkeypatch, captured, capsys):
    main = importlib.import_module("probe.cli.main")
    journal = seeded(tmp_path)
    journal.pause(hours=2)

    kicked = _notice(main, monkeypatch, journal)

    err = capsys.readouterr().err
    assert "1 pending; paused until " in err and " UTC — `probe outbox resume` sends them now" in err
    assert kicked == [] and journal.paused_file.exists()
    assert _lifted(captured) == []


def test_until_resume_has_no_end_in_the_banner(tmp_path, monkeypatch, captured, capsys):
    main = importlib.import_module("probe.cli.main")
    journal = seeded(tmp_path)
    journal.pause(hours=None)
    assert _notice(main, monkeypatch, journal) == [] and journal.paused_file.exists()
    assert "1 pending; paused — `probe outbox resume` sends them now" in capsys.readouterr().err


def test_a_self_host_command_lifts_the_pause_but_never_reports_it(tmp_path, monkeypatch, captured):
    """The outbox events' egress gate: a self-host backend sends the vendor
    nothing, and the pause is lifted all the same."""
    main = importlib.import_module("probe.cli.main")
    journal = seeded(tmp_path)
    _older_clis_pause(journal)
    assert _notice(main, monkeypatch, journal, base_url="https://research.internal.example.com") == [True]
    assert not journal.paused_file.exists()
    assert _lifted(captured) == []


def test_pausing_over_an_ended_pause_starts_no_drainer_first(tmp_path, monkeypatch, captured):
    """`probe outbox ...` owns the marker: the every-command check must not
    lift an ended one and start the drainer that `pause` is about to stop."""
    main = importlib.import_module("probe.cli.main")
    journal = seeded(tmp_path)
    journal.pause(hours=1)
    _expire(journal)
    lifted: list = []
    kicked: list = []
    rescued: list = []
    monkeypatch.setattr(main, "_lift_stale_pause", lambda status: lifted.append(status) or True)
    monkeypatch.setattr(main, "_kick_drainer", lambda: kicked.append(True))
    monkeypatch.setattr(outbox_worker, "maybe_rescue", lambda *a, **k: rescued.append(True))
    assert cli.main(["--spool-dir", str(journal.dir), "outbox", "pause", "--hours", "2"]) == 0
    assert lifted == [] and kicked == [] and rescued == [] and journal.paused
    assert 1.9 < _hours_left(_status(journal)["paused_until"]) <= 2


def test_the_pause_help_states_the_default():
    from typer.testing import CliRunner

    out = CliRunner().invoke(importlib.import_module("probe.cli.main").app, ["outbox", "pause", "--help"]).output
    assert f"({DEFAULT_PAUSE_HOURS:g} by default)" in " ".join(out.split())


# -- the Probe service -----------------------------------------------------------


def test_the_service_lift_reports_nothing_itself(tmp_path, monkeypatch, captured):
    """`_lift_outbox_pause` lifts an older CLI's pause at the default root and
    reports nothing: the drainer reports, under the person's own switches."""
    from probe.service import server

    journal = seeded(tmp_path)
    _older_clis_pause(journal)
    monkeypatch.setenv("PROBE_OUTBOX_DIR", str(journal.dir))
    lifted, root, held = server._lift_outbox_pause(None)
    assert (lifted, root, held) == (True, str(journal.dir), 1)
    assert not journal.paused_file.exists() and _lifted(captured) == []
    assert server._lift_outbox_pause(None)[0] is False


@contextmanager
def _running_service(tmp_path, monkeypatch, login_env, *, period="0.2"):
    from probe.service import paths, server
    from probe.service.registry import Registry

    monkeypatch.setenv("HOME", str(tmp_path / "home"))
    monkeypatch.setenv(server.OUTBOX_LOOK_ENV, period)

    async def login():
        return login_env

    monkeypatch.setattr(server, "_outbox_login_env", login)
    monkeypatch.setattr(server, "_mark_versions", lambda: None)
    monkeypatch.setattr(server, "_keep", lambda: None)
    path = paths.ensure_dirs().with_name("outbox-test.sock")
    listen = server._bind(path)
    service = server.Service(registry=Registry(paths.service_dir() / "outbox.json"), discovery_s=0, grace_s=30)
    drains: list[dict] = []
    monkeypatch.setattr(service.background, "drain", lambda request: drains.append(request) or {"accepted": True, "state": "started"})
    loop = asyncio.new_event_loop()
    thread = threading.Thread(target=lambda: loop.run_until_complete(service.run(listen)))
    thread.start()
    try:
        yield drains
    finally:
        loop.call_soon_threadsafe(service.stop, "test")
        thread.join(10)
        path.unlink(missing_ok=True)
    assert not thread.is_alive(), "the service must exit with its outbox look"


def _wait(predicate, seconds=10.0) -> bool:
    end = time.monotonic() + seconds
    while time.monotonic() < end:
        if predicate():
            return True
        time.sleep(0.05)
    return predicate()


def test_the_service_releases_a_stuck_outbox_as_it_starts_and_when_a_pause_ends(tmp_path, monkeypatch, captured):
    """No command at all: the service starting (as after an update) lifts an
    older CLI's pause and starts the drainer with the login shell's variables;
    a timed pause that ends later is lifted on a later look."""
    journal = seeded(tmp_path)
    _older_clis_pause(journal)
    monkeypatch.setenv("PROBE_OUTBOX_DIR", str(journal.dir))
    env = {"PATH": "/usr/bin:/bin", "PROBE_CONFIG_PATH": "/home/p/.probe.json", "HTTPS_PROXY": "http://proxy:3128"}
    with _running_service(tmp_path, monkeypatch, env) as drains:
        assert _wait(lambda: not journal.paused_file.exists())
        assert _wait(lambda: len(drains) == 1)
        assert drains[0]["dir"] == str(journal.dir) and drains[0]["env"] == env

        journal.pause(hours=1 / 3600)  # ends in a second
        assert journal.paused
        assert _wait(lambda: not journal.paused_file.exists())
        assert _wait(lambda: len(drains) == 2)
    assert _lifted(captured) == []


def test_the_service_starts_no_drainer_without_the_login_shell(tmp_path, monkeypatch):
    """Its own stripped environment has no proxy, no CA and maybe the wrong
    config: a drainer started with it could hold the outbox's lease failing
    forever (adversarial review). The marker still goes; the next command or
    write sends."""
    monkeypatch.setenv("PROBE_OUTBOX_DIR", str(tmp_path / "outbox"))
    journal = seeded(tmp_path)
    _older_clis_pause(journal)
    with _running_service(tmp_path, monkeypatch, None) as drains:
        assert _wait(lambda: not journal.paused_file.exists())
        time.sleep(0.5)
        assert drains == []


def test_the_service_starts_no_drainer_for_an_endpoint_the_login_may_not_go_to(tmp_path, monkeypatch):
    journal = seeded(tmp_path)
    _older_clis_pause(journal)
    monkeypatch.setenv("PROBE_OUTBOX_DIR", str(journal.dir))
    env = {"PATH": "/usr/bin:/bin", "PROBE_BASE_URL": "https://elsewhere.example.com"}
    with _running_service(tmp_path, monkeypatch, env) as drains:
        assert _wait(lambda: not journal.paused_file.exists())
        time.sleep(0.5)
        assert drains == []


def test_the_suite_s_services_leave_the_outbox_alone(tmp_path, monkeypatch):
    """`PROBE_SERVICE_OUTBOX_S=0` (conftest): nothing is looked at or lifted."""
    journal = seeded(tmp_path)
    _older_clis_pause(journal)
    monkeypatch.setenv("PROBE_OUTBOX_DIR", str(journal.dir))
    with _running_service(tmp_path, monkeypatch, {"PATH": "/usr/bin"}, period="0") as drains:
        time.sleep(0.6)
        assert journal.paused_file.exists() and drains == []
