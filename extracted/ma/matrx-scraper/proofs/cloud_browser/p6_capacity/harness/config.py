"""Guardrails, ramp schedule, capacity classes. Phase-0 proof harness (NOT shipped code).

Every threshold here is quoted from PLAN.md §"Capacity model and the '10 or 50?' answer".
Do not tune these to make a host look better; a changed threshold invalidates the
comparison between two hosts, which is the entire point of the harness.

PLAN.md, verbatim:
    "Increase concurrency in steps until any guardrail is crossed: sustained host CPU
     75%, memory 80%, disk p95 saturation, encoder capacity 80%, p95 input latency
     250 ms, p95 automation action latency 2x single-run baseline, or any OOM/crash."

Two of those are not numeric in the plan and are pinned here, flagged, and reported as
harness interpretations (see README "Where the plan needed interpretation"):
  * "disk p95 saturation"  -> p95 of device utilisation >= DISK_UTIL_SATURATED_PCT
  * "any OOM/crash"        -> any unit exiting non-zero/killed, or any kernel OOM line
"""

from __future__ import annotations

# --- PLAN.md guardrails ---------------------------------------------------
CPU_SUSTAINED_PCT = 75.0  # sustained host CPU
MEM_PCT = 80.0  # host memory
DISK_UTIL_SATURATED_PCT = 95.0  # harness interpretation of "disk p95 saturation"
ENCODER_PCT = 80.0  # encoder capacity
INPUT_LATENCY_P95_MS = 250.0  # p95 input latency
ACTION_LATENCY_BASELINE_MULT = 2.0  # p95 action latency vs single-run baseline
CRASH_RATE_MAX = 0.0  # "any OOM/crash"

# "sustained" host CPU: the p95 of the measurement window, not a momentary spike.
CPU_SUSTAINED_STATISTIC = "p95"

# --- admission control ----------------------------------------------------
# PLAN.md: "Production admission is 70% of the lowest measured failure/guardrail count,
# rounded down, and reserves capacity for one worker/node failure."
ADMISSION_FRACTION = 0.70

# --- ramp -----------------------------------------------------------------
DEFAULT_LEVELS = [1, 2, 3, 4, 6, 8, 12, 16, 24, 32, 48, 64]
DEFAULT_STABILIZE_S = 60.0  # discarded from the measurement window
DEFAULT_MEASURE_S = 120.0
SMOKE_STABILIZE_S = 5.0
SMOKE_MEASURE_S = 15.0
SAMPLE_INTERVAL_S = 1.0
CREDIT_SAMPLE_INTERVAL_S = 300.0  # CloudWatch CPU-credit datapoints are 5-minute data

# PLAN.md: "a minimum six-hour soak on burstable hosts"
SOAK_MIN_HOURS_BURSTABLE = 6.0

# --- capacity classes -----------------------------------------------------
# PLAN.md §"The operational model remains" separates these; admission limits are applied
# per class, never pooled.
CLASS_BROWSER_UNSTREAMED = "browser_unstreamed"
CLASS_STREAMED_BROWSER = "streamed_browser"
CLASS_FULL_UI_SANDBOX = "full_ui_sandbox"
CLASS_BURST = "burst"  # start/restore storms -- a rate, not a steady count

CLASS_ORDER = [
    CLASS_BROWSER_UNSTREAMED,
    CLASS_STREAMED_BROWSER,
    CLASS_FULL_UI_SANDBOX,
    CLASS_BURST,
]
