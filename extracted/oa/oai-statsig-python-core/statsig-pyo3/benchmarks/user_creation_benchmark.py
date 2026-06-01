#!/usr/bin/env python3
"""Benchmark Python-core StatsigUser construction for large user payloads."""

from __future__ import annotations

import argparse
import gc
import hashlib
import json
import os
import platform
import statistics
import sys
import time
from collections.abc import Callable
from datetime import datetime, timezone
from typing import Any

from statsig_python_core import StatsigUser


TOP_LEVEL_ARGS: dict[str, Any] = {
    "user_id": "user-synthetic-large-payload",
    "email": "synthetic.user@example.com",
    "ip": "2001:db8:5044:e800:a4fb:828c:12a9:d507",
    "user_agent": "ChatGPT/1.2026.097 (iOS 18.3.1; iPhone16,2; build 24313104440)",
    "country": "CA",
    "locale": "en-CA",
    "app_version": "1.2026.097",
}

# Sanitized fixture modeled after a representative Android request payload.
# Keep the production-like field mix and cardinality, but never copy live identifiers.
OPENAI_ANDROID_LIKE_TOP_LEVEL_ARGS: dict[str, Any] = {
    "user_id": "user-aaaaaaaaaaaaaaaaaaaaaaaa",
    "email": "anonuser123456@example.com",
    "ip": "47.222.57.240",
    "user_agent": "ChatGPT/1.2026.118 (Android 16; SM-S928U; build 2611813)",
    "country": "US",
    "locale": "en-US",
    "app_version": "1.2026.118",
}

CUSTOM_IDS: dict[str, Any] = {
    "ads_segment_id": "3252",
    "stableID": "589296E4-D534-4B5C-AE10-1F7ECF364F76",
    "WebAnonymousCookieID": "589296E4-D534-4B5C-AE10-1F7ECF364F76",
    "DeviceId": "589296E4-D534-4B5C-AE10-1F7ECF364F76",
}

OPENAI_ANDROID_LIKE_CUSTOM_IDS: dict[str, Any] = {
    "account_id": "11111111-2222-3333-4444-555555555555",
    "ads_segment_id": "1724",
    "stableID": "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee",
    "WebAnonymousCookieID": "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee",
    "DeviceId": "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee",
}

CUSTOM: dict[str, Any] = {
    "_openai_cluster": "unified-42",
    "_openai_track": "stable",
    "_openai_env": "prod",
    "is_paid": True,
    "account_user_id": "user-synthetic-large-payload",
    "plan_type": "pro",
    "client_type": "ios_app",
    "is_punch_out_user": False,
    "is_test_user": False,
    "user_agent": "ChatGPT/1.2026.097 (iOS 18.3.1; iPhone16,2; build 24313104440)",
    "region": "British Columbia",
    "region_code": "BC",
    "storefront_country_code": "CAN",
    "email_domain": "example.com",
    "days_since_user_creation": 1184,
    "days_since_user_creation_bucket": "29+",
    "user_created_at": 1674360986,
    "seconds_since_user_creation": -1,
    "organizations": ["org-synthetic-large-payload"],
    "email_domain_type": "social",
    "is_mfa_authenticated": False,
    "is_sso_authenticated": False,
    "is_hipaa_compliance_workspace": False,
    "is_delinquent": False,
    "build_number": 24313104440,
    "app_environment": "app_store",
    "os_version": "iOS 18.3.1",
    "auth_status": "logged_in",
    "host": "chat.gateway.unified-42.api.openai.com",
    "service": "sa-server-convo",
    "sa_server_deploy_id": "prod+service+sa-server~2821",
    "pod_name": "sa-server-convo-656946bcff-8trw6",
    "cluster": "unified-42",
    "pod_bucket_1000": 187,
}

OPENAI_ANDROID_LIKE_CUSTOM: dict[str, Any] = {
    "_openai_env": "prod",
    "_openai_cluster": "unified-149",
    "_openai_track": "stable",
    "is_paid": True,
    "account_user_id": "user-aaaaaaaaaaaaaaaaaaaaaaaa",
    "plan_type": "plus",
    "client_type": "android_app",
    "is_punch_out_user": False,
    "is_test_user": False,
    "user_agent": "ChatGPT/1.2026.118 (Android 16; SM-S928U; build 2611813)",
    "region": "Texas",
    "region_code": "TX",
    "state": "TX",
    "storefront_country_code": "US",
    "device_tier": "upper_mid",
    "email_domain": "mail.test",
    "days_since_user_creation": 628,
    "days_since_user_creation_bucket": "29+",
    "user_created_at": 1723935927,
    "seconds_since_user_creation": -1,
    "organizations": ["org-aaaaaaaaaaaaaaaaaaaaaaaa"],
    "email_domain_type": "social",
    "is_mfa_authenticated": False,
    "is_sso_authenticated": False,
    "is_hipaa_compliance_workspace": False,
    "is_delinquent": False,
    "build_number": 2611813,
    "os_version": "Android 16",
    "auth_status": "logged_in",
    "host": "chat.gateway.unified-149.api.openai.com",
    "service": "sa-server-convo",
    "sa_server_deploy_id": "prod+service+sa-server~2895",
    "pod_name": "sa-server-convo-64976dbbbb-g4b2z",
    "cluster": "unified-149",
    "pod_bucket_1000": 761,
}

STATSIG_ENVIRONMENT: dict[str, Any] = {"tier": "production"}

PRIVATE_ATTRIBUTES: dict[str, Any] = {
    "private_string": "synthetic-private-value",
    "private_number": 42000001,
    "private_bool": True,
    "private_list": ["one", "two", "three"],
    "private_object": {"nested": "value", "count": 2},
}


def repeated_custom(prefix: str, values: list[Any], count: int = 34) -> dict[str, Any]:
    return {f"{prefix}_{index}": values[index % len(values)] for index in range(count)}


def scenario_kwargs() -> dict[str, dict[str, Any]]:
    top = dict(TOP_LEVEL_ARGS)
    full = {
        **top,
        "custom_ids": CUSTOM_IDS,
        "custom": CUSTOM,
        "private_attributes": PRIVATE_ATTRIBUTES,
        "statsig_environment": STATSIG_ENVIRONMENT,
    }
    openai_android_like = {
        **OPENAI_ANDROID_LIKE_TOP_LEVEL_ARGS,
        "custom_ids": OPENAI_ANDROID_LIKE_CUSTOM_IDS,
        "custom": OPENAI_ANDROID_LIKE_CUSTOM,
        "statsig_environment": STATSIG_ENVIRONMENT,
    }

    return {
        "top_level": top,
        "with_custom_ids": {**top, "custom_ids": CUSTOM_IDS},
        "with_environment": {**top, "statsig_environment": STATSIG_ENVIRONMENT},
        "with_custom": {**top, "custom": CUSTOM},
        "with_private_attributes": {**top, "private_attributes": PRIVATE_ATTRIBUTES},
        "full": full,
        "full_get_custom": full,
        "full_get_private_attributes": full,
        "full_get_all_maps": full,
        "openai_android_like": openai_android_like,
        "openai_android_like_get_all_maps": openai_android_like,
        "custom_strings": {
            **top,
            "custom": repeated_custom("string", ["stable", "prod", "ios_app", "29+"]),
        },
        "custom_bools": {
            **top,
            "custom": repeated_custom("bool", [True, False]),
        },
        "custom_ints": {
            **top,
            "custom": repeated_custom("int", [1, 42, 1184, 24313104440]),
        },
        "custom_floats": {
            **top,
            "custom": repeated_custom("float", [0.1, 1.5, 42.25, 1184.0]),
        },
        "custom_lists": {
            **top,
            "custom": repeated_custom("list", [["one", "two", "three"], [1, 2, 3]]),
        },
        "custom_nested": {
            **top,
            "custom": repeated_custom(
                "nested",
                [
                    {"string": "value", "int": 42, "bool": True},
                    {"list": ["a", "b"], "float": 3.14},
                ],
            ),
        },
}


def make_action(scenario: str, kwargs: dict[str, Any]) -> Callable[[], Any]:
    if scenario == "full_get_custom":
        return lambda: StatsigUser(**kwargs).custom
    if scenario == "full_get_private_attributes":
        return lambda: StatsigUser(**kwargs).private_attributes
    if scenario in {"full_get_all_maps", "openai_android_like_get_all_maps"}:
        def action() -> tuple[Any, Any, Any, Any]:
            user = StatsigUser(**kwargs)
            return (
                user.custom,
                user.custom_ids,
                user.private_attributes,
                user.statsig_environment,
            )

        return action

    return lambda: StatsigUser(**kwargs)


def validate_user(scenario: str, kwargs: dict[str, Any]) -> str:
    user = StatsigUser(**kwargs)
    if user.user_id != kwargs["user_id"]:
        raise AssertionError(f"{scenario}: wrong user_id")
    if "custom" in kwargs and user.custom != kwargs["custom"]:
        raise AssertionError(f"{scenario}: custom mismatch")
    if "custom_ids" in kwargs and user.custom_ids != kwargs["custom_ids"]:
        raise AssertionError(f"{scenario}: custom_ids mismatch")
    if "private_attributes" in kwargs and user.private_attributes != kwargs["private_attributes"]:
        raise AssertionError(f"{scenario}: private_attributes mismatch")
    if "statsig_environment" in kwargs and user.statsig_environment != kwargs["statsig_environment"]:
        raise AssertionError(f"{scenario}: statsig_environment mismatch")

    signature = {
        "user_id": user.user_id,
        "custom_len": len(user.custom or {}),
        "custom_ids_len": len(user.custom_ids or {}),
        "private_attributes_len": len(user.private_attributes or {}),
        "environment_len": len(user.statsig_environment or {}),
    }
    return hashlib.sha256(json.dumps(signature, sort_keys=True).encode()).hexdigest()[:16]


def time_action(action: Callable[[], Any], iterations: int) -> float:
    started = time.perf_counter_ns()
    value = None
    for _ in range(iterations):
        value = action()
    elapsed = time.perf_counter_ns() - started
    if value is None:
        raise AssertionError("action returned None")
    return elapsed / iterations / 1_000


def summarize(samples: list[float]) -> dict[str, float]:
    sorted_samples = sorted(samples)
    return {
        "min_us": min(samples),
        "p50_us": statistics.median(samples),
        "p95_us": sorted_samples[max(0, int(len(sorted_samples) * 0.95) - 1)],
        "mean_us": statistics.fmean(samples),
        "stdev_us": statistics.stdev(samples) if len(samples) > 1 else 0.0,
        "max_us": max(samples),
    }


def run_scenario(
    scenario: str,
    kwargs: dict[str, Any],
    iterations: int,
    samples: int,
    warmups: int,
) -> dict[str, Any]:
    signature = validate_user(scenario, kwargs)
    action = make_action(scenario, kwargs)

    for _ in range(warmups):
        time_action(action, iterations)

    was_enabled = gc.isenabled()
    gc.disable()
    try:
        timings = [time_action(action, iterations) for _ in range(samples)]
    finally:
        if was_enabled:
            gc.enable()

    return {
        "scenario": scenario,
        "iterations": iterations,
        "samples": samples,
        "warmups": warmups,
        "signature": signature,
        "raw_us": timings,
        **summarize(timings),
    }


def add_incremental_costs(results: list[dict[str, Any]]) -> None:
    by_name = {result["scenario"]: result for result in results}
    top = by_name.get("top_level")
    full = by_name.get("full")
    if top is None:
        return

    top_p50 = top["p50_us"]
    full_delta = max((full or top)["p50_us"] - top_p50, 0.0)
    for result in results:
        delta = max(result["p50_us"] - top_p50, 0.0)
        result["incremental_over_top_level_p50_us"] = delta
        result["share_of_full_incremental_p50"] = delta / full_delta if full_delta > 0 else 0.0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--iterations", type=int, default=50_000)
    parser.add_argument("--samples", type=int, default=9)
    parser.add_argument("--warmups", type=int, default=2)
    parser.add_argument("--scenario", action="append", help="Scenario to run. Defaults to all.")
    parser.add_argument("--json-out", help="Write machine-readable results to this path.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    scenarios = scenario_kwargs()
    selected = args.scenario or list(scenarios)

    unknown = sorted(set(selected) - set(scenarios))
    if unknown:
        raise SystemExit(f"Unknown scenario(s): {', '.join(unknown)}")

    results = [
        run_scenario(
            scenario,
            scenarios[scenario],
            iterations=args.iterations,
            samples=args.samples,
            warmups=args.warmups,
        )
        for scenario in selected
    ]
    add_incremental_costs(results)

    payload = {
        "metadata": {
            "command": " ".join(sys.argv),
            "cwd": os.getcwd(),
            "python": sys.version,
            "platform": platform.platform(),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "benchmark_version": 2,
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
