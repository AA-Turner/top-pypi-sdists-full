# SPDX-FileCopyrightText: All Contributors to the PyTango project
# SPDX-License-Identifier: LGPL-3.0-or-later

import argparse
import math
import time

from tango import DeviceProxy
from tango.test_context import DeviceTestContext
from tango.server import Device, attribute

N_READS_PER_ITERATION = 100
N_ITERATIONS = 300


class TestDevice(Device):
    _value = 0.0

    @attribute
    def double_scalar(self) -> float:
        self._value += 1.0
        return self._value

    @double_scalar.write
    def double_scalar(self, value: float) -> None:
        self._value = value


def eval_telemetry_overhead(
    device_name,
    num_reads_per_iteration=N_READS_PER_ITERATION,
    num_iterations=N_ITERATIONS,
):
    time_per_iteration = []
    dp = DeviceProxy(device_name)

    for i in range(num_iterations):
        start = time.perf_counter()
        for _ in range(num_reads_per_iteration):
            _ = dp.read_attribute("double_scalar")
        end = time.perf_counter()
        duration_us = (end - start) * 1_000_000.0
        print(
            f"  {i:3d} Total execution time for {num_reads_per_iteration} iterations: {duration_us:.0f} microseconds."
        )
        tpi = duration_us / num_reads_per_iteration
        print(f"  {i:3d} Average execution time per iteration: {tpi:.0f} microseconds")
        time_per_iteration.append(tpi)

    average_tpi = sum(time_per_iteration) / num_iterations
    square_sum = 0.0
    for tpi in time_per_iteration:
        square_sum += (tpi - average_tpi) * (tpi - average_tpi)

    rms_tpi = (square_sum / num_iterations) ** 0.5
    sorted_time_per_iteration = sorted(time_per_iteration)

    print(f"Average execution time: {average_tpi:.0f} microseconds.")
    print(f"Standard deviation of execution times: {rms_tpi:.0f} microseconds.")
    print(f"50th percentile execution time: {percentile(sorted_time_per_iteration, 50):.0f} microseconds.")
    print(f"90th percentile execution time: {percentile(sorted_time_per_iteration, 90):.0f} microseconds.")
    print(f"95th percentile execution time: {percentile(sorted_time_per_iteration, 95):.0f} microseconds.")


def percentile(sorted_values, percentile_value):
    rank = math.ceil((percentile_value / 100.0) * len(sorted_values))
    rank = max(rank, 1)
    return sorted_values[rank - 1]


def positive_int(value):
    parsed_value = int(value)
    if parsed_value <= 0:
        raise argparse.ArgumentTypeError("must be a positive integer")
    return parsed_value


def benchmark_python_client_and_python_server(num_reads_per_iteration, num_iterations):
    with DeviceTestContext(TestDevice, device_name="test/device/1", process=True):
        print("Python server running, and runing Python client benchmark now...")
        eval_telemetry_overhead(
            "test/device/1",
            num_reads_per_iteration=num_reads_per_iteration,
            num_iterations=num_iterations,
        )


def benchmark_cpp_client_and_python_server(num_reads_per_iteration, num_iterations, server_port):
    context = DeviceTestContext(TestDevice, device_name="test/device/1", process=True, port=server_port)
    with context:
        device_url = context.get_device_access()
        print(f"Python server running - run C++ client benchmark now for {device_url}")
        print(
            f"Suggested C++ client options: --device {device_url} --reads-per-iteration {num_reads_per_iteration} --iterations {num_iterations}"
        )
        time.sleep(100)


def benchmark_python_client_and_cpp_server(num_reads_per_iteration, num_iterations):
    eval_telemetry_overhead(
        "sys/tg_test/1",
        num_reads_per_iteration=num_reads_per_iteration,
        num_iterations=num_iterations,
    )


BENCHMARKS = {
    "python-client-python-server": benchmark_python_client_and_python_server,
    "cpp-client-python-server": benchmark_cpp_client_and_python_server,
    "python-client-cpp-server": benchmark_python_client_and_cpp_server,
}


def main():
    parser = argparse.ArgumentParser(description="Run a PyTango telemetry benchmark.")
    parser.add_argument(
        "benchmark",
        choices=BENCHMARKS,
        default="python-client-python-server",
        nargs="?",
        help="Benchmark scenario to run.",
    )
    parser.add_argument(
        "--reads-per-iteration",
        default=N_READS_PER_ITERATION,
        type=positive_int,
        help="Number of reads per timed iteration.",
    )
    parser.add_argument(
        "--iterations",
        default=N_ITERATIONS,
        type=positive_int,
        help="Number of timed iterations.",
    )
    parser.add_argument(
        "--server-port",
        default=44555,
        type=positive_int,
        help="Port for the PyTango server used by the C++ client benchmark.",
    )
    args = parser.parse_args()
    if args.benchmark == "cpp-client-python-server":
        BENCHMARKS[args.benchmark](args.reads_per_iteration, args.iterations, args.server_port)
    else:
        BENCHMARKS[args.benchmark](args.reads_per_iteration, args.iterations)


if __name__ == "__main__":
    main()
