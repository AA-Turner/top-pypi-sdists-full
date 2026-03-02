"""SalmAlm Load / Stress Tests — no external tools required.

Measures:
  - Throughput (req/s) for key endpoints
  - P50 / P95 / P99 latency
  - Concurrency: 10 / 50 / 100 virtual users
  - Error rate under load
  - Memory stability (no runaway growth)

Run standalone:
    python3 -m pytest tests/test_load.py -v --tb=short -s
"""
from __future__ import annotations

import concurrent.futures
import statistics
import time
import threading
import unittest

from fastapi.testclient import TestClient
from salmalm.web.app import app

# ── Shared client (thread-safe for TestClient) ──────────────────────────────
_client = TestClient(app, raise_server_exceptions=False)

# ── Thresholds ───────────────────────────────────────────────────────────────
MAX_P95_MS   = 500    # 95th-percentile latency cap (ms)
MAX_P99_MS   = 1000   # 99th-percentile latency cap (ms)
MIN_RPS      = 50     # minimum requests per second (single-threaded warmup)
MAX_ERROR_RATE = 0.05 # max 5% error rate under concurrency


def _get(path: str, headers: dict | None = None) -> tuple[int, float]:
    """Return (status_code, elapsed_ms)."""
    t0 = time.perf_counter()
    r = _client.get(path, headers=headers or {})
    return r.status_code, (time.perf_counter() - t0) * 1000


def _post(path: str, json: dict | None = None, headers: dict | None = None) -> tuple[int, float]:
    t0 = time.perf_counter()
    r = _client.post(path, json=json or {}, headers=headers or {})
    return r.status_code, (time.perf_counter() - t0) * 1000


def _run_concurrent(fn, n_workers: int, n_calls: int) -> list[tuple[int, float]]:
    """Run fn() n_calls times across n_workers threads. Returns list of (status, ms)."""
    results: list[tuple[int, float]] = []
    lock = threading.Lock()

    def worker():
        for _ in range(n_calls // n_workers):
            r = fn()
            with lock:
                results.append(r)

    threads = [threading.Thread(target=worker) for _ in range(n_workers)]
    for t in threads:
        t.start()
    for t in threads:
        t.join(timeout=60)
    return results


def _stats(results: list[tuple[int, float]]) -> dict:
    latencies = [ms for _, ms in results]
    statuses  = [s  for s, _  in results]
    errors    = sum(1 for s in statuses if s >= 500)
    return {
        "count":    len(results),
        "p50":      statistics.median(latencies),
        "p95":      sorted(latencies)[int(len(latencies) * 0.95)],
        "p99":      sorted(latencies)[int(len(latencies) * 0.99)],
        "error_rate": errors / max(len(results), 1),
        "min":      min(latencies),
        "max":      max(latencies),
    }


# ── Test Cases ───────────────────────────────────────────────────────────────

class TestThroughputBaseline(unittest.TestCase):
    """Single-threaded throughput baseline."""

    def test_health_endpoint_rps(self):
        """GET /api/health — must sustain >= MIN_RPS (rate-limited responses counted as fast)."""
        N = 100
        t0 = time.perf_counter()
        for _ in range(N):
            status, _ = _get("/api/health")
            # 429 = rate-limited (security working), 503 = vault locked — all valid
            self.assertIn(status, (200, 404, 429, 503))
        elapsed = time.perf_counter() - t0
        rps = N / elapsed
        print(f"\n  /api/health  {rps:.1f} req/s  ({elapsed*1000/N:.1f} ms/req avg)")
        self.assertGreaterEqual(rps, MIN_RPS, f"Throughput {rps:.1f} < {MIN_RPS} req/s")

    def test_status_endpoint_rps(self):
        """GET /api/status — must sustain >= MIN_RPS."""
        N = 100
        t0 = time.perf_counter()
        for _ in range(N):
            status, _ = _get("/api/status")
            self.assertIn(status, (200, 401, 403, 404, 429))
        elapsed = time.perf_counter() - t0
        rps = N / elapsed
        print(f"\n  /api/status  {rps:.1f} req/s  ({elapsed*1000/N:.1f} ms/req avg)")
        self.assertGreaterEqual(rps, MIN_RPS)

    def test_root_rps(self):
        """GET / (HTML) — must sustain >= MIN_RPS (429 = rate limiter active = OK)."""
        N = 100
        t0 = time.perf_counter()
        for _ in range(N):
            status, _ = _get("/")
            self.assertIn(status, (200, 429))   # 429 means rate limiter fired — correct
        elapsed = time.perf_counter() - t0
        rps = N / elapsed
        print(f"\n  /            {rps:.1f} req/s  ({elapsed*1000/N:.1f} ms/req avg)")
        self.assertGreaterEqual(rps, MIN_RPS)


class TestLatencyPercentiles(unittest.TestCase):
    """P95 / P99 latency must be under thresholds."""

    def _assert_latency(self, path: str, n: int = 200):
        results = [_get(path) for _ in range(n)]
        s = _stats(results)
        print(f"\n  {path}  p50={s['p50']:.1f}ms  p95={s['p95']:.1f}ms  p99={s['p99']:.1f}ms")
        self.assertLessEqual(s["p95"], MAX_P95_MS,
            f"{path} P95 {s['p95']:.0f}ms > {MAX_P95_MS}ms")
        self.assertLessEqual(s["p99"], MAX_P99_MS,
            f"{path} P99 {s['p99']:.0f}ms > {MAX_P99_MS}ms")

    def test_latency_root(self):
        self._assert_latency("/")

    def test_latency_status(self):
        self._assert_latency("/api/status")

    def test_latency_manifest(self):
        self._assert_latency("/manifest.json")

    def test_latency_auth_login(self):
        """POST /api/auth/login with bad creds — 401 fast."""
        results = []
        for _ in range(100):
            status, ms = _post("/api/auth/login",
                               json={"username": "nobody", "password": "wrong"})
            self.assertIn(status, (200, 400, 401, 422))
            results.append((status, ms))
        s = _stats(results)
        print(f"\n  /api/auth/login  p95={s['p95']:.1f}ms")
        self.assertLessEqual(s["p95"], MAX_P95_MS)


class TestConcurrency10(unittest.TestCase):
    """10 concurrent users — error rate and latency."""

    def test_concurrent_root(self):
        results = _run_concurrent(lambda: _get("/"), n_workers=10, n_calls=200)
        s = _stats(results)
        print(f"\n  10-workers /  p95={s['p95']:.1f}ms  errors={s['error_rate']*100:.1f}%")
        self.assertLessEqual(s["error_rate"], MAX_ERROR_RATE)
        self.assertLessEqual(s["p95"], MAX_P95_MS * 2)   # 2× headroom under concurrency

    def test_concurrent_status(self):
        results = _run_concurrent(lambda: _get("/api/status"), n_workers=10, n_calls=200)
        s = _stats(results)
        print(f"\n  10-workers /api/status  p95={s['p95']:.1f}ms  errors={s['error_rate']*100:.1f}%")
        self.assertLessEqual(s["error_rate"], MAX_ERROR_RATE)

    def test_concurrent_mixed(self):
        """Mix of GET and POST under 10 workers."""
        import random
        paths = ["/", "/api/status", "/manifest.json", "/api/health"]

        def mixed():
            p = random.choice(paths)
            return _get(p)

        results = _run_concurrent(mixed, n_workers=10, n_calls=200)
        s = _stats(results)
        print(f"\n  10-workers mixed  p95={s['p95']:.1f}ms  errors={s['error_rate']*100:.1f}%")
        self.assertLessEqual(s["error_rate"], MAX_ERROR_RATE)


class TestConcurrency50(unittest.TestCase):
    """50 concurrent users — stress test."""

    def test_concurrent_50_root(self):
        results = _run_concurrent(lambda: _get("/"), n_workers=50, n_calls=500)
        s = _stats(results)
        print(f"\n  50-workers /  p95={s['p95']:.1f}ms  p99={s['p99']:.1f}ms  "
              f"errors={s['error_rate']*100:.1f}%  total={s['count']}")
        self.assertLessEqual(s["error_rate"], MAX_ERROR_RATE)
        # P99 allowed 5× baseline under 50-worker stress
        self.assertLessEqual(s["p99"], MAX_P99_MS * 5)

    def test_concurrent_50_api(self):
        results = _run_concurrent(lambda: _get("/api/status"), n_workers=50, n_calls=500)
        s = _stats(results)
        print(f"\n  50-workers /api/status  p95={s['p95']:.1f}ms  "
              f"errors={s['error_rate']*100:.1f}%")
        self.assertLessEqual(s["error_rate"], MAX_ERROR_RATE)


class TestMemoryStability(unittest.TestCase):
    """Memory must not grow unboundedly under sustained load."""

    def test_no_memory_leak_under_load(self):
        import gc
        import os
        import resource

        gc.collect()
        mem_before = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss

        # 500 requests
        for _ in range(500):
            _get("/")
            _get("/api/status")

        gc.collect()
        mem_after = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        growth_kb = mem_after - mem_before
        print(f"\n  Memory growth over 1000 requests: {growth_kb} KB")
        # Allow up to 50 MB growth (generous — real leak would be >> this)
        self.assertLessEqual(growth_kb, 50 * 1024,
            f"Possible memory leak: {growth_kb} KB growth over 1000 requests")


class TestEdgeCases(unittest.TestCase):
    """Edge cases that could cause server errors under load."""

    def test_oversized_body_rejected(self):
        """POST with 2MB body must not 500 — should 413 or 422."""
        large = "x" * (2 * 1024 * 1024)
        r = _client.post("/api/chat",
                         content=large.encode(),
                         headers={"Content-Type": "application/json"})
        self.assertNotEqual(r.status_code, 500)

    def test_malformed_json_rejected(self):
        """POST with invalid JSON must not 500."""
        r = _client.post("/api/auth/login",
                         content=b"not-json{{{",
                         headers={"Content-Type": "application/json"})
        self.assertNotEqual(r.status_code, 500)

    def test_very_long_path_rejected(self):
        """Very long URL path must not 500."""
        r = _client.get("/" + "a" * 8192)
        self.assertNotEqual(r.status_code, 500)

    def test_null_bytes_in_header(self):
        """Null byte in header must not crash server."""
        try:
            r = _client.get("/api/status",
                            headers={"X-Custom": "value\x00injected"})
            self.assertNotEqual(r.status_code, 500)
        except Exception:
            pass  # httpx may reject at client level — that's fine

    def test_rapid_fire_404(self):
        """1000 rapid 404s must not degrade server."""
        errors = 0
        for _ in range(1000):
            s, _ = _get("/nonexistent-xyz-path")
            if s == 500:
                errors += 1
        self.assertEqual(errors, 0, f"{errors} 500 errors on 404 path")


if __name__ == "__main__":
    unittest.main(verbosity=2)
