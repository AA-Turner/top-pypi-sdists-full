#!/usr/bin/env python3
"""
Snapshot Boot Time Benchmark

Measures how long it takes to boot sandboxes from snapshots with different:
- Snapshot sizes (10MB, 100MB, 1GB, 10GB)
- Snapshot types (FILESYSTEM vs FULL)
- Boot sequences (1st cold boot vs 2nd-5th warm boots)

For FILESYSTEM snapshots: size controlled by creating files
For FULL snapshots: size controlled by Redis memory usage

All tests use instance_type=xlarge
"""

import argparse
import csv
import os
import random
import string
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

from koyeb import Sandbox
from koyeb.sandbox import Snapshot, SnapshotType


@dataclass
class BootTiming:
    """Record of a single boot timing measurement."""
    snapshot_type: str
    snapshot_size_target: str
    snapshot_actual_size: Optional[int]
    boot_number: int
    boot_time_seconds: float
    sandbox_id: str
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class BenchmarkResult:
    """Aggregated results for a configuration."""
    snapshot_type: str
    snapshot_size_target: str
    snapshot_actual_size: Optional[int]
    boot_times: List[float] = field(default_factory=list)
    
    @property
    def mean_boot_time(self) -> float:
        return sum(self.boot_times) / len(self.boot_times) if self.boot_times else 0
    
    @property
    def min_boot_time(self) -> float:
        return min(self.boot_times) if self.boot_times else 0
    
    @property
    def max_boot_time(self) -> float:
        return max(self.boot_times) if self.boot_times else 0
    
    @property
    def first_boot_time(self) -> float:
        return self.boot_times[0] if self.boot_times else 0
    
    @property
    def warm_boot_times(self) -> List[float]:
        return self.boot_times[1:] if len(self.boot_times) > 1 else []
    
    @property
    def mean_warm_boot_time(self) -> float:
        warm = self.warm_boot_times
        return sum(warm) / len(warm) if warm else 0


class BenchmarkError(Exception):
    """Raised when benchmark encounters an error."""
    pass


def create_file_of_size(sandbox: Sandbox, path: str, size_mb: int) -> None:
    """Create a file of specific size in the sandbox."""
    # Use truncate if available (instant, doesn't write data)
    cmd = f"truncate -s {size_mb}M {path} 2>/dev/null"
    result = sandbox.exec(cmd, timeout=30)
    if result.success:
        return
    
    # Fallback to dd (slower, writes actual data)
    cmd = f"dd if=/dev/zero of={path} bs=1M count={size_mb} 2>/dev/null"
    result = sandbox.exec(cmd, timeout=600)
    if not result.success:
        # Fallback to python method if dd fails
        create_file_python(sandbox, path, size_mb)


def create_file_python(sandbox: Sandbox, path: str, size_mb: int) -> None:
    """Create a file of specific size using Python."""
    # Write in chunks to avoid memory issues on client side
    chunk_size_mb = 100
    chunks = size_mb // chunk_size_mb
    remainder = size_mb % chunk_size_mb
    
    # Write the file in chunks
    for i in range(chunks):
        cmd = f"python3 -c \"with open('{path}', 'ab') as f: f.write(b'x' * ({chunk_size_mb} * 1024 * 1024))\""
        result = sandbox.exec(cmd, timeout=300)
        if not result.success:
            raise BenchmarkError(f"Failed to write chunk {i}: {result.stderr}")
    
    if remainder > 0:
        cmd = f"python3 -c \"with open('{path}', 'ab') as f: f.write(b'x' * ({remainder} * 1024 * 1024))\""
        result = sandbox.exec(cmd, timeout=300)
        if not result.success:
            raise BenchmarkError(f"Failed to write remainder: {result.stderr}")


def setup_redis_with_data(sandbox: Sandbox, target_size_mb: int) -> None:
    """
    Install and start Redis, then populate with data to reach target memory size.
    
    Args:
        sandbox: The sandbox to set up
        target_size_mb: Target Redis memory usage in MB
    """
    print("    → Installing Redis and python redis client...")
    # Try alpine first (if using alpine-based image)
    result = sandbox.exec("apk add --no-cache redis python3 py3-redis 2>/dev/null || apt-get update && apt-get install -y redis-server python3-pip && pip3 install redis", timeout=600)
    if not result.success:
        raise BenchmarkError(f"Failed to install Redis: {result.stderr}")
    
    print("    → Starting Redis...")
    # Try different start commands
    result = sandbox.exec("redis-server --daemonize yes --bind 127.0.0.1 2>/dev/null || redis-server --daemonize yes 2>/dev/null", timeout=30)
    if not result.success:
        raise BenchmarkError(f"Failed to start Redis: {result.stderr}")
    
    # Wait for Redis to be ready
    print("    → Waiting for Redis to be ready...")
    for _ in range(30):
        result = sandbox.exec("redis-cli ping")
        if result.stdout.strip() == "PONG":
            break
        time.sleep(1)
    else:
        raise BenchmarkError("Redis did not become ready")
    
    # Calculate number of keys needed
    # Each key-value pair: key (e.g., "key_12345") + value (1KB) ≈ 1KB per entry
    # But Redis has overhead, so we need more
    # Empirically, ~1.5KB per entry in Redis memory
    num_keys = int(target_size_mb * 1024 / 1.5)
    
    print(f"    → Loading ~{num_keys:,} keys ({target_size_mb}MB target)...")
    
    # Load data in batches to avoid timeout
    batch_size = 10000
    for batch_start in range(0, num_keys, batch_size):
        batch_end = min(batch_start + batch_size, num_keys)
        batch_count = batch_end - batch_start
        # Use a separate Python script to avoid f-string indentation issues
        # Pass the count as a hardcoded value
        script_content = f"""
import redis
r = redis.Redis(decode_responses=True)
for i in range({batch_start}, {batch_end}):
    r.set(f'bench_key_{{i}}', 'x' * 1024)
print(f'Loaded {batch_count} keys', flush=True)
"""
        # Write script to temp file and execute
        script_path = "/tmp/load_redis.py"
        sandbox.filesystem.write_file(script_path, script_content.strip())
        result = sandbox.exec(f"python3 {script_path}", timeout=300)
        if not result.success:
            raise BenchmarkError(f"Failed to load Redis batch {batch_start}-{batch_end}: {result.stderr}")
        # Clean up script file
        sandbox.exec(f"rm -f {script_path}")
    
    # Verify memory usage
    result = sandbox.exec("redis-cli info memory | grep used_memory_human")
    print(f"    → Redis memory usage: {result.stdout.strip()}")


def create_filesystem_snapshot(sandbox: Sandbox, size_mb: int, suffix: str) -> Snapshot:
    """
    Create a FILESYSTEM snapshot with controlled size.
    
    Args:
        sandbox: Builder sandbox
        size_mb: Target size in MB
        suffix: Unique suffix for naming
        
    Returns:
        The created snapshot
    """
    print(f"    → Creating /data directory...")
    sandbox.exec("mkdir -p /data")
    
    print(f"    → Creating {size_mb}MB of filesystem data...")
    create_file_of_size(sandbox, "/data/snapshot_data.bin", size_mb)
    
    print(f"    → Creating FILESYSTEM snapshot...")
    snapshot = sandbox.snapshot(
        name=f"bench-filesystem-{size_mb}mb-{suffix}".lower(),
        snapshot_type=SnapshotType.FILESYSTEM,
        wait_available=True,
        timeout=1800,  # 30 minutes for large snapshots
    )
    
    return snapshot


def create_full_snapshot(sandbox: Sandbox, target_size_mb: int, suffix: str) -> Snapshot:
    """
    Create a FULL snapshot with Redis memory usage.
    
    Args:
        sandbox: Builder sandbox
        target_size_mb: Target Redis memory size in MB
        suffix: Unique suffix for naming
        
    Returns:
        The created snapshot
    """
    print(f"    → Setting up Redis with ~{target_size_mb}MB data...")
    setup_redis_with_data(sandbox, target_size_mb)
    
    print(f"    → Creating FULL snapshot...")
    snapshot = sandbox.snapshot(
        name=f"bench-full-{target_size_mb}mb-{suffix}".lower(),
        snapshot_type=SnapshotType.FULL,
        wait_available=True,
        timeout=1800,
    )
    
    return snapshot


def benchmark_boot_from_snapshot(
    snapshot: Snapshot,
    snapshot_type: str,
    snapshot_size_target: str,
    num_boots: int = 5,
) -> BenchmarkResult:
    """
    Benchmark boot times from a snapshot by spawning multiple sandboxes.
    
    Args:
        snapshot: The snapshot to boot from
        snapshot_type: 'FILESYSTEM' or 'FULL'
        snapshot_size_target: Human-readable size target (e.g., '1GB')
        num_boots: Number of sandboxes to spawn and time
        
    Returns:
        BenchmarkResult with all boot times
    """
    result = BenchmarkResult(
        snapshot_type=snapshot_type,
        snapshot_size_target=snapshot_size_target,
        snapshot_actual_size=snapshot.size,
    )
    
    api_token = snapshot.api_token
    host = snapshot.host
    
    for boot_num in range(1, num_boots + 1):
        boot_start = time.time()
        
        try:
            print(f"    → Boot #{boot_num} from snapshot {snapshot.name}...")
            
            # Generate a simple, valid sandbox name (lowercase, alphanumeric, hyphens)
            import re
            # Remove any non-alphanumeric characters from snapshot_size_target and convert to lowercase
            size_safe = re.sub(r'[^a-zA-Z0-9]', '', snapshot_size_target).lower()
            boot_name = f"bench-{snapshot_type.lower()}-{size_safe}-{boot_num}-{random_str(4)}"
            
            sbx = Sandbox.create(
                name=boot_name,
                snapshot=snapshot,
                instance_type="xlarge",
                wait_ready=True,
                timeout=1200,  # 20 minutes timeout for boot
                api_token=api_token,
                host=host,
            )
            
            boot_time = time.time() - boot_start
            result.boot_times.append(boot_time)
            
            print(f"    → Boot #{boot_num} completed in {boot_time:.1f}s")
            
            # Clean up the spawned sandbox immediately
            sbx.delete()
            
        except Exception as e:
            print(f"    → Boot #{boot_num} FAILED: {e}")
            # Still record the time (or timeout)
            boot_time = time.time() - boot_start
            result.boot_times.append(boot_time)
            raise
    
    return result


def random_str(length: int) -> str:
    """Generate a random lowercase alphanumeric string."""
    return "".join(random.choices(string.ascii_lowercase + string.digits, k=length)).lower()


def write_csv_results(results: List[BootTiming], filename: str) -> None:
    """Write benchmark results to CSV file."""
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            'snapshot_type',
            'snapshot_size_target',
            'snapshot_actual_size_bytes',
            'boot_number',
            'boot_time_seconds',
            'sandbox_id',
            'timestamp',
        ])
        
        for timing in results:
            writer.writerow([
                timing.snapshot_type,
                timing.snapshot_size_target,
                timing.snapshot_actual_size if timing.snapshot_actual_size else '',
                timing.boot_number,
                f"{timing.boot_time_seconds:.3f}",
                timing.sandbox_id,
                timing.timestamp.isoformat(),
            ])
    
    print(f"\n✓ Results written to {filename}")


def print_summary(results: List[BenchmarkResult]) -> None:
    """Print a human-readable summary of benchmark results."""
    print("\n" + "="*80)
    print(" SNAPSHOT BOOT BENCHMARK - SUMMARY")
    print("="*80)
    
    # Group by configuration
    for result in results:
        print(f"\n[{result.snapshot_type} | Target: {result.snapshot_size_target}]")
        print(f"  Actual size: {result.snapshot_actual_size / (1024*1024):.0f}MB" if result.snapshot_actual_size else "  Actual size: N/A")
        print(f"  Cold boot (1st):  {result.first_boot_time:.1f}s")
        if result.warm_boot_times:
            print(f"  Warm boots (2-5): {result.mean_warm_boot_time:.1f}s avg")
            print(f"  Min/Max:          {result.min_boot_time:.1f}s / {result.max_boot_time:.1f}s")
        print(f"  All boots:        {result.mean_boot_time:.1f}s avg")
    
    print("\n" + "="*80)


def run_filesystem_benchmarks(
    api_token: str,
    sizes_mb: List[int],
    num_boots: int,
    results: List[BootTiming],
) -> List[BenchmarkResult]:
    """Run FILESYSTEM snapshot benchmarks for all sizes."""
    suffix = random_str(8)
    benchmark_results = []
    
    for size_mb in sizes_mb:
        print(f"\n{'='*60}")
        print(f" FILESYSTEM SNAPSHOT: {size_mb}MB")
        print(f"{'='*60}")
        
        builder = None
        snapshot = None
        
        try:
            # Create builder sandbox
            print("  → Creating builder sandbox...")
            builder = Sandbox.create(
                name=f"bench-builder-fs-{size_mb}mb-{suffix}".lower(),
                instance_type="xlarge",
                wait_ready=True,
                timeout=600,
                api_token=api_token,
            )
            print(f"  ✓ Builder created: {builder.name}")
            
            # Create filesystem data and snapshot
            snapshot = create_filesystem_snapshot(builder, size_mb, suffix)
            print(f"  ✓ Snapshot created: {snapshot.name} (ID: {snapshot.id})")
            print(f"  ✓ Snapshot size: {snapshot.size / (1024*1024):.0f}MB" if snapshot.size else "  ✓ Snapshot size: N/A")
            
            # Benchmark boots
            bench_result = benchmark_boot_from_snapshot(
                snapshot, "FILESYSTEM", f"{size_mb}MB", num_boots
            )
            benchmark_results.append(bench_result)
            
            # Record individual timings
            for i, boot_time in enumerate(bench_result.boot_times):
                results.append(BootTiming(
                    snapshot_type="FILESYSTEM",
                    snapshot_size_target=f"{size_mb}MB",
                    snapshot_actual_size=snapshot.size,
                    boot_number=i + 1,
                    boot_time_seconds=boot_time,
                    sandbox_id=builder.sandbox_id,
                ))
            
        finally:
            print("  → Cleaning up...")
            if snapshot:
                try:
                    snapshot.delete()
                except Exception as e:
                    print(f"  ! Failed to delete snapshot: {e}")
            if builder:
                try:
                    builder.delete()
                except Exception as e:
                    print(f"  ! Failed to delete builder: {e}")
    
    return benchmark_results


def run_full_benchmarks(
    api_token: str,
    sizes_mb: List[int],
    num_boots: int,
    results: List[BootTiming],
) -> List[BenchmarkResult]:
    """Run FULL snapshot benchmarks for all sizes."""
    suffix = random_str(8)
    benchmark_results = []
    
    for size_mb in sizes_mb:
        print(f"\n{'='*60}")
        print(f" FULL SNAPSHOT: {size_mb}MB (Redis)")
        print(f"{'='*60}")
        
        builder = None
        snapshot = None
        
        try:
            # Create builder sandbox
            print("  → Creating builder sandbox...")
            builder = Sandbox.create(
                name=f"bench-builder-full-{size_mb}mb-{suffix}".lower(),
                image="koyeb/sandbox",  # Standard sandbox image
                instance_type="xlarge",
                wait_ready=True,
                timeout=600,
                api_token=api_token,
            )
            print(f"  ✓ Builder created: {builder.name}")
            
            # Setup Redis and create snapshot
            snapshot = create_full_snapshot(builder, size_mb, suffix)
            print(f"  ✓ Snapshot created: {snapshot.name} (ID: {snapshot.id})")
            print(f"  ✓ Snapshot size: {snapshot.size / (1024*1024):.0f}MB" if snapshot.size else "  ✓ Snapshot size: N/A")
            
            # Benchmark boots
            bench_result = benchmark_boot_from_snapshot(
                snapshot, "FULL", f"{size_mb}MB", num_boots
            )
            benchmark_results.append(bench_result)
            
            # Record individual timings
            for i, boot_time in enumerate(bench_result.boot_times):
                results.append(BootTiming(
                    snapshot_type="FULL",
                    snapshot_size_target=f"{size_mb}MB",
                    snapshot_actual_size=snapshot.size,
                    boot_number=i + 1,
                    boot_time_seconds=boot_time,
                    sandbox_id=builder.sandbox_id,
                ))
            
        finally:
            print("  → Cleaning up...")
            if snapshot:
                try:
                    snapshot.delete()
                except Exception as e:
                    print(f"  ! Failed to delete snapshot: {e}")
            if builder:
                try:
                    builder.delete()
                except Exception as e:
                    print(f"  ! Failed to delete builder: {e}")
    
    return benchmark_results


def main():
    parser = argparse.ArgumentParser(
        description="Benchmark snapshot boot times"
    )
    parser.add_argument(
        "--fs-sizes",
        default="10,100,1000",
        help="Comma-separated filesystem snapshot sizes in MB (default: 10,100,1000)",
    )
    parser.add_argument(
        "--full-sizes",
        default="10,100,1000",
        help="Comma-separated full snapshot Redis sizes in MB (default: 10,100,1000)",
    )
    parser.add_argument(
        "--boots",
        type=int,
        default=5,
        help="Number of boots per snapshot (default: 5)",
    )
    parser.add_argument(
        "--csv",
        default="snapshot_boot_benchmark.csv",
        help="CSV output filename (default: snapshot_boot_benchmark.csv)",
    )
    parser.add_argument(
        "--skip-full",
        action="store_true",
        help="Skip FULL snapshot benchmarks",
    )
    parser.add_argument(
        "--skip-fs",
        action="store_true",
        help="Skip FILESYSTEM snapshot benchmarks",
    )
    
    args = parser.parse_args()
    
    # Parse sizes
    fs_sizes = [int(x.strip()) for x in args.fs_sizes.split(',')]
    full_sizes = [int(x.strip()) for x in args.full_sizes.split(',')]
    
    api_token = os.getenv("KOYEB_API_TOKEN")
    if not api_token:
        print("Error: KOYEB_API_TOKEN environment variable is required")
        return 1
    
    print("Snapshot Boot Time Benchmark")
    print("="*60)
    print(f"Configuration:")
    print(f"  Filesystem sizes: {fs_sizes}")
    print(f"  Full snapshot sizes: {full_sizes}")
    print(f"  Boots per snapshot: {args.boots}")
    print(f"  Instance type: xlarge")
    print(f"  Output: {args.csv}")
    
    all_timings: List[BootTiming] = []
    all_results: List[BenchmarkResult] = []
    
    try:
        # Run FILESYSTEM benchmarks
        if not args.skip_fs:
            print("\n" + "="*60)
            print(" RUNNING FILESYSTEM SNAPSHOT BENCHMARKS")
            print("="*60)
            fs_results = run_filesystem_benchmarks(
                api_token, fs_sizes, args.boots, all_timings
            )
            all_results.extend(fs_results)
        
        # Run FULL benchmarks
        if not args.skip_full:
            print("\n" + "="*60)
            print(" RUNNING FULL SNAPSHOT BENCHMARKS")
            print("="*60)
            full_results = run_full_benchmarks(
                api_token, full_sizes, args.boots, all_timings
            )
            all_results.extend(full_results)
        
        # Write results
        write_csv_results(all_timings, args.csv)
        print_summary(all_results)
        
        print("\n✓ Benchmark completed successfully!")
        return 0
        
    except Exception as e:
        print(f"\n✗ Benchmark failed: {e}")
        import traceback
        traceback.print_exc()
        
        # Still try to write partial results
        if all_timings:
            partial_csv = args.csv.replace('.csv', '_partial.csv')
            write_csv_results(all_timings, partial_csv)
            print(f"\n✓ Partial results written to {partial_csv}")
        
        return 1


if __name__ == "__main__":
    sys.exit(main())
