#!/usr/bin/env python3
"""
Send capacity benchmark results to Datadog.
"""

import json
import os
import sys

from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v2.api.logs_api import LogsApi
from datadog_api_client.v2.model.http_log import HTTPLog
from datadog_api_client.v2.model.http_log_item import HTTPLogItem


def send_capacity_results(summary_file: str):
    """
    Read capacity_summary.json and send to Datadog.

    The summary file format is:
    {
        "clusterName": "dr-small",
        "workloads": {
            "parallel-small": {"maxSuccessfulTarget": 10, "avgExecutionLatencySeconds": 1.5},
            "parallel-tiny": {"maxSuccessfulTarget": 20, "avgExecutionLatencySeconds": 0.8}
        }
    }

    Args:
        summary_file: Path to capacity_summary.json
    """
    # Get environment variables
    dd_api_key = os.getenv("DD_API_KEY")
    if not dd_api_key:
        print("Error: DD_API_KEY not set", file=sys.stderr)  # noqa: T201
        sys.exit(1)

    dd_site = os.getenv("DD_SITE", "us5.datadoghq.com")

    # Read summary file
    try:
        with open(summary_file) as f:
            data = json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        print(f"Error reading {summary_file}: {e}", file=sys.stderr)  # noqa: T201
        sys.exit(1)

    cluster_name = data.get("clusterName", "unknown")
    workloads = data.get("workloads", {})

    if not workloads:
        print("Error: No workloads found in summary file", file=sys.stderr)  # noqa: T201
        sys.exit(1)

    # Configure Datadog client
    configuration = Configuration()
    configuration.server_variables["site"] = dd_site
    configuration.api_key["apiKeyAuth"] = dd_api_key

    # Create log items for each workload
    log_items = []
    for workload_name, result in workloads.items():
        benchmark_data = {
            "clusterName": cluster_name,
            "workloadName": workload_name,
            "maxSuccessfulTarget": result.get("maxSuccessfulTarget"),
            "avgExecutionLatencySeconds": result.get("avgExecutionLatencySeconds"),
            "benchmarkType": "capacity",
        }

        log_item = HTTPLogItem(
            ddsource="capacity-benchmark",
            ddtags=f"env:benchmarking,cluster:{cluster_name},workload:{workload_name}",
            hostname=os.getenv("HOSTNAME", "github-actions"),
            message=json.dumps(benchmark_data),
            service="capacity-benchmark",
        )
        log_items.append(log_item)

    # Send all logs to Datadog
    with ApiClient(configuration) as api_client:
        api_instance = LogsApi(api_client)
        body = HTTPLog(log_items)
        api_instance.submit_log(body=body)

    print("Sent capacity results to Datadog")  # noqa: T201


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: capacity_dd_report.py <capacity_summary.json>", file=sys.stderr)  # noqa: T201
        sys.exit(1)

    send_capacity_results(sys.argv[1])
