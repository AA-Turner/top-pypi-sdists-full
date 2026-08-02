"""Maddog batch 4 — NATIVE function-calling (the root fix).

Found by driving the real nx in a PTY: text-tag tool calls fumbled creates
(hallucinated 'integration' server, wrong tool, bad args). The model natively
supports OpenAI function-calling — confirmed live it returns structured tool_calls.
NX now hands it the connected tools as a schema (scoped to the integration the
query names) and executes the structured calls. Live result: Linear create/read/
update all work; delete is honestly reported as archive-only.

Locks in: tools_schema (OpenAI schema + [Integration] label + name→route map),
route_fn, relevant_slugs (query scoping), and the wiring in nx_cli (tools sent in
the payload, tool_calls accumulated, native execution loop).
"""
import os
import sys
import unittest
from unittest import mock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import nx_mcp_tools as T   # noqa: E402

_FS = {"linear": {"name": "Linear", "tools": [
            {"name": "save_issue", "description": "create/update an issue",
             "inputSchema": {"type": "object", "properties": {"title": {"type": "string"}},
                             "required": ["title"]}},
            {"name": "list_issues", "description": "list issues"}]},
       "notion": {"name": "Notion", "tools": [
            {"name": "notion-create-pages", "description": "create pages"}]}}


class ToolsSchema(unittest.TestCase):
    def test_openai_schema_shape_and_routing(self):
        with mock.patch.object(T, "gather_tools", lambda slugs=None, **k: _FS):
            sch = T.tools_schema()
        names = {f["function"]["name"] for f in sch}
        self.assertIn("linear__save_issue", names)
        self.assertIn("notion__notion-create-pages", names)
        save = next(f for f in sch if f["function"]["name"] == "linear__save_issue")
        self.assertEqual(save["type"], "function")
        self.assertTrue(save["function"]["description"].startswith("[Linear]"))   # integration label
        self.assertEqual(save["function"]["parameters"]["required"], ["title"])    # real inputSchema
        # name -> (server, tool) route map populated as a side effect
        self.assertEqual(T.route_fn("linear__save_issue"), ("linear", "save_issue"))
        self.assertEqual(T.route_fn("notion__notion-create-pages"), ("notion", "notion-create-pages"))
        self.assertIsNone(T.route_fn("does__not_exist"))

    def test_scoped_schema_only_includes_named_integration(self):
        with mock.patch.object(T, "gather_tools",
                               lambda slugs=None, **k: {s: _FS[s] for s in (slugs or _FS)}):
            sch = T.tools_schema(slugs=["linear"])
        servers = {f["function"]["name"].split("__")[0] for f in sch}
        self.assertEqual(servers, {"linear"})   # notion excluded → small, clear set


class RelevantSlugs(unittest.TestCase):
    def test_names_integration_in_query(self):
        with mock.patch.object(T, "connected_slugs", lambda: ["linear", "notion", "monday-com"]), \
             mock.patch.object(T._oauth, "get_server",
                               lambda s: {"name": {"linear": "Linear", "notion": "Notion",
                                                   "monday-com": "monday.com"}.get(s, s)}):
            self.assertEqual(T.relevant_slugs("create a Linear issue"), ["linear"])
            self.assertEqual(T.relevant_slugs("what's on my monday board"), ["monday-com"])
            self.assertIsNone(T.relevant_slugs("what's the weather"))   # nothing named → no scope


class WiredIntoCli(unittest.TestCase):
    def test_stream_chat_sends_tools_and_accumulates_tool_calls(self):
        src = open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                "nx_cli.py")).read()
        self.assertIn('_payload["tools"] = tools', src)          # tools go into the request
        self.assertIn('_payload["tool_choice"] = "auto"', src)
        self.assertIn('cfg.setdefault("_native_tool_calls"', src)  # streamed tool_calls accumulated
        self.assertIn("_mt.route_fn(c[\"name\"])", src)          # native loop routes + executes
        self.assertIn('"role": "tool"', src)                      # tool results fed back


if __name__ == "__main__":
    unittest.main()
