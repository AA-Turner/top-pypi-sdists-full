"""Goldens for one drain pass end to end: journal -> drain -> op handlers -> Transport -> HTTP.

Each scenario queues ops, scripts the server's answers over the fake API and records the requests,
the retry pauses, the DrainReport, the callbacks and the outbox tree after the pass."""

from __future__ import annotations

import os

import httpx
import pytest

from probe.sdk.delivery.journal.journal import Journal
from probe.sdk.delivery.outbox.drain.drain import drain
from tests.conftest import make_client, open_run
from tests.sdk.delivery.goldens.recorder import (
    HttpScript,
    Normaliser,
    check,
    describe_error,
    dump_tree,
    record_transport_sleeps,
)

METRIC = "/v1/runs/{run}/metrics"


@pytest.fixture(autouse=True)
def _isolated(monkeypatch, tmp_path):
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))
    monkeypatch.setenv("PROBE_CONFIG_PATH", str(tmp_path / "config" / "probe.json"))
    monkeypatch.delenv("PROBE_TOKEN", raising=False)
    monkeypatch.delenv("PROBE_ASYNC", raising=False)
    # Per-process memory of which servers take /steps/batch: each scenario asks its own.
    from probe.sdk.delivery.outbox.drain import coalesce

    monkeypatch.setattr(coalesce, "_STEPS_BATCH_KNOWN", {})


class World:
    """One fake server, one outbox and the recorders a scenario writes into."""

    def __init__(self, app, tmp_path, monkeypatch):
        self.app = app
        self.tmp = tmp_path
        self.norm = Normaliser(tmp_path)
        self.runs = [self._seed(f"r{n}") for n in (1, 2)]
        self.http = HttpScript(app.handler, self.norm)
        monkeypatch.setattr(app, "handler", self.http)
        self.sleeps: list[float] = []
        record_transport_sleeps(monkeypatch, self.sleeps)
        self.journal = Journal(tmp_path / "outbox")
        self.errors: list[dict] = []
        self.delivered: list = []

    def _seed(self, name: str) -> str:
        client = make_client(self.app)
        try:
            return open_run(client, experiment="e", name=name).id
        finally:
            client.close()

    def metric(self, run: str, step: int, journal: Journal | None = None, **kw) -> str:
        body = {"points": [{"key": "loss", "kind": "model", "value": float(step), "step_index": step}]}
        return (journal or self.journal).append_http("POST", METRIC.format(run=run), body, **kw)

    def upload(self, run: str, name: str = "ckpt.bin", data: bytes = b"weights", **kw) -> dict:
        src = self.tmp / name
        src.write_bytes(data)
        kw.setdefault("inline_hash", True)
        return self.journal.append_upload(anchor="run", anchor_id=run, name=f"files/{name}", src_path=str(src),
                                          run_ref=run, **kw)

    def drain(self, journal: Journal | None = None, *, client=None, **kwargs) -> dict:
        own = client is None
        client = client or make_client(self.app)
        kwargs.setdefault("on_error", lambda exc: self.errors.append(describe_error(exc, self.norm)))
        kwargs.setdefault("on_delivered", lambda correlation: self.delivered.append(correlation))
        try:
            report = drain(journal or self.journal, client_factory=lambda ctx: client, **kwargs)
        finally:
            if own:
                client.close()
        return self.norm.value(report)

    def record(self, report: dict, journal: Journal | None = None) -> dict:
        journal = journal or self.journal
        return {
            "report": report,
            "requests": self.http.log,
            "sleeps": self.sleeps,
            "on_error": self.errors,
            "on_delivered": self.norm.value(self.delivered),
            "outbox": dump_tree(journal.dir, self.norm),
        }


@pytest.fixture
def world(app, tmp_path, monkeypatch):
    return World(app, tmp_path, monkeypatch)


def scenario_delivers_in_order(w: World) -> dict:
    for step in (1, 2, 3):
        w.metric(w.runs[0], step)
    return w.record(w.drain())


def scenario_two_runs_round_robin(w: World) -> dict:
    for step in (1, 2):
        w.metric(w.runs[0], step)
        w.metric(w.runs[1], step)
    w.journal.append_http("POST", f"/v1/runs/{w.runs[0]}/spans", {"spans": []})
    return w.record(w.drain())


def scenario_permanent_404_dead_letters_and_flows(w: World) -> dict:
    w.journal.append_http("POST", "/v1/runs/poisoned/badroute", {})
    w.metric(w.runs[0], 1)
    return w.record(w.drain())


def scenario_permanent_422_scripted(w: World) -> dict:
    w.http.answer("POST", r"/metrics$", (422, {"detail": "bad points"}))
    w.metric(w.runs[0], 1)
    w.metric(w.runs[1], 1)
    return w.record(w.drain())


def scenario_transient_503_stalls_only_its_run(w: World) -> dict:
    w.http.answer("POST", rf"/v1/runs/{w.runs[0]}/metrics$", 503, times=10)
    w.metric(w.runs[0], 1)
    w.metric(w.runs[0], 2)
    w.metric(w.runs[1], 1)
    return w.record(w.drain())


def scenario_retry_after_429(w: World) -> dict:
    w.http.answer("POST", r"/metrics$", (429, {"detail": "slow"}, {"Retry-After": "7"}), times=10)
    w.metric(w.runs[0], 1)
    return w.record(w.drain())


def scenario_auth_401_unstamped_stops_queue(w: World) -> dict:
    w.http.answer("POST", r"/metrics$", (401, {"detail": "invalid or revoked token"}), times=10)
    w.metric(w.runs[0], 1)
    w.metric(w.runs[1], 1)
    return w.record(w.drain())


def scenario_scope_403(w: World) -> dict:
    w.http.answer("POST", r"/metrics$", (403, {"detail": "insufficient scope: write required"}), times=10)
    w.metric(w.runs[0], 1)
    return w.record(w.drain())


def scenario_conflict_409_first_attempt_is_permanent(w: World) -> dict:
    w.http.answer("POST", r"/metrics$", (409, {"detail": {"existing_id": "abc"}}))
    w.metric(w.runs[0], 1)
    return w.record(w.drain())


def scenario_conflict_409_on_retry_is_delivered(w: World) -> dict:
    w.http.answer("POST", r"/metrics$", 503, times=1)
    w.http.answer("POST", r"/metrics$", (409, {"detail": {"existing_id": "abc"}}))
    w.metric(w.runs[0], 1)
    first = w.drain()
    return {"first": first, **w.record(w.drain())}


def scenario_unreachable_connect_error(w: World) -> dict:
    w.http.answer("POST", r"/metrics$", httpx.ConnectError("refused"), times=20)
    w.metric(w.runs[0], 1)
    w.metric(w.runs[1], 1)
    return w.record(w.drain())


def scenario_lost_responses_twice_is_unreachable(w: World) -> dict:
    w.http.answer("POST", r"/metrics$", httpx.ReadTimeout("no answer"), times=20)
    w.metric(w.runs[0], 1)
    w.metric(w.runs[1], 1)
    w.journal.append_http("POST", "/v1/runs/other/spans", {"spans": []})
    return w.record(w.drain())


def scenario_unknown_kind_waits_in_order(w: World) -> dict:
    w.metric(w.runs[0], 1)
    path, op = w.journal.pending()[0]
    op["kind"] = "teleport"
    path.write_text(__import__("json").dumps(op))
    w.metric(w.runs[0], 2)
    w.metric(w.runs[1], 1)
    return w.record(w.drain())


def scenario_run_ref_barrier(w: World) -> dict:
    w.metric(w.runs[0], 1)
    w.metric(w.runs[1], 1)
    w.metric(w.runs[0], 2)
    return w.record(w.drain(run_ref=w.runs[0]))


def scenario_only_ops(w: World) -> dict:
    w.metric(w.runs[0], 1)
    wanted = w.metric(w.runs[1], 1)
    w.metric(w.runs[0], 2)
    return w.record(w.drain(only_ops={wanted}))


def scenario_skip_runs(w: World) -> dict:
    w.metric(w.runs[0], 1)
    w.metric(w.runs[1], 1)
    return w.record(w.drain(skip_runs={w.runs[0]}))


def scenario_paused_outbox(w: World) -> dict:
    w.metric(w.runs[0], 1)
    w.journal.pause(hours=1)
    return w.record(w.drain())


def scenario_lock_busy(w: World) -> dict:
    from probe._shared import oscompat

    w.metric(w.runs[0], 1)
    w.journal._ensure()
    with w.journal.drain_lock.open("a+") as held:
        oscompat.flock(held.fileno(), oscompat.LOCK_EX | oscompat.LOCK_NB)
        report = w.drain(lock_timeout=0.05)
        oscompat.flock(held.fileno(), oscompat.LOCK_UN)
    return w.record(report)


def scenario_coalesced_metrics(w: World) -> dict:
    for step in range(1, 7):
        w.metric(w.runs[0], step)
    w.journal.append_http("PATCH", f"/v1/runs/{w.runs[0]}", {"status": "completed"})
    return w.record(w.drain())


def scenario_coalesced_batch_transient(w: World) -> dict:
    w.http.answer("POST", r"/metrics$", 500, times=1)
    for step in range(1, 5):
        w.metric(w.runs[0], step)
    return w.record(w.drain())


def scenario_coalesced_batch_permanent_splits(w: World) -> dict:
    w.http.answer("POST", r"/metrics$", (422, {"detail": "one bad point"}), times=1)
    for step in range(1, 5):
        w.metric(w.runs[0], step)
    return w.record(w.drain())


def scenario_close_after_writes(w: World) -> dict:
    w.metric(w.runs[0], 1)
    w.journal.append_http("POST", f"/v1/runs/{w.runs[0]}/finish", {"status": "completed"})
    w.metric(w.runs[1], 1)
    return w.record(w.drain())


def scenario_upload_delivers(w: World) -> dict:
    w.upload(w.runs[0])
    w.metric(w.runs[0], 1)
    return w.record(w.drain())


def scenario_upload_refused_records_fallback(w: World) -> dict:
    w.http.answer("POST", r"/artifacts/(upload|presign|uploads)", (501, {"detail": "no storage"}), times=5)
    w.upload(w.runs[0])
    w.metric(w.runs[0], 1)
    return w.record(w.drain())


def scenario_upload_transient(w: World) -> dict:
    w.http.answer("POST", r"/artifacts", 503, times=10)
    w.upload(w.runs[0])
    w.metric(w.runs[1], 1)
    return w.record(w.drain())


def scenario_long_ops_false_and_deferred_hash(w: World) -> dict:
    w.upload(w.runs[0], inline_hash=False)
    w.metric(w.runs[0], 1)
    return w.record(w.drain(long_ops=False))


def scenario_on_error_raises(w: World) -> dict:
    w.http.answer("POST", r"/metrics$", 422, times=3)
    w.metric(w.runs[0], 1)
    w.metric(w.runs[1], 1)

    def refuse(exc):
        w.errors.append(describe_error(exc, w.norm))
        raise RuntimeError("caller keeps the op")

    try:
        report = w.drain(on_error=refuse)
    except RuntimeError as exc:
        report = {"raised": str(exc)}
    return w.record(report)


def scenario_dead_letter_then_retry_failed(w: World) -> dict:
    w.http.answer("POST", r"/metrics$", 422)
    op_id = w.metric(w.runs[0], 1)
    first = w.drain()
    requeued = w.journal.retry_failed(op_id)
    return {"first": first, "requeued": requeued, **w.record(w.drain())}


def scenario_receipt_journal(w: World) -> dict:
    receipts = Journal.for_receipts(w.tmp / "outbox")
    for run, name, correlation in ((0, "a.pt", "c-1"), (0, "a.pt", "c-1"), (1, "b.pt", "c-2")):
        body = {"name": name, "uri": f"file:///mnt/{name}", "is_reference": True}
        receipts.append_http("POST", f"/v1/runs/{w.runs[run]}/artifacts", body, correlation=correlation)
    report = w.drain(receipts)
    state = {c: w.norm.value(receipts.delivery_state(c)) for c in ("c-1", "c-2", "c-3")}
    return {"delivery_state": state, **w.record(report, receipts)}


def scenario_credential_queues(w: World) -> dict:
    fp = "0123456789abcdef"
    other = Journal.for_credential(w.tmp / "outbox", fp)
    w.metric(w.runs[0], 1)
    w.metric(w.runs[1], 1, journal=other)
    idle = Journal.for_credential(w.tmp / "outbox", "fedcba9876543210")
    idle._ensure()
    return w.record(w.drain())


def scenario_credential_queues_skipped(w: World) -> dict:
    other = Journal.for_credential(w.tmp / "outbox", "0123456789abcdef")
    w.metric(w.runs[0], 1)
    w.metric(w.runs[1], 1, journal=other)
    return w.record(w.drain(credential_queues=False))


def scenario_non_blocking_and_corrupt_op(w: World) -> dict:
    w.metric(w.runs[0], 1, blocking=False)
    (w.journal.ops_dir / "0000000000000000001-broken.json").write_text("{not json")
    w.metric(w.runs[0], 2)
    return w.record(w.drain())


def scenario_catalog_manifest_delivered(w: World) -> dict:
    import gzip
    import hashlib

    gz = bytearray(gzip.compress(b'{"files": []}', mtime=0))
    gz[9] = 3  # the header's OS byte: Python 3.13 writes 255 where 3.12 writes 3
    gz = bytes(gz)
    digest = hashlib.sha256(gz).hexdigest()
    w.http.answer("PUT", r"/v1/catalog/manifests/", (200, {"digest": digest}))
    w.journal.append_catalog_manifest(digest, gz)
    w.metric(w.runs[0], 1)
    return w.record(w.drain())


def scenario_upload_degrades_without_room(w: World) -> dict:
    import importlib

    import pytest as _pytest

    with _pytest.MonkeyPatch.context() as patch:
        for module in ("journal", "headroom", "uploads"):
            try:
                target = importlib.import_module(f"probe.sdk.delivery.journal.{module}")
            except ImportError:
                continue
            patch.setattr(target, "MIN_FREE_BYTES", 1 << 62, raising=False)
        queued = w.upload(w.runs[0])
    return {"queued": w.norm.value(queued), **w.record(w.drain())}


# Route-shaped branches (plan sdk-typed-write-ops): each is decided by what a write's path says.
EXPERIMENT = "11111111-1111-4111-8111-111111111111"
PROJECT = "22222222-2222-4222-8222-222222222222"


def scenario_steps_batch_route(w: World) -> dict:
    w.http.answer("GET", r"/v1/server/features$", (200, {"features": ["steps_batch"]}), times=5)
    w.http.answer("POST", r"/steps/batch$", (201, {"stored": 3}), times=5)
    for step in (1, 2, 3):
        w.journal.append_http("POST", f"/v1/runs/{w.runs[0]}/steps", {"step_index": step, "values": {"phase": f"s{step}"}})
    return w.record(w.drain())


def scenario_spans_nul_text_and_ingest(w: World) -> dict:
    w.journal.append_http("POST", f"/v1/runs/{w.runs[0]}/spans", {"spans": [{"attributes": {"result": "a\x00b"}}]})
    w.journal.append_http("POST", "/ingest/v1/runs", {"runs": []})
    return w.record(w.drain())


def scenario_closes_wait_for_another_credentials_writes(w: World) -> dict:
    other = Journal.for_credential(w.tmp / "outbox", "0123456789abcdef")
    w.metric(w.runs[0], 1, journal=other)
    w.metric(w.runs[1], 1, journal=other)
    release = {"write_epoch": 1, "exit_status": "completed", "writer": {}}
    w.journal.append_http("POST", f"/v1/runs/{w.runs[0]}/writers/sess-1/release", release)
    w.journal.append_http("PATCH", f"/v1/runs/{w.runs[1]}", {"status": "completed"})
    w.journal.append_http("PATCH", f"/v1/runs/{w.runs[1]}", {"tags": ["not-a-close"]})
    return w.record(w.drain())


def scenario_experiment_child_placement(w: World) -> dict:
    w.journal.append_http("POST", f"/v1/projects/~/experiments/{EXPERIMENT}/versions", {"note": "v1"})
    w.journal.append_http("PATCH", f"/v1/projects/{PROJECT}/experiments/{EXPERIMENT}", {"description": "q"})
    return w.record(w.drain())


def scenario_collect_window_holds_telemetry(w: World) -> dict:
    with pytest.MonkeyPatch.context() as patch:
        patch.setenv("PROBE_SEND_INTERVAL_SEC", "30")
        w.metric(w.runs[0], 1)
        w.journal.append_http("POST", f"/v1/runs/{w.runs[0]}/steps", {"step_index": 1, "values": {}})
        w.journal.append_http("PATCH", f"/v1/runs/{w.runs[1]}", {"tags": ["now"]})
        w.metric("not-a-uuid", 1)
    before = dump_tree(w.journal.dir, w.norm)
    from probe.sdk.delivery.outbox.drain.window import CollectWindow

    return _stamped({"before": before, **w.record(w.drain(window=CollectWindow()))})


def scenario_route_shapes_the_drain_reads_as_before(w: World) -> dict:
    """Shapes no SDK writer sends (a trailing slash, a query, a lowercase method, a corrupt close),
    recorded on main before the routes refactor (review of #3826)."""
    w.http.answer("GET", r"/v1/server/features$", (200, {"features": ["steps_batch"]}), times=5)
    w.http.answer("POST", r"/steps/batch$", (201, {"stored": 2}), times=5)
    run = w.runs[0]

    def points(step: int) -> dict:
        return {"points": [{"key": "loss", "kind": "model", "value": float(step), "step_index": step}]}

    w.journal.append_http("POST", f"/v1/runs/{run}/metrics/", points(1))
    w.journal.append_http("POST", f"/v1/runs/{run}/metrics?x=1", points(2))
    w.journal.append_http("POST", f"/v1/runs/{run}/metrics", points(3))
    w.journal.append_http("post", f"/v1/runs/{run}/metrics", points(4))
    w.journal.append_http("POST", f"/v1/runs/{run}/steps/", {"step_index": 1, "values": {}})
    w.journal.append_http("POST", f"/v1/runs/{run}/steps", {"step_index": 2, "values": {}})
    w.journal.append_http("POST", f"/v1/runs/{run}/spans?x=1", {"spans": [{"attributes": {"result": "a\x00b"}}]})
    w.journal.append_http("PATCH", f"/v1/runs/{run}/", {"status": []})
    before = dump_tree(w.journal.dir, w.norm)
    return {"before": before, **w.record(w.drain())}


def _stamped(value):
    """`send_after` / `send_in` are wall-clock readings (and an op file's `size` carries
    `send_after`'s digits): record only that they are there."""
    if isinstance(value, dict):
        return {k: (f"<{k}>" if k in ("send_after", "send_in", "size") else _stamped(v)) for k, v in value.items()}
    if isinstance(value, list):
        return [_stamped(v) for v in value]
    return value


def scenario_metrics_pass_an_upload(w: World) -> dict:
    w.upload(w.runs[0])
    w.metric(w.runs[0], 1)
    w.journal.append_http("POST", f"/v1/runs/{w.runs[0]}/steps", {"step_index": 1, "values": {}})
    w.metric(w.runs[0], 2)
    return w.record(w.drain())


SCENARIOS = {name[len("scenario_"):]: fn for name, fn in sorted(globals().items()) if name.startswith("scenario_")}


@pytest.mark.parametrize("name", sorted(SCENARIOS))
def test_drain_golden(name, world):
    check(f"drain/{name}", SCENARIOS[name](world))


def test_every_scenario_is_deterministic(app, tmp_path, monkeypatch):
    """Two runs of a busy scenario record the same thing (ids and times are normalised)."""
    first = scenario_two_runs_round_robin(World(app, tmp_path / "a", monkeypatch))
    second = scenario_two_runs_round_robin(World(app, tmp_path / "b", monkeypatch))
    assert os.environ.get("PROBE_GOLDENS_RECORD") == "1" or first["report"] == second["report"]
