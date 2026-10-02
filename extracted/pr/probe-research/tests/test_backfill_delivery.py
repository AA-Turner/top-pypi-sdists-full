"""Receipt-required artifacts use the existing uploader across crash boundaries."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from types import SimpleNamespace

import httpx
import pytest

from probe.sdk import journal as jm
from probe.sdk.client import Client
from probe.sdk.config import Settings
from probe.sdk.journal import Journal, drain
from probe.sdk.transport import Transport


@pytest.fixture(autouse=True)
def isolated(monkeypatch, tmp_path):
    monkeypatch.setenv("PROBE_CONFIG_PATH", str(tmp_path / "config.json"))
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))
    monkeypatch.delenv("PROBE_ATTRIBUTION", raising=False)
    monkeypatch.setattr(jm, "MIN_FREE_BYTES", 0)


@pytest.fixture
def queue(tmp_path):
    return Journal.for_receipts(
        tmp_path / "outbox", context={"name": None, "base_url": "http://test"}
    )


class Store:
    def __init__(self):
        self.records = {}
        self.calls = []
        self.transport = SimpleNamespace(request=self.reference)

    def upload_fingerprinted(self, anchor, anchor_id, name, path, *, digest, size, **kwargs):
        data = Path(path).read_bytes()
        assert hashlib.sha256(data).hexdigest() == digest
        assert len(data) == size
        self.calls.append((name, data))
        key = (anchor, anchor_id, name, digest)
        return self.records.setdefault(
            key,
            {
                "id": f"artifact-{len(self.records)}",
                "name": name,
                "status": "complete",
                "uri": f"r2://artifacts/{digest}",
                "content_hash": digest,
                "size_bytes": size,
                "is_reference": False,
            },
        )

    def reference(self, method, path, *, json_body):
        self.calls.append((method, path))
        key = (path, json_body["name"], json_body["uri"])
        return self.records.setdefault(
            key,
            {
                **json_body,
                "id": f"artifact-{len(self.records)}",
                "status": "complete",
            },
        )


def enqueue(queue, tmp_path, **kwargs):
    source = tmp_path / "source.py"
    if not source.exists():
        source.write_bytes(b"original")
    return queue.append_upload(
        correlation="scope:file:v1",
        anchor="project",
        anchor_id="p1",
        name="src/source.py",
        src_path=str(source),
        **kwargs,
    )


def test_immutable_upload_receipt_and_replay(queue, tmp_path):
    expected = hashlib.sha256(b"original").hexdigest()
    queued = enqueue(queue, tmp_path, expected_content_hash=expected)
    assert queued["state"] == "queued" and queued["staged"]
    (tmp_path / "source.py").write_bytes(b"new bytes")
    store = Store()
    assert drain(queue, client_factory=lambda _: store).delivered == 1
    receipt = queue.receipt("scope:file:v1")
    assert receipt["artifact_id"] == "artifact-0"
    assert receipt["content_hash"] == expected
    assert receipt["readable"] and receipt["status"] == "complete"
    assert receipt["name"] == "src/source.py"
    replay = enqueue(queue, tmp_path, expected_content_hash=expected)
    assert replay == receipt
    assert len(store.records) == 1 and len(queue.pending()) == 0


def test_correlation_rejects_changed_request(queue, tmp_path):
    enqueue(queue, tmp_path, notes="original")
    with pytest.raises(ValueError, match="different immutable request"):
        enqueue(queue, tmp_path, notes="changed")
    assert len(queue.pending()) == 1


class Crash(BaseException):
    pass


def test_crash_after_intent_before_operation_preserves_snapshot(queue, tmp_path, monkeypatch):
    real = jm.write_text_atomic

    def crash_on_op(path, *args, **kwargs):
        if Path(path).parent == queue.ops_dir:
            raise Crash()
        return real(path, *args, **kwargs)

    with monkeypatch.context() as m:
        m.setattr(jm, "write_text_atomic", crash_on_op)
        with pytest.raises(Crash):
            enqueue(queue, tmp_path)
    assert not queue.pending() and queue.recovery_file.exists()
    (tmp_path / "source.py").unlink()
    queue.gc_blobs()
    assert len(list(queue.blobs_dir.iterdir())) == 1
    restarted = Journal(queue.dir)
    store = Store()
    assert drain(restarted, client_factory=lambda _: store).delivered == 1
    assert store.calls == [("src/source.py", b"original")]
    assert restarted.receipt("scope:file:v1")["artifact_id"] == "artifact-0"


def test_remote_acceptance_before_receipt_replays_idempotently(queue, tmp_path, monkeypatch):
    enqueue(queue, tmp_path)
    store = Store()

    def fail_receipt(conn):
        raise OSError("disk full during receipt")

    with monkeypatch.context() as m:
        m.setattr(Journal, "_commit_receipt_index", staticmethod(fail_receipt))
        result = drain(queue, client_factory=lambda _: store)
    assert result.delivered == 0 and result.remaining == 1
    assert queue.receipt("scope:file:v1") is None
    assert drain(queue, client_factory=lambda _: store).delivered == 1
    assert len(store.records) == 1 and len(store.calls) == 2


def test_receipt_before_operation_removal_does_not_repeat_remote_write(
    queue, tmp_path, monkeypatch
):
    enqueue(queue, tmp_path)
    real = Path.unlink
    store = Store()

    def crash_delete(path, *args, **kwargs):
        if path.parent == queue.ops_dir:
            raise Crash()
        return real(path, *args, **kwargs)

    with monkeypatch.context() as m:
        m.setattr(Path, "unlink", crash_delete)
        with pytest.raises(Crash):
            drain(queue, client_factory=lambda _: store)
    assert queue.receipt("scope:file:v1") is not None and queue.pending()
    assert drain(queue, client_factory=lambda _: store).delivered == 1
    assert len(store.calls) == 1


def test_reference_receipt_retains_id_uri_and_pointer_mode(queue):
    op = queue.append_http(
        "POST",
        "/v1/projects/p1/artifacts",
        {
            "name": "weights.pt",
            "uri": "file:///mnt/weights.pt",
            "is_reference": True,
        },
        correlation="reference:v1",
    )
    store = Store()
    assert drain(queue, client_factory=lambda _: store).delivered == 1
    receipt = queue.receipt("reference:v1")
    assert receipt["op_id"] == op and receipt["artifact_id"] == "artifact-0"
    assert receipt["uri"] == "file:///mnt/weights.pt"
    assert receipt["is_reference"] and receipt["mode"] == "reference"
    assert not receipt["readable"]


def test_incomplete_server_artifact_is_not_a_delivery(queue, tmp_path):
    enqueue(queue, tmp_path)
    store = Store()
    real = store.upload_fingerprinted
    store.upload_fingerprinted = lambda *a, **kw: {**real(*a, **kw), "status": "pending"}
    report = drain(queue, client_factory=lambda _: store)
    assert report.delivered == 0 and report.remaining == 1
    assert queue.receipt("scope:file:v1") is None


@pytest.mark.parametrize("scenario", ["disk", "hash", "mutation"])
def test_failed_staging_never_queues_future_source_bytes(queue, tmp_path, monkeypatch, scenario):
    if scenario == "disk":
        monkeypatch.setattr(queue, "_staging_headroom", lambda _: "disk full")
    elif scenario == "mutation":
        real = jm.snapshot_file

        def mutate(src, dst):
            real(src, dst)
            Path(src).write_bytes(b"concurrent mutation")

        monkeypatch.setattr(jm, "snapshot_file", mutate)
    kwargs = {"expected_content_hash": "0" * 64} if scenario == "hash" else {}
    with pytest.raises((ValueError, jm.OutboxFull)):
        enqueue(queue, tmp_path, **kwargs)
    assert not queue.pending() and queue.receipt("scope:file:v1") is None
    assert not list(queue.blobs_dir.iterdir())


def test_old_worker_cannot_enumerate_receipt_namespace_and_new_status_counts_it(queue, tmp_path):
    enqueue(queue, tmp_path)
    old = Journal(queue.dir.parent)
    # This is the old worker's exact enumeration contract: <root>/ops/*.json.
    assert old.pending() == []
    status = Journal.read_status(old.dir)
    assert status["pending"] == status["delivery_pending"] == 1
    assert status["pending_bytes"] == len(b"original")
    old.pause()
    assert drain(old, client_factory=lambda _: Store()).remaining == 1
    old.resume()
    assert drain(old, client_factory=lambda _: Store()).delivered == 1


def test_pending_ceiling_includes_both_namespaces(queue, tmp_path, monkeypatch):
    monkeypatch.setattr(jm, "MAX_PENDING_OPS", 1)
    old = Journal(queue.dir.parent)
    old.append_http("POST", "/v1/runs", {"name": "live"})
    with pytest.raises(jm.OutboxFull):
        enqueue(queue, tmp_path)
    assert not queue.pending()


def test_old_worker_lease_does_not_suppress_receipt_worker(queue, tmp_path, monkeypatch):
    import fcntl
    from probe.sdk import outbox_worker as worker

    enqueue(queue, tmp_path)
    calls = []
    monkeypatch.setattr(
        worker.subprocess,
        "Popen",
        lambda argv, **kw: calls.append(argv) or SimpleNamespace(poll=lambda: None),
    )
    with (queue.dir.parent / ".worker.lock").open("a+") as lease:
        fcntl.flock(lease.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        assert worker.maybe_spawn(str(queue.dir.parent))
    assert len(calls) == 1 and calls[0][-1] == str(queue.dir)


def test_explicit_attribution_survives_queue_restart_and_preserves_transcript_payload(
    tmp_path, monkeypatch
):
    from probe.sdk import transport as tm

    monkeypatch.setattr(
        tm,
        "agent_session_headers",
        lambda: {
            "X-Probe-Agent": "claude_code",
            "X-Probe-Agent-Session": "ambient-session",
        },
    )
    seen = []

    def handle(request):
        seen.append(request)
        body = json.loads(request.content)
        return httpx.Response(200, json={**body, "id": "artifact-1", "status": "complete"})

    settings = Settings(base_url="http://test", token="test-token")
    live_transport = Transport(
        settings, client=httpx.Client(base_url="http://test", transport=httpx.MockTransport(handle))
    )
    producer = Client(
        settings=settings,
        transport=live_transport,
        spool_dir=tmp_path / "outbox",
        async_writes=False,
        attribution="backfill",
    )
    producer.transport.post("/v1/projects", {"name": "import"})
    queued = producer.enqueue_artifact_reference(
        correlation="scope:reference",
        anchor="project",
        anchor_id="p1",
        name="x.pt",
        uri="file:///mnt/x.pt",
    )
    assert queued["op_id"]
    # A new process with ambient attribution must honor the persisted operation.
    replay_transport = Transport(
        settings, client=httpx.Client(base_url="http://test", transport=httpx.MockTransport(handle))
    )
    drainer = Client(
        settings=settings,
        transport=replay_transport,
        async_writes=False,
        spool_dir=tmp_path / "other",
    )
    assert drain(Journal(tmp_path / "outbox"), client_factory=lambda _: drainer).delivered == 1
    assert all(
        "x-probe-agent-session" not in r.headers and "x-probe-agent" not in r.headers for r in seen
    )
    producer.transport.post(
        "/v1/ingestion/sessions", {"session_id": "native-history-id", "source": "claude_code"}
    )
    assert json.loads(seen[-1].content)["session_id"] == "native-history-id"
    assert seen[-1].headers["authorization"] == "Bearer test-token"
    drainer.transport.post("/v1/projects", {"name": "live"})
    assert seen[-1].headers["x-probe-agent-session"] == "ambient-session"


def test_append_status_retry_keeps_one_intent_and_operation(queue, tmp_path, monkeypatch):
    real = queue._write_status_locked
    attempts = 0

    def fail_once(**kwargs):
        nonlocal attempts
        attempts += 1
        if attempts == 1:
            raise OSError("status write failed after operation committed")
        return real(**kwargs)

    monkeypatch.setattr(queue, "_write_status_locked", fail_once)
    queued = enqueue(queue, tmp_path)
    # The operation committed before its status write failed, so the append
    # succeeds without retrying (status.json is bookkeeping the drain rebuilds;
    # test_outbox_low_disk.py has why a raise there lost writes).
    assert attempts == 1
    assert len(queue.pending()) == 1
    assert queue.pending()[0][1]["op_id"] == queued["op_id"]
    assert drain(queue, client_factory=lambda _: Store()).delivered == 1


@pytest.mark.parametrize(
    "field,value",
    [
        ("name", "different"),
        ("content_hash", "0" * 64),
        ("size_bytes", 900),
        ("uri", None),
        ("is_reference", True),
    ],
)
def test_upload_receipt_rejects_mismatched_remote_record(queue, tmp_path, field, value):
    enqueue(queue, tmp_path)
    store = Store()
    real = store.upload_fingerprinted
    store.upload_fingerprinted = lambda *a, **kw: {**real(*a, **kw), field: value}
    assert drain(queue, client_factory=lambda _: store).delivered == 0
    assert queue.receipt("scope:file:v1") is None


def test_failed_delivery_retry_and_discard_include_fenced_queue(queue, tmp_path):
    enqueue(queue, tmp_path)
    store = Store()
    real = store.upload_fingerprinted

    def reject(*args, **kwargs):
        raise jm.errors.ValidationError("rejected", status=422)

    store.upload_fingerprinted = reject
    root = Journal(queue.dir.parent)
    assert drain(root, client_factory=lambda _: store).dead_lettered == 1
    assert queue.delivery_state("scope:file:v1")["state"] == "failed"
    assert root.retry_failed() == 1
    assert drain(root, client_factory=lambda _: store).dead_lettered == 1
    assert root.discard_failed() == 1
    assert queue.delivery_state("scope:file:v1")["state"] == "discarded"
    assert not list(queue.blobs_dir.iterdir())
    store.upload_fingerprinted = real
    assert drain(root, client_factory=lambda _: store).delivered == 0
    assert enqueue(queue, tmp_path)["state"] == "discarded"
    assert queue.receipt("scope:file:v1") is None


def test_environment_attribution_applies_to_normal_queued_operations(tmp_path, monkeypatch):
    monkeypatch.setenv("PROBE_ATTRIBUTION", "backfill")
    client = Client(
        settings=Settings(base_url="http://test", token="test-token"),
        spool_dir=tmp_path / "outbox",
        async_writes=True,
        auto_drain=False,
    )
    client.write("POST", "/v1/projects", {"name": "historical"})
    assert client.transport.attribution == "backfill"
    assert client.journal.pending()[0][1]["attribution"] == "backfill"
    client.transport.close()


def test_admitted_intent_recovery_can_drain_below_new_enqueue_disk_floor(queue, tmp_path, monkeypatch):
    queued = enqueue(queue, tmp_path)
    queue.pending()[0][0].unlink()
    (tmp_path / "source.py").unlink()
    monkeypatch.setattr(jm, "MIN_FREE_BYTES", 1 << 100)
    report = drain(Journal(queue.dir.parent), client_factory=lambda _: Store())
    assert report.delivered == 1
    assert queue.receipt("scope:file:v1")["op_id"] == queued["op_id"]


def test_reference_replay_after_remote_acceptance_keeps_artifact_identity(queue, monkeypatch):
    kwargs = {"correlation": "reference:v1"}
    body = {"name": "x.pt", "uri": "file:///mnt/x.pt", "is_reference": True}
    op_id = queue.append_http("POST", "/v1/projects/p1/artifacts", body, **kwargs)
    store = Store()

    def reject_receipt(conn):
        raise OSError("crash after remote acceptance")

    with monkeypatch.context() as patch:
        patch.setattr(Journal, "_commit_receipt_index", staticmethod(reject_receipt))
        assert drain(queue, client_factory=lambda _: store).delivered == 0
    assert queue.append_http("POST", "/v1/projects/p1/artifacts", body, **kwargs) == op_id
    assert drain(queue, client_factory=lambda _: store).delivered == 1
    assert len(store.records) == 1
    assert queue.receipt("reference:v1")["artifact_id"] == "artifact-0"


@pytest.mark.parametrize("auto_drain", [True, False])
def test_explicit_enqueue_wakes_sync_clients_but_receipt_reads_do_not(tmp_path, monkeypatch, auto_drain):
    from probe.sdk import outbox_worker

    kicks = []
    monkeypatch.setattr(outbox_worker, "maybe_spawn", lambda directory: kicks.append(directory) or True)
    client = Client(settings=Settings(base_url="http://test", token="test-token"),
                    spool_dir=tmp_path / "outbox", async_writes=False, auto_drain=auto_drain)
    client.enqueue_artifact_reference(correlation="ref", anchor="project", anchor_id="p1",
                                      name="x", uri="file:///x")
    assert len(kicks) == int(auto_drain)
    assert client.delivery_receipt("ref") is None
    assert len(kicks) == int(auto_drain)
    client.close()


def test_recovery_does_not_clear_marker_for_append_after_directory_snapshot(queue, tmp_path, monkeypatch):
    enqueue(queue, tmp_path)
    real = queue._read_record
    injected = False

    def append_during_scan(path):
        nonlocal injected
        record = real(path)
        if Path(path).parent == queue.intents_dir and not injected:
            injected = True
            queue.append_http("POST", "/v1/projects/p1/artifacts", {
                "name": "second", "uri": "file:///second", "is_reference": True,
            }, correlation="second")
            for op_path, op in queue.pending():
                if op["correlation"] == "second":
                    op_path.unlink()
        return record

    monkeypatch.setattr(queue, "_read_record", append_during_scan)
    queue.recover_intents()
    assert queue.recovery_file.exists()
    assert queue.delivery_state("second")["state"] == "pending"
    assert queue.recover_intents() == 1
    assert not queue.recovery_file.exists()
    assert queue.delivery_state("second")["state"] == "queued"


def test_worker_retries_recovery_marker_before_empty_exit(queue, monkeypatch):
    from probe.sdk import outbox_worker

    queue._receipt_dirs()
    calls = []

    def drain_with_late_intent(journal, **_kwargs):  # skip_runs= (plan 1.6)
        calls.append(True)
        if len(calls) == 1:
            queue.recovery_file.write_text("late intent")
        else:
            queue.recovery_file.unlink(missing_ok=True)
        return jm.DrainReport()

    monkeypatch.setattr(jm, "drain", drain_with_late_intent)
    monkeypatch.setattr(outbox_worker, "_EXIT_GRACE_SECONDS", 0)
    assert outbox_worker.run(str(queue.dir)) == 0
    assert len(calls) == 2


@pytest.mark.parametrize(
    ("anchor", "expected"),
    [
        ("run", "/v1/runs/a1/artifacts"),
        # An experiment IS a project: `/v1/experiments/*` answers 410 since the
        # 5b cut, so a reference journaled there dead-letters on drain.
        ("experiment", "/v1/projects/a1/artifacts"),
        ("project", "/v1/projects/a1/artifacts"),
    ],
)
def test_a_reference_is_delivered_at_the_address_that_survives_the_cut(
    tmp_path, anchor, expected
):
    seen = []

    def handle(request):
        seen.append(request.url.path)
        body = json.loads(request.content)
        return httpx.Response(200, json={**body, "id": "artifact-1", "status": "complete"})

    settings = Settings(base_url="http://test", token="test-token")

    def client(spool):
        transport = Transport(
            settings,
            client=httpx.Client(base_url="http://test", transport=httpx.MockTransport(handle)),
        )
        return Client(settings=settings, transport=transport, spool_dir=spool, async_writes=False)

    producer = client(tmp_path / "outbox")
    producer.enqueue_artifact_reference(
        correlation=f"ref:{anchor}", anchor=anchor, anchor_id="a1", name="x.pt", uri="file:///x.pt"
    )
    drainer = client(tmp_path / "other")
    assert drain(Journal(tmp_path / "outbox"), client_factory=lambda _: drainer).delivered == 1
    assert seen == [expected]
    assert not any(path.startswith("/v1/experiments") for path in seen)
