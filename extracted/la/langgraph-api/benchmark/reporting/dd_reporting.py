#!/usr/bin/env python3
"""
Parse benchmark JSON results and send to Datadog.
Install: pip install datadog-api-client
"""

import argparse
import glob
import json
import os
import sys

from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v2.api.logs_api import LogsApi
from datadog_api_client.v2.model.http_log import HTTPLog
from datadog_api_client.v2.model.http_log_item import HTTPLogItem


def send_benchmark_results(
    benchmark_data, common_labels=None, dd_site="us5.datadoghq.com", api_key=None
):
    """
    Send benchmark JSON to Datadog.

    Args:
        benchmark_data: Dict containing 'settings' and 'metrics' from benchmark
        common_labels: Additional labels (e.g., base_url)
    """
    configuration = Configuration()
    configuration.server_variables["site"] = dd_site
    configuration.api_key["apiKeyAuth"] = api_key

    if common_labels:
        benchmark_data["labels"] = common_labels

    log_item = HTTPLogItem(
        ddsource="benchmark-6",
        ddtags="env:benchmarking",
        hostname=os.getenv("HOSTNAME", "localhost"),
        message=json.dumps(benchmark_data),
        service="benchmark-results",
    )

    with ApiClient(configuration) as api_client:
        api_instance = LogsApi(api_client)
        body = HTTPLog([log_item])

        api_instance.submit_log(body=body)


def process_benchmark_file(
    json_file, common_labels=None, dd_site="us5.datadoghq.com", api_key=None
):
    """
    Read benchmark JSON file and send to Datadog.

    Args:
        json_file: Path to benchmark results JSON file
        common_labels: Additional labels for all metrics
    """
    with open(json_file) as f:
        data = json.load(f)

    send_benchmark_results(data, common_labels, dd_site, api_key)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Send benchmark results to Datadog")
    parser.add_argument(
        "benchmark_file", type=str, help="Path to benchmark results file"
    )
    args = parser.parse_args()

    DD_API_KEY = os.getenv("DD_API_KEY")
    if not DD_API_KEY:
        sys.exit(1)

    DD_SITE = os.getenv("DD_SITE", "us5.datadoghq.com")

    for file in glob.glob(args.benchmark_file):
        labels = {"base_url": os.getenv("BASE_URL")}
        basename = os.path.basename(file)
        lowered = basename.lower()
        if "histogram" in lowered:
            labels["type"] = "histogram"
        else:
            labels["type"] = "individual_run"
        process_benchmark_file(file, labels, DD_SITE, DD_API_KEY)
