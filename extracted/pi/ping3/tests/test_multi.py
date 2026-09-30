"""
测试 ping3 在并发场景下的正确性。

核心风险：不同线程/进程 ping 同一目标时，ICMP 包可能混淆。
例如：delay 应该 500ms，但因每 100ms 发一个包，第四个线程
可能误收了第一个线程的回复，得到 ~100ms 的错误 delay，
而前三个线程反而 timeout。

macOS 特别注意：
- raw socket 会收到所有 ICMP 包（含其他线程发出的包）
- receive_one_ping 通过 icmp_id + seq 过滤，但 select()
  会被非目标包提前唤醒，可能导致超时判断异常
"""

import sys
import os
import time
import unittest
from unittest.mock import patch
import threading
import multiprocessing

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import ping3  # noqa: linter (pycodestyle) should not lint this line.

DEST_ADDR = "example.com"
UNREACHABLE_IP = "10.255.255.1"


def _ping_in_process(dest_addr, timeout, queue):
    """在子进程中执行 ping，结果通过 Queue 返回。"""
    try:
        result = ping3.ping(dest_addr, timeout=timeout)
        queue.put(("ok", result))
    except Exception as e:
        queue.put(("error", str(e)))


def _ping_in_process_with_timing(dest_addr, timeout, num_pings, queue):
    """在子进程中连续 ping 多次，记录每次的 delay。"""
    delays = []
    for i in range(num_pings):
        try:
            delay = ping3.ping(dest_addr, timeout=timeout)
            delays.append(delay)
        except Exception as e:
            delays.append(("error", str(e)))
    queue.put(("ok", delays))


# ============================================================
# 基础线程并发测试
# ============================================================

class TestThreadingBasic(unittest.TestCase):
    """基础多线程并发 ping 测试。"""

    def test_concurrent_pings_same_dest(self):
        """多个线程同时 ping 同一目标，所有线程都应返回结果。
        如果存在 ICMP 包混淆，部分线程可能 timeout（返回 None）。"""
        results = {}
        lock = threading.Lock()

        def worker(tid):
            delay = ping3.ping(DEST_ADDR, timeout=4)
            with lock:
                results[tid] = delay

        threads = []
        for i in range(4):
            t = threading.Thread(target=worker, args=(i,))
            threads.append(t)
            t.start()
        for t in threads:
            t.join(timeout=20)

        self.assertEqual(len(results), 4, "Not all threads returned results")
        for tid, delay in results.items():
            self.assertIsNotNone(
                delay,
                f"Thread {tid} returned None (timeout) — possible ICMP packet confusion"
            )
            self.assertIsInstance(delay, float)
            self.assertGreater(delay, 0, f"Thread {tid} delay must be positive")

    def test_concurrent_pings_different_hosts(self):
        """多个线程 ping 不同目标，不应互相干扰。"""
        hosts = ["example.com", "localhost", "127.0.0.1"]
        results = {}
        lock = threading.Lock()

        def worker(host):
            delay = ping3.ping(host, timeout=4)
            with lock:
                results[host] = delay

        threads = []
        for host in hosts:
            t = threading.Thread(target=worker, args=(host,))
            threads.append(t)
            t.start()
        for t in threads:
            t.join(timeout=15)

        # localhost 和 127.0.0.1 一定能成功
        for host in ["127.0.0.1", "localhost"]:
            self.assertIn(host, results, f"No result for {host}")
            self.assertIsNotNone(results[host], f"{host} timed out unexpectedly")
            self.assertIsInstance(results[host], float)


# ============================================================
# ICMP 包混淆专项测试
# ============================================================

class TestICMPConfusion(unittest.TestCase):
    """专项测试 ICMP 包混淆问题。

    场景：多个线程同时 ping 同一目标，每个线程的 icmp_id 不同。
    macOS 上 raw socket 收到所有 ICMP 包，receive_one_ping 的
    while 循环需要正确过滤非目标包。如果过滤失败：
    - 某线程可能拿到别人的 reply，算出错误的 delay（偏小）
    - 被"偷走" reply 的线程会 timeout（None）
    """

    def test_no_packet_stealing(self):
        """并发 ping 同一目标，所有线程都应成功，不应有 timeout。
        如果有线程 timeout，说明它的 reply 被其他线程"偷走"了。"""
        num_threads = 6
        results = {}
        lock = threading.Lock()

        def worker(tid):
            delay = ping3.ping(DEST_ADDR, timeout=4)
            with lock:
                results[tid] = delay

        threads = []
        for i in range(num_threads):
            t = threading.Thread(target=worker, args=(i,))
            threads.append(t)
            t.start()
        for t in threads:
            t.join(timeout=25)

        self.assertEqual(len(results), num_threads)
        timeouts = [tid for tid, d in results.items() if d is None]
        self.assertEqual(
            len(timeouts), 0,
            f"Threads {timeouts} timed out — their ICMP replies may have been "
            f"consumed by other threads (ICMP packet confusion)"
        )

    def test_delay_not_suspiciously_small(self):
        """如果一个线程误收了更早发出的包，delay 可能偏小。
        检查 delay 合理性：到 example.com 的正常 delay 通常 > 1ms。
        异常小的 delay（如 0.001s）可能是收到了旧包。"""
        num_threads = 4
        results = {}
        lock = threading.Lock()

        def worker(tid):
            delay = ping3.ping(DEST_ADDR, timeout=4, unit="s")
            with lock:
                results[tid] = delay

        threads = []
        for i in range(num_threads):
            t = threading.Thread(target=worker, args=(i,))
            threads.append(t)
            t.start()
        for t in threads:
            t.join(timeout=20)

        for tid, delay in results.items():
            if delay is not None:
                # 正常网络延迟不应低于 0.1ms（0.0001s）
                # 如果出现这种情况，很可能是收到了错误的包
                self.assertGreater(
                    delay, 0.0001,
                    f"Thread {tid} delay={delay:.6f}s is suspiciously small — "
                    f"may have received a stale/wrong ICMP reply"
                )

    def test_sequential_vs_concurrent_delays(self):
        """对比顺序 ping 和并发 ping 的 delay 分布。
        如果并发时有包混淆，平均 delay 会显著偏离顺序 ping 的结果。"""
        # 先做一次顺序 ping 作为基准
        baseline_delay = ping3.ping(DEST_ADDR, timeout=4, unit="ms")
        if baseline_delay is None:
            self.skipTest("Cannot reach destination, skipping baseline comparison")

        # 并发 ping
        concurrent_delays = []
        lock = threading.Lock()

        def worker():
            delay = ping3.ping(DEST_ADDR, timeout=4, unit="ms")
            with lock:
                concurrent_delays.append(delay)

        threads = []
        for _ in range(4):
            t = threading.Thread(target=worker)
            threads.append(t)
            t.start()
        for t in threads:
            t.join(timeout=20)

        # 所有并发 ping 都应成功
        self.assertEqual(len(concurrent_delays), 4)
        self.assertNotIn(None, concurrent_delays, "Some concurrent pings returned None (timeout)")

        # 并发 delay 不应偏离基准太多（5倍以内是合理的）
        for i, d in enumerate(concurrent_delays):
            self.assertIsNotNone(d, f"Concurrent ping {i} timed out")
            self.assertLess(
                d, baseline_delay * 5,
                f"Concurrent delay {d:.2f}ms is much larger than baseline {baseline_delay:.2f}ms — "
                f"possible packet confusion causing retransmission"
            )

    def test_multi_round_concurrent(self):
        """多轮并发 ping，每轮所有线程 ping 同一目标。
        如果存在包混淆，多轮下来失败率会累积。"""
        num_rounds = 3
        num_threads = 4
        total_pings = num_rounds * num_threads
        timeouts = 0
        anomalies = 0

        for round_idx in range(num_rounds):
            results = {}
            lock = threading.Lock()

            def worker(tid):
                delay = ping3.ping(DEST_ADDR, timeout=4)
                with lock:
                    results[tid] = delay

            threads = []
            for i in range(num_threads):
                t = threading.Thread(target=worker, args=(i,))
                threads.append(t)
                t.start()
            for t in threads:
                t.join(timeout=20)

            for tid, delay in results.items():
                if delay is None:
                    timeouts += 1
                elif isinstance(delay, float) and delay < 0.0001:
                    anomalies += 1

        # 允许偶尔超时（网络波动），但不应太多
        self.assertEqual(
            timeouts, 0,
            f"{timeouts}/{total_pings} pings timed out across {num_rounds} rounds — "
            f"possible systematic ICMP packet confusion"
        )
        self.assertEqual(
            anomalies, 0,
            f"{anomalies}/{total_pings} pings had suspiciously small delays"
        )


# ============================================================
# TTL 相关并发测试
# ============================================================

class TestTTLConcurrent(unittest.TestCase):
    """测试并发场景下 TTL 的行为。"""

    def test_concurrent_different_ttls(self):
        """多个线程使用不同 TTL 并发 ping 同一目标。
        TTL 越小越可能超时，但不应互相干扰。"""
        ttl_range = [1, 2, 5, 10, 20]
        results = {}
        lock = threading.Lock()

        def worker(ttl):
            try:
                delay = ping3.ping(DEST_ADDR, ttl=ttl, timeout=2)
            except Exception as e:
                delay = ("exception", type(e).__name__)
            with lock:
                results[ttl] = delay

        threads = []
        for ttl in ttl_range:
            t = threading.Thread(target=worker, args=(ttl,))
            threads.append(t)
            t.start()
        for t in threads:
            t.join(timeout=20)

        # TTL=1 到远程主机几乎一定超时或触发 TTL expired
        self.assertIn(1, results)
        # TTL=20 大多数情况应能到达
        self.assertIn(20, results)
        delay_20 = results[20]
        if isinstance(delay_20, float):
            self.assertGreater(delay_20, 0, "TTL=20 should get a valid positive delay")

    def test_traceroute_localhost_ttl1(self):
        """ping localhost（127.0.0.1）用 TTL=1，应立即成功（只有一跳）。"""
        delay = ping3.ping("127.0.0.1", ttl=1, timeout=2)
        self.assertIsNotNone(delay, "localhost TTL=1 should not timeout")
        self.assertIsInstance(delay, float)
        self.assertGreater(delay, 0)

    def test_ttl_exception_mode(self):
        """开启 EXCEPTIONS 模式下，TTL 过小可能抛出异常。"""
        with patch("ping3.EXCEPTIONS", True):
            try:
                result = ping3.ping(DEST_ADDR, ttl=1, timeout=2)
                # 如果没抛异常，结果应为 None、False 或 float
                if result is not None and result is not False:
                    self.assertIsInstance(result, float)
            except (ping3.errors.TimeToLiveExpired, ping3.errors.Timeout):
                # 这两种异常都是预期行为
                pass


# ============================================================
# 多进程并发测试
# ============================================================

class TestMultiprocessing(unittest.TestCase):
    """测试多进程并发 ping。"""

    def test_concurrent_pings_processes(self):
        """多个进程同时 ping，所有进程都应正常返回。"""
        queue = multiprocessing.Queue()
        num_workers = 3
        processes = []

        for _ in range(num_workers):
            p = multiprocessing.Process(
                target=_ping_in_process,
                args=(DEST_ADDR, 4, queue),
            )
            processes.append(p)
            p.start()
        for p in processes:
            p.join(timeout=15)

        results = []
        while not queue.empty():
            results.append(queue.get_nowait())

        self.assertEqual(len(results), num_workers)
        for status, value in results:
            self.assertEqual(status, "ok", f"Process failed: {value}")
            self.assertIsInstance(value, float)
            self.assertGreater(value, 0, "Process ping delay must be positive")

    def test_process_no_packet_stealing(self):
        """多进程并发 ping，不应有进程 timeout。"""
        queue = multiprocessing.Queue()
        num_workers = 4
        processes = []

        for _ in range(num_workers):
            p = multiprocessing.Process(
                target=_ping_in_process,
                args=(DEST_ADDR, 4, queue),
            )
            processes.append(p)
            p.start()
        for p in processes:
            p.join(timeout=20)

        results = []
        while not queue.empty():
            results.append(queue.get_nowait())

        self.assertEqual(len(results), num_workers)
        timeouts = [(s, v) for s, v in results if s == "ok" and v is None]
        self.assertEqual(
            len(timeouts), 0,
            f"{len(timeouts)} processes got None (timeout) — "
            f"possible cross-process ICMP packet confusion"
        )

    def test_process_consecutive_pings(self):
        """单个进程连续 ping 多次，所有结果应合理。
        这是检测进程内部 ICMP 残留包的基本测试。"""
        queue = multiprocessing.Queue()
        num_pings = 5
        p = multiprocessing.Process(
            target=_ping_in_process_with_timing,
            args=(DEST_ADDR, 4, num_pings, queue),
        )
        p.start()
        p.join(timeout=30)

        self.assertFalse(queue.empty(), "Process did not return results")
        status, delays = queue.get_nowait()
        self.assertEqual(status, "ok")
        self.assertEqual(len(delays), num_pings)

        for i, d in enumerate(delays):
            if isinstance(d, tuple) and d[0] == "error":
                self.fail(f"Ping {i} raised error: {d[1]}")
            self.assertIsNotNone(d, f"Ping {i} timed out in sequential pings")
            self.assertIsInstance(d, float)
            self.assertGreater(d, 0)


# ============================================================
# 多进程 vs 多线程一致性
# ============================================================

class TestMultiprocessVsThread(unittest.TestCase):
    """对比多进程与多线程的 ping 结果。"""

    def test_results_consistency(self):
        """多线程和多进程 ping 同一目标，都应返回合理的 delay。"""
        # 多线程
        thread_results = []
        lock = threading.Lock()

        def thread_worker():
            delay = ping3.ping(DEST_ADDR, timeout=4)
            with lock:
                thread_results.append(delay)

        threads = []
        for _ in range(2):
            t = threading.Thread(target=thread_worker)
            threads.append(t)
            t.start()
        for t in threads:
            t.join(timeout=15)

        # 多进程
        queue = multiprocessing.Queue()
        processes = []
        for _ in range(2):
            p = multiprocessing.Process(
                target=_ping_in_process,
                args=(DEST_ADDR, 4, queue),
            )
            processes.append(p)
            p.start()
        for p in processes:
            p.join(timeout=15)

        process_results = []
        while not queue.empty():
            status, value = queue.get_nowait()
            if status == "ok":
                process_results.append(value)

        # 两者都应有结果
        self.assertTrue(len(thread_results) > 0, "No thread results")
        self.assertTrue(len(process_results) > 0, "No process results")

        # 所有结果应为正数 float（不应有 None/timeout）
        for i, r in enumerate(thread_results):
            self.assertIsNotNone(r, f"Thread ping {i} timed out")
            self.assertIsInstance(r, float)
        for i, r in enumerate(process_results):
            self.assertIsNotNone(r, f"Process ping {i} timed out")
            self.assertIsInstance(r, float)


if __name__ == "__main__":
    unittest.main(verbosity=2, exit=False)
