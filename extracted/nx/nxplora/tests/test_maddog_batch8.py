"""Maddog batch 8 — the 4 next-batch findings (lead/CRM, multi-task truncation,
/save errors, council diagnostic), from the feature audit + live testing.
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import nx_prompts as P     # noqa: E402
import nx_routing as R     # noqa: E402
import nx_cli as C         # noqa: E402
import nx_slash_menu as M  # noqa: E402
import nx_mcp_tools as T   # noqa: E402

SRC = open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "nx_cli.py")).read()
COUNCIL = open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "nx_council.py")).read()


class F1_LeadUnderstanding(unittest.TestCase):
    def test_leads_customers_have_world_context(self):
        self.assertIn("leads", P.NX_WORLD_CONTEXT)
        self.assertIn("customers", P.NX_WORLD_CONTEXT)
        # substantive, not a stub — qualification framing present
        self.assertIn("qualif", P.NX_WORLD_CONTEXT["leads"].lower())
        self.assertIn("CRM", P.NX_WORLD_CONTEXT["leads"])

    def test_leads_world_is_frontier_tier(self):
        self.assertEqual(R.WORLD_CONFIG["leads"]["tier"], "frontier")

    def test_world_registries_consistent(self):
        # leads/customers now in BOTH NX_WORLD_CONTEXT and WORLD_CONFIG → no fallback
        self.assertEqual(R.assert_world_registries_consistent(), [])

    def test_lead_qualify_skill_in_both_registries(self):
        self.assertIn("lead_qualify", C._SKILL_PROMPTS)
        self.assertIn("pass", C._SKILL_PROMPTS["lead_qualify"].lower())   # decision shape
        in_menu = any("lead_qualify" in s.get("cmd", "")
                      for sec in M.SKILLS_SECTIONS for s in sec.get("skills", []))
        self.assertTrue(in_menu, "$lead_qualify must appear in the /skills menu too")


class F2_TruncationSignals(unittest.TestCase):
    def test_truncate_tool_output_signals(self):
        out = C._truncate_tool_output("x" * 20000)
        self.assertIn("TRUNCATED", out)
        self.assertIn("not", out.lower())   # "NOT the full result" / "do not assume"
        self.assertEqual(C._truncate_tool_output("short"), "short")

    def test_mcp_bound_signals(self):
        out = T._bound("y" * 20000)
        self.assertIn("TRUNCATED", out)
        self.assertEqual(T._bound("ok"), "ok")

    def test_call_uses_bound_not_hard_4000(self):
        # the old silent [:4000] is gone from call()'s result path
        import nx_mcp_tools as _t
        src = open(_t.__file__).read()
        self.assertIn("_bound(txt or json.dumps(content))", src)


class F3_SaveErrors(unittest.TestCase):
    def test_save_guards_empty_and_uses_real_error(self):
        # empty-guard before saving
        self.assertIn("Nothing to save yet", SRC)
        # local disk errors report the exception type, NOT the network sanitizer
        # (the _sanitize_gateway_error call was removed from the /save handler)
        save_block = SRC[SRC.index("def handle_storage_save_command"):
                         SRC.index("def _flush_storage_session")]
        self.assertNotIn("_sanitize_gateway_error", save_block)
        self.assertIn("type(e).__name__", save_block)


class F4_CouncilDiagnostic(unittest.TestCase):
    def test_all_voices_failed_emits_diagnostic(self):
        self.assertIn("Council couldn't reach the model layer", COUNCIL)
        self.assertNotIn("didn't converge cleanly", COUNCIL)   # vague non-answer removed

    def test_stale_synthesis_comment_fixed(self):
        self.assertNotIn("Synthesis stays on Kimi", COUNCIL)


if __name__ == "__main__":
    unittest.main()
