#!/usr/bin/env python3
"""
Generate and send capacity benchmark summary to Slack.
"""

import json
import os
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import cast
from urllib.error import URLError
from urllib.request import Request, urlopen
from zoneinfo import ZoneInfo


def load_capacity_results(results_dir: str) -> list[dict]:
    """Load all capacity summary JSON files.

    File format:
    {
        "clusterName": "dr-small",
        "workloads": {
            "parallel-small": {"maxSuccessfulTarget": 10, "avgExecutionLatencySeconds": 1.5},
            "parallel-tiny": {"maxSuccessfulTarget": 20, "avgExecutionLatencySeconds": 0.8}
        }
    }
    """
    results = []

    results_path = Path(results_dir)
    if not results_path.exists():
        return results

    for f in results_path.glob("**/*_capacity_summary.json"):
        try:
            with open(f) as fp:
                data = json.load(fp)

            cluster_name = data.get("clusterName")
            workloads = data.get("workloads", {})

            if not cluster_name or not workloads:
                continue

            for workload_name, workload_data in workloads.items():
                results.append(
                    {
                        "clusterName": cluster_name,
                        "workloadName": workload_name,
                        "maxSuccessfulTarget": workload_data.get("maxSuccessfulTarget"),
                        "avgExecutionLatencySeconds": workload_data.get(
                            "avgExecutionLatencySeconds"
                        ),
                    }
                )
        except (OSError, json.JSONDecodeError):
            continue

    return results


def format_latency(value: float | None) -> str:
    """Format latency in seconds."""
    if value is None:
        return "N/A"
    return f"{value:.3f}s"


def format_target(value: int | None) -> str:
    """Format target value."""
    if value is None:
        return "N/A"
    return str(value)


def generate_capacity_table(results: list[dict]) -> tuple[list[str], bool]:
    """Generate formatted table sections from capacity results, one per workload.

    Returns:
        tuple[list[str], bool]: (list of workload sections, has_missing_data)
    """
    if not results:
        return ["*No capacity results collected*"], False

    # Group by workload, then by cluster
    by_workload = defaultdict(dict)
    for r in results:
        workload = r["workloadName"]
        cluster = r["clusterName"]
        by_workload[workload][cluster] = r

    workload_sections = []
    has_missing_data = False

    sizes = ["1-node", "3-node", "5-node", "7-node", "10-node", "15-node", "20-node"]

    for workload in sorted(by_workload.keys()):
        clusters_data = by_workload[workload]
        lines = []
        lines.append(f"\n*Workload: `{workload}`*")
        lines.append("```")

        # Header
        header = (
            f"{'Size':<8} | "
            f"{'DR Max Runs':>12} | "
            f"{'PY Max Runs':>12} | "
            f"{'DR Latency':>12} | "
            f"{'PY Latency':>12}"
        )
        lines.append(header)
        lines.append("-" * 72)

        for size in sizes:
            dr_cluster = f"dr-{size}"
            py_cluster = f"py-{size}"

            dr_data = clusters_data.get(dr_cluster)
            py_data = clusters_data.get(py_cluster)

            # Check for missing data
            if not dr_data or not py_data:
                has_missing_data = True
                dr_runs = (
                    "❌"
                    if not dr_data
                    else str(dr_data.get("maxSuccessfulTarget", "N/A"))
                )
                py_runs = (
                    "❌"
                    if not py_data
                    else str(py_data.get("maxSuccessfulTarget", "N/A"))
                )
                dr_lat = (
                    "❌"
                    if not dr_data
                    else format_latency(dr_data.get("avgExecutionLatencySeconds"))
                )
                py_lat = (
                    "❌"
                    if not py_data
                    else format_latency(py_data.get("avgExecutionLatencySeconds"))
                )

                line = (
                    f"{size:<8} | "
                    f"{dr_runs:>12} | "
                    f"{py_runs:>12} | "
                    f"{dr_lat:>12} | "
                    f"{py_lat:>12}"
                )
                lines.append(line)
                continue

            # Both clusters have data - compare and add trophies
            dr_max = dr_data.get("maxSuccessfulTarget", 0)
            py_max = py_data.get("maxSuccessfulTarget", 0)
            dr_latency = dr_data.get("avgExecutionLatencySeconds", float("inf"))
            py_latency = py_data.get("avgExecutionLatencySeconds", float("inf"))

            # Format runs with trophy for winner
            if dr_max > py_max:
                dr_runs_str = f"🏆{dr_max}"
                py_runs_str = str(py_max)
            elif py_max > dr_max:
                dr_runs_str = str(dr_max)
                py_runs_str = f"🏆{py_max}"
            else:
                # Tie or both zero
                dr_runs_str = str(dr_max)
                py_runs_str = str(py_max)

            # Format latency with trophy for winner (lower is better)
            dr_lat_str = format_latency(dr_latency)
            py_lat_str = format_latency(py_latency)

            if dr_latency < py_latency:
                dr_lat_str = f"🏆{dr_lat_str}"
            elif py_latency < dr_latency:
                py_lat_str = f"🏆{py_lat_str}"

            line = (
                f"{size:<8} | "
                f"{dr_runs_str:>12} | "
                f"{py_runs_str:>12} | "
                f"{dr_lat_str:>12} | "
                f"{py_lat_str:>12}"
            )
            lines.append(line)

        lines.append("```")

        # Add this workload section to our list
        workload_sections.append("\n".join(lines))

    return workload_sections, has_missing_data


def send_to_slack(message: str, channel: str, token: str) -> bool:
    """Send message to Slack using the Web API."""
    # Local test mode - just print to stdout
    if channel == "LOCAL_TEST":
        print("=" * 80)  # noqa: T201
        print("📨 LOCAL TEST MODE - Message Preview:")  # noqa: T201
        print("=" * 80)  # noqa: T201
        print(message)  # noqa: T201
        print("=" * 80)  # noqa: T201
        return True

    try:
        payload = json.dumps(
            {
                "channel": channel,
                "text": message,
            }
        ).encode("utf-8")

        request = Request(
            "https://slack.com/api/chat.postMessage",
            data=payload,
            headers={
                "Content-Type": "application/json; charset=utf-8",
                "Authorization": f"Bearer {token}",
            },
        )

        with urlopen(request, timeout=10) as response:
            result = json.loads(response.read().decode("utf-8"))

        if not result.get("ok"):
            error = result.get("error", "Unknown error")
            print(f"❌ Slack API error: {error}", file=sys.stderr)  # noqa: T201
            return False

        print("✅ Message sent to Slack successfully")  # noqa: T201
        return True
    except (URLError, Exception) as e:
        print(f"❌ Failed to send to Slack: {e}", file=sys.stderr)  # noqa: T201
        return False


def generate_slack_messages(results: list[dict], run_url: str) -> list[str]:
    """Generate Slack messages, splitting into multiple if needed to stay under 4000 chars.

    Returns:
        list[str]: List of message strings, split at workload boundaries
    """
    # Generate capacity table sections (one per workload) and check if there's missing data
    workload_sections, has_missing_data = generate_capacity_table(results)

    # Determine status based on results
    if not results:
        status_emoji = "🔴"
        status = "No results collected"
    elif has_missing_data:
        status_emoji = "🟡"
        status = "Partially Completed"
    else:
        status_emoji = "🟢"
        status = "Completed"

    # Header for first message
    header = [
        f"📊 *Capacity Benchmark Summary* {status_emoji}",
        f"*Status*: {status}",
        "",
        "*📊 Capacity Benchmark Results*\n",
    ]

    # Footer with explanation
    footer = [
        "",
        "📖 *Metrics Explanation:*",
        "• *Max Runs*: Maximum number of concurrent runs the cluster can handle successfully",
        "• *Latency*: Average(mean) execution time across all maximum successful runs (lower is better)",
        "• 🏆: Winner in the comparison (higher Max Runs or lower Latency)",
    ]

    if has_missing_data:
        footer.extend(
            [
                "",
                "⚠️  *Note*: Some clusters marked with ❌ failed to complete even the iniital target concurrent runs(no data collected).",
            ]
        )

    footer.extend(
        [
            "",
            f"📁 *GitHub Actions Run*: <{run_url}|View Details>",
            "",
            f"🕐 *Run Completed Time*: {datetime.now(ZoneInfo('America/Los_Angeles')).strftime('%Y-%m-%d %H:%M %Z')}",
        ]
    )

    # Split messages at workload boundaries, keeping under 4000 chars per message
    MAX_CHARS = 3800  # Leave some buffer below 4000
    messages = []

    header_text = "\n".join(header)
    footer_text = "\n".join(footer)

    current_message_parts = [header_text]
    current_length = len(header_text)

    for section in workload_sections:
        section_length = len(section) + 1  # +1 for newline

        # Check if adding this section would exceed the limit
        # Account for footer that will be added at the end
        if (
            current_length + section_length + len(footer_text) + 2 > MAX_CHARS
            and len(current_message_parts) > 1
        ):
            # Finalize current message with footer
            current_message_parts.append(footer_text)
            messages.append("\n".join(current_message_parts))

            # Start new message with continuation header
            continuation_header = f"📊 *Capacity Benchmark Summary (continued {len(messages) + 1})* {status_emoji}\n"
            current_message_parts = [continuation_header, section]
            current_length = len(continuation_header) + section_length
        else:
            # Add section to current message
            current_message_parts.append(section)
            current_length += section_length

    # Finalize the last message
    if current_message_parts:
        current_message_parts.append(footer_text)
        messages.append("\n".join(current_message_parts))

    return messages


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(  # noqa: T201
            "Usage: capacity_slack_report.py <results_dir> <github_run_url>",
            file=sys.stderr,
        )
        sys.exit(1)

    results_dir = sys.argv[1]
    run_url = sys.argv[2]

    # Get Slack credentials
    slack_token = os.getenv("SLACK_BOT_TOKEN")
    slack_channel = os.getenv("SLACK_CHANNEL")
    slack_alert_channel = os.getenv("SLACK_ALERT_CHANNEL")

    if not slack_token or not slack_channel or not slack_alert_channel:
        print(  # noqa: T201
            "Error: SLACK_BOT_TOKEN, SLACK_CHANNEL, and SLACK_ALERT_CHANNEL must be set",
            file=sys.stderr,
        )
        sys.exit(1)

    # Load results
    results = load_capacity_results(results_dir)

    # Generate messages (may be split into multiple messages)
    messages = generate_slack_messages(results, run_url)

    # Determine which channel to use based on results
    target_channel = (
        cast("str", slack_channel) if results else cast("str", slack_alert_channel)
    )

    # Send all messages to Slack
    print(f"📤 Sending {len(messages)} message(s) to Slack...")  # noqa: T201
    all_succeeded = True
    for i, message in enumerate(messages, 1):
        print(f"📨 Sending message {i}/{len(messages)} ({len(message)} chars)...")  # noqa: T201
        if not send_to_slack(message, target_channel, cast("str", slack_token)):
            all_succeeded = False
            print(f"❌ Failed to send message {i}/{len(messages)}", file=sys.stderr)  # noqa: T201

    if not all_succeeded:
        sys.exit(1)

    print(f"✅ All {len(messages)} message(s) sent successfully")  # noqa: T201
