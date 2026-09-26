#!/usr/bin/env python3
"""SDK mechanism benchmark; run baseline/candidate in separate processes.

CPU includes SDK worker threads and explicit event flushes. The HTTP sink runs
in another process, so its CPU is excluded. Application wrapper work is not
measured. Use --oai-utils for the application's Python anon generator and
--native-anonymous for the new native RNG on the explicit anon_* scenarios.
"""

from __future__ import annotations

import argparse
import cProfile
import ctypes
import gzip
import hashlib
import json
import os
import platform
import resource
import statistics
import subprocess
import sys
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import urlparse

CUSTOM = {
    "service": "synthetic-service",
    "cluster_name": "synthetic-cluster",
    "deployment_track": "stable",
    "sa_server_deploy_id": "synthetic-deploy-123",
    "country": "US",
    "logged_in": False,
    "platform": "web",
    "client_version": "2026.09.14",
    "request_region": "west",
}
META = {
    "country": "US",
    "locale": "en-US",
    "ip": "192.0.2.1",
    "user_agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
    "custom": CUSTOM,
}
NAMES = {
    "gate": "native_context_gate",
    "feature_gate": "native_context_gate",
    "anonymous_gate": "test_50_50",
    "config": "big_number",
    "layer": "layer_with_many_params",
}


def serve(path: str) -> None:
    specs = json.loads(Path(path).read_text())
    specs.pop("checksum", None)
    gate = json.loads(json.dumps(specs["feature_gates"]["test_public"]))
    specs["condition_map"]["4200000000"] = {
        "type": "user_field",
        "field": "service",
        "operator": "any",
        "targetValue": [CUSTOM["service"]],
        "additionalValues": {},
        "idType": "userID",
    }
    gate["rules"][0]["conditions"] = ["4200000000"]
    gate["rules"][0]["passPercentage"] = 50
    specs["feature_gates"][NAMES["gate"]] = gate
    payload = json.dumps(specs).encode()
    counts: dict[str, int] = {}

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *_args):
            pass

        def _send_json(self, body):
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self):
            body = json.dumps(counts).encode() if self.path == "/counts" else payload
            self._send_json(body)

        def do_POST(self):
            body = self.rfile.read(int(self.headers.get("Content-Length", 0)))
            # The SDK posts an empty body when polling a non-CDN ID-list manifest.
            # Keep this separate from event parsing so malformed event batches fail.
            if urlparse(self.path).path == "/v1/get_id_lists":
                self._send_json(b"{}")
                return
            if self.headers.get("Content-Encoding") == "gzip":
                body = gzip.decompress(body)
            for event in json.loads(body).get("events", []):
                name = event.get("eventName", "unknown")
                counts[name] = counts.get(name, 0) + 1
            self._send_json(b'{"success":true}')

    server = HTTPServer(("127.0.0.1", 0), Handler)
    print(server.server_port, flush=True)
    server.serve_forever()


def drain_sdk_events(sdk, event_counts, expected=None):
    """Flush late partial batches until expected deliveries settle, within 10s."""
    assert sdk.flush_events().wait(10)
    counts = event_counts()
    deadline = time.monotonic() + 10
    stable = 0
    while stable < 2 or (expected and counts.get(expected[0], 0) < expected[1]):
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise AssertionError(("Exposures did not finish", expected, counts))
        if expected and counts.get(expected[0], 0) < expected[1]:
            # An automatic flush can publish a partial batch after the previous
            # manual flush took its batches. Polling alone does not flush it.
            assert sdk.flush_events().wait(remaining)
        time.sleep(0.005)
        current = event_counts()
        stable = stable + 1 if current == counts else 0
        counts = current
    return counts


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--server")
    parser.add_argument("--candidate", action="store_true")
    parser.add_argument("--native-anonymous", action="store_true")
    parser.add_argument("--oai-utils")
    parser.add_argument(
        "--specs",
        default=str(
            Path(__file__).resolve().parents[2]
            / "statsig-rust/tests/data/eval_proj_dcs.json"
        ),
    )
    parser.add_argument("--output")
    parser.add_argument("--iterations", type=int, default=12000)
    parser.add_argument("--repetitions", type=int, default=5)
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument("--filter", default="")
    parser.add_argument("--profile")
    parser.add_argument("--allocation-probe")
    parser.add_argument("--stack-output")
    args = parser.parse_args()
    if args.server:
        serve(args.server)
        return
    if args.native_anonymous and not (args.candidate and args.oai_utils):
        parser.error(
            "--native-anonymous requires --candidate and --oai-utils for matched ID semantics"
        )
    if args.oai_utils:
        sys.path.insert(0, args.oai_utils)
        from oai_utils.id_gen import rand_id_with_prefix

        def random_id():
            return rand_id_with_prefix("anon", 8)
    else:
        import uuid

        def random_id():
            return str(uuid.uuid4())

    import statsig_python_core as core
    import statsig_python_core.statsig_python_core as native

    probe = ctypes.CDLL(args.allocation_probe) if args.allocation_probe else None
    if probe:
        probe.probe_count.restype = ctypes.c_ulonglong
        probe.probe_bytes.restype = ctypes.c_ulonglong
        if args.stack_output:
            probe.probe_stacks(1)
            probe.probe_dump.argtypes = [ctypes.c_char_p]
    env = dict(os.environ)
    env.pop("LD_PRELOAD", None)
    server = subprocess.Popen(
        [sys.executable, __file__, "--server", args.specs],
        stdout=subprocess.PIPE,
        text=True,
        env=env,
    )
    port = int(server.stdout.readline())
    sdk = core.Statsig(
        "secret-native-context-benchmark",
        core.StatsigOptions(
            specs_url=f"http://127.0.0.1:{port}/specs",
            log_event_url=f"http://127.0.0.1:{port}/events",
            event_logging_max_queue_size=10000,
            event_logging_flush_interval_ms=600000,
            specs_sync_interval_ms=600000,
            disable_country_lookup=True,
            output_log_level="none",
        ),
    )
    assert sdk.initialize().wait(10) and sdk.is_config_spec_ready()
    anonymous_policy = (
        core.StatsigRandomUserID("anon", 8) if args.native_anonymous else None
    )

    def event_counts():
        with urllib.request.urlopen(f"http://127.0.0.1:{port}/counts") as response:
            return json.load(response)

    def drain_events(expected=None):
        return drain_sdk_events(sdk, event_counts, expected)

    profiler = cProfile.Profile() if args.profile else None
    pool = ThreadPoolExecutor(max_workers=args.workers) if args.workers > 1 else None
    # (label, entity, context reuse; 0=one-shot custom only, -1=one context/run,
    # -2=existing cached StatsigUser on both implementations, overlay, identity)
    scenarios = (
        [
            ("one_shot_custom", "gate", 0, False, "anon"),
            ("one_shot_context", "gate", 1, False, "anon"),
            ("reuse2", "gate", 2, False, "anon"),
            ("reuse8", "gate", 8, False, "anon"),
            ("repeated_metadata", "gate", -1, False, "anon"),
            ("changing_overlay", "gate", -1, True, "anon"),
            ("absent_id", "gate", -1, False, "absent"),
            ("stable_id", "gate", -1, False, "stable"),
            ("cached_user", "gate", -2, False, "stable"),
        ]
        + [
            (f"{kind}_{label}", kind, reuse, True, "anon")
            for kind in ("feature_gate", "config", "layer")
            for label, reuse in (("one_shot", 1), ("repeated", -1))
        ]
        + [
            (f"anon_{shape}_{kind}", kind, reuse, False, "anon")
            for kind in ("feature_gate", "layer")
            for shape, reuse in (("no_custom", -3), ("custom", -4), ("request", -5))
        ]
    )
    results = []
    try:
        for label, kind, reuse, overlays, identity in scenarios:
            for disabled in (True, False):
                scenario_name = f"{label}/{'disabled' if disabled else 'enabled'}"
                if args.filter and args.filter not in scenario_name:
                    continue
                option_type = {
                    "gate": core.FeatureGateEvaluationOptions,
                    "feature_gate": core.FeatureGateEvaluationOptions,
                    "config": core.DynamicConfigEvaluationOptions,
                    "layer": core.LayerEvaluationOptions,
                }[kind]
                options = option_type(disable_exposure_logging=disabled)
                method_name = {
                    "gate": "check_gate",
                    "feature_gate": "get_feature_gate",
                    "config": "get_dynamic_config",
                    "layer": "get_layer",
                }[kind]
                optimized = args.candidate and reuse != -2
                anonymous_scenario = label.startswith("anon_")
                native_anonymous = args.native_anonymous and anonymous_scenario
                entity_name = (
                    NAMES["anonymous_gate"]
                    if reuse == -3 and kind == "feature_gate"
                    else NAMES[kind]
                )
                method = getattr(
                    sdk,
                    method_name
                    + (
                        "_anonymous"
                        if native_anonymous
                        else "_with_context"
                        if optimized
                        else ""
                    ),
                )
                latencies = []
                rounds = []
                for repetition in range(args.repetitions):
                    counts_before = drain_events()
                    event_name = {
                        "gate": "statsig::gate_exposure",
                        "feature_gate": "statsig::gate_exposure",
                        "config": "statsig::config_exposure",
                        "layer": "statsig::layer_exposure",
                    }[kind]
                    expected_event = (
                        event_name if identity == "anon" and not disabled else None
                    )
                    if probe:
                        probe.probe_start()
                    start_cpu, start_wall = (
                        time.process_time_ns(),
                        time.perf_counter_ns(),
                    )
                    if profiler:
                        profiler.enable()

                    def run_calls(
                        start_index,
                        end_index,
                        *,
                        reuse=reuse,
                        optimized=optimized,
                        identity=identity,
                        native_anonymous=native_anonymous,
                        overlays=overlays,
                        anonymous_scenario=anonymous_scenario,
                        method=method,
                        entity_name=entity_name,
                        options=options,
                        kind=kind,
                        latencies=latencies,
                    ):
                        context = None
                        cached_user = (
                            core.StatsigUser("stable-session", **META)
                            if reuse == -2
                            else None
                        )
                        if optimized and reuse == -1:
                            context = core.StatsigUserContext(**META)
                        for i in range(start_index, end_index):
                            sample_start = time.perf_counter_ns() if i % 101 == 0 else 0
                            uid = (
                                random_id()
                                if identity == "anon" and not native_anonymous
                                else (
                                    None if identity == "absent" else "stable-session"
                                )
                            )
                            overlay = (
                                {
                                    "request_region": "west" if i % 2 else "east",
                                    "request_ordinal": i % 101,
                                }
                                if overlays
                                else None
                            )
                            if anonymous_scenario:
                                metadata = (
                                    {}
                                    if reuse == -3
                                    else {"custom": CUSTOM}
                                    if reuse == -4
                                    else META
                                )
                                if native_anonymous:
                                    result = method(
                                        entity_name,
                                        anonymous_policy,
                                        options=options,
                                        **metadata,
                                    )
                                elif optimized:
                                    context = (
                                        core.StatsigUserContext(**META)
                                        if reuse == -5
                                        else None
                                    )
                                    result = method(
                                        context,
                                        entity_name,
                                        user_id=uid,
                                        custom=CUSTOM if reuse == -4 else None,
                                        options=options,
                                    )
                                else:
                                    result = method(
                                        core.StatsigUser(uid, **metadata),
                                        entity_name,
                                        options,
                                    )
                            elif optimized:
                                if reuse > 0 and (i - start_index) % reuse == 0:
                                    context = core.StatsigUserContext(**META)
                                result = method(
                                    context,
                                    NAMES[kind],
                                    user_id=uid,
                                    custom=CUSTOM if reuse == 0 else overlay,
                                    options=options,
                                )
                            else:
                                metadata = {"custom": CUSTOM} if reuse == 0 else META
                                if overlay:
                                    metadata = {
                                        **metadata,
                                        "custom": {**CUSTOM, **overlay},
                                    }
                                user = (
                                    cached_user
                                    if cached_user is not None
                                    else core.StatsigUser(uid, **metadata)
                                )
                                result = method(user, NAMES[kind], options)
                            if kind == "config":
                                result.get_float("foo", 0)
                            elif kind == "layer":
                                result.get_string("a_string", "default")
                            if sample_start:
                                latencies.append(time.perf_counter_ns() - sample_start)
                            # Include batch serialization/compression/network CPU and
                            # do not lose events by overflowing the bounded queue.
                            if (i + 1) % 500 == 0:
                                assert sdk.flush_events().wait(10)

                    if pool is None:
                        run_calls(0, args.iterations)
                    else:
                        futures = [
                            pool.submit(
                                run_calls,
                                worker * args.iterations // args.workers,
                                (worker + 1) * args.iterations // args.workers,
                            )
                            for worker in range(args.workers)
                        ]
                        for future in futures:
                            future.result()
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
                    cpu, wall = (
                        time.process_time_ns() - start_cpu,
                        time.perf_counter_ns() - start_wall,
                    )
                    if probe:
                        probe.probe_stop()
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
                            "cpu_ns_per_call": cpu / args.iterations,
                            "wall_ns_per_call": wall / args.iterations,
                            "event_counts": event_delta,
                            "allocation_calls_per_call": probe.probe_count()
                            / args.iterations
                            if probe
                            else None,
                            "allocation_requested_bytes_per_call": probe.probe_bytes()
                            / args.iterations
                            if probe
                            else None,
                        }
                    )
                values = [r["cpu_ns_per_call"] for r in rounds]
                latencies.sort()
                results.append(
                    {
                        "scenario": scenario_name,
                        "cpu_median_ns": statistics.median(values),
                        "cpu_min_ns": min(values),
                        "cpu_max_ns": max(values),
                        "calls_per_cpu_second": 1e9 / statistics.median(values),
                        "latency_p50_ns": statistics.median(latencies),
                        "latency_p95_ns": latencies[int(len(latencies) * 0.95)],
                        "rounds": rounds,
                    }
                )
                print(
                    f"{scenario_name}: {statistics.median(values):.0f} ns CPU/call",
                    flush=True,
                )
        setup = {}
        for name, construct in [
            ("user", lambda: core.StatsigUser("fixed-id", **META))
        ] + (
            [("context", lambda: core.StatsigUserContext(**META))]
            if args.candidate
            else []
        ):
            start = time.process_time_ns()
            for _ in range(args.iterations):
                construct()
            setup[name + "_ns"] = (time.process_time_ns() - start) / args.iterations
        output = {
            "candidate": args.candidate,
            "native_anonymous": args.native_anonymous,
            "sdk_python": core.__file__,
            "sdk_native": native.__file__,
            "native_sha256": hashlib.sha256(
                Path(native.__file__).read_bytes()
            ).hexdigest(),
            "python": sys.version,
            "platform": platform.platform(),
            "generator": "oai_utils.rand_id_with_prefix('anon', 8)"
            if args.oai_utils
            else "uuid.uuid4",
            "anonymous_scenario_generator": "native OsRng / ASCII alphanumeric, prefix anon, length 8"
            if args.native_anonymous
            else "Python generator above",
            "iterations": args.iterations,
            "repetitions": args.repetitions,
            "workers": args.workers,
            "setup": setup,
            "max_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            "results": results,
        }
        if args.stack_output and probe:
            probe.probe_dump(args.stack_output.encode())
            Path(args.stack_output + ".maps").write_text(
                Path("/proc/self/maps").read_text()
            )
        if args.output:
            Path(args.output).write_text(json.dumps(output, indent=2) + "\n")
        if profiler:
            profiler.dump_stats(args.profile)
    finally:
        if pool:
            pool.shutdown()
        sdk.shutdown().wait(10)
        server.terminate()
        server.wait(10)


if __name__ == "__main__":
    main()
