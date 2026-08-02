"""Maddog batch 3 — live-driven fixes (found by driving the real nx in a PTY).

Locks in: hallucinated-server routing by tool name, real current date injected
into the prompt, autonomous create/edit container-resolution guidance.
"""
import datetime
import os
import sys
import unittest
from unittest import mock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import nx_mcp_tools as T   # noqa: E402
import nx_prompts as P     # noqa: E402


class HallucinatedServerRouting(unittest.TestCase):
    def test_unknown_server_routed_by_tool_name(self):
        T._TOOLS = {"linear": {"name": "Linear", "tools": [{"name": "create_issue"}, {"name": "list_teams"}]},
                    "notion": {"name": "Notion", "tools": [{"name": "notion-search"}]}}
        self.assertEqual(T._resolve_server_by_tool("create_issue"), "linear")
        self.assertEqual(T._resolve_server_by_tool("notion-search"), "notion")
        self.assertIsNone(T._resolve_server_by_tool("totally_made_up"))

    def test_ambiguous_tool_not_routed(self):
        T._TOOLS = {"a": {"name": "A", "tools": [{"name": "search"}]},
                    "b": {"name": "B", "tools": [{"name": "search"}]}}
        self.assertIsNone(T._resolve_server_by_tool("search"))   # 2 servers → ambiguous

    def test_call_reroutes_hallucinated_server(self):
        T._TOOLS = {"linear": {"name": "Linear", "tools": [{"name": "create_issue"}]}}
        captured = {}

        class S:
            def call_tool(self, n, a):
                captured["called"] = True
                return {"content": [{"type": "text", "text": "ok"}]}
        # 'integration' is not real → routes to linear (which has create_issue)
        with mock.patch.object(T._oauth, "get_server",
                               lambda s: None if s == "integration" else {"url": "u", "name": s}), \
             mock.patch.object(T, "_session", lambda s: S() if s == "linear" else None):
            r = T.call("integration", "create_issue", {})
        self.assertTrue(r["ok"])
        self.assertTrue(captured.get("called"))


class PromptHasRealDate(unittest.TestCase):
    def test_today_injected(self):
        sp = P.build_system_prompt(world="sales", voice="OPERATOR")
        self.assertIn("Today's date is", sp)
        self.assertIn(str(datetime.date.today().year), sp)   # real year, not training cutoff


class AutonomousCreate(unittest.TestCase):
    def test_prompt_directs_container_resolution(self):
        fs_tools = {"notion": {"name": "Notion", "tools": [{"name": "create"}]}}
        with mock.patch.object(T, "gather_tools", lambda slugs=None, **k: fs_tools), \
             mock.patch.object(T, "connected_slugs", lambda: ["notion"]):
            tp = T.tools_prompt()
        self.assertIn("UNIVERSAL CREATE", tp)         # the integration-agnostic protocol
        self.assertIn("DEFAULT to the first", tp)     # autonomy: don't stop to ask
        self.assertIn("never carry the target", tp)   # context-bleed fix


if __name__ == "__main__":
    unittest.main()
