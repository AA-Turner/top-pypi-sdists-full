"""Human summary emitter. Phase-0 proof harness (NOT shipped code).

Writes SUMMARY.md next to summary.json, pre-filled in the shape of
RESULTS-TEMPLATE.md so the operator pastes rather than transcribes. The first thing on
the page is what is MISSING, because a capacity report read as complete when it is not is
the failure this whole harness is built to prevent.
"""

from __future__ import annotations

from pathlib import Path


def _mb(value) -> str:
    if not value:
        return "-"
    return f"{float(value) / (1024 * 1024):.0f} MiB"


def _num(value, suffix: str = "", digits: int = 1) -> str:
    if value is None:
        return "-"
    try:
        return f"{float(value):.{digits}f}{suffix}"
    except (TypeError, ValueError):
        return str(value)


def write_summary(summary: dict, path: Path) -> None:
    host = summary["host"]
    lines: list[str] = []
    add = lines.append

    add("# P6 capacity benchmark — run summary")
    add("")
    add("*Phase-0 proof output. NOT shipped code, NOT a production SLA.*")
    add("")
    if summary.get("smoke_warning"):
        add(f"> 🚨 **{summary['smoke_warning']}**")
        add("")

    comp = summary["completeness"]
    add(f"## Completeness: **{comp['verdict']}**")
    add("")
    if comp["problems"]:
        for problem in comp["problems"]:
            add(f"- ❌ {problem}")
    else:
        add("- every PLAN.md workload ran and every guardrail was measurable on this host")
    add("")

    add("## Host")
    add("")
    add("| field | value |")
    add("|---|---|")
    add(f"| hostname | `{host.get('hostname')}` |")
    add(f"| EC2 instance type | `{(host.get('ec2') or {}).get('instance_type')}` |")
    add(f"| vCPU | {host.get('cpu_count')} |")
    add(f"| RAM | {_mb(host.get('mem_total_bytes'))} |")
    add(f"| CPU model | {host.get('cpu_model')} |")
    add(f"| kernel | {host.get('kernel')} |")
    add(f"| in container | {host.get('in_container')} |")
    add(
        f"| cgroup cpu.max / memory.max | "
        f"`{(host.get('cgroup') or {}).get('cpu_max')}` / "
        f"`{(host.get('cgroup') or {}).get('memory_max')}` |"
    )
    add(f"| GPU | {(host.get('gpu') or {}).get('gpu') or (host.get('gpu') or {}).get('reason')} |")
    add(f"| chromium | {host.get('chromium')} |")
    add(f"| playwright (python) | {host.get('playwright_python')} |")
    add(f"| ffmpeg | {(host.get('tools') or {}).get('ffmpeg')} |")
    add(
        f"| browser / sandbox / selkies image | "
        f"`{(host.get('images') or {}).get('browser_image')}` / "
        f"`{(host.get('images') or {}).get('sandbox_image')}` / "
        f"`{(host.get('images') or {}).get('selkies_image')}` |"
    )
    add("")

    credit = summary.get("cpu_credit_probe") or {}
    add("## CPU credits (burstable hosts)")
    add("")
    add(
        f"- burstable: **{credit.get('burstable')}** (instance type "
        f"`{credit.get('instance_type')}`)"
    )
    add(f"- source: `{credit.get('source')}` — {credit.get('reason') or 'live CloudWatch'}")
    soak = summary.get("soak")
    if soak and soak.get("ran"):
        add(
            f"- soak: {soak['hours']}h at concurrency {soak['concurrency']} "
            f"({soak['workload']}); meets PLAN minimum: "
            f"**{soak['meets_plan_minimum_for_burstable']}**"
        )
        add(
            f"- soak CPU p95 {_num(soak['cpu'].get('p95'), '%')}, "
            f"steal p95 {_num(soak['steal'].get('p95'), '%')}"
        )
        balances = [
            sample.get("measurement", {}).get("cpu_credit_balance")
            for sample in soak.get("cpu_credit_samples", [])
        ]
        balances = [value for value in balances if value is not None]
        if balances:
            add(
                f"- CPUCreditBalance trend: {_num(balances[0])} start → "
                f"{_num(balances[-1])} end; minimum {_num(min(balances))} "
                f"across {len(balances)} samples"
            )
        else:
            add("- CPUCreditBalance trend: **UNMEASURED**")
    else:
        add("- soak: **not run** (PLAN.md requires ≥6 h on a burstable host)")
    add("")

    add("## Per-workload result")
    add("")
    add("| # | workload | class | status | last passing | first failure | binding guardrail |")
    add("|---|---|---|---|---:|---:|---|")
    for result in summary["workloads"]:
        crossed = ""
        for step in result["steps"]:
            if step["guardrails_crossed"]:
                crossed = ", ".join(step["guardrails_crossed"])
        add(
            f"| {result['plan_workload']} | `{result['workload']}` | "
            f"{result['capacity_class']} | {result['preflight']['status']} | "
            f"{result['last_passing_level'] or '-'} | {result['failure_level'] or '-'} | "
            f"{crossed or '-'} |"
        )
    add("")

    for result in summary["workloads"]:
        if result["preflight"]["status"] == "skip":
            add(f"### `{result['workload']}` — SKIPPED")
            add("")
            for reason in result["preflight"]["reasons"]:
                add(f"- {reason}")
            add("")
            continue
        add(f"### `{result['workload']}` — {result['title']}")
        add("")
        if result["preflight"]["reasons"]:
            for reason in result["preflight"]["reasons"]:
                add(f"- ⚠️ {reason}")
            add("")
        add(
            "| conc | CPU p95 | steal p95 | mem p95 | disk util p95 | RSS/unit p95 | "
            "start p95 ms | action p50/p95/p99 ms | enc p95 | crashes |"
        )
        add("|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|")
        for step in result["steps"]:
            action = step["latency_ms"]["action"]
            enc = (step["encoder"]["utilisation_pct"] or {}).get("p95")
            add(
                f"| {step['concurrency']} "
                f"| {_num(step['host']['cpu_busy_pct']['p95'], '%')} "
                f"| {_num(step['host']['cpu_steal_pct']['p95'], '%')} "
                f"| {_num(step['host']['mem_used_pct']['p95'], '%')} "
                f"| {_num(step['host']['disk_util_pct']['p95'], '%')} "
                f"| {_mb(step['units']['rss_per_unit_bytes_p95'])} "
                f"| {_num(step['latency_ms']['browser_start']['p95'], '', 0)} "
                f"| {_num(action['p50'], '', 0)} / {_num(action['p95'], '', 0)} / "
                f"{_num(action['p99'], '', 0)} "
                f"| {_num(enc, '%')} "
                f"| {step['units']['crashes']} |"
            )
        add("")
        add(f"- stopped because: {result['stopped_because']}")
        if result.get("baseline_action_p95_ms"):
            add(
                f"- action-latency baseline (p95 at level "
                f"{result.get('baseline_from_level')}): "
                f"{_num(result['baseline_action_p95_ms'], ' ms', 0)}"
            )
        add("")

    add("## Admission control (computed, not transcribed)")
    add("")
    add(
        "PLAN.md: *70% of the lowest measured failure/guardrail count, rounded down, and "
        "reserves capacity for one worker/node failure.*"
    )
    add("")
    add(
        "| capacity class | binding workload | failure level | **per-node limit** | "
        "fleet limit | basis |"
    )
    add("|---|---|---:|---:|---:|---|")
    for capacity_class, data in summary["admission"].items():
        add(
            f"| {capacity_class} | `{data.get('binding_workload') or '-'}` | "
            f"{data.get('failure_level') or '-'} | **{data.get('limit')}** | "
            f"{data['fleet'].get('fleet_limit')} | {data.get('basis') or '-'} |"
        )
    add("")
    for capacity_class, data in summary["admission"].items():
        if data.get("note"):
            add(f"- `{capacity_class}`: {data['note']}")
        if data["fleet"].get("note"):
            add(f"- `{capacity_class}` fleet: {data['fleet']['note']}")
        if data.get("limit_from_last_passing_level") is not None and data.get("failure_level"):
            add(
                f"- `{capacity_class}`: alternative reading (70% of the last PASSING "
                f"level) = {data['limit_from_last_passing_level']}"
            )
    add("")
    add("## What remains outstanding")
    add("")
    if comp["problems"]:
        for problem in comp["problems"]:
            add(f"- {problem}")
    else:
        add(
            "- nothing on this host; run the same command on the other target shape and "
            "compare with RESULTS-TEMPLATE.md"
        )
    add("")

    path.write_text("\n".join(lines) + "\n")
