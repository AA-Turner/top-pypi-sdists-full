"""Maddog batch 7 — make native-FC + shell a UNIVERSAL standard (every integration
AND bring-your-own MCP servers), not Vercel/recipe-specific.

From the universal-standard audit: routing/execution were already generic; the gaps
were (1) guidance led with hardcoded recipes, (2) _op_rank only knew hardcoded resolver
names, (3) relevant_slugs didn't match BYO host-derived slugs, (4) a no-auth PUBLIC MCP
server couldn't connect at all, (5) /integrations add lacked the PAT fallback.

Locks in: universal RESOLVE-THEN-ACT protocol + BYO first-class note in the prompt,
generic op-rank, BYO slug matching, the public no-auth connect path + sentinel, and the
/integrations add token fallback.
"""
import os
import sys
import unittest
from unittest import mock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import nx_mcp_tools as T   # noqa: E402
import nx_mcp_oauth as O   # noqa: E402
import nx_mcp_client as C  # noqa: E402


class GenericOpRank(unittest.TestCase):
    def test_byo_resolver_names_rank_zero(self):
        for n in ("find_container", "resolve_board", "get_database", "search_repos",
                  "list_collections", "lookup_account"):
            self.assertEqual(T._op_rank(n), 0, n)

    def test_generic_mutators_rank_one(self):
        for n in ("publish_post", "submit_form", "approve_request", "merge_branch"):
            self.assertEqual(T._op_rank(n), 1, n)

    def test_plain_reads_and_misc(self):
        self.assertEqual(T._op_rank("get_status"), 2)
        self.assertEqual(T._op_rank("ask_question"), 3)


class ByoSlugScoping(unittest.TestCase):
    def test_host_derived_slug_matches_meaningful_token(self):
        with mock.patch.object(T, "connected_slugs", lambda: ["mcp-deepwiki-com", "linear"]), \
             mock.patch.object(T._oauth, "get_server",
                               lambda s: {"name": "mcp.deepwiki.com" if "deep" in s else "Linear"}):
            self.assertEqual(T.relevant_slugs("use deepwiki to read facebook/react"),
                             ["mcp-deepwiki-com"])      # matched 'deepwiki', not noise 'mcp'/'com'
            self.assertEqual(T.relevant_slugs("create a linear issue"), ["linear"])


class PublicNoAuthConnect(unittest.TestCase):
    def test_is_connected_honors_public_sentinel(self):
        with mock.patch.object(O, "load_token", lambda s: {"public": True}):
            self.assertTrue(O.is_connected("mcp-deepwiki-com"))
        with mock.patch.object(O, "load_token", lambda s: {}):
            self.assertFalse(O.is_connected("x"))

    def test_try_public_saves_sentinel_when_endpoint_serves_mcp(self):
        saved = {}

        class Live:
            def initialize(self): return True
        with mock.patch.object(O, "get_server", lambda s: {"url": "https://mcp.deepwiki.com/mcp", "name": "deepwiki"}), \
             mock.patch.object(C, "MCPSession", lambda u, t: Live()), \
             mock.patch.object(O, "save_token", lambda slug, tok: saved.update({slug: tok})):
            r = O._try_public("mcp-deepwiki-com")
        self.assertTrue(r["ok"])
        self.assertEqual(r["mode"], "public")
        self.assertTrue(saved["mcp-deepwiki-com"]["public"])   # sentinel stored

    def test_try_public_fails_closed_if_auth_required(self):
        class Dead:
            def initialize(self): raise Exception("401 unauthorized")
        with mock.patch.object(O, "get_server", lambda s: {"url": "u", "name": "x"}), \
             mock.patch.object(C, "MCPSession", lambda u, t: Dead()):
            r = O._try_public("x")
        self.assertFalse(r["ok"])

    def test_session_connects_public_server_with_no_token(self):
        # token None + is_connected True (public) → _session still builds a session.
        class Live:
            def initialize(self): return True
        with mock.patch.object(T._oauth, "get_server", lambda s: {"url": "u", "name": "x"}), \
             mock.patch.object(T._oauth, "usable_token", lambda s: None), \
             mock.patch.object(T._oauth, "is_connected", lambda s: True), \
             mock.patch.object(T._client, "MCPSession", lambda u, t: Live()):
            T._SESSIONS.pop("pub", None)
            self.assertIsNotNone(T._session("pub"))


class PromptUniversal(unittest.TestCase):
    def test_universal_protocol_and_byo_note(self):
        fs = {"x": {"name": "X", "tools": [{"name": "create_thing"}]}}
        with mock.patch.object(T, "gather_tools", lambda slugs=None, **k: fs), \
             mock.patch.object(T, "connected_slugs", lambda: ["x"]):
            tp = T.tools_prompt()
        self.assertIn("UNIVERSAL CREATE/UPDATE/DELETE PROTOCOL", tp)
        self.assertIn("ACCELERATORS", tp)            # recipes demoted to examples
        self.assertIn("FIRST-CLASS", tp)             # BYO note
        self.assertIn("RESOLVE-THEN-ACT", tp)


class CliTokenFallback(unittest.TestCase):
    def test_integrations_add_has_token_fallback(self):
        src = open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                "nx_cli.py")).read()
        # BYO add path falls back to a PAT when there's no one-click sign-in
        self.assertIn('_r=_mcpo.connect_url(_url)', src)
        self.assertIn('connect_with_token(_slug, _tok)', src)


if __name__ == "__main__":
    unittest.main()
