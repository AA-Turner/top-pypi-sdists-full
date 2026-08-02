"""Maddog batch 9 — new marketing channels (TikTok + Pinterest) as first-class
publishing connectors, alongside the existing Meta/Google/X/LinkedIn.
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import nx_channels as ch              # noqa: E402
import nx_integrations_directory as D  # noqa: E402


class NewChannelsRegistered(unittest.TestCase):
    def test_registry_has_tiktok_pinterest(self):
        self.assertIn("tiktok", ch.REGISTRY)
        self.assertIn("pinterest", ch.REGISTRY)

    def test_aliases_resolve_to_built_connectors(self):
        cases = {"tiktok": "TikTok", "pinterest": "Pinterest",
                 "instagram": "Meta", "facebook": "Meta", "youtube": "Google",
                 "twitter": "X", "x": "X", "linkedin": "LinkedIn"}
        for name, expect in cases.items():
            c = ch.connector_for_service(name)
            self.assertIsNotNone(c, f"{name} should resolve to a built connector")
            self.assertIn(expect.split()[0], c.display_name)

    def test_directory_marks_them_ready(self):
        self.assertIn("tiktok", D.BUILT_CONNECTORS)
        self.assertIn("pinterest", D.BUILT_CONNECTORS)
        for n in ("tiktok", "pinterest"):
            plan = D.resolve(n, world="cowork")
            self.assertEqual(plan["status"], "ready")
            self.assertEqual(plan["auth"], "oauth")


class ChannelOAuthShapes(unittest.TestCase):
    # TikTok moved to the bos-bridge model (Nexplora's own shared app, OAuth
    # server-side in nexplora-v2) — it no longer builds its own auth_url
    # locally. See tests/test_channels.py::BosBridgedChannelTests for the
    # current connect-flow coverage.

    def test_pinterest_auth_url(self):
        c = ch.connector_for_service("pinterest")
        u = c.auth_url("state123")
        self.assertTrue(u.startswith("https://www.pinterest.com/oauth"))
        self.assertIn("pins%3Awrite", u.replace(":", "%3A"))  # pins:write scope present


class PublicVsConfidentialAuth(unittest.TestCase):
    def setUp(self):
        # In-memory keychain so setup()/is_configured() work without a real Keychain backend
        # (no macOS `security` / Linux gnome-keyring in CI). Mirrors test_integrations_login.
        from unittest import mock
        self._kc = {}
        def fake_security(args, input_text=None):
            import types
            cp = types.SimpleNamespace(returncode=1, stdout="", stderr="")
            svc = args[args.index("-s") + 1] if "-s" in args else None
            op = args[0]
            if op == "find-generic-password" and svc in self._kc:
                cp.returncode = 0; cp.stdout = self._kc[svc] + "\n"
            elif op == "add-generic-password":
                wi = args.index("-w"); self._kc[svc] = args[wi + 1]; cp.returncode = 0
            elif op == "delete-generic-password":
                self._kc.pop(svc, None); cp.returncode = 0
            return cp
        p = mock.patch.object(ch, "_security", fake_security)
        p.start(); self.addCleanup(p.stop)

    def test_x_is_public_client_no_secret(self):
        x = ch.connector_for_service("x")
        self.assertIsInstance(x, ch._NexploraOAuthBridgedChannel)
        self.assertFalse(x.requires_secret)
        self.assertFalse(x.setup("CID_ONLY_TEST"))  # no parallel per-device vault
        self.assertTrue(x.is_configured())

    def test_confidential_channels_require_secret(self):
        for n in ("google", "pinterest", "tiktok"):
            c = ch.connector_for_service(n)
            self.assertTrue(c.requires_secret, f"{n} should need a secret")
            self.assertFalse(c.setup("CID"), f"{n} setup must reject id-only")


class MediaPublishIsHonest(unittest.TestCase):
    def test_tiktok_publish_never_fakes_success(self):
        # TikTok moved to the bos-bridge model — publish_text() was removed
        # along with the rest of the local OAuth path (no token ever lives
        # locally for it anymore). preflight() is the live honesty gate now:
        # never ok=True for "publish" until a server-side proxy exists.
        c = ch.connector_for_service("tiktok")
        pf = c.preflight("publish")
        self.assertFalse(pf["ok"])
        self.assertIn(pf["detail"], ("not_connected", "publish_not_wired_yet"))

    def test_pinterest_requires_image_and_board(self):
        c = ch.connector_for_service("pinterest")
        r = c.publish_text("a caption", image_url=None, board_id=None)
        self.assertFalse(r["ok"])
        self.assertIn(r["detail"], ("pinterest_requires_image_and_board", "not_connected", "not_configured"))


if __name__ == "__main__":
    unittest.main()
