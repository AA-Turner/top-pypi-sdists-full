#!/usr/bin/env python3
"""Benchmark live RSS for retained Python-core StatsigUser objects."""

from __future__ import annotations

import argparse
import gc
import json
import os
import platform
import statistics
import subprocess
import sys
from datetime import datetime, timezone
from typing import Any

import psutil
from statsig_python_core import StatsigUser

from user_creation_benchmark import (
    OPENAI_ANDROID_LIKE_CUSTOM,
    OPENAI_ANDROID_LIKE_CUSTOM_IDS,
    OPENAI_ANDROID_LIKE_TOP_LEVEL_ARGS,
    STATSIG_ENVIRONMENT,
    validate_user,
)


def repeated_payload(_: int) -> dict[str, Any]:
    return {
        **OPENAI_ANDROID_LIKE_TOP_LEVEL_ARGS,
        "custom_ids": dict(OPENAI_ANDROID_LIKE_CUSTOM_IDS),
        "custom": dict(OPENAI_ANDROID_LIKE_CUSTOM),
        "statsig_environment": dict(STATSIG_ENVIRONMENT),
    }


def unique_identity_payload(index: int) -> dict[str, Any]:
    suffix = f"{index:08d}"
    top_level = {
        **OPENAI_ANDROID_LIKE_TOP_LEVEL_ARGS,
        "user_id": f"user-{suffix}",
        "email": f"anonuser{suffix}@example.com",
    }
    custom_ids = {
        **OPENAI_ANDROID_LIKE_CUSTOM_IDS,
        "account_id": f"11111111-2222-3333-4444-{suffix[-8:]}",
        "stableID": f"aaaaaaaa-bbbb-cccc-dddd-{suffix[-8:]}",
        "WebAnonymousCookieID": f"aaaaaaaa-bbbb-cccc-dddd-{suffix[-8:]}",
        "DeviceId": f"aaaaaaaa-bbbb-cccc-dddd-{suffix[-8:]}",
    }
    custom = {
        **OPENAI_ANDROID_LIKE_CUSTOM,
        "account_user_id": f"user-{suffix}",
        "organizations": [f"org-{suffix}"],
    }
    return {
        **top_level,
        "custom_ids": custom_ids,
        "custom": custom,
        "statsig_environment": dict(STATSIG_ENVIRONMENT),
    }


SCENARIOS = {
    "openai_android_like_repeated": repeated_payload,
    "openai_android_like_unique_identity": unique_identity_payload,
}


def summarize(samples: list[dict[str, Any]]) -> dict[str, float]:
    rss_deltas = [sample["rss_delta_bytes"] for sample in samples]
    bytes_per_user = [sample["bytes_per_user"] for sample in samples]
    sorted_bytes_per_user = sorted(bytes_per_user)
    return {
        "rss_delta_bytes_p50": statistics.median(rss_deltas),
        "bytes_per_user_min": min(bytes_per_user),
        "bytes_per_user_p50": statistics.median(bytes_per_user),
        "bytes_per_user_p95": sorted_bytes_per_user[
            max(0, int(len(sorted_bytes_per_user) * 0.95) - 1)
        ],
        "bytes_per_user_mean": statistics.fmean(bytes_per_user),
        "bytes_per_user_stdev": statistics.stdev(bytes_per_user)
        if len(bytes_per_user) > 1
        else 0.0,
        "bytes_per_user_max": max(bytes_per_user),
    }


def child_run(scenario: str, count: int) -> dict[str, Any]:
    payload_factory = SCENARIOS[scenario]
    first_payload = payload_factory(0)
    signature = validate_user(scenario, first_payload)

    gc.collect()
    process = psutil.Process()
    before_rss = process.memory_info().rss
    users = [StatsigUser(**payload_factory(index)) for index in range(count)]
    after_rss = process.memory_info().rss
    if len(users) != count:
        raise AssertionError("unexpected retained user count")

    rss_delta = after_rss - before_rss
    return {
        "scenario": scenario,
        "count": count,
        "signature": signature,
        "before_rss_bytes": before_rss,
        "after_rss_bytes": after_rss,
        "rss_delta_bytes": rss_delta,
        "bytes_per_user": rss_delta / count,
    }


def run_parent(scenario: str, count: int, samples: int) -> dict[str, Any]:
    raw_samples: list[dict[str, Any]] = []
    for _ in range(samples):
        proc = subprocess.run(
            [
                sys.executable,
                __file__,
                "--child",
                "--scenario",
                scenario,
                "--count",
                str(count),
            ],
            check=True,
            capture_output=True,
            text=True,
            env=os.environ.copy(),
        )
        raw_samples.append(json.loads(proc.stdout))

    signatures = {sample["signature"] for sample in raw_samples}
    if len(signatures) != 1:
        raise AssertionError(f"{scenario}: signature mismatch across samples")

    return {
        "scenario": scenario,
        "count": count,
        "samples": samples,
        "signature": raw_samples[0]["signature"],
        "raw_samples": raw_samples,
        **summarize(raw_samples),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scenario", action="append", choices=sorted(SCENARIOS))
    parser.add_argument("--count", type=int, default=20_000)
    parser.add_argument("--samples", type=int, default=7)
    parser.add_argument("--json-out")
    parser.add_argument("--child", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    scenarios = args.scenario or list(SCENARIOS)

    if args.child:
        if len(scenarios) != 1:
            raise SystemExit("child mode requires exactly one --scenario")
        print(json.dumps(child_run(scenarios[0], args.count), sort_keys=True))
        return

    results = [run_parent(scenario, args.count, args.samples) for scenario in scenarios]
    payload = {
        "metadata": {
            "command": " ".join(sys.argv),
            "cwd": os.getcwd(),
            "python": sys.version,
            "platform": platform.platform(),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "benchmark_version": 1,
        },
        "results": results,
    }

    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as out:
            json.dump(payload, out, indent=2, sort_keys=True)
            out.write("\n")

    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
