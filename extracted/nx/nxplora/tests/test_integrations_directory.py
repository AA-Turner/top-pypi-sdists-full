"""
test_integrations_directory.py — maddog suite for the integration resolver ladder.

Intent: prove the resolver (a) climbs directory -> mcp_registry -> discoverable
-> bring_your_own correctly, (b) NEVER reports an install/connect as done (it
returns a PLAN), and (c) every step that would install software is
approval-gated. Honest no-ceilings extensibility.

Run: python3 -m unittest tests.test_integrations_directory
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import nx_integrations_directory as D  # noqa: E402


class ResolverLadderTests(unittest.TestCase):
    def test_built_connector_is_ready(self):
        for q in ("meta", "facebook", "instagram"):
            with self.subTest(q=q):
                p = D.resolve(q)
                self.assertEqual(p["status"], "ready")
                self.assertEqual(p["connector"], "meta")
                self.assertIn("/publish connect meta", p["steps"][0])

    def test_directory_oauth_requires_approval(self):
        p = D.resolve("Salesforce")
        self.assertEqual(p["status"], "directory")
        self.assertEqual(p["auth"], "oauth")
        self.assertTrue(p["requires_approval"])

    def test_directory_api_key(self):
        p = D.resolve("Stripe")
        self.assertEqual(p["status"], "directory")
        self.assertEqual(p["auth"], "api_key")
        self.assertTrue(p["requires_approval"])

    def test_mcp_registry_hit_offers_gated_install(self):
        # not curated, but the (injected) MCP registry knows it
        p = D.resolve("obscuretool", mcp_lookup=lambda n: {"slug": "obscuretool"})
        self.assertEqual(p["status"], "mcp_registry")
        self.assertTrue(p["requires_approval"])
        self.assertTrue(any("install" in s for s in p["steps"]))

    def test_discoverable_web_search_path_is_gated(self):
        p = D.resolve("somenewsaas", mcp_lookup=lambda n: None, web_search_available=True)
        self.assertEqual(p["status"], "discoverable")
        self.assertTrue(p["requires_approval"])
        self.assertTrue(any("web-search" in s for s in p["steps"]))

    def test_bring_your_own_when_nothing_found(self):
        p = D.resolve("totallyunknownx", mcp_lookup=lambda n: None, web_search_available=False)
        self.assertEqual(p["status"], "bring_your_own")
        self.assertIn("Bring your own", p["message"])

    def test_empty_name_is_honest(self):
        p = D.resolve("")
        self.assertEqual(p["status"], "bring_your_own")

    def test_resolver_never_executes_only_plans(self):
        # Every install/connect path must be approval-gated; the resolver returns
        # strings (a plan), never a side effect.
        for q, lookup, web in [
            ("somenewsaas", lambda n: None, True),       # discoverable
            ("obscuretool", lambda n: {"slug": "x"}, True),  # mcp_registry
            ("Salesforce", None, True),                   # directory oauth
        ]:
            with self.subTest(q=q):
                p = D.resolve(q, mcp_lookup=lookup, web_search_available=web)
                self.assertTrue(p["requires_approval"],
                                f"{p['status']} must be approval-gated")
                self.assertIsInstance(p["steps"], list)


class DirectoryTests(unittest.TestCase):
    def test_directory_for_world_returns_real_set(self):
        sales = D.directory_for("sales")
        self.assertGreaterEqual(len(sales), 5)
        names = [i.name for i in sales]
        self.assertIn("Salesforce", names)

    def test_merge_does_not_clobber_built_connector(self):
        before = D.find_in_directory("meta")
        self.assertIsNotNone(before)
        self.assertEqual(before[1].connector, "meta")
        # merge a generated 'marketing' set that re-lists Meta without a connector
        D.merge_directory({"marketing": [
            {"name": "Meta (Facebook + Instagram)", "category": "Channel", "auth": "oauth", "is_mcp": False},
            {"name": "Reddit Ads", "category": "Ads", "auth": "oauth", "is_mcp": False},
        ]})
        # Meta still carries its built connector (not clobbered)
        after = D.find_in_directory("meta")
        self.assertEqual(after[1].connector, "meta")
        # the new one was added
        self.assertIsNotNone(D.find_in_directory("Reddit Ads"))

    def test_merge_adds_new_world(self):
        D.merge_directory({"legal": [
            {"name": "Ironclad", "category": "CLM", "auth": "oauth", "is_mcp": False},
        ]})
        self.assertIsNotNone(D.find_in_directory("Ironclad"))


if __name__ == "__main__":
    unittest.main()
