"""One walk of a run's lane builds one `/metrics` POST and one `/steps/batch` POST (plan T4):
text values in a row no longer cost a POST each, an older server gets one `/steps` POST per
record, and a failed op still goes alone."""

from __future__ import annotations

import pytest

from probe.sdk import errors
from probe.sdk.delivery.journal.journal import Journal
from probe.sdk.delivery.outbox.drain import coalesce
from probe.sdk.delivery.outbox.drain.coalesce import _partition
from probe.sdk.delivery.outbox.drain.drain import drain

RUN = "6f1c1d1e-0000-4000-8000-0000000000c3"


@pytest.fixture(autouse=True)
def _one_effort_bucket(monkeypatch):
    """Every op queued here carries one `enqueued_at`. A batch splits at a 5-minute effort
    bucket (its delivery headers, review of #3785 I13), so 1,001 writes crossing a wall-clock
    boundary went out as two batches (main 3ec03660: [337, 664]). A test that wants another
    bucket sets `enqueued_at` itself."""
    from probe.sdk.delivery.journal import append

    monkeypatch.setattr(append, "now_iso", lambda: "2026-11-01T12:42:30.000000+00:00")
SESSION = "6f1c1d1e-0000-4000-8000-0000000000d4"


class _Server:
    """A drain client: records requests; ``features`` is what the server declares; ``fail``
    maps a path suffix to the exception its next request raises."""

    def __init__(self, *, features=frozenset(), fail=None):
        self.calls: list = []
        self.fail = dict(fail or {})
        self._server_features_cache = frozenset(features)
        self.settings = type("S", (), {"token": "t", "ingest_token": None, "base_url": "http://batch-test"})()
        outer = self

        class _Transport:
            def request(self, method, path, json_body=None, **kw):
                for suffix, exc in list(outer.fail.items()):
                    if path.endswith(suffix):
                        del outer.fail[suffix]
                        raise exc
                outer.calls.append((method, path, json_body))
                return {}

        self.transport = _Transport()

    def close(self):
        pass

    def paths(self):
        return [path.rsplit("/", 2)[-2] + "/" + path.rsplit("/", 1)[-1] if path.endswith("/batch") else path.rsplit("/", 1)[-1] for _, path, _ in self.calls]


@pytest.fixture(autouse=True)
def _fresh_feature_cache(monkeypatch):
    monkeypatch.setattr(coalesce, "_STEPS_BATCH_KNOWN", {})


def _rows(journal, count, *, text=True, start=0):
    for step in range(start, start + count):
        journal.append_http(
            "POST",
            f"/v1/runs/{RUN}/metrics",
            {
                "points": [
                    {"key": "loss", "value": 1.0 / (step + 1), "step_index": step},
                    {"key": "lr", "value": 0.1, "step_index": step},
                ],
                "session_id": SESSION,
                "write_epoch": 1,
            },
        )
        if text:
            journal.append_http(
                "POST",
                f"/v1/runs/{RUN}/steps",
                {"step_index": step, "name": None, "attributes": {"phase": "train"}, "session_id": SESSION, "write_epoch": 1},
            )


def _journal(tmp_path) -> Journal:
    return Journal(tmp_path / "outbox", context={"name": None, "base_url": "http://batch-test"})


def test_one_walk_splits_interleaved_rows_into_metrics_and_steps(tmp_path):
    journal = _journal(tmp_path)
    _rows(journal, 3)
    metrics, steps = _partition(journal.pending(), 0, None)
    assert len(metrics) == 3 and len(steps) == 3
    assert all(op["path"].endswith("/metrics") for _, op in metrics)
    assert all(op["path"].endswith("/steps") for _, op in steps)


def test_mixed_rows_go_in_one_metrics_post_and_one_steps_batch(tmp_path):
    journal = _journal(tmp_path)
    _rows(journal, 50)
    server = _Server(features={"steps_batch"})
    report = drain(journal, client_factory=lambda ctx: server)
    assert report.delivered == 100 and report.remaining == 0
    assert server.paths() == ["metrics", "steps/batch"]
    (_, _, metrics), (_, _, batch) = server.calls
    assert len(metrics["points"]) == 100
    assert [step["step_index"] for step in batch["steps"]] == list(range(50))
    assert batch["session_id"] == SESSION and batch["write_epoch"] == 1
    assert "session_id" not in batch["steps"][0], "the fence rides once, at the top"


def test_an_older_server_gets_one_steps_post_per_record(tmp_path):
    journal = _journal(tmp_path)
    _rows(journal, 5)
    server = _Server()
    report = drain(journal, client_factory=lambda ctx: server)
    assert report.delivered == 10
    assert server.paths() == ["metrics"] + ["steps"] * 5


def test_numeric_rows_still_ride_in_one_post(tmp_path):
    journal = _journal(tmp_path)
    _rows(journal, 20, text=False)
    server = _Server(features={"steps_batch"})
    drain(journal, client_factory=lambda ctx: server)
    assert server.paths() == ["metrics"]


def test_a_steps_head_sends_its_batch_first(tmp_path):
    journal = _journal(tmp_path)
    for step in range(3):
        journal.append_http("POST", f"/v1/runs/{RUN}/steps", {"step_index": step, "attributes": {"p": "x"}})
        journal.append_http("POST", f"/v1/runs/{RUN}/metrics", {"points": [{"key": "loss", "value": 1.0, "step_index": step}]})
    server = _Server(features={"steps_batch"})
    drain(journal, client_factory=lambda ctx: server)
    assert server.paths() == ["steps/batch", "metrics"]


def test_a_failed_op_never_merges(tmp_path):
    """Retry order: an op that already failed goes alone and stops the walk behind it."""
    journal = _journal(tmp_path)
    _rows(journal, 4)
    pending = journal.pending()
    retried_path, retried = pending[3]  # the second row's step record
    import json

    retried["attempts"] = 1
    retried_path.write_text(json.dumps(retried))
    metrics, steps = _partition(journal.pending(), 0, None)
    assert (len(metrics), len(steps)) == (2, 1), "the walk stops at the retried op"
    assert _partition(journal.pending(), 3, None) == ([], []), "a retried head goes alone"


def test_a_server_without_the_route_falls_back_to_one_post_per_record(tmp_path):
    """The feature was declared, then the server rolled back: FastAPI's own 404."""
    journal = _journal(tmp_path)
    _rows(journal, 3)
    server = _Server(features={"steps_batch"}, fail={"/steps/batch": errors.NotFoundError("Not Found", status=404, detail="Not Found")})
    report = drain(journal, client_factory=lambda ctx: server)
    assert report.delivered == 6 and report.dead_lettered == 0
    assert server.paths() == ["metrics", "steps", "steps", "steps"]
    assert not coalesce.steps_batch_supported(server)


def test_a_refused_batch_splits_to_find_the_bad_record(tmp_path):
    journal = _journal(tmp_path)
    _rows(journal, 4)
    server = _Server(features={"steps_batch"}, fail={"/steps/batch": errors.ValidationError("bad", status=422)})
    report = drain(journal, client_factory=lambda ctx: server)
    assert report.delivered == 8 and report.dead_lettered == 0
    assert server.paths() == ["metrics", "steps/batch", "steps/batch"]


def test_a_transient_failure_of_the_metrics_post_leaves_the_steps_queued(tmp_path):
    journal = _journal(tmp_path)
    _rows(journal, 3)
    server = _Server(features={"steps_batch"}, fail={"/metrics": errors.ServerError("busy", status=503)})
    report = drain(journal, client_factory=lambda ctx: server)
    assert server.calls == [], "the steps behind a stopped head wait with it"
    assert report.remaining == 6 and report.stopped_transient


def test_the_feature_is_asked_once_per_server(tmp_path):
    asked: list = []

    class _Asking(_Server):
        def supports_feature(self, name):
            asked.append(name)
            return True

    for attempt in range(3):
        journal = Journal(tmp_path / f"outbox-{attempt}", context={"name": None, "base_url": "http://batch-test"})
        _rows(journal, 2)
        server = _Asking()
        del server._server_features_cache
        drain(journal, client_factory=lambda ctx: server)
        assert server.paths() == ["metrics", "steps/batch"]
    assert asked == ["steps_batch"]


def _set(journal, index, **fields):
    import json

    path, op = journal.pending()[index]
    op.update(fields)
    path.write_text(json.dumps(op))


def test_steps_queued_by_another_agent_session_go_in_their_own_batch(tmp_path):
    """Review I13: a batch carries one session, effort bucket and write origin (the first op's):
    steps queued under another one rode under the wrong headers. They go apart now."""
    journal = _journal(tmp_path)
    for step in range(4):
        journal.append_http("POST", f"/v1/runs/{RUN}/steps", {"step_index": step, "attributes": {"p": "x"}})
    for index in (2, 3):
        _set(journal, index, agent_session="another-agent")
    _, steps = _partition(journal.pending(), 0, None)
    assert [op["body"]["step_index"] for _, op in steps] == [0, 1]
    _set(journal, 1, write_origin="run")
    assert _partition(journal.pending(), 0, None) == ([], []), "an origin apart is a header apart"
    server = _Server(features={"steps_batch"})
    report = drain(journal, client_factory=lambda ctx: server)
    assert report.delivered == 4
    assert server.paths() == ["steps", "steps", "steps/batch"]


def test_an_older_server_sends_each_step_under_its_own_headers(tmp_path, monkeypatch):
    """Review I13: the one-by-one fallback ran every op inside the first op's scope."""
    from contextlib import nullcontext

    journal = _journal(tmp_path)
    for step in range(3):
        journal.append_http("POST", f"/v1/runs/{RUN}/steps", {"step_index": step, "attributes": {"p": "x"}})
    scoped: list = []
    monkeypatch.setattr(coalesce, "_delivery_scope", lambda op: scoped.append(op["body"]["step_index"]) or nullcontext())
    drain(journal, client_factory=lambda ctx: _Server())
    assert scoped == [0, 1, 2]


def test_an_older_servers_step_records_let_a_waiting_close_in_between(tmp_path, monkeypatch):
    """Review I9: on a server without `steps_batch`, a lane of 1,000 step records went out one
    POST after another inside ONE batch, with no point for a `finish()` waiting for the drain
    lock to take it. At most `ALONE_MAX` go before the pass reaches its next op."""
    from probe.sdk.delivery.outbox.drain import lock

    journal = _journal(tmp_path)
    count = 3 * coalesce.ALONE_MAX + 5
    for step in range(count):
        journal.append_http("POST", f"/v1/runs/{RUN}/steps", {"step_index": step, "attributes": {"p": "x"}})
    yields: list = []
    real = lock._DrainHold.between_ops
    monkeypatch.setattr(lock._DrainHold, "between_ops", lambda self: yields.append(1) or real(self))
    server = _Server()
    report = drain(journal, client_factory=lambda ctx: server)
    assert report.delivered == count and report.remaining == 0
    assert [body["step_index"] for _, _, body in server.calls] == list(range(count)), "in order"
    assert len(yields) >= 4, f"{len(yields)} chances for a close to take the lock"


def test_a_lane_over_one_batch_sends_a_full_batch_then_the_rest(tmp_path):
    """The `STEPS_MAX` boundary: 1,001 step records are one 1,000-step batch and one more."""
    journal = _journal(tmp_path)
    for step in range(coalesce.STEPS_MAX + 1):
        journal.append_http("POST", f"/v1/runs/{RUN}/steps", {"step_index": step, "attributes": {"p": "x"}})
    server = _Server(features={"steps_batch"})
    report = drain(journal, client_factory=lambda ctx: server)
    assert report.delivered == coalesce.STEPS_MAX + 1
    assert server.paths() == ["steps/batch", "steps"]
    assert len(server.calls[0][2]["steps"]) == coalesce.STEPS_MAX


def test_a_real_client_delivers_step_records_through_the_batch_route(tmp_path, monkeypatch):
    """Through a real `Client` and its transport (loopback HTTP), not a stand-in: the feature
    read, the batch body and the fallback past `STEPS_MAX`."""
    from probe.sdk.client.client import Client

    from tests.fake_delivery_server import running_server

    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))
    monkeypatch.setenv("PROBE_CONFIG_PATH", str(tmp_path / "config" / "probe.json"))
    for name in ("PROBE_TOKEN", "PROBE_ASYNC", "PROBE_EXPORT_INTERVAL_SEC"):
        monkeypatch.delenv(name, raising=False)
    with running_server(features=("steps_batch",)) as server:
        journal = Journal(tmp_path / "outbox", context={"name": None, "base_url": server.url})
        with pytest.warns(UserWarning, match="no background drainer"):
            client = Client(base_url=server.url, token="probe_pat_process_test", async_writes=True, auto_drain=False, journal=journal)
        with client:
            for step in range(coalesce.STEPS_MAX + 1):
                client.write("POST", f"/v1/runs/{RUN}/steps", {"step_index": step, "attributes": {"phase": "train"}})
            assert client.flush() == coalesce.STEPS_MAX + 1
        batches = [body for _, path, body, _ in server.requests() if path.endswith("/steps/batch")]
        assert [len(body["steps"]) for body in batches] == [coalesce.STEPS_MAX]
        assert server.count(f"{RUN}/steps") == 1, "the one past the cap went alone"


@pytest.mark.parametrize(
    "field", ["agent_session", "write_origin", "enqueued_at"], ids=["session", "origin", "effort-bucket"]
)
def test_metric_ops_queued_under_other_delivery_headers_go_apart(tmp_path, field):
    """Review of #3785, I13, for metrics too: one POST carries one session, origin and effort
    bucket, so ops differing in any never merge."""
    journal = _journal(tmp_path)
    _rows(journal, 4, text=False)
    later = {"agent_session": "another-agent", "write_origin": "run", "enqueued_at": "2099-01-01T00:00:00+00:00"}[field]
    for index in (2, 3):
        _set(journal, index, **{field: later})
    metrics, _ = _partition(journal.pending(), 0, None)
    assert [op["body"]["points"][0]["step_index"] for _, op in metrics] == [0, 1]
