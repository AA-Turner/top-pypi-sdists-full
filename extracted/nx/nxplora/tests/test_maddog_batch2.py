"""Maddog batch 2 — agentic integration health + honest interpretation.

Locks in: a validation error reads as 'connected (needs input)' not broken;
the live health_check classifies live vs reconnect; the <nx:health/> tool routes;
the prompt directs connectivity checks to health, not blind data-tool calls.
"""
import os
import sys
import unittest
from unittest import mock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import nx_cli as N            # noqa: E402
import nx_mcp_tools as T      # noqa: E402
import nx_mcp_oauth as O      # noqa: E402
import nx_mcp_client as C     # noqa: E402


class ArgValidationIsConnected(unittest.TestCase):
    def test_arg_error_marked_connected(self):
        class S:
            def call_tool(self, n, a):
                raise Exception("MCP error -32602: Invalid arguments for tool "
                                "list_projects: missing required property teamId")
            def list_tools(self):
                return [{"name": "list_projects"}]
        with mock.patch.object(T, "_session", lambda s: S()):
            r = T.call("vercel", "list_projects", {})
        self.assertFalse(r["ok"])
        self.assertTrue(r.get("connected"))          # NOT broken
        self.assertTrue(r.get("needs_input"))
        self.assertIn("IS connected", r["error"])

    def test_is_arg_validation_error(self):
        self.assertTrue(T._is_arg_validation_error("MCP error -32602 invalid arguments"))
        self.assertTrue(T._is_arg_validation_error("missing required property teamId"))
        self.assertTrue(T._is_arg_validation_error('validating root: required: ["query"]'))
        self.assertFalse(T._is_arg_validation_error("square not connected"))
        self.assertFalse(T._is_arg_validation_error("Failed to fetch: 500 Server Error"))

    def test_handle_mcp_surfaces_connected_flag(self):
        class S:
            def call_tool(self, n, a):
                raise Exception("-32602: invalid arguments: missing required property")
            def list_tools(self):
                return [{"name": "x"}]
        with mock.patch.object(T, "_session", lambda s: S()):
            result, marker = N._handle_mcp(("vercel", "list_projects", {}), None, {})
        self.assertTrue(result.get("connected"))
        self.assertIn("needs an argument", marker.lower())   # not a bare ✗ "error"
        self.assertNotIn("[MCP", marker)                     # non-mimicable «…» form


class HealthProbe(unittest.TestCase):
    # Test the per-server classifier directly (no threads → pytest-safe).
    def test_live(self):
        class Live:
            def initialize(self): pass
            def list_tools(self): return [{"name": "a"}, {"name": "b"}, "junk"]
        with mock.patch.object(O, "usable_token", lambda s: "tok"), \
             mock.patch.object(O, "get_server", lambda s: {"url": "u", "name": "Notion"}), \
             mock.patch.object(C, "MCPSession", lambda u, t: Live()):
            r = T._health_probe("notion")
        self.assertEqual(r["status"], "live")
        self.assertEqual(r["tools"], 2)        # junk (non-dict) dropped

    def test_dead_session_is_reconnect(self):
        # 401 AND no refresh token (refresh() -> False) => genuine reconnect.
        class Dead:
            def initialize(self): raise C.MCPAuthError("not authorized")
        with mock.patch.object(O, "usable_token", lambda s: "tok"), \
             mock.patch.object(O, "get_server", lambda s: {"url": "u", "name": "Square"}), \
             mock.patch.object(O, "refresh", lambda s: False), \
             mock.patch.object(C, "MCPSession", lambda u, t: Dead()):
            r = T._health_probe("square")
        self.assertEqual(r["status"], "reconnect")
        self.assertIn("/integrations square", r["hint"])

    def test_401_reactive_refresh_revives_to_live(self):
        # A token dead server-side but refreshable: 401 on first init, refresh() works, re-init
        # succeeds => board SELF-HEALS to 'live', never a false reconnect. This is "connect once".
        calls = {"n": 0}
        class Flip:
            def __init__(self, u, t): pass
            def initialize(self):
                calls["n"] += 1
                if calls["n"] == 1:
                    raise C.MCPAuthError("401")
            def list_tools(self): return [{"name": "a"}]
        with mock.patch.object(O, "usable_token", lambda s: "tok"), \
             mock.patch.object(O, "is_connected", lambda s: True), \
             mock.patch.object(O, "get_server", lambda s: {"url": "u", "name": "Slack"}), \
             mock.patch.object(O, "refresh", lambda s: True), \
             mock.patch.object(C, "MCPSession", Flip):
            r = T._health_probe("slack")
        self.assertEqual(r["status"], "live")


class CallReactiveRefresh(unittest.TestCase):
    def test_call_401_refresh_retry_succeeds(self):
        class DeadSess:
            def call_tool(self, n, a): raise C.MCPAuthError("401")
            def list_tools(self): return [{"name": "x"}]
        class LiveSess:
            def call_tool(self, n, a): return {"content": [{"type": "text", "text": "ok-data"}]}
            def list_tools(self): return [{"name": "x"}]
        seq = [DeadSess(), LiveSess()]
        with mock.patch.object(T, "_session", lambda s: seq.pop(0) if seq else LiveSess()), \
             mock.patch.object(O, "get_server", lambda s: {"url": "u", "name": "S"}), \
             mock.patch.object(O, "refresh", lambda s: True):
            r = T.call("slack", "x", {})
        self.assertTrue(r["ok"])
        self.assertIn("ok-data", r["text"])

    def test_call_401_no_refresh_is_reconnect(self):
        class DeadSess:
            def call_tool(self, n, a): raise C.MCPAuthError("401")
            def list_tools(self): return [{"name": "x"}]
        with mock.patch.object(T, "_session", lambda s: DeadSess()), \
             mock.patch.object(O, "get_server", lambda s: {"url": "u", "name": "S"}), \
             mock.patch.object(O, "refresh", lambda s: False):
            r = T.call("slack", "x", {})
        self.assertFalse(r["ok"])
        self.assertIn("reconnect", r["error"])


class AuthorizeScope(unittest.TestCase):
    _meta = {"authorize": "https://x/auth", "resource": "https://x", "scopes": ["read", "write"]}

    def test_offline_access_requested(self):
        url = O.build_authorize_url(dict(self._meta), "cid", "st", "chal")
        self.assertIn("offline_access", url)   # signals the server to issue a refresh token

    def test_offline_access_added_when_none_advertised(self):
        m = dict(self._meta); m["scopes"] = []
        self.assertIn("offline_access", O.build_authorize_url(m, "cid", "st", "chal"))

    def test_no_duplicate_offline_access(self):
        m = dict(self._meta); m["scopes"] = ["offline_access", "read"]
        url = O.build_authorize_url(m, "cid", "st", "chal")
        self.assertEqual(url.count("offline_access"), 1)

    def test_no_token_is_reconnect(self):
        with mock.patch.object(O, "usable_token", lambda s: None), \
             mock.patch.object(O, "get_server", lambda s: {"url": "u", "name": "X"}):
            self.assertEqual(T._health_probe("x")["status"], "reconnect")

    def test_transient_error_is_slow_not_reconnect(self):
        # A LIVE token whose server times out / 5xx / resets (NON-auth) must NOT be told to
        # reconnect: the credential is fine, the ping just didn't finish. Mislabeling this as
        # 'reconnect' is the #1 false alarm behind "why does everything need reconnecting".
        # Only a real 401 (MCPAuthError) is a reconnect; everything else is 'slow' (retry).
        class Flaky:
            def initialize(self): raise TimeoutError("read timed out")
        with mock.patch.object(O, "usable_token", lambda s: "tok"), \
             mock.patch.object(O, "is_connected", lambda s: True), \
             mock.patch.object(O, "get_server", lambda s: {"url": "u", "name": "Linear"}), \
             mock.patch.object(C, "MCPSession", lambda u, t: Flaky()):
            r = T._health_probe("linear")
        self.assertEqual(r["status"], "slow")
        self.assertNotIn("/integrations", r["hint"])   # never a re-auth demand for a live token


class HealthTool(unittest.TestCase):
    def test_health_tag_detected_and_extracted(self):
        self.assertTrue(N._has_tool_tags("sure <nx:health/> ok"))
        self.assertEqual(N._extract_health("<nx:health/>"), [("<nx:health/>", ())])
        self.assertIn("health", N.TOOL_REGISTRY)

    def test_health_handler_reports_status(self):
        rows = [{"slug": "notion", "name": "Notion", "status": "live", "tools": 17, "hint": ""},
                {"slug": "square", "name": "Square", "status": "reconnect", "tools": 0,
                 "hint": "/integrations square"}]
        with mock.patch.object(T, "health_check", lambda timeout=10: rows):
            result, marker = N._handle_health((), None, {})
        out = result["output"]
        self.assertIn("1/2", out)
        self.assertIn("Notion", out)
        self.assertIn("RECONNECT", out)
        self.assertIn("Square", out)


if __name__ == "__main__":
    unittest.main()
