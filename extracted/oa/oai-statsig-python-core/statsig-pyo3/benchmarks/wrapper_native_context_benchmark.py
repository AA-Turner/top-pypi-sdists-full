#!/usr/bin/env python3
"""Complete monorepo helpers, including each version's per-call ID generation.

Run baseline and candidate in separate processes with their package roots on
PYTHONPATH. Requires the chatgpt-feature-flags-runtime test environment. The
sibling native_context_benchmark.py owns an external local HTTP sink. No real
SDK keys, network service, or production exposures are used.
"""

from __future__ import annotations

import argparse
import contextlib
import cProfile
import ctypes
import gc
import hashlib
import json
import os
import platform
import resource
import statistics
import subprocess
import sys
import time
import tracemalloc
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path


def current_rss_bytes() -> int | None:
    """Current process residency, including native allocations, on Linux."""
    try:
        resident_pages = int(Path("/proc/self/statm").read_text().split()[1])
        return resident_pages * os.sysconf("SC_PAGE_SIZE")
    except (OSError, ValueError, IndexError):
        return None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True)
    parser.add_argument("--iterations", type=int, default=10000)
    parser.add_argument("--repetitions", type=int, default=5)
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument("--filter", default="")
    parser.add_argument("--profile")
    parser.add_argument("--memory", action="store_true")
    parser.add_argument("--allocation-probe")
    parser.add_argument("--expect-native", action="store_true")
    parser.add_argument("--expect-native-anonymous", action="store_true")
    args = parser.parse_args()
    # Match metadata acquisition in the actual helper. Values are synthetic.
    os.environ.update(
        DD_SERVICE="synthetic-service",
        SA_SERVER_DEPLOY_ID="synthetic-deploy-123",
        OPENAI_CLUSTER="synthetic-cluster",
        OPENAI_DEPLOYMENT_TRACK="stable",
    )
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import statsig_python_core.statsig_python_core as native
    from chatgpt_feature_flags_runtime import feature_flags as feature_flags_module
    from native_context_benchmark import NAMES, drain_sdk_events
    from oai_statsig import evaluate, initialize_statsig, shutdown_statsig
    from oai_statsig.const import StatsigProject
    from starlette.requests import Request
    from statsig import statsig

    env = dict(os.environ)
    env.pop("LD_PRELOAD", None)
    server = subprocess.Popen(
        [
            sys.executable,
            str(Path(__file__).with_name("native_context_benchmark.py")),
            "--server",
            str(
                Path(__file__).resolve().parents[2]
                / "statsig-rust/tests/data/eval_proj_dcs.json"
            ),
        ],
        stdout=subprocess.PIPE,
        text=True,
        env=env,
    )
    port = int(server.stdout.readline())

    def event_counts():
        with urllib.request.urlopen(f"http://127.0.0.1:{port}/counts") as response:
            return json.load(response)

    def drain_events(expected=None):
        return drain_sdk_events(sdk, event_counts, expected)

    initialize_statsig(
        statsig_project=StatsigProject.OTHER,
        local_mode=False,
        sdk_mode="rust",
        use_proxy=False,
        api_key_override="secret-native-wrapper-benchmark",
        api=f"http://127.0.0.1:{port}",
        disable_shared_mem_datastore_for_initialization=True,
        evaluation_cache_enabled_for_initialization=False,
        rulesets_sync_interval=600,
        logging_interval=600,
    )
    adapter = statsig.get_instance()
    sdk = adapter.get_rust_sdk()
    assert sdk.is_config_spec_ready(), (
        "Benchmark cannot evaluate uninitialized defaults"
    )
    assert not adapter._evaluation_cache_enabled_for_initialization
    assert getattr(adapter, "native_evaluation_enabled", False) == args.expect_native
    assert (
        getattr(adapter, "native_anonymous_evaluation_enabled", False)
        == args.expect_native_anonymous
    )
    flagging = feature_flags_module.feature_flagging
    flagging.is_fake = False
    request = Request(
        {
            "type": "http",
            "client": ("192.0.2.1", 1234),
            "headers": [
                (b"cf-connecting-ip", b"192.0.2.2"),
                (b"cf-ipcountry", b"US"),
                (b"accept-language", b"en-US"),
                (b"oai-client-user-agent", b"synthetic-browser"),
            ],
        }
    )
    # Include both rule-match outcomes; no all-default benchmark is accepted.
    sample = {
        flagging._check_feature_internal(
            NAMES["gate"],
            None,
            additional_custom_fields={"service": "synthetic-service"},
        )
        for _ in range(128)
    }
    assert sample == {True, False}, sample
    no_custom_sample = {
        flagging._check_feature_internal(NAMES["anonymous_gate"], None)
        for _ in range(128)
    }
    assert no_custom_sample == {True, False}, no_custom_sample
    layer_parameters = {"a_string": "fallback"}
    example, _ = flagging.get_layer_param_values(
        NAMES["layer"], None, layer_parameters, expose=False
    )
    assert example["a_string"] != "fallback", example

    def call(scenario, i, disabled):
        # Construct caller overlays inside the measurement, at call frequency.
        if scenario == "cached_gate":
            return evaluate.check_unauthed_feature_gate(NAMES["gate"])
        if scenario == "cached_config":
            return evaluate.get_unauthed_dynamic_config(
                NAMES["config"], log_exposure=not disabled
            )
        if scenario in {"random_gate", "overlay_gate", "cold_gate"}:
            if scenario == "cold_gate" and hasattr(adapter, "_unauthed_contexts"):
                # Charge every candidate call for rebuilding its metadata context.
                adapter._unauthed_contexts.clear()
            return evaluate.check_unauthed_feature_gate(
                NAMES["gate"],
                use_semi_random_id=True,
                custom_fields={"request_region": "west", "request_number": i}
                if scenario == "overlay_gate"
                else None,
            )
        if scenario in {"custom_gate", "env_churn_gate"}:
            if scenario == "env_churn_gate":
                os.environ["SA_SERVER_DEPLOY_ID"] = f"synthetic-deploy-{i % 2}"
            return evaluate.check_unauthed_feature_gate(
                NAMES["gate"],
                custom_fields={"request_region": "west", "request_number": i},
            )
        if scenario == "random_config":
            return evaluate.get_unauthed_dynamic_config(
                NAMES["config"],
                use_semi_random_id=True,
                custom={"request_region": "west", "request_number": i},
                log_exposure=not disabled,
            )
        if scenario.startswith("anon_") and scenario.endswith("gate"):
            no_custom = "no_custom" in scenario
            return flagging._check_feature_internal(
                NAMES["anonymous_gate"] if no_custom else NAMES["gate"],
                None,
                request=request if "request" in scenario else None,
                additional_custom_fields={
                    "service": "synthetic-service",
                    "request_number": i,
                }
                if not no_custom
                else None,
            )
        if scenario.startswith("anon_") and scenario.endswith("layer"):
            no_custom = "no_custom" in scenario
            return flagging.get_layer_param_values(
                NAMES["layer"],
                None,
                layer_parameters,
                request=request if "request" in scenario else None,
                additional_custom_fields={
                    "service": "synthetic-service",
                    "request_number": i,
                }
                if not no_custom
                else None,
                expose=not disabled,
            )
        raise ValueError(scenario)

    probe = ctypes.CDLL(args.allocation_probe) if args.allocation_probe else None
    if probe:
        probe.probe_count.restype = ctypes.c_ulonglong
        probe.probe_bytes.restype = ctypes.c_ulonglong
    profiler = cProfile.Profile() if args.profile else None
    pool = ThreadPoolExecutor(max_workers=args.workers) if args.workers > 1 else None
    results = []
    scenarios = [
        "cached_gate",
        "cached_config",
        "random_gate",
        "overlay_gate",
        "custom_gate",
        "random_config",
        "anon_gate",
        "anon_no_custom_gate",
        "anon_request_gate",
        "anon_request_no_custom_gate",
        "anon_layer",
        "anon_no_custom_layer",
        "anon_request_layer",
        "anon_request_no_custom_layer",
        "cold_gate",
        "env_churn_gate",
    ]
    try:
        for scenario in scenarios:
            for disabled in (True, False):
                # Generic unauthed gate has no exposure-disable argument.
                if (
                    disabled
                    and scenario.endswith("gate")
                    and not scenario.startswith("anon_")
                ):
                    continue
                label = f"{scenario}/{'disabled' if disabled else 'enabled'}"
                if args.filter not in label:
                    continue
                rounds = []

                def run_calls(start, end, *, scenario=scenario, disabled=disabled):
                    suppression = (
                        feature_flags_module.suppress_user_statsig_exposure_logging()
                        if disabled
                        else contextlib.nullcontext()
                    )
                    with suppression:
                        for i in range(start, end):
                            call(scenario, i, disabled)

                run_calls(0, 100)
                for _ in range(args.repetitions):
                    counts_before = drain_events()
                    expected_event = (
                        (
                            "statsig::gate_exposure"
                            if scenario.endswith("gate")
                            else "statsig::layer_exposure"
                        )
                        if scenario.startswith("anon_") and not disabled
                        else None
                    )
                    if probe:
                        probe.probe_start()
                    cpu_start, wall_start = (
                        time.process_time_ns(),
                        time.perf_counter_ns(),
                    )
                    if profiler:
                        profiler.enable()
                    if pool:
                        futures = [
                            pool.submit(
                                run_calls,
                                args.iterations * worker // args.workers,
                                args.iterations * (worker + 1) // args.workers,
                            )
                            for worker in range(args.workers)
                        ]
                        for future in futures:
                            future.result()
                    else:
                        run_calls(0, args.iterations)
                    counts_after = drain_events(
                        (
                            expected_event,
                            counts_before.get(expected_event, 0) + args.iterations,
                        )
                        if expected_event
                        else None
                    )
                    if profiler:
                        profiler.disable()
                    cpu_ns, wall_ns = (
                        time.process_time_ns() - cpu_start,
                        time.perf_counter_ns() - wall_start,
                    )
                    allocations = None
                    if probe:
                        probe.probe_stop()
                        allocations = {
                            "requests_per_call": probe.probe_count() / args.iterations,
                            "requested_bytes_per_call": probe.probe_bytes()
                            / args.iterations,
                        }
                    event_delta = {
                        name: count - counts_before.get(name, 0)
                        for name, count in counts_after.items()
                    }
                    if expected_event:
                        assert event_delta.get(expected_event, 0) == args.iterations, (
                            event_delta
                        )
                    rounds.append(
                        {
                            "cpu_us": cpu_ns / args.iterations / 1000,
                            "throughput_per_s": args.iterations * 1e9 / wall_ns,
                            "allocations": allocations,
                            "event_counts": event_delta,
                        }
                    )
                # Latency instrumentation is excluded from the CPU loop above.
                latencies = []
                with (
                    feature_flags_module.suppress_user_statsig_exposure_logging()
                    if disabled
                    else contextlib.nullcontext()
                ):
                    for i in range(1000):
                        start = time.perf_counter_ns()
                        call(scenario, i, disabled)
                        latencies.append((time.perf_counter_ns() - start) / 1000)
                drain_events()
                memory = None
                if args.memory:
                    gc.collect()
                    tracemalloc.start()
                    run_calls(0, 1000)
                    drain_events()
                    gc.collect()
                    initial, _ = tracemalloc.get_traced_memory()
                    rss_initial = current_rss_bytes()
                    run_calls(1000, 11000)
                    drain_events()
                    gc.collect()
                    final, peak = tracemalloc.get_traced_memory()
                    rss_final = current_rss_bytes()
                    tracemalloc.stop()
                    memory = {
                        "retained_growth_bytes_10000_calls": final - initial,
                        "peak_traced_bytes": peak,
                        "rss_initial_bytes": rss_initial,
                        "rss_final_bytes": rss_final,
                        "rss_growth_bytes_10000_calls": rss_final - rss_initial
                        if rss_initial is not None and rss_final is not None
                        else None,
                    }
                cpu = [r["cpu_us"] for r in rounds]
                latencies.sort()
                row = {
                    "scenario": label,
                    "rounds": rounds,
                    "cpu_median_us": statistics.median(cpu),
                    "cpu_min_us": min(cpu),
                    "cpu_max_us": max(cpu),
                    "latency_us": {
                        f"p{p}": latencies[int(p / 100 * (len(latencies) - 1))]
                        for p in (50, 95, 99)
                    },
                    "latency_measurement": "single caller, excludes explicit flush",
                    "memory": memory,
                }
                results.append(row)
                print(json.dumps(row), flush=True)
        output = {
            "python": sys.version,
            "platform": platform.platform(),
            "native_file": native.__file__,
            "native_sha256": hashlib.sha256(
                Path(native.__file__).read_bytes()
            ).hexdigest(),
            "wrapper_file": evaluate.__file__,
            "chatgpt_file": feature_flags_module.__file__,
            "iterations": args.iterations,
            "repetitions": args.repetitions,
            "workers": args.workers,
            "native_enabled": args.expect_native,
            "native_anonymous_enabled": args.expect_native_anonymous,
            "evaluation_cache_enabled": False,
            "rss_max_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            "results": results,
        }
        Path(args.output).write_text(json.dumps(output, indent=2) + "\n")
        if profiler:
            profiler.dump_stats(args.profile)
    finally:
        if pool:
            pool.shutdown()
        shutdown_statsig()
        server.terminate()
        server.wait()


if __name__ == "__main__":
    main()
