import os
import unittest
from types import SimpleNamespace
from unittest.mock import patch
from flask import Flask
from hugpy_core.web import api_access


class ConsoleInferenceAuth(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.before_request(api_access.enforce_api_key_mode)
        self.app.add_url_rule('/api/v1/models', 'console', lambda: {'ok': True})
        self.app.add_url_rule('/v1/models', 'sdk', lambda: {'ok': True})
        self.client = self.app.test_client()
        self.env = patch.dict(os.environ, {'HUGPY_CONSOLE_PROXY_ADDRS': '127.0.0.1,192.168.1.100'})
        self.keys = patch.object(api_access.routing, 'KEYS', SimpleNamespace(
            check=lambda *_: (401, {'error': 'API key required'})))
        self.env.start(); self.keys.start()

    def tearDown(self):
        self.keys.stop(); self.env.stop()

    def request(self, path='/api/v1/models', peer='127.0.0.1', marker=True):
        return self.client.get(path, environ_base={'REMOTE_ADDR': peer},
            headers={'X-Hugpy-Console-Authenticated': '1'} if marker else {})

    def test_verified_console_alias_uses_existing_session(self):
        self.assertEqual(self.request().status_code, 200)

    def test_public_sdk_endpoint_still_needs_its_api_key(self):
        self.assertEqual(self.request('/v1/models').status_code, 401)

    def test_arbitrary_client_cannot_assert_a_verified_session(self):
        self.assertEqual(self.request(peer='203.0.113.9').status_code, 401)

    def test_alias_without_proxy_verification_still_needs_authentication(self):
        self.assertEqual(self.request(marker=False).status_code, 401)


if __name__ == '__main__':
    unittest.main()
