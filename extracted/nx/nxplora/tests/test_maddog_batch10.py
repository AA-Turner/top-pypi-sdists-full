"""Maddog batch 10 — user_id-namespaced credentials (one-account foundation).

Connections are now keyed by the signed-in Nexplora user_id so two accounts on the
SAME Mac never share creds (the long-flagged isolation gap), with migrate-on-read so
pre-namespacing connections are never lost. This is the prerequisite for the NX<->Nexplora
credential-vault sync (one business, one account).
"""
import os
import sys
import unittest
from unittest import mock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import nx_mcp_oauth as O  # noqa: E402


class KeyNamespacing(unittest.TestCase):
    def test_signed_out_uses_legacy_slug_only_key(self):
        with mock.patch.object(O, "_current_uid", lambda: ""):
            self.assertEqual(O._tok_key("linear"), "nx-mcp-linear-token")
            self.assertEqual(O._client_key("linear"), "nx-mcp-linear-client")

    def test_signed_in_namespaces_by_user(self):
        with mock.patch.object(O, "_current_uid", lambda: "user-abc"):
            self.assertEqual(O._tok_key("linear"), "nx-mcp-user-abc-linear-token")
            self.assertEqual(O._client_key("linear"), "nx-mcp-user-abc-linear-client")
        # legacy key is always the slug-only form (for migration lookups)
        self.assertEqual(O._legacy_tok_key("linear"), "nx-mcp-linear-token")

    def test_two_users_do_not_collide(self):
        with mock.patch.object(O, "_current_uid", lambda: "alice"):
            ka = O._tok_key("notion")
        with mock.patch.object(O, "_current_uid", lambda: "bob"):
            kb = O._tok_key("notion")
        self.assertNotEqual(ka, kb)   # the flagged same-Mac collision is fixed


class MigrateOnRead(unittest.TestCase):
    def test_legacy_connection_is_found_and_migrated_forward(self):
        store = {"nx-mcp-linear-token": '{"access_token":"legacy-tok"}'}  # pre-namespacing

        def kc_get(k): return store.get(k)
        def kc_set(k, v): store[k] = v; return True
        with mock.patch.object(O, "_current_uid", lambda: "user-x"), \
             mock.patch.object(O, "_kc_get", kc_get), \
             mock.patch.object(O, "_kc_set", kc_set):
            tok = O.load_token("linear")
        self.assertEqual(tok["access_token"], "legacy-tok")        # found via fallback
        self.assertIn("nx-mcp-user-x-linear-token", store)         # migrated forward
        self.assertEqual(O._json(store["nx-mcp-user-x-linear-token"])["access_token"], "legacy-tok")

    def test_signed_out_no_migration_just_legacy(self):
        store = {"nx-mcp-linear-token": '{"access_token":"t"}'}
        with mock.patch.object(O, "_current_uid", lambda: ""), \
             mock.patch.object(O, "_kc_get", lambda k: store.get(k)):
            self.assertEqual(O.load_token("linear")["access_token"], "t")


class DisconnectClearsBoth(unittest.TestCase):
    def test_disconnect_deletes_namespaced_and_legacy(self):
        deleted = []
        with mock.patch.object(O, "_current_uid", lambda: "user-x"), \
             mock.patch.object(O, "_kc_delete", lambda k: deleted.append(k) or True):
            O.disconnect("linear")
        self.assertIn("nx-mcp-user-x-linear-token", deleted)   # namespaced
        self.assertIn("nx-mcp-linear-token", deleted)          # legacy too


if __name__ == "__main__":
    unittest.main()
