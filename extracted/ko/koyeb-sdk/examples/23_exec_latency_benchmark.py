#!/usr/bin/env python3
"""Benchmark exec latency for various trivial tasks.

Runs a series of simple commands using both regular and streaming exec modes,
comparing wall-clock time against the duration reported by CommandResult to
show the overhead introduced by the SDK / network round-trip.
"""

import argparse
import os
import random
import string
import sys
import time

from koyeb import Sandbox


COMMANDS = [
    ("echo hello", "echo"),
    ("true", "no-op (true)"),
    ("date", "date"),
    ("cat /etc/hostname", "read small file"),
    ("ls /", "ls root"),
    ("echo -n abc | wc -c", "pipe + wc"),
    ("python3 -c 'print(1+1)'", "python one-liner"),
    ("sh -c 'for i in 1 2 3; do echo $i; done'", "shell loop"),
    ("env | head -5", "env (first 5)"),
    ("uname -a", "uname"),
]

# Commands that produce increasing amounts of output
OUTPUT_SIZE_COMMANDS = [
    ("echo ok", "5 bytes"),
    ("head -c 100 /dev/urandom | base64", "~136 bytes"),
    ("head -c 1000 /dev/urandom | base64", "~1.3 KB"),
    ("head -c 10000 /dev/urandom | base64", "~13 KB"),
    ("head -c 100000 /dev/urandom | base64", "~133 KB"),
    ("head -c 1000000 /dev/urandom | base64", "~1.3 MB"),
    ("seq 1 100", "100 lines"),
    ("seq 1 10000", "10k lines"),
    ("seq 1 100000", "100k lines"),
]

NUM_ITERATIONS = 3


def fmt_ms(seconds: float) -> str:
    return f"{seconds * 1000:7.1f}ms"


def noop(_data: str) -> None:
    pass


def run_benchmark(sandbox, label, exec_fn, pause=0.0):
    """Run the benchmark suite using the given exec function.

    Args:
        sandbox: The sandbox instance.
        label: A human-readable label for the exec mode (e.g. "regular", "streaming").
        exec_fn: A callable(cmd) -> CommandResult.
        pause: Seconds to sleep between each command execution.
    """
    print(f"\n{'=' * 76}")
    print(f" {label} exec")
    print(f"{'=' * 76}")

    # Warm-up
    exec_fn("true")

    print(f"\n  {'Command':<23} {'Iter':>4}  {'Wall':>9}  {'Duration':>9}  {'Overhead':>9}")
    print(f"  {'-' * 70}")

    summary: dict[str, list[float]] = {}

    for cmd, cmd_label in COMMANDS:
        summary[cmd_label] = []
        for i in range(NUM_ITERATIONS):
            if pause > 0:
                time.sleep(pause)
            wall_start = time.time()
            result = exec_fn(cmd)
            wall = time.time() - wall_start
            duration = result.duration
            overhead = wall - duration

            summary[cmd_label].append(wall)

            print(
                f"  {cmd_label:<23} {i + 1:>4}  {fmt_ms(wall)}  {fmt_ms(duration)}  {fmt_ms(overhead)}"
            )

            if result.exit_code != 0:
                print(f"    [exit_code={result.exit_code}] {result.stderr.strip()}")

    # Per-mode summary
    print(f"\n  {'-' * 70}")
    print(f"  {'Command':<23} {'Avg Wall':>9}  {'Min Wall':>9}  {'Max Wall':>9}")
    print(f"  {'-' * 70}")
    for cmd_label, times in summary.items():
        avg = sum(times) / len(times)
        print(f"  {cmd_label:<23} {fmt_ms(avg)}  {fmt_ms(min(times))}  {fmt_ms(max(times))}")

    return summary


def fmt_size(n_bytes: int) -> str:
    if n_bytes < 1024:
        return f"{n_bytes} B"
    elif n_bytes < 1024 * 1024:
        return f"{n_bytes / 1024:.1f} KB"
    else:
        return f"{n_bytes / (1024 * 1024):.1f} MB"


def run_output_benchmark(sandbox, label, exec_fn, pause=0.0):
    """Benchmark how exec performance scales with output size.

    Args:
        sandbox: The sandbox instance.
        label: A human-readable label for the exec mode.
        exec_fn: A callable(cmd) -> CommandResult.
        pause: Seconds to sleep between each command execution.
    """
    print(f"\n{'=' * 86}")
    print(f" {label} exec — output retrieval")
    print(f"{'=' * 86}")

    # Warm-up
    exec_fn("true")

    print(f"\n  {'Payload':<12} {'Iter':>4}  {'Wall':>9}  {'Duration':>9}  {'Overhead':>9}  {'Output':>10}")
    print(f"  {'-' * 80}")

    summary: dict[str, list[tuple[float, int]]] = {}

    for cmd, size_label in OUTPUT_SIZE_COMMANDS:
        summary[size_label] = []
        for i in range(NUM_ITERATIONS):
            if pause > 0:
                time.sleep(pause)
            wall_start = time.time()
            result = exec_fn(cmd)
            wall = time.time() - wall_start
            duration = result.duration
            overhead = wall - duration
            out_bytes = len(result.stdout.encode("utf-8"))

            summary[size_label].append((wall, out_bytes))

            print(
                f"  {size_label:<12} {i + 1:>4}  {fmt_ms(wall)}  {fmt_ms(duration)}  "
                f"{fmt_ms(overhead)}  {fmt_size(out_bytes):>10}"
            )

            if result.exit_code != 0:
                print(f"    [exit_code={result.exit_code}] {result.stderr.strip()}")

    # Per-mode summary
    print(f"\n  {'-' * 80}")
    print(f"  {'Payload':<12} {'Avg Wall':>9}  {'Min Wall':>9}  {'Max Wall':>9}  {'Avg Output':>10}")
    print(f"  {'-' * 80}")
    for size_label, entries in summary.items():
        times = [e[0] for e in entries]
        sizes = [e[1] for e in entries]
        avg = sum(times) / len(times)
        avg_size = sum(sizes) // len(sizes)
        print(
            f"  {size_label:<12} {fmt_ms(avg)}  {fmt_ms(min(times))}  "
            f"{fmt_ms(max(times))}  {fmt_size(avg_size):>10}"
        )

    return summary


def main(pause: float = 0.0):
    api_token = os.getenv("KOYEB_API_TOKEN")
    if not api_token:
        print("Error: KOYEB_API_TOKEN not set")
        return 1

    suffix = "".join(random.choices(string.ascii_lowercase + string.digits, k=8))

    sandbox = None
    try:
        print("Creating sandbox...")
        t0 = time.time()
        sandbox = Sandbox.create(
            image="koyeb/sandbox",
            name=f"bench-exec-{suffix}",
            wait_ready=True,
            api_token=api_token,
        )
        print(f"Sandbox ready in {time.time() - t0:.1f}s")
        if pause > 0:
            print(f"Pause between commands: {pause}s")

        # -- Regular exec (HTTP POST, wait for full response) --
        regular_summary = run_benchmark(
            sandbox,
            "Regular",
            lambda cmd: sandbox.exec(cmd),
            pause=pause,
        )

        # -- Streaming exec (SSE / chunked, with no-op callbacks) --
        streaming_summary = run_benchmark(
            sandbox,
            "Streaming",
            lambda cmd: sandbox.exec(cmd, on_stdout=noop, on_stderr=noop),
            pause=pause,
        )

        # -- Side-by-side comparison (trivial commands) --
        print(f"\n{'=' * 76}")
        print(" Comparison: Regular vs Streaming — trivial commands (avg wall-clock)")
        print(f"{'=' * 76}")
        print(f"  {'Command':<23} {'Regular':>9}  {'Streaming':>9}  {'Delta':>9}")
        print(f"  {'-' * 70}")
        for cmd_label in regular_summary:
            r_avg = sum(regular_summary[cmd_label]) / len(regular_summary[cmd_label])
            s_avg = sum(streaming_summary[cmd_label]) / len(streaming_summary[cmd_label])
            delta = s_avg - r_avg
            sign = "+" if delta >= 0 else ""
            print(
                f"  {cmd_label:<23} {fmt_ms(r_avg)}  {fmt_ms(s_avg)}  {sign}{fmt_ms(delta)}"
            )
        print(f"{'=' * 76}")

        # -- Output retrieval: regular --
        regular_out = run_output_benchmark(
            sandbox,
            "Regular",
            lambda cmd: sandbox.exec(cmd),
            pause=pause,
        )

        # -- Output retrieval: streaming --
        streaming_out = run_output_benchmark(
            sandbox,
            "Streaming",
            lambda cmd: sandbox.exec(cmd, on_stdout=noop, on_stderr=noop),
            pause=pause,
        )

        # -- Side-by-side comparison (output retrieval) --
        print(f"\n{'=' * 86}")
        print(" Comparison: Regular vs Streaming — output retrieval (avg wall-clock)")
        print(f"{'=' * 86}")
        print(f"  {'Payload':<12} {'Regular':>9}  {'Streaming':>9}  {'Delta':>9}  {'Avg Output':>10}")
        print(f"  {'-' * 80}")
        for size_label in regular_out:
            r_times = [e[0] for e in regular_out[size_label]]
            s_times = [e[0] for e in streaming_out[size_label]]
            r_avg = sum(r_times) / len(r_times)
            s_avg = sum(s_times) / len(s_times)
            avg_size = sum(e[1] for e in regular_out[size_label]) // len(regular_out[size_label])
            delta = s_avg - r_avg
            sign = "+" if delta >= 0 else ""
            print(
                f"  {size_label:<12} {fmt_ms(r_avg)}  {fmt_ms(s_avg)}  "
                f"{sign}{fmt_ms(delta)}  {fmt_size(avg_size):>10}"
            )
        print(f"{'=' * 86}")

        return 0
    finally:
        if sandbox:
            print("\nDeleting sandbox...")
            sandbox.delete()
            print("Done.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Benchmark exec latency for trivial tasks (regular vs streaming, output retrieval)"
    )
    parser.add_argument(
        "--pause",
        type=float,
        default=0.0,
        metavar="SECONDS",
        help="Pause between each command execution in seconds (default: 0)",
    )
    args = parser.parse_args()
    sys.exit(main(pause=args.pause))
