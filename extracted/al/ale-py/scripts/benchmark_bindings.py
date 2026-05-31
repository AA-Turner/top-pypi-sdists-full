#!/usr/bin/env python3
"""
Benchmark script for comparing ALE Python binding performance.

Usage:
  python benchmark_bindings.py

Tests the performance of key ALE operations with the current bindings.
Run this before and after migrating to nanobind to compare performance.
"""

import time
import numpy as np
from pathlib import Path

try:
    from ale_py import ALEInterface, roms
    print("Successfully imported ale_py")
except ImportError as e:
    print(f"Error importing ale_py: {e}")
    print("Make sure ALE is installed: pip install -e .")
    exit(1)


def benchmark_operation(name, func, iterations=1000):
    """Benchmark a single operation"""
    # Warm-up
    for _ in range(10):
        func()

    # Actual benchmark
    start = time.perf_counter()
    for _ in range(iterations):
        func()
    end = time.perf_counter()

    elapsed = (end - start) * 1000  # Convert to ms
    per_op = elapsed / iterations

    return elapsed, per_op


def main():
    print("=" * 60)
    print("ALE Python Bindings Performance Benchmark")
    print("=" * 60)
    print()

    # Initialize ALE
    ale = ALEInterface()

    # Try to load a ROM
    rom_path = None
    rom_files = ['breakout', 'pong', 'space_invaders']

    for rom_name in rom_files:
        try:
            rom_path = getattr(roms, rom_name.capitalize(), None)
            if rom_path and Path(rom_path).exists():
                ale.loadROM(rom_path)
                print(f"Loaded ROM: {rom_name}")
                break
        except Exception as e:
            continue

    if rom_path is None:
        print("Warning: No ROM found, trying default paths...")
        try:
            # Try loading any available ROM
            ale.loadROM("roms/breakout.bin")
        except:
            print("Error: Could not load any ROM. Some benchmarks may fail.")
            print("Please ensure at least one Atari ROM is available.")

    print()

    # Test parameters
    iterations_fast = 10000  # For very fast operations
    iterations_medium = 5000  # For medium operations
    iterations_slow = 1000   # For slower operations

    print("Running benchmarks...")
    print("-" * 60)

    results = []

    # Benchmark 1: Basic method calls
    print("\n1. Basic Method Calls")
    total, per_op = benchmark_operation(
        "lives()",
        lambda: ale.lives(),
        iterations_fast
    )
    results.append(("lives()", per_op))
    print(f"   lives()             : {per_op:.4f} ms/call ({iterations_fast} iterations)")

    total, per_op = benchmark_operation(
        "getFrameNumber()",
        lambda: ale.getFrameNumber(),
        iterations_fast
    )
    results.append(("getFrameNumber()", per_op))
    print(f"   getFrameNumber()    : {per_op:.4f} ms/call ({iterations_fast} iterations)")

    # Benchmark 2: Array operations
    print("\n2. Array Retrieval (Zero-Copy Operations)")

    total, per_op = benchmark_operation(
        "getScreen()",
        lambda: ale.getScreen(),
        iterations_medium
    )
    results.append(("getScreen()", per_op))
    print(f"   getScreen()         : {per_op:.4f} ms/call ({iterations_medium} iterations)")

    total, per_op = benchmark_operation(
        "getScreenRGB()",
        lambda: ale.getScreenRGB(),
        iterations_medium
    )
    results.append(("getScreenRGB()", per_op))
    print(f"   getScreenRGB()      : {per_op:.4f} ms/call ({iterations_medium} iterations)")

    total, per_op = benchmark_operation(
        "getScreenGrayscale()",
        lambda: ale.getScreenGrayscale(),
        iterations_medium
    )
    results.append(("getScreenGrayscale()", per_op))
    print(f"   getScreenGrayscale(): {per_op:.4f} ms/call ({iterations_medium} iterations)")

    total, per_op = benchmark_operation(
        "getRAM()",
        lambda: ale.getRAM(),
        iterations_fast
    )
    results.append(("getRAM()", per_op))
    print(f"   getRAM()            : {per_op:.4f} ms/call ({iterations_fast} iterations)")

    # Benchmark 3: Pre-allocated array operations
    print("\n3. Pre-allocated Array Operations")

    screen_dims = ale.getScreenDims()
    screen_buffer = np.zeros(screen_dims, dtype=np.uint8)
    total, per_op = benchmark_operation(
        "getScreen(buffer)",
        lambda: ale.getScreen(screen_buffer),
        iterations_medium
    )
    results.append(("getScreen(buffer)", per_op))
    print(f"   getScreen(buffer)   : {per_op:.4f} ms/call ({iterations_medium} iterations)")

    rgb_buffer = np.zeros((*screen_dims, 3), dtype=np.uint8)
    total, per_op = benchmark_operation(
        "getScreenRGB(buffer)",
        lambda: ale.getScreenRGB(rgb_buffer),
        iterations_medium
    )
    results.append(("getScreenRGB(buffer)", per_op))
    print(f"   getScreenRGB(buffer): {per_op:.4f} ms/call ({iterations_medium} iterations)")

    # Benchmark 4: Game stepping
    print("\n4. Game Stepping (Most Critical for RL)")

    legal_actions = ale.getLegalActionSet()
    action = legal_actions[0] if legal_actions else 0

    total, per_op = benchmark_operation(
        "act(action)",
        lambda: ale.act(action),
        iterations_slow
    )
    results.append(("act(action)", per_op))
    print(f"   act(action)         : {per_op:.4f} ms/call ({iterations_slow} iterations)")

    # Full step (act + getScreen)
    def full_step():
        ale.act(action)
        return ale.getScreenRGB()

    total, per_op = benchmark_operation(
        "act + getScreenRGB",
        full_step,
        iterations_slow
    )
    results.append(("act + getScreenRGB", per_op))
    print(f"   act + getScreenRGB  : {per_op:.4f} ms/call ({iterations_slow} iterations)")

    # Benchmark 5: State management
    print("\n5. State Management")

    total, per_op = benchmark_operation(
        "cloneState()",
        lambda: ale.cloneState(),
        iterations_medium
    )
    results.append(("cloneState()", per_op))
    print(f"   cloneState()        : {per_op:.4f} ms/call ({iterations_medium} iterations)")

    state = ale.cloneState()
    total, per_op = benchmark_operation(
        "restoreState()",
        lambda: ale.restoreState(state),
        iterations_medium
    )
    results.append(("restoreState()", per_op))
    print(f"   restoreState()      : {per_op:.4f} ms/call ({iterations_medium} iterations)")

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)

    # Categorize results
    fast_ops = [r for r in results if r[1] < 0.01]
    medium_ops = [r for r in results if 0.01 <= r[1] < 0.1]
    slow_ops = [r for r in results if r[1] >= 0.1]

    if fast_ops:
        print(f"\nFast operations (< 0.01 ms):")
        for name, time in sorted(fast_ops, key=lambda x: x[1]):
            print(f"  {name:25s}: {time:.6f} ms")

    if medium_ops:
        print(f"\nMedium operations (0.01-0.1 ms):")
        for name, time in sorted(medium_ops, key=lambda x: x[1]):
            print(f"  {name:25s}: {time:.6f} ms")

    if slow_ops:
        print(f"\nSlow operations (>= 0.1 ms):")
        for name, time in sorted(slow_ops, key=lambda x: x[1]):
            print(f"  {name:25s}: {time:.6f} ms")

    # Overall stats
    total_time = sum(r[1] for r in results)
    avg_time = total_time / len(results)

    print(f"\nAverage operation time: {avg_time:.6f} ms")
    print(f"Fastest operation: {min(results, key=lambda x: x[1])[0]} ({min(results, key=lambda x: x[1])[1]:.6f} ms)")
    print(f"Slowest operation: {max(results, key=lambda x: x[1])[0]} ({max(results, key=lambda x: x[1])[1]:.6f} ms)")

    print("\n" + "=" * 60)
    print("Benchmark complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()