import json
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import cpsl
from cpsl.clients.capsule import IntegrationCredential, PipedreamProxyResponse
from cpsl.integration import MODE_SECRET
from cpsl.runner.shared import _parse_integration_credential
from cpsl.session import Session, SessionChannel, UserInfo


class FakePipedreamStub:
    def __init__(self):
        self.requests = []

    def pipedream_proxy(self, req):
        self.requests.append(req)
        return PipedreamProxyResponse(
            status_code=200,
            headers={"Content-Type": "application/json"},
            body=b'{"ok":true}',
        )


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

    def test_pipedream_constructor_uses_platform_environment_by_default(self):
        self.assertEqual(
            cpsl.Pipedream("gmail").to_dict(),
            {
                "type": "gmail",
                "mode": "pipedream",
                "fields": [],
            },
        )

    def test_pipedream_constructor_serializes_explicit_environment(self):
        self.assertEqual(
            cpsl.Pipedream("gmail", environment="production").to_dict(),
            {
                "type": "gmail",
                "mode": "pipedream",
                "fields": ["environment:production"],
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

    def test_pipedream_payload_exposes_access_token_and_metadata(self):
        payload = {
            "provider": "pipedream",
            "account_id": "apn_123",
            "app_slug": "gmail",
            "access_token": "google-access-token",
            "token_type": "Bearer",
            "expires_at": "1800000000",
        }
        cred = _parse_integration_credential(
            IntegrationCredential(
                type="gmail",
                access_token=json.dumps(payload),
                token_type="pipedream",
                scopes=["https://www.googleapis.com/auth/gmail.readonly"],
                expires_at=1800000000,
            )
        )

        self.assertEqual(cred.access_token, "google-access-token")
        self.assertEqual(cred.token_type, "Bearer")
        self.assertEqual(cred.expires_at, 1800000000)
        self.assertEqual(cred.fields["account_id"], "apn_123")
        self.assertEqual(cred.fields["app_slug"], "gmail")

    def test_session_pipedream_returns_requests_like_proxy(self):
        stub = FakePipedreamStub()
        session = Session(
            id="sess-1",
            user=UserInfo(id="user-hash", email="viewer@example.com", org_id="org-1"),
            channel=SessionChannel(type="chat"),
        )
        session._session_stub = stub
        session._app_id = "app-1"

        proxy = session.pipedream("gmail")
        response = proxy.post(
            "https://gmail.googleapis.com/gmail/v1/users/me/messages/send",
            params={"uploadType": "media"},
            json={"raw": "abc"},
        )

        self.assertEqual(response.json(), {"ok": True})
        self.assertEqual(len(stub.requests), 1)
        req = stub.requests[0]
        self.assertEqual(req.app_id, "app-1")
        self.assertEqual(req.user_email, "viewer@example.com")
        self.assertEqual(req.owner_id, "org:org-1")
        self.assertEqual(req.integration_type, "gmail")
        self.assertEqual(req.method, "POST")
        self.assertEqual(
            req.url,
            "https://gmail.googleapis.com/gmail/v1/users/me/messages/send?uploadType=media",
        )
        self.assertEqual(req.headers["Content-Type"], "application/json")
        self.assertEqual(req.body, b'{"raw":"abc"}')


if __name__ == "__main__":
    unittest.main()
