#!/usr/bin/env python3
"""
Generate Slack message for slowest runs (to be posted as a thread reply).
"""

import json
import sys
from collections import defaultdict
from pathlib import Path


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


def get_deployment_short_name(base_url_name: str | None) -> str:
    """Extract short deployment name like 's', 'm', 'l', 'dr-s', etc."""
    if not base_url_name:
        return "unknown"
    name = base_url_name.replace("benchmark-", "")
    return name


def generate_mixed_slowest_runs(
    results: list[dict], max_runs_per_config: int = 5
) -> str:
    """Generate slowest runs message for mixed workload benchmarks (DR only)."""
    if not results:
        return ""

    # Group by deployment+scenario, then by quick/long
    # Structure: {(deployment, scenario): {"quick": [...], "long": [...]}}
    by_config = defaultdict(lambda: {"quick": [], "long": [], "baseUrl": ""})

    for r in results:
        settings = r.get("settings", {})
        deployment = get_deployment_short_name(settings.get("baseUrlName"))
        base_url = settings.get("baseUrl", "")
        scenario = settings.get("scenario", "unknown")

        # Only include DR deployments
        if not deployment.startswith("dr-"):
            continue

        config_key = (deployment, scenario)
        by_config[config_key]["baseUrl"] = base_url
        slowest = r.get("slowestRuns", {})

        for run in slowest.get("quick", []):
            by_config[config_key]["quick"].append(run)
        for run in slowest.get("long", []):
            by_config[config_key]["long"].append(run)

    if not by_config:
        return ""

    # Check if there are any actual slowest runs across all configs
    has_any_runs = any(data["quick"] or data["long"] for data in by_config.values())
    if not has_any_runs:
        return ""

    lines = ["*Slowest Runs - Mixed Workload (DR)*"]

    # Sort configs for consistent output
    for config_key in sorted(by_config.keys()):
        deployment, scenario = config_key
        data = by_config[config_key]
        base_url = data["baseUrl"]

        # Sort each list by duration descending
        data["quick"].sort(key=lambda x: x.get("durationSeconds", 0), reverse=True)
        data["long"].sort(key=lambda x: x.get("durationSeconds", 0), reverse=True)

        if not data["quick"] and not data["long"]:
            continue

        lines.append(f"\n`{deployment}` / `{scenario}` (baseUrl: `{base_url}`)")

        if data["quick"]:
            lines.append("```")
            lines.append("Quick:")
            lines.append(f"{'Duration':<10} {'ThreadId':<40} {'RunId':<40}")
            lines.append("-" * 90)
            for run in data["quick"][:max_runs_per_config]:
                dur = run.get("durationSeconds")
                run_id = run.get("runId", "?")
                thread_id = run.get("threadId", "?")
                dur_str = f"{dur:.2f}s" if dur else "?"
                lines.append(f"{dur_str:<10} {thread_id:<40} {run_id:<40}")
            lines.append("```")

        if data["long"]:
            lines.append("```")
            lines.append("Long:")
            lines.append(f"{'Duration':<10} {'ThreadId':<40} {'RunId':<40}")
            lines.append("-" * 90)
            for run in data["long"][:max_runs_per_config]:
                dur = run.get("durationSeconds")
                run_id = run.get("runId", "?")
                thread_id = run.get("threadId", "?")
                dur_str = f"{dur:.2f}s" if dur else "?"
                lines.append(f"{dur_str:<10} {thread_id:<40} {run_id:<40}")
            lines.append("```")

    return "\n".join(lines)


def generate_capacity_slowest_runs(
    results: list[dict], max_runs_per_config: int = 5
) -> str:
    """Generate slowest runs message for capacity benchmarks (DR only)."""
    if not results:
        return ""

    # Group by deployment+config
    # Structure: {(deployment, config_key): {"runs": [...], "baseUrl": ""}}
    by_config = defaultdict(lambda: {"runs": [], "baseUrl": ""})

    for r in results:
        settings = r.get("settings", {})
        deployment = get_deployment_short_name(settings.get("baseUrlName"))
        base_url = settings.get("baseUrl", "")

        # Only include DR deployments
        if not deployment.startswith("dr-"):
            continue

        config = r.get("config", {})
        expand = config.get("expand", "?")
        steps = config.get("steps", "?")
        data_size = config.get("dataSize", "?")
        config_key = f"e{expand}s{steps}d{data_size}"

        by_config[(deployment, config_key)]["baseUrl"] = base_url
        for run in r.get("slowestRuns", []):
            by_config[(deployment, config_key)]["runs"].append(run)

    if not by_config:
        return ""

    # Check if there are any actual slowest runs across all configs
    has_any_runs = any(data["runs"] for data in by_config.values())
    if not has_any_runs:
        return ""

    lines = ["*Slowest Runs - Capacity (DR)*"]

    # Sort configs for consistent output
    for deployment, config_key in sorted(by_config.keys()):
        data = by_config[(deployment, config_key)]
        runs = data["runs"]
        base_url = data["baseUrl"]

        # Sort by duration descending
        runs.sort(key=lambda x: x.get("durationSeconds", 0), reverse=True)

        if not runs:
            continue

        lines.append(f"\n`{deployment}` / `{config_key}` (baseUrl: `{base_url}`)")
        lines.append("```")
        lines.append(f"{'Duration':<10} {'ThreadId':<40} {'RunId':<40}")
        lines.append("-" * 90)

        for run in runs[:max_runs_per_config]:
            dur = run.get("durationSeconds")
            run_id = run.get("runId", "?")
            thread_id = run.get("threadId", "?")
            dur_str = f"{dur:.2f}s" if dur else "?"
            lines.append(f"{dur_str:<10} {thread_id:<40} {run_id:<40}")

        lines.append("```")

    return "\n".join(lines)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.stderr.write(
            "Usage: slack_slowest_runs.py <results_dir> [--capacity-only|--mixed-only] [--max-runs N]\n"
        )
        sys.exit(1)

    results_dir = sys.argv[1]
    capacity_only = "--capacity-only" in sys.argv
    mixed_only = "--mixed-only" in sys.argv

    # Parse --max-runs N
    max_runs = 5
    if "--max-runs" in sys.argv:
        try:
            idx = sys.argv.index("--max-runs")
            max_runs = int(sys.argv[idx + 1])
        except (IndexError, ValueError):
            pass

    mixed_results, capacity_results = load_json_files(results_dir)

    output_parts = []

    if capacity_only:
        msg = generate_capacity_slowest_runs(capacity_results, max_runs)
        if msg:
            output_parts.append(msg)
    elif mixed_only:
        msg = generate_mixed_slowest_runs(mixed_results, max_runs)
        if msg:
            output_parts.append(msg)
    else:
        mixed_msg = generate_mixed_slowest_runs(mixed_results, max_runs)
        capacity_msg = generate_capacity_slowest_runs(capacity_results, max_runs)
        if mixed_msg:
            output_parts.append(mixed_msg)
        if capacity_msg:
            output_parts.append(capacity_msg)

    if output_parts:
        sys.stdout.write("\n\n".join(output_parts))
    else:
        sys.stdout.write("")
