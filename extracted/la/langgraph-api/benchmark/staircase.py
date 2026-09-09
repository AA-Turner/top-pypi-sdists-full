# ruff: noqa: T201
"""Staircase capacity benchmark runner.

Monotonically increases load in discrete steps. For each step, invokes k6
for PLATEAU_DURATION seconds. Each VU discards its first WARMUP_ITERS
iterations to warm HTTP connections and server-side caches; only subsequent
iterations contribute to metrics.

Continues past SLO violations (to gather the full curve) but aborts if
error rate exceeds ABORT_ERROR_RATE to avoid destabilising the system.

After all steps complete, capacity is determined analytically: the top of the
highest sustained plateau of SLO-passing steps. A lone passing step above a
sustained failure region does not count (see find_capacity).

Environment variables:
    BASE_URL              Target server URL (default: http://localhost:9123)
    LANGSMITH_API_KEY     API key for authenticated endpoints

    K6_EXECUTOR           k6 executor: constant-vus (default) or constant-arrival-rate
    START_LOAD            Initial load for step 1 — VUs or iter/s (default: 40)
    STEP_SIZE             Load added per step (default: 20)
    NUM_STEPS             Max number of steps (default: 18)
    PLATEAU_DURATION      Seconds per step (default: 60)

    MAX_VUS               Fixed max VUs for constant-arrival-rate (overrides multiplier)
    MAX_VUS_MULTIPLIER    Max VUs = target * multiplier (default: 10)
    PRE_ALLOCATED_VUS     Pre-allocated VUs for constant-arrival-rate (default: target)

    WARMUP_ITERS          Iterations discarded per VU for warmup (default: 1)
    COOLDOWN_DURATION     Idle seconds between steps (default: 5)

    MIN_SUCCESS_RATE      SLO: minimum success rate % (default: 99)
    MAX_P50_DURATION_MS   SLO: maximum median duration in ms (default: 3000)
    MAX_P95_DURATION_MS   SLO: maximum p95 duration in ms (default: 10000)
    ABORT_ERROR_RATE      Stop the staircase if error rate exceeds this % (default: 10)
    CAPACITY_CONSECUTIVE_PASSES
                          Passing steps required to confirm capacity (default: 2)
    MIN_ITERS_PER_VU      Completed iterations per VU a step needs before it may
                          set capacity (default: 3)

    BENCHMARK_TYPE        Benchmark runner type (default: wait_write)
    BENCHMARK_PROFILE     Optional profile override (e.g. etsy, metaview)
    DEPLOYMENT_SLUG       Deployment slug for capacity CI metadata (optional)
    COMPUTE_TIER          Compute tier for capacity CI metadata (optional)
    SUMMARY_PATH          Output path for summary JSON (default: staircase_summary.json)
    RUN_MODE              stateless (default) or stateful
    DATA_SIZE, DELAY, EXPAND, STEPS, MODE — agent parameters
"""

import json
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path

BASE_URL = os.environ.get("BASE_URL", "http://localhost:9123")
K6_EXECUTOR = os.environ.get("K6_EXECUTOR", "constant-vus")
IS_ARRIVAL_RATE = K6_EXECUTOR == "constant-arrival-rate"
START_LOAD = int(os.environ.get("START_LOAD", "40"))
STEP_SIZE = int(os.environ.get("STEP_SIZE", "20"))
NUM_STEPS = int(os.environ.get("NUM_STEPS", "18"))
PLATEAU_DURATION = int(os.environ.get("PLATEAU_DURATION", "60"))
WARMUP_ITERS = int(os.environ.get("WARMUP_ITERS", "1"))
COOLDOWN_DURATION = int(os.environ.get("COOLDOWN_DURATION", "5"))
MAX_VUS_MULTIPLIER = int(os.environ.get("MAX_VUS_MULTIPLIER", "10"))
UNIT = "iter/s" if IS_ARRIVAL_RATE else "VUs"

MIN_SUCCESS_RATE = float(os.environ.get("MIN_SUCCESS_RATE", "99"))
MAX_P50_DURATION_MS = int(os.environ.get("MAX_P50_DURATION_MS", "3000"))
MAX_P95_DURATION_MS = int(os.environ.get("MAX_P95_DURATION_MS", "10000"))
ABORT_ERROR_RATE = float(os.environ.get("ABORT_ERROR_RATE", "10"))
CAPACITY_CONSECUTIVE_PASSES = int(os.environ.get("CAPACITY_CONSECUTIVE_PASSES", "2"))
# A floor rather than a derived optimum: the smallest value leaving more than one
# post-warmup sample per VU with any margin.
MIN_ITERS_PER_VU = float(os.environ.get("MIN_ITERS_PER_VU", "3"))

BENCHMARK_TYPE = os.environ.get("BENCHMARK_TYPE", "wait_write")
BENCHMARK_PROFILE = os.environ.get("BENCHMARK_PROFILE", "default")
DEPLOYMENT_SLUG = os.environ.get("DEPLOYMENT_SLUG", "")
COMPUTE_TIER = os.environ.get("COMPUTE_TIER", "")
SUMMARY_PATH = os.environ.get("SUMMARY_PATH", "staircase_summary.json")

K6_SCRIPT = Path(__file__).parent / "staircase_step_k6.js"


def validate_geometry() -> None:
    """Reject staircase geometry that cannot produce a result.

    These are reachable from the workflow_dispatch inputs, so they are an input
    boundary rather than developer-only config. PLATEAU_DURATION in particular
    is a divisor for every throughput figure, and a zero would surface as a
    ZeroDivisionError two thirds of the way through a step.
    """
    problems = [
        f"{name} must be >= 1, got {value}"
        for name, value in (
            ("START_LOAD", START_LOAD),
            ("STEP_SIZE", STEP_SIZE),
            ("NUM_STEPS", NUM_STEPS),
            ("PLATEAU_DURATION", PLATEAU_DURATION),
        )
        if value < 1
    ]
    if COOLDOWN_DURATION < 0:
        problems.append(f"COOLDOWN_DURATION must be >= 0, got {COOLDOWN_DURATION}")
    if WARMUP_ITERS < 0:
        problems.append(f"WARMUP_ITERS must be >= 0, got {WARMUP_ITERS}")
    if problems:
        raise SystemExit("Invalid staircase configuration: " + "; ".join(problems))


def run_step(target: int) -> dict | None:
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as result_file:
        result_path = result_file.name

    env = {
        **os.environ,
        "BASE_URL": BASE_URL,
        "TARGET": str(target),
        "PLATEAU_DURATION": str(PLATEAU_DURATION),
        "WARMUP_ITERS": str(WARMUP_ITERS),
        "K6_RESULT_FILE": result_path,
        "K6_EXECUTOR": K6_EXECUTOR,
    }
    if IS_ARRIVAL_RATE:
        env.setdefault("MAX_VUS", str(target * MAX_VUS_MULTIPLIER))
        env.setdefault("PRE_ALLOCATED_VUS", str(target))

    try:
        proc = subprocess.run(["k6", "run", str(K6_SCRIPT)], env=env)
        if proc.returncode != 0:
            print(f"k6 failed at target={target} (exit code {proc.returncode})")
            return None
    except FileNotFoundError:
        print(
            "k6 not found — install from https://k6.io/docs/get-started/installation/"
        )
        sys.exit(1)
    finally:
        try:
            data = Path(result_path).read_text().strip()
        except FileNotFoundError:
            data = ""
        os.unlink(result_path)

    if not data:
        print(f"No JSON output from k6 at target={target}")
        return None

    return json.loads(data)


def check_slo(metrics: dict) -> bool:
    if metrics["totalRuns"] == 0:
        return False
    # An iteration killed at gracefulStop never reaches totalRuns, successRate
    # or either duration percentile, so a step can report 100% success and fast
    # latency from the surviving subset while a quarter of its work never
    # finished. That is not evidence the deployment held at this load. It also
    # cannot happen on a healthy step: truncation means an iteration ran past
    # gracefulStop, six times the p95 SLO.
    if metrics.get("truncatedRuns", 0) > 0:
        return False
    if metrics["successRate"] < MIN_SUCCESS_RATE:
        return False
    if (
        metrics.get("medDurationMs") is not None
        and metrics["medDurationMs"] > MAX_P50_DURATION_MS
    ):
        return False
    return (
        metrics.get("p95DurationMs") is None
        or metrics["p95DurationMs"] <= MAX_P95_DURATION_MS
    )


def should_abort(metrics: dict) -> bool:
    """Abort the staircase if the error rate is dangerously high."""
    if metrics["totalRuns"] == 0:
        return True
    error_rate = 100.0 - metrics["successRate"]
    return error_rate > ABORT_ERROR_RATE


def has_enough_samples(step: dict, min_iters_per_vu: float = MIN_ITERS_PER_VU) -> bool:
    """Whether a step measured enough iterations per VU to be worth believing.

    At the top of a staircase the sample can collapse: 1000 VUs over a 60s
    plateau with a 36.5s median yields about 1.6 iterations per VU, and
    WARMUP_ITERS discards the first. One sample per VU is noise.

    Deliberately *not* symmetric, see find_capacity. A thin sample can never
    grant capacity but must still be able to deny it, because a step often has
    few samples precisely because the deployment is collapsing; treating that as
    "no data" would let capacity climb past a real breaking point.
    """
    if "totalRuns" not in step:
        # Nothing to judge, so defer to the step's own SLO verdict. check_slo
        # already rejects totalRuns == 0, so a passing step always has a sample.
        return True
    target = step.get("targetVUs") or 0
    if target <= 0:
        return False
    return step["totalRuns"] / target >= min_iters_per_vu


def find_capacity(
    steps: list[dict], consecutive: int = CAPACITY_CONSECUTIVE_PASSES
) -> int:
    """Find the top of the highest sustained plateau of SLO-passing steps.

    Returns the highest step that passes SLO *and* is corroborated by the
    `consecutive - 1` steps below it also passing, so neither a transient
    failure at a lower step nor a lone pass above a sustained failure region
    can set capacity. Near the bottom the window is clamped: step 1 needs only
    itself, having nothing beneath it to corroborate.
    """
    passed = {step["step"] for step in steps if step.get("passesSLO")}
    # Asymmetric on purpose: a thin sample cannot grant capacity, but it stays
    # in `passed` for corroboration and still denies capacity by being absent
    # when it failed. See has_enough_samples.
    eligible = {
        step["step"]
        for step in steps
        if step.get("passesSLO") and has_enough_samples(step)
    }
    for step in sorted(eligible, reverse=True):
        window = range(max(1, step - consecutive + 1), step + 1)
        if all(candidate in passed for candidate in window):
            return step
    return 0


def fmt(val, width: int) -> str:
    return str(val if val is not None else "-").ljust(width)


def main():
    validate_geometry()

    max_load = START_LOAD + STEP_SIZE * (NUM_STEPS - 1)
    step_duration = PLATEAU_DURATION + COOLDOWN_DURATION
    est_minutes = (NUM_STEPS * step_duration) / 60

    print("\nStaircase capacity benchmark")
    print(f"Executor: {K6_EXECUTOR}")
    if IS_ARRIVAL_RATE:
        fixed_max = os.environ.get("MAX_VUS")
        if fixed_max:
            print(
                f"{NUM_STEPS} steps: {START_LOAD} to {max_load} {UNIT} (step +{STEP_SIZE}), max VUs: {fixed_max}"
            )
        else:
            print(
                f"{NUM_STEPS} steps: {START_LOAD} to {max_load} {UNIT} (step +{STEP_SIZE}), max VUs: target * {MAX_VUS_MULTIPLIER}"
            )
    else:
        print(
            f"{NUM_STEPS} steps: {START_LOAD} to {max_load} {UNIT} (step +{STEP_SIZE})"
        )
    print(
        f"Per step: {PLATEAU_DURATION}s plateau + {COOLDOWN_DURATION}s cooldown (first {WARMUP_ITERS} iter/VU discarded)"
    )
    print(f"Estimated wall time: {est_minutes:.1f} min")
    print(
        f"SLO: success >= {MIN_SUCCESS_RATE}%, p50 <= {MAX_P50_DURATION_MS}ms, p95 <= {MAX_P95_DURATION_MS}ms"
    )
    print(f"Abort threshold: >{ABORT_ERROR_RATE}% error rate")
    print(f"Target: {BASE_URL}\n")

    steps: list[dict] = []

    for i in range(1, NUM_STEPS + 1):
        target = START_LOAD + STEP_SIZE * (i - 1)
        print(f"\n--- Step {i}/{NUM_STEPS}: {target} {UNIT} ---")

        metrics = run_step(target)

        if metrics is None:
            steps.append(
                {"step": i, "targetVUs": target, "error": True, "passesSLO": False}
            )
            print("  k6 error — aborting")
            break

        passes = check_slo(metrics)
        step_data = {"step": i, "targetVUs": target, **metrics, "passesSLO": passes}
        steps.append(step_data)

        icon = "✅" if passes else "❌"
        tput = metrics["successfulRuns"] / PLATEAU_DURATION
        print(
            f"  {icon} {metrics['successRate']:.1f}% success, "
            f"med={metrics['medDurationMs']}ms, "
            f"p95={metrics['p95DurationMs']}ms, "
            f"p99={metrics['p99DurationMs']}ms, "
            f"n={metrics['totalRuns']}, "
            f"throughput={tput:.1f} runs/sec"
        )

        floored = metrics.get("durationsFlooredAtTimeout") or 0
        if floored:
            # Those durations are a floor, not a measurement, so med/p95 above
            # understate how slow the step really was.
            print(
                f"  NOTE: {floored} request(s) hit the "
                f"{metrics.get('requestTimeoutMs')}ms timeout; their durations are "
                f"'at least' values, not exact"
            )

        if metrics.get("truncatedRuns"):
            # Should be 0: gracefulStop is set so iterations terminate rather
            # than being killed. Anything else means the step ran long enough
            # that k6 gave up on it, and the numbers above are missing those.
            print(
                f"  WARNING: {metrics['truncatedRuns']} iteration(s) killed before "
                f"finishing; excluded from the numbers above, so this step fails SLO"
            )

        if should_abort(metrics):
            print(f"  Error rate >{ABORT_ERROR_RATE}% — aborting staircase")
            break

        if i < NUM_STEPS and COOLDOWN_DURATION > 0:
            print(f"  Cooling down {COOLDOWN_DURATION}s ...")
            time.sleep(COOLDOWN_DURATION)

    # --- Summary table ---
    sep = "=" * 115
    print(f"\n{sep}")
    print("STAIRCASE CAPACITY RESULTS")
    print(sep)
    target_col = "Rate" if IS_ARRIVAL_RATE else "VUs"
    header = (
        f"{'Step':<6}{target_col:<6}{'Runs':<8}{'# Fail':<8}{'Success%':<12}"
        f"{'Med(ms)':<10}{'Avg(ms)':<10}{'p95(ms)':<10}{'p99(ms)':<10}"
        f"{'Tput(r/s)':<10}{'SLO':<5}"
    )
    print(header)
    print("-" * 115)
    for s in steps:
        if s.get("error"):
            print(f"{fmt(s['step'], 6)}{fmt(s['targetVUs'], 6)}ERROR")
            continue
        icon = "✅" if s["passesSLO"] else "❌"
        tput = f"{s['successfulRuns'] / PLATEAU_DURATION:.1f}"
        print(
            f"{fmt(s['step'], 6)}{fmt(s['targetVUs'], 6)}{fmt(s['totalRuns'], 8)}"
            f"{fmt(s.get('failedRuns', 0), 8)}"
            f"{s['successRate']:>7.2f}     "
            f"{fmt(s.get('medDurationMs'), 10)}{fmt(s.get('avgDurationMs'), 10)}"
            f"{fmt(s.get('p95DurationMs'), 10)}{fmt(s.get('p99DurationMs'), 10)}"
            f"{fmt(tput, 10)}{icon}"
        )
    print("-" * 115)

    capacity_step = find_capacity(steps)
    capacity_vus = (
        START_LOAD + STEP_SIZE * (capacity_step - 1) if capacity_step > 0 else 0
    )

    # Only SLO-passing steps count; the max over every step is throughput at
    # any cost, measured while the deployment was already failing.
    healthy_steps = [
        s
        for s in steps
        if not s.get("error") and s.get("totalRuns", 0) > 0 and s.get("passesSLO")
    ]
    max_throughput = 0.0
    max_throughput_vus = 0
    for s in healthy_steps:
        tput = s["successfulRuns"] / PLATEAU_DURATION
        if tput > max_throughput:
            max_throughput = tput
            max_throughput_vus = s["targetVUs"]

    capacity_throughput = next(
        (
            round(s["successfulRuns"] / PLATEAU_DURATION, 1)
            for s in steps
            if s["step"] == capacity_step
        ),
        None,
    )

    if capacity_step > 0:
        total_runs = sum(s.get("totalRuns", 0) for s in steps if s.get("passesSLO"))
        print(
            f"Max capacity subject to SLO: {capacity_vus} {UNIT} (step {capacity_step})"
        )
        print(f"Total runs (SLO-passing steps): {total_runs}")
    else:
        print("No step met SLO thresholds")

    if max_throughput > 0:
        print(
            f"Max throughput: {max_throughput:.1f} successful runs/sec (at {max_throughput_vus} {UNIT})"
        )
    print(sep)

    summary = {
        "capacity": {
            "step": capacity_step,
            "targetVUs": capacity_vus,
            # The number a customer actually cares about. VU count is an
            # artefact of a closed-model load generator; runs/sec is the
            # service rate, and it orders the tiers correctly where VU
            # capacity has been tying L with M.
            "successfulRunsPerSec": capacity_throughput,
        }
        if capacity_step > 0
        else None,
        "maxThroughput": {
            "successfulRunsPerSec": round(max_throughput, 2),
            "atVUs": max_throughput_vus,
        }
        if max_throughput > 0
        else None,
        "config": {
            "k6Executor": K6_EXECUTOR,
            "startLoad": START_LOAD,
            "stepSize": STEP_SIZE,
            "numSteps": NUM_STEPS,
            "plateauDurationSeconds": PLATEAU_DURATION,
            "warmupIters": WARMUP_ITERS,
            "cooldownDurationSeconds": COOLDOWN_DURATION,
            "minSuccessRate": MIN_SUCCESS_RATE,
            "maxP50DurationMs": MAX_P50_DURATION_MS,
            "maxP95DurationMs": MAX_P95_DURATION_MS,
            "abortErrorRate": ABORT_ERROR_RATE,
            "capacityConsecutivePasses": CAPACITY_CONSECUTIVE_PASSES,
            "baseUrl": BASE_URL,
            "benchmarkType": BENCHMARK_TYPE,
            "benchmarkProfile": BENCHMARK_PROFILE,
            "deploymentSlug": DEPLOYMENT_SLUG or None,
            "computeTier": COMPUTE_TIER or None,
        },
        "steps": steps,
    }
    Path(SUMMARY_PATH).write_text(json.dumps(summary, indent=2))
    print(f"\nResults written to {SUMMARY_PATH}")


if __name__ == "__main__":
    main()
