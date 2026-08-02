"""
test_mcp_tools.py — the bridge from connected remote MCP servers into NX's chat
tool loop: gather tools → describe in the prompt → route <nx:mcp/> calls. Mocks
the session; the live end-to-end (model tag → real DeepWiki call → real result
through nx_cli._execute_nx_tool_calls) is proven in the 0.9.0 commit message.
"""
import os
import sys
import unittest
from unittest import mock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import nx_mcp_tools as T   # noqa: E402
import nx_mcp_oauth as O   # noqa: E402


class FakeSession:
    def __init__(self, tools, result):
        self._tools = tools
        self._result = result
        self.calls = []

    def list_tools(self):
        return self._tools

    def call_tool(self, name, args):
        self.calls.append((name, args))
        return self._result


class GatherTests(unittest.TestCase):
    def setUp(self):
        T.reset()

    def test_gather_and_prompt(self):
        fs = FakeSession([{"name": "search", "description": "Search docs"}],
                         {"content": [{"type": "text", "text": "hi"}]})
        with mock.patch.object(T, "_session", lambda slug: fs), \
             mock.patch.object(T, "connected_slugs", lambda: ["notion"]), \
             mock.patch.object(O, "get_server", lambda s: {"name": "Notion", "url": "x"}):
            g = T.gather_tools()
            self.assertIn("notion", g)
            self.assertEqual(g["notion"]["tools"][0]["name"], "search")
            tp = T.tools_prompt()
            self.assertIn("nx:mcp", tp)
            self.assertIn("search", tp)
            self.assertIn("notion", tp)

    def test_prompt_empty_when_nothing_connected(self):
        with mock.patch.object(T, "connected_slugs", lambda: []):
            self.assertEqual(T.tools_prompt(), "")

    def test_prompt_bounded_with_huge_server(self):
        # A 520-tool server (GoHighLevel) must NOT balloon the system prompt —
        # that 400'd the model. Stay bounded + show the count + a "more" note.
        heavy = {"ghl": {"name": "GoHighLevel",
                         "tools": [{"name": f"t{i}", "description": "x" * 90} for i in range(520)]},
                 "sf": {"name": "Salesforce",
                        "tools": [{"name": f"s{i}", "description": "y" * 90} for i in range(150)]}}
        with mock.patch.object(T, "gather_tools", lambda slugs=None: heavy), \
             mock.patch.object(T, "connected_slugs", lambda: ["ghl", "sf"]):
            tp = T.tools_prompt()
        self.assertLess(len(tp), 6200, "tools_prompt must stay bounded")
        self.assertIn("520 tools", tp)
        self.assertIn("more", tp)

    def test_prompt_lists_every_connected_server(self):
        # The old 8-server cap left NX blind to >half of 16 connected integrations,
        # so it guessed tool names (get_projects) and -32602'd. EVERY connected
        # server must now appear, with its real tool names to call by.
        many = {f"srv{i}": {"name": f"Srv{i}",
                            "tools": [{"name": f"srv{i}_get", "description": "d"}]}
                for i in range(16)}
        with mock.patch.object(T, "gather_tools", lambda slugs=None: many), \
             mock.patch.object(T, "connected_slugs", lambda: [f"srv{i}" for i in range(16)]):
            tp = T.tools_prompt()
        for i in range(16):
            self.assertIn(f"srv{i}_get", tp, f"srv{i}'s tool must be listed (no 8-cap)")

    def test_prompt_carries_autonomous_execution_rules(self):
        fs = FakeSession([{"name": "search", "description": "Search docs"}],
                         {"content": [{"type": "text", "text": "hi"}]})
        with mock.patch.object(T, "_session", lambda slug: fs), \
             mock.patch.object(T, "connected_slugs", lambda: ["notion"]), \
             mock.patch.object(O, "get_server", lambda s: {"name": "Notion", "url": "x"}):
            tp = T.tools_prompt()
        # self-correct on error (don't bounce back to the operator) + execute the
        # directive across all integrations (don't ask which one)
        self.assertIn("SELF-CORRECT", tp)
        self.assertIn("retry", tp.lower())
        self.assertIn("EXECUTE DATA DIRECTIVES", tp)
        self.assertIn("<nx:health/>", tp)   # connectivity check uses health, not data tools

    def test_call_extracts_text_and_parses_args(self):
        fs = FakeSession([], {"content": [{"type": "text", "text": "the answer"}]})
        with mock.patch.object(T, "_session", lambda slug: fs):
            r = T.call("notion", "search", '{"q": "x"}')
        self.assertTrue(r["ok"])
        # The extracted text is present; call() now wraps third-party MCP output in the
        # ⟦UNTRUSTED_INTEGRATION_DATA⟧ envelope (prompt-injection defense), so assert containment.
        self.assertIn("the answer", r["text"])
        self.assertIn("UNTRUSTED_INTEGRATION_DATA", r["text"])
        self.assertEqual(fs.calls[0], ("search", {"q": "x"}))

    def test_call_not_connected_is_honest(self):
        with mock.patch.object(T, "_session", lambda slug: None):
            r = T.call("notion", "x", {})
        self.assertFalse(r["ok"])
        self.assertIn("not connected", r["error"])

    def test_call_invented_server_is_rejected_with_real_list(self):
        # NX hallucinated server="integration" and looped on it. An unknown server
        # must come back with a corrective error — "not a connected integration",
        # don't invent, here's the REAL list — so NX picks a valid one or stops.
        with mock.patch.object(T, "_session", lambda slug: None), \
             mock.patch.object(O, "get_server", lambda s: None), \
             mock.patch.object(T, "connected_slugs", lambda: ["notion", "sentry"]):
            r = T.call("integration", "list", {})
        self.assertFalse(r["ok"])
        self.assertIn("not a connected integration", r["error"].lower())
        self.assertIn("notion", r["error"])  # real servers offered to correct to


class AutoconnectSkipTests(unittest.TestCase):
    def test_mcp_connected_service_is_not_re_setup(self):
        # The bug: asking about Notion (connected via MCP sign-in) triggered the
        # OLD "notion not connected — setting it up → NOTION_API_KEY" path.
        import nx_autoconnect as A
        with mock.patch.object(A, "detect_needed_integrations", lambda m: ["notion"]), \
             mock.patch.object(A, "get_connected_integrations", lambda uid: []), \
             mock.patch.object(O, "is_connected", lambda s: s.strip().lower() == "notion"):
            self.assertEqual(A.maybe_autoconnect("what's on my notion roadmap?", "u"), [])

    def test_all_mcp_signins_counted_as_connected_even_if_hub_down(self):
        # Across the board: every MCP sign-in must register as connected at the
        # ROOT (get_connected_integrations), independent of the hub.
        import nx_autoconnect as A
        signed = {"notion", "linear", "gohighlevel", "sentry"}
        with mock.patch.object(O, "is_connected", lambda s: s.strip().lower() in signed), \
             mock.patch("httpx.get", side_effect=Exception("hub down")):
            conn = {c.lower() for c in A.get_connected_integrations("u")}
        for s in signed:
            self.assertIn(s, conn, f"{s} sign-in not counted as connected")

    def test_unconnected_service_still_sets_up(self):
        import nx_autoconnect as A
        with mock.patch.object(A, "detect_needed_integrations", lambda m: ["notion"]), \
             mock.patch.object(A, "get_connected_integrations", lambda uid: []), \
             mock.patch.object(O, "is_connected", lambda s: False), \
             mock.patch.object(A, "autoconnect", lambda i, u, canvas=None: {"success": True}):
            self.assertTrue(A.maybe_autoconnect("connect notion", "u"))


class PresentationTests(unittest.TestCase):
    def test_summary_collapses_raw_output(self):
        import nx_cli
        self.assertEqual(nx_cli._summarize_mcp_output('{"results":[]}', True), "no matches")
        self.assertEqual(nx_cli._summarize_mcp_output('{"results":[1,2]}', True), "2 results")
        self.assertIn("not found", nx_cli._summarize_mcp_output("Tool x not found", False))

    def test_streamer_hides_raw_mcp_tag(self):
        import io, re as _re
        from nx_terminal import _NxStream
        buf = io.StringIO()
        old = sys.stdout
        sys.stdout = buf
        try:
            s = _NxStream()
            s.write('<nx:mcp server="notion" tool="search" args=\'{"q":"x"}\'/>')
            s.finish()
        finally:
            sys.stdout = old
        out = _re.sub(r"\x1b\[[0-9;]*m", "", buf.getvalue())
        self.assertNotIn("<nx:mcp", out)          # raw XML never shown
        self.assertIn("Notion", out)              # clean action line instead


class ToolResultInjectionTests(unittest.TestCase):
    def test_mcp_results_reach_the_model(self):
        # The fabrication bug: _format_tool_results had no "mcp" branch, so the
        # real data never reached the model and it hallucinated fake records.
        import nx_cli
        ctx = nx_cli._format_tool_results([{
            "tool": "mcp", "server": "notion", "name": "get-teams",
            "success": True, "output": '{"joinedTeams":[],"otherTeams":[]}'}])
        self.assertIn('{"joinedTeams":[]', ctx)   # the EXACT data is injected
        self.assertIn("notion", ctx)
        self.assertIn("exact", ctx.lower())       # + the don't-paraphrase framing

    def test_any_tool_type_injects_data_no_one_off(self):
        # The CLASS of the bug: a tool type not explicitly coded for must STILL
        # have its real output injected — so the next integration can't recreate
        # the fabrication gap. Anti-fabrication framing applies universally.
        import nx_cli
        ctx = nx_cli._format_tool_results([
            {"tool": "some_future_tool", "success": True, "output": "REAL_DATA_XYZ"}])
        self.assertIn("REAL_DATA_XYZ", ctx)
        self.assertIn("NEVER", ctx)
        self.assertIn("invent", ctx)

    def test_executor_is_registry_driven_writes_last(self):
        import nx_cli
        order = sorted(nx_cli.TOOL_REGISTRY,
                       key=lambda n: bool(nx_cli.TOOL_REGISTRY[n].get("counts_as_write")
                                          or nx_cli.TOOL_REGISTRY[n].get("requires_approval")))
        self.assertEqual(order[-1], "run_command")          # write/exec runs last
        self.assertIn("mcp", order[:-1])                     # data tools run before it


class PayloadRegressionTests(unittest.TestCase):
    def test_no_nested_extra_body_in_request_payload(self):
        # Regression: a raw POST to Fireworks must NOT carry a nested "extra_body"
        # field — it 400s ("Extra inputs are not permitted"). Provider params are
        # merged at the top level instead.
        src = open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                "nx_cli.py")).read()
        self.assertNotIn('payload["extra_body"]', src)
        self.assertNotIn("payload['extra_body']", src)


class ExecutorIntegrationTests(unittest.TestCase):
    def test_mcp_tag_parsed_and_routed(self):
        import nx_cli
        resp = 'one sec <nx:mcp server="notion" tool="search" args=\'{"q": "roadmap"}\'/>'
        self.assertTrue(nx_cli._has_tool_tags(resp))
        with mock.patch("nx_mcp_tools.call", lambda s, t, a: {"ok": True, "text": "RESULT"}):
            cleaned, results = nx_cli._execute_nx_tool_calls(resp, cfg={}, approve_fn=None)
        self.assertIn("«ran notion.search ✓»", cleaned)   # non-mimicable history marker
        self.assertEqual(results[0]["output"], "RESULT")
        self.assertTrue(results[0]["success"])
        self.assertEqual(results[0]["server"], "notion")

    def test_mcp_tag_failure_is_marked(self):
        import nx_cli
        resp = '<nx:mcp server="x" tool="y" args=\'{}\'/>'
        with mock.patch("nx_mcp_tools.call", lambda s, t, a: {"ok": False, "error": "boom"}):
            cleaned, results = nx_cli._execute_nx_tool_calls(resp, cfg={}, approve_fn=None)
        self.assertFalse(results[0]["success"])
        # A failed call is marked in the «…» history and NEVER shown as the success ✓.
        # The glyph is ✗ (not connected) or ⚠ (connected-but-errored — deliberately not
        # rendered as "broken"; see the marker at nx_cli.py:1132). Assert the failure is
        # marked with either, not the specific ✗ that only the disconnected path uses.
        self.assertIn("«ran x.y", cleaned)
        self.assertNotIn("✓", cleaned)
        self.assertTrue(("✗" in cleaned) or ("⚠" in cleaned), f"failure not marked: {cleaned!r}")


if __name__ == "__main__":
    unittest.main()
