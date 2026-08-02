"""
MAX partnership (0.4+): $council = Qwen 3.8 Max × DeepSeek V4 Pro when both native keys are set. Tests the pure
composition + endpoint resolution + the ZERO-REGRESSION default (no native key ⇒ the Fireworks 3-voice is
unchanged). The partnership activates silently (invisible mechanic — no user-facing warning). The debate LOOP
itself is unchanged, so no network is touched here.

Run: python3 -m unittest tests.test_council_partnership < /dev/null
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import nx_council as C  # noqa: E402
from nx_obfuscate import ENV, FW, P, URLS  # noqa: E402

QW_ENV = ENV["dashscope_api_key"]
DS_ENV = ENV["deepseek_api_key"]


class TestPartnership(unittest.TestCase):
    def setUp(self):
        self._saved = {k: os.environ.get(k) for k in (QW_ENV, DS_ENV, "NX_QWEN_MODEL_MAX")}
        for k in self._saved:
            os.environ.pop(k, None)

    def tearDown(self):
        for k, v in self._saved.items():
            os.environ.pop(k, None)
            if v is not None:
                os.environ[k] = v

    def test_default_is_the_fireworks_three_voice_zero_regression(self):
        # No native key → composition + synthesis are byte-identical to before (the FW 3-voice).
        self.assertEqual(C.council_models(), list(C.COUNCIL_MODELS))
        self.assertEqual(C.synthesis_model(), C.SYNTHESIS_MODEL)
        self.assertFalse(C._native_council_active())

    def test_both_native_keys_activate_the_qwen_x_deepseek_partnership(self):
        os.environ[QW_ENV] = "qw-test"
        os.environ[DS_ENV] = "ds-test"
        self.assertTrue(C._native_council_active())
        comp = C.council_models()
        self.assertIn("qwen-max", comp)                 # Qwen is in the debate
        self.assertIn("deepseek-reasoner", comp)        # DeepSeek-V4-Pro is in the debate
        self.assertEqual(C.synthesis_model(), "deepseek-reasoner")  # DeepSeek-Pro merges

    def test_one_native_key_is_not_enough(self):
        # The partnership needs BOTH (Qwen for one voice, DeepSeek for the other) — one key alone stays FW default.
        os.environ[QW_ENV] = "qw-test"
        self.assertFalse(C._native_council_active())
        self.assertEqual(C.council_models(), list(C.COUNCIL_MODELS))

    def test_endpoint_resolution_is_per_model(self):
        os.environ[QW_ENV] = "qw-test"
        os.environ[DS_ENV] = "ds-test"
        qw = C._native_endpoint_for("qwen-max")
        ds = C._native_endpoint_for("deepseek-reasoner")
        self.assertEqual(qw[0], URLS[P["dashscope"]])
        self.assertEqual(qw[1], "qw-test")
        self.assertEqual(ds[0], URLS[P["deepseek"]])
        self.assertEqual(ds[1], "ds-test")
        # a Fireworks model id → None (uses the primary provider)
        self.assertIsNone(C._native_endpoint_for(FW["pro"]))

    def test_model_id_env_override_flows_into_composition(self):
        os.environ[QW_ENV] = "qw-test"
        os.environ[DS_ENV] = "ds-test"
        os.environ["NX_QWEN_MODEL_MAX"] = "qwen3.8-max-preview"
        self.assertIn("qwen3.8-max-preview", C.council_models())
        self.assertEqual(C._native_endpoint_for("qwen3.8-max-preview")[0], URLS[P["dashscope"]])

    def test_partnership_activates_with_no_user_facing_warning(self):
        # Invisible mechanic: the warning surface is gone entirely — the function must not exist, so nothing can
        # ever print a token heads-up. The partnership still activates purely on key presence.
        os.environ[QW_ENV] = "qw-test"
        os.environ[DS_ENV] = "ds-test"
        self.assertTrue(C._native_council_active())
        self.assertFalse(hasattr(C, "max_partnership_first_time_warning"))
        self.assertFalse(hasattr(C, "_COUNCIL_MAXWARN_MARK"))


if __name__ == "__main__":
    unittest.main()
