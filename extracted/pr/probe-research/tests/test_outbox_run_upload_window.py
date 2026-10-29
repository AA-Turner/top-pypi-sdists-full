"""A run's queued uploads go up together; nothing else in its queue moves.

The run outbox used to send its uploads one after another, three round trips
each. Now the uploads at the head of a run's queue move as one window: one
presign and one confirm request for all of them (`upload_many`), their PUTs in
parallel. These pin that, and -- the part that matters more -- every order that
must NOT change: an upload never lands before an earlier op of its run it could
depend on, two versions of a file land in queue order, the close waits, and a
server without the many-file doors still gets every file, one op at a time.
"""

from __future__ import annotations

import threading
import time
import uuid
from types import SimpleNamespace

import pytest

from probe.sdk import errors, upload_many
from probe.sdk import journal as jm
from probe.sdk.journal import Journal, drain

RUN = str(uuid.UUID(int=7))


@pytest.fixture(autouse=True)
def isolated(monkeypatch, tmp_path):
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))
    monkeypatch.setenv("PROBE_CONFIG_PATH", str(tmp_path / "config" / "probe.json"))
    monkeypatch.delenv("PROBE_TOKEN", raising=False)
    monkeypatch.delenv("PROBE_ATTRIBUTION", raising=False)
    monkeypatch.delenv("PROBE_UPLOAD_WORKERS", raising=False)
    monkeypatch.delenv("PROBE_UPLOAD_MANY", raising=False)
    monkeypatch.setattr(jm, "MIN_FREE_BYTES", 0)


@pytest.fixture
def queue(tmp_path):
    return Journal(tmp_path / "outbox")


class ConnectError(Exception):
    """Named like httpx's: `upload_many` matches the cause by name."""


class Server:
    """One server, recording what it was asked in arrival order. Rows are keyed
    on (run, name, digest), as the server's run identity is, so a replay of a
    file it already holds gets the same artifact back."""

    def __init__(self, *, doors: bool = True, refuse: tuple[str, ...] = (), delay: float = 0.02):
        # A base URL of its own: `upload_many` remembers a door-less server per URL.
        self.settings = SimpleNamespace(base_url=f"http://server-{uuid.uuid4().hex}")
        self.doors, self.refuse, self.delay = doors, set(refuse), delay
        self.lock = threading.Lock()
        self.log: list[tuple] = []
        self.rows: dict[tuple, str] = {}
        self.names: dict[str, tuple[str, str]] = {}
        self.in_flight = self.peak = 0
        self.many = self.confirms = self.singles = 0
        self.direct_asks: list[bool] = []
        self.single_direct: list[bool] = []
        #: The storage host a direct presign answers with (None: the relay's).
        self.direct_host: str | None = None
        #: Hosts a PUT cannot connect to (an egress allowlist).
        self.unreachable: set[str] = set()
        self.put_hosts: list[str] = []
        self.transport = SimpleNamespace(request=self._request, put_file=self._put_file)

    def _note(self, *entry) -> None:
        with self.lock:
            self.log.append(entry)

    def _row(self, run: str, name: str, digest: str) -> str:
        with self.lock:
            aid = self.rows.setdefault((run, name, digest), f"a-{len(self.rows)}")
            self.names[aid] = (name, digest)
            return aid

    def _artifact(self, aid: str) -> dict:
        name, digest = self.names[aid]
        return {
            "id": aid, "name": name, "status": "complete", "content_hash": digest,
            "uri": f"r2://bucket/{digest}", "is_reference": False,
        }

    def _body(self, name: str) -> None:
        with self.lock:
            self.in_flight += 1
            self.peak = max(self.peak, self.in_flight)
        try:
            time.sleep(self.delay)
            self._note("put", name)
        finally:
            with self.lock:
                self.in_flight -= 1

    # -- the many-file doors -------------------------------------------------
    def presign_run_uploads(self, run_id, items, *, direct=False):
        with self.lock:
            self.many += 1
            self.direct_asks.append(direct)
        if not self.doors:
            raise errors.NotFoundError("Not Found", status=404, detail="Not Found")
        answers = []
        for item in items:
            self._note("presign", item["name"])
            if item["name"] in self.refuse:
                answers.append({"status": 422, "detail": "span_id not found for this run"})
                continue
            aid = self._row(run_id, item["name"], item["content_hash"])
            host = self.direct_host if (direct and self.direct_host) else "api.test"
            answers.append(
                {"status": 201, "artifact_id": aid, "have": False,
                 "upload_url": f"https://{host}/{aid}", "upload_headers": {}}
            )
        return answers

    def _put_file(self, url, path, *, content_type=None, headers=None):
        host = url.split("/")[2]
        with self.lock:
            self.put_hosts.append(host)
        if host in self.unreachable:
            try:
                raise ConnectError(f"[Errno -2] Name or service not known: {host}")
            except ConnectError as cause:
                raise errors.TransportError(f"PUT {host}: {cause}") from cause
        self._body(self.names[url.rsplit("/", 1)[1]][0])

    def confirm_uploads(self, artifact_ids):
        with self.lock:
            self.confirms += 1
        out = []
        for aid in artifact_ids:
            self._note("confirm", self.names[aid][0])
            out.append({"artifact_id": aid, "status": 200, "artifact": self._artifact(aid)})
        return out

    # -- the per-row path ------------------------------------------------------
    def upload_fingerprinted(self, anchor, anchor_id, name, path, *, digest, size, direct=False, **_kw):
        with self.lock:
            self.singles += 1
            self.single_direct.append(direct)
        self._note("presign", name)
        if name in self.refuse:
            raise errors.ValidationError("span_id not found for this run", status=422)
        aid = self._row(anchor_id, name, digest)
        self._body(name)
        self._note("confirm", name)
        return self._artifact(aid)

    def _request(self, method, path, *, json_body=None, **_kw):
        self._note("http", method, path)
        return SimpleNamespace(content=b"{}", json=lambda: {})

    def first(self, *entry) -> int:
        return self.log.index(entry)


def upload(queue, tmp_path, name, body=None):
    src = tmp_path / f"src-{uuid.uuid4().hex}"
    src.write_bytes(body if body is not None else name.encode())
    return queue.append_upload(
        anchor="run", anchor_id=RUN, name=name, src_path=str(src), run_ref=RUN, inline_hash=True,
    )


def metric(queue, step):
    return queue.append_http(
        "POST", f"/v1/runs/{RUN}/metrics",
        {"points": [{"key": "loss", "value": 1.0, "step_index": step}]}, run_ref=RUN,
    )


def run_drain(queue, server):
    return drain(queue, client_factory=lambda _context: server)


def test_a_runs_queued_uploads_go_up_together(queue, tmp_path):
    names = [f"out/file{i}.txt" for i in range(20)]
    for name in names:
        upload(queue, tmp_path, name)
    server = Server()
    report = run_drain(queue, server)
    assert report.delivered == 20
    assert queue.pending() == []
    assert sorted(n for kind, n in server.log if kind == "confirm") == sorted(names)
    # One presign and one confirm request per chunk of 8 (presigned links are
    # short-lived, and a window's chunks go at once), not one of each per file.
    assert server.many == 3 and server.confirms == 3 and server.singles == 0
    assert server.peak > 1, "the PUTs were still one at a time"


def test_metric_points_between_uploads_do_not_end_the_window(queue, tmp_path):
    for i in range(6):
        upload(queue, tmp_path, f"ckpt{i}.pt")
        metric(queue, i)
    server = Server()
    assert run_drain(queue, server).delivered == 12
    assert server.many == 1 and server.singles == 0
    # The metrics themselves still go in their own order.
    metric_posts = [entry for entry in server.log if entry[0] == "http"]
    assert len(metric_posts) >= 1 and queue.pending() == []


def test_an_upload_never_lands_before_an_earlier_op_of_its_run(queue, tmp_path):
    """A span its upload cites, a reference row of the same name: any op that
    is not an upload or a metric point ends the run's window."""
    upload(queue, tmp_path, "a.txt")
    upload(queue, tmp_path, "b.txt")
    queue.append_http("POST", f"/v1/runs/{RUN}/spans", {"spans": []}, run_ref=RUN)
    upload(queue, tmp_path, "c.txt")
    server = Server()
    assert run_drain(queue, server).delivered == 4
    span = server.first("http", "POST", f"/v1/runs/{RUN}/spans")
    assert server.first("presign", "c.txt") > span
    assert server.first("confirm", "a.txt") < span and server.first("confirm", "b.txt") < span


def test_two_versions_of_one_file_land_in_queue_order(queue, tmp_path):
    upload(queue, tmp_path, "model.pt", b"version one")
    upload(queue, tmp_path, "other.pt")
    upload(queue, tmp_path, "model.pt", b"version two")
    server = Server()
    assert run_drain(queue, server).delivered == 3
    confirms = [n for kind, n in server.log if kind == "confirm"]
    presigns = [i for i, entry in enumerate(server.log) if entry == ("presign", "model.pt")]
    first_confirm = server.first("confirm", "model.pt")
    assert len(presigns) == 2 and presigns[1] > first_confirm
    assert confirms.count("model.pt") == 2


def test_the_close_waits_for_the_uploads_before_it_and_those_after_it_wait_for_it(queue, tmp_path):
    upload(queue, tmp_path, "a.txt")
    upload(queue, tmp_path, "b.txt")
    queue.append_http("PATCH", f"/v1/runs/{RUN}", {"status": "completed"}, run_ref=RUN)
    upload(queue, tmp_path, "late.txt")
    server = Server()
    assert run_drain(queue, server).delivered == 4
    close = server.first("http", "PATCH", f"/v1/runs/{RUN}")
    assert server.first("confirm", "a.txt") < close and server.first("confirm", "b.txt") < close
    assert server.first("presign", "late.txt") > close


def test_a_server_without_the_doors_still_gets_every_file_in_parallel(queue, tmp_path):
    for i in range(8):
        upload(queue, tmp_path, f"f{i}.txt")
    server = Server(doors=False)
    assert run_drain(queue, server).delivered == 8
    assert server.singles == 8 and server.peak > 1
    # Remembered for the process: the next window does not ask again.
    for i in range(8, 12):
        upload(queue, tmp_path, f"f{i}.txt")
    assert run_drain(queue, server).delivered == 4
    assert server.many == 1


def test_a_file_the_batch_refuses_is_sent_alone_and_classified_there(queue, tmp_path):
    for name in ("ok1.txt", "bad.txt", "ok2.txt"):
        upload(queue, tmp_path, name)
    server = Server(refuse=("bad.txt",))
    report = run_drain(queue, server)
    assert report.delivered == 2
    # The refused one went once more alone, through the per-row path, which
    # decided its fate the way it always has (a dead letter for a 422).
    assert server.singles == 1
    assert report.dead_lettered == 1 and queue.pending() == []


def test_a_window_whose_ops_were_not_settled_replays_without_new_rows(queue, tmp_path):
    """A crash after the bytes landed and before the op files went: the next
    pass sends the same files again, and the server's identity gives back the
    same artifacts -- no second row, nothing lost."""
    for i in range(5):
        upload(queue, tmp_path, f"f{i}.txt")
    server = Server()
    entries = queue.pending()
    landed = jm._prefetch_uploads(
        queue, entries, lambda *_a, **_k: server, 8, None, skips=lambda *_: False
    )
    assert len(landed) == 5 and len(queue.pending()) == 5  # landed, not settled
    rows_before = dict(server.rows)
    assert run_drain(queue, server).delivered == 5
    assert server.rows == rows_before and queue.pending() == []


def test_a_large_upload_goes_alone_beside_the_window(queue, tmp_path, monkeypatch):
    monkeypatch.setattr(upload_many, "ITEM_MAX_BYTES", 64)
    upload(queue, tmp_path, "small1.txt")
    upload(queue, tmp_path, "small2.txt")
    upload(queue, tmp_path, "big.bin", b"x" * 1000)
    server = Server()
    assert run_drain(queue, server).delivered == 3
    assert server.many == 1 and server.singles == 1


def test_one_file_queued_under_two_names_for_its_run_never_races(queue, tmp_path):
    """A run's file can be queued under the run's uuid and under its petname
    (`artifact add --from-manifest`): the window treats them as one file."""
    upload(queue, tmp_path, "model.pt", b"version one")
    src = tmp_path / "v2"
    src.write_bytes(b"version two")
    queue.append_upload(
        anchor="run", anchor_id="my-run-petname", name="model.pt", src_path=str(src),
        run_ref=RUN, inline_hash=True,
    )
    upload(queue, tmp_path, "other.pt")
    server = Server()
    assert run_drain(queue, server).delivered == 3
    presigns = [i for i, entry in enumerate(server.log) if entry == ("presign", "model.pt")]
    assert len(presigns) == 2 and presigns[1] > server.first("confirm", "model.pt")


def test_two_encodings_of_one_name_are_one_file(queue, tmp_path):
    """The server keys a name by its NFC form, so `café` and `cafe` + U+0301
    are one file: the second waits for the first, as any second version does."""
    upload(queue, tmp_path, "café.pt", b"version one")
    upload(queue, tmp_path, "other.pt")
    upload(queue, tmp_path, "café.pt", b"version two")
    server = Server()
    assert run_drain(queue, server).delivered == 3
    assert server.first("presign", "café.pt") > server.first("confirm", "café.pt")


def test_a_credential_the_doors_are_closed_to_falls_back_and_is_remembered(queue, tmp_path):
    class ClosedToThisToken(Server):
        def presign_run_uploads(self, run_id, items, **_kw):
            with self.lock:
                self.many += 1
            raise errors.NotFoundError(
                "not found: this route is not available to run tokens", status=404,
                detail="not found: this route is not available to run tokens",
            )

    for i in range(6):
        upload(queue, tmp_path, f"f{i}.txt")
    server = ClosedToThisToken()
    assert run_drain(queue, server).delivered == 6
    assert server.singles == 6
    for i in range(6, 9):
        upload(queue, tmp_path, f"f{i}.txt")
    assert run_drain(queue, server).delivered == 3
    assert server.many == 1


def test_a_run_that_does_not_exist_is_the_ops_own_failure_not_a_closed_door(queue, tmp_path):
    class NoSuchRun(Server):
        def presign_run_uploads(self, run_id, items, **_kw):
            with self.lock:
                self.many += 1
            raise errors.NotFoundError("run not found", status=404, detail="run not found")

    for i in range(4):
        upload(queue, tmp_path, f"f{i}.txt")
    server = NoSuchRun()
    run_drain(queue, server)
    assert upload_many.available(server)


def test_a_closed_door_is_asked_again_after_its_ttl(queue, tmp_path, monkeypatch):
    for i in range(4):
        upload(queue, tmp_path, f"f{i}.txt")
    server = Server(doors=False)
    run_drain(queue, server)
    assert not upload_many.available(server)
    clock = upload_many.time.monotonic() + upload_many.MISSING_TTL_SECONDS + 1
    monkeypatch.setattr(upload_many.time, "monotonic", lambda: clock)
    assert upload_many.available(server)


def test_a_door_closed_to_one_credential_stays_open_to_another():
    closed = Server(doors=False)
    closed.settings.token = "probe_pat_one"
    other = SimpleNamespace(settings=SimpleNamespace(base_url=closed.settings.base_url, token="probe_pat_two"))
    with upload_many._missing_lock:
        upload_many._missing[upload_many._server(closed)] = upload_many.time.monotonic()
    assert not upload_many.available(closed)
    assert upload_many.available(other)


def test_a_refused_put_is_presigned_once_more_then_refused_for_good(tmp_path, monkeypatch):
    """A presigned link lives minutes. One that expired before its PUT, or that
    the store no longer takes, gets one fresh presign; the second refusal stands."""
    import hashlib

    from probe.sdk.client import Client
    from probe.sdk.config import Settings

    src = tmp_path / "ckpt.bin"
    src.write_bytes(b"weights")
    digest = hashlib.sha256(b"weights").hexdigest()
    client = Client(settings=Settings(base_url="http://server.test", token="t"), async_writes=False)
    presigns, puts = [], []

    def post(path, body=None, **_kw):
        if path.endswith("/uploads"):
            presigns.append(path)
            return {"artifact_id": "a-1", "have": False, "upload_url": f"https://r2.test/{len(presigns)}"}
        return {"id": "a-1", "status": "complete"}

    def put_file(url, path, **_kw):
        puts.append(url)
        if refuse_every or len(puts) == 1:
            raise errors.UploadRefused("upload refused (403): expired", status=403)

    monkeypatch.setattr(client.transport, "post", post)
    monkeypatch.setattr(client.transport, "put_file", put_file)
    refuse_every = False
    assert client.upload_fingerprinted("run", RUN, "ckpt.bin", str(src), digest=digest, size=7)["status"] == "complete"
    assert len(presigns) == 2 and puts == ["https://r2.test/1", "https://r2.test/2"]
    presigns.clear(), puts.clear()
    refuse_every = True
    with pytest.raises(errors.UploadRefused):
        client.upload_fingerprinted("run", RUN, "ckpt.bin", str(src), digest=digest, size=7)
    assert len(presigns) == 2 and len(puts) == 2


def test_a_drain_at_interpreter_exit_sends_every_upload_serially(queue, tmp_path, monkeypatch):
    """The close a script's exit runs drains after the interpreter stopped taking
    new thread-pool work: the window steps aside and the serial pass sends all."""
    import concurrent.futures

    class ShutDown(concurrent.futures.ThreadPoolExecutor):
        def submit(self, *args, **kwargs):
            raise RuntimeError("cannot schedule new futures after interpreter shutdown")

    monkeypatch.setattr(jm, "ThreadPoolExecutor", ShutDown)
    for i in range(5):
        upload(queue, tmp_path, f"f{i}.txt")
    server = Server()
    assert run_drain(queue, server).delivered == 5
    assert server.singles == 5 and queue.pending() == []


def test_the_window_asks_for_direct_links_and_puts_straight_to_storage(queue, tmp_path):
    for i in range(4):
        upload(queue, tmp_path, f"f{i}.txt")
    server = Server()
    server.direct_host = "acct.r2.cloudflarestorage.com"
    assert run_drain(queue, server).delivered == 4
    assert server.direct_asks == [True] and server.singles == 0
    assert set(server.put_hosts) == {"acct.r2.cloudflarestorage.com"}


def test_a_storage_host_this_machine_cannot_reach_falls_back_to_the_relay_for_good(queue, tmp_path):
    """Behind an egress allowlist: the direct PUTs cannot connect, each file goes
    again alone through the per-op path (no direct ask: the relay), and this
    process stops asking for direct links."""
    for i in range(4):
        upload(queue, tmp_path, f"f{i}.txt")
    server = Server()
    server.direct_host = "acct.r2.cloudflarestorage.com"
    server.unreachable.add("acct.r2.cloudflarestorage.com")
    report = run_drain(queue, server)
    assert report.delivered == 4 and queue.pending() == []
    # Every file went again through the relay: alone, or in the next window,
    # which no longer asks for direct links.
    assert server.direct_asks[0] is True and False in server.direct_asks
    assert "acct.r2.cloudflarestorage.com" not in server.put_hosts[-1]
    assert not upload_many.direct_wanted(server)
    singles, asks = server.singles, len(server.direct_asks)
    for i in range(4, 8):
        upload(queue, tmp_path, f"f{i}.txt")
    assert run_drain(queue, server).delivered == 4
    assert server.direct_asks[asks:] == [False] and server.singles == singles



def test_without_the_doors_the_window_sends_each_file_on_its_own_worker_asking_for_direct(queue, tmp_path, monkeypatch):
    """`PROBE_UPLOAD_MANY=0`: a window's uploads go one per worker, eight in
    flight, each asking for a direct link."""
    monkeypatch.setenv("PROBE_UPLOAD_MANY", "0")
    for i in range(10):
        upload(queue, tmp_path, f"f{i}.txt")
    server = Server(delay=0.05)
    assert run_drain(queue, server).delivered == 10
    assert server.many == 0 and server.singles == 10 and server.peak > 1
    assert set(server.single_direct) == {True}


def test_a_direct_link_this_machine_cannot_reach_is_sent_again_through_the_relay(tmp_path, monkeypatch):
    import hashlib

    from probe.sdk.client import Client
    from probe.sdk.config import Settings

    src = tmp_path / "ckpt.bin"
    src.write_bytes(b"weights")
    digest = hashlib.sha256(b"weights").hexdigest()
    client = Client(settings=Settings(base_url="http://api.test", token="t-direct"), async_writes=False)
    asked, puts = [], []

    def post(path, body=None, *, extra_headers=None, **_kw):
        if path.endswith("/uploads"):
            direct = bool(extra_headers)
            asked.append(direct)
            host = "acct.r2.cloudflarestorage.com" if direct else "api.test"
            return {"artifact_id": "a-1", "have": False, "upload_url": f"https://{host}/k"}
        return {"id": "a-1", "status": "complete"}

    def put_file(url, path, **_kw):
        puts.append(url)
        if "r2.cloudflarestorage.com" in url:
            try:
                raise ConnectError("[Errno -2] Name or service not known")
            except ConnectError as cause:
                raise errors.TransportError("PUT acct.r2.cloudflarestorage.com") from cause

    monkeypatch.setattr(client.transport, "post", post)
    monkeypatch.setattr(client.transport, "put_file", put_file)
    out = client.upload_fingerprinted("run", RUN, "ckpt.bin", str(src), digest=digest, size=7, direct=True)
    assert out["status"] == "complete"
    assert asked == [True, False] and puts == ["https://acct.r2.cloudflarestorage.com/k", "https://api.test/k"]
    assert not upload_many.direct_wanted(client)


def test_uploads_queued_behind_a_runs_first_write_still_go_up_together(queue, tmp_path, monkeypatch):
    """Prod, 0.343.0: a run's queue opens with its own writes (metadata, a
    span), which end the window at position 0. The window was looked at again
    only 32 ops later, so the first 30 uploads went one by one. It is looked at
    again right after the write that held it."""
    queue.append_http("PATCH", f"/v1/runs/{RUN}", {"meta": {"host": "x"}}, run_ref=RUN)
    queue.append_http("POST", f"/v1/runs/{RUN}/spans", {"spans": []}, run_ref=RUN)
    for i in range(40):
        upload(queue, tmp_path, f"f{i}.txt")
    server = Server(delay=0.02)
    calls = []
    real = jm._execute

    def execute(journal, client, path, op, *a, **k):
        import threading as _t

        calls.append((op.get("kind"), _t.current_thread() is _t.main_thread()))
        return real(journal, client, path, op, *a, **k)

    monkeypatch.setattr(jm, "_execute", execute)
    assert run_drain(queue, server).delivered == 42
    serial_uploads = sum(1 for kind, main in calls if kind == "upload" and main)
    assert serial_uploads == 0, f"{serial_uploads} uploads went one by one on the drain's thread"
