"""The Probe service's state in PostHog (`probe.service.statepost`).

Three contracts, each with a test that fails when it is broken:

  * nothing but counts, booleans, versions, ages and enum members leaves the
    machine: `service.status` carries session ids, run names, job ids, plugin
    folders and update error text, and none of it may reach an event;
  * the machine's consent decides, not the service's own clean environment: a
    session whose agent runs with `PROBE_TELEMETRY=off` stops every event, and
    the outbox part goes only where its writes were going;
  * it is sent when it matters: at start, hourly, on a change at most every ten
    minutes, while an update runs (when the watch's scan is quiet), and as the
    service stops.
"""

from __future__ import annotations

import asyncio
import json
import os
import re

import pytest

from probe.service import statepost
from probe.service.registry import Registry
from probe.service.statepost import StatePost, digest, read_outbox, snapshot
from probe.service.watch import Live, decide_machine

HOSTED = "https://api.research.prbe.ai"
SELF_HOST = "https://research.internal.example.com"
SID = "8d1f7c2e-3b4a-4c5d-9e6f-0a1b2c3d4e5f"
RUN = "resnet-sweep-lr-0.003"
SECRET_PATH = "/Users/ben/work/secret-project"


def _leaves(value, path=""):
    if isinstance(value, dict):
        for key, inner in value.items():
            yield f"{path}.{key}", key
            yield from _leaves(inner, f"{path}.{key}")
    elif isinstance(value, (list, tuple, set)):
        for inner in value:
            yield from _leaves(inner, path)
    else:
        yield path, value


_UUID = re.compile(r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-")


def _stuffed_status() -> dict:
    """`service.status` as a real busy machine answers it, with every kind of
    text that must never leave it."""
    return {
        "service_version": "0.304.0", "pid": 4242, "started_at": 1_700_000_000.0, "state": "running",
        "sessions": 3, "app_clients": 1, "watched": 2, "discovering_until": None,
        "update": {
            "enabled": True, "last_check": 1_700_000_100.0, "in_progress": True, "cycle_id": "c0ffee1234",
            "step": "cli_and_plugins", "deferred": None, "deferred_since": None, "guard": {"to": SECRET_PATH},
            "last_result": {"cycle_id": "c0ffee1234", "ok": False, "trigger": "schedule",
                            "steps": {"cli_and_plugins": {"state": "failed", "error": f"uv failed in {SECRET_PATH}"},
                                      "app": {"state": "delegated"}}},
            "app": {"last": {"state": "failed", "result": "failed", "error": "no result from the app within 720 s"}},
        },
        "actions": {"running": {"action": "update", "pid": 77}},
        "hook_hosts": [{"root": f"{SECRET_PATH}/.claude/plugins/probe", "pid": 9}],
        "hook_queue": {"pending": 2},
        "recorders": [{"sid": SID, "alive": True, "recording": True, "started_at": 1.0, "last": {"path": SECRET_PATH},
                       "failures": 2, "tap_version": "0.10.17", "harness": "claude_code"},
                      {"sid": "other-sid", "alive": False, "recording": None, "failures": 1,
                       "tap_version": "0.10.17", "harness": "some agent; rm -rf /"}],
        "workers": [{"sid": SID, "pid": 1, "state": "backoff", "spawns": 4, "crashes": 3, "last_exit": "killed"},
                    {"sid": "x", "state": "made up state", "spawns": 1, "crashes": 0}],
        "runs": [{"run": RUN, "pid": 5, "since": 1.0}],
        "background": {"drains": [{"pid": 1, "running_s": 3.0}], "box_watchers": [],
                       "telemetry": {"queued": 1, "sent": 9, "dropped": 2}},
        "imports": [{"job_id": "job-abc", "pid": 3, "since": 1.0}],
        "statusline": {"folders": 2, "waiting": 1, "running": 0, "children": 1, "last": {"folder": SECRET_PATH}},
        "notes": {"running": True, "waiting": False, "runs": 4, "last": {"error": "boom in " + SECRET_PATH}},
        "watch": {"enabled": True, "last_scan": 1.0, "waiting": 1,
                  "reports": [{"family": "outbox_stuck", "reason": "credential_refused", "sid": None,
                               "answer": "sent", "at": 1.0},
                              {"family": "recorder", "reason": "x", "sid": SID, "answer": "sent", "at": 2.0}]},
    }


def _outbox(**fields) -> dict:
    return {
        "unproven": False,
        "status": {"pending": 12, "pending_bytes": 3_000_000, "failed": 1, "held": 5, "paused": False,
                   "blocked_reason": "credential_refused", "blocked_oldest_pending": "2026-10-23T17:23:00+00:00",
                   "oldest_pending": "2026-10-22T20:09:00+00:00", "refused_fingerprints": {"abababababababab": "x"},
                   "last_error": f"AuthError: 401 for {SECRET_PATH}"},
        "auth_blocked": True, "credential_queues": 3, "roots": 1,
        "discarded": {"writes": 12193, "by_enqueue_day": {"2026-10-22": 6868, "2026-10-23": 5325}},
        **fields,
    }


# -- nothing but counts and enums ----------------------------------------------------


def test_nothing_but_counts_versions_and_enums_leaves_the_machine():
    props = snapshot(_stuffed_status(), outbox=_outbox(), keys={"login": "refused", "daemon_key": "ok",
                                                                 "mcp_key": "who knows"}, now=1_700_003_600.0)
    for where, value in _leaves(props):
        assert value is None or isinstance(value, (bool, int, float, str)), where
        if isinstance(value, str):
            assert "/" not in value and "\\" not in value and "@" not in value and " " not in value, (where, value)
            assert not _UUID.search(value), (where, value)
    text = json.dumps(props)
    for secret in (SID, RUN, SECRET_PATH, "c0ffee1234", "job-abc", "abababababababab", "rm -rf", "boom",
                   "no result from the app"):
        assert secret not in text, secret
    assert props["update_in_progress"] is True and props["update_last_ok"] is False
    assert props["update_last_steps"] == {"cli_and_plugins": "failed", "app": "delegated"}
    assert props["recorders_by_harness"] == {"claude_code": 1, "other": 1}
    assert props["workers_by_state"] == {"backoff": 1, "other": 1}
    assert (props["key_login"], props["key_daemon_key"], props["key_mcp_key"]) == ("refused", "ok", None)
    assert props["watch_reports_by_family"] == {"outbox_stuck": 1, "recorder": 1}
    assert props["outbox_discarded"] == 12193
    assert props["outbox_discarded_by_enqueue_day"] == {"2026-10-23": 5325, "2026-10-22": 6868}
    assert props["outbox_last_error_kind"] == "AuthError"
    assert props["outbox_refused_credentials"] == 1


def test_an_outbox_whose_writes_go_elsewhere_is_left_out():
    props = snapshot(_stuffed_status(), outbox=_outbox(unproven=True))
    assert props["outbox"] is None and props["outbox_omitted"] == statepost.OUTBOX_UNPROVEN
    assert not any(k.startswith("outbox_") and k != "outbox_omitted" for k in props)


def test_the_fake_status_is_shaped_like_the_real_one(tmp_path):
    """A field `snapshot` reads, renamed in the service, would read as 0 or
    None while `_stuffed_status` kept the old name: its keys must be the
    real `service.status`'s."""
    from probe.service.server import Service

    real = Service(registry=Registry(tmp_path / "sessions.json"), discovery_s=0)._status(None, {})
    fake = _stuffed_status()
    assert set(fake) <= set(real), set(fake) - set(real)
    for part in ("update", "background", "watch", "hook_queue", "statusline", "notes", "actions"):
        assert set(fake[part]) <= set(real[part]), (part, set(fake[part]) - set(real[part]))


def test_the_service_starts_reports_and_stops_its_state_post(tmp_path, monkeypatch):
    """The wiring, through the real Service: its consent (`Watch.machine_consent`,
    the login shell when no session runs), its status, and `stop`."""
    from probe.service import watch
    from probe.service.server import Service

    service = Service(registry=Registry(tmp_path / "sessions.json"), discovery_s=0)
    sent: list = []
    service.statepost.enabled = True
    service.statepost.emit = lambda event, props, url: sent.append((event, url)) or True
    service.statepost.outbox = lambda cache: None

    async def login():
        return {}

    service.watch.login = login
    monkeypatch.setattr(watch, "config_base_url", lambda: HOSTED)

    async def go():
        service._done = asyncio.get_running_loop().create_future()
        await service.statepost.tick()
        service.stop("idle")

    asyncio.run(go())
    assert [event for event, _ in sent] == ["service.started", "service.state", "service.stopped"]
    assert {url for _, url in sent} == {HOSTED}


def test_the_real_services_status_snapshots(tmp_path):
    """The real `service.status` shape, not a hand-written one: a field
    renamed there must not silently drop out of the event."""
    from probe.service.server import Service

    service = Service(registry=Registry(tmp_path / "sessions.json"), discovery_s=0)
    props = snapshot(service._status(None, {}))
    assert props["service_state"] in statepost.SERVICE_STATES
    assert props["service_version"] and props["sessions"] == 0
    assert isinstance(props["update_enabled"], bool)


# -- the outbox read ------------------------------------------------------------------


def _queued(root, fp, base_url):
    from probe.sdk.journal import CREDENTIAL_NAMESPACE, Journal

    queue = Journal(str(root / CREDENTIAL_NAMESPACE / fp),
                    context={"name": None, "base_url": base_url, "principal": {"source": "env", "fingerprint": fp}})
    queue.append_http("POST", "/v1/runs/r/metrics", {"points": [{"step_index": 1}]})
    return queue


@pytest.fixture
def outbox_home(tmp_path, monkeypatch):
    from probe.sdk.journal import Journal

    monkeypatch.setattr(Journal, "discover", staticmethod(lambda: []))
    return tmp_path / "outbox"


def test_the_outbox_read_counts_discards_where_they_wait(outbox_home):
    from probe.sdk.journal import Journal

    queue = _queued(outbox_home, "ab" * 8, HOSTED)
    Journal(str(outbox_home)).discard_held(credential="ab" * 8)
    old = outbox_home / "credential-v1" / ("cd" * 8) / "discarded"  # an older release's, still in its queue
    old.mkdir(parents=True)
    (old / "0001-x.json").write_text(json.dumps({"kind": "http", "context": {"base_url": HOSTED},
                                                 "enqueued_at": "2026-10-22T20:00:00+00:00"}))
    found = read_outbox(outbox_home)
    assert found["unproven"] is False
    assert found["discarded"]["writes"] == 2
    assert queue.dir.exists()


def test_writes_pinned_to_a_self_hosted_server_make_the_outbox_unproven(outbox_home):
    _queued(outbox_home, "ab" * 8, HOSTED)
    _queued(outbox_home, "cd" * 8, SELF_HOST)
    assert read_outbox(outbox_home)["unproven"] is True


def test_every_write_is_checked_not_a_sample(outbox_home):
    """Three reviewers: only the first 20 writes of a queue (and of the
    discards) were read for their server, so a self-hosted write after them
    passed as hosted."""
    queue = _queued(outbox_home, "ab" * 8, HOSTED)
    for step in range(25):
        queue.append_http("POST", "/v1/runs/r/metrics", {"points": [{"step_index": step}]})
    assert read_outbox(outbox_home)["unproven"] is False
    late = json.loads(next(iter(sorted((queue.dir / "ops").iterdir()))).read_text())
    late["context"]["base_url"] = SELF_HOST
    (queue.dir / "ops" / "zzzz-late.json").write_text(json.dumps(late))
    assert read_outbox(outbox_home)["unproven"] is True


def test_a_dead_letter_going_elsewhere_makes_it_unproven(outbox_home):
    """Its count, its error and its refusal are reported too, with nothing pending."""
    queue = _queued(outbox_home, "cd" * 8, SELF_HOST)
    (path, _op), = queue.pending()
    queue.failed_dir.mkdir(parents=True, exist_ok=True)
    path.rename(queue.failed_dir / path.name)
    assert read_outbox(outbox_home)["unproven"] is True


def test_discards_are_dated_by_when_they_were_queued_not_their_file(outbox_home):
    folder = outbox_home / "discarded"
    folder.mkdir(parents=True)
    (folder / "0001-x.json").write_text(json.dumps({"kind": "http", "context": {"base_url": HOSTED},
                                                   "enqueued_at": "2026-10-22T20:00:00+00:00"}))
    assert read_outbox(outbox_home)["discarded"] == {"writes": 1, "by_enqueue_day": {"2026-10-22": 1}}


def test_every_outbox_root_is_counted(outbox_home, tmp_path, monkeypatch):
    """Codex: a distributed job's `rank-*` roots and the fallback outbox were
    checked for servers but their pending writes and blocks were not added."""
    from probe.sdk.journal import Journal

    other = tmp_path / "rank-1"
    Journal(str(other), context={"name": None, "base_url": HOSTED}).append_http("POST", "/v1/runs/r/metrics", {})
    monkeypatch.setattr(Journal, "discover", staticmethod(lambda: [other]))
    _queued(outbox_home, "ab" * 8, HOSTED)
    found = read_outbox(outbox_home)
    assert found["roots"] == 2 and found["status"]["pending"] == 2


def test_a_folder_that_cannot_be_listed_makes_it_unproven(outbox_home):
    if os.geteuid() == 0:
        pytest.skip("root reads every folder")
    queue = _queued(outbox_home, "ab" * 8, HOSTED)
    (queue.dir / "failed").mkdir(exist_ok=True)
    os.chmod(queue.dir / "failed", 0)
    try:
        assert read_outbox(outbox_home)["unproven"] is True
    finally:
        os.chmod(queue.dir / "failed", 0o700)


def test_a_scan_past_the_cache_limit_is_unproven_and_recovers(outbox_home):
    queue = _queued(outbox_home, "ab" * 8, HOSTED)
    for step in range(4):
        queue.append_http("POST", "/v1/runs/r/metrics", {"points": [{"step_index": step}]})
    cache = statepost.PinCache(limit=3)
    assert read_outbox(outbox_home, cache)["unproven"] is True
    for path in sorted((queue.dir / "ops").iterdir())[:3]:
        path.unlink()
    assert read_outbox(outbox_home, cache)["unproven"] is False, "the backlog shrank: proven again"


def test_a_write_gone_mid_scan_is_not_counted_and_proves_nothing_wrong(outbox_home):
    queue = _queued(outbox_home, "ab" * 8, HOSTED)
    (path, _op), = queue.pending()
    with os.scandir(path.parent) as entries:
        entry = next(e for e in entries if e.name == path.name)
    path.unlink()  # delivered between the listing and the read
    assert statepost.PinCache().get(entry)[0] is statepost.PinCache.GONE


def test_a_corrupt_dead_letter_is_counted_but_a_corrupt_queued_write_is_unproven(outbox_home):
    queue = _queued(outbox_home, "ab" * 8, HOSTED)
    queue.failed_dir.mkdir(parents=True, exist_ok=True)
    (queue.failed_dir / "0001-bad.json").write_text("not json")
    assert read_outbox(outbox_home)["unproven"] is False, "a quarantined file is sent nowhere"
    (queue.dir / "ops" / "zzzz-bad.json").write_text("not json")
    assert read_outbox(outbox_home)["unproven"] is True


@pytest.mark.parametrize("where", ["delivery-v1/ops", "multipart/ops"])
def test_receipt_and_multipart_writes_are_checked_too(outbox_home, where):
    from probe.sdk.journal import DELIVERY_NAMESPACE

    queue = _queued(outbox_home, "ab" * 8, HOSTED)
    folder = queue.dir / where.replace("delivery-v1", DELIVERY_NAMESPACE)
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "0001-x.json").write_text(json.dumps({"kind": "http", "context": {"base_url": SELF_HOST}}))
    assert read_outbox(outbox_home)["unproven"] is True


def test_tombstones_and_half_pruned_discards_are_counted(outbox_home):
    from probe.sdk.journal import DELIVERY_NAMESPACE

    tombstones = outbox_home / DELIVERY_NAMESPACE / "discarded"
    leftover = outbox_home / "credential-v1" / f".pruned-{'ab' * 8}-1-2" / "discarded"
    for folder in (tombstones, leftover):
        folder.mkdir(parents=True)
        (folder / "0001-x.json").write_text(json.dumps({"kind": "http", "context": {"base_url": HOSTED},
                                                       "enqueued_at": "2026-10-23T10:00:00+00:00"}))
    assert read_outbox(outbox_home)["discarded"]["writes"] == 2


def test_an_empty_outbox_proves_nothing_is_going_anywhere(outbox_home):
    outbox_home.mkdir(parents=True)
    found = read_outbox(outbox_home)
    assert found["unproven"] is False and found["discarded"]["writes"] == 0


# -- consent and cadence --------------------------------------------------------------


class Clock:
    def __init__(self):
        self.now = 1000.0

    def __call__(self):
        return self.now


def _post(status=None, *, voters=(), login=None, base_url=HOSTED, clock=None, outbox=None):
    """A StatePost whose consent is the real rule (`decide_machine`) over
    ``voters`` (a list the test may change), else ``login``."""
    sent: list = []
    status = status if status is not None else _stuffed_status()
    clock = clock or Clock()
    voters = voters if isinstance(voters, list) else list(voters)
    asked: list = []

    async def consent():
        asked.append(1)
        allowed, _ = decide_machine(list(voters), base_url, None if voters else login)
        return allowed, base_url

    post = StatePost(
        log=lambda line: None,
        status=lambda: status,
        consent=consent,
        voters=lambda: list(voters),
        login_env=lambda: login,
        outbox=outbox or (lambda cache: _outbox()),
        emit=lambda event, props, url: sent.append((event, dict(props), url)) or True,
        clock=clock,
        monotonic=clock,
    )
    post.enabled = True  # the suite's PROBE_SERVICE_REPORTS=0 turns it off; these tests are about it on
    post.asked = asked
    return post, sent, status, clock


def _events(sent):
    return [event for event, _, _ in sent]


def test_a_session_with_telemetry_off_stops_every_event():
    post, sent, _, _ = _post(voters=[Live("s1", hosted_env={"PROBE_TELEMETRY": "off"})])
    asyncio.run(post.tick())
    post.stopped("idle", uptime_s=60)
    assert sent == []


def test_with_no_session_the_login_shell_decides():
    post, sent, _, _ = _post(login={"PROBE_TELEMETRY": "off"})
    asyncio.run(post.tick())
    assert sent == []
    post, sent, _, _ = _post(login={})
    asyncio.run(post.tick())
    assert _events(sent) == ["service.started", "service.state"]


def test_a_self_hosted_backend_gets_nothing():
    post, sent, _, _ = _post(voters=[Live("s1", hosted_env={})], base_url=SELF_HOST)
    asyncio.run(post.tick())
    assert sent == []


def test_it_sends_at_start_hourly_and_on_a_change_at_most_every_ten_minutes():
    post, sent, status, clock = _post(voters=[Live("s1", hosted_env={})])
    asyncio.run(post.tick())
    assert _events(sent) == ["service.started", "service.state"]
    clock.now += 60
    asyncio.run(post.tick())
    assert len(sent) == 2, "nothing changed"
    status["state"] = "grace"
    clock.now += 4 * 60
    asyncio.run(post.tick())
    assert len(sent) == 2, "a change, but within ten minutes of the last"
    clock.now += 6 * 60
    asyncio.run(post.tick())
    assert _events(sent)[-1] == "service.state" and sent[-1][1]["service_state"] == "grace"
    clock.now += 30 * 60
    asyncio.run(post.tick())
    assert len(sent) == 3, "same state, under an hour"
    clock.now += 31 * 60
    asyncio.run(post.tick())
    assert len(sent) == 4, "the hourly one"
    assert _events(sent).count("service.started") == 1


def test_nothing_is_sent_while_discovering():
    """A state taken while the sessions come back would hold the first real
    one off by ten minutes (the change limit)."""
    status = _stuffed_status()
    status["discovering_until"] = 1_700_000_030.0
    post, sent, status, clock = _post(status, voters=[Live("s1", hosted_env={})])
    asyncio.run(post.tick())
    assert sent == []
    status["discovering_until"] = None
    clock.now += 5
    asyncio.run(post.tick())
    assert _events(sent) == ["service.started", "service.state"]


def test_the_state_is_sent_while_an_update_hands_over():
    """Codex O7: the watch's scan returns while an update runs or its barrier
    is up; a state report placed behind that gate would never show a stuck
    update. This timer is the service's own."""
    status = _stuffed_status()
    status["update"]["in_progress"] = True
    post, sent, _, _ = _post(status, voters=[Live("s1", hosted_env={})])
    asyncio.run(post.tick())
    assert sent[-1][1]["update_in_progress"] is True


def test_stopped_asks_the_sessions_as_they_are_now():
    voters = [Live("s1", hosted_env={})]
    post, sent, _, _ = _post(voters=voters)
    post.stopped("update", uptime_s=7200)
    assert sent == [], "no consent asked yet: nothing sent"
    asyncio.run(post.tick())
    post.stopped("update", uptime_s=7200)
    assert sent[-1] == ("service.stopped", {"reason": "update", "uptime_h": 2.0}, HOSTED)
    post.stopped("some free text", uptime_s=None)
    assert sent[-1][1] == {"reason": "other", "uptime_h": None}
    voters.append(Live("s2", hosted_env={"PROBE_TELEMETRY": "off"}))  # opted out since the last tick
    count = len(sent)
    post.stopped("idle", uptime_s=60)
    assert len(sent) == count, "a session that opted out since the last ask stops the stop event"


def test_a_session_that_joins_is_asked_before_the_next_send():
    voters = [Live("s1", hosted_env={})]
    post, sent, status, clock = _post(voters=voters)
    asyncio.run(post.tick())
    voters.append(Live("s2", hosted_env={"PROBE_TELEMETRY": "off"}))
    status["state"] = "grace"
    clock.now += 3600
    asyncio.run(post.tick())
    assert _events(sent) == ["service.started", "service.state"], "the new session's opt-out was not asked"


def test_a_refusal_is_not_asked_again_every_minute():
    post, sent, _, clock = _post(login={"PROBE_TELEMETRY": "off"})
    for _ in range(10):
        asyncio.run(post.tick())
        clock.now += 60
    assert sent == [] and len(post.asked) == 1
    clock.now += 3600
    asyncio.run(post.tick())
    assert len(post.asked) == 2, "asked again hourly: the login shell and the config change too"


def test_an_unset_backend_is_the_hosted_default():
    """Codex: `config_base_url()` is None with no `base_url` in the config;
    consent reads None as the hosted default, and the events must go there
    too, not to a context that refuses None."""
    post, sent, _, _ = _post(voters=[Live("s1", hosted_env={})], base_url=None)
    asyncio.run(post.tick())
    assert {url for _, _, url in sent} == {"https://api.research.prbe.ai"}


def test_the_suites_report_switch_turns_it_off(monkeypatch):
    monkeypatch.setenv("PROBE_SERVICE_REPORTS", "0")
    post = StatePost(log=print, status=dict, consent=None, voters=list)
    assert post.enabled is False
    post.start()
    assert post._task is None


def test_a_hung_outbox_read_is_never_started_twice():
    """Three reviewers: on a hung mount a read timed out, its busy flag was
    cleared, and another stuck thread joined the default executor every five
    minutes until the service could not exit. The read runs on a daemon thread
    of its own and stays busy until it really returns."""
    import threading

    release = threading.Event()
    started: list = []

    def stuck(cache):
        started.append(1)
        release.wait(10)
        return _outbox()

    post, sent, _, clock = _post(voters=[Live("s1", hosted_env={})], outbox=stuck)
    statepost_timeout = statepost.OUTBOX_TIMEOUT_S
    try:
        statepost.OUTBOX_TIMEOUT_S = 0.2
        asyncio.run(post._read_outbox())
        clock.now += statepost.OUTBOX_EVERY_S + 1
        asyncio.run(post._read_outbox())
        assert len(started) == 1, "a second read started while the first still hangs"
    finally:
        statepost.OUTBOX_TIMEOUT_S = statepost_timeout
        release.set()


def test_stopped_with_no_session_and_no_shell_answer_sends_nothing():
    """No session runs and the login shell was never read: unknown is no."""
    voters = [Live("s1", hosted_env={})]
    post, sent, _, _ = _post(voters=voters)
    asyncio.run(post.tick())
    voters.clear()  # the sessions ended; the shell was never read
    post.login_env = lambda: None
    count = len(sent)
    post.stopped("idle", uptime_s=10)
    assert len(sent) == count
    post.login_env = lambda: {}
    post.stopped("idle", uptime_s=10)
    assert _events(sent)[-1] == "service.stopped"


def test_a_config_that_cannot_be_read_is_not_taken_for_the_hosted_default():
    """Final review: a failed ask was cached with the hosted default, and
    `stopped` then sent a self-hosted machine's event to PostHog."""
    voters = [Live("s1", hosted_env={})]
    post, sent, _, _ = _post(voters=voters, base_url=SELF_HOST)
    asyncio.run(post.tick())  # asked: self-hosted, nothing sent
    calls = len(post.asked)

    async def unreadable():
        post.asked.append(1)
        raise TimeoutError("config read hung")

    post.consent = unreadable
    voters.append(Live("s2", hosted_env={}))  # the sessions changed: asked again, and it fails
    asyncio.run(post.tick())
    post.stopped("update", uptime_s=60)
    assert sent == [] or all(url == SELF_HOST for _, _, url in sent), sent
    assert not any(url == "https://api.research.prbe.ai" for _, _, url in sent)
    asyncio.run(post.tick())
    assert len(post.asked) == calls + 2, "a failed ask is never cached: asked again next tick"


def test_the_login_shell_is_read_when_the_last_session_leaves():
    """An idle stop comes five seconds after the last session leaves; `prime`
    reads the shell then, so `service.stopped` has an answer to ask."""
    voters = [Live("s1", hosted_env={})]
    post, sent, _, _ = _post(voters=voters)
    asyncio.run(post.tick())
    shell: dict = {}

    async def read():
        shell["read"] = {}
        return {}

    post.login_reader = read
    post.login_env = lambda: shell.get("read")
    voters.clear()

    async def go():
        post.prime()
        await asyncio.sleep(0)
        await asyncio.sleep(0)
        post.stopped("idle", uptime_s=30)

    asyncio.run(go())
    assert _events(sent)[-1] == "service.stopped"


def test_a_session_that_opts_out_during_the_outbox_read_stops_the_send():
    """Codex P1: the read takes up to 30 s; consent is asked again after it."""
    voters = [Live("s1", hosted_env={})]

    def read(cache):
        voters.append(Live("s2", hosted_env={"PROBE_TELEMETRY": "off"}))
        return _outbox()

    post, sent, _, _ = _post(voters=voters, outbox=read)
    asyncio.run(post.tick())
    assert sent == []


def test_the_first_minute_looks_every_few_seconds_then_every_minute():
    post, _, _, clock = _post(voters=[Live("s1", hosted_env={})])
    slept: list = []

    async def run_twice():
        real_sleep = asyncio.sleep

        async def sleep(seconds):
            slept.append(seconds)
            clock.now += seconds
            if len(slept) >= 3:
                post._closed = True
            await real_sleep(0)

        statepost.asyncio.sleep = sleep
        try:
            await post._run()
        finally:
            statepost.asyncio.sleep = real_sleep

    post._born = clock.now
    post._started_sent = False
    post.tick = lambda: asyncio.sleep(0)
    asyncio.run(run_twice())
    assert slept[0] == statepost.START_TICK_S
    post._born = clock.now - statepost.FAST_FOR_S - 1
    slept.clear()
    post._closed = False
    asyncio.run(run_twice())
    assert slept[0] == statepost.STATE_TICK_S, "past the first minute it is the normal tick, sent or not"


def test_a_crashed_last_run_is_named_on_start():
    post, sent, _, _ = _post(voters=[Live("s1", hosted_env={})])
    post.crashed = "unclean_exit"
    asyncio.run(post.tick())
    (started,) = [props for event, props, _ in sent if event == "service.started"]
    assert started["crashed_last_run"] is True and started["last_run_ended"] == "unclean_exit"


def test_the_digest_ignores_counts_that_move_all_day():
    one = snapshot(_stuffed_status(), outbox=_outbox())
    status = _stuffed_status()
    status["background"]["telemetry"]["dropped"] = 50
    status["recorders"][0]["failures"] = 9
    assert digest(snapshot(status, outbox=_outbox())) == digest(one)
    assert digest(snapshot(status, outbox=_outbox(auth_blocked=False))) != digest(one)


# -- the sender's own gate --------------------------------------------------------------


@pytest.fixture
def captured(tmp_path, monkeypatch):
    from probe.cli import telemetry as tm

    monkeypatch.setenv("PROBE_CONFIG_PATH", str(tmp_path / "probe" / "config.json"))
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    monkeypatch.delenv("PROBE_BASE_URL", raising=False)
    records: list = []
    monkeypatch.setenv("PROBE_TELEMETRY", "on")
    monkeypatch.setattr(tm, "_sender", None)
    monkeypatch.setattr(tm, "_flush_registered", True)
    monkeypatch.setattr(tm._Sender, "start", lambda self: None)
    monkeypatch.setattr(tm._Sender, "put", lambda self, rec: records.append(rec))
    return records


def test_the_sender_takes_only_the_services_events(captured, monkeypatch):
    from probe.cli import telemetry as tm

    assert tm.emit_service_event("service.state", {"sessions": 1}, base_url=HOSTED) is True
    assert tm.emit_service_event("outbox.stuck", {"pending": 1}, base_url=HOSTED) is False
    assert tm.emit_service_event("service.state", {"sessions": 1}, base_url=SELF_HOST) is False
    monkeypatch.setenv("PROBE_TELEMETRY", "off")
    assert tm.emit_service_event("service.state", {"sessions": 1}, base_url=HOSTED) is False
    assert [r["event"] for r in captured] == ["service.state"]
    assert captured[0]["properties"]["via"] == "service"
