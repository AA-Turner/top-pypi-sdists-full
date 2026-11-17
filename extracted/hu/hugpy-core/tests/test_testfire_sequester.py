"""The test fire's whole contract (operator rulings 2026-11-16):

  * its ONLY special behaviour is sequestering its worker — no OTHER call lands
    there; its own job-tagged, pinned calls pass;
  * it makes NO concurrency decision — it submits EVERY planned call in list
    order, each without waiting, and the job takes care of itself;
  * results come from each call's own call-log row (a call may wait arbitrarily
    long for the queue's verdict and is still assessed correctly);
  * an impossible model is auto-blocked to the worker (the Wrapper's feasibility
    verdict), so the test fire skips it with the reason and routing never calls it.
"""
import socket
import threading
import time

from hugpy_core.calllog import call_record
from hugpy_core.relay import admission, pick
from hugpy_core.models import modeldb
from hugpy_core.registry import registry
from hugpy_core.testfire import testfire
from hugpy_core.testfire import routes as tfroutes


def _patch_routing(monkeypatch, workers):
    by = {}
    for w in workers:
        by[w["id"]] = w
        by[w["name"]] = w
    monkeypatch.setattr(registry, "all_workers", lambda: list(workers))
    monkeypatch.setattr(registry, "lookup_worker", lambda k: by.get(k))
    monkeypatch.setattr(registry, "is_online", lambda w: True)
    monkeypatch.setattr(registry, "effective_pool", lambda w: "")
    monkeypatch.setattr(registry, "stamp_picked", lambda wid: None)
    monkeypatch.setattr(admission, "is_blocked", lambda wid: False)
    monkeypatch.setattr(modeldb, "blocked_worker_ids", lambda key: set())
    monkeypatch.setattr(modeldb, "routing_snapshot",
                        lambda key: ({w["id"]: (True, False, False) for w in workers}, {}))
    monkeypatch.setattr(modeldb, "record_routed_allocation", lambda *a, **k: True)
    monkeypatch.setattr(pick, "_serving_now", lambda *a, **k: None)
    monkeypatch.setattr(pick, "_central_has", lambda key: False)
    pick._SEQUESTERED.clear()


def test_a_sequestered_worker_takes_only_its_own_test_fires_tagged_calls(monkeypatch):
    W = {"id": "w-ae", "name": "ae", "models": ["org/m"]}
    OTHER = {"id": "w-2", "name": "comp", "models": ["org/m"]}
    _patch_routing(monkeypatch, [W, OTHER])
    pick.sequester("w-ae", "JOB1")

    try:
        pick.pick("org/m", pin="ae")
        assert False, "expected a sequester refusal"
    except pick.NoWorker as exc:
        assert "sequestered by test fire JOB1" in str(exc) and "ae" in str(exc)

    tagged = {"request_body": {"metadata": {"test_fire": {"job_id": "JOB1"}}}}
    with call_record.bound_call(tagged):
        assert pick.pick("org/m", pin="ae")["id"] == "w-ae"

    assert pick.pick("org/m")["id"] == "w-2"        # ordinary traffic avoids the held worker

    _patch_routing(monkeypatch, [W])
    pick.sequester("w-ae", "JOB1")
    try:
        pick.pick("org/m")
        assert False, "expected no-worker naming the sequester"
    except pick.NoWorker as exc:
        assert "sequestered by test fire JOB1" in str(exc)
    pick.release("w-ae", "JOB1")
    assert pick.pick("org/m")["id"] == "w-ae"


def test_fire_one_scores_from_the_call_log_even_when_the_call_waits_long(monkeypatch):
    testfire.reset_registry()
    job = testfire.start_job("w-ae", "ae", [{"model_key": "org/m"}], grade=False, spawn=False)

    sent = {}

    def fake_post(payload, job=None, client_rid=None):
        sent.update(payload)
        time.sleep(0.2)   # a queued call waits for the verdict; there is no read timeout
        # the HTTP body is deliberately wrong: assessment must read the call log
        return 200, "core-123", {"choices": [{"message": {"content": "HTTP-IGNORED"}}]}, None

    row = {
        "http_status": 200, "error": None, "total_s": 42.0, "worker": "ae",
        "response_body": {
            "choices": [{"index": 0, "message": {"role": "assistant", "content": "4"},
                         "finish_reason": "stop"}],
            "usage": {"completion_tokens": 3, "prompt_tokens": 10},
            "timings": {"predicted_per_second": 20.0},
            "hugpy": {"worker": "ae", "execution_request_id": "exec-9"},
        },
    }
    monkeypatch.setattr(testfire, "_post_chat", fake_post)
    from hugpy_core.calllog import calllog
    monkeypatch.setattr(calllog, "by_request_ids", lambda ids: {"core-123": row} if "core-123" in ids else {})

    res = testfire.fire_one("org/m", "what is 2+2?", 32, job)

    assert sent["alloc"] == {"worker": "w-ae"}
    assert sent["metadata"]["test_fire"]["job_id"] == job.job_id
    assert sent["model"] == "org/m" and sent["stream"] is False
    assert res["ok"] is True
    assert res["text"] == "4" and res["tokens"] == 3 and res["tok_s"] == 20.0
    assert res["latency_s"] == 42.0 and res["request_id"] == "exec-9"
    testfire.reset_registry()
    pick._SEQUESTERED.clear()


def test_every_planned_call_is_submitted_in_order_without_waiting(monkeypatch):
    testfire.reset_registry()
    pick._SEQUESTERED.clear()
    keys = [f"org/m{i}" for i in range(5)]
    seen = []
    gate = threading.Event()

    def call_fn(key, prompt, max_tokens, job):
        seen.append(key)
        gate.wait(5)                      # block: a call never returns until released
        return {"ok": True, "model_key": key, "text": "x", "tokens": 1,
                "request_id": "r-" + key, "client_request_id": "r-" + key}

    job = testfire.start_job("w-ae", "ae", [{"model_key": k} for k in keys],
                             grade=False, rounds=1, first_order=keys, call_fn=call_fn, spawn=True)
    try:
        deadline = time.time() + 5
        while len(seen) < 5 and time.time() < deadline:
            time.sleep(0.01)
        # all five were submitted (in first_order order) before ANY returned —
        # the job did not pace on earlier calls; it also held its sequester.
        assert seen == keys
        assert job.submitted == 5 and job.done_calls == 0
        assert pick.sequestered_by("w-ae") == job.job_id
    finally:
        gate.set()
        job.thread.join(5)
    assert job.done_calls == 5 and job.ok == 5
    assert pick.sequestered_by("w-ae") is None   # released when the run finished
    testfire.reset_registry()


def test_stop_closes_every_in_flight_connection_and_ends_the_job(monkeypatch):
    # a server that ACCEPTS but never answers: each call blocks in getresponse
    # with no read timeout, exactly like a call queued in the Wrapper.
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind(("127.0.0.1", 0))
    srv.listen(16)
    held = []

    def accept_loop():
        while True:
            try:
                conn, _ = srv.accept()
                held.append(conn)
            except OSError:
                return

    threading.Thread(target=accept_loop, daemon=True).start()
    from hugpy_core.imports import functions as fns
    monkeypatch.setattr(fns, "local_base", lambda: f"http://127.0.0.1:{srv.getsockname()[1]}")
    monkeypatch.setenv("HUGPY_TEST_FIRE_BRAIN", "0")
    testfire.reset_registry()
    pick._SEQUESTERED.clear()

    keys = [f"org/m{i}" for i in range(6)]
    job = testfire.start_job("w-ae", "ae", [{"model_key": k} for k in keys],
                             grade=False, rounds=1, first_order=keys, spawn=True)
    try:
        deadline = time.time() + 5
        while len(job._conns) < 6 and time.time() < deadline:
            time.sleep(0.01)
        assert len(job._conns) == 6          # all six calls are in flight, blocked on the read

        t0 = time.time()
        cancelled = job.cancel_in_flight("test fire stopped")
        assert len(cancelled) == 6
        assert {c["model_key"] for c in cancelled} == set(keys)
        job.thread.join(5)
        assert not job.running                # the run ended once the connections closed
        assert time.time() - t0 < 2.0         # ...within ~2 s
    finally:
        srv.close()

    # every cancelled call is recorded, not ok, with the stop reason
    results = job.snapshot()["results"]
    assert len(results) == 6
    assert all(r["status"] == "cancelled" and r["error"] == "test fire stopped" for r in results)
    testfire.reset_registry()
    pick._SEQUESTERED.clear()


def test_an_impossible_model_is_auto_blocked_and_the_test_fire_skips_it(monkeypatch):
    # Core reflects the Wrapper's feasibility verdict into the pair's auto_blocked:
    # set on possible=false, cleared on possible=true, untouched when absent.
    sql = []

    class FakeConn:
        def execute(self, q, params=()):
            sql.append((q, params))
            return None

    modeldb.reflect_feasibility(FakeConn(), "ae", [
        {"id": "org/big", "possible": False, "possible_reason": "never fits: 80GB > 24GB"},
        {"id": "org/ok", "possible": True},
        {"id": "org/unknown"},           # no field: left unchanged
    ])
    sets = [(q, p) for q, p in sql if "auto_blocked" in q and "||" in q]
    assert any("never fits: 80GB > 24GB" in p and "org/big" in p for q, p in sets for p in [str(p)])
    clears = [(q, p) for q, p in sql if "- 'auto_blocked'" in q]
    assert clears and "org/ok" in str(clears[0][1])
    assert all("org/unknown" not in str(p) for q, p in sql)

    # routing excludes an auto-blocked pair (blocked_worker_ids includes it)
    W = {"id": "w-ae", "name": "ae", "models": ["org/big"]}
    OTHER = {"id": "w-2", "name": "comp", "models": ["org/big"]}
    _patch_routing(monkeypatch, [W, OTHER])
    monkeypatch.setattr(modeldb, "blocked_worker_ids", lambda key: {"w-ae"})
    try:
        pick.pick("org/big", pin="ae")
        assert False, "expected a block refusal for the pinned infeasible pair"
    except pick.NoWorker as exc:
        assert "blocked" in str(exc)
    assert pick.pick("org/big")["id"] == "w-2"     # unpinned routes to the feasible worker

    # the test fire skips the auto-blocked pair, with the Wrapper's reason
    monkeypatch.setattr(modeldb, "worker_blocked_reasons",
                        lambda wid: {"org/big": "never fits: 80GB > 24GB"})
    kept, skipped = tfroutes._drop_blocked_pairs(
        "ae", [{"model_key": "org/big"}, {"model_key": "org/ok"}], [])
    assert [s["model_key"] for s in kept] == ["org/ok"]
    assert {"model_key": "org/big", "reason": "never fits: 80GB > 24GB"} in skipped
    pick._SEQUESTERED.clear()
