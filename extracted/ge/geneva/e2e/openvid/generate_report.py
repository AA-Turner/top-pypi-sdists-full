#!/usr/bin/env python3
# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""
Generate a trend report from OpenVid daily load test artifacts.

Reads metrics.json files from downloaded artifacts and produces a Markdown
report with cross-CSP trends, regression detection, and failure history.

Usage:
    python generate_report.py \
        --artifacts-dir /tmp/artifacts \
        --output-dir /tmp/report
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from datetime import datetime, timezone
from io import StringIO
from pathlib import Path


def load_metrics(artifacts_dir: str) -> list[dict]:
    """Load all metrics.json files from the artifacts directory."""
    metrics = []
    artifacts_path = Path(artifacts_dir)

    if not artifacts_path.exists():
        print(f"WARNING: Artifacts directory not found: {artifacts_dir}",
              file=sys.stderr)
        return metrics

    for metrics_file in sorted(artifacts_path.rglob("metrics.json")):
        try:
            data = json.loads(metrics_file.read_text())
            # Add source path for debugging
            data["_source"] = str(metrics_file)
            metrics.append(data)
        except (json.JSONDecodeError, OSError) as e:
            print(f"WARNING: Failed to load {metrics_file}: {e}",
                  file=sys.stderr)

    return metrics


def group_by_csp(metrics: list[dict]) -> dict[str, list[dict]]:
    """Group metrics by CSP."""
    groups: dict[str, list[dict]] = {}
    for m in metrics:
        csp = m.get("csp", "unknown")
        groups.setdefault(csp, []).append(m)
    # Sort each group by date
    for csp in groups:
        groups[csp].sort(key=lambda x: x.get("date", ""))
    return groups


def format_duration(seconds: float) -> str:
    """Format seconds into human-readable duration."""
    if seconds < 60:
        return f"{seconds:.1f}s"
    minutes = seconds / 60
    if minutes < 60:
        return f"{minutes:.1f}m"
    hours = minutes / 60
    return f"{hours:.1f}h"


def compute_rolling_avg(values: list[float], window: int = 7) -> float:
    """Compute rolling average over the last N values."""
    if not values:
        return 0.0
    recent = values[-window:]
    return sum(recent) / len(recent)


def detect_regressions(
    by_csp: dict[str, list[dict]],
    threshold: float = 0.20,
) -> list[dict]:
    """Detect tests whose duration regressed >threshold vs 7-day rolling avg."""
    regressions = []

    for csp, runs in by_csp.items():
        if len(runs) < 2:
            continue

        # Build per-test duration history
        test_history: dict[str, list[float]] = {}
        for run in runs:
            for test in run.get("metrics", {}).get("test_results", []):
                name = test["name"]
                if test["status"] == "passed":
                    test_history.setdefault(name, []).append(test["duration_s"])

        # Check latest vs rolling average
        for test_name, durations in test_history.items():
            if len(durations) < 3:
                continue
            rolling_avg = compute_rolling_avg(durations[:-1])
            latest = durations[-1]
            if rolling_avg > 0 and (latest - rolling_avg) / rolling_avg > threshold:
                regressions.append({
                    "csp": csp,
                    "test": test_name,
                    "latest_s": latest,
                    "rolling_avg_s": rolling_avg,
                    "increase_pct": ((latest - rolling_avg) / rolling_avg) * 100,
                })

    return regressions


def get_failure_history(by_csp: dict[str, list[dict]]) -> list[dict]:
    """Get all test failures from the data."""
    failures = []
    for csp, runs in by_csp.items():
        for run in runs:
            date = run.get("date", "unknown")
            run_id = run.get("run_id", "unknown")
            for test in run.get("metrics", {}).get("test_results", []):
                if test["status"] in ("failed", "errored"):
                    failures.append({
                        "csp": csp,
                        "date": date[:10],
                        "test": test["name"],
                        "status": test["status"],
                        "run_id": run_id,
                    })
    return failures


def generate_markdown_report(
    metrics: list[dict],
    by_csp: dict[str, list[dict]],
) -> str:
    """Generate the Markdown trend report."""
    lines = []
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines.append("# OpenVid Daily Load Test Report")
    lines.append(f"Generated: {now}")
    lines.append(f"Total runs analyzed: {len(metrics)}")
    lines.append("")

    # --- Latest Run Summary ---
    lines.append("## Latest Run Summary")
    lines.append("")
    lines.append("| CSP | Date | Status | Duration | Passed | Failed | Errored | Skipped |")
    lines.append("|-----|------|--------|----------|--------|--------|---------|---------|")

    for csp in sorted(by_csp.keys()):
        runs = by_csp[csp]
        if not runs:
            continue
        latest = runs[-1]
        m = latest.get("metrics", {})
        date = latest.get("date", "unknown")[:10]
        duration = format_duration(m.get("suite_duration_s", 0))
        passed = m.get("tests_passed", 0)
        failed = m.get("tests_failed", 0)
        errored = m.get("tests_errored", 0)
        skipped = m.get("tests_skipped", 0)
        status = "PASS" if (failed == 0 and errored == 0) else "FAIL"
        lines.append(
            f"| {csp} | {date} | {status} | {duration} "
            f"| {passed} | {failed} | {errored} | {skipped} |"
        )

    lines.append("")

    # --- Per-Test Duration Trend ---
    lines.append("## Per-Test Duration Trend (last 10 runs)")
    lines.append("")

    for csp in sorted(by_csp.keys()):
        runs = by_csp[csp]
        recent = runs[-10:]
        if not recent:
            continue

        lines.append(f"### {csp.upper()}")
        lines.append("")

        # Collect all test names
        all_tests: set[str] = set()
        for run in recent:
            for t in run.get("metrics", {}).get("test_results", []):
                all_tests.add(t["name"])

        if not all_tests:
            lines.append("No test data available.")
            lines.append("")
            continue

        # Header row
        dates = [r.get("date", "")[:10] for r in recent]
        lines.append("| Test | " + " | ".join(dates) + " |")
        lines.append("|---" + "|---" * len(dates) + "|")

        for test_name in sorted(all_tests):
            row = [test_name]
            for run in recent:
                test_data = next(
                    (
                        t for t in run.get("metrics", {}).get("test_results", [])
                        if t["name"] == test_name
                    ),
                    None,
                )
                if test_data is None:
                    row.append("-")
                elif test_data["status"] == "passed":
                    row.append(format_duration(test_data["duration_s"]))
                elif test_data["status"] == "skipped":
                    row.append("skip")
                else:
                    row.append("FAIL")
            lines.append("| " + " | ".join(row) + " |")

        lines.append("")

    # --- Regression Detection ---
    regressions = detect_regressions(by_csp)
    lines.append("## Regression Detection")
    lines.append("")
    if regressions:
        lines.append(
            "Tests with >20% duration increase vs 7-day rolling average:"
        )
        lines.append("")
        lines.append(
            "| CSP | Test | Latest | Rolling Avg | Increase |"
        )
        lines.append("|-----|------|--------|-------------|----------|")
        for r in regressions:
            lines.append(
                f"| {r['csp']} | {r['test']} "
                f"| {format_duration(r['latest_s'])} "
                f"| {format_duration(r['rolling_avg_s'])} "
                f"| +{r['increase_pct']:.0f}% |"
            )
    else:
        lines.append("No regressions detected.")
    lines.append("")

    # --- Failure History ---
    failures = get_failure_history(by_csp)
    lines.append("## Failure History")
    lines.append("")
    if failures:
        lines.append("| Date | CSP | Test | Status | Run ID |")
        lines.append("|------|-----|------|--------|--------|")
        for f in failures[-50:]:  # Last 50 failures
            lines.append(
                f"| {f['date']} | {f['csp']} | {f['test']} "
                f"| {f['status']} | {f['run_id']} |"
            )
        if len(failures) > 50:
            lines.append(
                f"\n*Showing last 50 of {len(failures)} total failures.*"
            )
    else:
        lines.append("No failures in the analyzed period.")
    lines.append("")

    # --- V-JEPA2 Metrics ---
    lines.append("## V-JEPA2 Embedding Metrics")
    lines.append("")
    has_vjepa_data = False
    for csp in sorted(by_csp.keys()):
        runs = by_csp[csp]
        vjepa_data = []
        for run in runs:
            log_m = run.get("metrics", {}).get("log_metrics", {})
            if "vjepa2_embeddings_generated" in log_m:
                vjepa_data.append({
                    "date": run.get("date", "")[:10],
                    "embeddings": log_m["vjepa2_embeddings_generated"],
                    "total": log_m.get("vjepa2_embeddings_total", "?"),
                    "tokens": log_m.get("vjepa2_tokens_per_video", "?"),
                })
        if vjepa_data:
            has_vjepa_data = True
            lines.append(f"### {csp.upper()}")
            lines.append("")
            lines.append("| Date | Embeddings | Total | Tokens/Video |")
            lines.append("|------|------------|-------|--------------|")
            for d in vjepa_data[-10:]:
                lines.append(
                    f"| {d['date']} | {d['embeddings']} "
                    f"| {d['total']} | {d['tokens']} |"
                )
            lines.append("")

    if not has_vjepa_data:
        lines.append("No V-JEPA2 metrics available.")
        lines.append("")

    # --- MV Metrics ---
    lines.append("## Materialized View Metrics")
    lines.append("")
    has_mv_data = False
    for csp in sorted(by_csp.keys()):
        runs = by_csp[csp]
        mv_data = []
        for run in runs:
            log_m = run.get("metrics", {}).get("log_metrics", {})
            if any(
                k in log_m
                for k in (
                    "mv_creation_rows",
                    "mv_refresh_rows",
                    "mv_incremental_refresh_rows",
                )
            ):
                mv_data.append({
                    "date": run.get("date", "")[:10],
                    "creation": log_m.get("mv_creation_rows", []),
                    "refresh": log_m.get("mv_refresh_rows", []),
                    "incremental": log_m.get(
                        "mv_incremental_refresh_rows", []
                    ),
                })
        if mv_data:
            has_mv_data = True
            lines.append(f"### {csp.upper()}")
            lines.append("")
            lines.append(
                "| Date | Creation Rows | Refresh Rows | Incremental Rows |"
            )
            lines.append(
                "|------|---------------|--------------|------------------|"
            )
            for d in mv_data[-10:]:
                creation = ", ".join(str(x) for x in d["creation"]) or "-"
                refresh = ", ".join(str(x) for x in d["refresh"]) or "-"
                incremental = (
                    ", ".join(str(x) for x in d["incremental"]) or "-"
                )
                lines.append(
                    f"| {d['date']} | {creation} "
                    f"| {refresh} | {incremental} |"
                )
            lines.append("")

    if not has_mv_data:
        lines.append("No materialized view metrics available.")
        lines.append("")

    return "\n".join(lines)


def generate_csv(metrics: list[dict]) -> str:
    """Generate CSV trend data for external analysis."""
    output = StringIO()
    writer = csv.writer(output)

    # Header
    writer.writerow([
        "date", "csp", "num_videos", "commit_sha", "run_id",
        "suite_duration_s", "tests_passed", "tests_failed",
        "tests_skipped", "tests_errored",
        "vjepa2_embeddings_generated", "vjepa2_tokens_per_video",
    ])

    for m in sorted(metrics, key=lambda x: (x.get("csp", ""), x.get("date", ""))):
        met = m.get("metrics", {})
        log_m = met.get("log_metrics", {})
        writer.writerow([
            m.get("date", "")[:10],
            m.get("csp", ""),
            m.get("num_videos", ""),
            m.get("commit_sha", "")[:8],
            m.get("run_id", ""),
            f"{met.get('suite_duration_s', 0):.1f}",
            met.get("tests_passed", 0),
            met.get("tests_failed", 0),
            met.get("tests_skipped", 0),
            met.get("tests_errored", 0),
            log_m.get("vjepa2_embeddings_generated", ""),
            log_m.get("vjepa2_tokens_per_video", ""),
        ])

    return output.getvalue()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate OpenVid daily load test trend report"
    )
    parser.add_argument(
        "--artifacts-dir",
        required=True,
        help="Directory containing downloaded artifact folders with metrics.json",
    )
    parser.add_argument(
        "--output-dir",
        default="/tmp/report",
        help="Output directory for report files",
    )

    args = parser.parse_args()

    # Load all metrics
    metrics = load_metrics(args.artifacts_dir)
    if not metrics:
        print("No metrics found. Nothing to report.", file=sys.stderr)
        sys.exit(0)

    print(f"Loaded {len(metrics)} metric files")

    # Group by CSP
    by_csp = group_by_csp(metrics)
    for csp, runs in by_csp.items():
        print(f"  {csp}: {len(runs)} runs")

    # Generate outputs
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Markdown report
    report = generate_markdown_report(metrics, by_csp)
    report_path = output_dir / "report.md"
    report_path.write_text(report)
    print(f"Report written to {report_path}")

    # CSV data
    csv_data = generate_csv(metrics)
    csv_path = output_dir / "trend_data.csv"
    csv_path.write_text(csv_data)
    print(f"CSV data written to {csv_path}")

    # Print report to stdout for workflow logs
    print("\n" + "=" * 80)
    print(report)


if __name__ == "__main__":
    main()
