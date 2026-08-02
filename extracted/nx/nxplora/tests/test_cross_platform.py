"""Cross-platform (Windows/Linux) secret-storage + surface guards — the 0.15.240 port.

macOS keeps its native `security`/Keychain path; every other platform routes the SAME
(account, service) contract through keyring (nx_keystore). These tests SIMULATE a non-mac
platform on the Mac CI box (patch sys.platform / nx_channels._IS_MAC) with an in-memory
fake keyring, so the Windows/Linux paths are exercised without a Windows machine:

  1. nx_keystore round-trips + validates names before touching keyring.
  2. nx_channels.kc_* route to keyring off-darwin (same values in/out).
  3. nx_key_pool._kc_read reads keyring off-darwin.
  4. iMessage is gated macOS-only with a clear error off-darwin.

Run: python3 -m unittest tests.test_cross_platform < /dev/null
"""
import os
import sys
import unittest
from unittest import mock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class _FakeKeyring:
    """Minimal in-memory stand-in for the `keyring` module (Credential Locker / Secret Service)."""
    def __init__(self):
        self.store = {}
    def get_password(self, service, username):
        return self.store.get((service, username))
    def set_password(self, service, username, password):
        self.store[(service, username)] = password
    def delete_password(self, service, username):
        if (service, username) in self.store:
            del self.store[(service, username)]
        else:
            raise KeyError("no such password")


class CrossPlatformKeystore(unittest.TestCase):
    def setUp(self):
        self._real_keyring = sys.modules.get("keyring")
        self.fake = _FakeKeyring()
        sys.modules["keyring"] = self.fake

    def tearDown(self):
        if self._real_keyring is not None:
            sys.modules["keyring"] = self._real_keyring
        else:
            sys.modules.pop("keyring", None)

    def test_keystore_roundtrip_and_validation(self):
        import nx_keystore
        self.assertTrue(nx_keystore.kr_set("nx-channels", "slack-token", "abc123"))
        self.assertEqual(nx_keystore.kr_get("nx-channels", "slack-token"), "abc123")
        self.assertTrue(nx_keystore.kr_delete("nx-channels", "slack-token"))
        self.assertIsNone(nx_keystore.kr_get("nx-channels", "slack-token"))
        # name validation: rejected before keyring is ever touched
        self.assertIsNone(nx_keystore.kr_get("bad name!", "x"))
        self.assertFalse(nx_keystore.kr_set("nx", "bad/slash", "v"))
        self.assertFalse(nx_keystore.kr_set("nx", "svc", None))

    def test_channels_kc_routes_to_keyring_off_mac(self):
        import nx_channels
        orig = nx_channels._IS_MAC
        nx_channels._IS_MAC = False   # simulate Windows/Linux
        try:
            self.assertTrue(nx_channels.kc_set("meta-token", "xyz789"))
            self.assertEqual(nx_channels.kc_get("meta-token"), "xyz789")
            # stored under the channels account namespace, keyed by service
            self.assertEqual(self.fake.store.get(("nx-channels", "meta-token")), "xyz789")
            self.assertTrue(nx_channels.kc_delete("meta-token"))
            self.assertIsNone(nx_channels.kc_get("meta-token"))
        finally:
            nx_channels._IS_MAC = orig

    def test_key_pool_reads_keyring_off_mac(self):
        self.fake.store[("nx", "nx-pool-1")] = "sk-pooled"
        import nx_key_pool
        with mock.patch.object(sys, "platform", "win32"):
            self.assertEqual(nx_key_pool._kc_read("nx-pool-1"), "sk-pooled")
            self.assertIsNone(nx_key_pool._kc_read("nx-pool-missing"))

    def test_imessage_gated_off_mac(self):
        try:
            import nx_cli
        except Exception as e:  # heavy import may be unavailable in a lean env
            self.skipTest(f"nx_cli import unavailable: {e}")
        with mock.patch.object(sys, "platform", "win32"):
            with self.assertRaises(RuntimeError):
                nx_cli._send_as_agent_imessage("+15551234567", "hi")


if __name__ == "__main__":
    unittest.main()
