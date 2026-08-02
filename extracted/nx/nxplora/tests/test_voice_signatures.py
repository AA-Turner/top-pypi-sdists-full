"""Audit-V: mode gates must produce structurally different system prompts.

The user-facing modes (Partner · Autopilot · Study · Refine) replaced the retired
voices (PEER/ADVISOR/CHALLENGER/OPERATOR/TEACHER). NX_VOICE_GATES is a back-compat
alias for NX_MODE_GATES, so these tests still assert on that name."""

from __future__ import annotations

import unittest


SIGNATURES = {
    "PARTNER":   [r"single declarative sentence", r"one step at a time"],
    "AUTOPILOT": [r"deliverable on line 1",       r"Report back"],
    "STUDY":     [r"Cite the source",             r"misconception"],
    "REFINE":    [r"DRAFT to make better",        r"tighter than the input"],
}


class VoiceGatesPresenceTests(unittest.TestCase):
    def test_all_voice_gates_defined(self):
        from nx_prompts import NX_VOICE_GATES
        self.assertEqual(
            set(NX_VOICE_GATES.keys()),
            set(SIGNATURES.keys()),
            "Voice-gate registry drifted from documented contract",
        )

    def test_each_gate_carries_its_signature(self):
        from nx_prompts import NX_VOICE_GATES
        for voice, patterns in SIGNATURES.items():
            gate = NX_VOICE_GATES[voice]
            for pat in patterns:
                self.assertRegex(
                    gate, pat,
                    f"voice {voice!r} missing signature pattern {pat!r}",
                )


class VoiceGatePairwiseDistinctTests(unittest.TestCase):
    def test_pairwise_diff_above_4pct(self):
        from nx_prompts import build_system_prompt
        prompts = {
            v: build_system_prompt(world="cowork", voice=v)
            for v in SIGNATURES.keys()
        }
        for a, p_a in prompts.items():
            for b, p_b in prompts.items():
                if a >= b:
                    continue
                set_a = set(p_a.split())
                set_b = set(p_b.split())
                only_a = set_a - set_b
                only_b = set_b - set_a
                distinct = len(only_a) + len(only_b)
                total = max(1, len(set_a | set_b))
                ratio = distinct / total
                self.assertGreater(
                    ratio, 0.04,
                    f"voices {a} vs {b} are too similar (ratio={ratio:.3f})",
                )

    def test_connected_integrations_injected_as_global(self):
        from nx_prompts import build_system_prompt
        # omitted -> no block at all (backward compatible; council/tests path)
        base = build_system_prompt(world="sales", voice="PARTNER")
        self.assertNotIn("CONNECTED INTEGRATIONS", base)
        # supplied -> the REAL names appear, framed as account-wide / GLOBAL, with
        # the world described as changing the execution GOAL (not the connections)
        p = build_system_prompt(world="sales", voice="PEER",
                                connected=["Notion", "Linear", "Square"])
        for name in ("Notion", "Linear", "Square"):
            self.assertIn(name, p)
        self.assertIn("account-wide", p)
        self.assertIn("GLOBAL", p)
        self.assertIn("execution goal", p)        # world = goals, not connections
        self.assertIn('"depends on the world"', p)  # explicit negation instruction
        # empty list -> say "none connected", never imply a fabricated connection
        empty = build_system_prompt(world="sales", voice="PEER", connected=[])
        self.assertIn("none connected", empty)

    def test_signatures_do_not_overlap(self):
        from nx_prompts import NX_VOICE_GATES
        seen = {}
        for voice, patterns in SIGNATURES.items():
            for pat in patterns:
                if pat in seen and seen[pat] != voice:
                    self.fail(
                        f"signature {pat!r} in both {seen[pat]} and {voice}"
                    )
                seen[pat] = voice

    def test_every_voice_gate_has_a_length_cap(self):
        # Each voice gate must carry an explicit brevity cap so a NEW voice
        # can't be added without the discipline (audit:
        # voice-gate-no-anti-narration-enforcement). 'Default length' or
        # 'sentences' must appear in the gate text.
        from nx_prompts import NX_VOICE_GATES
        for voice, text in NX_VOICE_GATES.items():
            low = text.lower()
            self.assertTrue(
                "default length" in low or "sentence" in low or "one line" in low,
                f"voice gate {voice} is missing an explicit length cap",
            )

    def test_voice_gates_dont_instruct_self_narration(self):
        # No voice gate should tell the model to narrate its own reasoning
        # (these would directly cause the leaks _scrub/_strip exist to clean up).
        from nx_prompts import NX_VOICE_GATES
        banned = ("think out loud", "here's my thinking", "walk through your reasoning",
                  "explain your reasoning step", "narrate your")
        for voice, text in NX_VOICE_GATES.items():
            low = text.lower()
            for b in banned:
                self.assertNotIn(b, low, f"voice gate {voice} instructs self-narration: {b!r}")


class TierRegistryCoverageTests(unittest.TestCase):
    def test_every_provider_has_a_tier_set(self):
        # Every provider NX can resolve to must have a tier registry, so a
        # resolved provider never inherits another provider's model namespace
        # (audit: tier-registry-default-fallback-to-fireworks).
        import importlib
        nx_obfuscate = importlib.import_module("nx_obfuscate")
        nx_routing = importlib.import_module("nx_routing")
        for prov in nx_obfuscate.P.values():
            self.assertIn(prov, nx_routing.TIERS_BY_PROVIDER,
                          f"provider {prov} has no tier registry")
        # And every tier set covers all 5 tiers.
        for prov, reg in nx_routing.TIERS_BY_PROVIDER.items():
            for tier in ("flash", "frontier", "agentic", "code", "council"):
                self.assertIn(tier, reg, f"{prov} tier set missing {tier}")


if __name__ == "__main__":
    unittest.main()
