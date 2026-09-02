"""Guardrail evaluation for one concurrency step. Phase-0 proof harness (NOT shipped code).

One rule per PLAN.md guardrail. Each returns a verdict dict:
    {name, crossed: bool|None, observed, threshold, statistic, note}

`crossed=None` means UNMEASURED -- the metric does not apply to this workload or the
capability was absent. An unmeasured guardrail never fails a step and never passes it
silently: the step result carries the list of unmeasured guardrails and the run summary
refuses to call that workload "complete".
"""

from __future__ import annotations

from . import config
from .metrics import percentile


def _v(name, crossed, observed, threshold, statistic, note=None):
    return {
        "name": name,
        "crossed": crossed,
        "observed": observed,
        "threshold": threshold,
        "statistic": statistic,
        "note": note,
    }


def evaluate(
    *,
    samples: list[dict],
    action_latencies_ms: list[float],
    input_latencies_ms: list[float] | None,
    encoder_pct: list[float] | None,
    baseline_action_p95_ms: float | None,
    crashes: int,
    units_started: int,
    oom_lines: list[str],
) -> list[dict]:
    cpu = [s["cpu_busy_pct"] for s in samples if s.get("cpu_busy_pct") is not None]
    mem = [s["mem_used_pct"] for s in samples if s.get("mem_used_pct") is not None]
    disk = [s["disk_util_pct"] for s in samples if s.get("disk_util_pct") is not None]

    out: list[dict] = []

    cpu_stat = percentile(cpu, 95)
    out.append(
        _v(
            "host_cpu_sustained",
            None if cpu_stat is None else cpu_stat >= config.CPU_SUSTAINED_PCT,
            cpu_stat,
            config.CPU_SUSTAINED_PCT,
            f"cpu_busy_pct {config.CPU_SUSTAINED_STATISTIC}",
            "iowait excluded from busy; steal reported separately",
        )
    )

    mem_stat = percentile(mem, 95)
    out.append(
        _v(
            "host_memory",
            None if mem_stat is None else mem_stat >= config.MEM_PCT,
            mem_stat,
            config.MEM_PCT,
            "mem_used_pct p95",
            "(MemTotal - MemAvailable) / MemTotal",
        )
    )

    disk_stat = percentile(disk, 95)
    out.append(
        _v(
            "disk_saturation",
            None if disk_stat is None else disk_stat >= config.DISK_UTIL_SATURATED_PCT,
            disk_stat,
            config.DISK_UTIL_SATURATED_PCT,
            "disk_util_pct p95",
            "harness interpretation of PLAN.md 'disk p95 saturation'",
        )
    )

    enc_stat = percentile(encoder_pct, 95) if encoder_pct else None
    out.append(
        _v(
            "encoder_capacity",
            None if enc_stat is None else enc_stat >= config.ENCODER_PCT,
            enc_stat,
            config.ENCODER_PCT,
            "encoder_utilisation_pct p95",
            None if enc_stat is not None else "no encoder in this workload / not measurable",
        )
    )

    inp_stat = percentile(input_latencies_ms, 95) if input_latencies_ms else None
    out.append(
        _v(
            "input_latency",
            None if inp_stat is None else inp_stat >= config.INPUT_LATENCY_P95_MS,
            inp_stat,
            config.INPUT_LATENCY_P95_MS,
            "input_latency_ms p95",
            None if inp_stat is not None else "requires an interactive stream plane",
        )
    )

    act_stat = percentile(action_latencies_ms, 95) if action_latencies_ms else None
    act_threshold = (
        baseline_action_p95_ms * config.ACTION_LATENCY_BASELINE_MULT
        if baseline_action_p95_ms
        else None
    )
    out.append(
        _v(
            "action_latency_vs_baseline",
            None if (act_stat is None or act_threshold is None) else act_stat >= act_threshold,
            act_stat,
            act_threshold,
            "action_latency_ms p95",
            "baseline is this workload's own concurrency=1 p95"
            if act_threshold
            else "no concurrency=1 baseline yet (this IS the baseline step)",
        )
    )

    crash_rate = (crashes / units_started) if units_started else 0.0
    out.append(
        _v(
            "crash_or_oom",
            bool(crashes) or bool(oom_lines),
            {
                "crashes": crashes,
                "units": units_started,
                "rate": crash_rate,
                "kernel_oom_lines": len(oom_lines),
            },
            config.CRASH_RATE_MAX,
            "any unit exit != 0 / killed, or kernel OOM line",
            None,
        )
    )
    return out


def any_crossed(verdicts: list[dict]) -> list[str]:
    return [v["name"] for v in verdicts if v["crossed"] is True]


def unmeasured(verdicts: list[dict]) -> list[str]:
    return [v["name"] for v in verdicts if v["crossed"] is None]
