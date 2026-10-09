import unittest
import uuid
from unittest.mock import patch

from rentdynamics.client import Client


class ClientTests(unittest.TestCase):
    def test_when_development_is_false_you_get_production_url(self):
        client = Client()
        base_url = client.get_base_url()
        self.assertEqual(base_url, 'https://api.rentdynamics.com')

    def test_when_development_is_false_with_alternate_base_url(self):
        base_url = str(uuid.uuid4())[:20]
        client = Client(base_url=base_url)
        url = client.get_base_url()
        self.assertEqual(url, base_url)

    def test_when_development_is_true_you_get_development_url(self):
        client = Client(development=True)
        base_url = client.get_base_url()
        self.assertEqual(base_url, 'https://api.rentdynamics.dev')

    def test_when_development_is_true_with_alternate_base_url(self):
        base_url = str(uuid.uuid4())[:20]
        client = Client(base_development_url=base_url, development=True)
        url = client.get_base_url()
        self.assertEqual(url, base_url)

    @patch.object(Client, 'get_timestamp_milliseconds', return_value=123456789)
    def test_existing_signature_and_token_headers(self, mock_timestamp):
        client = Client(api_key='api-key', api_secret='api-secret')
        client.auth_token = 'legacy-token'

        headers = client.get_headers('/endpoint', body={'value': 1})

        self.assertEqual(headers, {
            'x-rd-timestamp': '123456789',
            'x-rd-api-nonce': client.get_nonce('123456789', '/endpoint', {'value': 1}),
            'x-rd-api-key': 'api-key',
            'AUTHORIZATION': 'Token legacy-token',
        })
