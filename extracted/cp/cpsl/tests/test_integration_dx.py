import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import cpsl
from cpsl.integration import MODE_SECRET
from cpsl.session import Session, SessionChannel, UserInfo


class IntegrationDXTests(unittest.TestCase):
    def test_constructor_serializes_oauth_config(self):
        cfg = cpsl.GitHub(
            client_id=cpsl.Secret.from_name("GITHUB_CLIENT_ID"),
            client_secret=cpsl.Secret.from_name("GITHUB_CLIENT_SECRET"),
            scopes=["repo"],
        )

        self.assertEqual(
            cfg.to_dict(),
            {
                "type": "github",
                "mode": "oauth",
                "scopes": ["repo"],
                "client_id_secret": "GITHUB_CLIENT_ID",
                "client_secret_secret": "GITHUB_CLIENT_SECRET",
            },
        )

    def test_constructor_serializes_secret_config(self):
        self.assertEqual(
            cpsl.AWS().to_dict(),
            {
                "type": "aws",
                "mode": MODE_SECRET,
                "fields": ["access_key_id", "secret_access_key", "region"],
            },
        )

    def test_app_add_integration_accepts_config_and_string(self):
        app = cpsl.App(name="integration-dx", image=cpsl.Image())
        app.add_integration(cpsl.AWS())
        app.add_integration(
            "github",
            client_id=cpsl.Secret.from_name("GITHUB_CLIENT_ID"),
            client_secret=cpsl.Secret.from_name("GITHUB_CLIENT_SECRET"),
            scopes=["repo"],
        )

        app._finalize_config()
        self.assertEqual([i["type"] for i in app._cpsl_config["integrations"]], ["aws", "github"])

    def test_session_get_integration_accepts_enum_config_and_string(self):
        cred = cpsl.IntegrationCredentials(access_token="tok")
        session = Session(
            id="sess-1",
            user=UserInfo(id="user-1"),
            channel=SessionChannel(type="chat"),
            integrations={"github": cred},
        )
        self.assertIs(session.get_integration("github"), cred)
        self.assertIs(session.get_integration(cpsl.Integration.GITHUB), cred)
        self.assertIs(
            session.get_integration(cpsl.GitHub(client_id="id", client_secret="secret")), cred
        )


if __name__ == "__main__":
    unittest.main()
