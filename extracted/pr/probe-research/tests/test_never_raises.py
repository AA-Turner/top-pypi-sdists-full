"""The invariant every SDK reliability item serves (plan "The invariant every item
serves", docs/2026-09-26-sdk-reliability-plan.md; task T8).

Outside ``strict=True``, ``probe.init()`` after it returns, ``log()``,
``log_artifact()``, ``finish()`` and the exit hooks never raise into the user's
program -- across transport errors, 409/413/422/503, full disk (the free-space
floor), a read-only outbox and a killed worker.

Every public write method is driven through every fault, and every case
asserts its fault actually FIRED (a hit counter): a fault the operation never
reaches proves nothing. The combinations that cannot reach their fault by
design are listed in `_NOT_APPLICABLE` with the reason, and skipped as N/A:

* an async client's ``log()`` / ``log_artifact()`` only journal, so no network
  fault can reach them (the network faults are exercised by the closes);
* a sync client only touches the outbox when a send fails, so the disk faults
  are armed TOGETHER with a dead network there -- the write has nowhere to go.

A case that still breaks because another lane's fix has not landed is
``xfail(strict=True, raises=...)`` and names the plan item, so it FAILS the day
that fix lands and the marker must go. Each later PR adds its own case here.

"After init returns" is enforced with the threads init starts running for real
(the hardware monitor, a 0.05 s heartbeat): an unhandled exception in any of
them fails the test.

Out of scope: ``run.snapshot()`` called explicitly during an outage raises
``TransportError`` (it is not in the plan's list; `probe.init()`'s own
auto-snapshot is inside init, before it returns).

"Never raise" covers failures of OURS. ``KeyboardInterrupt`` and ``SystemExit``
are let through on purpose, from a queue write and from a warning alike: they
are the user stopping the process (#2055; ``test_delivery_notices.py`` holds
their tests).
"""

from __future__ import annotations

import errno
import os
import signal
import subprocess
import sys
import threading
import time
from http.server import ThreadingHTTPServer

import httpx
import pytest

import probe
from probe.sdk import errors, fluent
from probe.sdk import journal as journal_module
from probe.sdk import run as run_module
from probe.sdk.run import Run

from tests.conftest import FakeApp, make_client

pytestmark = pytest.mark.filterwarnings("error::pytest.PytestUnhandledThreadExceptionWarning")

#: What the server says for each refusal, in production's shape.
_REFUSALS = {
    409: {"detail": {"message": "stale writer epoch", "existing_id": None}},
    413: {"detail": "Request Entity Too Large"},
    422: {"detail": [{"loc": ["body", "points"], "msg": "invalid", "type": "value_error"}]},
    503: {"detail": "concurrent telemetry write; retry this ingest batch"},
}

FAULTS = [
    "transport_error",
    "http_409",
    "http_413",
    "http_422",
    "http_503",
    "full_disk",
    "read_only_outbox",
]
OPS = ["log", "log_artifact", "finish", "exit_hook", "with_block", "excepthook_then_exit"]


#: (op, fault, async_writes) combinations that cannot reach their fault, and why.
_NET = ("transport_error", "http_409", "http_413", "http_422", "http_503")
_NOT_APPLICABLE = {
    **{
        (op, fault, True): "an async log()/log_artifact() only journals: no network fault reaches it"
        for op in ("log", "log_artifact")
        for fault in _NET
    },
}


class _FaultyApp(FakeApp):
    """The fake API, answering every WRITE under /v1/runs/ with `status` once
    armed -- reads keep working, as they do when an ingest path is sick."""

    status: int | None = None
    hits = 0

    def handler(self, request: httpx.Request) -> httpx.Response:
        if (
            self.status is not None
            and request.method != "GET"
            and request.url.path.startswith("/v1/runs/")
        ):
            self.requests.append(request)
            self.hits += 1
            return httpx.Response(self.status, json=_REFUSALS[self.status])
        return super().handler(request)


@pytest.fixture(autouse=True)
def _clean(monkeypatch, tmp_path):
    _reset_fluent()
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))
    monkeypatch.setenv("PROBE_CONFIG_PATH", str(tmp_path / "config" / "probe.json"))
    monkeypatch.delenv("PROBE_TOKEN", raising=False)
    monkeypatch.delenv("PROBE_ASYNC", raising=False)
    monkeypatch.delenv("PROBE_FINISH_TIMEOUT_SEC", raising=False)
    # `probe.integrations.miles` exports PROBE_RUN_ID into os.environ itself
    # (and test_miles_integration.py can leave it behind on the same worker);
    # with it set, init(experiment=...) is refused as a contradiction.
    for var in ("PROBE_RUN_ID", "PROBE_RUN_EPOCH", "MILES_RUN_ID", "RESEARCH_OS_RUN_ID"):
        monkeypatch.delenv(var, raising=False)
    monkeypatch.setenv("PROBE_AUTO_SNAPSHOT", "0")
    # The threads init starts, running for real (conftest pins both off).
    monkeypatch.setenv("PROBE_HW", "1")
    monkeypatch.setenv("PROBE_HEARTBEAT_SECONDS", "0.05")
    # Every close in this file retries for half a second, not 600.
    monkeypatch.setattr(run_module, "FINISH_TIMEOUT_DEFAULT_SECONDS", 0.5)
    yield
    _reset_fluent()


def _reset_fluent():
    """The exit hooks keep process state on purpose; tests must not inherit it."""
    fluent._current.set(None)
    fluent._process_default = None
    fluent._exit_status = "completed"
    fluent._exit_recorded = False
    fluent._exit_exception = None
    fluent._exit_code = None
    fluent._exit_via = None


def _opened(tmp_path, *, async_writes: bool):
    app = _FaultyApp()
    app.seed_experiment("e1")
    client = make_client(app, tmp_spool=tmp_path / "outbox", async_writes=async_writes)
    run = probe.init(client=client, experiment="e1", name="never-raises")
    return app, client, run


def _arm(fault, app, client, monkeypatch, hits=None):
    """Break one thing, AFTER init returned. ``hits["n"]`` counts how often the
    fault actually fired."""
    hits = hits if hits is not None else {"n": 0}
    if fault == "transport_error":

        def down(*a, **k):
            hits["n"] += 1
            raise errors.TransportError("network unreachable")

        for verb in ("request", "put_url", "put_file", "put_fileobj"):
            monkeypatch.setattr(client.transport, verb, down)
    elif fault.startswith("http_"):
        app.status = int(fault.split("_")[1])
    elif fault == "full_disk":
        # Under the free-space floor (plan 1.5 keeps this knob).
        monkeypatch.setattr(journal_module, "MIN_FREE_BYTES", 1 << 62)
        client.journal._appends_since_statvfs = journal_module._STATVFS_EVERY
        client.journal._last_free_ok = True
        journal = client.journal
        # `below_floor`: plan 1.5 asks it BEFORE queueing, and a write sent
        # straight to the server instead meets the fault there.
        for name in ("below_floor", "_append_headroom", "_staging_headroom"):
            real = getattr(journal, name)

            def counted(*a, _real=real, **k):
                refusal = _real(*a, **k)
                if refusal is not None:
                    hits["n"] += 1
                return refusal

            monkeypatch.setattr(journal, name, counted)
    elif fault == "read_only_outbox":
        # A read-only mount: every write under the outbox fails with EROFS.
        # (chmod alone is not it -- the journal owns its directories and
        # re-asserts their modes before giving up on a write.)
        root = str(client.journal.dir)
        real_write = journal_module.write_text_atomic
        real_snapshot = journal_module.snapshot_file

        def erofs(path, *a, **k):
            if str(path).startswith(root):
                hits["n"] += 1
                raise OSError(errno.EROFS, "Read-only file system", str(path))

        def write(path, *a, **k):
            erofs(path)
            return real_write(path, *a, **k)

        def snapshot(src, dst, *a, **k):
            erofs(dst)
            return real_snapshot(src, dst, *a, **k)

        monkeypatch.setattr(journal_module, "write_text_atomic", write)
        monkeypatch.setattr(journal_module, "snapshot_file", snapshot)
    else:  # pragma: no cover
        raise AssertionError(fault)
    return hits


def _fired(fault, app, hits) -> int:
    return app.hits if fault.startswith("http_") else hits["n"]


def _do(op, run, tmp_path):
    artifact = tmp_path / "weights.bin"
    artifact.write_bytes(b"\x00" * 4096)
    if op == "log":
        probe.log({"loss": 0.5}, step=1)
        run.log({"acc": 0.9, "lr": 1e-3}, step=2)
        run.log({"loss": 0.4})
    elif op == "log_artifact":
        run.log_artifact("weights", path=str(artifact))
        probe.log_artifact("weights-2", path=str(artifact))
    elif op == "finish":
        run.log({"loss": 0.5}, step=1)
        probe.finish()
    elif op == "exit_hook":
        run.log({"loss": 0.5}, step=1)
        fluent._finish_at_exit()
    elif op == "with_block":
        with run:
            run.log({"loss": 0.5}, step=1)
    elif op == "excepthook_then_exit":
        # A script dying of its own error: the hooks run, and must neither
        # raise nor replace that error.
        run.log({"loss": 0.5}, step=1)
        seen = []
        # init installed the hooks; the one they chain to lives on `sys` (#2001).
        state = fluent._hooks()
        assert state is not None, "probe.init() installs the exit hooks"
        previous = state.get("excepthook")
        state["excepthook"] = lambda *a: seen.append(a[0])
        try:
            err = ValueError("the user's own bug")
            fluent._excepthook(ValueError, err, None)
        finally:
            state["excepthook"] = previous
        assert seen == [ValueError], "the user's error still reaches the previous hook"
        fluent._finish_at_exit()
    else:  # pragma: no cover
        raise AssertionError(op)


def _cases():
    for op in OPS:
        for fault in FAULTS:
            for async_writes in (True, False):
                case_id = f"{op}-{fault}-{'async' if async_writes else 'sync'}"
                reason = _NOT_APPLICABLE.get((op, fault, async_writes))
                marks = [pytest.mark.skip(reason=f"N/A: {reason}")] if reason else []
                yield pytest.param(op, fault, async_writes, id=case_id, marks=marks)


@pytest.mark.parametrize(("op", "fault", "async_writes"), list(_cases()))
def test_public_write_methods_never_raise(op, fault, async_writes, tmp_path, monkeypatch):
    app, client, run = _opened(tmp_path, async_writes=async_writes)
    hits = _arm(fault, app, client, monkeypatch)
    if not async_writes and fault in ("full_disk", "read_only_outbox"):
        # A sync write reaches the outbox only when its send fails.
        _arm("transport_error", app, client, monkeypatch, {"n": 0})

    _do(op, run, tmp_path)  # THE assertion: none of this raises

    assert _fired(fault, app, hits) > 0, f"{fault} never fired: this case proves nothing"
    client.close()


@pytest.mark.parametrize("async_writes", [True, False], ids=["async", "sync"])
@pytest.mark.parametrize("second", ["transport_error", "http_503", "http_422", "full_disk"])
def test_a_close_with_nowhere_to_put_it_never_raises(second, async_writes, tmp_path, monkeypatch):
    """Two faults at once: the outbox cannot take the close AND the server
    cannot take it either. There is nowhere left to record the verdict; the
    close must say so and return, not raise."""
    app, client, run = _opened(tmp_path, async_writes=async_writes)
    run.log({"loss": 1.0}, step=1)
    read_only = _arm("read_only_outbox", app, client, monkeypatch)
    _arm(second, app, client, monkeypatch)
    run.log({"loss": 2.0}, step=2)

    run.finish()

    assert read_only["n"] > 0, "the read-only outbox never fired"
    client.close()


# -- a killed worker -------------------------------------------------------------


@pytest.fixture
def live_server(monkeypatch, tmp_path):
    from tests.test_outbox_process import _Handler

    server = ThreadingHTTPServer(("127.0.0.1", 0), _Handler)
    server.daemon_threads = True
    server.records = []
    server.blobs = {}
    server.lock = threading.Lock()
    server.auth_fail = False
    server.delay = 0.0
    threading.Thread(target=server.serve_forever, daemon=True).start()
    url = f"http://127.0.0.1:{server.server_port}"
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    monkeypatch.setenv("PROBE_BASE_URL", url)
    monkeypatch.setenv("PROBE_TOKEN", "probe_pat_process_test")
    monkeypatch.delenv("PROBE_OUTBOX_DIR", raising=False)
    try:
        yield server, url
    finally:
        server.shutdown()
        server.server_close()


def test_a_worker_killed_mid_pass_breaks_nothing(live_server, tmp_path):
    """The detached worker dies (OOM killer, pod eviction) holding the drain
    lock mid-pass. Logging and closing afterwards must not raise, and every
    write still arrives."""
    from probe.sdk.client import Client
    from probe.sdk.journal import Journal

    server, url = live_server
    journal = Journal(tmp_path / "outbox", context={"name": None, "base_url": url})
    # auto_drain=False: the only drainer is the worker this test starts and kills.
    client = Client(journal=journal, async_writes=True, auto_drain=False)
    run = Run(client, {"id": "r-proc", "tags": []})
    for step in range(20):
        run.log({"loss": float(step)}, step=step)

    server.delay = 0.15  # slow the API so the kill lands mid-pass
    worker = subprocess.Popen(
        [sys.executable, "-m", "probe.sdk.outbox_worker", str(journal.dir)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    # Poll for the worker's first delivered op instead of sleeping a fixed
    # amount: a fixed sleep is too short on a slow/loaded runner (the worker
    # hasn't even started its pass yet) and wastefully long on a fast one.
    deadline = time.monotonic() + 20
    delivered_before_kill = 0
    while time.monotonic() < deadline:
        with server.lock:
            delivered_before_kill = sum(
                1 for _, path, _ in server.records if path.endswith("/metrics")
            )
        if delivered_before_kill >= 1 and journal.pending():
            break
        time.sleep(0.02)
    else:
        worker.kill()
        worker.wait(timeout=30)
        server.delay = 0.0
        pytest.fail(
            "the worker never delivered a first op within 20s; retune the pass "
            "size or server delay"
        )
    os.kill(worker.pid, signal.SIGKILL)
    worker.wait(timeout=30)
    server.delay = 0.0
    assert journal.pending(), "expected a mid-pass kill; retune the sleep"
    before_kill = delivered_before_kill
    # Otherwise the worker died before its pass began, and this proves nothing
    # about a pass cut short (review of #2015).
    assert before_kill >= 1, "the killed worker never reached the server"

    for step in range(20, 25):
        run.log({"loss": float(step)}, step=step)  # must not raise
    result = run.finish(flush_timeout=30)  # must not raise

    assert not (isinstance(result, dict) and result.get("finish_queued")), result
    with server.lock:
        steps = sorted(
            p["step_index"]
            for method, path, body in server.records
            if path.endswith("/metrics")
            for p in (body or {}).get("points", [])
        )
    # At-least-once: the killed pass may have landed a POST it never got to
    # unlink, and the server's metric insert dedupes the replay.
    assert sorted(set(steps)) == list(range(25)), "every write arrived"
    client.close()


# -- known breaks, owned by other lanes ------------------------------------------


@pytest.mark.parametrize("async_writes", [True, False], ids=["async", "sync"])
def test_log_artifact_over_the_size_ceiling_never_raises(tmp_path, async_writes):
    """Plan 0.7 (#2007): was an xfail here until that landed."""
    app, client, run = _opened(tmp_path, async_writes=async_writes)
    big = tmp_path / "checkpoint.pt"
    with open(big, "wb") as fh:
        fh.truncate(70 * 1024 * 1024)  # 70 MB, the live audit's size
    try:
        run.log_artifact("checkpoint", path=str(big))
    finally:
        client.close()


@pytest.mark.parametrize("async_writes", [True, False], ids=["async", "sync"])
def test_log_artifact_holding_a_secret_never_raises(tmp_path, async_writes):
    app, client, run = _opened(tmp_path, async_writes=async_writes)
    leaky = tmp_path / "config.env"
    leaky.write_text("AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY\n")
    try:
        run.log_artifact("config", path=str(leaky))
    finally:
        client.close()


def test_log_below_the_resume_point_never_raises(tmp_path):
    """Plan 2.4 (#2022): was an xfail here until that landed."""
    app, client, run = _opened(tmp_path, async_writes=True)
    run.arm_resume_guard(100)  # as attach_run() arms it after a reopen
    try:
        run.log({"loss": 0.5}, step=10)
    finally:
        client.close()


# -- strict=True still raises (the other half of the contract) --------------------


def test_strict_finish_still_raises(tmp_path):
    app, client, run = _opened(tmp_path, async_writes=True)
    app.status = 503
    run.log({"loss": 0.5}, step=1)
    with pytest.raises(errors.RosError):
        run.finish(strict=True, flush_timeout=0.3)
    client.close()
