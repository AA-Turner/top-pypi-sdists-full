"""@agent and $takeoff — calling an agent up by name, and dispatch as a skill.

`$` is already the skill sigil ($brain, $council, $browse) and `@` is the natural one for an
identity. These tests pin the resolver, because the resolver is where an identity mistake would
happen: resolving "@vin" to the wrong agent sends a real message over the wrong account.
"""
import os
import re
import sys
import unittest
from unittest import mock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import nx_cli  # noqa: E402

_NX_CLI_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "nx_cli.py"
)


VINNY = {"name": "Vinny", "display": "Vinny",
         "channels": {"email": {"handle": "victor@nexplora.ai", "verified": True},
                      "telegram": {"handle": "6672341304", "verified": True}}}
EZRA = {"name": "ezra", "display": "ezra",
        "channels": {"email": {"handle": "jlo320si320@gmail.com", "verified": False}}}
MIKAEL = {"name": "Mikael", "display": "Mikael",
          "channels": {"imessage": {"handle": "7186195095", "verified": True}}}
NO_CHANNEL = {"name": "Scout", "display": "Scout", "channels": {}}


def _with(binds):
    return mock.patch.object(nx_cli, "_load_user_items", lambda kind: binds if kind == "agent-channels" else [])


class AgentResolution(unittest.TestCase):
    def test_exact_name_resolves_case_insensitively(self):
        with _with([VINNY, EZRA, MIKAEL]):
            # The operator sees "Vinny" and types "@vinny". Both must land.
            self.assertEqual(nx_cli._agent_by_handle("vinny")["name"], "Vinny")
            self.assertEqual(nx_cli._agent_by_handle("VINNY")["name"], "Vinny")
            self.assertEqual(nx_cli._agent_by_handle("Vinny")["name"], "Vinny")

    def test_leading_at_is_tolerated(self):
        with _with([VINNY]):
            self.assertEqual(nx_cli._agent_by_handle("@vinny")["name"], "Vinny")

    def test_unique_prefix_resolves(self):
        with _with([VINNY, EZRA, MIKAEL]):
            self.assertEqual(nx_cli._agent_by_handle("vin")["name"], "Vinny")
            self.assertEqual(nx_cli._agent_by_handle("mik")["name"], "Mikael")

    def test_AMBIGUOUS_prefix_resolves_to_NOTHING(self):
        # The assertion that matters most. Two agents starting with the same letters must not be
        # guessed between — picking one sends a real message over the wrong identity, and the
        # operator would have no reason to suspect it happened.
        binds = [VINNY, {"name": "Vince", "display": "Vince", "channels": {"email": {"handle": "v@x", "verified": True}}}]
        with _with(binds):
            self.assertIsNone(nx_cli._agent_by_handle("vin"))
            # …but a full exact name still resolves, even while a sibling prefix exists.
            self.assertEqual(nx_cli._agent_by_handle("vinny")["name"], "Vinny")

    def test_duplicate_names_refuse_rather_than_pick(self):
        dup = dict(VINNY)
        with _with([VINNY, dup]):
            self.assertIsNone(nx_cli._agent_by_handle("vinny"))

    def test_an_agent_with_NO_channel_is_not_addressable(self):
        # It cannot act as itself, so addressing it would silently run the turn as the OPERATOR —
        # the quiet identity substitution this whole surface exists to prevent.
        with _with([NO_CHANNEL]):
            self.assertIsNone(nx_cli._agent_by_handle("scout"))

    def test_unknown_and_empty_tokens_are_none(self):
        with _with([VINNY]):
            for tok in ("", "  ", "@", "nobody", "2pm"):
                self.assertIsNone(nx_cli._agent_by_handle(tok), f"{tok!r} must not resolve")


class AgentPersonaWiring(unittest.TestCase):
    """`@vinny do X` must CHANGE the turn, not just print an attribution over an ordinary one."""

    def test_the_AT_BRANCH_sets_the_seam_and_not_a_dead_key(self):
        # HONEST LIMITS + why this is source-level. The two tests below exercise
        # _agent_persona_text and _augment_system_prompt directly, and they pass whether or not the
        # REPL is wired to them — I verified that by reverting the wiring and watching them stay
        # green. So they do not pin the fix; this does. The REPL loop is not callable in isolation,
        # so the @ branch is asserted at source, with comments stripped so prose ABOUT the code can
        # never satisfy it.
        src = open(_NX_CLI_PATH, encoding="utf-8").read()
        code = re.sub(r"^\s*#.*$", "", src, flags=re.M)
        # assertTrue, not assertIn: assertIn prints the whole haystack on failure, and the haystack
        # here is a 1.7MB source file. A failure nobody can read is barely a failure.
        self.assertTrue(
            'cfg["_agent_persona"] = _agent_persona_text(' in code,
            "@name must set _agent_persona — the per-turn seam _augment_system_prompt reads. "
            "Without it, `@vinny do X` prints an attribution over an ordinary turn.",
        )
        # A key nothing reads is decoration, and decoration that looks like behaviour is the exact
        # false green this feature exists to avoid.
        self.assertTrue(
            'cfg["_active_agent"]' not in code,
            "_active_agent is read by nothing; setting it would be decoration",
        )

    def test_the_persona_lands_on_the_seam_the_model_actually_reads(self):
        cfg = {"_agent_persona": nx_cli._agent_persona_text(VINNY)}
        # _augment_system_prompt is what composes the real system prompt; if the persona does not
        # survive that call, `@name` is decoration. A first draft set an `_active_agent` key that
        # nothing read, which is exactly this failure.
        out = nx_cli._augment_system_prompt(cfg, "BASE PROMPT")
        self.assertIn("BASE PROMPT", out)
        self.assertIn("Vinny", out)

    def test_persona_is_per_turn_and_does_not_stick(self):
        cfg = {"_agent_persona": nx_cli._agent_persona_text(VINNY)}
        nx_cli._augment_system_prompt(cfg, "BASE")
        # popped, so the NEXT turn is the operator again — an identity that silently persisted
        # would send later messages as an agent the operator did not name.
        self.assertNotIn("_agent_persona", cfg)
        self.assertNotIn("Vinny", nx_cli._augment_system_prompt(cfg, "BASE"))

    def test_only_VERIFIED_channels_are_offered_as_usable(self):
        mixed = {"name": "Mix", "display": "Mix", "channels": {
            "email": {"handle": "a@b.c", "verified": True},
            "telegram": {"handle": "999", "verified": False}}}
        text = nx_cli._agent_persona_text(mixed)
        self.assertIn("a@b.c", text)
        # The unverified one must be named as NOT working, never presented as reach the agent has.
        self.assertIn("UNVERIFIED", text)
        self.assertIn("telegram", text)

    def test_an_agent_with_no_verified_channel_is_told_not_to_offer_sending(self):
        text = nx_cli._agent_persona_text(EZRA)   # single untested email
        self.assertIn("no verified channel", text)


class AgentCard(unittest.TestCase):
    def test_card_states_verified_vs_untested_per_channel(self):
        out = []
        with mock.patch("builtins.print", lambda *a, **k: out.append(" ".join(str(x) for x in a))):
            nx_cli._print_agent_card(VINNY)
        text = "\n".join(out)
        self.assertIn("email", text)
        self.assertIn("victor@nexplora.ai", text)
        self.assertIn("verified", text)

    def test_an_untested_handle_is_never_shown_as_verified(self):
        out = []
        with mock.patch("builtins.print", lambda *a, **k: out.append(" ".join(str(x) for x in a))):
            nx_cli._print_agent_card(EZRA)
        text = "\n".join(out)
        self.assertIn("untested", text)
        # "✓ verified" must not appear for a handle we have not proven — saying ready for an
        # unproven channel is the false green in miniature.
        self.assertNotIn("✓ verified", text)

    def test_card_for_a_channelless_agent_points_at_supply(self):
        out = []
        with mock.patch("builtins.print", lambda *a, **k: out.append(" ".join(str(x) for x in a))):
            nx_cli._print_agent_card(NO_CHANNEL)
        self.assertIn("/supply", "\n".join(out))


if __name__ == "__main__":
    unittest.main()
