"""FORCING GUARD — the static seal's fingerprint work never slows the event loop (owner's rule,
``common-docs/systems/agents/agent-harness/projects/prompt-blocks-static-seal/VISION.md``, 2026-11-13: a real request is never
slowed for a saving).

The finding (2026-11-13): fingerprinting in server worker THREADS stalled the event loop 160-240 ms
while realistic 250 KB sends were parsed (full garbage collections from ``json.loads``, plus
interpreter-lock contention). The work now runs in ONE worker process (``seal_worker.py``).

* The load probe: an asyncio task sleeping 1 ms in a loop records its lateness, idle and then while
  20 realistic 250 KB sends are fingerprinted (3 interleaved rounds, a server-sized live heap). The
  median lateness under load stays within 1.5x idle (+0.1 ms jitter), p99 under 10 ms, the worst
  under 20 ms. RED with the job run in a server thread (``_run_in_worker`` pointed at ``worker_job``
  in-process: the retired thread design) — its median lateness is 2-3 ms. (p99 against 1.5x idle
  p99 was the first bar; on a shared 4-core machine at load 5 the idle loop's own p99/max swing
  0.3-2 ms / 1-20 ms, so the tail bars are absolute.)
* The worker never imports the server app or the config package: ``python -X importtime`` in the
  real worker boot, after a body job, a residual job and an xAI job.
* A dead worker drops jobs (said once) and is restarted at most once per
  ``seal_worker_restart_minutes`` — never a restart loop.
"""

from __future__ import annotations

import asyncio
import pickle
import statistics
import struct
import subprocess
import sys
import time
from typing import Any

import pytest
from test_static_seal_never_touches_the_send import CONV, _Ctx, _realistic_body  # noqa: F401 — fixtures below

from matrx_ai.orchestrator.execution_state import (
    ExecutionState,
    clear_execution_state,
    set_execution_state,
)
from matrx_ai.providers import final_outbound_snapshot as fos
from matrx_ai.providers import seal_worker
from matrx_ai.providers.outbound_capture import CallMeta, set_call_meta

URL = "https://api.anthropic.com/v1/messages"


@pytest.fixture(autouse=True)
def _on(monkeypatch: pytest.MonkeyPatch) -> Any:
    """The check switched on (production starts it off: knob seal_check_on = 0), inside a
    conversation and an agent loop."""
    monkeypatch.setattr(fos, "seal_check_on", lambda: True)
    fos.reset_for_tests()
    ctx = _Ctx()
    monkeypatch.setattr("matrx_connect.context.app_context.try_get_app_context", lambda: ctx)
    token = set_execution_state(ExecutionState())
    yield ctx
    clear_execution_state(token)
    fos.reset_for_tests()


def _observe(body: bytes, request_id: str, ctx: Any) -> Any:
    set_call_meta(CallMeta(provider="anthropic", model="m"))
    ctx.request_id = request_id
    fos.stamp_seal(fos.SealStamp(fos.SHAPE_ANTHROPIC, 230, None))
    return fos.observe_wire_body(url=URL, body=body)


def _quantile(values: list[float], q: float) -> float:
    ordered = sorted(values)
    return ordered[min(len(ordered) - 1, int(q * len(ordered)))]


def _source_of(body: bytes) -> tuple[Any, Any]:
    """What the translator rendered for ``body`` (``note_wire_source``'s shape): its system text and
    every message — so the dispatcher's server-side half of the residual check does its full work."""
    import json
    import types

    parsed = json.loads(body)
    return types.SimpleNamespace(system_instruction=parsed["system"], messages=[]), parsed["messages"]


def load_probe(ctx: Any, sends: int = 20, rounds: int = 3, *, residual: bool = False) -> dict[str, float]:
    """Loop lateness (ms) idle and while ``sends`` realistic 250 KB sends are fingerprinted, pooled
    over ``rounds`` interleaved idle/load windows (the machine's own noise lands in both). A live
    heap rides along (``_SERVER_HEAP``): a server holds millions of objects, which is what made a
    full garbage collection cost 160-240 ms when the parse ran in a server thread."""
    from matrx_ai.providers import residual_check

    bodies = [_realistic_body().replace(b'"[0] ', f'"[0] {k} '.encode(), 1) for k in range(sends)]
    sources = [_source_of(body) for body in bodies] if residual else [None] * sends
    jobs_with_residual: list[int] = []
    real_run = fos._run_in_worker

    def counting(payload: Any) -> Any:
        out = real_run(payload)
        if "known" in payload and isinstance(out, dict) and "residual" in out:
            jobs_with_residual.append(1)
        return out

    fos._run_in_worker = counting  # restored below

    async def run() -> dict[str, float]:
        late: list[float] = []
        stop = False

        async def probe() -> None:
            while not stop:
                began = time.perf_counter()
                await asyncio.sleep(0.001)
                late.append((time.perf_counter() - began - 0.001) * 1000)

        # Warm the worker (process start, imports) before measuring.
        _observe(bodies[0], "warm", ctx)
        await fos.wait_for_pending()
        task = asyncio.create_task(probe())
        idle: list[float] = []
        loaded: list[float] = []
        for round_index in range(rounds):
            late.clear()
            await asyncio.sleep(0.3)
            idle.extend(late)
            late.clear()
            for index, body in enumerate(bodies):
                if sources[index] is not None:
                    residual_check._wire_source_var.set(sources[index])
                assert _observe(body, f"req-{round_index}-{index}", ctx) is None
                await asyncio.sleep(0.002)  # sends arrive as a busy server's do: spread, not one burst
            await fos.wait_for_pending()
            loaded.extend(late)
        stop = True
        await task
        return {
            "idle_p50": statistics.median(idle),
            "idle_p90": _quantile(idle, 0.90),
            "idle_p99": _quantile(idle, 0.99),
            "idle_max": max(idle),
            "load_p50": statistics.median(loaded),
            "load_p90": _quantile(loaded, 0.90),
            "load_p99": _quantile(loaded, 0.99),
            "load_max": max(loaded),
            "load_samples": float(len(loaded)),
        }

    try:
        lag = asyncio.run(run())
    finally:
        fos._run_in_worker = real_run
    lag["residual_jobs"] = float(len(jobs_with_residual))
    return lag


#: A server-sized live heap while the probe runs (about a million small objects).
_SERVER_HEAP: list[Any] = []


@pytest.fixture
def server_heap() -> Any:
    _SERVER_HEAP.extend({"k": i, "v": [i]} for i in range(400_000))
    yield _SERVER_HEAP
    _SERVER_HEAP.clear()


@pytest.mark.parametrize("residual", [False, True], ids=["seal only", "seal + residual check"])
def test_fingerprinting_20_realistic_sends_never_slows_the_event_loop(_on: Any, server_heap: Any, residual: bool) -> None:
    assert 200 * 1024 < len(_realistic_body()) < 256 * 1024
    lag = load_probe(_on, residual=residual)
    if residual:
        assert lag["residual_jobs"] >= 60, lag  # every measured send ran the residual check
    else:
        assert lag["residual_jobs"] == 0, lag
    print("seal load probe (ms):", {k: round(v, 3) for k, v in lag.items()})
    assert fos.take_seal_records(CONV), "nothing was fingerprinted: this probe would prove nothing"
    # The typical send's loop is as punctual as an idle loop's (a worker THREAD made it 2-3 ms late:
    # every 1 ms tick waited for the interpreter lock). 0.1 ms: timer jitter.
    assert lag["load_p50"] <= 1.5 * lag["idle_p50"] + 0.1, lag
    # The tail: no stall anywhere near a garbage-collection freeze (160-240 ms in the server).
    assert lag["load_p99"] < 10.0, lag
    assert lag["load_max"] < 20.0, lag


_OUR_ROOTS = {"matrx_ai", "aidream", "matrx_connect", "matrx_utils", "matrx_orm", "matrx_graph"}
_PURE = [
    "matrx_ai",
    "matrx_ai.providers",
    "matrx_ai.providers.final_outbound_snapshot",
    "matrx_ai.providers.residual_check",
    "matrx_ai.providers.seal_worker",
]


def _boot_worker(jobs: list[dict[str, Any]]) -> tuple[list[Any], set[str], str]:
    """The REAL worker boot (``seal_worker._BOOT``) under ``-X importtime``: results, modules loaded."""
    frames = b""
    for item in [sys.path, *jobs]:
        data = pickle.dumps(item)
        frames += struct.pack("!Q", len(data)) + data
    done = subprocess.run(
        [sys.executable, "-X", "importtime", "-c", seal_worker._BOOT],
        input=frames, capture_output=True, timeout=60, check=False,
    )
    results = []
    out = done.stdout
    while out:
        (size,) = struct.unpack("!Q", out[:8])
        results.append(pickle.loads(out[8 : 8 + size]))
        out = out[8 + size :]
    stderr = done.stderr.decode(errors="replace")
    modules = {line.split("|")[-1].strip() for line in stderr.splitlines() if line.startswith("import time:")}
    return results, modules, stderr[-2000:]


def test_the_worker_imports_only_the_stdlib_and_the_pure_modules() -> None:
    """A body job and a residual job load the stdlib and the three pure modules — never the server
    app, the config package or any SDK; an xAI job adds only the SDK's proto module (and its deps)."""
    from xai_sdk.proto import chat_pb2

    from matrx_ai.providers.residual_check import platform_patterns

    stamp = fos.SealStamp(fos.SHAPE_ANTHROPIC, 1, None)
    body_jobs = [
        {"kind": "body", "shape": fos.SHAPE_ANTHROPIC, "stamp": stamp, "parse_max": 1 << 20, "body": _realistic_body(8)},
        {
            "kind": "body", "shape": fos.SHAPE_ANTHROPIC, "stamp": stamp, "parse_max": 1 << 20,
            "body": _realistic_body(8), "known": ["[0]"], "patterns": platform_patterns(),
        },
    ]
    results, modules, tail = _boot_worker(body_jobs)
    assert len(results) == 2 and all("error" not in r for r in results), (results, tail)
    assert results[0]["segments"] and results[1].get("residual") is not None
    assert sorted(m for m in modules if m.split(".")[0] in _OUR_ROOTS) == _PURE
    third_party = sorted({m.split(".")[0] for m in modules} - set(sys.stdlib_module_names) - _OUR_ROOTS - {"_virtualenv"})
    print(f"worker (body + residual jobs) loaded {len(modules)} modules; outside the stdlib: {third_party}")
    assert all(not m.startswith(("pydantic", "httpx", "fastapi", "uvicorn", "anthropic", "openai", "google")) for m in modules)

    proto = chat_pb2.GetCompletionsRequest(model="m")
    proto.messages.add(role=chat_pb2.MessageRole.ROLE_USER).content.add(text="hello")
    xai_job = {
        "kind": "xai", "shape": fos.SHAPE_XAI, "stamp": fos.SealStamp(fos.SHAPE_XAI, 1, None), "parse_max": 1 << 20,
        "whole": proto.SerializeToString(deterministic=True), "proto_ref": fos._proto_ref(chat_pb2.GetCompletionsRequest),
    }
    results, modules, tail = _boot_worker([xai_job])
    assert len(results) == 1 and "error" not in results[0] and results[0]["segments"], (results, tail)
    assert set(m for m in modules if m.split(".")[0] in _OUR_ROOTS) <= set(_PURE)
    assert any(m.startswith("xai_sdk") for m in modules)  # the SDK loads in the worker, for xAI jobs only


def test_a_dead_worker_drops_jobs_says_so_once_and_restarts_at_most_once_per_window(
    _on: Any, monkeypatch: pytest.MonkeyPatch
) -> None:
    said: list[str] = []
    real_say = fos._say_failure
    monkeypatch.setattr(fos, "_say_failure", lambda where, exc: (said.append(where), real_say(where, exc)))
    starts: list[int] = []
    real_cls = seal_worker.WorkerProcess

    class _Counting(real_cls):  # type: ignore[misc, valid-type]
        def __init__(self) -> None:
            starts.append(1)
            super().__init__()

    monkeypatch.setattr(seal_worker, "WorkerProcess", _Counting)
    body = _realistic_body(20)

    async def send(request_id: str) -> None:
        _observe(body, request_id, _on)
        await fos.wait_for_pending()

    async def run() -> None:
        fos._worker_down(seal_worker.WorkerGone("test: start fresh"))
        fos._WORKER_DOWN_AT[0] = None
        fos._FAILED.clear()
        said.clear()
        await send("a")  # starts a worker
        assert len(starts) == 1 and fos._WORKER is not None
        fos._WORKER.proc.kill()
        fos._WORKER.proc.wait(5)
        for index in range(5):  # dead: every job dropped, no restart inside the window
            await send(f"dropped-{index}")
        assert len(starts) == 1
        assert said.count("seal worker") == 1, said
        fos._WORKER_DOWN_AT[0] -= fos.seal_worker_restart_seconds() + 1  # the window has passed
        await send("b")  # one restart after the window
        assert len(starts) == 2 and fos._WORKER is not None and fos._WORKER.alive()

    asyncio.run(run())


def test_the_residual_check_rides_the_worker_job(_on: Any, caplog: pytest.LogCaptureFixture) -> None:
    """The residual subtraction runs in the worker process; the report is made server side, once."""
    import json
    import logging
    import types

    from matrx_ai.providers import residual_check

    caplog.set_level(logging.WARNING)
    pids: list[int] = []
    real = fos._run_in_worker

    def spy(payload: Any) -> Any:
        result = real(payload)
        pids.append(result["pid"])
        return result

    body = json.dumps(
        {
            "model": "m",
            "system": "You are a careful assistant.",
            "messages": [{"role": "user", "content": "Known words. And a sentence nobody registered anywhere."}],
        }
    ).encode()

    async def run() -> None:
        residual_check.note_wire_source(
            types.SimpleNamespace(system_instruction="You are a careful assistant.", messages=[]),
            [{"role": "user", "content": "Known words."}],
        )
        set_call_meta(CallMeta(provider="anthropic", model="m"))
        fos.stamp_seal(fos.SealStamp(fos.SHAPE_ANTHROPIC, 0, None))
        assert fos.observe_wire_body(url=URL, body=body) is None
        await fos.wait_for_pending()

    with pytest.MonkeyPatch.context() as mp:
        mp.setattr(fos, "_run_in_worker", spy)
        asyncio.run(run())
    import os

    assert pids and all(pid != os.getpid() for pid in pids)
    reports = [r for r in caplog.records if residual_check.REPORT_KIND in r.getMessage()]
    assert len(reports) == 1 and "nobody registered" in reports[0].getMessage()


def test_the_worker_runs_in_a_server_holding_more_than_1024_descriptors() -> None:
    """``select.select`` refuses a descriptor numbered 1024 or above (ValueError): a busy server holds
    thousands of sockets, so the worker's pipes must be waited on with ``poll``. Run in a child so the
    raised descriptor limit and the open files never leak into the suite."""
    code = (
        "import os, resource, sys\n"
        "soft, hard = resource.getrlimit(resource.RLIMIT_NOFILE)\n"
        "resource.setrlimit(resource.RLIMIT_NOFILE, (min(4096, hard), hard))\n"
        "held = [os.open(os.devnull, os.O_RDONLY) for _ in range(1100)]\n"
        "from matrx_ai.providers import final_outbound_snapshot as fos, seal_worker\n"
        "w = seal_worker.WorkerProcess()\n"
        "assert w._in >= 1024 and w._out >= 1024, (w._in, w._out)\n"
        "stamp = fos.SealStamp(fos.SHAPE_CHAT, 0, None)\n"
        "r = w.call({'kind': 'body', 'shape': fos.SHAPE_CHAT, 'stamp': stamp, 'parse_max': 1 << 20, 'body': b'{}'}, 30)\n"
        "assert r['parsed'] is True, r\n"
        "w.close()\n"
        "print('OK')\n"
    )
    done = subprocess.run([sys.executable, "-c", code], capture_output=True, timeout=60, check=False)
    assert done.stdout.decode().strip().endswith("OK"), done.stderr.decode()[-2000:]


def test_a_worker_that_fails_to_start_leaves_no_process_behind(monkeypatch: pytest.MonkeyPatch) -> None:
    """``WorkerProcess.__init__`` failing after its child started (the first frame cannot be sent)
    kills and reaps that child: no orphan per restart window."""
    started: list[Any] = []
    real_popen = subprocess.Popen

    def popen(*args: Any, **kwargs: Any) -> Any:
        proc = real_popen(*args, **kwargs)
        started.append(proc)
        return proc

    monkeypatch.setattr(seal_worker.subprocess, "Popen", popen)

    def boom(self: Any, data: bytes, deadline: float) -> None:
        raise seal_worker.WorkerGone("cannot send the first frame")

    monkeypatch.setattr(seal_worker.WorkerProcess, "_write", boom)
    with pytest.raises(seal_worker.WorkerGone):
        seal_worker.WorkerProcess()
    assert len(started) == 1
    assert started[0].returncode is not None, "the child was left running (an orphan)"


def test_a_forked_child_starts_clean_and_the_parent_keeps_its_worker(_on: Any) -> None:
    """After ``os.fork`` the child holds the parent's worker handle and dispatcher thread object, both
    useless there: it must start with none (no false "worker exited" alarm, no blind dispatcher)."""
    import os

    async def warm() -> None:
        _observe(_realistic_body(8), "warm", _on)
        await fos.wait_for_pending()

    asyncio.run(warm())
    assert fos._WORKER is not None and fos._DISPATCHER is not None
    parent_pid = fos._WORKER.pid
    child = os.fork()
    if child == 0:  # pragma: no cover — the child reports through its exit code
        clean = fos._WORKER is None and fos._DISPATCHER is None and fos._WORKER_DOWN_AT[0] is None and not fos._PENDING
        os._exit(0 if clean else 3)
    _, status = os.waitpid(child, 0)
    assert os.waitstatus_to_exitcode(status) == 0, "the forked child inherited the parent's worker state"
    assert fos._WORKER is not None and fos._WORKER.pid == parent_pid and fos._WORKER.alive()


def test_a_worker_found_dead_long_after_its_start_restarts_at_once(_on: Any, monkeypatch: pytest.MonkeyPatch) -> None:
    """The restart throttle measures from the last restart, not from when the death was noticed."""
    import asyncio

    from matrx_ai.providers import seal_worker

    starts: list[int] = []
    real_cls = seal_worker.WorkerProcess

    class _Counting(real_cls):  # type: ignore[misc, valid-type]
        def __init__(self) -> None:
            starts.append(1)
            super().__init__()

    monkeypatch.setattr(seal_worker, "WorkerProcess", _Counting)

    async def run() -> None:
        fos._worker_down(seal_worker.WorkerGone("test: start fresh"))
        fos._WORKER_DOWN_AT[0] = None
        await asyncio.sleep(0)
        # Start a worker, then pretend it started long ago and has since died unnoticed.
        fos._WORKER = seal_worker.WorkerProcess()
        fos._WORKER_STARTED_AT[0] = time.monotonic() - fos.seal_worker_restart_seconds() - 60
        fos._WORKER.proc.kill()
        fos._WORKER.proc.wait(5)
        fos._run_in_worker({"op": "noop"})
        assert len(starts) == 2, "a long-dead worker must restart immediately"
        # A crash loop is still throttled: a fresh start that dies at once is not restarted in-window.
        fos._WORKER.proc.kill()
        fos._WORKER.proc.wait(5)
        before = len(starts)
        assert fos._run_in_worker({"op": "noop"}) is None
        assert len(starts) == before

    asyncio.run(run())
    fos._worker_down(seal_worker.WorkerGone("test: cleanup"))
    fos._WORKER_DOWN_AT[0] = None
