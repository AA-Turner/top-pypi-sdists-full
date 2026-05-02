import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import cpsl


class IntegrationTests(unittest.TestCase):
    def test_outlook_helper_serializes_oauth_config_with_offline_access(self):
        config = cpsl.Outlook(
            client_id="client-id",
            client_secret="client-secret",
            scopes=["https://graph.microsoft.com/Mail.Read"],
        )

        data = config.to_dict()

        self.assertEqual(data["type"], cpsl.INTEGRATION_OUTLOOK)
        self.assertEqual(data["mode"], "oauth")
        self.assertEqual(data["client_id_secret"], "client-id")
        self.assertEqual(data["client_secret_secret"], "client-secret")
        self.assertEqual(data["scopes"], ["https://graph.microsoft.com/Mail.Read", "offline_access"])

    def test_outlook_helper_does_not_duplicate_offline_access(self):
        config = cpsl.Outlook(
            client_id="client-id",
            client_secret="client-secret",
            scopes=["offline_access", "https://graph.microsoft.com/Mail.Read"],
        )

        self.assertEqual(
            config.to_dict()["scopes"],
            ["offline_access", "https://graph.microsoft.com/Mail.Read"],
        )

    def test_outlook_is_exported_as_builtin_integration(self):
        self.assertEqual(cpsl.Integration.OUTLOOK.value, "outlook")
        self.assertEqual(cpsl.INTEGRATION_OUTLOOK, "outlook")


if __name__ == "__main__":
    unittest.main()
