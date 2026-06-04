# SPDX-FileCopyrightText: All Contributors to the PyTango project
# SPDX-License-Identifier: LGPL-3.0-or-later

import argparse
import json
import os
import re
import select
import signal
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.request


DEFAULT_READS_PER_ITERATION = 10
DEFAULT_ITERATIONS = 30
CPP_TANGO_DEVICE = "sys/tg_test/1"
TELEMETRY_ENV_KEYS = (
    "TANGO_TELEMETRY_ENABLE",
    "TANGO_TELEMETRY_TOPICS",
    "TANGO_TELEMETRY_TYPES",
    "TANGO_TELEMETRY_TRACES_EXPORTER",
    "TANGO_TELEMETRY_TRACES_ENDPOINT",
    "TANGO_TELEMETRY_TRACING_EXPORTER",
    "TANGO_TELEMETRY_TRACING_ENDPOINT",
    "TANGO_TELEMETRY_TRACING_EXPORTERS",
    "TANGO_TELEMETRY_TRACING_ENDPOINTS",
    "TANGO_TELEMETRY_LOGS_EXPORTER",
    "TANGO_TELEMETRY_LOGS_ENDPOINT",
    "TANGO_TELEMETRY_LOGGING_EXPORTER",
    "TANGO_TELEMETRY_LOGGING_ENDPOINT",
    "TANGO_TELEMETRY_LOGGING_EXPORTERS",
    "TANGO_TELEMETRY_LOGGING_ENDPOINTS",
    "PYTANGO_TELEMETRY_EMIT_KERNEL_SPANS",
)

MEASUREMENT_RE = re.compile(r"Average execution time: (?P<average>[0-9.eE+-]+) (?P<unit>microseconds|milliseconds).")
STDDEV_RE = re.compile(
    r"Standard deviation of execution times: (?P<stddev>[0-9.eE+-]+) (?P<unit>microseconds|milliseconds)."
)
PERCENTILE_RE = re.compile(
    r"(?P<percentile>50|90|95)th percentile execution time: "
    r"(?P<value>[0-9.eE+-]+) (?P<unit>microseconds|milliseconds)."
)


def positive_int(value):
    parsed_value = int(value)
    if parsed_value <= 0:
        raise argparse.ArgumentTypeError("must be a positive integer")
    return parsed_value


def clean_env(extra_env):
    env = os.environ.copy()
    for key in TELEMETRY_ENV_KEYS:
        env.pop(key, None)
    env.update(extra_env)
    return env


def pixi_command(args, manifest_path):
    command = ["pixi", "run"]
    if manifest_path is not None:
        command.extend(["--manifest-path", manifest_path])
    command.extend(args)
    return command


def telemetry_modes(env_var_style, telemetry_topics, emit_kernel_spans):
    if env_var_style == "singular":
        tracing_exporter = "TANGO_TELEMETRY_TRACES_EXPORTER"
        logging_exporter = "TANGO_TELEMETRY_LOGS_EXPORTER"
    else:
        tracing_exporter = "TANGO_TELEMETRY_TRACING_EXPORTERS"
        logging_exporter = "TANGO_TELEMETRY_LOGGING_EXPORTERS"

    pytango_env = {}
    if emit_kernel_spans:
        pytango_env["PYTANGO_TELEMETRY_EMIT_KERNEL_SPANS"] = "on"

    return [
        ("off", {}),
        (
            "grpc",
            {
                "TANGO_TELEMETRY_ENABLE": "on",
                "TANGO_TELEMETRY_TOPICS": telemetry_topics,
                tracing_exporter: "grpc",
                logging_exporter: "grpc",
            }
            | pytango_env,
        ),
        (
            "http",
            {
                "TANGO_TELEMETRY_ENABLE": "on",
                "TANGO_TELEMETRY_TOPICS": telemetry_topics,
                tracing_exporter: "http",
                logging_exporter: "http",
            }
            | pytango_env,
        ),
    ]


def run_command(command, env, timeout=None):
    completed = subprocess.run(
        command,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=timeout,
        check=False,
    )
    return completed.returncode, completed.stdout


def current_time_millis():
    return int(time.time() * 1000)


def query_tempo_span_count(grafana_url, datasource_uid, query, start_ms, end_ms):
    payload = {
        "queries": [
            {
                "refId": "A",
                "datasource": {"type": "tempo", "uid": datasource_uid},
                "queryType": "traceql",
                "metricsQueryType": "instant",
                "query": query,
                "limit": 20,
            }
        ],
        "from": str(start_ms),
        "to": str(end_ms),
    }
    request = urllib.request.Request(
        f"{grafana_url.rstrip('/')}/api/ds/query",
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            response_payload = json.load(response)
    except (urllib.error.URLError, TimeoutError) as exc:
        raise RuntimeError(f"Failed to query Grafana Tempo span count: {exc}") from exc

    frames = response_payload["results"]["A"]["frames"]
    if not frames:
        return 0
    values = frames[0]["data"]["values"]
    if len(values) < 2 or not values[1]:
        return 0
    return int(values[1][0])


def query_recent_tempo_span_count(grafana_url, datasource_uid, query, lookback_seconds):
    end_ms = current_time_millis()
    start_ms = end_ms - int(lookback_seconds * 1000)
    return query_tempo_span_count(grafana_url, datasource_uid, query, start_ms, end_ms)


def check_tempo_available(grafana_url, datasource_uid, query):
    try:
        query_recent_tempo_span_count(grafana_url, datasource_uid, query, 60)
    except Exception as exc:
        print(
            "Grafana Tempo is not available for span counting.\n"
            f"  Grafana URL: {grafana_url}\n"
            f"  Tempo datasource UID: {datasource_uid}\n"
            "Start a local telemetry stack, for example:\n"
            "  https://github.com/grafana/docker-otel-lgtm\n"
            "Or rerun with --no-span-count to skip Tempo span reporting.\n"
            f"Details: {exc}",
            file=sys.stderr,
        )
        raise SystemExit(1) from exc


def start_server(command, env, ready_text, timeout):
    process = subprocess.Popen(
        command,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        bufsize=1,
        start_new_session=True,
    )
    output = []
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if process.poll() is not None:
            remaining = process.stdout.read() if process.stdout else ""
            output.append(remaining)
            raise RuntimeError(f"Server exited before it was ready: {' '.join(command)}\n{''.join(output)}")
        readable, _, _ = select.select([process.stdout], [], [], 0.1)
        if not readable:
            continue
        line = process.stdout.readline()
        output.append(line)
        if ready_text in line:
            return process

    stop_process(process)
    raise TimeoutError(f"Timed out waiting for server readiness: {' '.join(command)}\n{''.join(output)}")


def stop_process(process):
    if process.poll() is not None:
        return
    process_group = os.getpgid(process.pid)
    os.killpg(process_group, signal.SIGINT)
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        os.killpg(process_group, signal.SIGTERM)
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            os.killpg(process_group, signal.SIGKILL)
            process.wait(timeout=5)
    time.sleep(0.2)


def find_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


def build_cpp_benchmark(env, manifest_path):
    command = pixi_command(
        [
            "sh",
            "-c",
            'clang++ -std=c++17 -isystem "$CONDA_PREFIX/include" '
            '-L"$CONDA_PREFIX/lib" -Wl,-rpath,"$CONDA_PREFIX/lib" '
            "benchmark.cpp -o benchmark -ltango -lomniORB4 -lomnithread",
        ],
        manifest_path,
    )
    returncode, output = run_command(command, env)
    if returncode != 0:
        raise RuntimeError(f"C++ benchmark build failed:\n{output}")


def cpp_benchmark_command(device_name, reads_per_iteration, iterations):
    return [
        "./benchmark",
        "--device",
        device_name,
        "--reads-per-iteration",
        str(reads_per_iteration),
        "--iterations",
        str(iterations),
    ]


def python_benchmark_command(scenario, reads_per_iteration, iterations, manifest_path, server_port=None):
    return pixi_command(
        [
            "python",
            "-u",
            "benchmark.py",
            scenario,
            "--reads-per-iteration",
            str(reads_per_iteration),
            "--iterations",
            str(iterations),
        ]
        + ([] if server_port is None else ["--server-port", str(server_port)]),
        manifest_path,
    )


def convert_to_microseconds(value, unit):
    if unit == "milliseconds":
        return value * 1000.0
    return value


def parse_result(output):
    measurement = MEASUREMENT_RE.search(output)
    stddev = STDDEV_RE.search(output)
    if measurement is None or stddev is None:
        raise ValueError(f"Could not parse benchmark result:\n{output}")

    average = convert_to_microseconds(float(measurement.group("average")), measurement.group("unit"))
    deviation = convert_to_microseconds(float(stddev.group("stddev")), stddev.group("unit"))
    percentiles = {
        match.group("percentile"): convert_to_microseconds(float(match.group("value")), match.group("unit"))
        for match in PERCENTILE_RE.finditer(output)
    }
    missing_percentiles = {"50", "90", "95"} - percentiles.keys()
    if missing_percentiles:
        raise ValueError(f"Could not parse percentile result:\n{output}")
    return average, deviation, percentiles["50"], percentiles["90"], percentiles["95"]


def run_cpp_client_cpp_server(env, reads_per_iteration, iterations, manifest_path, server_start_timeout):
    server = start_server(
        pixi_command(["TangoTest", "test"], manifest_path),
        env,
        "Ready to accept request",
        server_start_timeout,
    )
    try:
        command = cpp_benchmark_command(CPP_TANGO_DEVICE, reads_per_iteration, iterations)
        return run_command(command, env, timeout=120)
    finally:
        stop_process(server)


def run_cpp_client_python_server(env, reads_per_iteration, iterations, manifest_path, server_start_timeout):
    server_port = find_free_port()
    server = start_server(
        python_benchmark_command(
            "cpp-client-python-server",
            reads_per_iteration,
            iterations,
            manifest_path,
            server_port,
        ),
        env,
        "Python server running",
        server_start_timeout,
    )
    try:
        device_name = f"tango://127.0.0.1:{server_port}/test/device/1#dbase=no"
        command = cpp_benchmark_command(device_name, reads_per_iteration, iterations)
        return run_command(command, env, timeout=120)
    finally:
        stop_process(server)


def run_python_client_cpp_server(env, reads_per_iteration, iterations, manifest_path, server_start_timeout):
    server = start_server(
        pixi_command(["TangoTest", "test"], manifest_path),
        env,
        "Ready to accept request",
        server_start_timeout,
    )
    try:
        command = python_benchmark_command("python-client-cpp-server", reads_per_iteration, iterations, manifest_path)
        return run_command(command, env, timeout=120)
    finally:
        stop_process(server)


def run_python_client_python_server(env, reads_per_iteration, iterations, manifest_path, server_start_timeout):
    command = python_benchmark_command("python-client-python-server", reads_per_iteration, iterations, manifest_path)
    return run_command(command, env, timeout=120)


SCENARIOS = [
    ("cpp-client-cpp-server", run_cpp_client_cpp_server),
    ("python-client-cpp-server", run_python_client_cpp_server),
    ("cpp-client-python-server", run_cpp_client_python_server),
    ("python-client-python-server", run_python_client_python_server),
]


def format_span_count(spans):
    if spans is None:
        return "-"
    return f"{spans / 1000.0:.1f}k"


def print_results(results):
    print()
    headers = (
        "telemetry",
        "scenario",
        "average [us]",
        "stddev [us]",
        "p50 [us]",
        "p90 [us]",
        "p95 [us]",
        "spans",
    )
    widths = [
        max(len(headers[0]), *(len(row[0]) for row in results)),
        max(len(headers[1]), *(len(row[1]) for row in results)),
        max(len(headers[2]), *(len(f"{row[2]:.0f}") for row in results)),
        max(len(headers[3]), *(len(f"{row[3]:.0f}") for row in results)),
        max(len(headers[4]), *(len(f"{row[4]:.0f}") for row in results)),
        max(len(headers[5]), *(len(f"{row[5]:.0f}") for row in results)),
        max(len(headers[6]), *(len(f"{row[6]:.0f}") for row in results)),
        max(
            len(headers[7]),
            *(len(format_span_count(row[7])) for row in results),
        ),
    ]

    print(
        f"| {headers[0]:<{widths[0]}} | "
        f"{headers[1]:<{widths[1]}} | "
        f"{headers[2]:>{widths[2]}} | "
        f"{headers[3]:>{widths[3]}} | "
        f"{headers[4]:>{widths[4]}} | "
        f"{headers[5]:>{widths[5]}} | "
        f"{headers[6]:>{widths[6]}} | "
        f"{headers[7]:>{widths[7]}} |"
    )
    print(
        f"| {'-' * widths[0]} | "
        f"{'-' * widths[1]} | "
        f"{'-' * widths[2]} | "
        f"{'-' * widths[3]} | "
        f"{'-' * widths[4]} | "
        f"{'-' * widths[5]} | "
        f"{'-' * widths[6]} | "
        f"{'-' * widths[7]} |"
    )
    for telemetry_name, scenario_name, average, stddev, p50, p90, p95, spans in results:
        span_count = format_span_count(spans)
        print(
            f"| {telemetry_name:<{widths[0]}} | "
            f"{scenario_name:<{widths[1]}} | "
            f"{average:>{widths[2]}.0f} | "
            f"{stddev:>{widths[3]}.0f} | "
            f"{p50:>{widths[4]}.0f} | "
            f"{p90:>{widths[5]}.0f} | "
            f"{p95:>{widths[6]}.0f} | "
            f"{span_count:>{widths[7]}} |"
        )


def main():
    parser = argparse.ArgumentParser(description="Run telemetry benchmark scenarios.")
    parser.add_argument(
        "--reads-per-iteration",
        default=DEFAULT_READS_PER_ITERATION,
        type=positive_int,
        help="Number of reads per timed iteration.",
    )
    parser.add_argument(
        "--iterations",
        default=DEFAULT_ITERATIONS,
        type=positive_int,
        help="Number of timed iterations.",
    )
    parser.add_argument(
        "--skip-build",
        action="store_true",
        help="Do not rebuild the C++ benchmark before running scenarios.",
    )
    parser.add_argument(
        "--pixi-manifest-path",
        help="Pixi manifest path for the PyTango/cppTango version under test.",
    )
    parser.add_argument(
        "--telemetry-env-vars",
        choices=("plural", "singular"),
        default="plural",
        help="Telemetry exporter environment variable spelling to use.",
    )
    parser.add_argument(
        "--telemetry-topics",
        default="all",
        help="Value to set for TANGO_TELEMETRY_TOPICS when telemetry is enabled.",
    )
    parser.add_argument(
        "--emit-kernel-spans",
        action="store_true",
        help=(
            "Set PYTANGO_TELEMETRY_EMIT_KERNEL_SPANS=on for benchmark runs. "
            "By default PyTango kernel spans are skipped."
        ),
    )
    parser.add_argument(
        "--server-start-timeout",
        default=60.0,
        type=float,
        help="Seconds to wait for benchmark servers to become ready.",
    )
    parser.add_argument(
        "--grafana-url",
        default="http://localhost:3000",
        help="Grafana URL used to query Tempo span counts.",
    )
    parser.add_argument(
        "--tempo-datasource-uid",
        default="tempo",
        help="Grafana datasource UID for Tempo.",
    )
    parser.add_argument(
        "--span-count-query",
        default="{} | count_over_time()",
        help="TraceQL metrics query used to count spans.",
    )
    parser.add_argument(
        "--span-count-wait",
        default=40.0,
        type=float,
        help="Seconds to wait after all scenarios finish before querying Tempo.",
    )
    parser.add_argument(
        "--scenario-sleep",
        default=5.0,
        type=float,
        help="Seconds to sleep after each scenario - used as Tempo query padding.",
    )
    parser.add_argument(
        "--no-span-count",
        action="store_true",
        help="Do not query Grafana Tempo for per-scenario span counts.",
    )
    parser.add_argument(
        "--scenario",
        action="append",
        choices=[scenario_name for scenario_name, _ in SCENARIOS],
        help="Scenario to run. Can be repeated. Defaults to all scenarios.",
    )
    args = parser.parse_args()

    if not args.no_span_count:
        check_tempo_available(
            args.grafana_url,
            args.tempo_datasource_uid,
            args.span_count_query,
        )

    base_env = clean_env({})
    if not args.skip_build:
        print("Building C++ benchmark...")
        build_cpp_benchmark(base_env, args.pixi_manifest_path)

    results = []
    span_queries = []
    selected_scenarios = {scenario_name for scenario_name in args.scenario} if args.scenario else None
    for telemetry_name, telemetry_env in telemetry_modes(
        args.telemetry_env_vars, args.telemetry_topics, args.emit_kernel_spans
    ):
        env = clean_env(telemetry_env)
        for scenario_name, scenario_runner in SCENARIOS:
            if selected_scenarios is not None and scenario_name not in selected_scenarios:
                continue
            print(f"Running telemetry={telemetry_name}, scenario={scenario_name}...")
            time.sleep(args.scenario_sleep)
            print(f"  Starting scenario... {time.ctime()}")
            scenario_start_ms = current_time_millis()
            returncode, output = scenario_runner(
                env,
                args.reads_per_iteration,
                args.iterations,
                args.pixi_manifest_path,
                args.server_start_timeout,
            )
            scenario_end_ms = current_time_millis()
            print(f"  Scenario finished    {time.ctime()}")
            time.sleep(args.scenario_sleep)
            if returncode != 0:
                print(output)
                raise RuntimeError(f"Benchmark failed: telemetry={telemetry_name}, scenario={scenario_name}")
            average, stddev, p50, p90, p95 = parse_result(output)
            results.append((telemetry_name, scenario_name, average, stddev, p50, p90, p95, None))
            if not args.no_span_count:
                query_padding_ms = int(args.scenario_sleep * 1000)
                span_queries.append(
                    (
                        len(results) - 1,
                        scenario_start_ms - query_padding_ms,
                        scenario_end_ms + query_padding_ms,
                    )
                )

    if span_queries:
        print("Querying Tempo span counts...")
        time.sleep(args.span_count_wait)
        for result_index, start_ms, end_ms in span_queries:
            spans = query_tempo_span_count(
                args.grafana_url,
                args.tempo_datasource_uid,
                args.span_count_query,
                start_ms,
                end_ms,
            )
            results[result_index] = (*results[result_index][:-1], spans)

    print_results(results)


if __name__ == "__main__":
    main()
