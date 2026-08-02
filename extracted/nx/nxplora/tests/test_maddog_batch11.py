"""Maddog batch 11 — NX⇄Nexplora credential-vault sync (one account).

A connect in the CLI pushes to the Nexplora vault; login pulls the vault into the local
Keychain cache. Everything FAILS OPEN (no-op when signed out / offline / endpoint absent),
so shipping it before the backend deploy is safe.
"""
import json
import os
import sys
import unittest
from unittest import mock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import nx_vault_sync as V  # noqa: E402


class FailsOpen(unittest.TestCase):
    def test_endpoint_resolves(self):
        self.assertTrue(V._endpoint().endswith("/api/cli/credentials"))

    def test_signed_out_is_noop(self):
        with mock.patch.object(V, "_token", lambda: ""):
            self.assertFalse(V.enabled())
            self.assertFalse(V.push("linear", {"access_token": "x"}))
            self.assertEqual(V.pull_into_keychain(), 0)

    def test_endpoint_unreachable_is_noop(self):
        # token present but the POST raises (e.g. 404 not-deployed) → fail open, no raise
        with mock.patch.object(V, "_token", lambda: "tok"), \
             mock.patch.object(V, "_req", side_effect=Exception("404")):
            self.assertFalse(V.push("linear", {"access_token": "x"}))


class PushShape(unittest.TestCase):
    def test_push_body_is_correct(self):
        captured = {}
        def fake_req(method, url, tok, body=None, timeout=8):
            captured.update(method=method, url=url, tok=tok, body=body)
            return 200, {"ok": True}
        with mock.patch.object(V, "_token", lambda: "TOK"), \
             mock.patch.object(V, "_req", fake_req):
            ok = V.push("Linear", {"access_token": "abc", "scope": "read write"})
        self.assertTrue(ok)
        self.assertEqual(captured["method"], "POST")
        self.assertEqual(captured["tok"], "TOK")
        self.assertEqual(captured["body"]["provider"], "linear")     # lowercased
        self.assertEqual(captured["body"]["value"], "abc")
        self.assertEqual(captured["body"]["scopes"], ["read", "write"])
        self.assertEqual(captured["body"]["credentialType"], "oauth_access_token")

    def test_public_record_not_pushed(self):
        with mock.patch.object(V, "_token", lambda: "TOK"), \
             mock.patch.object(V, "_req", side_effect=AssertionError("should not POST")):
            self.assertFalse(V.push("deepwiki", {"public": True}))
            self.assertFalse(V.push("x", {}))   # no access_token


class PullReconciles(unittest.TestCase):
    def test_pull_writes_vault_tokens_to_keychain(self):
        calls = iter([
            (200, {"ok": True, "connections": [{"provider": "linear"}, {"provider": "notion"}]}),
            (200, {"value": "lin-tok"}),
            (200, {"value": "not-tok"}),
        ])
        written = {}
        import nx_mcp_oauth as O
        with mock.patch.object(V, "_token", lambda: "TOK"), \
             mock.patch.object(V, "_req", lambda *a, **k: next(calls)), \
             mock.patch.object(O, "_kc_set", lambda k, v: written.__setitem__(k, v) or True), \
             mock.patch.object(O, "_current_uid", lambda: ""):
            n = V.pull_into_keychain()
        self.assertEqual(n, 2)
        self.assertIn("nx-mcp-linear-token", written)
        self.assertEqual(json.loads(written["nx-mcp-linear-token"])["access_token"], "lin-tok")


class SaveTokenStillPushes(unittest.TestCase):
    def test_save_token_calls_push_best_effort(self):
        import nx_mcp_oauth as O
        pushed = {}
        with mock.patch.object(O, "_kc_set", lambda k, v: True), \
             mock.patch.object(V, "push", lambda slug, rec: pushed.update(slug=slug) or True):
            O.save_token("linear", {"access_token": "t", "expires_in": 3600})
        self.assertEqual(pushed.get("slug"), "linear")   # connect → vault push wired


if __name__ == "__main__":
    unittest.main()
