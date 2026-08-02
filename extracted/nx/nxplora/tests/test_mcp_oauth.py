"""
test_mcp_oauth.py — the Claude-Code-style remote MCP connect: OAuth 2.1 + DCR +
PKCE, no app/secret. Mocks the HTTP + loopback so the orchestration is locked;
the live discovery/DCR/consent-reachability is proven separately by a network
drive (see the 0.7.0 commit message).
"""
import json
import os
import re
import sys
import time
import unittest
from unittest import mock
from urllib.parse import urlparse, parse_qs

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import nx_mcp_oauth as M  # noqa: E402


class MCPOAuthTests(unittest.TestCase):
    def test_is_remote_mcp(self):
        self.assertTrue(M.is_remote_mcp("notion"))
        self.assertTrue(M.is_remote_mcp("Linear"))
        self.assertFalse(M.is_remote_mcp("totally-made-up"))

    def test_discover_via_www_authenticate(self):
        def fake_req(url, method="GET", headers=None, data=None, timeout=15):
            if method == "POST" and url == "https://x/mcp":
                return 401, {"WWW-Authenticate": 'Bearer resource_metadata="https://x/.well-known/oauth-protected-resource"'}, b""
            if url.endswith("/.well-known/oauth-protected-resource"):
                return 200, {}, json.dumps({"authorization_servers": ["https://x"],
                                            "resource": "https://x/mcp",
                                            "scopes_supported": ["read"]}).encode()
            if url.endswith("/.well-known/oauth-authorization-server"):
                return 200, {}, json.dumps({"authorization_endpoint": "https://x/authorize",
                                            "token_endpoint": "https://x/token",
                                            "registration_endpoint": "https://x/register",
                                            "code_challenge_methods_supported": ["S256"]}).encode()
            return 404, {}, b""
        with mock.patch.object(M, "_req", fake_req):
            meta = M.discover("https://x/mcp")
        self.assertEqual(meta["authorize"], "https://x/authorize")
        self.assertEqual(meta["register"], "https://x/register")
        self.assertEqual(meta["resource"], "https://x/mcp")

    def test_discovery_failed_when_no_oauth(self):
        with mock.patch.object(M, "_req", lambda *a, **k: (404, {}, b"")):
            with self.assertRaises(M.MCPOAuthError):
                M.discover("https://x/mcp")

    def test_register_client_no_secret(self):
        with mock.patch.object(M, "_req", lambda *a, **k: (201, {}, json.dumps(
                {"client_id": "cid123", "token_endpoint_auth_method": "none"}).encode())):
            cid, sec = M.register_client("https://x/register")
        self.assertEqual(cid, "cid123")
        self.assertIsNone(sec)

    def test_authorize_url_carries_pkce_and_resource(self):
        meta = {"authorize": "https://x/authorize", "resource": "https://x/mcp", "scopes": ["read"]}
        _v, ch = M._pkce()
        url = M.build_authorize_url(meta, "cid", "state123", ch)
        q = parse_qs(urlparse(url).query)
        self.assertEqual(q["response_type"][0], "code")
        self.assertEqual(q["client_id"][0], "cid")
        self.assertEqual(q["code_challenge_method"][0], "S256")
        self.assertEqual(q["code_challenge"][0], ch)
        self.assertEqual(q["resource"][0], "https://x/mcp")
        self.assertIn("localhost", q["redirect_uri"][0])

    def test_pkce_challenge_matches_verifier(self):
        import base64, hashlib
        v, ch = M._pkce()
        expect = base64.urlsafe_b64encode(hashlib.sha256(v.encode()).digest()).rstrip(b"=").decode()
        self.assertEqual(ch, expect)

    def test_connect_full_flow_no_secret(self):
        kc = {}
        def fake_req(url, method="GET", headers=None, data=None, timeout=15):
            if method == "POST" and url == M.REMOTE_MCP["notion"]["url"]:
                return 401, {"WWW-Authenticate": 'Bearer resource_metadata="https://mcp.notion.com/.well-known/oauth-protected-resource"'}, b""
            if "oauth-protected-resource" in url:
                return 200, {}, json.dumps({"authorization_servers": ["https://mcp.notion.com"],
                                            "resource": "https://mcp.notion.com/mcp"}).encode()
            if "oauth-authorization-server" in url:
                return 200, {}, json.dumps({"authorization_endpoint": "https://mcp.notion.com/authorize",
                                            "token_endpoint": "https://mcp.notion.com/token",
                                            "registration_endpoint": "https://mcp.notion.com/register",
                                            "code_challenge_methods_supported": ["S256"]}).encode()
            if url.endswith("/register"):
                return 201, {}, json.dumps({"client_id": "ephemeral-cid", "token_endpoint_auth_method": "none"}).encode()
            if url.endswith("/token"):
                return 200, {}, json.dumps({"access_token": "AT", "refresh_token": "RT",
                                            "expires_in": 3600, "scope": "read"}).encode()
            return 404, {}, b""
        import nx_mcp_client as _cl
        class _FakeSess:
            def __init__(self, *a, **k): pass
            def initialize(self): return True   # connect() now verifies the MCP session
        with mock.patch.object(M, "_req", fake_req), \
             mock.patch.object(_cl, "MCPSession", _FakeSess), \
             mock.patch.object(M, "_kc_get", lambda s: kc.get(s)), \
             mock.patch.object(M, "_kc_set", lambda s, v: kc.__setitem__(s, v) or True), \
             mock.patch.object(M, "_run_loopback", lambda url, state, **k: "AUTHCODE"):
            res = M.connect("notion")
        self.assertTrue(res["ok"], res)
        self.assertEqual(res["name"], "Notion")
        # keys are per-user namespaced (nx-mcp-<uid>-notion-token) when a uid is present — use the real builders.
        self.assertIn(M._tok_key("notion"), kc)
        self.assertIn("AT", kc[M._tok_key("notion")])
        # ephemeral client_id was cached, never a shipped secret
        self.assertEqual(kc.get(M._client_key("notion")), "ephemeral-cid")

    def test_connect_fails_closed_if_mcp_endpoint_dead(self):
        # OAuth can succeed while the MCP endpoint 404s (wrong transport/path, the
        # /sse-vs-/mcp bug). connect() must NOT save a token or report connected —
        # else /connected shows "ready" and it fails the moment a tool is called.
        kc = {}
        def fake_req(url, method="GET", headers=None, data=None, timeout=15):
            if method == "POST" and url == M.REMOTE_MCP["notion"]["url"]:
                return 401, {"WWW-Authenticate": 'Bearer resource_metadata="https://mcp.notion.com/.well-known/oauth-protected-resource"'}, b""
            if "oauth-protected-resource" in url:
                return 200, {}, json.dumps({"authorization_servers": ["https://mcp.notion.com"], "resource": "https://mcp.notion.com/mcp"}).encode()
            if "oauth-authorization-server" in url:
                return 200, {}, json.dumps({"authorization_endpoint": "https://mcp.notion.com/authorize", "token_endpoint": "https://mcp.notion.com/token", "registration_endpoint": "https://mcp.notion.com/register", "code_challenge_methods_supported": ["S256"]}).encode()
            if url.endswith("/register"):
                return 201, {}, json.dumps({"client_id": "ephemeral-cid", "token_endpoint_auth_method": "none"}).encode()
            if url.endswith("/token"):
                return 200, {}, json.dumps({"access_token": "AT", "expires_in": 3600}).encode()
            return 404, {}, b""
        import nx_mcp_client as _cl
        class _DeadSess:
            def __init__(self, *a, **k): pass
            def initialize(self): raise Exception("initialize failed (http 404)")
        with mock.patch.object(M, "_req", fake_req), \
             mock.patch.object(_cl, "MCPSession", _DeadSess), \
             mock.patch.object(M, "_kc_get", lambda s: kc.get(s)), \
             mock.patch.object(M, "_kc_set", lambda s, v: kc.__setitem__(s, v) or True), \
             mock.patch.object(M, "_run_loopback", lambda url, state, **k: "AUTHCODE"):
            res = M.connect("notion")
        self.assertFalse(res["ok"])
        self.assertEqual(res["detail"], "mcp_unreachable")
        self.assertNotIn(M._tok_key("notion"), kc)   # no token saved for a dead endpoint

    def test_connect_unknown_service(self):
        self.assertEqual(M.connect("not-a-real-service")["detail"], "not_remote_mcp")

    def test_expanded_registry_is_sane(self):
        # 40+ live-verified remote MCP servers, all https, no placeholders.
        self.assertGreaterEqual(len(M.REMOTE_MCP), 40)
        for slug, e in M.REMOTE_MCP.items():
            self.assertTrue(e["url"].startswith("https://"), slug)
            self.assertNotRegex(e["url"], r"[<{]", f"{slug}: placeholder URL")
        for name in ("notion", "linear", "slack", "github", "vercel", "clickup", "monday-com"):
            self.assertIn(name, M.REMOTE_MCP)

    def test_menu_registry_matches_classification(self):
        reg = M.menu_registry()
        self.assertEqual(len(reg), len(M.REMOTE_MCP))
        self.assertEqual(reg["Notion"]["tier"], "dcr")
        self.assertEqual(reg["HubSpot"]["tier"], "token")
        self.assertEqual(reg["Notion"]["worlds"], ["cowork"])
        self.assertEqual(reg["GoHighLevel"]["worlds"], ["sales"])
        # the menu returns DISPLAY names — connect must resolve them
        for disp in ("Monday.com", "GoHighLevel", "Atlassian (Jira/Confluence)", "HubSpot"):
            self.assertTrue(M.is_remote_mcp(disp), f"{disp} must resolve from the menu")

    def test_aliases_resolve(self):
        self.assertEqual(M.get_server("jira")["name"], M.REMOTE_MCP["atlassian"]["name"])
        self.assertEqual(M.get_server("confluence")["name"], M.REMOTE_MCP["atlassian"]["name"])
        self.assertEqual(M.get_server("monday"), M.REMOTE_MCP["monday-com"])
        self.assertTrue(M.is_remote_mcp("hugging face"))

    def test_connected_slugs_reflects_keychain(self):
        # /connected and auto-connect's "already connected?" check call this. It
        # must surface BOTH pasted-token connects and DCR sign-ins (both land
        # under _tok_key). Roundtrip: absent -> save -> present -> disconnect.
        kc = {}
        with mock.patch.object(M, "_kc_get", lambda s: kc.get(s)), \
             mock.patch.object(M, "_kc_set", lambda s, v: kc.__setitem__(s, v) or True), \
             mock.patch.object(M, "_kc_delete", lambda s: kc.pop(s, None) is not None):
            self.assertNotIn("zapier", M.connected_slugs())
            M.save_token("zapier", {"access_token": "tk", "expires_in": 10 ** 9})
            self.assertIn("zapier", M.connected_slugs())
            M.disconnect("zapier")
            self.assertNotIn("zapier", M.connected_slugs())

    def test_expired_signin_still_listed_then_refreshed_on_use(self):
        # /connected is LOCAL: an expired sign-in with a refresh_token still counts
        # as connected, so earlier connections don't vanish after ~1h. The actual
        # refresh happens lazily when a tool is used — usable_token() mints a fresh
        # access token in place, with NO network during the listing.
        kc = {
            M._tok_key("notion"): json.dumps({
                "access_token": "OLD", "refresh_token": "RT", "expires_at": 1.0,
                "token_endpoint": "https://mcp.notion.com/token"}),
            M._client_key("notion"): "ephemeral-cid",
        }

        def fake_req(url, method="GET", headers=None, data=None, timeout=15):
            if url.endswith("/token") and "grant_type=refresh_token" in (data or ""):
                return 200, {}, json.dumps({"access_token": "NEW", "refresh_token": "RT2",
                                            "expires_in": 3600}).encode()
            raise AssertionError("listing must not hit the network")

        with mock.patch.object(M, "_req", fake_req), \
             mock.patch.object(M, "_kc_get", lambda s: kc.get(s)), \
             mock.patch.object(M, "_kc_set", lambda s, v: kc.__setitem__(s, v) or True):
            # listed with NO network (local check) — fake_req would raise if called
            self.assertTrue(M.is_connected("notion"))
            self.assertIn("notion", M.connected_slugs())
            # used -> refreshed in place
            self.assertEqual(M.usable_token("notion"), "NEW")
            rec = json.loads(kc[M._tok_key("notion")])
            self.assertEqual(rec["access_token"], "NEW")        # rotated in place
            self.assertGreater(rec["expires_at"], time.time())  # new lifetime

    def test_expired_without_refresh_token_is_not_connected(self):
        kc = {"nx-mcp-notion-token": json.dumps({"access_token": "OLD", "expires_at": 1.0})}
        with mock.patch.object(M, "_kc_get", lambda s: kc.get(s)):
            self.assertFalse(M.is_connected("notion"))          # expired, no way to revive
            self.assertIsNone(M.usable_token("notion"))

    def test_failed_refresh_on_use_fails_closed(self):
        # A refresh failure at use time returns None (no dead token sent) but keeps
        # the record for a later retry — not a surprise wipe / logout.
        kc = {"nx-mcp-notion-token": json.dumps({
            "access_token": "OLD", "refresh_token": "RT", "expires_at": 1.0,
            "token_endpoint": "https://mcp.notion.com/token"})}
        with mock.patch.object(M, "_req", lambda *a, **k: (400, {}, b'{"error":"invalid_grant"}')), \
             mock.patch.object(M, "_kc_get", lambda s: kc.get(s)), \
             mock.patch.object(M, "_kc_set", lambda s, v: kc.__setitem__(s, v) or True):
            self.assertIsNone(M.usable_token("notion"))         # fails closed
            self.assertIn("nx-mcp-notion-token", kc)            # ...record preserved
            self.assertEqual(json.loads(kc["nx-mcp-notion-token"])["refresh_token"], "RT")

    def test_cli_oauth_calls_all_resolve(self):
        # Guard against the silent-AttributeError class: nx_cli wraps its _mcpo
        # calls in try/except, so a missing function (e.g. connected_slugs)
        # vanishes invisibly and /connected silently shows nothing. Every
        # _mcpo.<fn> the CLI references must actually exist on nx_mcp_oauth.
        cli = open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                "nx_cli.py")).read()
        refs = set(re.findall(r"_mcpo\.(\w+)\s*\(", cli))
        self.assertIn("connected_slugs", refs)  # sanity: scanning the right alias
        for name in sorted(refs):
            self.assertTrue(hasattr(M, name),
                            f"nx_cli calls _mcpo.{name}() but nx_mcp_oauth has no such symbol")

    def test_no_secrets_in_source(self):
        # This module must never embed a provider secret — DCR is the whole point.
        src = open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                "nx_mcp_oauth.py")).read()
        for bad in ("client_secret\":", "secret=\"", "GOCSPX", "sk_live"):
            self.assertNotIn(bad, src)


if __name__ == "__main__":
    unittest.main()
