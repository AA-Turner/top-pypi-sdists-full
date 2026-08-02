"""
Operator effort ladder (/effort · the web effort bar): low · mid · high · extra · council. Tests the canonical
effort→tier map, the coding-stays-on-code-tier rule, the council top stop, precedence over auto-escalation, and
the ZERO-REGRESSION default (no stop ⇒ routing byte-identical to before). Pure route() — no network.

Run: python3 -m unittest tests.test_effort_routing < /dev/null
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import nx_routing as R  # noqa: E402
from nx_obfuscate import ENV  # noqa: E402


def _clear_native():
    for k in (ENV["dashscope_api_key"], ENV["deepseek_api_key"], "NX_QWEN_MODEL_MAX"):
        os.environ.pop(k, None)


class TestNormalizeEffort(unittest.TestCase):
    def test_canonical_and_aliases(self):
        self.assertEqual(R.normalize_effort("low"), "low")
        self.assertEqual(R.normalize_effort("/HIGH"), "high")       # tolerates leading / + case
        self.assertEqual(R.normalize_effort("$council"), "council")  # tolerates leading $
        self.assertEqual(R.normalize_effort("med"), "mid")           # alias
        self.assertEqual(R.normalize_effort("medium"), "mid")
        self.assertEqual(R.normalize_effort("max"), "council")       # alias → top stop
        self.assertEqual(R.normalize_effort("ultracode"), "council")

    def test_unknown_and_empty_are_none(self):
        for bad in (None, "", "  ", "turbo", "extreme", "/xyz"):
            self.assertIsNone(R.normalize_effort(bad), bad)


class TestEffortLadder(unittest.TestCase):
    def setUp(self):
        self._saved = {k: os.environ.get(k) for k in (ENV["dashscope_api_key"], ENV["deepseek_api_key"], "NX_QWEN_MODEL_MAX")}
        _clear_native()

    def tearDown(self):
        _clear_native()
        for k, v in self._saved.items():
            if v is not None:
                os.environ[k] = v

    def test_non_coding_follows_the_ladder_tier_and_depth(self):
        # A NON-coding turn maps each stop to (tier, reasoning_effort) per the canonical ladder.
        cases = {"low": ("flash", "low"), "mid": ("frontier", "medium"), "high": ("frontier", "high"), "extra": ("agentic", "high")}
        for stop, (tier, effort) in cases.items():
            r = R.route(world="cowork", user_input="what should I have for lunch", effort_override=stop)
            self.assertEqual(r.tier, tier, stop)
            self.assertEqual(r.reasoning_effort, effort, stop)

    def test_coding_always_stays_on_code_tier_but_takes_the_stops_depth(self):
        # CODING keeps the code tier (→ Qwen when keyed, else Kimi) regardless of stop; the stop only sets depth.
        for stop, effort in (("low", "low"), ("mid", "medium"), ("high", "high"), ("extra", "high")):
            r = R.route(world="cowork", user_input="fix the null-pointer bug in auth.py", effort_override=stop)
            self.assertEqual(r.tier, "code", stop)
            self.assertEqual(r.reasoning_effort, effort, stop)

    def test_council_stop_forces_council_even_on_casual(self):
        r = R.route(world="cowork", user_input="hi", effort_override="council")
        self.assertEqual(r.tier, "council")

    def test_explicit_stop_beats_auto_escalation(self):
        # "please analyze Q3 revenue" auto-escalates flash→frontier; an explicit /low pins it back to flash.
        auto = R.route(world="cowork", user_input="please analyze Q3 revenue")
        self.assertEqual(auto.tier, "frontier")
        pinned = R.route(world="cowork", user_input="please analyze Q3 revenue", effort_override="low")
        self.assertEqual(pinned.tier, "flash")

    def test_no_stop_is_zero_regression(self):
        # No stop ⇒ identical to a bare route() with no effort arg (the default auto path is untouched).
        a = R.route(world="cowork", user_input="fix the bug in app.py")
        b = R.route(world="cowork", user_input="fix the bug in app.py", effort_override=None)
        self.assertEqual((a.tier, a.model, a.reasoning_effort), (b.tier, b.model, b.reasoning_effort))


if __name__ == "__main__":
    unittest.main()
