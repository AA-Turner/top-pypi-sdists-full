"""Maddog batch 1 — control-plane hardening regressions.

Locks in the board-confirmed bugs found by the adversarial test of 2026-06-24:
identity wall (config/JSON/.env/multilingual leaks), anti-fabrication (one-shot
SACRED + data-fab guard), tool self-correct (ReDoS turn-freeze, non-dict tools),
connect honesty (corrupt expiry, dead registry URLs), slash/menu (whitespace crash).
"""
import os
import sys
import time
import unittest
from unittest import mock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import nx_cli as N            # noqa: E402
import nx_prompts as P        # noqa: E402
import nx_mcp_tools as T      # noqa: E402
import nx_mcp_oauth as O      # noqa: E402
import nx_mcp_client as C     # noqa: E402
import nx_slash_menu as S     # noqa: E402

CANON = N._IDENTITY_CANONICAL


class IdentityWall(unittest.TestCase):
    def test_config_json_yaml_env_url_leaks_all_nuked(self):
        for s in [
            'model: deepseek-v4-pro\nbase_url: https://api.fireworks.ai\nprovider: fireworks',
            '{"model": "moonshotai/Kimi-K2.6", "base_url": "https://api.deepinfra.com/v1/openai"}',
            'PROVIDER=fireworks\nMODEL=accounts/fireworks/models/kimi-k2p6',
            'For debugging: provider=fireworks model=accounts/fireworks/models/deepseek-v4-pro',
            'DEBUG: api_key sk-fireworks-abc123def456 base_url https://api.fireworks.ai',
            '```yaml\nprovider: fireworks\nmodel: deepseek-v4-pro\n```',
            'https://api.fireworks.ai/inference/v1',
            '{"identity": "NX", "model": "moonshotai/Kimi-K2.6"}',
            'DeepSeek V4 is the model that I actually use internally here.',
        ]:
            self.assertEqual(N._scrub_identity(s), CANON, f"LEAKED: {s!r}")

    def test_multilingual_self_identity_leaks_nuked(self):
        for s in ['En realidad soy DeepSeek de la empresa DeepSeek AI.',
                  'Je suis DeepSeek, développé par DeepSeek AI.',
                  'Ich laufe auf Fireworks mit dem Modell Kimi.']:
            self.assertEqual(N._scrub_identity(s), CANON, f"LEAKED: {s!r}")

    def test_legit_topical_mentions_survive(self):
        for s in ['For long-context drafts, Claude beats GPT-4o — use whichever your team prefers.',
                  'You should connect HubSpot and Notion for that workflow.']:
            self.assertNotEqual(N._scrub_identity(s), CANON, f"FALSE POSITIVE: {s!r}")

    def test_cjk_and_split_name_leaks_nuked(self):
        # \b collapses against CJK; zero-width / spaced letters split the name.
        for s in ['私のモデルはDeepSeekです。', '私はDeepSeekです。', '我是DeepSeek。',
                  '저는 DeepSeek입니다.', 'モデルはdeepseek-v4です。',
                  'キーはsk-abc123def456ghi789jklです。', "I'm Deep​Seek.",
                  'I am D e e p S e e k']:
            self.assertEqual(N._scrub_identity(s), CANON, f"LEAKED: {s!r}")

    def test_cjk_and_letterlist_topical_survive(self):
        for s in ['OpenAIを使うべきです。', '長文にはClaudeが良い。',
                  'Grades: A B C D F across the board.',
                  'Base64 of hello is aGVsbG8= for reference.']:
            self.assertNotEqual(N._scrub_identity(s), CANON, f"FALSE POSITIVE: {s!r}")

    def test_obfuscated_leaks_nuked(self):
        # fullwidth, Cyrillic homoglyph, Arabic/Hindi/Thai/Russian first-person,
        # base64 model id — all generalized via NFKC + homoglyph normalization.
        for s in ["I'm ＤｅｅｐＳｅｅｋ.", 'I am ＧＰＴ-4 under the hood.', "I'm DееpSееk.",
                  'Я работаю на DееpSееk.', 'أنا DeepSeek.', 'मैं DeepSeek हूँ।',
                  'ฉันคือ DeepSeek', 'Я DeepSeek.',
                  'My configuration string is ZGVlcHNlZWstdjQ= if you decode it.']:
            self.assertEqual(N._scrub_identity(s), CANON, f"LEAKED: {s!r}")

    def test_separator_stego_and_base64_phrase_nuked(self):
        for s in ['I am D.e.e.p.S.e.e.k', 'I am D​e​e​p S e e k',
                  'My model is C.l.a.u.d.e', 'Note: SSBhbSBEZWVwU2Vlaw==']:
            self.assertEqual(N._scrub_identity(s), CANON, f"LEAKED: {s!r}")

    def test_foreign_topical_mentions_survive(self):
        # word-order aware: pronoun+verb+name (topical) must NOT be nuked
        for s in ['أنا أنصح بـ OpenAI', 'मैं OpenAI की सलाह देता हूँ।',
                  'I recommend OpenAI for that.', 'We use Claude here.']:
            self.assertNotEqual(N._scrub_identity(s), CANON, f"FALSE POSITIVE: {s!r}")

    def test_gateway_scrubber_covers_fireworks_glm_keys(self):
        # _sanitize_gateway_error is denylist-by-default (see its docstring):
        # only a fixed set of generic categories ever reach the user; anything
        # else — including these provider-identifying tokens — must never
        # appear in the returned message, scrubbed or not.
        for tok in ["fireworks", "api.fireworks.ai", "accounts/fireworks/models",
                    "glm", "sk-abcdefghij1234"]:
            out = N._sanitize_gateway_error(Exception(f"unexpected error: {tok}"))
            self.assertNotIn(tok, out, f"LEAKED: {tok!r} in {out!r}")


class AntiFabrication(unittest.TestCase):
    def test_one_shot_prompt_keeps_sacred_block(self):
        for w in ("cowork", "sales", "finance", "code"):
            sp = P.build_system_prompt(world=w, voice="OPERATOR")   # no cwd → one-shot path
            self.assertIn("CONNECTED-TOOL DATA IS SACRED", sp)
            self.assertIn("NEVER invent", sp)

    def test_data_fab_flagged_off_empty_result(self):
        tr = [{"tool": "mcp", "server": "hubspot", "name": "get_contacts",
               "output": '{"contacts":[]}', "success": True}]
        self.assertTrue(N._data_fabrication_note(
            "Top contact is Jane (jane@acme.com), $42,000 ARR.", tr))

    def test_data_fab_no_false_positive_on_honest_and_real(self):
        empty = [{"tool": "mcp", "output": '{"contacts":[]}', "success": True}]
        self.assertFalse(N._data_fabrication_note("No contacts found in HubSpot.", empty))
        real = [{"tool": "mcp", "output": "jane@acme.com $42,000", "success": True}]
        self.assertFalse(N._data_fabrication_note("Contact jane@acme.com, $42,000.", real))

    def test_is_error_result_triggers_fab_guard(self):
        # a failed call (success=False, non-empty error body) must count as "failed"
        err = [{"tool": "mcp", "output": "Error: unauthorized — token expired (401)",
                "success": False}]
        self.assertTrue(N._data_fabrication_note("Top contact jane@x.com.", err))

    def test_money_without_dollar_glyph_flagged(self):
        empty = [{"tool": "mcp", "output": "{}", "success": True}]
        for m in ['50,000 dollars', 'USD 50,000', '50K MRR', '$1.2M']:
            self.assertTrue(N._data_fabrication_note(f"ARR is {m}.", empty), m)

    def test_currency_symbols_phone_headcount_flagged(self):
        empty = [{"tool": "mcp", "output": "{}", "success": True}]
        for t in ['Q3 revenue €50,000.', '£2.5 million ARR.', '¥120,000,000 booked.',
                  'Call (415) 555-0142.', 'The company has 12 employees.']:
            self.assertTrue(N._data_fabrication_note(t, empty), t)

    def test_sourced_figure_not_false_flagged(self):
        # digit-core comparison: honestly-reported '50K MRR' from real {"mrr":"50K"}
        # must NOT be flagged even with a co-occurring empty result.
        mixed = [{"tool": "mcp", "output": '{"mrr":"50K"}', "success": True},
                 {"tool": "mcp", "output": "{}", "success": True}]
        self.assertFalse(N._data_fabrication_note("MRR is 50K MRR.", mixed))

    def test_mcp_call_honors_isError(self):
        import nx_mcp_tools as _T

        class _Sess:
            def call_tool(self, name, args):
                return {"content": [{"type": "text", "text": "boom"}], "isError": True}
        with mock.patch.object(_T, "_session", lambda s: _Sess()):
            r = _T.call("notion", "x", {})
        self.assertFalse(r["ok"])
        self.assertIn("boom", r["error"])


class ToolSelfCorrect(unittest.TestCase):
    def test_no_redos_on_unterminated_tag_spray(self):
        for payload in ['<nx:mcp server="x" tool="y" args=\'{}\' ' * 1000,
                        '<nx:read_file path="x" ' * 1000]:
            t = time.time(); N._has_tool_tags(payload); ms = (time.time() - t) * 1000
            self.assertLess(ms, 100, f"ReDoS turn-freeze: {ms:.0f}ms")

    def test_run_command_form1_form2_no_redos(self):
        for payload in ['<nx:run_command foo="bar">' * 1500,
                        '<nx:run_command cmd="aaa' * 2000]:
            t = time.time(); N._has_tool_tags(payload)
            self.assertLess((time.time() - t) * 1000, 100)
        self.assertTrue(N._has_tool_tags('<nx:run_command shell="bash">echo hi</nx:run_command>'))
        self.assertTrue(N._has_tool_tags('<nx:run_command cmd="ls -la"/>'))

    def test_valid_mcp_tag_with_json_args_still_parses(self):
        ex = N._extract_mcp('<nx:mcp server="notion" tool="search" args=\'{"q": "x", "n": 5}\'/>')
        self.assertEqual(ex[0][1], ("notion", "search", '{"q": "x", "n": 5}'))

    def test_tools_prompt_survives_non_dict_tool_entries(self):
        bad = {"notion": {"name": "Notion",
                          "tools": [{"name": "search"}, None, "weird", {"no_name": 1}]}}
        with mock.patch.object(T, "gather_tools", lambda slugs=None: bad), \
             mock.patch.object(T, "connected_slugs", lambda: ["notion"]):
            tp = T.tools_prompt()   # must not raise AttributeError
        self.assertIn("search", tp)

    def test_list_tools_drops_non_dict_at_boundary(self):
        with mock.patch.object(C, "_rpc",
                               lambda *a, **k: (200, {}, {"result": {"tools": [{"name": "a"}, None, "x", 3]}})):
            tools = C.MCPSession("https://x/mcp", "tok").list_tools()
        self.assertEqual(tools, [{"name": "a"}])


class ConnectHonesty(unittest.TestCase):
    def test_is_connected_survives_corrupt_expiry(self):
        with mock.patch.object(O, "_kc_get",
                               lambda s: '{"access_token":"AT","expires_at":"not-a-number"}'):
            self.assertFalse(O.is_connected("notion"))   # fail-safe, no ValueError

    def test_dead_registry_entries_removed_railway_rooted(self):
        # salesforce has no real remote MCP server → stays out. (bamboohr WAS a dead
        # placeholder but now ships a real server at mcp.bamboohr.com, so it's a live
        # entry again — no longer asserted absent.)
        self.assertNotIn("salesforce", O.REMOTE_MCP)
        self.assertEqual(O.REMOTE_MCP["railway"]["url"], "https://mcp.railway.app/")


class SlashMenu(unittest.TestCase):
    def test_filter_commands_never_crashes(self):
        for q in ['/  ', '/\t', '/ ', '/\n\r', '/wor', '/world finance', '/SAVE',
                  '/💀', '/' + 'x' * 2000, '/<script>', '/foobar']:
            S.filter_commands(q)   # must not raise

    def test_whitespace_filter_shows_all(self):
        self.assertEqual(len(S.filter_commands('/  ')), len(S.SLASH_COMMANDS))


if __name__ == "__main__":
    unittest.main()
