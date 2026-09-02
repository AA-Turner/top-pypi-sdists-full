"""The concurrency ramp. Phase-0 proof harness (NOT shipped code).

PLAN.md: "Increase concurrency in steps until any guardrail is crossed."

One step = launch N units -> let them stabilize (that window is DISCARDED) -> measure ->
stop them -> evaluate the guardrails against the measurement window only. The ramp stops
at the first crossing and reports the last passing level; the operator gets both numbers
plus every sample, so nothing rests on trusting this file's arithmetic.
"""

from __future__ import annotations

import json
import shutil
import signal
import subprocess
import threading
import time
from dataclasses import dataclass, field
from pathlib import Path

from . import config, guardrails
from .credits import CreditProbe
from .metrics import percentile, stats
from .sampler import Sampler
from .workloads.base import STATUS_SKIP


@dataclass
class RunContext:
    base_url: str
    work_dir: str
    out_dir: str
    display: str | None
    display_base: int
    headless: bool
    levels: list[int]
    stabilize_s: float
    measure_s: float
    sample_interval_s: float
    think_ms: int
    heavy_tabs: int
    stream_fps: int
    stream_bitrate: str
    selkies_image: str | None
    sandbox_image: str | None
    turn_url: str | None
    input_latency_cmd: str | None
    nodes: int
    smoke: bool = False

    @property
    def unit_duration_s(self) -> float:
        return self.stabilize_s + self.measure_s + 30.0


@dataclass
class Unit:
    unit_id: str
    proc: subprocess.Popen
    events: list[dict] = field(default_factory=list)
    reader: threading.Thread | None = None


def _read_events(unit: Unit) -> None:
    assert unit.proc.stdout is not None
    for line in unit.proc.stdout:
        line = line.strip()
        if not line:
            continue
        try:
            payload = json.loads(line)
        except json.JSONDecodeError:
            payload = {"ev": "unparsed", "raw": line[:400]}
        payload["_t"] = time.time()
        unit.events.append(payload)


def _dmesg_oom_lines(since_epoch: float) -> list[str]:
    """Best effort. A container usually cannot read the kernel ring buffer; that is why
    the crash guardrail ALSO keys on unit exit status, which always works."""
    if not shutil.which("dmesg"):
        return []
    try:
        out = subprocess.run(["dmesg", "-T"], capture_output=True, text=True, timeout=10)
    except (OSError, subprocess.SubprocessError):
        return []
    if out.returncode != 0:
        return []
    hits = [
        ln
        for ln in out.stdout.splitlines()
        if "Out of memory" in ln or "oom-kill" in ln or "oom_reaper" in ln
    ]
    return hits[-20:]


def _probe_input_latency(cmd: str) -> float | None:
    """Operator-supplied probe: a command printing ONE number (milliseconds) per call.

    The harness cannot measure human input latency by itself -- only the operator's own
    stream client can. This seam is how a real Selkies deployment closes PLAN.md's
    250 ms guardrail without this file pretending to own a WebRTC stack.
    """
    try:
        out = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=20)
    except (OSError, subprocess.SubprocessError):
        return None
    if out.returncode != 0:
        return None
    try:
        return float(out.stdout.strip().splitlines()[-1])
    except (ValueError, IndexError):
        return None


def run_step(
    workload,
    ctx: RunContext,
    level: int,
    sampler: Sampler,
    credit_probe: CreditProbe,
    baseline_p95: float | None,
) -> dict:
    step_started = time.time()
    units: list[Unit] = []
    work_profiles = Path(ctx.work_dir) / "profiles"
    work_profiles.mkdir(parents=True, exist_ok=True)

    for index in range(level):
        unit_id = f"{level:02d}-{index}"
        spec = workload.unit_spec(ctx, unit_id, level)
        proc = subprocess.Popen(
            spec.argv,
            env=spec.env,
            cwd=spec.cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
        )
        unit = Unit(unit_id=unit_id, proc=proc)
        unit.reader = threading.Thread(target=_read_events, args=(unit,), daemon=True)
        unit.reader.start()
        units.append(unit)
        sampler.track_unit(unit_id, proc.pid)

    time.sleep(ctx.stabilize_s)
    window_start_index = sampler.mark()
    window_start_t = time.time()

    input_latencies: list[float] = []
    credit_samples: list[dict] = []
    deadline = window_start_t + ctx.measure_s
    next_credit_sample = time.monotonic()
    while time.time() < deadline:
        now_monotonic = time.monotonic()
        if now_monotonic >= next_credit_sample:
            credit_samples.append({"sampled_at": time.time(), "measurement": credit_probe.sample()})
            next_credit_sample = now_monotonic + config.CREDIT_SAMPLE_INTERVAL_S
        if ctx.input_latency_cmd:
            value = _probe_input_latency(ctx.input_latency_cmd)
            if value is not None:
                input_latencies.append(value)
        time.sleep(min(1.0, max(0.0, deadline - time.time())))
    window_end_t = time.time()

    samples = sampler.window(window_start_index)
    credit = credit_probe.sample()
    credit_samples.append({"sampled_at": time.time(), "measurement": credit})

    for unit in units:
        try:
            unit.proc.send_signal(signal.SIGTERM)
        except OSError:
            pass
    for unit in units:
        try:
            unit.proc.wait(timeout=45)
        except subprocess.TimeoutExpired:
            unit.proc.kill()
        sampler.untrack_unit(unit.unit_id)
    for unit in units:
        if unit.reader:
            unit.reader.join(timeout=10)

    # --- collect per-unit event metrics, measurement window only -------------
    action_ms: list[float] = []
    start_ms: list[float] = []
    restore_ms: list[float] = []
    encoder_pct: list[float] = []
    bitrate_bps: list[float] = []
    errors = 0
    fatals: list[str] = []
    for unit in units:
        for ev in unit.events:
            kind = ev.get("ev")
            if kind == "ready":
                start_ms.append(float(ev.get("start_ms") or 0.0))
                if ev.get("restore_ms") is not None:
                    restore_ms.append(float(ev["restore_ms"]))
            elif kind == "restore" and ev.get("ms") is not None:
                restore_ms.append(float(ev["ms"]))
            elif kind == "action" and window_start_t <= ev["_t"] <= window_end_t:
                action_ms.append(float(ev.get("ms") or 0.0))
            elif kind == "error":
                errors += 1
            elif kind == "fatal":
                fatals.append(str(ev.get("msg"))[:300])
            elif kind == "encoder" and window_start_t <= ev["_t"] <= window_end_t:
                if ev.get("utilisation_pct") is not None:
                    encoder_pct.append(float(ev["utilisation_pct"]))
                if ev.get("bitrate_bps"):
                    bitrate_bps.append(float(ev["bitrate_bps"]))

    crashes = sum(1 for u in units if u.proc.returncode not in (0, -signal.SIGTERM, None))
    never_ready = sum(1 for u in units if not any(e.get("ev") == "ready" for e in u.events))
    oom_lines = _dmesg_oom_lines(step_started)

    verdicts = guardrails.evaluate(
        samples=samples,
        action_latencies_ms=action_ms,
        input_latencies_ms=input_latencies or None,
        encoder_pct=encoder_pct or None,
        baseline_action_p95_ms=baseline_p95,
        crashes=crashes + never_ready,
        units_started=level,
        oom_lines=oom_lines,
    )

    return {
        "workload": workload.id,
        "plan_workload": workload.plan_workload,
        "capacity_class": workload.capacity_class,
        "concurrency": level,
        "started_at": step_started,
        "measure_window_s": window_end_t - window_start_t,
        "samples_in_window": len(samples),
        "host": {
            "cpu_busy_pct": stats([s["cpu_busy_pct"] for s in samples]),
            "cpu_steal_pct": stats([s["cpu_steal_pct"] for s in samples]),
            "mem_used_pct": stats([s["mem_used_pct"] for s in samples]),
            "mem_used_bytes": stats([s["mem_used_bytes"] for s in samples]),
            "disk_util_pct": stats([s["disk_util_pct"] for s in samples]),
            "disk_read_bps": stats([s["disk_read_bps"] for s in samples]),
            "disk_write_bps": stats([s["disk_write_bps"] for s in samples]),
            "psi_cpu_avg10": stats(
                [s["psi_cpu_avg10"] for s in samples if s["psi_cpu_avg10"] is not None]
            ),
            "psi_io_avg10": stats(
                [s["psi_io_avg10"] for s in samples if s["psi_io_avg10"] is not None]
            ),
        },
        "units": {
            "requested": level,
            "unit_rss_bytes": stats([s["unit_rss_bytes"] for s in samples]),
            "rss_per_unit_bytes_p95": (
                (percentile([s["unit_rss_bytes"] for s in samples], 95) or 0) / level
                if level
                else None
            ),
            "procs": stats([s["unit_procs"] for s in samples]),
            "crashes": crashes,
            "never_became_ready": never_ready,
            "action_errors": errors,
            "fatal_messages": fatals[:5],
        },
        "latency_ms": {
            "browser_start": stats(start_ms),
            "restore": stats(restore_ms),
            "action": stats(action_ms),
            "input": stats(input_latencies) if input_latencies else None,
        },
        "encoder": {
            "utilisation_pct": stats(encoder_pct) if encoder_pct else None,
            "bitrate_bps": stats(bitrate_bps) if bitrate_bps else None,
        },
        "cpu_credit": credit,
        "cpu_credit_samples": credit_samples,
        "kernel_oom_lines": oom_lines,
        "guardrails": verdicts,
        "guardrails_crossed": guardrails.any_crossed(verdicts),
        "guardrails_unmeasured": guardrails.unmeasured(verdicts),
        "raw_samples": samples,
    }


def run_workload(workload, ctx: RunContext, sampler: Sampler, credit_probe: CreditProbe) -> dict:
    preflight = workload.preflight(ctx)
    result: dict = {
        "workload": workload.id,
        "plan_workload": workload.plan_workload,
        "title": workload.title,
        "capacity_class": workload.capacity_class,
        "steady_state": workload.steady_state,
        "preflight": preflight.to_json(),
        "steps": [],
        "failure_level": None,
        "last_passing_level": None,
        "baseline_action_p95_ms": None,
        "stopped_because": None,
    }
    if preflight.status == STATUS_SKIP:
        result["stopped_because"] = "skipped at preflight"
        return result

    steps_dir = Path(ctx.out_dir) / "steps"
    steps_dir.mkdir(parents=True, exist_ok=True)
    baseline: float | None = None

    for level in ctx.levels:
        print(f"  [{workload.id}] concurrency={level} ...", flush=True)
        step = run_step(workload, ctx, level, sampler, credit_probe, baseline)
        path = steps_dir / f"{workload.id}__c{level:03d}.json"
        path.write_text(json.dumps(step, indent=2, default=str))
        slim = {k: v for k, v in step.items() if k != "raw_samples"}
        slim["raw_samples_file"] = str(path)
        result["steps"].append(slim)

        if baseline is None and step["latency_ms"]["action"]["p95"]:
            # The FIRST completed level is the single-run baseline PLAN.md's 2x action
            # latency guardrail is measured against. It is this workload's own baseline;
            # comparing workload 3 against workload 2 would compare different work.
            baseline = float(step["latency_ms"]["action"]["p95"])
            result["baseline_action_p95_ms"] = baseline
            result["baseline_from_level"] = level

        crossed = step["guardrails_crossed"]
        if crossed:
            result["failure_level"] = level
            result["stopped_because"] = f"guardrail(s) crossed: {', '.join(crossed)}"
            print(f"  [{workload.id}] STOP at {level}: {result['stopped_because']}", flush=True)
            break
        result["last_passing_level"] = level
    else:
        result["stopped_because"] = (
            "ramp exhausted its level list without crossing a guardrail -- the ceiling "
            "was NOT found; re-run with a higher --max-concurrency"
        )
    return result
