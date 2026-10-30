"""A write says when its work happened (swarm friction R1, R2).

The server dates a session's effort -- its activity bucket and its mark on the
experiment -- by `X-Probe-Event-At` when it falls inside a window it clamps to
(`app/sessions/effort.py::effort_moment`), else by the write's arrival. The
outbox drain sends each op's `enqueued_at`, so a write the backlog held for an
hour still counts when it was made; the Probe daemon's `probe` commands run
with `PROBE_EVENT_AT` (the oldest event of the work they file,
`test_daemon_loop.py`). Sent only beside a session: it dates nothing else.
A queued op records the session that queued it and is sent as that session,
whichever process drains it.
"""

from __future__ import annotations

import json

import httpx
import pytest

from probe.sdk import journal as jm
from probe.sdk import transport as transport_mod
from probe.sdk.agent_session import AGENT_HEADER, AGENT_SESSION_HEADER, EVENT_AT_ENV, EVENT_AT_HEADER
from probe.sdk.client import Client
from probe.sdk.config import Settings
from probe.sdk.journal import Journal, drain
from probe.sdk.transport import Transport, event_at_scope

SESSION = {AGENT_HEADER: "claude_code", AGENT_SESSION_HEADER: "643ce138-4801-4409-b69c-ca30ab7605bc"}
SETTINGS = Settings(base_url="http://test", token="test-token")


@pytest.fixture(autouse=True)
def isolated(monkeypatch, tmp_path):
    monkeypatch.setenv("PROBE_CONFIG_PATH", str(tmp_path / "config.json"))
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))
    monkeypatch.delenv("PROBE_ATTRIBUTION", raising=False)
    monkeypatch.delenv(EVENT_AT_ENV, raising=False)
    monkeypatch.setattr(transport_mod, "agent_session_headers", lambda: dict(SESSION))


def _client(seen: list[httpx.Request], **kwargs) -> Client:
    def handle(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return httpx.Response(200, json={"id": "r1"})

    http = httpx.Client(base_url="http://test", transport=httpx.MockTransport(handle))
    return Client(settings=SETTINGS, transport=Transport(SETTINGS, client=http), auto_drain=False, **kwargs)


QUEUED_BY = "5f0c1d2e-bbbb-4a10-9f3e-00000000000b"


def _queue_one(tmp_path, monkeypatch, *, session: str | None = f"claude_code:{QUEUED_BY}") -> tuple:
    """One write queued by a process whose agent session is `session`."""
    monkeypatch.setattr(jm, "queued_session", lambda: session)
    spool = tmp_path / "outbox"
    producer = Client(settings=SETTINGS, spool_dir=spool, async_writes=True, auto_drain=False)
    producer.write("POST", "/v1/projects", {"name": "filed an hour late"})
    [(path, op)] = producer.journal.pending()
    producer.transport.close()
    return spool, path, op


def _drained(spool) -> list[httpx.Request]:
    """What a drainer whose own session is `SESSION` sends for the queue."""
    seen: list[httpx.Request] = []
    assert drain(Journal(spool), client_factory=lambda _ctx: _client(seen, spool_dir=spool)).delivered == 1
    return seen


def test_a_queued_write_is_its_writers_and_dated_when_it_was_queued(tmp_path, monkeypatch):
    """One outbox worker drains every session's backlog on a machine: the op
    goes as the session that queued it, at its queue time, not as the drainer's."""
    spool, _, op = _queue_one(tmp_path, monkeypatch)
    [sent] = _drained(spool)
    assert sent.headers[AGENT_SESSION_HEADER] == QUEUED_BY != SESSION[AGENT_SESSION_HEADER]
    assert sent.headers[EVENT_AT_HEADER] == op["enqueued_at"]

    seen: list[httpx.Request] = []
    with _client(seen, spool_dir=spool, async_writes=False) as live:
        live.transport.post("/v1/projects", {"name": "today"})
    assert seen[0].headers[AGENT_SESSION_HEADER] == SESSION[AGENT_SESSION_HEADER]
    assert EVENT_AT_HEADER not in seen[0].headers, "a live write arrives when it happens"


def test_a_write_queued_with_no_session_goes_with_none(tmp_path, monkeypatch):
    spool, _, _ = _queue_one(tmp_path, monkeypatch, session=None)
    [sent] = _drained(spool)
    assert AGENT_SESSION_HEADER not in sent.headers and EVENT_AT_HEADER not in sent.headers


def test_a_write_an_older_sdk_queued_goes_as_before(tmp_path, monkeypatch):
    """No recorded session: the drainer's, at its arrival (no event time that
    could date another session's write into this one's past)."""
    spool, path, op = _queue_one(tmp_path, monkeypatch)
    del op["agent_session"]
    path.write_text(json.dumps(op))
    [sent] = _drained(spool)
    assert sent.headers[AGENT_SESSION_HEADER] == SESSION[AGENT_SESSION_HEADER]
    assert EVENT_AT_HEADER not in sent.headers


def test_a_daemon_commands_queued_write_keeps_its_work_time(tmp_path, monkeypatch):
    monkeypatch.setenv(EVENT_AT_ENV, "2026-10-29T01:00:00+00:00")
    spool, _, op = _queue_one(tmp_path, monkeypatch)
    assert op["event_at"] == "2026-10-29T01:00:00+00:00"
    [sent] = _drained(spool)
    assert sent.headers[EVENT_AT_HEADER] == "2026-10-29T01:00:00+00:00"


def test_an_upload_request_carries_one_session_and_one_bucket(tmp_path, monkeypatch):
    """A window's uploads share a request only within one session and one
    5-minute bucket, and the request goes as its oldest op: 10:00 and 10:30
    uploads are two requests, each dated in its own bucket."""
    from test_outbox_run_upload_window import RUN, Server, upload

    monkeypatch.setattr(jm, "MIN_FREE_BYTES", 0)
    monkeypatch.delenv("PROBE_UPLOAD_WORKERS", raising=False)
    monkeypatch.delenv("PROBE_UPLOAD_MANY", raising=False)
    monkeypatch.setattr(jm, "queued_session", lambda: f"claude_code:{QUEUED_BY}")
    queue = Journal(tmp_path / "outbox")
    for i in range(4):
        upload(queue, tmp_path, f"out/file{i}.txt")
    times = ["2026-10-29T10:00:30+00:00", "2026-10-29T10:01:00+00:00",
             "2026-10-29T10:30:10+00:00", "2026-10-29T10:31:00+00:00"]
    for (path, op), queued in zip(queue.pending(), times, strict=True):
        path.write_text(json.dumps({**op, "enqueued_at": queued}))

    asked: list[tuple] = []

    class Recording(Server):
        def presign_run_uploads(self, run_id, items, *, direct=False):
            asked.append((transport_mod._queued_session.get(), transport_mod._event_at.get(), len(items)))
            return super().presign_run_uploads(run_id, items, direct=direct)

    assert drain(queue, client_factory=lambda _context: Recording()).delivered == 4
    assert sorted(asked) == [
        (f"claude_code:{QUEUED_BY}", "2026-10-29T10:00:30+00:00", 2),
        (f"claude_code:{QUEUED_BY}", "2026-10-29T10:30:10+00:00", 2),
    ]
    assert RUN


def test_a_daemon_command_dates_its_writes_and_a_scope_wins(tmp_path, monkeypatch):
    monkeypatch.setenv(EVENT_AT_ENV, "2026-10-29T01:00:00+00:00")
    seen: list[httpx.Request] = []
    with _client(seen, spool_dir=tmp_path / "outbox", async_writes=False) as client:
        client.transport.post("/v1/projects", {"name": "filed"})
        with event_at_scope("2026-10-29T00:30:00+00:00"):
            client.transport.post("/v1/projects", {"name": "queued earlier"})
        with event_at_scope(None):
            client.transport.post("/v1/projects", {"name": "no scope"})
        monkeypatch.setattr(transport_mod, "agent_session_headers", lambda: {})
        client.transport.post("/v1/projects", {"name": "no session"})
    assert [r.headers.get(EVENT_AT_HEADER) for r in seen] == [
        "2026-10-29T01:00:00+00:00",
        "2026-10-29T00:30:00+00:00",
        "2026-10-29T01:00:00+00:00",
        None,
    ]


def test_an_outbox_worker_never_inherits_a_daemon_commands_event_time(monkeypatch):
    """A worker the command kicks drains every producer's ops: each is dated by
    its own queue time, never by the command's."""
    from probe.sdk import outbox_worker

    monkeypatch.setenv(EVENT_AT_ENV, "2026-10-29T01:00:00+00:00")
    assert EVENT_AT_ENV not in outbox_worker._worker_env()
    assert EVENT_AT_ENV not in outbox_worker._rescuer_env()
