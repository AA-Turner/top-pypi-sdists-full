"""
Native raw-price routing (0.4+) — Qwen (DashScope) leads HEAVY/coding/long-turn, DeepSeek leads flash chat + deep
reasoning; no native key ⇒ ZERO change (the Fireworks/DeepInfra chain is byte-identical). Tests the pure
_native_override + one route() integration + the TIERS invariant for the new providers.

Run: python3 -m unittest tests.test_native_routing < /dev/null
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import nx_routing as R  # noqa: E402
from nx_obfuscate import P, NATIVE, ENV  # noqa: E402

DS_ENV = ENV["deepseek_api_key"]
QW_ENV = ENV["dashscope_api_key"]


def _clear():
    for k in (DS_ENV, QW_ENV, "NX_QWEN_MODEL_MAX", "NX_DEEPSEEK_MODEL_CHAT", "NX_DEEPSEEK_MODEL_REASONER"):
        os.environ.pop(k, None)


class TestNativeOverride(unittest.TestCase):
    def setUp(self):
        self._saved = {k: os.environ.get(k) for k in (DS_ENV, QW_ENV, "NX_QWEN_MODEL_MAX", "NX_DEEPSEEK_MODEL_CHAT", "NX_DEEPSEEK_MODEL_REASONER")}
        _clear()

    def tearDown(self):
        _clear()
        for k, v in self._saved.items():
            if v is not None:
                os.environ[k] = v

    def test_no_native_key_is_a_noop(self):
        # No native key set → _native_override returns None for EVERY tier (zero regression).
        for tier in ("flash", "frontier", "code", "agentic", "council"):
            self.assertIsNone(R._native_override(tier, "do the thing"), tier)

    def test_deepseek_leads_light_and_reasoning_tiers(self):
        os.environ[DS_ENV] = "ds-test"
        # flash chat → DeepSeek chat
        prov, model, *_ = R._native_override("flash", "quick note")
        self.assertEqual(prov, P["deepseek"])
        self.assertEqual(model, "deepseek-chat")
        # frontier / council deep reasoning → DeepSeek reasoner
        self.assertEqual(R._native_override("frontier", "analyze the strategy")[1], "deepseek-reasoner")
        self.assertEqual(R._native_override("council", "$council weigh in")[1], "deepseek-reasoner")

    def test_qwen_leads_agentic_and_ALL_coding(self):
        os.environ[QW_ENV] = "qw-test"
        os.environ[DS_ENV] = "ds-test"
        # agentic (heavy / long-horizon) → Qwen
        self.assertEqual(R._native_override("agentic", "orchestrate a multi-step build")[0], P["dashscope"])
        self.assertEqual(R._native_override("agentic", "orchestrate a multi-step build")[1], "qwen-max")
        # ALL coding → Qwen — heavy, light query, AND audit — every code turn
        for msg in ("refactor this entire multi-file service and add tests", "what does this one-line regex do", "audit this module for bugs"):
            self.assertEqual(R._native_override("code", msg)[0], P["dashscope"], msg)
            self.assertEqual(R._native_override("code", msg)[1], "qwen-max", msg)

    def test_coding_without_qwen_is_a_noop_meantime_kimi_lane(self):
        # No Qwen (DashScope) key → the native CODE override is a no-op (None), so route() uses the meantime
        # Kimi 2.6/7 code lane. DeepSeek is NOT a coding lead (coding = Qwen when keyed, else Kimi — never DeepSeek).
        os.environ[DS_ENV] = "ds-test"
        self.assertIsNone(R._native_override("code", "refactor this entire multi-file service and add tests"))

    def test_involves_coding_gate(self):
        # coding (incl. audit) → True; casual chat/talk → False
        for coding in ("fix the auth bug", "audit this module", "refactor foo.py", "why does this throw a TypeError", "```js\nconst x=1```"):
            self.assertTrue(R.involves_coding(coding), coding)
        for casual in ("hey how's your day going", "what should I have for lunch", "tell me a joke", "good morning!"):
            self.assertFalse(R.involves_coding(casual), casual)

    def test_casual_chat_in_code_world_downgrades_to_flash_deepseek(self):
        # On a code-tier world, a casual (non-coding) turn routes to flash → DeepSeek Flash, not Qwen.
        os.environ[DS_ENV] = "ds-test"
        os.environ[QW_ENV] = "qw-test"
        r_casual = R.route("code", "hey how's your day going")
        self.assertEqual(r_casual.tier, "flash")
        self.assertEqual(r_casual.provider, P["deepseek"])
        # an actual coding turn on the same world stays code → Qwen
        r_code = R.route("code", "fix the null-pointer bug in the auth module")
        self.assertEqual(r_code.tier, "code")
        self.assertEqual(r_code.provider, P["dashscope"])

    def test_model_id_env_override(self):
        os.environ[QW_ENV] = "qw-test"
        os.environ["NX_QWEN_MODEL_MAX"] = "qwen3.8-max-preview"
        self.assertEqual(R._native_override("agentic", "build it")[1], "qwen3.8-max-preview")

    def test_route_integration_flash_leads_deepseek_when_keyed(self):
        # A casual turn routes native to DeepSeek when the key is set; not-deepseek when it isn't.
        os.environ[DS_ENV] = "ds-test"
        r = R.route("cowork", "quick note about my day")
        self.assertEqual(r.provider, P["deepseek"])
        _clear()
        r2 = R.route("cowork", "quick note about my day")
        self.assertNotEqual(r2.provider, P["deepseek"])

    def test_tiers_invariant_covers_native_providers(self):
        # Both native providers MUST have a tier set (else route() could serve a wrong-namespace id).
        self.assertIn(P["deepseek"], R.TIERS_BY_PROVIDER)
        self.assertIn(P["dashscope"], R.TIERS_BY_PROVIDER)


if __name__ == "__main__":
    unittest.main()
