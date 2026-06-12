import threading
import time
import unittest
from unittest.mock import MagicMock

from abstra_internals.repositories.linter.repository import LocalLinterRepository


class SingleFlightTest(unittest.TestCase):
    """LocalLinterRepository must single-flight its rule fan-out: concurrent
    callers may not each spawn their own thread-per-rule fan-out (the cold-start
    race where _initial_lint and an HTTP /check both run update_checks)."""

    def test_concurrent_find_issues_runs_fanout_once(self):
        repo = LocalLinterRepository()
        gate = threading.Event()
        count_lock = threading.Lock()
        calls = {"n": 0}

        def slow_run_rules(target_rules, merge):
            with count_lock:
                calls["n"] += 1
            gate.wait(timeout=3.0)
            repo.checks = []
            return repo.checks

        repo._run_rules = slow_run_rules  # type: ignore[method-assign]

        threads = [
            threading.Thread(target=repo.find_issues_in_codebase) for _ in range(5)
        ]
        for t in threads:
            t.start()
        time.sleep(0.1)
        # Only the lock winner may be inside the fan-out; the other 4 fall
        # through to the current (empty) checks without re-triggering.
        with count_lock:
            self.assertEqual(calls["n"], 1)
        gate.set()
        for t in threads:
            t.join(timeout=5.0)
        self.assertEqual(calls["n"], 1)

    def test_update_checks_serializes_concurrent_callers(self):
        repo = LocalLinterRepository()
        active = {"n": 0, "max": 0}
        active_lock = threading.Lock()

        def tracking_run_rules(target_rules, merge):
            with active_lock:
                active["n"] += 1
                active["max"] = max(active["max"], active["n"])
            time.sleep(0.03)
            with active_lock:
                active["n"] -= 1
            return repo.checks

        repo._run_rules = tracking_run_rules  # type: ignore[method-assign]

        threads = [threading.Thread(target=repo.update_checks) for _ in range(5)]
        for t in threads:
            t.start()
        for t in threads:
            t.join(timeout=5.0)

        # Blocking acquire serializes every caller — never two fan-outs at once.
        self.assertEqual(active["max"], 1)

    def test_find_issues_does_not_block_when_lock_held(self):
        repo = LocalLinterRepository()
        sentinel = MagicMock()
        sentinel.name = "Existing"
        repo.checks = [sentinel]

        acquired = repo._run_lock.acquire(blocking=False)
        self.assertTrue(acquired)
        try:
            result = repo.find_issues_in_codebase()
            self.assertEqual(result, [sentinel])
        finally:
            repo._run_lock.release()

    def test_find_issues_skips_fanout_when_lock_busy_and_cache_empty(self):
        repo = LocalLinterRepository()
        repo.checks = []
        ran = {"n": 0}
        original = repo._run_rules

        def tracking(*args, **kwargs):
            ran["n"] += 1
            return original(*args, **kwargs)

        repo._run_rules = tracking  # type: ignore[method-assign]

        repo._run_lock.acquire()
        try:
            result = repo.find_issues_in_codebase()
            # Lock busy + cold cache: return current state, do NOT run a fan-out.
            self.assertEqual(result, [])
            self.assertEqual(ran["n"], 0)
        finally:
            repo._run_lock.release()


if __name__ == "__main__":
    unittest.main()
