"""GPU hardware metrics through a FAKE NVML (no GPU on the machine running this).

The released SDK's collector (on by default since 2026-09-21) imports
``pynvml``. ``fake_nvml/pynvml.py`` shadows it on ``PYTHONPATH`` with the same
names, return shapes and error classes, so the real collector, emitter and
outbox run end to end in a real child process; only the driver is fake.

Pass = the training loop's own points, status and exit code are untouched in
every mode; with a working "driver" the GPU series land on the server with the
fake's exact readings, per device; with a failing one they are skipped cleanly
(no traceback, no crash) and whatever was sampled before a mid-run loss stays.

NOT VALIDATED HERE, and still needing a real GPU machine: the real
nvidia-ml-py binding against a real driver (struct layouts, bytes-vs-str
names, MIG and CUDA_VISIBLE_DEVICES remapping on real UUIDs), sampling cost
beside a busy CUDA context, and driver hangs (a call that blocks rather than
raises).
"""

from __future__ import annotations

import time
from pathlib import Path

import pytest

from tests.environments import envlib
from tests.environments.envlib import LoopEvents, record

pytestmark = [envlib.requires_env]

FAKE_NVML = Path(__file__).resolve().parent / "fake_nvml"
TERMINAL = {"completed", "failed", "crashed", "canceled"}
STEPS = range(0, 40)


def _run_loop(be, sdk_py, tmp_path, mode: str) -> dict:
    nvml_log = tmp_path / "nvml.log"
    env = envlib.child_env(
        be,
        tmp_path,
        PYTHONPATH=str(FAKE_NVML),
        FAKE_NVML_MODE=mode,
        FAKE_NVML_LOG=str(nvml_log),
        FAKE_NVML_OK_SAMPLES="2",
        PROBE_HW_INTERVAL="1",
        PROBE_HW=None,  # the customer default: on
    )
    work = tmp_path / "work"
    work.mkdir()
    _start_before_a_window_closes()
    started = time.time()
    proc = envlib.run_child(
        [sdk_py, str(envlib.CUSTOMER_LOOP), "--name", f"gpu-{mode}", "--steps", "0:40",
         "--step-sleep", "0.4", "--config", "--then", "finish"],
        env=env,
        cwd=work,
        timeout=780,
    )
    events = LoopEvents.parse(proc.stdout)
    run_id = events.run_id
    assert run_id, f"no run opened:\n{envlib.tail(proc.stderr)}"
    expected = envlib.expected_points(STEPS)
    rec = be.wait_points(run_id, expected, timeout=60)
    status = be.wait_status(run_id, TERMINAL, timeout=60)
    points = be.points(run_id)
    gpu = [p for p in points if (p.get("kind") == "hardware") and str(p.get("key", "")).startswith(("hw/gpu/", "hw/proc/gpu"))]
    calls = nvml_log.read_text().splitlines() if nvml_log.exists() else []
    return {
        "proc": proc,
        "run_id": run_id,
        "rec": rec,
        "status": status,
        "gpu": gpu,
        "hw_total": sum(1 for p in points if p.get("kind") == "hardware"),
        "calls": calls,
        "real_home_writes": envlib.real_home_writes(started, [run_id, str(tmp_path)]),
    }


def _start_before_a_window_closes(lead: float = 10.0) -> None:
    """Hardware points are 60 s windows on the epoch grid (`probe/hw/grid.py`).
    Releases up to 0.198.0 send a window only once it has CLOSED and drop the
    one open at finish(), so there a run must straddle a minute boundary to
    record any: start ``lead`` seconds before one, train ~16 s, and the first
    window closes mid-run with the first samples in it. Later SDKs also send
    the open window at the close (lane E3's finding); the straddle then covers
    both a closed window and that last partial one."""
    wait = (60.0 - lead - time.time() % 60.0) % 60.0
    time.sleep(wait)


def _by_key_device(gpu: list[dict]) -> dict[tuple[str, int], set[float]]:
    out: dict[tuple[str, int], set[float]] = {}
    for p in gpu:
        dims = p.get("dimensions") or {}
        out.setdefault((p["key"], int(dims.get("gpu", -1))), set()).add(float(p["value"]))
    return out


def _common_asserts(r: dict) -> None:
    proc = r["proc"]
    assert proc.returncode == 0, envlib.tail(proc.stderr)
    assert "Traceback" not in proc.stderr, envlib.tail(proc.stderr)
    assert r["rec"].ok, r["rec"].summary()
    assert r["status"] == "completed"
    assert r["real_home_writes"] == []


def test_env_gpu_fake_nvml_readings_reach_the_server(be, sdk_py, sdk_version, tmp_path):
    r = _run_loop(be, sdk_py, tmp_path, "ok")
    series = _by_key_device(r["gpu"])
    record(
        "gpu/fake-nvml[ok]",
        sdk=sdk_version,
        exit=r["proc"].returncode,
        points=r["rec"].summary(),
        status=r["status"],
        nvml_calls=len(r["calls"]),
        gpu_series={f"{k}@gpu{d}": sorted(v)[:3] for (k, d), v in sorted(series.items())},
        hw_points=r["hw_total"],
    )
    _common_asserts(r)
    assert "nvmlInit" in r["calls"] and "nvmlDeviceGetUtilizationRates" in r["calls"], "the fake was not reached"
    # Exactly the fake's readings, on the right physical device.
    assert series.get(("hw/gpu/utilization", 0)) == {37.0}
    assert series.get(("hw/gpu/utilization", 1)) == {81.0}
    assert series.get(("hw/gpu/memory_used_bytes", 0)) == {float(3 * 1024**3)}
    assert series.get(("hw/gpu/memory_used_bytes", 1)) == {float(70 * 1024**3)}
    assert series.get(("hw/gpu/powerWatts", 1)) == {402.0}
    assert series.get(("hw/gpu/temp", 0)) == {61.0}
    assert series.get(("hw/proc/gpu_memory_bytes", 1)) == {2_500_000_000.0}


@pytest.mark.parametrize("mode", ["init_raises", "lost_midrun", "not_supported", "foreign_raise"])
def test_env_gpu_fake_nvml_failures_are_skipped_never_crash(be, sdk_py, sdk_version, tmp_path, mode):
    r = _run_loop(be, sdk_py, tmp_path, mode)
    series = _by_key_device(r["gpu"])
    record(
        f"gpu/fake-nvml[{mode}]",
        sdk=sdk_version,
        exit=r["proc"].returncode,
        points=r["rec"].summary(),
        status=r["status"],
        nvml_calls=len(r["calls"]),
        gpu_series=sorted(f"{k}@gpu{d}" for k, d in series),
        hw_points=r["hw_total"],
        stderr_tail=envlib.tail(r["proc"].stderr, 400),
    )
    _common_asserts(r)
    assert "nvmlInit" in r["calls"], "the fake was not reached"
    if mode == "init_raises":
        assert r["gpu"] == [], "no driver, so no GPU series"
    elif mode == "not_supported":
        # The supported readings still land; the unsupported ones are skipped.
        assert series.get(("hw/gpu/utilization", 0)) == {37.0}
        assert not any(k in ("hw/gpu/powerWatts", "hw/gpu/temp", "hw/proc/gpu_memory_bytes") for k, _ in series)
    elif mode == "lost_midrun":
        # What was sampled before the loss is kept, with the fake's values.
        assert series.get(("hw/gpu/utilization", 1)) in (None, {81.0})
    # foreign_raise: no expectation on GPU series beyond "the run is unharmed".
