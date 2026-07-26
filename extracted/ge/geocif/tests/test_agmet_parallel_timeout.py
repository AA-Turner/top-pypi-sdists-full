"""Regression test for the geoagmet parallel-plotting deadlock fix.

A production run hung for ~15 h: a Pool worker was OOM-killed mid-plot, and
``list(tqdm(pool.imap_unordered(...)))`` blocked forever waiting for the dead
worker's lost result (multiprocessing.Pool does not surface worker death).

The fix (geoagmet.loop_agmet):
1. Consume ``imap_unordered`` with a PER-RESULT timeout (``result_iter.next(
   timeout=...)``) so a dead/hung worker converts an infinite block into a
   logged skip.
2. Cap concurrent workers (``agmet_max_workers``) so 64+ heavy geopandas
   workers don't OOM-kill in the first place.

Source-based so it passes on any environment (the agmet runtime deps aren't
needed to inspect the function body).
"""
import ast
import inspect
import unittest
from pathlib import Path

_SRC = (Path(__file__).resolve().parents[1] / "geocif" / "agmet" / "geoagmet.py").read_text(
    encoding="utf-8"
)
_TREE = ast.parse(_SRC)


def _func_src(name):
    for node in ast.walk(_TREE):
        if isinstance(node, ast.FunctionDef) and node.name == name:
            return ast.get_source_segment(_SRC, node)
    raise AssertionError(f"function {name} not found")


class TestAgmetParallelTimeout(unittest.TestCase):
    def setUp(self):
        self.src = _func_src("loop_agmet")

    def test_no_blind_list_consume(self):
        # The blind, hang-prone consume must be gone.
        self.assertNotIn(
            "list(tqdm(", self.src.replace(" ", ""),
            msg="loop_agmet must not blindly list(tqdm(imap_unordered)) — that hangs on worker death",
        )

    def test_per_result_timeout(self):
        # imap result iteration must use a timeout and catch mp.TimeoutError.
        self.assertRegex(self.src, r"\.next\(\s*timeout\s*=")
        self.assertIn("mp.TimeoutError", self.src)

    def test_worker_cap(self):
        # Worker count must be capped to avoid OOM (agmet_max_workers).
        self.assertIn("agmet_max_workers", self.src)
        self.assertRegex(self.src, r"min\(")

    def test_still_uses_imap_unordered(self):
        # We keep the Pool + imap_unordered, just consume it safely.
        self.assertIn("imap_unordered", self.src)


if __name__ == "__main__":
    unittest.main()
