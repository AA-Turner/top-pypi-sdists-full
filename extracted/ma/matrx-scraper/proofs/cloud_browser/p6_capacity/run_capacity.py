#!/usr/bin/env python3
"""P6 capacity benchmark driver. Phase-0 proof harness (NOT shipped code).

Runs PLAN.md's six workloads at increasing concurrency until a guardrail is crossed,
records every metric PLAN.md names as machine-readable JSON, and computes the admission
limit so the operator does no arithmetic.

    python3 run_capacity.py --smoke                 # ~2 min, proves the harness works
    python3 run_capacity.py                         # the real ramp
    python3 run_capacity.py --soak-hours 6          # the burstable-host soak
    python3 run_capacity.py --only w2_navigation    # one workload

Read README.md before running this on a target host. Nothing here talks to production,
to Supabase, or to a real provider: the only site involved is testapp/server.py on
127.0.0.1.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import time
import uuid
from datetime import UTC, datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from harness import admission, config, hostinfo  # noqa: E402
from harness.credits import CreditProbe  # noqa: E402
from harness.sampler import Sampler  # noqa: E402
from harness.stepper import RunContext, run_workload  # noqa: E402
from harness.summary import write_summary  # noqa: E402
from harness.workloads import all_workloads  # noqa: E402
from testapp import server as testapp  # noqa: E402


def _start_xvfb(display: str, geometry: str = "1400x1000x24"):
    if not shutil.which("Xvfb"):
        return None
    proc = subprocess.Popen(
        ["Xvfb", display, "-screen", "0", geometry, "-nolisten", "tcp"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    time.sleep(1.5)
    if proc.poll() is not None:
        return None
    return proc


def main() -> int:
    ap = argparse.ArgumentParser(description="P6 capacity benchmark (Phase-0 proof)")
    ap.add_argument(
        "--smoke",
        action="store_true",
        help="tiny windows and levels 1,2 -- proves the harness runs; the "
        "NUMBERS from a smoke run are not capacity findings",
    )
    ap.add_argument(
        "--only", action="append", default=None, help="workload id (repeatable); default is all six"
    )
    ap.add_argument("--max-concurrency", type=int, default=None)
    ap.add_argument("--levels", default=None, help="comma list, overrides the default ramp")
    ap.add_argument("--stabilize", type=float, default=None)
    ap.add_argument("--measure", type=float, default=None)
    ap.add_argument(
        "--soak-hours",
        type=float,
        default=0.0,
        help="after the ramp, hold the last passing level for N hours "
        "(PLAN.md requires >=6 on burstable hosts)",
    )
    ap.add_argument("--soak-level", type=int, default=None)
    ap.add_argument(
        "--nodes", type=int, default=1, help="fleet size for the one-node-failure reserve"
    )
    ap.add_argument(
        "--headless",
        action="store_true",
        help="no Xvfb; NOT the production shape -- understates per-unit cost",
    )
    ap.add_argument("--port", type=int, default=8642)
    ap.add_argument("--display-base", type=int, default=90)
    ap.add_argument("--heavy-tabs", type=int, default=3)
    ap.add_argument("--think-ms", type=int, default=250)
    ap.add_argument("--stream-fps", type=int, default=30)
    ap.add_argument("--stream-bitrate", default="4M")
    ap.add_argument(
        "--input-latency-cmd",
        default=os.environ.get("P6_INPUT_LATENCY_CMD"),
        help="command printing ONE number (ms) per call; the only way the "
        "250 ms input-latency guardrail can be evaluated",
    )
    ap.add_argument("--out", default=None)
    ap.add_argument("--work-dir", default="/tmp/p6_capacity")
    ap.add_argument(
        "--force-burstable",
        action="store_true",
        help="treat this host as burstable when IMDS is unreachable",
    )
    args = ap.parse_args()

    run_id = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid.uuid4().hex[:6]
    out_dir = Path(args.out or (HERE / "out" / run_id))
    out_dir.mkdir(parents=True, exist_ok=True)
    work_dir = Path(args.work_dir) / run_id
    work_dir.mkdir(parents=True, exist_ok=True)

    levels = config.DEFAULT_LEVELS
    if args.levels:
        levels = [int(x) for x in args.levels.split(",") if x.strip()]
    elif args.smoke:
        levels = [1, 2]
    if args.max_concurrency:
        levels = [lv for lv in levels if lv <= args.max_concurrency]

    stabilize = (
        args.stabilize
        if args.stabilize is not None
        else (config.SMOKE_STABILIZE_S if args.smoke else config.DEFAULT_STABILIZE_S)
    )
    measure = (
        args.measure
        if args.measure is not None
        else (config.SMOKE_MEASURE_S if args.smoke else config.DEFAULT_MEASURE_S)
    )

    display = None
    xvfb = None
    if not args.headless:
        display = f":{args.display_base}"
        xvfb = _start_xvfb(display)
        if xvfb is None:
            print(
                "Xvfb could not start; falling back to --headless "
                "(this is recorded in the summary and is NOT the production shape)"
            )
            display = None
            args.headless = True

    httpd, _ = testapp.serve(args.port)
    base_url = f"http://127.0.0.1:{args.port}"

    ctx = RunContext(
        base_url=base_url,
        work_dir=str(work_dir),
        out_dir=str(out_dir),
        display=display,
        display_base=args.display_base,
        headless=args.headless,
        levels=levels,
        stabilize_s=stabilize,
        measure_s=measure,
        sample_interval_s=config.SAMPLE_INTERVAL_S,
        think_ms=args.think_ms,
        heavy_tabs=args.heavy_tabs,
        stream_fps=args.stream_fps,
        stream_bitrate=args.stream_bitrate,
        selkies_image=os.environ.get("P6_SELKIES_IMAGE"),
        sandbox_image=os.environ.get("P6_SANDBOX_IMAGE"),
        turn_url=os.environ.get("P6_TURN_URL"),
        input_latency_cmd=args.input_latency_cmd,
        nodes=args.nodes,
        smoke=args.smoke,
    )

    host = hostinfo.collect({"run_id": run_id, "harness_version": "p6-2026-08-17"})
    credit_probe = CreditProbe(force_burstable=args.force_burstable)
    (out_dir / "host.json").write_text(hostinfo.as_json(host))

    sampler = Sampler(interval=config.SAMPLE_INTERVAL_S)
    sampler.start()

    selected = all_workloads()
    if args.only:
        wanted = set(args.only)
        selected = [w for w in selected if w.id in wanted]
        if not selected:
            print(f"no workload matched {sorted(wanted)}")
            return 2

    results = []
    try:
        for workload in selected:
            print(f"[{workload.id}] {workload.title}", flush=True)
            result = run_workload(workload, ctx, sampler, credit_probe)
            if result["preflight"]["status"] == "skip":
                print(f"  SKIPPED: {'; '.join(result['preflight']['reasons'])}", flush=True)
            results.append(result)

        soak = None
        if args.soak_hours > 0:
            soak = _run_soak(args, ctx, sampler, credit_probe, results, out_dir)
    finally:
        sampler.stop()
        httpd.shutdown()
        if xvfb:
            xvfb.terminate()

    class_results = _by_capacity_class(results)
    limits = admission.compute(class_results, args.nodes)

    summary = {
        "run_id": run_id,
        "generated_at": datetime.now(UTC).isoformat(),
        "mode": "smoke" if args.smoke else "full",
        "smoke_warning": (
            "SMOKE MODE: windows and levels are tiny. These numbers prove the harness "
            "runs; they are NOT capacity findings and must never be reported as such."
        )
        if args.smoke
        else None,
        "plan_ref": "PLAN.md 'Capacity model and the 10 or 50? answer'",
        "host": host,
        "cpu_credit_probe": credit_probe.sample(),
        "ramp": {
            "levels": levels,
            "stabilize_s": stabilize,
            "measure_s": measure,
            "sample_interval_s": config.SAMPLE_INTERVAL_S,
        },
        "guardrail_thresholds": {
            "host_cpu_sustained_pct": config.CPU_SUSTAINED_PCT,
            "host_memory_pct": config.MEM_PCT,
            "disk_util_saturated_pct": config.DISK_UTIL_SATURATED_PCT,
            "encoder_capacity_pct": config.ENCODER_PCT,
            "input_latency_p95_ms": config.INPUT_LATENCY_P95_MS,
            "action_latency_baseline_multiple": config.ACTION_LATENCY_BASELINE_MULT,
            "crash_or_oom": "any",
        },
        "workloads": results,
        "capacity_classes": class_results,
        "admission": limits,
        "soak": soak,
        "completeness": _completeness(results, credit_probe, args),
    }
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2, default=str))
    write_summary(summary, out_dir / "SUMMARY.md")
    print(f"\nwrote {out_dir}/summary.json and {out_dir}/SUMMARY.md")
    print(f"completeness: {summary['completeness']['verdict']}")
    return 0


def _run_soak(
    args,
    ctx: RunContext,
    sampler: Sampler,
    credit_probe: CreditProbe,
    results: list[dict],
    out_dir: Path,
) -> dict:
    """PLAN.md: a minimum six-hour soak on burstable hosts, credit balance beside CPU."""
    from harness.stepper import run_step
    from harness.workloads import by_id

    steady = [r for r in results if r["steady_state"] and r["last_passing_level"]]
    if args.soak_level:
        level = args.soak_level
        workload_id = (args.only or [steady[0]["workload"] if steady else "w2_navigation"])[0]
    elif steady:
        pick = min(steady, key=lambda r: r["last_passing_level"])
        level, workload_id = pick["last_passing_level"], pick["workload"]
    else:
        return {"ran": False, "reason": "no steady-state workload produced a passing level"}

    workload = by_id(workload_id)
    seconds = args.soak_hours * 3600.0
    soak_ctx = RunContext(**{**ctx.__dict__, "measure_s": seconds, "stabilize_s": 60.0})
    print(f"[soak] {workload_id} at concurrency={level} for {args.soak_hours}h", flush=True)
    step = run_step(workload, soak_ctx, level, sampler, credit_probe, None)
    (out_dir / "soak.json").write_text(json.dumps(step, indent=2, default=str))
    return {
        "ran": True,
        "workload": workload_id,
        "concurrency": level,
        "hours": args.soak_hours,
        "meets_plan_minimum_for_burstable": args.soak_hours >= config.SOAK_MIN_HOURS_BURSTABLE,
        "guardrails_crossed": step["guardrails_crossed"],
        "cpu": step["host"]["cpu_busy_pct"],
        "steal": step["host"]["cpu_steal_pct"],
        "cpu_credit": step["cpu_credit"],
        "cpu_credit_samples": step["cpu_credit_samples"],
        "file": str(out_dir / "soak.json"),
    }


def _by_capacity_class(results: list[dict]) -> dict:
    """Lowest measured failure level per class -- the number the 70% rule keys on."""
    out: dict[str, dict] = {}
    for result in results:
        if result["preflight"]["status"] == "skip":
            continue
        entry = out.setdefault(
            result["capacity_class"],
            {
                "failure_level": None,
                "last_passing_level": None,
                "binding_workload": None,
                "workloads": [],
                "skipped_workloads": [],
                "partial_workloads": [],
            },
        )
        entry["workloads"].append(result["workload"])
        if result["preflight"]["status"] == "partial":
            entry["partial_workloads"].append(result["workload"])
        failure = result["failure_level"]
        if failure is not None and (
            entry["failure_level"] is None or failure < entry["failure_level"]
        ):
            entry["failure_level"] = failure
            entry["binding_workload"] = result["workload"]
        passing = result["last_passing_level"]
        if passing is not None and (
            entry["last_passing_level"] is None or passing < entry["last_passing_level"]
        ):
            entry["last_passing_level"] = passing
    for result in results:
        if result["preflight"]["status"] == "skip":
            entry = out.setdefault(
                result["capacity_class"],
                {
                    "failure_level": None,
                    "last_passing_level": None,
                    "binding_workload": None,
                    "workloads": [],
                    "skipped_workloads": [],
                    "partial_workloads": [],
                },
            )
            entry["skipped_workloads"].append(result["workload"])
    return out


def _completeness(results: list[dict], credit_probe: CreditProbe, args) -> dict:
    skipped = [r["workload"] for r in results if r["preflight"]["status"] == "skip"]
    partial = [r["workload"] for r in results if r["preflight"]["status"] == "partial"]
    # A guardrail counts as UNMEASURED for a workload only when no step of that workload
    # could measure it. Level 1 has no action-latency baseline by construction, and
    # reporting that as "never measured" would cry wolf on every single run.
    per_workload_unmeasured: dict[str, list[str]] = {}
    for result in results:
        steps = [s for s in result["steps"]]
        if not steps:
            continue
        never = set(steps[0].get("guardrails_unmeasured") or [])
        for step in steps[1:]:
            never &= set(step.get("guardrails_unmeasured") or [])
        if never:
            per_workload_unmeasured[result["workload"]] = sorted(never)
    unmeasured = {name for names in per_workload_unmeasured.values() for name in names}

    problems: list[str] = []
    if skipped:
        problems.append(f"{len(skipped)} workload(s) skipped: {', '.join(skipped)}")
    if partial:
        problems.append(f"{len(partial)} workload(s) partial: {', '.join(partial)}")
    for workload_id, names in per_workload_unmeasured.items():
        problems.append(
            f"{workload_id}: guardrail(s) never measured at any level: {', '.join(names)}"
        )
    if credit_probe.burstable and args.soak_hours < config.SOAK_MIN_HOURS_BURSTABLE:
        problems.append(
            f"burstable host but soak was {args.soak_hours}h "
            f"(PLAN.md requires >= {config.SOAK_MIN_HOURS_BURSTABLE}h)"
        )
    if credit_probe.burstable:
        final_credit = credit_probe.sample()
        if (
            final_credit.get("source") != "cloudwatch"
            or final_credit.get("cpu_credit_balance") is None
        ):
            problems.append(
                "burstable host but the real CloudWatch CPUCreditBalance is unavailable"
            )
    if args.smoke:
        problems.append("smoke mode: not a capacity measurement")
    if args.headless:
        problems.append("headless: not the production headed-on-Xvfb shape")
    return {
        "verdict": "COMPLETE" if not problems else "INCOMPLETE",
        "problems": problems,
        "skipped_workloads": skipped,
        "partial_workloads": partial,
        "unmeasured_guardrails": sorted(unmeasured),
    }


if __name__ == "__main__":
    sys.exit(main())
