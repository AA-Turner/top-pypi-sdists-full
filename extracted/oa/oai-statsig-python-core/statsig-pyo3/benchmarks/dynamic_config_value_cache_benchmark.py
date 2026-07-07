#!/usr/bin/env python3
"""Compare value-cached dynamic-config reads with uncached PyO3 conversion."""

from __future__ import annotations

import argparse
import gc
import json
import statistics
import time
from collections.abc import Callable
from typing import Any

from statsig_python_core import (
    DynamicConfigEvaluationOptions,
    EvaluationCache,
    Statsig,
    StatsigOptions,
    StatsigUser,
)


def make_value(key_count: int, array_size: int, text_size: int) -> dict[str, Any]:
    return {
        f"key_{index}": {
            "items": list(range(array_size)),
            "text": "x" * text_size,
        }
        for index in range(key_count)
    }


def measure(action: Callable[[], Any], iterations: int) -> float:
    gc.collect()
    start = time.perf_counter_ns()
    for _ in range(iterations):
        action()
    elapsed = time.perf_counter_ns() - start
    return elapsed / iterations


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--iterations", type=int, default=2_000)
    parser.add_argument("--samples", type=int, default=7)
    parser.add_argument("--keys", type=int, default=250)
    parser.add_argument("--array-size", type=int, default=20)
    parser.add_argument("--text-size", type=int, default=100)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    statsig = Statsig(
        "dynamic-config-evaluation-cache-benchmark",
        StatsigOptions(evaluation_cache=EvaluationCache()),
    )
    user = StatsigUser("benchmark-user")
    options = DynamicConfigEvaluationOptions(disable_exposure_logging=True)
    statsig.override_dynamic_config(
        "benchmark_config",
        make_value(args.keys, args.array_size, args.text_size),
        "benchmark-user",
    )

    first = statsig.get_dynamic_config(user, "benchmark_config", options)
    second = statsig.get_dynamic_config(user, "benchmark_config", options)
    if first.value is not second.value:
        raise AssertionError("dynamic-config value cache did not warm")
    if first.details is second.details:
        raise AssertionError("public evaluation details were unexpectedly reused")

    cached_samples = [
        measure(
            lambda: statsig.get_dynamic_config(user, "benchmark_config", options),
            args.iterations,
        )
        for _ in range(args.samples)
    ]
    uncached_samples = [
        measure(
            lambda: statsig._INTERNAL_get_dynamic_config(
                user, "benchmark_config", options
            ),
            args.iterations,
        )
        for _ in range(args.samples)
    ]

    cached_p50 = statistics.median(cached_samples)
    uncached_p50 = statistics.median(uncached_samples)
    print(
        json.dumps(
            {
                "iterations_per_sample": args.iterations,
                "samples": args.samples,
                "value_shape": {
                    "keys": args.keys,
                    "array_size": args.array_size,
                    "text_size": args.text_size,
                },
                "cached_ns_per_call_p50": cached_p50,
                "uncached_ns_per_call_p50": uncached_p50,
                "speedup_p50": uncached_p50 / cached_p50,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
