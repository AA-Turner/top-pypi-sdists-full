#!/usr/bin/env python3
"""Deterministic performance comparison with the reference json_repair package."""

from __future__ import annotations

import argparse
import gc
import json
import random
import statistics
import string
import time
from collections.abc import Callable

import fast_json_repair
import json_repair

RepairFunction = Callable[..., str]
Sample = tuple[str, str]


def generate_samples(seed: int = 0) -> list[Sample]:
    """Generate reproducible malformed and valid JSON workloads."""
    rng = random.Random(seed)
    samples: list[Sample] = [
        ("Simple quotes", "{'name': 'John', 'age': 30, 'city': 'New York'}"),
        (
            "Medium nested",
            """
            {
                'users': [
                    {'id': 1, 'name': 'Alice', active: True, 'tags': ['admin', 'user']},
                    {'id': 2, 'name': 'Bob', active: False, 'tags': ['user']},
                    {'id': 3, 'name': 'Charlie', active: None, 'tags': ['moderator']}
                ],
                metadata: {'total': 3, last_updated: '2024-01-01'}
            }
            """,
        ),
        ("Large array (1000)", f"[{','.join(map(str, range(1000)))},]"),
        (
            "Deep nesting (50)",
            "".join(f"{{level_{index}:" for index in range(50)) + "'deep'",
        ),
    ]

    large_object_values = ("True", "False", "None")
    large_object = ",".join(
        f"key_{index}:{rng.choice((repr(f'value_{index}'), str(index), *large_object_values))}"
        for index in range(500)
    )
    samples.append(("Large object (500)", f"{{{large_object},}}"))

    complex_mixed = """
    {
        users: [
            {id: 1, name: 'Alice', active: True, score: 95.5,},
            {id: 2, name: 'Bob', active: False, score: 87.3,},
            {id: 3, name: 'Charlie', active: True, score: 92.1,}
        ],
        settings: {
            theme: 'dark',
            notifications: {email: True, push: False, sms: None},
            preferences: ['option1', 'option2', 'option3',]
        }
    }
    """
    samples.append(("Complex mixed", complex_mixed))

    very_large_items = []
    for index in range(1000):
        name = "".join(rng.choices(string.ascii_letters, k=10))
        active = rng.choice(("True", "False", "None"))
        very_large_items.append(
            f"{{id:{index},name:'{name}',value:{rng.random()},active:{active}}}"
        )
    samples.append(("Large object array (1000)", f"[{','.join(very_large_items)},]"))

    samples.extend(
        [
            (
                "Unicode and comments",
                "{/* generated */ message:'你好世界',emoji:'😀🎉🚀',numbers:[1,2,3,]}",
            ),
            (
                "Long string (10K)",
                f"{{data:'{''.join(rng.choices(string.ascii_letters, k=10_000))}',count:10000}}",
            ),
            (
                "Missing commas",
                '{"a":1 "b":2 "c":3 "nested":{"value":42 "ok":true} "items":[1 2 3]}',
            ),
        ]
    )

    valid_values = [
        ("VALID: Small ASCII", {"name": "John", "age": 30, "active": True}),
        (
            "VALID: Unicode",
            {"name": "张三", "message": "你好世界", "emoji": "😀🎉", "japanese": "こんにちは"},
        ),
        (
            "VALID: Nested",
            {
                "users": [
                    {"id": 1, "name": "Alice", "active": True},
                    {"id": 2, "name": "Bob", "active": False},
                ],
                "metadata": {"total": 2, "page": 1},
            },
        ),
        (
            "VALID: Large array (1000)",
            [
                {"id": index, "value": f"item_{index}", "active": index % 2 == 0}
                for index in range(1000)
            ],
        ),
        (
            "VALID: Large object (500)",
            {
                f"key_{index}": {
                    "value": f"value_{index}",
                    "index": index,
                    "active": index % 2 == 0,
                }
                for index in range(500)
            },
        ),
        ("VALID: Very large array (5000)", list(range(5000))),
        (
            "VALID: Long string (10K)",
            {"description": "x" * 10_000, "metadata": {"length": 10_000}},
        ),
        (
            "VALID: Mixed types",
            {
                "string": "test",
                "number": 42.5,
                "boolean": True,
                "null": None,
                "array": [1, 2, 3],
                "object": {"nested": True},
            },
        ),
    ]
    samples.extend((name, json.dumps(value, ensure_ascii=False)) for name, value in valid_values)
    return samples


def validate_repair(
    repair_function: RepairFunction,
    sample: str,
    ensure_ascii: bool,
) -> None:
    """Validate once, outside the timed benchmark loop."""
    repaired = repair_function(sample, ensure_ascii=ensure_ascii)
    json.loads(repaired)


def median_runtime_ms(
    repair_function: RepairFunction,
    sample: str,
    *,
    ensure_ascii: bool,
    runs: int,
    warmups: int,
) -> float:
    """Return median repair time without including correctness validation."""
    validate_repair(repair_function, sample, ensure_ascii)
    for _ in range(warmups):
        repair_function(sample, ensure_ascii=ensure_ascii)

    timings: list[int] = []
    gc_enabled = gc.isenabled()
    gc.disable()
    try:
        for _ in range(runs):
            started = time.perf_counter_ns()
            repair_function(sample, ensure_ascii=ensure_ascii)
            timings.append(time.perf_counter_ns() - started)
    finally:
        if gc_enabled:
            gc.enable()

    return statistics.median(timings) / 1_000_000


def run_comparison(
    samples: list[Sample],
    *,
    runs: int,
    warmups: int,
) -> list[tuple[str, bool, float, float, float]]:
    """Benchmark both libraries for every sample and ASCII mode."""
    results = []
    for name, sample in samples:
        for ensure_ascii in (True, False):
            fast_ms = median_runtime_ms(
                fast_json_repair.repair_json,
                sample,
                ensure_ascii=ensure_ascii,
                runs=runs,
                warmups=warmups,
            )
            reference_ms = median_runtime_ms(
                json_repair.repair_json,
                sample,
                ensure_ascii=ensure_ascii,
                runs=runs,
                warmups=warmups,
            )
            results.append((name, ensure_ascii, fast_ms, reference_ms, reference_ms / fast_ms))
    return results


def print_results(results: list[tuple[str, bool, float, float, float]]) -> None:
    """Print per-case medians and geometric-mean speedups."""
    print(
        f"{'Test case':<39} {'ASCII':<7} {'fast (ms)':>11} "
        f"{'reference (ms)':>15} {'speedup':>10}"
    )
    print("-" * 88)

    invalid_speedups = []
    valid_speedups = []
    for name, ensure_ascii, fast_ms, reference_ms, speedup in results:
        print(
            f"{name.removeprefix('VALID: '):<39} {str(ensure_ascii):<7} "
            f"{fast_ms:>11.3f} {reference_ms:>15.3f} {speedup:>9.2f}x"
        )
        target = valid_speedups if name.startswith("VALID:") else invalid_speedups
        target.append(speedup)

    all_speedups = invalid_speedups + valid_speedups
    print("-" * 88)
    print(
        "Geometric-mean speedup: "
        f"invalid={statistics.geometric_mean(invalid_speedups):.2f}x, "
        f"valid={statistics.geometric_mean(valid_speedups):.2f}x, "
        f"all={statistics.geometric_mean(all_speedups):.2f}x"
    )


def print_hot_path_diagnostics(runs: int, warmups: int) -> None:
    """Measure the optimized object and deep-formatting paths."""
    item_count = 20_000
    invalid = (
        "{items:["
        + ",".join(
            f"{{id:{index},name:'item_{index}',active:True}}" for index in range(item_count)
        )
        + "]}"
    )

    def median_call(call: Callable[[], object]) -> float:
        for _ in range(warmups):
            call()
        timings = []
        gc_enabled = gc.isenabled()
        gc.disable()
        try:
            for _ in range(runs):
                started = time.perf_counter_ns()
                call()
                timings.append(time.perf_counter_ns() - started)
        finally:
            if gc_enabled:
                gc.enable()
        return statistics.median(timings) / 1_000_000

    string_ms = median_call(
        lambda: fast_json_repair.repair_json(invalid, ensure_ascii=False)
    )
    object_ms = median_call(
        lambda: fast_json_repair.repair_json(
            invalid,
            ensure_ascii=False,
            return_objects=True,
        )
    )

    payload = "x" * 100_000
    shallow = f"['{payload}']"
    deep = "[" * 900 + f"'{payload}'" + "]" * 900
    shallow_ms = median_call(
        lambda: fast_json_repair.repair_json(shallow, skip_json_loads=True)
    )
    deep_ms = median_call(
        lambda: fast_json_repair.repair_json(deep, skip_json_loads=True)
    )

    print("\nHot-path diagnostics")
    print("-" * 88)
    print(f"Invalid 20K objects -> string: {string_ms:.3f} ms")
    print(f"Invalid 20K objects -> object: {object_ms:.3f} ms")
    print(f"100K payload at depth 1:        {shallow_ms:.3f} ms")
    print(f"100K payload at depth 900:      {deep_ms:.3f} ms")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--runs", type=int, default=10)
    parser.add_argument("--warmups", type=int, default=3)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument(
        "--skip-diagnostics",
        action="store_true",
        help="Skip object-path and deep-formatting diagnostics.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    samples = generate_samples(args.seed)
    print(
        f"Benchmarking {len(samples)} deterministic samples, "
        f"{args.runs} timed runs and {args.warmups} warmups each.\n"
    )
    results = run_comparison(samples, runs=args.runs, warmups=args.warmups)
    print_results(results)
    if not args.skip_diagnostics:
        print_hot_path_diagnostics(args.runs, args.warmups)


if __name__ == "__main__":
    main()
