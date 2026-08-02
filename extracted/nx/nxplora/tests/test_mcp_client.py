"""
test_mcp_client.py — the MCP tool-calling client (initialize / tools/list /
tools/call over Streamable HTTP). Mocks the wire so framing + SSE parsing +
session handling are locked; the live initialize→list→call is proven separately
against real public servers (DeepWiki / GitMCP) in the 0.8.0 commit message.
"""
import json
import os
import sys
import unittest
from unittest import mock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import nx_mcp_client as C  # noqa: E402
import nx_mcp_oauth as O   # noqa: E402


class ParseTests(unittest.TestCase):
    def test_parse_plain_json(self):
        obj = C._parse("application/json", b'{"jsonrpc":"2.0","id":1,"result":{"ok":1}}')
        self.assertEqual(obj["result"]["ok"], 1)

    def test_parse_sse_stream(self):
        sse = (b"event: message\n"
               b'data: {"jsonrpc":"2.0","id":1,"result":{"tools":[]}}\n\n')
        obj = C._parse("text/event-stream", sse)
        self.assertIn("result", obj)
        self.assertEqual(obj["result"]["tools"], [])

    def test_parse_sse_ignores_non_result_events(self):
        sse = (b'data: {"jsonrpc":"2.0","method":"ping"}\n\n'
               b'data: {"jsonrpc":"2.0","id":1,"result":{"v":9}}\n\n')
        self.assertEqual(C._parse("text/event-stream", sse)["result"]["v"], 9)


class SessionTests(unittest.TestCase):
    def test_initialize_raises_on_401(self):
        with mock.patch.object(C, "_rpc", lambda *a, **k: (401, None, {})):
            with self.assertRaises(C.MCPAuthError):
                C.MCPSession("https://x/mcp", "tok").initialize()

    def test_initialize_and_list_and_call(self):
        calls = []
        def fake_rpc(url, token, method, params=None, session_id=None, notif=False, rid=1, timeout=45):
            calls.append(method)
            if method == "initialize":
                return 200, "sess-1", {"result": {"serverInfo": {"name": "X", "version": "1"},
                                                  "protocolVersion": "2025-06-18"}}
            if method == "notifications/initialized":
                return 202, session_id, {}
            if method == "tools/list":
                return 200, session_id, {"result": {"tools": [{"name": "do_thing"}]}}
            if method == "tools/call":
                return 200, session_id, {"result": {"content": [{"type": "text", "text": "done"}]}}
            return 200, session_id, {}
        with mock.patch.object(C, "_rpc", fake_rpc):
            s = C.MCPSession("https://x/mcp", "tok")
            info = s.initialize()
            self.assertEqual(info["name"], "X")
            self.assertEqual(s.session_id, "sess-1")
            self.assertIn("notifications/initialized", calls)
            tools = s.list_tools()
            self.assertEqual(tools[0]["name"], "do_thing")
            res = s.call_tool("do_thing", {"a": 1})
            self.assertEqual(res["content"][0]["text"], "done")

    def test_call_tool_raises_on_error(self):
        def fake_rpc(*a, **k):
            return 200, "s", {"error": {"message": "nope"}}
        with mock.patch.object(C, "_rpc", fake_rpc):
            s = C.MCPSession("https://x/mcp", "tok"); s.session_id = "s"
            with self.assertRaises(C.MCPError):
                s.call_tool("x")


class ConnectSessionTests(unittest.TestCase):
    def test_none_when_not_connected(self):
        # known server, but no token stored → None (honest, not a fake session)
        with mock.patch.object(O, "load_token", lambda slug: None):
            self.assertIsNone(C.connect_session("notion"))

    def test_none_for_unknown_service(self):
        self.assertIsNone(C.connect_session("not-a-real-thing-xyz"))


class ByoServerTests(unittest.TestCase):
    def setUp(self):
        self.kc = {}
        self._p = mock.patch.multiple(O,
                                      _kc_get=lambda s: self.kc.get(s),
                                      _kc_set=lambda s, v: self.kc.__setitem__(s, v) or True)
        self._p.start(); self.addCleanup(self._p.stop)

    def test_add_custom_server_then_resolve(self):
        slug = O.add_custom_server("https://mcp.acme.dev/mcp", "Acme")
        self.assertEqual(slug, "mcp-acme-dev")
        self.assertEqual(O.get_server(slug)["url"], "https://mcp.acme.dev/mcp")
        self.assertTrue(O.is_remote_mcp(slug))
        # curated ones still resolve
        self.assertEqual(O.get_server("notion")["name"], "Notion")


if __name__ == "__main__":
    unittest.main()
