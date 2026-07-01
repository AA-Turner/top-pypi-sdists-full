import asyncio
import contextlib
import statistics
import time
from typing import AsyncIterator, Iterator, Literal

from wireup import Injected, create_async_container
from wireup import service as injectable
from wireup._decorators import inject_from_container


class H: ...


async def make_h() -> AsyncIterator[H]:
    yield H()


class G:
    def __init__(self, h: H) -> None:
        self.h = h


class F:
    def __init__(self, g: G):
        self.g = g


class E:
    def __init__(self, f: F):
        self.f = f


class D:
    def __init__(self, e: E, g: G):
        self.e = e


class C:
    def __init__(self, d: D, g: G):
        self.d = d


class B:
    def __init__(self, c: C):
        self.c = c


class A:
    def __init__(self, b: B):
        self.b = b


def empty_middleware(
    scoped_container,  # noqa: ARG001
    *args,  # noqa: ARG001
    **kwargs,  # noqa: ARG001
) -> Iterator[None]:
    try:
        yield
    finally:
        pass


async def run_single_benchmark(
    test_name: str,
    test_func,
    iterations: int,
    warmup_iterations: int = 1000,
    num_runs: int = 5,
) -> dict:
    """Run a single benchmark with warmup and multiple runs."""
    # Warmup
    for _ in range(warmup_iterations):
        await test_func()

    # Multiple runs to get stable results
    times = []
    for _ in range(num_runs):
        start = time.perf_counter()
        for _ in range(iterations):
            await test_func()
        end = time.perf_counter()
        times.append(end - start)

    # Calculate statistics
    median_time = statistics.median(times)
    mean_time = statistics.mean(times)
    stdev_time = statistics.stdev(times) if len(times) > 1 else 0

    ops_per_sec = iterations / median_time
    latency_ns = (median_time / iterations) * 1_000_000_000

    return {
        "name": test_name,
        "ops_per_sec": ops_per_sec,
        "latency_ns": latency_ns,
        "median_time": median_time,
        "mean_time": mean_time,
        "stdev_time": stdev_time,
        "num_runs": num_runs,
    }


async def run_bench():
    classes = [make_h, G, F, E, D, C, B, A]
    iterations = 20_000
    warmup = 2_000
    num_runs = 10  # More runs for stable results

    lifetimes: list[Literal["singleton", "scoped"]] = ["singleton", "scoped"]
    middleware_options = [None, empty_middleware]

    results = []

    print("=" * 70)
    print("Wireup Microbenchmark - Dependency Chain (8 services)")
    print("=" * 70)
    print(f"Iterations per run: {iterations:,}")
    print(f"Warmup iterations: {warmup:,}")
    print(f"Number of runs: {num_runs}")
    print(f"Using median of {num_runs} runs for results")
    print("=" * 70)

    for lifetime in lifetimes:
        for middleware in middleware_options:
            middleware_name = "with_middleware" if middleware else "no_middleware"

            print(f"\n{'=' * 70}")
            print(f"LIFETIME: {lifetime.upper()} | {middleware_name.replace('_', ' ').upper()}")
            print("=" * 70)

            # Test 1: Raw container.get
            print("\n[1/2] Benchmarking: Raw await container.get()")
            container1 = create_async_container(services=[injectable(c, lifetime=lifetime) for c in classes])

            if lifetime == "scoped":

                async def raw_test():
                    async with container1.enter_scope() as scope:
                        await scope.get(A)
            else:
                # Initialize singleton once before benchmark
                await container1.get(A)

                async def raw_test():
                    await container1.get(A)

            raw_result = await run_single_benchmark(
                f"raw_{lifetime}_{middleware_name}",
                raw_test,
                iterations,
                warmup,
                num_runs,
            )

            print(f"  Ops/sec:  {raw_result['ops_per_sec']:>15,.0f}")
            print(f"  Latency:  {raw_result['latency_ns']:>15,.0f} ns/op")
            print(f"  Stdev:    {raw_result['stdev_time'] * 1000:>15,.2f} ms")

            # Test 2: @inject_from_container decorator
            print("\n[2/2] Benchmarking: @inject_from_container decorator")
            container2 = create_async_container(services=[injectable(c, lifetime=lifetime) for c in classes])

            @inject_from_container(container=container2, _middleware=middleware)
            async def target(a: Injected[A]) -> A:
                return a

            # Warmup for decorator too
            for _ in range(warmup):
                await target()

            decorator_result = await run_single_benchmark(
                f"decorator_{lifetime}_{middleware_name}",
                target,
                iterations,
                warmup_iterations=0,  # Already warmed up
                num_runs=num_runs,
            )

            print(f"  Ops/sec:  {decorator_result['ops_per_sec']:>15,.0f}")
            print(f"  Latency:  {decorator_result['latency_ns']:>15,.0f} ns/op")
            print(f"  Stdev:    {decorator_result['stdev_time'] * 1000:>15,.2f} ms")

            # Calculate overhead
            overhead_pct = (raw_result["ops_per_sec"] / decorator_result["ops_per_sec"] - 1) * 100
            overhead_ns = decorator_result["latency_ns"] - raw_result["latency_ns"]

            print(f"\n  Decorator overhead: {overhead_pct:>6.1f}% ({overhead_ns:,.0f} ns)")

            results.append(
                {
                    "lifetime": lifetime,
                    "middleware": middleware_name,
                    "raw": raw_result,
                    "decorator": decorator_result,
                    "overhead_pct": overhead_pct,
                    "overhead_ns": overhead_ns,
                }
            )

    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)

    # Group by lifetime
    for lifetime in lifetimes:
        print(f"\n{lifetime.upper()}:")
        print("-" * 70)

        lifetime_results = [r for r in results if r["lifetime"] == lifetime]

        for result in lifetime_results:
            mw_label = "With Middleware" if "with" in result["middleware"] else "No Middleware"
            print(f"\n  {mw_label}:")
            print(f"    Raw container.get:      {result['raw']['ops_per_sec']:>12,.0f} ops/sec")
            print(f"    @inject_from_container: {result['decorator']['ops_per_sec']:>12,.0f} ops/sec")
            print(f"    Overhead:               {result['overhead_pct']:>12.1f}% (+{result['overhead_ns']:,.0f} ns)")

    # Best case scenario
    print("\n" + "=" * 70)
    print("BEST CASE (Singleton, No Middleware):")
    print("=" * 70)
    best = next(r for r in results if r["lifetime"] == "singleton" and r["middleware"] == "no_middleware")
    print(f"  Decorator latency: {best['decorator']['latency_ns']:,.0f} ns per injection")
    print(f"  Overhead:          {best['overhead_ns']:,.0f} ns vs raw container.get()")
    print(f"  Throughput:        {best['decorator']['ops_per_sec']:,.0f} injections/sec")


if __name__ == "__main__":
    asyncio.run(run_bench())
