# asv#966: with setup hooks present, every timed call must observe
# freshly set-up state. Auto-calibrated number resolves to 1; warmup
# re-runs setup between calls; an explicitly set number is honored and
# batches with setup interleaved between individually timed calls.

import os
import sys
import unittest

_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from asv_runner.benchmarks.time import TimeBenchmark  # noqa: E402


def _make_benchmark(suite, method_name):
    method = getattr(suite, method_name)
    b = TimeBenchmark(f"Suite.{method_name}", method, [method, suite])
    b.do_setup()
    return b


class TestSetupBeforeEachTimedCall(unittest.TestCase):
    def test_auto_number_resolves_to_one_with_mutating_setup(self):
        """Reproducer from asv#966 under default (CPython) warmup."""

        class Suite:
            repeat = 5
            min_run_count = 1
            rounds = 1

            def setup(self):
                self.x = []

            def time_mutate(self):
                assert len(self.x) == 0
                self.x.append(0)

        result = _make_benchmark(Suite(), "time_mutate").run()
        self.assertEqual(result["number"], 1)
        self.assertGreaterEqual(len(result["samples"]), 1)

    def test_explicit_number_one_survives_warmup(self):
        """Warmup calls redo setup too: number=1 keeps its documented
        semantics (asv#966, the explicit-number report)."""

        class Suite:
            number = 1
            repeat = 3
            min_run_count = 1
            rounds = 1

            def setup(self):
                self.x = []

            def time_mutate(self):
                assert len(self.x) == 0
                self.x.append(0)

        result = _make_benchmark(Suite(), "time_mutate").run()
        self.assertEqual(result["number"], 1)
        self.assertGreaterEqual(len(result["samples"]), 1)

    def test_explicit_number_wins_over_setup(self):
        """A benign setup keeps timeit batching when number is explicit."""

        class Suite:
            number = 7
            repeat = 2
            warmup_time = 0
            min_run_count = 1
            rounds = 1

            def setup(self):
                self.data = list(range(8))

            def time_read(self):
                return sum(self.data)

        result = _make_benchmark(Suite(), "time_read").run()
        self.assertEqual(result["number"], 7)
        self.assertGreaterEqual(len(result["samples"]), 1)

    def test_explicit_number_batches_with_fresh_setup(self):
        """Explicit number>1 with a mutating setup: setup re-runs before
        every call and the batch still reports the requested number."""

        class Suite:
            number = 10
            repeat = 3
            warmup_time = 0.05
            min_run_count = 1
            rounds = 1

            def setup(self):
                self.x = []

            def time_mutate(self):
                assert len(self.x) == 0
                self.x.append(0)

        result = _make_benchmark(Suite(), "time_mutate").run()
        self.assertEqual(result["number"], 10)
        self.assertGreaterEqual(len(result["samples"]), 1)
        self.assertTrue(all(s >= 0 for s in result["samples"]))

    def test_auto_number_calibrates_without_setup(self):
        def time_fast():
            return 1 + 1

        time_fast.number = 0  # auto
        time_fast.repeat = 2
        time_fast.warmup_time = 0
        time_fast.sample_time = 0.001
        time_fast.min_run_count = 1
        time_fast.rounds = 1
        time_fast.processes = 1

        b = TimeBenchmark("m.time_fast", time_fast, [time_fast])
        b.do_setup()
        result = b.run()
        self.assertGreater(result["number"], 1)
        self.assertGreaterEqual(len(result["samples"]), 1)


if __name__ == "__main__":
    unittest.main()
