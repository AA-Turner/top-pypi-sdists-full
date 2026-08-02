#!/usr/bin/env python3
# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""
Collect metrics from OpenVid E2E test results.

Parses JUnit XML and test output logs to produce a structured metrics JSON
file for trend analysis across daily load test runs.

Usage:
    python collect_metrics.py \
        --junit-xml /tmp/junit-results.xml \
        --test-log /tmp/test-output.log \
        --csp gcp \
        --num-videos 100 \
        --output-dir /tmp/test-results
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path


def parse_junit_xml(path: str) -> dict:
    """Extract test results from JUnit XML."""
    results: dict = {
        "suite_duration_s": 0.0,
        "tests_passed": 0,
        "tests_failed": 0,
        "tests_skipped": 0,
        "tests_errored": 0,
        "test_results": [],
    }

    if not Path(path).exists():
        print(f"WARNING: JUnit XML not found at {path}", file=sys.stderr)
        return results

    tree = ET.parse(path)
    root = tree.getroot()

    # Handle both <testsuites> wrapper and direct <testsuite>
    suites = root.findall(".//testsuite")
    if not suites and root.tag == "testsuite":
        suites = [root]

    for suite in suites:
        suite_time = float(suite.get("time", "0"))
        results["suite_duration_s"] += suite_time

        for testcase in suite.findall("testcase"):
            name = testcase.get("name", "unknown")
            duration = float(testcase.get("time", "0"))

            # Determine status
            if testcase.find("skipped") is not None:
                status = "skipped"
                results["tests_skipped"] += 1
            elif testcase.find("failure") is not None:
                status = "failed"
                results["tests_failed"] += 1
            elif testcase.find("error") is not None:
                status = "errored"
                results["tests_errored"] += 1
            else:
                status = "passed"
                results["tests_passed"] += 1

            results["test_results"].append({
                "name": name,
                "classname": testcase.get("classname", ""),
                "duration_s": duration,
                "status": status,
            })

    return results


def parse_test_log(path: str) -> dict:
    """Extract custom metrics from test output log via regex."""
    metrics: dict = {}

    if not Path(path).exists():
        print(f"WARNING: Test log not found at {path}", file=sys.stderr)
        return metrics

    content = Path(path).read_text(errors="replace")

    # V-JEPA2 metrics
    m = re.search(r"Embeddings generated:\s*(\d+)/(\d+)", content)
    if m:
        metrics["vjepa2_embeddings_generated"] = int(m.group(1))
        metrics["vjepa2_embeddings_total"] = int(m.group(2))

    m = re.search(r"Tokens per video:\s*~?(\d+)", content)
    if m:
        metrics["vjepa2_tokens_per_video"] = int(m.group(1))

    m = re.search(r"Embedding tensor shape:\s*\[(\d+),\s*(\d+)\]", content)
    if m:
        metrics["vjepa2_embedding_tokens"] = int(m.group(1))
        metrics["vjepa2_embedding_dim"] = int(m.group(2))

    # Backfill metrics
    backfill_results = re.findall(r"Backfill completed:\s*(.*)", content)
    if backfill_results:
        metrics["backfill_results"] = backfill_results

    # MV creation metrics
    mv_created = re.findall(
        r"MV created successfully with (\d+) placeholder rows", content
    )
    if mv_created:
        metrics["mv_creation_rows"] = [int(x) for x in mv_created]

    # MV refresh metrics
    mv_refresh = re.findall(r"MV after refresh:\s*(\d+)\s*rows", content)
    if mv_refresh:
        metrics["mv_refresh_rows"] = [int(x) for x in mv_refresh]

    mv_incr = re.findall(
        r"MV after incremental refresh:\s*(\d+)\s*rows", content
    )
    if mv_incr:
        metrics["mv_incremental_refresh_rows"] = [int(x) for x in mv_incr]

    # MV version refresh
    mv_version = re.findall(
        r"MV after version refresh:\s*(\d+)\s*rows", content
    )
    if mv_version:
        metrics["mv_version_refresh_rows"] = [int(x) for x in mv_version]

    # Multiple refresh final count
    mv_final = re.findall(r"Final MV count:\s*(\d+)", content)
    if mv_final:
        metrics["mv_multi_refresh_final_rows"] = [int(x) for x in mv_final]

    # Cluster creation
    cluster_defined = re.findall(r"Cluster '([^']+)' defined", content)
    if cluster_defined:
        metrics["clusters_defined"] = cluster_defined

    # Test table info
    m = re.search(
        r"Test table created:.*rows=(\d+),\s*schema=\[([^\]]+)\]", content
    )
    if m:
        metrics["test_table_rows"] = int(m.group(1))

    return metrics


def build_metrics(
    *,
    junit_xml: str,
    test_log: str,
    csp: str,
    num_videos: int,
) -> dict:
    """Build the complete metrics document."""
    junit_data = parse_junit_xml(junit_xml)
    log_data = parse_test_log(test_log)

    return {
        "date": datetime.now(timezone.utc).isoformat(),
        "csp": csp,
        "num_videos": num_videos,
        "commit_sha": os.environ.get("GITHUB_SHA", "unknown"),
        "run_id": os.environ.get("GITHUB_RUN_ID", "unknown"),
        "run_number": os.environ.get("GITHUB_RUN_NUMBER", "unknown"),
        "ref": os.environ.get("GITHUB_REF", "unknown"),
        "metrics": {
            **junit_data,
            "log_metrics": log_data,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Collect metrics from OpenVid E2E test results"
    )
    parser.add_argument(
        "--junit-xml",
        default="/tmp/junit-results.xml",
        help="Path to JUnit XML results file",
    )
    parser.add_argument(
        "--test-log",
        default="/tmp/test-output.log",
        help="Path to test output log file",
    )
    parser.add_argument(
        "--csp",
        required=True,
        choices=["gcp", "aws", "azure"],
        help="Cloud service provider",
    )
    parser.add_argument(
        "--num-videos",
        type=int,
        default=1,
        help="Number of videos processed",
    )
    parser.add_argument(
        "--output-dir",
        default="/tmp/test-results",
        help="Output directory for metrics files",
    )

    args = parser.parse_args()

    # Build metrics
    metrics = build_metrics(
        junit_xml=args.junit_xml,
        test_log=args.test_log,
        csp=args.csp,
        num_videos=args.num_videos,
    )

    # Write output
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    metrics_path = output_dir / "metrics.json"
    with open(metrics_path, "w") as f:
        json.dump(metrics, f, indent=2)
    print(f"Metrics written to {metrics_path}")

    # Copy source files into output for archival
    for src, dst_name in [
        (args.junit_xml, "junit-results.xml"),
        (args.test_log, "test-output.log"),
    ]:
        src_path = Path(src)
        if src_path.exists():
            dst_path = output_dir / dst_name
            if src_path.resolve() != dst_path.resolve():
                dst_path.write_bytes(src_path.read_bytes())
                print(f"Copied {src} to {dst_path}")

    # Print summary
    m = metrics["metrics"]
    print(f"\n=== Metrics Summary ({args.csp}) ===")
    print(f"Suite duration: {m['suite_duration_s']:.1f}s")
    print(
        f"Tests: {m['tests_passed']} passed, "
        f"{m['tests_failed']} failed, "
        f"{m['tests_skipped']} skipped, "
        f"{m['tests_errored']} errored"
    )
    print(f"Test results: {len(m['test_results'])} tests")
    for t in m["test_results"]:
        print(f"  {t['status']:>8s}  {t['duration_s']:>8.1f}s  {t['name']}")

    log_m = m.get("log_metrics", {})
    if "vjepa2_embeddings_generated" in log_m:
        print(
            f"V-JEPA2 embeddings: {log_m['vjepa2_embeddings_generated']}"
            f"/{log_m.get('vjepa2_embeddings_total', '?')}"
        )
    if "mv_refresh_rows" in log_m:
        print(f"MV refresh rows: {log_m['mv_refresh_rows']}")


if __name__ == "__main__":
    main()
