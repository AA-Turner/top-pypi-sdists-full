"""Maddog batch 12 — NX cloud-gate dispatch (NX runs the whole business OS).

NX dispatches actions across 32 packs (marketing/sales/leads/finance/hr/…), each
evaluate → operator approval → execute, behind the backend's cost/approval gates.
Fails open with a clear reason when signed out / endpoint absent.
"""
import os
import sys
import unittest
from unittest import mock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import nx_cloud_dispatch as CD  # noqa: E402


class PacksAndBase(unittest.TestCase):
    def test_full_business_os_surface(self):
        for p in ("nx-marketing", "nx-sales", "nx-leads", "nx-finance", "nx-hr", "nx-growth"):
            self.assertIn(p, CD.PACKS)
        self.assertGreaterEqual(len(CD.PACKS), 30)

    def test_action_url(self):
        with mock.patch.object(CD, "_base", lambda: "https://api.nexplora.ai"):
            self.assertEqual(CD._action_url("nx-sales", "evaluate"),
                             "https://api.nexplora.ai/api/nx-sales/actions/evaluate")


class FailsOpen(unittest.TestCase):
    def test_signed_out_evaluate_is_clear(self):
        with mock.patch.object(CD, "_token", lambda: ""):
            r = CD.evaluate("nx-marketing", "draft_campaign", "launch v0.1")
            self.assertFalse(r["ok"])
            self.assertIn("not_signed_in", r["error"])

    def test_no_workspace_is_clear(self):
        with mock.patch.object(CD, "_token", lambda: "TOK"), \
             mock.patch.object(CD, "_base", lambda: "https://api.nexplora.ai"), \
             mock.patch.object(CD, "workspace_id", lambda: ""):
            r = CD.evaluate("nx-sales", "draft_sequence", "outbound to acme")
            self.assertFalse(r["ok"])
            self.assertIn("no_workspace", r["error"])


class EvaluateExecute(unittest.TestCase):
    def test_evaluate_posts_workspace_and_action(self):
        captured = {}
        def fake_req(method, url, tok, body=None, timeout=20):
            captured.update(method=method, url=url, body=body)
            return 200, {"ok": True, "request_id": "req1",
                         "gate": {"display_tag": "APPROVE", "action_label": "Draft campaign"},
                         "display_tag": "[APPROVE] Draft campaign"}
        with mock.patch.object(CD, "_token", lambda: "TOK"), \
             mock.patch.object(CD, "_base", lambda: "https://api.nexplora.ai"), \
             mock.patch.object(CD, "workspace_id", lambda: "ws-1"), \
             mock.patch.object(CD, "_req", fake_req):
            r = CD.evaluate("nx-marketing", "draft_campaign", "launch v0.1", run_id="run9")
        self.assertTrue(r["ok"])
        self.assertEqual(r["request_id"], "req1")
        self.assertTrue(captured["url"].endswith("/api/nx-marketing/actions/evaluate"))
        self.assertEqual(captured["body"]["workspace_id"], "ws-1")
        self.assertEqual(captured["body"]["action_id"], "draft_campaign")
        self.assertEqual(captured["body"]["requested_action"], "launch v0.1")

    def test_execute_approves_then_executes(self):
        urls = []
        def fake_req(method, url, tok, body=None, timeout=20):
            urls.append(url)
            return 200, {"ok": True, "decision": "EXECUTED"}
        with mock.patch.object(CD, "_token", lambda: "TOK"), \
             mock.patch.object(CD, "_base", lambda: "https://api.nexplora.ai"), \
             mock.patch.object(CD, "workspace_id", lambda: "ws-1"), \
             mock.patch.object(CD, "_req", fake_req):
            r = CD.execute("nx-sales", "send_sequence", "outbound", "run9", seed_approval=True)
        self.assertTrue(r["ok"])
        self.assertTrue(any(u.endswith("/actions/approve") for u in urls))   # approve first
        self.assertTrue(any(u.endswith("/actions/execute") for u in urls))   # then execute


class WorkspaceResolution(unittest.TestCase):
    def test_workspace_fetched_from_vault_when_uncached(self):
        with mock.patch.object(CD, "_cfg", lambda: {}), \
             mock.patch.object(CD, "_save_cfg", lambda c: True), \
             mock.patch.object(CD, "_token", lambda: "TOK"), \
             mock.patch.object(CD, "_base", lambda: "https://api.nexplora.ai"), \
             mock.patch.object(CD, "_req", lambda *a, **k: (200, {"ok": True, "workspace_id": "ws-from-vault"})):
            self.assertEqual(CD.workspace_id(), "ws-from-vault")


if __name__ == "__main__":
    unittest.main()
