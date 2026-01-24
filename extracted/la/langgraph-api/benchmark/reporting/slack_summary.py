#!/usr/bin/env python3
"""
Aggregate benchmark results and generate a Slack summary message.
"""

import json
import sys
from collections import defaultdict
from datetime import UTC
from pathlib import Path

MAX_MIXED_SCENARIOS = 3
MAX_CAPACITY_CONFIGS = 3
DATADOG_DASHBOARD_URL = "https://langchain-us.datadoghq.com/dashboard/kkw-wp3-jnp/langgraph-server-benchmarks-anirudh"


def load_json_files(results_dir: str) -> tuple[list[dict], list[dict]]:
    """Load all mixed workload and capacity summary JSON files."""
    mixed_results = []
    capacity_results = []

    results_path = Path(results_dir)
    if not results_path.exists():
        return mixed_results, capacity_results

    for f in results_path.glob("**/*.json"):
        if "job_info" in f.name:
            continue
        try:
            with open(f) as fp:
                data = json.load(fp)
                if (
                    "mixed_workload" in f.name
                    or data.get("config", {}).get("benchmarkType") == "mixed_workload"
                ):
                    mixed_results.append(data)
                elif "capacity_summary" in f.name:
                    capacity_results.append(data)
        except (OSError, json.JSONDecodeError):
            continue

    return mixed_results, capacity_results


def format_pct(value: float | None) -> str:
    """Format percentage value."""
    if value is None:
        return "N/A"
    return f"{value:.1f}%"


def format_duration(value: float | None) -> str:
    """Format duration in seconds."""
    if value is None:
        return "N/A"
    return f"{value:.2f}s"


def get_deployment_short_name(base_url_name: str | None) -> str:
    """Extract short deployment name like 's', 'm', 'l', 'dr-s', etc."""
    if not base_url_name:
        return "unknown"
    # base_url_name is like "benchmark-dr-l" or "benchmark-s"
    name = base_url_name.replace("benchmark-", "")
    return name


def generate_mixed_workload_summary(results: list[dict]) -> str:
    """Generate a table-style summary for mixed workload benchmarks."""
    if not results:
        return "*Mixed Workload*: No results collected\n"

    # Group by deployment and scenario
    # Structure: {deployment: {scenario: {quick: {...}, long: {...}}}}
    by_deployment = defaultdict(lambda: defaultdict(dict))

    for r in results:
        settings = r.get("settings", {})
        deployment = get_deployment_short_name(settings.get("baseUrlName"))
        scenario = settings.get("scenario", "unknown")

        quick = r.get("quick", {})
        long_data = r.get("long", {})

        by_deployment[deployment][scenario] = {
            "quick_success": quick.get("successRate"),
            "quick_p50": quick.get("runDuration", {}).get("p50"),
            "quick_p95": quick.get("runDuration", {}).get("p95"),
            "long_success": long_data.get("successRate"),
            "long_p50": long_data.get("runDuration", {}).get("p50"),
            "long_p95": long_data.get("runDuration", {}).get("p95"),
        }

    # Build summary text
    lines = ["*Short and Long running task benchmark*\n"]

    # Sort deployments: standard first, then DR
    standard = ["s", "m", "l"]
    dr = ["dr-s", "dr-m", "dr-l"]
    all_deployments = [d for d in standard if d in by_deployment] + [
        d for d in dr if d in by_deployment
    ]

    # Get all scenarios across all deployments
    all_scenarios = set()
    for dep_data in by_deployment.values():
        all_scenarios.update(dep_data.keys())
    all_scenarios = sorted(all_scenarios)

    # Create comparison table for each scenario (truncate if too many)
    scenarios_to_show = all_scenarios[:MAX_MIXED_SCENARIOS]
    truncated = len(all_scenarios) > MAX_MIXED_SCENARIOS

    for scenario in scenarios_to_show:
        lines.append(f"\n`{scenario}`:")
        lines.append("```")
        lines.append(
            f"{'Dep':<6} | {'Q-Succ':>7} | {'Q-P50':>6} | {'Q-P95':>6} | {'L-Succ':>7} | {'L-P50':>6} | {'L-P95':>6}"
        )
        lines.append("-" * 65)

        for dep in all_deployments:
            if scenario in by_deployment[dep]:
                data = by_deployment[dep][scenario]
                lines.append(
                    f"{dep:<6} | "
                    f"{format_pct(data['quick_success']):>7} | "
                    f"{format_duration(data['quick_p50']):>6} | "
                    f"{format_duration(data['quick_p95']):>6} | "
                    f"{format_pct(data['long_success']):>7} | "
                    f"{format_duration(data['long_p50']):>6} | "
                    f"{format_duration(data['long_p95']):>6}"
                )
        lines.append("```")

    if truncated:
        lines.append(
            f"\n_...and {len(all_scenarios) - MAX_MIXED_SCENARIOS} more scenarios (see Datadog for full details)_"
        )

    return "\n".join(lines)


def generate_capacity_summary(results: list[dict]) -> str:
    """Generate a summary for capacity benchmarks.

    Only includes results from the highest ramp level (target) for each deployment size
    """
    if not results:
        return "*Capacity Benchmarks*: No results collected\n"

    # Group by deployment and config (expand x steps)
    # For each deployment+config, only keep the result with the highest target
    by_deployment = defaultdict(lambda: defaultdict(dict))

    for r in results:
        settings = r.get("settings", {})
        deployment = get_deployment_short_name(settings.get("baseUrlName"))
        target = settings.get("target", 0)

        config = r.get("config", {})
        expand = config.get("expand", "?")
        steps = config.get("steps", "?")
        data_size = config.get("dataSize", "?")
        config_key = f"e{expand}s{steps}d{data_size}"

        metrics = r.get("metrics", {})

        existing = by_deployment[deployment].get(config_key)
        if existing is None or target > existing.get("target", 0):
            by_deployment[deployment][config_key] = {
                "target": target,
                "success_rate": metrics.get("successRate"),
                "p50": metrics.get("runDuration", {}).get("p50"),
                "p95": metrics.get("runDuration", {}).get("p95"),
                "total_runs": metrics.get("totalRuns"),
            }

    max_target = 0
    for dep_data in by_deployment.values():
        for config_data in dep_data.values():
            max_target = max(max_target, config_data.get("target", 0))

    lines = [f"*Capacity Benchmark Results* (at {max_target} concurrent runs)\n"]

    # Sort deployments
    standard = ["s", "m", "l"]
    dr = ["dr-s", "dr-m", "dr-l"]
    all_deployments = [d for d in standard if d in by_deployment] + [
        d for d in dr if d in by_deployment
    ]

    # Get all configs
    all_configs = set()
    for dep_data in by_deployment.values():
        all_configs.update(dep_data.keys())
    all_configs = sorted(all_configs)

    # Show summary per config (truncate if too many)
    configs_to_show = all_configs[:MAX_CAPACITY_CONFIGS]
    truncated = len(all_configs) > MAX_CAPACITY_CONFIGS

    for config_key in configs_to_show:
        lines.append(f"\n`{config_key}`:")
        lines.append("```")
        lines.append(
            f"{'Dep':<6} | {'Success':>8} | {'P50':>7} | {'P95':>7} | {'Target':>6}"
        )
        lines.append("-" * 47)

        for dep in all_deployments:
            if config_key in by_deployment[dep]:
                data = by_deployment[dep][config_key]
                target = data.get("target")
                target_str = str(target) if target is not None else "N/A"
                lines.append(
                    f"{dep:<6} | "
                    f"{format_pct(data['success_rate']):>8} | "
                    f"{format_duration(data['p50']):>7} | "
                    f"{format_duration(data['p95']):>7} | "
                    f"{target_str:>6}"
                )
        lines.append("```")

    if truncated:
        lines.append(
            f"\n_...and {len(all_configs) - MAX_CAPACITY_CONFIGS} more configs (see Datadog for full details)_"
        )

    return "\n".join(lines)


def generate_slack_message(
    header: str,
    sections: list[str],
    run_url: str,
    total_results: int,
) -> str:
    """Generate the full Slack message.

    Args:
        header: The header/title for the message
        sections: List of formatted section strings to include
        run_url: GitHub Actions run URL
        total_results: Total number of results for status determination
    """
    status_emoji = "🟢" if total_results > 0 else "🔴"
    status = "Completed" if total_results > 0 else "No results collected"

    lines = [
        f"{header} {status_emoji}",
        f"*Status*: {status}",
        "",
    ]

    for section in sections:
        lines.append(section)
        lines.append("")

    # Footer
    from datetime import datetime

    run_time = datetime.now(UTC).strftime("%Y-%m-%d %H:%M UTC")
    lines.extend(
        [
            f"📁 *View Details*: <{run_url}|GitHub Actions Run>",
            f"📈 *Datadog Dashboard*: <{DATADOG_DASHBOARD_URL}|View detailed metrics>",
            "",
            f"🕐 *Run Time*: {run_time}",
        ]
    )

    return "\n".join(lines)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.stderr.write(
            "Usage: slack_summary.py <results_dir> <github_run_url> [--capacity-only|--mixed-only]\n"
        )
        sys.exit(1)

    results_dir = sys.argv[1]
    run_url = sys.argv[2]
    capacity_only = "--capacity-only" in sys.argv
    mixed_only = "--mixed-only" in sys.argv

    mixed_results, capacity_results = load_json_files(results_dir)

    sections = []

    if capacity_only:
        header = "📊 *Capacity Benchmark Summary*"
        sections.append(generate_capacity_summary(capacity_results))
    elif mixed_only:
        header = "📊 *Mixed Workload Benchmark Summary*"
        sections.append(generate_mixed_workload_summary(mixed_results))
    else:
        header = "📊 *Daily Distributed Runtime vs Regular Runtime Benchmark Summary*"
        sections.append(generate_mixed_workload_summary(mixed_results))
        sections.append(generate_capacity_summary(capacity_results))

    if capacity_only:
        total = len(capacity_results)
    elif mixed_only:
        total = len(mixed_results)
    else:
        total = len(mixed_results) + len(capacity_results)

    message = generate_slack_message(header, sections, run_url, total)
    sys.stdout.write(message)
